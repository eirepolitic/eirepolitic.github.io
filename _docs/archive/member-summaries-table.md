---
title: Member Summaries Table
summary: Builds member-level background summaries for the 34th Dáil and publishes Athena-compatible outputs.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic
technologies:
  - Python
  - OpenAI API
  - Amazon S3
  - AWS Glue
  - Amazon Athena
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-05
last_verified: 2026-02-27
archived_date: 2026-08-05
archive_reason: Historical pipeline documentation migrated into the knowledge-base archive.
permalink: /projects/pipelines/member_summaries_table/
---

# Member Summaries Table

## Overview

This pipeline builds a member-level dataset for the 34th Dáil and generates neutral background summaries covering upbringing, pre-political work, and political history before 2025.

## Source of truth

- Member extraction: `monthly_members_extract.py`
- Summarizer: `members_background_summarizer.py`
- Workflow: `.github/workflows/members_background_summarizer.yml`
- Bucket: `eirepolitic-data`
- Region: `ca-central-1`

## Data flow

1. Fetch member records from the Oireachtas API.
2. Write `raw/members/oireachtas_members_34th_dail.csv`.
3. Generate or resume background summaries using the OpenAI Responses API with web search.
4. Write CSV and Parquet outputs under `processed/members/`.

Outputs:

- `processed/members/members_summaries.csv`
- `processed/members/parquets/members_summaries.parquet`

## Operation

The summarizer is manually triggered, supports `test_rows`, autosaves progress, and updates only missing backgrounds unless forced.

## Validation

Confirm S3 outputs, inspect workflow logs, and query the Parquet dataset in Athena. Run a Glue Crawler only when columns, types, or dataset locations change.

## Known failure modes

- Oireachtas API failures
- Missing OpenAI or AWS credentials
- Invalid or incomplete generated summaries
- Athena schema mismatches
