#!/usr/bin/env python3
"""
Skill Autoresearch — Self-improving SKILL.md optimization.

Karpathy autoresearch pattern applied to Claude skill instructions:
1. Execute skill on N test inputs (Claude API with SKILL.md body as system prompt)
2. Evaluate each output against fixed criteria via Claude judge
3. Keep SKILL.md if score beats the current best
4. Mutate the best version's instruction body for next cycle
5. Repeat

The prepare.py / train.py separation is preserved:
  - autoresearch/config.yaml  = fixed (criteria, test inputs — never touched by optimizer)
  - SKILL.md instruction body = the thing being optimized

Usage:
    python3 skill_autoresearch.py <skill-name>              # Continuous loop
    python3 skill_autoresearch.py <skill-name> --once       # Single cycle
    python3 skill_autoresearch.py <skill-name> --cycles 5   # Run N cycles
    python3 skill_autoresearch.py <skill-name> --reset      # Reset state, start fresh
"""

import argparse
import json
import os
import base64
import random
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")

# Execution uses Haiku — cheap, fast, good enough to expose skill instruction quality
# Eval + mutation use Sonnet — need strong judgment and rewriting ability
EXECUTE_MODEL = "claude-haiku-4-5-20251001"
EVAL_MODEL = "claude-sonnet-4-6"
MUTATE_MODEL = "claude-sonnet-4-6"

SKILLS_DIR = Path(__file__).resolve().parents[1]  # .claude/skills/
CYCLE_SECONDS = 60
MAX_EXEC_WORKERS = 5
MAX_EVAL_WORKERS = 5

# ─── Prompts ──────────────────────────────────────────────────────────────────

EVAL_PROMPT = """You are evaluating a skill output against defined quality criteria.

SKILL TEST INPUT:
{test_input}

SKILL OUTPUT:
{output}

EVALUATION CRITERIA:
{criteria_text}

Rate each criterion strictly as PASS (true) or FAIL (false).

Respond in this exact JSON format:
{json_template}

For any criterion that fails, add a brief description to the failures array explaining what was missing or wrong. Be specific — vague failure messages don't help improve the skill."""

MUTATION_PROMPT = """You are optimizing a Claude skill instruction document (SKILL.md body).
Your goal: modify the instructions so outputs consistently pass ALL evaluation criteria.

The criteria are fixed and cannot be changed — only the skill instructions change.

CURRENT SKILL INSTRUCTIONS:
---
{current_body}
---

LAST BATCH RESULTS ({score}/{max_score}):
{criteria_breakdown}

COMMON FAILURES FROM THIS BATCH:
{failures}

BEST SCORE SO FAR: {best_score}/{max_score}

MUTATION RULES:
- Preserve the skill's core purpose and intent exactly
- For any criterion below 80% pass rate: add an explicit, directive instruction
- Use ALL CAPS "RULE" sections for constraints that keep failing — Claude responds to emphasis
- Be specific and imperative ("Always include X", "Never omit Y") not aspirational ("try to include X")
- Always mutate from the best known version (provided above), not the current failing version
- Return ONLY the new instruction body — no frontmatter (no --- delimiters), no explanation, no preamble"""

VISION_EVAL_PROMPT = """You are evaluating a RENDERED IMAGE of a skill output against quality criteria.

Look carefully at the IMAGE. Evaluate what you SEE visually — not markup or code.

SKILL TEST INPUT:
{test_input}

EVALUATION CRITERIA:
{criteria_text}

Examine the rendered image carefully. Rate each criterion strictly as PASS (true) or FAIL (false)
based on what you can SEE in the image.

Respond in this exact JSON format:
{json_template}

For any criterion that fails, add a brief description to the failures array explaining what you
see that fails it. Be specific about visual evidence."""


# ─── Vision eval helpers ──────────────────────────────────────────────────────


def render_svg_to_png_b64(svg_text: str, width: int = 900) -> str | None:
    """Render SVG → PNG → base64. Returns None if cairosvg not installed."""
    try:
        import cairosvg
        png_bytes = cairosvg.svg2png(bytestring=svg_text.encode(), output_width=width)
        return base64.b64encode(png_bytes).decode()
    except ImportError:
        return None
    except Exception as e:
        print(f"    RENDER: {e}")
        return None


def evaluate_one_vision(client, test_input: str, png_b64: str, criteria: list[dict]) -> dict | None:
    """Evaluate a rendered PNG image via Claude vision instead of SVG text."""
    criteria_text = "\n".join(
        f"{i+1}. {c['name'].upper()}: {c['description']}"
        for i, c in enumerate(criteria)
    )
    json_keys = {c["name"]: True for c in criteria}
    json_keys["failures"] = []
    json_template = json.dumps(json_keys, indent=2)
    prompt = VISION_EVAL_PROMPT.format(
        test_input=test_input,
        criteria_text=criteria_text,
        json_template=json_template,
    )
    try:
        response = client.messages.create(
            model=EVAL_MODEL,
            max_tokens=512,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": png_b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }],
        )
        text = response.content[0].text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"    VISION EVAL ERROR: {e}")
        return None


def load_latest_labels(skill_dir: Path) -> dict:
    """Load most recent human label session. Returns {input_str: {criteria, overall_pass}}."""
    labels_dir = skill_dir / "autoresearch" / "labels"
    if not labels_dir.exists():
        return {}
    sessions = sorted(labels_dir.glob("session_*.json"))
    if not sessions:
        return {}
    latest = sessions[-1]
    try:
        data = json.loads(latest.read_text())
        result = {}
        for output in data.get("outputs", []):
            if not output.get("skipped") and output.get("overall_pass") is not None:
                result[output["input"]] = {
                    "criteria": {
                        k: v for k, v in output.get("human_labels", {}).items()
                        if v is not None
                    },
                    "overall_pass": output["overall_pass"],
                }
        print(f"  Loaded {len(result)} human labels from {latest.name}")
        return result
    except Exception as e:
        print(f"  WARN: Could not load labels: {e}")
        return {}


# ─── File helpers ─────────────────────────────────────────────────────────────


def find_skill_dir(skill_name: str) -> Path:
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists():
        print(f"ERROR: Skill '{skill_name}' not found at {skill_dir}", file=sys.stderr)
        print(f"Available skills:", file=sys.stderr)
        for d in sorted(SKILLS_DIR.iterdir()):
            if d.is_dir() and (d / "SKILL.md").exists():
                print(f"  {d.name}", file=sys.stderr)
        sys.exit(1)
    if not (skill_dir / "SKILL.md").exists():
        print(f"ERROR: No SKILL.md found in {skill_dir}", file=sys.stderr)
        sys.exit(1)
    return skill_dir


def load_config(skill_dir: Path) -> dict:
    config_path = skill_dir / "autoresearch" / "config.yaml"
    if not config_path.exists():
        print(f"ERROR: No autoresearch/config.yaml in {skill_dir}", file=sys.stderr)
        print("Create it with test_inputs, eval_criteria, and batch_size.", file=sys.stderr)
        print("See skill-autoresearch/example-config.yaml for the format.", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(config_path.read_text())


def load_state(ar_dir: Path) -> dict:
    state_file = ar_dir / "state.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {"best_score": -1, "run_number": 0}


def save_state(ar_dir: Path, state: dict):
    (ar_dir / "state.json").write_text(json.dumps(state, indent=2))


def split_frontmatter(skill_md: str) -> tuple[str, str]:
    """Return (frontmatter_with_delimiters, body). Body is what gets optimized."""
    if skill_md.startswith("---"):
        end = skill_md.find("---", 3)
        if end != -1:
            frontmatter = skill_md[:end + 3]
            body = skill_md[end + 3:].lstrip("\n")
            return frontmatter, body
    return "", skill_md


def read_skill(skill_dir: Path) -> tuple[str, str]:
    content = (skill_dir / "SKILL.md").read_text()
    return split_frontmatter(content)


def write_skill(skill_dir: Path, frontmatter: str, body: str):
    content = (frontmatter + "\n\n" + body) if frontmatter else body
    (skill_dir / "SKILL.md").write_text(content)


def write_best(ar_dir: Path, frontmatter: str, body: str):
    content = (frontmatter + "\n\n" + body) if frontmatter else body
    (ar_dir / "best_skill.md").write_text(content)


def read_best_body(ar_dir: Path, skill_dir: Path) -> str:
    best = ar_dir / "best_skill.md"
    if best.exists():
        _, body = split_frontmatter(best.read_text())
        return body
    _, body = read_skill(skill_dir)
    return body


# ─── Execute ─────────────────────────────────────────────────────────────────


def execute_one(client, system_prompt: str, test_input: str, max_tokens: int = 1024) -> str | None:
    """Run the skill with a test input. Returns output text or None on failure."""
    try:
        response = client.messages.create(
            model=EXECUTE_MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": test_input}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        print(f"    EXEC ERROR: {e}")
        return None


# ─── Evaluate ────────────────────────────────────────────────────────────────


def build_eval_prompt(test_input: str, output: str, criteria: list[dict]) -> str:
    criteria_text = "\n".join(
        f"{i+1}. {c['name'].upper()}: {c['description']}"
        for i, c in enumerate(criteria)
    )
    json_keys = {c["name"]: True for c in criteria}
    json_keys["failures"] = []
    json_template = json.dumps(json_keys, indent=2)
    return EVAL_PROMPT.format(
        test_input=test_input,
        output=output,
        criteria_text=criteria_text,
        json_template=json_template,
    )


def evaluate_one(client, test_input: str, output: str, criteria: list[dict]) -> dict | None:
    prompt = build_eval_prompt(test_input, output, criteria)
    try:
        response = client.messages.create(
            model=EVAL_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()
        return json.loads(text)
    except Exception as e:
        print(f"    EVAL ERROR: {e}")
        return None


# ─── Mutate ──────────────────────────────────────────────────────────────────


def mutate_skill_body(client, current_body: str, eval_results: list[dict],
                      criteria: list[dict], best_score: int, max_score: int) -> str:
    n = len(eval_results)

    breakdown = []
    for c in criteria:
        passes = sum(1 for r in eval_results if r.get(c["name"]))
        pct = int(passes / n * 100) if n else 0
        breakdown.append(f"- {c['name']}: {passes}/{n} ({pct}%)")

    all_failures = []
    for r in eval_results:
        for f in r.get("failures", []):
            all_failures.append(f)
    unique_failures = list(dict.fromkeys(all_failures))[:20]
    failures_text = "\n".join(f"- {f}" for f in unique_failures) or "- None"

    score = sum(sum(1 for r in eval_results if r.get(c["name"])) for c in criteria)

    response = client.messages.create(
        model=MUTATE_MODEL,
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": MUTATION_PROMPT.format(
                current_body=current_body,
                score=score,
                max_score=max_score,
                criteria_breakdown="\n".join(breakdown),
                failures=failures_text,
                best_score=best_score,
            )
        }],
    )
    return response.content[0].text.strip()


# ─── Main cycle ──────────────────────────────────────────────────────────────


def run_cycle(client, skill_dir: Path, ar_dir: Path, config: dict, state: dict,
             use_labels: bool = False) -> dict:
    run_num = state["run_number"] + 1
    state["run_number"] = run_num

    criteria = config["eval_criteria"]
    batch_size = config.get("batch_size", 5)
    all_inputs = config["test_inputs"]
    max_score = batch_size * len(criteria)

    test_inputs = random.sample(all_inputs, min(batch_size, len(all_inputs)))
    frontmatter, body = read_skill(skill_dir)

    print(f"\n{'='*60}")
    print(f"RUN {run_num} | {datetime.now().strftime('%H:%M:%S')} | Best: {state['best_score']}/{max_score}")
    print(f"Skill: {skill_dir.name} | Criteria: {len(criteria)} | Batch: {batch_size}")
    print(f"{'='*60}")

    # ── Execute ──────────────────────────────────────────────────
    print(f"\n  Executing on {batch_size} test inputs (model: {EXECUTE_MODEL})...")
    executions: list[tuple[str, str]] = []

    max_tokens = config.get("max_tokens", 1024)

    with ThreadPoolExecutor(max_workers=MAX_EXEC_WORKERS) as pool:
        futures = {pool.submit(execute_one, client, body, inp, max_tokens): inp for inp in test_inputs}
        for f in as_completed(futures):
            inp = futures[f]
            output = f.result()
            if output:
                executions.append((inp, output))
                print(f"    ✓ {inp[:70]}")
            else:
                print(f"    ✗ FAILED: {inp[:70]}")

    if not executions:
        print("  ERROR: All executions failed. Skipping cycle.")
        save_state(ar_dir, state)
        return state

    # ── Evaluate ──────────────────────────────────────────────────
    eval_mode = config.get("eval_mode", "text")
    print(f"\n  Evaluating {len(executions)} outputs (model: {EVAL_MODEL}, mode: {eval_mode})...")
    eval_results: list[dict] = []
    # Preserve order: list of (inp, out, result)
    ordered: list[tuple[str, str, dict]] = []

    def _eval_pair(pair):
        inp, out = pair
        if eval_mode == "vision" and "<svg" in out[:500].lower():
            png_b64 = render_svg_to_png_b64(out)
            if png_b64:
                return inp, out, evaluate_one_vision(client, inp, png_b64, criteria)
        return inp, out, evaluate_one(client, inp, out, criteria)

    with ThreadPoolExecutor(max_workers=MAX_EVAL_WORKERS) as pool:
        futures = {pool.submit(_eval_pair, pair): pair for pair in executions}
        for f in as_completed(futures):
            inp, out, result = f.result()
            if result:
                eval_results.append(result)
                ordered.append((inp, out, result))
                passes = sum(1 for c in criteria if result.get(c["name"]))
                fails = result.get("failures", [])
                print(f"    {passes}/{len(criteria)} | {'; '.join(fails) if fails else 'all pass'}")
            else:
                empty = {"failures": ["eval_error"]}
                eval_results.append(empty)
                ordered.append((inp, out, empty))
                print(f"    0/{len(criteria)} | eval failed")

    # ── Human label override (first cycle when --use-labels) ───────
    if use_labels:
        human_map = load_latest_labels(skill_dir)
        if human_map:
            overridden = 0
            disagree = {c["name"]: [0, 0] for c in criteria}  # [ai↑h↓, ai↓h↑]
            for i, (inp, out, ai_r) in enumerate(ordered):
                if inp not in human_map:
                    continue
                h = human_map[inp]
                # Record disagreements before overriding
                for c in criteria:
                    ai_v = bool(ai_r.get(c["name"], False))
                    h_v = h["criteria"].get(c["name"])
                    if h_v is not None and ai_v != bool(h_v):
                        if ai_v and not h_v:
                            disagree[c["name"]][0] += 1
                        else:
                            disagree[c["name"]][1] += 1
                # Build human result (None criteria fall back to AI eval)
                h_result = {}
                for c in criteria:
                    h_v = h["criteria"].get(c["name"])
                    h_result[c["name"]] = bool(h_v) if h_v is not None else bool(ai_r.get(c["name"], False))
                h_result["failures"] = []
                eval_results[i] = h_result
                ordered[i] = (inp, out, h_result)
                overridden += 1
            if overridden:
                print(f"\n  ★ Human labels applied: {overridden}/{len(ordered)} outputs overridden")
                has_disagree = any(v[0] + v[1] > 0 for v in disagree.values())
                if has_disagree:
                    print("  AI vs Human disagreements (per criterion):")
                    for c in criteria:
                        d = disagree[c["name"]]
                        if d[0] + d[1] > 0:
                            print(f"    {c['name']:<35}  AI↑/H↓: {d[0]}  AI↓/H↑: {d[1]}")

    # ── Save outputs ──────────────────────────────────────────────
    out_dir = ar_dir / "outputs" / f"run_{run_num:03d}"
    out_dir.mkdir(parents=True, exist_ok=True)
    run_records = []
    for i, (inp, out, result) in enumerate(ordered):
        is_svg = out.strip().lower().startswith("<svg") or "xmlns" in out[:200]
        ext = ".svg" if is_svg else ".txt"
        out_file = out_dir / f"exec_{i:02d}{ext}"
        out_file.write_text(out)
        run_records.append({
            "index": i,
            "input": inp,
            "output_file": out_file.name,
            "criteria": {c["name"]: result.get(c["name"], False) for c in criteria},
            "failures": result.get("failures", []),
        })
    (out_dir / "records.json").write_text(json.dumps(run_records, indent=2))

    # ── Score ─────────────────────────────────────────────────────
    score = sum(sum(1 for r in eval_results if r.get(c["name"])) for c in criteria)

    print(f"\n  SCORE: {score}/{max_score}")
    for c in criteria:
        passes = sum(1 for r in eval_results if r.get(c["name"]))
        bar = "█" * passes + "░" * (batch_size - passes)
        print(f"    {c['name']:<30} {bar}  {passes}/{batch_size}")

    # ── Log ───────────────────────────────────────────────────────
    criteria_scores = {
        c["name"]: sum(1 for r in eval_results if r.get(c["name"]))
        for c in criteria
    }
    log_entry = {
        "run": run_num,
        "timestamp": datetime.now().isoformat(),
        "score": score,
        "max": max_score,
        "criteria": criteria_scores,
        "skill_body_len": len(body),
        "executed": len(executions),
        "kept": False,
    }

    # ── Keep or discard ───────────────────────────────────────────
    if score > state["best_score"]:
        state["best_score"] = score
        write_best(ar_dir, frontmatter, body)
        log_entry["kept"] = True
        print(f"\n  ★ NEW BEST: {score}/{max_score}")
    else:
        print(f"\n  No improvement ({score} vs best {state['best_score']})")

    with open(ar_dir / "results.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    # ── Mutate ────────────────────────────────────────────────────
    if score < max_score:
        print(f"\n  Mutating skill instructions (model: {MUTATE_MODEL})...")
        base_body = read_best_body(ar_dir, skill_dir)
        new_body = mutate_skill_body(client, base_body, eval_results, criteria,
                                     state["best_score"], max_score)
        write_skill(skill_dir, frontmatter, new_body)
        delta = len(new_body) - len(body)
        print(f"  Updated SKILL.md: {len(new_body)} chars ({'+' if delta >= 0 else ''}{delta})")
    else:
        print(f"\n  ★★ PERFECT {score}/{max_score} — skill fully optimized.")
        # Restore best version as the final SKILL.md
        best_body = read_best_body(ar_dir, skill_dir)
        write_skill(skill_dir, frontmatter, best_body)

    save_state(ar_dir, state)
    return state


# ─── Entry point ─────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Skill autoresearch — self-improving SKILL.md")
    parser.add_argument("skill", help="Skill directory name in .claude/skills/")
    parser.add_argument("--once", action="store_true", help="Run a single cycle then exit")
    parser.add_argument("--cycles", type=int, default=0, help="Run N cycles (0 = infinite)")
    parser.add_argument("--reset", action="store_true", help="Reset state and start from scratch")
    parser.add_argument("--use-labels", action="store_true", dest="use_labels",
                        help="On the first cycle of this run, override AI eval with human labels from skill-label")
    args = parser.parse_args()

    if not ANTHROPIC_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    skill_dir = find_skill_dir(args.skill)
    ar_dir = skill_dir / "autoresearch"
    ar_dir.mkdir(exist_ok=True)

    config = load_config(skill_dir)

    if args.reset:
        import shutil
        for f in ["state.json", "results.jsonl", "best_skill.md"]:
            p = ar_dir / f
            if p.exists():
                p.unlink()
        outputs_dir = ar_dir / "outputs"
        if outputs_dir.exists():
            shutil.rmtree(outputs_dir)
        print(f"Reset state + outputs for {args.skill}")

    state = load_state(ar_dir)
    batch_size = config.get("batch_size", 5)
    n_criteria = len(config["eval_criteria"])
    max_score = batch_size * n_criteria

    print("Skill Autoresearch")
    print(f"  Skill:        {args.skill}")
    print(f"  Test inputs:  {len(config['test_inputs'])} (sampling {batch_size}/cycle)")
    print(f"  Criteria:     {n_criteria} → max score {max_score}/cycle")
    print(f"  Exec model:   {EXECUTE_MODEL}")
    print(f"  Eval model:   {EVAL_MODEL}")
    print(f"  Mutate model: {MUTATE_MODEL}")
    print(f"  State:        run {state['run_number']}, best {state['best_score']}/{max_score}")
    print(f"  Log:          {ar_dir / 'results.jsonl'}")

    if args.once:
        run_cycle(client, skill_dir, ar_dir, config, state, use_labels=args.use_labels)
        return

    max_cycles = args.cycles or float("inf")
    consecutive_perfect = 0
    perfect_stop = config.get("stop_after_perfect", 3)  # stop after N consecutive perfect runs
    i = 0
    while i < max_cycles:
        start = time.time()
        try:
            # use_labels only on the first cycle of this invocation to anchor to human ground truth
            state = run_cycle(client, skill_dir, ar_dir, config, state,
                              use_labels=args.use_labels and i == 0)
        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"\n  CYCLE ERROR: {e}")
            traceback.print_exc()
        elapsed = time.time() - start
        i += 1

        # Early exit once score is stable at perfect
        batch_size = config.get("batch_size", 5)
        max_score = batch_size * len(config["eval_criteria"])
        if state["best_score"] >= max_score:
            consecutive_perfect += 1
            if consecutive_perfect >= perfect_stop:
                print(f"\n  ✓ Stable at {max_score}/{max_score} for {perfect_stop} consecutive runs — stopping early.")
                break
        else:
            consecutive_perfect = 0

        if i < max_cycles:
            wait = max(0, CYCLE_SECONDS - elapsed)
            if wait > 0:
                print(f"\n  Waiting {wait:.0f}s until next cycle... (Ctrl+C to stop)")
                time.sleep(wait)

    print(f"\nDone. Best: {state['best_score']}/{max_score} over {state['run_number']} runs")
    best_path = ar_dir / "best_skill.md"
    if best_path.exists():
        print(f"Best version: {best_path}")


if __name__ == "__main__":
    main()
