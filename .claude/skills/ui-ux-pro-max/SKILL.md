---
name: ui-ux-pro-max
description: "UI/UX design intelligence. 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui)..---

# UI/UX Pro Max — Design Intelligence

## When to Apply This Skill

Apply this skill when the user asks to:
- Design, build, create, implement, or review any UI component or page
- Choose color palettes, typography, or visual style
- Fix UX problems or improve accessibility
- Build landing pages, dashboards, admin panels, SaaS apps, portfolios, e-commerce, or mobile apps

---

## Style Selection Decision Tree

Run this decision tree before writing any code.

**Step 1 — What is the product type?**

| Product type | Recommended style |
|---|---|
| SaaS / B2B dashboard | Minimalism, Flat Design, Dark Mode |
| E-commerce / consumer | Flat Design, Skeuomorphism, Claymorphism |
| Healthcare / finance | Minimalism, Flat Design (clean, trust-focused) |
| Gaming / entertainment | Glassmorphism, Dark Mode, Brutalism |
| Beauty / wellness / spa | Glassmorphism, Soft Minimalism, Skeuomorphism |
| Portfolio / creative | Brutalism, Bento Grid, Glassmorphism |
| Startup / landing page | Bento Grid, Glassmorphism, Neumorphism |
| Mobile app | Neumorphism, Claymorphism, Flat Design |

**Step 2 — What style keywords did the user mention?**

| Keyword | Style |
|---|---|
| minimal, clean, simple | Minimalism |
| playful, fun, soft | Claymorphism |
| dark, moody, neon | Dark Mode + Glassmorphism |
| bold, raw, editorial | Brutalism |
| elegant, luxury | Glassmorphism or Soft Skeuomorphism |
| data-heavy, dense | Flat Design, Bento Grid |

**Step 3 — If still ambiguous**, run the design system command (Step 2 below) and let the reasoning engine decide.

---

## Quick-Start Path (90% of tasks)

Do these four steps in order. Do not skip Step 2.

### Step 1 — Extract requirements from the user request

Identify:
- **Product type**: SaaS, e-commerce, portfolio, dashboard, landing page, etc.
- **Style keywords**: minimal, playful, professional, elegant, dark mode, etc.
- **Industry**: healthcare, fintech, gaming, education, beauty, etc.
- **Stack**: React, Vue, Next.js, or default to `html-tailwind` if unspecified

### Step 2 — Generate the design system (REQUIRED, always run this first)

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system [-p "Project Name"]
```

This searches 5 domains in parallel (product, style, color, landing, typography), applies reasoning rules from `ui-reasoning.csv`, and returns a complete design system: pattern, style, colors, typography, effects, and anti-patterns to avoid.

Example:
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "beauty spa wellness service elegant" --design-system -p "Serenity Spa"
```

Output format options:
```bash
# ASCII box (default — best for terminal)
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system

# Markdown (best for documentation)
python3 skills/ui-ux-pro-max/scripts/search.py "fintech crypto" --design-system -f markdown
```

### Step 3 — Supplement with domain searches (only when needed)

Use these after the design system to get additional detail:

| Need | Command |
|---|---|
| More style options | `python3 skills/ui-ux-pro-max/scripts/search.py "glassmorphism dark" --domain style` |
| Chart recommendations | `python3 skills/ui-ux-pro-max/scripts/search.py "real-time dashboard" --domain chart` |
| UX best practices | `python3 skills/ui-ux-pro-max/scripts/search.py "animation accessibility" --domain ux` |
| Alternative fonts | `python3 skills/ui-ux-pro-max/scripts/search.py "elegant luxury" --domain typography` |
| Landing structure | `python3 skills/ui-ux-pro-max/scripts/search.py "hero social-proof" --domain landing` |

### Step 4 — Get stack-specific guidelines

Default to `html-tailwind` if the user did not specify a stack.

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack html-tailwind
```

Available stacks: `html-tailwind`, `react`, `nextjs`, `vue`, `svelte`, `swiftui`, `react-native`, `flutter`, `shadcn`, `jetpack-compose`

---

## Persisting the Design System Across Sessions

Add `--persist` to save the design system for hierarchical retrieval:

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

This creates:
- `design-system/MASTER.md` — global source of truth
- `design-system/pages/` — folder for page-specific overrides

Add a page-specific override:
```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

**Retrieval rule:** When building a specific page, check `design-system/pages/<page-name>.md` first. If it exists, its rules override the Master. If not, use `MASTER.md` exclusively.

Retrieval prompt:
```
I am building the [Page Name] page. Please read design-system/MASTER.md.
Also check if design-system/pages/[page-name].md exists.
If the page file exists, prioritize its rules.
If not, use the Master rules exclusively.
Now, generate the code...
```

---

## Prerequisites

Verify Python is installed before running any scripts:

```bash
python3 --version || python --version
```

Install if missing:

**macOS:** `brew install python3`
**Ubuntu/Debian:** `sudo apt update && sudo apt install python3`
**Windows:** `winget install Python.Python.3.12`

---

## Available Domains

| Domain | Use for | Example keywords |
|---|---|---|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel, pie |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `react` | React/Next.js performance | waterfall, bundle, suspense, memo, rerender |
| `web` | Web interface guidelines | aria, focus, keyboard, semantic, virtualize |
| `prompt` | AI prompts, CSS keywords | (style name) |

---

## Rules by Priority

Apply these in order. Do not skip Priority 1–2.

### Priority 1 — Accessibility (CRITICAL)

- Minimum 4.5:1 contrast ratio for normal text
- Visible focus rings on all interactive elements
- Descriptive alt text on all meaningful images
- `aria-label` on icon-only buttons
- Tab order matches visual order
- `<label for>` on all form inputs

### Priority 2 — Touch & Interaction (CRITICAL)

- Minimum 44×44px touch targets
- Use click/tap (not hover) for primary interactions
- Disable buttons during async operations
- Show clear error messages near the problem field
- Add `cursor-pointer` to all clickable elements

### Priority 3 — Performance (HIGH)

- Use WebP, `srcset`, and `loading="lazy"` on images
- Respect `prefers-reduced-motion`
- Reserve space for async content to prevent layout shift

### Priority 4 — Layout & Responsive (HIGH)

- Set `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Minimum 16px body text on mobile
- Ensure no horizontal scroll at any viewport width
- Define a z-index scale (10, 20, 30, 50) — do not use arbitrary values

### Priority 5 — Typography & Color (MEDIUM)

- Line height 1.5–1.75 for body text
- 65–75 characters maximum line length
- Match heading and body font personalities

### Priority 6 — Animation (MEDIUM)

- 150–300ms for micro-interactions
- Animate `transform` and `opacity` only — not `width`/`height`
- Use skeleton screens or spinners for loading states

### Priority 7 — Style Consistency (MEDIUM)

- Match style to product type (use decision tree above)
- Use the same style across all pages
- Use SVG icons (Heroicons, Lucide) — never emoji as UI icons

### Priority 8 — Charts & Data (LOW)

- Match chart type to data type
- Use accessible color palettes
- Provide a table alternative for accessibility

---

## Common Professional UI Rules

### Icons & Visual Elements

| Rule | Do | Do not |
|---|---|---|
| No emoji icons | Use SVG icons (Heroicons, Lucide, Simple Icons) | Use emojis like 🎨 🚀 as UI icons |
| Stable hover states | Use color/opacity transitions | Use scale transforms that shift layout |
| Correct brand logos | Research official SVG from Simple Icons | Guess or use incorrect logo paths |
| Consistent icon sizing | Use fixed viewBox (24×24) with `w-6 h-6` | Mix different icon sizes randomly |

### Interaction & Cursor

| Rule | Do | Do not |
|---|---|---|
| Cursor pointer | Add `cursor-pointer` to all clickable/hoverable elements | Leave default cursor on interactive elements |
| Hover feedback | Provide visual feedback (color, shadow, border) | Give no indication an element is interactive |
| Smooth transitions | Use `transition-colors duration-200` | Use instant state changes or >500ms transitions |

### Light/Dark Mode Contrast

| Rule | Do | Do not |
|---|---|---|
| Glass card light mode | Use `bg-white/80` or higher opacity | Use `bg-white/10` (too transparent) |
| Text contrast light | Use `#0F172A` (slate-900) for body text | Use `#94A3B8` (slate-400) for body text |
| Muted text light | Use `#475569` (slate-600) minimum | Use gray-400 or lighter |
| Border visibility | Use `border-gray-200` in light mode | Use `border-white/10` (invisible) |

### Layout & Spacing

| Rule | Do | Do not |
|---|---|---|
| Floating navbar | Add `top-4 left-4 right-4` spacing | Stick navbar to `top-0 left-0 right-0` |
| Content padding | Account for fixed navbar height | Let content hide behind fixed elements |
| Consistent max-width | Use same `max-w-6xl` or `max-w-7xl` | Mix different container widths |

---

## Pre-Delivery Checklist

Run this before delivering any UI code.

**Visual Quality**
- [ ] No emojis used as icons (SVG only)
- [ ] All icons from consistent icon set (Heroicons or Lucide)
- [ ] Brand logos verified from Simple Icons
- [ ] Hover states do not cause layout shift
- [ ] Theme colors used directly (`bg-primary`) not via `var()` wrapper

**Interaction**
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover states provide clear visual feedback
- [ ] Transitions are 150–300ms
- [ ] Focus states visible for keyboard navigation

**Light/Dark Mode**
- [ ] Light mode text has 4.5:1 minimum contrast
- [ ] Glass/transparent elements visible in light mode
- [ ] Borders visible in both modes
- [ ] Both modes tested before delivery

**Layout**
- [ ] Floating elements have proper edge spacing
- [ ] No content hidden behind fixed navbars
- [ ] Responsive at 375px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile

**Accessibility**
- [ ] All images have alt text
- [ ] All form inputs have labels
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
