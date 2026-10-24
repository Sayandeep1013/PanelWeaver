"""Scoring functions behind docs/SUCCESS_CRITERIA.md (U1-U5, V2-V5)."""

from __future__ import annotations

import statistics
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass

Box = tuple[float, float, float, float]  # x0, y0, x1, y1


def iou(a: Box, b: Box) -> float:
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    union = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / union if union > 0 else 0.0


@dataclass(frozen=True)
class DetectionScore:
    precision: float
    recall: float
    matches: list[tuple[int, int]]  # (pred index, truth index)


def panel_pr(pred: Sequence[Box], truth: Sequence[Box], threshold: float = 0.5) -> DetectionScore:
    """Precision and recall with greedy one-to-one matching at IoU >= threshold (U1, U2).

    Boxes are axis-aligned; irregular panels are scored by their bounding box.
    """
    pairs = sorted(
        ((iou(p, t), i, j) for i, p in enumerate(pred) for j, t in enumerate(truth)),
        reverse=True,
    )
    used_p: set[int] = set()
    used_t: set[int] = set()
    matches: list[tuple[int, int]] = []
    for score, i, j in pairs:
        if score < threshold:
            break
        if i in used_p or j in used_t:
            continue
        used_p.add(i)
        used_t.add(j)
        matches.append((i, j))
    precision = len(matches) / len(pred) if pred else (1.0 if not truth else 0.0)
    recall = len(matches) / len(truth) if truth else 1.0
    return DetectionScore(precision, recall, sorted(matches, key=lambda m: m[1]))


def reading_order_accuracy(truth_rank: Sequence[int], pred_rank: Sequence[int]) -> float:
    """Share of panel pairs whose relative order agrees (U3).

    Both sequences describe the same matched panels: item k has rank
    truth_rank[k] in the true order and pred_rank[k] in the predicted one.
    """
    if len(truth_rank) != len(pred_rank):
        raise ValueError("rank sequences differ in length")
    n = len(truth_rank)
    pairs = n * (n - 1) // 2
    if pairs == 0:
        return 1.0
    agree = sum(
        (truth_rank[a] < truth_rank[b]) == (pred_rank[a] < pred_rank[b])
        for a in range(n)
        for b in range(a + 1, n)
    )
    return agree / pairs


def normalise_text(text: str) -> str:
    return "".join(unicodedata.normalize("NFKC", text).split())


def _levenshtein(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def cer(reference: str, hypothesis: str) -> float:
    """Character error rate after NFKC normalisation and whitespace removal (U4)."""
    ref, hyp = normalise_text(reference), normalise_text(hypothesis)
    if not ref:
        return 0.0 if not hyp else 1.0
    return _levenshtein(ref, hyp) / len(ref)


def speaker_accuracy(truth: Sequence[str | None], pred: Sequence[str | None]) -> float:
    """Share of labelled bubbles with the right speaker; unlabelled ones are skipped (U5)."""
    if len(truth) != len(pred):
        raise ValueError("sequences differ in length")
    labelled = [(t, p) for t, p in zip(truth, pred, strict=True) if t is not None]
    if not labelled:
        return 1.0
    return sum(t == p for t, p in labelled) / len(labelled)


@dataclass(frozen=True)
class Shot:
    start_s: float
    end_s: float
    motion: str

    @property
    def duration(self) -> float:
        return self.end_s - self.start_s


@dataclass(frozen=True)
class ShotStats:
    median_s: float
    cv: float
    longest_s: float
    longest_motion_run: int
    max_motion_share_2min: float


def shot_stats(shots: Sequence[Shot], window_s: float = 120.0) -> ShotStats:
    """Pacing and variety numbers for V2-V5."""
    if not shots:
        raise ValueError("no shots")
    durations = [s.duration for s in shots]
    mean = statistics.fmean(durations)
    cv = statistics.pstdev(durations) / mean if mean > 0 else 0.0

    run = best_run = 1
    for prev, cur in zip(shots, shots[1:], strict=False):
        run = run + 1 if cur.motion == prev.motion else 1
        best_run = max(best_run, run)

    # Only full-length windows count, or a trailing window of one or two shots
    # would always read 100%. A video shorter than the window is one window.
    end = shots[-1].end_s
    anchors = [s.start_s for s in shots if s.start_s + window_s <= end] or [shots[0].start_s]
    max_share = 0.0
    for t0 in anchors:
        window = [s for s in shots if t0 <= s.start_s < t0 + window_s]
        counts: dict[str, int] = {}
        for s in window:
            counts[s.motion] = counts.get(s.motion, 0) + 1
        max_share = max(max_share, max(counts.values()) / len(window))

    return ShotStats(
        median_s=statistics.median(durations),
        cv=cv,
        longest_s=max(durations),
        longest_motion_run=best_run,
        max_motion_share_2min=max_share,
    )
