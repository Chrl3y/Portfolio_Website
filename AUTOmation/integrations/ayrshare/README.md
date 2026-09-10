# Ayrshare Adapter

## Purpose
Ayrshare is a hosted social media publishing platform that posts to multiple networks (X, LinkedIn, TikTok, YouTube, etc.) from a single API.

This is a **config-only adapter** — no API keys stored, no services cloned.

## API Endpoint Usage

```
POST https://api.ayrshare.com/v1/post
Content-Type: application/json
Authorization: Bearer {{AYRSHARE_API_KEY}}

{
  "post": "Check out this video!",
  "media_urls": ["https://example.com/video.mp4"],
  "platforms": ["twitter", "linkedin", "youtube"],
  "schedule_date": "2026-01-01T12:00:00Z"
}
```

## Required Env Vars
- `AYRSHARE_API_KEY` — Ayrshare API key (NOT stored in repo, only in `.env` locally)
- `AYRSHARE_PROFILE_KEY` — Optional, for specific user profiles

## Webhook Strategy
- Ayrshare calls back to: `http://<n8n-host>:5678/webhook/ayrshare-status`
- n8n validates the webhook and updates the publishing-job status
- Ayrshare sends platform-specific permalinks back via webhook

## Expected Request/Response

### Request
```json
{
  "post": "Caption text",
  "media_urls": ["https://cdn.example.com/video.mp4"],
  "platforms": ["twitter", "linkedin"],
  "schedule_date": "2026-01-01T12:00:00Z"
}
```

### Response
```json
{
  "id": "abc123",
  "status": "scheduled",
  "postIds": {
    "twitter": "123456789",
    "linkedin": "987654321"
  },
  "errors": {},
  "success": true
}
```

## What n8n Will Call
1. `Workflow C` takes an approved content object
2. n8n sends the media URL + caption to Ayrshare API
3. n8n polls or receives webhook callbacks for status updates
4. n8n stores the published URLs in the content-item

## What Data Must Be Stored Locally
- `ayrshare_id` → maps to local content-item ID
- `postIds` → per-platform post IDs
- Published permalinks (stored in content-item.json)
- Status updates (stored in publishing-job.json)

## Note
Postiz is the primary publishing layer for this stack. Ayrshare is a fallback/secondary option for multi-network publishing that Postiz doesn't directly support.
