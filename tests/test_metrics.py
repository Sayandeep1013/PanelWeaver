import pytest

from panelweaver.eval.metrics import (
    Shot,
    cer,
    iou,
    panel_pr,
    reading_order_accuracy,
    shot_stats,
    speaker_accuracy,
)


def test_iou():
    assert iou((0, 0, 1, 1), (0, 0, 1, 1)) == 1.0
    assert iou((0, 0, 1, 1), (2, 2, 3, 3)) == 0.0
    assert iou((0, 0, 2, 1), (1, 0, 3, 1)) == pytest.approx(1 / 3)


def test_panel_pr_one_to_one():
    truth = [(0, 0, 0.5, 0.5), (0.5, 0, 1, 0.5), (0, 0.5, 1, 1)]
    # Two predictions overlap the same truth box; only one may match it.
    pred = [(0, 0, 0.5, 0.5), (0.02, 0, 0.5, 0.5), (0, 0.5, 1, 1)]
    s = panel_pr(pred, truth)
    assert s.precision == pytest.approx(2 / 3)
    assert s.recall == pytest.approx(2 / 3)
    assert s.matches == [(0, 0), (2, 2)]


def test_panel_pr_empty():
    assert panel_pr([], []).recall == 1.0
    assert panel_pr([], [(0, 0, 1, 1)]).recall == 0.0


def test_reading_order():
    assert reading_order_accuracy([0, 1, 2, 3], [0, 1, 2, 3]) == 1.0
    assert reading_order_accuracy([0, 1, 2, 3], [3, 2, 1, 0]) == 0.0
    assert reading_order_accuracy([0, 1, 2], [1, 0, 2]) == pytest.approx(2 / 3)
    assert reading_order_accuracy([0], [0]) == 1.0


def test_cer_normalises_width_and_whitespace():
    assert cer("ＡＢＣ", "A B C") == 0.0  # full-width vs half-width
    assert cer("abcd", "abed") == pytest.approx(0.25)
    assert cer("", "") == 0.0
    assert cer("ねこ", "ねこだ") == pytest.approx(0.5)


def test_speaker_accuracy_skips_unlabelled():
    assert speaker_accuracy(["a", None, "b", "c"], ["a", "x", "b", "z"]) == pytest.approx(2 / 3)


def test_shot_stats():
    shots = [Shot(i * 4.0, i * 4.0 + 4.0, m) for i, m in enumerate("pphpcpph" * 10)]
    s = shot_stats(shots)
    assert s.median_s == 4.0
    assert s.cv == 0.0
    assert s.longest_motion_run == 2
    assert s.max_motion_share_2min == pytest.approx(0.6, abs=0.05)
