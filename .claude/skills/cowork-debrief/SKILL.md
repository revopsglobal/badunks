---
name: cowork-debrief
library: true
description: Extract and capture Open Brain insights from a Cowork session.---

# Cowork Session Debrief

Extract capture-worthy knowledge from this conversation and save it to Open Brain.

## Step 1 — Scan the conversation

Review the full conversation for content that meets ALL of these:
1. Would apply beyond this specific session
2. Has retrieval value in a future conversation
3. Is specific enough to act on
4. Is not already obvious or generic

**What qualifies:**
- Client-specific patterns (how they work, what they prefer, problems they have)
- Technical or architectural decisions made with reasoning
- RevOps methodology insights (frameworks, patterns, what worked)
- Key business facts (new client details, engagement outcomes, strategic direction)
- Anything Greg said to "remember", "capture", "note", or "add"

**What does not qualify:**
- How Claude should behave (belongs in MEMORY.md, not Open Brain)
- Session task state (transient)
- Generic best practices with no RevOps-specific angle

## Step 2 — Draft capture entries

For each qualifying insight, draft a self-contained statement using one of these patterns:

- **Decision:** `Decision: [what]. Context: [why]. Owner: [who].`
- **Person note:** `[Name] — [what you learned about them].`
- **Insight:** `Insight: [realization]. Triggered by: [cause].`
- **Meeting debrief:** `Meeting with [who] about [topic]. Key points: [...]. Action items: [action — owner — why/triggered by: context].`
- **AI save:** `Saving from [tool]: [takeaway].`

Each entry must be self-contained — no pronouns or references that require session context to understand.

## Step 3 — Capture or output

**If `capture_thought` MCP is available:**

Show Greg the drafted entries first:

```
Found [N] entries worth capturing:

1. [entry text] — [type: Decision/Insight/Person/etc.]
2. ...

Capturing now...
```

Then call `capture_thought` for each one silently. Report the final count: "Captured [N] thoughts."

**If `capture_thought` MCP is not available:**

Output all entries in a format ready to paste into Claude Code:

```
## Cowork Session — [today's date]
Bring these to Claude Code and run: "capture these to Open Brain"

---
[Entry 1 text]

---
[Entry 2 text]

---
[Entry N text]
```

Tell Greg: "Open Brain MCP not available here. Copy the block above and paste it into a Claude Code session — it will capture everything automatically."

## Notes

- If nothing qualifies, say so directly: "Nothing in this session meets the capture threshold." Don't force entries.
- Quality over quantity. Three strong entries beat ten weak ones.
- Do not capture the same insight twice if it was already captured earlier in the session.

## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
