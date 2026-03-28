# Orchestration Patterns Reference

## Pattern 1: Fan-Out / Fan-In (Most Common)

The leader breaks a goal into independent tasks, fans them out to workers, then fans results back in for synthesis.

```
         Leader
        /  |  \         ← Fan out (create tasks)
       W1  W2  W3
        \  |  /         ← Fan in (collect results)
         Leader          ← Synthesize
```

**When to use:** Tasks are independent and can run in parallel. Most common pattern.

**Example:** "Build 5 API endpoints" → each worker builds one endpoint → leader verifies all work together.

## Pattern 2: Pipeline (Sequential Stages)

Work flows through stages. Each stage must complete before the next begins. Use `blocked_by` in task files.

```
Leader → W1 (design) → W2 (implement) → W3 (test) → Leader (review)
```

**When to use:** Each stage depends on the output of the previous stage.

**Example:** "Migrate database" → W1 writes migration scripts → W2 runs migration → W3 validates data integrity.

## Pattern 3: Competing Hypotheses

Multiple workers tackle the same problem with different approaches. Leader picks the best solution.

```
         Leader
        /  |  \         ← Same task, different approaches
       W1  W2  W3
        \  |  /         ← All submit results
         Leader          ← Pick winner
```

**When to use:** Debugging, design decisions, exploring solution spaces.

**Example:** "Fix the performance issue" → W1 tries caching → W2 tries query optimization → W3 tries algorithm change → Leader compares results.

## Pattern 4: Worker + Watchdog

One worker executes while another monitors for correctness or regressions.

```
Leader → W1 (implement) + W2 (watch/test continuously)
```

**When to use:** Safety-critical changes, refactoring with regression risk.

**Example:** W1 refactors auth module → W2 runs the test suite after each commit W1 makes, reports regressions immediately.

## Pattern 5: Hierarchical (Sub-Leaders)

For large projects, a leader delegates to sub-leaders, each of whom coordinates their own workers.

```
         Top Leader
        /         \
   Sub-Leader A   Sub-Leader B
    /    \          /    \
  W1     W2       W3     W4
```

**When to use:** 6+ workers, or when the project naturally splits into independent workstreams.

**Example:** "Build full-stack app" → Sub-Leader A handles backend (with 2 workers) → Sub-Leader B handles frontend (with 2 workers) → Top Leader integrates.

## Choosing the Right Pattern

| Situation | Pattern |
|-----------|---------|
| Independent tasks, same complexity | Fan-out/Fan-in |
| Tasks have strict ordering | Pipeline |
| Uncertain about best approach | Competing Hypotheses |
| High-risk changes | Worker + Watchdog |
| Large project, 6+ workers | Hierarchical |
| Mix of the above | Combine patterns per workstream |
