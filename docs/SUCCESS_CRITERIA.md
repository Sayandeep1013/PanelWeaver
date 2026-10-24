# PanelWeaver — Success Criteria and Camera Vocabulary

**Week 0, measure 4** (register C-05). Turns spec §102 into numbers and fixes the closed camera vocabulary.
**Status:** draft, 2026-10-24. The numbers are **starting values**: recalibrate after the first 3 renders. Every change goes in the change log at the bottom, with a date and a reason.

---

## 1. Numeric criteria

"Gate" = the first milestone where the criterion must pass (BUILD_GUIDE §6). Corpus = the eval corpus in `docs/EVAL_CORPUS.md`.

### 1.1 Understanding

| # | Criterion | How it's measured | Target | Gate |
|---|---|---|---|---|
| U1 | Panel detection recall | Greedy IoU matching at IoU ≥ 0.5 against corpus boxes | **> 90%** | M1 (detector choice), M2 |
| U2 | Panel detection precision | Same matching | **> 90%** | M1, M2 |
| U3 | Reading-order accuracy | Pairwise order accuracy over matched panels, per page, averaged | **> 95%** | M2 |
| U4 | Dialogue OCR CER | NFKC-normalised, whitespace removed, vs corpus transcriptions | **< 5%** (Japanese, vertical) · **< 3%** (English) | M2 (D-05) |
| U5 | Speaker attribution accuracy | Share of labelled dialogue bubbles assigned the right character (or correctly `unknown`) | **> 80%** | M3 |
| U6 | Character names in narration | Names that are not in the owner-confirmed registry (C-06) | **0** (hard gate) | M3 |

### 1.2 Script

| # | Criterion | How it's measured | Target | Gate |
|---|---|---|---|---|
| S1 | Evidence coverage | Beats with ≥ 1 `event_id` and ≥ 1 source panel (spec §35, C-07) | **100%** | M1 |
| S2 | Inferred-only beats | Beats whose only support is `INFERRED` (C-07) that weren't reviewed | **0** | M3 |
| S3 | Factual error rate | Owner audit: beats that contradict the source. Every beat in M1; a 50-beat sample per chapter later | **< 2%** of beats | M1 (scored), M3 (gate) |
| S4 | Generic lines | Owner audit: lines that could have been written without reading the comic (C-11) | **≤ 10%** of lines | M3 |
| S5 | Narration pace | Spoken words per minute over the whole video | **130–170 wpm** | M4 |

### 1.3 Audio

| # | Criterion | How it's measured | Target | Gate |
|---|---|---|---|---|
| A1 | Integrated loudness | `loudnorm` (print_format=json) on the final mix | **−16 LUFS ± 1** | M1 |
| A2 | True peak | Same | **≤ −1.5 dBTP** | M1 |
| A3 | Unintended silence | `silencedetect` (−45 dB, 1.5 s) outside planned pauses | **0** | M1 |
| A4 | Intelligibility | Whisper transcript of the TTS output vs the script text, WER | **< 5%** | M4 |
| A5 | Name pronunciation | Each glossary name heard once by the owner and marked OK | **100%** checked | M4 |
| A6 | Music under speech | Music bed level vs narration while narration plays | **≥ 12 dB below** | M5 |

### 1.4 Timing and timeline

| # | Criterion | How it's measured | Target | Gate |
|---|---|---|---|---|
| T1 | Cuts inside a word | Shot boundaries that fall strictly inside a word's [start, end] | **0** | M1 |
| T2 | Cut placement | Shot boundaries within 150 ms of a sentence or word boundary | **≥ 95%** | M4 |
| T3 | Subtitle error | Cue start vs word timestamp, spot checks | **≤ 100 ms** | M4 |
| T4 | Timeline integrity | Gaps or overlaps on the video track; audio and video durations differ by more than 1 frame | **0** | M1 |
| T5 | Black frames | `blackdetect` d=0.3, pix_th=0.05, excluding planned fades at start and end | **0** | M1 |
| T6 | Decode errors | `ffmpeg -v error -i video.mp4 -f null -` | **0** | M1 |

### 1.5 Visual direction

| # | Criterion | How it's measured | Target | Gate |
|---|---|---|---|---|
| V1 | Panel matches narration | Owner judgement, one frame per beat on a contact sheet | **≥ 90%** of beats | M1 (scored), M5 (gate) |
| V2 | Shot length | Median shot duration | **3–6 s** (recalibrate against the reference video) | M5 |
| V3 | Shot-length variety | Coefficient of variation of shot durations | **≥ 0.35** (detects monotony) | M5 |
| V4 | Longest shot | Any shot without a motion or framing change | **≤ 10 s** | M5 |
| V5 | Motion variety | Same motion in consecutive shots | **≤ 2** in a row; no motion > 40% of shots in any 2-minute window | M5 |
| V6 | Panel repetition | A panel shown more than twice | Only with a different region or a recorded reason (spec §48) | M5 |
| V7 | Smooth motion | (a) Unit test: crop rectangles are computed in floats and change monotonically. (b) The owner sees no shimmer on the fine-line fixture at 1080p | Pass both | M1 |

### 1.6 The overall bar ("not a slideshow")

The register's version (N = 10 videos, > 60% pass) assumes many videos; we make one demo. Adapted:

| # | Criterion | How it's measured | Target | Gate |
|---|---|---|---|---|
| O1 | Blind viewer test | ≥ 5 viewers not involved in the project each watch a 3-minute excerpt (random start) and answer one question: *"Does this feel like a directed video, or a slideshow of images?"* | **≥ 60%** say "directed" | M8 |
| O2 | Attention drops | The same viewers mark the second where their attention dropped | **≤ 1 per 3 minutes** on average | M8 |
| O3 | Owner A/B | The owner watches 3 variants of the same 60 s segment in random order, not knowing which is which, and picks the best | Recorded each time camera or pacing rules change (C-05) | M5 onward |

### 1.7 Output format (fixed)

1920×1080, 16:9, 30 fps constant, H.264 High, yuv420p, AAC 48 kHz stereo, MP4. Previews: 960×540, same everything else. Coordinates in every schema are normalised to [0, 1] (spec §56).

---

## 2. Camera vocabulary (closed, v1)

v1 has **no free-form camera planning**. The visual director (M5) picks one entry per shot, using the rules below. The renderer accepts nothing else.

### 2.1 The 8 entries

| Entry | Kind | What it does | Parameters (start values) |
|---|---|---|---|
| `hold` | motion | Static framing of a whole panel or region | — |
| `static-with-subtitle` | motion | `hold`, plus the spoken line's subtitle given visual priority (character dialogue in the hybrid script) | — |
| `push` | motion | Slow zoom in toward a focus point | strength **0.02–0.05** (relative scale change over the shot) |
| `pull` | motion | Slow zoom out from a focus point | strength **0.02–0.05** |
| `pan` | motion | Traverse a panel that overflows the frame | `direction` ∈ {left, right, up, down}; only when the overflow is ≥ 10% in that axis; speed **≤ 0.06 frame-heights/s** |
| `cut` | transition | Hard cut to the next shot | — |
| `crossfade-to-region` | transition | Dissolve to the next framing: a region of the same panel, or the next panel | duration **0.4–0.8 s** |
| `fade` | transition | Fade from or to black, **only** at the video's start and end | 0.5–1.0 s |

**Deviation from the register, needs the owner's OK.** The register lists `pan-left` and `pan-right` as separate entries, and has no `fade`. Its list comes from make-motion-comic, which renders 9:16, where wide panels are panned sideways. We render 16:9, and manga panels are mostly taller than the frame, so vertical pans are the common case. Here the two pans become one `pan` entry with a direction parameter, and the freed slot goes to `fade` for the opening and closing. The vocabulary stays closed at 8.

### 2.2 Rules that apply to every shot

- **One motion per shot.** Never combine push and pan (C-10).
- **Easing:** cosine ease-in-out on every motion.
- **Duration:** at least 1.0 s per shot (0.6 s for `impact` beats); at least 1.2 s for `hold`.
- **Transitions:** `cut` inside a scene; `crossfade-to-region` at scene changes or region changes; `fade` only at the video's start and end.
- **Anti-jitter render recipe** (from the register, converted to 16:9): working canvas 4608×2592 → motion rendered at 3840×2160 with sub-pixel float crop math → Lanczos downscale to 1920×1080 → 30 fps. Verify it in M1 on a fine-line fixture (V7).

### 2.3 Selection by beat intent

Each beat carries one intent from spec §75. The first motion listed is the default; the others are allowed alternatives.

| Beat intent | Motion | Typical transition in |
|---|---|---|
| `establish` | `hold` (full panel) · `pull` | `crossfade-to-region` (new scene) |
| `focus` | `push` toward the region · `hold` on the region | `crossfade-to-region` |
| `dialogue` | `static-with-subtitle` · `hold` | `cut` |
| `escalate` | `push` · `pan` | `cut` |
| `reveal` | `pull` · `hold` | `cut` |
| `impact` | `hold`, short (0.6–1.2 s) · `push` at 0.05 | `cut` |
| `react` | `push` (≤ 0.03) · `hold` | `cut` |
| `transition` / `resolve` | `pull` · `hold` | `crossfade-to-region` |

`pan` is also allowed for any intent when the chosen framing overflows the frame and the beat lasts long enough to keep under the speed limit.

---

## 3. Change log

| Date | Change | Why |
|---|---|---|
| 2026-10-24 | First draft | Week 0 measure 4 |
