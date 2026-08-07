---
title: Repository Scan — degenerate_investigator
summary: Documentation-target inventory for the UFC fight analytics, data, modelling, and reporting repository.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 32
permalink: /projects/high-director/repository-scan-degenerate-investigator/
---

# Repository Scan — `degenerate_investigator`

## Repository role

`degenerate_investigator` is a UFC-first fight analytics repository. Its README states that it ingests event, fighter, odds, and news data; stores raw/processed datasets in S3; builds matchup features; trains win-probability models; scores target events; and generates written fight-analysis reports. The README explicitly states that the repository does not include staking logic or bookmaker-targeted betting recommendations.

## Documentation targets

### 1. `degenerate_investigator` repository

**Categories:** repository, analytics system, data/model pipeline, deployment/operations.

Document repository purpose, structure, Python/AWS dependencies, workflow inventory, S3 layout, secrets/configuration names, and subordinate components.

### 2. UFC Event and Fighter Data Ingestion

**Categories:** extraction pipeline, UFC Stats integration, raw data products, GitHub Actions.

Evidence:

```text
extract/ufc_event_card.py
extract/ufc_fighter_profiles.py
.github/workflows/ufc_ingest_event.yml
.github/workflows/ufc_pull_fighter_profiles.yml
```

The manual event-ingest workflow accepts a UFC Stats event URL and writes through the shared S3 helper layer.

### 3. Historical Fight and Fighter-Profile Ingestion

**Categories:** historical data pipeline, model-training source data, GitHub Actions.

Evidence:

```text
extract/ufc_historical_fights.py
extract/ufc_historical_fighter_profiles.py
.github/workflows/ufc_build_history.yml
.github/workflows/ufc_pull_historical_fighter_profiles.yml
```

This should be documented separately from current-event ingestion because it feeds model training and has a distinct lifecycle.

### 4. Current MMA Odds Ingestion

**Categories:** external API integration, market-data pipeline, raw data product, authentication boundary.

Evidence:

```text
extract/odds_current_mma.py
.github/workflows/ufc_pull_odds.yml
```

Verified implementation uses The Odds API endpoint for MMA head-to-head odds, converts American prices to decimal values, and writes CSV/Parquet under `raw/odds/`. Configuration includes `ODDS_API_KEY`, regions, markets, and optional bookmaker filters.

Document as analytics input only; the repository itself states it does not implement staking or bookmaker-targeted recommendations.

### 5. Fighter Recent-News Enrichment

**Categories:** OpenAI integration, web-search enrichment, contextual data pipeline, raw data product.

Evidence:

```text
extract/fighter_recent_news.py
.github/workflows/ufc_pull_news.yml
```

Verified implementation uses the OpenAI Responses API with web search to collect recent factual fighter context, attempts JSON repair on malformed model output, and writes normalized CSV/Parquet under `raw/news/`.

### 6. Matchup Feature Engineering

**Categories:** feature pipeline, data integration, model-input data product.

Evidence:

```text
process/ufc_feature_builder.py
.github/workflows/ufc_build_features.yml
```

The feature builder joins event cards, fighter profiles, current odds, and recent-news flags. Derived differences include height, reach, striking, takedown, submission, defence/accuracy, career records, recent fights, and news flags. It also calculates implied probabilities from current odds.

### 7. Historical Training Dataset Builder

**Categories:** ML dataset pipeline, historical data product, training preparation.

Evidence:

```text
process/build_historical_training_dataset.py
.github/workflows/ufc_build_training_dataset.yml
```

Verified output:

```text
processed/ufc/training_dataset.csv
processed/ufc/parquets/training_dataset.parquet
```

The builder joins historical fights to historical fighter profiles, derives feature differences, creates mirrored matchup rows, and produces `fighter_1_win` as the target.

### 8. UFC Winner Model Training

**Categories:** machine-learning training pipeline, model artifact, metrics, GitHub Actions.

Evidence:

```text
process/train_ufc_winner_model.py
.github/workflows/ufc_train_model.yml
```

Verified implementation uses a scikit-learn pipeline with median imputation and a `RandomForestClassifier` (or `DummyClassifier` for single-class training data), train/test splitting, accuracy/log-loss/ROC-AUC metrics where applicable, model pickling, and feature-importance output.

Outputs include:

```text
processed/ufc/model_metrics.json
processed/ufc/model_artifacts.pkl
processed/ufc/feature_importance.csv
processed/ufc/parquets/feature_importance.parquet
```

### 9. Target Event Scoring

**Categories:** model inference, heuristic fallback, prediction data product, comparison analytics.

Evidence:

```text
process/score_target_event.py
.github/workflows/ufc_score_event.yml
```

The scorer loads the trained model when present and otherwise uses an explicit heuristic-weight fallback. It produces win probabilities, predicted winner, confidence bucket, top signals, and model-vs-market probability deltas.

Document the trained-model and heuristic paths distinctly so fallback behavior is not mistaken for the trained model.

### 10. Fight Analysis Report Generator

**Categories:** reporting pipeline, OpenAI integration, generated data/report products.

Evidence:

```text
process/generate_event_report.py
.github/workflows/ufc_generate_report.yml
reports/latest_fight_report.md
```

The report generator deduplicates matchups, joins predictions with fighter-news summaries, optionally uses OpenAI for concise structured previews, falls back to deterministic text on model failure, and writes CSV/Parquet/Markdown reports. Its prompt explicitly prohibits betting advice, parlays, and staking.

### 11. Report Export-to-Repository Workflow

**Categories:** publishing automation, S3-to-GitHub transfer, GitHub Actions write workflow.

Evidence:

```text
process/export_s3_report_to_repo.py
.github/workflows/export_latest_report_to_repo.yml
reports/latest_fight_report.md
```

This is a distinct publication/control flow and should be included in operations/security documentation, especially because it writes generated output back into the repository.

### 12. S3 Storage and Shared I/O Layer

**Categories:** AWS/S3 integration, storage subsystem, data-product conventions, configuration.

Evidence:

```text
common/io_helpers.py
README.md
```

Verified defaults:

```text
bucket: degenerative-investigator
region: us-east-2
```

S3 layout described by the repository:

```text
raw/ufc/events/
raw/ufc/fighters/
raw/ufc/fights/
raw/odds/
raw/news/
processed/ufc/
processed/ufc/parquets/
processed/reports/
```

The helper layer centralizes environment lookup, S3 existence/read/write, and paired CSV/Parquet output.

### 13. GitHub Actions Pipeline Orchestration

**Categories:** workflow orchestration, deployment/runtime, operations/runbook.

Evidence: all `.github/workflows/ufc_*.yml` plus report-export workflow.

Document stage ordering, manual inputs, Python version, AWS/OpenAI/Odds/News secret names, expected upstream S3 keys, timeouts, failure behavior, and which stages are independently rerunnable.

## Cross-cutting configuration/security boundaries

Repository README/workflows identify these secret/configuration names:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
OPENAI_API_KEY
ODDS_API_KEY
NEWS_API_KEY
```

Secret values must never be published. Full documentation should also record S3 permissions, API quota/failure handling, OpenAI model selection, data-source terms/access assumptions, and report-publication permissions.

## Dependency inventory

`requirements.txt` includes:

```text
requests
boto3
pandas
openai>=1.99.2
pyarrow
pyyaml
beautifulsoup4
scikit-learn
python-dateutil
lxml
```

GitHub workflows currently use Python 3.11.

## Current-vs-planned boundary

The README describes the repository as an MVP-oriented UFC analytics pipeline. Full documentation must use implementation/workflows as stronger evidence than README sequencing where they diverge.

The model/report outputs are analytical artifacts. Documentation should describe their technical generation and limitations without presenting them as wagering instructions.

## Preliminary priority

- **P0:** repository/system architecture; S3 data model; orchestration/security/configuration.
- **P1:** UFC ingestion; historical/training dataset; feature engineering; model training; scoring/reporting.
- **P2:** odds/news enrichment and report-export publishing subsystem.
- **P3:** superseded experimental behavior, if discovered during full documentation.

Final owner-wide priority is deferred until all repositories are scanned.

## Verification record

Verified on 2026-08-07 from the complete repository tree plus README, requirements, representative workflows, shared S3 helper code, odds/news extraction, feature building, training-dataset building, model training, scoring, and report generation. No credential values were inspected or published.

## Related Documents

- [Repository Documentation Discovery Initiative]({{ '/projects/high-director/repository-documentation-discovery/' | relative_url }})
