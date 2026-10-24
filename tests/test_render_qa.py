"""Render QA gate on tiny synthetic fixtures, generated here and never committed."""

import os
import shutil
import subprocess

import pytest

from panelweaver.qa.render import RenderProfile, check_render

if shutil.which("ffmpeg") is None:
    if os.environ.get("PW_REQUIRE_FFMPEG"):
        raise RuntimeError("ffmpeg is required (PW_REQUIRE_FFMPEG is set)")
    pytest.skip("ffmpeg not installed", allow_module_level=True)

TINY = RenderProfile(width=320, height=180)
# A stereo 997 Hz tone at amplitude 0.158 measures about -16 LUFS.
TONE = "{a}*sin(2*PI*997*t)"


def make(path, *, vf="null", af="anull", amp=0.158, size="320x180", seconds=4):
    tone = TONE.format(a=amp)
    subprocess.run(
        [
            "ffmpeg", "-v", "error", "-y",
            "-f", "lavfi", "-i", f"testsrc2=size={size}:rate=30:duration={seconds}",
            "-f", "lavfi", "-i", f"aevalsrc={tone}|{tone}:s=48000:d={seconds}",
            "-vf", vf, "-af", af,
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
            str(path),
        ],
        check=True,
    )  # fmt: skip
    return path


def failed(report):
    return {c.name for c in report.checks if not c.passed}


def test_clean_fixture_passes(tmp_path):
    report = check_render(make(tmp_path / "ok.mp4"), TINY)
    assert report.passed, report.model_dump_json(indent=2)


def test_black_gap_fails(tmp_path):
    video = make(tmp_path / "black.mp4", vf="drawbox=t=fill:c=black:enable='between(t,1.5,2.5)'")
    assert failed(check_render(video, TINY)) == {"black frames (T5)"}


def test_silence_gap_fails(tmp_path):
    video = make(tmp_path / "silent.mp4", af="volume=enable='between(t,1,2.9)':volume=0")
    assert "unintended silence (A3)" in failed(check_render(video, TINY))


def test_loud_audio_fails(tmp_path):
    video = make(tmp_path / "loud.mp4", amp=0.9)
    assert failed(check_render(video, TINY)) == {"loudness (A1)", "true peak (A2)"}


def test_wrong_size_fails(tmp_path):
    video = make(tmp_path / "small.mp4", size="160x90")
    assert failed(check_render(video, TINY)) == {"video format"}
