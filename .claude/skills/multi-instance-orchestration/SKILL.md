---
name: multi-instance-orchestration
library: true
description: Orchestrate multiple Claude Code instances in a leader/worker pattern.---

# Multi-Instance Orchestration

This skill covers how to run multiple Claude Code instances coordinated by a leader/conductor instance using file-based task queues.

## When to Use This

- You need to parallelize work across multiple Claude Code sessions
- A project has independent workstreams that can run simultaneously
- You want a conductor that plans, delegates, and reviews while workers execute
- You're running multiple Agent Teams and need meta-coordination above them

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    LEADER INSTANCE                       │
│  - Plans and breaks down the goal                       │
│  - Creates task files in queue/                         │
│  - Monitors check-ins/ for worker status                │
│  - Reviews results/ for completed work                  │
│  - Processes spawn-requests/ — approves or denies       │
│  - Manages roster.json — retained vs ephemeral workers  │
│  - Never implements — only coordinates                  │
└──────────┬──────────────────┬──────────────┬────────────┘
           │                  │              │
     ┌─────▼─────┐    ┌──────▼─────┐  ┌─────▼──────┐
     │ WORKER A   │    │ WORKER B   │  │ WORKER C   │
     │ Claims     │    │ Claims     │  │ Claims     │
     │ tasks,     │    │ tasks,     │  │ tasks,     │
     │ executes,  │    │ executes,  │  │ executes,  │
     │ reports    │    │ reports    │  │ reports    │
     │ CAN SPAWN  │    │            │  │            │
     └──────┬─────┘    └────────────┘  └────────────┘
            │
     ┌──────▼──────────────────────────┐
     │  SUB-WORKERS (spawned by A)     │
     │  Ephemeral: terminate on done   │
     │  Retained: added to roster if   │
     │  mission-aligned                │
     └─────────────────────────────────┘
```

## The Coordination Layer

All coordination happens through `.claude/orchestration/`:

| Directory/File | Purpose | Written By | Read By |
|----------------|---------|------------|---------|
| `queue/` | Unclaimed tasks | Leader | Workers |
| `claimed/` | Tasks in progress | Workers | Leader |
| `results/` | Completed deliverables | Workers | Leader |
| `check-ins/` | Worker heartbeats | Workers | Leader |
| `spawn-requests/` | Sub-worker hire requests | Workers | Leader |
| `approvals/` | Leader decisions on spawn requests | Leader | Workers |
| `roster.json` | Registry of active + retained workers | Leader | All |
| `leader-plan.md` | Strategic plan | Leader | Everyone |

## Dynamic Spawn Authority

Workers can hire sub-workers without waiting for the leader — but with two constraints:

1. **Write a spawn request.** Workers file a request in `spawn-requests/` describing what specialty they need, why, and whether to retain or terminate on completion.
2. **Wait for approval before the sub-worker executes external actions.** Sub-workers may start internal work immediately, but cannot communicate externally or touch shared files until the leader approves via `approvals/`.

**What workers can spawn autonomously (no approval needed):**
- Read-only research agents
- Analysis agents working on isolated file sets
- Draft-only agents (no publish/send authority)

**What requires leader approval:**
- Agents that write to shared files
- Agents that communicate externally (email, Slack, HubSpot, Salesforce)
- Agents flagged as permanent/retained hires

## Mission Alignment — Retention Criteria

A spawned worker should be **retained** (added to `roster.json`) if ALL of the following are true:

1. **The task completed successfully** — failed workers are not retained
2. **The specialty is recurring** — will this capability be needed again in future RevOps work?
3. **The specialty is not already covered** — check `roster.json` for redundancy before retaining
4. **The specialty maps to one of the RevOps core domains:**

| Domain | Qualifies for Retention | Examples |
|--------|------------------------|---------|
| Client delivery | Yes | CRM audits, MAP implementation, lifecycle modeling |
| Platform development | Yes | RGOS features, RevOps Engine plays, edge functions |
| GTM operations | Yes | Outbound research, content, ICP qualification |
| Business intelligence | Yes | Pipeline analysis, attribution, reporting |
| Technical architecture | Yes | Salesforce, HubSpot, Marketo, data models |
| One-off client task | No | Single engagement research, ad-hoc data pull |
| Single bug fix | No | Narrow code change, not a recurring specialty |
| Temporary unblock | No | Filling a gap while a retained agent is busy |

**When in doubt, terminate.** Retaining unnecessary workers adds roster bloat. A specialty needs to appear in 3+ future use cases before it's worth a permanent slot.

## Worker Lifecycle

```
SPAWNED → EXECUTING → SELF-EVALUATE → RETAIN or TERMINATE
                             │
                    Does the specialty qualify?
                    ├── Yes → update roster.json as "available"
                    └── No  → write final result, mark as terminated
```

Workers execute their own lifecycle:

```markdown
# In result file, workers include a lifecycle recommendation:

## Lifecycle Recommendation
- **Retain**: Yes / No
- **Reason**: [maps to recurring RevOps domain / one-off task]
- **Specialty label**: [e.g. "HubSpot workflow auditor"]
- **Last task**: [brief description]
```

The leader processes this recommendation and updates `roster.json`.

## Worker Roster

`roster.json` is the single source of truth for active workers:

```json
{
  "retained": [
    {
      "id": "revops-analyst",
      "specialty": "CRM data analysis, pipeline health, audit reporting",
      "status": "available",
      "mission_alignment": "Client delivery — core RevOps audit workflow",
      "sessions": 4,
      "last_active": "2026-03-09",
      "hired_by": "orchestrator"
    }
  ],
  "ephemeral": [
    {
      "id": "worker-alpha",
      "specialty": "ad-hoc research",
      "status": "active",
      "terminate_on": "task-007-complete",
      "hired_by": "worker-revops-analyst"
    }
  ]
}
```

**Status values:** `available` | `active` | `blocked` | `terminated`

## How to Launch

### Option A: Using the launcher script

```bash
# Terminal 1 — Start the leader
./scripts/orchestrate.sh leader "Build REST API with full test coverage"

# Terminal 2-4 — Start workers
./scripts/orchestrate.sh worker worker-alpha
./scripts/orchestrate.sh worker worker-beta
./scripts/orchestrate.sh worker worker-gamma

# Check status from any terminal
./scripts/orchestrate.sh status

# Reset when done
./scripts/orchestrate.sh reset
```

### Option B: Manual launch with Claude Code

```bash
# Terminal 1 — Leader
claude --resume orchestration-leader

# Tell it: "You are the orchestration leader. Goal: Build REST API.
# Read .claude/agents/orchestration-leader.md for your protocol."

# Terminal 2 — Worker
claude --resume worker-alpha

# Tell it: "You are orchestration worker worker-alpha.
# Read .claude/agents/orchestration-worker.md for your protocol."
```

### Option C: With Claude Agent SDK (programmatic)

```python
from claude_code_sdk import ClaudeCode

# Start leader
leader = ClaudeCode.create(
    prompt="You are the orchestration leader. Goal: Build REST API...",
    allowed_tools=["Read", "Write", "Edit", "Glob", "Grep", "Bash"],
)

# Start workers
workers = []
for name in ["worker-alpha", "worker-beta", "worker-gamma"]:
    w = ClaudeCode.create(
        prompt=f"You are orchestration worker {name}. Read .claude/agents/orchestration-worker.md...",
        allowed_tools=["Read", "Write", "Edit", "Glob", "Grep", "Bash"],
    )
    workers.append(w)
```

## Task Lifecycle

```
CREATED → QUEUED → CLAIMED → IN PROGRESS → COMPLETED → REVIEWED
  leader    queue/   worker     worker       results/    leader
  writes             moves to   executes     worker      reviews
                     claimed/                writes
```

## Best Practices

### Task Design
- **Size tasks for 5-15 minutes of focused work.** Too small = coordination overhead exceeds value. Too large = workers go dark without check-ins.
- **Each task owns distinct files.** Never assign two workers to the same file concurrently.
- **Use `blocked_by` for dependencies.** Workers skip blocked tasks and pick unblocked ones.
- **Include file paths and constraints.** Workers don't have the leader's context.

### Conflict Prevention
- Workers **move** task files from queue/ to claimed/ (atomic claim).
- If the file is gone when a worker tries to claim it, another worker got there first.
- Leader structures tasks so file ownership doesn't overlap.

### Check-in Frequency
- Workers update check-ins at: task claim, milestones, blockers, and completion.
- Leader reads check-ins every coordination cycle.
- If a worker goes silent (no check-in update), the leader should investigate.

### Scaling
- **2-3 workers**: File-based coordination works perfectly. Low overhead.
- **4-5 workers**: Still works, but leader needs to be more careful about task dependencies.
- **6+ workers**: Consider adding an MCP server as a proper message broker, or split into sub-teams with sub-leaders.

### When NOT to Orchestrate
- Sequential work where each step depends on the last
- Work that all touches the same files
- Simple tasks that one instance can handle in minutes
- Anthropic estimates multi-agent adds value for ~5% of development tasks

## Combining with Agent Teams

Each worker instance can itself be a full Agent Team (with its own internal subagents). This gives you two levels of orchestration:

```
Leader Instance
├── Worker A (Agent Team with 3 subagents)
├── Worker B (Agent Team with 2 subagents)
└── Worker C (Solo instance)
```

To enable Agent Teams within workers, set in `.claude/settings.json`:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Two workers claimed the same task | One will find the file missing from queue/. They should check claimed/ and pick a different task. |
| Worker is blocked | Worker writes blocker in check-in. Leader reads it and either answers the question, adjusts the task, or creates a prerequisite task. |
| Queue is empty but work isn't done | Leader needs to create more tasks. Workers sit idle until queue is populated. |
| Worker modified wrong files | Review task description — was file ownership clear? Add explicit constraints to future tasks. |
| Leader implemented instead of delegating | Remind the leader of its role. It should ONLY coordinate, never code. |


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
