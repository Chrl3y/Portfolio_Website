# AGENT CONTINUITY

> Last updated: 2026-09-10 08:00 EAT

## LOCAL ARCHITECTURE STATE

### Running Services

| Service | URL | Status | Container | Docker Context |
|---------|-----|--------|-----------|----------------|
| n8n | http://localhost:5678 | ✅ Healthy (200) | `n8n-automation` | OrbStack |
| Postiz | http://localhost:3004 | ✅ Healthy (307→200 on `/auth`) | `postiz-automation` | desktop-linux |
| PostgreSQL (Postiz) | localhost:5433 | ✅ Healthy | `postgres-postiz-automation` | desktop-linux |
| Redis (Postiz) | localhost:6380 | ✅ Healthy | `redis-postiz-automation` | desktop-linux |
| Temporal | localhost:7233 | ✅ Healthy | `temporal-postiz-automation` | desktop-linux |
| Elasticsearch | localhost:9200 | ✅ Healthy | `temporal-elasticsearch-automation` | desktop-linux |

**Important**: n8n runs under the **OrbStack** Docker context (`orbstack`), while Postiz runs under **Docker Desktop** (`desktop-linux`). Use `docker ps` for Postiz and `docker --context orbstack ps` for n8n.

### Python Environments (under AUTOmation/)

| Environment | Path | Purpose | Status |
|-------------|------|---------|--------|
| faster-whisper | `runtime/faster-whisper-env/` | Transcription (tiny, CPU) | ✅ Working — recognizes speech text |
| WhisperX | `runtime/whisperx-env/` | Alignment + diarization | ✅ Import OK (CPU) |
|| DeepFilterNet | `runtime/deepfilternet-env/` | Noise reduction (CLI) | ✅ Model loads, `deep-filter-py` CLI works |
| Manim | `runtime/manim-env/` | Technical animations | ✅ Rendering works (Manim 0.21.0) |

**All venvs use Python 3.12 via `uv`. PyTorch uses CPU index.**

### Node.js Projects

| Project | Path | Status |
|---------|------|--------|
| Remotion | `media/remotion/` | ✅ ViciExplainer renders (6s, 27.5KB MP4) |
| Mermaid CLI | global npm | ✅ `mmdc` renders SVG (puppeteer config needed) |

### Rendered Outputs (gitignored)

- `media/remotion/renders/vici-explainer.mp4` — 6s, 27.5KB
- `media/manim/renders/automation-flow-preview.mp4` — 29s, 357KB (AutomationFlow)
- `docs/architecture-diagram.svg` — 37KB (architecture diagram)

## Commands to Restart Services

### Start all Docker services
```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1

# Postiz stack (Docker Desktop context)
docker compose -f infra/postiz/docker-compose.yml --env-file /tmp/postiz-env-clean up -d

# n8n (OrbStack context)
docker --context orbstack compose -f infra/docker-compose.yml up -d
```

### Stop all services
```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1
docker compose -f infra/postiz/docker-compose.yml down
docker --context orbstack compose -f infra/docker-compose.yml down
```

### Run transcription (faster-whisper)
```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1
source runtime/faster-whisper-env/bin/activate
python tests/test_transcription.py tests/transcription-test.wav
# Or auto-generate speech: python tests/test_transcription.py
```

### Run Manim render
```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1
AUTOMATION_DIR=$(pwd)
"$AUTOMATION_DIR/runtime/manim-env/bin/manim" media/manim/scene.py AutomationFlow -ql -o automation-flow-preview
```

### Render Remotion video
```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation/media/remotion || exit 1
AUTOMATION_DIR="$(cd ../.. && pwd)"
"$AUTOMATION_DIR/runtime/manim-env/bin/manim" ... # (not remotion — use local binary)
./node_modules/.bin/remotion render index.jsx ViciExplainer ../../renders/vici-explainer.mp4
```

## Directory Layout

```
AUTOmation/
├── infra/
│   ├── docker-compose.yml          # n8n (port 5678, OrbStack context)
│   └── postiz/
│       ├── docker-compose.yml      # Postiz + Temporal + PostgreSQL + Redis
│       └── puppeteer.config.json
├── media/
│   ├── remotion/                   # Independent Remotion app
│   │   ├── index.jsx               # Entry point (registerRoot)
│   │   ├── ViciExplainer.jsx       # Test composition
│   │   ├── package.json
│   │   ├── package-lock.json
│   │   └── node_modules/            (gitignored)
│   │       └── renders/             (gitignored)
│   ├── manim/                      # Manim project source
│   │   ├── scene.py                # AutomationFlow scene
│   │   └── renders/                 (gitignored)
│   └── puppeteer.config.json       # Chrome path for Mermaid CLI
├── runtime/                        # Python venvs + data
│   ├── faster-whisper-env/         # faster-whisper 1.2.1 (CPU, tiny model)
│   ├── whisperx-env/               # WhisperX 3.8.6 (CPU)
│   ├── deepfilternet-env/          # DeepFilterNet venv
│   ├── manim-env/                  # Manim 0.21.0
│   ├── content-api-env/            # FastAPI content API
│   └── data/                       # SQLite databases (gitignored)
├── services/                       # Python service modules
│   ├── content_store/              # SQLite-backed persistence
│   ├── content_api/                # FastAPI endpoints
│   ├── transcription/              # Faster-whisper transcription service
│   ├── captions/                   # SRT/VTT/JSON caption generation
│   ├── scene_planner/              # Rule-based scene planning
│   └── video_assembler/            # FFmpeg-based video assembly
├── schemas/                        # JSON schemas
├── workflows/                      # n8n workflow JSON files
├── scripts/
│   ├── bootstrap-resources.sh
│   ├── clean-audio.sh
│   └── repair-voice.py
├── tests/
│   ├── test_transcription.py
│   ├── test_whisperx.py
│   └── test_deepfilter.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── LOCAL-SETUP.md
│   ├── architecture-diagram.mmd
│   ├── architecture-diagram.svg
│   ├── railroad-diagram.mmd
│   └── ...
├── integrations/
│   ├── vizard/README.md
│   └── ayrshare/README.md
├── voice/
│   └── README.md
├── vendor/                         # NOT COMMITTED (see .gitignore)
│   ├── postiz-app/
│   ├── postiz-docker-compose/
│   ├── remotion/
│   ├── manim/
│   └── mermaid/
├── CHANGELOG.md
├── AGENT-CONTINUITY.md
├── SECURITY.md
└── .env.example
```

### Important Path Notes (2026-09-10 cleanup)

- **ALL Python venvs are now standardized under `runtime/`**: `faster-whisper-env`, `whisperx-env`, `manim-env`
- **Stray venvs removed**: `manim-env/` and `faster-whisper-env/` at `AUTOmation/` root were deleted
- **Stray `media/remotion/manim-env/` removed**
- **Stray root `node_modules/` removed**
- **Package files moved to `media/remotion/`**: `package.json`, `package-lock.json`

## Verification Results (Gate Matrix)

| Component | Installed | Running | Functional Test | Notes |
|-----------|-----------|---------|-----------------|-------|
| n8n | ✅ | ✅ (200 on :5678) | Container `n8n-automation` up (OrbStack) | n8n UI accessible |
| Postiz | ✅ | ✅ (200 on :3004/auth) | All 6 containers healthy | Requires Temporal deps |
| PostgreSQL | ✅ | ✅ (healthy) | `postgres-postiz-automation` | Part of Postiz stack |
| Redis | ✅ | ✅ (healthy) | `redis-postiz-automation` | Part of Postiz stack |
| Temporal | ✅ | ✅ (healthy) | `temporal-postiz-automation` | Required by Postiz |
| faster-whisper | ✅ (1.2.1) | — | ✅ Recognized speech in test WAV | tiny model, CPU mode |
| WhisperX | ✅ (3.8.6) | — | ✅ Import OK | Optional, CPU mode |
| DeepFilterNet | ✅ (0.5.6) | — | ✅ Model loads, CLI works | Uses `deep-filter-py` |
| FFmpeg | ✅ (9.0.1) | — | ✅ Audio conversion works | Homebrew |
| Manim | ✅ (0.21.0) | — | ✅ Rendered 29s MP4 | CPU rendering |
| Remotion | ✅ (4.0.523) | — | ✅ Rendered 6s MP4 | 27.5KB, ViciExplainer |
| Mermaid CLI | ✅ (11.x) | — | ✅ SVG rendered | Needs puppeteer config |

### Required Green Gate (all ✅)
n8n ✅ · Postiz ✅ · FFmpeg ✅ · faster-whisper ✅ · Manim ✅ · Remotion ✅ · Mermaid ✅

## Next Recommended Steps

1. **n8n workflows**: Import JSON workflows into the n8n UI and test end-to-end
2. **Postiz**: Set up admin user, test draft publishing via API (no social accounts connected)
3. **DeepFilterNet**: Test with actual speech audio to verify processing completes
4. **Voice tools**: Survey Chatterbox licensing and test on M1 Pro
5. **Content data model**: Write n8n nodes that read/write the JSON schemas

## Deferred (explicitly out of scope for this gate)

- Activepieces
- Voice cloning (Chatterbox/OpenVoice/F5-TTS)
- Heavy video models (Wan2.2, LTX, CogVideoX)
- Cloud GPU models
- Social credentials
- Public publishing

## Problems Encountered & Solutions

### Problem 1: Postiz DATABASE_URL password masking
The Hermes terminal masks `postiz-password` as `***` in all output. The actual value is correct — this is display-level masking only.

### Problem 2: Postiz PostgreSQL auth failure
**Symptom**: Postiz Prisma reports "password authentication failed" for `postiz-user`.
**Root cause**: Container recreation with volume but password hash mismatch (`scram-sha-256`).
**Fix**: `ALTER USER "postiz-user" WITH PASSWORD 'postiz-password'` inside the postgres container.

### Problem 3: Hermes terminal cwd not applied
The terminal tool's `cwd` parameter sometimes doesn't take effect. **Workaround**: Always `cd /absolute/path || exit 1` at the start of commands.

### Problem 4: Multiple Docker contexts (OrbStack vs Desktop)
n8n was started under OrbStack context; Postiz under Docker Desktop. n8n compose commands need `--context orbstack` flag or the OrbStack context must be active.

### Problem 5: Stray venvs from inconsistent cwd
Background processes created venvs at `AUTOmation/` root instead of `runtime/` due to cwd resolution failures. All cleaned up and recreated under `runtime/`.

### Problem 6: Mermaid CLI puppeteer config
`mmdc` requires Chrome path via puppeteer config (`media/.puppeteer.json`) and `PUPPETEER_EXECUTABLE_PATH` env var.

### Problem 7: DeepFilterNet enhance() API change
The `enhance()` function signature changed in 0.5.6 — takes `audio: torch.Tensor` directly. Use `deep-filter-py` CLI for file I/O.
