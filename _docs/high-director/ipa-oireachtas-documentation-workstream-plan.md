---
title: "Irish Politics Analytics / Oireachtas documentation workstream plan"
summary: "Persistent execution plan for the Irish Politics Analytics and eirepolitic-data-pipeline documentation workstream."
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
systems:
  - irish-politics-analytics
repositories:
  - eirepolitic.github.io
  - eirepolitic-data-pipeline
permalink: /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
---

# Irish Politics Analytics / Oireachtas documentation workstream plan

## Purpose

This is the mutable execution plan for the Irish Politics Analytics / `eirepolitic-data-pipeline` documentation workstream. The owner-wide target catalogue remains the read-only scope contract.

## Scope contract

- **P0:** Irish Politics Analytics umbrella architecture; `eirepolitic-data-pipeline`; Unified Oireachtas Data Platform; canonical data-product catalogue; refresh/validation orchestration; write policies/downstream contracts.
- **P1:** Instagram/constituency rendering; AI member-profile/Instagram workflow; Member Profile Metrics Builder; Reusable LLM Task Runner Framework.
- **P2:** maintenance, repair, and backfill utilities.
- **P3:** assigned legacy enrichment/classification/media/destructive/editorial targets and successor mapping.

Excluded except for technically necessary cross-references: AutoDoc, `bb-comp-prices`, `degenerate_investigator`, and Overlord.

## Evidence rules

Use this evidence order: current implementation/configuration; observed runtime evidence; user-supplied authoritative source; current repository documentation/handoffs; historical/archive documentation; labelled inference only. Never publish secrets, credentials, private keys, personal identifiers, private individual URLs, or confidential identifiers.

## Working method

- Inspect current source completely enough to support the target being documented.
- Prefer exact paths, functions, workflows, configuration keys, tables, object keys, inputs/outputs, dependencies, failure modes, and validation procedures.
- Reconcile archive pages against source and document successor relationships rather than creating competing current pages.
- Use focused `docs/ipa-*` branches and PRs.
- Before every merge: documentation validation must pass; then merge; then the matching Pages deployment for the exact merged SHA must pass before the next major component.
- Start each new component from current `main` to avoid conflicts with parallel workstreams.

## P0 execution sequence

| Order | Component | State |
| --- | --- | --- |
| 1 | Irish Politics Analytics umbrella architecture | complete and published |
| 2 | `eirepolitic-data-pipeline` repository | complete and published |
| 3 | Unified Oireachtas Data Platform | draft on `docs/ipa-oireachtas-platform` |
| 4 | Oireachtas canonical data-product catalogue | discovery in progress |
| 5 | Oireachtas refresh/validation orchestration | discovery in progress |
| 6 | Oireachtas write policies and downstream contracts | discovery in progress |

## Discovery checklist

### Documentation repository

- [x] standard, complete templates, target catalogue and discovery plan
- [x] IPA overview and assigned archive pages
- [x] representative repository/system/runbook pages and validator

### `eirepolitic-data-pipeline`

- [x] full repository tree, root dependencies, `configs/`, `extract/`, `process/`, `docs/`, `instagram/`, `tasks/`, `tests/`
- [x] current Oireachtas API/schema/storage/batch/write-policy/contract core
- [x] current production orchestrator, reusable refresh and reusable validation
- [x] exact cadence table sets, modes, windows and page-size defaults
- [x] representative silver and gold builders and their DQ/storage patterns
- [x] current compatibility-adapter and executable contract behavior
- [x] member metrics and reusable LLM entry points at repository-map depth
- [ ] per-table Oireachtas builder lineage/DQ reconciliation for the canonical catalogue
- [ ] detailed maintenance/backfill utility status for P2
- [ ] detailed retained legacy/editorial successor/status audit for P3

## Current verified discovery notes

- Registry: 31 confirmed products — 23 silver, 3 control, 5 gold.
- API client performs complete offset pagination, retries HTTP 429/5xx, detects repeated pages and fails incomplete production pagination.
- Production publication uses immutable batches and production/previous pointers; candidate logical reads resolve to the active batch during validation.
- Weekly defaults: incremental, 35-day rolling window, page size 100. Monthly: incremental, previous month plus seven-day leading overlap, page size 200. Yearly: full, previous calendar year, page size 200.
- Compatibility contracts resolve through candidate/production state and enforce readability, columns, row minimum, PK integrity and freshness; comparison thresholds add key/row/join tolerances.
- **Observed runtime:** scheduled orchestrator run `30740881592` on 2026-08-02 completed refresh, validation, promotion and pointer verification successfully.
- July packet-status pending-observation statements are historical where contradicted by August runtime evidence.
- Repository legacy/trial workflow enablement alone is not evidence of production intent.

## PR ledger

| Component | Branch / PR | Validation | Pages deployment | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | `docs/ipa-workstream-plan` / PR #62 | `31219424981` success | `31219454738` success; SHA `e25a90677d11c732bfe86a87616aa25191827cff` | complete |
| P0 umbrella architecture | `docs/ipa-architecture` / PR #64 | `31219706244` success | `31219726250` success; SHA `307441a2479cda507589bf77a796a54f6c0042ac` | complete |
| P0 repository page | `docs/ipa-repository` / PR #66 | `31219954893` success | `31219991624` success; SHA `49c130d88cf84418be3f15a17848f8d50f3112e1` | complete |
| P0 Unified Oireachtas platform | `docs/ipa-oireachtas-platform` | pending | pending | draft in progress |
| P0 data-product catalogue | pending | pending | pending | pending |
| P0 orchestration | pending | pending | pending | pending |
| P0 policies/contracts | pending | pending | pending | pending |

## Unknowns to resolve

- Complete per-product extraction/normalization lineage and product-specific DQ behavior.
- Detailed status of every legacy, repair, patch and experimental workflow.
- Exact live IAM/S3/Glue/Athena configuration where checked-in source cannot establish deployed state.

## Next action

Validate and publish the Unified Oireachtas Data Platform page. After its exact Pages deployment succeeds, create the canonical data-product catalogue from current `main` and reconcile registry entries against their builders. No architecture, security, cost, access-control, or irreversible runtime change is authorized by this workstream.
