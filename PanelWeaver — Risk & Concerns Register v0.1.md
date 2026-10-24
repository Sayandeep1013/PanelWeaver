# PanelWeaver — Risk & Concerns Register

**Project:** PanelWeaver — AI Comic-to-Video Production System
**Companion document:** `PanelWeaver — AI Comic-to-Video Production System _ Initial Master Project Specification v0.1.md`
**Version:** `0.1`
**Status:** Pre-build risk assessment — no code written yet
**Purpose:** Enumerate every material concern in the master spec, pair each with concrete, costed, verifiable mitigations, and define the measures that must be taken *before* implementation begins.

---

## How to use this document

Every concern is a fixed-format record:

| Field | Meaning |
|---|---|
| **ID** | Stable identifier. Reference it in commits, issues, and design docs. |
| **Severity** | `FATAL` (stops the project) · `HIGH` (will cause major rework or a wrong build) · `MEDIUM` (costs weeks if ignored) · `LOW` (track, defer) |
| **Evidence** | What is actually known, with sources. Not speculation. |
| **Impact if unaddressed** | The concrete failure mode. |
| **Solution** | Named, verified options. Not "research this." |
| **Residual risk** | What the solution does *not* fix. |
| **Effort / Gate** | Time cost, and which build phase it must land before. |

**Severity distribution:** 2 FATAL · 7 HIGH · 7 MEDIUM · 3 LOW

**The two FATAL items are C-01 (no evaluation harness) and C-02 (the MVP is a shipped commodity).** Everything else is recoverable. Those two are not.

---

# PART 0 — Executive Summary

## 0.1 What the verification actually changed

Three findings materially altered the assessment after checking claims against current reality:

1. **The spec's hard front half is largely solved and nearly free.** Manga OCR now benchmarks at **2.91% CER** (PaddleOCR-VL-0.9B-For-Manga on JMangaBench). VLM image input costs **$0.0011–0.03 per image**. Word-level TTS timestamps are native and standard. The spec's five-phase, 36-item research programme is aimed at a target that has largely moved.

2. **The best off-the-shelf model for the hardest half cannot be used commercially.** Magiv3 (ICCV 2025) does panel/character/text localisation, bubble-tail detection, OCR, speaker association and character grounding — i.e. spec §12–§22 — as a 0.8B model on a consumer GPU. Its licence is explicitly **non-commercial, research-only**.

3. **A commercially-licensed evaluation corpus exists.** Manga109-s covers 87 volumes *newly approved for commercial use*, with results usable commercially. This dissolves the largest single blocker (C-03) and was not mentioned anywhere in the master spec.

**Net effect on the plan:** the MVP is a **weeks** project, not a multi-phase platform project. The spec's ambition and its engineering plan are misaligned by roughly an order of magnitude.

## 0.2 Timeline

| Milestone | Time | Gate |
|---|---|---|
| Ugly but real end-to-end (`comic → MP4`) | **1–2 weeks** | After C-01, C-03, C-04 land |
| Watchable — clears "not a slideshow" | **6–10 weeks** | After C-05, C-06, C-09 land |
| Spec Phase 2 (the actual product) | **+2–3 months** | After C-02 is answered |
| Spec Phase 3–5 (the vision) | **+6–12 months** | Research project, not engineering |

> **Honest constraint on the 6–10 week figure:** weeks 4–6 are gated by the human taste-feedback loop, not by engineering throughput. Spec §46 ("camera movement feels intentional rather than random") has no ground truth. It cannot be parallelised or accelerated by more compute.

## 0.3 The single most important structural criticism

The master spec spends effectively **100% of its planned effort on C-02** — a commodity — and **0% on §111/§112**, which the spec itself identifies as the core differentiator. RecapManga, MagaRecap and recapify already ship the §100 MVP. The differentiated product is the story engine, and it is not in the plan.

---

# PART 1 — Concern Register

## Group A — Measurement & Strategy (FATAL)

---

### C-01 — No evaluation harness · `FATAL`

**Evidence**
The spec defines an evaluation framework in §81 across nine layers and lists "evaluation datasets" and "end-to-end benchmarking" as items 35–36 in the §116 research backlog. Neither exists. There is no dataset, no ground-truth labels, no regression test, no scoring function.

This is worse in comics than in most CV domains. The *Comics Datasets Framework* paper (arXiv 2407.03540) documents the field's persistent structural problems directly: *"small datasets, inconsistent annotations, inaccessible model weights, and results that cannot be directly compared due to varying train/test splits and metrics."* Of the surveyed detection architectures, only two (DASS 2022, Magi 2024) had accessible weights. Manga copyright additionally prevents public redistribution of image corpora.

**Impact if unaddressed**
Every change becomes a coin flip. The team cannot answer "is v3 better than v2?" with evidence, only with preference. Expect to burn 3–4 weeks producing variants that cannot be compared, then argue about taste indefinitely. This is the single most common cause of LLM-pipeline projects stalling indefinitely.

**Solution**

1. **Adopt Manga109-s as the primary benchmark corpus.** 87 of 109 volumes are *newly approved for commercial use*. Stated permitted uses include *"using results, or portions of results, obtained from machine learning experiments or image processing experiments, for commercial use."* Redistribution of the dataset itself is forbidden — so it stays local, which is fine. This unblocks commercial evaluation at zero legal risk.
   `https://manga109.github.io/manga109-project-website/en/`
2. **Build a private 20-chapter labelled corpus on top of it.** Hand-label panel boxes, dialogue strings, reading order, and — critically — *"which panel belongs on screen at second N"* for 3 reference videos. This last label is what makes cinematography measurable.
3. **Write scoring functions, not vibes.** Convert §102's qualitative criteria into hard numbers (see C-05 for the full numeric set).
4. **Adopt JMangaBench for OCR specifically.** Real + synthetic, reports by orientation (1,390 vertical / 610 horizontal), crop type, and text length. Reproducible, single-GPU, published reference numbers.
   `https://github.com/muscgab/JMangaBench_Mixed/`
5. **Gate every pipeline stage behind a test.** If a stage has no test, it does not ship.

**Residual risk** — Manga109-s is Japanese-shogakukan-era academic corpus. It will not represent modern webtoon layout, colour manhwa, or Korean vertical text. It is a *floor*, not a representative distribution. A small private modern corpus is still required.

**Effort / Gate** — 4–6 days. **Must land before any pipeline code is written.**

---

### C-02 — The MVP is already a shipped commodity · `FATAL`

**Evidence**

| Product | Already ships |
|---|---|
| **RecapManga** | 25 panels/upload, multi-pass OCR incl. **vertical text and SFX**, **automatic speaker assignment**, 60+ voices, **word-level SRT captions**, 5 commentary styles, fair-use scoring, panel limits |
| **MagaRecap** | Panel detection (manga RTL / comics LTR / webtoon TTB), OCR, multiple TTS providers, animations, keyframes, audio slicing, export |
| **recapify** | One-click timeline generation, script sync, Premiere Pro export |

**This is spec §100's MVP, already in production, by funded competitors.**

**Impact if unaddressed**
The project builds a §100 MVP, ships it, and discovers at month four that the work is already commodity. Worse: the effort lands entirely in the commoditised quadrant, while §111/§112 — which the spec itself names as the differentiator — receives zero budget.

**Solution**

1. **Re-scope v1 explicitly.** Pick one and commit:
   - **(a) Story-engine first.** Build the narrative understanding layer (§25–§36) and *rent* the commodity layer (OCR/panel/TTS APIs). Differentiated, smaller, defensible.
   - **(b) Deliberate commodity play.** Compete on speed, price, language coverage, and a specific underserved input (e.g. Korean manhwa specifically, which the incumbents handle poorly). Requires a distribution advantage.
2. **Recommendation: (a).** The commodity layer is a solved, purchasable problem. The story engine is the only part of this spec that is hard to copy. See C-15 — the spec is *already* structured for (a); it just isn't prioritised that way.
3. **Write a differentiation memo before building.** One page: who is the customer, what can only we do, and why a competitor with more money cannot copy it in a quarter. If the answer is empty, that is the most valuable finding of Week 1.

**Residual risk** — Even the story engine has a research moat problem; see C-12.

**Effort / Gate** — 1 day. **Must be answered before the second week.**

---

### C-03 — Commercial licensing of the core model is unresolved · `HIGH`

**Evidence**

**Magiv3** (`ragavsachdeva/magiv3`, Sachdeva & Zisserman, ICCV 2025, arXiv 2503.23344) is a 0.8B unified vision-language model that performs, in one model:

- panel localisation
- character localisation
- text localisation
- **speech-bubble tail detection**
- OCR
- **speaker association**
- character grounding (locate a named character referenced in a caption)

That is spec §12–§22 — the entire "hard" understanding front half — in a single downloadable checkpoint that runs on a consumer GPU.

**Its licence is not commercial.** Verbatim from the model card:

> *"The provided model and datasets are available for unrestricted use in personal, research, non-commercial, and not-for-profit endeavors. For any other usage scenarios, kindly contact me via email, providing a detailed description of your requirements, to establish a tailored licensing arrangement."*

The GitHub README is blunter: *"The provided models and datasets are available for academic research purposes only."*

**Impact if unaddressed**
Build the entire understanding pipeline on Magiv3, then discover at commercialisation that you must either negotiate an individual licence with the author or reimplement. Both are expensive. This is the classic open-source-commons trap.

**Solution**

1. **Write a License Register before touching any dependency** (see Part 2, Measure 3). One table: dependency → licence → commercial OK? → fallback → cost.
2. **Assume research-only and design for substitution from day one.** The spec's §63 model-abstraction requirement is correct — enforce it at the *detector* level, not just the LLM level.
3. **Concrete commercial fallbacks for each capability:**

   | Capability | Research-only option | Commercial path |
   |---|---|---|
   | Panel detection | Magiv3, panelforge, CityU MM14 | LlamaGen panel segmentation API; commercial manga tooling; or fine-tune your own on Manga109-s (permitted, incl. commercial results) |
   | OCR | Magiv3, MangaOCR, HayaiOCR, BaberuOCR, PaddleOCR-VL | PaddleOCR-VL-0.9B-For-Manga (2.91% CER — verify licence); commercial OCR APIs |
   | Speaker association | Magiv3 | Build on bubble-tail detection + geometry; a VLM can also do this with a constrained-output prompt |
   | Character grounding | Magiv3 | DINOv2/v3 embeddings + FAISS (see C-08) |
   | TTS + word timings | Coqui, Piper | ElevenLabs, Deepgram Aura-2, Cartesia, Gradium (see C-09) |

4. **Contact the Magiv3 author early** if a commercial path is plausible. It is a single academic; the conversation costs one email and the answer materially changes the architecture.
5. **Note the fine-tuning escape hatch.** Manga109-s explicitly permits commercial use of *results obtained from ML experiments*. Training your own detector on it and shipping the resulting weights is a distinct and permitted activity. This is the cleanest long-term answer to the whole licensing category.

**Residual risk** — Fine-tuning your own detector means you now own model maintenance, dataset curation, and a training pipeline. That is real ongoing cost, not a one-off.

**Effort / Gate** — 1 day to write the register; licence negotiation lead time is unbounded. **Start the register before Week 1.**

---

## Group B — Perception & Abstraction (`HIGH`)

---

### C-04 — "Panel as the atomic unit" is wrong for the primary target market · `HIGH`

**Evidence**

Spec §13 makes the panel the atomic visual unit of the entire system. For **webtoon and manhwa** — the largest and fastest-growing segment (Solo Leveling, *The Beginning After the End*, *Tower of God*) — panels are **continuous vertical strips with no panel borders**. The cut between panels is purely semantic.

Every commercial tool confirms this. MagaRecap's own documentation states panel detection *"works best with clear panel borders,"* requires manual border drawing for borderless content, and ships a dedicated **"Smart Stitch"** pre-pass for webtoons specifically. From its troubleshooting table: *"Webtoons: Use Smart Stitch first."*

Critically, this is **not only a webtoon problem**. The CityU MM14 panel-extraction paper enumerates the failure modes in *manga* specifically: **irregular panels, fourth-wall breaks, joined panels, unclosed panels, and borderless panels** — and concludes that *"none of them are capable of dealing with all the aforementioned stylistic effects."* SFX effects, balloons and background texture that bleed across panel boundaries are the primary cause.

**Impact if unaddressed**
The core data structure of the entire system is undefined for your highest-volume input. Every downstream stage — panel ranking (§43), region-level selection (§44), camera planning (§45), visual continuity (§47) — inherits the defect. Discovering this in Month 3 means redesigning the document model.

**Solution**

1. **Decide scope on day one. Recommendation: manga-only for v1.** Bordered-panel manga is the well-served case, and it defuses this entirely.
2. **If manhwa/webtoon must be in v1, redefine the atomic unit** as a **scroll segment**: sample the vertical strip at a fixed interval (or at detected whitespace/gutter bands) to produce proxy panels. This is lossy but total — you can always split a segment, never rejoin one.
3. **Make the unit type explicit in the schema** (`Panel` vs `ScrollSegment`) rather than pretending one covers both. A discriminated union costs nothing now and prevents a rewrite later.
4. **Add a "panel confidence / is-borderless" flag** to every detection result, and route low-confidence cases to manual review rather than silently proceeding. This is §59's confidence system applied at the earliest stage instead of the last.

**Residual risk** — Scroll segments are a genuine approximation. Region-level visual selection (§44) becomes much harder when the unit is arbitrary.

**Effort / Gate** — 1 day decision. **Gate: before the schema is written.**

---

### C-05 — The "watchable" bar has no ground truth · `HIGH`

**Evidence**

Spec §102 sets the success bar qualitatively — *"camera movement feels intentional rather than random"*, *"a human can watch the result without immediately thinking: this is just an AI-generated slideshow."* These are not measurable. §46 (cinematography rules) and §75 (cinematic language) are descriptive, not algorithmic.

**Impact if unaddressed**
Weeks 4–6 become an unbounded taste-optimisation loop with no exit condition. Two reviewers can watch the same video and disagree. This is the most common way projects in this genre stall: everyone knows it isn't good enough, nobody can say what "good enough" is.

**Solution**

1. **Convert §102 into numbers.** Proposed starting set — calibrate after the first three videos:

   | Metric | Target | Notes |
   |---|---|---|
   | Dialogue OCR CER (vertical JP) | < 5% | JMangaBench reference |
   | Panel detection recall (bordered manga) | > 90% | on your corpus |
   | Speaker attribution accuracy | > 80% | on hand-labelled bubbles |
   | Script factual-error rate vs. source | < 2% | human audit of N=20 scripts |
   | Reading-order accuracy | > 95% | Manga109-s |
   | Blind human test: "not a slideshow" | > 60% pass | N=10 videos, random order, no context |
   | Mean shot duration variance | within stated band | detects monotony |

2. **Constrain cinematography to a closed preset vocabulary** — the single highest-leverage de-risking move available. Ship exactly these, with explicit selection rules:

   `push` · `pull` · `pan-left` · `pan-right` · `hold` · `cut` · `crossfade-to-region` · `static-with-subtitle`

   No free-form camera planning in v1. This converts an infinite taste problem into a tunable parameter. Reference implementation: `make-motion-comic` uses the same approach with push/pull/pan-l/pan-r/hold, strength `0.02–0.05`.

3. **Institutionalise blind A/B testing.** Watch three versions of the same video in randomised order, without knowing which is which. Record pass/fail against the one-line bar. Ten videos is enough signal to steer.

4. **Ship a timestamped feedback mechanism.** Every video gets a review URL where a human can mark the second at which attention dropped. That log becomes the training signal for the motion-selection rules.

**Residual risk** — Automated video scoring (spec §82) is a research problem with no reliable off-the-shelf solution. Do not attempt it in v1. Human blind testing is slower but is the only method that works today.

**Effort / Gate** — 2 days to define; ongoing. **Gate: before cinematography work begins (Week 4).**

---

### C-06 — Character identity across panels is an unsolved research problem · `HIGH`

**Evidence**

Spec §19 (Character Registry), §20 (Character Identity), §57 (Character QA), §71 (Cross-Chapter Continuity), and §104 (persistent character profiles) all depend on reliably answering *"who is this?"* across hundreds of stylised, often-deformed, often-silhouetted panels.

This is not solved. **Unsupervised Manga Character Re-identification** (FSAC, arXiv 2204.04621) is a dedicated research paper describing the problem as unsolved, noting that *"artistic expression and stylistic limitations of manga pose many challenges"* — exaggeration, deformation, stylisation, and characters who look alike because the series' art style constrains them.

Magiv3 provides per-page character localisation, clustering and grounding — **not** reliable cross-chapter identity.

**Impact if unaddressed**
This is a **silent failure**. The pipeline produces a video in which the wrong character is named, with no error signal. Wrong names in narration are the single most credibility-destroying error in a recap video, and a human reviewer may not notice on a 90-second video.

**Solution**

1. **Ship a human-in-the-loop character registry, not an automatic one.** The spec's §60 Human-in-the-Loop is correct — apply it here first, not last. Let a human name the cast once per series (20 names, 20 minutes), then let the system *propose* matches for human approval.
2. **Use embedding retrieval, not classification.** Fine-tuned **DINOv2 + FAISS** is the demonstrated pattern: the open-source *Visored* project reaches **81% Recall@1** on cross-domain retrieval (colour anime frame → B&W manga panel) across 42,112 panels / 706 chapters. The insight is transferable — you are doing the same retrieval problem, just within one medium, which is strictly easier.
3. **Never let character names reach narration without a human-set registry.** A name must be *confirmed*, not inferred. This converts a silent correctness risk into a one-time human cost.
4. **Add a validation pass that is cheap and high-yield:** for every character name in the final script, verify that at least one grounded detection supports it. Emit a warning listing unsupported names. This does not fix errors; it makes them visible.
5. **Instrument speaker attribution accuracy from day one.** Once it drops below the C-05 threshold, the video goes to review — it does not ship.

**Residual risk** — Accuracy will be well below 100% for off-panel characters, silhouettes, and first-appearance panels. Accept it. The mitigation is that humans approve names, so the *output* is correct even when the *matching* is not.

**Effort / Gate** — 1 week for registry + approval flow; 2 days for the grounding model. **Gate: before narration generation.**

---

### C-07 — The evidence graph is built on unverified claims · `MEDIUM`

**Evidence**

Spec §26 (Evidence-First Story Understanding), §27 (Evidence Graph), §35 (Script Evidence), §58 (Evidence-Based QA) and §59 (Confidence System) build a provenance layer over the pipeline. But the evidence base is:

- **OCR output** — verifiable against the image, and benchmarked
- **VLM-generated panel descriptions** — *not* verifiable. This is an unverified model claim, presented as structured data.

So the graph's leaves are, in large part, unverified LLM assertions. The provenance machinery makes hallucination *more* presentable and *harder* to spot, without making it less likely.

A related risk: spec §8's Canonical Project State assumes every stage emits reliable structured output. Constrained decoding fixes structure but not semantics — a 2026 benchmark (arXiv 2609.23742) found constrained decoding raises schema validity from 78.6–92.9% to **100%** while leaving a persistent, scale-dependent **semantic gap**: type-coercion errors are fully rescuable, but instruction-semantic failures are *not*. Well-formed JSON containing wrong content is the expected failure mode.

**Impact if unaddressed**
Narrative errors propagate silently through the graph with a false air of authority. Confidence scores derived from VLM self-report are not calibrated and will not help.

**Solution**

1. **Classify every field by verifiability** in the schema, explicitly:
   - `VERIFIED` — derived from OCR/geometry/detection, checkable against pixels
   - `DERIVED` — deterministic transform of verified data
   - `INFERRED` — model judgement, unverifiable
2. **Only allow `VERIFIED` facts into §35 script evidence.** Inferred content may influence style and phrasing but may not become load-bearing plot facts.
3. **Add a mandatory citation field**: every script beat carries `source_panel_ids[]` + `supporting_bubble_ids[]` + `evidence_class`. A beat with only `INFERRED` support is flagged for review.
4. **Never trust model-reported confidence.** Derive it from measurable proxies: OCR alignment loss, detection score margin, cross-model agreement, verification pass/fail. (Note: ElevenLabs forced alignment conveniently returns a per-word `loss`/confidence score — that pattern is worth copying for your own stages.)
5. **Adopt constrained decoding for every structured call**, and treat 100% schema validity as table stakes, not as correctness.

**Residual risk** — `INFERRED` fields are unavoidable — narrative compression (§72) *requires* abstraction. The goal is to make them *legible*, not to eliminate them.

**Effort / Gate** — 2 days of schema design. **Gate: before the Canonical Project State is defined.**

---

### C-08 — No cost model, and the spec optimises the wrong cost · `MEDIUM`

**Evidence**

Spec §64 (Model Routing), §65 (Caching), §84 (Cost Optimization) and §85 (Parallel Processing) represent roughly five subsystems of infrastructure. Verified 2026 pricing for the actual MVP workload:

| Item | 2026 cost |
|---|---|
| VLM image input | **$0.0011 – $0.03 per image** (Gemini tiers: $0.50 / $0.25 / $0.125 per 1M input tokens) |
| 30-panel chapter, 2 VLM passes | **≈ $0.01 – $1.80** |
| Narration TTS (~600 chars, Multilingual v2) | **$0.06** ($0.10 / 1k chars) |
| Narration TTS (~600 chars, Flash v2.5) | **$0.03** ($0.05 / 1k chars) |
| **Total per video** | **≈ $0.05 – $2.00** |

**Cost is not a problem at MVP scale. It will not become one until thousands of videos.**

**Impact if unaddressed**
Weeks spent on caching layers, routing tables and distributed queues — five subsystems — to optimise a $0.50/video problem, while shipping **zero measurement capability** (C-01). This is an inverted priority and it is the most likely way a small team burns a quarter.

**Solution**

1. **Build no cost-optimisation infrastructure in v1.** A single `--model` flag and a token counter are sufficient. Optimise on measurement (C-01), not on spend.
2. **Add a per-stage cost log from day one** — trivially cheap, and it becomes the input to §84 later. Never retrofit this.
3. **Cache only what is free to cache**: normalised page images and OCR results keyed by content hash. Do not build a cache tier.
4. **Reconsider §85 (parallel processing) too.** VLM calls at $0.001/image with sub-10s latency do not need a distributed worker pool. Sequential calls in one process are fine for 10–30 panels.
5. **Defer** the entire §92 stack — Redis, Celery, pgvector, Docker Compose, Kubernetes-style orchestration. Use **SQLite + local filesystem** until a stage genuinely requires more.

**Residual risk** — None material at this scale. Revisit at ~1,000 videos, or when latency becomes user-visible.

**Effort / Gate** — Ongoing logging: 0.5 days. **Gate: deferral decision, immediate.**

---

## Group C — Output Quality & Distribution (`HIGH`)

---

### C-09 — Narration audio ↔ visual timeline desynchronisation · `HIGH`

**Evidence**

Spec §41 (Audio Timing), §49 (Audio-Visual Synchronisation) and §50 (Timeline Engine) require precise audio timing. The open-source *make-motion-comic* project names this exact failure mode as one of its four recurring production problems: *"配音、字幕、镜头和片尾各自计时，返工后全部错位"* — voiceover, subtitles, shots and end-card each keep their own clock, so any rework desynchronises everything.

The underlying problem: TTS output length is determined by the script, while visual beat length is determined by the panel budget. They will not agree by construction.

**Impact if unaddressed**
Subtitle drift, cuts landing mid-word, and — worst case — a full re-record and re-render every time a script is edited. This compounds with §61's targeted regeneration, which assumes re-rendering is cheap.

**Solution**

1. **Use word-level timestamps as the single source of truth for the timeline.** This is now standard, not novel:
   - **ElevenLabs Forced Alignment** — `POST /v1/forced-alignment` returns per-**character** and per-**word** `start`/`end` in seconds, plus a per-word alignment `loss` score.
   - **Deepgram Aura-2**, **Cartesia Sonic-3**, **Gradium** — native word-level timestamps.
2. **Make the timeline derived, never authored.** Author narration text → synthesise → align → *derive* shot boundaries and subtitle cues from the alignment. Never hand-place a cut. This makes §61's targeted regeneration automatically correct.
3. **Solve the length mismatch at script time, not render time.** Before synthesis, estimate spoken duration from character count and pacing (~14–16 chars/sec conversational). If it exceeds the visual budget, either compress the script (LLM, constrained) or drop panels. Do it upstream.
4. **Use ElevenLabs Dubbing for the translation case** — 90+ languages, preserves emotion, timing, tone and per-speaker identity, retains original background audio, and can be given explicit `source_language` / `target_language` BCP-47 tags. Priced $0.33–0.50 per source minute.
5. **QA the render automatically.** From *make-motion-comic*'s validated checklist:
   ```
   ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate \
     -of json final.mp4
   ffmpeg -v error -i final.mp4 -f null -
   ffmpeg -hide_banner -i final.mp4 -vf blackdetect=d=0.3:pix_th=0.05 -an -f null -
   ffmpeg -hide_banner -i final.mp4 -af loudnorm=I=-16:LRA=9:TP=-1.5:print_format=summary -f null -
   ```
   Wire all four into CI. They catch the majority of silent render failures.

**Residual risk** — Alignment can drift on long passages with unusual prosody. Mitigate by aligning per-segment rather than once per file, so a local error cannot desynchronise the whole video.

**Effort / Gate** — 1 day to wire alignment into the schema; 1 day for the CI checks. **Gate: before the first render.**

---

### C-10 — Ken Burns micro-jitter and rendering artefacts · `MEDIUM`

**Evidence**

Spec §54/§55 specify FFmpeg rendering with zoom/pan. Slow `zoompan` moves less than one pixel per frame; integer rounding produces a visible stutter-jump, and **comic line art amplifies this severely** into shimmer. *make-motion-comic* identifies it as a primary failure mode: *"低分辨率 zoompan 产生一像素跳动和细线闪烁"* — low-resolution `zoompan` causes one-pixel jitter and fine-line flicker.

**Impact if unaddressed**
Output looks cheap and broken regardless of how good the script is. This is disproportionately damaging to perceived quality, and it is trivially fixable once known.

**Solution**

1. **Use the validated anti-jitter recipe** (from *make-motion-comic*, which solved this in production):
   - Source working canvas **2592×4608**
   - Motion output **2160×3840**
   - **Cosine ease-in-out**
   - **30 fps**
   - **Lanczos** downscale to 1080×1920
   - **One primary motion parameter per shot** — do not combine push + pan
   - Hold/static on emotional beats
2. **Keep push/pull strength in 0.02–0.05.** Beyond that it reads as amateur.
3. **Target 1080×1920 @ 30fps, H.264/AAC, ~−16 LUFS, True Peak ≤ −1.5 dBTP.** Consistent output specs make regressions visible.
4. **Build the render path with raw FFmpeg filtergraphs, not MoviePy.** MoviePy is convenient and adds a frame-accuracy tax that fights per-frame motion.
5. **Always run `blackdetect`** — black first-frames and dead gaps at shot boundaries are a common silent failure.

**Residual risk** — Very low-resolution source art (heavily compressed scans) will still shimmer. Detect and upscale or refuse, rather than shipping shimmer.

**Effort / Gate** — 2 days to a stable render path. **Gate: before Week 3.**

---

### C-11 — Translation quality is unaddressed and is where the value is · `HIGH`

**Evidence**

The source medium is Japanese, Korean and Chinese. The output narration is implicitly English. **Nothing in spec §9–§55 addresses translation, register, honorifics, transliteration, or cultural adaptation.**

This is not a minor gap. It is where the product lives or dies. The incumbents expose it as a first-class feature: RecapManga offers **Commentary / Educational / Humorous / Narrative / Dramatic** styles and markets "AI writes your recap script *in your voice*." The distinguishing characteristic of good recap videos is a human-sounding, opinionated narrator — not a flat reading of translated dialogue.

**Impact if unaddressed**
Output sounds like *"a robot reading a machine translation."* This is precisely the quality tier that gets a video dismissed as low-effort — and the exact failure the spec's §102 bar is trying to avoid.

**Solution**

1. **Decide the narration strategy explicitly. These are different products:**

   | Strategy | What it is | Effort | Defensibility |
   |---|---|---|---|
   | **Translate-and-narrate** | Faithful rendering of source dialogue in English | Low | Low — commodity |
   | **Commentary recap** | Original narrator voice over the panels; source is evidence, not script | Medium | **High** — this is the human value-add |
   | **Hybrid** | Commentary framing + quoted source lines | Medium | High |

   **Recommendation: commentary/hybrid.** It is what the spec's §97 "Creator adds commentary" already assumes, and it is the only version that clears the §102 bar comfortably.
2. **Add a register/translation QA stage.** Nothing ships without: name consistency (a glossary enforced across the whole script), honorific policy decided once, and a human spot-check of N=20 scripts.
3. **Build a pronunciation dictionary early** — spec §40 already calls for it. Given Korean and Japanese source with English narration, character-name pronunciation is a recurring, audible defect.
4. **Use the LLM for style transformation, not literal translation.** Constrain the output: given a structured evidence graph, produce narration in a chosen voice/stance with a length budget. Literal MT is the failure mode.
5. **Detect the "generic" failure explicitly.** If narration could have been written without looking at the comic, it has failed. That is a cheap automated check and a sharp design constraint.

**Residual risk** — Cultural adaptation and humour are genuinely hard to automate. Budget human review on a sample, permanently.

**Effort / Gate** — 2 days decision + glossary. **Gate: before §32 script generation is designed.**

---

### C-12 — Competitive moat is thin even in the differentiated story · `HIGH`

**Evidence**

Even the differentiated story-engine layer (spec §111/§112) has a defensibility problem. The reference literature is not merely academic — it is a working, published system doing the same thing:

**"From Panels to Prose: Generating Literary Narratives from Comics"** (Sachdeva & Zisserman, ICCV 2025) — Magiv3 performs panel, character and text localisation, speech-bubble-tail detection, OCR, speaker association, character clustering and visual grounding, then combines these structured outputs with VLM/LLM reasoning to generate coherent narratives.

That is the spec's §25–§36 thesis, already built, already published, already downloadable. It is research-only licensed (C-03), which is a legal moat of the weakest kind: it blocks a direct copier but not an independent reimplementation.

**Impact if unaddressed**
We build the differentiated layer, and a well-funded competitor independently reimplements the same ideas from the same public paper. Differentiation evaporates.

**Solution**

1. **Move the moat from models to assets and workflow.** Models commoditise; these do not:
   - **Proprietary, hand-annotated corpus** (C-01) that competitors must rebuild from scratch
   - **A learned cinematography policy** derived from human A/B feedback (C-05) — this is behavioural data no competitor has
   - **A creator-facing editing UX** — spec §107/§108/§109 (natural-language project editing) is genuinely hard to copy and is a *user-facing* moat rather than a model moat
2. **Prioritise the interactive/timeline-editor direction over the "one-click video" direction.** The market has converged on one-click; spec §109–§110's agentic editing is the actual defensible position and is cheap to build relative to its value.
3. **Ship the research paper as marketing.** Being the team that published the reference implementation is a durable credibility asset. Consider open-sourcing the understanding layer (MIT / Apache) and monetising the tool — this is the standard OSS-commons defence against a well-funded copier, and it directly exploits Magiv3's non-commercial licence as a competitive wedge.
4. **Write a moat memo** (see C-02, Measure 3) and stress-test it: "competitor with 10× our budget, 12 months — what can they not copy?"

**Residual risk** — If the answer is "not much", the correct business decision may be to build this as a product for your own use rather than a venture-scale company. Decide that explicitly rather than discovering it late.

**Effort / Gate** — 1 day. **Gate: alongside C-02.**

---

## Group D — Platform & Process (`MEDIUM` / `LOW`)

---

### C-13 — Architectural over-engineering relative to MVP input · `MEDIUM`

**Evidence**

Spec scope: 121 sections, 36-item research backlog, 14 named agents (§67), multi-tier memory (series/volume/chapter/scene/beat, §29), model routing (§64), caching (§65), agent orchestration with structured communication (§68), a 7-component infrastructure stack (§92: Next.js, FastAPI, PostgreSQL, pgvector, Redis+workers, object storage, FFmpeg, Docker), and a 20-directory repository layout (§93).

MVP input: **10–30 panels**, output **30–120 seconds**.

**Impact if unaddressed**
A small team spends a quarter building a platform and produces no video. The most likely concrete failure is a month of infrastructure before the first render.

**Solution**

1. **v1 is a Python package, a folder of Pydantic schemas, SQLite, and a CLI.** That is the entire architecture. Not a monorepo — a package.
2. **Explicitly defer from v1:** frontend · agents (§67) · memory tiers beyond chapter · Redis/workers · pgvector · Docker · caching · model routing · distributed rendering · auto-publish.
3. **Keep the spec's *interfaces*, discard its *infrastructure*.** The staged-pipeline discipline, evidence IDs and confidence fields are the valuable part and they cost nothing. The orchestration is what costs.
4. **Migrate up when forced, not before.** SQLite → Postgres and filesystem → S3 are days of work when actually needed. Retrofitting agent orchestration into a working pipeline is also days. Doing both up front is months.
5. **The spec's own §101 MVP Exclusions list is good — extend it** to include the platform items above.

**Residual risk** — A throwaway v1 becomes a production system by inertia. Counter by writing the schema module first and treating it as the durable artefact.

**Effort / Gate** — Immediate. **Gate: before repo scaffolding.**

---

### C-14 — Distribution channel risk (YouTube policy) · `HIGH` (business)

**Evidence**

Spec §96 flags copyright correctly and §97 argues for a "production assistant, not a content-spam generator." But §97/§118 assume a YouTube recap channel as the destination without stress-testing the policy.

YouTube's **"inauthentic content"** policy — renamed from "repetitive content" in a **15 July 2025** update — explicitly names this output category as ineligible for monetization. Stated examples include:

> *"Similar or repetitive content with low educational value, commentary, narratives, or minimal variation across videos"*
> *"Image slideshows, templated storylines, or scrolling text with minimal or no narrative, commentary, or educational value"*
> *"AI-generated content made with generic or unoriginal templates giving the impression of mass production without adding the creator's original, authentic insights or perspective"*

Critically, **reused-content review is channel-level**: *"If you have videos that violate our guidelines, or if we cannot clearly tell you that you made the content, monetization may be removed from your entire channel."*

**Impact if unaddressed**
A channel built on automated output is one policy update away from zero revenue — and the penalty applies to the **whole channel**, not the offending video. This is an existential dependency treated as a footnote in the spec.

**Solution**

1. **Keep auto-publishing excluded** (spec §101 already does). Do not add it in v1, v2, or v3. Manual upload is simultaneously your quality gate, your compliance gate, and your legal defence. This is the correct design, not a limitation.
2. **Design the output to be unmistakably authored.** The single strongest protection against "inauthentic content" is visible, substantial human creative contribution. This makes C-11 (commentary strategy) and C-14 the same problem — a strong reason to prioritise commentary over translate-and-narrate.
3. **Retain per-video provenance:** source panels, script versions, edit history, human review sign-off. When a channel is reviewed, the ability to evidence human authorship is worth more than any policy prediction.
4. **Do not build the business case on a single platform.** Treat YouTube as one channel among several, and never as the asset.
5. **Get a human copyright opinion before monetising anything.** A 1-hour consultation is trivially cheap against the downside. The spec is a technical document and this is outside its competence — flag it as such rather than resolving it in the spec.

**Residual risk** — Policy can change without notice and this is not fully controllable. Mitigation is diversification and genuine human authorship, not prediction.

**Effort / Gate** — Ongoing. **Gate: before any monetisation attempt.**

---

### C-15 — Provider churn and abstraction tax · `LOW`

**Evidence**

Spec §63 (Model Abstraction) and §64 (Model Routing) exist to manage this. The field is moving fast — the OCR leaderboard cited in C-01 already spans four models within 3 percentage points of CER, and provider model lineups turn over quarterly.

**Impact if unaddressed**
The abstraction, if built properly, is a permanent tax on every change. If built improperly (a thin wrapper over one vendor's response shape), it costs the same and buys nothing.

**Solution**

1. **Abstract at the capability level, not the SDK level.** Interface on *what you need* (`detect_panels(page) -> list[PanelBox]`), never on the vendor's object model. The spec's §63 is correct — enforce it strictly.
2. **Do not build routing in v1** (see C-08). One provider per capability, behind the interface. Routing is an optimisation for a cost problem that does not yet exist.
3. **Pin versions explicitly** and record the provider + model ID in every output artefact. Spec §66 (Reproducibility) already requires this — it is the actual defence against churn, and it is cheap.

**Residual risk** — None material. Under-investing here is the correct call at this stage.

**Effort / Gate** — Included in schema work. **Gate: before the second provider is added.**

---

### C-16 — Long-context and series-scale memory · `MEDIUM`

**Evidence**

Spec §29 defines five memory tiers (series/volume/chapter/scene/beat), §30 a context hierarchy, §91 vector search, §104 series memory, and §115 long-context story memory. Chapter-scale is tractable. Series-scale — hundreds of chapters, thousands of panels, full continuity of every character and plot thread — is a research project with a real cost curve.

**Impact if unaddressed**
Phase 4/5 slips indefinitely, and the system develops a "forgets everything after chapter 3" defect that undermines the §111 differentiator.

**Solution**

1. **Ship chapter-scoped memory in v1 and be explicit that it is chapter-scoped.** Honest limitation beats a broken promise.
2. **Design the schema so volume/series layers are *additive namespaces*, not schema rewrites.* Store per-chapter facts with a stable `series_id`/`volume_id`; retrieval scope is a query parameter, not a structural change.
3. **Use character names and IDs as the continuity spine** (C-06). A wrong name is worse than a forgotten plot thread.
4. **Defer pgvector until continuity is demonstrably needed.** Structured character + event tables in Postgres cover a surprising amount before vector search earns its cost.

**Residual risk** — True cross-series continuity (a plot thread from volume 1 surfacing in volume 9) is genuinely hard and should be scoped as research, not engineering.

**Effort / Gate** — Defer entirely. **Gate: Phase 4.**

---

### C-17 — Test and evaluation data cannot be redistributed · `LOW` (managed)

**Evidence**

Copyright prevents public distribution of comic corpora. Manga109's own terms: *"Redistribution of any part of the dataset to third parties is forbidden."* Magiv3's authors state they cannot distribute their collected manga images for the same reason.

**Impact if unaddressed**
If a second contributor (or future you) needs the corpus, it must be recreated. CI cannot run against real comic data on shared infrastructure.

**Solution**

1. **Store annotations separately from images**, version-controlled. Annotations are your work; the images are licensed and stay local. This makes the expensive human labelling effort portable and re-usable.
2. **Use a small, permissively-licensed synthetic set for CI** so automated tests run anywhere; reserve real corpora for local benchmark runs only.
3. **Record provenance for every annotated sample** (source, licence, permitted use) as part of the annotation schema. This is also your C-03 licence register, applied to data.

**Residual risk** — Low. The annotation/image split makes this a solved problem.

**Effort / Gate** — 0.5 days, part of C-01. **Gate: before labelling begins.**

---

### C-18 — Ambiguity in the spec's own scope boundary · `LOW`

**Evidence**

The spec oscillates between two products. §129 states *"manga recap generator is an implementation/use case… PanelWeaver is the underlying storytelling engine."* But §100 defines the MVP purely as a recap generator, and §101's exclusions list nothing about the engine. §107–§110 then describe a natural-language editing product that appears in no phase plan.

**Impact if unaddressed**
Scope creep in either direction — building a platform when a tool was needed, or a tool when a platform was promised.

**Solution**

1. **State the v1 scope in one sentence at the top of the register** and get it agreed. Everything else is deferrable by default.
2. **Park §107–§110 (natural-language editing) as a named v2 hypothesis**, not a background aspiration. Per C-12 it is the most defensible direction *and* the most expensive to build — it needs a working pipeline before it can be meaningful.
3. **Treat the spec as a capability catalogue, not a roadmap.** Everything in it is a legitimate capability; almost none of it is v1.

**Residual risk** — None, once stated.

**Effort / Gate** — 0.5 days. **Gate: immediate.**

---

### C-19 — Prompt and model version drift · `LOW`

**Evidence**

Spec §94 calls for prompts versioned like code; §62 for project versioning; §66 for reproducibility. Correct instincts, no mechanism yet. Prompt edits silently change output quality with no test to catch it.

**Impact if unaddressed**
"Reverting" a quality regression becomes guesswork. Combined with C-01 (no harness), this makes regressions permanently untraceable.

**Solution**

1. **Version prompts in git, hash them, and record the hash in every artefact** — the same discipline as C-15's provider/model pinning.
2. **The moment C-01's harness exists, add a golden-file test**: fixed input → assert output is within tolerance. Prompt changes then fail CI visibly.
3. **Keep the canonical project state (§8) fully serialisable** — it is the regression fixture. If it cannot be diffed, it cannot be tested.

**Residual risk** — None. Strictly a consequence of doing C-01 properly.

**Effort / Gate** — 0.5 days. **Gate: with C-01.**

---

### C-20 — Error taxonomy and observability specified but not designed · `LOW`

**Evidence**

Spec §88 (Error Taxonomy) and §89 (Observability) describe the requirement. Neither defines the actual error classes or the signal set.

**Impact if unaddressed**
When the pipeline fails at hour 3 of a 90-second render, there is no way to tell whether OCR failed, the story graph diverged, or TTS truncated. Debug time dominates.

**Solution**

1. **Minimum viable error taxonomy** — these five cover most real failures:
   `INGEST_FAILED` · `DETECTION_LOW_CONFIDENCE` · `OCR_FAILED` · `STORY_DIVERGED` (script contradicts evidence graph) · `RENDER_FAILED`
2. **Every stage emits a structured result envelope** with `status`, `confidence`, `cost`, `latency_ms`, `provider`, `model_id`, `prompt_hash`, `error_class`. This single envelope satisfies §64, §66, §84, §89 and §94 simultaneously.
3. **Fail loud, not silent.** Any stage below its confidence threshold halts the pipeline for review rather than passing bad data downstream. This is §59 working as designed, at the earliest possible point.

**Residual risk** — None.

**Effort / Gate** — 1 day, folded into schema work. **Gate: with C-01.**

---

# PART 2 — Pre-emptive Measures (Week 0, before any pipeline code)

Ordered by dependency. **Measures 1–4 are blocking; nothing should be built until they are done.**

| # | Measure | Addresses | Days | Blocking? |
|---|---|---|---|---|
| 1 | **Build the labelled eval corpus** on Manga109-s + private modern chapters. Annotations version-controlled, images local. Label: panel boxes, dialogue, reading order, and *"which panel at second N"* for 3 reference videos | C-01, C-06, C-17 | 4–6 | **Yes** |
| 2 | **Write the License Register** — one table: dependency → licence → commercial OK? → fallback → cost. Include Magiv3, every OCR model, TTS voices, music, subtitle fonts | C-03, C-14 | 1 | **Yes** |
| 3 | **Answer the two scope decisions in writing** | C-04, C-14 | 0.5 | **Yes** |
| 4 | **Convert §102 into numeric success criteria** and adopt the closed 8-motion vocabulary | C-05 | 1 | **Yes** |
| 5 | **Benchmark OCR + panel detection on your own corpus, 2-day timebox** | C-01, C-03, C-04 | 2 | No |
| 6 | **Write the differentiation + moat memo** — one page, stress-tested against a 10× competitor | C-02, C-12 | 1 | No |
| 7 | **Define the stage result envelope** (status, confidence, cost, latency, provider, model_id, prompt_hash, error_class) — one design, satisfies five spec sections | C-08, C-15, C-19, C-20 | 1 | No |
| 8 | **Set up the render QA gate** — `ffprobe` + `blackdetect` + `loudnorm` in CI | C-09, C-10 | 1 | No |
| 9 | **Decide the narration strategy** — commentary / translate-and-narrate / hybrid. Build the name glossary | C-11 | 1 | No |
| 10 | **Scaffold the minimum viable repo** — one Python package, `schemas/`, SQLite, CLI. Nothing else | C-13 | 0.5 | No |

### The two scope decisions, stated as questions

> **Q1 — Input scope.** Is v1 **manga-only** (bordered panels; defuses C-04 entirely), or must it handle **manhwa/webtoon** (requires redefining the atomic unit as a scroll segment)? *Recommendation: manga-only.*

> **Q2 — Distribution posture.** Is this a **personal/research tool** with manual upload (research-only models are acceptable), or a **commercial product** (every dependency must be commercially licensed, and C-03 must be resolved before building)? *This single answer determines the licensing posture of the entire project.*

**Neither question can be answered by the spec. Both must be answered by you in Week 0.**

---

# PART 3 — Deferred Concerns (explicitly out of v1)

| Concern | Revisit at | Trigger to pull it forward |
|---|---|---|
| C-08 cost optimisation (routing, caching) | ~1,000 videos | Per-video cost exceeds $5, or latency blocks interactive use |
| C-13 platform infrastructure (Redis, workers, pgvector, Docker) | When SQLite/Postgres actually blocks | Concurrent render queue, or search latency > 1s |
| C-16 series-scale memory | Phase 4 | Users request multi-chapter continuity |
| Agents (§67) | After the pipeline is stable and observable | A stage needs autonomous retry or re-planning |
| Automated video scoring (§82) | Research | Human A/B testing becomes the bottleneck |
| Auto-publishing | **Never, without legal review** | Not recommended |
| v2 hypothesis: NL project editing (§109–§110) | Phase 2+ | A working pipeline exists to edit |

---

# PART 4 — Decision Log

*To be completed as decisions are made. Every row must have an owner and a date.*

| ID | Decision | Options | Chosen | Rationale | Owner | Date | Reversible? |
|---|---|---|---|---|---|---|---|
| D-01 | Input scope (Q1) | manga-only / manhwa+webtoon | **Manga-only** | Bordered RTL manga is the well-served case (C-04); the demo is manga. Schema keeps a `Panel` / `ScrollSegment` union so webtoon can be added later | Owner (Sayandeep1013) | 2026-10-24 | Yes — schema is discriminated union |
| D-02 | Distribution posture (Q2) | research / commercial | **Personal / research** | Development demo on free tiers. Research-only models (e.g. Magi v3) are allowed; the demo stays private/unlisted unless the source allows sharing. Detectors stay behind capability interfaces with a commercial fallback recorded in `docs/LICENSE_REGISTER.md` | Owner (Sayandeep1013) | 2026-10-24 | **No** — determines all licensing |
| D-03 | Primary differentiator (C-02) | (a) story-engine / (b) commodity | | | | | No |
| D-04 | Narration strategy (C-11) | commentary / translate / hybrid | **Hybrid** | One narrator retells the story; key lines are spoken in character voices (spec §37). Clears the §102 bar better than translate-and-narrate | Owner (Sayandeep1013) | 2026-10-24 | Yes |
| D-05 | OCR engine | | | | | | Yes — behind interface |
| D-06 | TTS provider | | | | | | Yes — behind interface |
| D-07 | Panel detection approach | | | | | | Partially |
| D-08 | Music / SFX source (C-14) | e.g. Epidemic Sound Partner API (all-platform commercial licence incl. public performance rights) | | | | | Yes |
| D-09 | Subtitle font + burn-in path | | | | | | Yes |
| D-10 | v1 repo structure (C-13) | single package / monorepo | **Single package** | One Python package (`panelweaver`), Pydantic schemas, SQLite, a CLI. Nothing else (measure 10) | Owner, via `docs/BUILD_GUIDE.md` M0 | 2026-10-24 | Yes — early |

---

# PART 5 — Verification Sources

All claims in this register trace to these. Access dates: September 2026.

**Comprehension & datasets**
- Manga109 / Manga109-s — 87 of 109 volumes commercially approved; commercial use of *results* permitted; redistribution forbidden — `https://manga109.github.io/manga109-project-website/en/`
- Comics Datasets Framework (arXiv 2407.03540) — field-level dataset and reproducibility problems; accessible weights limited to DASS (2022) and Magi (2024) — `https://github.com/emanuelevivoli/cdf`
- JMangaBench_Mixed — mixed-domain Japanese manga OCR benchmark; orientation / crop-type / text-length slices — `https://github.com/muscgab/JMangaBench_Mixed/`
- Reference OCR results (RTX 4090): PaddleOCR-VL-0.9B-For-Manga 2.910% CER · BaberuOCR 4.589% · MangaOCR 4.683% · HayaiOCR 6.738%

**Models**
- Magiv3 / "From Panels to Prose" (ICCV 2025, arXiv 2503.23344) — 0.8B; panel / character / text localisation, bubble-tail detection, OCR, speaker association, character grounding. **Licence: personal, research, non-commercial, not-for-profit only** — `https://huggingface.co/ragavsachdeva/magiv3` · `https://github.com/ragavsachdeva/magi`
- panelforge — 3.4M-param U-Net, manga/manhwa panel segmentation + reading-order numbering, RTL/LTR/TTB, no pretrained backbone — `https://github.com/DATGMAC/panelforge`
- Visored — fine-tuned DINOv2 + FAISS, 81% Recall@1 cross-domain retrieval, 42,112 panels / 706 chapters — `https://github.com/dfdddfressd/Visored`
- FSAC / Unsupervised Manga Character Re-identification (arXiv 2204.04621) — character identity as an open problem

**Panel extraction**
- "A Robust Panel Extraction Method for Manga" (CityU, MM14) — enumerates irregular, fourth-wall-break, joined, unclosed and borderless panel failure modes; no prior method handles all — `https://www.cs.cityu.edu.hk/~rynson/papers/mm14a.pdf`
- MagaRecap panel detection docs — RTL/LTR/TTB support; "works best with clear panel borders"; Smart Stitch required for webtoons; manual border drawing for borderless — `https://magarecap.com/docs/image-processing/panel-detection`
- LlamaGen comic panel segmentation — commercial, reading order + bubble-safe margins — `https://llamagen.ai/features/comic-panel-segmentation-tool`

**Audio & narration**
- ElevenLabs pricing — TTS $0.10/1k chars (Multilingual v2/v3), $0.05/1k (Flash v2.5); Music $0.15/min; SFX $0.12/min; Dubbing $0.33–0.50/min — `https://elevenlabs.io/pricing/api`
- ElevenLabs Forced Alignment API — per-character and per-word `start`/`end` seconds plus per-word alignment `loss` — `https://elevenlabs.io/docs/api-reference/forced-alignment/create`
- ElevenLabs Dubbing — 90+ languages, preserves emotion/timing/speaker identity, retains background audio, BCP-47 tags — `https://elevenlabs.io/docs/overview/capabilities/dubbing.mdx`
- TTS provider comparison 2026 — native word-level timestamps (Gradium, Deepgram Aura-2, Cartesia); TTFA: Gradium 155–258 ms, Cartesia Sonic-3 188 ms, ElevenLabs Flash v2.5 288 ms, Deepgram Aura-2 313 ms — `https://gradium.ai/content/best-text-to-speech-apis-2026`

**Rendering**
- make-motion-comic — production anti-jitter recipe (2592×4608 → 2160×3840 → cosine ease → 30 fps → Lanczos to 1080×1920; push/pull strength 0.02–0.05), ffprobe/blackdetect/loudnorm QA gate, −16 LUFS / −1.5 dBTP — `https://github.com/ToBeWin/make-motion-comic`

**Platform & policy**
- YouTube monetization policies — "inauthentic content" (renamed 15 July 2025); names image slideshows, templated storylines, generic AI templates; **channel-level** monetization removal for reused content — `https://support.google.com/youtube/answer/1311392`
- Gemini Developer API pricing — image/text input tiers $0.50 / $0.25 / $0.125 per 1M tokens; images ≈ $0.0011–0.03 each — `https://ai.google.dev/gemini-api/docs/pricing`
- Epidemic Sound Partner API — all-platform commercial licence including public performance rights, cleared for commercial distribution — `https://www.epidemicsound.com/business/developers/`

**Structured output**
- "Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap" (arXiv 2609.23742) — schema validity 78.6–92.9% → 100%; type-coercion errors rescuable, instruction-semantic errors not — `https://arxiv.org/abs/2609.23742`

**Competitive**
- RecapManga — 25 panels, multi-pass OCR incl. vertical text + SFX, automatic speaker assignment, 60+ voices, word-level SRT, 5 commentary styles — `https://recapmanga.com/`
- recapify — one-click timeline, script sync, Premiere Pro export — `https://therecapify.com/`

---

# PART 6 — The Disagreement with the Master Spec

Stated plainly, because it matters more than any single risk item.

**The spec is a good architecture document and a bad plan.** Its instinct — staged pipeline, inspectable intermediate state, evidence before generation, confidence, targeted regeneration, reproducibility — is consistently correct and rare. Nothing in this register argues with the architecture.

The plan disagrees in three specific ways:

1. **It budgets for a solved problem.** §12–§36 target comprehension capabilities that now largely exist as open checkpoints and commercial APIs. That effort is better spent on the parts that remain hard: commentary quality (§32, §36), cinematography (§45–§48), and character continuity (§71).

2. **It budgets for a commodity.** §100's MVP is shipped by three funded competitors. Building it is a valid business decision, but it must be a *decision*, not the accidental default that a 121-section document produces by default.

3. **It adds documentation where it needs measurement.** §121 proposes the next deliverable be another architecture document. The single highest-value next artefact is instead a **20-chapter labelled corpus and a numeric pass/fail bar** — after which the second architecture document can be written in a day, and will be correct.

**The one-line version:** stop designing, start measuring. Everything expensive in this project is currently unfalsifiable, and nothing expensive can be scheduled until it becomes falsifiable.

---

*End of Risk & Concerns Register v0.1*
