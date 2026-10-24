"""Render QA gate (register measure 8, C-09, C-10).

Checks a rendered MP4 against docs/SUCCESS_CRITERIA.md: output format (§1.7),
decode errors (T6), black frames (T5), audio/video duration (T4), loudness
(A1, A2) and unintended silence (A3). ffprobe plus one ffmpeg decode pass.
"""

from __future__ import annotations

import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

from pydantic import BaseModel


class RenderProfile(BaseModel):
    width: int = 1920
    height: int = 1080
    fps: Fraction = Fraction(30)
    vcodec: str = "h264"
    pix_fmt: str = "yuv420p"
    acodec: str = "aac"
    sample_rate: int = 48000
    channels: int = 2
    lufs: float = -16.0
    lufs_tolerance: float = 1.0
    true_peak_max: float = -1.5
    black_min_s: float = 0.3
    black_pix_th: float = 0.05
    silence_db: float = -45.0
    silence_min_s: float = 1.5


PROFILES = {
    "final": RenderProfile(),
    "preview": RenderProfile(width=960, height=540),
}


class Check(BaseModel):
    name: str
    passed: bool
    detail: str


class QAReport(BaseModel):
    path: str
    passed: bool
    checks: list[Check]


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def probe(path: Path) -> dict:
    out = _run(
        [
            "ffprobe", "-v", "error", "-of", "json",
            "-show_entries",
            "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,"
            "pix_fmt,sample_rate,channels,duration",
            str(path),
        ]
    )  # fmt: skip
    if out.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {out.stderr.strip()}")
    return json.loads(out.stdout)


_BLACK = re.compile(r"black_start:\s*([\d.]+)\s+black_end:\s*([\d.]+)")
_SIL_START = re.compile(r"silence_start:\s*(-?[\d.]+)")
_SIL_END = re.compile(r"silence_end:\s*([\d.]+)")
_LOUD = re.compile(r'"(input_i|input_tp|input_lra)"\s*:\s*"(-?[\d.]+|-?inf)"')


def _edge(start: float, end: float, duration: float, eps: float = 0.05) -> bool:
    """Touches the start or the end of the video: a planned fade, not a dead gap."""
    return start <= eps or end >= duration - eps


def check_render(path: Path, profile: RenderProfile) -> QAReport:
    checks: list[Check] = []
    info = probe(path)
    duration = float(info["format"]["duration"])
    video = next((s for s in info["streams"] if s["codec_type"] == "video"), None)
    audio = next((s for s in info["streams"] if s["codec_type"] == "audio"), None)

    if video is None:
        checks.append(Check(name="video stream", passed=False, detail="missing"))
    else:
        got = (
            f"{video['width']}x{video['height']} {video['codec_name']} {video['pix_fmt']} "
            f"{Fraction(video['r_frame_rate'])} fps"
        )
        ok = (
            video["width"] == profile.width
            and video["height"] == profile.height
            and video["codec_name"] == profile.vcodec
            and video["pix_fmt"] == profile.pix_fmt
            and Fraction(video["r_frame_rate"]) == profile.fps
        )
        checks.append(Check(name="video format", passed=ok, detail=got))

    if audio is None:
        checks.append(Check(name="audio stream", passed=False, detail="missing"))
    else:
        got = f"{audio['codec_name']} {audio['sample_rate']} Hz {audio['channels']} ch"
        ok = (
            audio["codec_name"] == profile.acodec
            and int(audio["sample_rate"]) == profile.sample_rate
            and audio["channels"] == profile.channels
        )
        checks.append(Check(name="audio format", passed=ok, detail=got))

    if video is not None and audio is not None:
        # One video frame, plus one AAC frame of encoder padding.
        tolerance = float(1 / profile.fps) + 1024 / profile.sample_rate
        diff = abs(float(video["duration"]) - float(audio["duration"]))
        checks.append(
            Check(
                name="A/V duration (T4)",
                passed=diff <= tolerance,
                detail=f"differ by {diff * 1000:.0f} ms (limit {tolerance * 1000:.0f} ms)",
            )
        )

    args = ["ffmpeg", "-hide_banner", "-nostats", "-loglevel", "level+info", "-i", str(path)]
    if video is not None:
        args += ["-vf", f"blackdetect=d={profile.black_min_s}:pix_th={profile.black_pix_th}"]
    if audio is not None:
        args += [
            "-af",
            f"silencedetect=noise={profile.silence_db}dB:d={profile.silence_min_s},"
            f"loudnorm=I={profile.lufs}:LRA=9:TP={profile.true_peak_max}:print_format=json",
        ]
    args += ["-f", "null", "-"]
    log = _run(args).stderr

    errors = [ln for ln in log.splitlines() if "[error]" in ln or "[fatal]" in ln]
    checks.append(
        Check(
            name="decode errors (T6)",
            passed=not errors,
            detail=f"{len(errors)} error lines" + (f": {errors[0].strip()}" if errors else ""),
        )
    )

    if video is not None:
        blacks = [(float(a), float(b)) for a, b in _BLACK.findall(log)]
        gaps = [b for b in blacks if not _edge(*b, duration)]
        checks.append(
            Check(
                name="black frames (T5)",
                passed=not gaps,
                detail=", ".join(f"{a:.2f}-{b:.2f}s" for a, b in gaps) or "none mid-video",
            )
        )

    if audio is not None:
        starts = [max(0.0, float(s)) for s in _SIL_START.findall(log)]
        ends = [float(e) for e in _SIL_END.findall(log)]
        ends += [duration] * (len(starts) - len(ends))  # silence that runs to the end
        silences = [(s, e) for s, e in zip(starts, ends, strict=True) if not _edge(s, e, duration)]
        checks.append(
            Check(
                name="unintended silence (A3)",
                passed=not silences,
                detail=", ".join(f"{a:.2f}-{b:.2f}s" for a, b in silences) or "none mid-video",
            )
        )

        loud = dict(_LOUD.findall(log))
        if "input_i" in loud and "input_tp" in loud:
            i, tp = float(loud["input_i"]), float(loud["input_tp"])
            checks.append(
                Check(
                    name="loudness (A1)",
                    passed=abs(i - profile.lufs) <= profile.lufs_tolerance,
                    detail=f"{i:.1f} LUFS (target {profile.lufs} +/- {profile.lufs_tolerance})",
                )
            )
            checks.append(
                Check(
                    name="true peak (A2)",
                    passed=tp <= profile.true_peak_max,
                    detail=f"{tp:.1f} dBTP (max {profile.true_peak_max})",
                )
            )
        else:
            checks.append(Check(name="loudness (A1)", passed=False, detail="no loudnorm output"))

    return QAReport(path=str(path), passed=all(c.passed for c in checks), checks=checks)
