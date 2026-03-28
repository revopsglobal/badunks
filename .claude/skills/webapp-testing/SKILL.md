---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

Write native Python Playwright scripts to test or interact with local web applications.

**Helper scripts available** — run any script with `--help` before writing custom code:
- `scripts/with_server.py` — manages server lifecycle (single or multiple servers)

Run `--help` first. Only read the script source if `--help` output is insufficient and a custom solution is truly necessary. These scripts are large and will pollute the context window — treat them as callable tools, not code to study.

---

## Decision Tree

Use this to pick the right approach before writing any code.

```
What is the target app?
│
├─ Static HTML file (no JS framework, no build step)
│   └─ Read the HTML file directly → identify selectors → write Playwright using file:// URL
│       └─ If selectors are ambiguous or page behavior is dynamic after all:
│           └─ Treat as dynamic (see below)
│
├─ Dynamic webapp, server NOT running
│   └─ Use with_server.py to manage startup
│       └─ Run: python scripts/with_server.py --help
│       └─ Then: write a Playwright script that assumes the server is ready (see template below)
│
└─ Dynamic webapp, server already running
    └─ Use Reconnaissance-Then-Action pattern (see below)
        1. Navigate and wait for networkidle
        2. Screenshot or inspect DOM
        3. Identify selectors from rendered state
        4. Execute actions with discovered selectors
```

### When to use which Playwright approach

| Situation | Approach |
|---|---|
| Verify a static HTML file renders correctly | `file://` URL, read HTML first for selectors |
| Test a React/Vue/Svelte app locally | `with_server.py` + Playwright script |
| Debug a UI bug in a running dev server | Reconnaissance-Then-Action |
| Capture a screenshot for QA | Navigate → `networkidle` → `screenshot()` |
| Capture browser console logs | Use `examples/console_logging.py` as a starting point |
| Discover what elements exist on a page | Use `examples/element_discovery.py` as a starting point |

---

## Templates

### With server management (with_server.py)

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_script.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_script.py
```

**Playwright script template** (server already handled by with_server.py):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')  # CRITICAL: wait for JS to finish
    # ... automation logic here
    browser.close()
```

### Reconnaissance-Then-Action

Use this when you don't know the selectors yet or the page state is unknown.

```python
# Step 1: Inspect
page.goto('http://localhost:5173')
page.wait_for_load_state('networkidle')
page.screenshot(path='/tmp/inspect.png', full_page=True)
content = page.content()
buttons = page.locator('button').all()

# Step 2: Identify selectors from the output above

# Step 3: Act
page.locator('text=Submit').click()
page.wait_for_selector('#confirmation')
```

---

## Rules

- Always launch Chromium in headless mode: `p.chromium.launch(headless=True)`
- Always wait for `networkidle` before inspecting DOM on dynamic apps — not before
- Always close the browser when done
- Prefer descriptive selectors in this order: `role=`, `text=`, CSS selectors, IDs
- Add explicit waits (`wait_for_selector`, `wait_for_load_state`) rather than `wait_for_timeout`

---

## Reference Files

Use these as starting points — copy and adapt rather than writing from scratch:

- `examples/element_discovery.py` — discover buttons, links, and inputs on a page
- `examples/static_html_automation.py` — file:// URL pattern for local HTML
- `examples/console_logging.py` — capture browser console output during automation

---

## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
