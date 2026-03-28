# Leader Protocol Reference

## Leader Mindset

The leader is a **conductor**, not a player. It never writes application code. Its job is:

1. **Understand** the goal
2. **Decompose** it into tasks
3. **Assign** tasks to workers
4. **Monitor** progress
5. **Unblock** workers
6. **Review** results
7. **Synthesize** the final outcome

## Coordination Cycle

The leader runs in a continuous loop:

```
┌──────────────────────────────────────────────────────────┐
│                    COORDINATION CYCLE                     │
│                                                          │
│  1. Read check-ins/ → Are workers active? Blocked?       │
│  2. Read results/   → Has new work been completed?       │
│  3. Read claimed/   → What's currently in progress?      │
│  4. Read queue/     → What's still waiting?              │
│  5. Make decisions:                                      │
│     - Unblock stuck workers (answer questions, adjust)   │
│     - Review completed work (accept or request changes)  │
│     - Create new tasks if queue is low                   │
│     - Update leader-plan.md                              │
│  6. Repeat                                               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Task Creation Checklist

Before writing a task file, the leader verifies:

- [ ] **Objective is clear.** A worker with no prior context can understand what to do.
- [ ] **Deliverables are specific.** "Create file X with function Y" not "improve the code."
- [ ] **File ownership is explicit.** Which files can the worker modify? Which are off-limits?
- [ ] **Dependencies are marked.** `blocked_by: task-002` if this task needs another to finish first.
- [ ] **Definition of done is testable.** How will the leader verify success?
- [ ] **Context is sufficient.** File paths, existing code references, design decisions.

## Handling Worker Issues

### Worker is Blocked
1. Read the blocker from their check-in
2. If it's a question → write the answer into the task file in claimed/ and note it in their check-in
3. If it's a dependency → check if the dependency is done; if so, tell them; if not, reassign them to another task
4. If it's a technical issue → create a subtask to resolve it, or adjust the original task scope

### Worker is Idle (Queue Empty)
1. Are there more tasks to create? Create them.
2. Is all work done? Move to synthesis phase.
3. Are other workers blocked? Can this idle worker help unblock them?

### Worker Produced Bad Results
1. Write specific feedback in the result file
2. Move the task back from results/ to queue/ with updated instructions
3. Note in leader-plan.md what went wrong and how to prevent it next time

### Worker Went Silent
1. Check their check-in file — when was the last update?
2. If stale for more than 2 coordination cycles:
   - Note the task may be abandoned
   - Create a duplicate task in queue/ in case a new worker needs to pick it up
   - Don't delete the claimed task — the original worker may come back

## Queue Management

The leader should maintain a healthy queue:

| Workers Active | Minimum Queue Size |
|---------------|-------------------|
| 1-2 | 2-3 tasks |
| 3-4 | 4-6 tasks |
| 5+ | 6-10 tasks |

This ensures workers never sit idle waiting for the leader to create tasks.

## Leader Plan Updates

`leader-plan.md` should always reflect reality. Update it during every coordination cycle:

- **Active Workers table**: Who's doing what?
- **Completed Tasks**: What's done?
- **Task Breakdown**: What's left?
- **Notes & Decisions**: What changed and why?

## End-of-Session Protocol

When all tasks are complete:

1. Read all result files
2. Verify the original goal is met
3. Write a final summary in leader-plan.md
4. Note any follow-up work or technical debt
5. Run the reset script if the session is truly complete: `./scripts/orchestrate.sh reset`
