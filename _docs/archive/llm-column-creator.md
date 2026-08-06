---
title: LLM Column Creator
summary: Adds generated columns to S3-hosted tables using YAML-configured OpenAI prompts.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic
technologies:
  - Python
  - YAML
  - OpenAI API
  - Amazon S3
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-05
last_verified: 2026-02-27
archived_date: 2026-08-05
archive_reason: Historical pipeline documentation migrated into the knowledge-base archive.
permalink: /projects/pipelines/llm_column_creator/
---

# LLM Column Creator

## Overview

This configurable pipeline reads an S3-hosted table, uses selected columns as prompt variables, generates a new column with the OpenAI Responses API, and writes CSV and Parquet outputs back to S3.

## Source of truth

- Runner: `process/llm_table_runner.py`
- Task configuration: YAML files under `tasks/`
- Workflow templates: `.github/workflows/llm_task_controller_template.yml`

## Configuration

A task YAML defines:

- S3 bucket and input/output keys
- Columns to retain
- Row ID source or hash columns
- Up to five prompt-variable columns
- Output column and prompt template
- Model, reasoning, verbosity, retries, and delay
- `full_table` or `processed_only` write mode
- Resume or overwrite behavior
- Validation rules

## Operation

```bash
python process/llm_table_runner.py tasks/example.yml
```

The runner can use web search, remove citations, autosave progress, resume existing output, and validate non-empty text, maximum word count, and regular-expression requirements.

## Outputs

Outputs are written to configured S3 CSV and Snappy-compressed Parquet keys.

## Known failure modes

- Missing AWS or OpenAI credentials
- Invalid task YAML
- Prompt variables missing from the input table
- Model output failing validation
- Unsafe overwrite configuration
