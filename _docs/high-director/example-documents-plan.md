---
title: Example Documents Phase
summary: Track verified real-world examples for every documentation category and preserve the exact continuation state for future High Director sessions.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
repository: eirepolitic.github.io
system: Eire Politic Documentation Site
order: 40
permalink: /projects/high-director/example-documents-plan/
related:
  - /projects/high-director/documentation-section-template-plan/
  - /projects/decisions/use-metadata-driven-static-documentation/
---

# Example Documents Phase

## Purpose

Create one real, verified documentation example for each top-level category and give future High Director sessions an exact continuation point. Real usage should expose template defects; templates must not be changed merely to make examples look more complete.

## Current State

Six category examples are merged and deployed: Repository, System, Data & Schema, Runbook, Architecture Decision, and High Director. The Note example is being reviewed on branch `high-director/example-note-validation-findings`.

Archive is the only remaining category after the Note example.

## Scope

### Included

- Repository: `eirepolitic.github.io`.
- Technical documentation under `_docs/`.
- Existing documentation templates under `_templates/` as reference material only.
- Documentation validation workflow and GitHub Pages deployment evidence.
- One real example for each of the eight top-level documentation categories.

### Excluded

- Artificial examples.
- Unnecessary template revisions.
- Information-architecture changes.
- New security boundaries or cost-bearing infrastructure.
- Changes to unrelated repositories or systems.

## Source of Truth

- Repository: `eirepolitic.github.io`
- Default branch: `main`
- This phase plan: `_docs/high-director/example-documents-plan.md`
- Completed template initiative: `_docs/high-director/documentation-section-template-plan.md`
- Templates: `_templates/`
- Documentation standard: `DOCUMENTATION_STANDARD.md`
- Validator: `scripts/validate_docs.py`
- Validation workflow: `.github/workflows/validate-documentation.yml`
- Publishing: GitHub Pages from `main`

Current repository state and merged pull requests take precedence over stale progress text in this plan.

## Completed Work

- Repository — `eirepolitic.github.io`; PR #20, validation `31137389854`, Pages `31137413142`.
- System — Eire Politic Documentation Site; PR #21, validation `31137496390`, Pages `31137516088`.
- Data & Schema — Documentation Search Index; PR #22, validation `31137604054`, Pages `31137621658`.
- Runbook — Publish a Documentation Change; PR #23, validation `31137737015`, Pages `31137754183`.
- Architecture Decision — Use Metadata-Driven Static Documentation on GitHub Pages; PR #24, validation `31137849202`, Pages `31137870369`.
- High Director — this persistent Example Documents Phase plan; PR #25, validation `31137946466`, Pages `31137960412`.

## Category Progress

- [x] Repository
- [x] System
- [x] Data & Schema
- [x] Runbook
- [x] Architecture Decision
- [x] High Director — this persistent phase plan is the real continuation example.
- [x] Note — Documentation Validation Compatibility Findings drafted from observed validation failures and source files.
- [ ] Archive

## Current Implementation Details

Each documentation change uses a branch from current `main`, a focused pull request, the documentation validator, merge only after validation succeeds, and post-merge GitHub Pages confirmation. Stable examples created by this phase live in their matching `_docs/` sections.

The validator accepts only the documented site lifecycle vocabulary; `complete` is not an allowed front-matter status. Initiative or phase completion is therefore recorded explicitly in document content while valid lifecycle metadata is retained.

## Decisions and Constraints

- Use real implemented or historical work only.
- Keep pull requests small and reviewable.
- Run documentation validation before every merge.
- Confirm Pages deployment after every merged documentation change.
- Update this plan after every meaningful step.
- Do not modify templates unless real usage exposes a concrete defect.
- Do not change architecture, security boundaries, or cost without a separate decision.

The accepted static-site architecture is documented at `/projects/decisions/use-metadata-driven-static-documentation/`.

## Security and Access

The repository and GitHub Pages site are public. Do not commit credentials, tokens, private keys, session data, personal data, secret values, or confidential identifiers. Use repository, workflow, variable, and secret-object names only when documentation requires them.

## Validation and Evidence

For each category example:

1. Review authoritative repository files or existing operational evidence.
2. Draft the real example on a branch from `main`.
3. Open a focused pull request.
4. Require `Validate documentation` to succeed.
5. Merge only after validation passes.
6. Confirm the resulting Pages build and deploy jobs succeed.
7. Record PR, validation, and deployment evidence in this plan.

Evidence through the High Director example is recorded in `Completed Work`.

## Failure Modes and Recovery

- Outdated branch: recreate or update from current `main` before continuing.
- Validation failure: fix the referenced document or valid rule; do not bypass the validator.
- Failed Pages deployment: inspect the failed Pages job and correct the root cause in a small PR.
- Stale plan state: verify merged PRs and workflow runs, then correct this plan.
- Secret or confidential content discovered: stop normal publication work and use the appropriate security response rather than relying on a revert.

## Known Limitations

- The examples cover verified repository documentation work available in this site; they are not intended to represent every possible infrastructure pattern.
- GitHub Pages and GitHub Actions are external dependencies.
- Front-matter lifecycle vocabulary has no `complete` value.

## Outstanding Work

1. Validate, merge, and deploy the Note example.
2. Refine one existing real archived document against the Archive template without inventing missing historical facts.
3. Record final phase completion in this plan after all category examples are deployed.

## Next Safe Development Action

Validate and merge branch `high-director/example-note-validation-findings`, confirm the resulting Pages deployment, then inspect `_templates/archive-template.md` and one existing document under `_docs/archive/`. Change only factual gaps supported by the archived record.

## Handoff Notes

Always pass only `eirepolitic.github.io` to repository tools. Start each new documentation step from current `main`. Do not begin the next category until the previous merged documentation change has a successful Pages deployment. Keep this plan synchronized with actual PR and workflow evidence.

## Related Documents

- [Documentation Section Template Initiative](/projects/high-director/documentation-section-template-plan/) records the completed template phase.
- [Static Documentation Architecture Decision](/projects/decisions/use-metadata-driven-static-documentation/) records the implemented architecture choice.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: PRs #20 through #25; validation runs `31137389854`, `31137496390`, `31137604054`, `31137737015`, `31137849202`, and `31137946466`; Pages runs `31137413142`, `31137516088`, `31137621658`, `31137754183`, `31137870369`, and `31137960412`; `_templates/note-template.md`; current `main`
- Verified by: High Director
- Verification scope: category completion through High Director, Note source findings, validation/deployment gates, constraints, and next work
- Unverified areas: Note is not yet merged; Archive example is not yet complete
