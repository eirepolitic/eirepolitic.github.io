---
title: Irish Politics Analytics
summary: Umbrella architecture for the Eire Politic political-data platform, including the unified Oireachtas data layer, downstream analytics and content systems, orchestration, storage, and historical boundaries.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
system: Irish Politics Analytics
repository: eirepolitic-data-pipeline
order: 20
permalink: /projects/systems/irish-politics-analytics/
technologies:
  - Python
  - GitHub Actions
  - AWS S3
  - Oireachtas API
  - pandas
  - PyArrow
  - OpenAI API
  - Jinja2
  - Playwright
related:
  - /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
  - /projects/high-director/documentation-target-catalogue/
---

# Irish Politics Analytics

## Summary

Irish Politics Analytics is the umbrella political-data and content platform implemented primarily in `eirepolitic-data-pipeline`. Its current centre of gravity is the Unified Oireachtas Data Platform: a registry-driven Python pipeline that ingests official Oireachtas data, normalizes it into canonical silver tables, builds derived gold and control products, stages compatibility datasets for downstream consumers, validates immutable candidate batches, and promotes validated batches through an S3 production pointer.

The same repository also contains downstream member metrics, Instagram/content rendering, reusable LLM tasks, maintenance utilities, enrichment successors, and retained legacy/editorial scripts. Those components are part of the umbrella architecture but are documented separately where they have their own operating model.

`eirepolitic.github.io` is the technical-documentation repository for this platform. It is not part of the production data runtime.

## Current Implementation State

**Verified implementation:** the active repository contains a 31-product canonical Oireachtas registry in `configs/oireachtas/tables.yml`: 23 silver tables, 3 control tables, and 5 gold tables. All 31 registry entries are currently marked `confirmed` in checked-in configuration.

**Verified implementation:** current Oireachtas production writes use immutable batch locations and a production-pointer model. Unified logical production keys are resolved through `processed/oireachtas_unified/pointers/production.json`; candidate data is written under `processed/oireachtas_unified/batches/<batch_id>/...` before promotion.

**Verified implementation:** `.github/workflows/oireachtas_refresh_validation_orchestrator.yml` defines scheduled weekly, monthly, and yearly refreshes. Scheduled runs create candidate batches, seed unchanged products from current production, refresh the cadence-specific table set, run downstream validation, and automatically promote only after refresh and validation succeed.

**Observed runtime evidence:** scheduled orchestrator run `30740881592` on 2026-08-02 completed prepare, refresh, validation, promotion, production-pointer verification, and summary successfully. This supersedes the July 2026 handoff note that still described scheduled observation as pending.

## System Boundary

Included in the Irish Politics Analytics umbrella:

- Official Oireachtas ingestion and normalization in `extract/oireachtas/`.
- Canonical silver, gold, and control data products registered in `configs/oireachtas/tables.yml`.
- Write-policy, relationship, compatibility-contract, batch-publication, validation, and promotion controls.
- Oireachtas GitHub Actions refresh and validation workflows.
- Downstream compatibility/enrichment datasets used by current member-profile and Instagram consumers.
- Member-profile metrics in `process/build_member_profile_metrics.py`.
- Instagram campaign, constituency, member-profile, template, media-generation, and local deterministic rendering code under `instagram/` and `process/instagram_*`.
- Reusable OpenAI/YAML/S3 task execution in `process/llm_table_runner.py` and `tasks/`.
- Maintenance, repair, backfill, legacy enrichment/classification, and editorial/experimental scripts retained in the repository.

Outside this system boundary:

- `eirepolitic.github.io` runtime; it documents the system but does not process political data.
- AutoDoc, `bb-comp-prices`, `degenerate_investigator`, and Overlord, except where a technical cross-reference is required.
- Exact live IAM policies or account-level AWS configuration that cannot be proven from source.
- Secret values, credentials, API keys, personal identifiers, and private account configuration.

## Source of Truth

| Concern | Evidence class | Authoritative source |
| --- | --- | --- |
| Current repository implementation | verified implementation | `eirepolitic-data-pipeline` `main` |
| Oireachtas API and S3 defaults | verified configuration | `configs/oireachtas/api_params.yml` |
| Canonical data-product names, layers, cadences, schemas and keys | verified configuration | `configs/oireachtas/tables.yml` |
| Write strategies and declared relationships | verified configuration | `configs/oireachtas/write_policies.yml` |
| Compatibility datasets and acceptance thresholds | verified configuration | `configs/oireachtas/downstream_contracts.yml` |
| Table CLI and dispatch | verified implementation | `extract/oireachtas/build_table.py` |
| Immutable batch, promotion and rollback model | verified implementation | `extract/oireachtas/batch.py`, `extract/oireachtas/io_s3.py` |
| Scheduled orchestration | verified implementation | `.github/workflows/oireachtas_refresh_validation_orchestrator.yml` |
| Refresh implementation | verified implementation | `.github/workflows/oireachtas_refresh_reusable.yml` |
| Candidate validation | verified implementation | `.github/workflows/oireachtas_validation_reusable.yml` |
| Latest observed production execution | observed runtime evidence | GitHub Actions orchestrator run `30740881592`, 2026-08-02 |
| July unified-platform handoff | historical/current-at-write-time documentation | `docs/oireachtas_packet_status.md` |
| Legacy pipeline descriptions | historical behavior | `_docs/archive/` pages in `eirepolitic.github.io` |

Old README text, historical AutoDoc output, archive pages, and build plans do not override current implementation/configuration.

## Architecture

### 1. Official source acquisition

The default API configuration in `configs/oireachtas/api_params.yml` points to:

- API base: `https://api.oireachtas.ie/v1`
- source-data base: `https://data.oireachtas.ie`

Current configured canonical API endpoints include `/houses`, `/constituencies`, `/parties`, `/members`, `/debates`, `/divisions`, `/questions`, and `/legislation`. `/divisions` is the configured canonical division endpoint with `/votes` retained as a compatibility fallback in `endpoint_aliases`.

`extract/oireachtas/client.py` provides API access; table-specific modules under `extract/oireachtas/table_*.py` transform source payloads into canonical rows. Debate source files and parsed XML content are represented explicitly through `silver_source_files`, `silver_debate_records`, `silver_debate_sections`, and `silver_speeches`.

### 2. Canonical data layer

`configs/oireachtas/tables.yml` is the canonical registry. The current product layers are:

- **Silver:** 23 normalized source/domain tables covering houses, constituencies, parties, members and time-aware member relationships, source files, debates, speeches, divisions/votes, questions, and legislation.
- **Gold:** 5 derived marts for current members, yearly/monthly member activity, yearly constituency activity, and deterministic content facts.
- **Control:** 3 operational products for pipeline runs, latest table manifests, and data-quality results.

`python -m extract.oireachtas.build_table` is the central table CLI. It supports `test`, `full`, `incremental`, and `backfill` execution for real tables plus discovery/smoke modes. In `test` mode, candidate publication is suppressed by the default `--publish-latest auto` behavior.

### 3. Storage and publication control

Checked-in defaults use AWS region `ca-central-1` and S3 bucket `eirepolitic-data`.

The current Oireachtas publication model separates logical production names from immutable batch objects:

```text
processed/oireachtas_unified/latest/...       logical canonical products
processed/oireachtas_unified/compat/...       logical downstream compatibility products
processed/oireachtas_unified/batches/<id>/... immutable candidate/production batch objects
processed/oireachtas_unified/pointers/production.json
processed/oireachtas_unified/pointers/previous.json
```

`extract/oireachtas/io_s3.py` redirects requested unified production writes into the current `OIREACHTAS_BATCH_ID`. A candidate write requires both a publication request and a valid batch ID. Reads resolve through the current batch when one is being validated, then through the production pointer, with direct logical-key fallback for legacy compatibility.

`extract/oireachtas/batch.py` assembles a batch manifest from validated table entries. Promotion updates a single production pointer only after the batch manifest has status `validated`; the previous pointer is retained to support rollback. Rollback can target an earlier validated batch or the legacy-direct mode.

### 4. Write and relationship policy

`configs/oireachtas/write_policies.yml` declares one of four strategies per canonical table:

- `snapshot_replace` for complete authoritative snapshots;
- `upsert` for retained-history/key merges;
- `append` for audit records;
- `rebuild` for derived products.

The configuration also declares selected foreign-key relationships and time-validity/business-key metadata. `extract/oireachtas/write_policies.py` validates the registry values, while `extract/oireachtas/io_s3.py` loads the table policy before merging non-replacement candidate writes with current production data.

Detailed policy behavior belongs in the dedicated P0 write-policy/downstream-contract documentation.

### 5. Compatibility and downstream validation

`configs/oireachtas/downstream_contracts.yml` currently defines six compatibility datasets:

- `members_compat`
- `member_votes_compat`
- `member_photo_urls`
- `member_summaries`
- `constituency_images`
- `debate_issue_labels`

Each contract defines a logical S3 key, required columns, primary key, minimum row threshold, and maximum age. Comparison thresholds are also configured for roster and member-vote compatibility.

The reusable validation workflow stages enrichment contract inputs into the candidate batch, rebuilds compatibility adapters, validates contracts, runs strict compatibility/mismatch checks, optionally builds member metrics and an Instagram HTML smoke test, then reassembles the final candidate manifest.

### 6. Scheduled orchestration

`.github/workflows/oireachtas_refresh_validation_orchestrator.yml` is the current high-level production controller. Its checked-in scheduled triggers are:

```text
45 6 * * 0     weekly
15 7 1 * *     monthly
30 7 2 1 *     yearly
```

For scheduled events the workflow sets `publish_candidate=true`, `run_consumers=true`, and `auto_promote=true`. Manual runs expose those controls explicitly and default `auto_promote` to false.

The orchestration sequence is:

1. resolve refresh cadence and immutable `batch_id`;
2. invoke the reusable refresh workflow;
3. seed the candidate from current production when building a complete candidate;
4. refresh the cadence-specific table set;
5. assemble a candidate manifest;
6. invoke reusable validation;
7. validate compatibility contracts and consumers;
8. reassemble the final candidate manifest;
9. when auto-promotion is enabled, capture current pointers;
10. promote the validated batch;
11. verify the production pointer points to that batch;
12. automatically roll back to the previous pointer if post-promotion pointer verification fails.

Concurrency groups prevent overlapping production orchestrators/refreshes from cancelling each other (`cancel-in-progress: false`).

### 7. Downstream analytics and content systems

The unified Oireachtas platform supplies compatibility and canonical data to several downstream areas in the same repository:

- `process/build_member_profile_metrics.py` builds year-aware member metrics.
- `instagram/renderer/`, `instagram/templates/`, campaign specs, and `process/instagram_*` implement deterministic and template-based content rendering.
- `process/llm_table_runner.py` and `tasks/*.yml` provide a reusable LLM table-processing framework.
- Dedicated enrichment modules under `extract/oireachtas/enrichment_*` support current compatibility products for photos, summaries, constituency images, and speech issue labels.

These are architecture-level relationships only. Their detailed inputs, prompts, rendering specifications, retry rules, and operating procedures are P1/P3 documentation targets.

## Inputs and Outputs

### Primary inputs

- Public Oireachtas API responses.
- Oireachtas-hosted XML/PDF/source-file URLs exposed through API format fields.
- Existing production Oireachtas batch objects when a candidate is seeded or an upsert/append policy retains current data.
- Checked-in YAML configuration and workflow inputs.
- Legacy/current enrichment datasets where explicitly staged into downstream compatibility contracts.

### Primary outputs

- Canonical silver CSV/Parquet data products.
- Gold analytical products.
- Control/audit products and data-quality results.
- Immutable batch manifests and entries.
- Compatibility CSV datasets for downstream consumers.
- Review bundles and GitHub Actions evidence artifacts.
- Derived member metrics and Instagram validation/rendering artifacts in downstream workflows.

## Dependencies

Core repository dependencies are listed in `requirements.txt` and include `requests`, `boto3`, `pandas`, `pyarrow`, `pyyaml`, `openai`, `beautifulsoup4`, `jinja2`, `playwright`, `pillow`, `matplotlib`, and `cairosvg`.

For the Oireachtas foundation, the critical runtime dependencies are Python 3.12 in GitHub Actions, the public Oireachtas API/data host, AWS S3, `boto3`, `pandas`, `PyArrow`, YAML configuration, and GitHub Actions.

OpenAI and rendering/browser libraries are downstream dependencies rather than requirements for every canonical Oireachtas table build.

## Configuration and Security Boundaries

Non-secret checked-in configuration includes table names, schemas, cadences, Oireachtas endpoints, S3 bucket/region defaults, logical object keys, write strategies, validation thresholds, and workflow schedules.

GitHub Actions Oireachtas workflows read AWS credentials from repository secrets named `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. The environment also uses non-secret names such as `AWS_REGION`, `S3_BUCKET`, `OIREACHTAS_BATCH_ID`, `OIREACHTAS_PUBLISH_LATEST`, and `OIREACHTAS_PUBLISH_ENABLED`.

The source repository proves the credential names and where they are consumed; it does not prove the exact live IAM permissions attached to those credentials. Exact account-level IAM/S3 policy state remains unverified until inspected directly from AWS.

No secret values are documented here.

## Operation and Monitoring

Primary operational evidence is produced by GitHub Actions and S3 batch/control objects:

- refresh review output and logs;
- candidate batch manifest;
- downstream-contract validation results;
- compatibility and mismatch reports;
- consumer smoke output;
- promotion evidence and pre/post-promotion pointer status;
- control tables and table-level DQ results.

Observed runtime evidence on 2026-08-02 confirms the current scheduled orchestrator reached successful promotion and pointer verification. Historical handoff notes should not be used to claim a scheduled observation is still pending.

## Failure Modes and Recovery

Major verified failure controls include:

- API/request or table-builder failure causes the refresh job to fail before validation/promotion.
- A table with failing DQ returns a non-zero CLI result.
- Missing/failed candidate entries or objects cause batch-manifest validation to fail.
- Downstream contract, compatibility, mismatch, member-metric, or consumer-smoke failures block automatic promotion.
- `auto_promote=true` is rejected unless candidate publication is enabled.
- A requested candidate write without `OIREACHTAS_BATCH_ID` raises an error.
- A batch whose manifest is not `validated` cannot be promoted.
- Post-promotion pointer verification failure triggers `rollback-previous` when the promotion step itself succeeded.

Detailed diagnosis and rerun procedures belong in the dedicated orchestration runbook.

## Historical and Successor Boundaries

The documentation repository contains historical archive pages for the Constituency Images Indexer, Debate Issue Classifier, LLM Column Creator, Member Images Pipeline, Member Summaries Table, and S3 Column Deleter. Those pages remain historical records.

The current implementation repository contains both newer Oireachtas enrichment/compatibility modules and legacy scripts/workflows. Therefore archive descriptions must not be promoted into current-system documentation without source reconciliation. P3 work will record exact predecessor/successor relationships and whether retained legacy workflows remain active, rollback-only, experimental, or obsolete.

## Known Limitations and Unknowns

- Exact live IAM policies, S3 bucket policy/versioning/retention settings, Glue/Athena state, and account-level controls have not been verified from AWS in this workstream.
- A workflow file being present and active does not by itself prove every legacy or experimental workflow is intentionally part of current production operations.
- The July `docs/oireachtas_packet_status.md` handoff contains states that are now stale relative to current workflow YAML and August runtime evidence.
- Detailed table lineage, per-table source-field normalization, cadence table sets, and every maintenance/legacy script are intentionally deferred to their dedicated documentation components rather than duplicated here.

## Next Safe Development Action

Document the `eirepolitic-data-pipeline` repository as the implementation map for this umbrella architecture. That page should inventory the repository layout, dependency/runtime model, workflow families, test/validation structure, active-vs-legacy boundaries, and safe update procedure without changing production architecture or access control.

## Related Documents

- [IPA / Oireachtas documentation workstream plan](/projects/high-director/ipa-oireachtas-documentation-workstream-plan/)
- [Owner-Wide Documentation Target Catalogue](/projects/high-director/documentation-target-catalogue/)

## Verification Record

- Last verified: `2026-08-07`
- Verified implementation/configuration: `eirepolitic-data-pipeline` `main`; `configs/oireachtas/api_params.yml`; `configs/oireachtas/tables.yml`; `configs/oireachtas/write_policies.yml`; `configs/oireachtas/downstream_contracts.yml`; `extract/oireachtas/build_table.py`; `extract/oireachtas/batch.py`; `extract/oireachtas/io_s3.py`; `extract/oireachtas/write_policies.py`; Oireachtas workflow tree; reusable refresh/validation workflows; full repository tree; `process/` tree; `instagram/` tree; `tasks/` tree; `requirements.txt`.
- Observed runtime evidence: Oireachtas Refresh Validation Orchestrator run `30740881592` and its job/step results, 2026-08-02.
- Historical evidence consulted: `docs/oireachtas_packet_status.md` and assigned archive pages.
- Verification scope: umbrella boundary, canonical product/layer counts, source endpoints, storage/publication architecture, orchestration/promotion controls, subsystem map, security boundary, and current-vs-historical evidence classification.
