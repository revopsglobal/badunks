#!/usr/bin/env python3
"""
skill-label — Human-in-the-loop labeling tool for skill autoresearch.

Generates skill outputs, renders SVGs to PNG, and serves a browser-based
labeling UI for Pass/Fail annotation per quality criterion. Saves ground-truth
labels consumed by skill_autoresearch.py --use-labels.

Usage:
    python3 skill_label.py <skill-name>               # 10 fresh outputs
    python3 skill_label.py <skill-name> --batch N     # N fresh outputs
    python3 skill_label.py <skill-name> --from-run N  # label autoresearch run N
    python3 skill_label.py <skill-name> --review      # list saved sessions
"""

import argparse
import base64
import json
import os
import random
import socket
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
EXECUTE_MODEL = "claude-haiku-4-5-20251001"
SKILLS_DIR = Path(__file__).resolve().parents[1]  # .claude/skills/


# ─── HTML Template ────────────────────────────────────────────────────────────

_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>skill-label</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; background:#f5f6f8; color:#1a1d26; min-height:100vh; }
.header { background:#ffffff; border-bottom:1px solid #dde1ec; padding:12px 24px; display:flex; align-items:center; gap:14px; flex-wrap:wrap; }
.header h1 { font-size:15px; font-weight:700; color:#1a1d26; }
.badge { background:#2DD6FF; color:#072C87; font-size:10px; font-weight:800; padding:2px 8px; border-radius:4px; letter-spacing:1px; text-transform:uppercase; }
.progress-wrap { flex:1; min-width:160px; max-width:260px; margin-left:auto; }
.progress-label { font-size:10px; color:#4a4f62; margin-bottom:4px; text-align:right; }
.progress-bar { height:3px; background:#1e2333; border-radius:2px; overflow:hidden; }
.progress-fill { height:100%; background:#2DD6FF; border-radius:2px; transition:width 0.3s; }
.nav-btns { display:flex; gap:6px; }
.btn { padding:5px 12px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; border:none; transition:all 0.15s; }
.btn-primary { background:#2DD6FF; color:#072C87; }
.btn-primary:hover { background:#16F0DF; }
.btn-secondary { background:transparent; color:#5a5f72; border:1px solid #2a2f42; }
.btn-secondary:hover { color:#fff; border-color:#5a5f72; }
.btn-save-all { background:#16F0DF; color:#072C87; padding:6px 18px; font-size:12px; font-weight:700; }
.btn-save-all:hover { background:#2DD6FF; }
.btn-save-all:disabled { opacity:0.4; cursor:not-allowed; }
.container { max-width:1140px; margin:0 auto; padding:20px 24px; }
.item-nav { display:flex; align-items:center; gap:10px; margin-bottom:18px; }
.item-dots { display:flex; gap:4px; flex-wrap:wrap; }
.dot { width:11px; height:11px; border-radius:50%; background:#1e2333; cursor:pointer; transition:background 0.2s; flex-shrink:0; }
.dot.labeled-pass { background:#16F0DF; }
.dot.labeled-fail { background:#f5a623; }
.dot.labeled-skip { background:#3a3f52; }
.dot.current { outline:2px solid #2DD6FF; outline-offset:2px; }
.layout { display:grid; grid-template-columns:1fr 390px; gap:18px; align-items:start; }
@media(max-width:820px) { .layout { grid-template-columns:1fr; } }
.image-card { background:#ffffff; border:1px solid #dde1ec; border-radius:10px; overflow:hidden; }
.image-area { background:#0f2214; min-height:280px; display:flex; align-items:center; justify-content:center; overflow:hidden; border-radius:8px 8px 0 0; }
.image-area img { width:100%; height:auto; display:block; }
.image-area .svg-wrap { width:100%; padding:8px; }
.image-area .svg-wrap svg { width:100%; height:auto; }
.image-area .no-image { color:#888; font-size:13px; text-align:center; padding:40px; }
.image-meta { padding:12px 16px; border-top:1px solid #1e2333; }
.meta-label { font-size:10px; text-transform:uppercase; letter-spacing:1px; color:#3a3f52; margin-bottom:4px; }
.meta-text { font-size:13px; color:#8a91a2; line-height:1.5; }
.meta-idx { font-size:11px; color:#2a2f42; margin-top:6px; }
.label-card { background:#ffffff; border:1px solid #dde1ec; border-radius:10px; padding:18px 20px; }
.label-card h2 { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:#3a3f52; margin-bottom:14px; }
.crit-list { display:flex; flex-direction:column; gap:9px; margin-bottom:18px; }
.crit-row { display:flex; align-items:center; gap:10px; }
.crit-name { font-size:11px; color:#8a91a2; flex:1; line-height:1.4; cursor:help; word-break:break-word; }
.crit-btns { display:flex; gap:5px; flex-shrink:0; }
.radio-btn { padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600; cursor:pointer; border:1px solid #c8ccda; background:transparent; color:#5a6070; transition:all 0.15s; }
.radio-btn.pass.active { background:rgba(22,240,223,0.15); border-color:#16F0DF; color:#16F0DF; }
.radio-btn.fail.active { background:rgba(245,166,35,0.15); border-color:#f5a623; color:#f5a623; }
.radio-btn:hover:not(.active) { border-color:#5a5f72; color:#aaa; }
.divider { height:1px; background:#1e2333; margin:14px 0; }
.overall-row { display:flex; align-items:center; gap:10px; margin-bottom:14px; }
.overall-label { font-size:12px; font-weight:600; color:#e4e6ed; flex:1; }
.overall-pass.active { background:rgba(22,240,223,0.2) !important; border-color:#16F0DF !important; color:#16F0DF !important; font-size:12px !important; padding:5px 14px !important; }
.overall-fail.active { background:rgba(224,85,85,0.2) !important; border-color:#e05555 !important; color:#e05555 !important; font-size:12px !important; padding:5px 14px !important; }
.notes-area { margin-bottom:14px; }
.notes-area label { display:block; font-size:10px; text-transform:uppercase; letter-spacing:1px; color:#3a3f52; margin-bottom:5px; }
.notes-area textarea { width:100%; background:#f8f9fb; border:1px solid #dde1ec; border-radius:6px; color:#1a1d26; font-size:12px; padding:8px 10px; resize:vertical; min-height:56px; font-family:inherit; line-height:1.5; }
.notes-area textarea:focus { outline:none; border-color:#2DD6FF; }
.action-row { display:flex; gap:8px; margin-bottom:10px; }
.action-row .btn { flex:1; text-align:center; }
.kbd-hint { font-size:10px; color:#2a2f42; line-height:1.6; }
/* Tooltip on crit name hover */
.crit-name[data-tip] { position:relative; }
.crit-name[data-tip]:hover::after {
  content:attr(data-tip);
  position:absolute; bottom:calc(100% + 6px); left:0;
  background:#1e2333; border:1px solid #2a2f42; color:#e4e6ed;
  font-size:10px; padding:6px 10px; border-radius:5px;
  width:280px; white-space:normal; z-index:20; pointer-events:none;
  line-height:1.5;
}
.done-screen { text-align:center; padding:80px 24px; }
.done-screen h2 { font-size:24px; color:#16F0DF; margin-bottom:10px; }
.done-screen p { color:#5a5f72; font-size:14px; margin-bottom:8px; }
.done-screen .cmd { font-family:monospace; font-size:12px; color:#8a91a2; background:#0d1018; border:1px solid #1e2333; padding:10px 20px; border-radius:6px; display:inline-block; margin-top:16px; }
</style>
</head>
<body>

<div class="header">
  <h1>skill-label</h1>
  <span class="badge" id="skillBadge"></span>
  <div class="progress-wrap">
    <div class="progress-label" id="progressLabel">0 / 0 labeled</div>
    <div class="progress-bar"><div class="progress-fill" id="progressFill" style="width:0%"></div></div>
  </div>
  <div class="nav-btns">
    <button class="btn btn-secondary" onclick="navigate(-1)">← Prev</button>
    <button class="btn btn-secondary" onclick="navigate(1)">Next →</button>
    <button class="btn btn-save-all" id="btnSaveAll" onclick="saveAll()">Save All Labels</button>
  </div>
</div>

<div class="container">
  <div class="item-nav">
    <span style="font-size:11px;color:#3a3f52;">Outputs:</span>
    <div class="item-dots" id="dotNav"></div>
  </div>

  <div id="mainContent">
    <div class="layout">
      <div class="image-card">
        <div class="image-area" id="imageArea"></div>
        <div class="image-meta">
          <div class="meta-label">Input prompt</div>
          <div class="meta-text" id="inputText"></div>
          <div class="meta-idx" id="itemIdx"></div>
        </div>
      </div>

      <div class="label-card">
        <h2>Criteria</h2>
        <div class="crit-list" id="critList"></div>
        <div class="divider"></div>
        <div class="overall-row">
          <span class="overall-label">Overall</span>
          <div style="display:flex;gap:6px;">
            <button class="radio-btn overall-pass" id="btnOverallPass" onclick="setOverall(true)">Pass</button>
            <button class="radio-btn overall-fail" id="btnOverallFail" onclick="setOverall(false)">Fail</button>
          </div>
        </div>
        <div class="notes-area">
          <label>Notes (optional)</label>
          <textarea id="notesField" placeholder="What failed? What looks wrong?"></textarea>
        </div>
        <div class="action-row">
          <button class="btn btn-secondary" onclick="skipItem()">Skip</button>
          <button class="btn btn-primary" onclick="saveAndNext()">Save &amp; Next →</button>
        </div>
        <div class="kbd-hint">← → navigate &nbsp;·&nbsp; Enter = Save &amp; Next &nbsp;·&nbsp; S = Skip</div>
      </div>
    </div>
  </div>

  <div id="doneScreen" class="done-screen" style="display:none"></div>
</div>

<script>
const DATA = __DATA_JSON__;

let currentIdx = 0;
let labels = {};

function init() {
  document.getElementById('skillBadge').textContent = DATA.skill;
  DATA.items.forEach(item => {
    const crit = {};
    DATA.criteria.forEach(c => { crit[c.name] = null; });
    labels[item.index] = { criteria: crit, overall: null, notes: '', skipped: false };
  });
  buildDotNav();
  renderItem(0);
}

function buildDotNav() {
  const container = document.getElementById('dotNav');
  DATA.items.forEach(item => {
    const dot = document.createElement('div');
    dot.className = 'dot';
    dot.id = 'dot-' + item.index;
    dot.title = 'Output ' + (item.index + 1) + ': ' + item.input.slice(0, 50);
    dot.addEventListener('click', () => { saveCurrentState(); renderItem(item.index); });
    container.appendChild(dot);
  });
}

function updateDot(idx) {
  const dot = document.getElementById('dot-' + idx);
  if (!dot) return;
  dot.classList.remove('labeled-pass', 'labeled-fail', 'labeled-skip', 'current');
  const lbl = labels[idx];
  if (lbl.skipped) dot.classList.add('labeled-skip');
  else if (lbl.overall === true) dot.classList.add('labeled-pass');
  else if (lbl.overall === false) dot.classList.add('labeled-fail');
}

function renderItem(idx) {
  currentIdx = idx;
  const item = DATA.items[idx];

  // Update dot highlights
  document.querySelectorAll('.dot').forEach(d => d.classList.remove('current'));
  const cur = document.getElementById('dot-' + idx);
  if (cur) cur.classList.add('current');

  // Image display
  const imageArea = document.getElementById('imageArea');
  imageArea.innerHTML = '';
  if (item.png_b64) {
    const img = document.createElement('img');
    img.src = 'data:image/png;base64,' + item.png_b64;
    imageArea.appendChild(img);
  } else if (item.svg_b64) {
    const svgText = atob(item.svg_b64);
    const wrap = document.createElement('div');
    wrap.className = 'svg-wrap';
    wrap.innerHTML = svgText;
    imageArea.appendChild(wrap);
  } else {
    imageArea.innerHTML = '<div class="no-image">No image available</div>';
  }

  // Meta
  document.getElementById('inputText').textContent = item.input;
  document.getElementById('itemIdx').textContent =
    'Output ' + (idx + 1) + ' of ' + DATA.items.length;

  // Criteria rows
  const critList = document.getElementById('critList');
  critList.innerHTML = '';
  const lbl = labels[idx];

  DATA.criteria.forEach(c => {
    const val = lbl.criteria[c.name];
    const row = document.createElement('div');
    row.className = 'crit-row';

    const nameEl = document.createElement('span');
    nameEl.className = 'crit-name';
    nameEl.textContent = c.name.replace(/_/g, ' ');
    if (c.description) nameEl.setAttribute('data-tip', c.description);

    const btns = document.createElement('div');
    btns.className = 'crit-btns';

    const passBtn = document.createElement('button');
    passBtn.className = 'radio-btn pass' + (val === true ? ' active' : '');
    passBtn.textContent = 'Pass';
    passBtn.addEventListener('click', () => setCrit(idx, c.name, true));

    const failBtn = document.createElement('button');
    failBtn.className = 'radio-btn fail' + (val === false ? ' active' : '');
    failBtn.textContent = 'Fail';
    failBtn.addEventListener('click', () => setCrit(idx, c.name, false));

    btns.appendChild(passBtn);
    btns.appendChild(failBtn);
    row.appendChild(nameEl);
    row.appendChild(btns);
    critList.appendChild(row);
  });

  // Overall
  document.getElementById('btnOverallPass').className =
    'radio-btn overall-pass' + (lbl.overall === true ? ' active' : '');
  document.getElementById('btnOverallFail').className =
    'radio-btn overall-fail' + (lbl.overall === false ? ' active' : '');

  // Notes
  document.getElementById('notesField').value = lbl.notes || '';

  updateProgress();
}

function saveCurrentState() {
  if (labels[currentIdx] === undefined) return;
  labels[currentIdx].notes = document.getElementById('notesField').value;
  updateDot(currentIdx);
}

function setCrit(idx, name, val) {
  labels[idx].criteria[name] = val;
  // Update button states in the list
  const rows = document.querySelectorAll('#critList .crit-row');
  rows.forEach(row => {
    const nameEl = row.querySelector('.crit-name');
    if (nameEl && nameEl.textContent.trim() === name.replace(/_/g, ' ')) {
      const btns = row.querySelectorAll('.radio-btn');
      btns[0].classList.toggle('active', val === true);
      btns[1].classList.toggle('active', val === false);
    }
  });
}

function setOverall(val) {
  labels[currentIdx].overall = val;
  document.getElementById('btnOverallPass').className =
    'radio-btn overall-pass' + (val === true ? ' active' : '');
  document.getElementById('btnOverallFail').className =
    'radio-btn overall-fail' + (val === false ? ' active' : '');
}

function skipItem() {
  saveCurrentState();
  labels[currentIdx].skipped = true;
  updateDot(currentIdx);
  updateProgress();
  if (currentIdx < DATA.items.length - 1) renderItem(currentIdx + 1);
}

function saveAndNext() {
  saveCurrentState();
  updateDot(currentIdx);
  updateProgress();
  if (currentIdx < DATA.items.length - 1) {
    renderItem(currentIdx + 1);
  } else {
    const unlabeled = DATA.items.filter(
      item => labels[item.index].overall === null && !labels[item.index].skipped
    );
    if (unlabeled.length === 0) {
      doSaveAll();
    } else {
      alert(unlabeled.length + ' output(s) still need an Overall Pass/Fail before saving.');
    }
  }
}

function navigate(dir) {
  saveCurrentState();
  updateDot(currentIdx);
  const next = Math.max(0, Math.min(DATA.items.length - 1, currentIdx + dir));
  renderItem(next);
}

function updateProgress() {
  const total = DATA.items.length;
  const done = DATA.items.filter(item => {
    const lbl = labels[item.index];
    return lbl.overall !== null || lbl.skipped;
  }).length;
  document.getElementById('progressLabel').textContent = done + ' / ' + total + ' labeled';
  document.getElementById('progressFill').style.width = Math.round(done / total * 100) + '%';
}

function saveAll() {
  saveCurrentState();
  updateDot(currentIdx);
  const unlabeled = DATA.items.filter(
    item => labels[item.index].overall === null && !labels[item.index].skipped
  );
  if (unlabeled.length > 0) {
    if (!confirm(unlabeled.length + ' output(s) not yet labeled. Save partial labels anyway?')) return;
  }
  doSaveAll();
}

function doSaveAll() {
  const payload = {
    skill: DATA.skill,
    session: DATA.session,
    outputs: DATA.items.map(item => {
      const lbl = labels[item.index];
      const human_labels = {};
      DATA.criteria.forEach(c => { human_labels[c.name] = lbl.criteria[c.name]; });
      return {
        index: item.index,
        input: item.input,
        human_labels: human_labels,
        overall_pass: lbl.overall,
        skipped: lbl.skipped || false,
        notes: lbl.notes || ''
      };
    })
  };

  document.getElementById('btnSaveAll').disabled = true;
  document.getElementById('btnSaveAll').textContent = 'Saving…';

  fetch('/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  .then(r => r.json())
  .then(result => {
    if (result.ok) {
      const labeled = payload.outputs.filter(o => !o.skipped && o.overall_pass !== null);
      const passed = labeled.filter(o => o.overall_pass).length;
      const failed = labeled.filter(o => !o.overall_pass).length;
      const skipped = payload.outputs.filter(o => o.skipped).length;
      document.getElementById('mainContent').style.display = 'none';
      document.getElementById('doneScreen').style.display = 'block';
      document.getElementById('doneScreen').innerHTML =
        '<h2>Labels saved!</h2>' +
        '<p>' + labeled.length + ' labeled · ' + passed + ' pass · ' + failed + ' fail · ' + skipped + ' skipped</p>' +
        '<p style="margin-top:8px;color:#4a4f62;">Use with autoresearch:</p>' +
        '<div class="cmd">python3 skill_autoresearch.py ' + DATA.skill + ' --use-labels --cycles 20</div>' +
        '<p style="margin-top:20px;font-size:11px;color:#2a2f42;">' + result.path + '</p>';
    } else {
      alert('Save failed: ' + result.error);
      document.getElementById('btnSaveAll').disabled = false;
      document.getElementById('btnSaveAll').textContent = 'Save All Labels';
    }
  })
  .catch(e => {
    alert('Save error: ' + e.message);
    document.getElementById('btnSaveAll').disabled = false;
    document.getElementById('btnSaveAll').textContent = 'Save All Labels';
  });
}

// Keyboard shortcuts
document.addEventListener('keydown', e => {
  if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') return;
  if (e.key === 'ArrowRight') navigate(1);
  else if (e.key === 'ArrowLeft') navigate(-1);
  else if (e.key === 'Enter') saveAndNext();
  else if (e.key === 's' || e.key === 'S') skipItem();
});

init();
</script>
</body>
</html>
"""


# ─── Helpers ──────────────────────────────────────────────────────────────────


def find_skill_dir(skill_name: str) -> Path:
    skill_dir = SKILLS_DIR / skill_name
    if not skill_dir.exists() or not (skill_dir / "SKILL.md").exists():
        print(f"ERROR: Skill '{skill_name}' not found at {skill_dir}", file=sys.stderr)
        available = [d.name for d in sorted(SKILLS_DIR.iterdir())
                     if d.is_dir() and (d / "SKILL.md").exists()]
        print("Available:", ", ".join(available[:10]), file=sys.stderr)
        sys.exit(1)
    return skill_dir


def load_config(skill_dir: Path) -> dict:
    config_path = skill_dir / "autoresearch" / "config.yaml"
    if not config_path.exists():
        print(f"ERROR: No autoresearch/config.yaml in {skill_dir}", file=sys.stderr)
        sys.exit(1)
    return yaml.safe_load(config_path.read_text())


def split_frontmatter(text: str) -> str:
    """Strip YAML frontmatter, return body."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text


# ─── Execute ──────────────────────────────────────────────────────────────────


def execute_one(client, system_prompt: str, test_input: str, max_tokens: int) -> str | None:
    try:
        resp = client.messages.create(
            model=EXECUTE_MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": test_input}],
        )
        return resp.content[0].text.strip()
    except Exception as e:
        print(f"  EXEC ERROR: {e}")
        return None


def generate_outputs(skill_dir: Path, config: dict, batch_size: int) -> list[dict]:
    if not ANTHROPIC_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    skill_body = split_frontmatter((skill_dir / "SKILL.md").read_text())
    all_inputs = config["test_inputs"]
    test_inputs = random.sample(all_inputs, min(batch_size, len(all_inputs)))
    max_tokens = config.get("max_tokens", 4096)

    print(f"Generating {len(test_inputs)} outputs ({EXECUTE_MODEL})...")
    results = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {
            pool.submit(execute_one, client, skill_body, inp, max_tokens): inp
            for inp in test_inputs
        }
        for f in as_completed(futures):
            inp = futures[f]
            out = f.result()
            if out:
                results.append({"input": inp, "output": out})
                print(f"  ✓ {inp[:70]}")
            else:
                print(f"  ✗ FAILED: {inp[:70]}")
    return results


def load_from_run(skill_dir: Path, run_num: int) -> list[dict]:
    run_dir = skill_dir / "autoresearch" / "outputs" / f"run_{run_num:03d}"
    records_file = run_dir / "records.json"
    if not records_file.exists():
        print(f"ERROR: Run {run_num:03d} not found at {run_dir}", file=sys.stderr)
        sys.exit(1)
    records = json.loads(records_file.read_text())
    results = []
    for rec in records:
        out_file = run_dir / rec["output_file"]
        results.append({
            "input": rec["input"],
            "output": out_file.read_text() if out_file.exists() else "",
        })
    print(f"Loaded {len(results)} outputs from run_{run_num:03d}")
    return results


# ─── P Palette substitution (JSX → valid SVG colors) ─────────────────────────

_P = {
    "layer1": "#0f2214", "layer2": "#1a3a1e", "layer3": "#2d5c35",
    "layer4": "#3d7a46", "layer5": "#56a462", "layer6": "#78c484", "layer7": "#a8d8b0",
    "amber": "#c8861a", "amberM": "#d4952a", "amberL": "#e8b84c", "amberHL": "#f5d070",
    "rust": "#8c3a18", "rustM": "#b04820", "rustL": "#d06030",
    "cream": "#e8dbb0", "creamL": "#f2e8c8",
    "kTan": "#c89030", "kTanL": "#e8b050", "kBlk": "#1a0e08", "kBlkM": "#2a1808",
    "kPnk": "#e8a898", "kPnkD": "#c87868", "kRust": "#d47018", "kRustL": "#e8882a",
    "kWht": "#f0ece0", "kWhtS": "#d4ccc0",
    "gGold": "#c8a030", "gGoldL": "#e0be58", "gCream": "#f0e0a0",
    "tWheat": "#c8a840", "tDkWht": "#a07820", "tPale": "#e8d890",
    "sky": "#1a2a3a", "skyM": "#2a4060", "cloud": "#8aacb8",
}
_S = {
    "s1": "drop-shadow(0 1px 2px rgba(0,0,0,0.18))",
    "s2": "drop-shadow(0 2px 5px rgba(0,0,0,0.28))",
    "s3": "drop-shadow(0 3px 8px rgba(0,0,0,0.38))",
    "s4": "drop-shadow(0 5px 12px rgba(0,0,0,0.48))",
    "s5": "drop-shadow(0 7px 16px rgba(0,0,0,0.55))",
}

def resolve_jsx_svg(text: str) -> str:
    """Extract SVG from JSX output and replace P/s palette references with real values."""
    import re

    # 1. Parse local P object from the code (keys → hex values)
    p_local = dict(_P)  # start with defaults
    for km in re.finditer(r'(\w+)\s*:\s*"(#[0-9a-fA-F]{3,8})"', text):
        p_local[km.group(1)] = km.group(2)

    # 2. Parse local s1-s5 constants
    s_local = dict(_S)
    for sm in re.finditer(r'const\s+(s[1-5])\s*=\s*"([^"]+)"', text):
        s_local[sm.group(1)] = sm.group(2)

    # 3. Extract SVG block — handle truncated outputs (no closing </svg>)
    m = re.search(r'(<svg[\s\S]*?</svg>)', text, re.IGNORECASE)
    if m:
        svg = m.group(1)
    else:
        # Truncated — grab from <svg to end and close open tags
        start = text.lower().find('<svg')
        if start == -1:
            return text
        svg = text[start:]
        # Close any unclosed <g> tags
        open_g = svg.count('<g') - svg.count('</g>') - svg.count('/>')
        svg += ('</g>' * max(0, open_g)) + '</svg>'

    # 4. Remove JSX comments {/* ... */}
    svg = re.sub(r'\{/\*[\s\S]*?\*/\}', '', svg)

    # 5. Remove <style>{`...`}</style> template literals (not valid SVG)
    svg = re.sub(r'<style>\{`[\s\S]*?`\}</style>', '', svg)

    # 6. Replace {P.key} → hex color
    def sub_p(m2):
        key = m2.group(1)
        return p_local.get(key, '#888888')
    svg = re.sub(r'\{P\.(\w+)\}', sub_p, svg)

    # 7. Replace filter={sN} → style="filter: ..."
    def sub_filter_attr(m2):
        key = m2.group(1)
        val = s_local.get(key, 'none')
        return f'style="filter: {val}"'
    svg = re.sub(r'filter=\{(s[1-5])\}', sub_filter_attr, svg)

    # 8. Replace style={{filter: sN}} → style="filter: ..."
    def sub_style(m2):
        inner = m2.group(1)
        fm = re.search(r'filter:\s*(s[1-5])', inner)
        if fm:
            val = s_local.get(fm.group(1), 'none')
            return f'style="filter: {val}"'
        return f'style="{inner}"'
    svg = re.sub(r'style=\{\{([^}]+)\}\}', sub_style, svg)

    # 9. Replace stopColor={P.key} → stopColor="hex"
    def sub_stop(m2):
        key = m2.group(1)
        return f'stopColor="{p_local.get(key, "#888888")}"'
    svg = re.sub(r'stopColor=\{P\.(\w+)\}', sub_stop, svg)

    # 10. Remove any remaining {expr} JSX expressions
    svg = re.sub(r'\{[^{}]{0,120}\}', '', svg)

    # 11. Fix JSX attribute names → SVG/HTML valid
    svg = svg.replace('className=', 'class=')
    svg = svg.replace('strokeWidth=', 'stroke-width=')
    svg = svg.replace('strokeLinecap=', 'stroke-linecap=')
    svg = svg.replace('strokeLinejoin=', 'stroke-linejoin=')
    svg = svg.replace('strokeDasharray=', 'stroke-dasharray=')
    svg = svg.replace('fillOpacity=', 'fill-opacity=')

    return svg


# ─── Render ───────────────────────────────────────────────────────────────────


def svg_to_png_b64(svg_text: str, width: int = 900) -> str | None:
    """Render SVG → PNG → base64. Returns None if cairosvg not available."""
    try:
        import cairosvg
        png_bytes = cairosvg.svg2png(bytestring=svg_text.encode(), output_width=width)
        return base64.b64encode(png_bytes).decode()
    except ImportError:
        return None
    except Exception as e:
        print(f"  RENDER WARN: {e}")
        return None


def prepare_items(raw_outputs: list[dict]) -> list[dict]:
    """Prepare items with image data (PNG base64 preferred, SVG inline fallback)."""
    items = []
    cairosvg_available = True

    for i, rec in enumerate(raw_outputs):
        out = rec["output"]
        is_svg = "<svg" in out[:1000].lower()
        png_b64 = None
        svg_b64 = None

        if is_svg:
            out_resolved = resolve_jsx_svg(out)
            suffix = f"({i + 1}/{len(raw_outputs)})"
            if cairosvg_available:
                png_b64 = svg_to_png_b64(out_resolved)
                if png_b64:
                    print(f"  Rendered PNG {suffix}")
                else:
                    cairosvg_available = False
                    print(f"  cairosvg unavailable — using SVG inline {suffix}")
            else:
                print(f"  SVG inline {suffix}")
            # Always encode resolved SVG as fallback
            svg_b64 = base64.b64encode(out_resolved.encode()).decode()

        items.append({
            "index": i,
            "input": rec["input"],
            "is_svg": is_svg,
            "png_b64": png_b64,
            "svg_b64": svg_b64,
        })

    if not cairosvg_available and any(item["is_svg"] for item in items):
        print("\n  TIP: Install cairosvg for PNG rendering: pip install cairosvg")

    return items


# ─── HTML Builder ─────────────────────────────────────────────────────────────


def build_html(skill_name: str, criteria: list[dict], items: list[dict], session_name: str) -> str:
    """Build the labeling page with all image data embedded."""
    js_items = [
        {
            "index": item["index"],
            "input": item["input"],
            "is_svg": item["is_svg"],
            "png_b64": item.get("png_b64"),
            "svg_b64": item.get("svg_b64"),
        }
        for item in items
    ]
    criteria_for_js = [
        {"name": c["name"], "description": c.get("description", "").strip()}
        for c in criteria
    ]
    data = {
        "skill": skill_name,
        "session": session_name,
        "criteria": criteria_for_js,
        "items": js_items,
    }
    return _HTML.replace("__DATA_JSON__", json.dumps(data))


# ─── HTTP Server ──────────────────────────────────────────────────────────────


class _LabelServer:
    def __init__(self, html: str, labels_dir: Path, session_name: str):
        self._html = html.encode("utf-8")
        self.labels_dir = labels_dir
        self.session_name = session_name
        self.done = threading.Event()
        self.saved_path: Path | None = None

    def make_handler(self):
        parent = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path in ("/", "/index.html"):
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(parent._html)))
                    self.end_headers()
                    self.wfile.write(parent._html)
                else:
                    self.send_response(404)
                    self.end_headers()

            def do_POST(self):
                if self.path == "/save":
                    length = int(self.headers.get("Content-Length", 0))
                    body = self.rfile.read(length)
                    try:
                        payload = json.loads(body)
                        parent.labels_dir.mkdir(parents=True, exist_ok=True)
                        out_path = parent.labels_dir / f"{parent.session_name}.json"
                        out_path.write_text(json.dumps(payload, indent=2))
                        parent.saved_path = out_path
                        resp = json.dumps({"ok": True, "path": str(out_path)}).encode()
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(resp)))
                        self.end_headers()
                        self.wfile.write(resp)
                        threading.Timer(1.5, parent.done.set).start()
                    except Exception as e:
                        resp = json.dumps({"ok": False, "error": str(e)}).encode()
                        self.send_response(500)
                        self.send_header("Content-Type", "application/json")
                        self.send_header("Content-Length", str(len(resp)))
                        self.end_headers()
                        self.wfile.write(resp)
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, fmt, *args):
                pass  # suppress request logs

        return Handler


def _free_port() -> int:
    s = socket.socket()
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def serve_and_label(
    skill_dir: Path, items: list[dict], config: dict, session_name: str
) -> Path | None:
    labels_dir = skill_dir / "autoresearch" / "labels"
    criteria = config["eval_criteria"]

    print(f"\nBuilding labeling UI ({len(items)} outputs × {len(criteria)} criteria)...")
    html = build_html(skill_dir.name, criteria, items, session_name)

    server_state = _LabelServer(html, labels_dir, session_name)
    port = _free_port()
    httpd = HTTPServer(("localhost", port), server_state.make_handler())

    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    url = f"http://localhost:{port}"
    print(f"\nLabeling UI ready: {url}")
    print(f"  Label each output, then click 'Save All Labels' when done.")
    print(f"  Press Ctrl+C to abort without saving.\n")

    subprocess.run(["open", url], capture_output=True)

    try:
        server_state.done.wait()
    except KeyboardInterrupt:
        print("\nAborted — no labels saved.")
        httpd.shutdown()
        return None

    httpd.shutdown()
    return server_state.saved_path


# ─── Review Mode ──────────────────────────────────────────────────────────────


def show_review(skill_dir: Path):
    labels_dir = skill_dir / "autoresearch" / "labels"
    if not labels_dir.exists():
        print(f"No labels found for '{skill_dir.name}' — run without --review to create some.")
        return

    sessions = sorted(labels_dir.glob("session_*.json"))
    if not sessions:
        print(f"No sessions in {labels_dir}")
        return

    print(f"\nLabel sessions for '{skill_dir.name}':")
    print(f"  {'Session':<26} {'Outputs':>8} {'Labeled':>8} {'Pass':>6} {'Fail':>6} {'Skip':>6}")
    print("  " + "-" * 62)

    for path in sessions:
        try:
            data = json.loads(path.read_text())
            outputs = data.get("outputs", [])
            labeled = [o for o in outputs if o.get("overall_pass") is not None and not o.get("skipped")]
            passed = sum(1 for o in labeled if o.get("overall_pass"))
            failed = sum(1 for o in labeled if not o.get("overall_pass"))
            skipped = sum(1 for o in outputs if o.get("skipped"))
            print(f"  {path.stem:<26} {len(outputs):>8} {len(labeled):>8} {passed:>6} {failed:>6} {skipped:>6}")
        except Exception:
            print(f"  {path.stem:<26}  (error reading)")

    print(f"\n  Use with autoresearch:")
    print(f"  python3 .claude/skills/skill-autoresearch/skill_autoresearch.py {skill_dir.name} --use-labels")


# ─── Main ─────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="Human labeling tool for skill autoresearch"
    )
    parser.add_argument("skill", help="Skill directory name in .claude/skills/")
    parser.add_argument("--batch", type=int, default=10,
                        help="Number of outputs to generate (default: 10)")
    parser.add_argument("--from-run", type=int, metavar="N", dest="from_run",
                        help="Label outputs from autoresearch run N")
    parser.add_argument("--review", action="store_true",
                        help="List saved label sessions and their stats")
    args = parser.parse_args()

    skill_dir = find_skill_dir(args.skill)

    if args.review:
        show_review(skill_dir)
        return

    config = load_config(skill_dir)

    # Load or generate outputs
    if args.from_run is not None:
        raw_outputs = load_from_run(skill_dir, args.from_run)
    else:
        raw_outputs = generate_outputs(skill_dir, config, args.batch)

    if not raw_outputs:
        print("ERROR: No outputs generated. Check your ANTHROPIC_API_KEY.")
        sys.exit(1)

    # Render images
    print(f"\nPreparing {len(raw_outputs)} outputs for display...")
    items = prepare_items(raw_outputs)

    session_name = f"session_{datetime.now().strftime('%Y%m%dT%H%M%S')}"
    saved_path = serve_and_label(skill_dir, items, config, session_name)

    if saved_path:
        print(f"\n✓ Labels saved: {saved_path}")
        print(f"\nRun autoresearch with human ground truth:")
        print(f"  python3 .claude/skills/skill-autoresearch/skill_autoresearch.py {args.skill} --use-labels --cycles 20")
    else:
        print("No labels saved.")


if __name__ == "__main__":
    main()
