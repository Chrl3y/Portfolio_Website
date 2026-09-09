# Changelog

## 2026-09-09

### Added
- Created the `AUTOmation` subsystem inside the portfolio repository on branch `feature/automation-media-growth`.
- Added system architecture for source intake, orchestration, approval, social publishing, analytics, affiliates, and feedback loops.
- Added tool-role research covering Postiz, n8n, Activepieces, Ayrshare, Vizard, Remotion, Manim, and transcription tooling.
- Added a voice-preserving video repurposing plan for teachings, explainers, and technical content.
- Added monetization architecture covering affiliates, display ads, sponsorships, digital products, services, and consulting CTAs.
- Added `PUBLIC`, `REVIEW`, and `PRIVATE` publishing controls and secrets guidance.
- Added agent continuity notes so future agents can continue without relying on chat history.

### Decisions
- Do not vendor full Postiz/n8n/Activepieces codebases into the portfolio.
- Deploy large automation/social applications independently and integrate them through APIs, webhooks, and MCP surfaces.
- Use n8n as the primary orchestrator and Postiz as the preferred self-hosted social publishing layer.
- Keep Activepieces as a complementary option rather than duplicating every workflow.
- Keep Ayrshare and Vizard behind adapters as managed services.
- Preserve the user's real recorded voice by default; use Remotion/Manim for controllable animated visuals and Vizard for clipping/short-form assistance.
- Treat affiliate products as a first-class monetization channel with contextual relevance and disclosure.

### Not yet implemented
- No containers deployed.
- No API/social credentials connected.
- No live publishing enabled.
- No analytics/affiliate accounts connected.
- No video renderer code created yet.
- No canonical Astro/BRAIN content pipeline integration completed yet.
