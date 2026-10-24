# PanelWeaver — Build Guide (start here)

**Written:** 2026-10-24, from a planning conversation between the owner (Sayandeep1013) and Claude.
**Audience:** the Claude Code session that builds PanelWeaver, and the owner.
**Status:** nothing is built yet. The repo holds the spec, the risk register, this guide, the codespace setup and `scripts/cs`.

---

## 0. Read this first (for Claude)

Three documents. Read all three before writing any code:

| Document | What it is |
|---|---|
| `PanelWeaver — AI Comic-to-Video Production System _ Initial Master Project Specification v0.1.md` (repo root) | **The vision and architecture.** Pipeline, data model, principles. "§N" below refers to it. |
| `PanelWeaver — Risk & Concerns Register v0.1.md` (repo root) | **What must be measured and decided before building.** 20 concerns (C-01…C-20), the Week 0 measures, the decision log (D-01…D-10). "C-NN" / "D-NN" below refer to it. |
| `docs/BUILD_GUIDE.md` (this file) | **How we execute.** Where code runs, what compute does what, milestones to the demo, ground rules. |

How they fit together:
- **Architecture:** the spec. The register says plainly: *"The spec is a good architecture document and a bad plan."* Nothing here argues with the architecture.
- **What to measure first and what's in or out of v1:** the register. Its Week 0 blocking measures come before pipeline code (M0 below).
- **Process, environment, scope of the demo:** this guide.

The spec's core rules stand:
- **Understand first. Generate second. Direct third. Render last.** (§1)
- Every stage writes an inspectable artifact: `document.json → panels.json → story.json → script.json → voice/ → visual_plan.json → timeline.json → video.mp4` (§5).
- **AI decides what the video contains; deterministic code renders it** (§54). LLM output goes through validated schemas, never straight into shell or FFmpeg commands.
- **Motion graphics first, generative video later** (§76–77). The original artwork is the main visual.

And the register's: **stop designing, start measuring.** Everything expensive must become falsifiable before it gets scheduled.

Keep a running log in `docs/PROGRESS.md` (create it): what was done, what was measured, decisions, hours used, what's next. Commit and push small steps often.

---

## 1. The goal: one demo video

Build PanelWeaver to the point where it produces **one convincing demo video**, end to end.

| | |
|---|---|
| **Length** | 15–20 minutes |
| **Source** | 1–2 manga (chapters or a short volume). **Not chosen yet**, see §8 |
| **Format** | 16:9 landscape, 1080p, 30 fps, MP4 (H.264 + AAC). Normalized coordinates (§56) so 9:16 is possible later |
| **Narration** | **Hybrid** (§37, D-04, decided by the owner 2026-10-24): one narrator retells the story; key lines are spoken in character voices |
| **Also in the video** | Subtitles, background music, a few sound effects, intentional camera moves (§45–46) |
| **Extras (GPU)** | Upscaled artwork; a handful of short "hero shot" animations. Optional polish, never required for the video to work |

**The bar (§102, made numeric in M0):** a person can watch it without thinking "this is just an AI slideshow."

**Expected pace (register §0.2):** an ugly but real `comic → MP4` in 1–2 weeks after the Week 0 gates; "watchable" in 6–10 weeks, mostly gated by the owner's taste feedback (camera and pacing have no ground truth, C-05), not by compute.

---

## 2. Ground rules

### 2.1 Accounts and keys (important)
- Claude Code (on the PC and in the codespace) is logged in with the owner's **work** Claude account. Use it **only as the coding assistant**.
- **Never use that account, or any company key, as PanelWeaver's runtime model.** All model calls made *by the pipeline* use the owner's **personal free-tier keys** (§5).
- Keys live in **Codespaces secrets** (github.com/settings/codespaces → Secrets, scoped to this repo) and reach the codespace as environment variables. The pipeline only runs in the codespace, so keys never need to be on the PC. Never write a key into a file, a commit, a log or `docs/PROGRESS.md`.
- Ask the owner to add a secret when one is needed, and say exactly which name to use (e.g. `GEMINI_API_KEY`).

### 2.2 Compute: use it the way it's meant to be used
- **The codespace is for development**: code, tests, test renders, and rendering the demo while developing it.
- **GitHub Actions is CI only**: lint, tests, the render QA gate on tiny fixtures (measure 8). **Never render real videos or run the pipeline in Actions.**
- GPU providers (Kaggle, Modal, etc.) are used within their free tiers and their rules: no crypto mining, no always-on servers, no web UIs where a provider forbids them (Colab free restricts web UIs).

### 2.3 Copyright and licences (§96, C-03, C-14, C-17)
- **This repo is public.** Never commit manga pages, panels, generated audio of copyrighted text, eval images, or renders containing copyrighted artwork. Annotations (boxes, labels) may be committed; the images may not.
- Source material and outputs live in `workspace/` and `renders/`, which are git-ignored. Check `.gitignore` before every commit that touches new paths.
- **Ask the owner before downloading any source material.**
- Every model, voice, font and music track goes into the **License Register** (Week 0 measure 2) before it's used.

### 2.4 How the owner works
Two setups, same repo (details in §3):
- **From the PC (main):** a Claude Code session in `D:\Projects\PanelWeaver` on Windows edits code locally and drives the codespace over SSH.
- **From a phone (sometimes):** the owner opens the codespace in a phone browser and runs Claude Code inside it.

Either way:
- Keep messages short and scannable. Put long detail in `docs/PROGRESS.md` and point to it.
- Run commands yourself. Don't ask the owner to type long ones.
- Show results as images: extract frames or contact sheets as PNGs and look at them. For the MP4 itself, serve `renders/` on port 8000 in the codespace (phone), or copy a small 540p preview down to `pull/` (PC).

### 2.5 Done means verified
"The code ran" is not done. A step is done when its **output was checked**:
- JSON artifacts validate against their schema.
- Visual steps: render a contact sheet or sample frames and **look at them** (you can read images).
- Audio: check duration, loudness (`ffmpeg -af ebur128` / `loudnorm`), and a transcript round-trip if possible.
- Video: sample frames at several timestamps, check A/V sync at beat boundaries.

Say plainly what was and wasn't verified. "Unconfirmed" is a fine answer; a confident wrong one is not.

### 2.6 Ask before
- downloading source material,
- spending GPU credits on a run expected to cost more than about **$3**, or anything that could exceed a free tier,
- adding any paid service, or anything that needs a card,
- deleting renders the owner hasn't seen,
- creating or publishing a claude.ai **Artifact**. Default to a normal local file (Markdown in `docs/`, or a standalone styled HTML file).

### 2.7 The owner's preferences (carried over from other projects)
- **Keep the PC light.** Nothing heavy is installed on the Windows PC: no Python environments for the pipeline, no models, no SDKs, no browser downloads, no caches. All of that lives in the codespace. The PC holds the git checkout and small previews only.
- **No leftovers.** Delete previews in `pull/` once looked at, don't pile up preview HTML pages, and clean temporary files in the same session.
- **Branch names never look like release tags** (`vX.Y.Z`). Use `feat-…`, `fix-…`, `rel-…`.
- **Windows tool quirk:** when writing files, backslash-u escape sequences in tool input get turned into the literal character. In Python patch scripts, build escapes with `chr(92) + 'u…'` and use raw strings for regexes; after writing, scan for stray control or invisible characters.

---

## 3. The environment

### 3.1 Two setups, one source of truth
**GitHub is the source of truth.** Code moves only through commits:

```text
PC  D:\Projects\PanelWeaver  ── edit, commit ──►  GitHub  ◄── git pull ──  codespace /workspaces/PanelWeaver
        (code only, light)       git push                                    (runs everything heavy)
                                                                             workspace/  renders/  logs/  (never committed)
```

- **Edit code in one place at a time.** In the PC setup, edit only on the PC and never in the codespace (outputs excepted). If a phone session committed in the codespace, `scripts/cs sync` pulls it to the PC first.
- **Never run two Claude sessions on this repo at once** (PC + phone). They will conflict.

### 3.2 The PC setup: `scripts/cs`
The local session drives the codespace with `scripts/cs` (bash; run it from the repo root with the Bash tool). It finds the codespace by repo, and any command wakes a stopped codespace (measured: 18 s from fully stopped to command done):

| Command | Does |
|---|---|
| `scripts/cs status` | Show the codespace and its state |
| `scripts/cs run "<cmd>"` | Run a command in `/workspaces/PanelWeaver` and wait for it |
| `scripts/cs sync` | `git pull` on the PC, `git push`, then `git pull --ff-only` in the codespace |
| `scripts/cs job <name> "<cmd>"` | Start a long job **detached** (survives SSH disconnects). Log in `logs/<name>.log` |
| `scripts/cs log <name> [lines]` | Tail a job's log |
| `scripts/cs jobs` | List running jobs |
| `scripts/cs get <path> [dest]` | Copy a file from the codespace repo to `pull/` on the PC |
| `scripts/cs stop` | Stop the codespace (saves free hours) |

Measured on 2026-10-24:
- **Each call costs about 7 s** of SSH setup, so **batch work into one `run`** (`cmd1 && cmd2 && …`) instead of many small calls.
- Commands travel base64-encoded, so any quoting works (quotes, `$`, pipes).
- Anything over about a minute goes through `job`, never `run`: a dropped connection kills a `run`, not a `job`.
- `get` copies one file at a time, and `-e` expansion allows a remote glob. Keep pulled files small (PNG frames, contact sheets, 540p clips) and delete them after looking.

Typical loop: edit locally → commit → `scripts/cs sync` → `scripts/cs run "pytest -q"` or `scripts/cs job render "python -m panelweaver …"` → `scripts/cs get renders/frames/0001.png` → look → iterate. At the end of a session: push, then `scripts/cs stop`.

### 3.3 The codespace
A GitHub Codespace: a Linux VM in GitHub's cloud. It's built from `.devcontainer/`:
- `Dockerfile`: Python 3.12 (Debian bookworm), **ffmpeg 5.1**, **espeak-ng** (Kokoro TTS phonemes), **Noto CJK fonts**. The base image's broken Yarn apt source is removed there. Keep that line, or every `apt-get` fails.
- `devcontainer.json`: the sshd feature (needed by `scripts/cs`), port 8000 for previews.
- `setup.sh` (post-create): Claude Code, `workspace/` and `renders/` folders.

New system packages go in the `Dockerfile`, user-level tools in `setup.sh`, so the next codespace has them too. Python dependencies go in `pyproject.toml`. **If the codespace ever starts in "recovery mode"** (a bare Alpine container), the build failed: read `/workspaces/.codespaces/.persistedshare/creation.log`.

Verified working on 2026-10-24: ffmpeg 5.1.9, espeak-ng 1.51, Python 3.12.11, Noto CJK fonts, Claude Code 2.1.310, a detached ffmpeg job, and file copy back to the PC.

### 3.4 Limits (GitHub Free personal account; verify on GitHub's billing page)
| Limit | Value | What it means |
|---|---|---|
| Compute | **120 core-hours / month** | **~60 h on this 2-core machine** (30 h on 4-core) |
| Storage | **15 GB-month** | Keep the codespace's disk use well under ~10 GB. Delete old renders and intermediates |
| Machine | 2 cores, 8 GB RAM, 32 GB disk | Enough for the whole CPU pipeline (§4). Not for diffusion or video models |
| Idle timeout | **4 h** (the max) | It stops 4 h after the last activity. **Run `scripts/cs stop` at the end of every session**, or an idle codespace burns up to 4 h |
| Retention | 30 days after stopping | A codespace stopped for 30 days is deleted. Uncommitted work is lost; outputs in `workspace/` and `renders/` too, so nothing irreplaceable lives only there |
| No GPU | | GPU work goes to §5 providers |

Budget the 60 h. Log hours used per session in `docs/PROGRESS.md`.

### 3.5 Phone quickstart (owner)
1. Phone browser → **github.com/codespaces** → open **PanelWeaver** (desktop-site mode works best).
2. Terminal: `git pull`, then `claude`. First time: open the login link, approve, paste the code back.
3. Say what to do, e.g. *"Read docs/PROGRESS.md and continue."*
4. When done: commit and push, then ⋯ → **Stop codespace**.

---

## 4. Compute plan: what needs a GPU

**The core pipeline runs on CPU in the codespace. A GPU is only for polish.** These timings are planning guesses: **measure the real ones** and record them.

| Stage | First choice → fallback | Where | Notes |
|---|---|---|---|
| Ingest (§9) | Pillow, `zipfile`, PyMuPDF | CPU | Seconds |
| Panels, bubbles, characters, speakers (§12, §17–18) | Benchmark on our corpus (measure 5): **Magi v3** (best fit for §12–22, but **non-commercial / research-only licence**, C-03) or Magi v2 (check licence) → classical OpenCV gutter detection | CPU, or a Kaggle GPU batch | Magi is usable **only if D-02 = personal/research**. Guess ~5–15 s/page on CPU |
| OCR (§15–16) | **PaddleOCR-VL-0.9B-For-Manga** (register: 2.91% CER on JMangaBench) → `manga-ocr` (Japanese) / PaddleOCR (English) → VLM verification | CPU (GPU if too slow) | Check its licence for the License Register |
| Scene and character understanding (§22) | Vision LLM via **personal free-tier API** (Gemini), cached by image hash (§65) | API | Register: VLM images cost $0.0011–0.03 each on paid tiers; free-tier limits apply |
| Story, beats, script (§25–35) | Text LLM via personal free-tier API (Gemini / Groq) | API | The story engine is the differentiator (C-02, register §0.3): spend effort here |
| Narrator + character voices (§38–39) | **Kokoro-82M** (Apache-2.0; several distinct voices, enough for hybrid) → Piper | CPU | Expect real time or faster: measure |
| Timing (§41, C-09) | Synthesize **per sentence** (the audio file's length *is* the timestamp); word-level from the TTS's native timestamps or forced alignment (WhisperX / stable-ts) | CPU | Register: word timestamps are standard now |
| Visual plan, timeline (§42–50) | Our own Python + schemas, the closed 8-motion vocabulary (measure 4) | CPU | Seconds |
| Render (§54–55, C-10) | FFmpeg; avoid zoompan's integer-pixel jitter (supersample, then scale down, or crop with sub-pixel math) | CPU | 1080p on 2 cores: guess 0.5–1× real time ≈ 20–40 min per full render. **Iterate at 540p** |
| **Upscale artwork** (polish) | Real-ESRGAN (anime model) | **GPU**: Kaggle batch | |
| **Hero shots** (polish, §77) | An image-to-video model (Wan 2.x / LTX-Video class, whatever is current and licensed) on 5–10 panels, 3–5 s each | **GPU**: Modal (or Kaggle) | Estimate credits first (§2.6). Reject any clip with character or style drift |
| **Voice cloning** (optional) | XTTS / F5-TTS class | GPU optional | Only if Kokoro's voices aren't enough |

**ComfyUI:** not in the codespace (CPU diffusion takes minutes per image, and SDXL/Flux don't fit in 8 GB). Prefer scripted, reproducible GPU jobs (diffusers on Modal) over a UI, per §54 and §66. For ComfyUI experiments, use Lightning AI or Kaggle.

---

## 5. Free compute and API providers

These figures come from third-party roundups (Oct 2026) and they conflict. **Check each provider's official page before relying on a number**, and record what you find.

| Provider | Free tier (as reported) | Use it for |
|---|---|---|
| **GitHub Codespaces** | 120 core-h + 15 GB-month / month | Everything CPU (§4) |
| **Gemini API** (AI Studio, personal key) | Free tier with rate limits; vision, long context | Panel understanding, story, script. Free-tier data may be used by Google to improve products: tell the owner, let them decide |
| **Groq** (personal key) | Free tier, fast open models | Cheap text steps: OCR correction, classification |
| **Kaggle notebooks** | ~**30 GPU h/week** (T4/P100), 9–12 h sessions; **idle time counts** | Batch GPU jobs (Magi over all pages, upscaling). Outputs saved as a dataset, pulled back into the codespace |
| **Modal** | ~**$30/month credits** (Starter, no card, reported) | Serverless GPU functions called from the codespace: hero shots, voice cloning |
| **Google Colab** | Free T4, no published quota, not guaranteed | Backup GPU. Free tier restricts web UIs |
| **Lightning AI** | Some free GPU credits monthly (reports vary widely) | Persistent GPU box; ComfyUI experiments |
| **Hugging Face** | Weights; free CPU Spaces; other people's GPU Spaces with a daily quota | Model downloads, quick trials |

No single provider may become a hard dependency: put providers behind interfaces (§63), but keep them thin (C-15 warns about the "abstraction tax").

---

## 6. Milestones

Each milestone ends with a **verified** output (§2.5) and a `docs/PROGRESS.md` entry. Don't start the next until the current one is verified.

### M0: Week 0, the register's gates (before any pipeline code)
From register Part 2. **Measures 1–4 are blocking.**
1. **Eval corpus** (C-01): register says Manga109-s (commercially usable, needs an access request) plus private chapters; label panel boxes, dialogue, reading order, and "which panel at second N" for 3 reference videos. Images stay in `workspace/`, annotations are versioned. The register estimates 4–6 days. Agree the size with the owner: a smaller first corpus is fine if it gives a numeric pass/fail bar.
2. **License Register** (C-03): dependency → licence → commercial OK? → fallback → cost. Every model, voice, font and track.
3. **The two scope decisions in writing** (owner): D-01 manga-only vs manhwa (register recommends manga-only; the demo is manga), D-02 personal/research vs commercial (decides whether Magi is allowed).
4. **Numeric success criteria** for §102, and adopt the closed 8-motion camera vocabulary (C-05).

Then the non-blocking ones that make later milestones cheaper: **7** (stage result envelope: status, confidence, cost, latency, provider, model_id, prompt_hash, error_class), **8** (render QA gate in CI: ffprobe, blackdetect, loudnorm on tiny fixtures), **10** (minimum repo scaffold: one Python package, `schemas/`, SQLite, CLI; nothing else, C-13).
- **Done when:** measures 1–4 are written down in the repo, D-01, D-02 and D-04 are filled in the register's decision log, and the scaffold's CI is green.

### M1: Ugly but real end-to-end (spec MVP, §100)
- An owner-approved source → pages → panels (simplest detector that passes the corpus bar) → OCR → VLM descriptions → simple script → Kokoro → per-sentence timing → one panel per beat with a slow push-in → MP4.
- **Done when:** a 60–120 s MP4 exists, frames sampled at every beat boundary show the right panel, and it's scored against the M0 criteria. Record real timings for every stage.

### M2: Ingestion and understanding at chapter scale
- Measure 5: benchmark OCR and panel detection on the corpus (2-day timebox), choose D-05 and D-07.
- Reading order (RTL, stored explicitly, §14), speakers, character clusters, all with confidence (§59). Contact sheets per page with numbered panels.
- **Done when:** a full chapter's contact sheets are correct, and low-confidence items are listed.

### M3: The story engine and the hybrid script
- Character registry (§19), scenes (§24), events with evidence links (§26–28), narrative plan (§31), beats with `event_id` + candidate panels (§34). Name glossary (measure 9).
- Hybrid script: narrator lines + selected character lines. Prompts versioned in `prompts/` (§94), outputs validated against schemas.
- **Done when:** every beat traces to an event and its panels (§35), and the script reads as a coherent retelling. This is where the product's value is (C-02): give it the time.

### M4: Voices and timing (C-09)
- Narrator + distinct Kokoro voices per main character (§39). The owner picks the narrator from 3–4 samples of the same paragraph.
- Exact beat timestamps, SRT + ASS subtitles (§53), loudness normalized, narration vs dialogue balanced.
- **Done when:** a chapter's audio plays cleanly and subtitles line up within ~100 ms at spot checks.

### M5: Visual director, timeline and renderer (C-10)
- Candidate ranking (§43), region focus using character boxes (§44), the 8-motion vocabulary chosen by beat type (§45–46), continuity (§47), repetition penalty (§48).
- `timeline.json` (§50) is the single source of truth; the renderer builds the FFmpeg graph from it. Transitions, music bed ducked under speech, a few SFX (sources in the License Register, D-08).
- **Done when:** a full chapter renders at 540p, sampled frames match the narration, and motion is smooth (no jitter) and varied.

### M6: QA pass
- Automated checks (§57–58): beats without evidence, timeline gaps or overlaps, repeated panels, clipping or silence, subtitle drift.
- One frame per beat as a contact sheet for the owner to skim.
- **Done when:** the QA report is clean or every warning is explained.

### M7: GPU polish
- Upscale source pages (Kaggle). 5–10 hero shots (Modal), each **optional** in the timeline with the static panel as fallback.
- **Done when:** the owner approves the hero shots from preview frames.

### M8: The demo
- 15–20 min, 1080p, 16:9 final render of 1–2 manga.
- Deliver the MP4: a 540p copy pulled to the PC, or the full file served on port 8000. It becomes a public release asset **only if** the source allows sharing. Add a short write-up of how it was made, with final timings and costs.
- **Done when:** the owner has watched it.

Rough codespace time from M1 on: ~50–75 h, more than one month's free 60 h. Spread it over two months, or move batch work (Magi over all pages, upscaling) to Kaggle.

---

## 7. Working agreement (for Claude)

1. Start every session by reading `docs/PROGRESS.md`, and in the PC setup run `scripts/cs sync` first.
2. Plan the step, do it, verify it (§2.5), commit with a clear message, push, then update `docs/PROGRESS.md`.
3. Measure and record real timings and hours. Replace this guide's guesses with facts as you go.
4. Cache everything expensive by input hash + model + prompt version (§65). Re-running a stage must not redo upstream work.
5. Never let an LLM produce a shell or FFmpeg command directly: LLM → schema → our code → FFmpeg (§54).
6. Decisions in §2.6 and §8 go to the owner. Otherwise, use judgement and keep going.
7. End every session with: push, `docs/PROGRESS.md` updated, `pull/` cleaned, `scripts/cs stop`.

---

## 8. Open decisions (owner)

| | Decision | Status |
|---|---|---|
| D-01 | Input scope: manga-only vs manhwa/webtoon | **Decided 2026-10-24: manga-only** (register decision log) |
| D-02 | Distribution: personal/research vs commercial | **Decided 2026-10-24: personal/research.** Magi may be used; keep a commercial fallback recorded per capability |
| D-04 | Narration strategy | **Decided 2026-10-24: hybrid.** Record it in the register's decision log |
| Source | Which manga for the demo | **Open: ask before M1.** Freely-usable: *Give My Regards to Black Jack* (Shuho Sato allowed free secondary use; **verify current terms and whether they cover any English translation**); *Pepper&Carrot* (CC-BY 4.0 webcomic, a clean test source). A popular copyrighted manga: better showcase, but the demo stays private or unlisted (§96, §118, C-14). Japanese originals need Japanese OCR and translation (C-11) |
| D-08 | Music and SFX source | Open. The licence must allow use; record each track |
| Corpus size | How big a first eval corpus (M0, measure 1) | **Decided 2026-10-24: small first**, ~3 chapters (~60 pages), 1 reference video; grow toward 20 chapters as M2 needs. Sources allowed: *Give My Regards to Black Jack* (after its terms are verified) and the owner's own chapters. Plan in `docs/EVAL_CORPUS.md` |

---

## 9. How we got here (context from the planning chat)

- The owner wants to build without a laptop session tied to a browser: Claude Code on the PC drives a cloud machine, and a phone can take over when away from the PC.
- **Claude Code on the web (claude.ai/code) was ruled out.** The owner's Claude account is a company one, and web sessions would show up in the company's shared space. Claude Code run locally, or inside a codespace terminal, is fine.
- **Codespaces were chosen** because they're free (§3.4), give a full Linux machine, and keep the PC light. `scripts/cs` and the sshd feature were added so the PC session can drive it without a browser.
- **Compute split:** CPU codespace for the whole core pipeline; GPU providers only for polish (upscaling, hero shots, optional voice cloning). A GPU is not required for PanelWeaver to work.
- The demo target (15–20 min from 1–2 manga, with GPU extras) was agreed as a development demo within the providers' intended use (§2.2).
- The owner chose: 16:9, hybrid narration, source decided later, and the register committed to the repo so every session shares the same plan.
