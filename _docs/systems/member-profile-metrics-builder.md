---
title: Member Profile Metrics Builder
summary: Year-aware member analytics builder that joins Unified Oireachtas compatibility members, votes, photos, and classified debate issues into reusable member-profile metrics for deterministic and AI Instagram workflows.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
system: Member Profile Metrics Builder
repository: eirepolitic-data-pipeline
order: 42
permalink: /projects/systems/member-profile-metrics-builder/
technologies:
  - Python
  - pandas
  - PyArrow
  - AWS S3
  - GitHub Actions
related:
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/systems/instagram-constituency-campaign-rendering/
  - /projects/systems/instagram-ai-member-profile-content-workflow/
  - /projects/repositories/eirepolitic-data-pipeline/
---

# Member Profile Metrics Builder

## Summary

`process/build_member_profile_metrics.py` is the current generic member-profile analytics builder in `eirepolitic-data-pipeline`. It reads four Unified Oireachtas compatibility datasets, computes year-specific speech/issue and vote-participation metrics, joins member photos, and writes a member-level CSV and Parquet product.

The builder supports two output modes:

- normal/manual output under `processed/members/`;
- immutable candidate-consumer output under the active Unified Oireachtas batch when `OIREACHTAS_BATCH_ID` is set.

The historical `process/build_member_profile_metrics_2025.py` file remains only as a backward-compatible wrapper that sets `TARGET_YEAR=2025` before calling the generic builder.

## Current implementation state

**Verified implementation:** `process/build_member_profile_metrics.py` is the authoritative implementation. The 2025-specific file no longer contains independent metric logic.

**Verified implementation/configuration:** `.github/workflows/build_member_profile_metrics_2025.yml`, despite its filename, exposes a `target_year` workflow input and calls the generic builder directly.

**Verified implementation:** current default inputs are all Unified Oireachtas compatibility products.

**Verified implementation:** when `OIREACHTAS_BATCH_ID` is set, the shared Oireachtas S3 read resolver causes those logical compatibility reads to resolve inside the candidate batch, and the metric outputs are also written beneath that candidate's consumer namespace.

**Observed runtime evidence:** workflow ID `266755732` has nine recorded manual runs. The latest observed run, `29299647855` on 2026-07-14, completed successfully including input validation, dependency installation, metrics build, and evidence upload. Earlier recorded runs include both successes and failures; current source is the authoritative behavior definition.

## Source of truth

| Concern | Current source |
| --- | --- |
| metric implementation | `process/build_member_profile_metrics.py` |
| 2025 compatibility entry point | `process/build_member_profile_metrics_2025.py` |
| manual workflow | `.github/workflows/build_member_profile_metrics_2025.yml` |
| candidate batch identity/resolution | `extract/oireachtas/batch.py`, `extract/oireachtas/io_s3.py` |
| compatibility input contracts | `configs/oireachtas/downstream_contracts.yml` |
| candidate validation invocation | `.github/workflows/oireachtas_validation_reusable.yml` |
| deterministic member-profile campaign consumer | `process/instagram_render_campaign.py` |
| AI member-profile consumer | `process/render_member_profile_ai_edit.py` |

## Inputs

Current default S3 bucket and region are inherited from the Oireachtas storage helpers and can be overridden through environment variables.

The builder defaults to these four logical compatibility inputs:

```text
MEMBERS_INPUT_KEY=
processed/oireachtas_unified/compat/members/oireachtas_members_34th_dail_compat.csv

MEMBER_VOTES_INPUT_KEY=
processed/oireachtas_unified/compat/votes/dail_vote_member_records_compat.csv

MEMBER_PHOTOS_INPUT_KEY=
processed/oireachtas_unified/compat/media/members_photo_urls_compat.csv

DEBATE_ISSUES_INPUT_KEY=
processed/oireachtas_unified/compat/debates/debate_speeches_classified_compat.csv
```

The workflow pins the same four keys explicitly, so its runtime inputs do not depend on undocumented defaults.

### Required members columns

The builder requires these exact columns from the members compatibility dataset:

- `member_code`
- `full_name`
- `constituency`
- `party`

Missing any of those columns raises `ValueError` and stops the build.

### Flexible photo columns

For the photos dataset, member identity can be read from either:

- `member_code`; or
- `memberCode`.

The photo URL column must be `photo_url` for a join to occur. If no compatible member-code/photo combination exists, the builder creates a blank `photo_url` column rather than failing the entire build.

### Flexible debate columns

The classified debate input supports multiple current/legacy column aliases.

Member identity preference:

- `member_code`
- `speaker_member_code`
- `Speaker Member Code`
- `memberCode`

Fallback speaker-name columns:

- `Speaker Name`
- `speaker_name`
- `member_name`

Issue-label candidates:

- `PoliticalIssues`
- `political_issues`
- `issue`
- `Issue`
- `issue_label`
- `category`
- `label`

Date candidates:

- `Debate Date`
- `date`
- `speech_date`

If an issue column and a member/member-name column are available, debate metrics are computed. Otherwise the member output remains valid with zero/blank speech metrics.

### Flexible vote columns

Member identity candidates:

- `memberCode`
- `member_code`

Vote ID candidates:

- `unique_vote_id`
- `division_id`
- `vote_id`

Vote date candidates:

- `date`
- `division_date`

Vote metrics are computed only when both a member column and a vote-ID column are available.

## Target year

The target calendar year is controlled by `TARGET_YEAR`.

Current default in Python:

```text
current UTC year - 1
```

The manual workflow requires a `target_year` input, defaulting to `2025`, and validates it against a four-digit numeric pattern before execution.

Metric column names are generated dynamically as `<metric>_<TARGET_YEAR>`.

Examples for 2025:

```text
top_issue_2025
vote_participation_pct_2025
speech_count_2025
speech_rank_2025
```

## Member identity normalization

The builder adds a temporary normalized `member_key` from `full_name` using `process.instagram_render_post.normalize_name`.

This normalized name is used only as a fallback for classified-debate rows that do not contain a member code. In that case, the builder creates a member-name lookup that keeps only normalized names that are unique in the member roster, then inner-joins debates through that lookup.

This deliberately avoids assigning a speech to an ambiguous duplicate normalized name.

## Speech and issue metrics

When a debate date column is present, only rows whose parsed date year equals `TARGET_YEAR` are retained.

Rows are then filtered to require:

- a nonblank resolved member code;
- a nonblank issue label;
- an issue label other than `NONE`, case-insensitive.

### `speech_count_<year>`

Defined as the count of remaining classified debate rows for that member in the target year.

This is therefore a count of rows in the classified debate compatibility input after the filters above. It is not independently inferred as total parliamentary speaking activity outside that dataset.

### `speech_rank_<year>`

Defined as a dense descending rank of `speech_count_<year>`.

Members tied on speech count receive the same rank; the next rank advances by one dense-rank level rather than leaving a gap.

### `top_issue_<year>` and `top_issue_count_<year>`

The builder counts classified rows by `member_code` and issue label, then chooses one top issue per member by sorting:

1. member code ascending;
2. issue count descending;
3. issue label ascending.

The final alphabetical tie-break means equal-count issues produce a deterministic top issue.

`NONE` and blank labels are excluded before this calculation.

## Vote metrics

When a vote-date column exists, only target-year rows are retained.

### `all_distinct_vote_ids_<year>`

Defined once for the whole filtered vote dataset as the number of distinct, nonblank values in the selected vote-ID column.

The same total is written to every member row.

### `distinct_votes_participated_<year>`

Defined per member as the number of distinct `(member, vote_id)` combinations after blanks are removed and duplicates dropped.

### `vote_participation_pct_<year>`

Defined as:

```text
distinct_votes_participated_<year>
--------------------------------- × 100
all_distinct_vote_ids_<year>
```

The result is rounded to the nearest whole percentage and stored as an integer.

If the total distinct vote count is zero, participation percentage is set to zero.

This metric measures presence in member-vote records relative to all distinct vote IDs in the filtered compatibility dataset. It does not infer abstention/absence reasons beyond the rows present in that source.

## Output schema

For a target year `Y`, the output columns are exactly:

```text
member_code
full_name
constituency
party
photo_url
top_issue_Y
top_issue_count_Y
vote_participation_pct_Y
distinct_votes_participated_Y
all_distinct_vote_ids_Y
speech_count_Y
speech_rank_Y
```

Numeric metric columns are coerced to integers, with missing values filled as zero. `top_issue_Y` becomes a blank string when missing.

The final output is sorted by:

1. `speech_count_Y` descending;
2. `full_name` ascending.

## Output locations

### Normal/manual mode

When no active Oireachtas batch ID exists:

```text
processed/members/member_profile_metrics_<year>.csv
processed/members/parquets/member_profile_metrics_<year>.parquet
```

### Candidate-batch mode

When `OIREACHTAS_BATCH_ID` is set:

```text
processed/oireachtas_unified/batches/<batch_id>/consumers/member_profile_metrics/member_profile_metrics_<year>.csv
processed/oireachtas_unified/batches/<batch_id>/consumers/member_profile_metrics/member_profile_metrics_<year>.parquet
```

This keeps consumer validation outputs isolated inside the same immutable candidate being validated.

## S3 and candidate read semantics

The builder reads through `extract.oireachtas.io_s3.get_bytes()` rather than directly calling `boto3.get_object()`.

That matters because logical `processed/oireachtas_unified/compat/...` keys resolve through current Oireachtas candidate/production state.

When a batch ID is active, the builder therefore evaluates the candidate's compatibility datasets instead of silently reading current production. This makes it suitable as a downstream consumer check during Oireachtas candidate validation.

## Manual workflow

Workflow name: **Build Member Profile Metrics**.

File: `.github/workflows/build_member_profile_metrics_2025.yml`.

Despite the filename, the current workflow is year-parameterized.

Inputs:

| Input | Default | Validation |
| --- | --- | --- |
| `target_year` | `2025` | exactly four digits |
| `batch_id` | blank | optional; if set, `[A-Za-z0-9][A-Za-z0-9._-]{0,127}` |

Runtime:

- `ubuntu-latest`;
- Python 3.12;
- timeout 90 minutes;
- concurrency group `build-member-profile-metrics-<target_year>`;
- `cancel-in-progress: false`;
- contents read-only permission.

Credential/environment boundary:

- `AWS_ACCESS_KEY_ID` secret;
- `AWS_SECRET_ACCESS_KEY` secret;
- region fixed non-secret to `ca-central-1`;
- bucket fixed non-secret to `eirepolitic-data`;
- four compatibility input keys checked into workflow YAML.

The builder prints a small JSON summary containing row count, target year, and output keys. The workflow captures that as `member_profile_metrics.json` and uploads it as a GitHub artifact retained for 90 days.

## Oireachtas candidate-validation integration

The reusable Oireachtas validation workflow can invoke this builder as a downstream consumer test while `OIREACHTAS_BATCH_ID` points at the candidate.

That checks whether candidate compatibility outputs are sufficient to build the year-aware member-profile product before production promotion.

The builder itself does not promote Oireachtas data or change the production pointer.

## Consumers

### Deterministic member-profile campaign

`process/instagram_render_campaign.py` currently reads:

```text
processed/members/member_profile_metrics_2025.csv
```

for the checked-in `member_profile_batch_v1` campaign and uses 2025 fields for member selection/bindings.

### AI member-profile test

`process/render_member_profile_ai_edit.py` defaults to the same normal-mode 2025 CSV and uses its member/photo/issue/vote/speech fields as exact source truth for image editing.

### Candidate Instagram smoke validation

Within the Unified Oireachtas validation path, candidate member metrics can also feed candidate-only Instagram smoke behavior without publishing social content.

## Backward-compatible 2025 wrapper

`process/build_member_profile_metrics_2025.py` contains no independent analytics logic.

It only performs:

```text
TARGET_YEAR defaults to 2025
call process.build_member_profile_metrics.main
```

Treat it as a compatibility entry point for older workflows/scripts. Documentation and future metric changes should target the generic builder unless the wrapper's compatibility behavior itself changes.

## Observed runtime evidence

Workflow ID `266755732` currently exposes nine recorded manual runs.

The latest observed run:

- run `29299647855`;
- created 2026-07-14;
- conclusion: success;
- checkout, Python setup, dependency installation, metric build, and post steps all succeeded.

Other observed history includes successful runs on July 13, July 5, July 3, June 30, and April 26, plus two recorded failures. Exact failure causes for historical failed runs were not required for this current component and are not inferred.

The workflow display history still contains older naming that mentions “2025 (Manual)” even though current checked-in workflow name is `Build Member Profile Metrics`; workflow-run names are historical metadata and do not override current YAML.

## Failure modes

Verified/directly implied current failures include:

- missing required members columns;
- unreadable/missing S3 input object;
- invalid CSV input;
- invalid manual target-year or candidate batch-ID syntax;
- S3 permission or write failure;
- empty output: `main()` returns non-zero when `len(output) == 0`;
- incompatible upstream schema aliases causing a metric family to remain zero/blank;
- candidate compatibility object missing while a batch is active.

A metric family being zero does not automatically mean the workflow failed: speech and vote calculations intentionally degrade to zero/blank when the required optional source columns are unavailable. Operators must distinguish successful computation of zero from missing expected upstream content.

## Safe operating procedure

1. Choose the target calendar year explicitly.
2. For production/current outputs, leave `batch_id` blank.
3. For pre-promotion consumer validation, use the exact immutable Oireachtas candidate batch ID; never guess or reuse a different batch.
4. Run **Build Member Profile Metrics** manually.
5. Confirm the build step succeeds and inspect `member_profile_metrics.json` for row count/year/output keys.
6. For changes to metric logic, inspect the CSV itself and validate representative members rather than relying only on a nonzero row count.
7. Confirm the intended compatibility inputs actually contain target-year records before interpreting zeros as real political activity.
8. Do not substitute legacy `processed/votes/...` or other historical inputs unless intentionally overriding the input environment variables and documenting the reason.

## Change procedure

When changing metric definitions or input compatibility:

1. update `process/build_member_profile_metrics.py` as the authoritative implementation;
2. preserve or deliberately revise supported alias handling;
3. verify normal/manual output and candidate-batch output behavior;
4. run against a test/immutable candidate when the change can affect Oireachtas promotion consumers;
5. re-run deterministic and AI member-profile consumers if their expected columns/semantics change;
6. update this page and the related Instagram pages;
7. do not fork new year-specific metric logic into `build_member_profile_metrics_2025.py`.

Metric-definition changes are downstream data-contract changes and should not be hidden as presentation-only updates.

## Security boundary

The builder uses AWS credentials supplied by GitHub Actions. No OpenAI credential is required for metric computation itself.

Input data is read from S3 and derived metrics are written back to S3. Exact live IAM permissions and bucket policy remain external to checked-in source.

No secrets or credential values belong in documentation or output artifacts.

## Known limitations

- The workflow filename still carries `_2025` although the current workflow accepts arbitrary four-digit years.
- The normal-mode output namespace `processed/members/` remains outside the canonical `processed/oireachtas_unified/` logical namespace for compatibility with current Instagram consumers.
- Speech metrics depend on the classified debate compatibility dataset and count its retained classified rows; they are not a separate authoritative count of all parliamentary utterances.
- Top issue is determined by count with alphabetical tie-break, not editorial weighting.
- Vote participation uses distinct vote IDs present in the compatibility input and does not explain absences or reasons.
- Missing compatible optional source columns can yield zero/blank metric families without a hard failure.
- There is no checked-in formal typed schema/version object for this metrics product beyond code and consuming workflows.
- Dedicated unit tests for the metric formulas were not identified in the current `tests/` inventory during this audit; current confidence comes from implementation review, Oireachtas consumer integration, and observed workflow runs.

## Next safe development action

Document the Reusable LLM Task Runner Framework from current source, including YAML task schema, S3 read/write contract, OpenAI Responses API behavior, resume/overwrite semantics, retries/autosave, optional web search, output validation, current task definitions, and manual controller workflow.

## Related documents

- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)
- [Instagram and constituency campaign rendering system](/projects/systems/instagram-constituency-campaign-rendering/)
- [AI member-profile and Instagram visual content workflow](/projects/systems/instagram-ai-member-profile-content-workflow/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)

## Verification record

- Last verified: `2026-08-07`
- Verified implementation/configuration: `process/build_member_profile_metrics.py`; `process/build_member_profile_metrics_2025.py`; `.github/workflows/build_member_profile_metrics_2025.yml`; current Oireachtas S3/batch helpers and downstream contract paths already verified in P0; current deterministic/AI consumer paths.
- Observed runtime evidence: workflow ID `266755732`; latest run `29299647855` plus run history and job-step conclusions.
- Verification scope: inputs, aliases, target-year behavior, exact metric formulas, output schema/paths, candidate-batch integration, manual workflow, consumers, security boundary, failure modes, historical wrapper relationship, and limitations.
