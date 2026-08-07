---
title: degenerate_investigator Matchup Feature Engineering
summary: Source-grounded documentation for building current-event UFC matchup features from event cards, fighter profiles, optional market context, and optional recent-news enrichment, including exact transformations, joins, feature definitions, S3 products, and failure modes.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Matchup Feature Engineering

## Purpose

`process/ufc_feature_builder.py` converts the current event card and fighter-profile snapshot into a matchup-level feature dataset used by target-event scoring. Current market context and fighter recent-news data are optional enrichments.

The feature contract is directional: numerical difference features are calculated as **fighter 1 minus fighter 2**. That orientation must remain consistent with model training and inference.

## Source paths

- implementation: `process/ufc_feature_builder.py`;
- workflow: `.github/workflows/ufc_build_features.yml`;
- shared S3 I/O: `common/io_helpers.py`.

Important functions:

- `parse_height_to_inches()`;
- `parse_reach_to_inches()`;
- `parse_percent()`;
- `parse_float()`;
- `american_to_implied_prob()`;
- `build_fighter_lookup()`;
- `build_news_flags()`;
- `build_market_lookup()`;
- `main()`.

## Inputs

Required:

- `EVENT_CARD_KEY` — no script default; required by `get_env(..., required=True)`;
- fighter-profile object from `FIGHTER_PROFILES_KEY`, default `raw/ufc/fighters/fighter_profiles.csv`.

Optional enrichment inputs:

- `ODDS_KEY`, default `raw/odds/current_mma_odds.csv`;
- `NEWS_KEY`, default `raw/news/fighter_recent_news.csv`.

Storage:

- `S3_BUCKET`, default `degenerative-investigator`;
- `AWS_REGION`, default `us-east-2`.

The event card and fighter profiles are hard dependencies. Market/news reads are wrapped in broad exception handlers and become empty lookup tables on any read/processing exception.

## Workflow

`.github/workflows/ufc_build_features.yml`:

- trigger: `workflow_dispatch`;
- input: `event_card_key`;
- committed default: `raw/ufc/events/ufc-327-prochazka-vs-ulberg_card.csv`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 60 minutes;
- repository permission: `contents: read`;
- command: `python process/ufc_feature_builder.py`.

The committed event-card default is event-specific. Verify it before every run for a different target event.

## Fighter-profile normalization

`build_fighter_lookup()` creates a lowercase/trimmed `fighter_name_key` and derives numeric forms of raw profile strings.

### Height

`parse_height_to_inches()` expects a feet/inches pattern such as `N' M` and returns total inches. Non-matching values become `NaN`.

### Reach

`parse_reach_to_inches()` removes double quotes, extracts the first integer, and returns it as inches. Non-matching values become `NaN`.

### Rate/average fields

These raw fields are converted with `parse_float()`:

- `slpm` -> `slpm_num`;
- `sapm` -> `sapm_num`;
- `td_avg` -> `td_avg_num`;
- `sub_avg` -> `sub_avg_num`.

Failed conversion becomes `NaN`.

### Percentage fields

These fields have `%` removed and are converted to numeric percentage-point values, not fractions:

- `str_acc` -> `str_acc_num`;
- `str_def` -> `str_def_num`;
- `td_acc` -> `td_acc_num`;
- `td_def` -> `td_def_num`.

For example, a raw `52%` becomes numeric `52.0`, not `0.52`.

## Fighter matching

The event card creates:

- `fighter_1_key` from lowercased/trimmed `fighter_1_name`;
- `fighter_2_key` from lowercased/trimmed `fighter_2_name`.

The normalized fighter-profile table is duplicated with `f1_` and `f2_` prefixes and left-joined by name key.

Missing name matches remain in the matchup row with null profile-derived columns. There is no explicit completeness assertion after the joins.

## News aggregation

`build_news_flags()` returns one row per normalized fighter name:

- `news_flag_count` = pandas `count` of non-null `label` values;
- `news_summary` = first `summary` in the group.

If the news input is empty, an empty lookup with the expected columns is returned.

### Important semantic limitation

`news_flag_count` is a count of rows with non-null labels. The ingestion layer uses labels such as `parse_error` and `no_recent_items`, and this feature function does not exclude them. Therefore `news_flag_count` is **not** guaranteed to mean “number of verified adverse news signals”. It is the current count-of-label-rows implementation.

The resulting directional feature is `f1_news_flag_count - f2_news_flag_count` after numeric coercion.

## Market-context aggregation

`build_market_lookup()`:

1. filters to rows whose `market_key` equals `h2h`;
2. creates a lowercase/trimmed key from `outcome_name`;
3. coerces `american_price` to numeric;
4. calculates `implied_prob` through `american_to_implied_prob()`;
5. sorts by `event_name`, fighter key, and `last_update`;
6. keeps the last row per `(event_name, fighter_name_key)`.

This produces at most one retained provider row for each fighter/event-name pair after sorting; it does not aggregate multiple sources mathematically.

### Join limitation

When the market lookup is merged into the event-card features, the join condition uses only `fighter_name_key`. It does **not** also join on the UFC event identity or market `event_name`.

Therefore, if the current market snapshot contains the same fighter in multiple event rows, the left join can duplicate a UFC matchup row. Joining both fighters can further multiply rows. Treat unexpected duplicate matchup rows as a possible market-join issue.

The retained market fields are:

- `f1_event_name`, `f1_american_price`, `f1_implied_prob`;
- `f2_event_name`, `f2_american_price`, `f2_implied_prob`.

Market-context fields are analytical inputs only; they are not staking or execution instructions.

## Difference feature contract

The builder creates these fourteen signed differences:

| Feature | Definition |
| --- | --- |
| `height_diff` | `f1_height_in - f2_height_in` |
| `reach_diff` | `f1_reach_in - f2_reach_in` |
| `slpm_diff` | `f1_slpm_num - f2_slpm_num` |
| `sapm_diff` | `f1_sapm_num - f2_sapm_num` |
| `td_avg_diff` | `f1_td_avg_num - f2_td_avg_num` |
| `sub_avg_diff` | `f1_sub_avg_num - f2_sub_avg_num` |
| `str_acc_diff` | `f1_str_acc_num - f2_str_acc_num` |
| `str_def_diff` | `f1_str_def_num - f2_str_def_num` |
| `td_acc_diff` | `f1_td_acc_num - f2_td_acc_num` |
| `td_def_diff` | `f1_td_def_num - f2_td_def_num` |
| `wins_diff` | `f1_career_wins_scraped - f2_career_wins_scraped` |
| `losses_diff` | `f1_career_losses_scraped - f2_career_losses_scraped` |
| `recent_fights_diff` | `f1_recent_fights_scraped - f2_recent_fights_scraped` |
| `news_flag_diff` | `f1_news_flag_count - f2_news_flag_count` |

Each operand is passed through `pd.to_numeric(..., errors="coerce")`, so missing/unparseable values propagate as `NaN` rather than being filled here.

## Output structure

The feature output is a wide joined dataset. It includes:

- all event-card columns;
- `fighter_1_key`, `fighter_2_key`;
- prefixed raw and normalized profile columns for both fighters;
- prefixed news aggregate columns;
- selected prefixed market-context fields;
- the fourteen directional difference features.

The script takes `event_slug` from `df["event_slug"].iloc[0]`. An empty post-input DataFrame therefore fails rather than emitting an empty feature object.

## S3 products

For the first row's event slug:

- `processed/ufc/{event_slug}_fight_features.csv`;
- `processed/ufc/parquets/{event_slug}_fight_features.parquet`.

A rerun for the same event slug replaces the logical feature products.

## Normal operating sequence

1. Build the intended event card.
2. Refresh the current fighter-profile snapshot for that card.
3. Optionally refresh current market context and fighter recent-news enrichment.
4. Dispatch `UFC Build Features (Manual)` with the exact event-card key.
5. Confirm the output event slug matches the intended target event.
6. Check row count against the event card and investigate unexpected duplication.
7. Check profile-derived feature coverage/nulls.
8. Check whether optional enrichment was actually joined when expected.
9. Use the resulting feature key for target-event scoring.

## Validation checks

At minimum:

- output is non-empty;
- event slug is correct;
- expected matchups are present;
- row count has not increased unexpectedly versus the event card;
- both fighter profile name matches succeeded where expected;
- the fourteen difference columns exist;
- numeric differences have plausible non-null coverage;
- optional enrichment fields are interpreted as optional and not silently assumed present;
- market event-name fields, when present, correspond to the intended fighter/event context;
- `news_flag_count` is not misinterpreted as a validated adverse-news count.

## Failure modes

- missing/incorrect `EVENT_CARD_KEY`;
- missing profile object or required profile columns;
- empty event-card input causing `.iloc[0]` failure;
- fighter-name mismatch causing null profile joins;
- unexpected raw profile format producing `NaN` conversions;
- optional market/news exceptions being hidden by broad fallback to empty lookup;
- market snapshot containing a fighter in multiple events causing duplicate matchup rows;
- missing news producing null news differences rather than a filled zero in the current-event feature builder;
- S3 write/authentication failure;
- event-specific workflow default used accidentally for another event.

## Rerun and recovery

- Wrong event card: rerun with the correct `event_card_key`.
- Profiles refreshed/corrected: rebuild features.
- Market/news refreshed and intended for inference: rebuild features.
- Feature logic changed: rebuild current features and the historical training dataset before retraining, because model-training and inference feature semantics must stay aligned.
- Duplicate rows caused by market joins: correct the source/feature-join implementation or input snapshot before scoring; do not assume downstream deduplication restores the intended feature row.

No downstream stage is triggered automatically.

## Security considerations

The feature job requires only S3 access and `contents: read` repository permission. It does not need external enrichment credentials directly because it consumes enrichment outputs from S3.

Do not include AWS credential values or personal/account identifiers in documentation. Market context remains analytical only.

## Limitations

- fighter joins use normalized names, not stable UFC identifiers;
- market join does not enforce event identity;
- optional market/news read failures are swallowed into empty lookups;
- news flag semantics are row-count based;
- missing numeric values are not imputed at feature-build time;
- output is wide and carries upstream raw columns as well as model-oriented differences;
- no explicit duplicate-matchup or completeness assertion is implemented;
- event-card workflow default is event-specific;
- no schema-version field is written with the feature dataset.

## Related documentation

- [degenerate_investigator Current UFC Event and Fighter Ingestion](degenerate-investigator-current-ufc-ingestion.md)
- [degenerate_investigator Current MMA Market-Context Ingestion](degenerate-investigator-current-mma-market-ingestion.md)
- [degenerate_investigator Fighter Recent-News Enrichment](degenerate-investigator-fighter-recent-news-enrichment.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Any change to name matching, unit conversion, optional-enrichment handling, market row selection/join logic, news aggregation, difference-feature names, or directionality must be synchronized with historical training-dataset construction and model documentation in the same development sequence.
