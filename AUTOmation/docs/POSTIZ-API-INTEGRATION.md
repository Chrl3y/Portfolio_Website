# Postiz API Integration

## Overview

Postiz's self-hosted public API is available at `/public/v1/` on the Postiz backend container.
Version verified: **v1.47.0**

## Container Network vs Host URLs

**Container-internal** (for n8n inside the same Docker network):
```
http://postiz-automation:3004/public/v1/
```

**Host/browser** (for local testing from outside Docker):
```
http://localhost:3004/public/v1/
```

Inside the Postiz stack, the backend NestJS server listens on port 3000, while nginx
acts as a reverse proxy on port 5000. Docker maps port 5000 to host port 3004.

## Authentication

The public API uses **API key authentication** via the `Authorization` header.

The API key is stored per-organization and can be found in the Postiz dashboard under
Settings → API Keys. It can also be auto-generated via the `getOrgByApiKey` flow
(middleware `PublicAuthMiddleware`).

```
Authorization: <your-api-key>
```

Or via OAuth token (starts with `pos_`):
```
Authorization: pos_<oauth-token>
```

**No API key is set** in the local dev environment `.env.example`. The key must be
generated from the Postiz dashboard after first login.

## Endpoints

### Create Post
```
POST /public/v1/posts
```

Headers:
```
Authorization: <api-key>
Content-Type: application/json
```

Body:
```json
{
  "type": "draft",
  "creationMethod": "API",
  "posts": [
    {
      "identifier": "linkedin",
      "value": [
        {
          "text": "Post content here",
          "image": []
        }
      ]
    }
  ]
}
```

- `type`: `"draft"` or `"post"`. **Always use `"draft"` during development.**
- `creationMethod`: `"API"` or `"CLI"`
- `identifier`: Social platform identifier (e.g., `linkedin`, `twitter`, `mastodon`)
- At least one integration must be configured per group for non-draft posts

### Get Posts
```
GET /public/v1/posts
```

Query params: `page`, `perPage`

### Delete Post
```
DELETE /public/v1/posts/:id
DELETE /public/v1/posts/group/:group
```

### Media Upload
```
POST /public/v1/upload
Content-Type: multipart/form-data
```

File field name: `file`. Allowed MIME types:
- `image/jpeg`, `image/png`, `image/gif`, `image/webp`, `image/avif`, `image/bmp`, `image/tiff`
- `video/mp4`

### Upload From URL
```
POST /public/v1/upload-from-url
{
  "url": "https://example.com/image.png"
}
```

### List Integrations (Connected Channels)
```
GET /public/v1/integrations?group=<groupId>
```

Returns connected social channels with identifiers (e.g., `twitter`, `linkedin`).

### Check Connection
```
GET /public/v1/is-connected
```

Returns `{ connected: true }` if the org has at least one integration.

### List Groups
```
GET /public/v1/groups
```

Returns customer/groups with IDs and names.

### Social Auth URL
```
GET /public/v1/social/:integration
```

Generates an OAuth URL for connecting a social account. This is how new social
accounts are connected — do NOT use this during development (no live accounts).

### Find Free Slot
```
GET /public/v1/find-slot/:id
```

Finds a free scheduling slot for a given integration.

### Generate Video (Postiz's own video generation)
```
POST /public/v1/generate-video
```

### Notifications
```
GET /public/v1/notifications
```

## Draft Behavior

When `type: "draft"` is passed, Postiz creates the post as a draft that can be
reviewed and published later from the dashboard. This is the **only** safe mode
for development.

**No draft creation is permitted unless:**
1. `classification` is not `PRIVATE`
2. `approval_status` is `APPROVED`
3. `confidentiality_checked` is `true`

## Scheduling Format

Posts can be scheduled using the `find-slot` endpoint to find available time slots,
then posting with a specific datetime. The date/time should be provided in ISO 8601
format.

## Container Network Details

Within the Postiz Docker Compose network (`postiz-network`):

| Service | Hostname | Internal Port |
|---------|----------|---------------|
| Postiz app | `postiz-automation` | 5000 (nginx → 3000 backend, 4200 frontend) |
| PostgreSQL | `postgres-postiz` | 5432 |
| Redis | `redis-postiz` | 6379 |
| Temporal | `temporal-postiz` | 7233 |
| Elasticsearch | `temporal-elasticsearch` | 9200 |

## Environment Variables Reference

Key environment variables in `infra/postiz/docker-compose.yml`:

| Variable | Value | Notes |
|----------|-------|-------|
| `MAIN_URL` | `http://localhost:3004` | Public-facing URL |
| `BACKEND_INTERNAL_URL` | `http://localhost:3000` | Backend NestJS port (NOT 5000) |
| `DATABASE_URL` | `postgresql://postiz-user:***@postgres-postiz:5432/postiz-db-local` | Password is `postiz-dev-pass` |
| `REDIS_URL` | `redis://redis-postiz:6379` | Redis for caching + queues |
| `TEMPORAL_ADDRESS` | `temporal-postiz:7233` | Temporal workflow engine |
| `API_LIMIT` | `30` | Rate limiting (requests per minute) |

## Test Commands

```bash
# Health check
curl -s -o /dev/null -w "%{http_code}" http://localhost:3004/auth
# Expected: 200

# API without auth (should return 401)
curl -s -w "\n%{http_code}" http://localhost:3004/public/v1/integrations
# Expected: 401 "No API Key found"
```
