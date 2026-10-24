"""Eval corpus annotations (register measure 1, C-01, C-17). See docs/EVAL_CORPUS.md.

Annotation files are committed; the images they describe never are.
Coordinates are normalised to [0, 1] of the page (spec §56).
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Point = tuple[float, float]


class _Model(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Polygon(_Model):
    points: list[Point] = Field(min_length=3)

    @field_validator("points")
    @classmethod
    def _normalised(cls, points: list[Point]) -> list[Point]:
        for x, y in points:
            if not (0.0 <= x <= 1.0 and 0.0 <= y <= 1.0):
                raise ValueError(f"point ({x}, {y}) is outside [0, 1]")
        return points

    @classmethod
    def from_box(cls, x: float, y: float, w: float, h: float) -> Polygon:
        return cls(points=[(x, y), (x + w, y), (x + w, y + h), (x, y + h)])

    def bbox(self) -> tuple[float, float, float, float]:
        """Axis-aligned (x0, y0, x1, y1)."""
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return min(xs), min(ys), max(xs), max(ys)


class Provenance(_Model):
    source_id: str
    title: str
    licence: str
    permitted_use: str
    # Whether dialogue transcriptions of this source may live in the public repo.
    text_committable: bool = False


class Panel(_Model):
    # D-01 is manga-only, but the unit type stays explicit so a ScrollSegment
    # can join a discriminated union later without a rewrite (C-04).
    kind: Literal["panel"] = "panel"
    panel_id: str
    polygon: Polygon
    order: int = Field(ge=0)
    borderless: bool = False
    irregular: bool = False
    splash: bool = False
    crosses_gutter: bool = False


class TextType(StrEnum):
    DIALOGUE = "dialogue"
    THOUGHT = "thought"
    NARRATION = "narration"
    SFX = "sfx"
    SIGN = "sign"


class TextRegion(_Model):
    text_id: str
    panel_id: str
    polygon: Polygon
    type: TextType
    order: int = Field(ge=0)  # within its panel
    # None when the source's text isn't committable; see docs/EVAL_CORPUS.md §2.
    text: str | None = None
    text_sha256: str | None = None
    # A character_id from the chapter cast, or "unknown" / "offscreen".
    speaker: str | None = None


class Page(_Model):
    page_id: str
    width_px: int = Field(gt=0)
    height_px: int = Field(gt=0)
    panels: list[Panel] = Field(default_factory=list)
    text_regions: list[TextRegion] = Field(default_factory=list)

    @model_validator(mode="after")
    def _consistent(self) -> Page:
        orders = sorted(p.order for p in self.panels)
        if orders != list(range(len(orders))):
            raise ValueError(f"{self.page_id}: panel order must be 0..n-1, got {orders}")
        panel_ids = {p.panel_id for p in self.panels}
        if len(panel_ids) != len(self.panels):
            raise ValueError(f"{self.page_id}: duplicate panel_id")
        for t in self.text_regions:
            if t.panel_id not in panel_ids:
                raise ValueError(f"{self.page_id}: {t.text_id} refers to unknown {t.panel_id}")
        return self


class Character(_Model):
    character_id: str
    name: str  # named by the owner, never inferred (C-06)


class ChapterAnnotation(_Model):
    schema_version: Literal[1] = 1
    chapter_id: str
    provenance: Provenance
    reading_direction: Literal["rtl", "ltr"] = "rtl"
    language: str  # BCP-47, e.g. "ja", "en"
    cast: list[Character] = Field(default_factory=list)
    pages: list[Page]

    @model_validator(mode="after")
    def _speakers_known(self) -> ChapterAnnotation:
        known = {c.character_id for c in self.cast} | {"unknown", "offscreen"}
        for page in self.pages:
            for t in page.text_regions:
                if t.speaker is not None and t.speaker not in known:
                    raise ValueError(f"{t.text_id}: speaker {t.speaker!r} is not in the cast")
                if t.text is not None and not self.provenance.text_committable:
                    raise ValueError(
                        f"{t.text_id}: source {self.provenance.source_id!r} does not allow "
                        "committing its text; store it in workspace/ and keep only text_sha256"
                    )
        return self


class ReferenceShot(_Model):
    start_s: float = Field(ge=0)
    end_s: float = Field(gt=0)
    panel_id: str | None  # None: nothing from the corpus on screen
    framing: Literal["full", "region"] | None = None
    motion: str | None = None  # an entry from docs/SUCCESS_CRITERIA.md §2


class ReferenceTimeline(_Model):
    """'Which panel is on screen at second N' for a human-made recap video."""

    schema_version: Literal[1] = 1
    video_id: str
    chapter_id: str
    duration_s: float = Field(gt=0)
    shots: list[ReferenceShot]

    @model_validator(mode="after")
    def _ordered(self) -> ReferenceTimeline:
        prev_end = 0.0
        for s in self.shots:
            if s.end_s <= s.start_s:
                raise ValueError(f"shot at {s.start_s}s ends before it starts")
            if s.start_s < prev_end - 1e-6:
                raise ValueError(f"shot at {s.start_s}s overlaps the previous one")
            prev_end = s.end_s
        return self
