---
title: degenerate_investigator UFC Winner-Model Training
summary: Source-grounded documentation for UFC winner-model training, including feature selection, median imputation, Random Forest and single-class dummy behavior, train/test splitting, metrics, model artifacts, failure modes, stale-artifact risks, and retraining recovery.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator UFC Winner-Model Training

## Purpose

`process/train_ufc_winner_model.py` trains the classifier consumed by target-event scoring. Its normal estimator is a Random Forest. If the training target contains only one class, the script deliberately trains a `DummyClassifier(strategy="prior")` instead.

The dummy-prior path is a **training fallback estimator**, not the trained Random Forest and not the scoring-time heuristic fallback. These three behaviors must remain distinct in documentation and report interpretation.

## Source paths

- implementation: `process/train_ufc_winner_model.py`;
- workflow: `.github/workflows/ufc_train_model.yml`;
- input dataset builder: `process/build_historical_training_dataset.py`;
- shared S3 I/O: `common/io_helpers.py`.

Important source elements:

- `FEATURE_COLS`;
- `build_pipeline()`;
- `main()`.

## Input

Required runtime input:

- `TRAINING_DATA_KEY` — required by source.

Workflow input:

- `training_data_key` — committed/default value `processed/ufc/training_dataset.csv`.

Storage:

- `S3_BUCKET`, default `degenerative-investigator`;
- `AWS_REGION`, default `us-east-2`.

The input CSV must contain `fighter_1_win`.

## Candidate feature contract

`FEATURE_COLS` contains fourteen directional features:

- `height_diff`;
- `reach_diff`;
- `slpm_diff`;
- `sapm_diff`;
- `td_avg_diff`;
- `sub_avg_diff`;
- `str_acc_diff`;
- `str_def_diff`;
- `td_acc_diff`;
- `td_def_diff`;
- `wins_diff`;
- `losses_diff`;
- `recent_fights_diff`;
- `news_flag_diff`.

The trainer does not require all fourteen. It creates `available_feature_cols` by retaining only candidate columns that both exist and contain at least one non-null value.

Therefore the serialized model's feature contract can vary between training runs. Consumers must use the artifact's stored `feature_cols`, not assume the full constant list was trained.

## Target preparation

The target is converted with:

`pd.to_numeric(df["fighter_1_win"], errors="coerce")`

Rows with null/unparseable targets are removed from `X` and `y`; the remaining target is cast to integer.

The script records `metrics["rows"]` as the original DataFrame row count, while `train_rows` and `test_rows` reflect only the usable target rows after this filtering.

## Minimum-size gate

After target filtering, the script requires at least ten rows. Fewer than ten raises:

`RuntimeError("Training dataset is too small to train a model.")`

There is no stronger minimum per class beyond what the later split/estimator requires.

## Estimator selection

The sorted unique target classes determine the training path.

### Normal path: Random Forest

When two or more target classes are present:

- classifier: `RandomForestClassifier`;
- `n_estimators=300`;
- `random_state=42`;
- `min_samples_leaf=3`.

### Single-class path: dummy prior

When fewer than two target classes are present:

- classifier: `DummyClassifier(strategy="prior")`;
- persisted `model_type`: `dummy_prior`.

This is explicit source behavior for a degenerate training target. It is not evidence that a Random Forest was trained.

## Preprocessing pipeline

`build_pipeline()` creates a scikit-learn `Pipeline` with:

1. a `ColumnTransformer` selecting the run's `available_feature_cols`;
2. a nested numerical pipeline containing `SimpleImputer(strategy="median")`;
3. the selected classifier.

Missing feature values are therefore imputed using medians learned from the training partition, rather than being filled by the feature or training-dataset builders.

## Train/test split

Test size is 20%, with `random_state=42`.

Random-Forest/multi-class path:

- `stratify=y`.

Single-class dummy path:

- no stratification.

The split is row-level. It does not group mirrored rows from the same historical fight, event, fighter, or time period.

### Evaluation leakage limitation

The historical training-dataset builder creates a mirrored counterpart for each base fight row. Since the trainer randomly splits rows, a base row can be in training while its mirrored counterpart is in testing.

This can leak the same underlying fight/outcome structure across partitions and make holdout metrics appear stronger than a truly fight-isolated evaluation. Metrics should be interpreted with this limitation until grouped/time-aware splitting is implemented.

## Additional split failure mode

The stratified multi-class split can fail when a class has too few examples to satisfy scikit-learn's stratification requirements, even when total usable rows are at least ten. The source does not pre-check per-class counts or convert that condition into the dummy path.

## Probability handling

After fitting, the script calls `predict_proba(X_test)`.

### Two-class probability

For a normal two-class estimator, it finds the classifier class index corresponding to class `1` and uses that probability as the positive-class probability.

### One-class probability

For a one-column dummy probability matrix, it checks the estimator's only class:

- only class `1` -> probability vector of `1.0`;
- only class `0` -> probability vector of `0.0`.

Binary predictions are then `1` where probability is at least `0.5`, otherwise `0`.

## Metrics artifact

The script writes `processed/ufc/model_metrics.json` with:

- `rows` — original input row count;
- `train_rows`;
- `test_rows`;
- `accuracy`;
- `log_loss`;
- `features` — actual `available_feature_cols` used;
- `unique_classes`;
- `model_type` — `random_forest` or `dummy_prior`.

`roc_auc` is added only when more than one unique target class exists.

The metrics file contains no model version, training timestamp, source object version, Git commit SHA, historical window identifier, or schema version.

## Serialized model artifact

The script pickles this dictionary to `processed/ufc/model_artifacts.pkl`:

- `model` — fitted scikit-learn pipeline;
- `feature_cols` — actual feature list used for training.

Target-event scoring later unpickles this artifact and uses the stored feature list.

### Pickle security boundary

Python pickle is code-execution-capable when loading untrusted data. The scoring system must treat `model_artifacts.pkl` as a trusted internal artifact and should not load arbitrary/untrusted pickle objects into the pipeline.

Repository source does not prove live S3 write-policy restrictions, object signing, or artifact-integrity controls.

## Feature-importance artifacts

For Random Forest training only, the script writes sorted feature importances to:

- `processed/ufc/feature_importance.csv`;
- `processed/ufc/parquets/feature_importance.parquet`.

Columns:

- `feature`;
- `importance`.

The importances come directly from `model.named_steps["clf"].feature_importances_`.

### Stale-importance risk

When `use_dummy=True`, the script does not write feature importance—and it also does not delete any pre-existing fixed-key feature-importance objects.

Therefore after a prior Random Forest run followed by a dummy-prior run:

- `model_artifacts.pkl` can describe the dummy model;
- `model_metrics.json` can report `model_type=dummy_prior`;
- old feature-importance CSV/Parquet objects can still remain in S3 from the earlier Random Forest.

Never infer current model type from the presence of feature-importance files. Check `model_metrics.json` and the serialized artifact's actual estimator.

## S3 write ordering

The script writes:

1. `model_metrics.json`;
2. `model_artifacts.pkl`;
3. feature-importance files only for Random Forest.

These are separate S3 operations rather than one atomic transaction. A failure between writes can leave mixed-generation artifacts. There is no run identifier tying them together.

## Workflow behavior

`.github/workflows/ufc_train_model.yml`:

- trigger: `workflow_dispatch`;
- input: `training_data_key`;
- default: `processed/ufc/training_dataset.csv`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 180 minutes;
- repository permission: `contents: read`;
- command: `python process/train_ufc_winner_model.py`.

The workflow installs `requirements.txt` and uses GitHub secret names for AWS access/region. It does not automatically run after the training-dataset builder.

## Normal operating sequence

1. Rebuild/validate the intended historical training dataset.
2. Dispatch `UFC Train Model (Manual)` with the intended training-data key.
3. Confirm workflow success.
4. Read `model_metrics.json` and confirm `model_type`.
5. Confirm the actual feature list in metrics/artifact is expected.
6. Interpret accuracy/log-loss/ROC AUC with the mirrored-row leakage limitation.
7. If `model_type=random_forest`, inspect feature importance only as belonging to that run when artifact consistency has been established.
8. Only then use the model artifact for target-event scoring.

## Validation checks

At minimum:

- usable training rows >= 10;
- target classes are understood before training;
- `model_type` matches the expected path;
- `features` contains the intended model inputs;
- train/test counts add up to usable target rows;
- metric values are finite/plausible;
- Random Forest importance rows match the trained feature list;
- stale feature-importance objects are not mistaken for current dummy-model output;
- model artifact and metrics were produced by the same intended training run;
- evaluation limitations are considered before drawing conclusions from holdout performance.

## Failure modes

- training object missing/unreadable;
- missing `fighter_1_win` target;
- all candidate feature columns absent or entirely null;
- fewer than ten usable target rows;
- stratified split failure because a class has too few examples;
- median imputation/model fit error;
- metric calculation error;
- S3 partial-write failure causing mixed-generation metrics/model/importance artifacts;
- dummy-prior run leaving stale prior Random Forest importance files;
- upstream mirrored-pair leakage producing misleadingly optimistic evaluation;
- downstream scoring feature data incompatible with artifact `feature_cols`.

## Rerun and recovery

Retrain whenever:

- the historical training dataset changes materially;
- target construction changes;
- feature names/semantics change;
- shared profile normalization changes;
- model algorithm/hyperparameters change.

After a successful retrain, verify metrics/model artifacts before rescoring current events.

If training fails after writing only some fixed-key artifacts, rerun the complete training stage after correcting the cause; do not assume the remaining objects belong to one consistent generation.

For a dummy-prior run, ignore or remove stale feature-importance objects through an explicit reviewed operational change; the current trainer itself does not clean them up.

## Model source-of-truth rules

- `model_type=random_forest`: Random Forest classifier was trained.
- `model_type=dummy_prior`: single-class dummy fallback was trained.
- scoring `scoring_method=heuristic`: no trained model artifact was used for that prediction.

These labels describe separate code paths. Do not call dummy-prior or heuristic outputs “Random Forest predictions”.

## Security considerations

- never publish AWS credential values;
- treat the S3 pickle artifact as trusted-code material;
- restrict model-artifact write authority in live infrastructure according to an explicit security design; live IAM scope is not proven here;
- the training workflow needs only `contents: read` repository permission;
- no personal/account identifiers belong in model metadata or documentation.

## Limitations

- random row split rather than fight-grouped or temporal validation;
- mirrored-row leakage risk;
- no cross-validation;
- no hyperparameter search;
- no probability calibration stage;
- feature availability can vary per training run;
- historical `news_flag_diff` has no variation in the current training dataset;
- no model/dataset version or training timestamp in artifacts;
- fixed artifact keys are non-atomic across separate writes;
- stale feature importance can survive a dummy run;
- single-class fallback is operationally valid but does not represent a meaningful learned two-class winner model.

## Related documentation

- [degenerate_investigator Historical Training-Dataset Builder](degenerate-investigator-historical-training-dataset.md)
- [degenerate_investigator Matchup Feature Engineering](degenerate-investigator-matchup-feature-engineering.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Any change to `FEATURE_COLS`, estimator type/hyperparameters, imputation, split strategy, metrics, artifact schema, artifact keying/versioning, or single-class behavior should update this page together with scoring documentation and regenerate compatible model artifacts before production inference.
