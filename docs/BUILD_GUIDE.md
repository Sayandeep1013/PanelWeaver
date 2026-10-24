# PanelWeaver — Build Guide (start here)

**Written:** 2026-10-24, from a planning conversation between the owner (Sayandeep1013) and Claude.
**Audience:** the Claude Code session that will build PanelWeaver inside this repo's GitHub Codespace, and the owner.
**Status:** nothing is built yet. The repo holds the vision spec and this guide.

---

## 0. Read this first (for Claude)

There are two documents. Read both before writing any code:

| Document | What it is |
|---|---|
| `PanelWeaver — AI Comic-to-Video Production System _ Initial Master Project Specification v0.1.md` (repo root) | **The vision and architecture.** What PanelWeaver is, the pipeline, data model, principles. Section numbers below (§N) refer to it. |
| `docs/BUILD_GUIDE.md` (this file) | **How we execute it.** Where it runs, what compute does what, the milestones to the demo, and the ground rules. |

Where they disagree, this guide wins on *process and scope*, the spec wins on *architecture*. The spec's core rules stand:

- **Understand first. Generate second. Direct third. Render last.** (§1)
- Every stage writes an inspectable artifact: `document.json → panels.json → story.json → script.json → voice/ → visual_plan.json → timeline.json → video.mp4` (§5).
- **AI decides what the video contains; deterministic code renders it** (§54). LLM output goes through validated schemas, never straight into shell/FFmpeg commands.
- **Motion graphics first, generative video later** (§76–77). The original artwork is the main visual.

Keep a running log in `docs/PROGRESS.md` (create it): what was done, what was measured, what is next. A codespace can stop at any time, so commit and push small steps often.

---

## 1. The goal: one demo video

Build PanelWeaver to the point where it produces **one convincing demo video**, end to end, that proves the pipeline works.

| | |
|---|---|
| **Length** | 15–20 minutes |
| **Source** | 1–2 manga (chapters or a short volume). **Not chosen yet**, see §8 "Open decisions" |
| **Format** | 16:9 landscape, 1080p, 30 fps, MP4 (H.264 + AAC). Keep coordinates normalized (§56) so 9:16 is possible later |
| **Narration** | **Hybrid** (§37): one narrator retells the story; key lines are spoken in character voices |
| **Also in the video** | Subtitles, background music, a few sound effects, intentional camera moves (§45–46) |
| **Extras (GPU)** | Upscaled artwork; a handful of short "hero shot" animations. Optional polish, never required for the video to work |

This goes well past the spec's MVP (§100, 30–120 s). The MVP is milestone M1 below, and the demo is the end of the road (M8).

**The bar (§102):** a person can watch it without thinking "this is just an AI slideshow."

---

## 2. Ground rules

### 2.1 Accounts and keys (important)
- Claude Code in this codespace is logged in with the owner's **work** Claude account. Use it **only as the coding assistant**.
- **Never use that account, or any company key, as PanelWeaver's runtime model.** All model calls made *by the pipeline* (vision, script, etc.) use the owner's **personal free-tier keys** (see §5).
- Keys live in **Codespaces secrets** (github.com/settings/codespaces → Secrets, scoped to this repo) and arrive as environment variables. Never write a key into a file, a commit, a log or `docs/PROGRESS.md`.
- Ask the owner to add a secret when one is needed, and say exactly which name to use (e.g. `GEMINI_API_KEY`).

### 2.2 Compute: use it the way it's meant to be used
- **The codespace is for development**: writing code, running tests, test renders, and rendering the demo while developing it. That is what it is for.
- **GitHub Actions is CI only**: lint and tests for this repo. **Never render videos or run the pipeline in Actions.**
- GPU providers (Kaggle, Modal, etc.) are used within their free tiers and their rules: no crypto mining, no always-on servers, no web UIs where a provider forbids them (Colab free restricts web UIs).

### 2.3 Copyright (§96)
- **This repo is public.** Never commit manga pages, panels, generated audio of copyrighted text, or renders containing copyrighted artwork.
- All source material and outputs live in `workspace/` and `renders/`, which are git-ignored. Check `.gitignore` before every commit that touches new paths.
- **Ask the owner before downloading any source material.** Prefer freely-usable sources (see §8).

### 2.4 The owner works from a phone
The point of this setup is **no laptop**: the owner opens this codespace in a phone browser and talks to you.
- Keep messages short and scannable. Put long detail in `docs/PROGRESS.md` and point to it.
- Don't ask the owner to type long commands. Run them yourself.
- To show results: extract frames or contact sheets as PNGs and describe them, and serve outputs on a forwarded port (`python -m http.server 8000` in `renders/`) so the owner can open the MP4 on the phone. Keep files small: a 540p preview is fine for checking.
- Commit and push often. The codespace stops after the idle timeout.

### 2.5 Done means verified
"The code ran" is not done. A step is done when its **output was checked**:
- JSON artifacts validate against their schema.
- Visual steps: render a contact sheet or sample frames with FFmpeg and **look at them** (you can read images).
- Audio: check duration, loudness (`ffmpeg -af ebur128` / `loudnorm`) and a transcript round-trip if possible.
- Video: sample frames at several timestamps, check A/V sync at beat boundaries.

Say plainly what was and wasn't verified.

### 2.6 Ask before
- downloading source material,
- spending GPU credits on a run expected to cost more than about **$3**, or anything that could exceed a free tier,
- adding any paid service, or anything that needs a card,
- deleting renders the owner hasn't seen.

---

## 3. The environment: this codespace

### 3.1 What it is
A GitHub Codespace: a Linux VM in GitHub's cloud, opened in the browser (VS Code + terminal). It was set up by `.devcontainer/` in this repo:

- Python 3.12 (Debian bookworm base image)
- `ffmpeg`, `espeak-ng` (needed by Kokoro TTS), Noto CJK fonts (Japanese text in subtitles and contact sheets)
- Claude Code (native installer)
- Port 8000 forwarded for previews

If something is missing, install it and add it to the setup so the next codespace has it too: system packages (apt) go in `.devcontainer/Dockerfile`, user-level tools in `.devcontainer/setup.sh`. The base image's Yarn apt source is broken and removed in the Dockerfile; keep that line.

### 3.2 Limits (GitHub Free personal account; verify on GitHub's billing page)
| Limit | Value | What it means |
|---|---|---|
| Compute | **120 core-hours / month** | **~60 h on this 2-core machine** (30 h if switched to 4-core) |
| Storage | **15 GB-month** | Keep the codespace disk use well under ~10 GB. Delete old renders and intermediates you no longer need |
| Machine | 2 cores, 8 GB RAM, 32 GB disk | Enough for the whole CPU pipeline (§4). Not enough for diffusion/video models |
| Idle timeout | set to **4 h** (the max) | A long task with no owner input can still be cut off at 4 h. Make long jobs resumable |
| No GPU, no Android emulator | | GPU work goes to the providers in §5 |

**Budget the 60 hours.** Rough plan: ~40 h development and test renders, ~10 h for the full demo renders, ~10 h slack. Log hours used per session in `docs/PROGRESS.md`. Stop the codespace when a session ends (the owner can tap Stop, or run `gh codespace stop`).

### 3.3 Owner's phone quickstart
1. Phone browser → **github.com/codespaces** → open the PanelWeaver codespace (desktop-site mode works best).
2. In the terminal: `claude`. The first time, it shows a login link: open it, approve, paste the code back. Once per codespace.
3. Say what to do, e.g. *"Read docs/BUILD_GUIDE.md and start M0."*
4. Done for the day: ⋯ → **Stop codespace** (saves hours; files are kept).

---

## 4. Compute plan: what needs a GPU

**The core pipeline runs on CPU in the codespace.** A GPU is only for polish. These timings are planning guesses: **measure the real ones in M1/M2 and record them** in `docs/PROGRESS.md`.

| Stage (spec §) | Tool (first choice → fallback) | Where | Rough cost for the demo (~300 pages) |
|---|---|---|---|
| Ingest pages: images / CBZ / PDF (§9) | Pillow, `zipfile`, PyMuPDF | Codespace CPU | Seconds |
| Panels, text boxes, characters, speaker links (§12, §17–18) | **Magi v2** (`ragavsachdeva/magiv2` on Hugging Face; check its licence) → OpenCV whitespace/contour fallback | CPU, or a Kaggle GPU batch if CPU is too slow | CPU: guess ~5–15 s/page ≈ ~1 h total. Kaggle: minutes. If Magi v3 (ICCV 2025, §78) weights are public, evaluate it |
| OCR (§15–16) | Magi's OCR → `manga-ocr` (Japanese) / PaddleOCR (English) → VLM verification | CPU | ~1–5 s per text region |
| Scene/character understanding (§22) | Vision LLM via **personal free-tier API** (Gemini; see §5), cached per image hash (§65) | API | Free-tier rate limits: batch and cache |
| Story graph, beats, script (§25–35) | Text LLM via personal free-tier API (Gemini / Groq) | API | Minutes |
| Narrator + character voices (§38–39) | **Kokoro-82M** (Apache-2.0; several distinct voices, enough for hybrid) → Piper | CPU | Expect roughly real time or faster: 20 min of audio ≈ ≤20 min. Measure in M1 |
| Timing (§41, §49) | Synthesize **per sentence**: the audio file's length *is* the timestamp. Word-level later via forced alignment (e.g. WhisperX / stable-ts) | CPU | Free |
| Visual plan, timeline (§42–50) | Our own Python + schemas | CPU | Seconds |
| Render (§54–55) | FFmpeg (crop/scale/zoompan, xfade, ASS subtitles, amix, loudnorm) | CPU | 1080p is slow on 2 cores: guess 0.5–1× real time ≈ 20–40 min per full render. **Iterate at 540p**, render 1080p only for finals |
| **Upscale artwork** (polish) | Real-ESRGAN (anime model) | **GPU**: Kaggle batch | CPU possible but very slow; GPU minutes |
| **Hero shots** (polish, §77) | An image-to-video model (e.g. Wan 2.x / LTX-Video class; pick what's current and fits) on 5–10 panels, 3–5 s each | **GPU**: Modal (or Kaggle) | Should fit inside free credits; estimate before running (§2.6) |
| **Voice cloning** (optional) | A cloning TTS (e.g. XTTS / F5-TTS class) | GPU optional | Only if Kokoro's voices aren't enough |

**ComfyUI:** not in the codespace (CPU-only diffusion takes minutes per image, and SDXL/Flux don't fit in 8 GB). Prefer scripted, reproducible GPU jobs (diffusers/Modal functions) over a UI, in line with §54 and §66. If the owner wants to play with ComfyUI, use Lightning AI or Kaggle.

---

## 5. Free compute and API providers

Figures come from third-party roundups (Oct 2026) and they conflict. **Check each provider's official page before relying on a number**, and record what you find in `docs/PROGRESS.md`.

| Provider | Free tier (as reported) | Use it for |
|---|---|---|
| **GitHub Codespaces** | 120 core-h + 15 GB-month / month | Everything CPU (§4) |
| **Gemini API** (Google AI Studio, personal key) | Free tier with rate limits; has vision and long context | Panel understanding, story, script. Note: free-tier data may be used by Google to improve products. Tell the owner and let them decide |
| **Groq** (personal key) | Free tier, fast open models | Cheap text steps: OCR correction, classification |
| **Kaggle notebooks** | ~**30 GPU h/week** (T4/P100), ~9–12 h sessions; **idle time counts** | Batch GPU jobs: Magi on all pages, upscaling. Drive by notebook, save outputs as a dataset, pull back into the codespace |
| **Modal** | ~**$30/month credits** on Starter, no card (reported) | Serverless GPU functions called from the codespace: hero shots, voice cloning |
| **Google Colab** | Free T4, no published quota, not guaranteed | Backup GPU. Free tier restricts web UIs |
| **Lightning AI** | Some free GPU credits monthly (reports vary widely) | Persistent GPU box, ComfyUI experiments |
| **Hugging Face** | Model weights; free CPU Spaces; other people's GPU Spaces with a daily quota | Model downloads; quick trials via Space APIs |

The pipeline must not depend on any single provider. Use the provider interfaces from §63 (`LLMProvider`, `VisionProvider`, `OCRProvider`, `TTSProvider`, …) so a provider can be swapped by config.

---

## 6. Milestones

Each milestone ends with a **verified** output (§2.5) and a `docs/PROGRESS.md` entry. Don't start the next one until the current one is verified.

### M0: Bootstrap (≈2–4 h)
- Python package layout, trimmed from §93: `panelweaver/` with `ingestion/ panels/ ocr/ vision/ story/ script/ voice/ visuals/ timeline/ rendering/ qa/ providers/ schemas/`, plus `prompts/`, `tests/`. No web app yet.
- `pyproject.toml`, a CLI entry point (`pw`), pydantic schemas for: Document, Page, Panel, TextRegion, Character, Event, Beat, VisualSegment, Timeline (§10–50).
- `.gitignore` already covers `workspace/`, `renders/`, `.env`, caches. Keep it that way.
- GitHub Actions workflow: ruff + pytest only (§2.2).
- Smoke tests: FFmpeg renders a 3 s test clip; Kokoro speaks one sentence to a WAV.
- **Done when:** `pw --help` works, CI is green, the test clip and WAV exist and were checked.

### M1: Spec MVP, 60–120 s (§100) (≈6–10 h)
- 10–30 panels **prepared by hand** (cropped images in `workspace/`), from a source the owner approved.
- VLM scene descriptions → simple story → narration script (beats) → Kokoro → per-sentence timing → one panel per beat with a slow push-in → FFmpeg MP4.
- **Done when:** the 60–120 s MP4 exists and frames sampled at every beat boundary show the right panel for the narration. Record real timings for every stage.

### M2: Real ingestion and understanding (≈8–12 h)
- Input CBZ / PDF / image folder → pages → panels (Magi v2 or fallback) → **reading order** (RTL for manga, stored explicitly, §14) → text regions + OCR → speakers and character clusters, all with confidence (§59).
- Output `document.json`, `panels.json`, plus a **contact sheet per page** with numbered panel boxes, for checking.
- **Done when:** contact sheets for a full chapter show correct panels and order; low-confidence items are listed.

### M3: Story and hybrid script (≈6–10 h)
- Character registry (§19), scenes (§24), events with evidence links (§26–28), narrative plan (§31), beats with `event_id` + candidate panels (§34).
- Hybrid script: narrator lines + selected character lines (speaker from M2). Pronunciation dictionary (§40).
- Prompts versioned in `prompts/` (§94). LLM outputs validated against schemas.
- **Done when:** every beat traces to an event and panels (§35), and a chapter's script reads as a coherent retelling.

### M4: Voices and timing (≈4–6 h)
- Narrator voice + distinct Kokoro voices per main character (voice profiles, §39).
- Per-sentence synthesis → exact beat timestamps (§41). SRT + ASS subtitles (§53).
- Loudness normalization; narration vs dialogue levels balanced.
- **Done when:** a chapter's full audio track plays cleanly, and subtitles line up within ~100 ms at spot checks.

### M5: Visual director, timeline and renderer (≈10–14 h)
- Candidate ranking (§43), region focus using character boxes (§44), camera vocabulary (§45) chosen by beat type (§46), continuity (§47), repetition penalty (§48).
- `timeline.json` (§50) as the single source of truth → renderer builds the FFmpeg graph from it. Transitions, music bed with ducking under speech, a few SFX.
- Music/SFX: royalty-free sources whose licence allows use (CC0 preferred). Record the source and licence of each track in `docs/PROGRESS.md`.
- **Done when:** a full chapter renders at 540p and sampled frames match the narration; camera moves vary and look intentional.

### M6: QA pass (≈4–6 h)
- Automated checks (§57–58): beats without evidence, timeline gaps/overlaps, repeated panels, audio clipping/silence, subtitle drift.
- Contact sheet of one frame per beat for a human skim (the owner can review it on the phone).
- **Done when:** the QA report is clean or every warning is explained.

### M7: GPU polish (≈3–5 h of codespace time; GPU time on Kaggle/Modal)
- Upscale the source pages (Real-ESRGAN anime, Kaggle batch).
- 5–10 hero shots (image-to-video, Modal), each **optional** in the timeline with the static panel as fallback. Reject any clip with character or style drift (§77).
- Estimate credits before each run (§2.6).
- **Done when:** the hero shots are composited and the owner approves them from preview frames.

### M8: The demo (≈4–6 h)
- 15–20 min, 1080p, 16:9 final render of 1–2 manga.
- Deliver: the MP4 (on the forwarded port or as a GitHub release asset **only if** the source allows sharing; otherwise keep it in the codespace and the owner downloads it), a short write-up of how it was made, and the final timings and costs.
- **Done when:** the owner has watched it.

Total ≈ 50–75 h, which is more than one month's 60 free hours. That's fine: spread it over two months, or move part of M2 (Magi over all pages) and M7 to Kaggle.

---

## 7. Working agreement (for Claude)

1. Start each session by reading `docs/PROGRESS.md`, then continue the current milestone.
2. Plan the step, do it, verify it (§2.5), commit with a clear message, push, then update `docs/PROGRESS.md`.
3. Measure and record real timings and hours. Replace this guide's guesses with facts as you go.
4. Cache everything expensive by input hash + model + prompt version (§65). Re-running a stage must not redo upstream work.
5. Never let an LLM produce a shell or FFmpeg command directly. LLM → schema → our code → FFmpeg (§54).
6. Keep the owner in the loop on decisions in §2.6 and §8. Otherwise, use judgement and keep going.

---

## 8. Open decisions (ask the owner)

1. **Which manga for the demo?** Decide with the owner *before M1*. Options discussed:
   - **Freely-usable sources** (best for a public demo): *Give My Regards to Black Jack* (Shuho Sato made it free for secondary use: **verify the current terms, and whether they cover any English translation**); *Pepper&Carrot* by David Revoy (CC-BY 4.0, high-res, many languages; a webcomic, not manga, but a clean test source).
   - **A popular copyrighted manga**: a better showcase, but the demo must then stay private or unlisted, not monetized (§96, §118).
   - Japanese originals need Japanese OCR (`manga-ocr`) and translation; English scans don't. This choice affects M2.
2. **Music and SFX sources** (licence must allow use; record each).
3. **Narrator voice** pick from Kokoro's voices: render 3–4 samples of the same paragraph and let the owner choose on the phone.

---

## 9. How we got here (context from the planning chat)

- The owner wants to build without a laptop: phone → browser → this codespace → Claude Code.
- **Claude Code on the web (claude.ai/code) was ruled out.** The owner's Claude account is a company one, and web sessions would show up in the company's shared space. Claude Code in a codespace terminal runs like it does on a local machine.
- Codespaces were chosen because they're free (within §3.2), have a full Linux environment, and keep the owner's PC light.
- Compute was split: **CPU codespace for the whole core pipeline; GPU providers only for polish** (upscaling, hero shots, optional voice cloning). A GPU is not required for PanelWeaver to work.
- The demo target (15–20 min from 1–2 manga, with GPU extras) was agreed as a development demo, inside the providers' intended use (§2.2).
- The owner asked for this guide so the building session starts with the full plan and doesn't need the chat history.
