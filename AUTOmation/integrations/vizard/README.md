# Vizard Adapter

## Purpose
Vizard.ai is a hosted video clipping service that auto-generates short-form clips from long-form content (highlights, chapters, etc.).

This is a **config-only adapter** — no API keys stored, no services cloned.

## API Endpoint Usage

```
POST https://api.vizard.ai/v1/video
Content-Type: application/json
Authorization: Bearer {{VIZARD_API_KEY}}

{
  "video_url": "https://example.com/recording.mp4",
  "language": "en",
  "max_clip_duration": 60,
  "num_clips": 3
}
```

## Required Env Vars
- `VIZARD_API_KEY` — Vizard API key (NOT stored in repo, only in `.env` locally)

## Webhook Strategy
- Vizard calls back to: `http://<n8n-host>:5678/webhook/vizard-callback`
- n8n validates the webhook signature
- n8n then triggers the Postiz publishing layer

## Expected Request/Response

### Request
```json
{
  "video_url": "https://...",
  "language": "en",
  "max_clip_duration": 60,
  "num_clips": 3
}
```

### Response
```json
{
  "task_id": "vzr_12345",
  "status": "processing",
  "clips": []
}
```

## What n8n Will Call
1. `Workflow B` sends recording URL to Vizard API
2. n8n waits for webhook callback with clip URLs
3. n8n forwards clip URLs to Postiz for publishing

## What Data Must Be Stored Locally
- `task_id` → maps to local content-item ID
- Generated clip URLs (stored in content-item.json)
- Processing status (stored in publishing-job.json)
