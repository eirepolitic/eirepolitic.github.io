---
title: Experimental and editorial content-generation workflows
summary: Status and lineage reference for retained manual editorial experiments in eirepolitic-data-pipeline, centered on the ridiculous-sentences scoring and prompt-comparison workflows.
section: notes
doc_type: reference
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - OpenAI Responses API
  - Amazon S3
  - GitHub Actions
  - pandas
  - PyArrow
order: 46
permalink: /projects/notes/experimental-editorial-content-workflows/
related:
  - /projects/notes/legacy-debate-member-enrichment-lineage/
  - /projects/pipelines/debate_issue_classifier/
  - /projects/repositories/eirepolitic-data-pipeline/
---

# Experimental and editorial content-generation workflows

## Purpose

This page records the current status of retained editorial/experimental content workflows in `eirepolitic-data-pipeline` that should not be presented as canonical political-data infrastructure.

The principal checked-in family is:

```text
process/ridiculous_sentences_weekly.py
process/ridiculous_sentences_experiments.py
prompts/ridiculous_sentences_variants.json
.github/workflows/ridiculous_sentences_weekly.yml
.github/workflows/ridiculous_sentences_experiments.yml
```

Both workflows are manually dispatched editorial experiments over legacy debate-speech data. Neither is scheduled and neither publishes social-media or website content.

## Current status classification

**Classification: retained manual editorial experiments.**

Evidence:

- both workflow files use `workflow_dispatch` only;
- neither has a cron schedule;
- both read legacy debate speech data from S3;
- both call the OpenAI Responses API to score or extract editorially notable quotations;
- both write derived CSV/Parquet outputs directly to legacy `processed/debates/` S3 paths;
- neither participates in the canonical Oireachtas table registry, immutable candidate publication, downstream-contract promotion gate, or Instagram publish queue;
- observed runs exist, but only as manual April 2026 executions.

Current source therefore establishes executable retained experiments, not normal production intent.

## Weekly ridiculous-sentences workflow

Workflow:

```text
.github/workflows/ridiculous_sentences_weekly.yml
```

Implementation:

```text
process/ridiculous_sentences_weekly.py
```

Workflow name:

**Ridiculous Sentences Weekly (Manual)**

Despite the word “Weekly” in the name, the current workflow has no schedule. It is manual-only.

### Current inputs

Manual inputs include:

- `run_mode` — `year` or `previous_week`;
- `run_year` — default `2026`;
- `run_week_id` — exact test override, currently default `202601`;
- `as_of_date`;
- `test_rows`;
- `openai_model` — default `gpt-4.1-mini`;
- `batch_size` — default `20`;
- `top_n_per_week` — default `10`.

Runtime uses Python 3.11, a 240-minute timeout, concurrency group `ridiculous-sentences-weekly`, AWS credentials, and `OPENAI_API_KEY`.

## Weekly source and outputs

Default input:

```text
raw/debates/debate_speeches_extracted.csv
```

Default outputs:

```text
processed/debates/ridiculous_sentences_weekly.csv
processed/debates/parquets/ridiculous_sentences_weekly.parquet
```

The input belongs to the retained legacy debate-extraction lineage, not the canonical `silver_speeches` product.

The output schema is:

```text
week_id
sentence
speaker_name
score
```

## Weekly selection logic

The weekly implementation:

1. requires `Debate Date`, `Speaker Name`, and `Speech Text`;
2. splits speech text into sentence-like candidates;
3. rejects blank/nonalphabetic candidates and candidates over the configured word limit;
4. deduplicates by week, speaker, and normalized sentence;
5. selects an exact week, a year, or the previous completed week;
6. optionally truncates the work set using `TEST_ROWS`;
7. sends candidates to OpenAI in batches;
8. requires one numeric score per candidate ID;
9. clamps model scores to the 1–100 range;
10. selects the configured top N per week;
11. merges those rows into the existing output, replacing the target week/year scope;
12. writes CSV and Parquet directly to S3.

The editorial scoring prompt asks the model to rank sentences according to how unusually comic, absurd, harsh, insulting, or otherwise striking they sound in parliamentary context.

That score is a model/editorial judgment. It is not a factual political-data field or canonical classification.

## Weekly retry and overwrite behavior

OpenAI calls retry up to the configured `MAX_RETRIES`, default `5`, using increasing delay.

Invalid JSON/score payloads also trigger prompt repair/retry.

The output merge preserves weeks outside the selected target scope but replaces:

- the exact `RUN_WEEK_ID`, when set;
- the selected year for a full-year run;
- the selected previous week for previous-week mode.

CSV and Parquet writes are sequential, not atomic.

## Weekly observed runtime

Workflow history currently includes two manual runs:

- `24096027584`, 2026-04-07: success;
- `24101358197`, 2026-04-07: success.

These prove historical execution of the workflow family. They do not establish recurring weekly production operation because the current workflow has no schedule.

## Prompt-comparison experiments

Workflow:

```text
.github/workflows/ridiculous_sentences_experiments.yml
```

Implementation:

```text
process/ridiculous_sentences_experiments.py
```

Prompt configuration:

```text
prompts/ridiculous_sentences_variants.json
```

Workflow name:

**Ridiculous Sentences Experiments (Manual)**

It is also manual-only.

### Experimental purpose

The experiments workflow compares multiple editorial prompt strategies for identifying notable debate quotations.

Current configured approaches are:

```text
sentence_score
extract_then_score
```

Prompt families include variants focused on:

- strict filtering;
- absurd/comic wording;
- unusually harsh or insulting wording;
- memorable/quotable wording;
- mixed strict criteria.

The prompt-variant file contains multiple versions so their selection behavior can be compared rather than treating one prompt as an authoritative model definition.

## Experiment source and outputs

Default source:

```text
raw/debates/debate_speeches_extracted.csv
```

Default output products:

```text
processed/debates/ridiculous_sentences_experiments.csv
processed/debates/parquets/ridiculous_sentences_experiments.parquet
processed/debates/ridiculous_sentences_experiments_summary.csv
processed/debates/parquets/ridiculous_sentences_experiments_summary.parquet
```

The experiment is scoped to configured week IDs, currently defaulting in Python to `202602,202603`.

The manual workflow defaults to the `extract_then_score` approach and six named extraction variants.

## Two experimental approaches

### `sentence_score`

The script deterministically splits speeches into sentence candidates, then asks the model to score those candidates.

### `extract_then_score`

The model first extracts a small set of direct quotations from each speech that fit a configured editorial prompt family, then a second scoring stage ranks the extracted quotes.

Extracted quotes are accepted only when they are short enough and can be matched as contiguous normalized text inside the original speech. This reduces, but does not eliminate, model-selection risk.

## Experiment outputs

Top-row output includes fields such as:

- `variant_id`;
- `prompt_family`;
- `approach`;
- `week_id`;
- `debate_date`;
- `speaker_name`;
- `quote`;
- `score`;
- `speech_id`;
- `section_name`;
- `word_count`;
- `week_rank`.

The summary output reports per variant/week counts and score summaries.

These are evaluation artifacts for comparing editorial prompt behavior, not canonical datasets.

## Experiment retry behavior

The experiment code has more aggressive recovery than the simple weekly scorer:

- OpenAI API requests retry;
- extraction JSON can be repaired/retried;
- partial score responses are accepted when they contain some requested candidate IDs;
- missing score subsets are retried;
- failing score batches can be recursively split into smaller chunks until all candidate IDs resolve or a single-candidate failure becomes fatal.

This improves experimental completion but does not make the resulting editorial scores objectively correct.

## Experiment observed runtime

Current workflow history includes:

- `24171819992`, 2026-04-09: failure;
- `24275150361`, 2026-04-11: success.

The successful later run shows the experiments workflow was exercised after the initial failure. Exact root cause of the failed run is not required for current status classification and is not inferred here.

## Relationship to current canonical Oireachtas platform

These editorial workflows are not part of the Unified Oireachtas canonical product catalogue.

They currently depend on:

```text
raw/debates/debate_speeches_extracted.csv
```

from the retained legacy debate extraction path.

They do not currently read canonical `silver_speeches`, do not write `processed/oireachtas_unified/...`, and do not participate in candidate validation/promotion.

Therefore they should remain outside the canonical data-product documentation unless a future implementation intentionally migrates them.

## Relationship to Instagram/content systems

The inspected workflows create S3 tables only.

They do **not**:

- render Instagram images;
- generate captions through the current Instagram copy-pack path;
- create the review-gated Instagram publish queue;
- publish or schedule social content;
- approve editorial selections.

Any future use of these outputs in content should have an explicit downstream review boundary rather than treating high model scores as publication approval.

## External processing and cost boundary

Both workflows send parliamentary text or derived quotations to the OpenAI Responses API.

The weekly scorer generally makes one scoring request per configured batch, with retries on API/format failure.

The experiments workflow can make substantially more calls because `extract_then_score` may perform extraction requests per speech plus scoring requests per candidate batch, with repair/split retries.

Cost therefore depends on:

- number of candidate speeches/sentences;
- selected prompt variants;
- approach type;
- batch size;
- retries/fallback splits;
- active OpenAI model/pricing.

The checked-in workflows expose test/scope limits and are manual-only, which are the main current controls against accidental full-scale experimental runs.

## Security boundary

Current workflows use GitHub Actions secrets for:

- AWS access key;
- AWS secret key;
- AWS region;
- OpenAI API key.

The scripts then read/write S3 objects directly and send selected text to OpenAI.

No secret values should be documented or written into generated tables.

## Editorial limitations

- Scores are subjective model judgments, not factual measurements.
- Prompt wording materially changes selection/ranking behavior.
- The term used in the workflow/product name is editorial framing, not a neutral analytical taxonomy.
- Extracted quotations can lose surrounding speech/debate context even when copied verbatim.
- Speaker identity and quote text come from legacy extracted debate data, so upstream extraction quality matters.
- The workflows contain no human approval state in the generated S3 tables.
- There is no canonical schema/version/manifest or immutable candidate publication.
- CSV and Parquet output writes are direct and sequential.
- Observed successful runs are from April 2026; no scheduled/current recurring execution is established.

## Status rule

Until current source gains an explicit scheduled/production integration or the system owner establishes active operational intent, classify this family as:

> **retained manual editorial experiments**

Do not promote it to a P1 current production system based solely on file presence, workflow `active` registry state, or historical successful manual runs.

## Safe operating guidance

1. Use small week/speech/test scopes when evaluating prompt changes.
2. Review the exact prompt variant before running because variants intentionally encode different editorial preferences.
3. Treat generated scores/rankings as review candidates, not publication approval.
4. Verify quotations against the source speech and surrounding context before external use.
5. Do not infer political misconduct, truthfulness, or factual significance from an editorial score.
6. Keep these outputs separate from canonical Oireachtas datasets unless an explicit architecture decision migrates them.

## Verification record

- Last verified: `2026-08-07`
- Current source verified against: `process/ridiculous_sentences_weekly.py`; `process/ridiculous_sentences_experiments.py`; `prompts/ridiculous_sentences_variants.json`; `.github/workflows/ridiculous_sentences_weekly.yml`; `.github/workflows/ridiculous_sentences_experiments.yml`; complete current workflow tree.
- Observed runtime evidence: weekly runs `24096027584`, `24101358197`; experiment runs `24171819992`, `24275150361`.
- Current classification: retained manual editorial experiment family; executable and historically exercised, but not scheduled, canonical, or integrated with a publishing/approval path.
