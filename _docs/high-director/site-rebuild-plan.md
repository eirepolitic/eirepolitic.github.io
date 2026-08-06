---
title: Documentation Site Rebuild Plan
summary: Persistent implementation plan for rebuilding the site as a structured technical knowledge base.
section: high-director
doc_type: agent
status: active
created: 2026-08-05
updated: 2026-08-05
last_verified: 2026-08-05
order: 20
permalink: /projects/high-director/site-rebuild-plan/
---

# Documentation Site Rebuild Plan

The initial rebuild of the Eire Politic documentation site is complete.

## Operating rules

- Use branches and pull requests for material changes.
- Preserve established public URLs where practical.
- Never commit secrets or confidential information.
- Follow `DOCUMENTATION_STANDARD.md`.
- Validate changes before merging.
- Verify the Pages deployment after merging.

## Completed steps

- **Step 0 — Record the plan:** Complete — 2026-08-05, PR #2
- **Step 1 — Documentation standard:** Complete — 2026-08-05, PR #3
- **Step 2 — Jekyll collection foundation:** Complete — 2026-08-05, PR #4
- **Step 3 — Migrate and normalize documentation:** Complete — 2026-08-05, PR #5
- **Step 4 — Data-driven navigation:** Complete — 2026-08-05, PR #6
- **Step 5 — Documentation layout and design system:** Complete — 2026-08-05, PR #7
- **Step 6 — Homepage redesign:** Complete — 2026-08-05, PR #8
- **Step 7 — Client-side search:** Complete — 2026-08-05, PR #9
- **Step 8 — Indexes and relationships:** Complete — 2026-08-05, PR #10
- **Step 9 — Documentation quality validation:** Complete — 2026-08-05, PR #11
- **Step 10 — Operational documentation:** Complete — 2026-08-05, PR #12
- **Step 11 — Final cleanup and release:** Complete — 2026-08-05, PR #13

Step 11 added a custom 404 page, a final architecture summary, stronger keyboard focus and reduced-motion behavior, small-screen safeguards, and removal of obsolete placeholder files.

## Final architecture

- Hosting: GitHub Pages
- Generator: Jekyll
- Technical content: `_docs/`
- Metadata standard: `DOCUMENTATION_STANDARD.md`
- Navigation model: `_data/docs_sections.yml`
- Search: generated JSON index and browser JavaScript
- Validation: `scripts/validate_docs.py` and GitHub Actions
- Operations guide: Documentation Site Operations runbook
- Architecture reference: Documentation Site Architecture

## Future work

Future work should be tracked as normal documentation or a new focused build plan rather than extending this completed rebuild plan.

Potential optional improvements:

- Add repository and system documentation as projects are reviewed.
- Decide whether dark mode is useful.
- Decide whether archived documents should remain in default search results.
- Add selected homepage features when active repositories are documented.

## Continuation note for a new chat

Read `DOCUMENTATION_STANDARD.md`, Documentation Site Operations, Documentation Site Architecture, and the latest merged pull requests. Create a new focused plan for any substantial future initiative.
