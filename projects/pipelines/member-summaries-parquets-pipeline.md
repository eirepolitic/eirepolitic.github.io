---
layout: page
title: Member Summaries Parquets Pipeline Documentation
permalink: /projects/pipelines/member-summaries-parquets-pipeline/
---

# members_summaries_parquets Pipeline

## Overview
### Purpose
Generate and maintain the Athena external table `members_summaries_parquets` from a resumable OpenAI-powered enrichment job that writes `members_summaries.csv` and `members_summaries.parquet` to S3.

---

## Architecture
### High-Level Flow
1. Read member roster CSV from S3 (`raw/members/oireachtas_members_34th_dail.csv`).
2. Build base table (`member_code`, `full_name`) as the source-of-truth roster and ordering.
3. Load existing output CSV from S3 if present to preserve other columns and enable resumability.
4. For rows missing `background` (or forced recompute), call OpenAI Responses API with the `web_search` tool.
5. Post-process model output to remove citations/links and normalize whitespace.
6. Write updated CSV and Parquet to S3 (autosave periodically + final save).
7. Athena table `members_summaries_parquets` reads Parquet data from `s3://eirepolitic-data/processed/members/parquets/`.
8. AWS Glue crawler `members_crawler` updates schema/metadata as needed.

### Components
1. Input roster (S3): `raw/members/oireachtas_members_34th_dail.csv`
2. Processing job: `process/members_background_summarizer.py`
3. Orchestration: GitHub Actions workflow `Summarize Member Backgrounds (Manual)`
4. Storage (S3):
   - CSV: `processed/members/members_summaries.csv`
   - Parquet: `processed/members/parquets/members_summaries.parquet`
5. Glue Crawler: `members_crawler`
6. Athena Table: `members_summaries_parquets`

---

## Data Flow
### Inputs
- S3 input CSV:
  - `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv`
- Required columns in input:
  - `member_code`
  - `full_name`

### Processing Steps
- Load input roster CSV from S3.
- Create `df_base = [member_code, full_name]` with `member_code` normalized to trimmed strings.
- Load existing output CSV if present:
  - `s3://eirepolitic-data/processed/members/members_summaries.csv`
- Build `df_res` by right-joining existing output onto `df_base`:
  - Ensures current roster membership and ordering matches `df_base`
  - Preserves any additional columns present in the prior output CSV
  - Refreshes `full_name` from `df_base` as source of truth
- Ensure output column exists:
  - `background` (OUT_COL)
- Determine rows to process:
  - Default: where `background` is missing (NA/empty/"nan"/"null"/"na")
  - Optional override: `FORCE_COLUMNS` env var includes `background` or `ALL`
  - Optional limit: `TEST_ROWS` env var to process first N rows of the to-do set
- For each row to process:
  - Build prompt via `build_prompt(full_name)`
  - Call OpenAI Responses API with `tools=[{"type":"web_search"}]`
  - Retry up to `MAX_RETRIES` with backoff on exceptions/empty output
  - For GPT-5 family models:
    - Apply `reasoning.effort` and `text.verbosity`
    - If `OPENAI_REASONING_EFFORT=minimal`, it is automatically upgraded to `low` to avoid `web_search` incompatibility
  - Post-process output:
    - Remove parenthetical references containing URLs/markdown links
    - Remove raw URLs
    - Remove numeric bracket citations like `[1]`
    - Normalize whitespace
  - Write summary to `background`
- Autosave:
  - Every `AUTOSAVE_INTERVAL` processed rows, write CSV + Parquet to S3
- Final save:
  - Always writes final CSV + Parquet to S3

### Outputs
- CSV:
  - `s3://eirepolitic-data/processed/members/members_summaries.csv`
- Parquet:
  - `s3://eirepolitic-data/processed/members/parquets/members_summaries.parquet`
- Athena (external) table:
  - `members_summaries_parquets`
  - LOCATION: `s3://eirepolitic-data/processed/members/parquets/`

---

## Implementation Details
### Technologies Used
- Python 3.11
- GitHub Actions (manual workflow dispatch)
- AWS S3 (storage)
- boto3 (S3 I/O)
- pandas (dataframe transforms)
- pyarrow (Parquet writing; snappy compression)
- OpenAI Python SDK (Responses API)
- OpenAI tool: `web_search`
- AWS Glue Crawler (`members_crawler`)
- AWS Athena (external table over Parquet)

### Execution Method
- Manual trigger via GitHub Actions `workflow_dispatch`
- Job timeout: `timeout-minutes: 180`

### Configuration
#### GitHub Actions inputs
- `test_rows` (string; "0" = all missing; default "25")

#### Environment variables (job level)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`
- `S3_BUCKET` = `eirepolitic-data`
- `INPUT_KEY` = `raw/members/oireachtas_members_34th_dail.csv`
- `OUTPUT_CSV_KEY` = `processed/members/members_summaries.csv`
- `OUTPUT_PARQUET_KEY` = `processed/members/parquets/members_summaries.parquet`

#### Environment variables (step level)
- `OPENAI_API_KEY` (required)
- `OPENAI_MODEL` = `gpt-4.1-mini` (configurable; supports GPT-5 family)
- `OPENAI_REASONING_EFFORT` = `low` (used for GPT-5 family)
- `OPENAI_VERBOSITY` = `low` (used for GPT-5 family)
- `MAX_OUTPUT_TOKENS` = `320` (module default is 320 if not set)
- `TEST_ROWS` = `${{ inputs.test_rows }}`
- Optional (module defaults if unset):
  - `FORCE_COLUMNS` (e.g., "background" or "ALL")
  - `AUTOSAVE_INTERVAL` (default 25)
  - `DELAY_BETWEEN_REQUESTS` (default 0.25 seconds)
  - `MAX_RETRIES` (default 5)

---

## Dependencies
### Internal
- Repo script:
  - `process/members_background_summarizer.py`
- Input roster generation pipeline that produces:
  - `raw/members/oireachtas_members_34th_dail.csv` (not documented here)

### External
- OpenAI Responses API
- OpenAI `web_search` tool availability (model-dependent behavior handled in code)
- Oireachtas/member information indexed by web search sources

---

## Operational Details
### Runtime Characteristics
- Trigger: manual via GitHub Actions
- Concurrency:
  - `group: summarize-member-backgrounds`
  - `cancel-in-progress: false` (multi-run safe due to resumable design, but concurrent runs can still cause last-write-wins on outputs)
- Typical runtime drivers:
  - number of missing `background` rows
  - request throttling via `DELAY_BETWEEN_REQUESTS`
  - retries on empty/error outputs

### Failure Handling
- OpenAI call retries:
  - Up to `MAX_RETRIES` attempts with increasing sleep (`2.0 * attempt`)
  - Treats empty output as retryable
- Resumability:
  - If outputs exist, only missing `background` rows are processed (unless forced)
- Data safety:
  - Periodic autosaves reduce loss on interruption
  - Final write always updates CSV + Parquet

### Monitoring
- GitHub Actions run status + logs
- Validate S3 outputs exist/updated:
  - `processed/members/members_summaries.csv`
  - `processed/members/parquets/members_summaries.parquet`
- Validate Athena table freshness:
  - `SELECT COUNT(*) FROM members_summaries_parquets;`
- Glue crawler:
  - Run `members_crawler` when schema changes are introduced

---

## Maintenance
### Known Limitations
- `web_search` tool usage can vary by model capability; code prevents GPT-5 + minimal reasoning from using `web_search` by upgrading effort to `low`.
- Output is single-field `background` summaries; no source citations are retained by design (citations/links are stripped).
- Writes a single Parquet file path in practice, but Athena table LOCATION points to the folder:
  - `s3://eirepolitic-data/processed/members/parquets/`

### Future Improvements
- Add deterministic model settings/versioning for reproducibility.
- Add incremental provenance fields (e.g., `summary_generated_at`, `model_used`).
- Add rate-limit/backoff logic based on HTTP status codes and OpenAI errors.
- Add automated crawler run when schema changes are detected (optional).

---

## Related Resources
### Code Location
- GitHub Actions workflow:
  - `Summarize Member Backgrounds (Manual)` (workflow file path in repo not provided)
- Python module:
  - `process/members_background_summarizer.py`

### Athena Table DDL (current)
- Table: `members_summaries_parquets`
- Columns:
  - `member_code` string
  - `full_name` string
  - `background` string
  - `absence_reason` string
- LOCATION:
  - `s3://eirepolitic-data/processed/members/parquets/`
- Crawler:
  - `UPDATED_BY_CRAWLER = members_crawler`
