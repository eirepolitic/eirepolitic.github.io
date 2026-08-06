---
title: Debate Issue Classifier
summary: Extracts Dáil debate speeches and classifies them into political issue categories.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic
technologies:
  - Python
  - OpenAI API
  - Amazon S3
  - Amazon Athena
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-05
last_verified: 2026-02-27
archived_date: 2026-08-05
archive_reason: Historical pipeline documentation migrated into the knowledge-base archive.
permalink: /projects/pipelines/debate_issue_classifier/
---

# Debate Issue Classifier

## Overview

This pipeline retrieves Dáil 34 debate records from the Oireachtas API, stores raw XML in S3, extracts and deduplicates speeches, and classifies eligible speeches into political issue categories using an OpenAI model.

## Source of truth

- Extractor: `extract/monthly_extract.py`
- XML parser: `extract/debates_xml_to_csv_s3.py`
- Classifier: `process/speech_issue_classifier.py`
- Workflows: `.github/workflows/monthly_extract.yml` and `.github/workflows/speech_issue_classifier.yml`
- Region: `ca-central-1`
- Bucket: `eirepolitic-data`

## Data flow

1. Download Akoma Ntoso XML debate files.
2. Store files under `raw/debates/xml/`.
3. Extract and deduplicate speeches into `raw/debates/debate_speeches_extracted.csv`.
4. Classify speeches into one of the configured political issue categories or `NONE`.
5. Write classified CSV and Parquet outputs.

Outputs:

- `processed/debates/debate_speeches_classified.csv`
- `processed/debates/parquets/debate_speeches_classified.parquet`

## Operation

The extraction workflow runs monthly. Classification is manually triggered and supports a `test_rows` input. AWS credentials and `OPENAI_API_KEY` are stored as GitHub secrets.

## Validation

Check workflow logs, confirm S3 outputs, and query the Parquet dataset in Athena. Classification validates responses against the allowed category list and autosaves partial progress.

## Known failure modes

- Oireachtas API throttling or XML parsing errors
- Invalid model output after retries
- Missing AWS or OpenAI secrets
- Athena schema mismatch after structural changes
