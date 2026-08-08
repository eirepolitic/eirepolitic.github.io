---
title: Debate Issue Classifier
summary: Historical Dáil speech-classification pipeline record retained for lineage; the newer Unified Oireachtas enrichment layer consumes its classified output rather than replacing the OpenAI classification function.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - OpenAI API
  - Amazon S3
  - Amazon Athena
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-07
last_verified: 2026-08-07
archived_date: 2026-08-05
archive_reason: Historical standalone pipeline documentation retained for lineage; current Unified Oireachtas speech-issue enrichment still depends on the legacy classified debate output.
permalink: /projects/pipelines/debate_issue_classifier/
related:
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/systems/member-profile-metrics-builder/
  - /projects/notes/oireachtas-write-policies-downstream-contracts/
---

# Debate Issue Classifier

## Current status

This page is an **archive/lineage record** for the older debate extraction and OpenAI classification path.

The key current-source finding is that the newer Unified Oireachtas speech-issue enrichment code does **not** perform classification. It reads the legacy classified CSV and reshapes/validates those existing labels.

Current source therefore does not support describing the old classifier as fully replaced.

Retained legacy implementation:

```text
extract/monthly_extract.py
extract/debates_xml_to_csv_s3.py
process/speech_issue_classifier.py
.github/workflows/monthly_extract.yml
.github/workflows/speech_issue_classifier.yml
```

Current successor-layer implementation:

```text
extract/oireachtas/enrichment_speech_issue_labels.py
.github/workflows/oireachtas_enrichment_speech_issue_labels_trial.yml
```

## Historical extraction path that remains configured

`.github/workflows/monthly_extract.yml` remains present on current `main` and is still configured with this schedule:

```text
15 9 1 * *
```

That is 09:15 UTC on the first day of each month.

The workflow runs:

1. `extract/monthly_extract.py` to fetch/store debate XML;
2. `extract/debates_xml_to_csv_s3.py` to produce the speech CSV;
3. `extract/monthly_members_extract.py` for the older member extract.

This schedule is checked-in current configuration. It does not make the old extraction path canonical where the Unified Oireachtas platform has a newer equivalent; current Oireachtas source/configuration remains the stronger source of truth for canonical data.

## Retained legacy classifier

`process/speech_issue_classifier.py` currently defaults to:

```text
INPUT_KEY=raw/debates/debate_speeches_extracted.csv
OUTPUT_KEY=processed/debates/debate_speeches_classified.csv
PARQUET_KEY=processed/debates/parquets/debate_speeches_classified.parquet
```

The manual workflow `.github/workflows/speech_issue_classifier.yml` explicitly runs the classifier with:

```text
OPENAI_MODEL=gpt-4.1-mini
OPENAI_REASONING_EFFORT=low
OPENAI_VERBOSITY=low
```

and exposes `test_rows`, default `50`.

The script itself has a fallback default model of `gpt-4o-mini` when not overridden. The workflow override is therefore the relevant checked-in configuration for that manual workflow.

### Classification categories

The retained classifier requires exactly one label from a fixed 25-value set consisting of 24 political issue categories plus `NONE`.

Examples include:

- `Macroeconomics`;
- `Health`;
- `Agriculture`;
- `Education`;
- `Environment`;
- `Housing and Community Development`;
- `International Affairs and Foreign Aid`;
- `Government Operations`;
- `Other/Miscellaneous`;
- `Domestic Terrorism`;
- `NONE`.

The complete category list is defined in current `process/speech_issue_classifier.py` and mirrored by the newer enrichment validator.

## Classification behavior

The retained classifier:

1. reads the legacy extracted speech CSV;
2. creates deterministic `speech_id` values when missing using debate date, speaker, speech order, and speech text;
3. loads an existing classified output if present;
4. reuses nonmissing classifications by `speech_id`;
5. processes only missing labels, optionally limited by `TEST_ROWS`;
6. assigns `NONE` to blank speeches or speeches under 20 words;
7. calls the OpenAI Responses API for eligible rows;
8. validates the response against the fixed category list;
9. retries/refines invalid labels up to `MAX_ITERATIONS`, currently default `5`;
10. falls back to `NONE` if no valid category is obtained;
11. autosaves CSV and Parquet after the configured processed-row interval;
12. writes final CSV and Parquet even if no new rows required classification.

API-call failures use incremental retry delay before becoming a hard runtime failure.

## Output mutation behavior

The classifier reconstructs the result from the current extracted input while reusing existing classifications by `speech_id`, then overwrites:

```text
processed/debates/debate_speeches_classified.csv
```

and a Parquet representation.

The workflow then separately runs `process/debate_speeches_csv_to_parquet.py`, which writes the expected classified Parquet object with normalized column names.

The classifier is not candidate-batch aware and writes legacy S3 locations directly.

## Current Oireachtas enrichment relationship

`extract/oireachtas/enrichment_speech_issue_labels.py` explicitly states:

- it does **not** call OpenAI;
- it does **not** overwrite the legacy classified debate output;
- it reshapes the existing classified CSV into a unified enrichment table and a legacy-compatible adapter.

Its source is:

```text
processed/debates/debate_speeches_classified.csv
```

### Enrichment trial outputs

```text
processed/oireachtas_unified/enrichment/speech_issue_labels/speech_issue_labels_2025_trial.csv
processed/oireachtas_unified/enrichment/speech_issue_labels/parquets/speech_issue_labels_2025_trial.parquet
```

The richer trial table adds fields such as:

- `record_id`;
- `speech_id`;
- `member_code`;
- `speaker_name`;
- `debate_date`;
- `speech_order`;
- source speech-text hash;
- normalized `issue_label`;
- classification/review/source/run metadata.

The current source labels the model as `legacy_unknown` because the enrichment layer is importing an existing classification rather than producing a new one itself.

### Compatibility outputs

```text
processed/oireachtas_unified/compat/debates/debate_speeches_classified_compat.csv
processed/oireachtas_unified/compat/debates/parquets/debate_speeches_classified_compat.parquet
```

The compatibility output preserves the legacy classified rows while ensuring required fields such as `speech_id`, `PoliticalIssues`, `Speaker Name`, and `Debate Date` are present.

`debate_issue_labels` is one of the current six Unified Oireachtas downstream contracts, and the member-profile metrics builder consumes the compatibility dataset for speech/issue metrics.

## Current enrichment validation

The enrichment trial validates:

- nonzero row count;
- unique generated `record_id`;
- populated `speech_id`;
- all nonblank issue labels belong to the approved category set;
- row count matches the expected source/row-limit count.

It writes trial/compat CSV and Parquet, manifests, schema/DQ JSON, review samples, Markdown reports, and review-branch/artifact evidence.

The manual trial workflow explicitly reports that it does not call OpenAI and does not overwrite `processed/debates/debate_speeches_classified.csv`.

## Lineage interpretation

The checked-in relationship is currently:

```text
legacy monthly debate XML extraction
    ↓
raw/debates/debate_speeches_extracted.csv
    ↓
legacy/manual OpenAI speech classifier
    ↓
processed/debates/debate_speeches_classified.csv
    ↓
Unified Oireachtas speech-issue enrichment trial
    ├─ richer enrichment/review table
    └─ downstream compatibility dataset
         ↓
member-profile metrics and other consumers
```

Therefore:

- the old page remains appropriate as an archive/lineage record;
- the legacy classifier is still the checked-in producer of issue labels for this lineage;
- the new enrichment layer validates/adapts labels but does not replace classification;
- full classifier retirement is **not established** by current source.

## Operational caution

Do not delete or stop producing the legacy classified CSV solely because a Unified Oireachtas compatibility path exists. The current enrichment module reads that exact legacy key.

Likewise, do not treat `monthly_extract.yml` as the canonical Oireachtas ingestion architecture simply because it remains scheduled. The canonical Unified Oireachtas platform is separately implemented/configured and should remain the source of truth for current canonical data products.

This creates a transitional dependency: newer enrichment/consumer code still relies on one legacy classified output while canonical ingestion has moved elsewhere.

## Security and cost boundary

The retained classifier sends speech text to the OpenAI API and uses `OPENAI_API_KEY` plus AWS credentials from GitHub Actions secrets.

A full classification run can make one or more model calls per previously unclassified eligible speech because invalid labels trigger refinement iterations. `test_rows` is the current manual control for limiting the work set.

No secret values belong in documentation.

## Known limitations

- Classification remains tied to the legacy extracted speech CSV rather than directly classifying canonical `silver_speeches`.
- The newer enrichment trial imports existing labels and records model provenance only as `legacy_unknown`.
- `NONE` conflates short/blank speech handling and valid model/category outcomes at the legacy classifier level.
- The retained classifier overwrites legacy CSV/Parquet paths directly rather than using immutable candidate publication.
- The monthly legacy extraction remains scheduled in source even though it is not the canonical Oireachtas architecture.
- Current workflow/file presence does not prove long-term operational intent; full retirement/cutover has not been established.

## Verification record

- Last verified: `2026-08-07`
- Legacy implementation verified against: `process/speech_issue_classifier.py`, `.github/workflows/speech_issue_classifier.yml`, `.github/workflows/monthly_extract.yml` and the retained extraction path named there.
- Current successor-layer implementation verified against: `extract/oireachtas/enrichment_speech_issue_labels.py`, `.github/workflows/oireachtas_enrichment_speech_issue_labels_trial.yml`.
- Current classification: archived standalone pipeline documentation with retained executable/scheduled upstream source; its classified CSV remains the explicit input to the newer Oireachtas enrichment/compatibility layer. Full replacement is **not established**.
