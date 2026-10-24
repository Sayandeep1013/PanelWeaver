"""Classical panel pre-labeller: proposes panel boxes for a human to correct.

Not a detector we ship: its job is to save labelling time (docs/EVAL_CORPUS.md
§4). Its raw output is scored separately so the corrected ground truth can't
quietly inherit its bias. Also the OpenCV baseline for measure 5.

Method: binarise the page, close small breaks in panel borders, take the
outer contours of ink regions, keep the large ones, then order them RTL.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

Box = tuple[float, float, float, float]  # normalised x0, y0, x1, y1


@dataclass(frozen=True)
class Proposal:
    box: Box
    area_frac: float


def propose_panels(
    gray: np.ndarray, min_area_frac: float = 0.01, close_px: int = 5
) -> list[Proposal]:
    """Candidate panel boxes for one page (grayscale uint8), unordered."""
    h, w = gray.shape
    _, ink = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (close_px, close_px))
    ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(ink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    proposals = []
    for c in contours:
        x, y, bw, bh = cv2.boundingRect(c)
        frac = (bw * bh) / (w * h)
        if frac < min_area_frac or frac > 0.98:
            continue
        proposals.append(Proposal((x / w, y / h, (x + bw) / w, (y + bh) / h), frac))
    return proposals


def reading_order(boxes: list[Box], rtl: bool = True, row_overlap: float = 0.5) -> list[int]:
    """Indices of `boxes` in reading order: rows top to bottom, then RTL (or LTR) in a row.

    A box joins the current row when it overlaps the row's vertical span by at
    least `row_overlap` of its own height. Good enough for regular layouts;
    the human fixes the rest.
    """
    remaining = sorted(range(len(boxes)), key=lambda i: boxes[i][1])
    order: list[int] = []
    while remaining:
        first = remaining[0]
        top, bottom = boxes[first][1], boxes[first][3]
        row = []
        for i in remaining:
            y0, y1 = boxes[i][1], boxes[i][3]
            overlap = min(bottom, y1) - max(top, y0)
            if overlap >= row_overlap * (y1 - y0):
                row.append(i)
        row.sort(key=lambda i: boxes[i][0], reverse=rtl)
        order.extend(row)
        remaining = [i for i in remaining if i not in row]
    return order
