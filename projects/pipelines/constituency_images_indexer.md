---
title: "AutoDoc Creation Pipeline"
layout: doc
---

# Constituency Images Indexer

**Project:** eirepolitic  
**Type:** pipeline  
**Last generated:** 2026-02-26T02:14:25.244325Z

---

## Overview

### Purpose
The Constituency Images Indexer pipeline creates an Athena table of constituency image URLs. Images are manually generated in Inkscape and uploaded to the public S3 bucket "eirepolitic-data."

### Scope
The pipeline lists public images in the specified S3 prefix, filtering by typical image extensions. It generates an index table (`filename`, `s3_key`, `url`), sorted by filename, and writes it as CSV and Parquet to S3. Implemented in Python (boto3, pandas, pyarrow), it runs via a manual GitHub Actions workflow.

## Assets

Images are uploaded to the public S3 bucket `eirepolitic-data` under the prefix `processed/constituencies/images/`. The pipeline lists images with the extensions: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`, `.svg`.

The pipeline creates an index table with columns `filename`, `s3_key`, and `url`, sorted by filename:

- CSV: `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
- Parquet: `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet`

Public URLs follow:

```
https://{bucket}.s3.{region}.amazonaws.com/{encoded_key}
```

Environment variables configure the pipeline:

- `AWS_REGION` (default: `ca-central-1`)
- `S3_BUCKET` (default: `eirepolitic-data`)
- `SOURCE_PREFIX` (default: `processed/constituencies/images/`)
- `OUTPUT_CSV_KEY` (default: `processed/constituencies/constituency_images.csv`)
- `OUTPUT_PARQUET_KEY` (default: `processed/constituencies/parquets/constituency_images.parquet`)

Uses `boto3` (S3), `pandas` (data), and `pyarrow` (Parquet, Snappy). CSV aids inspection; Parquet is for analytics with Athena.

The architecture: S3 (storage), Glue Crawler (schema inference), Athena (query). Athena tables point to S3 prefixes for flexible dataset expansion. Glue Crawler runs only when schema changes occur.

Script: `process/constituency_images_indexer.py`. The "Build Constituency Image Index (Manual)" GitHub Actions workflow runs the pipeline manually, sets up Python and dependencies, and configures environment variables.

Validation: Confirm S3 outputs exist and verify with simple Athena queries (e.g., `SELECT COUNT(*)`). Pipelines are idempotent, overwriting or updating output datasets in place; schema remains consistent unless changed.

## Inputs and Outputs

### Inputs
- S3 bucket: `eirepolitic-data`
- Source prefix: `processed/constituencies/images/`
- Environment variables:
  - `AWS_REGION` (default: `ca-central-1`)
  - `S3_BUCKET` (default: `eirepolitic-data`)
  - `SOURCE_PREFIX` (default: `processed/constituencies/images/`)
  - `OUTPUT_CSV_KEY` (default: `processed/constituencies/constituency_images.csv`)
  - `OUTPUT_PARQUET_KEY` (default: `processed/constituencies/parquets/constituency_images.parquet`)
- Image file extensions: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`, `.svg`

### Outputs
- CSV: `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
- Parquet: `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet`
- Both with columns: `filename`, `s3_key`, `url` (public S3 URL)

## How it works

The pipeline lists images from S3 `processed/constituencies/images/`, filters by image extensions, and builds a table (`filename`, `s3_key`, `url`). Public URLs use:

```
https://{bucket}.s3.{region}.amazonaws.com/{encoded_key}
```

Configured by environment variables, it writes sorted output as both CSV and Parquet to S3. It uses Python (`boto3`, `pandas`, `pyarrow`) and is triggered manually by the "Build Constituency Image Index (Manual)" workflow, which sets up the environment and runs the script.

## How to run

Run `constituency_images_indexer.py` to index images in `s3://eirepolitic-data/processed/constituencies/images/` and output indexed CSV and Parquet files to the same bucket.

### Environment variables

Defaults:

- `AWS_REGION`: `ca-central-1`
- `S3_BUCKET`: `eirepolitic-data`
- `SOURCE_PREFIX`: `processed/constituencies/images/`
- `OUTPUT_CSV_KEY`: `processed/constituencies/constituency_images.csv`
- `OUTPUT_PARQUET_KEY`: `processed/constituencies/parquets/constituency_images.parquet`

### Processing

- List S3 keys, filter by image extensions.
- Construct public URLs.
- Build DataFrame (`filename`, `s3_key`, `url`), sorted by filename.
- Write as CSV and Parquet (Snappy compressed).

### Running

Execute manually via **Build Constituency Image Index (Manual)** workflow:

1. Checkout code.
2. Setup Python 3.11.
3. Install dependencies.
4. Run:  
   `python process/constituency_images_indexer.py`

Workflow sets AWS credentials and environment variables.

### Requirements & Output

- AWS credentials for S3 access required.
- Script outputs progress messages and a "Done" on completion.

## Data quality and validation

All data is stored in a single S3 bucket, organized as `raw/` and `processed/`. Outputs are valid CSV and Parquet (PyArrow Snappy), maintaining schema unless changed. CSV is for inspection; Parquet is optimized for analytics.

Athena external tables reference S3 folder prefixes. Parquet SerDe allows Athena to read datasets directly. Glue Crawlers are run manually only for schema changes.

Pipeline scripts overwrite outputs idempotently and maintain Athena compatibility. Validate by confirming S3 outputs and querying Athena (e.g., `SELECT COUNT(*)`).

Typical issues: schema mismatches, missed crawler runs, or S3 permission errors. Schema-stable row-level updates don't require a crawler; changes to columns/types or S3 location do.

## Maintenance

The pipeline script indexes public images in S3 (`processed/constituencies/images/`) and produces indexed CSV/Parquet output. It filters typical image types and constructs public URLs. Triggered manually by the GitHub Actions workflow `constituency_images_index.yml` on `ubuntu-latest`, which installs Python and dependencies, sets AWS credentials and environment, and runs the script.

The architecture organizes S3 into `raw/` and `processed/`. CSV is for inspection; Parquet (Snappy) for analytics. Athena tables reference S3 prefixes, allowing multiple Parquet files without table changes.

Glue Crawlers are required only for schema changes. Pipelines must always write valid outputs with stable schema (unless changed intentionally). Glue Crawlers manage schema and metadata as needed.

Validate by confirming S3 outputs and running Athena queries (e.g., `SELECT COUNT(*)`). Common failure causes are schema mismatches, missing crawler runs, or S3 permissions. Row-level updates with unchanged schema don't require a crawler, but structural/schema changes do.

Architecture:

```
S3 (storage) → Glue Crawler (schema inference) → Athena (query layer)
```

## Orchestration

The pipeline runs via the manual GitHub Actions workflow **Build Constituency Image Index (Manual)**. This workflow (triggered by `workflow_dispatch`) executes on `ubuntu-latest`, sets environment variables, installs dependencies, and runs `process/constituency_images_indexer.py`.

It lists and indexes public images in `eirepolitic-data`, filtered by image extensions, generating public URLs:

```
https://{bucket}.s3.{region}.amazonaws.com/{encoded_key}
```

Outputs are saved to S3 as:

- CSV: `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
- Parquet: `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet`

The data lake uses a single S3 bucket, logical zones (`raw/`, `processed/`); Athena tables reference prefixes for multiple Parquet files. Glue Crawlers handle schema inference and updates with Athena as the query layer.

Glue Crawlers are run only for schema changes. Athena queries S3 directly using Parquet SerDe. The pipeline is idempotent, overwriting or updating outputs with a consistent schema. Validation includes confirming S3 outputs and running Athena queries.

Typical issues: schema mismatches, missing crawler runs, or S3 permissions. Row-level updates are safe without a crawler; schema changes require one.

Architecture:

```
S3 (storage) → Glue Crawler (schema inference) → Athena (query layer)
```

## Lineage

The pipeline creates an Athena table referencing URLs of constituency images, manually produced in Inkscape and stored publicly in the S3 prefix `processed/constituencies/images/`.

It lists S3 images filtered by relevant extensions, encodes S3 keys, and creates a table with `filename`, `s3_key`, `url`, sorted by filename. Outputs are written with UTF-8 BOM as CSV and with Snappy-compressed Parquet.

Pipeline configuration uses environment variables and runs via the manual GitHub Actions workflow "Build Constituency Image Index (Manual)", which sets environment, installs dependencies, and executes `process/constituency_images_indexer.py`.