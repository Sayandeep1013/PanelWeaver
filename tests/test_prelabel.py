"""Pre-labeller on a synthetic manga page drawn here (no real artwork in CI, C-17)."""

import numpy as np
import pytest

cv2 = pytest.importorskip("cv2")

from panelweaver.corpus.prelabel import propose_panels, reading_order  # noqa: E402
from panelweaver.eval.metrics import panel_pr  # noqa: E402

W, H = 1000, 1500
# Truth in RTL reading order: top row right then left, a wide middle panel,
# bottom row right then left.
TRUTH_PX = [
    (520, 40, 960, 500),
    (40, 40, 480, 500),
    (40, 540, 960, 900),
    (620, 940, 960, 1460),
    (40, 940, 580, 1460),
]


def synthetic_page(rng: np.random.Generator) -> np.ndarray:
    page = np.full((H, W), 255, np.uint8)
    for x0, y0, x1, y1 in TRUTH_PX:
        cv2.rectangle(page, (x0, y0), (x1, y1), 0, 4)
        for _ in range(12):  # "artwork": strokes that stay inside the panel
            p = rng.integers((x0 + 10, y0 + 10), (x1 - 10, y1 - 10), size=(2, 2))
            cv2.line(page, tuple(map(int, p[0])), tuple(map(int, p[1])), 0, 2)
    # A white balloon with an outline crossing the gutter between the top panels.
    cv2.ellipse(page, (500, 270), (60, 40), 0, 0, 360, 255, -1)
    cv2.ellipse(page, (500, 270), (60, 40), 0, 0, 360, 0, 2)
    return page


def test_finds_panels_and_rtl_order():
    page = synthetic_page(np.random.default_rng(0))
    proposals = propose_panels(page)
    pred = [p.box for p in proposals]
    truth = [(x0 / W, y0 / H, x1 / W, y1 / H) for x0, y0, x1, y1 in TRUTH_PX]
    score = panel_pr(pred, truth)
    # The balloon merges the two top panels into one region: a known failure
    # mode (C-04, "crosses_gutter"). The other three must be found.
    assert score.recall >= 0.6
    assert score.precision >= 0.75
    found = {j for _, j in score.matches}
    assert {2, 3, 4} <= found


def test_reading_order_rtl_and_ltr():
    truth = [(x0 / W, y0 / H, x1 / W, y1 / H) for x0, y0, x1, y1 in TRUTH_PX]
    shuffled = [truth[i] for i in (4, 2, 0, 3, 1)]
    order = reading_order(shuffled)
    assert [shuffled[i] for i in order] == truth
    ltr = reading_order(truth, rtl=False)
    assert ltr == [1, 0, 2, 4, 3]
