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
| 52 | S3 Column Deleter | reconciliation draft on `docs/ipa-legacy-s3-column-deleter` |
| 53 | Retained debate/member enrichment and classification scripts | pending |
| 54 | Experimental/editorial content-generation workflows | pending |

## Verified P3 findings

- **47 Constituency Images Indexer:** retained image index remains an explicit source for the newer Oireachtas constituency-image enrichment/compatibility layer; full retirement is not established.
- **48 Debate Issue Classifier:** retained legacy classifier still produces issue labels; the newer Oireachtas layer validates/adapts that classified CSV and does not call OpenAI itself.
- **49 LLM Column Creator:** no separate current implementation remains; the old concept is superseded/generalized by the current Reusable LLM Task Runner Framework.
- **50 Member Images Pipeline:** retained scraper remains the photo-discovery producer; newer Oireachtas photo enrichment consumes the legacy nested/root fallback CSV and does not scrape new pages. Full scraper retirement is not established.
- **51 Member Summaries Table:** retained background summarizer still generates `background`; newer Oireachtas enrichment consumes that table without calling OpenAI. The same table is also shared by current generic LLM tasks, with different column-preservation semantics.
- **52 S3 Column Deleter:** current implementation remains a manually dispatchable destructive in-place S3 utility. `STRICT=1` only requires the target column to exist in both representations before writes; it is not a dry-run, backup, confirmation, rollback, or isolation mode. Current safety/operating guidance belongs to the P2 maintenance reference, while the archive page preserves the historical utility identity and lineage.

## Discovery state

- [x] P0 complete
- [x] P1 complete
- [x] P2 target 38 complete
- [x] P3 targets 47–51 complete
- [x] P3 target 52 archive/current-operation reconciliation audited
- [ ] P3 target 53 retained enrichment/classification lineage
- [ ] P3 target 54 experimental/editorial workflows

## PR ledger

| Component | PR | Validation | Pages | Result |
| --- | --- | --- | --- | --- |
| P0/P1/P2 prior components | #62–#107 | passed | exact-SHA Pages gates passed | complete |
| P3 Constituency Images Indexer | #108 | `31240091714` success | `31240103424` success | complete |
| P3 Debate Issue Classifier | #109 | `31240199572` success | `31240218461` success | complete |
| P3 LLM Column Creator | #110 | `31240280395` success | `31240290648` success | complete |
| P3 Member Images Pipeline | #111 | `31240361712` success | `31240378449` success | complete |
| P3 Member Summaries Table | #112 | `31240455460` success | `31240471450` success; SHA `8e2eca79cc4ee33a7c47e0bdbda529645735e82e` | complete |
| P3 S3 Column Deleter | pending PR | pending | pending | draft in progress |

## Next action

Validate, merge, and exact-SHA Pages-verify target 52. Only after that succeeds, begin target 53 retained enrichment/classification lineage from current `main`.
