---
title: AutoDoc LLM section-fact extraction
summary: Current verified AutoDoc extraction stage that derives one facts-only text field per documentation H2 section from the full enriched configuration and persists the result as a two-column CSV contract.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 36
permalink: /projects/systems/autodoc-section-fact-extraction/
tags:
  - autodoc
  - openai
  - extraction
  - csv
  - pipeline
---

# AutoDoc LLM section-fact extraction

## Summary

`process/section_extract.py` is AutoDoc's persisted section-fact extraction stage. It loads the base and enriched project configuration, derives the document's section list from the merged Markdown templates, calls OpenAI once per H2 section, and overwrites `doc_configs/<project>/summaries/<doc_key>.csv` with one row per section.

The current model is hard-coded in Python as `gpt-4.1-mini` with `temperature=0`. Each call receives the section title and the **full enriched JSON without truncation**. Although the function accepts the section-template body as an argument and the source docstring says it is supplied to the model, the current prompt does not interpolate that body. That discrepancy is documented as verified implementation drift rather than silently repeating the docstring.

## Source of Truth

```text
process/section_extract.py
.github/workflows/section_extract.yml
.github/workflows/autodoc_pipeline.yml
templates/base.md
templates/types/*.md
doc_configs/<project>/summaries/*.csv
```

Current implementation SHA:

```text
process/section_extract.py
fe2c7adc527d1cb8c6b6a61c293bb86231538a2b
```

Verified persisted example:

```text
doc_configs/autodoc/summaries/autodoc_creation_pipeline.csv
```

## Entry Point

The script is environment-driven rather than CLI-argument-driven:

```text
PROJECT=<project> DOC_KEY=<doc_key> python process/section_extract.py
```

Required environment:

```text
PROJECT
DOC_KEY
OPENAI_API_KEY
```

`PROJECT` and `DOC_KEY` are explicitly checked by the script. `OPENAI_API_KEY` is consumed by `OpenAI()` through the OpenAI client environment convention.

## Required Inputs

The stage requires both:

```text
doc_configs/<project>/<doc_key>.json
doc_configs/<project>/<doc_key>.enriched.json
```

`load_config()` and `load_enriched()` raise immediately when the corresponding file is absent.

The base config must contain a non-empty:

```text
type
```

because that value controls type-template selection.

## Template Merge

`merge_templates(doc_type)` requires:

```text
templates/base.md
```

and appends:

```text
templates/types/<type>.md
```

when that file exists.

If the type-specific file does not exist, extraction proceeds with `templates/base.md` only. Missing `templates/base.md` is fatal.

The merge is simple text concatenation:

```text
base + "\n\n" + type_text
```

No Jinja rendering or placeholder substitution occurs in this extraction-stage merge.

## Section Discovery

`split_sections()` identifies headings matching exactly:

```regex
^## (.+)$
```

with multiline matching.

Each H2 produces:

```text
(section_title, section_body)
```

The body extends from the end of that H2 heading to the next H2 or end of template.

If no H2 sections are found, the stage fails with:

```text
No sections found. Template must contain '## ' headings.
```

Current `templates/base.md` supplies these base sections:

```text
Overview
Assets
Inputs and Outputs
How it works
How to run
Data quality and validation
Maintenance
```

Type templates can append more sections.

## Verified Prompt Contract

For each section, `call_llm()` currently constructs a prompt containing:

1. the section title;
2. a label stating that the model is extracting factual information for that section;
3. `json.dumps(enriched_json, indent=2)` for the full enriched configuration;
4. rules to identify only relevant factual information, not invent, not summarize generally, and return only a bullet list with one fact per bullet.

### Important source/code discrepancy

The function signature is:

```text
call_llm(client, section_title, section_text, enriched_json)
```

and `main()` passes the discovered section body as `section_text`.

However, current prompt construction does not reference `section_text` at all. Therefore the actual model input is the section title plus full enriched JSON and fixed rules—not the section-template body.

Historical/generated descriptions that say the current extraction prompt includes the section-template text are not authoritative over the executable source.

## OpenAI Configuration

Current Python constant:

```text
MODEL = "gpt-4.1-mini"
```

Current request:

```text
client.responses.create(
    model="gpt-4.1-mini",
    input=<prompt>,
    temperature=0,
)
```

The stage returns:

```text
(resp.output_text or "").strip()
```

There is no separate environment model override in `section_extract.py` or `section_extract.yml`.

## Full-Enriched-JSON Boundary

The full enriched dictionary is serialized for **every section call**, with no source-code truncation step.

That can include:

- project context;
- all asset base fields;
- resolved text content;
- base64-encoded binary content;
- `resolved_content_lines`;
- source/provenance metadata;
- resolution errors;
- top-level `_enrichment` metadata.

This is both a privacy/trust boundary and a cost/token-volume boundary. This documentation records current behavior; it does not approve changing the model, prompt, truncation, or filtering policy.

## Rate-Limit Retry Behavior

Only exceptions identified as rate-limit errors are retried.

`is_rate_limit_error()` treats an exception string as rate-limited when it contains any of:

```text
rate limit
rate_limit
429
```

Maximum attempts:

```text
8
```

### Server-indicated delay

`parse_retry_after_seconds()` recognizes text matching:

```text
try again in <number>s
```

When found, wait time is:

```text
parsed seconds + random 0.5..1.5 second jitter
```

### Exponential fallback

Otherwise wait time is:

```text
min(60, 2 ** attempt) + random 0.5..1.5 second jitter
```

After eight persistent rate-limit attempts, the stage raises a `RuntimeError` naming the affected section.

Any non-rate-limit OpenAI exception is re-raised immediately rather than retried by this function.

## Inter-Section Throttling

After a successful section call, and before the next section, the script sleeps:

```text
6 seconds
```

There is no six-second sleep after the final section.

The source comment states this is intended to reduce token-per-minute spikes.

## CSV Contract

Output path:

```text
doc_configs/<project>/summaries/<doc_key>.csv
```

The directory is created with parents when necessary.

The file is opened in write mode and therefore overwritten on each successful run.

Header is exactly:

```text
section_title,extracted_facts
```

Logical row contract:

| Column | Meaning |
| --- | --- |
| `section_title` | H2 title derived from the merged base/type template |
| `extracted_facts` | Raw stripped `output_text` returned by the extraction model for that section |

Python `csv.writer` handles quoting/newlines. Persisted examples therefore contain quoted multi-line `extracted_facts` fields when the model returns multiple bullet lines.

One row is appended for every discovered section, in template order.

## Output Validation Boundary

The prompt requests a bullet list, but current code does not parse or validate bullet syntax.

It also does not validate:

- minimum number of facts;
- factual correctness;
- duplication;
- whether every line is a bullet;
- whether the output is empty.

An empty `output_text` becomes an empty string and is still added to the row list. The CSV is written after all section calls complete.

Rendering is responsible for consuming this persisted text contract; extraction does not create Markdown sections directly.

## Failure Atomicity

Rows are accumulated in memory and `write_csv()` is called only after all sections complete.

Therefore, if a required file/template/config error or an unrecovered OpenAI exception occurs before the end of the section loop, the current run does not write a new partial CSV through `write_csv()`.

A pre-existing CSV can remain on disk from an earlier run because the script does not delete it before processing. Operators must not assume an existing summary CSV was produced by the latest failed attempt.

## Automatic Pipeline Integration

The automatic workflow invokes:

```text
PROJECT=<project> DOC_KEY=<doc_key> python process/section_extract.py
```

immediately after enrichment and before rendering.

Automatic workflow environment includes:

```text
OPENAI_API_KEY
PROJECT
DOC_KEY
```

A non-zero extraction command stops the automatic processing shell because it uses `set -euo pipefail`.

The automatic workflow later stages changed summary CSVs along with other generated artifacts when the full processing sequence reaches the commit step.

## Manual Workflow

Workflow:

```text
.github/workflows/section_extract.yml
Extract Section Facts
```

Trigger:

```text
workflow_dispatch
```

Required inputs:

```text
project
doc_key
```

Permissions:

```text
contents: write
```

Concurrency:

```text
extract-section-facts
cancel-in-progress: false
```

Runtime:

```text
ubuntu-latest
Python 3.11
pip install openai
```

Secret name:

```text
OPENAI_API_KEY
```

After extraction, the workflow stages only:

```text
doc_configs/<project>/summaries/<doc_key>.csv
```

If unchanged, it exits without a commit. Otherwise it commits and pushes directly to `autodoc`.

## Trust, Privacy, and Cost Boundaries

### Enriched repository content -> OpenAI

Every section call serializes the full enriched config. Anything persisted during enrichment can therefore be included repeatedly in OpenAI requests.

Never put tokens, credentials, private keys, signed secret URLs, personal data, or confidential source material into AutoDoc configs/assets unless an explicitly approved data-handling design says it is appropriate.

### Repeated full-context calls

The number of OpenAI calls equals the number of merged-template H2 sections. Full enriched JSON is sent independently for every section. More sections or larger enriched assets therefore increase request volume.

Changing this behavior, model, or prompt can affect cost/quality and is outside routine documentation work.

### CSV persistence

Model output is committed as repository content. Extracted facts can therefore become durable source for later rendering and repository history.

## Failure Modes and Recovery

### `PROJECT` / `DOC_KEY` missing

Stage fails before loading files. Supply the correct workflow inputs/environment.

### Base config missing

Fix the path/project/doc key. Do not fabricate a CSV manually as the first recovery step.

### Enriched config missing

Run/fix enrichment first. Extraction is a downstream stage.

### Config `type` missing

Repair the base configuration contract; rerun enrichment if its output is now stale, then rerun extraction.

### Base template missing or no H2 headings

Treat as template-system failure. Do not bypass template discovery by inventing CSV section names.

### Rate limit

The script retries up to eight attempts with parsed delay or exponential fallback plus jitter. If it still fails, preserve the previous artifacts, address the API/capacity condition, and rerun the extraction stage.

### Other OpenAI error

The exception is immediate. Inspect non-secret error details and correct API/input/configuration problems; do not expose `OPENAI_API_KEY`.

### Extraction run fails but old CSV exists

Treat the old CSV as previous-run state, not proof of current success. Confirm workflow/run history before rendering/recovery decisions.

## Known Limitations

- Section-template body is passed into `call_llm()` but unused in the current prompt.
- Full enriched JSON is sent without truncation for every section.
- Bullet-list format is requested but not programmatically validated.
- Empty model output can be persisted as an empty CSV field if the call itself succeeds.
- Retry handling is specific to rate-limit-like errors; other transient failures are not retried here.
- The model is hard-coded to `gpt-4.1-mini` rather than configured through the workflow environment.

## Next Safe Development Action

Publish this extraction/CSV-contract component through validation, merge, and matching Pages success. Then document the template and Markdown rendering stage on a fresh branch from current `main`.

Do not change model, prompt/context selection, retry policy, throttle timing, or data sent to OpenAI without explicit cost/architecture/security approval.

## Related Documents

- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc/main` `process/section_extract.py` SHA `fe2c7adc527d1cb8c6b6a61c293bb86231538a2b`; current `section_extract.yml`, `autodoc_pipeline.yml`, `templates/base.md`, type-template set, and persisted `doc_configs/autodoc/summaries/autodoc_creation_pipeline.csv`.
- Verified by: High Director
- Verification scope: required files/env, template merge/section discovery, actual prompt content, OpenAI model/API configuration, retries/throttling, CSV schema/write semantics, output validation boundary, automatic/manual workflow behavior, trust/privacy/cost boundary, and failures.
- Not verified: current OpenAI service limits, account billing/quotas, or factual accuracy of historical model outputs.
