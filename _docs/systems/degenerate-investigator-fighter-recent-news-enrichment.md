---
title: degenerate_investigator Fighter Recent-News Enrichment
summary: Source-grounded documentation for OpenAI web-search enrichment of current UFC fighter profiles, including prompts, structured output, repair behavior, schemas, S3 products, failure degradation, workflow inputs, and rerun guidance.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Fighter Recent-News Enrichment

## Purpose

This stage enriches the current fighter-profile snapshot with recent factual reporting that can provide analytical context for a target UFC event. It uses the OpenAI Responses API with web search, requests structured JSON for each fighter, flattens returned items into tabular rows, and stores a fixed current-news snapshot in S3.

The output is contextual enrichment, not a model target and not a substitute for source verification. Downstream feature engineering reduces item labels to simple fighter-level flags; report generation also consumes the summaries/items as narrative context.

## Source paths

- implementation: `extract/fighter_recent_news.py`;
- workflow: `.github/workflows/ufc_pull_news.yml`;
- shared S3 helpers: `common/io_helpers.py`.

Important functions:

- `extract_json()`;
- `make_parse_error_row()`;
- `call_model()`;
- `main()`.

## Inputs

Primary S3 input:

- `FIGHTER_PROFILES_KEY` — source default `raw/ufc/fighters/fighter_profiles.csv`.

The input CSV must contain `fighter_name`.

Other runtime configuration:

- `S3_BUCKET` — default `degenerative-investigator`;
- `AWS_REGION` — default `us-east-2`;
- `OPENAI_API_KEY` — required secret value;
- `OPENAI_MODEL` — optional model override, source default `gpt-4.1-mini`;
- `TEST_ROWS` — source default `0`, meaning all fighter names;
- `DELAY_BETWEEN_REQUESTS` — source default `0.5` seconds.

Never publish the API-key value. Only the configuration name is technically relevant.

## Workflow-default distinction

The workflow `.github/workflows/ufc_pull_news.yml` exposes:

- `fighter_profiles_key` — committed default `raw/ufc/fighters/fighter_profiles.csv`;
- `test_rows` — committed default `6`.

The script itself defaults `TEST_ROWS` to `0`, but the workflow always passes its input value. Therefore a manual workflow dispatch that accepts the defaults processes only the first six fighter names, not all current fighters.

A full current-event enrichment run requires `test_rows=0` in the workflow input.

## Fighter selection

`main()` reads the profile CSV, then builds:

`df_profiles["fighter_name"].dropna().astype(str).str.strip().tolist()`

If `TEST_ROWS > 0`, the resulting list is truncated to the first N entries. The script does not explicitly deduplicate fighter names; current profile ingestion normally deduplicates by fighter URL upstream.

## Search prompt contract

For each fighter, the initial request asks for recent factual reporting and strict JSON containing:

- `fighter_name`;
- `summary`;
- `items`.

Each item is expected to contain:

- `title`;
- `source`;
- `published_date`;
- `url`;
- `label`;
- `note`.

The prompt focuses the search on recent context such as injuries, weight-cut issues, training-camp changes, layoffs, short-notice status, legal/personal disruptions, and coach comments.

This prompt shapes collection scope but does not independently verify the truth or completeness of returned claims.

## OpenAI request behavior

`call_model(client, prompt, use_web_search)` builds a Responses API request with:

- model from `OPENAI_MODEL`, default `gpt-4.1-mini`;
- the prompt as `input`;
- `max_output_tokens=900`.

When `use_web_search=True`, it adds the `web_search` tool and automatic tool choice.

The initial fighter request uses web search. A repair request, when needed, does not.

## Structured-output parsing and repair

`extract_json(text)`:

1. trims the response text;
2. finds the first `{` and last `}`;
3. raises if braces are absent;
4. parses the enclosed substring with `json.loads()`.

For each fighter:

1. call the model with web search;
2. attempt `extract_json(raw_text)`;
3. if parsing fails, call the model a second time with `REPAIR_TEMPLATE` and `use_web_search=False`;
4. parse the repaired response;
5. if the overall fighter process still raises, persist a `parse_error` row and continue.

The repair pass is text repair only; it does not conduct a second web search.

## Row construction

### Returned items

If the parsed payload contains one or more `items`, one output row is written per item. The same payload-level `summary` is repeated across those fighter rows.

### No returned items

If `items` is empty or absent, the script writes one row with:

- the fighter name;
- returned summary;
- blank item fields;
- `label=no_recent_items`;
- `note=No recent items returned.`

This is a valid degraded data state, not an exception.

### Parse/request failure

An exception in the fighter processing block produces one row from `make_parse_error_row()` with:

- fighter name;
- blank summary/item fields;
- `label=parse_error`;
- note containing the error reason and up to 1,500 characters of captured raw response text.

The batch continues to the next fighter.

## Output schema

The flattened output has eight fields:

| Field | Meaning |
| --- | --- |
| `fighter_name` | Fighter from the input profile list. |
| `summary` | Payload-level recent-news summary, repeated for item rows. |
| `title` | Individual returned item title. |
| `source` | Returned source/publisher label. |
| `published_date` | Returned publication-date text. |
| `url` | Returned item URL. |
| `label` | Returned analytical label or local sentinel such as `no_recent_items` / `parse_error`. |
| `note` | Returned item note or local degradation/error note. |

The repository does not enforce a closed vocabulary for normal model-returned `label` values in this ingestion script.

## S3 products

Fixed outputs:

- `raw/news/fighter_recent_news.csv`;
- `raw/news/parquets/fighter_recent_news.parquet`.

A successful rerun replaces the logical current-news snapshot. The key is not event-versioned or timestamp-versioned.

## Workflow behavior

`.github/workflows/ufc_pull_news.yml`:

- trigger: `workflow_dispatch`;
- inputs: `fighter_profiles_key`, `test_rows`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 180 minutes;
- repository permission: `contents: read`;
- installs `requirements.txt`;
- command: `python extract/fighter_recent_news.py`.

The workflow supplies AWS credentials/region and `OPENAI_API_KEY` through GitHub secret names. It does not automatically follow current fighter-profile ingestion.

## Downstream use

### Feature engineering

`process/ufc_feature_builder.py` reads the news CSV optionally and creates fighter-level news flags. An unavailable news object is tolerated and becomes an empty lookup.

Therefore a feature-build success does not prove recent-news enrichment was present, complete, or parseable.

### Report generation

`process/generate_event_report.py` can read the same current-news CSV and incorporate fighter summaries/items into report context. Missing news is also tolerated by that stage.

## Validation checks

Before relying on the snapshot, verify:

- the input profile key corresponds to the intended current event;
- `test_rows=0` was used for a full run;
- expected fighter names appear in the output;
- `parse_error` rows are reviewed;
- `no_recent_items` is distinguished from a parser/request failure;
- item URLs, dates, and claims are treated as externally returned context rather than internally verified facts;
- the fixed snapshot was not unintentionally replaced by a six-fighter/default test run.

The repository does not implement a minimum-source count, freshness threshold, or per-fighter completeness gate.

## Failure and degradation modes

- missing/unreadable fighter-profile S3 object;
- missing `fighter_name` column;
- missing required OpenAI credential;
- OpenAI request/service/rate-limit/transport failure;
- web-search tool failure or incomplete evidence;
- initial response is not parseable JSON;
- repair response is also not parseable JSON;
- model returns empty `items`;
- model-returned schema values are missing or weakly structured;
- workflow default `test_rows=6` produces an intentionally partial snapshot when the operator expected all fighters;
- S3 final write failure after processing;
- fixed-key overwrite replaces an earlier more complete snapshot.

Most per-fighter request/parse failures do not fail the workflow; they become rows. Operational success must therefore include content-quality checks, not only GitHub Actions status.

## Raw-text error-note caveat

`raw_text` is assigned inside the loop before normal parsing, and the exception handler retrieves it with `locals().get("raw_text", "")`. Because Python function locals persist across loop iterations, an exception that occurs before a new fighter assigns `raw_text` can potentially cause the handler to reuse the prior iteration's value.

This can make a `parse_error` note misleading and can associate the wrong raw-response excerpt with a fighter. Treat `parse_error.note` as troubleshooting context, not authoritative evidence. A future implementation should initialize `raw_text = ""` at the start of every fighter iteration.

## Rerun and recovery

### Partial/test snapshot

If a run used `test_rows>0` but a complete current snapshot is required, rerun the workflow with the same correct profile key and `test_rows=0` before downstream feature/report generation.

### Per-fighter parse errors

If transient request/formatting failures caused `parse_error` rows, rerun the entire fixed-snapshot job after the external issue clears. The source does not support selective per-fighter checkpoint/resume into the existing object.

### Upstream profiles changed

After current fighter profiles are refreshed for a new/changed event, rerun recent-news enrichment before rebuilding features/reports that should use current context.

### Prompt/model changes

Treat prompt, model, search-tool, and JSON-parsing changes as data-generation changes. Regenerate the news snapshot and assess downstream flag/report behavior; no automatic invalidation occurs.

## Cost and external-service boundary

A full run can make at least one model request per fighter and can make a second repair request for fighters whose initial JSON cannot be parsed. `TEST_ROWS` is the repository's existing mechanism for deliberately limiting a test run.

Changes that materially increase request count, model selection, or search behavior can affect external cost and should be reviewed as implementation decisions rather than silently changed through documentation.

## Security considerations

- Never publish `OPENAI_API_KEY` or AWS credential values.
- Search/model responses can contain external text and URLs; treat them as untrusted data.
- Error notes can persist raw response excerpts into S3 and should not be assumed free of sensitive or inappropriate external content.
- The workflow requests only `contents: read`; it does not need repository write permission.
- No separate `NEWS_API_KEY` integration is present in the inspected source.

## Limitations

- fixed current snapshot, not event/timestamp-versioned history;
- workflow defaults to only six fighters unless changed;
- no closed label vocabulary or schema validator for model-returned item labels;
- no deterministic guarantee of search coverage, factual completeness, or source quality;
- repair improves JSON syntax only and does not re-search;
- per-fighter failures can coexist with a successful workflow;
- downstream stages treat missing news as optional;
- potential stale-`raw_text` error-note issue described above;
- no automatic provenance snapshot of all underlying web-search evidence beyond returned item fields.

## Related documentation

- [degenerate_investigator Repository and UFC Analytics Architecture](../repositories/degenerate-investigator.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [degenerate_investigator Current UFC Event and Fighter Ingestion](degenerate-investigator-current-ufc-ingestion.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Any change to `PROMPT_TEMPLATE`, `REPAIR_TEMPLATE`, `OPENAI_MODEL`, fighter selection, `TEST_ROWS`, flattened schema, error degradation, or fixed output keys should update this page in the same change set because those changes alter the enrichment data contract consumed by features and reports.
