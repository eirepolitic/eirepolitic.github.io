---
title: Example Documents Phase
summary: Build one verified real-world documentation example for each top-level documentation category and refine templates only when real usage exposes defects.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 40
permalink: /projects/high-director/example-documents-plan/
related:
  - /projects/high-director/documentation-section-template-plan/
---

# Example Documents Phase

## Purpose

Create one real, verified documentation example for each top-level documentation category using existing repositories, systems, pipelines, datasets, operational procedures, architecture decisions, High Director work, notes, or archived work.

Templates should be refined only when real usage exposes a concrete defect.

## Working Rules

- Use real implemented or historical work; do not invent artificial examples.
- Work in small reviewable pull requests.
- Run documentation validation before every merge.
- Confirm GitHub Pages deployment after every merged documentation change.
- Update this plan after every meaningful step.
- Do not change information architecture, security boundaries, or cost-bearing infrastructure without a separate decision.

## Category Progress

- [x] Repository — `eirepolitic.github.io`; PR #20 merged, validation `31137389854` passed, Pages deployment `31137413142` succeeded.
- [x] System — Eire Politic Documentation Site drafted from the live implementation and verified architecture.
- [ ] Data & Schema
- [ ] Runbook
- [ ] Architecture Decision
- [ ] High Director
- [ ] Note
- [ ] Archive

## Current Step

System example is in review on branch `high-director/example-system-documentation-site`.

## Next Safe Action

Validate and merge the system example, confirm Pages deployment, then create the Data & Schema example from the real generated documentation search index or documentation metadata model.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: completed template initiative, PR #20, validation run `31137389854`, Pages run `31137413142`, `main`, repository tree, `_templates/system-template.md`, and `_docs/high-director/site-architecture.md`
- Verified by: High Director
- Verification scope: repository example completion, system example source material, validation requirement, and deployment requirement
