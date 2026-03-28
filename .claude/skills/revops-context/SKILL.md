---
name: revops-context
library: true
description: Load RevOps Global's organizational context, methodology, and institutional knowledge.---

# RevOps Global — Org Context

This skill surfaces RevOps Global's organizational context, naming conventions, brand rules, and methodology. In Cowork, the org context also auto-loads via the plugin's CLAUDE.md — this skill goes deeper, covering the knowledge base and session protocol.

## Company

RevOps Global — 10-person Revenue Operations consultancy helping B2B SaaS companies build the operational infrastructure behind their GTM motion.

## Team

| Person | Role |
|--------|------|
| Greg Harned | CEO / Founder |
| Kristina | HubSpot Strategist |
| Rachit | HubSpot Architect |
| Anumeet | Salesforce Architect |

## Products & Naming

| Internal shorthand | Client-facing name | Repo |
|-------------------|-------------------|------|
| RGOS | RevOps Global OS | `rgos/` |
| revops-init | RevOps Global AI | `revops-init/` |

**Rule:** Use "RevOps Global OS" and "RevOps Global AI" in all outward-facing materials. RGOS / revops-init are internal only.

## Brand Rules (Absolute)

- **No emojis anywhere** — HTML, TSX, slides, docs, comments, emails. Use SVG icons instead.
- **Colors:** Deep Navy `#072C87` (primary), Cyan `#2DD6FF`, Mint Teal `#16F0DF`
- **Typography:** Urbanist (headings), Inter (body)
- **Logo:** `logo_allwhite.png` on dark, `logo_color.png` on light
- **Logo ratios:** `logo_color.png` → 1.9481:1, `logo_white.png` → 7.0289:1 (different — never swap)
- Apply official RevOps Global brand to all visual outputs — never use custom palettes for RevOps's own materials.

## The Four Foundations

Every client engagement starts by diagnosing these four pillars:

1. **Clean database** — deduplication, canonical fields, data hygiene as a process issue
2. **Lifecycle model** — stage design, journey objects, pre/post-MQL rules, company stages
3. **Source/campaign attribution** — multi-touch, UTM strategy, two-dashboard reporting
4. **Bidirectional CRM sync** — HubSpot ↔ Salesforce sync, Salesforce as source of truth

## Key Methodology Patterns

- Opportunity Influence (multi-touch) over single-touch attribution for budget decisions
- Two-dashboard attribution: overall lead dashboard (where+what) + campaign drill-down
- Lifecycle dashboard = Volume + Conversion + Velocity
- "Attribution is directional, not precise" — Greg's reframe for exec challenges
- Knowledge transfer: diagnose and suggest; let client admin implement
- Retainer overage: roll over once, then have the direct conversation

## Attribution Maturity Tiers (use in discovery calls)

When a client says they can't show marketing's impact on pipeline, diagnose which tier they're at:

| Tier | What they have | What's missing |
|------|---------------|----------------|
| 1 — Basic | Lead Source on some records | UTM capture, CRM mapping |
| 2 — Campaign Member | SF Campaigns + Campaign Members | Opportunity Contact Roles, Responded status |
| 3 — Opportunity Influence | Contact Roles + Campaign Influence enabled | Multi-touch model, cost tracking |
| 4 — Buying Committee | Multi-contact association + influence | Attribution weighted by persona |
| 5 — Weighted Attribution | Full multi-touch + weighted model | Continuous calibration |

Most new clients are at Tier 1 or early Tier 2. The engagement scopes up from where they are. The buying committee gap diagnostic question: "On average, how many contacts are associated to your closed-won opportunities?" If the answer is 1 or they don't know, OCR hygiene is the blocker before attribution can work.

## Internal Defaults

- HubSpot owner ID (Greg): `26662531`
- Always validate before claiming done — call the function, check browser logs, use Playwright

## Knowledge Base

2700 items extracted from client meeting transcripts (May 2023 – Mar 2026) across 25 topic files.

**To query the KB:** Use the `revops-knowledge-base` skill, which has all 25 topic files bundled as references. Key topics:

| Topic | Items | When to use |
|-------|-------|-------------|
| Campaign Attribution | 87 | Any attribution, UTM, or campaign influence question |
| Lifecycle Management | 57 | Stage design, MQL rules, journey objects |
| RevOps Methodology | 47 | Positioning, frameworks, client management |
| Marketing Automation | 41 | Workflow design, contact status, nurture |
| HubSpot Data Model | 40 | HubSpot field architecture, lifecycle stages |
| Salesforce Integrations | 29 | LinkedIn, Google Ads, Marketo sync |
| Lead Scoring | 23 | MQL definition, scoring model design |
| Marketo Architecture | 8 | UTM handling, deduplication, campaign patterns |

## Session Protocol

When this skill is invoked:
1. Confirm you have the org context loaded (naming, brand, four foundations)
2. Identify which KB topics are relevant to the current task
3. Load those topics via the `revops-knowledge-base` skill before proceeding
4. Apply RevOps Global's specific methodology — not generic industry advice


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
