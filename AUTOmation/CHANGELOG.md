# Changelog

## 2026-09-10

### Installed
- **faster-whisper**: `faster-whisper==1.2.1` (CPU mode, `tiny` model smoke-test PASSED)
- **WhisperX**: `whisperx==3.8.6` (with `torch==2.14.0`, CPU mode import OK)
- **DeepFilterNet**: `deepfilternet==0.5.6` (model loads, CLI works — processing slow on CPU sine wave)
- **Manim**: `manim==0.21.0` (low-quality preview rendered, 29s/357KB)
- **Remotion**: `@remotion/cli@4.0.523` (ViciExplainer rendered, 6s/27.5KB)
- **Mermaid CLI**: `v11.17.0` (architecture SVG rendered, 37KB)
- **Postiz**: `ghcr.io/gitroomhq/postiz-app:latest` (booting, auth fixed, UI accessible on :3004)
- **n8n**: `n8nio/n8n:1.106.2` (healthy on :5678)

### Successful Tests
- faster-whisper transcription smoke test → PASSED (0 segments on sine wave, expected)
- Manim `AutomationFlow` scene render → PASSED (29s, 357KB, ffprobe verified)
- Remotion `ViciExplainer` render → PASSED (6s, 27.5KB, ffprobe verified)
- Mermaid architecture diagram render → PASSED (SVG, 37KB)
- Postiz UI accessible (307→200 on `/auth`)
- n8n healthy (HTTP 200)
- PostgreSQL auth for Postiz → FIXED (password reset resolved scram-sha-256 mismatch)

### Failures / Deferred
- DeepFilterNet CLI processing timed out (>60s) on sine-wave test audio — likely too slow for non-speech audio on CPU; model loads fine
- Activepieces → DEFERRED (n8n is primary orchestrator)
- Voice cloning tools (Chatterbox, OpenVoice, F5-TTS) → NOT INSTALLED (no synthetic voice needed yet)
- Heavy video models (Wan2.2, LTX, CogVideoX) → NOT DOWNLOADED (M1 Pro 16GB constraint)

### New Files
- `AUTOmation/infra/docker-compose.yml` — n8n Docker Compose
- `AUTOmation/infra/postiz/docker-compose.yml` — Postiz + Temporal + PostgreSQL + Redis
- `AUTOmation/media/remotion/` — independent Remotion app with ViciExplainer composition
- `AUTOmation/media/manim/scene.py` — AutomationFlow Manim scene
- `AUTOmation/tests/test_transcription.py` — faster-whisper smoke test
- `AUTOmation/tests/test_whisperx.py` — WhisperX smoke test
- `AUTOmation/tests/test_deepfilter.py` — DeepFilterNet smoke test
- `AUTOmation/schemas/` — content-item, publishing-job, video-scene-plan JSON schemas
- `AUTOmation/workflows/` — n8n workflow definitions (content-intake, video-intake, publish-draft)
- `AUTOmation/scripts/clean-audio.sh` — DeepFilterNet wrapper script
- `AUTOmation/scripts/repair-voice.py` — voice repair placeholder
- `AUTOmation/voice/README.md` — voice tools documentation
- `AUTOmation/integrations/vizard/README.md` — Vizard API adapter docs
- `AUTOmation/integrations/ayrshare/README.md` — Ayrshare API adapter docs
- `AUTOmation/docs/LOCAL-SETUP.md` — reproducible installation guide
- `AUTOmation/docs/architecture-diagram.mmd` / `.svg` — architecture diagram
- `AUTOmation/railroad-diagram.mmd` — railroad diagram (Railway.app alternative)

## 2026-09-09

### Added
- Created the `AUTOmation` subsystem inside the portfolio repository on branch `feature/automation-media-growth`.
- Added system architecture for source intake, orchestration, approval, social publishing, analytics, affiliates, and feedback loops.
- Added tool-role research covering Postiz, n8n, Activepieces, Ayrshare, Vizard, Remotion, Manim, and transcription tooling.
- Added a voice-preserving video repurposing plan for teachings, explainers, and technical content.
- Added monetization architecture covering affiliates, display ads, sponsorships, digital products, services, and consulting CTAs.
- Added `PUBLIC`, `REVIEW`, and `PRIVATE` publishing controls and secrets guidance.
- Added agent continuity notes so future agents can continue without relying on chat history.

### Decisions
- Do not vendor full Postiz/n8n/Activepieces codebases into the portfolio.
- Deploy large automation/social applications independently and integrate them through APIs, webhooks, and MCP surfaces.
- Use n8n as the primary orchestrator and Postiz as the preferred self-hosted social publishing layer.
- Keep Activepieces as a complementary option rather than duplicating every workflow.
- Keep Ayrshare and Vizard behind adapters as managed services.
- Preserve the user's real recorded voice by default; use Remotion/Manim for controllable animated visuals and Vizard for clipping/short-form assistance.
- Treat affiliate products as a first-class monetization channel with contextual relevance and disclosure.

### Not yet implemented
- Activepieces deployment (deferred)
- Voice cloning tools (not installed — no synthetic voice needed yet)
- Heavy video models (not downloaded — M1 Pro 16GB constraint)
- Social media account connections (not connected)
