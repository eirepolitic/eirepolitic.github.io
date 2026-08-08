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
| 50 | Member Images Pipeline | reconciliation draft on `docs/ipa-legacy-member-images` |
| 51 | Member Summaries Table | pending |
| 52 | S3 Column Deleter | pending |
| 53 | Retained debate/member enrichment and classification scripts | pending |
| 54 | Experimental/editorial content-generation workflows | pending |

## Verified P3 findings

- **47 Constituency Images Indexer:** retained image index remains an explicit source for the newer Oireachtas constituency-image enrichment/compatibility layer; full retirement is not established.
- **48 Debate Issue Classifier:** retained legacy classifier still produces issue labels; the newer Oireachtas layer validates/adapts that classified CSV and does not call OpenAI itself.
- **49 LLM Column Creator:** no separate current implementation remains; the old concept is superseded/generalized by the current Reusable LLM Task Runner Framework.
- **50 Member Images Pipeline:** `process/members_photo_urls.py` remains the photo-discovery scraper. The current manual workflow overrides the script's old root-level output paths and writes under `processed/members/member_photos/`. The newer Oireachtas member-photo enrichment checks that nested path first, falls back to the old root-level path, and explicitly does not scrape new pages. It publishes richer trial/review data plus `members_photo_urls_compat.csv`, which feeds current member metrics/Instagram consumers. Full scraper retirement is not established.

## Discovery state

- [x] P0 complete
- [x] P1 complete
- [x] P2 target 38 complete
- [x] P3 target 47 complete
- [x] P3 target 48 complete
- [x] P3 target 49 complete
- [x] P3 target 50 member-photo legacy/current lineage audited
- [ ] P3 target 51 Member Summaries Table
- [ ] P3 target 52 S3 Column Deleter
- [ ] P3 target 53 retained enrichment/classification lineage
- [ ] P3 target 54 experimental/editorial workflows

## PR ledger

| Component | PR | Validation | Pages | Result |
| --- | --- | --- | --- | --- |
| P0/P1/P2 prior components | #62–#107 | passed | exact-SHA Pages gates passed | complete |
| P3 Constituency Images Indexer | #108 | `31240091714` success | `31240103424` success; SHA `0e39df9568871353978341b01450ce6fe6ae8c1f` | complete |
| P3 Debate Issue Classifier | #109 | `31240199572` success | `31240218461` success; SHA `1209256adc461e3efff5e4a1947e1248f6131628` | complete |
| P3 LLM Column Creator | #110 | `31240280395` success | `31240290648` success; SHA `46c2c8e8361715a7e2950ff3cee36d930706ab1c` | complete |
| P3 Member Images Pipeline | pending PR | pending | pending | draft in progress |

## Next action

Validate, merge, and exact-SHA Pages-verify target 50. Only after that succeeds, begin target 51 Member Summaries Table from current `main`.
