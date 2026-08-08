---
title: bb-comp-prices documentation workstream plan
summary: Persistent High Director plan and completion ledger for the bb-comp-prices competitor-pricing documentation workstream.
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

This page is the persistent continuation and completion record for the `bb-comp-prices` documentation workstream. It preserves scope, evidence rules, delivered pages, merge/deployment gates, known implementation gaps, and the safest future maintenance path without relying on conversation history.

## Current State

The assigned catalogue scope is **documented and published**. P0, P1, P2, and P3 targets have dedicated maintainable pages based on current repository evidence, with planned/experimental/superseded behavior kept separate from current implementation.

The workstream is now in maintenance-ready state rather than active initial discovery. Future work should update the existing authoritative pages when source behavior changes instead of creating duplicate documentation.

The owner-wide target catalogue remains read-only coordination input for this workstream.

## Delivered Catalogue Scope

### P0

- Target 7 — [bb-comp-prices repository/platform overview](/projects/repositories/bb-comp-prices/)
- Target 8 — [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)
- Target 9 — [bb-comp-prices end-to-end orchestration and security boundary](/projects/systems/bb-comp-prices-orchestration-security/)

### P1

- Target 21 — [Best Buy Marketplace category discovery](/projects/systems/bb-comp-prices-bestbuy-category-discovery/)
- Target 22 — [Best Buy product and Marketplace-offer extraction](/projects/systems/bb-comp-prices-bestbuy-extraction/)
- Target 23 — [Amazon.ca competitor acquisition and recovery](/projects/systems/bb-comp-prices-amazon-acquisition/)
- Target 24 — [Product matching and confidence scoring](/projects/systems/bb-comp-prices-product-matching/)

### P2

- Target 39 — [Walmart.ca acquisition and probe subsystem](/projects/systems/bb-comp-prices-walmart-probes/)
- Target 40 — [Diagnostics, probes, and extraction research](/projects/systems/bb-comp-prices-diagnostics-research/)
- Target 41 — [Validation and data-quality framework](/projects/systems/bb-comp-prices-validation-data-quality/)
- Target 42 — [Python package, CLI, configuration, and developer reference](/projects/systems/bb-comp-prices-developer-reference/)

### P3

- Target 55 — [Superseded bb-comp-prices probes and experiments](/projects/archive/bb-comp-prices-superseded-probes-experiments/)

## Scope and Evidence Rules

The workstream used:

```text
current executable source/workflow/current validation report
  > current configuration
  > build plan/README
  > historical experiment
```

`docs/BUILD_PLAN.md` is not deployment proof. Generated `docs/LATEST_*REPORT.md` files are observed evidence and must be checked for semantic currency against current source before being treated as current validation authority.

Current, planned, experimental, superseded, and unverified behavior are explicitly separated throughout the published pages.

## Source of Truth

- Documentation repository: `eirepolitic.github.io` `main`.
- Source repository: `bb-comp-prices` `main`.
- Documentation standard: `DOCUMENTATION_STANDARD.md`.
- Templates: `_templates/`.
- Scope coordination: `_docs/high-director/documentation-target-catalogue.md`.
- Discovery plan: `_docs/high-director/repository-documentation-discovery-plan.md`.
- Initial repository scan: `_docs/high-director/repository-scan-bb-comp-prices.md`.
- Documentation validator: `scripts/validate_docs.py`.
- Validation workflow: `.github/workflows/validate-documentation.yml` (`Validate documentation`).
- Pages deployment workflow: `pages-build-deployment`.

## Delivery Ledger

| Component | PR | Merge | Pages gate |
| --- | ---: | --- | ---: |
| Persistent workstream plan | #63 | `26843f1b…` | #169 success |
| Repository/platform overview | #65 | `80934057…` | #171 success |
| S3/data-product model | #67 | `59e82598…` | #173 success |
| Orchestration/security boundary | #69 | `16ed87ca…` | #175 success |
| Best Buy category discovery | #71 | `eea47607…` | #177 success |
| Best Buy extraction/offers | #72 | `20d14986…` | #178 success |
| Amazon.ca acquisition/recovery | #75 | `05499a3d…` | #181 success |
| Product matching | #83 | `90c98a378b0168583b8c8cd049ddc414e9bdc77f` | #189 superseded/cancelled; newer main #190 success and included merge |
| Walmart probes | #86 | `e05f9a58853499c1ceb2783d831b228909f8e918` | #193 success |
| Diagnostics/research framework | #89 | `3df605be6eeecd77e936c57727552623d0475d2d` | #195 success |
| Validation/data quality | #92 | `129a0f50e5162f380e7a85fe2f6e8fdb1a346326` | #198 success |
| Developer reference | #96 | `b219d9e8451d5f5955c4b911e65f8e13729b8412` | #202 success |
| Superseded experiments archive | #99 | `839e09e1c6a78c237ba7d2133047ed336b7615ee` | #204 success |

All focused PRs passed the repository documentation validator before merge. The product-matching exact-commit Pages run was cancelled because a newer `main` deployment superseded it; Pages #190 succeeded on newer `main` containing the matching merge. All subsequent components received successful exact-commit Pages deployments.

## Verified Architecture Findings

The documentation now captures these operationally important facts:

- Python requirement is `>=3.12`.
- Configured AWS region is `ca-central-1`, bucket `eirepolitic-data`, prefix `bb-comp-prices`.
- Major live workflows inspected are manual dispatch rather than scheduled production jobs.
- End-to-end stage order is `bestbuy -> category -> amazon -> Walmart blocked -> matching`.
- Same-run category discovery therefore cannot feed same-run Best Buy extraction in the current controller.
- Stage selection does not enforce upstream dependency freshness; isolated Amazon/matching runs can consume older stable `latest/` objects.
- Some dataset families are conditionally written, so a zero-row newer run can leave an older stable `latest/` object in place.
- CSV nested lists/dictionaries are JSON strings while Parquet preserves nested representation through pandas/PyArrow.
- Best Buy current extraction validates Marketplace/new-condition PDP context and publishes all normalized Marketplace offers from the offers API, with best-effort seller enrichment.
- Amazon current production has a hard search-health publication gate, exact variant prefilter/detail rules, and a stricter search-verified fallback.
- Product matching uses deterministic evidence/scoring plus authoritative Amazon exact-variant/verification-state overrides; scores are not calibrated probabilities.
- Walmart currently remains probe/research maturity and is explicitly blocked in end-to-end production orchestration.
- `PipelineSettings.max_retries` exists, but shared `HttpClient.get()` currently hard-codes three attempts.

## Current Data-Quality/Research Findings

These are current implementation/documentation findings, not unresolved documentation omissions:

### Amazon known-ASIN recovery gap

The current committed Amazon validation report passes its structural/semantic checks for produced rows but reports two expected ASINs missing from known-ASIN coverage. Do not describe Amazon recovery as exhaustive.

### Stale product-matching validation report

`docs/LATEST_PRODUCT_MATCHING_REPORT.md` is stale relative to current executable Amazon matching behavior. Current unit tests/source make Amazon exact-variant and verification-state rules authoritative, while the retained report reflects older generic `attribute_score` outcomes.

A future source-repository maintenance task should regenerate this report only after confirming current upstream `latest/` inputs are the intended datasets.

### Walmart search detector inconsistency

Current Walmart search evidence is visibly redirected to `/blocked` with `Verify Your Identity` / `We like real shoppers, not robots!`, but the search probe's structured `block_signals` currently remains empty for that exact challenge wording. The Walmart detail probe has stronger challenge detection and correctly recognizes the observed flow.

### Historical Amazon success semantics

Older Amazon run diagnostics contain zero-result runs recorded as successful. These predate the current `amazon_search_health.py` hard gate and are historical evidence only.

## Security and Access

Credential/configuration names such as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are documented where operationally relevant. Their values are not published.

Repository source verifies configured AWS interfaces and secret names, but not exact current live IAM policy, bucket policy, encryption, versioning, lifecycle, or account-level state.

No live AWS evidence was required to complete the assigned documentation scope. If future maintenance requires exact live state, request one coherent authoritative AWS source at a time, provide click-by-click retrieval instructions, identify fields to redact, and persist the sanitized evidence into this documentation repository.

## Validation and Cross-Page Review

The final `main` tree contains all assigned pages under `repositories`, `data`, `systems`, and `archive`. Internal links are covered by the site validator, and each focused page passed validation before merge.

Final review confirmed:

- no target page was created per individual probe script;
- Walmart current probes remain in the active diagnostics model rather than being incorrectly archived;
- historical experiments are grouped under one archive page;
- matching acquisition scores and final match states are documented separately;
- current-vs-planned wording is explicit;
- credential values/private account identifiers are absent;
- the catalogue itself was not modified by routine workstream execution.

## Known Limitations

- Live AWS deployment state remains intentionally unverified beyond repository-configured interfaces.
- Retailer page/API behavior is external and can change after `last_verified` dates.
- Report filenames containing `LATEST` do not guarantee semantic currency.
- The product-matching validation report needs regeneration against current source/output before it can be cited as current operational validation.
- Walmart search block detection should be aligned with the stronger detail detector before any future production-enablement discussion.
- Source repository experiments retained on `main` can still be manually runnable even when archived here as superseded operational authority.

## Outstanding Work

There are no missing assigned catalogue documentation targets.

Future work is maintenance-driven rather than catalogue completion:

1. Update the relevant page when `bb-comp-prices` implementation/workflows/configuration change.
2. Regenerate and re-evaluate the matching validation report when current matching outputs are intentionally refreshed.
3. If Walmart challenge behavior changes, update probe detection/tests and the Walmart page before proposing production acquisition.
4. Verify live AWS state only when a concrete operational question requires it.
5. Keep this plan synchronized when major successor architecture changes make any page obsolete.

## Next Safe Development Action

Do not create additional `bb-comp-prices` top-level documentation pages merely to continue the workstream. The next safe action is source-driven maintenance: when a concrete `bb-comp-prices` implementation change occurs, identify the existing authoritative page affected, re-verify current source/workflow/test evidence, update that page in a focused `docs/bb-comp-*` PR, run documentation validation, merge, and confirm the resulting Pages deployment.

If choosing an implementation-quality task rather than documentation maintenance, the lowest-risk known candidates are regenerating current product-matching validation evidence or aligning Walmart search challenge detection with the already-tested detail detector. Those changes belong in `bb-comp-prices` source and should be handled as separate implementation work, not silently changed by this documentation closeout.

## Handoff Notes

- Use repository name only with the GitHub integration; the owner is configured separately.
- Keep future branch names unique to this workstream (`docs/bb-comp-*`).
- Do not edit parallel workstream plans during routine maintenance.
- Re-read current source before changing claims; external retailer behavior is time-sensitive.
- Preserve the evidence hierarchy and current/planned/experimental/superseded classifications.

## Related Documents

- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)
- [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)
- [bb-comp-prices orchestration/security boundary](/projects/systems/bb-comp-prices-orchestration-security/)
- [bb-comp-prices diagnostics/research framework](/projects/systems/bb-comp-prices-diagnostics-research/)
- [bb-comp-prices validation/data-quality framework](/projects/systems/bb-comp-prices-validation-data-quality/)
- [bb-comp-prices developer reference](/projects/systems/bb-comp-prices-developer-reference/)
- [Superseded bb-comp-prices probes/experiments](/projects/archive/bb-comp-prices-superseded-probes-experiments/)
- [Documentation target catalogue](/projects/high-director/documentation-target-catalogue/)
- [Repository documentation discovery plan](/projects/high-director/repository-documentation-discovery/)
- [bb-comp-prices repository scan](/projects/high-director/repository-scan-bb-comp-prices/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `eirepolitic.github.io` `main` tree after PR #99; all published `bb-comp-prices` repository/data/system/archive pages; documentation validator workflow; current `bb-comp-prices` source/configuration/workflow/test/probe/report evidence inspected throughout this workstream.
- Verified by: High Director
- Verification scope: assigned catalogue coverage, page presence, cross-page relationships, delivery gates, implementation findings, known validation/research gaps, security boundary, and maintenance handoff.
- Unverified areas: exact live AWS/IAM/S3 deployment state beyond repository configuration; future retailer behavior after the verification date.
