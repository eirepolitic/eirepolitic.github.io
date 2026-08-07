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

This page is the mutable execution plan for the Irish Politics Analytics / `eirepolitic-data-pipeline` documentation workstream. The owner-wide target catalogue remains the read-only scope contract.

## Scope contract

The assigned catalogue targets are:

- **P0:** Irish Politics Analytics umbrella architecture; `eirepolitic-data-pipeline`; Unified Oireachtas Data Platform; canonical data-product catalogue; refresh/validation orchestration; write policies and downstream contracts.
- **P1:** Instagram/constituency campaign rendering; AI member-profile/Instagram content workflow; Member Profile Metrics Builder; Reusable LLM Task Runner Framework.
- **P2:** data maintenance, repair, and backfill utilities.
- **P3:** Constituency Images Indexer; Debate Issue Classifier; LLM Column Creator; Member Images Pipeline; Member Summaries Table; S3 Column Deleter; debate/speech classification and member-enrichment legacy scripts; experimental/editorial content-generation workflows.

Excluded except for technically necessary cross-references: AutoDoc, `bb-comp-prices`, `degenerate_investigator`, and Overlord.

## Evidence rules

Documentation in this workstream uses this evidence order:

1. current implementation and checked-in configuration;
2. observed runtime evidence from repository workflows or deployment records;
3. user-supplied authoritative source, when explicitly provided;
4. current repository documentation and handoff notes;
5. historical/archive documentation;
6. inference, which must be labelled and never presented as verified implementation.

Secrets, credentials, private keys, personal identifiers, private individual URLs, and confidential identifiers are never published.

## Working method

- Inspect the complete `eirepolitic-data-pipeline` tree before declaring coverage complete.
- Prefer exact repository paths, workflow names, commands, configuration keys, table names, object keys, inputs, outputs, dependencies, failure modes, and validation procedures.
- Reconcile archive pages against current or legacy source rather than cloning archive text into current-system pages.
- Record historical-to-current successor mappings where a legacy pipeline is superseded.
- Use one small, coherent documentation component per PR where practical.
- Before every documentation merge: run documentation validation, confirm success, merge, then confirm the matching `pages-build-deployment` run succeeds for the merged commit SHA.
- Do not start the next major component until Pages succeeds for the previous merged component.
- Sync from current `main` before final cross-cutting edits.

## P0 execution sequence

| Order | Component | Intended canonical output | State |
| --- | --- | --- | --- |
| 1 | Irish Politics Analytics umbrella architecture | system page describing the platform boundary, major subsystems, repositories, data flow, operational boundaries, and continuation map | draft on `docs/ipa-architecture` |
| 2 | `eirepolitic-data-pipeline` repository | repository page covering layout, entry points, dependencies, workflows, tests, operational controls, and safe change procedure | discovery in progress |
| 3 | Unified Oireachtas Data Platform | system page covering extraction, canonical/silver/gold/control layers, compatibility outputs, orchestration, and consumers | discovery in progress |
| 4 | Oireachtas canonical data-product catalogue | data/reference documentation derived from `configs/oireachtas/tables.yml` and implementation | discovery in progress |
| 5 | Oireachtas refresh/validation orchestration | runbook/system documentation for weekly/monthly/yearly refresh, orchestrator behavior, triggers, validation, failure handling, and observed runtime state | discovery in progress |
| 6 | Oireachtas write policies and downstream contracts | reference/runbook documentation derived from policy/contract configuration and enforcing code | discovery in progress |

## Discovery checklist

### Documentation repository

- [x] `DOCUMENTATION_STANDARD.md`
- [x] complete `_templates/` directory
- [x] `_docs/high-director/documentation-target-catalogue.md`
- [x] `_docs/high-director/repository-documentation-discovery-plan.md`
- [x] `projects/ipa-overview.md`
- [x] assigned archive pages for legacy IPA/Oireachtas pipelines
- [x] representative repository, system, and runbook pages

### `eirepolitic-data-pipeline`

- [x] full repository tree enumerated
- [x] root repository metadata and dependency definitions
- [x] `configs/oireachtas/`
- [ ] `extract/oireachtas/` — tree and core publication/policy entry points inspected; per-table builders still being reconciled
- [ ] `process/oireachtas/` — operational helper tree enumerated; individual procedures still being inspected
- [ ] `.github/workflows/oireachtas_*.yml` — complete workflow tree enumerated; production orchestrator/reusable refresh/reusable validation inspected
- [x] `docs/oireachtas_packet_status.md`
- [ ] `instagram/` — complete tree enumerated; implementation detail remains for P1
- [ ] `process/build_member_profile_metrics.py`
- [ ] `process/llm_table_runner.py`
- [ ] `tasks/` — complete tree enumerated; task schema/content remains for P1
- [ ] maintenance/backfill utilities
- [ ] legacy enrichment/classification scripts
- [ ] relevant tests and validation scripts

## Current verified discovery notes

Verified on 2026-08-07 against current `eirepolitic-data-pipeline` source/configuration unless otherwise labelled:

- `configs/oireachtas/tables.yml` contains 31 confirmed canonical products: 23 silver, 3 control, and 5 gold tables.
- The unified Oireachtas implementation is registry-driven and exposes `python -m extract.oireachtas.build_table` as its central table CLI.
- Checked-in Oireachtas defaults are AWS region `ca-central-1`, S3 bucket `eirepolitic-data`, API base `https://api.oireachtas.ie/v1`, and source-data base `https://data.oireachtas.ie`.
- Current production publication is immutable-batch based. Logical `processed/oireachtas_unified/latest/` and `processed/oireachtas_unified/compat/` keys resolve through `processed/oireachtas_unified/pointers/production.json`; candidate data is written under `processed/oireachtas_unified/batches/<batch_id>/`.
- `configs/oireachtas/write_policies.yml` defines snapshot-replace, upsert, append, and rebuild strategies plus selected relationship metadata. `extract/oireachtas/io_s3.py` applies policy-aware merging for candidate latest-table writes.
- `configs/oireachtas/downstream_contracts.yml` defines six compatibility datasets plus roster/member-vote comparison thresholds.
- The current refresh-validation orchestrator has weekly, monthly, and yearly scheduled triggers. Scheduled runs publish candidates, run consumer validation, and request automatic promotion only after refresh and validation succeed.
- **Observed runtime evidence:** scheduled orchestrator run `30740881592` on 2026-08-02 completed refresh, validation, promotion, pointer verification, and summary successfully.
- The July 2026 `docs/oireachtas_packet_status.md` handoff is now stale where it describes scheduled observation as pending; it remains historical handoff evidence, not current runtime truth.
- The repository also contains downstream member metrics, Instagram/content rendering, reusable LLM task execution, maintenance utilities, enrichment modules, retained legacy scripts, and editorial/experimental workflows. Detailed status classification remains in scope for P1-P3.

## PR ledger

| Component | Branch / PR | Validation | Pages deployment | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | `docs/ipa-workstream-plan` / PR #62 | run `31219424981` success | run `31219454738` success for merge SHA `e25a90677d11c732bfe86a87616aa25191827cff` | complete |
| P0 umbrella architecture | `docs/ipa-architecture` | pending | pending | draft in progress |
| P0 repository page | pending | pending | pending | pending |
| P0 Unified Oireachtas platform | pending | pending | pending | pending |
| P0 data-product catalogue | pending | pending | pending | pending |
| P0 orchestration | pending | pending | pending | pending |
| P0 policies/contracts | pending | pending | pending | pending |

## Unknowns to resolve from implementation or runtime evidence

- Exact cadence-specific table sets and date-window defaults used by `process/oireachtas_refresh_inputs.py`.
- Complete per-table extraction/normalization lineage and all table-specific failure/DQ rules.
- Exact current compatibility-adapter construction and enrichment staging behavior.
- Current intent/status of every legacy, repair, patch, and experimental workflow still registered as active in GitHub Actions.
- Exact current authentication/environment-variable boundaries for downstream OpenAI and external rendering paths.
- Exact live IAM/S3/Glue/Athena account configuration where source code cannot establish deployed state.

## Next action

Validate and publish the Irish Politics Analytics umbrella architecture. After the matching Pages deployment succeeds, start the `eirepolitic-data-pipeline` repository page from current `main` while continuing the implementation audit. No architecture, security, cost, access-control, or irreversible implementation change is authorized by this documentation workstream.
