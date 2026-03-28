---
name: kb-extract
library: true
library_category: Session Foundation
description: Extract institutional knowledge from Fathom meeting transcripts and append to the RevOps Global knowledge base.---

# KB Extract — Fathom Knowledge Extraction

Keeps the RevOps Global knowledge base current by pulling insights from Fathom meeting transcripts.

## When to Run

- **Monthly** — routine cadence to catch anything that accumulated
- **After a client engagement completes** — capture patterns before they fade
- **After internal strategy or team meetings** — RevOps's own methodology evolves here
- **After onboarding a new client** — their stack and context belong in the KB
- **When prompted by Greg** — "run kb-extract" or "update the knowledge base"

## Process

### Step 1 — Check what's already processed

Read `docs/knowledge-base/EXTRACTION_LOG.md`. Note:
- All `recording_id` values in the Processed Meetings table
- The date range covered
- Any notes on what's pending

### Step 2 — List recent Fathom meetings

Use `mcp__fathom__list_meetings` to get recent recordings. Compare against the extraction log — identify meetings NOT yet in the Processed Meetings table.

Filter out:
- Meetings already in the log (by `recording_id`)
- Meetings with `transcript_language: unknown` (no transcript available — skip)
- Pure standup calls with no substantive discussion (use judgment from title + summary)

### Step 3 — Extract from each unprocessed meeting

For each candidate meeting:
1. Call `mcp__fathom__get_transcript` to get the full transcript
2. Call `mcp__fathom__get_summary` for context
3. Extract insights that are **specific to RevOps Global** — not generic industry knowledge

**What qualifies as an insight:**
- A pattern Greg applies repeatedly across clients
- A specific technical decision or architecture (with rationale)
- A client-specific gotcha or workaround that others might hit
- A RevOps methodology principle stated explicitly
- A scoping or pricing pattern
- An objection handled in a characteristic way

**What does NOT qualify:**
- Generic Salesforce / HubSpot documentation facts
- Things the client said that don't reflect RevOps's approach
- Off-topic conversation

### Step 4 — Route to the right topic file

Each insight goes into the most relevant file in `docs/knowledge-base/topics/`:

| File | Route insights about |
|------|---------------------|
| `campaign-attribution.md` | Multi-touch attribution, UTM, campaign influence, dashboards |
| `lifecycle-management.md` | Stage design, MQL rules, journey objects, PLG lifecycle |
| `revops-methodology.md` | Four foundations, service positioning, team structure, client management |
| `marketing-automation.md` | Workflow design, contact status, nurture programs |
| `hubspot-data-model.md` | HubSpot field architecture, lifecycle stages, permissions |
| `revops-marketing-strategy.md` | RevOps's own GTM, positioning, SEO, outbound |
| `salesforce-integrations.md` | LinkedIn, Google Ads, Marketo sync, PLG stacks |
| `lead-scoring.md` | MQL definition, scoring model design |
| `outbound-sales-strategy.md` | Cold outreach, sequences, prospecting |
| `seo-strategy.md` | SEO vendor evaluation, B2B SaaS SEO |
| `gtm-operations.md` | RevOps GTM motion, outbound engine |
| `revops-positioning.md` | How RevOps describes itself, differentiators |
| `client-engagement-methodology.md` | Kickoff, knowledge transfer, scope management |
| `chatbots-ai.md` | HubSpot chatbot, AI prospecting, phased rollout |
| `buying-committee-automation.md` | OCR auto-assignment, contact role taxonomy |
| `ai-prospecting.md` | AI-powered outbound, HubSpot AI sequences |
| `hubspot-asset-management.md` | Landing pages, forms, modules, CMS |
| `data-governance.md` | Field ownership, canonical fields, deduplication |
| `salesforce-territory-data.md` | Territory design, data cleanup |
| `salesforce-contract-management.md` | Contract workflows, approval processes |
| `marketo-architecture.md` | UTM handling, deduplication, campaign patterns |
| `hubspot-migrations.md` | HubSpot-to-HubSpot migration |
| `data-enrichment.md` | Lead enrichment strategy, providers |
| `sales-messaging.md` | Talk tracks, objection handling |
| `sales-alignment.md` | Marketing-sales handoff, SLA design |

If an insight doesn't fit any existing topic, propose a new topic file.

### Step 5 — Format each insight

Append to the end of the relevant topic file using this exact format (match existing entries):

```markdown
---

### [Descriptive title in sentence case]
**Pain points:** #tag1, #tag2
**Speaker:** [Name] | **Date:** [YYYY-MM-DD] | **Client context:** [Client name + brief stack/context]
**Prompted by:** [What question or situation triggered this insight]

> [Direct quote or close paraphrase of the key insight. 1-4 sentences. Include the "why" where stated. Quote Greg directly when the phrasing is precise and reusable.]

**Source:** [Meeting title] ([YYYY-MM-DD])
**Tags:** #tag1, #tag2, #tag3

---
```

### Step 6 — Update the extraction log

Add the meeting to the Processed Meetings table in `docs/knowledge-base/EXTRACTION_LOG.md`:
- `recording_id`, title, date, item count, topic files updated

Update the Processing Queue — mark done or move to Skipped with reason.

Update the Status block at the top with new total item count.

### Step 7 — Check for org context updates

After extraction, ask: did any meeting reveal something that should update `docs/context/revops-org-context.md`? Examples:
- New team member joined
- New client added to active roster
- A methodology pattern stated more precisely than current version
- A naming convention or default clarified

If yes, propose the update before committing.

### Step 8 — Commit

Stage and commit:
```
git add docs/knowledge-base/
git add docs/context/revops-org-context.md  # if updated
```

The pre-commit hook automatically syncs the updated KB topics into the Cowork plugin and stages the plugin changes. No separate sync step needed.

## Natural Trigger Events

| Event | What to extract |
|-------|----------------|
| New client kickoff completed | Onboarding patterns, stack notes, client context |
| Client engagement closed | Final methodology patterns, what worked, what didn't |
| Internal strategy meeting | RevOps positioning, methodology, GTM thinking |
| Quarterly team meeting | Any methodology evolution, new patterns |
| New tool or integration implemented | Technical patterns for that tool/integration |


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
