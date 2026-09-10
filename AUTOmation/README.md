# AUTOmation

AUTOmation is the automation, media repurposing, distribution, analytics, and monetization subsystem for the portfolio.

The portfolio remains the public destination and traffic hub. AUTOmation is the control plane that turns approved source material into articles, social posts, videos, analytics feedback, affiliate placements, and growth experiments.

## Core objectives

1. Capture publishable material from BRAIN/Obsidian, project changelogs, GitHub activity, photos, videos, recordings, and approved daily work.
2. Classify every source as `PUBLIC`, `REVIEW`, or `PRIVATE` before any publishing action.
3. Repurpose one approved source into website, LinkedIn, X, Threads, Facebook, Instagram, TikTok, YouTube, newsletter, and other formats.
4. Preserve the creator's real voice for teaching/explainer videos while replacing or augmenting visuals with animations, diagrams, infographics, captions, and B-roll.
5. Publish through official APIs/MCP-enabled platforms rather than browser scraping.
6. Track traffic and conversion with campaign IDs, UTM tags, analytics, affiliate sub-IDs, and revenue events.
7. Feed performance back into future content decisions.
8. Monetize with relevant affiliates, display ads, sponsorships, consulting CTAs, digital products, and services.
9. Keep enough documentation for another AI/coding agent to continue safely without rereading chat history.

## Architecture decision

Do **not** vendor Postiz, n8n, or Activepieces directly into the portfolio source tree. They are large independent services with their own release cycles and databases. Run them as external/self-hosted services and connect them through adapters and webhooks.

- **n8n**: primary orchestration/control plane.
- **Postiz**: primary self-hostable social publishing layer and MCP/API surface.
- **Activepieces**: secondary automation/MCP layer and useful connector catalogue; evaluate as complement/fallback rather than duplicating every n8n flow.
- **Ayrshare**: SaaS social API fallback/enterprise adapter for broad network coverage, analytics, history, comments/DMs, and agent-oriented API workflows.
- **Vizard**: AI clipping, captions, B-roll, short-form edits, and direct social publishing.
- **Remotion**: programmatic React-based video rendering for controlled animated explainers and branded motion graphics.
- **Manim**: precise programmatic diagrams/technical animations where useful.
- **Whisper/faster-whisper**: transcription/timestamp layer for recorded teachings and explanations.
- **Portfolio**: traffic destination, articles/case studies, CTAs, affiliate placements, newsletter capture, and ad inventory.

## Folder map

```text
AUTOmation/
├── README.md
├── AGENT-CONTINUITY.md
├── CHANGELOG.md
├── SECURITY.md
├── .env.example
├── docs/
│   ├── ARCHITECTURE.md
│   ├── TOOLING-RESEARCH.md
│   ├── VIDEO-REPURPOSING.md
│   ├── MONETIZATION-AFFILIATES.md
│   └── ROADMAP.md
└── integrations/
    └── sources.yml
```

## Publishing states

```text
CAPTURED -> CLASSIFIED -> DRAFTED -> REVIEWED -> APPROVED -> SCHEDULED -> PUBLISHED -> MEASURED -> REUSED
```

Rules:

- `PUBLIC`: may enter automated publishing after validation.
- `REVIEW`: requires explicit human approval before publishing.
- `PRIVATE`: never leaves the private system unless reclassified deliberately.
- Company/client/internal material defaults to `PRIVATE`.

## First implementation target

Build one end-to-end vertical slice:

```text
approved note/video
  -> n8n intake
  -> content metadata + transcript
  -> Postiz draft/schedule
  -> portfolio article draft
  -> Vizard short-form clip
  -> UTM links
  -> analytics capture
  -> performance report
```

Do not connect live social credentials or enable blind auto-publishing until the approval and secrets controls in `SECURITY.md` are implemented.

## Official upstream references

- Postiz: https://github.com/gitroomhq/postiz-app
- Postiz docs: https://docs.postiz.com/
- n8n: https://n8n.io/
- n8n MCP: https://n8n.io/mcp/
- Activepieces: https://github.com/activepieces/activepieces
- Activepieces docs: https://www.activepieces.com/docs/
- Ayrshare: https://www.ayrshare.com/
- Vizard API: https://docs.vizard.ai/
- Remotion: https://www.remotion.dev/
- Manim Community: https://docs.manim.community/
- Whisper: https://github.com/openai/whisper
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
