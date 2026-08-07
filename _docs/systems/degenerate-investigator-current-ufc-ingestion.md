---
title: degenerate_investigator Current UFC Event and Fighter Ingestion
summary: Source-grounded operating and data-contract documentation for manually ingesting a current UFC Stats event card and the corresponding fighter-profile snapshot into S3.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Current UFC Event and Fighter Ingestion

## Purpose

This pipeline creates the current-event UFC Stats inputs used by downstream feature engineering:

1. an event-card snapshot for one selected UFC Stats event;
2. a current fighter-profile snapshot for the unique fighters on that event card.

The two stages are separate manually dispatched GitHub Actions workflows connected through the event-card S3 key. They are not automatically chained.

## Source paths

### Event card

- implementation: `extract/ufc_event_card.py`;
- workflow: `.github/workflows/ufc_ingest_event.yml`.

Important functions:

- `normalize_ufcstats_url()`;
- `fetch_soup()`;
- `parse_event_card()`;
- `main()`.

### Fighter profiles

- implementation: `extract/ufc_fighter_profiles.py`;
- workflow: `.github/workflows/ufc_pull_fighter_profiles.yml`.

Important functions:

- `normalize_ufcstats_url()`;
- `fetch_soup()`;
- `parse_profile()`;
- `main()`.

## Inputs and outputs

### Stage 1: event card

Required runtime input:

- `EVENT_URL` — UFC Stats event page URL.

Workflow input:

- `event_url` — passed to `EVENT_URL`.

The current workflow contains a committed event-specific default URL. Treat it as a convenience default, not as a dynamically selected “latest event”. Verify it before every run for a different target event.

Outputs:

- `raw/ufc/events/{event_slug}_card.csv`;
- `raw/ufc/events/parquets/{event_slug}_card.parquet`.

`{event_slug}` is generated from the event title with `common.io_helpers.slugify()`.

### Stage 2: fighter profiles

Required runtime input:

- `EVENT_CARD_KEY` — S3 CSV key produced by the intended event-card run.

Optional runtime input:

- `DELAY_BETWEEN_REQUESTS` — seconds slept after each fighter-profile request; source default `0.25`.

Workflow input:

- `event_card_key` — passed to `EVENT_CARD_KEY`.

The workflow currently defaults to:

`raw/ufc/events/ufc-327-prochazka-vs-ulberg_card.csv`

That default is event-specific. A maintainer processing another event must supply the correct event-card key.

Outputs:

- `raw/ufc/fighters/fighter_profiles.csv`;
- `raw/ufc/fighters/parquets/fighter_profiles.parquet`.

These profile keys are fixed current-snapshot keys rather than event-versioned keys. A successful rerun replaces the logical current fighter-profile snapshot.

## Storage and AWS configuration

Both scripts use `common/io_helpers.py`.

Verified defaults:

- bucket: `degenerative-investigator`;
- region: `us-east-2`.

The workflows set `S3_BUCKET=degenerative-investigator` and supply these GitHub secret names:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`.

Only names are documented. Credential values and live IAM policy scope are outside the repository source boundary.

## UFC Stats request behavior

Both extractors use the same request pattern:

1. normalize a `https://ufcstats.com...` URL to `http://ufcstats.com...`;
2. request the normalized URL with a browser-like `User-Agent` and 30-second timeout;
3. if the normalized URL is HTTP, retry once using HTTPS when the first attempt raises;
4. raise `RuntimeError` after both attempts fail.

This is a URL-scheme retry, not a general exponential-backoff or rate-limit retry system.

## Event-card parsing

`parse_event_card(event_url)`:

1. fetches and parses the event page with BeautifulSoup;
2. reads the event title from `.b-content__title-highlight`, falling back to `.b-content__title` and finally the URL text;
3. builds `event_slug` from the chosen event name;
4. concatenates `.b-list__box-list-item` text into `event_meta`;
5. iterates `tr.b-fight-details__table-row` rows;
6. identifies fighter links by `/fighter-details/` and the bout link by `/fight-details/`;
7. records a row only when at least two fighter names are present;
8. raises `RuntimeError("No fights found on event page. Check EVENT_URL.")` when no rows are produced.

### Event-card schema

The current DataFrame contains 13 columns:

| Field | Meaning / construction |
| --- | --- |
| `event_name` | Event title parsed from the page, or URL fallback. |
| `event_slug` | Slug generated from `event_name`. |
| `event_url` | Normalized UFC Stats event URL. |
| `event_meta` | Concatenated event metadata text from the page. |
| `bout_url` | Fight-detail link found in the row; empty when absent. |
| `fighter_1_name` | First fighter name in row order. |
| `fighter_1_url` | First fighter profile URL, joined to the UFC Stats base URL. |
| `fighter_2_name` | Second fighter name in row order. |
| `fighter_2_url` | Second fighter profile URL. |
| `weight_class` | Table cell index 6 when present. |
| `method_hint` | Table cell index 7 when present. |
| `round_hint` | Table cell index 8 when present. |
| `time_hint` | Table cell index 9 when present. |

The `*_hint` fields are direct page-table text and should not be treated as independently validated fight-result fields.

## Fighter-profile parsing

The profile stage first reads the event-card CSV from S3 and constructs the sorted set union of non-null `fighter_1_url` and `fighter_2_url` values. Each unique URL is passed to `parse_profile()`.

`parse_profile(url)`:

1. fetches the fighter page;
2. parses the displayed fighter name;
3. converts colon-delimited `.b-list__box-list-item` text into a normalized `stat_map`;
4. scans fighter-history table rows with at least ten cells;
5. derives scraped win/loss/other counts from row result letters;
6. returns one current profile record.

The current-profile loop does not catch per-fighter `parse_profile()` exceptions. A single unhandled profile fetch/parser failure can fail the whole workflow before the final snapshot is written.

### Fighter-profile schema

The output contains 18 fields:

| Field | Meaning / construction |
| --- | --- |
| `fighter_name` | Displayed full name from fighter page. |
| `fighter_url` | Normalized UFC Stats fighter URL. |
| `height` | Raw profile height text. |
| `weight` | Raw profile weight text. |
| `reach` | Raw profile reach text. |
| `stance` | Raw stance text. |
| `dob` | Raw date-of-birth text. |
| `slpm` | Raw significant-strikes-landed-per-minute value. |
| `str_acc` | Raw striking-accuracy value. |
| `sapm` | Raw significant-strikes-absorbed-per-minute value. |
| `str_def` | Raw striking-defence value. |
| `td_avg` | Raw takedown-average value. |
| `td_acc` | Raw takedown-accuracy value. |
| `td_def` | Raw takedown-defence value. |
| `sub_avg` | Raw submission-average value. |
| `career_wins_scraped` | Count of parsed history rows whose result is `W`. |
| `career_losses_scraped` | Count of parsed history rows whose result is `L`. |
| `career_other_scraped` | Count of parsed history rows whose result is `D` or `NC`. |
| `recent_fights_scraped` | Number of parsed history rows. |

The statistical values remain strings at ingestion time. Numeric/unit conversion is a downstream feature-engineering responsibility.

## Important profile-history caveat

Inside the temporary profile-history row parser, both `opponent` and `fighter` are assigned from the same table cell. Those temporary rows are used only to derive result counts and `recent_fights_scraped` in the current implementation; they are not written as a separate current-history dataset.

Do not infer a reliable fighter/opponent history schema from this helper structure.

## Workflow details

### UFC Ingest Event (Manual)

File: `.github/workflows/ufc_ingest_event.yml`

- trigger: `workflow_dispatch`;
- input: `event_url`;
- repository permission: `contents: read`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 60 minutes;
- installs `requirements.txt`;
- command: `python extract/ufc_event_card.py`.

### UFC Pull Fighter Profiles (Manual)

File: `.github/workflows/ufc_pull_fighter_profiles.yml`

- trigger: `workflow_dispatch`;
- input: `event_card_key`;
- repository permission: `contents: read`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 120 minutes;
- installs `requirements.txt`;
- command: `python extract/ufc_fighter_profiles.py`.

Neither workflow automatically invokes the other.

## Normal operating sequence

1. Identify the intended UFC Stats event URL outside the pipeline.
2. Dispatch `UFC Ingest Event (Manual)` with that exact event URL rather than relying on an old committed default.
3. Confirm the workflow succeeds and note the emitted `{event_slug}` from the S3 key in its output log.
4. Use `raw/ufc/events/{event_slug}_card.csv` as the profile workflow input.
5. Dispatch `UFC Pull Fighter Profiles (Manual)` with that exact key.
6. Confirm it succeeds and writes the fixed current-profile CSV/Parquet pair.
7. Only then run downstream feature engineering for the same event.

Because S3 browsing/live object state is not proven in this documentation repository, workflow success logs and known producer/consumer keys are the source-grounded verification points available here.

## Validation checks before downstream use

At minimum, verify:

- the event-card key contains the intended event slug;
- the card has at least one row;
- every intended matchup has two fighter names and profile URLs;
- current profile output contains the unique fighters expected from the event card;
- profile `fighter_url` values are unique after the script's deduplication;
- a profile rerun did not accidentally use the committed default card for another event.

Do not treat a successful GitHub Actions status alone as proof that the operator selected the intended event.

## Failure modes

### Event workflow

- missing/blank `EVENT_URL` when run outside the workflow: `get_env(..., required=True)` raises;
- UFC Stats request failure on both HTTP/HTTPS attempts;
- upstream page markup change prevents fight rows from being recognized;
- selected page is not an event-detail page or contains no parseable fights;
- AWS/S3 authentication, region, bucket, or write failure;
- Parquet serialization/dependency failure.

### Fighter-profile workflow

- `EVENT_CARD_KEY` points to a missing object;
- event-card schema lacks `fighter_1_url` or `fighter_2_url`;
- wrong event-card key refreshes the fixed profile snapshot for the wrong fighters;
- one fighter request/parser exception terminates the batch;
- upstream profile markup changes produce missing/blank stat values;
- AWS/S3 write failure after profile collection;
- workflow timeout on an unexpectedly slow/large run.

## Rerun and recovery

### Event-card failure

Correct the event URL/source issue and rerun only the event-card workflow. The event-specific key makes this rerun naturally replace the same logical event snapshot when the parsed slug is unchanged.

### Fighter-profile failure

Verify the exact intended event-card key first. Then rerun only the fighter-profile workflow. Because final writes occur after the profile loop completes, a failed run before `write_csv_and_parquet()` does not intentionally publish a partial new snapshot from this script.

If the fixed current-profile snapshot was successfully written from the wrong event card, rerun the profile stage with the correct event-card key before any downstream current-event feature build.

### Parser/schema change

When UFC Stats markup changes, update and test the relevant extractor before trusting regenerated objects. If column names or semantics change, update downstream feature documentation and code contracts in the same development sequence.

## Idempotency and overwrite behavior

- Re-running the event workflow for the same parsed event title writes the same event-specific key pair.
- Re-running current profiles always writes the same fixed current-profile key pair.
- The source does not implement object-level append, merge, snapshot timestamping, or history preservation for these outputs.
- S3 bucket versioning, if any, is a live-state property not established by repository source.

## Dependencies

Direct imports used by these extractors include:

- `pandas`;
- `requests`;
- `bs4.BeautifulSoup`;
- shared helpers from `common.io_helpers`.

Use `requirements.txt` as the dependency-version source of truth.

## Security considerations

The workflows use secret names for AWS credentials and only request `contents: read` from GitHub. They do not need repository write permission.

Do not put credential values into workflow inputs, logs, documentation, event URLs, or S3 key names. Live IAM policy scope is not established by source and must not be guessed.

## Limitations

- manual dispatch and event-specific defaults permit operator selection mistakes;
- extraction depends on UFC Stats HTML structure rather than a versioned API contract;
- retry behavior covers URL-scheme fallback only;
- current profile output is a single fixed snapshot, not event-versioned;
- current profile ingestion lacks per-fighter exception isolation;
- ingestion stores raw profile statistics as strings and leaves numeric normalization downstream;
- no repository workflow automatically validates card/profile row coverage against an external canonical event roster.

## Related documentation

- [degenerate_investigator Repository and UFC Analytics Architecture](../repositories/degenerate-investigator.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

If this pipeline changes, keep the workflow inputs, output key patterns, card/profile schemas, request behavior, overwrite semantics, and rerun guidance synchronized with `extract/ufc_event_card.py`, `extract/ufc_fighter_profiles.py`, and their two GitHub Actions workflows.
