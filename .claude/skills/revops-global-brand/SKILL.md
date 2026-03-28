---
name: revops-global-brand
library: true
description: Applies RevOps Global's official brand colors and typography to any artifact that may benefit from having RevOps Global's look-and-feel.---

# RevOps Global Brand Styling

## Mandatory Rules — Apply to Every Deliverable

These rules are NON-NEGOTIABLE. Every branded artifact MUST follow all of them.

1. **Fonts**: Use `"Urbanist"` for ALL headings. Use `"Inter"` for ALL body text. Never default to Arial as primary — it is fallback only.
2. **Font installation**: Before generating any document, run the Step 0 setup block (see bottom). If fonts cannot be installed, fall back to `"Arial"` and warn the user the document is not fully on-brand.
3. **Logo**: Every document, presentation, and report MUST include the RevOps Global logo. Use `assets/logo_color.png` on light backgrounds; `assets/logo_allwhite.png` (full wordmark, all white) on dark/navy backgrounds. Place on the cover page/title slide minimum. **Never use letter marks, abbreviations, or "RG" squares** — always use the full logo image file. For HTML/UI: `height: 28px; width: auto`.
4. **Heading color**: Use Deep Navy (`#072C87`) for all headings. Never use generic black for headings.
5. **Cover page**: Every multi-page document MUST have a branded cover page with logo, title in Urbanist, and a Cyan-to-Mint-Teal accent element.
6. **Font files**: Always copy `.ttf` font files to the user's workspace `fonts/` folder so teammates can install them locally.
7. **No emojis — ever.** Emojis are strictly prohibited in all RevOps Global brand design, UI, documents, presentations, and reports. Use clean inline SVG icons (line-weight style, 1.8px stroke, Deep Navy or Cyan) instead. This applies everywhere: navigation, KPI cards, page headers, sidebar items, buttons, tables, and body copy. Use the `revops-vector-art` skill to generate custom SVG icons when needed.

---

## Quick Reference

### Colors

| Name | Hex | RGB | Role |
|------|-----|-----|------|
| Deep Navy | `#072C87` | 7, 44, 135 | Primary brand — headings, key UI, dark backgrounds |
| Cyan | `#2DD6FF` | 45, 214, 255 | Vibrant accent — CTAs, highlights, interactive |
| Mint Teal | `#16F0DF` | 22, 240, 223 | Gradient partner — secondary highlights, accents |
| Black | `#000000` | 0, 0, 0 | Body text, high-contrast |
| White | `#FFFFFF` | 255, 255, 255 | Backgrounds, text on dark surfaces |
| Gray | `#8A91A2` | 138, 145, 162 | Captions, secondary text |
| Light Lavender | `#CDD5E7` | 205, 213, 231 | Table alternating rows, soft backgrounds |
| Medium Blue-Gray | `#8396C3` | 131, 150, 195 | Mid-tone accents, borders |
| Medium Blue | `#39569F` | 57, 86, 159 | H2 color, secondary headings |

**Signature gradient**: `#2DD6FF` → `#16F0DF` (Cyan to Mint Teal) — use for hero sections, dividers, accents.

### Typography

| Element | Font | Size (pt) | Weight | Color |
|---------|------|-----------|--------|-------|
| Document title | Urbanist | 36–48 | Bold (700) | Deep Navy |
| H1 | Urbanist | 28–32 | Bold (700) | Deep Navy |
| H2 | Urbanist | 22–26 | SemiBold (600) | Medium Blue |
| H3 | Urbanist | 18–22 | SemiBold (600) | Deep Navy |
| Body text | Inter | 11–12 | Regular (400) | Black |
| Captions / footnotes | Inter | 9–10 | Regular (400) | Gray |
| Data labels / KPIs | Inter | 14–18 | SemiBold (600) | Deep Navy |

### Logo

| File | Size | Use when |
|------|------|----------|
| `assets/logo_color.png` | 300×154px | Light or white backgrounds (most docs) |
| `assets/logo_allwhite.png` | Full wordmark, all white | Dark/navy backgrounds — **preferred for all dark surfaces including HTML UI** |
| `assets/logo_white.png` | 1216×173px | Legacy — use `logo_allwhite.png` instead |

---

## Application Rules

### Color Usage
- **Dark backgrounds**: Deep Navy bg + White text. Accent with Cyan or Mint Teal. Use `logo_white.png`.
- **Light backgrounds**: White bg + Deep Navy or Black text. Accent with Cyan or Mint Teal. Use `logo_color.png`.
- **Gradients**: Cyan → Mint Teal gradient is the signature element — use for hero sections, dividers, feature highlights.
- **Charts**: Cycle Deep Navy → Cyan → Mint Teal → Medium Blue → Medium Blue-Gray for data series.
- **Tables**: Light Lavender alternating rows. Deep Navy header row with White text.

### Logo Placement
1. Cover page: centered or left-aligned, above the title
2. Headers/footers: small (~1.5 inches wide), right-aligned
3. Never stretch, distort, or recolor the logo
4. Maintain clear space: minimum half the logo height on all sides
5. Dark background = always `logo_white.png` — never filter or reduce opacity of the color logo

### Presentation Slide Layouts

**Title slide**: Deep Navy full-bleed bg / `logo_white.png` centered upper third / Title: Urbanist Bold 36–44pt White centered / Subtitle: Inter Regular 18pt Cyan or Light Lavender

**Section divider**: Deep Navy bg / Section title: Urbanist Bold 32pt White centered / Cyan-to-Mint-Teal gradient bar (4px) below title

**Content slide**: White bg / Slide title: Urbanist SemiBold 24pt Deep Navy top-left / Full-width gradient accent bar (3px) below title / Body: Inter Regular 14–16pt Black / `logo_color.png` bottom-right footer (~0.8in wide)

**Data/chart slide**: White bg / Title: Urbanist SemiBold 24pt Deep Navy / Brand color cycle for chart series / KPI callout: Deep Navy bg, White text, Urbanist Bold number, Inter label

**Closing slide**: Deep Navy full-bleed / `logo_white.png` centered / CTA: Urbanist Bold 32pt White / Contact: Inter Regular 14pt Light Lavender

### Icons and Graphics
- Icons: line-weight (not filled), Deep Navy or Cyan. Recommended: Lucide icons.
- Illustrations: flat, geometric, clean. No 3D or skeuomorphic.
- Photography: professional business/tech imagery with cool blue tones.
- Dividers: Cyan-to-Mint-Teal gradient rule (2–4px). Never plain black or gray hairlines.

---

## Mandatory Checklist — Verify Before Delivering

- [ ] Step 0 was run — fonts installed in VM, font files staged in `fonts/`
- [ ] **Urbanist** used for ALL headings (not Arial, not Calibri)
- [ ] **Inter** used for ALL body text (not Arial, not Calibri)
- [ ] **Deep Navy (#072C87)** is the heading color (not black, not generic blue)
- [ ] **Logo** appears on cover/title slide (color version on light bg, white version on dark bg)
- [ ] **Cyan/Mint Teal accents** used for dividers, highlights, or decorative elements
- [ ] **Light Lavender (#CDD5E7)** used for alternating table rows
- [ ] **Gradient bar** (Cyan → Mint Teal) used as a section divider or accent
- [ ] **Font install reminder** appended at end of response
- [ ] No generic/default styling remains (no black headings, no Arial body, no gray table stripes)
- [ ] Presentations: title slide uses Deep Navy background with white logo
- [ ] Charts: data series follow brand color cycle (Deep Navy → Cyan → Mint Teal → Medium Blue → Medium Blue-Gray)

After delivering any document, always append this note:

> **Font check:** If headings or body text look wrong when you open the document, install the brand fonts (one-time setup). Font files are in your `fonts/` folder — double-click each `.ttf` and click "Install Font". Fonts persist across all future documents.

---

## Common Mistakes to Avoid

| Mistake | Correct approach |
|---------|-----------------|
| Using Arial as the primary font name in code | Always specify `"Urbanist"` or `"Inter"` by name; Arial only appears as the last entry in CSS font-family stacks |
| Black headings | Always use Deep Navy (`#072C87`) for headings |
| Gray or plain table header rows | Header rows: Deep Navy bg (`#072C87`) with White text |
| Generic gray table row stripes | Use Light Lavender (`#CDD5E7`) for alternating rows |
| Using `logo_color.png` on dark/navy backgrounds | Use `logo_white.png` on any dark background |
| CSS filter/opacity hacks on the color logo | Use the correct logo file for the background — never filter |
| Plain black or gray horizontal rules | Dividers must use the Cyan-to-Mint-Teal gradient |
| Skipping the cover page on multi-page docs | Every multi-page document requires a branded cover page |
| Forgetting font files in `fonts/` | Always copy `.ttf` files to workspace `fonts/` for teammates |
| Using emoji anywhere | Use inline SVG icons (line-weight, Deep Navy or Cyan) — never emoji |
| Using "RG" letter mark or square logo placeholder | Always use the full logo image (`logo_color.png` / `logo_white.png`) |
| Hype language in copy | No "revolutionary," "game-changing," "cutting-edge," "best-in-class" |

---

## Brand Voice & Tone

### Four Core Tones
Every piece of content should reflect at least one tone and ideally blend multiple naturally:

**1. Knowledgeable / Insight-Driven** — Authority backed by data and experience. Specific metrics and outcomes, not vague claims.
- Do: "Our attribution model connects 14 distinct touchpoint categories to pipeline progression"
- Don't: "We have the best attribution solution on the market"
- Phrases: "Based on our experience across 50+ implementations…", "The data consistently shows…"

**2. Solutions-Oriented** — Lead with outcomes, not features. Show the path from current state to desired state.
- Do: "We help you answer 'what's actually driving pipeline?' with confidence"
- Don't: "Our platform has 200+ integrations and real-time dashboards"
- Phrases: "Here's how we solve that…", "What this unlocks for your team…"

**3. Collaborative / Client-Centric** — Partner, not vendor. Building WITH them, not deploying AT them.
- Do: "We work alongside your team to design an attribution model that fits your sales cycle"
- Don't: "We'll install our proprietary attribution system in your org"
- Phrases: "In partnership with your team…", "We co-design…"

**4. Hands-On / Proactive** — RevOps Global does the work, not just advises. Anticipates needs.
- Do: "We build, test, and deploy the solution — your team gets trained on day one"
- Don't: "We provide a comprehensive recommendations document for your team to implement"
- Phrases: "We handle the build…", "Already in progress…"

### Channel Tone Weights

| Channel | Primary Tones |
|---------|---------------|
| Website service pages | Knowledgeable + Solutions-Oriented |
| Website case studies | Collaborative + Insight-Driven |
| LinkedIn posts | Insight-Driven + Hands-On |
| Email outreach | Solutions-Oriented + Collaborative |
| Proposals/SOWs | All four tones |
| Internal docs | Hands-On + Knowledgeable |

### Words to Avoid
"revolutionary," "game-changing," "cutting-edge," "next-gen," "our platform," "proprietary technology," "best-in-class," "businesses grow," "streamline your operations." Almost never use exclamation points.

---

## Brand Positioning

**Category**: Revenue Systems Engineering (not "RevOps consulting")

**Positioning**: RevOps Global engineers the systems, data infrastructure, and operational architecture that B2B companies need to scale revenue predictably — combining deep Salesforce/HubSpot expertise with strategic advisory.

**Differentiator**: Sits at the intersection of strategy and execution. Unlike pure consultants who advise and leave, or pure implementers who build without context — RevOps Global does both.

**Approved taglines**:
- "Engineer Your Revenue Engine"
- "Revenue Operations, Engineered"
- "Where Revenue Strategy Meets Technical Execution"

### Messaging Pillars

| Pillar | Claim | Proof |
|--------|-------|-------|
| Revenue Architecture | Design systems connecting marketing, sales, and CS into a unified revenue engine | Complex multi-object Salesforce builds, custom data models, integration architecture |
| Data-Driven Operations | Build the infrastructure for clean, connected, trustworthy data | Attribution modeling, pipeline analytics, reporting frameworks, data hygiene programs |
| Scalable Process Design | Design operational frameworks that scale with growth | Lead lifecycle design, territory planning, CPQ, renewal automation |
| Technology Enablement | Optimize and integrate tools so they actually work together | Salesforce/HubSpot optimization, MarTech integration, platform migrations |

### Rewrite Examples

| Instead of | Write |
|------------|-------|
| "We provide Salesforce consulting services to help you optimize your CRM." | "We architect Salesforce environments that give your revenue team a single source of truth — from lead capture through closed-won and beyond." |
| "Our team has deep expertise in marketing operations." | "We build the operational backbone that connects your marketing spend to pipeline — attribution models, lead scoring, campaign architecture, and the reporting to prove what's working." |
| "We help companies improve their sales processes." | "We design and implement the sales infrastructure your reps actually use — territory models, opportunity management, forecasting frameworks, and the automation that eliminates manual work." |

### Website Content Rules
1. Hero sections: lead with client's problem or desired outcome, not RevOps Global's capabilities
2. Section flow: Problem → Insight → Approach → Proof → CTA
3. CTAs: specific and action-oriented — "Book a Revenue Architecture Review" over "Contact Us"
4. Social proof: integrate inline, not as dedicated testimonial blocks
5. Technical depth: enough to earn credibility with RevOps practitioners, accessible to VP/C-level

---

## Code References

### docx-js (Node.js)

```javascript
import fs from 'fs';
import { Document, Packer, Paragraph, TextRun, ImageRun, Header, Footer,
         HeadingLevel, AlignmentType, BorderStyle, ShadingType, WidthType,
         Table, TableRow, TableCell, PageBreak } from 'docx';

// Brand colors (hex without #)
const DEEP_NAVY = "072C87";
const CYAN = "2DD6FF";
const MINT_TEAL = "16F0DF";
const BLACK = "000000";
const WHITE = "FFFFFF";
const GRAY = "8A91A2";
const LIGHT_LAVENDER = "CDD5E7";
const MEDIUM_BLUE_GRAY = "8396C3";
const MEDIUM_BLUE = "39569F";

// Brand fonts — MANDATORY
const HEADING_FONT = "Urbanist";  // NEVER change to Arial
const BODY_FONT = "Inter";        // NEVER change to Arial

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, font: HEADING_FONT, size: 32, bold: true, color: DEEP_NAVY })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun({ text, font: HEADING_FONT, size: 26, bold: true, color: MEDIUM_BLUE })]
  });
}

function heading3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text, font: HEADING_FONT, size: 22, bold: true, color: DEEP_NAVY })]
  });
}

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120 },
    children: [new TextRun({ text, font: BODY_FONT, size: 22, color: BLACK, ...opts })]
  });
}

function coverPage(title, subtitle, logoData) {
  return [
    new Paragraph({ spacing: { before: 2000 }, alignment: AlignmentType.CENTER,
      children: [new ImageRun({ data: logoData, type: 'png',
        transformation: { width: 200, height: 103 } })] }),
    new Paragraph({ spacing: { before: 600 }, alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: title, font: HEADING_FONT, size: 48, bold: true, color: DEEP_NAVY })] }),
    new Paragraph({ alignment: AlignmentType.CENTER,
      children: [new TextRun({ text: subtitle, font: BODY_FONT, size: 24, color: GRAY })] }),
    new Paragraph({ children: [new PageBreak()] })
  ];
}

function brandedTableRow(cells, isHeader = false) {
  return new TableRow({
    children: cells.map(text => new TableCell({
      shading: isHeader ? { type: ShadingType.SOLID, color: DEEP_NAVY } : undefined,
      children: [new Paragraph({
        children: [new TextRun({
          text, font: isHeader ? HEADING_FONT : BODY_FONT,
          size: isHeader ? 22 : 20,
          bold: isHeader, color: isHeader ? WHITE : BLACK
        })]
      })]
    }))
  });
}
```

### python-pptx

```python
from pptx.util import Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# Brand colors
DEEP_NAVY = RGBColor(0x07, 0x2C, 0x87)
CYAN = RGBColor(0x2D, 0xD6, 0xFF)
MINT_TEAL = RGBColor(0x16, 0xF0, 0xDF)
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GRAY = RGBColor(0x8A, 0x91, 0xA2)
LIGHT_LAVENDER = RGBColor(0xCD, 0xD5, 0xE7)
MEDIUM_BLUE_GRAY = RGBColor(0x83, 0x96, 0xC3)
MEDIUM_BLUE = RGBColor(0x39, 0x56, 0x9F)
CHART_COLORS = [DEEP_NAVY, CYAN, MINT_TEAL, MEDIUM_BLUE, MEDIUM_BLUE_GRAY]

# Brand fonts — MANDATORY
HEADING_FONT = "Urbanist"  # NEVER change to Arial
BODY_FONT = "Inter"        # NEVER change to Arial

def set_text(shape, text, font_name=BODY_FONT, size=Pt(14), color=BLACK, bold=False, alignment=PP_ALIGN.LEFT):
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = size
    run.font.color.rgb = color
    run.font.bold = bold

def add_gradient_bar(slide, top, width=Inches(10), height=Inches(0.04)):
    shape = slide.shapes.add_shape(1, Inches(0), top, width, height)
    shape.line.fill.background()
    fill = shape.fill
    fill.gradient()
    fill.gradient_stops[0].color.rgb = CYAN
    fill.gradient_stops[1].color.rgb = MINT_TEAL
```

### ReportLab (Python — PDF)

```python
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register brand fonts (run Step 0 first)
pdfmetrics.registerFont(TTFont('Urbanist', os.path.expanduser('~/.local/share/fonts/Urbanist-Variable.ttf')))
pdfmetrics.registerFont(TTFont('Inter', os.path.expanduser('~/.local/share/fonts/Inter-Variable.ttf')))

DEEP_NAVY = HexColor('#072C87')
CYAN = HexColor('#2DD6FF')
MINT_TEAL = HexColor('#16F0DF')
BLACK = HexColor('#000000')
WHITE = HexColor('#FFFFFF')
GRAY = HexColor('#8A91A2')
LIGHT_LAVENDER = HexColor('#CDD5E7')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('RG_Title', fontName='Urbanist', fontSize=36, textColor=DEEP_NAVY, spaceAfter=20, leading=42))
styles.add(ParagraphStyle('RG_H1', fontName='Urbanist', fontSize=24, textColor=DEEP_NAVY, spaceAfter=12, spaceBefore=24, leading=30))
styles.add(ParagraphStyle('RG_H2', fontName='Urbanist', fontSize=18, textColor=HexColor('#39569F'), spaceAfter=10, spaceBefore=18, leading=22))
styles.add(ParagraphStyle('RG_Body', fontName='Inter', fontSize=11, textColor=BLACK, spaceAfter=8, leading=16))
styles.add(ParagraphStyle('RG_Caption', fontName='Inter', fontSize=9, textColor=GRAY, spaceAfter=6, leading=12))

RG_TABLE_STYLE = TableStyle([
    ('FONTNAME', (0, 0), (-1, 0), 'Urbanist'),
    ('FONTNAME', (0, 1), (-1, -1), 'Inter'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('BACKGROUND', (0, 0), (-1, 0), DEEP_NAVY),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_LAVENDER]),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
])
```

### openpyxl (Python — XLSX)

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

DEEP_NAVY = "072C87"
CYAN = "2DD6FF"
MINT_TEAL = "16F0DF"
WHITE = "FFFFFF"
LIGHT_LAVENDER = "CDD5E7"
GRAY = "8A91A2"
HEADING_FONT = "Urbanist"
BODY_FONT = "Inter"

header_font = Font(name=HEADING_FONT, size=12, bold=True, color=WHITE)
header_fill = PatternFill(start_color=DEEP_NAVY, end_color=DEEP_NAVY, fill_type="solid")
body_font = Font(name=BODY_FONT, size=11, color="000000")
alt_row_fill = PatternFill(start_color=LIGHT_LAVENDER, end_color=LIGHT_LAVENDER, fill_type="solid")
thin_border = Border(
    left=Side(style='thin', color=GRAY), right=Side(style='thin', color=GRAY),
    top=Side(style='thin', color=GRAY), bottom=Side(style='thin', color=GRAY)
)

def style_header_row(ws, row=1, col_count=10):
    for col in range(1, col_count + 1):
        cell = ws.cell(row=row, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = thin_border

def style_data_rows(ws, start_row=2, end_row=100, col_count=10):
    for row in range(start_row, end_row + 1):
        for col in range(1, col_count + 1):
            cell = ws.cell(row=row, column=col)
            cell.font = body_font
            cell.border = thin_border
            if row % 2 == 0:
                cell.fill = alt_row_fill
```

### HTML/CSS

```css
@import url('https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
  --rg-deep-navy: #072C87;
  --rg-cyan: #2DD6FF;
  --rg-mint-teal: #16F0DF;
  --rg-black: #000000;
  --rg-white: #FFFFFF;
  --rg-gray: #8A91A2;
  --rg-light-lavender: #CDD5E7;
  --rg-medium-blue-gray: #8396C3;
  --rg-medium-blue: #39569F;
  --rg-heading-font: 'Urbanist', system-ui, Arial, sans-serif;
  --rg-body-font: 'Inter', system-ui, Arial, sans-serif;
  --rg-gradient: linear-gradient(135deg, #2DD6FF, #16F0DF);
}

h1, h2, h3, h4, h5, h6 { font-family: var(--rg-heading-font); color: var(--rg-deep-navy); }
body, p, li, td, th { font-family: var(--rg-body-font); color: var(--rg-black); }
h1 { font-size: 2.25rem; font-weight: 700; }
h2 { font-size: 1.75rem; font-weight: 600; color: var(--rg-medium-blue); }
h3 { font-size: 1.375rem; font-weight: 600; }

.rg-accent-bar { height: 4px; background: var(--rg-gradient); border: none; border-radius: 2px; }

.rg-table { width: 100%; border-collapse: collapse; }
.rg-table th {
  background: var(--rg-deep-navy); color: var(--rg-white);
  font-family: var(--rg-heading-font); font-weight: 600;
  padding: 10px 14px; text-align: left;
}
.rg-table td { padding: 8px 14px; border-bottom: 1px solid var(--rg-light-lavender); }
.rg-table tr:nth-child(even) { background: var(--rg-light-lavender); }

.rg-kpi { background: var(--rg-deep-navy); color: var(--rg-white); border-radius: 8px; padding: 20px; text-align: center; }
.rg-kpi .number { font-family: var(--rg-heading-font); font-size: 2.5rem; font-weight: 700; }
.rg-kpi .label { font-family: var(--rg-body-font); font-size: 0.875rem; color: var(--rg-light-lavender); margin-top: 4px; }
```

### React / Tailwind

```jsx
const RG_BRAND = {
  deepNavy: '#072C87',
  cyan: '#2DD6FF',
  mintTeal: '#16F0DF',
  gray: '#8A91A2',
  lightLavender: '#CDD5E7',
  mediumBlue: '#39569F',
  headingFont: "'Urbanist', system-ui, Arial, sans-serif",
  bodyFont: "'Inter', system-ui, Arial, sans-serif",
  gradient: 'linear-gradient(135deg, #2DD6FF, #16F0DF)',
};

// Google Fonts (add to <head>):
// <link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

---

## Step 0 — Font Setup (Run Before Every Document)

Run this silently before generating any branded artifact. Do not narrate it to the user.

```bash
# Install fonts in VM for document rendering
mkdir -p ~/.local/share/fonts

# Locate skill assets
SKILL_DIR=""
for candidate in \
  "$(dirname "$(readlink -f "$0" 2>/dev/null)" 2>/dev/null)/assets" \
  "$(find /sessions -path '*/revops-global-brand/assets' -type d 2>/dev/null | head -1)" \
  "$(find "$HOME" -path '*/.claude/skills/revops-global-brand/assets' -type d 2>/dev/null | head -1)" \
  "$(find . -path '*/revops-global-brand/assets' -type d 2>/dev/null | head -1)"; do
  [ -n "$candidate" ] && [ -d "$candidate" ] && [ -f "$candidate/Urbanist-Variable.ttf" ] && SKILL_DIR="$candidate" && break
done

if [ -n "$SKILL_DIR" ]; then
  cp "$SKILL_DIR/Urbanist-Variable.ttf" ~/.local/share/fonts/
  cp "$SKILL_DIR/Inter-Variable.ttf" ~/.local/share/fonts/
else
  # Fall back to Google Fonts CDN
  curl -sL -o ~/.local/share/fonts/Urbanist-Variable.ttf \
    "https://raw.githubusercontent.com/google/fonts/main/ofl/urbanist/Urbanist%5Bwght%5D.ttf"
  curl -sL -o ~/.local/share/fonts/Inter-Variable.ttf \
    "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"
fi
fc-cache -f

# Stage font files in user's workspace
WORKSPACE=""
if [ -d "/sessions" ]; then
  for mnt in /sessions/*/mnt/*/; do
    [ -d "$mnt" ] && WORKSPACE="$mnt" && break
  done
fi
[ -z "$WORKSPACE" ] && WORKSPACE="."

mkdir -p "$WORKSPACE/fonts"
cp ~/.local/share/fonts/Urbanist-Variable.ttf "$WORKSPACE/fonts/" 2>/dev/null
cp ~/.local/share/fonts/Inter-Variable.ttf "$WORKSPACE/fonts/" 2>/dev/null

# Verify
fc-list | grep -iq urbanist && echo "Urbanist installed" || echo "WARNING: Urbanist MISSING — fallback to Arial"
fc-list | grep -iq inter && echo "Inter installed" || echo "WARNING: Inter MISSING — fallback to Arial"
```

### Teammate Font Installation (One-Time)

**macOS**: Open `fonts/` folder → double-click `Urbanist-Variable.ttf` → click "Install Font" in Font Book → repeat for `Inter-Variable.ttf`.

**Windows**: Open `fonts/` folder → right-click `Urbanist-Variable.ttf` → "Install for all users" → repeat for `Inter-Variable.ttf`.

Word, PowerPoint, and other desktop apps require fonts installed locally to render documents correctly. The VM installs fonts for generation; the person opening the file needs them locally too.

---

## Component Library

A production-ready component library built on **shadcn/ui + Framer Motion + Tailwind CSS**, styled with RevOps Global brand tokens. Browse at `docs/component-library/index.html` (local) or reference React components in `docs/component-library/components/`.

### Installation
```bash
# Install dependencies
npm install framer-motion @radix-ui/react-dialog lucide-react clsx tailwind-merge

# Initialize shadcn/ui (if not already)
npx shadcn@latest init

# Add base components
npx shadcn@latest add button badge input table dialog
```

### Brand Token Import
```typescript
import { RG } from '@/components/revops/index';
// RG.navy = '#072C87', RG.cyan = '#2DD6FF', etc.
```

### Available Components

| Component | File | Use When |
|-----------|------|----------|
| `<KpiCard>` | `kpi-card.tsx` | Showing metrics with trend (navy/light/gradient variants) |
| `<ScoreCircle>` | `score-circle.tsx` | ICP scores, health scores, any 0-100 value |
| `<AiInsightBox>` | `ai-insight-box.tsx` | Showing AI-generated analysis below data |
| `<DataTable>` | `data-table.tsx` | All tabular data — inherits brand header + alt rows |
| `<StatusBadge>` | `status-badge.tsx` | HIGH/MED/LOW risk, MVP/Post-MVP, Completed/Running |
| `<SidebarNav>` | `sidebar-nav.tsx` | App navigation with sections, badges, user footer |
| `<TabBar>` | `tab-bar.tsx` | Tab switching (underline or pill variant) |
| `<CommandPalette>` | `command-palette.tsx` | ⌘K global search/navigation |
| `<AttributionBarChart>` | `attribution-bar-chart.tsx` | Horizontal bar charts with animated fill |
| `<FunnelChart>` | `funnel-chart.tsx` | Pipeline/attribution funnels |
| `<AlertBanner>` | `alert-banner.tsx` | error/warning/success/info alerts |
| `<PlayRunningState>` | `play-running-state.tsx` | Play execution progress UI |
| `<ConnectorCard>` | `connector-card.tsx` | CRM/MAP integration cards |
| `<OutputHeader>` | `output-header.tsx` | Play output page header with metadata |

### Design Principles from 21st.dev Patterns

1. **Animated entry** — Use `framer-motion` `initial/animate` on all data components. KPI numbers count up. Charts animate width/height on mount.
2. **Hover elevation** — Cards use `whileHover={{ y: -2, boxShadow }}` for lift effect.
3. **Active state animation** — TabBar uses `layoutId` for smooth indicator movement.
4. **Brand gradient** — Cyan (`#2DD6FF`) → Mint Teal (`#16F0DF`) gradient is the signature element. Use on progress bars, borders, accent lines — sparingly.
5. **No emojis** — All icons are `lucide-react` icons or inline SVGs. Never use emoji in components.
6. **Type safety** — All components fully typed. Use discriminated unions for `variant` props.

### Quick Usage Example
```tsx
import { KpiCard, ScoreCircle, AiInsightBox, StatusBadge } from '@/components/revops';

export function PipelineDashboard() {
  return (
    <div className="grid grid-cols-4 gap-4">
      <KpiCard
        variant="navy"
        label="Pipeline at Risk"
        value="$847K"
        delta="+23%"
        deltaDirection="up"
        subText="3 deals flagged"
      />
      <KpiCard
        variant="light"
        label="ICP Accounts Scored"
        value="47"
        delta="+12 new"
        deltaDirection="up"
      />
      <ScoreCircle score={94} label="TechVault Inc" size="md" animated />
      <StatusBadge variant="high" />
    </div>
  );
}
```

---

## Related Skills

> **Always use these together.** This skill and `revops-component-library` are two halves of the same system.

| Skill | When to reach for it |
|-------|----------------------|
| **`revops-global-brand`** ← you are here | Brand colors (hex values, named palette), typography rules (Urbanist/Inter), logo usage, cover page standards, SVG icon rules. Use when producing any RevOps-branded artifact — presentations, documents, reports, HTML pages. |
| **`revops-component-library`** | React/TSX component code, Tailwind token classes, CSS variable system, shadcn/ui patterns. Use when writing or reviewing any UI code for RGOS, RevOps AI Portal, or RevOps Global AI. |

**Rule:** The brand skill defines the *why* (design intent, hex values, logo rules). The component library defines the *how* (Tailwind classes, component APIs, token names). For any UI code task, load both. For documents and static artifacts, this skill is sufficient on its own.

**Token bridge — how brand colors map to Tailwind classes:**

| Brand color | Hex | Tailwind class |
|------------|-----|----------------|
| Deep Navy | `#072C87` | `text-primary` / `bg-primary` |
| Cyan | `#2DD6FF` | `text-accent` / `bg-accent` |
| Mint Teal | `#16F0DF` | `text-teal` / `bg-teal` |
| Brand Grey | `#8A91A2` | `text-muted-foreground` |
| Tint Light | `#CDD5E7` | `brand-tint-light` |

**Visual reference:** `team-brain/docs/component-library/index.html` — open in browser for live previews of all 89 components.

---

## Skill Notes

### What Works Well

**2026-03-10 — Google Docs paragraph spacing standard (tight, confirmed by Greg)**

Use these `spaceAbove` / `spaceBelow` values (in PT) for all branded Google Docs:

| Element | spaceAbove | spaceBelow |
|---------|-----------|-----------|
| Document title (H1) | 2 | 2 |
| Subtitle / date | 4 | 4 |
| Divider line (━━━) | 6 | 6 |
| Section heading (H2, e.g. MEETING GOAL) | 10 | 4 |
| Body paragraph | 4 | 4 |
| Agenda item / numbered heading | 10 | 2 |
| Bullet point | 1 | 1 |
| Decision / checklist item | 3 | 3 |
| Footer | 2 | 2 |

Keep `lineSpacing` unset (inherits Google Docs default 115%). Do not set explicit line spacing unless instructed.

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

- **2026-03-10** — In Google Docs, the RevOps Global logo ALWAYS goes in the document header (via `insertInlineImage` with `segmentId` = the header ID), never inline in the body. Use `logo_color.png` on light backgrounds. Aspect ratio 1.9481:1 — at 100pt wide, height = 51pt.
- **2026-03-10** — The standard logo to use is `Revops_Main_Logo_Color@3x.png` from Google Drive: `/Users/gregharned/Library/CloudStorage/GoogleDrive-greg@revopsglobal.com/My Drive/RevOps Global/RevOps Website Brand/Logo Design/Main Logo/Revops_Main_Logo_Color@3x.png`. Dimensions 3486×690px, ratio 5.0522:1. At 120pt wide, height = 24pt. This supersedes `logo_color.png` from the skill assets for Google Docs.

### Lessons Learned
<!-- What went wrong and what to do instead -->

- **2026-03-10** — First attempt used Arial instead of Urbanist/Inter and placed the logo inline in the body. Both are wrong. Always use `"Urbanist"` and `"Inter"` by name in all API font family fields (Google Docs supports them as Google Fonts). Always insert the logo into the document header, not the body.
