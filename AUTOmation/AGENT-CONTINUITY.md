# Agent Continuity

## Purpose

This file is the handoff point for any future agent working on the portfolio automation/media-growth system.

## Current state

Created on branch `feature/automation-media-growth`.

Implemented so far:
- Project architecture and tool-role decisions.
- Documentation skeleton for orchestration, video repurposing, monetization, and security.
- No live credentials connected.
- No deployments performed.
- No autonomous publishing enabled.

## Decisions already made

1. Keep the portfolio as the public website/traffic destination.
2. Keep automation services logically separate under `AUTOmation/`.
3. Prefer service integration over vendoring third-party applications into the portfolio.
4. n8n is the primary orchestrator.
5. Postiz is the preferred self-hosted social publishing layer.
6. Activepieces is evaluated as a complementary connector/automation layer, not automatically duplicated with n8n.
7. Ayrshare remains an optional paid SaaS social API adapter for broader/managed coverage.
8. Vizard handles clipping, captioning, B-roll, social-ready edits, and publishing support.
9. Remotion/Manim are the preferred controllable rendering tools for animated explanations and infographics while preserving the creator's real narration.
10. All content passes `PUBLIC`, `REVIEW`, or `PRIVATE` classification before distribution.
11. Company/client/internal content defaults to `PRIVATE`.
12. Affiliate links must be contextual, disclosed, tracked, and never inserted solely to maximize clicks.

## Expected source systems

Potential source material:
- Obsidian/BRAIN notes.
- Publication Pipeline / Content Seeds.
- Project CHANGELOG files.
- GitHub commits/releases/issues.
- Screenshots/photos.
- Recorded explanations and teachings.
- Meeting/event notes that are explicitly cleared for public use.
- Finished public projects/case studies.

Do not assume any raw work note is publishable.

## Target lifecycle

```text
SOURCE
 -> normalize
 -> classify
 -> redact
 -> extract claims/assets
 -> draft canonical content object
 -> create channel variants
 -> human approval where required
 -> publish/schedule
 -> collect analytics
 -> attribute traffic/revenue
 -> identify reusable winners
 -> update content strategy
```

## Minimum content object fields

Future implementation should carry at least:

```yaml
id:
source_id:
source_type:
title:
summary:
topics: []
classification: PUBLIC|REVIEW|PRIVATE
approval_status: pending|approved|rejected
claims_checked: false
confidentiality_checked: false
canonical_url:
media_assets: []
channels: []
campaign_id:
utm:
  source:
  medium:
  campaign:
  content:
affiliate_candidates: []
published_urls: []
analytics_status:
created_at:
updated_at:
```

## Secrets policy

Never commit:
- OAuth access/refresh tokens.
- API keys.
- Social platform secrets.
- Webhook signing secrets.
- Database credentials.
- Affiliate private keys or payment credentials.

Use `.env`, secret stores, or platform credential vaults. Keep only `.env.example` in Git.

## Next agent tasks

Priority order:

1. Inspect the user's current BRAIN/portfolio publication pipeline and align metadata instead of inventing a competing content schema.
2. Build a local/self-host deployment plan for n8n + Postiz; decide whether Activepieces adds distinct value before deploying it.
3. Implement a test intake workflow using non-sensitive sample content.
4. Add Postiz adapter/webhook definitions.
5. Add portfolio draft-generation output (prefer Markdown/MDX if the portfolio is migrated to Astro; current repo is static HTML).
6. Build video prototype using one user-owned recording: transcript -> scene plan -> Remotion/Manim visuals -> original narration -> captions -> vertical and horizontal outputs.
7. Connect analytics only after canonical URLs and campaign conventions are defined.
8. Implement affiliate registry + disclosure component before inserting any affiliate links.
9. Add monetization dashboards after real traffic/revenue data exists.

## Important mismatch to resolve

This GitHub repository currently contains a static HTML/CSS/JS portfolio, while earlier planning discussed an Astro portfolio fed from BRAIN. A future agent must determine whether:
- this repo is temporary/legacy,
- it should be migrated to Astro,
- or the Astro project exists elsewhere locally/private and this repo should only receive documentation/integration hooks.

Do not blindly rebuild the content layer until that is resolved.

## Safety check before live activation

No agent should enable unattended posting until all are true:
- social credentials are stored securely;
- content classification works;
- approval workflow works;
- redaction/privacy checks work;
- failure/retry logs exist;
- rate limits are understood;
- platform policy constraints are documented;
- delete/correction workflow exists;
- analytics identifiers and disclosure rules are implemented.
