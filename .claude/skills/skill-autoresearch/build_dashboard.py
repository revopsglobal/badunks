#!/usr/bin/env python3
"""
Build a self-contained HTML dashboard from skill autoresearch results.
Embeds all SVG outputs inline — no external files needed.

Usage:
    python3 build_dashboard.py <skill-name>
    python3 build_dashboard.py revops-vector-art
"""

import json
import re
import sys
from pathlib import Path

SKILLS_DIR = Path(__file__).resolve().parents[1]


def load_results(ar_dir: Path) -> list[dict]:
    results_file = ar_dir / "results.jsonl"
    if not results_file.exists():
        return []
    runs = []
    for line in results_file.read_text().strip().splitlines():
        if line.strip():
            try:
                runs.append(json.loads(line))
            except Exception:
                pass
    return runs


def load_run_outputs(ar_dir: Path, run_num: int) -> list[dict]:
    run_dir = ar_dir / "outputs" / f"run_{run_num:03d}"
    records_file = run_dir / "records.json"
    if not records_file.exists():
        return []
    records = json.loads(records_file.read_text())
    # Load actual SVG/text content for each record
    for rec in records:
        out_file = run_dir / rec["output_file"]
        if out_file.exists():
            rec["output"] = out_file.read_text()
        else:
            rec["output"] = ""
    return records


def clean_svg(svg_text: str) -> str:
    """Strip XML declaration, normalize for inline embedding."""
    svg = svg_text.strip()
    if svg.startswith("<?xml"):
        svg = svg[svg.index("<svg"):]
    # Remove width/height fixed attrs so it scales with CSS
    svg = re.sub(r'\s+width="\d+"', '', svg)
    svg = re.sub(r'\s+height="\d+"', '', svg)
    return svg


def criteria_names(runs: list[dict]) -> list[str]:
    if not runs:
        return []
    return list(runs[0].get("criteria", {}).keys())


def build(skill_name: str):
    skill_dir = SKILLS_DIR / skill_name
    ar_dir = skill_dir / "autoresearch"

    if not ar_dir.exists():
        print(f"No autoresearch data found for '{skill_name}'", file=sys.stderr)
        sys.exit(1)

    runs = load_results(ar_dir)
    if not runs:
        print(f"No results.jsonl found — run some cycles first.", file=sys.stderr)
        sys.exit(1)

    criteria = criteria_names(runs)
    batch_size = runs[0].get("executed", 5) if runs else 5
    max_score = runs[0].get("max", len(criteria) * batch_size) if runs else len(criteria) * batch_size

    # Load outputs for each run
    for run in runs:
        run["outputs"] = load_run_outputs(ar_dir, run["run"])

    # Build run cards HTML
    run_cards_html = ""
    for run in runs:
        score = run["score"]
        pct = int(score / max_score * 100)
        kept = run.get("kept", False)
        badge = '<span class="tag-keep">★ kept</span>' if kept else '<span class="tag-skip">—</span>'
        score_class = "perfect" if score == max_score else ("good" if pct >= 80 else "bad")

        # SVG thumbnails
        thumbs = ""
        for rec in run["outputs"]:
            inp = rec.get("input", "")[:50]
            out = rec.get("output", "")
            crit = rec.get("criteria", {})
            passes = sum(1 for v in crit.values() if v)
            total = len(crit)
            fail_class = " fail" if passes < total else ""
            failures = rec.get("failures", [])
            fail_tip = "; ".join(failures) if failures else "all pass"

            if out.strip().lower().startswith("<svg") or "<svg" in out[:300]:
                svg_content = clean_svg(out)
                thumb = f'<div class="thumb{fail_class}" title="{fail_tip}"><div class="thumb-svg">{svg_content}</div><div class="thumb-label">{inp}…</div><div class="thumb-score">{passes}/{total}</div></div>'
            else:
                thumb = f'<div class="thumb{fail_class}" title="{fail_tip}"><div class="thumb-text">[no SVG]</div><div class="thumb-label">{inp}…</div><div class="thumb-score">{passes}/{total}</div></div>'
            thumbs += thumb

        # Criteria mini bars
        crit_bars = ""
        for cname, cval in run.get("criteria", {}).items():
            pct_c = int(cval / batch_size * 100)
            color = "#16F0DF" if cval == batch_size else ("#f5a623" if cval > 0 else "#e05555")
            crit_bars += f'<div class="crit-row"><span class="crit-name">{cname.replace("_", " ")}</span><div class="crit-bar-bg"><div class="crit-bar-fill" style="width:{pct_c}%;background:{color}"></div></div><span class="crit-val" style="color:{color}">{cval}/{batch_size}</span></div>'

        run_cards_html += f"""
<div class="run-card">
  <div class="run-card-header">
    <div class="run-num">Run {run['run']}</div>
    <div class="run-score {score_class}">{score}/{max_score}</div>
    {badge}
    <div class="run-time">{run.get('timestamp','')[-8:-3] if run.get('timestamp') else ''}</div>
  </div>
  <div class="run-criteria">{crit_bars}</div>
  <div class="run-thumbs">{thumbs}</div>
</div>"""

    # Build criteria data for JS charts
    criteria_js = json.dumps(criteria)
    scores_js = json.dumps([r["score"] for r in runs])
    labels_js = json.dumps([f"R{r['run']}" for r in runs])
    max_score_js = max_score
    kept_js = json.dumps([r.get("kept", False) for r in runs])
    criteria_data_js = json.dumps({
        c: [r.get("criteria", {}).get(c, 0) for r in runs]
        for c in criteria
    })
    baseline = runs[0]["score"] if runs else 0
    best = max((r["score"] for r in runs), default=0)
    improvement = round((best - baseline) / baseline * 100, 1) if baseline > 0 else 0
    kept_count = sum(1 for r in runs if r.get("kept"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Skill Autoresearch — {skill_name}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:#0a0d14; color:#e4e6ed; padding:28px; max-width:1400px; margin:0 auto; }}
h1 {{ font-size:24px; font-weight:700; color:#fff; }}
.header-row {{ display:flex; align-items:center; gap:12px; margin-bottom:6px; }}
.badge {{ background:#2DD6FF; color:#072C87; font-size:10px; font-weight:800; padding:3px 10px; border-radius:4px; letter-spacing:1.5px; text-transform:uppercase; }}
.subtitle {{ color:#4a4f62; font-size:13px; margin-bottom:28px; }}

.stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:24px; }}
.stat-card {{ background:#111520; border:1px solid #1e2333; border-radius:10px; padding:16px 20px; }}
.stat-label {{ font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:#3a3f52; margin-bottom:8px; }}
.stat-value {{ font-size:28px; font-weight:700; }}
.cyan {{ color:#2DD6FF; }} .teal {{ color:#16F0DF; }} .white {{ color:#fff; }} .muted {{ color:#5a5f72; }}

.charts-row {{ display:grid; grid-template-columns:2fr 1fr; gap:14px; margin-bottom:24px; }}
.panel {{ background:#111520; border:1px solid #1e2333; border-radius:10px; padding:20px 22px; }}
.panel-title {{ font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:#3a3f52; margin-bottom:14px; }}
.chart-wrap {{ height:200px; }}

.crit-mini-grid {{ display:grid; grid-template-columns:1fr; gap:6px; }}
.crit-mini {{ display:flex; align-items:center; gap:8px; }}
.crit-mini-label {{ font-size:10px; color:#5a5f72; width:130px; flex-shrink:0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.crit-mini-wrap {{ height:40px; flex:1; }}

h2 {{ font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#3a3f52; margin-bottom:14px; }}

.run-card {{ background:#111520; border:1px solid #1e2333; border-radius:10px; padding:18px 20px; margin-bottom:16px; }}
.run-card-header {{ display:flex; align-items:center; gap:12px; margin-bottom:14px; }}
.run-num {{ font-size:15px; font-weight:700; color:#fff; width:50px; }}
.run-score {{ font-size:22px; font-weight:700; }}
.run-score.perfect {{ color:#16F0DF; }}
.run-score.good {{ color:#2DD6FF; }}
.run-score.bad {{ color:#f5a623; }}
.tag-keep {{ background:rgba(22,240,223,0.12); color:#16F0DF; border-radius:4px; padding:2px 8px; font-size:11px; font-weight:700; }}
.tag-skip {{ color:#2a2f42; font-size:11px; }}
.run-time {{ color:#2a2f42; font-size:11px; margin-left:auto; }}

.run-criteria {{ margin-bottom:14px; }}
.crit-row {{ display:flex; align-items:center; gap:8px; margin-bottom:4px; }}
.crit-name {{ font-size:10px; color:#4a4f62; width:160px; flex-shrink:0; }}
.crit-bar-bg {{ flex:1; height:4px; background:#1a1f2e; border-radius:2px; overflow:hidden; }}
.crit-bar-fill {{ height:100%; border-radius:2px; transition:width 0.3s; }}
.crit-val {{ font-size:10px; width:30px; text-align:right; }}

.run-thumbs {{ display:flex; gap:10px; flex-wrap:wrap; }}
.thumb {{ width:220px; background:#0d1018; border:1px solid #1a1f2e; border-radius:8px; overflow:hidden; cursor:pointer; transition:border-color 0.2s; }}
.thumb:hover {{ border-color:#2DD6FF; }}
.thumb.fail {{ border-color:#f5a623; }}
.thumb-svg {{ width:100%; aspect-ratio:12/7; overflow:hidden; padding:4px; background:#f8f8f8; }}
.thumb-svg svg {{ width:100%; height:100%; }}
.thumb-text {{ width:100%; aspect-ratio:12/7; display:flex; align-items:center; justify-content:center; color:#3a3f52; font-size:12px; background:#0d1018; }}
.thumb-label {{ font-size:9px; color:#4a4f62; padding:4px 6px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
.thumb-score {{ font-size:9px; color:#5a5f72; padding:0 6px 4px; }}

/* Modal */
.modal-overlay {{ display:none; position:fixed; inset:0; background:rgba(0,0,0,0.85); z-index:100; align-items:center; justify-content:center; }}
.modal-overlay.open {{ display:flex; }}
.modal {{ background:#111520; border:1px solid #2a2f42; border-radius:12px; padding:24px; max-width:900px; width:90%; max-height:90vh; overflow-y:auto; }}
.modal-svg {{ width:100%; background:#f8f8f8; border-radius:8px; padding:16px; margin-bottom:16px; }}
.modal-svg svg {{ width:100%; height:auto; }}
.modal-title {{ font-size:13px; color:#fff; margin-bottom:8px; font-weight:600; }}
.modal-meta {{ font-size:11px; color:#4a4f62; margin-bottom:16px; }}
.modal-close {{ background:none; border:1px solid #2a2f42; color:#8a8f9e; padding:6px 14px; border-radius:6px; cursor:pointer; font-size:12px; float:right; }}
.modal-close:hover {{ color:#fff; border-color:#5a5f72; }}
</style>
</head>
<body>

<div class="header-row"><h1>Skill Autoresearch</h1><span class="badge">{skill_name}</span></div>
<div class="subtitle">8 criteria · {batch_size} SVGs/cycle · Haiku execute → Sonnet eval → Sonnet mutate · 100% Anthropic</div>

<div class="stats">
  <div class="stat-card"><div class="stat-label">Best Score</div><div class="stat-value teal" id="v-best">—</div></div>
  <div class="stat-card"><div class="stat-label">Baseline</div><div class="stat-value muted">{baseline}/{max_score}</div></div>
  <div class="stat-card"><div class="stat-label">Improvement</div><div class="stat-value cyan">+{improvement}%</div></div>
  <div class="stat-card"><div class="stat-label">Runs / Kept</div><div class="stat-value white">{len(runs)} / {kept_count}</div></div>
</div>

<div class="charts-row">
  <div class="panel">
    <div class="panel-title">Score Over 20 Runs</div>
    <div class="chart-wrap"><canvas id="mainChart"></canvas></div>
  </div>
  <div class="panel">
    <div class="panel-title">Criteria Trend</div>
    <div class="crit-mini-grid" id="critMinis"></div>
  </div>
</div>

<h2>Run-by-Run Outputs — click any SVG to inspect</h2>
{run_cards_html}

<!-- Modal -->
<div class="modal-overlay" id="modal" onclick="closeModal(event)">
  <div class="modal">
    <button class="modal-close" onclick="document.getElementById('modal').classList.remove('open')">Close ✕</button>
    <div class="modal-title" id="modal-title"></div>
    <div class="modal-meta" id="modal-meta"></div>
    <div class="modal-svg" id="modal-svg"></div>
  </div>
</div>

<script>
const SCORES = {scores_js};
const LABELS = {labels_js};
const MAX = {max_score_js};
const KEPT = {kept_js};
const CRIT_DATA = {criteria_data_js};
const CRIT_NAMES = {criteria_js};
const BATCH = {batch_size};

const TEAL = '#16F0DF'; const CYAN = '#2DD6FF'; const ORANGE = '#f5a623'; const DIM = '#2a2f42';

Chart.defaults.color = '#4a4f62';
Chart.defaults.borderColor = '#1a1f2e';

// ── Main chart ──────────────────────────────────────────────────
const ctx = document.getElementById('mainChart').getContext('2d');
let best = -1;
const dotColors = SCORES.map((s,i) => {{
  if (KEPT[i]) {{ best = s; return TEAL; }}
  return s < MAX ? (s < MAX*0.8 ? ORANGE : CYAN) : DIM;
}});

new Chart(ctx, {{
  type:'line',
  data:{{
    labels:LABELS,
    datasets:[{{
      data:SCORES,
      borderColor:CYAN,
      backgroundColor:'rgba(45,214,255,0.05)',
      fill:true,
      tension:0.3,
      pointRadius:5,
      pointBackgroundColor:dotColors,
      pointBorderColor:'#0a0d14',
      pointBorderWidth:2,
    }}]
  }},
  options:{{
    responsive:true, maintainAspectRatio:false,
    plugins:{{ legend:{{display:false}}, tooltip:{{ backgroundColor:'#111520', borderColor:'#2a2f42', borderWidth:1, callbacks:{{ label: c => ` ${{c.raw}}/${{MAX}}` }} }} }},
    scales:{{
      x:{{ grid:{{display:false}}, ticks:{{font:{{size:10}},color:'#3a3f52'}} }},
      y:{{ min:0, max:MAX, grid:{{color:'#141822'}}, ticks:{{font:{{size:10}},color:'#3a3f52',stepSize:Math.ceil(MAX/8)}} }}
    }}
  }}
}});

// Update best display
document.getElementById('v-best').textContent = Math.max(...SCORES) + '/' + MAX;

// ── Criteria minis ──────────────────────────────────────────────
const colors = [TEAL, CYAN, '#39569F', ORANGE, '#8A91A2', '#CDD5E7', '#2DD6FF', '#16F0DF'];
const minis = document.getElementById('critMinis');
CRIT_NAMES.forEach((name, i) => {{
  const div = document.createElement('div');
  div.className = 'crit-mini';
  const label = document.createElement('div');
  label.className = 'crit-mini-label';
  label.textContent = name.replace(/_/g,' ');
  const wrap = document.createElement('div');
  wrap.className = 'crit-mini-wrap';
  const canvas = document.createElement('canvas');
  wrap.appendChild(canvas);
  div.appendChild(label);
  div.appendChild(wrap);
  minis.appendChild(div);
  const color = colors[i % colors.length];
  new Chart(canvas.getContext('2d'), {{
    type:'line',
    data:{{
      labels:LABELS,
      datasets:[{{ data:CRIT_DATA[name], borderColor:color, backgroundColor:`${{color}}22`, fill:true, tension:0.3, pointRadius:2, pointBackgroundColor:color }}]
    }},
    options:{{
      responsive:true, maintainAspectRatio:false,
      plugins:{{legend:{{display:false}}, tooltip:{{enabled:false}}}},
      scales:{{ x:{{display:false}}, y:{{min:0, max:BATCH, display:false}} }}
    }}
  }});
}});

// ── Modal ────────────────────────────────────────────────────────
document.querySelectorAll('.thumb').forEach(thumb => {{
  thumb.addEventListener('click', () => {{
    const svgEl = thumb.querySelector('.thumb-svg svg');
    const label = thumb.querySelector('.thumb-label')?.textContent || '';
    const score = thumb.querySelector('.thumb-score')?.textContent || '';
    const tip = thumb.getAttribute('title') || '';
    if (!svgEl) return;
    document.getElementById('modal-title').textContent = label;
    document.getElementById('modal-meta').textContent = `${{score}} · ${{tip}}`;
    document.getElementById('modal-svg').innerHTML = svgEl.outerHTML;
    document.getElementById('modal').classList.add('open');
  }});
}});

function closeModal(e) {{
  if (e.target.id === 'modal') document.getElementById('modal').classList.remove('open');
}}
</script>
</body>
</html>"""

    out_path = ar_dir / "dashboard.html"
    out_path.write_text(html)
    print(f"Dashboard written: {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 build_dashboard.py <skill-name>", file=sys.stderr)
        sys.exit(1)
    path = build(sys.argv[1])
    import subprocess
    subprocess.run(["open", str(path)])
