---
title: "Debate Issue Classifier"
layout: default
---

# Debate Issue Classifier

**Project:** eirepolitic  
**Type:** pipeline  
**Last generated:** 2026-02-27T21:14:21.447560Z

---

## Overview

### Purpose
The "Debate Issue Classifier" pipeline assigns political issue categories to sections of speech from Dáil Éireann debate records. It processes raw debate data, extracts and deduplicates speeches, and assigns each to a predefined category using large language model calls.

### Scope
The pipeline collects Dáil 34 debate records from the Oireachtas API, downloads raw XML files, and uploads them to an S3 bucket. It parses XML files to extract deduplicated speeches (with metadata) and saves them as CSVs to S3. Each speech is classified into one of 25 political categories or "NONE" using OpenAI models. Results are saved in CSV and Parquet formats in S3. The pipeline supports validation, autosaving, iterative refinement, and monthly scheduling via GitHub Actions. It is implemented in Python with libraries including requests, boto3, pandas, xml.etree.ElementTree, the OpenAI SDK, and pyarrow.

## Assets

Key assets are stored in the S3 bucket `eirepolitic-data` in the `ca-central-1` region.

- **Raw XML Debate Files**  
  Downloaded from Oireachtas API, normalized, and stored under:  
  `raw/debates/xml/`  
  Files:  
  `YYYY-MM-DD__<debate_id>.xml`  
  Overwrites are permitted on reruns.

- **Extracted Debate Speeches CSV**  
  Deduplicated speeches from XML files are saved to:  
  `raw/debates/debate_speeches_extracted.csv`

- **Classified Speeches CSV and Parquet**  
  OpenAI-classified speeches are saved as CSV at:  
  `processed/debates/debate_speeches_classified.csv`  
  And as Parquet under:  
  `processed/debates/parquets/`  
  with a `.parquet` extension. Autosaving of partial progress is supported.

S3 operations require AWS credentials and region configuration. GitHub Actions workflows orchestrate extraction and processing.

## Inputs and Outputs

### Inputs
- Raw XML debate records for Dáil 34 from the Oireachtas API.
- XML files named `YYYY-MM-DD__<debate_id>.xml`, stored at `raw/debates/xml/` in the S3 bucket `eirepolitic-data`.
- Extracted debate speeches CSV at `s3://eirepolitic-data/raw/debates/debate_speeches_extracted.csv`.
- Environment variables for OpenAI model parameters, AWS credentials, region, and processing limits.

### Outputs
- Raw XML files at `s3://eirepolitic-data/raw/debates/xml/YYYY-MM-DD__<debate_id>.xml`.
- Extracted speech CSV at `s3://eirepolitic-data/raw/debates/debate_speeches_extracted.csv`.
- Classified CSV at `s3://eirepolitic-data/processed/debates/debate_speeches_classified.csv`.
- Classified Parquet at `s3://eirepolitic-data/processed/debates/parquets/debate_speeches_classified.parquet`.

## How it works

The pipeline fetches Dáil Éireann debate records from the Oireachtas API for Dáil 34, pages through the API, downloads Akoma Ntoso XML files, and uploads them to S3 (`eirepolitic-data/raw/debates/xml/`) with the naming format `YYYY-MM-DD__<debate_id>.xml`.

It parses XML speeches, extracting metadata such as date, section, speaker name, and text, and deduplicates speeches by debate date, speaker name, and speech text. Deduplicated speeches are saved as a CSV to S3.

OpenAI's GPT models then classify each speech into one of 25 political issue categories or "NONE." Only speeches with at least 20 words are classified; shorter or empty speeches are labeled "NONE." The classification process features prompt refinement and retries (up to five) to ensure valid output.

Classified results are saved to CSV and Parquet in S3, with each speech assigned a deterministic `speech_id` for tracking and deduplication. The pipeline implements retry and backoff for API calls, and autosaves partial results.

The process is fully automated and scheduled monthly via GitHub Actions.

## How to run

Run these three Python scripts in order:

1. **`monthly_extract.py`**  
   Fetches all Dáil 34 debates, downloads XMLs, uploads to S3 at `raw/debates/xml/`.  
   Required env vars:  
   - `AWS_ACCESS_KEY_ID`  
   - `AWS_SECRET_ACCESS_KEY`  
   - `AWS_REGION`  
   Optional env vars (defaults):  
   - `CHAMBER_ID` (`/ie/oireachtas/house/dail/34`)  
   - `LANG` (`en`)  
   - `API_LIMIT` (`200`)  
   - `API_SLEEP` (`0.2`)  
   - `DOWNLOAD_TIMEOUT` (`30`)  

2. **`debates_xml_to_csv_s3.py`**  
   Reads XMLs from S3, extracts & deduplicates speeches, writes CSV at `raw/debates/debate_speeches_extracted.csv`.  
   Required env var:  
   - `AWS_REGION` (default `ca-central-1`)  

3. **`speech_issue_classifier.py`**  
   Loads extracted CSV, classifies speeches via OpenAI API, writes classified results to CSV (`processed/debates/debate_speeches_classified.csv`) and Parquet.  
   Required env vars:  
   - `AWS_REGION` (default `ca-central-1`)  
   - `OPENAI_API_KEY`  
   Optional env vars (defaults):  
   - `OPENAI_MODEL` (`gpt-4o-mini`)  
   - `OPENAI_REASONING_EFFORT` (`minimal`)  
   - `OPENAI_VERBOSITY` (`low`)  
   - `MAX_OUTPUT_TOKENS` (`0`)  
   - `DELAY_BETWEEN_REQUESTS` (`0.25`)  
   - `MAX_ITERATIONS` (`5`)  
   - `AUTOSAVE_INTERVAL` (`50`)  
   - `TEST_ROWS` (`0`)  
   - `S3_BUCKET` (`eirepolitic-data`)  
   - `INPUT_KEY`  
   - `OUTPUT_KEY`  
   - `PARQUET_KEY`  

### Running locally or in CI

- Set AWS credentials and region in the environment.  
- Install dependencies from `requirements.txt`.  
- Run, in order:  
  1. `monthly_extract.py`  
  2. `debates_xml_to_csv_s3.py`  
  3. `speech_issue_classifier.py`  

Python scripts use `boto3` and require network access to the Oireachtas and OpenAI APIs.

### Running via GitHub Actions

- The `monthly_extract.yml` workflow runs monthly (1st, 09:15 UTC) and:  
  - Checks out the repo  
  - Sets up Python 3.11  
  - Installs dependencies  
  - Runs `monthly_extract.py`  
  - Runs `debates_xml_to_csv_s3.py`  
  - Runs `monthly_members_extract.py`  

- The `speech_issue_classifier.yml` workflow is triggered manually (`workflow_dispatch`, input: `test_rows`, default `50`) and:  
  - Sets environment and AWS credentials  
  - Checks out repo  
  - Sets up Python 3.11  
  - Installs dependencies  
  - Runs `speech_issue_classifier.py`  
  - Converts the classified CSV to Parquet

## Data quality and validation

Data quality is ensured through the following:

- **Acquisition and storage**: Debates are fetched and XMLs uploaded to S3 (`raw/debates/xml/`) as `YYYY-MM-DD__<debate_id>.xml` (overwrites allowed).
- **Extraction**: Retry logic with exponential backoff and HTTP 429 handling on fetches. Extracts debate date, XML URI (normalized), and debate ID.
- **XML parsing**: Robust parsing and error logging; skipped files on parse error.
- **Sorting and deduplication**: Stable sort by date and order; deduplication on normalized date, speaker, and text.
- **Classification validation**: Uses a deterministic `speech_id`. Custom missing check treats nulls/empty as missing except literal `"NONE"`. Short speeches labeled `"NONE"`.
- **OpenAI classification**: Calls OpenAI with validation and retries for valid output against the allowed list.
- **Progress monitoring**: Autosaves classification progress every 50 rows. Logs process statistics.
- **Repeatable execution**: GitHub Actions workflows use environment variables for secure, repeatable execution.

## Maintenance

Pipeline configuration relies on environment variables, including AWS credentials.

### Extractor Configuration

`monthly_extract.py` uses optional env vars:

- `CHAMBER_ID` (default: `/ie/oireachtas/house/dail/34`)
- `LANG` (default: `en`)
- `API_LIMIT` (default: 200)
- `API_SLEEP` (default: 0.2)
- `DOWNLOAD_TIMEOUT` (default: 30)

It fetches debates, downloads XMLs, and uploads to S3 as `YYYY-MM-DD__<debate_id>.xml` (overwrites allowed). HTTP fetches use retry and backoff logic.

### XML-to-CSV Conversion

`debates_xml_to_csv_s3.py` lists XMLs from S3, extracts and deduplicates speeches, and writes to `raw/debates/debate_speeches_extracted.csv`.

### Speech Issue Classification

`speech_issue_classifier.py` classifies missing labels using OpenAI, with retry and validation. Outputs are written as CSV and Parquet in S3. Supports autosave every 50 rows.

Classifier configuration via environment variables, including:

- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `OPENAI_REASONING_EFFORT`
- `OPENAI_VERBOSITY`
- `TEST_ROWS`
- S3 input/output keys

### GitHub Actions Workflows

- **Monthly Extraction:** Runs at 09:15 UTC on the 1st. Sets up Python 3.11, installs dependencies, and runs extract and conversion steps. AWS credentials are GitHub secrets.
- **Manual Classification:** Allows a `test_rows` input. Runs classifier and CSV-to-Parquet conversion. Requires AWS credentials and OpenAI API key as secrets.

AWS credentials and OpenAI API keys must be managed as GitHub secrets.

## Orchestration

Orchestration uses GitHub Actions workflows in `.github/workworks/monthly_extract.yml` and `.github/workflows/speech_issue_classifier.yml`.

### Monthly Extract Workflow

- Scheduled for 09:15 UTC monthly or can run manually.
- Uses concurrency group `monthly-extract`.
- Steps:
  - Checkout repository
  - Setup Python 3.11
  - Install dependencies
  - Run `extract/monthly_extract.py`
  - Run `extract/debates_xml_to_csv_s3.py`
  - Run `extract/monthly_members_extract.py`

### Speech Issue Classifier Workflow

- Triggered manually (`workflow_dispatch`, input: `test_rows`).
- Runs on `ubuntu-latest` (timeout: 720 min).
- Uses concurrency group `classify-political-issues`.
- Sets AWS credentials/environment.
- Steps:
  - Checkout repository
  - Setup Python 3.11
  - Install dependencies
  - Run `process/speech_issue_classifier.py`
  - Run `process/debate_speeches_csv_to_parquet.py`

### Environment Variables

Both workflows depend on AWS credentials: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, and optionally `AWS_SESSION_TOKEN`.

## Lineage

The pipeline pages through the Oireachtas `/debates` API for Dáil 34, downloads XMLs, and uploads to S3 (`raw/debates/xml/`) as `YYYY-MM-DD__<debate_id>.xml` (overwrites allowed).

Each XML yields debate date, XML URI (normalized to absolute), and debate ID. Extracted speeches are saved as a deduplicated CSV at `raw/debates/debate_speeches_extracted.csv` with fields: Debate Date, Debate Section, Debate Section Name, Speaker Name, Speech Text, and Speech Order. Speaker names are resolved from XML references or tags. Deduplication uses normalized Debate Date, Speaker Name, and Speech Text.

OpenAI (default `gpt-4o-mini`) classifies speeches ≥20 words into one of 25 political categories or "NONE," assigning a deterministic `speech_id`. Existing classifications are reused to avoid reprocessing. Outputs are saved as CSV (`processed/debates/debate_speeches_classified.csv`) and Parquet (`processed/debates/parquets/debate_speeches_classified.parquet`).

The pipeline is scheduled monthly via a GitHub Actions workflow ("Monthly Extract"). Classification is run manually or with test row limits via the "Classify Political Issues (Manual)" workflow.