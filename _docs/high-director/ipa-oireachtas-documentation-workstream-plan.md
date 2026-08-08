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

## Scope and publication rule

P0 covers the current Oireachtas platform; P1 covers Instagram/member metrics/LLM systems; P2 covers maintenance/repair/backfill; P3 reconciles assigned legacy enrichment/classification/media/destructive/editorial targets against current successors.

Current implementation/configuration outranks runtime evidence, handoffs, archive material, and labelled inference. Each major component must pass documentation validation, merge, and then receive a successful `pages-build-deployment` for that exact merge SHA before the next component begins.

## Priority execution state

- **P0:** complete and published.
- **P1:** complete and published.
- **P2 target 38:** complete and published.

### P3

| Order | Component | State |
| --- | --- | --- |
| 47 | Constituency Images Indexer | complete and published |
| 48 | Debate Issue Classifier | complete and published |
| 49 | LLM Column Creator | complete and published |
| 50 | Member Images Pipeline | complete and published |
| 51 | Member Summaries Table | complete and published |
| 52 | S3 Column Deleter | complete and published |
| 53 | Retained debate/member enrichment and classification scripts | complete and published |
| 54 | Experimental/editorial content-generation workflows | draft on `docs/ipa-experimental-editorial-workflows` |

## Verified P3 findings

- Targets 47/48/50/51 reveal a common transitional pattern: retained producer → legacy mutable S3 output → newer Unified Oireachtas enrichment/review adapter → compatibility product → current contracts/consumers.
- **47 Constituency Images Indexer:** newer Oireachtas code consumes the legacy image index and does not discover/create images.
- **48 Debate Issue Classifier:** newer Oireachtas code consumes existing classified speech output and does not call OpenAI.
- **49 LLM Column Creator:** historical concept is superseded by the current reusable LLM task runner; no separate current implementation remains.
- **50 Member Images Pipeline:** newer Oireachtas member-photo enrichment consumes retained legacy photo-index output and does not scrape member pages.
- **51 Member Summaries Table:** newer Oireachtas summaries enrichment consumes the retained summary table and does not generate summaries; that legacy table is also shared by generic LLM tasks.
- **52 S3 Column Deleter:** retained destructive implementation remains manually dispatchable; current operational/safety guidance belongs to the P2 maintenance reference.
- **53 cross-cutting lineage:** the four `extract/oireachtas/enrichment_*` modules are adapter/review/compatibility layers, not complete upstream replacements. Full retirement is not established for the corresponding legacy producers. Older scheduled debate/member extraction also coexists with the canonical Oireachtas platform and still feeds parts of the legacy enrichment lineage.
- **54 experimental/editorial workflows:** the retained ridiculous-sentences family is manual-only, reads legacy debate speech data, calls the OpenAI Responses API, writes direct legacy S3 CSV/Parquet outputs, and has no publishing/approval/canonical Oireachtas integration. Weekly has two observed successful April 2026 runs; experiments has one failed then one successful April run. Current classification is retained manual editorial experiment, not production system.

## Discovery state

- [x] P0 complete
- [x] P1 complete
- [x] P2 target 38 complete
- [x] P3 targets 47–53 complete
- [x] P3 target 54 experimental/editorial workflow status audit drafted

## PR ledger

| Component | PR | Validation | Pages | Result |
| --- | --- | --- | --- | --- |
| P0/P1/P2 prior components | #62–#107 | passed | exact-SHA Pages gates passed | complete |
| P3 Constituency Images Indexer | #108 | `31240091714` success | `31240103424` success | complete |
| P3 Debate Issue Classifier | #109 | `31240199572` success | `31240218461` success | complete |
| P3 LLM Column Creator | #110 | `31240280395` success | `31240290648` success | complete |
| P3 Member Images Pipeline | #111 | `31240361712` success | `31240378449` success | complete |
| P3 Member Summaries Table | #112 | `31240455460` success | `31240471450` success | complete |
| P3 S3 Column Deleter | #113 | `31240538235` success | `31240557035` success | complete |
| P3 legacy enrichment/classification lineage | #114 | `31240633404` success | `31240646296` success; SHA `c0420b2f3f7f783823aec939c82a48d7e8013130` | complete |
| P3 experimental/editorial workflows | pending PR | pending | pending | draft in progress |

## Next action

Validate, merge, and exact-SHA Pages-verify target 54. After that succeeds, create one final plan-only synchronization PR marking the entire assigned P0–P3 workstream complete and close it only after its exact-SHA Pages deployment also succeeds.
