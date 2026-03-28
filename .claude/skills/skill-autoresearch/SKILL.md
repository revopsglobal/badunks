---
name: skill-autoresearch
description: Self-improving SKILL.md optimization using the Karpathy autoresearch pattern.
allowed-tools: Read, Bash, Glob, Grep
---

# Skill Autoresearch — Self-Improving SKILL.md Optimization

## What It Does

Applies the Karpathy autoresearch pattern to SKILL.md instruction bodies:

1. **Execute** — runs the skill on N random test inputs using Claude (Haiku, cheap)
2. **Evaluate** — judges each output against fixed criteria using Claude (Sonnet)
3. **Score** — counts criteria passes across the batch
4. **Keep-if-better** — saves SKILL.md as `best_skill.md` only if score improves
5. **Mutate** — Claude rewrites the instruction body targeting failures, always from the best version
6. **Repeat** — every 60 seconds by default

The critical structural rule from Karpathy: **criteria are fixed, never touched by the optimizer.**
This prevents Goodhart's Law. Only the SKILL.md instruction body changes.

## Opting a Skill In

Add an `autoresearch/config.yaml` to the skill directory:

```
.claude/skills/your-skill/
  SKILL.md                   ← optimized (train.py equivalent)
  autoresearch/
    config.yaml              ← fixed (prepare.py equivalent — never modified)
    best_skill.md            ← best version found so far
    state.json               ← run_number, best_score
    results.jsonl            ← append-only experiment log
```

## config.yaml Format

```yaml
batch_size: 5
stop_after_perfect: 3   # stop automatically after N consecutive perfect scores (default: 3)
                        # set to 1 to exit immediately on first perfect run

test_inputs:
  - "First realistic test scenario"
  - "Second realistic test scenario"
  - "Third test scenario"
  # ... 15-30 total; batch_size are sampled randomly each cycle

eval_criteria:
  - name: actionable
    description: "Output includes at least one concrete next step or recommendation the user can act on immediately"
  - name: structured
    description: "Output uses headers, bullets, or clear sections — not a wall of prose"
  - name: scoped
    description: "Output stays within the skill's domain — no irrelevant tangents"
  - name: complete
    description: "Output addresses the full request, not just part of it"
```

**Criteria writing rules (critical):**
- Each criterion must be binary — either clearly passes or clearly fails
- Description must be specific enough that a third-party judge gives consistent scores
- 3-5 criteria is ideal — too few misses quality dimensions, too many dilutes the signal
- Never put style/tone criteria that are subjective; prefer structural/content criteria

## Quick Start

```bash
# Single cycle (test your config)
python3 .claude/skills/skill-autoresearch/skill_autoresearch.py your-skill --once

# Run 10 cycles
python3 .claude/skills/skill-autoresearch/skill_autoresearch.py your-skill --cycles 10

# Continuous loop (60s between cycles)
python3 .claude/skills/skill-autoresearch/skill_autoresearch.py your-skill

# Reset and start over
python3 .claude/skills/skill-autoresearch/skill_autoresearch.py your-skill --reset --once
```

## Environment

```
ANTHROPIC_API_KEY=your_key
```

Dependencies: `anthropic`, `pyyaml`, `python-dotenv`

```bash
pip install anthropic pyyaml python-dotenv
```

## Models

| Stage | Model | Why |
|-------|-------|-----|
| Execute | `claude-haiku-4-5-20251001` | Cheap — expose instruction quality, not model quality |
| Evaluate | `claude-sonnet-4-6` | Strong judgment for consistent scoring |
| Mutate | `claude-sonnet-4-6` | Strong rewriting to target specific failures |

Using Haiku for execution is intentional: if Sonnet runs the skill, it compensates for bad
instructions. Haiku exposes gaps more honestly.

## Cost

- ~$0.001 per execution (Haiku, text-in/text-out)
- ~$0.003 per eval (Sonnet, short prompt + response)
- ~$0.01 per mutation (Sonnet, ~2K tokens)
- **~$0.03-0.05 per cycle (batch_size=5, 4 criteria)**
- At 60s intervals: ~$2-3/hour

## What Makes a Good Candidate Skill

Best candidates for autoresearch:
- Skills used frequently (high ROI on improvement)
- Skills where outputs have been corrected multiple times
- Skills with clear, measurable output structure (reports, analyses, audits)

Poor candidates:
- Skills that primarily look up external data (quality depends on the data)
- Skills with highly subjective outputs (creative writing, brand voice)
- Skills that are already working well and rarely corrected

## Skill Notes

### What Works Well
- Haiku execution exposes instruction gaps that Sonnet would silently fix — this is the right model choice
- Keep criteria to 3-5 binary checks; vague criteria produce inconsistent eval scores
- Fixing one failing criterion per mutation cycle is more reliable than fixing all at once

### Lessons Learned
- If a criterion fails 100% of the time from the start, it may be too strict or poorly worded — check before running many cycles
- The optimizer will sometimes make the SKILL.md longer to satisfy criteria; that's fine — verbosity beats failures
