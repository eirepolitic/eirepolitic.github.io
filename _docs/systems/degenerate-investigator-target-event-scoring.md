---
title: degenerate_investigator Target-Event Scoring
summary: Source-grounded documentation for scoring current UFC event features with the persisted trained estimator or the explicit heuristic fallback, including probability handling, confidence, heuristic top-signals, market-comparison fields, S3 outputs, workflow behavior, failure modes, and provenance limitations.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Target-Event Scoring

## Purpose

`process/score_target_event.py` converts a current-event feature dataset into matchup-level winner probabilities and prediction rows.

There are two mutually exclusive scoring paths:

- `trained_model` — a serialized estimator artifact exists in S3 and is loaded successfully;
- `heuristic` — the configured model object does not exist, so the explicit weighted heuristic is used.

The heuristic is not the trained model. An existing but corrupt or incompatible model artifact is not silently converted into heuristic scoring; it can fail the stage.

## Source paths

- implementation: `process/score_target_event.py`;
- workflow: `.github/workflows/ufc_score_event.yml`;
- model trainer: `process/train_ufc_winner_model.py`;
- feature builder: `process/ufc_feature_builder.py`;
- shared S3 I/O: `common/io_helpers.py`.

Important functions/constants:

- `HEURISTIC_WEIGHTS`;
- `sigmoid()`;
- `safe_num()`;
- `build_top_signals()`;
- `heuristic_probabilities()`;
- `confidence_bucket()`;
- `model_probabilities()`;
- `main()`.

## Inputs

Required:

- `FEATURES_KEY` — S3 CSV key for a current-event feature dataset.

Optional/defaulted:

- `MODEL_KEY` — default `processed/ufc/model_artifacts.pkl`;
- `S3_BUCKET` — default `degenerative-investigator`;
- `AWS_REGION` — default `us-east-2`.

Workflow input:

- `features_key` — committed default `processed/ufc/ufc-327-prochazka-vs-ulberg_fight_features.csv`.

The workflow default is event-specific. Verify it for every new target event.

## Workflow behavior

`.github/workflows/ufc_score_event.yml`:

- trigger: `workflow_dispatch`;
- input: `features_key`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 60 minutes;
- repository permission: `contents: read`;
- installs `requirements.txt`;
- command: `python process/score_target_event.py`.

The workflow does not expose `MODEL_KEY` as a dispatch input and does not automatically train a model or rebuild features first.

## Model-artifact detection

The script constructs an S3 client and checks `MODEL_KEY` with `s3_exists()`.

### Model object absent

If the object is not found, scoring uses `heuristic_probabilities()` and records:

`scoring_method=heuristic`

### Model object present

If the object exists, the script reads and unpickles it.

Current training artifacts are dictionaries containing:

- `model` — fitted scikit-learn pipeline;
- `feature_cols` — actual trained feature list.

The scorer supports a legacy/non-dictionary artifact by treating the entire unpickled object as the model and falling back to the trainer's `FEATURE_COLS` constant.

After successful model probability calculation it records:

`scoring_method=trained_model`

This label does not distinguish Random Forest from the training-time `dummy_prior` estimator. To identify the trained estimator type, inspect the model-training metrics/artifact generation, not only the prediction row.

## Pickle trust boundary

The scorer uses `pickle.loads()` on the S3 model object. Pickle can execute code during deserialization and must be treated as trusted internal artifact material.

Do not point `MODEL_KEY` at arbitrary/untrusted objects. Live S3 write restrictions and artifact-integrity controls are not established by repository source.

## Trained-model probability path

`model_probabilities(model, feature_cols, df)` calls:

`model.predict_proba(df[feature_cols])`

Consequences:

- every artifact feature column must exist in the current feature DataFrame;
- missing columns raise before prediction;
- the model pipeline handles null numeric values through its trained median-imputation step;
- the current feature builder and trained artifact must therefore be semantically/schema compatible.

For two-class estimators, the scorer locates classifier class `1` and returns that probability as fighter 1's win probability.

For a one-class trained estimator:

- only class `1` -> probability `1.0`;
- only class `0` -> probability `0.0`.

This permits a persisted dummy-prior single-class estimator to score through the `trained_model` path, even though it is not a Random Forest.

## Explicit heuristic path

The heuristic uses fourteen directional feature weights:

| Feature | Weight |
| --- | ---: |
| `reach_diff` | `0.020` |
| `height_diff` | `0.015` |
| `slpm_diff` | `0.180` |
| `sapm_diff` | `-0.150` |
| `td_avg_diff` | `0.110` |
| `sub_avg_diff` | `0.090` |
| `str_acc_diff` | `0.012` |
| `str_def_diff` | `0.012` |
| `td_acc_diff` | `0.008` |
| `td_def_diff` | `0.008` |
| `wins_diff` | `0.020` |
| `losses_diff` | `-0.035` |
| `recent_fights_diff` | `0.015` |
| `news_flag_diff` | `-0.020` |

`safe_num()` converts missing, null, or unparseable values to `0.0` for the heuristic.

The base heuristic score is the sum of weighted feature differences. It then adds current market-context adjustments when implied-probability columns are present through:

- `+ 0.35 * (f1_implied_prob - 0.5)`;
- `- 0.35 * (f2_implied_prob - 0.5)`.

The final raw score is clipped to `[-4.0, 4.0]` and transformed with a sigmoid.

This is explicit fallback code, not learned model behavior and not a recommendation/staking system.

## Heuristic market-missing behavior

Because `safe_num()` maps missing implied probabilities to `0.0`, the heuristic treats a missing single-side implied probability as zero rather than neutral `0.5`. If both sides are missing, the two `-0.5` offsets cancel; if only one side is missing, the market adjustment can be distorted.

This limitation applies only to the heuristic path. The trained model does not directly use these implied-probability fields unless they were separately part of its stored feature list, which the current trainer's `FEATURE_COLS` does not include.

## Predicted winner and probabilities

The output records:

- `fighter_1_win_probability` = calculated probability;
- `fighter_2_win_probability` = `1 - fighter_1_win_probability`;
- `predicted_winner` = fighter 1 when fighter 1 probability is `>= 0.5`, otherwise fighter 2.

At exactly `0.5`, fighter 1 is selected by the tie rule.

## Confidence bucket

`confidence_bucket(prob)` uses distance from `0.5`:

- `high` when `abs(prob - 0.5) >= 0.20`;
- `medium` when `>= 0.10` but `< 0.20`;
- `low` otherwise.

The same thresholds apply to trained-model and heuristic probabilities.

Confidence is therefore a deterministic probability-distance label, not a separately calibrated uncertainty estimate.

## `top_signals` provenance

`build_top_signals()` always uses `HEURISTIC_WEIGHTS`, regardless of `scoring_method`.

For each heuristic feature it calculates:

`feature_value * heuristic_weight`

then selects the three largest absolute contributions and renders strings such as:

`feature=contribution`

### Critical interpretation rule

For `scoring_method=trained_model`, `top_signals` is **not** Random Forest feature attribution, SHAP, permutation importance, or a local explanation of the trained model prediction. It is a separate heuristic-weight summary calculated from the same input row.

Do not describe `top_signals` as “the model's top drivers” when the trained estimator path was used.

## Market-comparison output fields

If `f1_implied_prob` exists in the feature DataFrame, the scorer writes:

- `fighter_1_market_implied_prob`;
- `fighter_1_model_market_delta` = fighter 1 score probability minus implied probability.

If `f2_implied_prob` exists, it writes:

- `fighter_2_market_implied_prob`;
- `fighter_2_model_market_delta`.

### Naming limitation

These output names use `model_market_delta` even when `scoring_method=heuristic`. In that case the delta is actually **heuristic probability minus market implied probability**, not trained-model probability minus market.

Consumers must inspect `scoring_method` before interpreting these fields. The fields are analytical comparison signals only, not wagering instructions.

## Output schema

Always written:

- `event_name`;
- `event_slug`;
- `fighter_1_name`;
- `fighter_2_name`;
- `weight_class`;
- `scoring_method`;
- `fighter_1_win_probability`;
- `fighter_2_win_probability`;
- `predicted_winner`;
- `confidence_bucket`;
- `top_signals`.

Conditionally written when corresponding feature columns exist:

- `fighter_1_market_implied_prob`;
- `fighter_1_model_market_delta`;
- `fighter_2_market_implied_prob`;
- `fighter_2_model_market_delta`.

## S3 products

The event slug is taken from the first output row.

Outputs:

- `processed/ufc/{event_slug}_predictions.csv`;
- `processed/ufc/parquets/{event_slug}_predictions.parquet`.

An empty feature dataset reaches `.iloc[0]` and fails rather than writing an empty prediction product.

## Normal operating sequence

1. Build and validate current-event features.
2. Determine whether the intended trained model artifact should exist.
3. If trained inference is required, verify the model/metrics artifacts are the intended generation before scoring.
4. Dispatch `UFC Score Event (Manual)` with the exact event feature key.
5. Inspect `scoring_method` in the prediction output.
6. If `heuristic` was unexpected, restore/train the intended model and rescore before reporting.
7. Validate matchup count/probabilities and investigate feature-builder duplicates before report generation.
8. Treat `top_signals` as heuristic-weight context, not trained-model attribution.

## Validation checks

At minimum:

- output is non-empty;
- event slug is correct;
- matchup count is expected;
- every row has an understood `scoring_method`;
- trained inference did not unexpectedly become heuristic because the model object was absent;
- probabilities are numeric and in `[0,1]`;
- fighter 1 and fighter 2 probabilities sum to approximately `1`;
- current feature columns satisfy the artifact feature contract;
- market-comparison fields are interpreted according to `scoring_method`;
- `top_signals` is not presented as trained-model explanation.

## Failure modes

- missing/unreadable features object;
- empty feature dataset;
- missing required identity/output columns in feature data;
- existing corrupt/untrusted pickle object;
- artifact missing expected model structure;
- artifact feature column absent from current feature DataFrame;
- estimator/probability API incompatibility;
- classifier classes do not contain class `1` in an unexpected multi-class artifact;
- duplicated feature rows propagate into duplicated predictions;
- missing model object silently changes intended trained inference into the documented heuristic path unless the operator checks `scoring_method`;
- S3 output write failure.

## Rerun and recovery

### Unexpected heuristic

If `scoring_method=heuristic` but a trained estimator was intended:

1. verify/train the intended model artifact;
2. verify its feature contract matches current features;
3. rerun scoring;
4. confirm rows now record `trained_model`;
5. regenerate downstream reports.

### Corrupt/incompatible model

Correct or regenerate the model artifact and rerun scoring. Do not delete/rename the object merely to force heuristic fallback unless that is an explicit reviewed operational decision.

### Feature changes

Rebuild current features and, where semantics changed, rebuild historical training data/retrain before rescoring.

### Duplicate rows

Fix the upstream feature-row issue and rerun scoring. Report-generation deduplication should not be treated as a substitute for a correct inference input.

## Security considerations

- treat the pickle model object as trusted internal code material;
- never publish AWS credentials or secret values;
- the scoring workflow needs only `contents: read`;
- market comparison remains analytical and does not authorize wagering actions;
- live S3/IAM controls are not proven by source.

## Limitations

- model presence rather than a required-mode flag controls trained vs heuristic path;
- no automatic check that current model metrics describe the loaded pickle generation;
- `trained_model` does not distinguish Random Forest from dummy-prior training fallback;
- heuristic missing values are coerced to zero;
- heuristic market adjustment can be distorted by one-sided missing implied probability;
- `top_signals` is heuristic attribution even on trained rows;
- `model_market_delta` names are retained for heuristic rows;
- confidence buckets are not calibrated uncertainty measures;
- tie probability selects fighter 1;
- no schema/run/model-version metadata is written into prediction rows.

## Related documentation

- [degenerate_investigator Matchup Feature Engineering](degenerate-investigator-matchup-feature-engineering.md)
- [degenerate_investigator UFC Winner-Model Training](degenerate-investigator-ufc-winner-model-training.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Any change to model-artifact loading, fallback conditions, probability handling, heuristic weights, confidence thresholds, `top_signals`, comparison-field naming, or prediction schema must update this page and the report-generator documentation together so scoring provenance remains visible end to end.
