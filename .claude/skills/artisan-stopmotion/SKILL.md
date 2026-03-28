---
name: artisan-stopmotion
description: >
  Stop-motion video production system based on the Wes Anderson "Isle of Dogs" sushi scene aesthetic.
  Invoke when the user says "make a stop motion video about X", "create a stop motion for X",
  or "artisan stop motion". Produces a finished MP4 video by generating frames with Nano Banana 2
  and assembling with ffmpeg. Style: cinematic process noir, overhead birds-eye, warm muted palette,
  one saturated pop color, ASMR sound design, rhythm-locked editing.
library: true
---

# Artisan Stop-Motion Production System

## Reference Aesthetic

Wes Anderson — Isle of Dogs sushi-making scene (2018).
YouTube: https://www.youtube.com/watch?v=enuua9-1Y5Q

**Core identity:** Staccato process cinema. Multiple distinct actions, each shown in 2–5 poses, hard-cut between shots. The rhythm is fast and precise. The hands are deliberate — they enter, perform, and exit.

---

## The Fundamental Structure

**This is the most important thing to understand:**

The Isle of Dogs sushi scene is NOT one long action shown over 30 frames. It is **many distinct shots**, each showing a **complete action in 2–5 poses**, hard-cut together. Each shot has its own framing. Hands enter and exit between shots. The cuts are fast — 0.2–0.5s per pose.

```
Shot 1 (2–5 poses): Action A complete
     ↓ HARD CUT
Shot 2 (2–5 poses): Action B complete
     ↓ HARD CUT
Shot 3 (2–5 poses): Action C complete
     ↓ HARD CUT (slower)
Shot 4 (2–3 poses, longer holds): The reveal
```

Each shot is generated independently — different framing, different crop, different subject emphasis. The slight variation between poses within a shot (from individual AI renders) creates the stop-motion jitter. No compositing, no pixel-sliding.

---

## Execution Pipeline

```
1. Generate background plate (empty surface, no hands)
2. For each shot:
   a. Generate Shot Frame 1 using bg_plate as -i
   b. Generate Shot Frames 2–N using [bg_plate + frame 1] as -i references
      (dual-reference: locks background AND pose)
3. Assemble with ffmpeg — varying hold durations per pose
4. Warm LUT grade → output MP4
```

Output: `/tmp/stopmotion-{slug}/output.mp4`

---

## The Style Lock

Append verbatim to EVERY prompt:

```
STYLE LOCK:
"Stop-motion animation film still, Wes Anderson Isle of Dogs aesthetic. Miniature diorama quality.
HANDS: Matte ochre-yellow sculpted resin hands, solid uniform skin tone approximately #C7A446, simplified blocky fingers, no pores no wrinkles, tiny scattered black speckles visible on skin surface, mannequin-like smooth finish — NOT realistic human skin, NOT claymation, NOT marionette.
CAMERA: Overhead 90-degree birds-eye locked flat-lay, no perspective tilt, clean graphic framing.
LIGHTING: Soft flat overhead studio light, even diffused illumination, gentle shadows, controlled like product photography — NOT dramatic side lighting.
SURFACE: Light ash or oak wood, straight prominent vertical grain, warm neutral tone, matte finish — NOT dark walnut, NOT glossy.
CUTTING BOARD (if present): Pale maple or birch, rectangular, slightly worn matte finish, sits on top of main surface.
MATTE EVERYTHING: No specular reflections, no shine, no gloss anywhere except lacquerware props. Every surface is matte.
FOOD/OBJECTS: Stylized and simplified like sculpted models — NOT photorealistic. Graphic, clean forms.
COLOR: Warm neutral palette dominated by ochre, tan, pale wood. One saturated accent color as pop.
SHARPNESS: Ultra-sharp, every frame a perfect photograph, no motion blur, no depth-of-field bokeh."
```

---

## Generation — Shot by Shot

### Background Plate (once, no hands)

```bash
uv run {nb2_script} \
  --prompt "Light ash wood surface, overhead birds-eye flat-lay. Straight prominent vertical grain, warm neutral tone, matte finish. Empty — no objects, no hands. {STYLE_LOCK}" \
  --filename "/tmp/stopmotion-{slug}/frames/bg_plate.png" \
  --resolution 2K
```

### Shot Frame 1 (anchors hand + object)

```bash
uv run {nb2_script} \
  --prompt "Match the exact surface and lighting of the reference. {shot_description}. Matte ochre-yellow sculpted resin hands (~#C7A446), simplified blocky fingers, tiny black speckles on skin, no pores, mannequin-like — in the Isle of Dogs stop-motion aesthetic. {STYLE_LOCK}" \
  -i "/tmp/stopmotion-{slug}/frames/bg_plate.png" \
  --filename "/tmp/stopmotion-{slug}/frames/{shot}_f1.png" \
  --resolution 2K
```

### Shot Frames 2–N (chained from frame 1, max 4 frames per shot)

```bash
uv run {nb2_script} \
  --prompt "Match the surface of the first reference and the hand/object position of the second reference. Only change: {tiny_action_change}. Same matte ochre-yellow sculpted resin hands. {STYLE_LOCK}" \
  -i "/tmp/stopmotion-{slug}/frames/bg_plate.png" \
  -i "/tmp/stopmotion-{slug}/frames/{shot}_f1.png" \
  --filename "/tmp/stopmotion-{slug}/frames/{shot}_f2.png" \
  --resolution 2K
```

**Max 4 frames per shot.** Chains longer than 4 drift. If you need more poses, start a new shot.

---

## Hold Durations

```
Act 1 setup shots:   0.4–0.6s per pose
Act 2 process shots: 0.2–0.35s per pose  ← the staccato rhythm
Act 2 peak shot:     0.35–0.5s per pose  ← slightly slower, more weight
Act 3 reveal:        1.0–3.0s            ← breathe here
```

**ffmpeg concat entry:** `duration 0.25` (adjust per above)

---

## Shot List by Subject Type

### Fungal / Mushroom Cultivation (grain spawn jar filling)

**Design variables:**
- Surface: light ash/oak, straight vertical grain, matte
- Cutting board: pale maple, sits on main surface
- Accent: muted teal or red lacquer prop
- Pop: bright white colonized mycelium against golden uncolonized grain
- Label: strain name only ("Blue Oyster", "Lion's Mane") — never substrate
- Narrative arc: uncolonized grain → colonized spawn bag → breaking clumps → scooping → filling → sealing → reveal

**Shot sequence:**

| Shot | Framing | Poses | Hold | Description |
|------|---------|-------|------|-------------|
| A — Uncolonized jar | Wide | 3 | 0.5s | Ochre-yellow sculpted resin hand slides jar of golden uncolonized grain to center. Hand exits. |
| B — Spawn bag enters | Medium | 3 | 0.45s | Hand brings colonized spawn bag next to jar. Stark contrast: golden grain vs white mycelium. |
| C — Break up clumps | Tight | 4 | 0.35s | Two hands squeeze spawn bag — clumped white mycelium mass breaks apart into loose fluffy grain. |
| D — Scoop loads | Medium | 3 | 0.4s | Hand plunges scoop into bag, lifts heaped white grain, moves toward jar. |
| E — Grain pours | Tight crop | 4 | 0.3s | Scoop tips over jar mouth — cascade of white colonized grain falls in across 4 poses. |
| F — Lid seals | Medium | 3 | 0.45s | Lid with silicone port descends and seals jar. Hand exits. |
| G — Reveal | Wide | 2 | 2.0s | Jar labeled "Blue Oyster" alone on light wood surface. Warm pool of light. |

Total: ~22 poses. At average 0.42s = ~9 seconds.

**Shot C safety note:** Avoid "syringe", "needle", "piercing", "penetration". Use: "inoculation tool", "tip of the tool", "self-healing silicone port", "the tool enters the port".

### Botanical / Growing

| Shot | Poses | Hold | Description |
|------|-------|------|-------------|
| A — Seed reveal | 3 | 0.5s | Hand opens seed packet, small seeds visible in palm. |
| B — Soil prep | 3 | 0.3s | Finger makes small depression in soil in pot. |
| C — Planting | 3 | 0.25s | Seed placed in depression, finger covers. |
| D — Water | 3 | 0.3s | Water drops fall from above onto soil. |
| E — Reveal | 2 | 2.0s | Same overhead framing, seedling emerged (time jump implied). |

### Food Preparation

| Shot | Poses | Hold | Description |
|------|-------|------|-------------|
| A — Ingredient reveal | 2 | 0.5s | Ingredient placed on cutting board. |
| B — Prep action | 4 | 0.25s | Knife, fold, press, roll — the core technique in 4 poses. |
| C — Assembly | 3 | 0.3s | Components brought together. |
| D — Reveal | 2 | 2.0s | Completed dish overhead, hero lighting. |

---

## ffmpeg Assembly

```bash
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -vf "scale=1920:1080:force_original_aspect_ratio=decrease,
       pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black,
       eq=brightness=0.02:contrast=1.08:saturation=0.85,
       curves=red='0/0 0.5/0.55 1/1':green='0/0 0.5/0.50 1/0.96':blue='0/0 0.5/0.43 1/0.87'" \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -r 24 \
  output.mp4
```

---

## Quality Gates

Before calling done:
- [ ] Each shot has a distinct framing — not all the same wide overhead
- [ ] Hard cuts between shots — no dissolves
- [ ] Process shots average 0.2–0.35s hold — it should feel fast and precise
- [ ] Reveal shot is noticeably slower — 1–3s hold
- [ ] All holds are varied — not every frame the same duration
- [ ] Label reads "Blue Oyster" (strain), not "rye grain" (substrate)
- [ ] One hand maximum per shot

---

## The 10 Non-Negotiable Rules

1. **Overhead is the hero angle.** 90% of shots locked-off birds-eye.
2. **Natural tactile surfaces only.** Wood, slate, linen, ceramic.
3. **Warm muted base + one saturated pop.**
4. **Dual lighting.** Soft process / hard reveal. Never mixed.
5. **Maker's hands always present.** Objects don't materialize — hands bring them.
6. **Rhythm drives everything.** Fast process, slow reveal.
7. **ASMR sound.** Every action hyper-amplified.
8. **Multiple distinct shots.** Not one action dragged across 30 frames.
9. **No graphic overlays.** Cinematic only.
10. **Beautiful artifice.** Idealized, not documentary.

---

## Skill Notes

### What Works Well
- Two `-i` flags (bg_plate + shot frame 1) locks both surface and pose within a shot

### Calibrations
- 2K resolution is minimum — 1K is too soft
- ffmpeg warm curves: `red='0/0 0.5/0.55 1/1':green='0/0 0.5/0.50 1/0.96':blue='0/0 0.5/0.43 1/0.87'`

### Lessons Learned
- 2026-03-19: Generating 30 frames of one action = herky-jerky slideshow. The reference has MANY distinct shots (2–5 poses each), not one action across 30 frames.
- 2026-03-19: Compositing (sliding one image across background) looks like PowerPoint animation, not stop-motion. Stop-motion = photographs of physical objects re-posed. Each frame must be a genuine render.
- 2026-03-19: Chain drift accumulates after ~6 frames. Max 4 frames per shot chain.
- 2026-03-19: Jar labels = strain name ("Blue Oyster"), never substrate ("rye grain").
- 2026-03-19: Inoculation port is on the LID (top), not the side of the jar.
- 2026-03-19: One hand per shot maximum. Hands enter and exit between shots.
- 2026-03-19: Avoid "syringe/needle/piercing/penetration" — use "inoculation tool/tip/port" language.
- 2026-03-24: THE SURFACE IS LIGHT ASH/OAK — not dark walnut. Isle of Dogs uses a light wood with straight vertical grain. "Dark aged walnut" was wrong and produced the wrong look entirely.
- 2026-03-24: DO NOT SAY "puppet hands" — it generates marionette/claymation/sock puppet associations. Instead describe specifically: "matte ochre-yellow sculpted resin hands, ~#C7A446, simplified blocky fingers, tiny black speckles on skin, no pores no wrinkles, mannequin-like smooth finish, Isle of Dogs stop-motion aesthetic."
- 2026-03-24: EVERYTHING IS MATTE — no specular highlights anywhere except lacquerware. Adding shine/gloss destroys the aesthetic.
- 2026-03-24: Food and objects are STYLIZED SCULPTED MODELS, not photorealistic. The fish has graphic stripes. Blood is paint drops. Rice is a solid white shape. Prompt for simplified, graphic, model-like forms.
- 2026-03-24: Shots have wide-to-tight spatial continuity — establish wide, cut tighter for detail. Not isolated independent worlds.
- 2026-03-24: The #1 stop-motion quality signal is ZERO motion blur + subtle non-uniform jitter between frames. Add `noise=alls=2:allf=t+u` in ffmpeg to simulate this.
- 2026-03-24: Use Gemini multimodal video analysis (`mcp__gemini__analyze_video`) on reference videos before generating. Download with yt-dlp + upload to Files API if needed. Extract frames with ffmpeg for image analysis.
