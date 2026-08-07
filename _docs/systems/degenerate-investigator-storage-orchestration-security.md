---
title: degenerate_investigator S3, Orchestration, and Security Boundary
summary: Source-grounded S3 object contracts, manual GitHub Actions orchestration, security/configuration boundaries, failure recovery, model-artifact lifecycle, and report publication controls for degenerate_investigator.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator S3, Orchestration, and Security Boundary

## Purpose

This page documents the storage contracts, manual workflow orchestration, configuration names, security boundaries, failure/recovery behavior, and report-publication boundary for the `degenerate_investigator` UFC analytics system.

It is source-grounded. It does not claim knowledge of live IAM policies, bucket policies, secret values, encryption settings, retention rules, or account-level controls that are not represented in repository source.

## Boundary summary

Amazon S3 is the cross-stage persistence layer. GitHub Actions workflows are manually dispatched and run individual Python stages. Most workflows need repository read access plus AWS credentials supplied through GitHub secrets. The final report-export workflow is separate because it also needs repository write permission to commit the exported Markdown artifact.

There is no verified end-to-end workflow that automatically chains all stages. Operators must select compatible stages and inputs and respect the S3 object dependencies between them.

## Source-of-truth files

Primary control-plane sources:

- `common/io_helpers.py`;
- `.github/workflows/ufc_ingest_event.yml`;
- `.github/workflows/ufc_pull_fighter_profiles.yml`;
- `.github/workflows/ufc_build_history.yml`;
- `.github/workflows/ufc_pull_historical_fighter_profiles.yml`;
- `.github/workflows/ufc_pull_odds.yml`;
- `.github/workflows/ufc_pull_news.yml`;
- `.github/workflows/ufc_build_features.yml`;
- `.github/workflows/ufc_build_training_dataset.yml`;
- `.github/workflows/ufc_train_model.yml`;
- `.github/workflows/ufc_score_event.yml`;
- `.github/workflows/ufc_generate_report.yml`;
- `.github/workflows/export_latest_report_to_repo.yml`;
- `process/export_s3_report_to_repo.py`.

## Shared S3 helper behavior

`common/io_helpers.py` defines:

- `get_env()` — read configuration and fail on missing required values;
- `slugify()` — normalize names into object-name components;
- `s3_client()` — create a boto3 S3 client;
- `s3_exists()` — check object existence while re-raising non-not-found client errors;
- `read_s3_csv()` — retrieve and parse UTF-8-sig CSV;
- `put_s3_text()` — write text objects;
- `put_s3_bytes()` — write binary objects;
- `write_csv_and_parquet()` — write paired CSV and Snappy-compressed Parquet objects;
- `pick_first()` — return the first non-empty value.

Verified defaults:

- `S3_BUCKET=degenerative-investigator`;
- `AWS_REGION=us-east-2`.

The GitHub Actions workflows also set the bucket explicitly to `degenerative-investigator`; they supply the region through the `AWS_REGION` secret.

## S3 layout and object contracts

### Raw UFC event and fighter data

| Purpose | CSV key | Parquet key | Producer |
| --- | --- | --- | --- |
| Target event card | `raw/ufc/events/{event_slug}_card.csv` | `raw/ufc/events/parquets/{event_slug}_card.parquet` | `extract/ufc_event_card.py` |
| Current fighter profiles | `raw/ufc/fighters/fighter_profiles.csv` | `raw/ufc/fighters/parquets/fighter_profiles.parquet` | `extract/ufc_fighter_profiles.py` |
| Historical fights | `raw/ufc/fights/historical_fights.csv` | `raw/ufc/fights/parquets/historical_fights.parquet` | `extract/ufc_historical_fights.py` |
| Historical fighter profiles | `raw/ufc/fighters/historical_fighter_profiles.csv` | `raw/ufc/fighters/parquets/historical_fighter_profiles.parquet` | `extract/ufc_historical_fighter_profiles.py` |

### Raw analytical enrichment

| Purpose | CSV key | Parquet key | Producer |
| --- | --- | --- | --- |
| Current MMA market-context snapshot | `raw/odds/current_mma_odds.csv` | `raw/odds/parquets/current_mma_odds.parquet` | `extract/odds_current_mma.py` |
| Fighter recent-news enrichment | `raw/news/fighter_recent_news.csv` | `raw/news/parquets/fighter_recent_news.parquet` | `extract/fighter_recent_news.py` |

The market-context objects are analytical inputs only. Documentation does not provide external service-access instructions or wagering guidance.

### Processed UFC features and training data

| Purpose | CSV key | Parquet key | Producer |
| --- | --- | --- | --- |
| Event matchup features | `processed/ufc/{event_slug}_fight_features.csv` | `processed/ufc/parquets/{event_slug}_fight_features.parquet` | `process/ufc_feature_builder.py` |
| Historical training dataset | `processed/ufc/training_dataset.csv` | `processed/ufc/parquets/training_dataset.parquet` | `process/build_historical_training_dataset.py` |

### Model artifacts

| Purpose | Key | Producer |
| --- | --- | --- |
| Serialized model artifact | `processed/ufc/model_artifacts.pkl` | `process/train_ufc_winner_model.py` |
| Model metrics/metadata | `processed/ufc/model_metrics.json` | `process/train_ufc_winner_model.py` |
| Feature importance CSV | `processed/ufc/feature_importance.csv` | `process/train_ufc_winner_model.py` when Random Forest is used |
| Feature importance Parquet | `processed/ufc/parquets/feature_importance.parquet` | same |

The serialized artifact contains the estimator pipeline plus its feature-column contract. The metrics object records row counts, train/test counts, accuracy, log loss, available features, unique target classes, and `model_type`; ROC AUC is present only for multi-class data.

### Predictions

| Purpose | CSV key | Parquet key | Producer |
| --- | --- | --- | --- |
| Event predictions | `processed/ufc/{event_slug}_predictions.csv` | `processed/ufc/parquets/{event_slug}_predictions.parquet` | `process/score_target_event.py` |

Prediction rows explicitly include `scoring_method`:

- `trained_model` — serialized model artifact loaded and used;
- `heuristic` — explicit fallback path used because the configured model object did not exist.

A heuristic output must not be described as a trained-model prediction.

### Reports

| Purpose | Key pattern | Producer |
| --- | --- | --- |
| Report rows CSV | `processed/reports/{event_slug}_fight_report.csv` | `process/generate_event_report.py` |
| Report rows Parquet | `processed/reports/parquets/{event_slug}_fight_report.parquet` | same |
| Markdown report | `processed/reports/{event_slug}_fight_report.md` | same |
| Repository publication target | `reports/latest_fight_report.md` | `process/export_s3_report_to_repo.py` plus export workflow |

The repository Markdown file is a copied publication artifact, not an independent analytical source of truth.

## Workflow trigger model

Every inspected workflow uses `workflow_dispatch`. No schedule, push, pull-request, or workflow-to-workflow chaining trigger was verified for these pipeline jobs.

All inspected workflows run on `ubuntu-latest`, set up Python 3.11, install `requirements.txt`, set `PYTHONPATH` to the workspace, and execute one repository Python entry point.

## Workflow catalogue

### Current event ingestion

`.github/workflows/ufc_ingest_event.yml`

- input: `event_url`;
- environment: `EVENT_URL`;
- timeout: 60 minutes;
- command: `python extract/ufc_event_card.py`;
- permission: `contents: read`.

The script derives `{event_slug}` from the fetched event title and writes the event-card CSV/Parquet pair.

### Current fighter profiles

`.github/workflows/ufc_pull_fighter_profiles.yml`

- input: `event_card_key`;
- environment: `EVENT_CARD_KEY`;
- committed default: `raw/ufc/events/ufc-327-prochazka-vs-ulberg_card.csv`;
- timeout: 120 minutes;
- command: `python extract/ufc_fighter_profiles.py`;
- permission: `contents: read`.

The output keys are fixed current-profile snapshot keys rather than event-versioned keys.

### Historical fights

`.github/workflows/ufc_build_history.yml`

- input: `max_events`;
- environment: `MAX_EVENTS`;
- committed default: `150` completed events;
- timeout: 360 minutes;
- command: `python extract/ufc_historical_fights.py`;
- permission: `contents: read`.

The script rewrites aggregate historical fight objects for the selected completed-event window.

### Historical fighter profiles

`.github/workflows/ufc_pull_historical_fighter_profiles.yml`

- inputs: `historical_fights_key`, `test_rows`;
- environments: `HISTORICAL_FIGHTS_KEY`, `TEST_ROWS`;
- default historical-fights key: `raw/ufc/fights/historical_fights.csv`;
- default test limit: `0`;
- timeout: 360 minutes;
- command: `python extract/ufc_historical_fighter_profiles.py`;
- permission: `contents: read`.

Per-profile exceptions are captured into output rows with `profile_error`.

### Current market-context ingestion

`.github/workflows/ufc_pull_odds.yml`

- no workflow inputs;
- timeout: 60 minutes;
- command: `python extract/odds_current_mma.py`;
- permission: `contents: read`.

Only the internal analytical stage boundary is documented here. External service-access details are intentionally omitted.

### Fighter recent-news enrichment

`.github/workflows/ufc_pull_news.yml`

- inputs: `fighter_profiles_key`, `test_rows`;
- environments: `FIGHTER_PROFILES_KEY`, `TEST_ROWS`;
- committed default profile key: `raw/ufc/fighters/fighter_profiles.csv`;
- committed workflow test limit: `6`;
- secret: `OPENAI_API_KEY`;
- timeout: 180 minutes;
- command: `python extract/fighter_recent_news.py`;
- permission: `contents: read`.

The source script defaults `TEST_ROWS` to `0`, but the workflow default is `6`; when manually dispatched without changing the input, the workflow value wins.

### Event feature builder

`.github/workflows/ufc_build_features.yml`

- input: `event_card_key`;
- environment: `EVENT_CARD_KEY`;
- committed default: `raw/ufc/events/ufc-327-prochazka-vs-ulberg_card.csv`;
- timeout: 60 minutes;
- command: `python process/ufc_feature_builder.py`;
- permission: `contents: read`.

The script also defaults to current fighter-profile, market-context, and news S3 objects. Market/news read failures are converted to empty lookups; fighter-profile reads are not optional in the same way.

### Historical training-dataset builder

`.github/workflows/ufc_build_training_dataset.yml`

- no workflow inputs;
- `HISTORICAL_FIGHTS_KEY=raw/ufc/fights/historical_fights.csv`;
- `HISTORICAL_FIGHTER_PROFILES_KEY=raw/ufc/fighters/historical_fighter_profiles.csv`;
- timeout: 120 minutes;
- command: `python process/build_historical_training_dataset.py`;
- permission: `contents: read`.

The builder produces mirrored fighter-order rows, inverts the binary target for the mirror row, and negates all feature-difference signs. `news_flag_diff` is currently set to `0.0` for historical training rows.

### Model training

`.github/workflows/ufc_train_model.yml`

- input: `training_data_key`;
- environment: `TRAINING_DATA_KEY`;
- default: `processed/ufc/training_dataset.csv`;
- timeout: 180 minutes;
- command: `python process/train_ufc_winner_model.py`;
- permission: `contents: read`.

Training requires at least ten usable rows. Multi-class target data uses the Random Forest pipeline; single-class target data uses `DummyClassifier(strategy="prior")` and records `model_type=dummy_prior`.

### Target-event scoring

`.github/workflows/ufc_score_event.yml`

- input: `features_key`;
- environment: `FEATURES_KEY`;
- committed default: `processed/ufc/ufc-327-prochazka-vs-ulberg_fight_features.csv`;
- timeout: 60 minutes;
- command: `python process/score_target_event.py`;
- permission: `contents: read`.

The script defaults `MODEL_KEY=processed/ufc/model_artifacts.pkl`. If the object exists, it is loaded and used. If it is absent, scoring uses the explicit heuristic path and writes `scoring_method=heuristic`.

### Report generation

`.github/workflows/ufc_generate_report.yml`

- inputs: `predictions_key`, `news_key`;
- environments: `PREDICTIONS_KEY`, `NEWS_KEY`;
- default prediction key: `processed/ufc/ufc-327-prochazka-vs-ulberg_predictions.csv`;
- default news key: `raw/news/fighter_recent_news.csv`;
- `USE_OPENAI_REPORTS=true`;
- secret: `OPENAI_API_KEY`;
- timeout: 120 minutes;
- command: `python process/generate_event_report.py`;
- permission: `contents: read`.

The script deduplicates reversed matchup rows, preferring trained-model rows and then higher confidence. Missing news is tolerated. Generated-JSON failure uses deterministic `simple_fallback()` prose; that does not alter the underlying scoring method.

### S3-to-repository publication

`.github/workflows/export_latest_report_to_repo.yml`

- inputs: `report_key`, `output_path`;
- default report key: `processed/reports/ufc-327-prochazka-vs-ulberg_fight_report.md`;
- default repository path: `reports/latest_fight_report.md`;
- environments: `REPORT_KEY`, `OUTPUT_PATH`;
- timeout: 30 minutes;
- command: `python process/export_s3_report_to_repo.py`;
- permission: `contents: write`;
- checkout preserves workflow credentials;
- workflow commits only if the exported file changed, then pushes.

This is the only inspected pipeline workflow that requires repository write permission. Treat it as a publication/control boundary, not an analytical computation stage.

## Dependency order

The source-implied stage dependency graph is:

1. current event card;
2. current fighter profiles;
3. optional analytical enrichment snapshots;
4. event feature build;
5. historical fights;
6. historical fighter profiles;
7. historical training dataset;
8. model training;
9. target-event scoring;
10. report generation;
11. optional report export to repository.

Historical preparation/model training and current-event preparation can proceed independently until scoring needs a compatible model and feature contract. The repository does not enforce sequencing automatically.

## Configuration and secret names

Safe source-level names documented for the non-market integrations and core pipeline:

### AWS/S3

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`;
- `S3_BUCKET`.

### OpenAI

- `OPENAI_API_KEY`;
- `OPENAI_MODEL`.

### Stage inputs

- `EVENT_URL`;
- `EVENT_CARD_KEY`;
- `FIGHTER_PROFILES_KEY`;
- `HISTORICAL_FIGHTS_KEY`;
- `HISTORICAL_FIGHTER_PROFILES_KEY`;
- `MAX_EVENTS`;
- `TEST_ROWS`;
- `DELAY_BETWEEN_REQUESTS`;
- `ODDS_KEY`;
- `NEWS_KEY`;
- `TRAINING_DATA_KEY`;
- `FEATURES_KEY`;
- `MODEL_KEY`;
- `PREDICTIONS_KEY`;
- `USE_OPENAI_REPORTS`;
- `REPORT_KEY`;
- `OUTPUT_PATH`.

No separate news-service API integration was verified in source. Do not document one unless implementation changes establish it.

## Security boundary

Repository source demonstrates that workflows use AWS credential variable names rather than an explicitly configured GitHub OIDC role flow. It does **not** prove the live IAM principal, policy scope, bucket policy, credential rotation mechanism, or secret ownership.

Never publish secret values. Documentation may name required variables and explain source consumption, but must not contain credential values, account identifiers, personal email addresses, tokens, passwords, or private keys.

Analytical workflows request `contents: read`. The report-export workflow requests `contents: write`, making it the higher-impact GitHub permission boundary. Changes to that permission model, authentication architecture, bucket policy, or publication strategy require explicit architectural/security review.

## Failure modes

### S3/input

- missing object key: S3 retrieval fails;
- unauthorized or other S3 client errors: propagated rather than treated as missing;
- wrong event key: downstream data may belong to a different event;
- incompatible CSV schema: pandas or downstream column access fails;
- partial upstream snapshot: downstream stages may have incomplete context unless they validate coverage.

### UFC Stats extraction

- transport/HTTP failure after both URL-scheme attempts;
- markup changes causing selectors to produce no expected rows;
- malformed profile fields;
- historical-profile errors are isolated per fighter while current-profile errors are less isolated.

### Enrichment

- missing required external configuration;
- service/rate-limit/transport errors;
- malformed structured model response;
- recent-news parsing failures become `parse_error` rows where possible;
- feature building tolerates unavailable optional market/news objects by using empty lookups.

### Training

- missing `fighter_1_win` target;
- no usable feature columns;
- fewer than ten usable rows;
- data split or fit failure;
- single target class invokes the dummy-prior training path rather than Random Forest.

### Scoring

- missing features object: hard failure;
- missing model object: explicit heuristic fallback;
- corrupt/incompatible existing model artifact: can fail hard rather than silently falling back;
- feature-column incompatibility: model scoring failure.

### Reporting

- missing predictions object: hard failure;
- missing news object: tolerated;
- generated report JSON error: deterministic `simple_fallback()` text;
- empty predictions may produce an effectively empty report.

### Publication

- missing S3 report object;
- AWS read-permission failure;
- invalid/unwritable output path;
- Git push rejected by permissions or branch rules;
- concurrent branch changes causing push rejection.

## Rerun and recovery

Use the smallest safe rerun that restores the broken contract:

- ingestion failure before output: rerun that ingestion stage after correcting its source/configuration issue;
- current profiles incomplete: rerun profiles after verifying the event-card key;
- historical window changed: rerun historical fights, historical profiles, training dataset, and model;
- feature logic changed: rebuild historical training data and current features before retraining/rescoring;
- model logic changed: retrain, inspect metrics/artifact, then rescore;
- scoring used `heuristic` because the model object was absent: restore/train the intended model, rerun scoring, then regenerate the report;
- report prose failed while predictions are correct: rerun report generation only;
- report export failed after S3 report creation: rerun only the export workflow after fixing repository-write/push conditions.

After an upstream rerun, regenerate every downstream artifact whose meaning depends on the changed object. Several current/aggregate products use fixed keys, so reruns replace prior object contents unless S3 versioning exists; versioning is not proven by repository source.

## Publication lifecycle

1. `process/generate_event_report.py` writes `processed/reports/{event_slug}_fight_report.md` to S3.
2. The export workflow is manually dispatched with `REPORT_KEY` and `OUTPUT_PATH`.
3. `process/export_s3_report_to_repo.py` reads the S3 object and writes UTF-8 Markdown into the checkout.
4. The workflow stages the file.
5. If unchanged, no commit is created.
6. If changed, the workflow creates a bot-authored commit and pushes.

A publication commit therefore proves only that the selected S3 Markdown object was copied into the repository; it does not validate model quality, source freshness, or upstream pipeline correctness.

## Live-state unknowns

Source does not prove:

- live IAM user/role identity;
- exact IAM action/resource policy scope;
- S3 bucket policy;
- public-access-block settings;
- object encryption settings;
- versioning/retention/lifecycle rules;
- audit logging coverage;
- GitHub environment protection rules;
- secret rotation cadence;
- branch-protection interaction with report publication.

Do not fill these gaps by assumption. If one becomes necessary, collect one coherent sanitized source of deployed-state evidence at a time and update this page.

## Limitations

- manual orchestration permits ordering mistakes;
- fixed object keys can replace prior snapshots;
- several workflow defaults are event-specific and must be checked before dispatching a different event;
- historical extraction is rebuild-oriented;
- optional enrichment can become empty feature lookups;
- model absence invokes a documented heuristic fallback, while corrupt/incompatible model presence can fail hard;
- report-text fallback is independent of the scoring fallback;
- live AWS security posture cannot be inferred from source-only evidence;
- repository report export writes directly through a workflow token and should remain isolated from read-only analytical jobs.

## Related documentation

- [degenerate_investigator Repository and UFC Analytics Architecture](../repositories/degenerate-investigator.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)
- [Repository Scan: degenerate_investigator](../high-director/repository-scan-degenerate-investigator.md)

## Continuation

Subordinate pipeline pages should reuse these object and control contracts. Any implementation change to an S3 key, workflow input, core secret/configuration name, fallback condition, or publication permission should update this page in the same documentation change set. Market-context pages must remain limited to internal analytical contracts and must not become service-access or wagering guidance.
