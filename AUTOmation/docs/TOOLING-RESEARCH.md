# Tooling Research

This document records the current role of each major tool in the AUTOmation architecture. Re-verify pricing, limits, platform support, and terms before production deployment because these change frequently.

## Decision summary

| Tool | Role | Deployment stance | Why |
|---|---|---|---|
| n8n | Primary orchestrator/control plane | Self-host preferred | Strong workflow engine, agent/MCP direction, broad integrations, webhooks, retries, credential handling |
| Postiz | Primary social publishing service | Self-host preferred | Social scheduling/publishing focus, open source, MCP/API orientation, many social networks |
| Activepieces | Secondary automation/connector layer | Self-host optional | Useful connector catalogue and MCP/agent capabilities; use where it adds distinct value rather than duplicating n8n |
| Ayrshare | Managed social API | SaaS/API | Broad multi-network API and analytics; useful when managed reliability or a supported network is easier through one vendor |
| Vizard | AI video repurposing | SaaS/API | Highlight detection, clipping, captions, B-roll, resizing, social-ready publishing |
| Remotion | Programmatic animation/video rendering | Local/worker/container | React-based reproducible video compositions and branded explainers |
| Manim | Precision animation | Local/worker/container | Technical/math/diagram animation where deterministic motion is valuable |
| Whisper / faster-whisper | Transcription | Local or hosted worker | Time-aligned transcripts for video/audio processing |

## Postiz

Use Postiz as the social distribution surface, not as the content intelligence layer.

Target responsibilities:
- schedule/publish approved content;
- hold platform connections;
- expose posting operations to n8n/agents;
- return publishing status/URLs;
- optionally provide social inbox/analytics functionality where available;
- act as the primary social adapter for platforms it supports well.

Upstream:
- https://github.com/gitroomhq/postiz-app
- https://docs.postiz.com/

Integration pattern:

```text
n8n -> Postiz API/MCP -> social network
                 -> status/webhook -> n8n
```

Do not fork Postiz into the portfolio unless we intentionally plan to maintain custom upstream patches. Prefer an independent deployment and a thin adapter.

## n8n

n8n is the primary stateful workflow orchestrator.

Use for:
- schedules/cron;
- webhooks;
- source ingestion;
- AI calls;
- classification/redaction gates;
- branching/approval states;
- content transformation;
- Postiz/Ayrshare/Vizard calls;
- analytics ingestion;
- affiliate matching;
- alerts/retries/dead-letter handling;
- MCP-facing workflows where appropriate.

Official references:
- https://docs.n8n.io/
- https://n8n.io/mcp/

Do not put irreversible publish actions directly after an LLM node without validation/approval controls.

## Activepieces

Activepieces is worth keeping in the architecture because it has a large connector ecosystem and agent/MCP direction, but running two full workflow engines creates operational overhead.

Use criteria:
- choose Activepieces for a connector/piece that is materially easier or absent in n8n;
- use it for isolated workflows if its piece catalogue is superior;
- avoid maintaining duplicate versions of the same workflow in both platforms.

Official references:
- https://github.com/activepieces/activepieces
- https://www.activepieces.com/docs/

Initial recommendation: document and test it, but deploy n8n first.

## Ayrshare

Ayrshare is a managed API option for cross-platform publishing and social data. It can serve as:
- fallback when a Postiz integration is weak or unavailable;
- a managed alternative if self-hosted social platform maintenance becomes expensive;
- an enterprise abstraction for multi-profile/customer scenarios;
- analytics/history/comments/DM integration where supported.

Official:
- https://www.ayrshare.com/

Keep all Ayrshare use behind an adapter so it can be replaced without changing the content model.

## Vizard

Vizard is positioned in the pipeline after long-form source preparation and before final publication.

Use it for:
- clip discovery;
- short-form repurposing;
- automatic captions;
- reframing;
- B-roll assistance;
- social publishing where useful.

Official docs:
- https://docs.vizard.ai/

Do not rely on Vizard projects as the only archive of the creative pipeline. Save transcript, scene metadata, captions, assets, and publication metadata in our own system.

## Remotion

Remotion is a strong fit for the user's desire to keep their own narration while regenerating the visuals as animations/infographics.

Use it to render reusable compositions from JSON/scene-plan input. Example components:
- branded title;
- architecture diagram animation;
- statistic card;
- timeline;
- code snippet;
- quote/scripture card;
- chart;
- image + callout;
- CTA/outro.

Official:
- https://www.remotion.dev/

## Manim

Manim is complementary to Remotion. Use it when the visual itself benefits from programmatic mathematical/technical animation rather than standard motion graphics.

Official:
- https://docs.manim.community/

## Tool-selection principle

Do not chain every tool into every workflow. Use the smallest reliable chain for each content type.

Examples:

```text
Text note -> n8n -> LLM -> approval -> Postiz
Long video -> transcription -> scene plan -> Remotion/Vizard -> approval -> Postiz
Quick clip -> Vizard -> approval -> Postiz
Managed social API edge case -> n8n -> Ayrshare
Rare connector unavailable in n8n -> Activepieces -> webhook back to n8n
```

## Open questions for implementation

1. Which social accounts are priority 1?
2. Which accounts are personal versus company-owned?
3. Does the user want one Postiz workspace or separate identities/brands?
4. Where will n8n/Postiz databases and object storage live?
5. Which portfolio implementation is canonical: current static repo or planned Astro/BRAIN pipeline?
6. Which analytics stack is canonical: GA4/Search Console only or plus first-party event store/Metabase?
7. Which affiliate networks successfully onboard/pay publishers in Uganda?
