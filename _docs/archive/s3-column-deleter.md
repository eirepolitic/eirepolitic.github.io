---
title: S3 Column Deleter
summary: Removes a named column from paired CSV and Parquet files stored in S3.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic
technologies:
  - Python
  - Amazon S3
  - Pandas
  - PyArrow
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-05
last_verified: 2026-02-27
archived_date: 2026-08-05
archive_reason: Historical pipeline documentation migrated into the knowledge-base archive.
permalink: /projects/pipelines/s3_column_deleter/
---

# S3 Column Deleter

## Overview

This utility removes a specified column from both a CSV and Parquet table in S3, then overwrites the original objects.

## Source of truth

- Script: `process/delete_s3_column.py`
- Workflow: `.github/workflows/column_deleter.yml`
- Default bucket: `eirepolitic-data`
- Default region: `ca-central-1`

## Configuration

Required:

- `CSV_KEY`
- `PARQUET_KEY`
- `COLUMN`

Optional:

- `AWS_REGION`
- `S3_BUCKET`
- `STRICT`

When `STRICT=1`, the process fails if the column is missing from either file. When `STRICT=0`, missing columns are ignored.

## Operation

The workflow is manually triggered and runs:

```bash
python process/delete_s3_column.py
```

## Validation

Inspect the resulting CSV and Parquet schemas before downstream use. Confirm that only the intended column was removed.

## Security and risk

This process overwrites source objects. Verify bucket, keys, and column name before running. S3 versioning or backups should be used where rollback is required.
