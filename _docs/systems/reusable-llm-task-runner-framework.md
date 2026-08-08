---
title: Reusable LLM Task Runner Framework
summary: YAML-driven S3 table enrichment framework that calls the OpenAI Responses API row-by-row with optional web search, resumable output reuse, autosave, retry, repair attempts, CSV/Parquet output, and manual GitHub Actions controllers.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
system: Reusable LLM Task Runner Framework
repository: eirepolitic-data-pipeline
order: 43
permalink: /projects/systems/reusable-llm-task-runner-framework/
technologies:
  - Python
  - YAML
  - OpenAI Responses API
  - AWS S3
  - pandas
  - PyArrow
  - GitHub Actions
related:
  - /projects/repositories/eirepolitic-data-pipeline/
  - /projects/systems/member-profile-metrics-builder/
  - /projects/systems/irish-politics-analytics/
---

# Reusable LLM Task Runner Framework

## Summary

`process/llm_table_runner.py` is a generic, YAML-driven table enrichment runner in `eirepolitic-data-pipeline`.

It:

1. reads a CSV from S3;
2. keeps selected columns;
3. resolves a stable row ID;
4. exposes up to five row values to a prompt template;
5. calls the OpenAI Responses API, optionally with the built-in `web_search` tool;
6. validates and optionally retries a failed output shape;
7. writes the enriched result back to S3 as CSV and Parquet;
8. can reuse already-populated output values to resume incomplete work;
9. periodically autosaves long-running jobs.

The framework is configuration-driven rather than hard-coded to one political-enrichment task. Current checked-in tasks include member absence-reason research and current-government membership classification, plus a reusable example/template task.

## Current implementation state

**Verified implementation:** `process/llm_table_runner.py` is the single current generic runner.

**Verified configuration:** `tasks/` currently contains exactly three YAML files:

- `Absence_Reasons.yml`;
- `In_Government.yml`;
- `llm_task_template.yml`.

**Verified workflow configuration:** the repository currently contains:

- `.github/workflows/llm_task_controller_template.yml` — generic/manual example controller;
- `.github/workflows/Absence_Reason_Manual.yml` — dedicated absence-reason controller;
- `.github/workflows/In_Government_Manual.yml` — dedicated government-membership controller.

All three use `workflow_dispatch` only and share concurrency group `run-llm-tasks` with `cancel-in-progress: false`.

**Observed runtime evidence:** the generic controller's latest recorded run `21535030240` on 2026-01-31 succeeded after two earlier failures. The dedicated absence workflow latest run `21878606063` on 2026-02-10 succeeded. The dedicated government workflow latest run `21642958774` on 2026-02-03 succeeded.

These historical successes establish that those revisions executed successfully; current source remains the stronger definition of current behavior.

## Source of truth

| Concern | Current source |
| --- | --- |
| generic runner | `process/llm_table_runner.py` |
| configuration example | `tasks/llm_task_template.yml` |
| absence task | `tasks/Absence_Reasons.yml` |
| government-membership task | `tasks/In_Government.yml` |
| generic manual controller | `.github/workflows/llm_task_controller_template.yml` |
| absence controller | `.github/workflows/Absence_Reason_Manual.yml` |
| government controller | `.github/workflows/In_Government_Manual.yml` |

No dedicated automated test file for `llm_table_runner.py` was identified in the current repository audit. Current confidence is therefore based on implementation review plus observed workflow history.

## Task configuration contract

A task YAML is split into these effective sections:

```text
s3
columns
prompt_template
llm
run
write_mode
validation
```

### `s3`

Required/current fields:

- `bucket`
- `region`
- `input_key`
- `output_csv_key`
- `output_parquet_key`

`bucket` defaults to `eirepolitic-data` if omitted. `region` defaults to `AWS_REGION`, then `us-east-2`.

The runner uses direct `boto3` S3 calls rather than the Unified Oireachtas candidate/pointer resolver. Therefore this framework is not automatically candidate-batch aware.

### `columns`

Supported fields:

- `keep` — columns retained from the input; an empty list retains all input columns;
- `id` — preferred stable ID column;
- `id_hash_cols` — fallback source columns used to generate `_row_id` if the configured ID is unavailable;
- `vars` — up to five input columns exposed to the prompt as `{var1}` through `{var5}`;
- `output_col` — destination column for the LLM result.

Only the first five entries in `vars` are used. Missing positions are padded with blank values.

### `prompt_template`

Rendered with Python string formatting:

```text
prompt_template.format(var1=..., var2=..., ..., var5=...)
```

Any literal braces in a prompt therefore need normal Python-format escaping if they are not intended as variables.

### `llm`

Current supported fields:

- `model`;
- `use_web_search`;
- `strip_citations`;
- `reasoning_effort`;
- `verbosity`;
- `temperature`;
- `max_output_tokens`.

The configured model defaults to `OPENAI_MODEL`, then `gpt-4.1-mini`.

For non-GPT-5 models with no web search, omitted `temperature` becomes `0.0`. For GPT-5-family models, the runner sends `reasoning.effort` and `text.verbosity` instead of temperature. If GPT-5-family web search is enabled with `reasoning_effort=minimal`, the runner upgrades that request to `low`.

When `max_output_tokens` is zero or omitted, the runner sends `320`.

### `run`

Supported fields:

- `max_retries`;
- `delay_between_requests`;
- `autosave_interval`;
- `test_rows`;
- `overwrite_existing`.

Fallback environment variables exist for retries, delay, autosave interval, and test-row count.

### `write_mode`

Documented/current intended modes:

- `full_table`;
- `processed_only`.

Current code explicitly checks only whether the value equals `processed_only`; any other string falls through to full-table behavior. There is no strict write-mode enum validation in `load_config()`.

### `validation`

Supported fields:

- `require_non_empty`;
- `max_words`;
- `regex_must_match`.

These checks are intentionally lightweight and have important semantics described below.

## Stable row identity

If `columns.id` exists in the retained input columns, its values are converted to strings and trimmed.

If the configured ID is unavailable, the runner requires `id_hash_cols` and creates:

```text
_row_id = first 24 hex characters of SHA-256(
  value1 || value2 || ...
)
```

The hash is deterministic for the configured source values.

If neither a usable configured ID nor fallback hash columns are available, execution stops.

## Existing-output reuse and resume behavior

Before processing rows, the runner checks whether the configured output CSV already exists.

If it exists:

1. the CSV is loaded;
2. its ID column must be present;
3. a map is built from ID to nonmissing values of the current `output_col` only.

Unless `overwrite_existing=true`, those values pre-fill the current result and only rows where the current output column is missing are sent to OpenAI.

This is the framework's resumability mechanism.

### What “resume” does and does not preserve

Resume is scoped to the current configured `output_col`.

The runner does **not** merge arbitrary extra columns from the existing output CSV back into the result. Full-table output is reconstructed from the current input's retained `keep` columns plus the current output column.

This matters when multiple enrichment tasks write to the same S3 key.

## Current same-key enrichment risk

All three checked-in task YAML files currently use:

```text
input_key: processed/members/members_summaries.csv
output_csv_key: processed/members/members_summaries.csv
```

The two dedicated enrichment tasks retain only:

- `member_code`;
- `full_name`;
- `background`;

plus their own current output column.

Therefore, for example:

- running the absence task can write `member_code`, `full_name`, `background`, `absence_reason`;
- subsequently running the government task reconstructs the table from the configured keep columns plus `in_government`;
- `absence_reason` is not automatically retained unless it is also present in `columns.keep` for that task.

The current implementation can therefore drop unrelated enrichment columns when multiple tasks independently overwrite the same full-table output key.

This is a verified implementation characteristic and an important operator limitation, not a theoretical concern.

Changing task output keys, keep lists, or merge behavior would alter data-contract/architecture semantics and should be handled as an implementation change rather than silently adjusted in documentation.

## Overwrite semantics

### `overwrite_existing: false`

Default behavior.

Only rows whose current configured output column is missing are sent to OpenAI.

### `overwrite_existing: true`

All rows are selected for recomputation, regardless of whether an output already exists.

`tasks/In_Government.yml` currently sets `overwrite_existing: true`, so every selected row is recomputed each run unless `test_rows` restricts the selection.

This matters because the task asks a time-sensitive political question: current government membership can change, so the checked-in task deliberately refreshes the entire classification.

## Test-row behavior

If `test_rows > 0`, the selected work list is truncated to the first N rows after normal overwrite/resume selection.

The manual workflows also expose a `test_rows` input. If provided, the workflow mutates the checked-out task YAML in the ephemeral runner workspace before invoking the generic runner.

That mutation is not committed back to GitHub.

The shared concurrency group prevents the checked-in LLM manual workflows from running simultaneously with one another.

## OpenAI Responses API behavior

Each selected row produces a rendered prompt and one normal call to:

```text
client.responses.create(...)
```

The runner extracts text first from `response.output_text`, then falls back to message content items where necessary.

### Optional web search

When `use_web_search=true`, the request includes:

```text
tools = [{ type: web_search }]
tool_choice = auto
```

Both current dedicated tasks use web search.

The framework delegates source discovery/citation behavior to the OpenAI Responses API and stores only the returned final text in the table. It does not persist a structured list of source URLs, search queries, model-response IDs, or tool-call trace to S3.

### Citation stripping

When `strip_citations=true`, the runner removes inline numeric citation markers matching patterns like `[1]` from returned text.

This is simple text cleanup, not source verification.

`In_Government.yml` currently enables citation stripping; `Absence_Reasons.yml` does not.

## Retry behavior

`call_openai()` retries any exception up to `max_retries`.

Between failures it sleeps:

```text
2 seconds × attempt number
```

This is a linear increasing delay: 2, 4, 6, ... seconds.

After all attempts fail, the runner raises `RuntimeError` and the task stops.

The configured `delay_between_requests` is applied separately after each successfully processed row.

## Output validation and repair semantics

`validate_output()` applies checks in this order:

1. reject an empty output if `require_non_empty=true`;
2. if `max_words > 0`, truncate the text to at most that many words;
3. if `regex_must_match` is configured, require a regex match.

### `max_words` is truncation, not rejection

Exceeding the word limit does **not** mark the output invalid. The text is simply clamped to the configured maximum and can then pass.

### Failed validation triggers one repair call

When normal output validation fails, the runner appends a short correction instruction to the original prompt and calls OpenAI again.

The second response is validated once.

### Validation is not a hard final gate

If the second response still fails validation, current code does not raise an error.

Instead, it keeps the cleaned first response and writes it to the result.

Therefore the framework currently provides a **repair attempt**, not a strict “invalid output blocks write” guarantee.

This distinction is important for consumers that expect a constrained value such as `TRUE`/`FALSE`.

## Current validation gaps in task YAML

Both dedicated task configurations currently set:

```text
require_non_empty: true
max_words: 2000
regex_must_match: null
```

`In_Government.yml` prompts the model to return only `TRUE` or `FALSE`, but does **not** configure a regex enforcing those two values.

Therefore current implementation relies on prompt compliance rather than an executable Boolean-output contract.

`Absence_Reasons.yml` likewise has no regex enforcing its expected `NONE`/reason shape.

## Autosave behavior

After every `autosave_interval` processed rows, the runner writes current outputs to S3.

Current task YAML files use an autosave interval of 5 rows.

This reduces loss when a long API job fails after partial progress.

### Full-table autosave

For `full_table`, autosave writes the current reconstructed full result table.

### Processed-only autosave limitation

For `processed_only`, the write contains only `processed_rows` accumulated during the **current process invocation**.

A resumed processed-only run can therefore overwrite the configured output object with only the rows processed in the later invocation rather than automatically merging previously processed-only output rows.

No current checked-in task uses `processed_only`, but this is a current framework limitation operators should understand before adopting that mode.

## Final output behavior

At the end of the run the framework always writes:

- CSV using UTF-8 with BOM;
- Parquet using PyArrow/Snappy.

The output write is not transactional across both objects: the CSV is written first, followed by Parquet. A failure between those writes can temporarily leave the two representations out of sync.

The runner does not create a manifest, run ID, schema version, source snapshot, prompt hash, or model-metadata sidecar.

## Current task: Absence Reasons

Configuration: `tasks/Absence_Reasons.yml`.

Purpose: research whether a current Irish TD has a documented reason that could explain significant Dáil absences in 2025, returning an identified reason/period or `NONE`.

Current configuration:

- input/output CSV: `processed/members/members_summaries.csv`;
- Parquet: `processed/members/parquets/members_summaries.parquet`;
- ID: `member_code`;
- prompt variable: `full_name`;
- output column: `absence_reason`;
- model: `gpt-4.1-mini`;
- web search: enabled;
- citation stripping: disabled;
- overwrite existing: default false;
- full-table write;
- autosave every 5 processed rows;
- max retries 5.

The result remains model-generated research text. It should not be treated as a verified medical, family, employment, or personal-status fact without source review.

## Current task: In Government

Configuration: `tasks/In_Government.yml`.

Purpose: classify whether a current Irish TD was part of the coalition forming the current Irish government, requesting a `TRUE`/`FALSE` response.

Current configuration:

- same members summary input/output paths;
- ID: `member_code`;
- variable: `full_name`;
- output column: `in_government`;
- model: `gpt-4.1-mini`;
- web search: enabled;
- inline numeric citation stripping: enabled;
- overwrite existing: true;
- full-table write;
- no regex enforcing `TRUE|FALSE`.

Because this task asks about the **current** Irish government, its truth value is time-sensitive. The task's full overwrite behavior is consistent with recomputing time-sensitive classifications, but model/web-search output still requires quality review if used analytically.

## Generic example/template task

`tasks/llm_task_template.yml` is not a neutral empty schema file; it contains an executable example concerning potential conflicts of interest for Irish politicians.

It uses the same members summary S3 input/output key and writes a `conflicts_of_interest` column.

The manual `Run LLM Tasks (Manual)` workflow currently executes this template directly as its Task 1. Therefore the so-called template is also runnable current configuration.

It should not be assumed to be harmless scaffolding when the workflow is dispatched.

## Manual GitHub Actions controllers

All three current controllers:

- run on `ubuntu-latest`;
- use Python 3.11;
- have a 180-minute timeout;
- install repository requirements plus `pyarrow` and `pyyaml`;
- use `contents: read` permissions;
- consume AWS and OpenAI credentials from GitHub Actions secrets;
- share concurrency group `run-llm-tasks`;
- expose optional `test_rows` override.

The generic controller currently executes only `tasks/llm_task_template.yml`; a second-task example remains commented out.

The dedicated controllers each execute their matching task file.

## Observed runtime evidence

### Generic controller

Workflow ID `228928223`:

- run `21534781128`, 2026-01-30: failure;
- run `21534859761`, 2026-01-30: failure;
- run `21535030240`, 2026-01-31: success.

### Absence Reason

Workflow ID `232687901`:

- run `21878241423`, 2026-02-10: failure;
- run `21878360729`, 2026-02-10: cancelled;
- run `21878606063`, 2026-02-10: success.

### In Government

Workflow ID `229765365`:

- run `21610903529`, 2026-02-03: success;
- run `21613048864`, 2026-02-03: cancelled;
- run `21613580583`, 2026-02-03: failure;
- run `21642958774`, 2026-02-03: success.

Exact root causes of the historical failed/cancelled runs were not required to define current framework semantics and are not inferred here.

## External processing, privacy, and security boundary

The workflows supply these secrets:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`;
- `OPENAI_API_KEY`.

No secret values should be documented.

For each selected row, values mapped into `{var1}` through `{var5}` become part of the OpenAI request prompt. When web search is enabled, the request may also invoke OpenAI's web-search tool.

Operators should therefore treat selection of task input columns as an external-data-processing decision. Do not map private identifiers, credentials, confidential data, or unnecessary personal data into prompt variables.

Checked-in source proves the application-level API request behavior; it does not establish OpenAI account-level retention, organization settings, contractual controls, or current pricing.

## Cost boundary

The framework makes at least one OpenAI Responses API call per selected row.

Additional calls occur when validation fails and the repair path is invoked. Web-search-enabled tasks can also incur tool/search-related model usage according to the active API pricing/model behavior.

Total external API cost therefore scales approximately with:

```text
selected rows × normal model call
+ validation-repair calls
+ any applicable web-search/tool usage
```

`overwrite_existing=true` can materially increase cost because it recomputes every selected row even when values already exist.

`test_rows` is the primary current mechanism for limiting an experimental run before full-table execution.

## Failure modes

Verified/directly implied failure areas include:

- S3 input missing or unreadable;
- missing retained columns;
- missing configured ID and unusable hash columns;
- existing output missing the configured ID column;
- prompt-formatting errors;
- OpenAI API/authentication/rate/service errors exhausting retries;
- output validation/repair producing an unexpected value without hard failure;
- S3 CSV write succeeding while Parquet write fails;
- same-key full-table tasks dropping non-kept enrichment columns;
- processed-only resumed runs overwriting earlier processed-only rows;
- workflow timeout during large row counts/web searches;
- cost amplification from overwrite mode or repeated repair calls.

## Safe operating procedure

1. Read the exact task YAML before dispatching a workflow; do not assume a file named `template` is non-executable.
2. Confirm input and output S3 keys, especially whether they are the same object.
3. Confirm `columns.keep` includes every column that must survive a full-table rewrite.
4. Confirm the ID column is stable and present in `keep`.
5. Review which source columns are exposed as prompt variables.
6. Use a small `test_rows` value for new or changed prompts/models.
7. Confirm whether `overwrite_existing` is appropriate; leave it false for resumable enrichment unless a time-sensitive field must be recomputed.
8. For constrained outputs, add an executable regex and independently review whether soft repair semantics are acceptable.
9. Inspect output CSV/Parquet and representative rows before downstream use.
10. Do not treat model-generated research claims as verified facts solely because the workflow succeeded.

## Safe change procedure

For a new task:

1. Copy a YAML task as a structural starting point, but replace its keys/prompt/output deliberately.
2. Prefer a new output key until merge/preservation behavior has been proven.
3. Use a stable source ID rather than hash fallback where possible.
4. Keep only the minimum necessary prompt variables.
5. Configure strict output validation for machine-consumed categorical fields.
6. Run with `test_rows` first.
7. Inspect data preservation across CSV and Parquet.
8. Only then add or enable a dedicated manual workflow controller.

For framework changes, add dedicated automated tests before changing resume/write/validation semantics because current task data can be overwritten in place.

## Known limitations

- No dedicated automated test suite was identified for the generic runner.
- Current YAML loading has limited schema validation and no strict enum check for `write_mode`.
- Validation repair is soft: a still-invalid second response does not block writing.
- `max_words` silently truncates rather than failing.
- Current categorical `In_Government` task has no regex enforcing `TRUE`/`FALSE`.
- Existing output reuse preserves only the current output column, not arbitrary enrichment columns.
- Multiple current tasks write back to the same source CSV/Parquet and can drop one another's fields if keep lists are incomplete.
- `processed_only` is not safe as a cumulative resume store without additional merge behavior.
- CSV/Parquet writes are sequential rather than atomic.
- No run manifest, model-response metadata, prompt hash, source citations object, or task-version sidecar is written.
- Direct boto3 S3 access means the framework does not inherit Unified Oireachtas candidate/pointer isolation.
- Historical successful workflow runs are from January/February 2026 and do not constitute a fresh current-main execution test.

## Next safe development action

P1 is complete once this page passes documentation validation, merges, and its exact merge SHA succeeds in Pages.

The next priority is P2 target 38: maintenance, repair, and backfill utilities. That audit should classify each utility by current/historical status, mutation scope, destructive risk, workflow controls, dry-run/backup behavior, and whether a safer current successor exists.

## Related documents

- [Member Profile Metrics Builder](/projects/systems/member-profile-metrics-builder/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [Irish Politics Analytics](/projects/systems/irish-politics-analytics/)

## Verification record

- Last verified: `2026-08-07`
- Verified implementation/configuration: `process/llm_table_runner.py`; complete current `tasks/` tree; `tasks/llm_task_template.yml`; `tasks/Absence_Reasons.yml`; `tasks/In_Government.yml`; `.github/workflows/llm_task_controller_template.yml`; `.github/workflows/Absence_Reason_Manual.yml`; `.github/workflows/In_Government_Manual.yml`; current workflow registry.
- Observed runtime evidence: generic workflow ID `228928223` including run `21535030240`; absence workflow ID `232687901` including run `21878606063`; government workflow ID `229765365` including run `21642958774`.
- Verification scope: task schema, ID generation, row selection, resume/overwrite behavior, prompt rendering, Responses API/web-search behavior, GPT-5/non-GPT-5 request differences, retry timing, output validation/repair semantics, autosave/write modes, CSV/Parquet outputs, same-key preservation risks, current tasks/controllers, security/cost boundaries, runtime evidence, failure modes, and limitations.
