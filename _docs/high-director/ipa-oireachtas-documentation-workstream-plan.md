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

Target 38 is complete and published.

### P3

| Order | Component | State |
| --- | --- | --- |
| 47 | Constituency Images Indexer | reconciliation draft on `docs/ipa-legacy-constituency-images` |
| 48 | Debate Issue Classifier | pending |
| 49 | LLM Column Creator | pending |
| 50 | Member Images Pipeline | pending |
| 51 | Member Summaries Table | pending |
| 52 | S3 Column Deleter | pending |
| 53 | Retained debate/member enrichment and classification scripts | pending |
| 54 | Experimental/editorial content-generation workflows | pending |

## Verified P2 discoveries

- The baseline Oireachtas inventory is read-only and explicitly disables publication flags.
- The S3 column deleter is a current manual destructive utility with no dry-run, backup, confirmation token, rollback, prefix allow-list, or candidate isolation; CSV and Parquet are overwritten sequentially.
- `STRICT=1` only verifies the column is present in both representations before writes; it is not a safety/dry-run mode.
- The debate CSV→Parquet helper preserves the source CSV but overwrites a normalized Parquet output.
- The July 2026 validation-fixes workflows are retained branch/batch/date-specific repair-campaign tooling, not the normal reusable production backfill interface.

## Verified P3 target-47 discoveries

- `process/constituency_images_indexer.py` and `.github/workflows/constituency_images_index.yml` remain present on current `main`.
- Observed legacy workflow run `21652253875` succeeded on 2026-02-03; this is historical runtime evidence, not proof of current production intent.
- The newer `extract/oireachtas/enrichment_constituency_images.py` explicitly reads `processed/constituencies/constituency_images.csv`, the legacy index output.
- The newer enrichment module does not create/download/overwrite image files. It reshapes the legacy index into richer trial/review outputs and a Unified Oireachtas compatibility adapter.
- The current relationship is therefore dependency/adapter migration, not full replacement: image discovery/index creation remains upstream in the retained legacy implementation.
- Current source does not establish complete retirement of the legacy indexer, so the archive page must preserve lineage rather than claim a clean successor cutover.

## Discovery state

- [x] full P0 implementation/configuration/runtime audit and documentation
- [x] all four assigned P1 component audits and documentation
- [x] P2 target 38 utility inventory, risk classification, repair/backfill status, and operating guidance
- [x] P3 target 47 legacy/current constituency-image lineage audit
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
| P0 catalogue | #70 plus retry #73 | validation passed | final exact-SHA Pages success `31220683272`; `6f5c9c1d9685addeed5ec75a05a6d701de04733d` | complete |
| P0 orchestration | #74 plus retry #84 | validation passed | final exact-SHA Pages success `31229230209`; `9b68becb6e2ca69c58c57cf1b2104948ec6a60d0` | complete |
| P0 policies/contracts | #85 | `31229340996` success | `31229357085` success; `021db2fe9fb9ea6b1d581b121508bdd8cd81bb83` | complete |
| P1 Instagram/constituency rendering | #90 plus retries | validation passed | final retry `31229966372` success; `925938a0db20c0d58f5fda33f1fb361bc53dcf1d` | complete |
| P1 AI member-profile / Instagram content | #104 | `31230259270` success | `31230282153` success; `507464f44a3321b70a473bd75095abb28da22f08` | complete |
| P1 Member Profile Metrics Builder | #105 | `31239709900` success | `31239725625` success; `c2422d9e9d2ee958563be10114c23961df8e6c1e` | complete |
| P1 Reusable LLM Task Runner Framework | #106 | `31239847243` success | `31239858541` success; `dd573507439153e9f18c8520549548c12c65c126` | complete |
| P2 Data maintenance/repair/backfill utilities | #107 | `31239997132` success | `31240013265` success; `f46435b4aabb2b7ca9298e531744431ee658c62b` | complete |
| P3 Constituency Images Indexer reconciliation | pending PR | pending | pending | draft in progress |

## Publication-gate note

P2 target 38 passed its exact-SHA Pages gate in run `31240013265`. P3 target 47 began only after that success. Every P3 reconciliation must use the same validation → merge → exact-SHA Pages discipline before the next target begins.

## Next action

Validate, merge, and exact-SHA Pages-verify target 47. Only after that gate succeeds, begin target 48 Debate Issue Classifier from current `main`.
