---
name: open-brain-weekly-review
library: true
library_category: Session Foundation
description: Weekly synthesis of captured Open Brain thoughts.---

# Open Brain Weekly Review

Run a structured end-of-week synthesis across all captured thoughts.

## Steps

### 1. Pull this week's thoughts

Call `list_thoughts` with `days: 7` and `limit: 50`. If volume is low, extend to `days: 14`.

### 2. Pull open action items

Call `search_thoughts` with query: `"action items tasks to do follow up"` and `limit: 20`.

### 3. Synthesize — produce this structure

**Week of [date range]**

**Themes this week** (2-4 recurring topics or patterns across captures):
- [Pattern]: [evidence from thoughts]

**Open action items** (extracted from metadata + semantic search):
- [ ] [action] — owner: [who] — why: [context/trigger] — from: [meeting/decision, date]

**People threads** (notable entries involving specific people):
- [Name]: [what was captured, any follow-up needed]

**Insights worth revisiting** (high-value ideas/observations):
- [Insight] — [date captured]

**Forgotten threads** (items that haven't had follow-up):
- [thread] — last captured [date]

### 4. Call `thought_stats` to close

Show totals and top topics so Greg has a sense of system health.

### 5. KB promotion check (always run)

After the synthesis, count how many `reference` or `decision` type thoughts were in this week's
pull. If there are 3 or more, prompt:

> "Found [N] references and decisions this week worth promoting to the permanent KB.
> Run `/open-brain-to-kb` now to review and promote them?"

This keeps Open Brain and the knowledge base in sync on a weekly cadence without requiring
a separate trigger.

## Output format

Render as clean markdown. No filler. Lead with the themes — that's the highest-value part.
If there are no open action items or no people threads, omit those sections rather than showing empty ones.

## Cadence

Friday afternoon is the recommended time. Can also run ad hoc mid-week if a lot has been captured.
Always follow with `/open-brain-to-kb` when reference/decision count is high.

## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
