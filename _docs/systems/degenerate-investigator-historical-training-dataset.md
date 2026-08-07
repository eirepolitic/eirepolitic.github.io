---
title: degenerate_investigator Historical Training-Dataset Builder
summary: Source-grounded documentation for constructing the supervised UFC winner-model training dataset from historical fights and fighter profiles, including target inheritance, feature directionality, mirrored rows, S3 products, workflow behavior, failure modes, and leakage limitations.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Historical Training-Dataset Builder

## Purpose

`process/build_historical_training_dataset.py` transforms historical fight results and historical fighter profiles into the supervised dataset consumed by UFC winner-model training.

The output uses the same directional feature family as current-event feature engineering: **fighter 1 minus fighter 2**. For every base historical fight row, the builder also creates a mirrored fighter-order row, flips the winner target, and negates every directional difference.

## Source paths

- implementation: `process/build_historical_training_dataset.py`;
- workflow: `.github/workflows/ufc_build_training_dataset.yml`;
- shared feature normalization: `process/ufc_feature_builder.py` via `build_fighter_lookup()`;
- shared S3 I/O: `common/io_helpers.py`.

Source constant:

- `DIFF_COLS` — the fourteen model-oriented difference columns.

## Inputs

Historical fights:

- `HISTORICAL_FIGHTS_KEY`;
- source/workflow default `raw/ufc/fights/historical_fights.csv`.

Historical profiles:

- `HISTORICAL_FIGHTER_PROFILES_KEY`;
- source/workflow default `raw/ufc/fighters/historical_fighter_profiles.csv`.

Storage:

- `S3_BUCKET`, default `degenerative-investigator`;
- `AWS_REGION`, default `us-east-2`.

Both historical inputs are hard dependencies; reads are not wrapped as optional.

## Identity matching

Unlike current-event feature engineering, which joins profiles primarily by normalized fighter name, the historical training builder matches profiles by normalized fighter URL.

For fight rows it creates:

- `fighter_1_key` from `fighter_1_url`;
- `fighter_2_key` from `fighter_2_url`.

For profiles it creates `fighter_url_key` from `fighter_url`.

The profile table is duplicated with `f1_` and `f2_` prefixes and left-joined by URL key.

This is generally a stronger identity contract than display-name matching, but missing/placeholder historical profiles can still produce null feature values.

## Shared profile normalization

The builder imports `build_fighter_lookup()` from current feature engineering. Therefore historical and current pipelines share the same raw-profile conversions for:

- height -> inches;
- reach -> inches;
- rate/average fields -> floats;
- striking/takedown percentages -> numeric percentage-point values.

Changes to `build_fighter_lookup()` affect both current inference features and historical training features.

## Target source of truth

The input historical-fights object already contains `fighter_1_win`, produced by `extract/ufc_historical_fights.py`.

The training builder does not independently re-parse fight outcomes. It carries the historical target into `df_base`, then mirrors it for the reversed row.

Therefore the upstream historical extraction rule is the label source of truth. Changes to historical result parsing change model labels and require rebuilding the training dataset and trained model.

## Difference feature definitions

The builder calculates thirteen profile-derived directional differences plus one constant historical news difference:

| Feature | Base-row definition |
| --- | --- |
| `height_diff` | fighter 1 height inches - fighter 2 height inches |
| `reach_diff` | fighter 1 reach inches - fighter 2 reach inches |
| `slpm_diff` | fighter 1 SLpM - fighter 2 SLpM |
| `sapm_diff` | fighter 1 SApM - fighter 2 SApM |
| `td_avg_diff` | fighter 1 takedown average - fighter 2 takedown average |
| `sub_avg_diff` | fighter 1 submission average - fighter 2 submission average |
| `str_acc_diff` | fighter 1 striking accuracy - fighter 2 striking accuracy |
| `str_def_diff` | fighter 1 striking defence - fighter 2 striking defence |
| `td_acc_diff` | fighter 1 takedown accuracy - fighter 2 takedown accuracy |
| `td_def_diff` | fighter 1 takedown defence - fighter 2 takedown defence |
| `wins_diff` | fighter 1 scraped wins - fighter 2 scraped wins |
| `losses_diff` | fighter 1 scraped losses - fighter 2 scraped losses |
| `recent_fights_diff` | fighter 1 scraped history-row count - fighter 2 count |
| `news_flag_diff` | fixed to `0.0` for every base historical row |

Each profile-derived operand is coerced with `pd.to_numeric(..., errors="coerce")`, so missing/unparseable values become `NaN`.

## Historical-news limitation

The training builder does not load historical news data. It explicitly writes:

`news_flag_diff = 0.0`

for all historical base rows.

Current-event feature engineering, however, can derive `news_flag_diff` from the current news snapshot. This creates a train/inference asymmetry: the model can be trained on a feature that is constant zero historically but non-zero at inference time if that feature is retained by training.

Model training must therefore be interpreted together with the recorded `available_features`/feature-column artifact rather than assuming every current feature has learned historical variation.

## Kept base schema

Before mirroring, `df_base` keeps:

- `event_name`;
- `event_url`;
- `fighter_1_name`;
- `fighter_2_name`;
- `weight_class`;
- `fighter_1_win`;
- all fourteen `DIFF_COLS`.

Upstream URLs/profile raw columns are not kept in the final training dataset.

## Mirrored-row construction

`df_mirror` is a copy of `df_base` with these transformations:

1. swap `fighter_1_name` and `fighter_2_name`;
2. set `fighter_1_win = 1 - fighter_1_win` after numeric coercion;
3. multiply every difference column by `-1` after numeric coercion.

Base and mirror frames are concatenated. Rows whose target is null are dropped, then `fighter_1_win` is cast to integer.

When upstream targets are valid binary values, the intent is two directional training rows per historical fight.

## Mirroring implications

Mirroring makes the feature/target orientation symmetric by construction, but it does not create independent fights. The two rows from one fight contain the same underlying event/outcome information in reversed orientation.

The current model trainer later performs a random row-level train/test split. It does not group mirrored pairs by original fight. Therefore a base row can be placed in training while its mirrored counterpart is placed in testing, creating potential evaluation leakage and overly optimistic metrics.

This is a current methodological limitation and should be considered when interpreting model metrics. A future grouped split would be an implementation/model-design change.

## S3 products

Fixed outputs:

- `processed/ufc/training_dataset.csv`;
- `processed/ufc/parquets/training_dataset.parquet`.

A successful rebuild replaces the logical current training dataset. The source does not version datasets by historical window, feature schema, or build timestamp.

## Workflow

`.github/workflows/ufc_build_training_dataset.yml`:

- trigger: `workflow_dispatch`;
- workflow inputs: none;
- fixed historical-fights key in environment;
- fixed historical-profile key in environment;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 120 minutes;
- repository permission: `contents: read`;
- installs `requirements.txt`;
- command: `python process/build_historical_training_dataset.py`.

The workflow cannot select alternate historical input keys through dispatch inputs without code/workflow changes.

## Normal operating sequence

1. Rebuild historical fights for the intended completed-event window.
2. Rebuild historical fighter profiles with full coverage (`TEST_ROWS=0`).
3. Review profile error rows/coverage.
4. Dispatch `UFC Build Training Dataset (Manual)`.
5. Verify output row count and target values.
6. Assess missing feature coverage.
7. Only then train/retrain the UFC winner model.

Because the output is fixed-key, ensure no truncated historical-profile test snapshot is present before building training data.

## Validation checks

At minimum:

- dataset is non-empty;
- `fighter_1_win` is present and integer/binary as expected;
- row count is approximately twice the number of valid base historical fight rows;
- each expected `DIFF_COLS` field exists;
- mirrored rows have swapped fighter names, inverted target, and negated differences;
- profile-derived features have acceptable non-null coverage;
- historical profile placeholder/error rows have not created unexpectedly sparse features;
- `news_flag_diff` is understood to be constant zero historically;
- historical source window corresponds to the intended training population.

The builder itself does not enforce minimum coverage or class balance.

## Failure modes

- missing historical fights/profile S3 object;
- required URL/profile columns missing;
- malformed profile values producing widespread `NaN` features;
- truncated historical-profile snapshot from a prior `TEST_ROWS>0` run;
- upstream label/parser errors carried directly into `fighter_1_win`;
- target values outside the intended binary contract produce incorrect mirror semantics;
- S3 write/authentication failure;
- successful rebuild silently changes training population when historical ingestion scope changed;
- no dataset version metadata ties the output to exact source-object versions.

## Rerun and recovery

Rebuild this dataset whenever any of these change materially:

- historical completed-event window;
- historical fight label parsing;
- historical fighter-profile snapshot;
- shared profile normalization;
- directional feature definitions;
- feature names or semantics.

After rebuilding, retrain the model before relying on the new dataset for inference. If current feature semantics also changed, rebuild current-event features before rescoring.

No automatic model invalidation or retraining occurs.

## Security considerations

This stage consumes only S3 data and requires no external enrichment credentials. The workflow uses AWS secret names and `contents: read` repository permission.

Never publish credential values or personal/account identifiers. Historical data source/versioning and live IAM state remain separate concerns.

## Limitations

- fixed-key dataset with no schema/build version metadata;
- no historical news enrichment; `news_flag_diff` is constant zero;
- missing numeric features are retained for later model imputation rather than rejected here;
- no minimum row count, feature-completeness threshold, or class-balance gate in this builder;
- row mirroring doubles examples but not independent information;
- random row-level model splitting can separate mirror pairs and cause evaluation leakage;
- target quality depends entirely on upstream historical result parsing;
- workflow cannot select alternate S3 history/profile keys through manual inputs.

## Related documentation

- [degenerate_investigator Historical UFC Fight and Fighter-Profile Ingestion](degenerate-investigator-historical-ufc-ingestion.md)
- [degenerate_investigator Matchup Feature Engineering](degenerate-investigator-matchup-feature-engineering.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Any change to target inheritance, URL identity matching, shared profile conversions, `DIFF_COLS`, mirrored-row logic, or historical-news treatment is a training-contract change and should be documented together with the model-training behavior and regenerated model artifacts.
