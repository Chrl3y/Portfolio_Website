# AUTOmation Roadmap

## Phase 0 — Documentation and decisions
- Confirm canonical portfolio implementation: current static repo vs planned Astro/BRAIN pipeline.
- Confirm priority social accounts and ownership boundaries.
- Confirm hosting target for n8n/Postiz and media workers.
- Confirm which monetization programs can onboard/pay a Uganda-based publisher.

## Phase 1 — Safe content intake
- Define canonical content schema aligned with existing BRAIN publication metadata.
- Build intake from approved Markdown/notes and one user-owned recording.
- Implement `PUBLIC / REVIEW / PRIVATE` classification.
- Add redaction and rights checks.
- Add immutable source references and version hashes.

## Phase 2 — Publishing control plane
- Deploy n8n.
- Deploy Postiz independently.
- Connect Postiz through API/MCP/webhooks.
- Build approval flow and idempotent publishing jobs.
- Support LinkedIn + one secondary channel first, then expand.
- Test Activepieces only for connectors/workflows where it adds distinct value.
- Keep Ayrshare as managed fallback/enterprise adapter.

## Phase 3 — Portfolio content engine
- Migrate or connect portfolio to a structured Markdown/MDX content source.
- Generate article drafts from approved source objects.
- Add canonical URLs, tags, related content, CTAs, structured metadata, sitemap/RSS, and analytics hooks.
- Add newsletter capture.

## Phase 4 — Voice-preserving video engine
- Transcribe with Whisper/faster-whisper.
- Generate scene plans from timestamps.
- Create reusable Remotion brand components.
- Add Manim for precise technical animation where needed.
- Use Vizard for clipping, reframing, captions, B-roll, and distribution support.
- Produce 16:9 master + 9:16 short from one source recording.

## Phase 5 — Analytics feedback loop
- Generate consistent campaign IDs and UTM parameters.
- Collect portfolio traffic/conversions.
- Collect social publication IDs and available metrics.
- Rank content by meaningful outcomes: qualified traffic, saves/shares, newsletter signups, affiliate clicks, inquiries, product conversions—not raw impressions only.
- Feed winning topics/formats back into content planning.

## Phase 6 — Affiliate engine
- Build affiliate registry.
- Verify network/program acceptance, KYC, tax, payout, and Uganda availability before use.
- Add contextual merchant matching.
- Add disclosure component.
- Add click/sub-ID attribution.
- Start with tools genuinely used in tutorials/content.

## Phase 7 — Display ads and sponsorships
- Prepare privacy/about/contact/disclosure pages and original content base.
- Apply for AdSense when site is ready.
- Keep ads primarily in Insights/Blog/Lab, not flagship portfolio pages.
- At higher relevant traffic, evaluate developer-focused networks and direct sponsors.

## Phase 8 — Paid growth
- Use organic performance as the testing layer.
- Promote only proven content/offers.
- Add conversion pixels/server-side events deliberately.
- Maintain strict spend caps and approval around paid campaigns until attribution is reliable.

## Definition of first useful release
A source note or recording can be ingested, classified, turned into one portfolio draft and channel-specific social drafts, approved, published through Postiz, tagged with campaign attribution, and measured afterward—without exposing secrets/private work material.
