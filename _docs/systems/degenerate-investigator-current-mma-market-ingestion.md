---
title: degenerate_investigator Current MMA Market-Context Ingestion
summary: Source-grounded internal data-contract documentation for the current MMA market-context ingestion stage, including normalization, S3 products, workflow behavior, failure handling, and downstream analytical boundaries.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Current MMA Market-Context Ingestion

## Purpose

This stage creates the current MMA market-context snapshot consumed optionally by matchup feature engineering and target-event scoring. It normalizes external market-price rows into a stable tabular contract and writes fixed CSV/Parquet products to S3.

The data is an analytical comparison input only. The repository does not implement staking, wager sizing, bookmaker selection, bankroll management, or bet execution. This page does not provide instructions for obtaining access to, using, or selecting external wagering services.

## Source paths

- implementation: `extract/odds_current_mma.py`;
- workflow: `.github/workflows/ufc_pull_odds.yml`;
- shared storage: `common/io_helpers.py`.

Important functions:

- `american_to_decimal()`;
- `fetch_the_odds_api()`;
- `normalize_odds()`;
- `main()`.

The provider-specific fetch function exists in source, but external service-access details are intentionally outside this documentation boundary. Operational documentation here starts at the configured ingestion stage and its normalized data contract.

## Runtime configuration

Core storage configuration:

- `S3_BUCKET` — source default `degenerative-investigator`;
- `AWS_REGION` — source default `us-east-2`.

The source also expects a provider credential through the environment. Its value must never be persisted in documentation, logs, examples, or repository files. The workflow obtains that credential through a GitHub secret and exposes no manual workflow input for it.

Additional source-level market filters/configuration exist for region, market, and optional provider filtering. They are implementation configuration, not wagering recommendations. The committed workflow leaves its provider filter blank and does not expose these filters as workflow-dispatch inputs.

## Fetch and normalization boundary

`main()`:

1. resolves storage/configuration values;
2. obtains the configured external market payload through `fetch_the_odds_api()`;
3. passes the payload to `normalize_odds()`;
4. writes the resulting DataFrame as paired CSV and Parquet objects.

`normalize_odds()` iterates:

- events;
- each event's provider/bookmaker entries;
- each market;
- each outcome.

Outcomes with no numeric price are skipped. For accepted outcomes, the source records the provider-supplied American-style price and a decimal representation calculated by `american_to_decimal()`.

The conversion function is a format normalization step only; it is not a recommendation, staking rule, or profitability calculation.

## Output schema

The normalized DataFrame contains 14 fields:

| Field | Meaning / construction |
| --- | --- |
| `event_id` | External event identifier. |
| `event_name` | Concatenated home/away names in `A vs B` form. |
| `event_slug` | Slug generated from the two participant names. |
| `commence_time` | External event start timestamp. |
| `fighter_1_name` | External `home_team` value. |
| `fighter_2_name` | External `away_team` value. |
| `bookmaker_key` | Provider/bookmaker key from the payload. |
| `bookmaker_title` | Provider/bookmaker display title. |
| `market_key` | Market identifier from the payload. |
| `outcome_name` | Participant/outcome name associated with the row. |
| `american_price` | Provider-supplied American-style numeric price. |
| `decimal_price` | Equivalent normalized decimal representation. |
| `last_update` | Provider/bookmaker update timestamp. |
| `extracted_at` | UTC timestamp generated once for the normalization batch. |

This is a provider-level/outcome-level table: one fight can produce multiple rows across providers and outcomes.

## S3 products

Fixed outputs:

- `raw/odds/current_mma_odds.csv`;
- `raw/odds/parquets/current_mma_odds.parquet`.

A successful rerun replaces the logical current market-context snapshot. The repository does not create an event-versioned or extraction-timestamped object key for this stage.

S3 versioning/retention, if configured, is live AWS state and is not established by repository source.

## Workflow behavior

`.github/workflows/ufc_pull_odds.yml`:

- trigger: `workflow_dispatch`;
- workflow inputs: none;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 60 minutes;
- repository permission: `contents: read`;
- installs `requirements.txt`;
- command: `python extract/odds_current_mma.py`.

The workflow receives AWS configuration through GitHub secrets, fixes `S3_BUCKET` to `degenerative-investigator`, and invokes the ingestion stage directly. It is not automatically chained to event ingestion or feature building.

## Empty-result behavior

`normalize_odds()` raises `RuntimeError` if it produces no normalized rows. Therefore a successfully completed workflow is expected to have produced at least one market-context row and written the paired S3 products.

An empty result is treated as an ingestion failure rather than as a valid empty snapshot.

## Downstream analytical use

The current feature builder reads `raw/odds/current_mma_odds.csv` through its optional market-context path. It uses participant-name matching to create matchup context, and later scoring can expose model-vs-market comparison fields.

Market-context availability is optional for feature building: an unavailable/read-failing market S3 object is converted to an empty lookup by the feature builder. This means downstream feature generation can succeed without current market context.

A successful feature-build workflow therefore does not prove that this enrichment was present or matched correctly.

## Validation checks

Before treating the snapshot as useful analytical context, verify:

- the ingestion workflow succeeded;
- the fixed CSV/Parquet objects correspond to the intended current extraction;
- `fighter_1_name`, `fighter_2_name`, `outcome_name`, and `event_id` are populated for expected rows;
- prices are numeric and non-null on retained rows;
- `extracted_at` reflects the intended ingestion run;
- the target event/fighter names can be matched by downstream feature logic;
- the snapshot has not been unintentionally replaced by a stale or unrelated extraction.

The repository does not implement automated target-event coverage thresholds for this stage.

## Failure modes

- missing/invalid external provider configuration;
- external request timeout, transport error, rate-limit response, or upstream schema change;
- provider payload contains no normalizable rows;
- missing participant names can break source assumptions used to build `event_name`;
- non-numeric price values can fail conversion;
- S3 authentication, region, bucket, or write failure;
- downstream fighter-name mismatch produces no useful market lookup even when ingestion itself succeeded;
- fixed-key overwrite can replace a previously useful snapshot with a newer but less relevant one.

## Rerun and recovery

If ingestion fails before S3 publication, correct the configuration/upstream issue and rerun only this workflow.

If a bad or irrelevant snapshot is successfully written, rerun the same stage when the intended source data is available. Because outputs use fixed keys, the next successful run becomes the logical current snapshot.

After refreshing market context for an event whose features were already built, rerun current matchup feature engineering and then any downstream scoring/report stages that should incorporate the updated analytical comparison signal.

No automatic downstream invalidation or workflow chaining exists.

## Security considerations

- Never document or commit provider credential values.
- Never paste credential values into workflow inputs or report artifacts.
- AWS credential values are also secret and remain outside documentation.
- This workflow requests only `contents: read`; it does not need repository write access.
- Live provider-account permissions, quotas, billing, and AWS IAM policy scope are not established by repository source.

## Limitations

- fixed current-snapshot keys rather than event-versioned history;
- no automatic association with the currently selected UFC event;
- downstream name matching can fail because external naming is not canonicalized to UFC Stats identities;
- no automated coverage/recency gate before feature building;
- provider/upstream schema and availability can change independently of this repository;
- the feature builder treats missing market context as optional;
- this system is analytical only and contains no staking, execution, or bookmaker-recommendation logic.

## Related documentation

- [degenerate_investigator Repository and UFC Analytics Architecture](../repositories/degenerate-investigator.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [degenerate_investigator Current UFC Event and Fighter Ingestion](degenerate-investigator-current-ufc-ingestion.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Changes to normalized column names, fixed S3 keys, external participant mapping, optionality in the feature builder, or market-price conversion semantics should update this page with the corresponding code change. Keep future documentation strictly analytical and do not expand it into wagering instructions or external service-access guidance.
