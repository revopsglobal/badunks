---
name: skill-label
description: Human-in-the-loop labeling tool for skill outputs.---

# skill-label — Human Labeling Tool for Skill Autoresearch

Generates skill outputs, renders them to PNG if applicable, and opens a
browser labeling UI where you click Pass/Fail on each quality criterion.
Saves `labels/session_{timestamp}.json` as ground truth for `--use-labels`
in `skill_autoresearch.py`.

## Usage

```bash
# Generate 10 fresh outputs and open labeling UI
python3 .claude/skills/skill-label/skill_label.py revops-vector-art

# Generate N outputs
python3 .claude/skills/skill-label/skill_label.py revops-vector-art --batch 15

# Label outputs from an existing autoresearch run
python3 .claude/skills/skill-label/skill_label.py revops-vector-art --from-run 5

# List saved sessions and their stats
python3 .claude/skills/skill-label/skill_label.py revops-vector-art --review
```

## Dependencies

```bash
pip install anthropic pyyaml python-dotenv cairosvg
```

`cairosvg` is optional — if not installed, SVGs render inline in the browser instead of as PNGs.

## UI Controls

- **← →** navigate outputs
- **Enter** save current labels and advance
- **S** skip current output
- Click criterion **Pass / Fail** buttons
- Set **Overall** pass/fail for the output
- Add **Notes** explaining failures
- Click **Save All Labels** when done → writes `labels/session_{timestamp}.json`

## Output Format

```json
{
  "skill": "revops-vector-art",
  "session": "2026-03-14T03:00:00",
  "outputs": [
    {
      "index": 0,
      "input": "Create a visual for data integration",
      "human_labels": {
        "no_background_rect": true,
        "brand_colors_only": false
      },
      "overall_pass": false,
      "skipped": false,
      "notes": "Off-brand gray #444 used on secondary boxes"
    }
  ]
}
```

## How Labels Feed Into Autoresearch

```bash
# Use human labels on cycle 1 to anchor the loop to human ground truth
python3 .claude/skills/skill-autoresearch/skill_autoresearch.py revops-vector-art \
  --use-labels --cycles 20
```

On cycle 1: the autoresearch runner matches labeled inputs to the batch,
replaces AI eval scores with human scores for those inputs, and prints a
disagreement report showing where AI and human disagreed per criterion.
Subsequent cycles use AI eval (now calibrated to match human baseline).

## Why This Matters

Without human labels, the autoresearch loop converges on "Claude's 40/40"
not "Greg's 40/40". Human labeling is the calibration step that anchors the
loop to actual quality standards. The same pattern applies to any visual
skill where outputs need human aesthetic judgment.
