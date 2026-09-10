# LOCAL SETUP — AUTOmation Media Stack

## Prerequisites

- macOS 14+ (Sonoma or later)
- Apple Silicon (M1/M2/M3) — tested on M1 Pro
- Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Docker Desktop (for Postiz stack) + OrbStack (for n8n)

## System Dependencies

```bash
brew install ffmpeg
brew install python
brew install uv
brew install node
brew install pnpm
```

## Python Environments

All Python environments use `uv` with Python 3.12 and live under `runtime/` (with the exception of DeepFilterNet):

```bash
# ALWAYS start from the AUTOmation root
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1

# faster-whisper (transcription)
uv venv --python 3.12 runtime/faster-whisper-env
source runtime/faster-whisper-env/bin/activate
uv pip install faster-whisper
deactivate

# WhisperX (alignment + diarization)
uv venv --python 3.12 runtime/whisperx-env
source runtime/whisperx-env/bin/activate
uv pip install torch --index-url https://download.pytorch.org/whl/cpu
uv pip install whisperx
deactivate

# DeepFilterNet (noise reduction)
uv venv --python 3.12 deepfilternet-env
source deepfilternet-env/bin/activate
uv pip install deepfilternet
uv pip install torch torchaudio
deactivate

# Manim (technical animations)
uv venv --python 3.12 runtime/manim-env
source runtime/manim-env/bin/activate
uv pip install manim
deactivate
```

### Apple Silicon Notes

- PyTorch CPU builds work via `--index-url https://download.pytorch.org/whl/cpu`
- MPS (Metal Performance Shaders) is NOT recommended for faster-whisper — CPU mode is more stable
- Manim runs natively on macOS ARM
- DeepFilterNet runs on CPU (no GPU needed for basic noise reduction)

## Docker Services

### n8n (runs under OrbStack context)
```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1
docker --context orbstack compose -f infra/docker-compose.yml up -d
# UI: http://localhost:5678
```

### Postiz (runs under Docker Desktop context)
Postiz requires PostgreSQL, Redis, and Temporal. Uses the official docker-compose template:

```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1
cp infra/postiz/.env.example /tmp/postiz-env-clean
# Edit /tmp/postiz-env-clean to set POSTGRES_PASSWORD, BACKEND_INTERNAL_URL=http://localhost:3000
docker compose -f infra/postiz/docker-compose.yml --env-file /tmp/postiz-env-clean up -d
# UI: http://localhost:3004
```

## Node.js Tooling

```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation/media/remotion || exit 1
npm install
node_modules/.bin/remotion compositions index.jsx
mkdir -p renders
node_modules/.bin/remotion render index.jsx ViciExplainer renders/vici-explainer.mp4
```

## Mermaid CLI

```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1
# Install Chrome for Testing (required for headless rendering)
npx puppeteer browsers install chrome
# Install mermaid CLI
npm install -g @mermaid-js/mermaid-cli
# Render (use puppeteer config for Chrome path)
PUPPETEER_EXECUTABLE_PATH="$(node -e "console.log(require('puppeteer').executablePath())")" \
  mmdc -i docs/architecture-diagram.mmd -o docs/architecture-diagram.svg -t dark
```

## Verification Commands

```bash
cd /Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation || exit 1

# faster-whisper (generates test speech if no arg provided)
source runtime/faster-whisper-env/bin/activate
python tests/test_transcription.py tests/transcription-test.wav
deactivate

# WhisperX
source runtime/whisperx-env/bin/activate
python -c "import whisperx; print('WhisperX OK')"
deactivate

# DeepFilterNet
source deepfilternet-env/bin/activate
deep-filter-py --help
deactivate

# Manim
runtime/manim-env/bin/manim media/manim/scene.py AutomationFlow -ql -o automation-flow-preview

# Remotion
cd media/remotion && ../node_modules/.bin/remotion render index.jsx ViciExplainer renders/vici-explainer.mp4

# n8n
curl -s -o /dev/null -w "%{http_code}" http://localhost:5678

# Postiz
curl -s -o /dev/null -w "%{http_code}" http://localhost:3004/auth

# Mermaid
npx -y @mermaid-js/mermaid-cli --version

# Docker (Postiz stack)
docker compose -f infra/postiz/docker-compose.yml ps

# Docker (n8n — OrbStack context)
docker --context orbstack compose -f infra/docker-compose.yml ps
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
│   ├── docker-compose.yml          # n8n (port 5678, OrbStack context)
│   └── postiz/
│       ├── docker-compose.yml      # Postiz + Temporal + PostgreSQL + Redis
│       └── dynamicconfig/
│           └── development-sql.yaml
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
├── runtime/                        # Python venvs (canonical location)
│   ├── faster-whisper-env/
│   ├── whisperx-env/
│   └── manim-env/
├── deepfilternet-env/              # DeepFilterNet venv (root level)
├── voice/
│   └── README.md
├── integrations/
│   ├── vizard/README.md
│   └── ayrshare/README.md
├── media/
│   ├── remotion/                   # Independent Remotion app
│   │   ├── index.jsx               # Entry point (registerRoot)
│   │   ├── ViciExplainer.jsx       # Test composition
│   │   ├── VideoSchema.jsx
│   │   ├── package.json
│   │   ├── package-lock.json
│   │   ├── node_modules/            (gitignored)
│   │   └── renders/                 (gitignored)
│   ├── manim/                      # Manim project source
│   │   ├── scene.py
│   │   └── renders/                 (gitignored)
│   └── puppeteer.config.json        # Chrome path for Mermaid CLI
├── docs/
│   ├── ARCHITECTURE.md
│   ├── TOOLING-RESEARCH.md
│   ├── VIDEO-REPURPOSING.md
│   ├── MONETIZATION-AFFILIATES.md
│   ├── ROADMAP.md
│   ├── LOCAL-SETUP.md
│   ├── architecture-diagram.mmd
│   ├── architecture-diagram.svg
│   └── railroad-diagram.mmd
├── vendor/                         # NOT COMMITTED (see .gitignore)
│   ├── remotion/
│   ├── postiz-app/
│   ├── postiz-docker-compose/
│   ├── manim/
│   └── mermaid/
└── renders/                         # NOT COMMITTED
```
