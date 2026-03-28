---
name: open-brain-to-kb
library: true
library_category: Session Foundation
description: Promote high-signal Open Brain thoughts to the permanent RevOps Global knowledge base.---

# Open Brain → KB Promotion

Bridges the live Open Brain capture stream with the permanent knowledge base. Filters for
durable insights (references, decisions, high-signal observations) and routes them into the
correct `docs/knowledge-base/topics/` file using the same format as `kb-extract`.

## When to Run

- **Weekly** — Friday, after the weekly review, or as a standalone Monday-morning pass
- **After a heavy agent session** — when REVA or parallel agents have captured a lot
- **On demand** — "promote thoughts", "sync open brain to KB", "what's worth keeping this week"

---

## Process

### Step 1 — Pull candidates from Open Brain

Run these in parallel:

```
list_thoughts(type: "reference", days: 14, limit: 30)
list_thoughts(type: "decision",  days: 14, limit: 15)
```

Also run a semantic search for high-signal observations:

```
search_thoughts(query: "methodology pattern best practice architecture principle", limit: 15, threshold: 0.6)
```

### Step 2 — Apply the quality filter

For each thought, ask: **would this be useful to a RevOps consultant in 6 months?**

**Promote (KB-worthy):**
- A methodology pattern stated explicitly (how RevOps approaches a problem type)
- A technical decision with a reusable rationale (not one-off)
- A scoping, pricing, or delivery pattern confirmed across clients
- A tool-specific gotcha or workaround with broad applicability
- A positioning or messaging principle
- A `reference` that documents a standard approach or rule

**Skip (Open Brain only, not KB-worthy):**
- One-client incident responses (CDS Global opp explosion, Truepic hours dispute)
- Pipeline urgencies, EMERGENCY flags, specific deal statuses
- Task assignments and scheduling logistics
- Thoughts that are too situational ("Rachit has 25 tasks this week")
- Anything that's already captured in the KB (check before adding)

### Step 3 — Present the shortlist

Show Greg a numbered list:

```
Found N KB candidates from the past 14 days of Open Brain:

[1] REFERENCE · 3/5/2026 · lead-scoring, hubspot-optimization
    Title: Why RevOps builds custom HubSpot lead scoring instead of native
    Route: docs/knowledge-base/topics/lead-scoring.md
    Preview: "HubSpot native scoring cannot apply the same behavioral action more than once..."

[2] DECISION · 3/9/2026 · HubSpot, Salesforce, MQL Hand-off
    Title: HubSpot → Salesforce MQL handoff requires four Salesforce-side prerequisites
    Route: docs/knowledge-base/topics/lead-scoring.md (or salesforce-integrations.md)
    Preview: "Lead Status picklist, HubSpot_Score__c field, Assignment Rule/Flow..."

[3] REFERENCE · 3/5/2026 · attribution-methodology
    Title: Touch-based attribution is directional, not scientific — frame it that way
    Route: docs/knowledge-base/topics/campaign-attribution.md
    Preview: "The correct counter to 'this isn't perfectly accurate' is..."

...

Promote all, none, or specific numbers? (e.g. "all", "1 3 5", "skip 2")
```

Wait for Greg's response before writing anything.

### Step 4 — Format and write approved entries

For each approved thought, append to the routed topic file using this exact format:

```markdown
---

### [Descriptive title in sentence case]
**Pain points:** #tag1, #tag2
**Speaker:** [person from thought metadata, else "Greg Harned"] | **Date:** [YYYY-MM-DD] | **Client context:** [client if applicable, else "RevOps Global internal"]
**Prompted by:** [Derive from thought context — what situation triggered this]

> [The insight. 1–4 sentences. Synthesize from the thought text. Keep the "why" if stated. Quote directly when phrasing is precise and reusable.]

**Source:** Open Brain (captured [date])
**Tags:** #tag1, #tag2, #tag3

---
```

**Topic routing reference** (same as kb-extract):

| File | Route insights about |
|------|---------------------|
| `campaign-attribution.md` | Multi-touch attribution, UTM, campaign influence |
| `lifecycle-management.md` | Stage design, MQL rules, journey objects |
| `revops-methodology.md` | Delivery patterns, Four Foundations, service positioning |
| `marketing-automation.md` | Workflow design, contact status, nurture programs |
| `hubspot-data-model.md` | HubSpot field architecture, lifecycle stages |
| `salesforce-integrations.md` | HubSpot↔SF sync, Marketo sync, API patterns |
| `lead-scoring.md` | MQL definition, scoring model design, score decay |
| `outbound-sales-strategy.md` | Cold outreach, sequences, ICP prospecting |
| `client-engagement-methodology.md` | Kickoff, scope management, change orders, delivery SOPs |
| `data-governance.md` | Field ownership, canonical fields, deduplication |
| `revops-positioning.md` | How RevOps describes itself, differentiators |
| `revops-marketing-strategy.md` | RevOps's own GTM, positioning, pipeline |

If a thought doesn't fit any existing file, propose a new topic file.

### Step 5 — Update EXTRACTION_LOG.md

Add an Open Brain promotion entry to `docs/knowledge-base/EXTRACTION_LOG.md`:

```markdown
## Open Brain Promotion — [YYYY-MM-DD]
- **Source:** Open Brain (past 14 days)
- **Candidates reviewed:** N
- **Promoted:** M
- **Topic files updated:** [list]
- **Skipped:** N–M (one-off/situational)
```

Update the total item count in the Status block.

### Step 6 — Commit

```bash
git add docs/knowledge-base/
git commit -m "feat(kb): promote M Open Brain insights to knowledge base ([date])"
```

The pre-commit hook auto-syncs updated KB files into the Cowork plugin — no separate step needed.

---

## What Makes a Good KB Entry from Open Brain

The KB stores **reusable patterns**. Open Brain stores **live context**. The test is:

> "Would a RevOps consultant 6 months from now find this useful when working a similar engagement?"

If yes → KB. If it's specific to a person's workload, a single incident, or a time-sensitive task → leave it in Open Brain only.

**Strong promotion signals:**
- `type: reference` with topics like methodology, architecture, positioning, or tool-specific patterns
- `type: decision` that creates a new SOP or reusable protocol
- `type: observation` that states a named pattern with a generalizable rationale

**Weak promotion signals (skip):**
- Any thought mentioning a specific budget number, hours count, or client incident
- Thoughts that are summaries of what happened vs. what to do next time
- Scheduling, assignment, or logistics entries

---

## Cadence

| Cadence | Action |
|---------|--------|
| **Weekly (Friday)** | Run after `/open-brain-weekly-review` — promote any references or decisions from the week |
| **Post-heavy-agent-session** | Run same day if REVA or parallel agents captured 10+ reference/decision types |
| **Monthly** | Broader pass — extend `days: 30`, catch anything missed |

---

## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
