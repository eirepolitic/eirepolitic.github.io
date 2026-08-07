---
title: bb-comp-prices end-to-end orchestration and security boundary
summary: Verified controller, GitHub Actions, configuration, authentication, stage dependency, failure, and safe-rerun contract for the bb-comp-prices platform.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 31
permalink: /projects/systems/bb-comp-prices-orchestration-security/
tags:
  - github-actions
  - orchestration
  - security
  - aws
  - playwright
---

# bb-comp-prices end-to-end orchestration and security boundary

## Summary

The current `bb-comp-prices` end-to-end control plane is a Python controller invoked by a manually dispatched GitHub Actions workflow. It can run Best Buy extraction, category discovery, Amazon.ca acquisition, and product matching in one process, with a shared `run_id` and S3-backed outputs.

The verified controller is not a general dependency scheduler. It executes selected stages in fixed source-code order, stops on the first raised stage exception, and relies on existing S3 `latest/` products for stages whose upstream producers were not run earlier in the same invocation.

Walmart is accepted as a competitor selection but is explicitly recorded as `blocked`; current orchestration does not run a Walmart extraction stage.

## Current Implementation State

The active orchestration path is:

```text
GitHub Actions workflow_dispatch
  -> .github/workflows/end_to_end.yml
  -> Python 3.12 + bb-comp-prices[browser] + Chromium
  -> scripts/run_end_to_end.py
  -> src/bb_comp_prices/pipeline/orchestrator.py::run_end_to_end
       -> Best Buy extraction (optional)
       -> category discovery (optional)
       -> Amazon extraction (optional and only if Amazon selected)
       -> Walmart blocked record (if Walmart selected)
       -> product matching (optional)
  -> S3 stage outputs
  -> S3 end-to-end summary on successful controller completion
  -> S3 run manifest in script finally block
  -> GitHub artifact/job summary
```

The workflow is manual only (`workflow_dispatch`) in the verified source. No cron/schedule trigger is defined in `.github/workflows/end_to_end.yml`.

## Source of Truth

- Controller: `src/bb_comp_prices/pipeline/orchestrator.py`.
- Script wrapper/run manifest: `scripts/run_end_to_end.py`.
- GitHub Actions workflow: `.github/workflows/end_to_end.yml`.
- General CLI: `src/bb_comp_prices/cli.py`.
- Settings model and environment overrides: `src/bb_comp_prices/config.py`.
- Shared HTTP client: `src/bb_comp_prices/http.py`.
- S3 implementation: `src/bb_comp_prices/storage/s3.py`.
- Stage producers: `src/bb_comp_prices/pipeline/category_discovery.py`, `bestbuy_extract.py`, `amazon_extract.py`, `product_matching.py`.
- Storage/data contract: [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/).

`docs/BUILD_PLAN.md` is lower-precedence planning evidence and is not used as proof of deployed scheduling, IAM, or stage behavior.

## Trigger and Runtime

`.github/workflows/end_to_end.yml` exposes one `workflow_dispatch` job on `ubuntu-latest` with:

- Python `3.12`;
- `pip install -e ".[browser]"`;
- Playwright Chromium installed with `python -m playwright install --with-deps chromium`;
- job timeout `240` minutes;
- concurrency group `bb-comp-prices-end-to-end`;
- `cancel-in-progress: false`.

The concurrency group prevents overlapping executions of this workflow group from being intentionally cancelled in favor of a newer run. Exact GitHub queue behavior is platform-managed.

The workflow repository permission is `contents: read`. AWS access is provided separately through environment variables populated from GitHub Secrets.

## Workflow Inputs

| Input | Default | Controller meaning |
| --- | ---: | --- |
| `stages` | `bestbuy,amazon,matching` | Comma-separated subset of `bestbuy`, `category`, `amazon`, `matching`, or `all`. |
| `competitors` | `amazon,walmart` | Comma-separated subset of `amazon`, `walmart`, or `all`. |
| `max_category_products` | `100` | Maximum discovered category products per category browser pass. |
| `max_show_more_clicks` | `10` | Maximum category lazy-load/show-more rounds. |
| `amazon_max_queries_per_product` | `0` | `0` means all generated Amazon queries. |
| `amazon_max_pages_per_query` | `5` | Maximum Amazon result pages per query. |
| `amazon_max_results_per_query` | `0` | `0` means retain all results from scanned pages. |
| `amazon_max_candidates_per_product` | `0` | `0` means all qualifying ASINs; otherwise cheapest N. |
| `matched_threshold` | `75` | Generic automatic-match threshold passed to product matching. |
| `review_threshold` | `60` | Generic review threshold; must be below matched threshold. |

`_parse_selection()` rejects unsupported stage/competitor values. `all` expands to every value in the corresponding valid tuple.

## Stage Order and Dependency Contract

`run_end_to_end()` always evaluates selected stages in this code order:

1. `bestbuy`
2. `category`
3. `amazon`
4. Walmart blocked record when Walmart is selected
5. `matching`

This order has operational consequences.

### Best Buy stage

Calls `run_bestbuy_extract(settings, products_path, run_id=run_id)`. The wrapper default `products_path` is `config/test_products.yaml` because the end-to-end GitHub workflow does not expose a products-path input.

This stage does **not** automatically consume category discovery from the same run.

### Category stage

Calls `run_category_pipeline()` using `config/test_categories.yaml` by wrapper default. It publishes current Marketplace discovery data, but it runs **after** Best Buy extraction in the same controller invocation.

Therefore, selecting `bestbuy,category` does not mean "discover then extract." To extract newly discovered products, the verified separate path is `src/bb_comp_prices/pipeline/bestbuy_discovered_batch.py`/the corresponding discovered-batch workflow, followed by Best Buy extraction.

### Amazon stage

Runs only when both conditions are true:

- `amazon` is in selected stages; and
- `amazon` is in selected competitors.

It reads `latest/bestbuy_products.parquet` from S3. The controller does not verify that the Best Buy data came from the current `run_id`; if the Best Buy stage is omitted, Amazon uses whatever compatible object currently exists at that stable key.

### Walmart selection

If `walmart` is selected as a competitor, the controller appends a `blocked` stage record and warning:

> Walmart extraction skipped because unattended Walmart.ca search/PDP requests redirect to an identity-verification challenge.

There is no current Walmart extraction call in `run_end_to_end()`.

Because the workflow default competitors are `amazon,walmart`, the default successful controller result includes a Walmart warning and therefore has overall status `succeeded_with_warnings` rather than plain `succeeded`.

### Matching stage

Calls `run_product_matching()` whenever `matching` is selected, regardless of whether Amazon acquisition ran in the same invocation.

If Amazon is not selected as a competitor, the controller adds a warning but still executes matching. The matching implementation reads current `latest/bestbuy_products.parquet` and `latest/amazon_products.parquet` from S3. This makes matching a valid isolated rerun only when those latest inputs are known-good and compatible.

## Controller Status and Failure Semantics

Each selected executable stage is wrapped by an internal `execute()` helper that records duration and result. On a stage exception it appends a failed stage result and immediately re-raises the exception.

This means the controller is **fail-fast**:

- later stages do not run after a raised stage failure;
- the code that constructs/writes the normal end-to-end summary at the bottom of `run_end_to_end()` is not reached on that exception;
- partial stage outputs already written to S3 remain present because there is no rollback transaction.

On successful completion, overall controller status is:

- `failed` only if a failed stage somehow exists in the completed result path;
- `succeeded_with_warnings` when warnings exist;
- otherwise `succeeded`.

In the current fail-fast implementation, ordinary executable-stage exceptions escape before the summary is built, so failed controller runs are primarily represented by the run manifest and stage-specific evidence rather than a completed end-to-end summary.

## S3 Run Evidence

On successful controller completion, `run_end_to_end()` writes:

```text
bb-comp-prices/runs/date=YYYY-MM-DD/run_id=<run_id>/end_to_end_summary.json
bb-comp-prices/latest/end_to_end_summary.json
```

The summary contains run ID, status, UTC start/completion/duration, selected stages/competitors, Amazon controls, warnings, per-stage results, and its own S3 URIs.

`scripts/run_end_to_end.py` independently creates a `RunManifest`. Its `finally` block writes:

```text
bb-comp-prices/manifests/end-to-end-<run_id>.json
```

That manifest write is attempted whether the controller succeeds or raises. On success it contains row-count summaries, warnings, and summary URIs. On controller failure it contains `status: failed` and the exception text.

A failure in the final S3 manifest write itself can mask or compound the original failure at process level; there is no secondary local persistence fallback in the script.

## GitHub Run Evidence

The workflow executes:

```bash
python scripts/run_end_to_end.py ... | tee end-to-end-results.json
```

Then, with `if: always()`:

- uploads `end-to-end-results.json` as artifact `end-to-end-results-<github.run_id>` when present, with retention `30` days and `if-no-files-found: warn`;
- writes a GitHub job summary, displaying the file if present or noting that the controller failed before writing its summary artifact.

The durable operational record is S3 plus the GitHub workflow/run logs. Artifact retention is bounded and should not be treated as long-term storage.

## Configuration Boundary

`src/bb_comp_prices/config.py::load_settings()` loads YAML then applies environment overrides only to AWS settings.

| Setting/environment | Current behavior |
| --- | --- |
| `aws.region` | YAML/default, overridden by `AWS_REGION` when present. |
| `aws.bucket` | YAML/default, overridden by `BB_COMP_S3_BUCKET` when present. |
| `aws.prefix` | YAML/default, overridden by `BB_COMP_S3_PREFIX` when present. |
| `user_agent` | YAML/default; no environment override in current loader. |
| `request_timeout_seconds` | YAML/default; used by `HttpClient`. |
| `max_retries` | YAML/default exists, but shared `HttpClient.get()` currently hard-codes `stop_after_attempt(3)` rather than reading this setting. |
| `default_postal_code` | YAML/default; used by Best Buy location/shipping paths, with stage-level fallback to `V5Y1L3` in current producers. |

Verified file values are region `ca-central-1`, bucket `eirepolitic-data`, prefix `bb-comp-prices`, user-agent `bb-comp-prices/0.1`, request timeout `30`, max retries `3`, and postal code `V5Y1L3`.

The end-to-end workflow sets `AWS_REGION` and `AWS_DEFAULT_REGION` to `ca-central-1`. `AWS_DEFAULT_REGION` is not read explicitly by `load_settings()` but can be used by AWS tooling/SDK behavior outside that loader.

## HTTP and Browser Boundary

The shared `HttpClient` uses `httpx.Client` with:

- configured user agent;
- `Accept-Language: en-CA,en;q=0.9`;
- HTML/JSON accept header;
- configured timeout;
- redirects enabled;
- retries only for `httpx.TimeoutException` and `httpx.TransportError`;
- fixed maximum three attempts with exponential jitter, initial 1 second and maximum 8 seconds.

HTTP status codes are not automatically raised by `HttpClient.get()`; callers decide whether a returned response is acceptable.

Browser-dependent code imports Playwright at execution time. The end-to-end workflow always installs the browser extra and Chromium even when the selected stages may not require a browser. Browser execution occurs on the GitHub-hosted runner and is an external-network trust boundary.

## Authentication and Security Boundary

The end-to-end workflow has GitHub repository permission:

```text
contents: read
```

AWS credentials are injected into the job environment from GitHub Secrets named:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Their values are not stored in repository source and must not be copied into documentation, artifacts, manifests, or logs.

Verified trust boundaries are:

```text
GitHub repository source
  -> GitHub-hosted Actions runner
     -> public Best Buy/Amazon network endpoints
     -> Playwright/Chromium browser process
     -> AWS API/S3 using secret-backed credentials
```

Repository source does not prove the exact live IAM user/role, policy, bucket policy, encryption configuration, or account-level controls. Those remain unverified until sanitized authoritative AWS evidence is specifically required.

The current workflow uses long-lived-style AWS access-key environment variable names rather than an inspected OIDC role-assumption flow. This statement describes the repository interface only; it does not infer credential age or account policy.

## Safe Rerun Procedure

Before rerunning, determine whether the failure occurred before or after durable upstream publication.

1. Open the failed GitHub Actions run and identify the first failing controller/stage error.
2. Record the `run_id` from available output, manifest path, or stage evidence when present.
3. Inspect `bb-comp-prices/manifests/end-to-end-<run_id>.json` if it was successfully written.
4. Inspect stage-specific raw/error objects and any curated/history outputs associated with that run ID.
5. Do **not** assume later stages ran after the first raised exception.
6. For an isolated Amazon rerun, first verify `latest/bestbuy_products.parquet` is the intended compatible input.
7. For an isolated matching rerun, first verify both `latest/bestbuy_products.parquet` and `latest/amazon_products.parquet` are the intended compatible inputs.
8. For newly discovered Best Buy Marketplace products, do not rely on `category` + `bestbuy` in the same end-to-end invocation; use the discovered-batch extraction path in the correct order.
9. Re-run only the smallest stage set needed, using bounded category/Amazon controls where diagnosis or cost/runtime exposure should be limited.
10. Confirm new manifests, stage outputs, and latest publications before treating recovery as complete.

Reruns are not transactional rollbacks. Historical objects remain by run/date, while successful `latest/` publications replace stable keys.

## Failure Modes and Recovery

### Invalid selection or thresholds

Symptoms: immediate `ValueError` for unsupported values, or `review threshold must be below matched threshold`.

Safe action: correct dispatch inputs; no retailer stage should have run before these validations complete.

### Missing or stale upstream `latest/` data

Symptoms: S3 `get_object`, Parquet, missing-column, or semantically stale-input behavior during Amazon/matching.

Safe action: verify/re-run the upstream producer first. Do not create synthetic replacement objects merely to make the downstream stage start.

### Retailer challenge/network/parser failure

Symptoms: stage exception, source-specific validation/probe evidence, missing normalized records.

Safe action: inspect existing raw/probe evidence and source-specific diagnostics before changing production parser logic or repeatedly retrying.

### AWS authentication/authorization failure

Symptoms: STS/S3 access errors or failure writing manifests/data.

Safe action: confirm secret configuration names and workflow error details; use the repository S3 smoke workflow if appropriate. Never expose secret values. Exact IAM diagnosis may require sanitized AWS evidence if repository source is insufficient.

### Workflow timeout

The end-to-end job has a hard 240-minute workflow timeout. A terminated run can leave partial S3 outputs because writes occur during each stage and no rollback exists.

Safe action: inspect run/history objects before rerunning. Use narrower stage/coverage controls rather than automatically increasing the timeout, because timeout/cost architecture changes require an explicit decision.

### Walmart selected

This is currently an expected blocked condition, not an executable Walmart failure. The controller records a warning/blocked stage and can otherwise complete.

## Validation

Relevant automated coverage includes `tests/unit/test_orchestrator.py` plus unit tests for the underlying Best Buy, Amazon, matching, configuration, and retailer-specific logic. Repository CI runs:

```bash
ruff check .
pytest --cov=bb_comp_prices --cov-report=term-missing
bb-comp-prices --config config/settings.yaml validate-config
```

Operational verification for an end-to-end run should include GitHub workflow conclusion, run manifest status, expected per-stage S3 outputs, and—on successful controller completion—the history/latest end-to-end summary.

## Known Limitations

- Stage dependency readiness is not automatically validated before execution.
- The fixed stage order makes same-run category discovery occur too late to feed the same-run Best Buy extraction.
- Matching can run against an older Amazon latest dataset even when Amazon was not selected; the controller warns only when Amazon is excluded as a competitor, not when the Amazon stage is simply omitted.
- Amazon acquisition likewise can use an older Best Buy latest dataset when Best Buy is omitted.
- Walmart remains blocked in the end-to-end controller.
- No schedule/cron is defined for this workflow.
- No transaction spans S3 writes across stages; partial outputs can survive failures.
- Normal end-to-end summary JSON is not written when an executable stage exception escapes before summary construction; the manifest is the intended failure record when its final write succeeds.
- `PipelineSettings.max_retries` is not currently wired into the shared HTTP retry decorator; retries are fixed at three attempts there.
- The workflow always installs Playwright/Chromium, even for stage combinations that may not need browser execution.
- Live IAM, S3 policy, encryption, versioning, and credential-management details beyond repository interfaces are unverified.

## Outstanding Work

- Document Best Buy category discovery and Best Buy extraction as subordinate operational components.
- Document Amazon recovery/search-health behavior in detail.
- Document matching thresholds and strict Amazon variant-gate behavior.
- Document validation/readiness rules and source-specific probe framework.
- Any redesign of stage ordering, dependency enforcement, Walmart handling, AWS authentication mechanism, scheduling, concurrency, or timeout is an architecture/security/cost decision and is outside this documentation change.

## Next Safe Development Action

Document the current Best Buy pipeline without changing orchestration. Verify category discovery/classification, discovered-batch handoff, PDP parsing, offers/availability clients, extraction workflows, current validation reports, and exact recovery paths. Preserve the orchestration limitation that category discovery does not feed Best Buy extraction inside the same end-to-end run.

## Related Documents

- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)
- [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)
- [bb-comp-prices documentation workstream plan](/projects/high-director/bb-comp-prices-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main` commit `d24c5bd98a6764bd75476fbf31c6441657305640`; `src/bb_comp_prices/pipeline/orchestrator.py`; `scripts/run_end_to_end.py`; `.github/workflows/end_to_end.yml`; `src/bb_comp_prices/cli.py`; `config.py`; `http.py`; current stage producers and S3 contract.
- Verified by: High Director
- Verification scope: manual trigger, workflow inputs, stage order/selection/dependencies, concurrency/timeout, browser runtime, configuration/environment overrides, HTTP retry boundary, AWS secret names, S3 summary/manifests, fail-fast behavior, safe rerun procedure, and live-cloud unknowns.
