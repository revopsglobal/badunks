---
name: find-skills
library: true
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.---

# Find Skills

## When to Use This Skill

Use when the user:
- Says "find a skill for X", "is there a skill for X", or "can you do X"
- Asks "how do I do X" where X sounds like a discrete, reusable capability
- Wants to search for tools, templates, or workflows
- Expresses interest in extending agent capabilities

---

## What is the Skills CLI?

`npx skills` is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

```bash
npx skills find [query]       # Search by keyword
npx skills add <package>      # Install a skill
npx skills check              # Check for updates
npx skills update             # Update all installed skills
```

Browse all skills at: https://skills.sh/

---

## Local Skill Library

Before searching externally, check the local library for team-specific skills:

```bash
ls /Users/gregharned/work/team-brain/.claude/skill-library/   # 143 specialty skills
ls /Users/gregharned/work/team-brain/.claude/command-library/  # 317 slash commands
```

Categories available: salesforce, hubspot, marketo, eloqua, operations, marketing, sales, SEO, CRO, data analytics (da-*), lifecycle, attribution, and RevOps methodology playbooks.

---

## Step 1: Extract Domain and Task

Identify two things from the user's request:
1. **Domain** — React, testing, Salesforce, design, deployment, etc.
2. **Task** — writing tests, reviewing PRs, creating changelogs, etc.

If the request is vague ("can you help me?"), ask one clarifying question before searching.

---

## Step 2: Search

Run the find command with the most specific terms available:

```bash
npx skills find [domain] [task]
```

Examples:
- "How do I make my React app faster?" → `npx skills find react performance`
- "Can you help me with PR reviews?" → `npx skills find pr review`
- "I need a changelog" → `npx skills find changelog`

The command returns results in this format:
```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

---

## Step 3: Decision — Exact, Partial, or No Match

### If exact match found (skill clearly covers the request):
Present it directly with the install command and a one-sentence description of what it does. Offer to install.

```
I found a skill for this: "vercel-react-best-practices" — React and Next.js
performance optimization guidelines from Vercel Engineering.

Install it:
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

Want me to install it now?
```

### If partial match found (skill covers part of the request):
Present the closest matches with honest descriptions of the gap. Let the user decide which is most useful. Offer to install the best fit and proceed with the gap using general capabilities.

```
I found a skill that covers most of this: [name] handles [X] but not [Y].

Install it:
npx skills add [package]

I can handle [Y] directly. Want me to install the skill and then address [Y]?
```

### If no match found:
Acknowledge it clearly, offer to help directly, and suggest creating a custom skill if this is a recurring need.

```
I searched for skills related to "[query]" but didn't find any matches.

I can still help with this directly — want me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-[name]-skill
```

---

## Step 4: Install (if the user confirms)

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` installs globally (user-level). `-y` skips confirmation prompts.

---

## Search Tips

- Use specific terms: "react testing" over "testing"
- Try alternatives if the first search fails: "deploy" → "deployment" or "ci-cd"
- Common sources: `vercel-labs/agent-skills`, `ComposioHQ/awesome-claude-skills`

### Common categories and search terms

| Category | Example Queries |
|----------|----------------|
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |

---

## Edge Cases

- **Multiple strong matches**: List all, ask the user which fits their context before installing
- **Request too broad**: Ask one scoping question before searching ("Are you looking for X or Y?")
- **User wants to browse**: Direct them to https://skills.sh/ to explore by category


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
