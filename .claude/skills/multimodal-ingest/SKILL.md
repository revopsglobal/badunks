---
name: multimodal-ingest
library: true
description: >
  Ingest any file or URL into the Open Brain pipeline. Supports PDFs, images
  (jpg/png/webp), videos (mp4/mov), and web URLs. Uses Gemini to extract
  RevOps-relevant insights and captures them to Open Brain, where the Saturday
  promotion pipeline handles KB curation. Trigger with: "ingest this file",
  "add this PDF to the knowledge base", "capture this article".
---

# Multimodal Ingest — File & URL → Open Brain

Extracts RevOps insights from rich documents using Gemini, then feeds them into the standard Open Brain → KB pipeline. No separate vector store, no new infrastructure — everything flows through the existing system.

## Pipeline Position

```
PDFs / Images / Video / URLs
          │
  multimodal-ingest.js
  (Gemini extraction)
          │
      Open Brain
          │
  kb-promote.js (Saturdays)
          │
      KB markdown
```

## Supported Inputs

| Type | Extensions | Method |
|------|-----------|--------|
| Images | .jpg .jpeg .png .gif .webp | Gemini inline base64 |
| PDFs | .pdf | Gemini inline base64 (up to ~18MB) |
| Videos | .mp4 .mov .webm | Gemini File API (any size) |
| Web pages | https:// URLs | Fetch + strip HTML → Gemini |

## How to Run

```bash
node ~/work/team-brain/scripts/multimodal-ingest.js <file-or-url>
node ~/work/team-brain/scripts/multimodal-ingest.js ~/Downloads/deck.pdf
node ~/work/team-brain/scripts/multimodal-ingest.js ~/Downloads/audit-report.pdf --title "Vitalant Q1 Audit"
node ~/work/team-brain/scripts/multimodal-ingest.js https://revopsglobal.ai/blog/buying-groups
```

## When to Use

- A client sends a deck, report, or one-pager worth capturing
- After exporting a strategy doc or proposal as PDF
- A relevant blog post or article worth adding to the knowledge base
- A recorded video walkthrough of a client's stack

## What Gemini Extracts

- RevOps methodology, process, and framework insights
- HubSpot / Salesforce / Marketo architecture decisions
- Lead scoring, lifecycle, attribution concepts
- Charts and tables — described in text with numbers, labels, and trends
- Frameworks and visual models — translated to prose
- GTM strategy, sales alignment, client engagement patterns

Insights with no RevOps relevance are not captured. The script logs everything to `logs/multimodal-ingest.log` and sends a Slack summary to Greg's DM when done.

## Output

- Insights captured to Open Brain immediately
- KB-worthy insights queued in `~/.claude/team-brain-sessions/pending-kb-candidates.json`
- Saturday `kb-promote.js` handles promotion to KB markdown automatically
- State tracked in `~/.claude/team-brain-sessions/multimodal-ingest-state.json` — each input is processed once (deduped by file path / URL)

## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
