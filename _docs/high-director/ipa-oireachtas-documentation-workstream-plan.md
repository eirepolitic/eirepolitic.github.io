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

Mutable execution plan for the Irish Politics Analytics / `eirepolitic-data-pipeline` documentation workstream. The owner-wide target catalogue remains the read-only scope contract.

## Scope

- **P0:** umbrella architecture; repository; Unified Oireachtas platform; canonical product catalogue; refresh/validation orchestration; write policies/downstream contracts.
- **P1:** Instagram/constituency rendering; AI member-profile/Instagram workflow; Member Profile Metrics Builder; Reusable LLM Task Runner Framework.
- **P2:** maintenance, repair, and backfill utilities.
- **P3:** assigned legacy enrichment/classification/media/destructive/editorial targets and successor mapping.

Excluded except for necessary cross-references: AutoDoc, `bb-comp-prices`, `degenerate_investigator`, and Overlord.

## Evidence and publication rules

Current implementation/configuration outranks runtime evidence, user-supplied authoritative sources, current handoffs, archive material, and labelled inference. Never publish secrets or personal/private account details.

Each major documentation component uses a focused `docs/ipa-*` PR. Before moving to the next component: documentation validation must pass, the PR must merge, and the matching `pages-build-deployment` run must succeed for that exact merge SHA.

## Priority execution state

### P0

All six P0 components are complete and published.

### P1

All four assigned P1 components are complete and published.

### P2

| Order | Component | State |
| --- | --- | --- |
| 38 | Data maintenance / repair / backfill utilities | draft on `docs/ipa-maintenance-repair-backfill` |

### P3

Targets 47–54 are pending successor/status reconciliation after target 38 publishes.

## Verified P1 discoveries

- The deterministic Instagram campaign workflow is review-only and does not publish, schedule, or approve content.
- The checked-in Option 5 AI workflows are manual experiments: member-profile template editing and constituency-cover background generation. Neither publishes or approves content.
- `process/build_member_profile_metrics.py` is the authoritative year-aware member metrics implementation and supports candidate-batch consumer output.
- `process/llm_table_runner.py` is the generic YAML-driven S3 table enrichment runner; current validation repair is soft and current same-key full-table tasks can drop unrelated enrichment fields if `keep` lists are incomplete.

## Verified P2 discoveries

- `process/oireachtas_audit_inventory.py` plus `o...baseline_audit.yml` form a read-only S3 inventory utility and explicitly disable Oireachtas publication flags.
- `process/delete_s3_column.py` plus `column_deleter.yml` are a current active manual destructive utility. The workflow has no dry-run, backup, confirmation token, rollback, prefix allow-list, or candidate isolation. CSV and Parquet are overwritten sequentially.
- The column deleter's `STRICT=1` only fails if the target column is absent from either representation before writes begin; it is not a dry-run/safety mode.
- Observed column-deleter runs `21647221436` and `21878566586` both succeeded in February 2026.
- `process/debate_speeches_csv_to_parquet.py` is a standalone compatibility/conversion helper: source CSV remains intact, target Parquet is overwritten, and column names are normalized/deduplicated.
- `o...repair_ci.yml` is non-mutating regression/registry/YAML validation despite retaining a repair-branch trigger.
- The `o...validation_fixes_*` workflows and `process/oireachtas_verify_validation_fixes.py` form a retained July 2026 branch-specific repair campaign, not the normal current backfill interface.
- The repair candidate workflow is hard-coded to batch `validation-fixes-20260719-3`, date window `2024-11-29` through `2026-07-19`, all 31 products, candidate-only publication, and downstream validation; it does not promote production.
- The acceptance workflow is S3 read-only but GitHub-mutating: it commits candidate acceptance evidence back to `fix/oireachtas-validation-findings` and uploads a 365-day artifact.
- Current branch inventory still contains `fix/oireachtas-validation-findings`, `release/oireachtas-validation-fixes-20260719-3`, and `repair/oireachtas-production-hardening`; branch existence is retained-source evidence, not routine-production intent.

## Discovery state

- [x] full P0 implementation/configuration/runtime audit and all six P0 documentation components
- [x] all four assigned P1 component audits and documentation
- [x] target 38 current utility inventory, mutation/risk classification, repair/backfill campaign status, and safe operating guidance
- [ ] P3 target 47 Constituency Images Indexer successor/status reconciliation
- [ ] P3 target 48 Debate Issue Classifier successor/status reconciliation
- [ ] P3 target 49 LLM Column Creator predecessor mapping to current LLM runner
- [ ] P3 target 50 Member Images Pipeline successor/status reconciliation
- [ ] P3 target 51 Member Summaries Table successor/status reconciliation
- [ ] P3 target 52 S3 Column Deleter archive/current-utility reconciliation
- [ ] P3 target 53 retained debate/member enrichment/classification scripts lineage audit
- [ ] P3 target 54 experimental/editorial workflow status audit

## PR ledger

| Component | PR | Validation | Pages | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | #62 | `31219424981` success | `31219454738` success; `e25a90677d11c732bfe86a87616aa25191827cff` | complete |
| P0 umbrella architecture | #64 | `31219706244` success | `31219726250` success; `307441a2479cda507589bf77a796a54f6c0042ac` | complete |
| P0 repository | #66 | `31219954893` success | `31219991624` success; `49c130d88cf84418be3f15a17848f8d50f3112e1` | complete |
| P0 Unified Oireachtas platform | #68 | `31220172926` success | `31220199307` success; `74aa6405164440b62d28e6ac64d76f01388a7957` | complete |
| P0 data-product catalogue | #70 | `31220389309` success | initial exact-SHA deployment cancelled; later retry succeeded | complete |
| P0 orchestration | #74 | validation passed | initial exact-SHA deployment cancelled; later retry succeeded | complete |
| P0 policies/contracts | #85 | `31229340996` success | `31229357085` success; `021db2fe9fb9ea6b1d581b121508bdd8cd81bb83` | complete |
| P1 Instagram/constituency rendering | #90 plus retries | validation passed | final retry `31229966372` success; `925938a0db20c0d58f5fda33f1fb361bc53dcf1d` | complete |
| P1 AI member-profile / Instagram content | #104 | `31230259270` success | `31230282153` success; `507464f44a3321b70a473bd75095abb28da22f08` | complete |
| P1 Member Profile Metrics Builder | #105 | `31239709900` success | `31239725625` success; `c2422d9e9d2ee958563be10114c23961df8e6c1e` | complete |
| P1 Reusable LLM Task Runner Framework | #106 | `31239847243` success | `31239858541` success; `dd573507439153e9f18c8520549548c12c65c126` | complete |
| P2 Data maintenance/repair/backfill utilities | pending PR | pending | pending | draft in progress |

## Publication-gate note

Targets 18, 19, and 20 all passed their exact-SHA Pages gates normally after target 17's earlier publication-concurrency retries. P2 target 38 must now pass validation and exact-SHA Pages before P3 begins.

## Next action

Validate, merge, and exact-SHA Pages-verify the data maintenance/repair/backfill utilities reference. Only after that gate succeeds, begin P3 target 47 from current `main` and reconcile each historical page against current successors one target at a time.
