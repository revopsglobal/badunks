---
name: claude-code-best-practices
library: true
description: Best practices for using Claude Code at RevOps Global.---

# Claude Code Best Practices — RevOps Global

How our team uses Claude Code to work with repositories, build tools, and ship code.

## What Is Claude Code?

Claude Code is Claude with the ability to read, write, and execute code in a cloud environment connected to your GitHub repositories. Think of it as having a developer on your team who can actually open your codebase, make changes, run tests, and push commits.

It's different from regular Claude chat because it can:
- Access and modify files in your GitHub repos
- Run commands and scripts
- Create pull requests
- Work with your actual codebase, not just talk about code in the abstract

## Getting Started

### Connecting to Our Org

Claude Code connects to our **RevOps-Global** GitHub organization. When you open Claude Code, make sure you're pointed at the right repo (you'll see the repo name and branch in the bottom left of the interface).

If you see a prompt to install the Claude GitHub app, it needs to be installed on the **RevOps-Global** org — not any other organization.

### The Cloud Environment

Our cloud environment ("GitHub RevOps Global") is configured with:
- **Full network access** — Claude Code can reach external APIs and services
- **Environment variables** — API keys and credentials are stored here securely (ask Greg if you need access)

## The Golden Rules

### 1. Always Use Plan Mode First

Just like with Claude chat — but even more important here because Claude Code can actually make changes to your files. Start every task by asking Claude to plan its approach before writing any code.

> "Plan how you would add a pipeline snapshot trigger to this Salesforce project. Don't make any changes yet."

### 2. Work on Branches, Not Main

Always have Claude Code work on a feature branch. Never make changes directly to `main`. 

> "Create a new branch called feature/pipeline-snapshots and make the changes there."

### 3. Review Before Committing

Claude Code can create commits and PRs, but always review what it's done before merging. Use the diff view to check changes, and don't be shy about asking Claude to explain why it made specific choices.

### 4. Be Explicit About Scope

Tell Claude Code exactly which files or areas of the codebase to focus on. Without direction, it might make changes in places you didn't expect.

**Bad example:**
> "Fix the bug."

**Good example:**
> "In the file src/triggers/OpportunitySnapshot.trigger, there's an issue where the snapshot isn't capturing the Amount field. Fix just that field mapping — don't change anything else."

## When to Use Claude Code

- **Building or modifying code in a GitHub repo** — Apex classes, triggers, LWC components, scripts
- **Creating new files or project structures** — scaffolding out a new project
- **Code review and refactoring** — "Review this class and suggest improvements"
- **Debugging with access to the actual code** — "This test is failing, figure out why"
- **Creating PRs with proper descriptions** — Claude can write the PR summary too
- **Building skills for our team-brain repo** — meta, but true

## When NOT to Use Claude Code

- **Quick questions about code** → Regular Claude chat is faster
- **Working with local files on your Mac** → Use Cowork instead
- **Non-code tasks** (writing, analysis, brainstorming) → Use Claude chat
- **Sensitive credentials** → Never paste passwords or tokens into the chat; use the environment variables config instead

## Common Workflows for Our Team

### Creating a New Skill
```
1. "Create a new skill in the skills/ directory called [skill-name]"
2. "Write the SKILL.md with the following purpose: [describe it]"
3. "Add any reference files it needs in a references/ subdirectory"
4. "Commit and push to a new branch, then create a PR"
```

### Working on Salesforce Code
```
1. "Switch to the salesforce-src repo, branch: feature/my-feature"
2. "Plan the changes needed for [describe the task]"
3. Review the plan
4. "Go ahead and implement it"
5. "Run the tests and fix any failures"
6. "Create a PR with a description of what changed and why"
```

## Pro Tips

1. **Claude Code remembers conversation context** — you can iteratively refine code across multiple messages, just like in chat.

2. **You can paste error messages** — if something breaks, paste the full error and Claude Code will diagnose it with access to your actual code.

3. **Use it for documentation too** — Claude Code is great at writing README files, inline comments, and documentation that lives alongside your code.

4. **Ask it to explain existing code** — New to a repo? Ask Claude Code to walk you through what a file or function does.

## Keywords
Claude Code, GitHub, coding, repositories, RevOps Global, development, pull requests


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
