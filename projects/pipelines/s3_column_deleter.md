---
title: "S3 Column Deleter"
layout: default
---

# S3 Column Deleter

**Project:** eirepolitic  
**Type:** pipeline  
**Last generated:** 2026-02-27T01:44:32.326575Z

---

## Overview

### Purpose
The "S3 Column Deleter" pipeline deletes a specified column from both CSV and Parquet tables in the main S3 bucket, mainly for cleanup and testing.

### Scope
The pipeline processes paired CSV and Parquet files in S3, removes a specified column if present, and writes the updated files back. It requires environment variables `CSV_KEY`, `PARQUET_KEY`, and `COLUMN`. Optional variables are `AWS_REGION`, `S3_BUCKET`, and `STRICT`. The implementation is in `process/delete_s3_column.py`, manually triggered via the "Delete Column From S3 CSV+Parquet (Manual)" GitHub Actions workflow.

## Assets

The primary asset is the Python script `delete_s3_column.py`. It deletes a specified column from both a CSV and a Parquet file in S3 using environment variables:

- `AWS_REGION` (default: `"ca-central-1"`)
- `S3_BUCKET` (default: `"eirepolitic-data"`)
- `CSV_KEY` (required)
- `PARQUET_KEY` (required)
- `COLUMN` (required)
- `STRICT` (default: `"0"`): Controls error handling if the column is missing.

The script uses `boto3`, `pandas`, and `pyarrow`, preserving the original file content types when overwriting.

A GitHub Actions workflow `.github/workflows/column_deleter.yml` allows manual execution with inputs for `csv_key`, `parquet_key`, `column`, and `strict`, running on Ubuntu with Python 3.11.

## Inputs and Outputs

### Inputs
- **AWS_REGION**: Optional. AWS region (default: `"ca-central-1"`).
- **S3_BUCKET**: Optional. S3 bucket (default: `"eirepolitic-data"`).
- **CSV_KEY**: Required. S3 key for the CSV file.
- **PARQUET_KEY**: Required. S3 key for the Parquet file.
- **COLUMN**: Required. Name of the column to delete.
- **STRICT**: Optional. `"1"`: error if the column is missing. `"0"`: skip missing files (default).

### Outputs
- Updated CSV and Parquet files overwritten in S3, with the specified column removed if present.
- CSV content type `"text/csv"`.
- Parquet content type `"application/x-parquet"`.
- Status messages indicating column removal.

## How it works

The pipeline deletes a specified column from both CSV and Parquet files in S3. It uses environment variables for S3 location, column name, and strictness. It reads the files using `pandas` (CSV) and `pyarrow` (Parquet), drops the column if present, and writes the results back to S3, overwriting originals.

If `STRICT` is `"1"` and the column is missing in either file, a runtime error is raised. If `"0"`, missing columns are ignored for those files. Execution is managed via the Python script and a manual GitHub Actions workflow.

## How to run

To delete a column from both a CSV and Parquet file in S3:

### Environment Variables

- **Required:**
  - `CSV_KEY`: S3 key for CSV.
  - `PARQUET_KEY`: S3 key for Parquet.
  - `COLUMN`: Column to delete.

- **Optional:**
  - `AWS_REGION` (default: `"ca-central-1"`).
  - `S3_BUCKET` (default: `"eirepolitic-data"`).
  - `STRICT`: `"1"` for error if column missing, `"0"` for ignore (default).

### Running the Script

Python 3.11 with `pandas` and `pyarrow` is required.

```bash
python process/delete_s3_column.py
```

Set the environment variables before running. The script reads and updates both files in S3.

### GitHub Actions Workflow

Manually trigger the workflow with these inputs:

- `csv_key`
- `parquet_key`
- `column`
- `strict`

AWS credentials and region are set via GitHub secrets. The workflow uses the `"eirepolitic-data"` bucket, installs dependencies, and runs the script.

## Data quality and validation

Data validation is enforced by checking for the specified column in both files. `STRICT=1` causes a runtime error if the column is missing in either file, detailing where it's missing. `STRICT=0` skips missing columns.

Files are always re-written to S3 for consistency, using UTF-8 BOM (CSV) or Snappy compression (Parquet). The workflow installs necessary dependencies and runs the script, with a 60-minute timeout and AWS details from secrets.

## Maintenance

Set `AWS_REGION` and `S3_BUCKET` as needed (defaults: `ca-central-1`, `eirepolitic-data`). For each run, supply `CSV_KEY`, `PARQUET_KEY`, and `COLUMN`.

`STRICT=1` stops on missing columns; `STRICT=0` writes files back even if no column is removed.

The pipeline uses `boto3`, processes/removes columns, and always writes results back to S3.

The GitHub Actions workflow runs on `ubuntu-latest`, with a 60-minute timeout, needs AWS secrets, installs dependencies, and is triggered via `workflow_dispatch` with the relevant inputs. Workflow concurrency group: `delete-s3-column`, with `cancel-in-progress` disabled.

## Orchestration

The pipeline is triggered manually via the **Delete Column From S3 CSV+Parquet (Manual)** GitHub Actions workflow. Required inputs:

- `csv_key`
- `parquet_key`
- `column`
- `strict` (default `"0"`)

Workflow runs on `ubuntu-latest`, 60-minute timeout, concurrency group `delete-s3-column`, `cancel-in-progress` false.

AWS credentials/region are set from GitHub secrets, S3 bucket as `"eirepolitic-data"`.

Workflow steps:

1. Checkout repo.
2. Setup Python 3.11.
3. Install dependencies.
4. Run `process/delete_s3_column.py`.

The Python script deletes the column from both files, obeying the `STRICT` flag, and writes files back to S3.

## Lineage

This pipeline deletes a specified column from both CSV and Parquet files in the `eirepolitic-data` S3 bucket.

Required environment variables specify file keys and the column to delete. The files are read, updated, and written back to S3, with error handling controlled by the `STRICT` flag.

Implemented in Python using `boto3`, `pandas`, and `pyarrow`. Manually triggered via the **Delete Column From S3 CSV+Parquet (Manual)** workflow, requiring the relevant keys, column name, and strictness flag, with AWS credentials from GitHub secrets.