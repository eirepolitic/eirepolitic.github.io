---
title: bb-comp-prices Best Buy Marketplace category discovery
summary: Verified browser discovery, availability-based ownership classification, condition filtering, S3 outputs, validation, and extraction handoff for Best Buy Canada categories.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 32
permalink: /projects/systems/bb-comp-prices-bestbuy-category-discovery/
tags:
  - best-buy
  - playwright
  - discovery
  - marketplace
---

# bb-comp-prices Best Buy Marketplace category discovery

## Summary

The Best Buy category-discovery subsystem discovers product-detail links from configured Best Buy Canada category pages, deduplicates product IDs across categories, classifies Best Buy-owned versus Marketplace products using the availability endpoint, determines condition where possible, and publishes both the complete classification set and a filtered new-condition Marketplace handoff dataset.

The subsystem uses browser automation only for category-page discovery. Classification primarily uses Best Buy's availability endpoint and listing title; a product PDP is fetched only when a Marketplace product's condition cannot be inferred from its discovered title.

## Current Implementation

Primary implementation paths:

- browser discovery: `src/bb_comp_prices/bestbuy/category_discovery.py`;
- availability classification: `src/bb_comp_prices/bestbuy/availability_client.py`;
- embedded PDP state parsing: `src/bb_comp_prices/bestbuy/initial_state.py`;
- pipeline and publication: `src/bb_comp_prices/pipeline/category_discovery.py`;
- current-data validation: `src/bb_comp_prices/pipeline/category_validation.py`;
- discovered-product handoff: `src/bb_comp_prices/pipeline/bestbuy_discovered_batch.py`;
- CLI command: `bb-comp-prices ... bestbuy-category-discover` in `src/bb_comp_prices/cli.py`;
- manual workflow: `.github/workflows/bestbuy_category_discover.yml`.

The latest committed validation report, `docs/LATEST_CATEGORY_DISCOVERY_REPORT.md`, reports 57 discovered/classified rows, 30 Best Buy-owned rows, 27 Marketplace rows across all conditions, 3 new-condition Marketplace rows, 0 failed classifications, and all implemented validation checks passing. This is dated repository evidence of one observed latest dataset, not a guarantee of future retailer behavior or coverage.

## Inputs

`config/test_categories.yaml` currently contains five configured phone categories:

- `743355` — Unlocked Phones;
- `743360` — Unlocked Android Phones;
- `12535387` — Unlocked Samsung Phones;
- `12535497` — Unlocked Google Phones;
- `743358` — iPhone Unlocked.

The workflow defaults are `max_products=100` and `max_show_more_clicks=10`. The Python browser function supports larger defaults (`500` and `30`) when called directly unless overridden by the pipeline/wrapper.

The configured postal code is used for the availability request; current settings supply `V5Y1L3`, and the pipeline also falls back to that value if the setting is empty.

## Browser Discovery Logic

`discover_category_products()` launches headless Chromium with:

- locale `en-CA`;
- timezone `America/Vancouver`;
- viewport `1440x1200`.

It navigates with `wait_until="domcontentloaded"` and fails when no response is returned or the navigation status is at least 400. It then attempts a bounded `networkidle` wait and a short additional delay.

Discovery scans links matching:

```text
a[href*="/en-ca/product/"]
```

The browser repeatedly scrolls to the bottom of the page and looks for visible controls containing `Show more` or `Load more`. It stops when the product limit is reached, the click limit is reached, or two stagnant rounds occur without a clickable load-more control.

A URL qualifies as a product only when its path contains `/product/` and ends in a numeric identifier of at least six digits. Duplicate product IDs are discarded while preserving first-seen order.

## Cross-Category Deduplication

`run_category_pipeline()` maintains one `seen_product_ids` set across every configured category in the run. `_deduplicate_discovered_products()` drops a product already discovered in an earlier category.

Consequences:

- the same Best Buy product appears at most once in the run-level published dataset;
- its retained `category_id`, `category_url`, and `source_position` correspond to the first configured category in which it survived discovery;
- this is not a many-to-many category-membership dataset.

## Ownership Classification

For each category's newly discovered IDs, `BestBuyAvailabilityClient.get_availability()` calls:

```text
https://www.bestbuy.ca/ecomm-api/availability/products
```

with `accept`, `accept-language`, `locations`, `postalCode`, and pipe-separated `skus` query parameters. IDs are batched in groups of 50 by default.

The client requires HTTP status 200 and an `availabilities` list. Returned items are keyed by `sku`.

For each discovered product, the pipeline requires an availability record and non-empty `sellerId`.

Ownership rule:

```text
sellerId case-insensitively equals "bbyca" -> Best Buy-owned
otherwise                                  -> Marketplace
```

If availability data is missing, malformed, or lacks `sellerId`, that product becomes a failed classification record rather than being silently omitted.

## Condition Classification

The pipeline first inspects the discovered listing title:

- title contains `open box` -> `Open Box`;
- title contains `refurbished` -> `Refurbished`;
- title contains `brand new` -> `Brand New`;
- otherwise condition is unknown at this point.

For a Best Buy-owned record, an unknown title-derived condition does not trigger a PDP fetch because Marketplace new-condition filtering is the relevant purpose.

For a Marketplace record with unknown condition, the pipeline fetches the PDP and saves the HTML under `raw/bestbuy/category_classification/...`. It parses `window.__INITIAL_STATE__`, requires `product.product`, verifies that `isMarketplace` is exactly true, then obtains the title and condition from `grade` or `condition`.

A condition qualifies as new only when case/hyphen-normalized text is exactly `new` or `brand new`.

This is intentionally strict: unknown, open-box, refurbished, or other condition strings do not enter the new-condition Marketplace export.

## Record States

Every discovered product that reaches classification processing becomes a `BestBuyCategoryProductRecord` with `classification_status`:

- `classified` — ownership and required evidence were resolved; or
- `failed` — an exception occurred for that product.

Failed records retain product/category/URL/title context plus `classification_error` and any raw S3 URI captured before failure.

The filtered Marketplace handoff contains only records satisfying all three conditions:

```text
classification_status == "classified"
is_marketplace == true
is_new_condition == true
```

## Outputs

The complete classification output is written as CSV and Parquet to history and latest keys:

```text
curated/bestbuy_category_products_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
latest/bestbuy_category_products.{csv,parquet}
```

The filtered new-condition Marketplace subset is written only when non-empty:

```text
curated/bestbuy_marketplace_discovery_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
latest/bestbuy_marketplace_discovery.{csv,parquet}
```

Per-category availability evidence is written to:

```text
raw/bestbuy/category_availability/date=YYYY-MM-DD/run_id=<run_id>/category_id=<category_id>.json
```

Marketplace classification PDPs are written when needed to:

```text
raw/bestbuy/category_classification/date=YYYY-MM-DD/run_id=<run_id>/product_id=<id>.html
```

Classification errors, when any, are collected under:

```text
errors/bestbuy_category_discovery/date=YYYY-MM-DD/run_id=<run_id>.json
```

See [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/) for schema/serialization details.

## Extraction Handoff

`src/bb_comp_prices/pipeline/bestbuy_discovered_batch.py::load_discovered_marketplace_products()` reads only:

```text
latest/bestbuy_marketplace_discovery.parquet
```

It requires columns `bestbuy_product_id` and `pdp_url`, deduplicates again by product ID, converts rows to the product-list shape expected by Best Buy extraction, and applies a configurable row limit (`25` by default in the function).

This handoff is a separate operation. The end-to-end controller currently runs `bestbuy` before `category`, so selecting both stages in one end-to-end invocation does not make newly discovered category products feed that same run's Best Buy extraction.

## Workflow Operation

`.github/workflows/bestbuy_category_discover.yml` is `workflow_dispatch` only. It:

1. checks out source;
2. uses Python 3.12;
3. installs `bb-comp-prices[browser]`;
4. installs Chromium;
5. runs `bb-comp-prices --config config/settings.yaml bestbuy-category-discover` with configured categories and dispatch limits;
6. captures the JSON CLI result as `category-discovery-results.json`;
7. uploads it as a GitHub artifact retained for 14 days;
8. writes the result into the job summary.

The job receives AWS region and credentials through the same secret-backed environment boundary documented in the orchestration/security page.

## Validation

`build_category_validation_markdown()` reads both CSV and Parquet forms of the two `latest/` products and checks:

- all-output CSV/Parquet row counts match;
- Marketplace-output CSV/Parquet row counts match;
- product ID sets match between formats;
- discovered product IDs are unique;
- Marketplace export IDs are a subset of the full dataset;
- every Marketplace-export row is Marketplace;
- every Marketplace-export row is new condition;
- classified ownership counts balance between Marketplace and Best Buy-owned rows.

The current committed report records all these checks as passing for the observed 57-row dataset.

Relevant unit coverage includes `tests/unit/test_category_discovery.py`, `test_initial_state.py`, and the shared configuration/parser tests.

## Failure Modes and Safe Recovery

### Category navigation/browser loading fails

Symptoms: navigation exception/status failure or zero discovered products.

Safe recovery: inspect the current category URL manually through repository configuration and use category/browser probe evidence before modifying selectors. A retailer page-layout or challenge change should not be solved by increasing click limits blindly.

### Availability endpoint fails

Symptoms: non-200 response aborts the category's availability call; malformed payload raises.

Safe recovery: inspect the endpoint/probe evidence and network response. A whole-call failure is different from an individual product lacking an availability record.

### Individual product classification fails

Symptoms: product is retained with `classification_status=failed`; an error JSON is published.

Safe recovery: inspect `classification_error` and `raw_s3_uri` when present. Re-run only after identifying whether the issue is transient, title logic, availability contract, or PDP initial-state parsing.

### Filtered Marketplace output is empty

The writer is not called for the Marketplace subset when no records qualify, so no new `latest/bestbuy_marketplace_discovery.*` object is written by that run.

This means an older stable latest object can remain in S3. Operators must not infer that an existing `latest/bestbuy_marketplace_discovery.parquet` was produced by the most recent category run without checking run evidence/history.

### Overlapping categories

Cross-category deduplication intentionally keeps only first-seen membership. Do not interpret absence of repeated category rows as missing deduplication.

## Security and Access

The subsystem accesses public Best Buy Canada category/PDP/availability endpoints and writes evidence to S3. Playwright executes on the runner. AWS credential values come from GitHub Secrets and must not be logged or documented.

Raw HTML/availability responses are evidence objects and may contain more source-site metadata than curated records; protect them under the same S3 access boundary.

No live Best Buy authentication credential is present in the inspected implementation.

## Known Limitations

- Discovery depends on current Best Buy page links and visible load-more behavior.
- Cross-category deduplication loses secondary category membership.
- New-condition recognition is intentionally narrow (`new`/`brand new` after normalization).
- Marketplace identity relies on `sellerId != bbyca`; a retailer contract change could invalidate that rule.
- A Marketplace PDP is fetched only when title condition is unknown; classification behavior is therefore evidence-path dependent.
- Empty filtered results do not clear the prior `latest/bestbuy_marketplace_discovery.*` object.
- The latest committed validation report proves one observed dataset, not completeness of all Marketplace inventory.
- Same-run end-to-end stage order does not provide discovery-to-extraction chaining.

## Next Safe Development Action

Document the Best Buy product/Marketplace-offer extraction path from `bestbuy_extract.py`, `parse_product.py`, `offers_client.py`, `availability_client.py`, the discovered-batch workflow, extraction workflow, current extraction validation, and exact seller/offer normalization rules. Do not change retailer contracts or stage ordering while documenting them.

## Related Documents

- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)
- [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)
- [bb-comp-prices end-to-end orchestration and security boundary](/projects/systems/bb-comp-prices-orchestration-security/)
- [bb-comp-prices documentation workstream plan](/projects/high-director/bb-comp-prices-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main` commit `d24c5bd98a6764bd75476fbf31c6441657305640`; `bestbuy/category_discovery.py`; `bestbuy/availability_client.py`; `bestbuy/initial_state.py`; `pipeline/category_discovery.py`; `pipeline/category_validation.py`; `pipeline/bestbuy_discovered_batch.py`; `config/test_categories.yaml`; `.github/workflows/bestbuy_category_discover.yml`; `docs/LATEST_CATEGORY_DISCOVERY_REPORT.md`.
- Verified by: High Director
- Verification scope: discovery mechanics, deduplication, ownership/condition classification, raw/curated/latest outputs, validation checks, workflow operation, extraction handoff, failure recovery, and current limitations.
