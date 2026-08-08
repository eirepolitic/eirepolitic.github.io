---
title: Member Summaries Table
summary: Historical member-background summarization pipeline retained as the source producer for the newer Unified Oireachtas member-summary compatibility layer; the same legacy table is also shared by current generic LLM enrichment tasks.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - OpenAI API
  - Amazon S3
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-07
last_verified: 2026-08-07
archived_date: 2026-08-05
archive_reason: Historical standalone pipeline record retained for lineage; current Oireachtas summary enrichment consumes the legacy table rather than replacing summary generation.
permalink: /projects/pipelines/member_summaries_table/
related:
  - /projects/systems/reusable-llm-task-runner-framework/
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/notes/oireachtas-write-policies-downstream-contracts/
---

# Member Summaries Table

## Current status

This is an **archive/lineage record** for the dedicated member-background summarizer.

The retained implementation is directly verifiable on current `eirepolitic-data-pipeline/main`:

```text
process/members_background_summarizer.py
.github/workflows/members_background_summarizer.yml
```

The newer Unified Oireachtas summaries layer is:

```text
extract/oireachtas/enrichment_member_summaries.py
.github/workflows/oireachtas_member_summaries_enrichment_trial.yml
```

The newer layer explicitly does **not** call OpenAI. It reads the legacy summary table and adapts/validates it into enrichment and compatibility outputs.

Therefore the dedicated background-generation function has not been replaced by the Oireachtas enrichment layer.

## Retained background summarizer

`process/members_background_summarizer.py` reads:

```text
raw/members/oireachtas_members_34th_dail.csv
```

and requires:

```text
member_code
full_name
```

It produces/updates:

```text
processed/members/members_summaries.csv
processed/members/parquets/members_summaries.parquet
```

The generated field is:

```text
background
```

The prompt asks for a neutral, factual member background of no more than 200 words covering, where reliably available:

- where the member grew up;
- pre-political work;
- political history before 2025.

The implementation uses the OpenAI Responses API with the `web_search` tool.

## Current manual workflow

Workflow: **Summarize Member Backgrounds (Manual)**.

Current checked-in configuration:

- manual `workflow_dispatch`;
- Python 3.11;
- `test_rows`, default `25`;
- 180-minute timeout;
- concurrency group `summarize-member-backgrounds`;
- model override `gpt-4.1-mini`;
- `OPENAI_REASONING_EFFORT=low`;
- `OPENAI_VERBOSITY=low`;
- `MAX_OUTPUT_TOKENS=320`;
- AWS/OpenAI credentials from GitHub Actions secrets.

The script itself also supports `FORCE_COLUMNS`, including `background` or `ALL`, but the inspected workflow does not expose that as a manual input.

## Resume and table-preservation behavior

The dedicated summarizer is designed to preserve other columns already present in `members_summaries.csv`.

It:

1. treats the current input roster as the source of truth for member list/order;
2. loads the existing output table when present;
3. right-joins existing output onto the current member roster by `member_code`;
4. keeps additional existing output columns;
5. adds `background` if absent;
6. updates only missing `background` rows unless forced;
7. autosaves CSV and Parquet;
8. writes final CSV and Parquet in place.

That preservation behavior is important because the table is now shared by other enrichment tasks.

## OpenAI/web-search behavior

Current defaults include:

```text
OPENAI_MODEL=gpt-4.1-mini
AUTOSAVE_INTERVAL=25
DELAY_BETWEEN_REQUESTS=0.25
MAX_RETRIES=5
```

For GPT-5-family models, minimal reasoning is upgraded to low when web search is used.

Returned text is cleaned to remove:

- parenthetical URL/link references;
- raw URLs;
- numeric citation markers such as `[1]`.

If OpenAI returns an empty result or errors, the call is retried with increasing delay until `MAX_RETRIES` is exhausted, then the run fails.

The code requests a maximum 200-word answer through the prompt, but there is no separate deterministic post-generation word-count enforcement in this dedicated summarizer.

## The table is now shared by the generic LLM runner

Current task files audited under the Reusable LLM Task Runner Framework also use:

```text
processed/members/members_summaries.csv
```

as both input and output.

Those tasks add fields such as:

- `absence_reason`;
- `in_government`;
- the example/template task's `conflicts_of_interest` field.

This means `members_summaries.csv` is no longer only a three-column member/background product in practice. It is a shared legacy enrichment table used by multiple independent LLM tasks.

### Important preservation difference

The dedicated background summarizer preserves arbitrary extra columns already present in the table.

The current generic `llm_table_runner.py`, by contrast, reconstructs `full_table` output from each task's configured `keep` columns plus that task's current output column. As documented on the current LLM framework page, same-key tasks can therefore drop unrelated enrichment columns if their `keep` lists are incomplete.

That risk belongs to the current generic runner, but it affects this historical table because the tasks write back to the same key.

## Current Oireachtas enrichment relationship

`extract/oireachtas/enrichment_member_summaries.py` has one fixed source:

```text
processed/members/members_summaries.csv
```

It does not generate new summaries.

### Enrichment trial outputs

```text
processed/oireachtas_unified/enrichment/text/member_summaries/member_summaries_trial.csv
processed/oireachtas_unified/enrichment/text/member_summaries/parquets/member_summaries_trial.parquet
```

The richer trial table adds fields including:

- `record_id`;
- `member_code`;
- `full_name`;
- normalized `summary_text`;
- source/model/review/run metadata.

Because generation provenance is not available in the legacy table, the enrichment layer records:

```text
summary_source=legacy_member_summaries_output
model_name=legacy_unknown
```

### Compatibility outputs

```text
processed/oireachtas_unified/compat/text/members_summaries_compat.csv
processed/oireachtas_unified/compat/text/parquets/members_summaries_compat.parquet
```

The compatibility builder begins from a copy of the legacy source table, normalizes:

```text
member_code
full_name
background
```

and then retains any additional source columns after those three core fields.

`member_summaries` is one of the six current Unified Oireachtas downstream contracts; the contract itself requires only `member_code`, `full_name`, and `background`.

## Current enrichment DQ

The Oireachtas summaries trial requires:

- output row count greater than zero;
- unique generated `record_id`;
- populated `member_code`;
- populated summary text on every selected row;
- expected row count relative to source/row limit.

Unlike member-photo enrichment, missing summary text is a **hard DQ failure**.

The workflow writes manifests, schema/DQ JSON, review samples/reports, pushes review output to `oireachtas-review-output`, and uploads artifacts.

## Lineage interpretation

Current checked-in lineage is:

```text
legacy/current raw members roster
    ↓
dedicated OpenAI background summarizer
    ↓
processed/members/members_summaries.csv
    ├─ shared generic LLM enrichment tasks may add/replace columns
    ↓
Unified Oireachtas member-summaries enrichment trial
    ├─ richer review/provenance-shaped table
    └─ members_summaries_compat.csv
         ↓
current downstream contract/consumers
```

Therefore:

- the archived system name represents the original dedicated summary-generation role;
- summary generation is still performed by retained legacy code;
- the Unified Oireachtas layer is an adapter/contract layer, not a replacement generator;
- the underlying table now has broader shared-enrichment use than the original archive description implied.

## Operational caution

Do not delete `processed/members/members_summaries.csv` solely because a Unified Oireachtas compatibility product exists. The current enrichment module reads that exact key.

When running current generic LLM tasks against this same table, review the task `keep` list before execution because current same-key full-table behavior can remove unrelated columns.

The dedicated background summarizer's column-preservation behavior should not be assumed to apply to the generic runner.

## Security and external-processing boundary

The dedicated summarizer sends member names/prompts to the OpenAI Responses API with web search and uses AWS/OpenAI credentials from GitHub Actions secrets.

The generic LLM tasks sharing the table have their own prompt-variable/data-processing boundaries documented on the current framework page.

No secret values belong in documentation.

## Known limitations

- The summary generator still reads the older raw members CSV rather than canonical Unified Oireachtas member data.
- The prompt requests <=200 words but the dedicated script does not deterministically enforce the final word count.
- The legacy table does not persist structured source citations, model-response IDs, prompt hashes, or generation timestamps per row.
- The enrichment layer therefore cannot reconstruct exact original model provenance and records `legacy_unknown`.
- The table is mutable and shared by independent LLM tasks.
- Legacy CSV/Parquet writes are direct/in-place rather than immutable candidate publication.
- Full retirement of the dedicated summary generator is not established.

## Verification record

- Last verified: `2026-08-07`
- Legacy implementation verified against: `process/members_background_summarizer.py`, `.github/workflows/members_background_summarizer.yml`.
- Current successor-layer implementation verified against: `extract/oireachtas/enrichment_member_summaries.py`, `.github/workflows/oireachtas_member_summaries_enrichment_trial.yml`.
- Shared-table behavior cross-checked against the current Reusable LLM Task Runner Framework audit and checked-in task configurations.
- Current classification: historical standalone summary-generation pipeline with retained executable source; current Oireachtas enrichment/compatibility code depends on its legacy table. Full replacement is **not established**.
