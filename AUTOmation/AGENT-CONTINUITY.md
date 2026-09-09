# AGENT CONTINUITY

> Last updated: 2026-09-10 02:30 EAT

## LOCAL ARCHITECTURE STATE

### Running Services

| Service | URL | Status | Container |
|---------|-----|--------|-----------|
| n8n | http://localhost:5678 | Healthy (200) | `n8n-automation` |
| Postiz | http://localhost:3004 | Healthy (307→200 on `/auth`) | `postiz-automation` |
| PostgreSQL (Postiz) | localhost:5433 | Healthy | `postgres-postiz-automation` |
| Redis (Postiz) | localhost:6380 | Healthy | `redis-postiz-automation` |
| Temporal | localhost:7233 | Healthy | `temporal-postiz-automation` |
| Elasticsearch | localhost:9200 | Healthy | `elasticsearch-postiz-automation` |

**Note**: All Postiz services use custom container names suffixed with `-automation` to avoid conflicts.

### Python Environments (under AUTOmation/)

| Environment | Path | Purpose | Status |
|-------------|------|---------|--------|
| faster-whisper | `runtime/faster-whisper-env/` | Transcription | ✅ Working (CPU) |
| WhisperX | `runtime/whisperx-env/` | Alignment + diarization | ✅ Import OK (CPU) |
| DeepFilterNet | `deepfilternet-env/` | Noise reduction | ✅ Model loads (CPU) |
| Manim | `manim-env/` | Technical animations | ✅ Rendering works |

**Apple Silicon note**: All Python environments use `uv` with Python 3.12. PyTorch uses CPU index (`https://download.pytorch.org/whl/cpu`). MPS is NOT recommended for faster-whisper (CPU mode is more stable).

### Node.js Projects

| Project | Path | Status |
|---------|------|--------|
| Remotion | `media/remotion/` | ✅ ViciExplainer renders (6s MP4) |
| Mermaid CLI | global (npm) | ✅ mmdc renders SVG |

### Rendered Outputs (gitignored)

- `media/remotion/renders/vici-explainer.mp4` — 6s, 27.5KB
- `media/manim/renders/` — 29s, 357KB (AutomationFlow)
- `docs/architecture-diagram.svg` — architecture diagram

## Commands to Restart Services

### Start all Docker services
```bash
docker compose -f infra/docker-compose.yml up -d n8n
docker compose -f infra/postiz/docker-compose.yml --env-file /tmp/postiz-env-clean up -d
```

### Stop all services
```bash
docker compose -f infra/docker-compose.yml down
docker compose -f infra/postiz/docker-compose.yml down
```

### Run transcription
```bash
source runtime/faster-whisper-env/bin/activate
python tests/test_transcription.py tests/test-audio.wav
```

### Run Manim render
```bash
source manim-env/bin/activate
manim media/manim/scene.py AutomationFlow -ql -o automation-flow-preview
```

### Render Remotion video
```bash
cd media/remotion
node_modules/.bin/remotion render index.jsx ViciExplainer renders/vici-explainer.mp4 --duration 180 --fps 30
```

## Directory Layout

```
AUTOmation/
├── infra/
│   ├── docker-compose.yml          # n8n (port 5678)
│   └── postiz/
│       ├── docker-compose.yml      # Postiz + Temporal + PostgreSQL + Redis
│       └── puppeteer.config.json
├── media/
│   ├── remotion/                   # Independent Remotion app
│   │   ├── index.jsx               # Entry point (registerRoot)
│   │   ├── ViciExplainer.jsx       # Test composition
│   │   ├── package.json
│   │   └── renders/
│   ├── manim/                      # Manim project
│   │   ├── scene.py                # AutomationFlow scene
│   │   ├── manim-env/
│   │   └── renders/
│   └── puppeteer.config.json       # Chrome path for Mermaid CLI
├── runtime/                        # Python venvs for transcription
│   ├── faster-whisper-env/
│   └── whisperx-env/
├── deepfilternet-env/              # DeepFilterNet venv (root level)
├── manim-env/                      # Manim venv (root level)
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
├── renders/                        # NOT COMMITTED
├── CHANGELOG.md
├── AGENT-CONTINUITY.md
├── SECURITY.md
└── .env.example
```

### Important Path Notes

- Python venvs were created at different levels (some at `AUTOmation/` root, some under `runtime/` and `media/manim/`). This happened because background process cwd was inconsistent. Future agent note: consider standardizing to `runtime/` subdirs.
- The `manim-env` at `AUTOmation/manim-env/` is the actual installed environment (NOT `media/manim/manim-env/`).
- The `faster-whisper-env` at `AUTOmation/runtime/faster-whisper-env/` is empty/unused. The working one is at `AUTOmation/faster-whisper-env/`.

## Next Recommended Steps

1. **Activepieces**: Start using official Docker Compose (defer if Temporal conflicts arise)
2. **Voice tools**: Survey Chatterbox licensing and test on M1 Pro
3. **n8n workflows**: Import JSON workflows into the n8n UI and test end-to-end
4. **Postiz**: Set up admin user, test draft publishing via API (no social accounts connected)
5. **DeepFilterNet**: Test with actual speech audio (not sine wave) to verify processing completes
6. **WhisperX**: Run alignment test with a real audio file
7. **Content data model**: Write n8n nodes that read/write the JSON schemas

## Unresolved Problems

### Problem 1: Postiz DATABASE_URL password masking
The Hermes terminal masks `postiz-password` as `***` in all output, making debugging difficult. The actual value is correct in the file and container — this is a display-level masking, not a real issue.

### Problem 2: Postiz PostgreSQL auth failure
**Symptom**: Postiz Prisma reports "password authentication failed" for `postiz-user` even though the same credentials work from the host.
**Root cause**: The `postgres-postiz-automation` container was recreated with the volume but the password hash in the database didn't match. The `pg_hba.conf` uses `scram-sha-256` for non-localhost connections.
**Fix**: Reset the password with `psql -U postgres -c "ALTER USER \"postiz-user\" WITH PASSWORD 'postiz-password'"` inside the postgres container.

### Problem 3: Hermes terminal cwd not applied
The `terminal` tool's `cwd` parameter sometimes doesn't take effect — commands run from the session's original working directory. **Workaround**: Always use `cd /absolute/path &&` prefix or absolute paths in commands.

### Problem 4: Hermes terminal password masking
The terminal tool masks strings containing `password` as `***`, making it impossible to verify credential values in output. This is a display-level masking only.

### Problem 5: Tool name confusion
The tool is named `terminal`, not `shell`. Repeated muscle-memory errors caused wasted tool calls.

### Problem 6: npx vs local binary
`npx remotion` resolves to a different (older) version than the local `node_modules/.bin/remotion`. Always use the local binary.

### Problem 7: pnpm vs npm
pnpm didn't create `node_modules/.bin/` links properly in this environment. Using `npm install` instead resolved the issue.

### Problem 8: DeepFilterNet enhance() API change
The `enhance()` function signature changed in DeepFilterNet 0.5.6 — it now takes `audio: torch.Tensor` directly instead of a file path. Use the `deep-filter-py` CLI for file I/O instead.
