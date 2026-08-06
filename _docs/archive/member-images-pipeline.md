---
title: Member Images Pipeline
summary: Scrapes Oireachtas member profile images and publishes a reusable S3 table of photo URLs.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic
technologies:
  - Python
  - Amazon S3
  - Beautiful Soup
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-05
last_verified: 2026-02-27
archived_date: 2026-08-05
archive_reason: Historical pipeline documentation migrated into the knowledge-base archive.
permalink: /projects/pipelines/member_images_pipeline/
---

# Member Images Pipeline

## Overview

This pipeline reads the 34th Dáil member table from S3, visits each public Oireachtas member profile, extracts the profile image URL, and publishes CSV and Parquet outputs.

## Source of truth

- Script: `process/members_photo_urls.py`
- Workflow: `.github/workflows/member_photo_urls.yml`
- Default bucket: `eirepolitic-data`
- Default region: `ca-central-1`

## Inputs and outputs

Input:

- `raw/members/oireachtas_members_34th_dail.csv`
- Required columns: `member_code`, `full_name`, `uri`

Outputs:

- `processed/members/members_photo_urls.csv`
- `processed/members/parquets/members_photo_urls.parquet`
- Columns: `member_code`, `full_name`, `photo_url`

## Operation

The workflow is manually triggered and accepts a `test_rows` limit. The process resumes from existing output and only attempts rows with missing `photo_url` values.

```bash
python process/members_photo_urls.py
```

Key settings include `REQUEST_TIMEOUT`, `DELAY_BETWEEN_REQUESTS`, `AUTOSAVE_INTERVAL`, and `TEST_ROWS`.

## Validation

Confirm required input columns, inspect workflow failure counts, and verify both S3 output files.

## Known failure modes

- Oireachtas page structure changes
- Missing profile images
- Request failures or throttling
- Missing S3 permissions
