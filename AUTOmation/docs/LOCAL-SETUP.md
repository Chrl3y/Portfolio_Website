# LOCAL SETUP — AUTOmation Media Stack

## Prerequisites

- macOS 14+ (Sonoma or later)
- Apple Silicon (M1/M2/M3) — tested on M1 Pro
- Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Docker Desktop or OrbStack

## System Dependencies

```bash
brew install ffmpeg
brew install python
brew install uv
brew install node
brew install pnpm
```

## Python Environments

All Python environments use `uv` with Python 3.12:

```bash
cd AUTOmation

# faster-whisper (transcription)
uv venv --python 3.12 runtime/faster-whisper-env
source runtime/faster-whisper-env/bin/activate
uv pip install faster-whisper

# WhisperX (alignment + diarization)
uv venv --python 3.12 runtime/whisperx-env
source runtime/whisperx-env/bin/activate
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install whisperx

# DeepFilterNet (noise reduction)
uv venv --python 3.12 deepfilternet-env
source deepfilternet-env/bin/activate
uv pip install deepfilternet
uv pip install torch torchaudio

# Manim (technical animations)
uv venv --python 3.12 manim-env
source manim-env/bin/activate
uv pip install manim
```

### Apple Silicon Notes

- PyTorch CPU builds work via `--index-url https://download.pytorch.org/whl/cpu`
- MPS (Metal Performance Shaders) is NOT recommended for faster-whisper — CPU mode is more stable
- Manim runs natively on macOS ARM via Homebrew Python
- DeepFilterNet runs on CPU (no GPU needed for basic noise reduction)

## Docker Services

### n8n
```bash
docker compose -f AUTOmation/infra/docker-compose.yml up -d n8n
# UI: http://localhost:5678
```

### Postiz
Postiz requires PostgreSQL, Redis, and Temporal. Use the official docker-compose:

```bash
# Clone official repo (already in vendor/postiz-docker-compose)
docker compose -f AUTOmation/infra/postiz/docker-compose.yml --env-file /tmp/postiz-env-clean up -d
# UI: http://localhost:3004
```

### Activepieces (deferred)
See Phase 14 notes.

## Node.js Tooling

```bash
cd AUTOmation/media/remotion
npm install
npx remotion render index.jsx ViciExplainer renders/vici-explainer.mp4 --duration 180 --fps 30
```

## Mermaid CLI

```bash
# Requires Chrome for Testing (install first)
npx puppeteer browsers install chrome
npm install -g @mermaid-js/mermaid-cli
mmdc -i docs/architecture-diagram.mmd -o docs/architecture-diagram.svg -t dark -p media/puppeteer.config.json
```

## Verification Commands

```bash
# faster-whisper
source runtime/faster-whisper-env/bin/activate
python tests/test_transcription.py tests/test-audio.wav

# DeepFilterNet
source deepfilternet-env/bin/activate
python tests/test_deepfilter.py tests/test-audio.wav

# Manim
source manim-env/bin/activate
manim media/manim/scene.py AutomationFlow -pql

# Remotion
cd media/remotion && npx remotion render index.jsx ViciExplainer renders/vici-explainer.mp4 --duration 180 --fps 30

# n8n
curl -s -o /dev/null -w "%{http_code}" http://localhost:5678

# Postiz
curl -s -o /dev/null -w "%{http_code}" http://localhost:3004/

# Mermaid
mmdc -i docs/architecture-diagram.mmd -o docs/architecture-diagram.svg -t dark
```

## Directory Layout

```
AUTOmation/
├── CHANGELOG.md
├── AGENT-CONTINUITY.md
├── SECURITY.md
├── .env.example
├── .gitignore
├── resources.yml
├── scripts/
│   ├── bootstrap-resources.sh
│   ├── clean-audio.sh
│   └── repair-voice.py
├── infra/
│   ├── docker-compose.yml          # n8n
│   └── postiz/
│       ├── docker-compose.yml      # Postiz + Temporal + PostgreSQL + Redis
│       └── puppeteer.config.json
├── schemas/
│   ├── content-item.schema.json
│   ├── publishing-job.schema.json
│   └── video-scene-plan.schema.json
├── workflows/
│   ├── content-intake.json
│   ├── video-intake.json
│   └── publish-draft.json
├── tests/
│   ├── test_transcription.py
│   ├── test_whisperx.py
│   └── test_deepfilter.py
├── runtime/                        # Python venvs
│   ├── faster-whisper-env/
│   └── whisperx-env/
├── deepfilternet-env/              # DeepFilterNet venv
├── manim-env/                      # Manim venv
├── voice/
│   └── README.md
├── integrations/
│   ├── vizard/README.md
│   └── ayrshare/README.md
├── media/
│   ├── remotion/                   # Independent Remotion app
│   │   ├── index.jsx
│   │   ├── ViciExplainer.jsx
│   │   ├── VideoSchema.jsx
│   │   ├── package.json
│   │   └── renders/
│   ├── manim/                      # Manim project
│   │   ├── scene.py
│   │   ├── manim-env/
│   │   └── renders/
│   └── puppeteer.config.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── TOOLING-RESEARCH.md
│   ├── VIDEO-REPURPOSING.md
│   ├── MONETIZATION-AFFILIATES.md
│   ├── ROADMAP.md
│   ├── LOCAL-SETUP.md
│   ├── architecture-diagram.mmd
│   ├── architecture-diagram.svg
│   └── architecture-diagram.png
├── vendor/                         # NOT COMMITTED
│   ├── remotion/
│   ├── postiz-app/
│   ├── postiz-docker-compose/
│   ├── manim/
│   └── mermaid/
├── renders/                        # NOT COMMITTED
└── models/                         # NOT COMMITTED
```
