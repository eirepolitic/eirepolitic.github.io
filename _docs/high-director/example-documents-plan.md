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

- [x] Repository — `eirepolitic.github.io` documentation drafted from the live repository and verified source files.
- [ ] System
- [ ] Data & Schema
- [ ] Runbook
- [ ] Architecture Decision
- [ ] High Director
- [ ] Note
- [ ] Archive

## Current Step

Repository example is in review on branch `high-director/example-repository-eirepolitic-github-io`.

## Next Safe Action

Validate and merge the repository example, confirm Pages deployment, then create the system-category example using the existing documentation-site architecture as the source of truth.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: completed template initiative, `main`, repository tree, `_templates/repository-template.md`, `_docs/high-director/site-architecture.md`, and `_docs/runbooks/documentation-site-operations.md`
- Verified by: High Director
- Verification scope: phase scope, repository example source material, validation requirement, and deployment requirement
