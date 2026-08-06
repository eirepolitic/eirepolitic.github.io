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

- Review the current documentation standard, layouts, navigation metadata, templates, validation rules, and existing `_docs` content.
- Define required and optional front matter for each category using the current metadata vocabulary.
- Define recommended title, summary, heading order, section purpose, source-of-truth details, security guidance, related-document guidance, verification expectations, and subordinate-page criteria.
- Add useful placeholders and examples that do not encourage secret values or fabricated state.
- Keep templates compatible with current navigation, search, generated indexes, related-document links, layouts, and validation.
- Update this plan after each implementation step.
- Run documentation validation before each merge.
- Confirm GitHub Pages deployment after material merged changes.

### Excluded

- Creating real example documents for the eight categories.
- Changing the documentation information architecture unless template implementation exposes a blocking defect.
- Adding new metadata values without a separately reviewed standards change.
- Adding secrets, credentials, account identifiers, or environment-specific confidential values.

## Current-State Findings

- `_docs` is the canonical documentation collection and existing pages rely on the current required metadata vocabulary.
- Section navigation is driven by `_data/docs_sections.yml`.
- `_layouts/docs.html` and `_layouts/docs-section.html` consume the established metadata and stable document URLs; category templates do not require layout changes.
- Existing templates cover several categories but do not fully address development continuity, verification, failure modes, security, outstanding work, next safe action, or subordinate-page guidance.
- Existing archive documents are intentionally concise and must remain valid without retroactive expansion.
- `scripts/validate_docs.py` is the local and workflow validation authority for documentation metadata and links.
- Pull request #13 completed the initial rebuild and is the baseline for this initiative.

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

Every category template will include:

- A commented front-matter example distinguishing required and optional fields.
- Guidance for a specific, searchable title and a one-sentence summary describing purpose and scope.
- A recommended heading sequence with concise instructions beneath each heading.
- Source-of-truth guidance covering repositories, file paths, systems, datasets, schemas, dashboards, workflows, or decisions as applicable.
- Current implementation state, dependencies, inputs, outputs, deployment or operation, validation, failure modes, limitations, outstanding work, next safe action, and last verification guidance where relevant.
- Security notes that name configuration keys and access boundaries without exposing values.
- Related-document guidance using stable internal document links and clear parent/child relationships.
- Criteria for moving detailed material into subordinate pages.
- Placeholder text that authors must replace or remove.

## Implementation Steps

### Step 1 — Plan and compatibility baseline

Status: complete

- [x] Review the required standards, architecture, operations runbook, rebuild plan, section metadata, layouts, existing templates, validation script, current `_docs` documents, repository tree, and recent merged pull requests.
- [x] Confirm the template initiative can proceed without layout or navigation changes.
- [x] Commit the persistent plan on a dedicated branch.
- [x] Pass validation and merge pull request #14.
- [x] Confirm the GitHub Pages deployment for the merged change.

Result: pull request #14 merged successfully; documentation validation and Pages deployment completed successfully.

### Step 2 — Core implementation templates

Status: merged; deployment requires retry

- [x] Rebuild `_templates/repository-template.md`.
- [x] Rebuild `_templates/system-template.md`.
- [x] Add `_templates/data-schema-template.md`.
- [x] Rebuild `_templates/runbook-template.md`.
- [x] Update `DOCUMENTATION_STANDARD.md` with shared template usage rules.
- [x] Open and validate pull request #15.
- [x] Merge pull request #15.
- [ ] Obtain a successful Pages deployment for merged commit `ef60fec607d07d1ed180375d11f8041d510066ae` or a later commit containing the same changes.

Deployment record: Pages run `31110810856` built the Jekyll site successfully, but the deployment job failed after ten minutes. The templates passed documentation validation and the Pages build stage; the deployment state is not yet confirmed successful.

### Step 3 — Governance and agent templates

Status: in review

- [x] Rebuild `_templates/decision-template.md`.
- [x] Add `_templates/high-director-template.md`.
- [x] Update this persistent plan.
- [ ] Open and pass validation for the Step 3 pull request.
- [ ] Merge only after validation passes and the outstanding Pages deployment state is resolved.
- [ ] Confirm the resulting Pages deployment.

Emphasis:

- Decision context, alternatives, consequences, supersession, implementation state, reversal, and verification.
- Agent-assisted development context, exact actions taken, constraints, evidence, security boundaries, safe continuation, and unresolved work.

Approval checkpoint: review decision-record and High Director continuation guidance.

### Step 4 — Reference lifecycle templates

Status: not started

Create or revise templates for:

- Notes
- Archive

Emphasis:

- Notes must state purpose, confidence, source, scope, and promotion criteria without pretending to be authoritative documentation.
- Archive pages must preserve historical value, explain why the item is inactive, identify the last known state, warn against treating it as current, and point to replacements where known.

Deliverables follow the same branch, pull request, validation, plan-update, merge, and deployment checks as earlier steps.

Approval checkpoint: review lifecycle and historical-state guidance.

### Step 5 — Cross-template consistency review

Status: not started

- Compare all eight templates for unnecessary duplication, missing requirements, conflicting terminology, and validator incompatibility.
- Verify every template addresses source of truth, security, related documents, status, verification, subordinate pages, known limitations, outstanding work, and next safe action where applicable.
- Verify filenames and references match `_data/docs_sections.yml` and the documented section vocabulary.
- Run local validation and the GitHub Actions documentation workflow.
- Merge the final consistency pull request.
- Confirm GitHub Pages deployment.
- Mark this plan complete with final pull request and deployment references.

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

Existing general-purpose templates will be retained only where they remain useful and non-conflicting.

## Validation and Deployment

For each implementation pull request:

1. Run `python scripts/validate_docs.py` against the branch contents.
2. Review the pull request diff for metadata, internal links, placeholder safety, and category consistency.
3. Confirm the repository documentation workflow succeeds.
4. Merge only after validation passes.
5. Confirm the GitHub Pages deployment associated with the merged commit reaches a successful state when the change affects published documentation.
6. Record completion and references in this plan.

## Risks and Controls

### Template duplication

Control: keep shared guidance in the documentation standard where practical, while retaining category-specific instructions in each template.

### Overly rigid forms

Control: mark headings as recommended and explicitly permit omission when a section adds no value.

### False verification claims

Control: require authors to use `last_verified` only after checking the implementation or authoritative source; unknown state must be labelled unknown.

### Secret exposure

Control: show configuration names and storage locations only. Never include secret values, tokens, credentials, private keys, or confidential identifiers.

### Breaking existing documents

Control: do not increase validator requirements for existing `_docs` pages solely to support richer templates.

### Deployment uncertainty

Control: distinguish a successful Jekyll build from a successful Pages deployment and do not mark a material step complete until the deployment job succeeds.

### Premature example work

Control: the example phase remains blocked until Step 5 is approved.

## Completion Criteria

This initiative is complete only when:

- All eight templates exist and satisfy the requested guidance.
- Existing documents remain compatible.
- The documentation standard clearly explains how templates should be used.
- This plan records every completed step and pull request.
- Documentation validation and relevant GitHub Actions pass.
- Material merged changes have successful GitHub Pages deployments.
- The final template review is approved.
- No real category examples have been created.

## Next Safe Action

Open the Step 3 pull request, pass documentation validation, resolve the outstanding Pages deployment state, and merge only after both checks are satisfactory.

## Verification Record

- Last verified: 2026-08-06
- Verified against: merged pull requests #14 and #15; Pages run `31110810856`; Step 3 branch files
- Verification scope: template commits, documentation validation state, Jekyll Pages build result, failed deployment result, and Step 3 implementation status
