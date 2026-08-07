---
title: Unified Oireachtas Data Platform
summary: Canonical Oireachtas ingestion, normalization, analytical-product, compatibility, validation, immutable-batch publication, and production-promotion system in eirepolitic-data-pipeline.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
system: Unified Oireachtas Data Platform
repository: eirepolitic-data-pipeline
order: 30
permalink: /projects/systems/unified-oireachtas-data-platform/
technologies:
  - Python
  - GitHub Actions
  - AWS S3
  - Oireachtas API
  - pandas
  - PyArrow
  - YAML
related:
  - /projects/systems/irish-politics-analytics/
  - /projects/repositories/eirepolitic-data-pipeline/
  - /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
---

# Unified Oireachtas Data Platform

## Summary

The Unified Oireachtas Data Platform is the canonical Oireachtas data subsystem inside `eirepolitic-data-pipeline`. It replaces a collection of separate extraction/enrichment paths with a registry-driven platform that:

1. reads public Oireachtas API and source-file data;
2. normalizes it into canonical silver tables;
3. builds derived gold products and control products;
4. applies explicit write/merge policies;
5. builds downstream compatibility datasets;
6. validates data quality, contracts and consumer compatibility;
7. writes a complete immutable candidate batch;
8. promotes the validated batch by changing one production pointer;
9. retains the previous production pointer for rollback.

This page documents the platform as a system. Exact per-product schema/cadence details belong in the dedicated canonical data-product catalogue; operator procedures belong in the orchestration runbook; write-policy and compatibility-contract details belong in their dedicated P0 reference.

## Current Implementation State

**Verified implementation:** the canonical registry at `configs/oireachtas/tables.yml` contains 31 products, all currently marked `confirmed`: 23 silver, 5 gold and 3 control.

**Verified implementation:** `python -m extract.oireachtas.build_table` is the table execution entry point. Builders are dispatched to `extract/oireachtas/table_*.py` modules using registry metadata.

**Verified implementation:** production publication is candidate/batch based. Requested writes to logical unified production keys are redirected to `processed/oireachtas_unified/batches/<batch_id>/...`; production reads resolve through `processed/oireachtas_unified/pointers/production.json`.

**Observed runtime evidence:** scheduled orchestrator run `30740881592` on 2026-08-02 completed refresh, downstream validation, final candidate reassembly, promotion and post-promotion production-pointer verification successfully.

## System Boundary

Included:

- `configs/oireachtas/` configuration.
- `extract/oireachtas/` API client, table builders, storage, batching, compatibility and validation logic.
- `process/oireachtas_*.py` operational helpers.
- `.github/workflows/oireachtas_*.yml` current production/test/repair workflows.
- canonical Oireachtas S3 products under `processed/oireachtas_unified/` and raw Oireachtas snapshots under `raw/oireachtas_unified/`.
- downstream compatibility datasets under `processed/oireachtas_unified/compat/`.
- candidate consumer validation for member profile metrics and Instagram HTML rendering where invoked by reusable validation.

Outside this system boundary:

- detailed Instagram publishing/content workflows after the candidate smoke-test boundary;
- generic LLM task execution not used by a specific Oireachtas enrichment path;
- older standalone extraction/enrichment utilities except where they are legacy sources or compatibility inputs;
- account-level AWS/IAM configuration not represented in source.

## Authoritative Sources

| Concern | Current source of truth |
| --- | --- |
| API defaults/endpoints | `configs/oireachtas/api_params.yml` |
| canonical products/schemas/cadences | `configs/oireachtas/tables.yml` |
| write strategies/relationships | `configs/oireachtas/write_policies.yml` |
| downstream compatibility contracts | `configs/oireachtas/downstream_contracts.yml` |
| schema registry loader | `extract/oireachtas/schemas.py` |
| API pagination/retry | `extract/oireachtas/client.py` |
| table dispatch/CLI | `extract/oireachtas/build_table.py` |
| table implementation | `extract/oireachtas/table_*.py` |
| storage and production-key resolution | `extract/oireachtas/io_s3.py` |
| batch assembly/promotion/rollback | `extract/oireachtas/batch.py` |
| compatibility adapters | `extract/oireachtas/downstream_compat.py` |
| contract enforcement | `extract/oireachtas/contracts.py` |
| refresh input/cadence logic | `process/oireachtas_refresh_inputs.py` |
| production orchestration | `.github/workflows/oireachtas_refresh_validation_orchestrator.yml` |
| reusable refresh | `.github/workflows/oireachtas_refresh_reusable.yml` |
| reusable validation | `.github/workflows/oireachtas_validation_reusable.yml` |

Repository handoff/plan documents under `docs/` are supporting or historical evidence only when current source differs.

## Data Flow

```text
Oireachtas API / data.oireachtas.ie
        |
        v
OireachtasClient + table-specific normalization
        |
        +--> raw/oireachtas_unified/...               source snapshots where applicable
        |
        v
canonical silver tables
        |
        +--> gold analytical products
        +--> control products / DQ / manifests
        |
        v
logical latest keys
processed/oireachtas_unified/latest/{csv,parquet}/...
        |
        +--> compatibility adapters / enrichment contracts
        |    processed/oireachtas_unified/compat/...
        |
        v
immutable candidate batch
processed/oireachtas_unified/batches/<batch_id>/...
        |
        v
contract + compatibility + mismatch + consumer validation
        |
        v
validated batch manifest
        |
        v
production pointer promotion
processed/oireachtas_unified/pointers/production.json
```

The logical `latest/` and `compat/` names are API-like logical paths. During candidate publication, `extract/oireachtas/io_s3.py` maps them into immutable batch objects instead of overwriting production objects directly.

## Source Acquisition

### API defaults

Current checked-in defaults are:

- API base: `https://api.oireachtas.ie/v1`
- source-file base: `https://data.oireachtas.ie`
- default chamber: `dail`
- default house: `34`
- maximum configured API page size: `200`
- default request timeout: `30` seconds

Canonical configured API endpoints include `/houses`, `/constituencies`, `/parties`, `/members`, `/debates`, `/divisions`, `/questions` and `/legislation`. `/votes` is retained as a compatibility fallback alias for divisions rather than the canonical endpoint.

### API client behavior

`extract/oireachtas/client.py` provides `OireachtasClient`.

For requests carrying a `limit`, pagination is automatic unless explicitly disabled. Important behavior:

- `limit` is a page size, not a production row cap;
- page size is capped at 200;
- offset pagination uses `skip`;
- reported totals are used when available;
- short/empty pages also terminate complete pagination;
- repeated-page detection fails the request rather than silently looping;
- incomplete pagination due to max-page exhaustion fails unless an explicit test `max_rows` limit caused the stop;
- HTTP 429 and 5xx responses are retried with incremental backoff;
- request/pagination telemetry is returned in `ApiResponseSummary` and can be recorded in manifests.

This behavior is tested by `tests/test_oireachtas_pagination.py` and `tests/test_oireachtas_partitioned_fetch.py` for relevant paths.

## Canonical Product Layers

### Silver layer

The 23 silver products normalize Oireachtas domains and source structures into stable table contracts. The current registry covers:

- houses, constituencies and parties;
- members;
- time-aware memberships, parties, constituencies and offices;
- source files;
- debate records, sections and speeches;
- divisions, tallies and member votes;
- questions;
- bills, versions, stages, related documents, sponsors, debates and events.

Silver builders are responsible for source extraction, normalization, deduplication, schema alignment, DQ and storage.

### Gold layer

Five gold products build reusable analytical marts from canonical silver data:

- current member roster;
- yearly member activity;
- monthly member activity;
- yearly constituency activity;
- deterministic content fact pool.

Gold builders read logical latest silver data through the same S3 read-resolution path. For example, `gold_current_members` combines members, memberships, member parties, member constituencies and offices, selecting current-or-latest relationship records before applying DQ requirements.

### Control layer

Three control products provide platform audit/operational state:

- pipeline runs;
- latest table manifests;
- data-quality results.

Control write policies differ from business data: pipeline runs and DQ results append, while the current manifest table is a snapshot replacement.

## Table Build Contract

`extract/oireachtas/build_table.py` is the shared command surface. Supported execution modes include `test`, `incremental`, `full` and `backfill` as allowed by the selected path/table.

A typical silver builder performs these steps:

1. generate a UTC run ID and snapshot date;
2. call the configured API endpoint through `OireachtasClient`;
3. normalize source structures to registry-defined columns;
4. deduplicate according to table semantics;
5. construct a pandas DataFrame aligned to `TableSchema.columns`;
6. calculate table-specific DQ checks;
7. write immutable run CSV/Parquet/raw/manifests where applicable;
8. request logical `latest` CSV/Parquet writes;
9. write review sample/schema/manifest artifacts;
10. return a `TableBuildResult` with manifest, schema, DQ and S3 keys.

The CLI returns a failure status when DQ fails. In `test` mode, `--publish-latest auto` suppresses candidate publication.

Do not assume every table has identical DQ checks. The common pattern is verified, but required content/population checks vary by builder.

## Storage Model

### Immutable run outputs

Table builders retain run-specific raw/processed/manifests. Representative patterns include:

```text
raw/oireachtas_unified/api/<domain>/snapshot_date=<date>/run_id=<run>/...
processed/oireachtas_unified/silver/<table>/snapshot_date=<date>/run_id=<run>/...
processed/oireachtas_unified/silver_csv/<table>/snapshot_date=<date>/run_id=<run>/...
processed/oireachtas_unified/gold/<table>/snapshot_date=<date>/run_id=<run>/...
processed/oireachtas_unified/gold_csv/<table>/snapshot_date=<date>/run_id=<run>/...
processed/oireachtas_unified/manifests/<table>/run_id=<run>.json
processed/oireachtas_unified/review/<table>/latest/...
```

Exact raw/run paths depend on the builder.

### Logical current products

Canonical logical current products use:

```text
processed/oireachtas_unified/latest/csv/<table>.csv
processed/oireachtas_unified/latest/parquet/<table>.parquet
```

Compatibility products use:

```text
processed/oireachtas_unified/compat/...
```

### Immutable candidate/production batches

Requested unified production writes require a valid `OIREACHTAS_BATCH_ID`. They are redirected under:

```text
processed/oireachtas_unified/batches/<batch_id>/tables/...
processed/oireachtas_unified/batches/<batch_id>/compat/...
processed/oireachtas_unified/batches/<batch_id>/review/...
```

Batch entries and the assembled batch manifest are stored beneath the same batch root.

Production state is represented by:

```text
processed/oireachtas_unified/pointers/production.json
processed/oireachtas_unified/pointers/previous.json
```

The pointer may also express `legacy_direct` mode for rollback/transition compatibility.

## Read and Write Resolution

`extract/oireachtas/io_s3.py` centralizes current unified S3 behavior.

For reads of `latest/` or `compat/` logical keys:

1. if `OIREACHTAS_BATCH_ID` is set, resolve into that candidate batch;
2. otherwise resolve via the production pointer;
3. if pointer resolution fails, fall back to the direct logical key for legacy compatibility.

For writes to `latest/` or `compat/` logical keys:

1. if candidate publication was not requested, the logical production write is skipped;
2. if publication was requested but no valid batch ID exists, raise an error;
3. otherwise map the logical key into the immutable candidate batch.

This means a table builder can keep using stable logical names while candidate validation reads its own isolated batch.

## Write Semantics

`configs/oireachtas/write_policies.yml` declares one strategy per canonical table:

- `snapshot_replace`
- `upsert`
- `append`
- `rebuild`

For candidate writes of logical latest table CSV/Parquet data, `io_s3.py` loads the table policy. Snapshot/rebuild products use incoming data directly; upsert/append products read current production and pass existing/incoming data to policy-aware merge logic.

Selected time-valid business keys and foreign-key declarations are also configuration data. They are documented in full in the dedicated write-policy/contract reference.

## Refresh Cadences

`process/oireachtas_refresh_inputs.py` controls cadence-specific defaults.

### Weekly

- default mode: `incremental`
- default page size: `100`
- default date window: `as_of - 35 days` through `as_of`
- default products: members and member relationships, debates/sections/speeches, divisions/tallies/member votes, questions, all five gold products except no separate omission in current set, and all three control products.

### Monthly

- default mode: `incremental`
- default page size: `200`
- default date window: seven days before the start of the previous month through the previous month end
- default products: constituencies, parties, source files, legislation/bill products, constituency/content gold products, and all three control products.

The seven-day pre-month overlap is implementation behavior intended to catch boundary changes; this page does not infer a business rationale beyond the code.

### Yearly

- default mode: `full`
- default page size: `200`
- default date window: January 1 through December 31 of the previous calendar year
- default products: houses, constituencies, parties, members and their relationships/offices, selected bill products, current-member/member-year/constituency-year/content gold products, and all three control products.

The normalizer rejects unknown/duplicate table names, invalid cadence/mode combinations, invalid house/chamber/date/page-size/sample inputs, and always moves the three control products to the end of the requested table order.

## Compatibility Layer

The platform deliberately preserves stable downstream-shaped datasets while canonical tables evolve.

`extract/oireachtas/downstream_compat.py` currently constructs two core adapters from canonical silver data:

- `members_compat` from `silver_members`;
- `member_votes_compat` from `silver_member_votes`.

The compatibility output identifies `source=oireachtas_unified` and preserves downstream-required legacy-style column names such as `memberCode`, `unique_vote_id` and `date` for votes.

Four additional compatibility contracts are supplied by current enrichment-staging paths:

- member photo URLs;
- member summaries;
- constituency images;
- debate issue labels.

During candidate validation these enrichment datasets are staged into the candidate batch before all six contracts are checked.

## Downstream Contract Validation

`extract/oireachtas/contracts.py` loads `configs/oireachtas/downstream_contracts.yml` and validates each selected logical dataset after resolving it through candidate/production state.

A dataset contract can fail for:

- unreadable/missing object;
- row count below minimum;
- missing required columns;
- missing PK columns;
- duplicate PK rows;
- blank PK rows;
- object age exceeding configured freshness maximum.

Separate comparison thresholds evaluate compatibility versus legacy/reference datasets using:

- maximum legacy-only keys;
- maximum compatibility-only keys;
- maximum row-count delta percentage;
- minimum compatibility join coverage percentage.

Contract failure blocks the reusable validation workflow and therefore scheduled automatic promotion.

## Candidate Construction and Validation

The reusable refresh workflow builds a complete candidate rather than only the changed tables when `seed_from_production=true`:

1. validate/normalize refresh inputs;
2. validate immutable batch ID;
3. seed the candidate from current production;
4. rebuild the cadence-selected products into the candidate;
5. assemble an initial batch manifest for required refreshed products.

The reusable validation workflow then:

1. stages current enrichment contract data into the candidate;
2. builds candidate compatibility adapters;
3. validates all six downstream contracts;
4. runs compatibility comparison and mismatch review;
5. optionally builds year-aware member profile metrics;
6. optionally executes an Instagram candidate-only HTML smoke test;
7. reassembles the final candidate manifest, requiring the compatibility-adapter entry.

The candidate is therefore validated as a complete downstream-consumable state, not only as independent canonical tables.

## Batch Manifest and Promotion

`extract/oireachtas/batch.py` records table entries containing batch ID, table, DQ status, row count, PK/schema, source run ID, GitHub run metadata, object existence/metadata, manifest and DQ payload.

`assemble_batch_manifest()` fails the batch if it detects:

- missing required tables;
- table entries not validated or with failing DQ;
- missing candidate objects;
- duplicate table entries;
- no usable entries.

`promote_batch()` refuses to promote unless the stored batch manifest status is `validated`.

Promotion:

1. captures the current production pointer as `previous.json` (or captures a `legacy_direct` previous state if no pointer exists);
2. writes `production.json` pointing to the validated batch and its manifest;
3. records actor/workflow metadata and prior mode/batch.

No table-by-table production copy is required for promotion; the effective production dataset changes through the pointer.

## Production Orchestration

The high-level controller is `.github/workflows/oireachtas_refresh_validation_orchestrator.yml`.

Triggers:

```text
45 6 * * 0     weekly
15 7 1 * *     monthly
30 7 2 1 *     yearly
```

Scheduled runs force:

- candidate publication enabled;
- downstream consumer validation enabled;
- automatic promotion enabled.

Manual dispatch allows these controls to be changed, with automatic promotion defaulting to false.

The workflow uses a production concurrency group with `cancel-in-progress: false`, creates a batch ID from cadence/run ID/run attempt, calls reusable refresh and validation, then promotes only after both jobs succeed.

After promotion it reads production status and asserts that `production.json` is in batch mode and points at the new batch. If this verification fails after the promotion step succeeded, the workflow invokes `rollback-previous`.

## Observed Runtime Evidence

GitHub Actions shows scheduled production orchestrator activity after the July 2026 handoff.

For run `30740881592`, created 2026-08-02:

- `prepare`: success;
- reusable `refresh`: success, including candidate seeding, table refresh and manifest assembly;
- reusable `validation`: success, including enrichment staging, compatibility adapters, contracts, mismatch/compat checks, member metrics, Instagram smoke and final reassembly;
- `promote`: success;
- production pointer verification: success;
- automatic rollback step: skipped because verification succeeded;
- summary: success.

This is observed runtime evidence for that run, not a guarantee that every future run succeeds.

## Data Quality and Review Evidence

Table builders produce table-specific DQ payloads and review artifacts. Common checks include row-count, required-column and PK requirements, but business-content checks vary by product.

Review paths normally include the latest sample, schema and manifest for a table. GitHub refresh/validation workflows also upload run artifacts containing logs, normalized input records, batch manifests, contract results, comparison/mismatch reports, consumer outputs and promotion evidence with configured retention periods.

## Security and Access Boundaries

The current production workflows consume AWS credential secrets named:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`

They use checked-in non-secret defaults for region `ca-central-1` and bucket `eirepolitic-data`.

The repository proves secret names and code access paths, not the exact live IAM policy. Exact live role/user permissions, bucket policy, versioning, retention, Glue/Athena state or account controls remain unverified unless inspected directly from AWS.

The public Oireachtas API path itself does not use a checked-in API secret.

## Failure Modes and Recovery

Verified failure paths include:

- API non-success after retry, invalid result shape, repeated pagination page or incomplete pagination;
- normalization/table-builder exceptions;
- empty/malformed tables or table-specific DQ failures;
- S3 write failures;
- invalid refresh inputs/table sets/modes;
- requested candidate publication without a valid batch ID;
- incomplete candidate seeding/build entries;
- missing candidate objects;
- downstream contract failures;
- compatibility/mismatch threshold failures;
- member-metric or Instagram smoke-test failure when consumer validation is enabled;
- promotion attempt against a non-validated batch;
- post-promotion pointer verification failure.

Recovery controls include rerunning a corrected immutable candidate, `rollback-previous`, rollback to another validated batch, or explicit `legacy_direct` rollback mode. Operators should use the dedicated orchestration runbook once published rather than editing production pointer objects manually.

## Historical-to-Current Relationship

Older top-level extractors and standalone enrichment scripts remain in the repository, but the Unified Oireachtas Data Platform is the current canonical foundation where equivalent current modules/configuration exist.

In particular:

- canonical Oireachtas tables are defined by `configs/oireachtas/tables.yml` and `extract/oireachtas/table_*.py`, not older monthly extractor scripts;
- compatibility adapters are deliberately produced from unified canonical outputs;
- current Oireachtas enrichment modules coexist with earlier standalone member-photo, member-summary, constituency-image and issue-classification scripts until P3 successor reconciliation is fully documented;
- old documentation plans/handoffs should be treated as historical when current workflow/configuration contradicts them.

## Known Limitations

- Per-table DQ and normalization behavior is not uniform and must be consulted in each builder; the data-product catalogue will record product-level facts.
- The table registry is checked-in configuration, not a database catalogue; schema evolution depends on code/config review.
- Direct-key fallback remains for legacy compatibility when production-pointer resolution fails, so historical direct objects still matter during transition/recovery.
- Shared Python dependencies are not fully pinned.
- Exact live AWS access-control/storage settings are not established from source.
- Several legacy/repair/trial workflows remain enabled and require target-specific status reconciliation; they are not automatically part of this production system.

## Next Safe Development Action

Create the canonical Oireachtas data-product catalogue directly from `configs/oireachtas/tables.yml`, then reconcile each product against its builder for source/lineage, write strategy and table-specific validation facts. Keep the catalogue descriptive; do not change schemas or runtime behavior as part of documentation.

## Related Documents

- [Irish Politics Analytics](/projects/systems/irish-politics-analytics/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [IPA / Oireachtas documentation workstream plan](/projects/high-director/ipa-oireachtas-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified implementation/configuration: current `eirepolitic-data-pipeline` tree; `configs/oireachtas/*.yml`; `extract/oireachtas/schemas.py`; `client.py`; `build_table.py`; `io_s3.py`; `batch.py`; `write_policies.py`; `contracts.py`; `downstream_compat.py`; representative silver builder `table_members.py`; representative gold builder `table_gold_current_members.py`; `process/oireachtas_refresh_inputs.py`; current reusable refresh/validation/orchestrator workflows; Oireachtas tests inventory.
- Observed runtime evidence: orchestrator run `30740881592`, 2026-08-02, including job/step conclusions.
- Historical evidence consulted: `docs/oireachtas_packet_status.md` and repository Oireachtas plan/handoff inventory.
- Verification scope: platform boundary, source acquisition, product layers, storage/read/write resolution, cadences, compatibility/contracts, candidate validation, batch promotion/rollback, security boundary, runtime evidence and failure/recovery model.
