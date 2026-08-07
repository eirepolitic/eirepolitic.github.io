---
layout: default
title: "Irish Politics Analytics / Oireachtas documentation workstream plan"
description: "Persistent execution plan for documenting the Irish Politics Analytics and eirepolitic-data-pipeline workstream."
doc_type: high-director
status: active
updated: 2026-08-07
owner: High Director
systems:
  - irish-politics-analytics
repositories:
  - eirepolitic.github.io
  - eirepolitic-data-pipeline
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
| 1 | Irish Politics Analytics umbrella architecture | system page describing the platform boundary, major subsystems, repositories, data flow, operational boundaries, and continuation map | discovery in progress |
| 2 | `eirepolitic-data-pipeline` repository | repository page covering layout, entry points, dependencies, workflows, tests, operational controls, and safe change procedure | pending |
| 3 | Unified Oireachtas Data Platform | system page covering extraction, canonical/silver/gold/control layers, compatibility outputs, orchestration, and consumers | pending |
| 4 | Oireachtas canonical data-product catalogue | data/reference documentation derived from `configs/oireachtas/tables.yml` and implementation | pending |
| 5 | Oireachtas refresh/validation orchestration | runbook/system documentation for weekly/monthly/yearly refresh, orchestrator behavior, triggers, validation, failure handling, and observed runtime state | pending |
| 6 | Oireachtas write policies and downstream contracts | reference/runbook documentation derived from policy/contract configuration and enforcing code | pending |

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
- [ ] root repository metadata and dependency definitions
- [ ] `configs/oireachtas/`
- [ ] `extract/oireachtas/`
- [ ] `process/oireachtas/`
- [ ] `.github/workflows/oireachtas_*.yml`
- [x] `docs/oireachtas_packet_status.md`
- [ ] `instagram/`
- [ ] `process/build_member_profile_metrics.py`
- [ ] `process/llm_table_runner.py`
- [ ] `tasks/`
- [ ] maintenance/backfill utilities
- [ ] legacy enrichment/classification scripts
- [ ] relevant tests and validation scripts

## Current verified discovery notes

Verified from the repository tree and `docs/oireachtas_packet_status.md` on 2026-08-07:

- The unified Oireachtas implementation is registry-driven and exposes `python -m extract.oireachtas.build_table` as a documented CLI entry point.
- The checked-in registry path is `configs/oireachtas/tables.yml`.
- The handoff records `ca-central-1`, S3 bucket `eirepolitic-data`, and unified output prefixes under `processed/oireachtas_unified/` as non-secret implementation facts; these remain subject to confirmation against current configuration/code before being promoted into canonical documentation.
- The repository contains dedicated weekly, monthly, yearly, compatibility, comparison, and refresh-validation orchestration workflows.
- The repository contains current compatibility outputs used by member-profile and Instagram consumers alongside legacy enrichment keys retained for rollback.
- The July 2026 handoff identifies pending scheduled observations; because that note predates this workstream, current workflow-run state must be re-checked before documenting those observations as current runtime facts.

## PR ledger

| Component | Branch / PR | Validation | Pages deployment | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | `docs/ipa-workstream-plan` | pending | pending | in progress |
| P0 umbrella architecture | pending | pending | pending | pending |
| P0 repository page | pending | pending | pending | pending |
| P0 Unified Oireachtas platform | pending | pending | pending | pending |
| P0 data-product catalogue | pending | pending | pending | pending |
| P0 orchestration | pending | pending | pending | pending |
| P0 policies/contracts | pending | pending | pending | pending |

## Unknowns to resolve from implementation or runtime evidence

- Exact current table registry contents, schemas, source endpoints, and layer semantics.
- Exact write-policy rules and the code paths that enforce them.
- Exact downstream contract definitions and contract-check behavior.
- Current schedule/run state after the July 2026 handoff, including the first scheduled orchestrator run and the August monthly run.
- Current consumer cutover state versus compatibility/legacy rollback paths.
- Exact current authentication/environment-variable boundaries required by workflows and scripts.

## Next action

Finish implementation/configuration discovery for P0, then update this page with verified facts and produce the umbrella architecture component first. No architecture, security, cost, access-control, or irreversible implementation change is authorized by this documentation workstream.
