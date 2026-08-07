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

Use this evidence order:

1. current implementation and checked-in configuration;
2. observed runtime evidence;
3. user-supplied authoritative source;
4. current repository documentation/handoffs;
5. historical/archive documentation;
6. labelled inference only.

Never publish secrets, credentials, private keys, personal identifiers, private individual URLs, or confidential identifiers.

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
| 2 | `eirepolitic-data-pipeline` repository | draft on `docs/ipa-repository` |
| 3 | Unified Oireachtas Data Platform | discovery in progress |
| 4 | Oireachtas canonical data-product catalogue | discovery in progress |
| 5 | Oireachtas refresh/validation orchestration | discovery in progress |
| 6 | Oireachtas write policies and downstream contracts | discovery in progress |

## Discovery checklist

### Documentation repository

- [x] `DOCUMENTATION_STANDARD.md`
- [x] complete `_templates/` directory
- [x] owner-wide target catalogue and discovery plan
- [x] `projects/ipa-overview.md`
- [x] assigned archive pages
- [x] representative repository/system/runbook pages and validator

### `eirepolitic-data-pipeline`

- [x] full repository tree enumerated
- [x] root README/dependencies
- [x] complete `configs/` tree and Oireachtas configuration
- [x] complete `extract/` tree; current Oireachtas package distinguished from older top-level extractors
- [x] complete `process/` tree; major current and retained legacy families mapped
- [x] complete Oireachtas workflow tree; production orchestrator/reusable refresh/reusable validation inspected
- [x] `docs/oireachtas_packet_status.md` and complete `docs/` tree inventoried
- [x] complete `instagram/` tree inventoried; detailed P1 behavior remains later work
- [x] `process/build_member_profile_metrics.py` and its manual workflow
- [x] `process/llm_table_runner.py`, `tasks/llm_task_template.yml`, and controller workflow
- [x] complete `tasks/` tree inventoried
- [x] complete `tests/` tree inventoried
- [ ] per-table Oireachtas builder lineage/DQ reconciliation for the platform/catalogue pages
- [ ] detailed maintenance/backfill utility status for P2
- [ ] detailed retained legacy/editorial successor/status audit for P3

## Current verified discovery notes

- `configs/oireachtas/tables.yml` contains 31 confirmed products: 23 silver, 3 control, 5 gold.
- The central table CLI is `python -m extract.oireachtas.build_table`.
- Checked-in Oireachtas defaults are `ca-central-1`, bucket `eirepolitic-data`, API base `https://api.oireachtas.ie/v1`, and source-data base `https://data.oireachtas.ie`.
- Current Oireachtas production publication uses immutable batches under `processed/oireachtas_unified/batches/<batch_id>/` and production/previous pointers under `processed/oireachtas_unified/pointers/`.
- Write policies define snapshot-replace, upsert, append, and rebuild behavior; policy-aware merge is applied in current S3 write handling.
- Downstream contracts currently define six compatibility datasets.
- Scheduled orchestration has weekly, monthly, and yearly triggers and automatic promotion only after successful refresh/validation on scheduled runs.
- **Observed runtime:** scheduled orchestrator run `30740881592` on 2026-08-02 completed refresh, validation, promotion and pointer verification successfully.
- The July `docs/oireachtas_packet_status.md` pending-observation language is historical and stale relative to August runtime evidence.
- Member profile metrics currently consume unified compatibility members/votes/photos/debate-label inputs and can write inside an immutable candidate batch.
- `process/llm_table_runner.py` is a YAML-driven resumable S3 → OpenAI Responses API → CSV/Parquet framework with retry, autosave, optional web search, overwrite/resume controls and output validation.
- The repository contains many enabled trial/patch/legacy/editorial workflows; enabled state alone is not evidence of current production intent.

## PR ledger

| Component | Branch / PR | Validation | Pages deployment | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | `docs/ipa-workstream-plan` / PR #62 | `31219424981` success | `31219454738` success; SHA `e25a90677d11c732bfe86a87616aa25191827cff` | complete |
| P0 umbrella architecture | `docs/ipa-architecture` / PR #64 | `31219706244` success | `31219726250` success; SHA `307441a2479cda507589bf77a796a54f6c0042ac` | complete |
| P0 repository page | `docs/ipa-repository` | pending | pending | draft in progress |
| P0 Unified Oireachtas platform | pending | pending | pending | pending |
| P0 data-product catalogue | pending | pending | pending | pending |
| P0 orchestration | pending | pending | pending | pending |
| P0 policies/contracts | pending | pending | pending | pending |

## Unknowns to resolve

- Complete per-table extraction/normalization lineage and table-specific DQ behavior.
- Exact cadence-specific table sets and date-window calculation from `process/oireachtas_refresh_inputs.py`.
- Detailed compatibility-adapter construction and enrichment staging behavior.
- Current intent/status of every legacy, repair, patch and experimental workflow.
- Exact live IAM/S3/Glue/Athena configuration where checked-in source cannot establish deployed state.

## Next action

Validate and publish the `eirepolitic-data-pipeline` repository page. After its exact Pages deployment succeeds, begin the Unified Oireachtas Data Platform component from current `main` and continue per-table implementation reconciliation. No architecture, security, cost, access-control, or irreversible runtime change is authorized by this workstream.
