---
title: degenerate_investigator S3, Orchestration, and Security Boundary
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

It is intentionally operational and source-grounded. It does not claim knowledge of live IAM policies, bucket policies, secret values, encryption settings, retention rules, or account-level controls that are not represented in repository source.

## Boundary summary

The implementation uses Amazon S3 as the cross-stage persistence layer. GitHub Actions workflows are manually dispatched and run individual Python stages. Most workflows need repository read access plus AWS credentials supplied through GitHub secrets. The final report-export workflow is separate because it also needs repository write permission to commit the exported Markdown artifact.

There is no verified end-to-end workflow that automatically chains all stages. The operator is responsible for selecting a compatible stage order and supplying the correct S3 key inputs when a workflow exposes them.

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

`common/io_helpers.py` defines these shared functions:

- `get_env(name, default=None, required=False)` — read an environment variable and raise when a required value is absent/blank;
- `slugify(value)` — normalize names into lowercase hyphenated object-name components;
- `s3_client(region=None)` — construct a boto3 S3 client using the requested or default region;
- `s3_exists(s3, bucket, key)` — use `head_object` and return `False` only for not-found conditions while re-raising other client errors;
- `read_s3_csv(bucket, key, region=None)` — retrieve an object and parse UTF-8-sig CSV into a DataFrame;
- `put_s3_text(bucket, key, text, content_type="text/csv", region=None)` — write UTF-8-sig text;
- `put_s3_bytes(bucket, key, payload, content_type, region=None)` — write arbitrary bytes;
- `write_csv_and_parquet(df, bucket, csv_key, parquet_key, region=None)` — write equivalent CSV and Snappy-compressed Parquet objects;
- `pick_first(values, default="")` — return the first non-empty value from an iterable.

Verified defaults in this module:

- `S3_BUCKET`: `degenerative-investigator`;
- `AWS_REGION`: `us-east-2`.

The GitHub Actions workflows also set the bucket explicitly to `degenerative-investigator`; they supply the region through the `AWS_REGION` secret.

## S3 layout and object contracts

The following key patterns are generated or consumed by the current source.

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
| Current MMA market-data snapshot | `raw/odds/current_mma_odds.csv` | `raw/odds/parquets/current_mma_odds.parquet` | `extract/odds_current_mma.py` |
| Fighter recent-news enrichment | `raw/news/fighter_recent_news.csv` | `raw/news/parquets/fighter_recent_news.parquet` | `extract/fighter_recent_news.py` |

The market-data objects are analytical inputs only. They support implied-probability and model-vs-market comparison fields; the repository does not implement staking or wagering execution logic.

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
| Feature importance CSV | `processed/ufc/feature_importance.csv` | `process/train_ufc_winner_model.py` when the trained estimator is Random Forest |
| Feature importance Parquet | `processed/ufc/parquets/feature_importance.parquet` | same |

The model artifact contains the fitted estimator pipeline and the feature-column list expected for scoring. The metrics JSON records row counts, train/test counts, accuracy, log loss, available features, unique target classes, and `model_type`; ROC AUC is added only when more than one target class exists.

### Predictions

| Purpose | CSV key | Parquet key | Producer |
| --- | --- | --- | --- |
| Event predictions | `processed/ufc/{event_slug}_predictions.csv` | `processed/ufc/parquets/{event_slug}_predictions.parquet` | `process/score_target_event.py` |

Prediction rows explicitly include `scoring_method`. `trained_model` means the serialized model artifact was loaded and used. `heuristic` means the explicit fallback path was used because the configured model object did not exist. A heuristic output must not be described as a trained-model prediction.

### Reports

| Purpose | Key pattern | Producer |
| --- | --- | --- |
| Report rows CSV | `processed/reports/{event_slug}_fight_report.csv` | `process/generate_event_report.py` |
| Report rows Parquet | `processed/reports/parquets/{event_slug}_fight_report.parquet` | same |
| Markdown report | `processed/reports/{event_slug}_fight_report.md` | same |
| Repository publication target | `reports/latest_fight_report.md` | `process/export_s3_report_to_repo.py` plus export workflow |

The repository Markdown file is a copied publication artifact. It is not an independent source of analytical truth.

## Workflow trigger model

Every inspected workflow uses `workflow_dispatch`. No schedule, push, pull-request, or workflow-to-workflow chaining trigger was verified for these pipeline jobs.

All inspected workflows:

- run on `ubuntu-latest`;
- set up Python 3.11;
- install `requirements.txt`;
- set `PYTHONPATH` to the GitHub workspace;
- execute one repository Python entry point.

## Workflow catalogue and inputs

### Current event ingestion

Workflow: `.github/workflows/ufc_ingest_event.yml`

- input: `event_url`;
- environment passed to script: `EVENT_URL`;
- default input is a specific UFC Stats event URL currently committed in the workflow;
- timeout: 60 minutes;
- command: `python extract/ufc_event_card.py`;
- repository permission: `contents: read`.

The script derives `{event_slug}` from the fetched event title and writes the event-card CSV/Parquet pair.

### Current fighter profiles

Workflow: `.github/workflows/ufc_pull_fighter_profiles.yml`

- input: `event_card_key`;
- environment: `EVENT_CARD_KEY`;
- committed default: `raw/ufc/events/ufc-327-prochazka-vs-ulberg_card.csv`;
- timeout: 120 minutes;
- command: `python extract/ufc_fighter_profiles.py`;
- repository permission: `contents: read`.

The resulting current profile objects have fixed keys, so rerunning this stage replaces the current-profile snapshot rather than versioning by event slug.

### Historical fights

Workflow: `.github/workflows/ufc_build_history.yml`

- input: `max_events`;
- environment: `MAX_EVENTS`;
- committed default: `150` completed events;
- timeout: 360 minutes;
- command: `python extract/ufc_historical_fights.py`;
- repository permission: `contents: read`.

The script rewrites the aggregate historical fight objects for the selected completed-event window.

### Historical fighter profiles

Workflow: `.github/workflows/ufc_pull_historical_fighter_profiles.yml`

- input: `historical_fights_key`;
- input: `test_rows`;
- environments: `HISTORICAL_FIGHTS_KEY`, `TEST_ROWS`;
- committed default historical-fights key: `raw/ufc/fights/historical_fights.csv`;
- committed default test limit: `0` (all unique fighter URLs);
- timeout: 360 minutes;
- command: `python extract/ufc_historical_fighter_profiles.py`;
- repository permission: `contents: read`.

Per-profile exceptions are captured into output rows with `profile_error`, allowing the batch to continue.

### Current market-data ingestion

Workflow: `.github/workflows/ufc_pull_odds.yml`

- no workflow inputs;
- requires the secret name `ODDS_API_KEY`;
- timeout: 60 minutes;
- command: `python extract/odds_current_mma.py`;
- repository permission: `contents: read`.

This documentation intentionally records the integration boundary without providing service-access or wagering instructions. The stored product is a normalized analytical market-data snapshot used by feature engineering.

### Fighter recent-news enrichment

Workflow: `.github/workflows/ufc_pull_news.yml`

- input: `fighter_profiles_key`;
- input: `test_rows`;
- environments: `FIGHTER_PROFILES_KEY`, `TEST_ROWS`;
- committed default profile key: `raw/ufc/fighters/fighter_profiles.csv`;
- committed default test limit: `6`;
- secret: `OPENAI_API_KEY`;
- timeout: 180 minutes;
- command: `python extract/fighter_recent_news.py`;
- repository permission: `contents: read`.

The script source itself defaults `TEST_ROWS` to `0`, but the workflow currently defaults the manual input to `6`. When run through the workflow without changing the input, the workflow value controls and only the first six fighters are processed.

### Event feature builder

Workflow: `.github/workflows/ufc_build_features.yml`

- input: `event_card_key`;
- environment: `EVENT_CARD_KEY`;
- committed default: `raw/ufc/events/ufc-327-prochazka-vs-ulberg_card.csv`;
- timeout: 60 minutes;
- command: `python process/ufc_feature_builder.py`;
- repository permission: `contents: read`.

The script also defaults these S3 inputs if not supplied by another execution context:

- `FIGHTER_PROFILES_KEY=raw/ufc/fighters/fighter_profiles.csv`;
- `ODDS_KEY=raw/odds/current_mma_odds.csv`;
- `NEWS_KEY=raw/news/fighter_recent_news.csv`.

Missing market-data or news objects are tolerated by this stage and replaced with empty lookups; fighter profiles are not wrapped in the same optional read behavior.

### Historical training-dataset builder

Workflow: `.github/workflows/ufc_build_training_dataset.yml`

- no workflow inputs;
- `HISTORICAL_FIGHTS_KEY=raw/ufc/fights/historical_fights.csv`;
- `HISTORICAL_FIGHTER_PROFILES_KEY=raw/ufc/fighters/historical_fighter_profiles.csv`;
- timeout: 120 minutes;
- command: `python process/build_historical_training_dataset.py`;
- repository permission: `contents: read`.

The builder produces mirrored fighter-order rows and inverts the binary winner target and feature-difference signs for the mirror row. Historical news is not sourced; `news_flag_diff` is set to `0.0` in the current training builder.

### Model training

Workflow: `.github/workflows/ufc_train_model.yml`

- input: `training_data_key`;
- environment: `TRAINING_DATA_KEY`;
- committed default: `processed/ufc/training_dataset.csv`;
- timeout: 180 minutes;
- command: `python process/train_ufc_winner_model.py`;
- repository permission: `contents: read`.

The training script requires at least ten usable rows. Multi-class target data uses the Random Forest pipeline; single-class target data uses the explicit `DummyClassifier(strategy="prior")` fallback and records `model_type=dummy_prior`.

### Target-event scoring

Workflow: `.github/workflows/ufc_score_event.yml`

- input: `features_key`;
- environment: `FEATURES_KEY`;
- committed default: `processed/ufc/ufc-327-prochazka-vs-ulberg_fight_features.csv`;
- timeout: 60 minutes;
- command: `python process/score_target_event.py`;
- repository permission: `contents: read`.

The script defaults `MODEL_KEY=processed/ufc/model_artifacts.pkl`. If that object exists, it is loaded and used as the scoring source. If it does not exist, the script takes the explicit heuristic path and marks rows `scoring_method=heuristic`.

### Report generation

Workflow: `.github/workflows/ufc_generate_report.yml`

- input: `predictions_key`;
- input: `news_key`;
- environments: `PREDICTIONS_KEY`, `NEWS_KEY`;
- committed prediction default: `processed/ufc/ufc-327-prochazka-vs-ulberg_predictions.csv`;
- committed news default: `raw/news/fighter_recent_news.csv`;
- `USE_OPENAI_REPORTS=true`;
- secret: `OPENAI_API_KEY`;
- timeout: 120 minutes;
- command: `python process/generate_event_report.py`;
- repository permission: `contents: read`.

The report script deduplicates matchup orientations, preferring trained-model rows over fallback rows and then higher confidence. Missing news is tolerated. If generated JSON cannot be obtained, the script uses its deterministic `simple_fallback()` prose path; that prose fallback does not change the underlying scoring method.

### S3-to-repository publication

Workflow: `.github/workflows/export_latest_report_to_repo.yml`

- input: `report_key`;
- input: `output_path`;
- committed report default: `processed/reports/ufc-327-prochazka-vs-ulberg_fight_report.md`;
- committed repository default: `reports/latest_fight_report.md`;
- environments: `REPORT_KEY`, `OUTPUT_PATH`;
- timeout: 30 minutes;
- command: `python process/export_s3_report_to_repo.py`;
- repository permission: `contents: write`;
- checkout preserves workflow credentials;
- after export, the workflow stages the output file, commits only if the staged file changed, then pushes.

This is the only inspected pipeline workflow that requires repository write permission. It should be treated as a publication/control boundary, not as an analytical computation stage.

## Recommended stage order

The dependency graph implied by source is:

1. current event card;
2. current fighter profiles;
3. optional current market-data snapshot;
4. optional recent-news enrichment;
5. event feature build;
6. historical fights;
7. historical fighter profiles;
8. historical training dataset;
9. model training;
10. target-event scoring;
11. report generation;
12. optional report export to repository.

Historical preparation/model training and current-event enrichment can be performed independently until scoring needs a compatible model and feature contract. The repository does not enforce this order automatically.

## Configuration and secret names

Safe source-level names relevant to this boundary:

### AWS/S3

- `AWS_ACCESS_KEY_ID` — GitHub secret in inspected workflows;
- `AWS_SECRET_ACCESS_KEY` — GitHub secret in inspected workflows;
- `AWS_REGION` — GitHub secret in inspected workflows, source default `us-east-2`;
- `S3_BUCKET` — set by workflows to `degenerative-investigator`, source default is the same.

### External analytical integrations

- `OPENAI_API_KEY` — required by recent-news enrichment and supplied to the report workflow when generated summaries are enabled;
- `OPENAI_MODEL` — source-level optional model override, default `gpt-4.1-mini`;
- `ODDS_API_KEY` — required by the current market-data ingestion stage.

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

No `NEWS_API_KEY` use was verified in the inspected source. Do not document it as an active dependency unless code changes establish that integration.

## Security boundary

Repository source demonstrates that workflows use long-lived AWS credential variable names rather than an explicitly configured GitHub OIDC role flow. It does **not** disclose or prove the live IAM principal, policy scope, bucket policy, credential rotation mechanism, or secret ownership.

Never publish secret values. Documentation may name required variables and explain where code consumes them, but should not contain copied secret values, account identifiers, personal email addresses, tokens, passwords, or private keys.

The analytical workflows request only `contents: read`. The report-export workflow requests `contents: write`, making it the higher-impact GitHub permission boundary. Changes to that permission model, authentication architecture, bucket policy, or publication strategy are architecture/security decisions and require explicit review rather than routine documentation edits.

## Failure modes and detection

### S3/input failures

- missing object key: `read_s3_csv` raises from S3 retrieval;
- unauthorized object access or other S3 client errors: propagated rather than treated as missing;
- wrong event key: downstream data can belong to a different target event;
- incompatible CSV schema: pandas or downstream column access fails;
- partial upstream snapshot: downstream run may succeed with incomplete data unless the stage validates row coverage itself.

### UFC Stats extraction failures

- transport/HTTP failure after both URL-scheme attempts;
- site markup changes causing selectors to return no rows;
- malformed fighter-profile fields;
- historical profile failures are captured per row while current-profile failures are not equivalently isolated.

### Enrichment failures

- missing external API secret;
- transport/rate-limit/service errors;
- malformed structured model response;
- fighter-news parsing failures become `parse_error` rows where possible;
- missing market/news S3 objects are tolerated by feature building and converted to empty lookup tables.

### Training failures

- missing `fighter_1_win` target;
- no usable feature columns;
- fewer than ten usable rows;
- data split or model fit error;
- single target class triggers the documented dummy-prior training path rather than Random Forest.

### Scoring failures or fallback

- missing features object: hard failure;
- missing model object: not a hard failure; scoring switches to the explicit heuristic and labels the output accordingly;
- existing but corrupt/incompatible model artifact: current code attempts to load/use it and can fail rather than silently falling back;
- feature-column incompatibility with the serialized artifact: model scoring can fail.

### Reporting failures

- missing predictions object: hard failure;
- missing news object: tolerated;
- generated report JSON error: deterministic `simple_fallback()` report text is used;
- empty prediction data can lead to an effectively empty event report.

### Publication failures

- missing S3 report object;
- AWS read-permission failure;
- invalid/unwritable output path;
- Git push rejected because workflow token lacks required permission or branch rules prevent the push;
- concurrent changes to the target branch causing push rejection.

## Rerun and recovery

Use the smallest safe rerun that restores the broken contract:

- ingestion failed before writing outputs: rerun that ingestion workflow after correcting its input/configuration issue;
- current profile snapshot is incomplete: rerun current fighter profiles after verifying the event-card key;
- historical window changed intentionally: rerun historical fights, historical profiles, training dataset, and model in that order;
- feature logic changed: rebuild both historical training data and current event features before retraining/rescoring;
- model training changed: retrain, verify metrics/artifact, then rescore the target event;
- scoring used `heuristic` because the model object was absent: restore/train the intended model and rerun scoring before regenerating the report;
- report prose failed but predictions are correct: rerun report generation only;
- report export failed after S3 report creation: rerun only the export workflow after addressing repository-write or push conditions.

After any rerun that changes an upstream object, regenerate every downstream artifact whose meaning depends on that object. S3 writes use fixed keys for several current/aggregate products and therefore replace prior object contents unless bucket versioning exists; bucket versioning is not proven by repository source.

## Publication lifecycle

1. `process/generate_event_report.py` writes the event report to `processed/reports/{event_slug}_fight_report.md` in S3.
2. The export workflow is manually dispatched with an S3 `REPORT_KEY` and repository `OUTPUT_PATH`.
3. `process/export_s3_report_to_repo.py` reads the S3 object and writes UTF-8 Markdown into the checkout.
4. The workflow stages the file.
5. If the staged content is unchanged, no commit is created.
6. If changed, the workflow creates a bot-authored commit and pushes it.

A publication commit therefore proves only that the selected S3 Markdown object was copied into the repository. It does not independently validate model quality, source freshness, or upstream pipeline correctness.

## Live-state unknowns

The repository does not prove:

- the live IAM user/role identity;
- exact IAM action/resource policy scope;
- S3 bucket policy;
- S3 public-access-block settings;
- object encryption settings;
- object versioning/retention/lifecycle rules;
- CloudTrail or other audit logging coverage;
- GitHub environment protection rules;
- secret rotation cadence;
- branch-protection interaction with the publication workflow.

Do not fill these gaps by assumption. If any one becomes necessary for operations or a security review, collect one coherent sanitized source of deployed-state evidence at a time and update this page.

## Limitations

- manual orchestration means ordering errors are possible;
- fixed object keys can overwrite prior snapshots;
- several workflow defaults are currently event-specific and must be checked before dispatching a different event;
- historical extraction is rebuild-oriented;
- optional enrichment can silently become empty feature lookups;
- model absence causes a documented heuristic fallback, but corrupt/incompatible model presence can fail hard;
- report-text fallback is independent of the scoring fallback;
- live AWS security posture cannot be inferred from source-only evidence;
- repository report export writes directly through a workflow token and should remain isolated from read-only analytical jobs.

## Related documentation

- [degenerate_investigator Repository and UFC Analytics Architecture](../repositories/degenerate-investigator.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)
- [Repository Scan: degenerate_investigator](../high-director/repository-scan-degenerate-investigator.md)

## Continuation

Subordinate pipeline pages should reuse these object and control contracts rather than restating them inconsistently. Any implementation change to a key name, workflow input, secret/configuration name, fallback condition, or publication permission should update this page in the same documentation change set.
