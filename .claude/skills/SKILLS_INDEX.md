# Skills Index

**Last updated:** 2026-03-23

A machine-readable catalog of all available agent skills. Organized by category for fast discovery.

---

## How Agents Should Use This Index

**Leader agents (Phase 0 — before decomposing work):**
Read this index before breaking a request into tasks. If an existing skill covers the work, reference it in the task description rather than inventing a bespoke approach. This prevents reinventing patterns the team has already codified.

**Worker agents (before executing a task):**
Read the task description, then scan this index for skills that accelerate execution. Invoke via the `Skill` tool: `skill: "skill-name"`. A matching skill gives you proven patterns, org-specific context, and quality calibrations — use it. Once you identify a matching skill, read its SKILL.md before invoking — the one-liner describes when to use it, not how.

**After identifying a reusable pattern:**
If you discover a pattern worth reusing, write a skill proposal using the template at `templates/skill-proposal-template.md`, then raise it for review.

---

## Business Strategy & Advisory

- **brainstorming** — Explore divergent ideas and creative options before committing to any direction on a feature, component, or design decision
- **launch-strategy** — Plan a product launch, feature announcement, or release strategy
- **marketing-ideas** — Generate marketing ideas, inspiration, or strategies for a SaaS or software product
- **pricing-strategy** — Make pricing decisions, design packaging, or develop monetization strategy
- **outbound-meeting-engine** — Holistic GTM plan for RevOps Global to generate 3–5 qualified meetings per week
- **free-tool-strategy** — Plan, evaluate, or build a free tool for marketing purposes (lead gen, SEO, brand awareness)
- **referral-program** — Create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy
- **operations-change-management** — Plan and execute organizational or technical changes
- **operations-compliance-tracking** — Track compliance requirements and audit readiness
- **operations-process-optimization** — Analyze and improve business processes
- **operations-resource-planning** — Plan and optimize resource allocation
- **operations-risk-assessment** — Identify, assess, and mitigate operational risks
- **operations-vendor-management** — Evaluate, compare, and manage vendor relationships
- **four-pillars-scoring** — Semi-automate the RevOps Global maturity assessment

---

## Sales & Customer

- **sales-account-research** — Research a company or person for actionable sales intel, with or without enrichment tools
- **sales-call-prep** — Prepare for a sales call with account context, attendee research, and suggested agenda
- **sales-competitive-intelligence** — Research competitors and build an interactive battlecard
- **sales-create-an-asset** — Generate tailored sales assets (landing pages, decks, one-pagers, workflow demos) from deal context
- **sales-daily-briefing** — Start the day with a prioritized sales briefing based on meetings and priorities
- **sales-draft-outreach** — Research a prospect then draft personalized outreach
- **sales-signal-outreach** — Weekly LinkedIn signal scan that finds 1st-degree connections with buying signals, scores them, drafts messages, and opens compose windows pre-filled for review
- **customer-support-customer-research** — Research customer questions by searching documentation and knowledge bases
- **customer-support-escalation** — Package support escalations for engineering, product, or leadership with full context
- **customer-support-knowledge-management** — Write and maintain knowledge base articles from resolved support issues
- **customer-support-response-drafting** — Draft professional, empathetic customer-facing responses adapted to the situation and channel
- **customer-support-ticket-triage** — Triage incoming support tickets by categorizing issues, assigning priority, and recommending routing

---

## Engineering & Development

- **app-development** — Architecture and engineering patterns for building robust application features
- **systematic-debugging** — Use when encountering any bug, test failure, error, or unexpected behavior — before proposing fixes
- **test-driven-development** — Write tests first, then implementation — for any feature or bugfix
- **verification-before-completion** — Run verification commands before claiming work is complete, fixed, or passing
- **requesting-code-review** — Package completed work for review and verify it meets the original requirements
- **receiving-code-review** — Process incoming code review feedback before implementing suggestions
- **finishing-a-development-branch** — Use when implementation is complete and you need to decide how to integrate the work
- **using-git-worktrees** — Isolate feature work from the current workspace before executing implementation plans
- **supabase-postgres-best-practices** — Postgres performance optimization and best practices from Supabase
- **vite** — Vite build tool configuration, plugin API, SSR, and Vite 8 Rolldown migration
- **vercel-react-best-practices** — React and Next.js performance optimization guidelines from Vercel Engineering
- **vercel-composition-patterns** — React composition patterns that scale
- **salesforce-cli** — Drive programmatic Salesforce work in client orgs using the Salesforce CLI (sf)
- **salesforce-flow-builder** — Build, debug, and optimize Salesforce Flows (record-triggered, scheduled, screen, and autolaunched)
- **salesforce-integration-architecture** — Design and implement scalable integration patterns, select middleware, and build resilient data flows
- **salesforce-cpq-configuration** — Configure Salesforce CPQ for accurate quoting, pricing rules, and approval workflows
- **mcp-builder** — Create high-quality MCP servers that enable LLMs to interact with external services
- **mcp2cli** — Turn any MCP server or OpenAPI spec into a CLI for terminal-based interaction
- **add-team-mcp** — Add a new MCP server so the whole RevOps Global team can use it across all repos
- **rgos-platform** — Interact with the RGOS internal platform (clients, projects, time logging, tasks, dashboard)
- **playwright-cli** — Token-efficient Playwright CLI for UAT, E2E tests, and browser interaction (4x fewer tokens than MCP)
- **webapp-testing** — Test and debug local web apps running on localhost via Playwright
- **agent-browser** — Browser automation CLI built for AI agents — navigate, click, fill forms, screenshot, scrape
- **browser-use** — General-purpose browser automation for web testing, form filling, and data extraction
- **tmux** — Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output

---

## RevOps & CRM Platform

- **revops-context** — Load RevOps Global's organizational context, methodology, and institutional knowledge
- **revops-data-visualization** — Generate publication-ready, branded data visualizations (charts, dashboards, SVG/HTML) using RevOps Global brand colors and typography
- **revops-knowledge-base** — Query RevOps Global's institutional knowledge base (626 items from client meeting transcripts)
- **revops-tech-stack-audit** — Inventory tools, measure overlap, assess integration health, evaluate ROI, and build consolidation strategy
- **revops-attribution-modeling** — RevOps Global's Attribution Modeling engagement methodology — Pillar 2 of the Four Pillars
- **revenue-attribution-modeling** — Select attribution models, implement Salesforce Campaign Influence, and measure marketing pipeline contribution
- **revops-buying-group** — Design and implement buying group automation for B2B companies that sell to committees
- **lifecycle-modeling** — RevOps Global's Lifecycle Modeling engagement methodology — Pillar 1 of the Four Pillars
- **hubspot-audit** — Audit a HubSpot portal before or during a client engagement
- **hubspot-to-salesforce-migration** — Plan and execute CRM migrations from HubSpot to Salesforce
- **salesforce-org-audit** — Audit a new or existing Salesforce org before or during a client engagement
- **salesforce-data-cleanup** — Consolidate duplicates, normalize field values, and audit field utilization in Salesforce
- **salesforce-data-model-relationships** — Understand and design Salesforce data model relationships using industry standards
- **salesforce-lead-scoring** — Design and implement lead scoring models in Salesforce that align sales and marketing on lead quality
- **salesforce-dashboard-strategy** — Design executive, manager, rep, marketing, and CS dashboards with the right KPIs
- **sf-pipeline-snapshot** — Automate end-to-end setup of Salesforce Pipeline Snapshot reporting for a client org
- **building-salesforce-campaigns** — Architect Salesforce Campaigns that properly track marketing influence on pipeline and revenue
- **marketo-audit** — Audit an Adobe Marketo Engage instance before or during a client engagement
- **eloqua-audit** — Audit an Oracle Eloqua instance before or during a client engagement
- **martech-maturity-audit** — Conduct a comprehensive MarTech Maturity Audit spanning both MAP and CRM
- **audit-data-extraction** — Programmatically extract audit metrics from client CRM and MAP instances using provisioned credentials
- **database-hygiene** — Audit, clean, or recommend ongoing maintenance for a client's CRM or MAP database
- **renewal-expansion-playbooks** — Automate renewal opportunity creation, track expansion, and forecast renewals accurately

---

## Data & Analytics

- **data-data-exploration** — Profile and explore datasets to understand shape, quality, and patterns before analysis
- **data-data-validation** — QA an analysis before sharing — methodology checks, accuracy verification, bias detection
- **data-data-visualization** — Create effective data visualizations with Python (matplotlib, seaborn, plotly)
- **data-interactive-dashboard-builder** — Build self-contained interactive HTML dashboards with Chart.js, dropdown filters, and professional styling
- **data-sql-queries** — Write correct, performant SQL across all major data warehouse dialects
- **data-statistical-analysis** — Apply statistical methods including descriptive stats, trend analysis, outlier detection, and hypothesis testing
- **data-data-context-extractor** — Generate or improve a company-specific data analysis skill by extracting tribal knowledge from analysts
- **analytics-tracking** — Set up, improve, or audit analytics tracking and measurement implementation
- **ab-test-setup** — Plan, design, or implement an A/B test or experiment with statistically valid results

---

## Content, Marketing & SEO

- **copywriting** — Write, rewrite, or improve marketing copy for any page (homepage, landing, pricing, features)
- **copy-editing** — Edit, review, or improve existing marketing copy
- **humanizer** — Remove signs of AI-generated writing from text using Wikipedia's 25-pattern detection guide
- **brand-guidelines** — Apply *Anthropic's* brand colors and typography (not RevOps Global's) to artifacts
- **marketing-brand-voice** — Apply and enforce brand voice, style guide, and messaging pillars across content
- **marketing-campaign-planning** — Plan marketing campaigns with objectives, audience segmentation, channel strategy, and success metrics
- **marketing-competitive-analysis** — Research competitors and compare positioning, messaging, content strategy, and market presence
- **marketing-psychology** — Apply psychological principles, mental models, or behavioral science to marketing
- **social-content** — Create, schedule, or optimize social media content for LinkedIn, Twitter/X, Instagram, TikTok
- **email-sequence** — Create or optimize email sequences, drip campaigns, automated email flows, or lifecycle email programs
- **paid-ads** — Plan and optimize paid advertising campaigns on Google Ads, Meta, LinkedIn, or other ad platforms
- **content-strategy** — Plan a content strategy, decide what content to create, or figure out what topics to cover
- **seo-audit** — Audit, review, or diagnose SEO issues on a site
- **seo-content-rewrite** — Full-page SEO and content audit for B2B WordPress homepages using a 7-agent parallel system across 3 zones
- **programmatic-seo** — Create SEO-driven pages at scale using templates and data
- **schema-markup** — Add, fix, or optimize schema markup and structured data on a site
- **competitor-alternatives** — Create competitor comparison or alternative pages for SEO and sales enablement
- **seo-slide-decks** — SEO and social media optimization for slide decks published on SlideShare, Scribd, LinkedIn
- **audit-website** — Audit websites for SEO, performance, security, technical, and content issues (230+ rules)
- **internal-comms** — Write all kinds of internal communications using company-preferred formats
- **kb-extract** — Extract institutional knowledge from Fathom meeting transcripts and append to the RevOps Global knowledge base

---

## UI/UX & Frontend

- **frontend-design** — Create distinctive, production-grade frontend interfaces with high design quality
- **teach-impeccable** — One-time setup that gathers and saves project design context (audience, brand, tone) before any design work
- **adapt** — Adapt designs to work across different screen sizes, devices, contexts, or platforms
- **animate** — Add purposeful animations, micro-interactions, and motion effects to improve feel and feedback
- **arrange** — Improve layout, spacing, and visual rhythm — fix monotonous grids, inconsistent spacing, weak hierarchy
- **audit** — Comprehensive design audit across accessibility, performance, theming, responsive design, and anti-patterns
- **bolder** — Amplify safe or boring designs to make them more visually interesting and impactful
- **clarify** — Improve unclear UX copy, error messages, microcopy, labels, and instructions
- **colorize** — Add strategic color to monochromatic or low-interest interfaces
- **critique** — Evaluate design effectiveness from a UX perspective — visual hierarchy, IA, clarity, and conversion
- **delight** — Add moments of joy, personality, and unexpected touches that make interfaces memorable
- **distill** — Strip designs to their essence by removing unnecessary complexity
- **extract** — Extract and consolidate reusable components, design tokens, and patterns into a design system
- **harden** — Improve interface resilience through error handling, i18n support, text overflow, and edge cases
- **normalize** — Normalize design to match your design system and ensure visual consistency
- **onboard** — Design or improve onboarding flows, empty states, and first-time user experiences
- **optimize** — Improve interface performance across loading speed, rendering, animations, and bundle size
- **overdrive** — Push interfaces past conventional limits with technically ambitious, highly creative implementations
- **polish** — Final quality pass before shipping — fixes alignment, spacing, consistency, and detail issues
- **quieter** — Tone down overly bold or visually aggressive designs while maintaining design quality
- **typeset** — Improve typography: fix font choices, hierarchy, sizing, weight consistency, and readability
- **ui-design-system** — Create and maintain scalable design systems
- **ui-ux-pro-max** — UI/UX design intelligence — 50 styles, 21 palettes, 50 font pairings, 20 charts, 9 stacks
- **mobile-design** — Mobile-first design thinking and decision-making for iOS and Android apps
- **web-design-guidelines** — Review UI code for Web Interface Guidelines compliance
- **critique** — Design critique for catching generic AI-generated aesthetics, visual hierarchy issues, and UX anti-patterns
- **audit** — Technical UI audit for accessibility (WCAG 2.1 AA), performance (Core Web Vitals), and responsive design
- **web-artifacts-builder** — Create elaborate, multi-component HTML artifacts using React, Tailwind, and modern web technologies
- **revops-component-library** — Build production-quality UI components for RevOps Global products using the branded component library
- **form-cro** — Optimize any non-signup form (lead capture, contact, demo request) for conversion
- **page-cro** — Optimize or increase conversions on any marketing page (homepage, landing, pricing, features)
- **popup-cro** — Create or optimize popups, modals, overlays, slide-ins, or banners for conversion
- **signup-flow-cro** — Optimize signup, registration, account creation, or trial activation flows
- **onboarding-cro** — Optimize post-signup onboarding, user activation, first-run experience, or time-to-value
- **paywall-upgrade-cro** — Create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates
- **canvas-design** — Create beautiful visual art in .png and .pdf documents using design philosophy
- **theme-factory** — Style artifacts (slides, docs, reports, HTML pages) with one of 10 preset themes
- **revops-vector-art** — Create professional SVG vector illustrations in RevOps Global's distinctive flat, clean style
- **revops-global-brand** — Apply RevOps Global's official brand colors and typography to any artifact
- **revops-wp-page** — Build and deploy production-ready WordPress page content for revopsglobal.com

---

## Productivity & Tools

- **productivity-memory-management** — Two-tier memory system for workplace context — decodes shorthand, acronyms, and internal language
- **productivity-task-management** — Simple task management using a shared TASKS.md file
- **apple-reminders** — Manage Apple Reminders via the `remindctl` CLI on macOS
- **reminder-processor** — Process AI-completable tasks from Apple Reminders using subagent delegation
- **superhuman** — Manage email in Superhuman (check, read, reply, send, archive, search)
- **nlm-skill** — Expert guide for the NotebookLM CLI (nlm) and MCP server — create notebooks, add sources, generate podcasts, reports, and more
- **open-brain-weekly-review** — Weekly synthesis of captured Open Brain thoughts — surfaces patterns and open action items
- **cowork-debrief** — Extract and capture Open Brain insights from a Cowork session
- **trello** — Manage Trello boards, lists, and cards via the Trello REST API
- **spotify-player** — Control Spotify from the terminal via spogo or spotify_player CLI
- **sonoscli** — Control Sonos speakers via CLI — discover devices, play/pause/skip, adjust volume
- **gws-meta-workflows** — Six production-ready meta-workflows chaining Google Workspace CLI (gws) commands for inbox triage, meeting prep, client onboarding, weekly digests, email security scanning, and scheduling conflict resolution
- **claude-chat-best-practices** — Best practices for using Claude chat at RevOps Global
- **claude-code-best-practices** — Best practices for using Claude Code at RevOps Global
- **cowork-best-practices** — Best practices for using Claude Cowork at RevOps Global
- **prompting-guide** — Practical guide to writing effective prompts for Claude, with good vs bad examples

---

## Skill Creation & Orchestration

- **skill-creator** — Build, improve, test, and debug Claude agent skills (SKILL.md files)
- **writing-skills** — Create new SKILL.md files, edit or improve existing skills, audit the skill library
- **skills-vs-plugins** — Explains the difference between Claude Skills and plugins, when to create each
- **find-skills** — Discover and install agent skills when you don't know what's available
- **dispatching-parallel-agents** — Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
- **subagent-driven-development** — Execute implementation plans with multiple independent tasks in parallel within the current session
- **multi-instance-orchestration** — Orchestrate multiple Claude Code instances in a leader/worker pattern
- **executing-plans** — Execute a written implementation plan step-by-step with reversibility checks
- **writing-plans** — Create an implementation plan before touching code — for multi-step tasks from a spec or feature request
- **qa-playbook** — Comprehensive QA playbook covering unit, integration, E2E, visual, performance, and security testing

---

## Document & Deliverable Generation

- **pdf** — Read, extract, combine, or manipulate PDF files
- **pdf-processing-pro** — Production-ready PDF processing with forms, tables, OCR, validation, and batch operations
- **docx** — Create, read, edit, or manipulate Word documents (.docx files)
- **pptx** — Create, edit, convert, or work with PowerPoint presentations (.pptx files)
- **xlsx** — Open, read, edit, analyze, or create spreadsheet files
- **sow-creator** — Create professional Statement of Work PDFs for RevOps Global client engagements
- **slide-deck-storytelling** — Content balance, storytelling, visual hierarchy, and narrative flow for slide decks
- **doc-coauthoring** — Guide users through a structured workflow for co-authoring documentation
- **product-management-feature-spec** — Write structured PRDs with problem statements, user stories, requirements, and success metrics
- **product-management-roadmap-management** — Plan and prioritize product roadmaps using RICE, MoSCoW, and ICE frameworks
- **product-management-stakeholder-comms** — Draft stakeholder updates tailored to audience (executives, engineering, customers)
- **product-management-user-research-synthesis** — Synthesize qualitative and quantitative user research into structured insights
- **product-management-metrics-tracking** — Define, track, and analyze product metrics with goal-setting and dashboard design frameworks
- **product-management-competitive-analysis** — Analyze competitors with feature comparison matrices, positioning analysis, and strategic implications
- **product-marketing-context** — Create or update the product marketing context document

---

## Misc & Specialized

- **remotion** — Build, edit, or debug video compositions with Remotion (React-based programmatic video)
- **remotion-best-practices** — Apply correct patterns and avoid common mistakes when writing or reviewing Remotion code
- **video-creation** — Create videos programmatically using Higgsfield AI and Remotion
- **elevenlabs** — Generate speech and sound effects via the ElevenLabs API
- **slack-gif-creator** — Create animated GIFs optimized for Slack (constraints, validation, animation concepts)
- **nano-banana-pro** — Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro)
- **playground** — Create interactive HTML playgrounds — self-contained single-file explorers with visual configuration
- **algorithmic-art** — Create algorithmic art using p5.js with seeded randomness and interactive parameter exploration
- **ralph-tui-prd** — Generate a Product Requirements Document (PRD) for ralph-tui task orchestration
- **supreme-optimization-brand** — Apply Supreme Optimization's official brand colors and typography to any artifact
- **seo-page-audit** — Run a full SEO page audit and copy rewrite for a client: keyword research, competitive analysis, recommended structure, visual HTML deliverable, and source citations
- **utmstandard-brand** — Apply UTMStandard's official brand, typography, components, and voice to any artifact

---

## Maintenance

**When creating a new skill:**
1. Add it to the appropriate category section above
2. Format: `- **{skill-name}** — {one-line purpose describing when to use it}`
3. Update the "Last updated" date at the top of this file

**When deleting a skill:**
Remove its entry from the index and update the "Last updated" date.

**When significantly changing a skill's purpose:**
Update its entry to reflect the new trigger contexts — stale entries cause agents to miss or misuse skills.

**When reorganizing categories:**
Keep categories broad enough that each has 5+ skills. Prefer 10–15 categories total. If a skill fits two categories, place it in the most specific one.

**This file lives in `.claude/skills/` but is NOT itself a skill** — it has no YAML frontmatter and should not be invoked via the `Skill` tool.

- **open-brain-to-kb** — Promote high-signal Open Brain thoughts to the permanent RevOps Global knowledge base.
- **revops-google-doc** — Create and brand Google Docs for RevOps Global client engagements via gws CLI, with logo, Urbanist/Inter typography, and Navy/Cyan palette.
- **churn-prevention** — Design and audit SaaS churn prevention systems — cancel flows, save offer playbooks, exit surveys, and dunning sequences.
- **revops-cro-frameworks** — Strategic revenue frameworks for CRO-level analysis and client advisory covering ARR waterfall mechanics, NRR analysis, and expansion revenue.
- **scenario-war-room** — Model cascading what-if scenarios across multiple simultaneous business variables for risk and opportunity analysis.
- **ob1-paper-illustrations** — Create paper cut-out SVG illustrations for ob1-app using the 5-7 layer depth system, P palette, and animation patterns.
- **ob1-paper-illustrations** — Create paper cut-out SVG illustrations for ob1-app using the 5-7 layer depth system, P palette, and animation patterns.

- **autoresearch-diagrams** — Self-improving diagram prompt optimization using the Karpathy autoresearch pattern.
- **skill-autoresearch** — Self-improving SKILL.md optimization using the Karpathy autoresearch pattern. Supports eval_mode: vision (renders SVG/TSX output to PNG via cairosvg for visual evaluation). Requires cairosvg + system cairo for vision mode. Use max_tokens: 2048 for skills that produce SVG components.
- **skill-label** — Human-in-the-loop labeling tool for skill outputs — renders SVGs and serves a browser UI for visual review.
- **ob1-garden-planner** — Week-by-week garden planner for ob1-app, calibrated to zip code 98642 (Ridgefield/Washougal, Zone 8b).
- **ob1-garden-planner** — Week-by-week garden planner for ob1-app, calibrated to zip code 98642 (Ridgefield/Washougal, Zone 8b).
- **greg-social-media** — LinkedIn & Reddit thought leadership: post drafting, commenting, and engagement sessions.
- **artisan-stopmotion** — Stop-motion video production system based on the Wes Anderson "Isle of Dogs" sushi scene aesthetic.
- **inbox-zero** — Draft replies to all of today's emails in Greg's voice using Superhuman MCP.
- **multimodal-ingest** — Ingest any file or URL (PDFs, images, URLs) into the Open Brain pipeline for knowledge capture.
