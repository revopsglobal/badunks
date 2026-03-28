---
name: rgos-platform
library: true
library_category: Session Foundation
description: This skill should be used when the user asks to "check on clients", "list projects", "log time", "create a task", "show the dashboard", "update a project", "log a touchpoint", "show my time entries", "search RGOS", "list the team", "show invoices", "update client health", or any other query about RevOps Global platform data.
version: 1.0.0
---

# RGOS Platform — RevOps Global Connector

Connect to the RevOps Global platform to manage clients, projects, tasks, time tracking, invoices, and team data using natural language. All 16 tools support **fuzzy name matching** — use plain names like "Acme" or "Greg" instead of UUIDs.

## Available Tools (16)

### Clients

- **rgos_list_clients** — List all clients with health status, contract value, renewal dates. Optional filters: `status` (active/churned/at_risk), `type` (retainer/project/advisory).
- **rgos_get_client** — Deep dive on one client: contacts, active projects, recent touchpoints, financial summary. Pass `client_name` (fuzzy matched).
- **rgos_update_client** — Update health_status, contract_value, renewal_date, or type. Pass `client_name` + fields to change.
- **rgos_log_touchpoint** — Record a client interaction. Pass `client_name`, `type` (call/meeting/email/escalation), `subject`, and optional `notes`.

### Projects

- **rgos_list_projects** — List projects. Optional filters: `client_name`, `status` (active/on_hold/completed/cancelled), `risk_level`.
- **rgos_get_project** — Project detail: hours budget vs actual, team members, open tasks, financial summary. Pass `project_name`.
- **rgos_update_project** — Update status, risk_level, budget_hours, monthly_fee, start_date, end_date. Pass `project_name` + fields.

### Tasks

- **rgos_list_tasks** — List tasks. Filters: `project_name`, `client_name`, `assignee_name`, `status` (todo/in_progress/completed/blocked), `priority` (low/medium/high/urgent).
- **rgos_create_task** — Create a task. Required: `project_name`, `title`. Optional: `assignee_name`, `priority`, `due_date`, `description`.
- **rgos_update_task** — Update task status, priority, assignee, due_date. Pass `task_name` + fields.

### Time Tracking

- **rgos_log_time** — Log hours. Required: `project_name`, `hours`. Optional: `task_name`, `date` (defaults to today), `description`, `billable` (defaults true).
- **rgos_list_time** — View time entries. Filters: `team_member_name`, `project_name`, `start_date`, `end_date`.

### Dashboard & Search

- **rgos_dashboard** — Quick business overview: client health breakdown, total hours this week, overdue tasks, upcoming renewals, revenue summary.
- **rgos_search** — Cross-entity keyword search across clients, projects, and tasks. Pass `query` string.
- **rgos_list_team** — Team members with roles, email, and active project count.
- **rgos_list_invoices** — Invoices with filters: `client_name`, `status` (draft/sent/paid/overdue).

## How to Use

When the user asks about RGOS data, pick the right tool and call it directly. Key patterns:

**Quick overview** → `rgos_dashboard`
**Find something** → `rgos_search` with keywords
**Client questions** → `rgos_get_client` or `rgos_list_clients`
**Project questions** → `rgos_get_project` or `rgos_list_projects`
**Task management** → `rgos_list_tasks`, `rgos_create_task`, or `rgos_update_task`
**Time logging** → `rgos_log_time` (always confirm hours and project before logging)
**Record client interaction** → `rgos_log_touchpoint`

## Name Resolution

All name parameters use fuzzy matching. Use the most distinctive part of the name:
- "Acme" matches "Acme Corp" or "Acme Industries"
- "HubSpot" matches "HubSpot Migration Q1"
- "Greg" matches "Greg Harned"

If multiple matches are found, the tool returns all candidates — present them and ask the user to pick one.

## Important Rules

1. **Confirm before writes.** Always confirm with the user before calling update, create, or log tools.
2. **Use today's date** for time logging unless the user specifies otherwise.
3. **Hours are decimal.** 30 minutes = 0.5, not "30 min".
4. **Billable by default.** Time entries default to billable unless the user says otherwise.
5. **Format currency** with $ and commas (e.g., $12,500).
6. **Present data cleanly.** Use tables for lists, summaries for single-entity views.

For detailed tool schemas and parameters, see `references/tool-reference.md`.


## Skill Notes

### What Works Well
<!-- Confirmed patterns — repeat these -->

### Calibrations
<!-- Subtle preferences Greg consistently nudges — pre-apply these next time -->

### Lessons Learned
<!-- What went wrong and what to do instead -->
