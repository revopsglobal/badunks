---
name: ob1-paper-illustrations
description: Create paper cut-out SVG illustrations for ob1-app.---

# OB-1 Paper Cut-Out Illustration System

All illustrations live in:
`/Users/gregharned/work/ob1-app/app/Illustrations.tsx`

Animation keyframes are in:
`/Users/gregharned/work/ob1-app/app/globals.css` (under `/* ─── Illustration motion ─── */`)

**Read Illustrations.tsx before writing anything new.** The file contains the P palette, shadow constants, hooks, and all existing illustrations. Match their depth, density, and craft.

---

## The Aesthetic — What These Illustrations Must Feel Like

Imagine physically cutting shapes from colored paper and stacking them. Each cut piece is:
- A **flat, solid color** — no gradients within the shape itself
- Slightly **organic and imperfect** — scissors follow curves, not rulers
- Casting a **shadow onto the layer below** — depth comes from this stacking

The reference quality to target:

**Scene density**: Think of a tropical leaf composition on a dark background — 10–15 individual leaf shapes, each slightly lighter than the one behind it, all overlapping. That's the depth to aim for. Not 5 shapes. Not 8 shapes. Rich stacking.

**Color progression**: Background = darkest and most muted. Each layer forward gets slightly lighter, warmer, or more saturated. The P palette encodes this exactly: `layer1` (deep shadow) → `layer7` (bright front surface).

**Warm atmosphere**: The sky is never just a flat rect. It has a radial glow — amber/rust tones radiating from where the sun would be. This single detail separates a rich illustration from a flat one.

**Botanical richness**: Plants, trees, and grasses are built from many individual shapes — not one generic blob. A tree is a trunk + 3–4 stacked canopy ellipses at slightly different values. Grass is a series of small arch paths. This is what makes the foreground feel lush.

**Living details**: Every illustration has at least one animated element. Trees sway. Smoke drifts. The sun pulses. Animals breathe. These micro-animations are what make the scene feel alive.

---

## Codebase Conventions — Match These Exactly

### File & component location
```tsx
// Illustrations.tsx header:
'use client';
import { useState, useEffect } from 'react';

// Hooks already defined in the file — do NOT redefine:
// useIsDay()  — returns true 6am–8pm, updates every minute
// useIsLight() — returns true if document has .light class
```

### SVG root
```tsx
<svg viewBox="0 0 W H" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
```
ViewBox varies per illustration. Match proportions to the card dimensions (~16:9 or wider).
Common sizes: `200×150`, `300×165`, `180×140`, `280×160`.

### Background
```tsx
{/* Always two layers: theme-aware base + atmospheric glow */}
<rect x="0" y="0" width={W} height={H} style={{ fill: "var(--ill-bg)" }} />
<rect x="0" y="0" width={W} height={H} fill="url(#atmosphericGlow)" />
```
`var(--ill-bg)` adapts to dark/light mode. The atmospheric glow is a `radialGradient` in `<defs>`.

### Shadow constants (defined at file level — do NOT redefine)
```tsx
const s1 = "drop-shadow(0 1px 2px rgba(0,0,0,0.18))";   // furthest back
const s2 = "drop-shadow(0 2px 5px rgba(0,0,0,0.28))";
const s3 = "drop-shadow(0 3px 8px rgba(0,0,0,0.38))";
const s4 = "drop-shadow(0 5px 12px rgba(0,0,0,0.48))";
const s5 = "drop-shadow(0 7px 16px rgba(0,0,0,0.55))";   // frontmost
```
Apply as: `style={{ filter: s3 }}` on `<g>` groups, not individual elements.

### Export syntax — `export function` only
```tsx
export function FarmIllustration() { ... }  // ✅
export const FarmIllustration = () => { ... }  // ❌ never
```

---

## The P Palette — Use It, Don't Invent Colors

The palette is already defined in Illustrations.tsx. Do not redefine it — just use `P.xxx`:

```tsx
const P = {
  // Earth depth (back = dark, front = light)
  layer1: "#0f2214",  // deepest shadow
  layer2: "#1a3a1e",  // deep ground
  layer3: "#2d5c35",  // mid-dark
  layer4: "#3d7a46",  // mid
  layer5: "#56a462",  // mid-light
  layer6: "#78c484",  // front
  layer7: "#a8d8b0",  // highlight / top surface

  // Warm accents
  amber: "#c8861a",  amberM: "#d4952a",  amberL: "#e8b84c",  amberHL: "#f5d070",
  rust:  "#8c3a18",  rustM:  "#b04820",  rustL:  "#d06030",

  // Neutral
  cream: "#e8dbb0",  creamL: "#f2e8c8",

  // Sky
  sky: "#1a2a3a",  skyM: "#2a4060",  cloud: "#8aacb8",

  // Kunekune pig colors
  kTan: "#c89030", kTanL: "#e8b050", kBlk: "#1a0e08", kBlkM: "#2a1808",
  kPnk: "#e8a898", kPnkD: "#c87868",
  kRust: "#d47018", kRustL: "#e8882a",
  kWht: "#f0ece0",  kWhtS: "#d4ccc0",

  // Dog colors
  gGold: "#c8a030", gGoldL: "#e0be58", gCream: "#f0e0a0",
  tWheat: "#c8a840", tDkWht: "#a07820", tPale: "#e8d890",
};
```

---

## How to Build a Rich Scene — Layer by Layer

### Structure every illustration as 5–7 named depth layers

```tsx
export function MyIllustration() {
  return (
    <svg viewBox="0 0 300 165" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
      <defs>
        {/* Atmospheric glow — placed here for portability */}
        <radialGradient id="myGlow" cx="70%" cy="25%" r="45%">
          <stop offset="0%" stopColor={P.amberL} stopOpacity="0.18" />
          <stop offset="100%" stopColor={P.layer1} stopOpacity="0" />
        </radialGradient>
      </defs>

      {/* ── Layer 1: SKY + ATMOSPHERE ── */}
      <rect ... style={{ fill: "var(--ill-bg)" }} />
      <rect ... fill="url(#myGlow)" />
      {/* sun or moon depending on isDay */}

      {/* ── Layer 2: FAR RIDGE / HORIZON ── */}
      <path ... fill={P.layer2} style={{ filter: s1 }} />

      {/* ── Layer 3: MID GROUND + STRUCTURES ── */}
      <path ... fill={P.layer3} style={{ filter: s2 }} />
      {/* buildings, large trees, water */}

      {/* ── Layer 4: SUBJECT + ACTIVITY ── */}
      <g style={{ filter: s3 }}>
        {/* the named subject — barn, garden beds, animals */}
      </g>

      {/* ── Layer 5: NEAR GROUND + FOREGROUND PLANTS ── */}
      <path ... fill={P.layer4} style={{ filter: s4 }} />
      {/* fence, rocks, near plants */}

      {/* ── Layer 6: FOREGROUND DETAILS + ANIMATION ── */}
      <g style={{ animation: "float 14s cubic-bezier(0.37,0,0.63,1) infinite" }}>
        {/* animated animals, foreground elements */}
      </g>

      {/* ── Layer 7: CLOSEST GROUND STRIP ── */}
      <ellipse cx={W/2} cy={H} rx={W*0.6} ry="14" fill={P.layer6} style={{ filter: s5 }} />
    </svg>
  );
}
```

### Gradients: ONLY for atmosphere, NEVER for paper shapes
```tsx
// ✅ Correct — atmospheric glow on the sky
<radialGradient id="sunGlow" cx="75%" cy="25%" r="35%">
  <stop offset="0%" stopColor={P.amberHL} stopOpacity="0.6" />
  <stop offset="100%" stopColor={P.amberL} stopOpacity="0" />
</radialGradient>

// ✅ Correct — background disc with depth
<radialGradient id="mntBg" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stopColor={P.layer3} />
  <stop offset="100%" stopColor={P.layer1} />
</radialGradient>

// ❌ Wrong — gradient fill on a paper shape (hill, barn, leaf)
<path fill="url(#someGradient)" />  // paper is flat — use solid P.layerN
```

### Build botanical elements with many shapes, not one blob
```tsx
// ❌ Too simple:
<ellipse cx="38" cy="100" rx="18" ry="14" fill={P.layer4} />

// ✅ Rich tree — 3 stacked canopy layers:
<g style={{ animation: "treeSway 4.2s cubic-bezier(0.37,0,0.63,1) infinite", transformOrigin: "38px 130px" }}>
  <rect x="35" y="104" width="6" height="28" rx="2" fill={P.layer3} />
  <ellipse cx="38" cy="100" rx="14" ry="10" fill={P.layer4} style={{ filter: s2 }} />
  <ellipse cx="38" cy="94" rx="10" ry="8" fill={P.layer5} style={{ filter: s2 }} />
  <ellipse cx="38" cy="89" rx="7" ry="6" fill={P.layer6} />
</g>
```

### Use `.map()` for repeating elements — don't repeat the same code
```tsx
// Fence posts:
{[14, 28, 42, 56].map(x => (
  <g key={x} style={{ filter: s2 }}>
    <rect x={x} y="130" width="4" height="22" rx="1.5" fill={P.layer7} opacity="0.82" />
    <polygon points={`${x-1},130 ${x+2},126 ${x+5},130`} fill={P.cream} opacity="0.7" />
  </g>
))}

// Barn wood siding lines:
{[90, 98, 106, 114, 122].map(x => (
  <line key={x} x1={x} y1="88" x2={x} y2="134" stroke={P.layer1} strokeWidth="0.5" opacity="0.4" />
))}
```

### Shadow ellipses for grounded feel
```tsx
{/* Always add a shadow ellipse beneath foreground subjects */}
<ellipse cx="108" cy="143" rx="30" ry="5" fill="rgba(0,0,0,0.25)" />
```

---

## Animation Catalogue

All keyframes are in globals.css. Use `cubic-bezier(0.37,0,0.63,1)` for all easing — it gives natural paper-like motion.

```tsx
// Trees — always anchor the transformOrigin at the base of the trunk
style={{ animation: "treeSway 4.2s cubic-bezier(0.37,0,0.63,1) infinite", transformOrigin: "38px 130px" }}

// Multiple trees at slightly different speeds for organic feel:
// Tree 1: 4.2s, Tree 2: 5.1s 0.7s delay, Tree 3: 3.8s 1.1s delay

// Sun
style={{ animation: "sunPulse 3s cubic-bezier(0.37,0,0.63,1) infinite" }}

// Chimney smoke
style={{ animation: "smokeDrift 3s ease-in-out infinite", transformOrigin: "216px 100px" }}

// Floating ambient group (wraps multiple foreground elements for gentle bob)
style={{ animation: "float 14s cubic-bezier(0.37,0,0.63,1) infinite 2s" }}

// Animal breathing
style={{ animation: "breathe 3.2s cubic-bezier(0.37,0,0.63,1) infinite", transformOrigin: "cx py" }}

// Tail wag
style={{ animation: "wagTail 2.1s cubic-bezier(0.37,0,0.63,1) infinite", transformOrigin: "px py" }}

// Leaves
style={{ animation: "leafSway 3s ease-in-out infinite alternate" }}

// Flowers
style={{ animation: "petalBloom 2s ease-in-out infinite alternate" }}

// Hammer / tool
style={{ animation: "hammerSwing 1.4s cubic-bezier(0.37,0,0.63,1) infinite", transformOrigin: "90px 50px" }}
```

---

## Day/Night Theming

Use the `useIsDay()` hook for outdoor sky illustrations. Use `useIsLight()` for UI adjustments.

```tsx
export function GroundsIllustration() {
  const isDay = useIsDay();
  const isLight = useIsLight();
  const sunOuter = isLight ? 0.30 : 0.08;
  // ...
  return (
    <svg ...>
      {isDay ? (
        <g style={{ animation: "float 10s cubic-bezier(0.37,0,0.63,1) infinite" }}>
          <g style={{ animation: "sunPulse 3s cubic-bezier(0.37,0,0.63,1) infinite" }}>
            <circle cx="160" cy="28" r="28" fill={P.amberL} opacity={sunOuter} />
            <circle cx="160" cy="28" r="18" fill={P.amberL} opacity={0.15} />
            <circle cx="160" cy="28" r="9" fill={P.amberM} style={{ filter: `drop-shadow(0 0 12px ${P.amberL})` }} />
            <circle cx="160" cy="28" r="5" fill={P.amberHL} />
          </g>
        </g>
      ) : (
        <g>
          {/* Stars + crescent moon */}
          <circle cx="145" cy="10" r="1" fill="#d4ddf0" opacity="0.7" />
          <circle cx="160" cy="28" r="13" fill="#c8d4f0" opacity="0.9" />
          <circle cx="166" cy="24" r="11" fill={P.layer1} />
        </g>
      )}
    </svg>
  );
}
```

---

## Subject-Specific Patterns

### Outdoor landscape (Grounds, Farm, Garden, Cottage)
- 5–6 rolling hill layers using `<path>` with Q curves
- Each hill: `fill={P.layerN}` where N increases as hills come forward
- Trees built with trunk rect + 3 stacked canopy ellipses (dark→mid→light)
- Fence posts via `.map()` over an x-coordinate array
- Animals near layer 5/6

### Barn / Farm structures
- Roof = 3 overlapping polygons (dark base, mid layer, highlight ridge): `P.layer2, P.layer3, P.layer4`
- Walls = rect with vertical siding lines (`.map()` over x values, 0.4 opacity)
- Barn door = arch + X-brace pattern
- Silo = rounded rect + ellipse cap

### Indoor / circular badge (Maintenance, Media, Insights)
- Backing disc: `<circle>` with `P.layer1` fill
- Mid ring: gradient disc from `P.layer3` → `P.layer1`
- Inner accent ring at reduced opacity
- Subjects centered, tools rotated with `transform="rotate(deg, cx, cy)"`
- Center focal element with `sunPulse` animation

### Kunekune pig (KunekPig helper function — already in Illustrations.tsx)
- Use the existing `KunekPig` helper for pig portraits
- For hero scenes, build pigs from: 4 leg rects + body ellipse + head circle + ear ellipse + snout ellipse + eye circle
- Use `P.kTan` / `P.kTanL` / `P.kPnk` / `P.kBlk` — never invent pig colors
- Add `breathe` animation anchored at body center, `wagTail` at tail root

### Animals (chickens, ducks, dogs)
- **Silkie chicken**: fluffy body from 3–4 overlapping circles (different opacities) + head circle + crest ellipse + beak polygon + eye circle + legs as `<line>` elements
- **Duck**: body ellipse + neck ellipse + green head circle + bill ellipse + white collar ellipse
- **Dog**: body ellipse + head circle + ear ellipses + snout + eye

---

## Wiring (Illustrations.tsx)

New illustrations append to the bottom as `export function`. When modifying existing ones, find by name and replace in place.

The file imports at the top (`'use client'`, hooks) apply to everything — do not duplicate them.

---

## What Separates Good from Great

- **Depth**: 6+ distinct layer values, each stepping `+1` toward the front
- **Atmosphere**: radialGradient glow in the sky, ground shadow ellipse beneath subjects
- **Botanical density**: trees have 3–4 canopy shapes, grass has 3–4 arch strokes, hedges have 5+ ellipses
- **Character detail**: animals have eyes, wattles, individual legs, highlights — not just silhouettes
- **Animation variety**: mix fast micro-animations (wagTail 2s) with slow ambient ones (float 14s)
- **Repeating elements via .map()**: fence posts, siding lines, stars, orchard trees
- **Shadow ellipses**: every grounded subject has a cast shadow ellipse beneath it
