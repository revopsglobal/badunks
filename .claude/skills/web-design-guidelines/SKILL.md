---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance.
metadata:
  author: vercel
  version: "2.0.0"
  argument-hint: <file-or-pattern>
---

# Web Interface Guidelines

Review UI code for compliance with web interface best practices. All rules are embedded below — no external fetch required.

## Trigger

When given a file or pattern, run the full audit. When given no files, ask which files to review.

Output format: `file:line — [category] violation: description. Fix: remedy.`

---

## Quick Audit (Check These First)

The 10 most critical things to verify before anything else:

1. **Touch targets** — All interactive elements (buttons, links, inputs) are at least 44x44px
2. **Color contrast** — Text on background meets 4.5:1 minimum (3:1 for large text ≥18px or bold ≥14px)
3. **Line height** — Body text has `line-height` of at least 1.5
4. **Font size** — Base font size is at least 16px; nothing below 12px anywhere
5. **Focus indicators** — All interactive elements have a visible `:focus` or `:focus-visible` style (not `outline: none` without replacement)
6. **Alt text** — Every `<img>` has a meaningful `alt` attribute (empty `alt=""` is correct only for decorative images)
7. **Heading hierarchy** — One `<h1>` per page; headings do not skip levels (h1 → h2 → h3)
8. **Max content width** — Body text columns are capped at 60–80 characters (roughly 640–800px wide)
9. **Tap/click feedback** — Buttons and links have a visible hover/active state change
10. **Form labels** — Every input has an associated `<label>` (not just placeholder text)

---

## Full Review Checklist

### Layout

- Page has a single `<main>` landmark; content is not dumped directly into `<body>`
- Maximum content width is constrained (e.g., `max-width: 1280px` or narrower for reading columns)
- Text columns for reading are 60–80 characters wide (`max-width: ~65ch`)
- Layout uses CSS Grid or Flexbox; no layout done with `float` or `position: absolute` for flow
- No horizontal overflow on mobile (`overflow-x: hidden` on `<body>` is a red flag — fix the cause, not the symptom)
- Content reflows correctly at 320px viewport width without loss of functionality
- Sticky/fixed elements do not cover more than 20% of the viewport height on mobile

### Typography

- Base font size is `16px` or larger (do not set `font-size` below `1rem` on `<html>` or `<body>`)
- No text set below `12px` (`0.75rem`) anywhere, including labels and captions
- Body text `line-height` is at least `1.5` (e.g., `line-height: 1.5` or `line-height: 24px` for 16px text)
- Heading `line-height` is at least `1.2`
- Letter spacing on body text is not set to a negative value
- Font stacks include a system fallback (e.g., `font-family: 'Inter', system-ui, sans-serif`)
- No more than 2 typeface families on a single page (decorative excluded)
- Text is left-aligned for body copy (justified text is not used without `hyphens: auto`)
- Paragraph spacing (`margin-bottom`) is at least `1em`

### Color

- Normal text (< 18px / non-bold) has at least 4.5:1 contrast ratio against its background
- Large text (≥ 18px or bold ≥ 14px) has at least 3:1 contrast ratio
- UI components and focus indicators have at least 3:1 contrast against adjacent colors
- Color is never the sole means of conveying information (e.g., error state uses icon or text, not just red)
- Links are distinguishable from surrounding text by more than color alone (underline or weight difference)
- Dark mode (if present) re-specifies all hardcoded color values; no `#000` or `#fff` absolute values in shared components

### Accessibility

- All `<img>` elements have an `alt` attribute; decorative images use `alt=""`
- All form inputs have an associated `<label>` element (via `for`/`id` or wrapping)
- `placeholder` is not used as a substitute for a visible label
- Interactive elements are native HTML (`<button>`, `<a href>`, `<input>`) or have `role`, `tabindex`, and keyboard handlers
- Focus order follows visual reading order; no `tabindex` values above `0`
- All interactive elements are reachable and operable by keyboard alone
- Focus is never trapped (modals manage focus correctly — trap while open, restore on close)
- Visible `:focus` or `:focus-visible` style exists for all interactive elements; `outline: none` without a replacement is a violation
- `aria-label` or `aria-labelledby` present on icon-only buttons
- `<html lang="...">` is set
- Page `<title>` is descriptive and unique per page
- Error messages are associated with their input via `aria-describedby`

### Spacing

- Touch targets (buttons, links, inputs) are at least `44px` tall and `44px` wide
- Spacing between interactive elements is at least `8px` to prevent accidental taps
- Content padding on mobile is at least `16px` on left and right edges
- Section spacing is proportional — closer elements share more visual relationship
- Consistent spacing scale used throughout (e.g., 4px base unit: 4, 8, 12, 16, 24, 32, 48, 64px)

### Motion & Animation

- Animations respect `prefers-reduced-motion`: wrap non-essential animations in `@media (prefers-reduced-motion: no-preference)`
- Auto-playing animations can be paused or stopped by the user
- Transitions are under 500ms for UI state changes (hover, focus); page transitions under 1000ms

### Images & Media

- Images that convey content have descriptive `alt` text (not filename or "image of")
- `<img>` elements have explicit `width` and `height` attributes to prevent layout shift (CLS)
- Images are served in modern formats (WebP/AVIF) with fallbacks where possible
- No image is used to convey text that could be HTML text

### Forms

- Required fields are marked with both a visual indicator and `required` attribute
- Error messages appear adjacent to the relevant field, not only at the top of the form
- Success state is communicated to screen readers via `aria-live` or focus management
- Autocomplete attributes are set on common fields (`autocomplete="email"`, `autocomplete="name"`, etc.)
- Submit buttons are `<button type="submit">` or `<input type="submit">`, not `<div>` or `<span>`

---

## Common Violations and Fixes

| Violation | Fix |
|-----------|-----|
| `outline: none` with no replacement focus style | Add `outline: 2px solid currentColor; outline-offset: 2px` on `:focus-visible` |
| `<div onClick>` used for interactive element | Replace with `<button>` or `<a>` with appropriate attributes |
| Placeholder as label | Add a `<label>` element; keep placeholder as hint only |
| `font-size: 14px` on body | Set `font-size: 16px` minimum; use `14px` only for supplementary text like captions |
| `line-height: 1` or `1.2` on body | Set `line-height: 1.5` or `1.6` for body copy |
| Low-contrast grey text | Use a contrast checker; ensure 4.5:1 minimum; darken text or lighten background |
| Missing `alt` on `<img>` | Add `alt="descriptive text"` or `alt=""` for decorative images |
| Touch target `height: 32px` on mobile | Set `min-height: 44px; min-width: 44px` |
| `max-width` not set on text column | Add `max-width: 65ch` or equivalent to reading containers |
| Heading skips level (h1 → h3) | Add the missing heading level or reclassify with `class` and `aria-level` |
| Color-only error state | Add error icon or text message alongside the color change |
| `<html>` missing `lang` attribute | Add `<html lang="en">` (or appropriate language code) |
| No `width`/`height` on `<img>` | Add `width` and `height` attributes matching the image's intrinsic dimensions |
| Autoplaying animation with no pause | Wrap in `prefers-reduced-motion` or add a pause control |

---

## Pass / Fail Criteria

**Fail immediately (must fix before shipping):**
- Any text with contrast ratio below 3:1
- Interactive element unreachable by keyboard
- Form input with no label (placeholder-only)
- Missing `alt` on content images
- Focus indicator removed with no replacement
- Touch targets below 44px on mobile views
- `<html>` missing `lang`

**Warn (should fix, not blocking):**
- Line height below 1.5 on body text
- Font size below 16px on body
- Heading hierarchy skipped
- Max content width unconstrained (text wider than 80ch)
- Spacing between interactive elements below 8px
- No `prefers-reduced-motion` handling on animations
- Missing `width`/`height` on images

---

## Supplementary Reference

For the full Vercel Web Interface Guidelines source:
```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use this only to check edge cases not covered above. The embedded rules above are the primary source for audits.

---

## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
