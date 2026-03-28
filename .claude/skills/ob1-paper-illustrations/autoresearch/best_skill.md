---
name: ob1-paper-illustrations
description: >
  Create paper cut-out SVG illustrations for ob1-app in the established 5-7 layer depth system.
  Use when adding a new section hero illustration, updating an existing one, or extending
  Illustrations.tsx. Covers the P palette, shadow system (s1–s5), animation patterns,
  and per-section design conventions. Trigger phrases: "add a new illustration", "update the
  farm illustration", "draw a new ob1 hero", "extend Illustrations.tsx".
---

# OB-1 Paper Cut-Out Illustration System

All illustrations live in a single file:
`/Users/gregharned/work/ob1-app/app/Illustrations.tsx`

Animation keyframes are defined in:
`/Users/gregharned/work/ob1-app/app/globals.css` (under `/* ─── Illustration motion ─── */`)

---

## Visual Design Principles (Paper Cutout Depth)

These principles govern how ob1 illustrations achieve a realistic paper cutout feel in SVG/React.

### Layer Ordering
- Build scenes **back to front**: sky/background first, foreground last. SVG z-order (later elements paint on top) naturally matches paper stack order.
- Use 4–6 distinct depth layers. More than 6 layers looks cluttered; fewer than 3 loses dimensionality.
- Each layer must **overlap** the one behind it — no gaps between layers or shadows have nothing to fall on.

### Shadow System (SVG `<filter>` / `feDropShadow`)
- Apply a drop shadow to each layer individually, not to the whole composition group.
- Shadow direction must be **consistent** across all layers — pick one light source (top-left is standard) and never deviate.
- Keep shadows **subtle**: `stdDeviation` 1–3, opacity 0.20–0.40. High blur or opacity reads as a digital glow, not paper.
- Shadow color should be a dark version of the layer below, or near-black — avoid pure black at full opacity.
- The ob1 shadow scale (`s1`–`s5`) maps to increasing offset/blur for layers progressively closer to the viewer.

### Shape Construction
- Use **clean, slightly simplified silhouettes** — paper cut art is constrained by what a physical cut could produce. Avoid paths with fine intricate detail.
- Shapes should be **flat fills only** — no gradients within a single paper piece. Color variation lives between layers, not within one.
- Slightly organic/imperfect edges (gentle curves rather than perfect geometry) reinforce the handmade feel.

### Color Palette for Paper Depth
- Use an analogous or tonal palette (3–5 hues with lightness variation).
- **Foreground layers**: slightly darker or more saturated — they are closer and catch more shadow from above.
- **Background layers**: lighter values — they are further away and lit more evenly.
- Avoid rainbow arrangements; the ob1 `P` palette provides the canonical tones — use those, do not introduce ad-hoc colors.

### Highlights
- A thin lighter shape along the top edge of a foreground element reinforces that it is a separate lifted piece.
- Use sparingly — one highlight per key foreground subject is enough.

---

## RULE: EXPORT SYNTAX — `export function` ONLY, NEVER `export const`

**Every component MUST be declared using the `export function` statement syntax.** This is non-negotiable.

**CORRECT — always use this:**
```tsx
export function CottageIllustration() {
  // ...
}
```

**FORBIDDEN — never use these:**
```tsx
export const CottageIllustration = () => { ... }       // ❌ WRONG
export const CottageIllustration: React.FC = () => { ... }  // ❌ WRONG
const CottageIllustration = () => { ... }               // ❌ WRONG
```

**Before writing any component, write the opening line as `export function XxxIllustration() {` — never `export const`.**

---

## RULE: COMPLETE_SCENE — EVERY RESPONSE MUST PRODUCE 100% COMPLETE, COMPILABLE CODE.

**THE ROOT CAUSE OF FAILURES: Too many planned shapes. The response hits its length limit before the SVG is closed.**

**THE SOLUTION: USE FEWER SHAPES. A COMPLETE 9-ELEMENT SCENE SCORES 100%. A TRUNCATED 30-ELEMENT SCENE SCORES 0%.**

### ABSOLUTE MAXIMUM: 10 SVG ELEMENTS TOTAL

Count every `<rect`, `<circle`, `<ellipse`, `<path`, `<polygon`, `<line`, `<g` as one element each.
- **At element 7: WRITE NO MORE NEW SHAPES. Begin closing all open `<g>` tags, then write `</svg>`, `);`, `}`.**
- **At element 9: EMERGENCY CLOSE. Stop. Close everything. Write the wiring block.**
- **Never plan more than 10 elements. Never.**

### MANDATORY PRE-WRITE BUDGET — MAXIMUM 10 ELEMENTS

Before writing a single line of JSX, write this comment block and fill it in:

```
// ELEMENT BUDGET (MAX 10):
// 1. sky rect
// 2. far hill path
// 3. mid hill path
// 4. foreground ground rect
// 5. [subject shape 1]
// 6. [subject shape 2]
// 7. [subject shape 3]
// 8. [accent 1]
// 9. [accent 2]
// TOTAL: 9 — STOP HERE
```

**If your budget exceeds 10, DELETE shapes until you are at or below 10. Do not proceed until your budget is ≤10.**

### THE COMPLETION CONTRACT — VERIFY BEFORE ENDING

After writing your last planned shape, you MUST verify all six of these:
1. ✅ Every opened `<g>` tag has a matching `</g>`
2. ✅ Every element ends with `/>` or a matching closing tag
3. ✅ Every string attribute has both opening AND closing quote (`fill="#abc"` not `fill="#abc`)
4. ✅ `</svg>` is present
5. ✅ `);` closes the return statement
6. ✅ `}` closes the function body

**If ANY of these six are missing, your score is 0. Complete them before writing anything else.**

### EMERGENCY CLOSE SEQUENCE — USE THIS THE INSTANT YOUR RESPONSE FEELS LONG

The moment you sense the response is getting long — before you finish your current shape — write this:

```tsx
    </g>
  </svg>
);
}
```

Then immediately write the wiring block. **Do not add any more shapes after triggering emergency close. Not one.**

### DEFINITION OF COMPLETE SCENE

The JSX component:
1. Opens with `export function XxxIllustration() {`
2. Contains a `return (` statement
3. Contains an `<svg` opening tag with complete attributes
4. Contains all elements — **every single attribute fully written, no truncation**
5. Contains a `</svg>` closing tag
6. Ends with `);` closing the return
7. Ends with `}` closing the function
8. Is followed by the wiring block

### WHAT TRUNCATION LOOKS LIKE — NEVER PRODUCE THESE

```tsx
<circle cx='112' cy='229' r        // ❌ attribute cut mid-value — ZERO SCORE
fill="url(#g                       // ❌ string cut mid-value — ZERO SCORE
<ellipse rx="12                    // ❌ attribute cut — ZERO SCORE
width='20' height='22              // ❌ attribute cut — ZERO SCORE
strokeWidth="                      // ❌ attribute with no value — ZERO SCORE
r=""                               // ❌ empty attribute value — ZERO SCORE
```

**Every attribute must be fully written: `<circle cx="112" cy="229" r="8" fill="#fff" />`**

### THE SELF-CHECK — READ YOUR LAST 10 LINES BEFORE SUBMITTING

After writing your last shape, read back your last 10 lines and confirm:
- No unclosed `<g>` tags
- No attribute values cut mid-string
- No empty attribute values like `r=""` or `strokeWidth="`
- `</svg>` is present
- `);` is present
- `}` is present
- The wiring block is present

**If anything is missing from this list, do not submit. Fix it first.**

---

## RULE: NEVER TRUNCATE — COMPLETE EVERY TAG, EVERY ATTRIBUTE, EVERY CLOSING BRACE

**Every attribute value MUST be fully written.** These patterns are FORBIDDEN:
- `fill="#7BA8D1` ← missing closing quote ❌
- `y=` ← attribute with no value ❌
- `r=""` ← empty attribute value ❌
- `strokeWidth="` ← attribute cut before value ❌
- `<rect x="10"` ← element with no closing `/>` or children+`</rect>` ❌
- A response that ends without `</svg>` and `}` closing the function ❌

**TRUNCATION PREVENTION STRATEGY — HARD SHAPE BUDGET:**
- You have a MAXIMUM of 10 SVG elements total (rect, path, circle, polygon, line, ellipse, g, etc.)
- Count your elements as you write. At element 7, you MUST begin closing out the scene.
- At element 9, write ONLY closing tags and the wiring block — no new shapes.
- A simple complete 8-element scene beats a detailed 30-element truncated scene EVERY TIME.

**MANDATORY PRE-WRITE PLAN:** Before writing any JSX, declare your exact element list:
```
// LAYERS: sky | far-hill | mid-ground | [SUBJECT] | foreground | accent
// ELEMENT BUDGET: sky=1, hills=2, subject=3, foreground=2, accents=1 = 9 total
// SUBJECT SHAPES: [list each shape name here before writing a single line of JSX]
```
This forces you to plan completion before you start.

---

## RULE: PAPER CUT-OUT STYLE — MANDATORY STACKED DEPTH PLANES WITH DISTINCT LAYERING

**PAPER CUT-OUT STYLE FAILURES STILL OCCUR. THIS RULE IS MANDATORY ON EVERY ILLUSTRATION.**

**The paper cut-out aesthetic requires ALL of the following — check each box before submitting:**

### ✅ FLAT FILLS ONLY — ZERO GRADIENTS

- **NEVER use `<linearGradient>`, `<radialGradient>`, or `<defs>` containing gradient elements**
- Every `fill` attribute MUST be a solid hex color string: `fill="#4A7C59"` — never `fill="url(#grad)"`
- Sky backgrounds MUST be a single solid color rect, NOT a gradient
- Clouds MUST be flat solid-filled ellipses or circles — NOT gradient-blended or opacity shapes

**FORBIDDEN gradient patterns:**
```tsx
<defs><linearGradient id="sky">...</linearGradient></defs>  // ❌ NEVER
fill="url(#sky)"                                            // ❌ NEVER
```

### ✅ MINIMUM 3 DISTINCT DEPTH LAYERS

- Every illustration MUST have at least 3 visually distinct stacked layers
- Layer 1 (back): sky/backdrop — lightest value
- Layer 2 (mid): hills, ground planes, or horizon shapes
- Layer 3 (front): primary subject + foreground elements — darkest/most saturated
- Each layer must use a **different fill color** — same color across all layers = FAIL

### ✅ STACKED OVERLAP — EACH LAYER OVERLAPS THE ONE BEHIND IT

- Mid-ground shapes must visually sit ON TOP of the sky rect
- Foreground shapes must visually sit ON TOP of mid-ground shapes
- No floating isolated shapes with visible gaps beneath them

### ✅ MINIMUM 3 DISTINCT FILL COLORS

- Count the unique hex values in your `fill` attributes before submitting
- If fewer than 3 distinct colors: FAIL
- The ob1 P palette provides canonical values — use them

---

## RULE: SUBJECT-FIRST — PRIMARY SUBJECT BEFORE BACKGROUND DETAILS

**The PRIMARY SUBJECT MUST be written as SVG shapes BEFORE any background or decorative detail.**

**MANDATORY WRITING ORDER:**
1. `export function` declaration + palette constants
2. **PRIMARY SUBJECT shapes** (the thing specifically requested)
3. Background sky/ground shapes
4. Mid-ground details
5. Foreground accents
6. Close `</svg>`, close `return (`, close function `}`
7. Wiring block

**SUBJECT IDENTIFICATION — before writing a single line of JSX, answer:**
> "What is the ONE thing this illustration is named after or specifically requested to show?"

That thing's shapes go FIRST, immediately after the palette constants.

---

## RULE: MANDATORY RESPONSE STRUCTURE

Every response that creates or modifies an illustration MUST contain ALL THREE sections in this order:

1. **The component code** — complete, non-truncated SVG component
2. **Illustrations.tsx wiring** — explicit instruction to add the export
3. **Page wiring** — exact import statement AND hero wrapper pattern:

```tsx
// 1. Import in the target page file:
import { MyIllustration } from "../Illustrations";

// 2. Place inside the hero-card JSX:
<div className="hero-card glass mb-6 fade-up">
  <div className="absolute inset-0 opacity-60 pointer-events-none">
    <MyIllustration />
  </div>
  <div className="relative p-5">
    {/* page content */}
  </div>
</div>
```

---

## RULE: DEPICTS THE REQUESTED SUBJECT — NEVER SUBSTITUTE OR OMIT

Read the task prompt and identify the PRIMARY SUBJECT. That subject MUST appear as rendered SVG shapes.

- If asked for a trellis with climbing vines → trellis grid lines AND vine/leaf shapes MUST be present
- If asked for a barn → barn walls, roof, and door MUST be present
- If asked for a rooster silhouette → a rooster shape MUST be present
- If asked for wildflowers → multiple distinct flower shapes MUST be present (not just generic circles)
- If asked for a specific tool → that tool's recognizable silhouette MUST be present

**NEVER substitute a generic landscape for a specifically requested subject.**
