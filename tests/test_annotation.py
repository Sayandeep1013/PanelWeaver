import pytest
from pydantic import ValidationError

from panelweaver.schemas.annotation import (
    ChapterAnnotation,
    Page,
    Panel,
    Polygon,
    ReferenceTimeline,
    TextRegion,
)

PROV = {
    "source_id": "synthetic",
    "title": "Synthetic fixture",
    "licence": "CC0-1.0",
    "permitted_use": "anything",
    "text_committable": True,
}


def _page(**kw):
    return Page(
        page_id="p1",
        width_px=1000,
        height_px=1500,
        panels=[
            Panel(panel_id="a", polygon=Polygon.from_box(0.5, 0, 0.5, 0.5), order=0),
            Panel(panel_id="b", polygon=Polygon.from_box(0, 0, 0.5, 0.5), order=1),
        ],
        **kw,
    )


def test_valid_chapter():
    text = TextRegion(
        text_id="t1",
        panel_id="a",
        polygon=Polygon.from_box(0.6, 0.1, 0.1, 0.2),
        type="dialogue",
        order=0,
        text="Hello",
        speaker="hero",
    )
    ch = ChapterAnnotation(
        chapter_id="c1",
        provenance=PROV,
        language="en",
        cast=[{"character_id": "hero", "name": "Hero"}],
        pages=[_page(text_regions=[text])],
    )
    assert ch.pages[0].panels[0].polygon.bbox() == (0.5, 0, 1.0, 0.5)


def test_rejects_unnormalised_points():
    with pytest.raises(ValidationError):
        Polygon.from_box(0.5, 0.5, 0.6, 0.1)


def test_rejects_gaps_in_reading_order():
    with pytest.raises(ValidationError):
        Page(
            page_id="p1",
            width_px=10,
            height_px=10,
            panels=[Panel(panel_id="a", polygon=Polygon.from_box(0, 0, 1, 1), order=1)],
        )


def test_rejects_unknown_speaker_and_uncommittable_text():
    region = {
        "text_id": "t1",
        "panel_id": "a",
        "polygon": Polygon.from_box(0.6, 0.1, 0.1, 0.2),
        "type": "dialogue",
        "order": 0,
    }
    with pytest.raises(ValidationError, match="not in the cast"):
        ChapterAnnotation(
            chapter_id="c1",
            provenance=PROV,
            language="en",
            pages=[_page(text_regions=[TextRegion(**region, speaker="ghost")])],
        )
    with pytest.raises(ValidationError, match="does not allow"):
        ChapterAnnotation(
            chapter_id="c1",
            provenance={**PROV, "text_committable": False},
            language="en",
            pages=[_page(text_regions=[TextRegion(**region, text="secret")])],
        )


def test_reference_timeline_rejects_overlap():
    with pytest.raises(ValidationError, match="overlaps"):
        ReferenceTimeline(
            video_id="v",
            chapter_id="c1",
            duration_s=10,
            shots=[
                {"start_s": 0, "end_s": 4, "panel_id": "a"},
                {"start_s": 3, "end_s": 6, "panel_id": "b"},
            ],
        )
