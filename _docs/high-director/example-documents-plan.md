---
title: Example Documents Phase
summary: Completed real-world examples for every documentation category, with validation, deployment evidence, and continuation guidance for future High Director sessions.
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

The Example Documents phase is complete. All eight top-level documentation categories now have a real example that was validated, merged, and successfully deployed through GitHub Pages.

No template changes were required during the phase.

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
- Note — Documentation Validation Compatibility Findings; PR #26, validation `31138059436`, Pages `31138080555`.
- Archive — Member Images Pipeline; PR #27, validation `31138182928`, Pages `31138202986`.

## Category Progress

- [x] Repository
- [x] System
- [x] Data & Schema
- [x] Runbook
- [x] Architecture Decision
- [x] High Director
- [x] Note
- [x] Archive

## Current Implementation Details

Each documentation change used a branch from current `main`, a focused pull request, the documentation validator, merge only after validation succeeded, and post-merge GitHub Pages confirmation. Stable examples created or refined by this phase live in their matching `_docs/` sections.

The validator accepts only the documented site lifecycle vocabulary; `complete` is not an allowed front-matter status. Phase completion is therefore recorded explicitly in this document while valid lifecycle metadata is retained.

## Decisions and Constraints

- Use real implemented or historical work only.
- Keep pull requests small and reviewable.
- Run documentation validation before every merge.
- Confirm Pages deployment after every merged documentation change.
- Update persistent plans after meaningful steps.
- Do not modify templates unless real usage exposes a concrete defect.
- Do not change architecture, security boundaries, or cost without a separate decision.

The accepted static-site architecture is documented at `/projects/decisions/use-metadata-driven-static-documentation/`.

## Security and Access

The repository and GitHub Pages site are public. Do not commit credentials, tokens, private keys, session data, personal data, secret values, or confidential identifiers. Use repository, workflow, variable, and secret-object names only when documentation requires them.

## Validation and Evidence

Every category example completed the required path:

1. Source material reviewed.
2. Focused branch and pull request created.
3. `Validate documentation` passed.
4. Pull request merged into `main`.
5. GitHub Pages build and deployment succeeded.
6. Evidence recorded in this plan.

The exact PR, validation, and Pages run IDs are recorded in `Completed Work`.

## Failure Modes and Recovery

- Outdated branch: recreate or update from current `main` before continuing.
- Validation failure: fix the referenced document or valid rule; do not bypass the validator.
- Failed Pages deployment: inspect the failed Pages job and correct the root cause in a small PR.
- Stale documentation state: verify merged PRs and workflow runs, then correct the relevant page.
- Secret or confidential content discovered: stop normal publication work and use the appropriate security response rather than relying on a revert.

## Known Limitations

- The examples cover verified documentation work available in this site; they are not intended to represent every possible infrastructure pattern.
- GitHub Pages and GitHub Actions are external dependencies.
- Front-matter lifecycle vocabulary has no `complete` value.
- The historical `eirepolitic` repository referenced by the Archive example is not accessible through the configured GitHub connection, so current source state remains deliberately unverified in that archive.

## Outstanding Work

No required work remains for the Example Documents phase.

Future documentation should use these examples and the existing templates as practical references. Templates should change only when real usage reveals a concrete defect or a separately reviewed standards requirement changes.

## Next Safe Development Action

Treat the Example Documents phase as closed. For the next real documentation task, start from current `main`, select the matching template and relevant real example, verify facts against the current source of truth, run documentation validation before merge, and confirm Pages deployment after merge.

## Handoff Notes

Always pass only `eirepolitic.github.io` to repository tools for this site. The template initiative and Example Documents phase are both complete. Do not reopen either initiative without a real defect, standards change, or new documentation requirement.

## Related Documents

- [Documentation Section Template Initiative](/projects/high-director/documentation-section-template-plan/) records the completed template phase.
- [Static Documentation Architecture Decision](/projects/decisions/use-metadata-driven-static-documentation/) records the implemented architecture choice.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: PRs #20 through #27; validation runs `31137389854`, `31137496390`, `31137604054`, `31137737015`, `31137849202`, `31137946466`, `31138059436`, and `31138182928`; Pages runs `31137413142`, `31137516088`, `31137621658`, `31137754183`, `31137870369`, `31137960412`, `31138080555`, and `31138202986`; all eight category examples; current `main`
- Verified by: High Director
- Verification scope: all eight category examples, validation gates, merge state, deployment evidence, phase completion, constraints, and continuation guidance
- Unverified areas: current source repository state for the historical Member Images Pipeline only; this does not block archive or phase completion
