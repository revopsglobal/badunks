---
name: cowork-best-practices
library: true
description: Best practices for using Claude Cowork at RevOps Global.---

# Cowork Best Practices — RevOps Global

How our team uses Cowork to automate tasks on our local machines.

## What Is Cowork?

Cowork is Claude running on your desktop with the ability to interact with your local files, apps, and system. It's like having an assistant who can actually open your files, move things around, process documents, and work with the apps on your Mac.

It's different from Claude chat (which can only talk) and Claude Code (which works with GitHub repos). Cowork works with whatever's on your computer right now.

## Getting Started

Cowork runs as a desktop application. Once installed, it connects to Claude and can access files and folders you give it permission to work with.

**Important:** Cowork sometimes has reliability quirks — authentication popups and timeouts can happen. If Cowork stops responding or asks you to re-authenticate, just follow the prompts. If it times out on a long task, you may need to restart it and pick up where you left off.

## The Golden Rules

### 1. Start with Plan Mode

Yes, this applies to Cowork too. Every tool in the Claude family works better when you plan first.

> "I have 50 PDF invoices in my Downloads folder. Plan how you would extract the vendor name, date, and amount from each one and put them in a spreadsheet."

### 2. Be Clear About File Locations

Always tell Cowork exactly where your files are. Use full paths or be very specific.

**Bad example:**
> "Process my invoices."

**Good example:**
> "In ~/Documents/Q4-Invoices/, there are 50 PDF files. Each one has a vendor name on page 1, an invoice date, and a total amount. Extract these three fields from each PDF and create a CSV file on my Desktop called Q4_invoice_summary.csv."

### 3. Start Small, Then Scale

When doing batch operations, always test on one or two files first before processing the whole batch.

> "Try this on just the first two files in the folder so I can check the output before we do all 50."

### 4. Keep an Eye on It

Cowork is powerful but it's still a beta product. For important tasks, check in periodically to make sure it's still running and producing the right output. Don't kick off a huge job and walk away for an hour without checking.

## When to Use Cowork

- **Batch file processing** — renaming, organizing, converting files
- **Data extraction from local documents** — pulling info from PDFs, spreadsheets, docs
- **Local file creation** — generating reports, documents, or spreadsheets on your machine
- **System tasks** — organizing folders, cleaning up downloads, file management
- **Working with apps on your Mac** — interacting with local applications

## When NOT to Use Cowork

- **Quick questions or brainstorming** → Use Claude chat
- **Working with GitHub repos** → Use Claude Code
- **Tasks that need internet research** → Use Claude chat with web search
- **Anything involving sensitive credentials** → Be cautious about what files you expose

## Common Workflows for Our Team

### Processing Client Documents
```
"In ~/Documents/ClientName/, I have a folder of signed contracts (PDFs). 
For each one, extract the client name, contract start date, end date, 
and annual value. Create a summary spreadsheet on my Desktop."
```

### Organizing Downloads
```
"Look at my ~/Downloads folder. Move all PDFs to ~/Documents/PDFs, 
all spreadsheets to ~/Documents/Spreadsheets, and all images to 
~/Pictures. Delete any .dmg files older than 30 days."
```

### Creating Reports from Local Data
```
"I have a CSV file at ~/Desktop/pipeline_data.csv. Create a formatted 
Word document summarizing the key metrics: total pipeline value, 
average deal size, and top 5 deals by value. Save it as 
~/Documents/Reports/Pipeline_Summary.docx."
```

## Dealing with Common Issues

**Authentication popups:** If Cowork shows an auth popup, just follow the prompts to re-authenticate. This happens occasionally and is a known issue.

**Timeouts on long tasks:** If a task takes too long and Cowork seems stuck, you may need to restart it. Try breaking the task into smaller chunks next time.

**Permission issues:** Make sure Cowork has access to the folders you want it to work with. You may need to grant permissions in System Settings.

## Pro Tips

1. **Cowork is great for "glue" tasks** — things that connect different file types or move data between formats. CSV to formatted report, raw data to organized folders, etc.

2. **Use it for repetitive manual work** — anything you'd do by hand in Finder or a text editor over and over is a good Cowork candidate.

3. **Combine with Claude chat** — plan your approach in Claude chat, then execute with Cowork. You can even paste instructions from a chat conversation into Cowork.

4. **For dedicated automation**, consider running Cowork on a dedicated machine (like a Mac Mini) so it doesn't interfere with your daily work.

## Keywords
Cowork, desktop automation, local files, file management, batch processing, RevOps Global


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
