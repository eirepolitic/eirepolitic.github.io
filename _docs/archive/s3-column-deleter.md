---
title: S3 Column Deleter
summary: Historical destructive-utility record for the still-retained manual CSV+Parquet column-deletion workflow; current operating guidance lives in the maintenance/repair/backfill reference.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - Amazon S3
  - Pandas
  - PyArrow
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-07
last_verified: 2026-08-07
archived_date: 2026-08-05
archive_reason: Historical utility record retained for lineage; current implementation still exists, but current risk and operating guidance is maintained in the data maintenance/repair/backfill reference.
permalink: /projects/pipelines/s3_column_deleter/
related:
  - /projects/notes/data-maintenance-repair-backfill-utilities/
  - /projects/repositories/eirepolitic-data-pipeline/
---

# S3 Column Deleter

## Current status

This page is an **archive/lineage record** for a destructive utility whose implementation still exists on current `eirepolitic-data-pipeline/main`:

```text
process/delete_s3_column.py
.github/workflows/column_deleter.yml
```

The current operational source of truth is [Data maintenance, repair, and backfill utilities](/projects/notes/data-maintenance-repair-backfill-utilities/). That page should be used for safety assessment and recovery guidance.

The workflow remains manually dispatchable and directly overwrites caller-selected S3 CSV and Parquet objects. It is not part of the immutable Oireachtas candidate/promotion model.

## Exact current behavior

Required inputs are:

```text
CSV_KEY
PARQUET_KEY
COLUMN
```

Optional/current defaults:

```text
S3_BUCKET=eirepolitic-data
AWS_REGION=ca-central-1
STRICT=0
```

The script:

1. downloads the full CSV object;
2. removes the named column if present;
3. downloads the full Parquet object;
4. removes the named column if present;
5. if `STRICT=1`, fails before either write when the column was absent from either representation;
6. overwrites the CSV object;
7. overwrites the Parquet object.

When `STRICT=0`, an object where the column is absent is still written back using its original bytes.

## `STRICT=1` is not a safety mode

`STRICT=1` provides exactly one guard:

> require the column to exist in both representations before writes begin.

It does **not** provide:

- dry-run behavior;
- a preview of the resulting schemas;
- a backup or version copy;
- a typed confirmation token;
- a rollback step;
- an approved-prefix allow-list;
- candidate-batch isolation;
- validation that the CSV and Parquet are actually the same logical dataset;
- a transaction spanning both writes.

The previous archive text could be read as though `STRICT` meaningfully reduced destructive risk. Current source does not support that interpretation.

## Failure consistency risk

Writes occur sequentially:

```text
CSV overwrite
then
Parquet overwrite
```

If the CSV write succeeds and the Parquet write fails, the two objects can remain inconsistent.

There is no automatic rollback inside the utility.

Before rerunning after a partial failure, operators must inspect both objects independently and determine their current schemas/state.

## Current workflow

Workflow name:

**Delete Column From S3 CSV+Parquet (Manual)**

Current characteristics:

- `workflow_dispatch` only;
- Python 3.11;
- 60-minute timeout;
- concurrency group `delete-s3-column`;
- contents permission read-only;
- AWS credentials supplied from GitHub Actions secrets;
- bucket fixed in workflow YAML to `eirepolitic-data`;
- arbitrary CSV/Parquet keys and column name supplied by the operator.

The implementation itself has no prefix allow-list, so application-level blast radius is primarily constrained by the AWS permissions attached to those workflow credentials plus the operator-supplied object keys.

## Observed runtime evidence

The current workflow registry contains historical successful runs including:

- `21647221436`, 2026-02-03: success;
- `21878566586`, 2026-02-10: success.

Those runs prove the destructive workflow has been used successfully. They do not establish that an arbitrary future invocation is safe or that current S3 recovery/versioning controls are available.

## Current operational guidance

Do not use this utility as routine schema-management tooling.

Before any invocation, independently establish:

1. the exact CSV and Parquet keys;
2. that both objects represent the intended dataset;
3. that the column is no longer needed by downstream consumers;
4. that a recoverable prior object version or backup exists if rollback could be required;
5. that the target is not a canonical Oireachtas product whose schema/write behavior should instead be changed through registry, builder, candidate-validation, and publication controls.

After the run, verify both schemas and relevant row counts before downstream use.

## Relationship to current maintenance documentation

This archive page preserves the historical utility name and implementation lineage.

The current maintenance reference adds the broader context needed to operate it safely, including:

- comparison with read-only audit utilities;
- mutation-risk classification;
- recovery guidance for partial failure;
- distinction from candidate-isolated Oireachtas repair/backfill workflows;
- known absence of dry-run/backup/rollback controls.

Future safety improvements should be documented on that current reference and implemented in current source rather than turning this archive page back into the primary runbook.

## Known limitations

- destructive direct overwrite;
- no dry-run;
- no automatic backup or rollback;
- no confirmation token;
- no S3 prefix allow-list;
- no candidate isolation;
- no atomic CSV+Parquet transaction;
- no post-write schema/row-count verification;
- no proof from repository source that S3 versioning is enabled;
- workflow “active” state does not mean routine use is recommended.

## Verification record

- Last verified: `2026-08-07`
- Current implementation verified against: `process/delete_s3_column.py`, `.github/workflows/column_deleter.yml`.
- Current operational guidance cross-checked against: `/projects/notes/data-maintenance-repair-backfill-utilities/`.
- Observed runtime evidence retained from the P2 audit: successful workflow runs `21647221436` and `21878566586`.
- Current classification: archived historical utility record with retained active implementation; current operational/safety guidance belongs to the maintenance/repair/backfill reference.
