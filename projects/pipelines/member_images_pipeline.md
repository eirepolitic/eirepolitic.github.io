---
title: "Member Images Pipeline"
layout: default
---

# Member Images Pipeline

**Project:** eirepolitic  
**Type:** pipeline  
**Last generated:** 2026-02-27T21:54:03.854342Z

---

## Overview

### Purpose
The Member Images Pipeline creates an Athena table of member image URLs by scraping member profiles on the Oireachtas website.

### Scope
Part of the eirepolitic project, the pipeline processes an S3 CSV (`raw/members/oireachtas_members_34th_dail.csv` by default). It scrapes Oireachtas public member pages for profile photo URLs, using fallback selectors as needed. Output includes two S3 files: a CSV (`processed/members/members_photo_urls.csv`) and a Parquet file (`processed/members/parquets/members_photo_urls.parquet`). The pipeline is resumable, updating only missing photo URLs if output exists.

Implemented in Python using boto3, pandas, requests, BeautifulSoup, and pyarrow, configuration is via environment variables: AWS credentials, S3 bucket (`eirepolitic-data` default), input/output keys, request timeout (10s default), request delay (0.2s default), autosave interval (50 rows default), and test rows (0 default).

Execution is manually triggered by the "Build Member Photo URLs (Manual)" GitHub Actions workflow, which sets up Python 3.11, installs dependencies, and runs the script. The workflow accepts a `test_rows` parameter to limit processing to the first N missing records (default 50).

## Assets

The pipeline includes the `members_photo_urls.py` Python script, which builds a member table with columns `member_code`, `full_name`, and `photo_url` by scraping each public member profile for its photo.

### Input

- CSV file at:  
  `s3://<bucket>/raw/members/oireachtas_members_34th_dail.csv`

### Output

- CSV at:  
  `s3://<bucket>/processed/members/members_photo_urls.csv`  
  (UTF-8 with BOM)
- Parquet at:  
  `s3://<bucket>/processed/members/parquets/members_photo_urls.parquet`  
  (Snappy)

### Script Behavior

- Resumable: only missing `photo_url` values are filled if output exists.
- S3 read/write via `boto3`.
- Configurable via environment variables:  
  - AWS credentials and region  
  - S3 bucket/keys:  
    - `S3_BUCKET` (default: `eirepolitic-data`)  
    - `INPUT_KEY` (default: `raw/members/oireachtas_members_34th_dail.csv`)  
    - `OUTPUT_CSV_KEY` (default: `processed/members/members_photo_urls.csv`)  
    - `OUTPUT_PARQUET_KEY` (default: `processed/members/parquets/members_photo_urls.parquet`)  
  - Request/processing parameters:  
    - `REQUEST_TIMEOUT` (default: 10)  
    - `DELAY_BETWEEN_REQUESTS` (default: 0.2)  
    - `AUTOSAVE_INTERVAL` (default: 50)  
    - `TEST_ROWS` (default: 0)

### Automation

- Workflow `.github/workflows/member_photo_urls.yml` runs script manually.
- AWS and S3 configs set in environment.
- Installs dependencies.
- Supports limiting by `test_rows` (default 50).

## Inputs and Outputs

### Inputs
- Input CSV: `s3://<bucket>/raw/members/oireachtas_members_34th_dail.csv` with columns: `member_code`, `full_name`, `uri`.
- Input path configurable via:
  - `S3_BUCKET` (default: `eirepolitic-data`)
  - `INPUT_KEY` (default: `raw/members/oireachtas_members_34th_dail.csv`)

### Outputs
- Outputs:
  - CSV: `s3://<bucket>/processed/members/members_photo_urls.csv`
  - Parquet: `s3://<bucket>/processed/members/parquets/members_photo_urls.parquet`
- Output columns: `member_code`, `full_name`, `photo_url`.
- Resumable: only missing `photo_url` rows processed if output exists.
- Output paths configurable via:
  - `OUTPUT_CSV_KEY` (default: `processed/members/members_photo_urls.csv`)
  - `OUTPUT_PARQUET_KEY` (default: `processed/members/parquets/members_photo_urls.parquet`)

## How it works

The pipeline reads a CSV from S3 (`raw/members/oireachtas_members_34th_dail.csv`) and builds a table with `member_code`, `full_name`, and `photo_url`.

For each member, the script converts the `uri` to a public profile URL and scrapes for the profile image using CSS selectors, including fallbacks. Existing photo URLs in the output CSV are mapped to skip already-processed rows; only missing photo URLs are scraped, optionally limited via a test rows parameter.

Progress autosaves to S3 as CSV and Parquet at intervals (`AUTOSAVE_INTERVAL`). All configuration (AWS, S3 keys, processing parameters) is via environment variables.

S3 interaction is handled by `boto3`; web requests and parsing are via `requests` and `BeautifulSoup`. Errors or missing images result in a missing `photo_url`.

A GitHub Actions workflow sets up Python and dependencies, runs the script, and allows a manual input for row limits.

## How to run

The script `members_photo_urls.py` builds a member table (`member_code`, `full_name`, `photo_url`) by scraping the Oireachtas profile photos.

### Input and Output

- **Input CSV:** `s3://<bucket>/raw/members/oireachtas_members_34th_dail.csv`
- **Output CSV:** `s3://<bucket>/processed/members/members_photo_urls.csv`
- **Output Parquet:** `s3://<bucket>/processed/members/parquets/members_photo_urls.parquet`
- Script resumes, processing only missing `photo_url` values if output exists.

### Environment Variables

Set before running:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` (default: `ca-central-1`)
- `S3_BUCKET` (default: `eirepolitic-data`)
- `INPUT_KEY` (default: `raw/members/oireachtas_members_34th_dail.csv`)
- `OUTPUT_CSV_KEY` (default: `processed/members/members_photo_urls.csv`)
- `OUTPUT_PARQUET_KEY` (default: `processed/members/parquets/members_photo_urls.parquet`)
- `REQUEST_TIMEOUT` (default: 10)
- `DELAY_BETWEEN_REQUESTS` (default: 0.2)
- `AUTOSAVE_INTERVAL` (default: 50)
- `TEST_ROWS` (default: 0)

### Dependencies

- `boto3`
- `pandas`
- `requests`
- `beautifulsoup4`
- `pyarrow`

### Running the Script

```bash
python process/members_photo_urls.py
```

Ensure required environment variables are set.

### GitHub Actions Workflow

The **Build Member Photo URLs (Manual)** workflow runs on `ubuntu-latest` (60 min timeout):

- Sets AWS/s3 environment variables.
- Installs dependencies.
- Runs script with optional `TEST_ROWS` limit (default 50).
- Triggered manually.

## Data quality and validation

- **Input validation:** Confirms input CSV includes `member_code`, `full_name`, and `uri`. Missing columns raise errors.
- **Resumable:** Loads existing output to skip filled `photo_url` values.
- **Missing data:** Only missing `photo_url` rows are scraped.
- **Scraping validation:** Uses CSS selectors with fallbacks. Failure to get photo or errors results in missing `photo_url`.
- **Autosave:** Progress saved to S3 at `AUTOSAVE_INTERVAL` in CSV (UTF-8-sig) and Parquet (Snappy).
- **Logging:** Logs total failures (no URL, no image, errors).
- **Configurable execution:** Delay between requests (`DELAY_BETWEEN_REQUESTS`) and row limit (`TEST_ROWS`) configurable.

## Maintenance

The script resumes from existing output, processing only missing `photo_url` values. Configuration is via environment variables for AWS, S3 keys, and processing parameters.

Progress autosaves to S3 every `AUTOSAVE_INTERVAL` rows, minimizing data loss.

Scraping failures are handled by setting `photo_url` to null. Validation checks the CSV for required columns.

The manual GitHub Actions workflow supports a `test_rows` input (default 50) and installs all needed dependencies.

A delay (`DELAY_BETWEEN_REQUESTS`) controls scraping rate.

S3 operations use `boto3`. Console logging facilitates monitoring.

## Orchestration

Orchestrated by the **Build Member Photo URLs (Manual)** GitHub Actions workflow, triggered manually (`workflow_dispatch`) with input `test_rows` (default 50).

Workflow concurrency group: `members-photo-urls`, allowing multiple jobs. Runs on `ubuntu-latest`, 60 min timeout.

Env variables set for AWS, S3, and path configuration:

- `S3_BUCKET`
- `INPUT_KEY`
- `OUTPUT_CSV_KEY`
- `OUTPUT_PARQUET_KEY`

Workflow steps:

1. Checkout repo.
2. Set up Python 3.11.
3. Install dependencies.
4. Run script (`TEST_ROWS` passed from input).

## Lineage

The pipeline builds a table (`member_code`, `full_name`, `photo_url`) by reading from `s3://<bucket>/raw/members/oireachtas_members_34th_dail.csv` and scraping Oireachtas profile photos.

Member URIs are converted to public profile URLs; images are scraped using CSS selectors with fallbacks. 

The pipeline loads existing output to avoid duplicate scraping, is resumable for missing `photo_url` values, and can be limited by row count. Progress is autosaved to S3 (CSV and Parquet).

Implemented in Python using boto3, pandas, requests, BeautifulSoup, and pyarrow, with configuration via environment variables.

Manually executed via the "Build Member Photo URLs (Manual)" GitHub Actions workflow, which installs dependencies and allows an input for test rows.