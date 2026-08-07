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
| 3 | Unified Oireachtas Data Platform | complete and published |
| 4 | Oireachtas canonical data-product catalogue | publication retry on `docs/ipa-oireachtas-catalogue-pages-retry` |
| 5 | Oireachtas refresh/validation orchestration | discovery complete enough to draft; blocked on catalogue Pages gate |
| 6 | Oireachtas write policies and downstream contracts | discovery complete enough to draft; blocked on prior P0 gates |

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
- [x] all 31 registry definitions, PKs, columns, cadences, endpoints, statuses and builder locations
- [x] configured write strategy and selected relationship metadata for all 31 products
- [x] representative silver and gold builder DQ/storage behavior
- [x] current compatibility-adapter and executable contract behavior
- [x] batch control, candidate seeding/reassembly, promotion and rollback guard behavior
- [x] write-policy merge/integrity tests and refresh-orchestration tests
- [x] member metrics and reusable LLM entry points at repository-map depth
- [ ] detailed maintenance/backfill utility status for P2
- [ ] detailed retained legacy/editorial successor/status audit for P3

## Current verified discovery notes

- Registry: 31 confirmed products — 23 silver, 3 control, 5 gold. Registry columns are authoritative names/order but do not encode formal types/nullability.
- API client performs complete offset pagination, retries HTTP 429/5xx, detects repeated pages and fails incomplete production pagination.
- Production publication uses immutable batches and production/previous pointers; candidate logical reads resolve to the active batch during validation.
- Weekly defaults: incremental, 35-day rolling window, page size 100. Monthly: incremental, previous month plus seven-day leading overlap, page size 200. Yearly: full, previous calendar year, page size 200.
- Write strategies: snapshot replacement for core dimensions/current manifest, upsert for history/facts, append for run/DQ audit streams, rebuild for all gold products.
- Compatibility contracts resolve through candidate/production state and enforce readability, columns, row minimum, PK integrity and freshness; comparison thresholds add key/row/join tolerances.
- Auxiliary enrichment staging refuses source objects older than each contract maximum before copying them into a candidate and records candidate provenance.
- Batch pointer mutation requires both `OIREACHTAS_PUBLISH_ENABLED=true` and `OIREACHTAS_PUBLISH_LATEST=true` in the batch-control CLI.
- **Observed runtime:** scheduled orchestrator run `30740881592` on 2026-08-02 completed refresh, validation, promotion and pointer verification successfully.
- July packet-status pending-observation statements are historical where contradicted by August runtime evidence.
- Repository legacy/trial workflow enablement alone is not evidence of production intent.

## PR ledger

| Component | Branch / PR | Validation | Pages deployment | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | `docs/ipa-workstream-plan` / PR #62 | `31219424981` success | `31219454738` success; SHA `e25a90677d11c732bfe86a87616aa25191827cff` | complete |
| P0 umbrella architecture | `docs/ipa-architecture` / PR #64 | `31219706244` success | `31219726250` success; SHA `307441a2479cda507589bf77a796a54f6c0042ac` | complete |
| P0 repository page | `docs/ipa-repository` / PR #66 | `31219954893` success | `31219991624` success; SHA `49c130d88cf84418be3f15a17848f8d50f3112e1` | complete |
| P0 Unified Oireachtas platform | `docs/ipa-oireachtas-platform` / PR #68 | `31220172926` success | `31220199307` success; SHA `74aa6405164440b62d28e6ac64d76f01388a7957` | complete |
| P0 data-product catalogue | `docs/ipa-oireachtas-catalogue` / PR #70 | `31220389309` success | `31220425800` cancelled for merge SHA `cc8d53cb4f96e5df40316d51e1ab7a1545b1db47` after a newer parallel `main` Pages run started; build did not report a content/Jekyll failure | publication retry in progress |
| P0 catalogue Pages retry | `docs/ipa-oireachtas-catalogue-pages-retry` | pending | pending | in progress |
| P0 orchestration | pending | pending | pending | pending |
| P0 policies/contracts | pending | pending | pending | pending |

## Publication-gate incident note

The first Pages deployment for catalogue PR #70 was cancelled while Jekyll was running because a newer `main` commit started another Pages deployment. The newer run `31220463394` succeeded for SHA `eea476070d0d55594fa7e397e9ffe94321eafa31`, but it is not accepted as the catalogue publication proof because this workstream requires the matching merged SHA to succeed. A focused retry is therefore being published and validated from current `main` before P0 orchestration work begins.

## Unknowns to resolve

- Exact live IAM/S3/Glue/Athena configuration where checked-in source cannot establish deployed state.
- Detailed status of every legacy, repair, patch and experimental workflow, reserved for P2/P3.
- Formal data types/nullability for canonical columns are not declared by the registry and should not be invented without typed source/observed schema evidence.

## Next action

Complete the catalogue publication retry: validate, merge, and require Pages success for the retry merge SHA. Only after that exact gate succeeds, create the refresh/validation orchestration runbook from current `main`, then complete the P0 write-policy/downstream-contract reference. No architecture, security, cost, access-control, or irreversible runtime change is authorized by this workstream.
