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
| 49 | LLM Column Creator | reconciliation draft on `docs/ipa-legacy-llm-column-creator` |
| 50 | Member Images Pipeline | pending |
| 51 | Member Summaries Table | pending |
| 52 | S3 Column Deleter | pending |
| 53 | Retained debate/member enrichment and classification scripts | pending |
| 54 | Experimental/editorial content-generation workflows | pending |

## Verified P3 findings

### Target 47 — Constituency Images Indexer

The retained legacy indexer still produces `processed/constituencies/constituency_images.csv`, which is the explicit source of the newer Oireachtas constituency-image enrichment trial. The newer layer adds trial/review/compatibility outputs but does not create/discover image objects. Full legacy retirement is not established.

### Target 48 — Debate Issue Classifier

The older monthly debate extraction remains scheduled in checked-in source and the manual `speech_issue_classifier.py` path remains the checked-in OpenAI label generator. The newer Oireachtas speech-issue enrichment module explicitly does not call OpenAI; it consumes `processed/debates/debate_speeches_classified.csv`, validates/reshapes it, and publishes the compatibility dataset used by current downstream contracts and member-profile metrics. Full classifier retirement is not established.

### Target 49 — LLM Column Creator

No separate current repository implementation named `LLM Column Creator` or `llm_column_creator` was identified. The archived page had incorrectly pointed directly at current `process/llm_table_runner.py` as though it were the archive target's own implementation. The correct relationship is a superseded predecessor concept whose capability has been generalized into the current Reusable LLM Task Runner Framework.

## Discovery state

- [x] P0 complete
- [x] P1 complete
- [x] P2 target 38 complete
- [x] P3 target 47 audited and published
- [x] P3 target 48 audited and published
- [x] P3 target 49 predecessor/successor mapping audited
- [ ] P3 target 50 Member Images Pipeline
- [ ] P3 target 51 Member Summaries Table
- [ ] P3 target 52 S3 Column Deleter
- [ ] P3 target 53 retained enrichment/classification lineage
- [ ] P3 target 54 experimental/editorial workflows

## PR ledger

| Component | PR | Validation | Pages | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | #62 | `31219424981` success | `31219454738` success | complete |
| P0 umbrella architecture | #64 | `31219706244` success | `31219726250` success | complete |
| P0 repository | #66 | `31219954893` success | `31219991624` success | complete |
| P0 Unified Oireachtas platform | #68 | `31220172926` success | `31220199307` success | complete |
| P0 catalogue | #70 + #73 | validation passed | `31220683272` success | complete |
| P0 orchestration | #74 + #84 | validation passed | `31229230209` success | complete |
| P0 policies/contracts | #85 | `31229340996` success | `31229357085` success | complete |
| P1 Instagram rendering | #90 + retries through #100 | validation passed | `31229966372` success | complete |
| P1 AI Instagram content | #104 | `31230259270` success | `31230282153` success | complete |
| P1 Member Profile Metrics | #105 | `31239709900` success | `31239725625` success | complete |
| P1 Reusable LLM Task Runner | #106 | `31239847243` success | `31239858541` success | complete |
| P2 maintenance/repair/backfill | #107 | `31239997132` success | `31240013265` success | complete |
| P3 Constituency Images Indexer | #108 | `31240091714` success | `31240103424` success; SHA `0e39df9568871353978341b01450ce6fe6ae8c1f` | complete |
| P3 Debate Issue Classifier | #109 | `31240199572` success | `31240218461` success; SHA `1209256adc461e3efff5e4a1947e1248f6131628` | complete |
| P3 LLM Column Creator | pending PR | pending | pending | draft in progress |

## Next action

Validate, merge, and exact-SHA Pages-verify target 49. Only after that succeeds, begin target 50 Member Images Pipeline from current `main`.
