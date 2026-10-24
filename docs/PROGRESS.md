# PanelWeaver — Progress Log

Newest first. Each entry: what was done, what was measured, decisions, hours used, what's next.

**Codespace hours this month (budget ~60 h on 2 cores):** ~0.4 h

---

## 2026-10-25 — Decisions delegated to Claude

The owner asked Claude to make the open calls. This is a free, public, non-commercial showcase.
- **D-12 demo source: *Give My Regards to Black Jack*, official English.** Scanlations / "fan manga" rejected: unauthorised copies risk a DMCA takedown of the public repo and strikes on the video, whether or not money is made. Black Jack's terms allow a **public** demo.
- D-03 story-engine first · D-08 incompetech + Freesound CC0 · D-09 Noto Sans CJK via ASS · D-11 Gemini free tier (fine for free-licensed pages).
- Camera vocabulary adopted (`docs/SUCCESS_CRITERIA.md` is now "adopted"). Own chapters: not needed.
- **Repo licence: MIT** (`LICENSE`). None of the owner's public repos had a licence, which legally means "all rights reserved".
- Manhwa stays out of v1 (D-01 is reversible). Revisit after the manga demo works, with a freely licensed manhwa.

**M0 status:** measures 2, 3, 4, 7, 8, 10 done; measure 1 (labelled corpus) remains.

---

## 2026-10-24 — Session 1: M0 started (PC setup)

**Decisions (owner)**
- D-01 **manga-only**, D-02 **personal/research**, D-04 **hybrid** (recorded earlier). All three are now in the register's decision log, along with D-10 (single package).
- Eval corpus: **small first** (~3 chapters, ~60 pages, 1 reference video). Sources allowed: *Give My Regards to Black Jack* (after its terms are verified) and the owner's own chapters.

**Done**
- Measure 4 drafted: `docs/SUCCESS_CRITERIA.md` (numeric criteria U/S/A/T/V/O, closed camera vocabulary, selection rules). **Needs owner OK** on one deviation: a single `pan` entry with a direction (16:9 needs vertical pans) and `fade` for the start and end.
- Measure 1 planned: `docs/EVAL_CORPUS.md` (label set, storage split, labelling flow, scoring functions). No images yet.
- Measures 7, 8, 10 (scaffold): package `panelweaver` (`src/`), `schemas/envelope.py` (stage result envelope), `schemas/annotation.py` (corpus schema), `eval/metrics.py`, `qa/render.py` (render QA gate), `store.py` (SQLite), CLI (`panelweaver qa-render`, `panelweaver validate`), CI workflow.

**Verified**
- `ruff` clean, **22/22 tests pass** in the codespace (Python 3.12.11, ffmpeg 5.1) and **CI is green on main** (GitHub Actions, 44 s).
- Render QA gate on 20 s, 540p synthetic fixtures. Clean file: all checks PASS, −16.1 LUFS, −14.6 dBTP, A/V duration diff 0 ms. Broken file: it finds the planted black gap (8.00–9.03 s) and silence (12.01–14.02 s) at the right times.

**Measured**
- Codespace wake + venv + install + lint + tests in one `scripts/cs run`: **55 s**.
- Test suite: 18 s (most of it ffmpeg fixtures).

**Also done (later in the session)**
- **Measure 2: `docs/LICENSE_REGISTER.md`**, from two research passes over primary sources. Key findings:
  - Magi is allowed under D-02; the commercial route is by email only.
  - The register's "2.91% CER" for PaddleOCR-VL-For-Manga isn't on its card (unverified); JMangaBench_Mixed returns 401.
  - `kokoro` pulls GPL phonemizer/espeak (only matters if we distribute); Piper is now GPL; the lessac voice is research-only.
  - Manga109 needs an institutional email. Manga109-s pages may never appear in a video.
  - **Pepper&Carrot now prohibits AI derivations: avoid.**
  - **Gemini free tier uses inputs for training, with human review: owner decision before M1.** Groq's free plan has no vision model.
  - Kaggle is personal/non-commercial only. Modal appears to need a card.
  - D-08 recommendation: incompetech (CC BY) + Freesound CC0.
- **Black Jack terms verified** at densho810.com/free/ (commercial OK, adaptations OK; credit "Give My Regards to Black Jack / SHUHO SATO"; email info@densho810.com within 1 month of publishing). **English vol 1 downloaded** to `workspace/corpus/blackjack/src/` (420 MB PDF, 209 pages, ~2 min). The EN edition is not mirrored (RTL). Chapters picked: Ep.02, Ep.03, "The First Lie" (~63 pages), see `docs/EVAL_CORPUS.md` §6.
- OpenCV panel pre-labeller (`panelweaver.corpus.prelabel`) with an RTL reading-order heuristic. Checked on a synthetic page by looking at the overlay: 3 of 4 rows exact, RTL order right, and a balloon crossing a gutter merges two panels (the expected C-04 failure, now pinned by a test).

**Next**
- Labelling page (served on port 8000) + page extraction for the 3 chapters → pre-label → owner corrects → `eval/annotations/blackjack/*.json`.
- Score the raw pre-labeller against the corrected labels (first measure 5 data point).
- Owner: OK on the camera-vocabulary deviation; Gemini free-tier data use; own chapters now or later.
