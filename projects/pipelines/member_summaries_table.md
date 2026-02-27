---
title: "Member Summaries Table"
layout: default
---

# Member Summaries Table

**Project:** eirepolitic  
**Type:** pipeline  
**Last generated:** 2026-02-27T22:24:45.396732Z

---

## Overview

### Purpose
This pipeline creates the member summaries Athena table, holding generated or scraped background information about Dáil TDs, including absence reasons. It supports analytics and reporting with curated, queryable datasets for the 34th Dáil.

### Scope
The pipeline fetches all members for the 34th Dáil, builds a member-level table, and uploads a CSV to `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv`, overwriting on reruns. The summarizer reads this CSV from S3, builds a table with `member_code` and `full_name`, and uses the OpenAI Responses API (with web_search) to generate up to 200-word neutral background summaries on upbringing, pre-political work, and political history before 2025. Outputs are written in CSV and Parquet formats in `processed/members/`.

Data in S3 is logically organized: `raw/` for source data, `processed/` for curated datasets. Athena external tables point to S3 Parquet prefixes to allow schema evolution without table changes. AWS Glue Crawlers are run manually to infer schema and update Athena metadata when needed. The pipeline is idempotent, safely overwriting outputs while maintaining schema consistency for reliable Athena queries and BI integration.

Required environment variables include AWS credentials and region, with optional configuration for API and summarizer parameters. The summarizer supports resumable, multi-task safe execution, preserving outputs unless forced to recompute. Validation involves checking S3 outputs and simple Athena queries. Failure modes include schema mismatches, unrun crawlers, and S3 permissions. Only structural schema changes or relocations require new crawler runs. The pipeline conforms to the standard S3 → Glue Crawler → Athena pattern.

## Assets

The pipeline manages these datasets in S3 bucket `eirepolitic-data`, organized as:

- **Raw Data**  
  - `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv`: Member-level data for the 34th Dáil, overwritten on reruns.

- **Processed Data**  
  - CSV: `processed/members/members_summaries.csv` (for inspection/debugging)
  - Parquet: `processed/members/parquets/members_summaries.parquet` (optimized for analytics; written using PyArrow with Snappy compression)

The summarizer output is resumable and multi-task safe, updating only the "background" column.

### S3 Data Lake Structure

- `raw/` for source data  
- `processed/` for curated datasets  

### Athena and Glue Integration

- Athena external tables point to S3 folder prefixes, supporting multiple Parquet files.
- AWS Glue Crawlers are run manually for schema changes (column or dataset changes), not for routine data refreshes.
- Athena uses Parquet SerDe with LOCATION set to the Parquet prefix.

### Pipeline and Validation

- Scripts produce valid, schema-consistent CSV and Parquet outputs; Parquet outputs are Athena-compatible.
- Outputs are overwritten or updated in place (idempotent).
- Validation: confirm file existence in S3, run simple Athena queries (e.g., `SELECT COUNT(*)`).

### Environment Configuration

- Required: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- Summarizer uses environment variables for S3 location and summarization parameters.

### Failure Modes

- Schema mismatches may cause Athena errors.
- New schema in Athena needs a Glue Crawler run.
- S3 permission issues can block data access.

## Inputs and Outputs

### Inputs

- **Extraction pipeline:**  
  - Oireachtas API response JSON (`https://api.oireachtas.ie/v1/members?chamber=dail&house_no=34&limit=500`), configurable via `API_URL`.
- **Summarizer pipeline:**  
  - Input CSV from `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv` (configurable via `INPUT_KEY`), must contain `member_code` and `full_name`.
  - Environment variables: `OPENAI_API_KEY`, `S3_BUCKET`, `OUTPUT_CSV_KEY`, `OUTPUT_PARQUET_KEY`, `OPENAI_MODEL`, and others for configuration.

### Outputs

- **Extraction pipeline:**  
  - CSV: `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv` (columns: `full_name`, `first_name`, `last_name`, `constituency`, `party`, `gender`, `member_code`, `uri`), overwritten on reruns.
- **Summarizer pipeline:**  
  - CSV: `s3://eirepolitic-data/processed/members/members_summaries.csv`
  - Parquet: `s3://eirepolitic-data/processed/members/parquets/members_summaries.parquet`
  - Outputs include all original columns plus a `background` column.
  - Files have appropriate content types.
  - Summarizer merges input and existing outputs, processing only missing/empty backgrounds unless forced. The process is resumable and multi-task safe.

## How it works

The extraction script fetches all Dáil 34 members (preferring Dáil 34 membership, else most recent), producing a member-level CSV at `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv`. Data is gathered from the Oireachtas API with retries and backoff for failures. Configuration is via AWS/environment variables.

The summarizer reads the members CSV from S3, creates a table with `member_code` and `full_name`, and uses the OpenAI Responses API with web_search to generate factual, neutral backgrounds (max 200 words, covering upbringing, pre-political work, and political history pre-2025). Summaries are stripped of citations, URLs, and markdown.

Output is written as CSV and Parquet in `processed/members/`, with each run resumable and task-safe, updating only the background column unless forced. Autosaving occurs at defined intervals using PyArrow with Snappy compression.

Athena tables point to S3 prefixes, allowing multiple Parquet files without table changes. Schema is managed by manually-run Glue Crawlers—triggered only for schema changes, not data refresh. Athena tables use the Parquet SerDe and S3 LOCATION.

Outputs are idempotently overwritten/updated to maintain schema and Athena compatibility. Only structural dataset or schema changes require a new Glue Crawler run.

The architecture follows: S3 (storage) → Glue Crawler (schema inference) → Athena (query layer).

## How to run

### Running the member extraction pipeline

Run `monthly_members_extract.py` to fetch and upload the 34th Dáil CSV to S3:

```
s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv
```

- Required environment:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_REGION`
- Optional:
  - `API_URL` (default: `https://api.oireachtas.ie/v1/members?chamber=dail&house_no=34&limit=500`)
  - `API_TIMEOUT` (default: 30)
  - `API_SLEEP` (default: 0.2)

Run with:

```bash
python monthly_members_extract.py
```

---

### Running the members background summarizer

Run `members_background_summarizer.py`, which reads the input CSV and writes outputs:

- Input: `s3://<bucket>/raw/members/oireachtas_members_34th_dail.csv` (must have `member_code`, `full_name`)
- Outputs:
  - CSV: `s3://<bucket>/processed/members/members_summaries.csv`
  - Parquet: `s3://<bucket>/processed/members/parquets/members_summaries.parquet`
- Resumable; only updates `background` unless forced.
- Autosaves according to `AUTOSAVE_INTERVAL` (default 25).
- Required: `OPENAI_API_KEY`
- Optional: `S3_BUCKET`, `INPUT_KEY`, `OUTPUT_CSV_KEY`, `OUTPUT_PARQUET_KEY`, `OPENAI_MODEL`, `OPENAI_REASONING_EFFORT`, `OPENAI_VERBOSITY`, `MAX_OUTPUT_TOKENS`, `TEST_ROWS`, `FORCE_COLUMNS`, `AUTOSAVE_INTERVAL`, `DELAY_BETWEEN_REQUESTS`, `MAX_RETRIES`.

Run with:

```bash
python members_background_summarizer.py
```

---

### Environment setup

Set AWS credentials and region before running scripts. Set `OPENAI_API_KEY` before running the summarizer.

---

### GitHub Actions workflow

`.github/workflows/members_background_summarizer.yml` runs the summarizer script manually with a `test_rows` input (default 25), on `ubuntu-latest` (timeout: 180 minutes), using Python 3.11, and installs required dependencies.

## Data quality and validation

Pipelines output valid, schema-consistent CSV and Parquet files, safely overwritten/updated for idempotency. Data availability is validated by presence in S3 and Athena queries (e.g., `SELECT COUNT(*)`).

Athena tables reference S3 Parquet prefixes, with schema inferred and updated by manually-run Glue Crawlers upon schema changes. Routine data updates need no new crawler run unless schema changes.

Common failure modes: schema mismatches (Athena errors), missing crawler runs (absent columns), and S3 permission errors.

## Maintenance

Pipelines are idempotent, overwriting/updating outputs in-place, maintaining a consistent schema, and writing Parquet files with PyArrow and Snappy for Athena compatibility.

Athena tables point to S3 prefixes, allowing dataset growth without table changes. Athena tables remain stable with unchanged schema.

Validation: confirm S3 outputs and run Athena queries.

Structural changes (column addition/removal/type, S3 relocation) require a Glue Crawler run. Routine refreshes do not.

Maintain correct S3 permissions for uninterrupted access.

## Orchestration

All datasets are in a single S3 bucket partitioned by `raw/` (source) and `processed/` (analytics-ready). Scripts output valid CSV and Parquet, maintaining schema stability. CSVs are for inspection; Parquet is for analytics (PyArrow + Snappy).

Athena tables are defined over S3 prefixes, supporting multi-file expansion and using Parquet SerDe. Athena queries data directly from S3.

Glue Crawlers infer schema and manage metadata, run manually on structural changes only. Routine refreshes need no crawler run if the schema is stable.

Pipelines are idempotent, safely updating outputs, ensuring Athena compatibility. Validation is by checking S3 and running Athena queries.

Standardized pattern:

```
S3 (storage) → Glue Crawler (schema inference) → Athena (query layer)
```

All pipelines use this architecture for maintainability.

## Lineage

The extraction pipeline fetches and builds the member-level table for Dáil 34—preferring explicit Dáil 34 records, else most recent—exporting CSV to `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv` (overwritten on reruns).

The summarizer reads that CSV, generating ≤200-word member background summaries (upbringing, pre-political work, political history pre-2025), using the OpenAI Responses API (web_search). Output (including updated `background`) is written to `processed/members/members_summaries.csv` and `processed/members/parquets/members_summaries.parquet`.

The summarizer is resumable and task-safe, updating only backgrounds unless forced, and is configured by environment variables. It can be triggered manually in GitHub Actions as "Summarize Member Backgrounds (Manual)" (Python 3.11, `ubuntu-latest`, 180 min timeout).

Architecture: S3 → Glue Crawlers (schema/metadata) → Athena. Glue Crawlers are manually run for any schema or location changes; Athena external tables point to S3 Parquet prefixes with schema via Glue. Pipelines output CSV/Parquet, preserving schema and idempotency.