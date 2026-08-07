---
title: bb-comp-prices documentation workstream plan
summary: Persistent High Director plan for documenting the bb-comp-prices competitor-pricing platform from verified repository evidence through focused validated pull requests.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 100
permalink: /projects/high-director/bb-comp-prices-documentation-workstream-plan/
repository: eirepolitic.github.io
tags:
  - high-director
  - bb-comp-prices
  - documentation
---

# bb-comp-prices documentation workstream plan

## Purpose

This page is the persistent continuation plan for the complete `bb-comp-prices` documentation workstream. It coordinates evidence review, page creation, validation, merge, and Pages deployment checks so a future High Director session can continue without relying on chat history.

## Current State

The workstream is active. Repository discovery material already exists at `_docs/high-director/repository-scan-bb-comp-prices.md`, and the owner-wide target catalogue assigns the following `bb-comp-prices` documentation targets:

- P0: repository/platform overview; S3 storage and data-product model; end-to-end orchestration and security/configuration boundary.
- P1: Best Buy Marketplace category discovery; Best Buy product and Marketplace-offer extraction; Amazon.ca competitor acquisition/recovery; product matching and confidence scoring.
- P2: Walmart.ca acquisition/probes; diagnostics/extraction research; validation/data quality; Python package/CLI/configuration/developer reference.
- P3: superseded probes and experiments.

Current source verification has begun against `bb-comp-prices` `main`. Confirmed source areas already inspected include `pyproject.toml`, `config/settings.yaml`, `docs/BUILD_PLAN.md`, `src/bb_comp_prices/models.py`, `src/bb_comp_prices/config.py`, `src/bb_comp_prices/http.py`, `src/bb_comp_prices/storage/`, `src/bb_comp_prices/cli.py`, `src/bb_comp_prices/pipeline/orchestrator.py`, `scripts/run_end_to_end.py`, and `.github/workflows/end_to_end.yml`.

No architecture or operational page created by this workstream is complete until its focused pull request passes documentation validation, is merged, and the matching `pages-build-deployment` run succeeds for the merged commit.

## Scope

### Included

- Documentation repository: `eirepolitic.github.io`.
- Source repository: `bb-comp-prices`.
- All catalogue targets assigned to the `bb-comp-prices` workstream.
- Current executable source, GitHub Actions workflows, configuration, tests, scripts, current validation reports, and relevant historical probes/experiments.
- Exact repository/file/function/class paths; workflow triggers; CLI stages/options; acquisition methods; matching rules and states; S3/data-product contracts; outputs; validation; dependencies; configuration; security boundaries; rerun/recovery procedures; limitations.

### Excluded

- Routine edits to `_docs/high-director/documentation-target-catalogue.md`; it is read-only coordination input for this workstream.
- Other repositories or workstream plans owned by parallel chats.
- Live AWS changes, IAM changes, credential rotation, cost-bearing infrastructure changes, or access-control changes without explicit approval.
- Treating `docs/BUILD_PLAN.md` as deployment proof when executable source, workflows, configuration, or current validation evidence do not confirm the claim.
- Publishing secret values, private account identifiers, session data, or credentials.
- Creating one top-level page per probe script; probes are grouped unless repository evidence shows a separately operated subsystem.

## Source of Truth

- Documentation repository: `eirepolitic.github.io`.
- Documentation default branch: `main`.
- Source repository: `bb-comp-prices`.
- Source default branch: `main`.
- Documentation standard: `DOCUMENTATION_STANDARD.md`.
- Templates: `_templates/`.
- Scope coordination: `_docs/high-director/documentation-target-catalogue.md`.
- Discovery plan: `_docs/high-director/repository-documentation-discovery-plan.md`.
- Existing scan: `_docs/high-director/repository-scan-bb-comp-prices.md`.
- Documentation validator: `scripts/validate_docs.py`.
- Validation workflow: `.github/workflows/validate-documentation.yml` (`Validate documentation`).
- Pages deployment gate: repository `pages-build-deployment` workflow for the merged commit.

Evidence precedence for factual implementation claims is: current executable source/workflow/current validation report > current configuration > build plan/README > historical experiment. Where sources conflict, documentation must state the conflict and use the higher-precedence verified source.

## Current Implementation Details

Verified foundation currently includes Python `>=3.12`, AWS region `ca-central-1`, S3 bucket name `eirepolitic-data`, S3 prefix `bb-comp-prices`, source-specific Best Buy/Amazon.ca/Walmart.ca logic, optional Playwright/browser automation, and GitHub Actions AWS credential secret names. These facts must be re-checked in the exact source used by each page before publication.

The first documentation sequence is fixed as:

1. Repository/platform architecture.
2. S3 storage and data-product model.
3. End-to-end orchestration and security/configuration boundary.
4. Best Buy pipeline.
5. Amazon pipeline.
6. Matching engine.
7. Remaining P2/P3 targets in dependency order.

Each major component should use a small focused branch named `docs/bb-comp-*` and a focused pull request.

## Decisions and Constraints

- Document current implementation separately from planned, experimental, superseded, and unverified behavior.
- Product matching must be described as technical scoring/data-quality logic, including evidence, contradictions, thresholds, states, and manual-review boundaries, without overstating quality.
- Generated `docs/LATEST_*REPORT.md` files are evidence of observed validation/probe results, not implementation authority by themselves.
- Safe obvious documentation work proceeds autonomously.
- Stop for architecture, security, cost, access-control, or irreversible decisions.
- Before final cross-cutting changes, synchronize with current documentation `main` because parallel workstreams may merge concurrently.

## Security and Access

Credential/configuration names such as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` may be documented. Their values must never be copied into documentation.

If exact live S3, IAM, or other AWS deployment state becomes necessary and cannot be verified from repository source, request one coherent authoritative source at a time. The request must explain why it is needed, provide click-by-click AWS Console instructions, identify exactly what to copy or screenshot, and identify secret/personal fields to cover. Any supplied sanitized technical evidence must then be persisted into `eirepolitic.github.io` rather than remaining only in chat.

## Validation and Evidence

For each documentation pull request:

1. Open the focused PR from a `docs/bb-comp-*` branch.
2. Confirm the `Validate documentation` workflow passes. Its authoritative validation command is `python scripts/validate_docs.py` under Python 3.12 with `PyYAML==6.0.2`.
3. Merge only after validation succeeds.
4. Identify the merged commit.
5. Confirm the matching `pages-build-deployment` workflow succeeds for that merged commit.
6. Only then begin the next major component.

Current workstream-plan verification is based on the documentation standard/templates/catalogue/discovery pages in `eirepolitic.github.io` `main` and the current `bb-comp-prices` repository tree plus the source/configuration/workflow paths listed in Current State.

## Failure Modes and Recovery

- **Outdated documentation branch:** symptom is conflicts or missing parallel changes. First check current `main`; recreate or rebase the focused branch before final cross-cutting edits.
- **Validation failure:** inspect the `Validate documentation` run and `scripts/validate_docs.py`; fix metadata, links, placeholders, or structure before merge.
- **Pages deployment failure:** do not start the next major component. Inspect the `pages-build-deployment` run for the merged commit and repair the documentation/site issue in a focused follow-up PR.
- **Source conflict:** use the evidence hierarchy above and mark lower-confidence claims planned, experimental, superseded, or unverified.
- **Live-cloud ambiguity:** do not infer deployment state from plans. Request sanitized authoritative AWS evidence only when needed.
- **Secret exposure risk:** omit values and private identifiers; document only names, roles, boundaries, and safe retrieval procedures.

## Known Limitations

- The full `bb-comp-prices` source review is still in progress; this plan does not claim every workflow, function, test, probe, or report has been individually verified yet.
- Repository evidence can establish configured AWS resources and expected paths, but not necessarily current live S3/IAM state.
- Historical probe outputs may describe conditions that no longer reflect current retailer behavior and must be dated and classified accordingly.

## Outstanding Work

Required work, in order:

1. Complete source verification for repository/platform architecture and publish its focused repository page.
2. Verify storage writers/readers, S3 key construction, schemas, formats, and consumers; publish the S3/data-product page.
3. Verify all orchestration workflows, triggers, CLI stages/options, configuration loading, secret names, permissions, rerun/failure behavior; publish the orchestration/security page.
4. Verify and document Best Buy category discovery plus product/Marketplace-offer extraction.
5. Verify and document Amazon.ca acquisition/recovery.
6. Verify and document matching/scoring states, thresholds, contradictions, validation, and manual-review boundary.
7. Verify/document Walmart, diagnostics/research, validation/data quality, package/CLI/developer reference, and superseded experiments.
8. Perform a final cross-page consistency/link review from current `main`.

## Next Safe Development Action

From current `eirepolitic.github.io` `main`, create a new focused branch named `docs/bb-comp-platform-overview`. Finish verification of `bb-comp-prices` repository structure, package entry points, workflows, dependencies, configuration, tests, scripts, and current reports; then create the repository/platform overview using `_templates/repository-template.md`. Open a focused PR, require `Validate documentation` to pass, merge it, and require the matching `pages-build-deployment` run to succeed before starting the S3/data-product page.

## Handoff Notes

- Keep this page synchronized as components are completed; record PRs, merged commits, validation runs, Pages runs, and the next safe action.
- Use repository name only with the GitHub integration; the owner is configured separately.
- Keep branch names unique to this workstream (`docs/bb-comp-*`).
- Do not edit parallel workstream plans during routine work.
- Do not merge multiple major catalogue targets merely to reduce PR count; focused reviewability is preferred.

## Related Documents

- [Documentation target catalogue](/projects/high-director/documentation-target-catalogue/)
- [Repository documentation discovery plan](/projects/high-director/repository-documentation-discovery-plan/)
- [bb-comp-prices repository scan](/projects/high-director/repository-scan-bb-comp-prices/)
- [Documentation site](/systems/documentation-site/)
- [Documentation site operations](/runbooks/documentation-site-operations/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `eirepolitic.github.io` `main`; `DOCUMENTATION_STANDARD.md`; full `_templates/` set; catalogue/discovery/scan pages; current `bb-comp-prices` tree and the source/configuration/workflow paths listed above.
- Verified by: High Director
- Verification scope: workstream scope, evidence hierarchy, documentation standards, branch/PR/deployment gates, and initial platform foundation.
- Unverified areas: complete function-by-function/source-by-source `bb-comp-prices` review; live AWS deployment state.
