---
name: revops-google-doc
library: true
description: Create and brand Google Docs for RevOps Global client engagements — meeting agendas, FRDs, briefs, SOWs, and any other client-facing documents.---

# Skill: RevOps Global Google Doc Builder

## Critical Rules

1. **Always use `gws docs documents batchUpdate`** — never try to edit doc content directly via the Drive API.
2. **Logo goes in the document header, not the body.** Use `createHeader` + `insertInlineImage` at index 0 of the header segment.
3. **Insert all text first, then apply styles.** Text insertion shifts indices — apply `updateTextStyle` and `updateParagraphStyle` in a second batch after reading fresh indices.
4. **Always re-read the doc after insertions** to get accurate character indices before styling.
5. **Never guess indices** — always use `full_text.find(s) + 1` to locate content.

---

## Brand Specification

### Colors (exact rgbColor values)
```python
NAVY = {"red": 0.027, "green": 0.173, "blue": 0.529}   # #072C87 — headings, titles
CYAN = {"red": 0.176, "green": 0.839, "blue": 1.0}     # #2DD6FF — dividers, accents
GREY = {"red": 0.541, "green": 0.569, "blue": 0.635}   # subtitles, metadata
```

### Typography
| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Document title | Urbanist | 26pt | Bold | Navy |
| Section headings | Urbanist | 13pt | Bold | Navy |
| Sub-headings / agenda items | Urbanist | 12pt | Bold | Navy |
| Body text | Inter | 10pt | Regular | Black |
| Dates / metadata | Inter | 10–11pt | Regular | Grey |
| Divider line | Inter | 5pt | Regular | Cyan |

### Divider Line
Use this Unicode character string as a visual divider between sections:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
Style it: Inter, 5pt, Cyan color.

### Logo
- **Drive URI:** `https://drive.google.com/uc?id=1IMkc9ZXr5rxPGymsAuNCBRY60crT5qvB&export=download`
- **Size:** height 23.75pt, width 120pt
- **Position:** Document header, index 0

### Reference Doc
`1Rr2kVFfOO589FcEbCDZomOPxcSHmYsr-EFoDMUGXb_w` — Acceleration Academies FRD. Inspect this doc to verify styling when uncertain.

---

## Standard Document Structure

```
[HEADER: Logo]

[Title — Urbanist 26pt Navy Bold]
[Date / subtitle — Inter 11pt Grey]
━━━━━━━ [Cyan divider] ━━━━━━━

[SECTION HEADING — Urbanist 13pt Navy Bold]
[Body content — Inter 10pt]

[SECTION HEADING — Urbanist 13pt Navy Bold]
1. [Agenda item — Urbanist 12pt Navy Bold]
   [Description — Inter 10pt]
```

---

## Step-by-Step Workflow

### 1. Create the doc
```bash
gws docs documents create --json '{"title": "Doc Title Here"}'
# Returns documentId — save this
```

### 2. Insert all text content in one batch
```python
requests = [{"insertText": {"location": {"index": 1}, "text": full_content}}]
```
Insert the complete text content at index 1 (start of body). Use `\n` for line breaks.

### 3. Create header and insert logo
```python
# Create header first
resp = upd(doc_id, [{"createHeader": {"type": "DEFAULT"}}])
header_id = resp["replies"][0]["createHeader"]["headerId"]

# Insert logo at index 0 of the header segment
upd(doc_id, [{
    "insertInlineImage": {
        "location": {"segmentId": header_id, "index": 0},
        "uri": "https://drive.google.com/uc?id=1IMkc9ZXr5rxPGymsAuNCBRY60crT5qvB&export=download",
        "objectSize": {
            "height": {"magnitude": 23.75, "unit": "PT"},
            "width":  {"magnitude": 120.0, "unit": "PT"}
        }
    }
}])
```

### 4. Re-read doc and apply styles
```python
doc = get_doc(doc_id)
full_text = "".join(
    el["textRun"]["content"]
    for block in doc["body"]["content"] if "paragraph" in block
    for el in block["paragraph"].get("elements", []) if "textRun" in el
)

def find(s):
    idx = full_text.find(s)
    return idx + 1, idx + 1 + len(s)

# Apply text styles
def ts(s, e, font, size, bold=False, color=NAVY):
    return {"updateTextStyle": {
        "range": {"startIndex": s, "endIndex": e},
        "textStyle": {
            "bold": bold,
            "fontSize": {"magnitude": size, "unit": "PT"},
            "foregroundColor": {"color": {"rgbColor": color}},
            "weightedFontFamily": {"fontFamily": font, "weight": 700 if bold else 400},
        },
        "fields": "bold,fontSize,foregroundColor,weightedFontFamily"
    }}
```

### 5. Add hyperlinks
```python
def link(s, e, url, color=NAVY):
    return {"updateTextStyle": {
        "range": {"startIndex": s, "endIndex": e},
        "textStyle": {
            "link": {"url": url},
            "foregroundColor": {"color": {"rgbColor": color}},
        },
        "fields": "link,foregroundColor"
    }}
```

---

## Common Document Types

### Meeting Agenda
Structure: Title → Date → Divider → Attendees → Agenda (numbered items) → Materials (linked)

### FRD / Brief
Structure: Title → Client → Date → Divider → Meeting Goal → Divider → Agenda → Open Decisions → Next Steps

### SOW
Use the `sow-creator` skill instead — it generates a full PDF with proper legal structure.

---

## gws CLI Reference

```bash
# Create doc
gws docs documents create --json '{"title": "..."}'

# Batch update (insert text, apply styles, insert image)
gws docs documents batchUpdate \
  --params '{"documentId": "DOC_ID"}' \
  --json '{"requests": [...]}'

# Read doc (for fresh indices)
gws docs documents get --params '{"documentId": "DOC_ID"}'
```

---

## Skill Notes

### What Works Well
- Insert full text in one `insertText` call at index 1, then style in a second pass — cleanest approach
- Logo at header index 0 (not 1) — `createHeader` reply gives headerId, insert immediately
- Divider lines with `━` characters styled to 5pt Cyan are visually clean and match brand exactly
- Always re-read the doc to get fresh indices before any styling batch

### Lessons Learned
- **2026-03-10:** `insertInlineImage` fails silently if URI is inaccessible or index is wrong — always verify by checking `inlineObjects` in a subsequent `get` call
- **2026-03-10:** Header element `startIndex` may be `None` in API response — use index 0 for the header segment, not 1
- **2026-03-10:** For spreadsheets, ALWAYS duplicate tabs first (`duplicateSheet`) and write ONLY to tabs with "v2" in the name. Never edit originals in place. Verify tab name contains "v2" before every write.
