# AUTOmation — Resources & Access Guide

> Updated: 2026-09-10

## Running Services (UI Access)

| Service | UI URL | API URL (Container) | API URL (Host) | Container | Port |
|---------|--------|---------------------|-----------------|-----------|------|
| n8n (workflow orchestration) | http://localhost:5678 | n/a (internal UI) | http://localhost:5678 | `n8n-automation` | 5678 |
| Postiz (social publishing) | http://localhost:3004 | http://postiz-automation:3004 | http://localhost:3004 | `postiz-automation` (nginx) | 3004 |
| | | http://postiz-automation:3000 | http://localhost:3000 | `postiz-automation` (NestJS) | 3000 |
| PostgreSQL (Postiz DB) | — | postgres-postiz-automation:5432 | localhost:5433 | `postgres-postiz-automation` | 5433 |
| Redis (cache/queue) | — | redis-postiz-automation:6379 | localhost:6380 | `redis-postiz-automation` | 6380 |
| Temporal (workflow engine) | — | temporal-postiz-automation:7233 | localhost:7233 | `temporal-postiz-automation` | 7233 |
| Elasticsearch (Temporal) | — | temporal-elasticsearch-automation:9200 | localhost:9201 | `temporal-elasticsearch-automation` | 9201 |
| Content API | http://localhost:8010 | n/a | http://localhost:8010 | (local process) | 8010 |

**Note on Docker contexts:** n8n runs under **OrbStack** (`--context orbstack`), Postiz runs under **Docker Desktop** (`desktop-linux`).

## Python Environments (Canonical Paths)

All venvs are under `AUTOmation/runtime/`:

| Environment | Path | Python | Purpose | Status |
|-------------|------|--------|---------|--------|
| faster-whisper | `runtime/faster-whisper-env/` | 3.12 | Transcription (tiny/small, CPU) | ✅ Working — recognizes speech |
| WhisperX | `runtime/whisperx-env/` | 3.12 | Alignment + diarization | ✅ Import OK |
| DeepFilterNet | `runtime/deepfilternet-env/` | 3.12 | Noise reduction CLI | ✅ Model loads, CLI works |
| Manim | `runtime/manim-env/` | 3.12 | Technical animations | ✅ Renders (29s MP4) |
| content-api | `runtime/content-api-env/` | 3.12 | FastAPI content API | ✅ All endpoints working |

**Activate pattern:**
```bash
source AUTOmation/runtime/faster-whisper-env/bin/activate
python script.py
deactivate
```

**Direct invocation pattern (for scripts):**
```bash
AUTOmation/runtime/faster-whisper-env/bin/python script.py
```

## Node.js Projects

| Project | Path | Status | UI Access |
|---------|------|--------|-----------|
| Remotion | `media/remotion/` | ✅ Renders (6s MP4) | Local (Node CLI) |
| Mermaid CLI | Global npm | ✅ SVG rendering | Local (CLI) |

## Database

| File | Path | Gitignored |
|------|------|------------|
| Content store | `runtime/data/automation.db` | ✅ Yes |

## Job Output Directory

```
runtime/jobs/<content-id>/     # gitignored
├── source.json
├── transcript.json
├── captions.srt / .vtt / .json
├── scene-plan.json
├── audio-original.wav
├── audio-clean.wav
├── renders/
├── master.mp4
└── job.json
```

## Content API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/content` | Create content item |
| GET | `/content` | List all items |
| GET | `/content/{id}` | Get item |
| PATCH | `/content/{id}` | Update fields |
| POST | `/content/{id}/approve` | Approve (records audit) |
| POST | `/content/{id}/reject` | Reject (records audit) |
| POST | `/content/{id}/classify` | Change classification |
| GET | `/content/{id}/transcript` | Get transcript |
| GET | `/content/{id}/scene-plan` | Get scene plan |
| GET | `/content/{id}/media` | Get media assets |
| GET | `/content/{id}/publications` | Get publications |

## Safety Gate (Before Any Publishing)

The `can_publish()` method in `ContentStore` enforces:
1. `classification != PRIVATE`
2. `approval_status == APPROVED`
3. `confidentiality_checked == true`

**No workflow may call Postiz/Ayrshare without passing all three checks.**
