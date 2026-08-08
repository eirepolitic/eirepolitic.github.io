---
title: LLM Column Creator
summary: Historical predecessor concept for adding model-generated columns to S3 tables; current functionality is implemented by the Reusable LLM Task Runner Framework.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - YAML
  - OpenAI API
  - Amazon S3
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-07
last_verified: 2026-08-07
archived_date: 2026-08-05
archive_reason: Superseded documentation concept; no separate current LLM Column Creator implementation was identified, and its functionality is now represented by the reusable YAML-driven LLM task runner framework.
permalink: /projects/pipelines/llm_column_creator/
related:
  - /projects/systems/reusable-llm-task-runner-framework/
  - /projects/repositories/eirepolitic-data-pipeline/
---

# LLM Column Creator

## Current status

This is a **predecessor/archive record**.

A current repository search found no separate script, task, or workflow whose implementation identity is `LLM Column Creator` or `llm_column_creator`.

The active equivalent capability is now documented as the [Reusable LLM Task Runner Framework](/projects/systems/reusable-llm-task-runner-framework/), implemented by:

```text
process/llm_table_runner.py
tasks/*.yml
.github/workflows/llm_task_controller_template.yml
.github/workflows/Absence_Reason_Manual.yml
.github/workflows/In_Government_Manual.yml
```

The current framework should be treated as the implementation source of truth. This archive page exists only to preserve the earlier system name/concept and provide the successor link.

## Historical concept

The historical “LLM Column Creator” concept was to:

1. read a table from S3;
2. select existing row fields as prompt variables;
3. call an OpenAI model;
4. write the generated result into a new table column;
5. persist CSV/Parquet output back to S3.

That broad capability still exists, but it is no longer represented by a distinct current component named LLM Column Creator.

## Current successor

The Reusable LLM Task Runner Framework generalizes the concept through task YAML rather than one-off column-specific code.

Current framework capabilities include:

- configured S3 input/output keys;
- stable ID or deterministic fallback row identity;
- up to five prompt variables;
- configurable output column;
- OpenAI Responses API calls;
- optional web search;
- retries and request delay;
- autosave;
- resumable reuse of the current output column;
- overwrite mode;
- CSV and Parquet outputs;
- lightweight validation and one repair attempt;
- `full_table` and `processed_only` write behaviors;
- manual GitHub Actions controllers.

The detailed semantics, risks, and operating procedures belong on the current system page rather than being duplicated here.

## Important differences from the old summary

The previous archive text effectively described the **current** runner and listed `process/llm_table_runner.py` as this archived pipeline's source of truth. That blurred historical and current system identities.

The corrected interpretation is:

```text
historical LLM Column Creator concept
    ↓ superseded/generalized by
Reusable LLM Task Runner Framework
    ↓ configured through
current task YAML + manual controllers
```

No separate current implementation has been identified that should remain documented under the old name.

## Current framework caveats

For operator safety, the successor framework has important current limitations already documented on its system page, including:

- validation repair is not a hard final correctness gate;
- `max_words` truncates instead of failing;
- same-key full-table tasks can drop unrelated enrichment columns when `keep` lists omit them;
- resumed `processed_only` mode is not a cumulative merge store;
- direct boto3 access does not inherit Unified Oireachtas candidate/pointer isolation.

Those are current-framework behaviors, not historical properties that should be projected backward onto the predecessor concept.

## Migration guidance

Do not create new one-off “LLM Column Creator” scripts solely to preserve the historical naming convention.

For a new table-enrichment task:

1. use the current reusable runner unless its current write/validation semantics are unsuitable;
2. create a focused task YAML;
3. choose a safe output key and complete `keep` list;
4. use a small test-row limit first;
5. add strict executable validation for machine-consumed categorical outputs where needed;
6. review whether external OpenAI processing is appropriate for the selected prompt variables.

Any framework redesign should occur in the current runner documentation/implementation, not in this archive record.

## Verification record

- Last verified: `2026-08-07`
- Repository search: no separate current `LLM Column Creator`/`llm_column_creator` implementation identified.
- Current successor verified against: `process/llm_table_runner.py`, complete current `tasks/` tree, and current LLM manual controller workflows already audited for P1 target 20.
- Current classification: **superseded predecessor record**. Current functionality belongs to the Reusable LLM Task Runner Framework.
