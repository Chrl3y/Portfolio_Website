# AUTOmation Architecture

## System boundary

AUTOmation is the automation/media/growth subsystem. The portfolio website is the public destination, not the workflow engine.

```text
BRAIN / GitHub / recordings / photos / public project activity
                         |
                         v
                Source Intake Layer
                         |
                         v
                 n8n Orchestrator
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
     Classification   Content AI     Media Pipeline
 PUBLIC/REVIEW/PRIVATE   drafts     transcript/scene plan
          |              |              |
          +--------------+--------------+
                         |
                         v
                    Approval Gate
                         |
          +--------------+---------------+
          |              |               |
          v              v               v
       Postiz         Ayrshare         Vizard
     primary social   optional API     clip/publish
          |              |               |
          +--------------+---------------+
                         |
                         v
                 Social platforms
                         |
                         v
                  Portfolio website
                         |
          +--------------+---------------+
          |              |               |
          v              v               v
       Analytics      Affiliates       Leads/Products
          \              |               /
           +-------------+--------------+
                         |
                         v
                  Performance Agent
                         |
                         v
                 Strategy feedback
```

## Canonical content model

External tools must not become the source of truth. Every item should exist first as a canonical content object with classification, approval, campaign, asset, publication, and analytics metadata.

## Orchestration

n8n owns cross-service workflow state. Individual tools own their specialist operations.

Examples:
- Postiz owns social connection/scheduling state.
- Vizard owns clip-generation jobs.
- Remotion/Manim own reproducible render definitions.
- Portfolio owns canonical public URLs.
- Analytics layer owns events/attribution.

## Approval modes

`PUBLIC`: eligible for automated publishing after automated validation.

`REVIEW`: generation can be automated, but publishing requires explicit approval.

`PRIVATE`: may be summarized internally but cannot be sent to publishing or monetization systems.

All work/client/company notes default to `PRIVATE` unless deliberately reclassified.

## Video path

```text
recording
 -> audio cleanup
 -> Whisper/faster-whisper transcript
 -> segmenter
 -> claims/source checker
 -> scene-plan JSON
 -> Remotion/Manim/selected generated visuals
 -> preserve original narration
 -> captions
 -> Vizard for clip extraction/reframing when useful
 -> approval
 -> Postiz/Ayrshare
```

## Traffic attribution

Every distributed link should include a campaign ID and UTM metadata. The canonical article stores the campaign relationship. Affiliate links additionally use merchant/placement IDs and network sub-IDs where supported.

## Failure handling

Publishing jobs need:
- idempotency key;
- external provider job ID;
- retry count;
- last error;
- next retry time;
- manual intervention flag;
- published URL;
- delete/correction state.

## Deployment stance

Prefer independent containers/services for n8n, Postiz, databases, queues, and optional Activepieces. Do not bundle those applications into the static website deployment.

Longer term, object storage should hold media renders while the website stores optimized derivatives/URLs only.
