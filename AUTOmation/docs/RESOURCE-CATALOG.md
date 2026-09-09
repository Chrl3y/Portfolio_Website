# Pullable Resource Catalog

This file is the acquisition map for AUTOmation. It distinguishes resources we can clone/install locally from hosted services that should remain API integrations.

## Core automation and social distribution

| Resource | Role | Pull/install stance |
|---|---|---|
| `gitroomhq/postiz-app` | Social publishing/scheduling, agent/MCP-friendly layer | Clone/deploy independently; do not embed in static portfolio |
| `n8n-io/n8n` | Main workflow/orchestration engine | Clone or Docker deploy independently |
| `activepieces/activepieces` | Secondary automation/connector engine | Clone or Docker deploy independently; use only where it adds value |
| Ayrshare | Managed multi-social API | API only; no source pull expected |
| Vizard | AI clipping, captions, B-roll and publishing | API/SaaS only; no source pull expected |

## Voice, transcription and audio cleanup

### Recommended baseline

| Resource | Role | Notes |
|---|---|---|
| `openai/whisper` | Speech transcription | Strong baseline; simple and local |
| `SYSTRAN/faster-whisper` | Faster Whisper inference | Preferred for production throughput |
| `m-bain/whisperX` | Word-level timestamps + diarization/alignment | Useful for scene timing, captions and precise edits |
| `Rikorose/DeepFilterNet` | Speech enhancement/noise suppression | Use before transcription/rendering when recording quality is poor |
| `facebookresearch/demucs` | Source separation | Useful for separating speech from music/noise in mixed recordings |
| `FFmpeg/FFmpeg` | Media conversion/muxing/filtering | Required foundation; install as system dependency rather than vendor source |

### Voice preservation and repair

Default policy: preserve the user's original recorded narration whenever possible.

| Resource | Role | Use policy |
|---|---|---|
| `myshell-ai/OpenVoice` | Zero-shot voice cloning / voice style transfer | Optional for user-owned voice repairs; MIT licensed per upstream |
| `SWivid/F5-TTS` | Expressive zero-shot TTS/voice cloning | Optional research/repair route; review model/license terms before production |
| `coqui-ai/TTS` or maintained compatible fork | TTS and XTTS-style voice cloning | Optional; verify current maintenance and model licenses |
| Fish Speech | High-quality voice cloning/speech generation | Optional; review research/model license carefully before monetized use |
| Piper | Fast local TTS | Good for generic system narration; not primary choice for preserving the user's identity |

Voice cloning must only be used for the user's own voice or voices with explicit permission. The preferred use case is repairing a missed sentence, pronunciation, or transition while keeping the original recording as the source of truth.

## Animated video and infographic rendering

### Deterministic/programmatic layer

| Resource | Role | Priority |
|---|---|---|
| `remotion-dev/remotion` | React-based programmatic video rendering | HIGH |
| `ManimCommunity/manim` | Mathematical/technical diagrams and animation | HIGH |
| `mermaid-js/mermaid` | Diagram generation from text | HIGH for architecture/workflow content |
| `ImageMagick/ImageMagick` | Image composition/processing | Utility |
| `FFmpeg/FFmpeg` | Video/audio assembly | Mandatory utility |

Use this layer for branded explainers where we need repeatability, accurate text, charts, diagrams and controlled motion.

### Generative video layer

| Resource | Role | Priority |
|---|---|---|
| `comfyanonymous/ComfyUI` | Node-based local generative media control plane | HIGH as optional visual-generation backend |
| `Lightricks/LTX-Video` / LTX-2 ecosystem | Text/image/video generation | HIGH candidate; supports local workflows and ComfyUI integration |
| Wan video models | Text/image-to-video | Evaluate based on hardware/license |
| CogVideoX | Open video generation family | Evaluate based on hardware/license |
| AnimateDiff ecosystem | Diffusion-based animation | Secondary; useful for stylized motion workflows |

Generated video should normally be used as scene B-roll/illustration, not to replace the full factual teaching with synthetic talking-head footage.

## Talking-head / portrait animation (optional)

| Resource | Role | Stance |
|---|---|---|
| LivePortrait | Portrait animation/retargeting | Optional; for user-owned portrait/avatar only |
| MuseTalk | Real-time/high-quality lip sync | Optional |
| Wav2Lip | Lip synchronization | Optional legacy/fallback |
| SadTalker | Portrait + audio to talking-head video | Optional; not default |

These modules are not required for the core teaching workflow. They are only for intros, avatar segments, or approved talking-head recreations.

## Recommended media pipeline

```text
recording
  -> DeepFilterNet (only if needed)
  -> faster-whisper + WhisperX
  -> transcript + word timestamps
  -> scene planner
  -> Mermaid / Manim / Remotion
  -> optional ComfyUI + LTX/Wan/CogVideo visual scenes
  -> original user voice retained
  -> FFmpeg assembly
  -> Vizard for clipping/reframing/B-roll assistance
  -> approval
  -> Postiz
```

## Hosted/API-only resources

Do not waste time attempting to clone proprietary services. Create adapters/config only for:

- Ayrshare
- Vizard
- ElevenLabs (if later chosen for user-owned voice repair)
- HeyGen/Synthesia-style avatar services (only if later justified)
- commercial image/video APIs
- social platform official APIs

## Hardware reality

The user's 14-inch M1 Pro 16GB machine is excellent for transcription, FFmpeg, Remotion, Manim and lightweight/local audio work. Large generative-video models may be impractical or very slow locally. Keep the architecture capable of routing those jobs to a GPU server, cloud inference API, RunPod/Modal/Replicate-style runtime, or a future dedicated GPU workstation.

## Licensing rule

Every pulled resource must have its repository/model license recorded before production use. Code license and model-weight license can differ. Do not assume an open GitHub repository means commercial model usage is permitted.

## Acquisition strategy

Use `scripts/bootstrap-resources.sh` to clone selected source repos into `AUTOmation/vendor/` for local experimentation. Do not commit those full vendor repositories back into the portfolio repository. `vendor/` should remain gitignored in the eventual local project setup.
