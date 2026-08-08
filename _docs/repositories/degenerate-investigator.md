---
title: degenerate_investigator Repository and UFC Analytics Architecture
summary: Source-grounded repository and system architecture for the UFC analytics, ingestion, feature engineering, model training, scoring, reporting, S3, and publication workflow.
section: repositories
doc_type: repository
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Repository and UFC Analytics Architecture

## Purpose

`degenerate_investigator` is a Python-based UFC analytics, data-engineering, machine-learning, scoring, and report-generation repository. It gathers current and historical UFC data, enriches selected matchups with market-context and recent-news data, engineers model features, builds a historical training dataset, trains a UFC winner model, scores a target event, generates analytical reports, stores pipeline products in Amazon S3, and can publish the latest Markdown report back into the repository.

The repository is analytical. It does **not** implement staking logic, bankroll management, bookmaker selection, or bookmaker-targeted recommendations. Market-price data is treated only as an analytical input and a model-vs-market comparison signal.

## Repository maturity

The repository contains executable Python pipelines and GitHub Actions workflows rather than a single deployed application or service. The implementation is stage-oriented and S3-backed. The inspected workflows are manually dispatched and do not form an automatically chained end-to-end orchestrator.

A capable maintainer should treat repository source and persisted S3 contracts as the implementation source of truth. Live AWS/IAM deployment state is not fully provable from repository source alone.

## Top-level implementation map

| Area | Source | Responsibility |
| --- | --- | --- |
| Shared I/O | `common/io_helpers.py` | S3 client creation, object existence checks, CSV reads, text/byte writes, and paired CSV/Parquet publication. |
| Current UFC ingestion | `extract/ufc_event_card.py`, `extract/ufc_fighter_profiles.py` | Pull a current UFC event card and fighter-profile data from UFC Stats. |
| Historical UFC ingestion | `extract/ufc_historical_fights.py`, `extract/ufc_historical_fighter_profiles.py` | Build historical fight and fighter-profile inputs from UFC Stats. |
| Current market data | `extract/odds_current_mma.py` | Normalize current MMA market-price data into analytical rows. |
| Fighter news | `extract/fighter_recent_news.py` | Use the OpenAI Responses API with web search to enrich fighters with recent-news context. |
| Matchup features | `process/ufc_feature_builder.py` | Convert event, fighter, market-context, and news inputs into matchup-level analytical features. |
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
3. **External enrichment** obtains market-context data and recent fighter-news context.
4. **Feature engineering** builds matchup-level numerical and contextual features for the selected event.
5. **Historical dataset construction** creates model-training rows and a binary winner target from completed fights.
6. **Model training** fits a winner classifier and persists the trained artifact and evaluation metadata.
7. **Target-event scoring** loads engineered features and, when available and compatible, the trained model to produce matchup probabilities/picks and comparison fields.
8. **Report generation** combines scored matchup data and news context into machine-readable outputs and a human-readable Markdown report.
9. **Publication** optionally copies the S3 Markdown report into `reports/latest_fight_report.md` and commits it through a separate write-enabled GitHub Actions workflow.

There is no verified workflow that automatically invokes all stages in sequence. Operators select workflows and inputs explicitly and must respect the S3 dependencies between them.

## Current UFC Stats ingestion

Primary source paths:

- `extract/ufc_event_card.py`;
- `extract/ufc_fighter_profiles.py`.

Important functions in `extract/ufc_event_card.py`:

- `normalize_ufcstats_url()`;
- `fetch_soup()`;
- `parse_event_card()`;
- `main()`.

Important functions in `extract/ufc_fighter_profiles.py`:

- `normalize_ufcstats_url()`;
- `fetch_soup()`;
- `parse_profile()`;
- `main()`.

The extractors try the alternate URL scheme when the first UFC Stats request fails and raise if the event parser finds no fights. Current fighter-profile ingestion reads the selected event-card S3 object, extracts unique fighter URLs, parses profile statistics, deduplicates by fighter URL, and writes a current profile snapshot.

## Historical UFC ingestion

Primary source paths:

- `extract/ufc_historical_fights.py`;
- `extract/ufc_historical_fighter_profiles.py`.

Important historical-fight functions:

- `normalize_ufcstats_url()`;
- `fetch_soup()`;
- `completed_event_urls()`;
- `parse_event()`;
- `main()`.

The historical-fighter-profile script reuses `parse_profile()` from the current profile extractor and captures per-profile failures into `profile_error` rows so the batch can continue.

Historical fight ingestion rewrites aggregate outputs for the selected completed-event window; it is not an incremental append-only event store.

## Market-context ingestion boundary

`extract/odds_current_mma.py` normalizes external market-price data into machine-readable analytical rows, including American and decimal price representations. This documentation intentionally records only the internal analytical contract. It does not provide external service-access instructions or wagering guidance.

Downstream use is limited to analytical market-context and model-vs-market comparison features.

## Fighter recent-news enrichment

`extract/fighter_recent_news.py` uses the OpenAI Responses API with web search. Important functions are:

- `extract_json()`;
- `make_parse_error_row()`;
- `call_model()`;
- `main()`.

The implementation defaults to model `gpt-4.1-mini`. It first requests structured JSON with web search and, if parsing fails, attempts a second no-search repair call. Per-fighter failures are persisted as `parse_error` rows where possible instead of aborting the entire batch.

## Feature engineering

`process/ufc_feature_builder.py` contains the current-event feature contract. Important functions include:

- `parse_height_to_inches()`;
- `parse_reach_to_inches()`;
- `parse_percent()`;
- `parse_float()`;
- `american_to_implied_prob()`;
- `build_fighter_lookup()`;
- `build_news_flags()`;
- `build_market_lookup()`;
- `main()`.

The builder converts fighter measurements/statistics into numeric fields, joins fighter profiles twice (fighter 1/fighter 2), optionally joins market/news enrichment, and calculates pairwise differences used by scoring/training. Current difference features include height, reach, striking rate/defence, takedown/submission statistics, career record proxies, recent-fight count, and news-flag count.

If current market or news S3 reads fail, the builder substitutes empty lookup tables. Fighter-profile reads are not treated as optional in the same way.

## Historical training-dataset construction

`process/build_historical_training_dataset.py` imports `build_fighter_lookup()` and uses historical fight/profile data to create the supervised dataset.

The target column is `fighter_1_win`. The builder creates a base orientation and a mirrored orientation: fighter names are swapped, `fighter_1_win` is inverted, and each feature-difference sign is negated. `news_flag_diff` is fixed to `0.0` in the current historical builder because historical news enrichment is not supplied there.

The output is `processed/ufc/training_dataset.csv` plus its Parquet equivalent.

## Model source of truth

The trained model and fallback paths are separate behaviors and must not be conflated.

### Trained estimator

`process/train_ufc_winner_model.py` defines:

- `FEATURE_COLS`;
- `build_pipeline()`;
- `main()`.

For normal multi-class training data, `build_pipeline()` creates a median-imputation preprocessing step followed by `RandomForestClassifier(n_estimators=300, random_state=42, min_samples_leaf=3)`.

Training requires at least ten usable rows and at least one usable feature column. Multi-class data is split 80/20 with stratification.

### Single-class training fallback

If the target contains only one unique class, the training script uses `DummyClassifier(strategy="prior")` instead of Random Forest. This is a training-time fallback estimator and is recorded as `model_type=dummy_prior`.

### Model artifacts and metrics

Training writes:

- `processed/ufc/model_artifacts.pkl` — serialized estimator pipeline plus feature-column contract;
- `processed/ufc/model_metrics.json` — row counts, train/test counts, accuracy, log loss, available features, unique classes, and `model_type`; ROC AUC is present only for multi-class data;
- `processed/ufc/feature_importance.csv` and Parquet equivalent only for Random Forest training.

Do not infer model quality from report prose. Use the metrics artifact and the matching feature/training contracts.

## Target-event scoring

`process/score_target_event.py` contains:

- `HEURISTIC_WEIGHTS`;
- `sigmoid()`;
- `safe_num()`;
- `build_top_signals()`;
- `heuristic_probabilities()`;
- `confidence_bucket()`;
- `model_probabilities()`;
- `main()`.

The script reads the event feature dataset and checks for the configured model object, defaulting to `processed/ufc/model_artifacts.pkl`.

- If the object exists and loads successfully, prediction rows are marked `scoring_method=trained_model`.
- If the object does not exist, the explicit heuristic path is used and rows are marked `scoring_method=heuristic`.

The heuristic is **not** the trained model. An existing but corrupt/incompatible model artifact can fail hard; the code does not silently convert every model error into heuristic scoring.

Prediction output includes fighter win probabilities, predicted winner, confidence bucket, top signals, and—when present—market-implied probability/model-market delta fields.

## Report generation

`process/generate_event_report.py` contains:

- `parse_json()`;
- `simple_fallback()`;
- `load_news_summary()`;
- `deduplicate_matchups()`;
- `build_event_overview()`;
- `main()`.

The report builder deduplicates reversed matchup rows and prefers, in order, trained-model scoring, higher confidence, then earlier row order. It joins recent-news summaries, optionally generates structured fight-preview text, and falls back to deterministic `simple_fallback()` prose if generated JSON is unavailable.

The report-text fallback does not change or hide the underlying `scoring_method` distinction.

Outputs are:

- `processed/reports/{event_slug}_fight_report.csv`;
- `processed/reports/parquets/{event_slug}_fight_report.parquet`;
- `processed/reports/{event_slug}_fight_report.md`.

The repository copy at `reports/latest_fight_report.md` is a publication artifact, not the primary analytical source of truth.

## Storage architecture

Shared S3 behavior is centralized in `common/io_helpers.py`.

Verified source defaults:

- `S3_BUCKET=degenerative-investigator` when no override is supplied;
- `AWS_REGION=us-east-2` when no override is supplied.

The helper supports object existence checks, CSV reads, text/byte writes, and paired CSV/Parquet writes. Exact key names and stage-to-stage object contracts are documented in [degenerate_investigator S3, Orchestration, and Security Boundary](../systems/degenerate-investigator-storage-orchestration-security.md).

These are source-code defaults, not proof that every live object or IAM policy currently uses those values.

## GitHub Actions architecture

The repository contains manual workflows for current/historical ingestion, enrichment, feature building, training-dataset construction, model training, target-event scoring, report generation, and report export.

The analytical workflows run Python 3.11 and use `workflow_dispatch`. The inspected read-oriented jobs use `contents: read`. The export workflow is a distinct publication boundary: it requires `contents: write`, preserves checkout credentials, copies the Markdown report from S3, commits only when the repository file changed, and pushes the resulting commit.

## Dependencies

`requirements.txt` is the Python dependency source of truth. Major implementation categories include HTTP/web parsing, pandas/Parquet data processing, AWS S3 access, scikit-learn model training/inference, and the OpenAI client. GitHub Actions installs the requirement file before executing a stage.

Use the repository requirement file rather than copying package versions from documentation because dependency updates are implementation changes.

## Failure modes

Architecture-level failure classes include:

- upstream UFC Stats markup or URL behavior changes;
- missing or malformed event/fighter rows;
- missing required S3 input objects;
- AWS authentication, region, bucket, or object-permission failures;
- unavailable external enrichment configuration;
- external API rate limits, transport errors, or schema changes;
- incompatible feature columns between a trained artifact and inference data;
- single-class historical targets causing the documented training fallback;
- absent trained model object causing the explicit scoring heuristic fallback;
- malformed generated JSON in news/report enrichment;
- publication workflow unable to write/push to the repository;
- operator dispatching a downstream stage before its required S3 inputs exist.

## Rerun and recovery principles

Because workflows are stage-specific, recovery should normally rerun the smallest failed stage after correcting its input/configuration issue. Before rerunning a downstream stage, verify that its upstream S3 inputs exist and represent the intended event/history window.

Historical aggregate jobs should be treated as rebuilds for the selected window. Model training should be rerun after intentional training-dataset or feature-contract changes. Target-event scoring should be rerun after model or feature changes, followed by report generation and, only if desired, repository export.

A successful report export proves only that a selected report artifact was copied; it does not validate upstream model training or scoring.

## Security and configuration

Safe source-level configuration names for the non-market integrations include:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`;
- `S3_BUCKET`;
- `OPENAI_API_KEY`;
- `OPENAI_MODEL`.

Do not publish credential values, tokens, passwords, private keys, personal email addresses, or personal account identifiers.

Repository source proves how these names are consumed, but it does not prove the complete live IAM policy, bucket policy, secret-store configuration, object retention policy, or encryption configuration. Those must not be guessed.

## Limitations

- End-to-end orchestration is manual rather than automatically chained.
- External HTML and API dependencies can change independently of this repository.
- Historical ingestion is rebuild-oriented for a selected window.
- Live AWS/IAM configuration is not fully represented in source.
- Model quality is bounded by the historical dataset, features, label construction, and evaluation design.
- A heuristic score is not equivalent to a trained-model probability.
- Recent-news enrichment depends on external search/model availability and structured-output quality.
- Market-context coverage depends on the upstream snapshot and name matching.
- The repository does not implement wagering execution, staking logic, bookmaker selection, or bankroll management.

## Related documentation

- [degenerate_investigator S3, Orchestration, and Security Boundary](../systems/degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)
- [Documentation Target Catalogue](/projects/high-director/documentation-target-catalogue/)
- [Repository Scan: degenerate_investigator](../high-director/repository-scan-degenerate-investigator.md)

## Continuation

The next documentation layer should describe each pipeline stage with exact CLI/workflow inputs, source functions, S3 keys, schemas, feature definitions, failure handling, rerun procedure, and artifact contracts. Market-data documentation should remain limited to internal analytical contracts and must not become service-access or wagering guidance.
