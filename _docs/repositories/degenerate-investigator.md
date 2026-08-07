---
title: degenerate_investigator Repository and UFC Analytics Architecture
doc_type: repository
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Repository and UFC Analytics Architecture

## Purpose

`degenerate_investigator` is a Python-based UFC analytics, data-engineering, machine-learning, scoring, and report-generation repository. It gathers current and historical UFC data, enriches selected matchups with market and recent-news context, engineers model features, builds a historical training dataset, trains a UFC winner model, scores a target event, generates analytical reports, stores pipeline products in Amazon S3, and can publish the latest Markdown report back into the repository.

The repository is analytical. It does **not** implement staking logic, bankroll management, bookmaker selection, or bookmaker-targeted betting recommendations. Odds are used as an analytical input and model-vs-market comparison signal.

## Repository maturity

The repository contains executable Python pipelines and GitHub Actions workflows rather than a single deployed application or service. The implementation is stage-oriented and S3-backed. The inspected workflows are manually dispatched and do not form an automatically chained end-to-end orchestrator.

A capable maintainer should treat the repository source and persisted S3 contracts as the implementation source of truth. Live AWS/IAM deployment state is not fully provable from repository source alone.

## Top-level implementation map

| Area | Source | Responsibility |
| --- | --- | --- |
| Shared I/O | `common/io_helpers.py` | S3 client creation, object existence checks, CSV reads, text/byte writes, and paired CSV/Parquet publication. |
| Current UFC ingestion | `extract/ufc_event_card.py`, `extract/ufc_fighter_profiles.py` | Pull a current UFC event card and fighter-profile data from UFC Stats. |
| Historical UFC ingestion | `extract/ufc_historical_fights.py`, `extract/ufc_historical_fighter_profiles.py` | Build historical fight and fighter-profile inputs from UFC Stats. |
| Current odds | `extract/odds_current_mma.py` | Pull current MMA head-to-head odds from The Odds API and normalize price representations. |
| Fighter news | `extract/fighter_recent_news.py` | Use the OpenAI Responses API with web search to enrich fighters with recent-news context. |
| Matchup features | `process/ufc_feature_builder.py` | Convert event, fighter, odds, and enrichment inputs into matchup-level analytical features. |
| Historical training dataset | `process/build_historical_training_dataset.py` | Convert historical fights/profiles into supervised training rows and targets. |
| Model training | `process/train_ufc_winner_model.py` | Train and persist the UFC winner model plus metrics and metadata. |
| Target-event scoring | `process/score_target_event.py` | Score event matchups using a trained model when available and an explicit heuristic fallback otherwise. |
| Report generation | `process/generate_event_report.py` | Build tabular and Markdown fight-analysis outputs from scored matchups and enrichment. |
| Report export | `process/export_s3_report_to_repo.py` | Copy the latest Markdown report from S3 into the repository working tree for publication. |
| Automation | `.github/workflows/*.yml` | Manually dispatch the individual pipeline stages and report export. |
| Published report | `reports/latest_fight_report.md` | Repository copy of the latest exported fight-analysis Markdown report. |

## End-to-end architecture

The system is organized as independently runnable stages connected by S3 objects:

1. **Current-event ingestion** obtains the UFC event card and fighter profiles.
2. **Historical ingestion** obtains completed fight history and historical fighter profiles.
3. **External enrichment** obtains current MMA odds and recent fighter-news context.
4. **Feature engineering** builds matchup-level numerical and contextual features for the selected event.
5. **Historical dataset construction** creates model-training rows and a binary winner target from completed fights.
6. **Model training** fits a winner classifier and persists the trained artifact and evaluation metadata.
7. **Target-event scoring** loads engineered features and, when available and compatible, the trained model to produce matchup probabilities/picks and comparison fields.
8. **Report generation** combines scored matchup data and news context into machine-readable outputs and a human-readable Markdown report.
9. **Publication** optionally copies the S3 Markdown report into `reports/latest_fight_report.md` and commits it through a separate write-enabled GitHub Actions workflow.

There is no verified workflow that automatically invokes all nine stages in sequence. Operators select workflows and inputs explicitly and must respect the S3 dependencies between them.

## Data sources and APIs

### UFC Stats

The UFC ingestion scripts use UFC Stats web pages as the source for current events, fight history, and fighter profiles. The extractors attempt both `http` and `https` forms where needed and fail when expected event rows cannot be located rather than silently manufacturing results.

Relevant source paths:

- `extract/ufc_event_card.py`;
- `extract/ufc_fighter_profiles.py`;
- `extract/ufc_historical_fights.py`;
- `extract/ufc_historical_fighter_profiles.py`.

Historical fight ingestion rebuilds the aggregate historical outputs for the selected completed-event window; it is not documented as an incremental append-only event store.

### The Odds API

`extract/odds_current_mma.py` uses The Odds API for current MMA head-to-head prices. The source requires `ODDS_API_KEY`. The inspected implementation defaults to regions `us,eu,uk` and market `h2h`, and normalizes American and decimal price representations for analytical use.

Odds data is not a staking instruction. Downstream use is limited to matchup context and model-vs-market comparison.

### OpenAI Responses API and web search

`extract/fighter_recent_news.py` uses `OPENAI_API_KEY` and the OpenAI Responses API with web search. The inspected implementation defaults to model `gpt-4.1-mini`. It attempts structured JSON extraction and, when the initial response is not parseable, makes a second no-search repair request. Per-fighter parse failures are persisted as error data so a single malformed response does not necessarily abort the entire batch.

No separate `NEWS_API_KEY`-driven integration was verified in the inspected source.

## Feature and training architecture

### Matchup feature engineering

`process/ufc_feature_builder.py` is the current-event feature stage. It combines event/fighter information and available enrichment into matchup-level rows. Feature definitions and exact transformations belong to the dedicated P1-29 page; this repository page establishes that this stage is the feature-contract boundary used by scoring.

### Historical target construction

`process/build_historical_training_dataset.py` converts completed fight history and historical fighter profiles into supervised rows. The target represents the observed winner from historical fight results. Exact row orientation, feature definitions, filtering, and target construction belong to P1-30 and must be maintained alongside the code because changes can invalidate model compatibility.

## Model source of truth

The trained model and fallback paths are separate behaviors and must not be conflated.

### Trained estimator

`process/train_ufc_winner_model.py` trains a scikit-learn pipeline using median imputation and, for normal multi-class training data, a `RandomForestClassifier` with 300 trees. The persisted training metadata records the model type, feature columns, evaluation metrics, and Random Forest feature importance when applicable.

### Single-class training fallback

If the available training target contains only one class, the training script uses `DummyClassifier(strategy="prior")` rather than fitting the Random Forest. This is a training-time fallback estimator and should be identified by the persisted `model_type` metadata.

### Scoring heuristic fallback

`process/score_target_event.py` also contains an explicit heuristic fallback for event scoring when the trained model path cannot be used. This is **not** the trained model and its outputs must never be presented as Random Forest predictions.

Documentation, troubleshooting, and report interpretation must identify which path produced a prediction whenever that distinction matters.

## Model artifacts and metrics

The training stage persists a model artifact plus machine-readable training metadata. The metadata is the authoritative place to determine:

- estimator/model type;
- feature-column contract;
- recorded evaluation metrics;
- feature importance where supported.

Do not infer deployed model quality from report prose alone. A maintainer troubleshooting inference should first verify that the model artifact and its metadata correspond to the feature dataset being scored.

## Inference and report outputs

`process/score_target_event.py` writes scored matchup products for the selected target event. `process/generate_event_report.py` then:

- deduplicates matchup rows as needed;
- merges recent-news context;
- generates analytical fight summaries;
- uses a safe fallback summary path when richer generation is unavailable;
- writes CSV and Parquet report data;
- writes a Markdown event report.

The repository copy at `reports/latest_fight_report.md` is a publication artifact, not the primary analytical source of truth. The corresponding S3 outputs and upstream scoring data should be used when troubleshooting a report discrepancy.

## Storage architecture

Shared S3 behavior is centralized in `common/io_helpers.py`.

Verified source defaults:

- `S3_BUCKET=degenerative-investigator` when no override is supplied;
- `AWS_REGION=us-east-2` when no override is supplied.

The helper supports object existence checks, CSV reads, text/byte writes, and paired CSV/Parquet writes. Exact key names and stage-to-stage object contracts are documented in [degenerate_investigator S3, Orchestration, and Security Boundary](../systems/degenerate-investigator-storage-orchestration-security.md).

These are source-code defaults, not proof that every live object or IAM policy currently uses those values.

## GitHub Actions architecture

The repository contains manual workflows for:

- current event ingestion;
- current fighter profiles;
- historical fights;
- historical fighter profiles;
- odds ingestion;
- fighter-news enrichment;
- feature building;
- historical training-dataset building;
- model training;
- target-event scoring;
- report generation;
- latest-report export to the repository.

The analytical workflows run Python 3.11 and use `workflow_dispatch`. The inspected read-oriented jobs use `contents: read`. The export workflow is a distinct publication boundary: it requires `contents: write`, preserves checkout credentials, copies the Markdown report from S3, commits only when the repository file changed, and pushes the resulting commit.

## Dependencies

`requirements.txt` is the Python dependency source of truth. Major implementation dependencies include HTTP/web parsing, pandas/Parquet data processing, AWS S3 access, scikit-learn model training/inference, and the OpenAI client. GitHub Actions installs dependencies before running each stage.

A maintainer should use the repository requirement file rather than copying package versions from documentation, because dependency updates are implementation changes.

## Failure modes

Common architecture-level failure classes include:

- upstream UFC Stats markup or URL behavior changes;
- missing or malformed event/fighter rows;
- missing required S3 input objects;
- AWS authentication, region, bucket, or object-permission failures;
- missing `ODDS_API_KEY` for odds ingestion;
- missing `OPENAI_API_KEY` for news enrichment or generated report text where used;
- external API rate limits, transport errors, or schema changes;
- incompatible feature columns between a trained artifact and inference data;
- single-class historical targets causing the documented training fallback;
- trained model unavailable or unusable, causing the explicit scoring heuristic fallback;
- malformed generated JSON in news enrichment;
- publication workflow unable to write/push to the repository;
- operator dispatching a downstream stage before its required S3 inputs exist.

## Rerun and recovery principles

Because workflows are stage-specific, recovery should normally rerun the smallest failed stage after correcting its input/configuration issue. Before rerunning a downstream stage, verify that its upstream S3 inputs exist and represent the intended event/history window.

Historical aggregate jobs should be treated as rebuilds for the selected window rather than presumed incremental appends. Model training should be rerun after intentional training-dataset or feature-contract changes. Target-event scoring should be rerun after model or feature changes, followed by report generation and, only if desired, repository export.

Never treat a successful report export as proof that upstream model training or scoring was correct; publication only copies the generated report artifact.

## Security and configuration

Names that are safe and technically necessary to document include:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`;
- `S3_BUCKET`;
- `ODDS_API_KEY`;
- `OPENAI_API_KEY`.

Do not publish values for credentials, tokens, passwords, private keys, personal email addresses, or personal account identifiers.

Repository source proves how these names are consumed, but it does not prove the complete live IAM policy, bucket policy, secret-store configuration, object retention policy, or encryption configuration. Those must not be guessed.

## Limitations

- End-to-end orchestration is manual rather than automatically chained.
- External HTML and API dependencies can change independently of this repository.
- Historical ingestion behavior is rebuild-oriented for a selected window.
- Live AWS/IAM configuration is not fully represented in source.
- Model quality is bounded by the historical dataset, features, label construction, and evaluation design implemented at training time.
- A fallback score is not equivalent to a trained-model probability.
- Recent-news enrichment is dependent on external search/model availability and structured-output quality.
- Odds coverage depends on The Odds API response, configured regions/market, and event/fighter name matching.
- The repository does not implement wagering execution, staking logic, bookmaker selection, or bankroll management.

## Related documentation

- [degenerate_investigator S3, Orchestration, and Security Boundary](../systems/degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)
- [Documentation Target Catalogue](../high-director/documentation-target-catalogue.md)
- [Repository Scan: degenerate_investigator](../high-director/repository-scan-degenerate-investigator.md)

## Continuation

The next documentation layer should describe each pipeline stage with exact CLI/workflow inputs, source functions, S3 keys, schemas, feature definitions, failure handling, rerun procedure, and artifact contracts. Those subordinate pages should link back here instead of redefining the system boundary.
