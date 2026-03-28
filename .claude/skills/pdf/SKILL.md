---
name: pdf
library: true
description: Use this skill whenever the user wants to do anything with PDF files.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Tool Decision — Choose Before Writing Any Code

Apply the matching rule and use that tool. Do not default to pypdf for everything.

| If the task is... | Use this tool |
|---|---|
| Merge, split, rotate, watermark, encrypt/decrypt | **pypdf** |
| Extract text with layout preserved | **pdfplumber** |
| Extract tables (especially multi-column) | **pdfplumber** |
| Create a new PDF from scratch | **reportlab** |
| Fill an existing PDF form | **pdf-lib** or pypdf — read FORMS.md first |
| OCR a scanned PDF (image-based, no selectable text) | **pytesseract + pdf2image** |
| Quick command-line merge/split/decrypt | **qpdf** |
| Quick command-line text extraction | **pdftotext (poppler-utils)** |
| Advanced pypdfium2 features | See REFERENCE.md |
| JavaScript environment | See REFERENCE.md |

If the task involves **filling a PDF form**, stop here and read FORMS.md before continuing — forms have their own process.

---

## pypdf — Merge, Split, Rotate, Watermark, Encrypt

### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Split PDF (one file per page)
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Rotate Pages
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()
page = reader.pages[0]
page.rotate(90)  # 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Password Protect
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")
with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

### Extract Metadata
```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}, Author: {meta.author}")
```

---

## pdfplumber — Text and Table Extraction

### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### Extract Tables
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

### Extract Tables → Excel
```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

---

## reportlab — Create PDFs from Scratch

### Basic PDF
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter
c.drawString(100, height - 100, "Hello World!")
c.line(100, height - 140, 400, height - 140)
c.save()
```

### Multi-Page PDF with Styled Content
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

story.append(Paragraph("Report Title", styles['Title']))
story.append(Spacer(1, 12))
story.append(Paragraph("Body content here.", styles['Normal']))
story.append(PageBreak())
story.append(Paragraph("Page 2", styles['Heading1']))

doc.build(story)
```

### Subscripts and Superscripts — Critical Rule

**Never use Unicode subscript/superscript characters (₀₁₂, ⁰¹²) in ReportLab PDFs.** Built-in fonts do not include these glyphs — they render as solid black boxes.

Use ReportLab XML markup tags instead:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font size and position — do not use Unicode superscripts/subscripts.

---

## OCR — Scanned PDFs

Use when the PDF contains images of text, not selectable text.

```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

images = convert_from_path('scanned.pdf')
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

---

## Command-Line Tools

### qpdf
```bash
# Merge
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages 1-5
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf

# Rotate page 1 by 90 degrees
qpdf input.pdf output.pdf --rotate=+90:1

# Decrypt
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftotext (poppler-utils)
```bash
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt   # preserve layout
pdftotext -f 1 -l 5 input.pdf output.txt # pages 1-5
```

### pdfimages (poppler-utils) — Extract Images
```bash
pdfimages -j input.pdf output_prefix
# produces: output_prefix-000.jpg, output_prefix-001.jpg, ...
```

### pdftk (if available)
```bash
pdftk file1.pdf file2.pdf cat output merged.pdf
pdftk input.pdf burst          # split
pdftk input.pdf rotate 1east output rotated.pdf
```

---

## Reference

- Advanced pypdfium2 usage → REFERENCE.md
- JavaScript libraries (pdf-lib) → REFERENCE.md
- Troubleshooting → REFERENCE.md
- PDF form filling → FORMS.md (read before attempting)

---

## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
