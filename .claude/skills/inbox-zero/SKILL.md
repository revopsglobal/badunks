---
name: inbox-zero
description: >
  Inbox Zero — draft replies to all of today's emails in Greg's voice. Use this skill when the
  user says "inbox zero", "process my inbox", "draft replies to my emails", "check my inbox and
  draft responses", "go through my email", or anything involving drafting email replies in bulk.
  Also trigger when asked to "clear out my inbox" or "get through my emails today". Skips
  newsletters, notifications, automated mail, and anything Greg sent himself. Creates Gmail drafts
  only — never sends. Always runs interactively so Greg can skip individual emails.
---

# Inbox Zero

Work through today's inbound emails for gregharned@gmail.com, draft a reply to each qualifying
thread in Greg's voice, and save them as Gmail drafts. Never send anything.

## Setup check

Before fetching emails, verify the superhuman CLI is available:

```bash
superhuman status
```

If this fails, tell Greg: "Superhuman needs to be running with CDP enabled. Launch it with:
`/Applications/Superhuman.app/Contents/MacOS/Superhuman --remote-debugging-port=9333`"

If tokens are expired, run:
```bash
superhuman account auth
```

## Step 1: Fetch today's inbound emails

Get today's date and build the search query. Today's emails means messages that arrived today,
not sent by Greg.

**Critical:** Always use the `superhuman` CLI (via `bun`) for fetching emails and creating drafts.
Do NOT use `gws` for this skill — `gws` is authenticated as `greg@revopsglobal.com` but the
inbox is `gregharned@gmail.com`. Using `gws` produces wrong thread IDs that cause 404 errors when
creating Superhuman drafts.

```bash
SUPERHUMAN="bun run /Users/gregharned/.local/share/superhuman-cli/src/cli.ts"

# Get today in YYYY/MM/DD format
TODAY=$(date +%Y/%m/%d)

# Fetch today's inbox — limit 50, JSON output
$SUPERHUMAN search "after:${TODAY} -from:gregharned@gmail.com" \
  --account gregharned@gmail.com \
  --limit 50 \
  --json
```

Parse the JSON to get thread IDs, subjects, and senders. The thread IDs from this output are the
correct IDs to use with `superhuman reply` later.

## Step 2: Filter out noise

Skip a thread if any of these are true:

**Auto-detected skips (no need to ask Greg):**
- Sender address contains: `noreply`, `no-reply`, `notifications@`, `mailer@`, `newsletter@`,
  `automated@`, `updates@`, `donotreply`, `do-not-reply`, `bounce@`, `alert@`, `digest@`
- Subject starts with: `[BULK]`, `FWD:` from an automated sender, or contains "unsubscribe"
- Greg is in BCC (can't reply meaningfully)
- Thread already has a draft in it (check `superhuman draft list`)
- Sender is gregharned@gmail.com (Greg sent it, including emails he sent to himself)

When you skip a thread silently, note it in your internal tally but don't interrupt Greg about it.
Show the full skip list at the end.

## Step 3: Read each qualifying thread

For each thread that passes filtering:

```bash
SUPERHUMAN="bun run /Users/gregharned/.local/share/superhuman-cli/src/cli.ts"
$SUPERHUMAN read <thread-id> --account gregharned@gmail.com --context 3
```

This loads the last 3 messages in the thread so you have context for the reply.

## Step 4: Present and draft — interactively

For each qualifying thread, present Greg with:

```
─────────────────────────────────────────────────────
📨  Thread N of M
From:     [sender name <email>]
Subject:  [subject]
Date:     [date/time]

Summary: [2–3 sentence summary of what they're asking or saying]

Proposed reply:
─────────────────────────────────────────────────────
[draft text]
─────────────────────────────────────────────────────
Draft this reply? [Enter to confirm / "skip" to skip / "edit: <your text>" to override]
```

Wait for Greg's response before moving to the next thread. He can:
- Press Enter (or say "yes", "ok", "go", "draft it") → create the draft
- Say "skip" or "next" → move on without drafting
- Say "edit: [new text]" → use his text instead of yours

## Step 5: Create the draft

When confirmed, create the draft reply using the superhuman CLI:

```bash
SUPERHUMAN="bun run /Users/gregharned/.local/share/superhuman-cli/src/cli.ts"
$SUPERHUMAN reply <thread-id> \
  --account gregharned@gmail.com \
  --body "[draft text]"
```

**Do not add `--send`.** Draft only.

This creates a Superhuman-native draft visible directly in the Superhuman UI — Greg can review
and hit Send without copying anything.

**Do NOT fall back to `gws gmail users drafts create` or `superhuman draft create`** — these
create Gmail API drafts that are NOT visible in Superhuman UI.

## Step 6: Final tally

After all threads are processed, show a clean summary:

```
─────────────────────────────────────────────────
Inbox Zero — Done
─────────────────────────────────────────────────
Drafted:  N replies
Skipped:  N (by you)
Filtered: N (newsletters, notifications, no-replies)

Drafts created:
  • [Subject] → [to: sender] ✓
  • [Subject] → [to: sender] ✓

Filtered/skipped:
  • [Subject] — from: [sender] (newsletter/notification)
  • [Subject] — skipped by you
─────────────────────────────────────────────────
```

---

## Greg's Voice — Drafting Guidelines

Every draft must sound like Greg wrote it. He writes short, direct emails. No filler, no
pleasantries he doesn't mean. Get to the point immediately.

**Tone:** Confident, direct, collaborative. Not cold — just efficient. He's a RevOps operator
who respects people's time, including his own.

**What he does:**
- Leads with the actual answer or next step, not a setup sentence
- Uses short paragraphs, often 1–2 sentences each
- Acknowledges context without restating it ("Got it." / "Makes sense." / "Noted.")
- Signs off simply: just "Greg" or nothing at all for short replies
- Uses first names in openers when he knows the person, skips "Hi" for very short replies

**What he never does:**
- "I hope this email finds you well" — never
- "Please don't hesitate to reach out" — never
- "Circling back" as an opener — never
- Exclamation points to soften tone (one is ok if genuinely enthusiastic, never for politeness)
- Emojis (none, ever)
- "Just wanted to follow up" — starts with the actual follow-up instead
- Over-explaining or hedging — he states a position and moves on

**For RevOps/client emails:** Lead with impact. "Here's the timeline." not "I wanted to share
some thoughts on the timeline."

**Length guide:**
- Quick acknowledgment / scheduling: 1–3 sentences
- Answering a question: 2–4 sentences
- Complex ask or proposal: 3–6 sentences, short paragraphs
- Rarely longer than this

**Example contrast:**

Bad (not Greg):
> Hi Sarah, hope you're having a great week! Thanks so much for reaching out about the project
> timeline. I wanted to take a moment to share some thoughts. I think we should probably aim for
> the end of Q2, but please let me know if that works for your team's schedule.

Good (Greg):
> Q2 end works. Lock in May 30th and I'll send the kickoff agenda by Friday.

---

## Edge Cases

**If a thread has multiple senders** (e.g., a group reply-all): address the most recent message
only. Reply to the thread, not individual senders.

**If an email is in a foreign language:** draft the reply in the same language. Note this to Greg:
"(Drafted in [language] to match their message)"

**If an email is unclear or needs real judgment** (legal, financial, emotionally charged): flag it
instead of drafting. Say: "Flagged: [subject] — this one might need your direct attention before
drafting."

**If the inbox is empty or has no qualifying threads:** "Your inbox is clear for today. Nothing
to draft."

**If there are more than 15 qualifying threads:** warn Greg upfront. "Found [N] threads that need
replies — that's a lot. Want me to start with unread ones first, or go oldest-to-newest?"

---

## Allowed Tools

Uses `superhuman` CLI (Bash with `superhuman:*` prefix allowed by the superhuman skill).

Do not use `mcp__gmail__*` tools. The superhuman CLI is the approved method per memory.

---

## Skill Notes

### What Works Well
- `bun run src/cli.ts reply <thread-id> --account gregharned@gmail.com --body "..."` (no `--send`)
  creates a Superhuman-native draft — visible in Superhuman UI, syncs to all devices. This is the
  correct method and confirmed working.
- The superhuman binary at `~/.local/share/superhuman-cli/superhuman` is broken (missing Nix
  dependency). Always use `bun run src/cli.ts` instead.

### Calibrations
- **Account disambiguation:** `gws` CLI is authed as `greg@revopsglobal.com`. The Superhuman inbox
  is `gregharned@gmail.com`. These are different accounts with different thread IDs. Always use the
  superhuman CLI's search output for thread IDs — never use gws thread IDs for superhuman reply.
- `superhuman search "after:YYYY/MM/DD -from:gregharned@gmail.com" --account gregharned@gmail.com --limit 50 --json`
  uses CDP fallback (launches Superhuman) and returns correct thread IDs for the right account.

### Lessons Learned
- 2026-03-18: `gws` and `superhuman` use different account auth — mixing them causes 404 errors.
  gws → greg@revopsglobal.com, superhuman CLI → gregharned@gmail.com. Never use gws for drafts.
- Gmail API drafts (`gws drafts create`) are NOT visible in Superhuman. Only `superhuman reply
  --body "..."` (no --send) creates drafts that appear in Superhuman.
