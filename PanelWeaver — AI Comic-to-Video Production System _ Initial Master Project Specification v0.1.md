# PanelWeaver

## AI-Directed Sequential Visual Storytelling & Comic-to-Video Production System

**Project:** PanelWeaver  
**Repository:** `PanelWeaver`  
**Document:** Initial Master Project Specification  
**Version:** `0.1`  
**Status:** Initial Architecture / Research Foundation  
**Primary Domain:** AI, Computer Vision, Multimodal Understanding, Narrative Generation, TTS, Video Editing, Agentic Systems  
**Primary Target Media:** Manga, Manhwa, Manhua, Webtoons, Comics, Graphic Novels

---

# 1. Executive Summary

PanelWeaver is an AI-powered system designed to transform sequential visual storytelling—particularly manga, manhwa, manhua, webtoons and comics—into coherent narrated audiovisual experiences.

The system is intended to automate the majority of the production process behind the type of videos commonly seen as:

- manga recaps
- manhwa recaps
- comic walkthroughs
- narrated comic stories
- cinematic comic summaries
- accessibility-oriented comic narration
- AI-assisted comic adaptations

The system should not be treated as a simple:

```text
Images → LLM → Voice → Video
```

That architecture is too shallow.

PanelWeaver should instead treat the comic as a **structured narrative source** and progressively transform it through several machine-readable representations:

```text
RAW COMIC
    ↓
DOCUMENT MODEL
    ↓
VISUAL UNDERSTANDING
    ↓
TEXT / CHARACTER / SCENE MODEL
    ↓
STORY MODEL
    ↓
NARRATIVE MODEL
    ↓
SCRIPT
    ↓
AUDIO
    ↓
VISUAL DIRECTION
    ↓
EDIT DECISIONS
    ↓
TIMELINE
    ↓
RENDERED VIDEO
```

The core philosophy is:

> **Understand first. Generate second. Direct third. Render last.**

The system should preserve the ability to inspect, modify, regenerate and validate every stage.

---

# 2. The Vision

The long-term goal is not merely to create AI-generated recap videos.

The broader vision is:

> **Build an AI system capable of understanding sequential visual storytelling and transforming it into another coherent audiovisual medium.**

This distinction is important.

The same underlying system could eventually support:

```text
Comic
 ↓
Narrated Video
```

but also:

```text
Comic
 ↓
Accessible Audio Description
```

```text
Comic
 ↓
Screenplay
```

```text
Comic
 ↓
Audiobook-style narration
```

```text
Comic
 ↓
Animated motion-comic
```

```text
Comic
 ↓
Short-form video
```

```text
Comic
 ↓
Interactive story
```

Therefore, "manga recap generator" is an implementation/use case.

**PanelWeaver is the underlying storytelling engine.**

---

# 3. Why "PanelWeaver"?

The name reflects the fundamental operation of the system.

A comic contains many separate pieces:

- panels
- dialogue
- narration
- characters
- expressions
- actions
- environments
- objects
- transitions
- events

PanelWeaver takes these pieces and **weaves them into a continuous narrative experience**.

It does not merely concatenate panels.

It determines:

```text
What happened?
        ↓
What matters?
        ↓
How should it be explained?
        ↓
What should the viewer see?
        ↓
When should they see it?
        ↓
How should the camera move?
        ↓
How should audio and visuals interact?
```

---

# 4. The Core Problem

Producing a high-quality narrated comic video manually requires a human to repeatedly perform several tasks.

### Source preparation

- acquire the source
- extract pages
- identify reading order
- split pages into panels
- clean/normalize artwork

### Understanding

- read dialogue
- identify narration
- identify characters
- identify actions
- understand expressions
- identify locations
- connect events between panels

### Writing

- understand the complete chapter
- determine important events
- construct a narrative
- rewrite dialogue where appropriate
- maintain character names
- maintain continuity

### Audio

- record narration
- edit mistakes
- control pacing
- handle pronunciation
- synchronize dialogue

### Video

- select panels
- crop panels
- zoom
- pan
- transition
- add subtitles
- add music
- add SFX
- synchronize visuals

### Quality control

- watch the entire result
- find mistakes
- replace visuals
- fix narration
- re-record sections
- re-render

PanelWeaver exists to automate these repetitive operations while preserving creative control.

---

# 5. The Fundamental Design Principle

PanelWeaver should **never collapse the entire process into one AI call**.

Instead:

```text
Input
 ↓
Understanding
 ↓
Structured State
 ↓
Generation
 ↓
Structured State
 ↓
Direction
 ↓
Structured State
 ↓
Rendering
```

Every major transformation should produce an inspectable artifact.

For example:

```text
comic.zip
   ↓
document.json
   ↓
panels.json
   ↓
story.json
   ↓
script.json
   ↓
voice/
   ↓
visual_plan.json
   ↓
timeline.json
   ↓
video.mp4
```

This enables:

- debugging
- versioning
- regeneration
- human review
- model comparison
- caching
- reproducibility
- evaluation

---

# 6. High-Level Architecture

```text
                         PANELWEAVER
                              │
                              ▼
                    ┌───────────────────┐
                    │   INPUT LAYER     │
                    │                   │
                    │ Images / PDF /    │
                    │ CBZ / Webtoon    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ DOCUMENT ENGINE   │
                    │                   │
                    │ Pages             │
                    │ Reading Order     │
                    │ Panel Detection   │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ UNDERSTANDING     │
                    │ ENGINE            │
                    │                   │
                    │ OCR               │
                    │ Characters        │
                    │ Speech Bubbles    │
                    │ Scenes            │
                    │ Actions           │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ STORY ENGINE      │
                    │                   │
                    │ Events            │
                    │ Relationships     │
                    │ Story Graph       │
                    │ Chapter Memory    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ NARRATIVE ENGINE  │
                    │                   │
                    │ Script            │
                    │ Beats             │
                    │ Dialogue          │
                    │ Style             │
                    └─────────┬─────────┘
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
          ┌─────────────────┐   ┌──────────────────┐
          │   VOICE ENGINE  │   │ VISUAL DIRECTOR │
          │                 │   │                  │
          │ TTS             │   │ Panel Selection  │
          │ Voice Profiles  │   │ Cropping         │
          │ Timing          │   │ Camera           │
          │ Dialogue        │   │ Transitions      │
          └────────┬────────┘   └─────────┬────────┘
                   │                      │
                   └──────────┬───────────┘
                              ▼
                    ┌───────────────────┐
                    │ TIMELINE ENGINE   │
                    │                   │
                    │ Audio             │
                    │ Visuals           │
                    │ Music              │
                    │ SFX                │
                    │ Subtitles          │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ RENDER ENGINE     │
                    │                   │
                    │ FFmpeg            │
                    │ Encoding          │
                    │ Compositing       │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │      QA ENGINE    │
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                    ▼                   ▼
                  PASS                 FAIL
                    │                   │
                    ▼                   ▼
              FINAL VIDEO        Targeted Repair
```

---

# 7. The Two Most Important Concepts

PanelWeaver should separate:

## 7.1 Understanding

> What objectively exists in the source?

and:

## 7.2 Direction

> How should the source be transformed into an audiovisual experience?

For example:

```text
UNDERSTANDING

Jin is standing outside a dungeon.
He appears nervous.
A large doorway is in front of him.
```

Then:

```text
DIRECTION

Narration:
"Jin hesitates outside the abandoned dungeon."

Visual:
Wide shot of entrance.

Camera:
Slow push-in toward Jin.

Duration:
3.2 seconds.
```

This separation reduces hallucination and makes the system much easier to debug.

---

# 8. Canonical Project State

PanelWeaver should have a canonical structured project state.

Conceptually:

```text
Project
│
├── Source
│
├── Document
│
├── Pages
│   └── Panels
│
├── Text
│   ├── Dialogue
│   ├── Narration
│   ├── Monologue
│   └── SFX
│
├── Characters
│
├── CharacterAppearances
│
├── Locations
│
├── Objects
│
├── Scenes
│
├── Events
│
├── StoryGraph
│
├── ChapterMemory
│
├── Script
│   └── Beats
│
├── Audio
│
├── VisualPlan
│
├── CameraInstructions
│
├── Timeline
│
├── QA
│
└── Renders
```

This structure should become one of the most important architectural artifacts in the project.

---

# 9. Input Layer

PanelWeaver should eventually support:

### Traditional manga

```text
001.jpg
002.jpg
003.jpg
```

### Manhwa/webtoon

```text
long_vertical_image.png
```

### PDF

```text
chapter.pdf
```

### Comic archives

```text
chapter.cbz
chapter.cbr
```

### Future

- EPUB
- scanned books
- creator uploads
- licensed source APIs
- original artwork
- public-domain comics

The system should normalize all of these into a common internal representation.

---

# 10. Document Model

Example:

```json
{
  "document_id": "doc_001",
  "title": "Example Chapter",
  "type": "manhwa",
  "language": "en",
  "reading_direction": "ltr",
  "pages": [
    "page_001",
    "page_002"
  ]
}
```

The document model should retain:

- source file
- source hash
- page count
- dimensions
- language
- reading direction
- chapter/volume metadata
- processing status

---

# 11. Page Analysis

Every page should first be analyzed independently.

```text
PAGE
 │
 ├── dimensions
 ├── orientation
 ├── reading direction
 ├── text regions
 ├── speech bubbles
 ├── characters
 ├── panels
 └── background/environment
```

The system should not assume that a page equals a panel.

---

# 12. Panel Detection

Panel detection is a dedicated computer-vision problem.

Traditional manga may contain:

```text
┌───────┬────────┐
│ P1    │ P2     │
├───────┼────────┤
│ P3             │
├────────┬───────┤
│ P4     │ P5    │
└────────┴───────┘
```

Manhwa may instead contain:

```text
┌────────────────┐
│      P1        │
│                │
├────────────────┤
│                │
│      P2        │
│                │
├────────────────┤
│      P3        │
└────────────────┘
```

But real pages can be considerably more complicated:

- borderless panels
- irregular boundaries
- overlapping panels
- splash pages
- full-page artwork
- whitespace-separated scenes
- panels embedded inside other compositions

Therefore panel detection should combine:

- computer vision
- geometry
- whitespace analysis
- visual segmentation
- VLM verification

The ICCV 2025 *From Panels to Prose* work is particularly relevant here: its Magiv3 model is designed to localize panels, characters, text and speech-bubble tails, perform OCR, associate text with speakers and ground characters in visual regions.

---

# 13. Panel as the Atomic Visual Unit

Each panel becomes a first-class object.

Example:

```json
{
  "panel_id": "panel_000143",
  "page_id": "page_000037",
  "sequence": 143,

  "bbox": {
    "x": 120,
    "y": 840,
    "width": 1080,
    "height": 620
  },

  "characters": [],
  "text_regions": [],
  "speech_bubbles": [],

  "scene_id": "scene_18",

  "importance": 0.84,

  "confidence": 0.96
}
```

Everything downstream should be able to refer back to this panel.

---

# 14. Reading Order

Reading order cannot be hard-coded universally.

Possible modes:

- manga RTL
- western comics LTR
- manhwa vertical
- custom order

The system should calculate a logical reading sequence.

Example:

```text
Physical order:

P1
P2
P3
P4

Narrative order:

P1 → P3 → P2 → P4
```

if the visual structure requires it.

The reading order should be stored explicitly rather than inferred repeatedly.

---

# 15. OCR Engine

OCR should extract all meaningful text.

Categories:

```text
Dialogue
Narration
Monologue
SFX
Signs
UI/System text
Titles
Environmental text
```

Example:

```json
{
  "text_id": "text_00192",
  "panel_id": "panel_143",
  "type": "dialogue",
  "text": "Where are you going?",
  "bbox": {},
  "reading_order": 2,
  "confidence": 0.94
}
```

---

# 16. OCR Should Be Multi-Stage

Instead of trusting one OCR call:

```text
Panel
 ↓
Text Detection
 ↓
Region Crop
 ↓
OCR
 ↓
VLM Verification
 ↓
Reading Order
 ↓
Correction
 ↓
Canonical Text
```

The VLM can be used as a verification/fallback layer rather than the only OCR engine.

This lets the system use cheaper specialized OCR for ordinary text and expensive multimodal reasoning only when necessary.

---

# 17. Speech Bubble Understanding

A speech bubble is more than text.

We need:

```text
Bubble
 ├── shape
 ├── text
 ├── location
 ├── tail
 ├── speaker
 ├── type
 └── confidence
```

The tail may point toward the speaker.

However:

- tails can be hidden
- multiple characters can be nearby
- dialogue can occur off-screen
- bubbles can represent thoughts
- narration boxes have no speaker
- monsters may have unusual speech bubbles

Therefore speaker assignment should be probabilistic.

---

# 18. Speaker Identification

Candidate signals:

```text
Speech bubble tail
+
Character proximity
+
Character orientation
+
Visual identity
+
Dialogue context
+
Previous speaker
+
Conversation structure
+
VLM reasoning
```

Output:

```json
{
  "speaker": "character_jin",
  "confidence": 0.91
}
```

Low-confidence cases should be surfaced to QA.

---

# 19. Character Registry

PanelWeaver should maintain persistent character identities.

Example:

```json
{
  "character_id": "char_jin",
  "canonical_name": "Jin",
  "aliases": [
    "Jin",
    "Jinwoo"
  ],

  "visual_references": [],

  "appearances": [],

  "relationships": [],

  "voice_profile": null
}
```

The registry exists because the system must understand:

> "This is the same character."

rather than independently describing the person in every panel.

---

# 20. Character Identity

Potential methods:

- visual embeddings
- face/person embeddings
- character reference images
- VLM descriptions
- clustering
- temporal continuity
- dialogue context
- known character attributes

Character identity should have confidence.

```text
Jin
0.98

Unknown Male
0.44
```

Unknown should remain unknown rather than being hallucinated into an existing character.

---

# 21. Character Knowledge

The registry can eventually contain:

```text
Character
 ├── Identity
 ├── Appearance
 ├── Aliases
 ├── Relationships
 ├── Personality
 ├── Abilities
 ├── Affiliations
 ├── Voice
 ├── First Appearance
 └── Story Events
```

This becomes the foundation for cross-chapter continuity.

---

# 22. Scene Understanding

Each panel should receive semantic information.

Example:

```json
{
  "location": "abandoned dungeon",
  "time": "night",

  "characters": [
    "jin",
    "monster"
  ],

  "action": "Jin raises his sword",

  "emotion": {
    "jin": "determined",
    "monster": "aggressive"
  },

  "environment": "dark underground corridor"
}
```

This information should be evidence-backed by the panel.

---

# 23. Objects and Important Visual Elements

Not everything needs to become a tracked object.

The system should identify objects that matter to the story.

Examples:

- sword
- key
- magical artifact
- letter
- vehicle
- weapon
- treasure
- door
- portal
- UI element

Important objects should receive persistent IDs.

```text
artifact_001
 ↓
appears panel 43
 ↓
mentioned panel 61
 ↓
used panel 78
```

---

# 24. Scene Segmentation

Panels should be grouped into scenes.

Example:

```text
Scene 01
Panels 1–8
Location: City

Scene 02
Panels 9–24
Location: Dungeon

Scene 03
Panels 25–41
Location: Boss Room
```

Scene boundaries can be inferred from:

- location change
- time change
- character group change
- major event
- visual transition
- narrative transition

---

# 25. Story Reconstruction

This is one of the most important parts of PanelWeaver.

A weak implementation does:

```text
Panel 1 → summary
Panel 2 → summary
Panel 3 → summary
```

This produces disconnected narration.

PanelWeaver should instead perform:

```text
ALL VISUAL/TEXTUAL EVIDENCE
          ↓
      EVENT EXTRACTION
          ↓
     STORY STRUCTURE
          ↓
      NARRATIVE PLAN
```

---

# 26. Evidence-First Story Understanding

The system should maintain the distinction between:

### Observed fact

> Jin is holding a sword.

### Inferred fact

> Jin appears ready to fight.

### Speculation

> Jin may be planning to attack.

The system should know which is which.

This is crucial for preventing hallucinated narration.

---

# 27. Evidence Graph

Every important story statement should ideally be traceable.

Example:

```text
Narration:
"Jin discovers that the monster is injured."

        ↓

Story Event:
event_82

        ↓

Evidence:
panel_341
panel_342

        ↓

Visual:
monster has visible wound

        ↓

Optional OCR:
"You're already wounded..."
```

This creates an **evidence graph**.

---

# 28. Story Graph

The story should be represented as events rather than raw panels.

Example:

```text
EVENT 01
Jin enters dungeon
        ↓
EVENT 02
Jin discovers signs of battle
        ↓
EVENT 03
Monster appears
        ↓
EVENT 04
Fight begins
        ↓
EVENT 05
Jin discovers new ability
```

Each event stores:

- description
- supporting panels
- characters
- location
- objects
- dialogue
- importance
- chronology
- confidence

---

# 29. Story Memory

PanelWeaver needs multiple levels of memory.

## Series Memory

Persistent knowledge across the entire series.

```text
characters
world
locations
abilities
relationships
terminology
```

## Volume Memory

Events and state changes within a volume.

## Chapter Memory

Current chapter's events.

## Scene Memory

Immediate local context.

## Beat Memory

The current narration/visual unit.

This prevents the system from repeatedly sending huge amounts of context to an LLM.

---

# 30. Context Hierarchy

```text
SERIES
  ↓
VOLUME
  ↓
CHAPTER
  ↓
SCENE
  ↓
EVENT
  ↓
BEAT
  ↓
PANEL
```

The system should only retrieve the context necessary for each task.

---

# 31. Narrative Planning

Before writing prose, the system should decide:

```text
What are the important events?
What can be omitted?
What must be explained?
Which dialogue matters?
What is the emotional arc?
Where are the transitions?
Where should tension rise?
```

Output:

```text
Narrative Plan
 ├── Hook
 ├── Setup
 ├── Escalation
 ├── Conflict
 ├── Resolution
 └── Cliffhanger
```

Not every chapter will have this exact structure, but the system should identify the applicable narrative pattern.

---

# 32. Script Generation

Supported modes should include:

### Third Person

> Jin cautiously enters the abandoned dungeon.

### First Person

> I step into the dungeon, immediately sensing that something is wrong.

### Commentary

> Jin makes what might be his biggest mistake yet. Instead of retreating, he walks straight inside.

### Dramatic

> The moment Jin crosses the threshold, the dungeon falls completely silent.

### Documentary

More neutral and informational.

### Accessibility

More explicit descriptions of:

- characters
- environments
- actions
- expressions
- spatial relationships

---

# 33. Script Configuration

The user should eventually control:

```text
Perspective
Tone
Pacing
Detail
Humor
Drama
Dialogue density
Description density
Target duration
Spoiler level
Audience
Language
Narrator
```

---

# 34. Script Should Be Beat-Based

Do not generate one giant paragraph.

Instead:

```json
{
  "beat_id": "beat_021",

  "event_id": "event_05",

  "text": "The monster suddenly charges toward Jin.",

  "visual_candidates": [
    "panel_143",
    "panel_144",
    "panel_145"
  ],

  "estimated_duration": 3.2
}
```

The beat is the bridge between story and video.

---

# 35. Script Evidence

Every important beat should ideally retain:

```text
beat
 ↓
event
 ↓
panels
 ↓
OCR / visual evidence
```

This allows the user to ask:

> Why did PanelWeaver say this?

and receive a traceable explanation.

---

# 36. Narration Quality

PanelWeaver should avoid:

- robotic summaries
- repetitive sentence structures
- unnecessary descriptions
- reading every dialogue bubble
- describing obvious visuals unnecessarily
- invented motivations
- invented events
- over-explaining

The target is:

> **A human-feeling retelling grounded in the actual source.**

---

# 37. Dialogue Strategy

PanelWeaver should support multiple modes.

## Narration-only

Dialogue is paraphrased or described.

```text
Jin warns the monster to stay back.
```

## Dialogue-preserving

Characters speak through generated voices.

```text
JIN:
"Stay back."
```

## Hybrid

Narrator handles most content while important dialogue is performed.

Hybrid should likely become the default cinematic mode.

---

# 38. Voice Engine

The voice engine receives structured beats.

It produces:

```text
audio.wav
+
duration
+
word timestamps
+
sentence timestamps
+
beat timestamps
```

This is extremely important.

The visual timeline should be based on **actual generated audio**, not text-length estimates.

---

# 39. Voice Profiles

A profile should contain:

```text
voice_id
language
accent
pitch
speed
emotion
style
pronunciation dictionary
```

For characters:

```text
Character
 ↓
Voice Profile
 ↓
Dialogue
```

For narration:

```text
Narrator
 ↓
Voice Profile
 ↓
Narration
```

---

# 40. Pronunciation Dictionary

Names and fictional terminology frequently break TTS.

Maintain:

```json
{
  "term": "Cha Hae-In",
  "pronunciation": "...",
  "aliases": [
    "Hae-In"
  ]
}
```

The dictionary should be shared across the entire series.

---

# 41. Audio Timing

The audio engine should generate timing metadata.

Example:

```text
Sentence:
"The monster suddenly charges toward Jin."

Start:
42.10s

End:
45.24s
```

Then:

```text
42.10s
   ↓
visual plan begins

45.24s
   ↓
visual plan ends
```

---

# 42. Visual Director

The Visual Director determines what the viewer sees.

Its job is not simply:

> Pick a panel.

It answers:

```text
What is being said?
        ↓
What event is occurring?
        ↓
What should the viewer focus on?
        ↓
Which visual contains that information?
        ↓
Which region matters?
        ↓
How long should it remain?
        ↓
Should the camera move?
        ↓
When should the shot change?
```

---

# 43. Visual Candidate Ranking

Candidate panels can be scored using:

```text
Visual Score =
    semantic relevance
  + event relevance
  + character relevance
  + object relevance
  + emotional relevance
  + chronological proximity
  + visual quality
  - repetition penalty
```

Example:

```text
Panel 143 → 0.94
Panel 144 → 0.88
Panel 139 → 0.62
Panel 120 → 0.24
```

---

# 44. Region-Level Visual Selection

Panel-level selection is not enough.

A panel might contain:

```text
┌──────────────────────────────┐
│                              │
│  JIN                 MONSTER │
│                              │
│                              │
│       SWORD                  │
│                              │
└──────────────────────────────┘
```

The narration may specifically discuss Jin.

The Visual Director should be able to select:

```text
panel_143
focus = character_jin
```

rather than simply showing the entire panel.

---

# 45. Camera Planning

Possible camera instructions:

```text
STATIC

SLOW_PUSH_IN

FAST_PUSH_IN

PULL_OUT

PAN_LEFT

PAN_RIGHT

PAN_UP

PAN_DOWN

FOCUS_CHARACTER

FOCUS_OBJECT

FOCUS_TEXT

CENTER_CROP

FULL_PANEL
```

Example:

```json
{
  "panel": "panel_143",
  "start": 42.1,
  "end": 45.2,

  "camera": {
    "type": "slow_push_in",
    "focus": "character_jin",
    "start_scale": 1.0,
    "end_scale": 1.14
  }
}
```

---

# 46. Cinematography Rules

Camera motion should be intentional.

Examples:

```text
Establishing shot
→ wide / stable

Dialogue
→ stable / subtle movement

Emotional moment
→ slow push-in

Revelation
→ controlled zoom

Action
→ faster cuts / movement

Impact
→ short aggressive movement

Transition
→ pan / cut / fade
```

The system should avoid applying the same animation template to every panel.

---

# 47. Visual Continuity

The Visual Director should consider:

```text
Previous shot
+
Current shot
+
Next shot
```

This prevents bad sequences such as:

```text
wide shot
→ extreme face crop
→ tiny object
→ full-page splash
→ unrelated character
```

without narrative justification.

---

# 48. Repetition Control

Panel repetition should be explicitly tracked.

Example:

```text
panel_143
used 4 times
```

The system can apply a penalty.

However, repetition should not be forbidden.

A critical panel may legitimately appear multiple times if:

- the narration revisits it
- it is an important establishing image
- different crops reveal different details

Therefore:

> **Discourage unnecessary repetition, not repetition itself.**

---

# 49. Audio-Visual Synchronization

The temporal backbone should be:

```text
SCRIPT
 ↓
TTS
 ↓
ACTUAL AUDIO
 ↓
WORD/SENTENCE TIMESTAMPS
 ↓
BEAT TIMESTAMPS
 ↓
VISUAL PLAN
```

This means visuals are synchronized against the final audio.

Not:

```text
text length → guessed duration
```

---

# 50. Timeline Engine

Everything should eventually become one normalized timeline.

Example:

```json
{
  "duration": 120.42,

  "tracks": [
    {
      "type": "video",
      "segments": []
    },
    {
      "type": "narration",
      "segments": []
    },
    {
      "type": "dialogue",
      "segments": []
    },
    {
      "type": "music",
      "segments": []
    },
    {
      "type": "sfx",
      "segments": []
    },
    {
      "type": "subtitles",
      "segments": []
    }
  ]
}
```

This becomes the canonical representation of the final video.

---

# 51. Music

Music should eventually be event-aware.

Example:

```text
calm
 ↓
mystery
 ↓
tension
 ↓
combat
 ↓
victory
```

The system should be able to create music regions:

```json
{
  "type": "music",
  "track": "tension_01",
  "start": 82.0,
  "end": 114.0,
  "volume_curve": []
}
```

---

# 52. Sound Effects

Future SFX types:

- footsteps
- sword swings
- impacts
- explosions
- magic
- doors
- ambience
- wind
- rain
- crowd
- UI/system effects

Example:

```json
{
  "type": "sfx",
  "asset": "sword_impact_03",
  "start": 103.24,
  "duration": 0.48
}
```

---

# 53. Subtitles

Subtitle generation should derive from the same timing system.

Supported outputs:

```text
SRT
VTT
ASS
```

ASS should eventually be supported for cinematic positioning and styling.

---

# 54. Rendering Engine

The initial renderer should use FFmpeg.

The important architectural principle is:

> **AI decides what the video should contain. Deterministic software decides how to render it.**

LLMs should not directly control arbitrary production commands without validation.

Instead:

```text
AI
 ↓
Validated Timeline Schema
 ↓
Renderer
 ↓
FFmpeg
```

---

# 55. Rendering Operations

The renderer should support:

- image scaling
- crop
- zoom
- pan
- rotation
- overlays
- opacity
- fades
- transitions
- subtitles
- audio mixing
- volume automation
- background music
- SFX
- encoding

---

# 56. Resolution Independence

The internal timeline should not be tied to 1920×1080.

The same project should render to:

```text
16:9
9:16
1:1
4:5
4K
1080p
720p
```

Camera coordinates should therefore preferably use normalized coordinates.

Example:

```text
x = 0.42
y = 0.31
width = 0.27
height = 0.38
```

rather than hard-coded pixels.

---

# 57. Quality Assurance

A rendered video should not automatically be considered finished.

PanelWeaver needs a QA engine.

## Story QA

- missing events
- incorrect chronology
- character confusion
- hallucinated facts
- incorrect dialogue

## Visual QA

- narration/panel mismatch
- wrong character
- bad crop
- repeated panel
- awkward transition

## Audio QA

- clipping
- silence
- pronunciation
- unnatural pacing
- volume imbalance

## Timeline QA

- gaps
- overlaps
- timing errors
- subtitle mismatch

---

# 58. Evidence-Based QA

The QA system should be able to ask:

```text
Does narration beat B42 have evidence?
```

If:

```text
B42
 ↓
Event 18
 ↓
Panels 84, 85
```

then it passes.

If there is no evidence:

```text
B42
 ↓
No supporting evidence
```

then it should be flagged.

---

# 59. Confidence System

Every AI-derived decision should ideally have confidence.

Example:

```text
Speaker identification
0.94

Character identity
0.89

Scene classification
0.97

Narrative event
0.82

Visual alignment
0.76
```

Potential policy:

```text
≥ 0.90
Automatic

0.70–0.89
Automatic + logged

0.50–0.69
Review recommended

< 0.50
Mandatory review
```

Exact thresholds should eventually be empirically calibrated.

---

# 60. Human-in-the-Loop

Full automation is the long-term goal.

Human review is the practical reliability mechanism.

The user should be able to inspect:

```text
Narration
      ↓
Supporting event
      ↓
Candidate panels
      ↓
Selected panel
      ↓
Camera
      ↓
Audio
```

Actions:

```text
Approve
Reject
Regenerate
Replace panel
Edit narration
Change voice
Change timing
Change camera
```

---

# 61. Targeted Regeneration

The system should never regenerate the entire project unnecessarily.

If the user changes:

> "Make this sentence more dramatic."

Only:

```text
Script Beat
 ↓
Audio Beat
 ↓
Timing
```

should be regenerated.

If the user changes:

> "Use the previous panel instead."

Only:

```text
Visual Beat
 ↓
Timeline segment
```

should change.

---

# 62. Versioning

Major artifacts should be versioned.

```text
script_v1
script_v2
script_v3

voice_v1
voice_v2

visual_plan_v1
visual_plan_v2

timeline_v1
timeline_v2
```

This enables:

- undo
- comparison
- rollback
- A/B testing
- debugging
- experimentation

---

# 63. Model Abstraction

PanelWeaver should not become locked to a single AI provider.

Interfaces should exist for:

```text
LLMProvider
VisionProvider
OCRProvider
EmbeddingProvider
TTSProvider
MusicProvider
SFXProvider
```

Potential providers can change over time.

---

# 64. Model Routing

Not every operation needs the most expensive model.

Example:

```text
CHEAP MODEL
 ├── metadata extraction
 ├── OCR correction
 ├── simple classification
 └── embeddings

MEDIUM MODEL
 ├── panel understanding
 ├── character analysis
 └── scene analysis

LARGE MODEL
 ├── story synthesis
 ├── complex continuity
 ├── difficult visual reasoning
 └── final script
```

The router should select models based on:

```text
task
+
confidence
+
complexity
+
cost
```

---

# 65. Caching

Every expensive operation should be cacheable.

Example:

```text
Image hash
+
model
+
prompt version
+
parameters
        ↓
cache key
```

If the user changes the narration style, PanelWeaver should not redo:

- OCR
- panel detection
- character recognition
- scene analysis

unless necessary.

---

# 66. Reproducibility

Each generated artifact should store:

```text
model
model version
prompt version
parameters
source hash
input artifact IDs
timestamp
software version
```

This is essential for debugging.

---

# 67. Agent Architecture

PanelWeaver can eventually be organized into specialized agents.

## Ingestion Agent

Normalizes source material.

## Document Agent

Determines page/panel structure.

## Vision Agent

Understands visual content.

## OCR Agent

Extracts and verifies text.

## Character Agent

Tracks identities.

## Story Agent

Builds the event graph.

## Script Agent

Generates narration.

## Voice Agent

Produces audio.

## Visual Director Agent

Creates the visual plan.

## Editor Agent

Constructs the timeline.

## QA Agent

Checks the result.

---

# 68. Agents Must Use Structured Communication

Agents should not communicate primarily through giant natural-language prompts.

Instead:

```text
VisionAgent
      ↓
PanelAnalysisSchema
      ↓
StoryAgent
      ↓
StoryEventSchema
      ↓
ScriptAgent
      ↓
ScriptBeatSchema
      ↓
VisualAgent
      ↓
VisualSegmentSchema
```

This reduces ambiguity and makes individual components replaceable.

---

# 69. Agent Orchestration

A possible future orchestration graph:

```text
INGEST
  ↓
ANALYZE
  ↓
VALIDATE
  ↓
BUILD STORY
  ↓
VALIDATE STORY
  ↓
GENERATE SCRIPT
  ↓
VALIDATE SCRIPT
  ↓
GENERATE AUDIO
  ↓
DIRECT VISUALS
  ↓
BUILD TIMELINE
  ↓
RENDER PREVIEW
  ↓
QA
  │
  ├── FAIL → targeted repair
  │
  └── PASS → final render
```

This should be deterministic at the workflow level even if individual AI decisions are probabilistic.

---

# 70. Why the Story Graph Matters

Suppose a character appears in Chapter 3:

```text
"mysterious masked man"
```

Then Chapter 8 reveals:

```text
"His identity is Jin's brother."
```

PanelWeaver should be able to update the world model.

The story graph becomes:

```text
Character A
   │
   └── relationship
          ↓
       Character B
```

rather than treating every chapter as an isolated task.

---

# 71. Cross-Chapter Continuity

Long-term processing should support:

```text
Series
 ├── Chapter 01
 ├── Chapter 02
 ├── Chapter 03
 └── Chapter 04
```

with persistent:

```text
characters
locations
relationships
abilities
terminology
story state
```

This is essential for long-form recap channels.

---

# 72. Narrative Compression

The source may contain hundreds of panels.

The final video may only need a subset.

Therefore PanelWeaver needs a compression layer.

Example:

```text
500 panels
 ↓
120 story events
 ↓
80 narration beats
 ↓
160 visual segments
 ↓
18-minute video
```

The goal is not simply to remove panels.

The goal is to preserve **story information** while reducing unnecessary visual repetition.

---

# 73. Information Importance

Every event should receive an importance score.

Factors:

```text
Plot importance
Character importance
Future relevance
Emotional significance
Visual significance
Dialogue significance
```

Low-importance events can be compressed.

High-importance events should receive more narration and visual attention.

---

# 74. Pacing Engine

The final video should have a pacing curve.

Example:

```text
Intensity

100 |                    /\
 80 |             /\    /  \
 60 |      /\    /  \__/    \
 40 |_____/  \__/             \__
 20 |
    └────────────────────────────
              Timeline
```

The pacing engine can consider:

- sentence length
- scene duration
- shot duration
- music
- SFX
- event importance
- action density

---

# 75. Cinematic Language

PanelWeaver should eventually learn a vocabulary of cinematic decisions.

```text
Establish
Reveal
Focus
Escalate
Impact
React
Transition
Resolve
```

For example:

```text
Reveal
→ wide shot
→ pause
→ slow push
→ important dialogue
```

This can make the generated videos feel directed rather than mechanically assembled.

---

# 76. Motion-Comic Philosophy

PanelWeaver should initially preserve the original artwork.

It should use:

- crops
- pans
- zooms
- transitions
- overlays
- timing
- sound
- narration

rather than attempting to generate entirely new animation.

Generative video can eventually become an optional layer.

---

# 77. Why Not Use Generative Video Immediately?

Because generative video introduces problems:

- character inconsistency
- artwork distortion
- style drift
- hallucinated motion
- changed clothing
- changed environments
- altered story details

For recap-style production, preserving the original artwork is often more valuable.

Therefore:

> **Motion graphics first. Generative video later.**

---

# 78. Industry / Research Landscape

PanelWeaver is not inventing every component independently.

Existing work already demonstrates several pieces.

The ICCV 2025 *From Panels to Prose* paper presents Magiv3, a unified manga-analysis system handling panel, character and text localization, speech-bubble tails, OCR, speaker association, character clustering and grounding, followed by VLM/LLM-based prose generation. This is especially important because it validates the architecture of separating comic understanding from narrative generation.

There is also an open-source `manga-reader` project that demonstrates an end-to-end manga-to-video pipeline using PDF extraction, GPT Vision analysis, storytelling summaries, ElevenLabs narration and video generation.

Commercial tools such as MagaRecap advertise capabilities including panel detection, OCR, AI narration, TTS provider selection, animation/keyframes and export workflows. These are useful as product references, although their internal implementations should not be assumed to match their marketing descriptions.

The conclusion is:

> The basic pipeline is technically validated. The opportunity for PanelWeaver is to build a deeper, inspectable, modular and agentic system rather than a black-box generator.

---

# 79. Traditional Human Workflow vs PanelWeaver

## Traditional

```text
Human reads
 ↓
Human writes
 ↓
Human records
 ↓
Human edits
 ↓
Human synchronizes
 ↓
Human renders
```

## AI-Assisted

```text
Human reads
 ↓
AI drafts
 ↓
Human fixes
 ↓
AI voices
 ↓
Human edits
```

## PanelWeaver

```text
Source
 ↓
AI understands
 ↓
AI reconstructs story
 ↓
AI drafts
 ↓
AI voices
 ↓
AI directs
 ↓
AI renders
 ↓
AI evaluates
 ↓
Human approves / intervenes when needed
```

The human becomes the **director/editor**, rather than performing every mechanical operation.

---

# 80. Human vs AI Responsibilities

### AI should handle

- repetitive analysis
- OCR
- classification
- candidate selection
- draft writing
- voice generation
- timing
- camera planning
- rendering
- QA

### Human should initially handle

- final story direction
- ambiguous character identity
- questionable source interpretation
- style selection
- sensitive content decisions
- final approval

Long-term, human involvement should decrease as confidence improves.

---

# 81. Evaluation Framework

PanelWeaver needs an evaluation harness from early development.

## OCR

Measure:

- character error rate
- word error rate
- text detection accuracy

## Panel Detection

Measure:

- panel boundary accuracy
- missed panels
- false panels
- ordering accuracy

## Character

Measure:

- identity accuracy
- clustering accuracy
- speaker accuracy

## Story

Measure:

- event recall
- chronology
- factual consistency
- hallucination rate

## Script

Measure:

- human preference
- narrative coherence
- coverage
- verbosity
- repetition

## Visual

Measure:

- panel relevance
- character relevance
- event relevance
- repetition
- timing

## Audio

Measure:

- pronunciation
- intelligibility
- timing
- naturalness

## Final Video

Measure:

- watchability
- pacing
- coherence
- visual/narration alignment
- human preference

---

# 82. Automated Video Scoring

A future QA model could score:

```text
Story coherence       0–100
Visual relevance      0–100
Narration quality     0–100
Timing                0–100
Audio quality         0–100
Visual variety        0–100
Continuity            0–100
```

Overall:

```text
PanelWeaver Score =
weighted combination
```

But human evaluation remains necessary.

---

# 83. Experimentation Framework

PanelWeaver should eventually support:

```text
Model A
vs
Model B
```

and:

```text
Prompt A
vs
Prompt B
```

and:

```text
Voice A
vs
Voice B
```

The system should record:

```text
quality
cost
latency
failure rate
```

This allows evidence-based model selection.

---

# 84. Cost Optimization

Potential expensive operations:

- VLM analysis
- LLM story generation
- TTS
- embeddings
- large-context reasoning

Optimization techniques:

```text
Caching
Batching
Model routing
Context retrieval
Local models
OCR specialization
Incremental processing
Parallel processing
Targeted regeneration
```

The goal is not necessarily minimum cost.

The goal is:

> **Maximum quality per unit of compute.**

---

# 85. Parallel Processing

Many tasks can happen concurrently.

Example:

```text
Pages 1–20
Pages 21–40
Pages 41–60
```

can be analyzed in parallel.

Within a panel:

```text
OCR
Character detection
Scene analysis
Object detection
```

may also run concurrently.

But story synthesis should wait for the necessary structured evidence.

---

# 86. Dependency Graph

A project should explicitly know what depends on what.

Example:

```text
Panel
 ├── OCR
 ├── Character analysis
 └── Scene analysis

OCR + Character + Scene
           ↓
       Story Event

Story Event
           ↓
       Script Beat

Script Beat
           ↓
         TTS

TTS + Story Event + Panels
           ↓
      Visual Plan

Visual Plan + TTS
           ↓
       Timeline

Timeline
           ↓
        Render
```

This allows targeted regeneration.

---

# 87. Incremental Processing

If only Chapter 37 changes:

```text
Chapter 36
unchanged

Chapter 37
reprocess

Chapter 38
unchanged
```

If only the voice changes:

```text
Vision
unchanged

Story
unchanged

Script
unchanged

TTS
regenerate

Timeline
recalculate

Render
regenerate
```

This should be fundamental to the architecture.

---

# 88. Error Taxonomy

PanelWeaver should classify failures.

### Source errors

- corrupted image
- unsupported PDF
- missing pages

### Vision errors

- wrong panel boundaries
- wrong character

### OCR errors

- unreadable text
- wrong language
- bad ordering

### Story errors

- hallucination
- chronology error
- missing event

### Script errors

- repetitive prose
- incorrect tone
- excessive compression

### Audio errors

- bad pronunciation
- unnatural speech

### Visual errors

- wrong panel
- bad crop
- repetitive motion

### Rendering errors

- FFmpeg failure
- missing asset
- encoding error

This makes debugging systematic.

---

# 89. Observability

Every pipeline stage should log:

```text
project_id
artifact_id
agent
model
duration
tokens
cost
status
confidence
error
```

A processing dashboard should eventually show:

```text
Project: Chapter 37

Panels analyzed: 342
OCR: 342/342
Characters: 14
Events: 87
Script beats: 63
Audio: 100%
Visual plan: 100%
QA: 4 warnings
```

---

# 90. Project Storage

Initial prototype:

```text
local filesystem
+
SQLite/PostgreSQL
```

Later:

```text
Object Storage
+
PostgreSQL
+
pgvector
```

Potential objects:

```text
source images
cropped panels
OCR artifacts
audio
renders
thumbnails
embeddings
metadata
```

---

# 91. Vector Search

Vector embeddings can eventually power:

- character retrieval
- similar-panel search
- object retrieval
- scene retrieval
- story memory retrieval
- visual candidate ranking

Example:

```text
"Find panels showing Jin holding the sword."
```

becomes a semantic/visual retrieval problem.

---

# 92. Suggested Initial Technology Direction

The exact stack should remain flexible.

A likely architecture:

```text
Frontend
    React / Next.js

Backend
    Python / FastAPI

AI Orchestration
    Python

Database
    PostgreSQL

Vector Search
    pgvector

Queue
    Redis + worker system

Storage
    Local filesystem initially
    Object storage later

Rendering
    FFmpeg

Containerization
    Docker
```

Model providers should remain abstracted.

---

# 93. Repository Structure

Initial concept:

```text
PanelWeaver/
│
├── apps/
│   ├── web/
│   └── api/
│
├── core/
│   ├── ingestion/
│   ├── documents/
│   ├── panels/
│   ├── ocr/
│   ├── vision/
│   ├── characters/
│   ├── scenes/
│   ├── story/
│   ├── script/
│   ├── voice/
│   ├── visuals/
│   ├── timeline/
│   ├── rendering/
│   └── qa/
│
├── agents/
│
├── providers/
│   ├── llm/
│   ├── vision/
│   ├── ocr/
│   ├── embeddings/
│   ├── tts/
│   └── media/
│
├── schemas/
│
├── prompts/
│
├── datasets/
│
├── experiments/
│
├── tests/
│
├── docs/
│
└── infrastructure/
```

The final structure can change after implementation begins.

---

# 94. Prompt Management

Prompts should be versioned like code.

```text
prompts/
├── panel-analysis/
│   ├── v1.txt
│   └── v2.txt
│
├── story/
│   ├── v1.txt
│   └── v2.txt
│
├── script/
│   └── v1.txt
│
└── visual-director/
    └── v1.txt
```

A generated artifact should record which prompt version produced it.

---

# 95. Security and Isolation

If PanelWeaver eventually processes user-uploaded media:

- sandbox image processing
- limit file sizes
- validate archives
- prevent path traversal
- isolate FFmpeg jobs
- restrict external network access where appropriate
- sanitize metadata
- isolate model/API credentials

The rendering worker should not have unnecessary system privileges.

---

# 96. Legal / Copyright Considerations

This project has an important distinction between:

### Technical processing

and:

### Distribution rights.

PanelWeaver may technically process copyrighted artwork.

That does not automatically grant the user rights to redistribute it.

Similarly, YouTube monetization rules are separate from copyright law.

YouTube's current monetization policy states that monetized content should be original/authentic and not mass-produced or repetitive. Its "inauthentic content" policy specifically addresses mass-produced/template-like content, while its reused-content policy focuses on whether material from other sources has been meaningfully transformed with original commentary, modification, or entertainment/educational value.

YouTube also explicitly says that reused-content review is separate from copyright enforcement: permission or absence of a copyright claim does not automatically make content eligible for monetization.

Therefore PanelWeaver should be designed as a **general production tool**, not around scraping and mass-republishing copyrighted chapters.

Preferred legitimate inputs include:

- user-owned artwork
- licensed artwork
- public-domain material
- original comics
- authorized datasets
- appropriate research/accessibility use cases

---

# 97. Why This Still Makes Sense for YouTube

The target workflow can still support creators.

The important distinction is:

```text
BAD ARCHITECTURE

Upload 10,000 chapters
        ↓
Same template
        ↓
AI voice
        ↓
Mass upload
```

versus:

```text
PANELWEAVER

Creator chooses:
    style
    narrative perspective
    commentary
    pacing
    voice
    visual direction

        ↓

AI performs production work
        ↓

Creator reviews
        ↓

Unique final video
```

This is much closer to an AI production assistant than a content-spam generator.

---

# 98. Accessibility

There is a strong non-YouTube use case.

Comic understanding can generate rich descriptions for people who cannot visually access the artwork.

The ICCV 2025 *From Panels to Prose* research explicitly targets this accessibility problem and demonstrates a pipeline that produces richer literary descriptions from manga, including scene descriptions, character interactions and emotional/contextual information.

PanelWeaver can eventually expose:

```text
Comic
 ↓
Audio Description
 ↓
TTS
 ↓
Accessible Story
```

This could become a completely separate output mode.

---

# 99. MVP Philosophy

The first version should **not** attempt to build the entire vision.

The MVP should answer one question:

> **Can PanelWeaver turn a small comic segment into a genuinely watchable narrated video?**

---

# 100. MVP Scope

Input:

```text
10–30 panels
```

Pipeline:

```text
Images
 ↓
VLM analysis
 ↓
Structured scene descriptions
 ↓
Basic story reconstruction
 ↓
Narration script
 ↓
TTS
 ↓
Panel selection
 ↓
Basic zoom/pan
 ↓
FFmpeg
 ↓
MP4
```

Target:

```text
30–120 second video
```

---

# 101. MVP Exclusions

Do not initially build:

- full series memory
- advanced character voice acting
- automatic music composition
- advanced SFX
- mobile application
- SaaS infrastructure
- distributed rendering
- automatic YouTube publishing
- custom foundation model training
- sophisticated nonlinear editor
- automatic web scraping

These can come later.

---

# 102. MVP Success Criteria

The prototype succeeds when:

### Understanding

The system understands the major events.

### Script

The narration is coherent.

### Visual

The displayed panel generally matches the narration.

### Audio

The narration sounds natural enough.

### Timing

Visual changes happen at sensible moments.

### Cinematography

Camera movement feels intentional rather than random.

### Overall

A human can watch the result without immediately thinking:

> "This is just an AI-generated slideshow."

---

# 103. Phase 2

Add:

- robust panel detection
- specialized OCR
- speaker identification
- character registry
- story graph
- chapter memory
- visual candidate ranking
- subtitles
- timeline editor
- script editing
- multiple narration styles

---

# 104. Phase 3

Add:

- character voices
- dialogue acting
- music
- SFX
- advanced camera planning
- pacing engine
- automatic QA
- targeted regeneration
- cross-scene continuity

---

# 105. Phase 4

Add:

- series memory
- cross-chapter story graph
- persistent character profiles
- voice profiles
- style profiles
- batch processing
- automated project generation

---

# 106. Phase 5

Potentially turn PanelWeaver into:

```text
PanelWeaver Studio
        │
        ├── Creator UI
        ├── AI Production Pipeline
        ├── API
        ├── Batch Processor
        └── Accessibility Mode
```

---

# 107. The Ultimate User Experience

Eventually:

```text
NEW PROJECT

Upload:
    Chapter 37

Narration:
    Third Person

Style:
    Cinematic

Tone:
    Dramatic

Detail:
    High

Target:
    18 minutes

Voice:
    Narrator A

[ GENERATE ]
```

PanelWeaver performs:

```text
INGEST
 ↓
UNDERSTAND
 ↓
RECONSTRUCT
 ↓
WRITE
 ↓
VOICE
 ↓
DIRECT
 ↓
EDIT
 ↓
QA
 ↓
RENDER
```

The user receives:

```text
┌──────────────────────────────────────┐
│          GENERATED VIDEO             │
│                                      │
│              ▶ Preview               │
│                                      │
├──────────────────────────────────────┤
│ Story │ Script │ Visuals │ Audio │ QA│
└──────────────────────────────────────┘
```

Everything remains editable.

---

# 108. The Most Important Future Interaction

The user should eventually be able to talk to the project itself.

For example:

> "The fight starts too early. Give the dungeon reveal another 10 seconds."

PanelWeaver should understand that this means:

```text
modify pacing
+
extend scene
+
possibly modify narration
+
adjust music
+
recalculate visual timing
+
re-render affected region
```

Or:

> "Focus more on Jin during this scene."

which could trigger:

```text
visual candidate re-ranking
+
character focus
+
camera crop
+
possibly narration adjustment
```

This is where PanelWeaver becomes an **agentic editing system** rather than a fixed pipeline.

---

# 109. Natural-Language Project Editing

Long-term commands:

```text
"Make the narration darker."

"Use more dialogue."

"Show the monster more often."

"Don't reveal the identity yet."

"Slow down this scene."

"Make the fight feel more intense."

"Use a calmer narrator."

"Remove this panel."

"Explain this ability better."

"Make the ending more dramatic."
```

These commands should modify structured project state rather than simply regenerate the entire video.

---

# 110. The Agentic Editing Model

```text
USER COMMAND
      ↓
INTENT PARSER
      ↓
PROJECT STATE QUERY
      ↓
CHANGE PLAN
      ↓
AFFECTED ARTIFACTS
      ↓
TARGETED REGENERATION
      ↓
QA
      ↓
UPDATED PROJECT
```

This is one of the major long-term differentiators.

---

# 111. Core Differentiator

Many tools can potentially do:

```text
Comic → AI narration → video
```

PanelWeaver should aim to do:

```text
Comic
 ↓
Structured understanding
 ↓
Evidence-backed story
 ↓
Persistent memory
 ↓
Editable narrative
 ↓
Directed visual plan
 ↓
Deterministic timeline
 ↓
Iterative AI editing
```

The **structured intermediate state** is the moat.

---

# 112. Questions PanelWeaver Must Eventually Answer

The project should be driven by questions.

## Source

- What type of comic is this?
- What is the reading direction?
- Where are the panels?
- What is the correct reading order?

## Vision

- Who is present?
- What are they doing?
- What objects matter?
- What environment are they in?
- What emotions are visible?

## Text

- What does the text say?
- Who said it?
- Is it dialogue, narration or SFX?
- What language is it?

## Story

- What happened?
- Why did it happen?
- What changed?
- What is important?
- What is setup versus payoff?

## Continuity

- Who is this character?
- Have we seen them before?
- What do we know about them?
- What changed since the previous chapter?

## Narrative

- What should be narrated?
- What can be omitted?
- What should be quoted?
- What should be paraphrased?
- What tone should be used?

## Audio

- Who speaks?
- What voice?
- What emotion?
- How fast?
- Where are pauses?

## Visuals

- Which panel?
- Which region?
- How long?
- What camera?
- When should it change?

## Timeline

- What happens at exactly 43.2 seconds?
- Which audio and visual tracks overlap?
- Is the transition correct?

## QA

- Is this statement supported?
- Does this panel match?
- Is the character correct?
- Is the timing natural?
- Does the final video make sense?

If PanelWeaver can answer these questions reliably, it can produce the video.

---

# 113. The Ultimate Internal Pipeline

The complete future architecture can be summarized as:

```text
                    SOURCE
                      │
                      ▼
              ┌───────────────┐
              │ INGESTION     │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ DOCUMENT      │
              │ UNDERSTANDING │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ PANEL / TEXT  │
              │ / CHARACTER   │
              │ EXTRACTION    │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ SCENE MODEL   │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ STORY GRAPH   │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ NARRATIVE     │
              │ PLAN          │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ SCRIPT BEATS  │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ AUDIO         │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ VISUAL        │
              │ DIRECTOR      │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ TIMELINE      │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ RENDER        │
              └───────┬───────┘
                      ▼
              ┌───────────────┐
              │ QA            │
              └───────┬───────┘
                      │
              ┌───────┴────────┐
              ▼                ▼
             PASS             FAIL
              │                │
              ▼                ▼
          FINAL VIDEO     TARGETED REPAIR
```

---

# 114. What PanelWeaver Is NOT

PanelWeaver is not initially intended to be:

- an AI image generator
- an AI animation generator
- a generic text-to-video tool
- a simple manga summarizer
- a TTS wrapper
- a slideshow generator
- a CapCut clone
- an LLM wrapper

Those may become components.

They are not the core product.

---

# 115. What PanelWeaver IS

PanelWeaver is:

> **A structured AI production system for understanding, narrating, directing and rendering sequential visual stories.**

Its core capabilities are:

```text
UNDERSTAND
RECONSTRUCT
NARRATE
DIRECT
SYNCHRONIZE
RENDER
EVALUATE
ITERATE
```

---

# 116. Initial Research Backlog

The next technical research iterations should investigate these independently:

```text
01. Manga / Manhwa ingestion
02. Panel detection
03. Reading-order detection
04. Speech-bubble detection
05. Comic OCR
06. OCR verification
07. Speaker attribution
08. Character detection
09. Character identity clustering
10. Character grounding
11. Scene segmentation
12. Object tracking
13. Event extraction
14. Story graph construction
15. Long-context story memory
16. Narrative compression
17. Script generation
18. Script factual verification
19. TTS benchmarking
20. Word-level timing
21. Visual-to-text alignment
22. Panel ranking
23. Region-level visual grounding
24. Camera planning
25. Cinematic motion rules
26. Music selection
27. SFX selection
28. Timeline schema
29. FFmpeg rendering
30. Automated video QA
31. Human review UI
32. Model routing
33. Caching
34. Cost optimization
35. Evaluation datasets
36. End-to-end benchmarking
```

Each should eventually become its own technical research document.

---

# 117. Initial Research References

### Comic Understanding

**From Panels to Prose: Generating Literary Narratives from Comics — ICCV 2025**

This is one of the most directly relevant pieces of research for PanelWeaver. Its Magiv3 system performs panel, character and text localization, speech-bubble-tail detection, OCR, speaker association, character clustering and visual grounding, then combines those structured outputs with VLM/LLM reasoning to generate coherent narratives.

### Open-Source Manga-to-Video Reference

**manga-reader**

An open-source project demonstrating PDF/image extraction, GPT Vision analysis, storytelling summaries, ElevenLabs narration and video generation. This is useful as a baseline/reference implementation for the basic pipeline.

### Commercial Product Reference

**MagaRecap**

A useful product reference because it exposes the kinds of features the market is converging on: panel detection, OCR, AI narration, multiple TTS providers, animations, keyframes, audio slicing and export. Its advertised functionality should be treated as product documentation rather than proof of its internal architecture.

---

# 118. YouTube / Distribution Considerations

YouTube's current monetization rules are particularly relevant to the intended use case.

YouTube's July 2025 policy clarification renamed "repetitious content" to **inauthentic content** and explicitly states that mass-produced or repetitive content can be ineligible for monetization. It also states that image slideshows or templated content with minimal narrative/commentary and generic AI-generated content produced at scale can fall under this restriction.

Its reused-content policy separately considers whether material from elsewhere has been meaningfully transformed with original commentary, substantive modifications or educational/entertainment value. YouTube explicitly notes that reused-content review is separate from copyright enforcement.

Therefore PanelWeaver's architecture should encourage:

```text
creator direction
+
original narration
+
meaningful editing
+
unique pacing
+
commentary
+
visual transformation
+
human review
```

rather than:

```text
automated scraping
+
identical template
+
mass generation
```

This is both technically better and more defensible as a creator tool.

---

# 119. Initial Product Principle

PanelWeaver should optimize for:

> **Quality × Control × Automation**

not simply:

> **Automation × Volume**

The best version of the system is one where the user can intervene at any level while allowing AI to handle everything else.

---

# 120. Final Project Definition

## PanelWeaver

> **PanelWeaver is an AI-directed sequential visual storytelling system that transforms comic and manga artwork into structured story representations, evidence-backed narration, synchronized audiovisual timelines and editable cinematic videos.**

Its fundamental pipeline is:

```text
SOURCE
  ↓
UNDERSTAND
  ↓
STRUCTURE
  ↓
RECONSTRUCT
  ↓
NARRATE
  ↓
DIRECT
  ↓
SYNCHRONIZE
  ↓
RENDER
  ↓
VERIFY
  ↓
ITERATE
```

Its fundamental architectural principle is:

> **Never lose the structure between the source and the final video.**

Its long-term objective is:

> **Give an AI the ability to understand sequential visual storytelling deeply enough that it can function as a writer, narrator, visual director, editor and QA assistant—while keeping the entire production process inspectable and controllable by the creator.**

---

# 121. Immediate Next Step

The next document should **not** yet be another giant master document.

The most valuable next iteration is to take the architecture above and perform a deep technical decomposition of the hardest subsystem:

## `PanelWeaver — Comic Understanding & Story Reconstruction Architecture`

It should answer, in implementation-level detail:

```text
How do we ingest manga/manhwa?

How do we detect panels?

How do we determine reading order?

How do we detect speech bubbles?

How do we associate bubbles with characters?

Which OCR systems should we use?

Which VLMs should we benchmark?

How do we build character embeddings?

How do we build the story graph?

How much context goes to each model?

How do we prevent hallucinations?

How do we represent evidence?

How do we persist chapter/series memory?

What happens when models disagree?

What gets cached?

What gets recomputed?

What happens when confidence is low?

Which parts can run locally?

Which parts need APIs?

What does each stage cost?

What does the exact JSON/schema look like?

What should the first prototype implement?

How do we benchmark it?

```

That document would turn **PanelWeaver v0.1 from a product concept into an actual engineering/research blueprint**.

# END — PANELWEAVER INITIAL MASTER PROJECT SPECIFICATION v0.1