---
title: Constituency Images Indexer
summary: Builds an Athena-compatible index of constituency image files stored in S3.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic
technologies:
  - Python
  - Amazon S3
  - AWS Glue
  - Amazon Athena
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-05
last_verified: 2026-02-27
archived_date: 2026-08-05
archive_reason: Historical pipeline documentation migrated into the knowledge-base archive.
permalink: /projects/pipelines/constituency_images_indexer/
---

# Constituency Images Indexer

## Overview

This pipeline indexes constituency images stored under `s3://eirepolitic-data/processed/constituencies/images/` and creates a queryable table containing each filename, S3 key, and public URL.

## Source of truth

- Script: `process/constituency_images_indexer.py`
- Workflow: `.github/workflows/constituency_images_index.yml`
- Default region: `ca-central-1`
- Default bucket: `eirepolitic-data`

## Inputs and outputs

Input image formats include JPG, PNG, WebP, GIF, BMP, TIFF, and SVG.

Outputs:

- CSV: `processed/constituencies/constituency_images.csv`
- Parquet: `processed/constituencies/parquets/constituency_images.parquet`
- Columns: `filename`, `s3_key`, `url`

Parquet output uses Snappy compression and is intended for Athena.

## Operation

The manually triggered GitHub Actions workflow runs Python 3.11 and executes:

```bash
python process/constituency_images_indexer.py
```

Configuration is supplied through `AWS_REGION`, `S3_BUCKET`, `SOURCE_PREFIX`, `OUTPUT_CSV_KEY`, and `OUTPUT_PARQUET_KEY`.

## Validation

Confirm both output files exist in S3 and run an Athena count query. A Glue Crawler is only required when the schema or dataset location changes.

## Known failure modes

- Missing S3 permissions
- Images stored outside the configured prefix
- Athena metadata not refreshed after a schema change
