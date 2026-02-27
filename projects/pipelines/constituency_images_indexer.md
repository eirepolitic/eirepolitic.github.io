---
title: "Constituency Images Indexer"
layout: default
---

# Constituency Images Indexer

**Project:** eirepolitic  
**Type:** pipeline  
**Last generated:** 2026-02-27T20:41:06.827932Z

---

## Overview

### Purpose
The Constituency Images Indexer pipeline creates an Athena table containing URLs of constituency images by indexing publicly available images in an S3 bucket for efficient querying.

### Scope
The pipeline lists images at `s3://eirepolitic-data/processed/constituencies/images/`, filtering by common image formats. It generates and sorts an index table with filename, S3 key, and URL, output as CSV and Parquet files to specified S3 locations. The pipeline configures via environment variables, uses boto3 and pandas with pyarrow for data handling, and encodes S3 keys for safe URLs. The process is manually triggered via GitHub Actions, following a standardized architecture using S3, Glue Crawlers, and Athena.

## Assets

Images are stored in S3 bucket `eirepolitic-data` under `processed/constituencies/images/`, created in Inkscape from a base SVG.

Supported formats: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`, `.svg`. The pipeline creates an index table with `filename`, `s3_key`, and public `url`.

Outputs:

- CSV: `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
- Parquet: `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet` (Snappy compression via PyArrow)

Public URLs pattern:

```
https://{bucket}.s3.{region}.amazonaws.com/{encoded_key}
```

The Python script `process/constituency_images_indexer.py` is executed manually via the GitHub Actions workflow "Build Constituency Image Index (Manual)" on `ubuntu-latest` with Python 3.11, installing required dependencies.

Outputs are designed for Athena compatibility and use a standardized S3 layout. Idempotency is maintained by overwriting outputs in place.

Schema management relies on AWS Glue Crawlers, run manually if schema changes.

Key environment variables:

- `AWS_REGION`
- `S3_BUCKET`
- `SOURCE_PREFIX`
- CSV and Parquet output keys

## Inputs and Outputs

### Inputs
- Public images in `eirepolitic-data/processed/constituencies/images/`
- File types: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`, `.svg`
- Images are recolored SVGs created in Inkscape
- Environment variables (defaults):
  - `AWS_REGION`: `ca-central-1`
  - `S3_BUCKET`: `eirepolitic-data`
  - `SOURCE_PREFIX`: `processed/constituencies/images/`

### Outputs
- Index table with: `filename`, `s3_key`, `url`
- Formats:
  - CSV: `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
  - Parquet: `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet` (Snappy)
- Configurable output keys:
  - `OUTPUT_CSV_KEY`
  - `OUTPUT_PARQUET_KEY`
- Athena-compatible; overwritten in place unless schema changes

## How it works

The pipeline lists and filters images in the configured S3 location by extension, then creates an index table with filename, S3 key, and a constructed public URL.

Outputs:
- CSV written with UTF-8 BOM for inspection/debugging
- Parquet written with PyArrow and Snappy compression, optimized for Athena

Configuration uses environment variables with sensible defaults.

Manual execution is via GitHub Actions with Python 3.11. The job installs dependencies, then runs the script.

Outputs are routinely overwritten for idempotency. Parquet outputs are structured for Athena external tables, supporting future expansion.

Schema and metadata updates are handled separately by running AWS Glue Crawlers if schema changes; routine refreshes do not require it.

## How to run

Run `constituency_images_indexer.py` to index S3 images at `s3://eirepolitic-data/processed/constituencies/images/`. Output locations:

- CSV: `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
- Parquet: `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet`

### Environment Variables (defaults):

- `AWS_REGION`: `ca-central-1`
- `S3_BUCKET`: `eirepolitic-data`
- `SOURCE_PREFIX`: `processed/constituencies/images/`
- `OUTPUT_CSV_KEY`: `processed/constituencies/constituency_images.csv`
- `OUTPUT_PARQUET_KEY`: `processed/constituencies/parquets/constituency_images.parquet`

### Image Filtering

Indexed extensions: `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`, `.svg`

### Implementation

- Uses boto3 to interact with S3
- CSVs are UTF-8 BOM
- Parquet uses Snappy (Athena-compatible)
- Overwrites outputs to maintain idempotency

### Manual Execution

Trigger GitHub Actions workflow `constituency_images_index.yml` with `workflow_dispatch`. The workflow runs on `ubuntu-latest`, sets up Python 3.11, installs required packages, and runs:

```bash
python process/constituency_images_indexer.py
```

## Data quality and validation

Validation consists of confirming output file existence in S3 and running simple Athena queries such as `SELECT COUNT(*)` to verify readability and accessibility.

Schema consistency is maintained unless intentionally changed. Run a Glue Crawler only if schema changes (e.g., columns/data types/dataset location). For routine data updates with no schema changes, no Crawler run is needed.

Pipelines overwrite or update data safely in place. Adding/replacing data rows and overwriting Parquet files with the same schema are safe changes not requiring a crawler.

Be aware of S3 permission issues and missing crawler runs as potential failure points.

## Maintenance

The pipeline overwrites output datasets in place to ensure idempotency and schema consistency. Athena tables remain stable except when schema is modified.

### Verification

Check S3 output files and run Athena queries, such as:

```sql
SELECT COUNT(*) FROM your_table;
```

### Schema Changes and Glue Crawlers

Manually run Glue Crawlers if:

- Columns are added/removed/modified
- Data types are changed
- Dataset S3 location changes

If not run, Athena queries may fail due to schema issues.

### Routine Updates

Routine data refreshes that don’t alter the schema don’t require a crawler run.

### Permissions

S3 permissions must allow required operations for listing and querying.

### Summary

- Pipeline provides stable CSV and Parquet outputs.
- Run Glue Crawlers only for structural/schema changes.
- Data refreshes with same schema do not require Glue Crawlers.
- Validate by checking S3 and Athena access.
- Ensure correct S3 permissions.

## Orchestration

The pipeline builds an Athena-compatible index of image URLs using images stored at `eirepolitic-data/processed/constituencies/images/`, manually created and uploaded.

The Python script lists public images via boto3, filters by file extension, and generates an index table (filename, S3 key, public URL), outputting to CSV and (Snappy-compressed, Athena-compatible) Parquet.

Execution is manual via GitHub Actions (`workflow_dispatch`), on `ubuntu-latest` and Python 3.11. Steps include checking out the code, installing dependencies, and running the script.

The architecture applies a standard pattern: S3 for storage, logical folders like `raw/` and `processed/`, CSV for inspection, Parquet for analytics. Athena tables point to Parquet prefixes. Glue Crawlers manage schema and are run only for schema changes.

Athena tables query S3 Parquet data using the Parquet SerDe. The pipeline maintains schema consistency and idempotent outputs.

Validation steps: Confirm S3 outputs, run Athena queries such as `SELECT COUNT(*)`.

Safe changes without a Glue Crawler: add/replace rows, overwrite Parquet with same schema. Crawler is needed for structural or type changes or S3 location moves.

Overall pattern: S3 → Glue Crawler (schema) → Athena (query).

## Lineage

The pipeline indexes public images at `eirepolitic-data/processed/constituencies/images/`, recolored SVGs created in Inkscape.

It filters by standard image extensions, builds an index table (filename, S3 key, public URL), sorts it, and outputs to:

- CSV: `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
- Parquet: `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet` (Snappy-compressed with PyArrow)

Configuration relies on environment variables, with sensible defaults.

Execution is via the GitHub Actions workflow "Build Constituency Image Index (Manual)" (`workflow_dispatch`) running Python 3.11.

The architecture: datasets in S3, schema managed by Glue Crawlers, and querying with Athena. Glue Crawlers are only needed for schema changes; routine refreshes do not require them.

