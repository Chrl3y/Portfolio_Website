# Video Repurposing Pipeline

## Goal

Record a teaching, technical explanation, project walkthrough, or commentary once, then preserve the creator's real voice while producing polished visual versions with diagrams, infographics, animation, captions, and platform-specific edits.

## Preferred principle

Preserve the original recorded narration whenever possible. Voice cloning should be optional, consent-based, and used only when a clean re-record is necessary. The default system should not synthesize a new voice if the original voice can be cleaned and retained.

## Pipeline

```text
RAW RECORDING
  -> ingest
  -> audio extraction/cleanup
  -> transcription + timestamps
  -> topic/claim segmentation
  -> scene plan
  -> factual/theological/technical review
  -> visual storyboard
      -> infographic scenes
      -> diagrams
      -> animated text
      -> B-roll
      -> screenshots/code
  -> render against original narration
  -> subtitles
  -> branded intro/outro
  -> horizontal master (16:9)
  -> vertical master (9:16)
  -> short clips
  -> approval
  -> distribution
  -> analytics feedback
```

## Tool roles

### Whisper / faster-whisper
Use for transcription and timestamps. Store the transcript as source data, not just subtitles. Preserve speaker wording separately from any edited publication script.

### Remotion
Use for repeatable branded motion graphics generated with React. Best for:
- title cards;
- animated diagrams;
- timelines;
- comparison tables;
- code callouts;
- charts;
- quote/highlight scenes;
- lower thirds;
- reusable brand components;
- rendering the same story into 16:9, 1:1, and 9:16 variants.

### Manim
Use selectively for precise explanatory animation, especially mathematical, technical, systems, geometry, flow, architecture, and data concepts. It is not necessary for every social clip.

### Vizard
Use for:
- identifying highlights from long-form videos;
- creating short clips;
- captions;
- reframing into vertical formats;
- AI/stock B-roll where appropriate;
- social-ready edits;
- publishing or scheduling to supported networks.

Vizard should not be the sole source of truth for complex branded explainers. Programmatic compositions should live in our own rendering project so they can be regenerated later.

### Optional generative video tools
Runway or similar models can be used for short illustrative scenes when animation or B-roll cannot communicate the point efficiently. Generated visuals should be clearly treated as illustrative, especially for historical, scientific, financial, or theological claims.

## Scene-generation concept

Transcript segment:

> A payment trigger leaves the core banking system, reaches the orchestration layer, then the correct partner adapter fires the collection or asset-control action.

Possible generated scene spec:

```yaml
start: 00:01:13.200
end: 00:01:28.800
narration_source: original_audio
visual_type: architecture_flow
objects:
  - Helaplus
  - Orchestrator
  - Partner adapter
  - Payment rail
  - Asset platform
animation:
  - highlight Helaplus
  - animate event packet to orchestrator
  - branch to partner adapter
  - show acknowledgement path
caption_style: branded
```

The rendering layer can turn that spec into Remotion or Manim scenes.

## Teaching-content review gate

Teachings and explanatory videos should not be blindly reworded by an AI. Maintain three artifacts:

1. `raw-transcript` — exact source transcript.
2. `editorial-script` — cleaned language without changing intended meaning.
3. `scene-plan` — visual explanation mapped to timestamps.

Where factual claims, quotations, scripture, research, or technical specifications are used, attach sources/checks before publication.

## Voice workflow

Preferred order:

1. Use original narration as recorded.
2. Clean noise, breaths, long pauses, and level inconsistencies.
3. If a sentence needs correction, request/re-record the sentence and splice it.
4. Only if deliberately enabled, use a voice model trained/authorized from the creator's own voice to patch short corrections.
5. Label synthetic/altered voice where required by platform policy or applicable law.

## Formats generated from one recording

Long teaching can become:
- YouTube 16:9 full version;
- portfolio article/transcript;
- podcast/audio version;
- 3–10 vertical shorts;
- Instagram Reel;
- TikTok;
- YouTube Shorts;
- LinkedIn short video;
- carousel summarizing key points;
- quote cards;
- newsletter summary;
- X/Threads excerpts.

## Asset storage

Do not keep generated media inside the website repo long-term if it becomes large. Use object storage/CDN and store only metadata/URLs in the portfolio/content system.

Suggested asset metadata:

```yaml
asset_id:
source_recording:
transcript:
voice_track:
scene_plan:
render_version:
aspect_ratio:
duration:
caption_file:
thumbnail:
rights_status:
classification:
published_urls: []
```

## First prototype

Use one non-sensitive, user-owned 3–10 minute recording.

Deliver:
1. timestamped transcript;
2. scene plan;
3. 16:9 animated explainer preserving original voice;
4. one 9:16 short;
5. captions;
6. Postiz/Vizard-ready publication metadata;
7. UTM-linked portfolio article draft.
