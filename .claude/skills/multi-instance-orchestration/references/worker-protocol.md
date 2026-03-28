# Worker Protocol Reference

## Worker Mindset

A worker is a **focused executor**. It picks up one task at a time, does it well, reports clearly, and moves on. It does NOT:

- Plan the overall project (that's the leader's job)
- Modify files outside its assigned scope
- Communicate with other workers directly (all coordination goes through the filesystem)
- Create tasks (it can suggest follow-ups in its result file, but the leader decides)

## The Worker Loop

```
┌──────────────────────────────────────────────────────────┐
│                      WORKER LOOP                         │
│                                                          │
│  1. Update check-in → "idle, looking for tasks"          │
│  2. Read queue/ → Pick highest-priority unblocked task   │
│  3. Claim task → mv queue/task-NNN.md claimed/           │
│  4. Update check-in → "working on task-NNN"              │
│  5. Execute task → Do the work                           │
│  6. Write result → results/result-NNN.md                 │
│  7. Update check-in → "completed task-NNN"               │
│  8. Go to step 1                                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Claiming Tasks Safely

The file-move operation is the claiming mechanism:

```bash
mv .claude/orchestration/queue/task-001-api-auth.md .claude/orchestration/claimed/task-001-api-auth.md
```

If the `mv` fails (file not found), another worker already claimed it. Pick the next task. Do not retry the same file.

After moving, edit the task file in claimed/:
- Set `assigned_to: {your-name}`
- Set `status: in_progress`

## Checking for Dependencies

Before claiming a task, check its `blocked_by` field:

1. If `blocked_by: none` → claim it immediately
2. If `blocked_by: task-002` → check if `results/result-002-*.md` exists
   - If yes → the dependency is done, you can claim this task
   - If no → skip this task, pick another one

## Check-in Frequency

Update your check-in file at these moments:

| Event | Status to Set |
|-------|--------------|
| Starting up | `idle` |
| Claiming a task | `working`, set `current_task` |
| Hit a milestone (halfway) | `working`, update progress notes |
| Hit a blocker | `blocked`, describe blocker and questions |
| Completed a task | `completed_task`, set current_task to "NNN (completed)" |
| Queue is empty | `idle`, note "waiting for tasks" |

## Writing Good Results

Your result file is how the leader evaluates your work. Include:

1. **Summary**: What was accomplished in 2-3 sentences
2. **Deliverables checklist**: Check off each deliverable from the original task
3. **Files modified**: Table of every file touched with what changed
4. **Testing**: How you verified the work (commands run, tests passed)
5. **Follow-up suggestions**: Anything the leader should know about next steps

## Handling Blocked Situations

When you're blocked:

1. **Immediately** update your check-in file with:
   - `status: blocked`
   - Clear description of the blocker
   - Specific questions for the leader
2. **Check if you can work around it.** Sometimes you can skip one part and do the rest.
3. **Look for another task.** If the queue has unblocked tasks, claim one while waiting.
4. **Check back.** After completing another task, re-read your blocked task — the leader may have written answers into the task file or your check-in.

## File Ownership Rules

- Only modify files explicitly listed in your task's scope
- If you discover you need to change a file outside your scope:
  - Do NOT change it
  - Note it in your result file under "Follow-up suggestions"
  - The leader will create a new task for it or adjust scope
- This prevents two workers from creating merge conflicts

## Quality Standards

Before marking a task complete:

- [ ] All deliverables in the task are addressed
- [ ] Code compiles / runs without errors
- [ ] You've tested your changes (run tests, verify manually)
- [ ] You haven't modified files outside your assigned scope
- [ ] Your result file is complete and specific
- [ ] Your check-in file is updated
