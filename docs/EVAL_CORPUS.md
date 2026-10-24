# PanelWeaver — Eval Corpus

**Week 0, measure 1** (register C-01, C-17). Plan agreed with the owner 2026-10-24: **small first**, then grow.
**Status:** plan. No images downloaded yet.

---

## 1. Size and sources

| | |
|---|---|
| **First corpus** | ~3 chapters, ~60 pages, fully labelled; **1 reference video** with timing labels |
| **Later** | Grow toward the register's 20 chapters + 3 reference videos as M2 needs it |
| **Allowed sources** (owner, 2026-10-24) | *Give My Regards to Black Jack*, **only after its terms are verified** (`docs/LICENSE_REGISTER.md`); the owner's own chapters (the owner puts them in `workspace/corpus/`) |
| **Not chosen now** | Pepper&Carrot (not manga), Manga109-s (needs an access request; revisit at the 20-chapter stage) |

Pick the chapters to cover the cases that break detectors (register C-04): regular grids, irregular or diagonal panels, at least one splash page, at least one borderless or unclosed panel, panels with balloons crossing the gutter, and vertical Japanese text (if the source is Japanese).

## 2. Where things live

| What | Where | Committed? |
|---|---|---|
| Page images | `workspace/corpus/<source_id>/<chapter_id>/<page>.png` in the codespace | **Never** |
| Annotations (boxes, order, types, speakers) | `eval/annotations/<source_id>/<chapter_id>.json` | Yes |
| Dialogue transcriptions | In the annotation file **only if** the source's terms allow it (`text_committable: true`); otherwise in `workspace/corpus/<source_id>/<chapter_id>.text.json`, with only a hash committed | Depends on the source |
| Reference video | `workspace/reference/` | **Never** |
| Reference timing labels | `eval/annotations/reference/<video_id>.json` | Yes |
| CI fixtures | Synthetic pages drawn by code in `tests/` (C-17) | Yes |

Dialogue text is part of the copyrighted work. A public repo can hold our boxes and labels, but not a full transcript of someone else's manga. The owner's chapters are presumably copyrighted, so their transcriptions stay out of git.

## 3. What gets labelled

Per **page**: size, source provenance (source, licence, permitted use; C-17).

Per **panel**: polygon (normalised [0, 1] coordinates; a rectangle is a 4-point polygon), reading-order index, flags `borderless` · `irregular` · `splash` · `crosses_gutter`.

Per **text region**: polygon, panel it belongs to, type (`dialogue` · `thought` · `narration` · `sfx` · `sign`), order within its panel, transcription (see §2), speaker = a character id from the chapter's cast, or `unknown` / `offscreen`.

Per **chapter**: the cast list, named by the owner (C-06: a name is confirmed, never inferred).

Per **reference-video second**: which panel is on screen (or `none`), framing (`full` / `region`), and the motion seen (from the vocabulary in `docs/SUCCESS_CRITERIA.md`). Used to calibrate pacing (V2–V5), not as ground truth for our own narration.

Character bounding boxes are **not** in the first corpus. They're needed for region focus (spec §44) and get added in M2 if the detector benchmark needs them.

## 4. How labelling works

1. **Pre-label** panel boxes with a simple OpenCV gutter detector.
2. **Correct** them on a small labelling page served from the codespace on port 8000 (draw, move, delete boxes; set the order; tag the text regions). The owner checks **every** page, because pre-labels would otherwise bias the ground truth toward that detector. Its raw, uncorrected scores are recorded separately.
3. **Validate**: every annotation file must pass its Pydantic schema (`panelweaver.schemas.annotation`) in CI.

Estimate: ~1.5–2 days in total, most of it owner review time (~3–4 minutes per page).

## 5. Scoring functions

These live in `panelweaver.eval`, with tests on synthetic fixtures:

| Function | Metric | Feeds |
|---|---|---|
| `panel_pr` | Precision and recall at IoU ≥ 0.5, greedy matching | U1, U2 |
| `reading_order_accuracy` | Pairwise order accuracy per page | U3 |
| `cer` | Character error rate after NFKC normalisation and whitespace removal | U4 |
| `speaker_accuracy` | Share of labelled bubbles with the right speaker | U5 |
| `shot_stats` | Median shot duration, coefficient of variation, motion mix (from a timeline or reference labels) | V2–V5 |

## 6. Open items

- [ ] Verify the Black Jack terms (licence research in progress), then choose its chapters.
- [ ] Owner: which of your own chapters, and in what language?
- [ ] Choose the reference video. It has to be a human-made recap of one corpus chapter, and downloading it counts as source material (ask the owner first).
