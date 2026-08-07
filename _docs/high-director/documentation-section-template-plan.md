---
title: Documentation Section Template Initiative
summary: Build and validate best-practice documentation templates for every top-level documentation section without beginning the example-document phase.
section: high-director
doc_type: agent
status: active
created: 2026-08-05
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 30
permalink: /projects/high-director/documentation-section-template-plan/
---

# Documentation Section Template Initiative

## Purpose

Create a compatible, practical template for the main documentation page of an item in each top-level documentation section:

- Repositories
- Systems
- Data and Schemas
- Runbooks
- Architecture Decisions
- High Director
- Notes
- Archive

The templates are guidance rather than rigid forms. Authors may omit sections that add no value, but each template must preserve enough operational and development context for safe continuation.

## Scope

### Included

- Define required and optional front matter for each category using the current metadata vocabulary.
- Define recommended title, summary, heading order, section purpose, source-of-truth details, security guidance, related-document guidance, verification expectations, and subordinate-page criteria.
- Add useful placeholders that do not encourage secret values or fabricated state.
- Keep templates compatible with current navigation, search, generated indexes, related-document links, layouts, and validation.
- Update this plan after each implementation step.
- Run documentation validation before each merge.
- Confirm GitHub Pages deployment after material merged changes.

### Excluded

- Creating real example documents for the eight categories.
- Changing the information architecture unless template implementation exposes a blocking defect.
- Adding metadata values without a separately reviewed standards change.
- Adding secrets, credentials, account identifiers, or confidential values.

## Design Principles

1. Preserve the current metadata contract and validator compatibility.
2. Make the main page sufficient for ordinary items.
3. Create subordinate pages only when detail would make the main page difficult to scan, maintain, or verify.
4. Record exact repository names, paths, configuration object names, interfaces, inputs, outputs, and deployment locations without secret values.
5. Separate verified current state from planned, historical, inferred, or unknown state.
6. End operational templates with outstanding work and the next safe development action.
7. Avoid empty headings, duplicated facts, and generic prose.
8. Treat `last_verified` as evidence of a deliberate check, not merely an edit date.

## Standard Template Contract

Every category template must include:

- Required and optional front-matter guidance.
- Title and one-sentence summary guidance.
- Recommended heading order and section purpose.
- Source-of-truth guidance.
- Current implementation or lifecycle state.
- Security guidance without secret values.
- Related-document guidance.
- Status and verification expectations.
- Useful placeholders.
- Criteria for subordinate pages.
- Outstanding work and next safe action where relevant.

## Implementation Steps

### Step 1 — Plan and compatibility baseline

Status: complete

- [x] Review standards, architecture, operations, layouts, templates, validation, current documents, repository tree, and recent merged work.
- [x] Confirm no layout or navigation changes are required.
- [x] Merge pull request #14.
- [x] Pass documentation validation.
- [x] Confirm Pages deployment.

### Step 2 — Core implementation templates

Status: complete

- [x] Rebuild `_templates/repository-template.md`.
- [x] Rebuild `_templates/system-template.md`.
- [x] Add `_templates/data-schema-template.md`.
- [x] Rebuild `_templates/runbook-template.md`.
- [x] Update `DOCUMENTATION_STANDARD.md` with shared template usage rules.
- [x] Merge pull request #15 after validation.
- [x] Confirm later successful Pages run `31134967087` contains these changes.

### Step 3 — Governance and agent templates

Status: complete

- [x] Rebuild `_templates/decision-template.md`.
- [x] Add `_templates/high-director-template.md`.
- [x] Pass documentation validation run `31126187599`.
- [x] Merge pull request #16.
- [x] Confirm later successful Pages run `31134967087` contains these changes.

### Step 4 — Reference lifecycle templates

Status: complete

- [x] Add `_templates/note-template.md`.
- [x] Add `_templates/archive-template.md`.
- [x] Pass documentation validation run `31128483540`.
- [x] Merge pull request #17.
- [x] Confirm Pages run `31134967087` succeeded for merged commit `bcbc32a83790d84c1eae3c19a0277213540d6eb0`.

### Step 5 — Cross-template consistency review

Status: in review

- [x] Compare all eight templates for duplication, missing requirements, conflicting terminology, and validator incompatibility.
- [x] Verify filenames and metadata values match `_data/docs_sections.yml` and `DOCUMENTATION_STANDARD.md`.
- [x] Verify each template addresses source of truth, security, related documents, status, verification, subordinate pages, limitations, outstanding work, and next safe action where applicable.
- [x] Strengthen `_templates/archive-template.md` with explicit continuation, source-of-truth, security, and verification guidance.
- [x] Update `.github/workflows/validate-documentation.yml` so `_templates/**` changes trigger validation automatically and manual `workflow_dispatch` remains available.
- [ ] Open the final consistency-review pull request.
- [ ] Pass documentation validation.
- [ ] Merge the final consistency-review pull request.
- [ ] Confirm Pages deployment.
- [ ] Mark this plan complete in a final recorded update.

Approval checkpoint: final template review. Do not begin example documents until this checkpoint is approved.

## Template Files

- `_templates/repository-template.md`
- `_templates/system-template.md`
- `_templates/data-schema-template.md`
- `_templates/runbook-template.md`
- `_templates/decision-template.md`
- `_templates/high-director-template.md`
- `_templates/note-template.md`
- `_templates/archive-template.md`

## Validation and Deployment

For each implementation pull request:

1. Run `python scripts/validate_docs.py` or the documentation validation workflow.
2. Review metadata, internal links, placeholder safety, and category consistency.
3. Merge only after validation passes.
4. Confirm the Pages build and deployment both succeed.
5. Record the result in this plan.

Template-only pull requests now trigger the documentation validation workflow automatically through the `_templates/**` path filter.

## Risks and Controls

### Secret exposure

Document configuration object names and storage locations only. Never include credentials, tokens, private keys, connection strings, secret values, or confidential identifiers.

### Breaking existing documents

Do not increase validator requirements for existing `_docs` pages solely to support richer templates.

### Deployment uncertainty

Distinguish a successful Jekyll build from a successful Pages deployment. A later successful Pages deployment containing an earlier material change satisfies deployment confirmation for that earlier change.

### Premature example work

The example phase remains blocked until Step 5 is approved and this plan is marked complete.

## Completion Criteria

This initiative is complete only when:

- All eight templates exist and satisfy the requested guidance.
- Existing documents remain compatible.
- The documentation standard explains template usage.
- This plan records completed steps and pull requests.
- Documentation validation passes.
- Material changes have successful Pages deployments.
- The final template review is approved.
- No real category examples have been created.

## Next Safe Action

Open the Step 5 consistency-review pull request, verify automatic documentation validation, merge after validation succeeds, confirm the Pages deployment, then record final completion without beginning the example phase.

## Verification Record

- Last verified: 2026-08-06
- Verified against: pull requests #14 through #17; validation runs `31126187599` and `31128483540`; successful Pages run `31134967087`; all eight templates; section metadata; documentation standard; validation workflow
- Verification scope: template consistency, metadata vocabulary, validation triggers, merge state, and deployment state through Step 4
