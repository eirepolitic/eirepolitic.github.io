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
- [x] System — Eire Politic Documentation Site; PR #21 merged, validation `31137496390` passed, Pages deployment `31137516088` succeeded.
- [x] Data & Schema — Documentation Search Index; PR #22 merged, validation `31137604054` passed, Pages deployment `31137621658` succeeded.
- [x] Runbook — Publish a Documentation Change; PR #23 merged, validation `31137737015` passed, Pages deployment `31137754183` succeeded.
- [x] Architecture Decision — Use Metadata-Driven Static Documentation on GitHub Pages drafted from the implemented site architecture.
- [ ] High Director
- [ ] Note
- [ ] Archive

## Current Step

Architecture Decision example is in review on branch `high-director/example-decision-static-documentation`.

## Next Safe Action

Validate and merge the Architecture Decision example, confirm Pages deployment, then review this persistent phase plan against the High Director template and use it as the real High Director example.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: PRs #20 through #23; validation runs `31137389854`, `31137496390`, `31137604054`, and `31137737015`; Pages runs `31137413142`, `31137516088`, `31137621658`, and `31137754183`; `_templates/decision-template.md`; implemented documentation-site architecture
- Verified by: High Director
- Verification scope: repository, system, data, and runbook example completion; architecture decision source material; validation requirement; deployment requirement
