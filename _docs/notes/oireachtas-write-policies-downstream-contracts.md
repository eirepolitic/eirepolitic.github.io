---
title: Oireachtas write policies and downstream contracts
summary: Reference for canonical table write semantics, relationship metadata, compatibility dataset contracts, comparison thresholds, and their enforcing implementation in the Unified Oireachtas Data Platform.
section: notes
doc_type: reference
status: active
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - YAML
  - AWS S3
  - pandas
tags:
  - oireachtas
  - write-policy
  - downstream-contracts
  - compatibility
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
order: 30
permalink: /projects/notes/oireachtas-write-policies-downstream-contracts/
related:
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/data/oireachtas-canonical-data-product-catalogue/
  - /projects/runbooks/oireachtas-refresh-validation-orchestration/
---

# Oireachtas write policies and downstream contracts

## Overview

This reference documents two control layers in the Unified Oireachtas Data Platform:

1. **canonical write policies** that define how each registered Oireachtas product is merged or replaced when a candidate is built; and
2. **downstream contracts** that define the minimum shape, key integrity, row-count, freshness, and legacy-compatibility conditions required before a candidate can pass downstream validation.

These controls are executable configuration backed by Python implementation and tests. They are not descriptive-only documentation.

## Current state

**Verified implementation/configuration:** every one of the 31 canonical products in `configs/oireachtas/tables.yml` has a corresponding entry in `configs/oireachtas/write_policies.yml`. `tests/test_oireachtas_write_semantics.py` asserts complete policy coverage.

**Verified implementation:** policy-aware merging is performed by `extract/oireachtas/merge.py` and invoked by current S3 candidate-write handling in `extract/oireachtas/io_s3.py` for logical latest-table writes.

**Verified implementation/configuration:** `configs/oireachtas/downstream_contracts.yml` currently defines six dataset contracts and two comparison-threshold sets. Contract validation is implemented by `extract/oireachtas/contracts.py` and invoked by `process/oireachtas_validate_downstream_contracts.py` in the reusable candidate-validation workflow.

**Verified implementation:** candidate reads do not fall back to production when `OIREACHTAS_BATCH_ID` is set. Tests explicitly verify that missing candidate objects fail rather than silently reading the production logical object.

## Source of truth

| Concern | Authoritative source |
| --- | --- |
| Product write strategy and selected relationships | `configs/oireachtas/write_policies.yml` |
| Write-policy parsing/coverage validation | `extract/oireachtas/write_policies.py` |
| Merge, temporal, overlap and FK helpers | `extract/oireachtas/merge.py` |
| Candidate-aware read/write behavior | `extract/oireachtas/io_s3.py` |
| Dataset contracts and comparison thresholds | `configs/oireachtas/downstream_contracts.yml` |
| Contract loading/evaluation | `extract/oireachtas/contracts.py` |
| Core compatibility adapters | `extract/oireachtas/downstream_compat.py` |
| Legacy-vs-compat comparison | `extract/oireachtas/compat_comparison.py` |
| Member-code mismatch review | `extract/oireachtas/mismatch_review.py` |
| Auxiliary contract staging | `process/oireachtas_stage_downstream_contracts.py` |
| Contract CLI | `process/oireachtas_validate_downstream_contracts.py` |
| Write-policy regression tests | `tests/test_oireachtas_write_semantics.py` |
| Candidate/contract regression tests | `tests/test_oireachtas_downstream_contracts.py` |

Current code/configuration overrides older handoff or archive descriptions.

## Write policy model

`extract/oireachtas/write_policies.py` loads `configs/oireachtas/write_policies.yml` into `WritePolicy` objects. Supported strategies are:

- `snapshot_replace`
- `upsert`
- `append`
- `rebuild`

Unknown strategies are rejected. `validate_policy_coverage()` reports missing or extra policy entries relative to the canonical table registry.

### `snapshot_replace`

The incoming candidate replaces the current table contents rather than retaining rows absent from the new snapshot.

Current products:

- `silver_houses`
- `silver_constituencies`
- `silver_parties`
- `silver_members`
- `control_table_manifests`

Regression evidence: `test_snapshot_replace_does_not_retain_missing_rows` proves that an existing row omitted from the incoming snapshot is not retained.

### `upsert`

Existing and incoming rows are concatenated, then deterministically deduplicated so the latest incoming record wins for a duplicate primary key. If a configured business key exists, a second deterministic dedupe is applied on that business key.

Current `upsert` products are the member history/relationship products, source/debate/speech/division/vote/question products, and all legislation silver products.

This strategy is intended to preserve history across overlapping incremental windows. Regression evidence verifies that an incoming duplicate PK replaces the older version while unrelated historical rows remain, and that preserved history remains available for annual aggregation.

### `append`

Current products:

- `control_pipeline_runs`
- `control_data_quality_results`

At implementation level, `merge_for_policy()` currently uses the same current+incoming deterministic PK-dedupe path for both `append` and `upsert`. Therefore `append` means retain the audit stream while protecting against duplicate PK records; it does **not** mean blindly allow duplicate primary keys.

### `rebuild`

All five gold products use `rebuild`:

- `gold_current_members`
- `gold_member_activity_yearly`
- `gold_member_activity_monthly`
- `gold_constituency_activity_yearly`
- `gold_content_fact_pool`

`merge_for_policy()` returns incoming data directly for `rebuild`, like `snapshot_replace`, because gold products are regenerated from canonical upstream state rather than merged incrementally at the product level.

## Relationship and temporal metadata

Selected write-policy entries declare additional metadata:

- `valid_from_column`
- `valid_to_column`
- `current_column`
- `business_key`
- `foreign_keys`

The current relationship configuration includes member history tables, debate/section/speech relationships, division/tally/vote relationships, member/question relationships, and bill child tables.

These declarations are configuration contracts. Because storage is CSV/Parquet on S3, they are not database-enforced foreign keys by themselves.

### Temporal integrity

`temporal_integrity()` detects:

- rows where `valid_from > valid_to`;
- rows marked current whose start date is in the future relative to the supplied `as_of` date.

The helper returns pass/fail plus counts for invalid ranges and future-current rows.

`tests/test_oireachtas_write_semantics.py` verifies both cases fail temporal integrity.

### Foreign-key integrity

`foreign_key_integrity()` checks configured child key tuples against parent key tuples. By default, completely blank child FK values are ignored unless `allow_blank=false`.

The helper returns pass/fail, orphan count, and a sample of orphan keys. A regression test verifies a missing member reference is reported as an orphan.

### Overlap detection

`overlap_count()` counts overlapping validity ranges for a specified business entity grouping and start/end columns. A test verifies an overlapping member range is counted.

This helper existing in code does not prove every configured time-aware table invokes overlap validation on every build. Runtime invocation must be verified in the relevant builder before treating overlap checks as universal per-table DQ.

## Stable history identity

Member relationship builders deliberately use stable identifiers that do not change when an open-ended historical record later receives an end date.

Regression tests verify this for:

- `membership_id`
- `member_party_id`
- `member_constituency_id`
- `member_office_id`

This allows a later update to close a previously open relationship while still matching the same canonical history row during upsert.

## Candidate write isolation

Current candidate behavior is safety-critical:

- setting `OIREACHTAS_PUBLISH_LATEST=true` with a valid `OIREACHTAS_BATCH_ID` writes logical production-shaped keys into that immutable candidate batch;
- candidate writes do not require the repository-level production-promotion switch `OIREACHTAS_PUBLISH_ENABLED=true`;
- when a candidate batch ID is active, a read of a logical `latest/` or `compat/` key resolves to the candidate physical key;
- if that candidate object is missing, the read fails rather than falling back to the production logical object.

`tests/test_oireachtas_downstream_contracts.py` explicitly covers these behaviors.

This prevents a candidate validation run from accidentally passing because it read a healthy production object that is absent from the candidate.

## Downstream dataset contracts

The six current contracts are exact checked-in configuration from `configs/oireachtas/downstream_contracts.yml`.

| Contract | Logical key | Primary key | Min rows | Max age |
| --- | --- | --- | ---: | ---: |
| `members_compat` | `processed/oireachtas_unified/compat/members/oireachtas_members_34th_dail_compat.csv` | `member_code` | 150 | 14 days |
| `member_votes_compat` | `processed/oireachtas_unified/compat/votes/dail_vote_member_records_compat.csv` | `memberCode`, `unique_vote_id` | 1 | 45 days |
| `member_photo_urls` | `processed/oireachtas_unified/compat/media/members_photo_urls_compat.csv` | `member_code` | 150 | 45 days |
| `member_summaries` | `processed/oireachtas_unified/compat/text/members_summaries_compat.csv` | `member_code` | 150 | 45 days |
| `constituency_images` | `processed/oireachtas_unified/compat/media/constituency_images_compat.csv` | `filename` | 1 | 45 days |
| `debate_issue_labels` | `processed/oireachtas_unified/compat/debates/debate_speeches_classified_compat.csv` | `speech_id` | 1 | 45 days |

### Required columns

`members_compat`:

`member_code`, `full_name`, `constituency`, `party`, `house_no`, `source`, `snapshot_date`.

`member_votes_compat`:

`memberCode`, `member_name`, `unique_vote_id`, `date`, `vote`, `party`, `constituency`, `source`, `snapshot_date`.

`member_photo_urls`:

`member_code`, `full_name`, `photo_url`.

`member_summaries`:

`member_code`, `full_name`, `background`.

`constituency_images`:

`filename`, `s3_key`, `url`.

`debate_issue_labels`:

`speech_id`, `Speaker Name`, `PoliticalIssues`.

## Contract enforcement

`validate_dataset_contract()` resolves the logical dataset through candidate/production S3 state, reads the CSV, and evaluates:

- object readability/existence;
- minimum row count;
- required-column presence;
- primary-key column presence;
- duplicate primary-key rows;
- blank primary-key rows;
- object age relative to `maximum_age_days`.

A complete fresh unique dataset passes. Tests verify that missing required columns, duplicate PK rows, and stale object age produce contract failure.

The CLI wrapper returns a non-zero exit status when selected contract validation fails, so the reusable validation workflow treats a contract failure as a hard stop.

## Auxiliary enrichment staging

The core compatibility adapters for members and member votes are built from unified canonical data. Four additional contracts are supplied from enrichment datasets:

- member photos;
- member summaries;
- constituency images;
- debate issue labels.

`process/oireachtas_stage_downstream_contracts.py` stages these into the active candidate. Before copying, it checks the source object's age against the target contract's configured `maximum_age_days`. A stale source is rejected rather than silently copied into a fresh candidate path.

The staging output records provenance, including the source key and candidate destination. Staging a file does not erase its actual source freshness constraint.

## Compatibility adapters

`extract/oireachtas/downstream_compat.py` builds the current core adapters from canonical data:

- `members_compat` from `silver_members`;
- `member_votes_compat` from `silver_member_votes`.

These adapters intentionally preserve downstream-required legacy-shaped field names while identifying the source as `oireachtas_unified`.

They are compatibility products, not alternative canonical source tables.

## Legacy/reference comparison thresholds

`configs/oireachtas/downstream_contracts.yml` currently declares:

### `members_roster_compat`

- maximum legacy-only keys: `0`
- maximum compatibility-only keys: `0`
- maximum row-count delta: `2.0%`
- minimum compatibility join coverage: `100.0%`

### `member_votes_compat`

- maximum legacy-only keys: `2`
- maximum compatibility-only keys: `2`
- maximum row-count delta: `100.0%`
- minimum compatibility join coverage: `99.0%`

These numbers are current checked-in acceptance thresholds, not inferred service-level objectives.

## Compatibility comparison implementation

`extract/oireachtas/compat_comparison.py` compares:

- legacy member roster `raw/members/oireachtas_members_34th_dail.csv` against unified `members_compat`;
- legacy member votes `processed/votes/dail_vote_member_records.csv` against unified `member_votes_compat`.

For each comparison it calculates:

- legacy and compatibility row/column counts;
- join-key population coverage;
- matched key count;
- legacy-only key count;
- compatibility-only key count;
- row-count delta percentage.

`comparison_status()` applies the configured thresholds. Missing threshold configuration is itself a failure. The comparison DQ fails if any configured comparison fails.

## Member-code mismatch review

`extract/oireachtas/mismatch_review.py` creates a detailed roster mismatch review showing legacy-only and compatibility-only member codes plus available name, party, constituency and source hints.

This report is diagnostic. Its own DQ checks successful review generation and unique review IDs; it does not independently replace the stricter configured compatibility thresholds. The strict roster acceptance decision is made by the compatibility comparison/contract path.

## Promotion relationship

Downstream contract and compatibility checks are executed inside `.github/workflows/oireachtas_validation_reusable.yml` before scheduled automatic promotion.

The high-level sequence is:

1. stage auxiliary enrichment contracts into the candidate;
2. build core compatibility adapters;
3. validate the six dataset contracts;
4. run legacy/reference compatibility comparison;
5. generate mismatch review;
6. run enabled downstream consumers, including member metrics and Instagram smoke validation;
7. reassemble the final candidate manifest;
8. permit the high-level orchestrator to call promotion only if refresh and validation succeed.

A failed downstream contract or compatibility check therefore blocks scheduled promotion.

## Operator interpretation

When a policy or contract check fails:

- **Do not change the threshold simply to make an incident pass.** Treat threshold changes as intentional contract changes requiring review.
- If a PK duplicate appears, determine whether the builder's identity/dedupe logic or the source data changed.
- If a candidate object is missing, fix/rerun the candidate rather than allowing production fallback.
- If an auxiliary enrichment is stale, refresh or reconcile that enrichment before candidate validation.
- If a roster/vote comparison exceeds tolerance, inspect the generated compatibility and mismatch review evidence before promotion.
- If a write-policy change is proposed, assess overlapping-window behavior, history retention, gold rebuild semantics, candidate seeding, and downstream compatibility together.

Use the Oireachtas refresh/validation runbook for GitHub Actions procedures and promotion/rollback steps.

## Change procedure

For a write-policy or contract change:

1. Identify the exact product/consumer whose semantics require a change.
2. Update checked-in YAML and the enforcing Python code only when necessary; do not update documentation as a substitute for implementation.
3. Add or update focused regression tests.
4. Run write-semantics/contract tests and relevant Oireachtas CI.
5. Build an immutable candidate using the normal refresh/validation path.
6. Confirm table DQ, all downstream contracts, compatibility comparison, mismatch review and required consumer smoke checks pass.
7. Review the candidate evidence before any production promotion.
8. Update this reference and the canonical catalogue/runbook if the operational contract changed.

Changes to thresholds, schemas, identity semantics, publication behavior or access controls can affect downstream consumers and should not be treated as documentation-only maintenance.

## Known limitations

- Write-policy relationship declarations are not relational-database constraints; enforcement depends on the code paths that invoke the relevant helpers.
- The presence of temporal/FK/overlap helpers does not prove every table executes every helper on every run.
- Contract freshness is based on S3 object modification age, not domain-event age inside every row.
- Current comparison thresholds encode migration/compatibility acceptance rules; they do not establish long-term analytical accuracy guarantees.
- The four auxiliary enrichment contracts still depend on retained enrichment sources during candidate staging; exact predecessor/successor status is a P3 documentation concern.
- Exact live AWS IAM/bucket policies remain unverified from source.

## How to continue development

P0 is complete once this reference passes documentation validation, merges, and its exact merge SHA completes Pages deployment successfully.

The next workstream should begin P1 with the Instagram/constituency campaign rendering system, followed by the AI member-profile/Instagram workflow, Member Profile Metrics Builder, and Reusable LLM Task Runner Framework. Before detailed P1 documentation, re-read current `main` to avoid stale assumptions from this P0 audit.

## Related documentation

- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)
- [Oireachtas Canonical Data-Product Catalogue](/projects/data/oireachtas-canonical-data-product-catalogue/)
- [Operate Oireachtas refresh, validation, promotion, and rollback](/projects/runbooks/oireachtas-refresh-validation-orchestration/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)

## Verification record

- Last verified: `2026-08-07`
- Verified against: `configs/oireachtas/write_policies.yml`; `configs/oireachtas/downstream_contracts.yml`; `extract/oireachtas/write_policies.py`; `extract/oireachtas/merge.py`; `extract/oireachtas/io_s3.py`; `extract/oireachtas/contracts.py`; `extract/oireachtas/downstream_compat.py`; `extract/oireachtas/compat_comparison.py`; `extract/oireachtas/mismatch_review.py`; `process/oireachtas_stage_downstream_contracts.py`; `process/oireachtas_validate_downstream_contracts.py`; `tests/test_oireachtas_write_semantics.py`; `tests/test_oireachtas_downstream_contracts.py`; current reusable validation/orchestrator workflow behavior already verified in the P0 runbook audit.
- Verified by: High Director
- Verification scope: write strategy semantics, policy coverage, history identity, candidate read/write isolation, relationship/temporal helpers, all six downstream dataset contracts, exact comparison thresholds, compatibility comparison, mismatch diagnostics, candidate staging, promotion gating, operator interpretation and safe change procedure.
