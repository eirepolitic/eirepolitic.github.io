---
title: degenerate_investigator Historical UFC Fight and Fighter-Profile Ingestion
summary: Source-grounded operating, schema, S3, failure, and rerun documentation for rebuilding historical UFC fight results and the corresponding historical fighter-profile snapshot.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Historical UFC Fight and Fighter-Profile Ingestion

## Purpose

This two-stage pipeline builds the historical UFC Stats inputs used by the supervised training-dataset builder:

1. a fixed-key aggregate of fights from a selected number of completed UFC events;
2. a fixed-key historical fighter-profile snapshot for the unique fighter URLs present in that aggregate.

Both stages are manually dispatched GitHub Actions workflows. They are rebuild jobs, not an incremental append pipeline.

## Source paths

Historical fights:

- `extract/ufc_historical_fights.py`;
- `.github/workflows/ufc_build_history.yml`.

Historical fighter profiles:

- `extract/ufc_historical_fighter_profiles.py`;
- `.github/workflows/ufc_pull_historical_fighter_profiles.yml`;
- reuses `parse_profile()` from `extract/ufc_fighter_profiles.py`.

Shared S3 behavior:

- `common/io_helpers.py`.

## Historical-fight stage

### Functions

`extract/ufc_historical_fights.py` defines:

- `normalize_ufcstats_url()`;
- `fetch_soup()`;
- `completed_event_urls()`;
- `parse_event()`;
- `main()`.

### Runtime configuration

- `S3_BUCKET` — default `degenerative-investigator`;
- `AWS_REGION` — default `us-east-2`;
- `MAX_EVENTS` — default `150` in source;
- `DELAY_BETWEEN_REQUESTS` — default `0.2` seconds in source.

Workflow input:

- `max_events` — manual input with committed default `150`, passed to `MAX_EVENTS`.

`DELAY_BETWEEN_REQUESTS` is not exposed as a workflow input in the current workflow.

### Completed-event discovery

`completed_event_urls(max_events)` fetches the UFC Stats completed-events listing using `statistics/events/completed?page=all`, selects links containing `event-details`, normalizes/deduplicates them in page order, then returns `urls[:max_events]`.

The source therefore means “first N completed-event links returned by the current listing page”, not a date-range query or persisted incremental cursor.

### Event parsing

For each selected event URL, `parse_event()`:

1. fetches the event page;
2. reads the event title;
3. iterates `tr.b-fight-details__table-row` rows;
4. extracts the first two fighter names and fighter-detail URLs;
5. reads weight class from table cell index 6 when present;
6. reads the row result from cell index 0;
7. sets `fighter_1_win=1` only when that result text uppercases exactly to `W`; otherwise it writes `0`;
8. emits no row unless at least two fighter names are present.

Unlike current-event ingestion, `parse_event()` does not raise when an individual event yields zero rows. A markup/parser problem affecting one event can therefore reduce the aggregate without an event-specific hard failure.

### Historical-fight schema

The aggregate contains eight fields:

| Field | Construction |
| --- | --- |
| `event_name` | Parsed event title, with URL fallback. |
| `event_url` | Normalized event URL. |
| `fighter_1_name` | First fighter name in page row order. |
| `fighter_1_url` | First fighter profile URL. |
| `fighter_2_name` | Second fighter name. |
| `fighter_2_url` | Second fighter profile URL. |
| `weight_class` | Table cell index 6 when present. |
| `fighter_1_win` | `1` only when row result is exactly `W` after uppercasing; otherwise `0`. |

`fighter_1_win` is the historical target precursor used by downstream training-dataset construction. Changes to this extraction rule are therefore model-label changes, not merely presentation changes.

### Outputs

Fixed keys:

- `raw/ufc/fights/historical_fights.csv`;
- `raw/ufc/fights/parquets/historical_fights.parquet`.

Each successful run rewrites these aggregate logical products for the selected `MAX_EVENTS` window.

## Historical fighter-profile stage

### Runtime configuration

- `S3_BUCKET` — default `degenerative-investigator`;
- `AWS_REGION` — default `us-east-2`;
- `HISTORICAL_FIGHTS_KEY` — default `raw/ufc/fights/historical_fights.csv`;
- `DELAY_BETWEEN_REQUESTS` — default `0.15` seconds in source;
- `TEST_ROWS` — default `0`.

Workflow inputs:

- `historical_fights_key` — default `raw/ufc/fights/historical_fights.csv`;
- `test_rows` — default `0`.

A positive `TEST_ROWS` value truncates the sorted unique fighter-URL list to its first N entries. `0` means all unique URLs.

### URL selection

The stage reads the historical-fights CSV from S3 and forms a sorted set union of non-null `fighter_1_url` and `fighter_2_url` values. This means profile coverage is determined entirely by the supplied historical-fights object.

### Profile parsing and error isolation

Each URL is passed to the same `parse_profile()` used by current fighter ingestion. On success, it produces the standard fighter-profile fields.

Unlike current-profile ingestion, this historical loop catches exceptions per fighter. A failed fighter produces a placeholder row containing:

- the original `fighter_url`;
- blank profile/statistic fields;
- `profile_error` containing the exception text.

The batch then continues after the normal inter-request delay.

Because `profile_error` exists only in failure dictionaries, the output DataFrame contains that column only when at least one profile failure occurs in the run; successful rows in such a mixed DataFrame have an empty/NaN value for that column.

### Standard profile fields

Successful rows contain:

- `fighter_name`;
- `fighter_url`;
- `height`;
- `weight`;
- `reach`;
- `stance`;
- `dob`;
- `slpm`;
- `str_acc`;
- `sapm`;
- `str_def`;
- `td_avg`;
- `td_acc`;
- `td_def`;
- `sub_avg`;
- `career_wins_scraped`;
- `career_losses_scraped`;
- `career_other_scraped`;
- `recent_fights_scraped`.

The script deduplicates by `fighter_url` before writing.

### Outputs

Fixed keys:

- `raw/ufc/fighters/historical_fighter_profiles.csv`;
- `raw/ufc/fighters/parquets/historical_fighter_profiles.parquet`.

These are aggregate historical-profile snapshots, not event-versioned products.

## Request behavior

Historical fight page retrieval uses the same UFC Stats request helper pattern as current ingestion:

- normalize HTTPS UFC Stats URLs to HTTP first;
- request with 30-second timeout and browser-like user agent;
- retry the same URL once via HTTPS if the HTTP attempt fails;
- raise after both attempts fail.

Historical profile parsing inherits this behavior through `parse_profile()`.

The configured sleeps are request pacing only; the repository does not implement general exponential backoff, retry-after handling, or a persisted retry queue.

## GitHub Actions workflows

### UFC Build History (Manual)

`.github/workflows/ufc_build_history.yml`

- trigger: `workflow_dispatch`;
- input: `max_events`;
- default: `150`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 360 minutes;
- permission: `contents: read`;
- command: `python extract/ufc_historical_fights.py`.

### UFC Pull Historical Fighter Profiles (Manual)

`.github/workflows/ufc_pull_historical_fighter_profiles.yml`

- trigger: `workflow_dispatch`;
- inputs: `historical_fights_key`, `test_rows`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 360 minutes;
- permission: `contents: read`;
- command: `python extract/ufc_historical_fighter_profiles.py`.

Both workflows install `requirements.txt`, set `PYTHONPATH`, use the fixed S3 bucket name, and receive AWS credential/region values through GitHub secret names.

## Normal operating sequence

1. Decide the intended completed-event window size (`max_events`).
2. Dispatch `UFC Build History (Manual)` with that value.
3. Confirm the aggregate historical-fights CSV/Parquet pair is written successfully.
4. Dispatch `UFC Pull Historical Fighter Profiles (Manual)` against that exact historical-fights key.
5. Use `test_rows=0` for a full profile rebuild; a positive value is a deliberately truncated test run.
6. Review the resulting profile data for any `profile_error` values before downstream training-dataset construction.
7. Only after fight and profile snapshots correspond to the intended rebuild should the historical training-dataset builder run.

## Validation checks

Before downstream use, verify at minimum:

- the chosen `MAX_EVENTS` value matches the intended rebuild scope;
- the historical-fights output is non-empty;
- rows contain two fighter names/URLs and expected event identifiers;
- `fighter_1_win` contains only values consistent with the current binary extraction contract;
- historical-profile URL coverage corresponds to unique fight URLs;
- `TEST_ROWS` was `0` for a production/full rebuild;
- any `profile_error` rows are understood before training-dataset construction;
- fixed-key objects were not unintentionally replaced by a small test run.

The repository does not implement an automated row-count/coverage threshold for these checks.

## Failure modes

### Historical fights

- completed-events listing cannot be fetched;
- UFC Stats markup changes and event links are no longer found;
- an individual event request fails after the HTTP/HTTPS attempts, terminating the run;
- individual event markup can yield zero rows without an event-specific exception;
- `MAX_EVENTS` is non-integer and source conversion fails;
- S3 write/authentication/region errors;
- a successful small-window run replaces the fixed aggregate with that smaller scope.

### Historical profiles

- historical-fights S3 key is missing or unreadable;
- required fighter URL columns are missing;
- a positive `TEST_ROWS` unintentionally truncates a production rebuild;
- individual profile failures are persisted as placeholder `profile_error` rows rather than failing the workflow;
- large numbers of placeholder profiles can materially reduce downstream feature coverage even though the workflow itself succeeds;
- S3 final write fails after profile collection.

## Rerun and recovery

### Fight aggregate

If the fight rebuild fails, correct the input/source problem and rerun `UFC Build History`. Because the outputs use fixed aggregate keys, the next successful run becomes the logical historical-fight snapshot.

If an incorrect `MAX_EVENTS` value was successfully written, rerun with the intended value before any downstream dataset rebuild.

### Historical profiles

If only some profiles produce `profile_error`, decide whether those missing profiles are acceptable for the intended training-data rebuild. To restore coverage after a transient/source problem, rerun the profile workflow against the same correct historical-fights key.

If a `TEST_ROWS>0` test run replaced the fixed historical-profile snapshot, immediately rerun with `test_rows=0` before downstream production use.

### Downstream invalidation

When the historical fight window or historical profile snapshot changes materially, rebuild:

1. historical training dataset;
2. trained model;
3. target-event scoring if the updated model is intended for current inference;
4. downstream report artifacts as appropriate.

A historical ingestion rerun does not automatically trigger any of these stages.

## Idempotency and overwrite behavior

Both historical products use fixed keys. Repeating a run with the same source state and same inputs is intended to rebuild the same logical products; the repository does not append or preserve prior snapshots itself.

S3 object versioning/retention is live AWS state and is not established by repository source.

## Security considerations

Workflow secret names used for S3 access are:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`.

The jobs request only `contents: read`. Never persist credential values or personal/account identifiers in documentation or workflow inputs. Exact IAM permissions and S3 policy state are not provable from this source.

## Limitations

- historical scope is count-based (`MAX_EVENTS`), not a date interval or incremental watermark;
- outputs are fixed aggregate snapshots;
- no automatic comparison detects unexpectedly missing events/fights;
- fight target construction is tied directly to the current result-cell parser;
- historical profile success can coexist with per-fighter placeholder error rows;
- a positive `TEST_ROWS` test run writes the same fixed profile keys as a full run;
- no automatic workflow chaining or downstream invalidation exists;
- source HTML changes can alter extraction behavior independently of repository code.

## Related documentation

- [degenerate_investigator Repository and UFC Analytics Architecture](../repositories/degenerate-investigator.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [degenerate_investigator Current UFC Event and Fighter Ingestion](degenerate-investigator-current-ufc-ingestion.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Any change to the completed-event selection rule, fight-label parsing, profile error handling, `TEST_ROWS` behavior, fixed S3 keys, or workflow inputs should update this page in the same documentation change set because those changes can alter the historical training population or label contract.
