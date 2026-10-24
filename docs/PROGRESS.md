# PanelWeaver — Progress Log

Newest first. Each entry: what was done, what was measured, decisions, hours used, what's next.

**Codespace hours this month (budget ~60 h on 2 cores):** ~0.2 h

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
- `ruff` clean, **20/20 tests pass** in the codespace (Python 3.12.11, ffmpeg 5.1).
- Render QA gate on 20 s, 540p synthetic fixtures. Clean file: all checks PASS, −16.1 LUFS, −14.6 dBTP, A/V duration diff 0 ms. Broken file: it finds the planted black gap (8.00–9.03 s) and silence (12.01–14.02 s) at the right times.

**Measured**
- Codespace wake + venv + install + lint + tests in one `scripts/cs run`: **55 s**.
- Test suite: 18 s (most of it ffmpeg fixtures).

**Next**
- License Register (measure 2) from the licence research → `docs/LICENSE_REGISTER.md`.
- Verify the Black Jack terms, then choose chapters; owner picks their own chapters.
- Pre-labeller (OpenCV gutters) + labelling page → label the first corpus.
