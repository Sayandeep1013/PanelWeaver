# PanelWeaver — License Register

**Week 0, measure 2** (register C-03, C-14). Every model, library, voice, font, track, dataset and service goes here **before** it's used.
**Posture: D-02 = personal / research** (owner, 2026-10-24). "Allowed" below means allowed under that posture. The commercial column is kept so that a later switch is a lookup, not a re-audit.
**Checked:** 2026-10-24, against primary sources (model cards, LICENSE files, official terms pages), web reading only. "Unverified" means we couldn't confirm it; it doesn't mean "fine".

Status: **use** = chosen · **candidate** = may be used, not chosen yet · **avoid** = don't use without revisiting this row.

---

## 1. Models

| Item | Use | Licence | Allowed (D-02)? | Commercial? | Conditions / notes | Commercial fallback | Status | Source |
|---|---|---|---|---|---|---|---|---|
| Magi v1 / v2 / v3 | Panels, bubbles, characters, speakers | Custom terms; no LICENSE file anywhere | **Yes** | **No**, the author licenses commercial use by email | HF cards: "unrestricted use in personal, research, non-commercial, and not-for-profit endeavors". The GitHub README is narrower: "academic research purposes only". The demo must not be monetised | panelforge (MIT, train it ourselves) · OpenCV gutters | candidate (measure 5) | huggingface.co/ragavsachdeva/magiv3 |
| PaddleOCR-VL-For-Manga (`jzhang533/…`, ~0.96B) | Japanese manga OCR | Apache-2.0 | Yes | Yes | Trained on Manga109-s crops: credit Manga109-s when publishing results. **The register's "2.91% CER" figure is not on the card; unverified.** We measure it ourselves (measure 5) | — | candidate | huggingface.co/jzhang533/PaddleOCR-VL-For-Manga |
| PaddleOCR-VL (base), PaddleOCR | OCR base / English OCR | Apache-2.0 | Yes | Yes | The base model's ERNIE-4.5-0.3B licence wasn't checked; per-model PP-OCR weight licences unverified | — | candidate | github.com/PaddlePaddle/PaddleOCR |
| manga-ocr (code + `manga-ocr-base`) | Japanese OCR | Apache-2.0 | Yes | Yes | Trained on Manga109-s: credit it | — | candidate | github.com/kha-white/manga-ocr |
| panelforge | Panel detection + reading order | MIT (code) | Yes | Yes | **No published weights**: we'd train it on Manga109-s and inherit those terms | — | candidate | github.com/DATGMAC/panelforge |
| Kokoro-82M + voice packs | Narrator and character voices | Apache-2.0 | Yes | Yes | The ja voices (Koniwa, CC BY 3.0) and ff_siwis (CC BY 4.0) need attribution; the English voices have no CC BY flags | — | **use** (planned, M1) | huggingface.co/hexgrad/Kokoro-82M |
| `kokoro` + `misaki[en]` | TTS runtime, G2P | Apache-2.0, but pulls **phonemizer-fork (GPL-3.0+)** and the espeak-ng loader | Yes | Yes to run; GPL affects only **distributing** the software, not the audio | The espeak fallback is on by default for English; if it fails, unknown words are **silently dropped** (`unk=''`). Check for this in M4 (A4 round-trip) | `fallback=None`, and handle unknown words via the pronunciation dictionary | **use** | github.com/hexgrad/misaki |
| Piper (`rhasspy/piper`) | TTS fallback | MIT, **archived 2025-10-06** | Yes | Yes | Successor `OHF-Voice/piper1-gpl` is GPL-3.0 | — | candidate | github.com/rhasspy/piper |
| Piper voices | TTS fallback voices | Per voice (repo says MIT) | Depends on the voice | Depends on the voice | **en_US-lessac: research only, "not for use as audio books"** → avoid. en_US-ljspeech: public domain | ljspeech | avoid lessac | huggingface.co/rhasspy/piper-voices |
| WhisperX (+ default wav2vec2 align model) | Word timings | BSD-2-Clause; align model MIT / Apache-2.0 | Yes | Yes | The pyannote diarisation model is CC-BY-4.0 with a user agreement; we don't need diarisation | — | candidate (M4) | github.com/m-bain/whisperX |
| stable-ts, faster-whisper, Whisper weights | Alignment / ASR (A4 round-trip) | MIT | Yes | Yes | — | — | candidate | github.com/jianfch/stable-ts |
| Real-ESRGAN code | Upscaling (M7) | BSD-3-Clause | Yes | Yes | — | — | candidate | github.com/xinntao/Real-ESRGAN |
| Real-ESRGAN anime weights | Upscaling (M7) | **No licence stated for the weights** | Probably | **Unverified** | — | Ask the author | candidate, unverified | GitHub releases |
| Wan 2.1 / 2.2 I2V | Hero shots (M7) | Apache-2.0 | Yes | Yes | Use restrictions on the card (illegal or harmful content); no claim over outputs | — | candidate (preferred) | huggingface.co/Wan-AI |
| LTX-Video / LTX-2 | Hero shots (M7) | LTXV Open Weights / LTX-2 Community licence | Yes | Yes under $10M annual revenue | **Outputs must be disclaimed as machine-generated**; a licence copy must be shipped | Wan | avoid (prefer Wan) | huggingface.co/Lightricks/LTX-Video |
| DINOv2 | Character embeddings (M3) | Apache-2.0 (code + weights) | Yes | Yes | — | — | candidate | github.com/facebookresearch/dinov2 |
| DINOv3 | Character embeddings | DINOv3 License (custom) | Yes | Yes | Weights only after a request; trade controls; publications must acknowledge DINO | DINOv2 | candidate | github.com/facebookresearch/dinov3 |
| FAISS | Similarity search | MIT | Yes | Yes | — | — | candidate | github.com/facebookresearch/faiss |
| XTTS-v2 | Voice cloning (optional) | Coqui Public Model License 1.0.0 | Yes (non-commercial) | **No**, and **outputs** are non-commercial too | coqui.ai/cpml is 404; no visible commercial route | Kokoro | avoid unless Kokoro falls short | huggingface.co/coqui/XTTS-v2 |
| F5-TTS | Voice cloning (optional) | Code MIT; **weights CC-BY-NC-4.0** | Yes | Weights no | — | Kokoro | avoid unless Kokoro falls short | github.com/SWivid/F5-TTS |

## 2. Datasets and sources

| Item | Use | Licence / terms | Allowed (D-02)? | Commercial? | Conditions / notes | Status | Source |
|---|---|---|---|---|---|---|---|
| Manga109 (109 vols) | Eval corpus | Custom; "academic purposes by non-commercial organizations" | **Probably not for the owner**: access needs an institutional email ("Gmail" is refused) | No | HF gate is manual, 2–3 days to a week | avoid | manga109.org/en/download.html |
| Manga109-s (87 vols) | Eval / training corpus (later) | Custom | Yes | **Results and models only**, never the pages | **Never put Manga109-s pages in a video.** "Must not be treated as products"; publish at most 20% of a volume; no redistribution; credit Manga109-s. Access form asks for name, address and affiliation (company or university); whether an unaffiliated individual qualifies is unverified | not chosen now (owner) | huggingface.co/datasets/hal-utokyo/Manga109-s |
| JMangaBench_Mixed | OCR benchmark | **Unverified: the repo returns HTTP 401** (private or removed) | — | — | The register cites it. The only visible sibling, `JMangaBench_Read`, is CC-BY-NC-SA-4.0. We rely on our own corpus | unavailable | huggingface.co/datasets/muscgab |
| *Give My Regards to Black Jack* | Corpus + demo candidate | *(pending §3 research)* | | | | pending | |

## 3. Software, fonts, services, music

*(Second research batch in progress; filled in below when it lands.)*

## 4. Open items

- **PanelWeaver's own licence:** the repo is public but has **no LICENSE file**, which means "all rights reserved". Owner decision (not blocking M0).
- Unverified items to resolve before first use: Real-ESRGAN anime weights, the PaddleOCR-VL-For-Manga CER claim, the ERNIE base licence, and Manga109-s eligibility for an individual.
