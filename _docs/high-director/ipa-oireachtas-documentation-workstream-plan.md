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

## Final state

The assigned Irish Politics Analytics / `eirepolitic-data-pipeline` documentation workstream is complete.

All assigned P0, P1, P2 and P3 components have been discovered, reconciled, documented, validated, merged, and published through the required exact-SHA GitHub Pages gate.

The owner-wide target catalogue remains the read-only scope contract for any future documentation initiatives outside this completed workstream.

## Completed scope

### P0 — foundational

- Irish Politics Analytics umbrella architecture.
- `eirepolitic-data-pipeline` repository.
- Unified Oireachtas Data Platform.
- Oireachtas canonical data-product catalogue.
- Oireachtas refresh/validation orchestration.
- Oireachtas write policies and downstream contracts.

### P1 — active operational

- Instagram / constituency campaign rendering system.
- AI member-profile / Instagram visual content workflow.
- Member Profile Metrics Builder.
- Reusable LLM Task Runner Framework.

### P2 — supporting

- Data maintenance, repair, and backfill utilities.

### P3 — historical/status reconciliation

- Constituency Images Indexer.
- Debate Issue Classifier.
- LLM Column Creator.
- Member Images Pipeline.
- Member Summaries Table.
- S3 Column Deleter.
- Retained debate/member enrichment and classification lineage.
- Experimental/editorial content-generation workflows.

## Persistent architectural findings

- The Unified Oireachtas platform is the canonical current political-data foundation where equivalent canonical products exist.
- Four retained enrichment producer lineages remain transitional dependencies: constituency image indexing, member-photo discovery, member-summary generation, and speech issue classification.
- The corresponding `extract/oireachtas/enrichment_*` modules are adapter/review/compatibility layers rather than complete upstream replacements.
- `LLM Column Creator` is fully superseded as a named component by the current Reusable LLM Task Runner Framework.
- The S3 Column Deleter remains a destructive manual utility and should be operated only through the current maintenance/safety guidance.
- The retained ridiculous-sentences workflows are manual editorial experiments, not canonical data products or publishing pipelines.
- Current implementation/configuration is the primary source of truth; historical pages preserve provenance and successor relationships rather than competing with current system documentation.

## Publication ledger

| Component | PR | Validation | Exact-SHA Pages | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | #62 | `31219424981` | `31219454738` | complete |
| P0 umbrella architecture | #64 | `31219706244` | `31219726250` | complete |
| P0 repository | #66 | `31219954893` | `31219991624` | complete |
| P0 Unified Oireachtas platform | #68 | `31220172926` | `31220199307` | complete |
| P0 catalogue | #70 + retry #73 | passed | `31220683272` | complete |
| P0 orchestration | #74 + retry #84 | passed | `31229230209` | complete |
| P0 policies/contracts | #85 | `31229340996` | `31229357085` | complete |
| P1 Instagram rendering | #90 + retries through #100 | passed | `31229966372` | complete |
| P1 AI Instagram content | #104 | `31230259270` | `31230282153` | complete |
| P1 Member Profile Metrics | #105 | `31239709900` | `31239725625` | complete |
| P1 Reusable LLM Task Runner | #106 | `31239847243` | `31239858541` | complete |
| P2 maintenance/repair/backfill | #107 | `31239997132` | `31240013265` | complete |
| P3 Constituency Images Indexer | #108 | `31240091714` | `31240103424` | complete |
| P3 Debate Issue Classifier | #109 | `31240199572` | `31240218461` | complete |
| P3 LLM Column Creator | #110 | `31240280395` | `31240290648` | complete |
| P3 Member Images Pipeline | #111 | `31240361712` | `31240378449` | complete |
| P3 Member Summaries Table | #112 | `31240455460` | `31240471450` | complete |
| P3 S3 Column Deleter | #113 | `31240538235` | `31240557035` | complete |
| P3 legacy enrichment/classification lineage | #114 | `31240633404` | `31240646296` | complete |
| P3 experimental/editorial workflows | #115 | `31240767005` | `31240780787`; SHA `1fde69e260ecc2ba7fd3d30024e3729dd844ab30` | complete |

## Completion criteria

- [x] All assigned targets documented or reconciled.
- [x] Current versus historical evidence clearly separated.
- [x] Legacy successor/dependency relationships recorded.
- [x] Destructive/security-sensitive operating boundaries documented without exposing secret values.
- [x] Every substantive component passed documentation validation before merge.
- [x] Every substantive component received a successful Pages deployment for its exact merge SHA.
- [x] No unauthorized architecture, security, cost, access-control, or irreversible runtime change was made.

## Future maintenance

This plan now serves as a completion ledger rather than an execution queue.

Future implementation changes should update the relevant current system/reference page and any affected archive lineage page. In particular, if any retained enrichment producer is eventually replaced, update the lineage matrix and archive record only after current source proves the legacy output is no longer required.

Any new owner-wide documentation target should be taken from the canonical target catalogue or a newly approved discovery initiative rather than appended implicitly to this completed workstream.

## Final verification record

- Workstream completed: `2026-08-07` Pacific time / `2026-08-08` UTC publication activity.
- Final substantive target: P3 target 54, PR #115.
- Final substantive target validation: `31240767005` success.
- Final substantive target Pages deployment: `31240780787` success for SHA `1fde69e260ecc2ba7fd3d30024e3729dd844ab30`.
- Final remaining action for this ledger: validate, merge, and exact-SHA Pages-verify this completion-only synchronization change.
