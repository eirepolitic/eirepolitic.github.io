---
title: bb-comp-prices Amazon.ca competitor acquisition and recovery
summary: Verified Amazon.ca search, search-health gating, candidate filtering, detail recovery, search fallback, offer normalization, validation, and safe rerun behavior.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 34
permalink: /projects/systems/bb-comp-prices-amazon-acquisition/
tags:
  - amazon
  - playwright
  - competitor-pricing
  - recovery
---

# bb-comp-prices Amazon.ca competitor acquisition and recovery

## Summary

The Amazon.ca acquisition subsystem reads current Best Buy normalized products from S3, searches Amazon.ca through Playwright, verifies search-run health before allowing publication, scores and prefilters candidate ASINs, attempts detail-page recovery, normalizes accepted products/offers, and persists both accepted and rejected candidate evidence.

The subsystem has two distinct accepted verification levels:

- `detail` — the ASIN detail page resolved with an acceptable title and passed the exact variant gate plus detail score threshold;
- `search` — the detail page did not yield a usable title, but the exact observed search result passed the stricter search-fallback threshold and exact variant gate.

A search-verified product is intentionally not equivalent to a detail-verified product: it has no resolved buy-box evidence and produces no Amazon offer rows. The downstream matching engine treats these states differently.

## Source of Truth

- production pipeline: `src/bb_comp_prices/pipeline/amazon_extract.py`;
- search/browser acquisition: `src/bb_comp_prices/competitors/amazon_probe.py`;
- search-health gate: `src/bb_comp_prices/pipeline/amazon_search_health.py`;
- candidate scoring/detail browser recovery: `src/bb_comp_prices/competitors/amazon_details_probe.py`;
- exact phone-variant rules: `src/bb_comp_prices/competitors/amazon_variant.py`;
- normalization/search fallback/offers: `src/bb_comp_prices/competitors/amazon_normalize.py`;
- executable wrapper: `scripts/run_amazon_exhaustive.py`;
- workflow: `.github/workflows/amazon_extract.yml`;
- current validation logic: `src/bb_comp_prices/pipeline/amazon_validation.py`;
- current committed validation evidence: `docs/LATEST_AMAZON_EXTRACTION_REPORT.md`.

Older probe/diagnostic reports are historical evidence and do not override the current executable health gate.

## Input Contract

`load_bestbuy_products()` reads:

```text
s3://eirepolitic-data/bb-comp-prices/latest/bestbuy_products.parquet
```

Each row becomes `AmazonSearchInput` with:

- `bestbuy_product_id`;
- `title`;
- optional `brand`;
- optional `model_number`;
- zero or more UPCs.

The pipeline does not verify that this latest Best Buy dataset was produced in the same run. An isolated Amazon rerun therefore depends on the operator confirming that the stable Best Buy latest object is the intended upstream input.

## Search Query Generation

`build_amazon_queries()` derives a deduplicated ordered query list from available source evidence:

1. core title with common phone/noise terms removed;
2. full title;
3. brand + model;
4. model;
5. each UPC;
6. brand + core title + capacity + colour;
7. brand + core title.

Queries are case-insensitively deduplicated. `max_queries_per_product=0` means no query-count truncation.

The current workflow defaults are:

- all generated queries;
- maximum 5 result pages per query;
- all results from scanned pages;
- all qualifying candidate ASINs.

These breadth controls can be reduced for a bounded diagnostic/recovery run.

## Browser Search Acquisition

Search uses headless Playwright Chromium with:

- locale `en-CA`;
- timezone `America/Vancouver`;
- viewport `1440x1200`;
- a Chromium-style desktop user agent.

Search pages use `https://www.amazon.ca/s?k=<query>` and `&page=<n>` for later pages. Current defaults include a 45-second navigation timeout, 10-second delay between requests, up to three navigation attempts per page, and increasing retry backoff.

Result cards are selected from:

```text
div[data-component-type="s-search-result"][data-asin]
```

The extractor records ASIN, title candidates, detail link, price text, sponsored marker, text preview, page number, and global position. Title selection rejects common price/ad/delivery noise and can fall back to useful card text.

ASINs are deduplicated within a query. Pagination stops when configured limits are met, no new results appear, the next button is disabled, or no next link exists.

## Search Blocking and Health Gate

The search layer records challenge/availability indicators including:

- CAPTCHA text;
- robot check;
- access denied;
- service unavailable;
- generic Amazon error text, including the implemented French marker;
- HTTP 429 as `rate_limited`;
- HTTP 5xx as `http_5xx`.

When a blocked page is detected, the browser stops subsequent searches. This can leave later product reports with no searches; the health layer treats that incompleteness as unhealthy.

`summarize_amazon_search_health()` marks a run healthy only when:

```text
result_count > 0
AND every searched page is healthy
AND every source product received searches
```

An unhealthy search run is a hard publication gate. Before raising `AmazonSearchUnavailableError`, `run_amazon_extract()` writes raw evidence containing search health and search reports to:

```text
raw/amazon/date=YYYY-MM-DD/run_id=<run_id>/probe.json
```

It then refuses to publish/overwrite the Amazon latest datasets.

This current behavior is an important recovery safeguard. The older committed `docs/LATEST_AMAZON_RUN_DIAGNOSTICS.md` includes historical runs from July 20, 2026 that recorded zero search results as `succeeded`; those manifests predate the current search-health behavior and must not be used to describe current success semantics.

## Search Candidate Scoring

`score_amazon_candidate()` is a retailer-acquisition candidate score, not the final cross-source product-matching confidence score.

Immediate zero-score conditions include:

- accessory terms;
- renewed/refurbished/used/open-box terms;
- disjoint explicit capacities;
- disjoint recognized colours.

Otherwise the score uses RapidFuzz token-set title similarity plus evidence adjustments:

- base token-set ratio;
- brand present: `+10`; brand absent: `-20` when a source brand exists;
- source model found in candidate: `+20`;
- explicit capacity present on both sides: `+20` after mismatch rejection;
- recognised colour overlap: `+15`;
- source colour present but candidate colour absent: `-10`.

The candidate score is clamped to `0..150`. Production `run_amazon_extract()` defaults the minimum search candidate score to `65`.

`select_amazon_candidates()` keeps only the highest-scoring occurrence per ASIN. With `max_candidates_per_product=0`, qualifying ASINs are sorted primarily by score. When a positive candidate cap is supplied, selection instead prioritizes the cheapest known search price, then score/position.

## Exact Variant Prefilter

Before detail navigation, `_split_prefilter_candidates()` applies `exact_variant_mismatch_reasons()`.

Implemented contradiction classes include:

- accessory;
- bundle;
- non-new condition terms;
- phone family/generation/variant mismatch for recognized Pixel, Galaxy S, and iPhone families;
- capacity mismatch;
- colour mismatch;
- candidate phone family missing when the source family is known and source model evidence is not found.

All reasons except `candidate_phone_family_missing` are blocking at the search prefilter. That one reason is deliberately allowed through to detail recovery so stronger page evidence can resolve ambiguity.

Prefiltered candidates are still published as rejected `AmazonMatchRecord` rows, with `verification_level=search`, `detail_resolved=false`, and rejection reason prefixed `search_prefilter_`.

## Detail-Page Recovery

Accepted search candidates are probed at:

```text
https://www.amazon.ca/dp/<ASIN>
```

The current recovery attempt sequence is:

1. canonical detail URL;
2. detail URL with `?th=1&psc=1`;
3. canonical detail URL again.

The default maximum is three attempts.

A detail title is sought in this order:

1. visible `#productTitle` or `h1`;
2. title metadata (`og:title`, `title`, `twitter:title`);
3. Product JSON-LD;
4. cleaned document title.

A detail page is considered resolved only when a usable title exists and no detail block marker is present.

For a resolved page, the probe also attempts to collect product-detail table rows, current price, availability, seller, ships-from text, condition text, and the all-offers display. It tries known all-offer controls, extracts up to 30 `#aod-offer` blocks, and captures relevant network responses whose URLs contain AOD/offer/buying-choice terms. These captures are diagnostic evidence; normalized offers come from parsed visible candidate data in the current normalization function.

## Detail Verification and Search Fallback

### Detail-resolved path

The detail title receives a fresh candidate score and the exact variant gate.

The default detail threshold is `65`. A candidate is rejected when:

- ASIN is missing;
- exact variant contradictions exist; or
- detail score is below the threshold.

A passing candidate becomes:

```text
verification_level = detail
detail_resolved = true
match_status = matched
```

### Search-verified fallback

When detail navigation does not produce a usable detail title, normalization can accept the exact observed search result only if all of these hold:

- ASIN exists;
- cleaned search title exists;
- exact variant mismatch list is empty;
- score is at least the search-fallback threshold.

The current fallback threshold is `90`, stricter than the default `65` search-candidate/detail threshold.

A passing fallback becomes:

```text
verification_level = search
detail_resolved = false
match_status = matched
```

Its `AmazonProductRecord` can retain observed search price but has no buy-box seller/price/ship-origin evidence and produces no Amazon offer rows.

If fallback fails, the candidate is rejected with `missing_detail_title_and_search_fallback_failed`.

## Amazon Product and Offer Normalization

A detail-verified product records ASIN, URL, title, search price, parsed buy-box price/seller/ship origin, availability, score, verification state, and the shared raw evidence URI.

For offers:

- a buy-box offer is created when both buy-box price and seller are available;
- all-offers rows are accepted only when condition normalizes to `new` or starts with `new `;
- an offer also requires a parseable CAD price and seller;
- rows are deduplicated by casefolded seller plus price;
- buy-box ID is `<asin>:buybox`;
- AOD offer IDs are `<asin>:aod:<position>`;
- `is_amazon_retail` is true only when seller normalizes to `Amazon` or `Amazon.ca`;
- `is_fulfilled_by_amazon` uses the same check against parsed ship-origin text.

The implementation does not claim broader seller identity inference beyond those explicit string rules.

## Outputs

Raw evidence:

```text
raw/amazon/date=YYYY-MM-DD/run_id=<run_id>/probe.json
```

When record collections are non-empty:

```text
curated/amazon_matches_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
latest/amazon_matches.{csv,parquet}

curated/amazon_products_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
latest/amazon_products.{csv,parquet}

curated/amazon_offers_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
latest/amazon_offers.{csv,parquet}
```

The executable wrapper always attempts a run manifest in `finally`:

```text
manifests/amazon-extract-<run_id>.json
```

On search-health or other failure, the manifest is marked failed before the exception is re-raised, assuming the final S3 manifest write itself succeeds.

## Conditional-Publication Edge Case

The health gate protects stable latest objects from an **unhealthy search run**. It does not clear stale product/offer latest objects during every healthy run.

Writes are conditional by collection:

- no match rows -> no new latest matches object;
- no normalized Amazon products -> no new latest products object;
- no normalized Amazon offers -> no new latest offers object.

Therefore a healthy search run that produces zero accepted Amazon products or zero offers can leave an older `latest/amazon_products.*` or `latest/amazon_offers.*` object in place. Consumers must use manifests/run IDs/observation timestamps rather than treating existence of a stable latest key as proof that it belongs to the newest Amazon attempt.

## Workflow Operation

`.github/workflows/amazon_extract.yml` is manual dispatch only. It exposes four breadth controls:

- max queries per product, default `0` (all);
- max pages per query, default `5`;
- max results per query, default `0` (all scanned);
- max candidates per product, default `0` (all qualifying).

The workflow:

- runs on Ubuntu with Python 3.12;
- installs `.[browser]` and Chromium;
- has a 180-minute timeout;
- uses concurrency group `bb-comp-prices-amazon-extract` with `cancel-in-progress: false`;
- uses `contents: read` repository permissions;
- injects AWS secret names `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` plus region variables;
- invokes `scripts/run_amazon_exhaustive.py`;
- uploads the JSON summary with `if: always()` and 30-day retention when present.

The wrapper itself also exposes `--minimum-search-score` and `--minimum-detail-score`, both default `65.0`, although the GitHub workflow does not expose those thresholds as dispatch inputs.

The stricter `90.0` search fallback threshold is a normalization default and is not exposed as a workflow/wrapper option in current code.

## Validation and Current Evidence

`build_amazon_validation_markdown()` checks current latest CSV/Parquet consistency plus semantic rules including:

- matched Best Buy IDs have Amazon product rows;
- offer ASINs belong to matched candidate ASINs;
- search-verified ASINs have no offers;
- search-verified products have no buy-box seller and remain unresolved;
- detail-verified products are resolved;
- all offers are `New`;
- all offer prices are positive;
- offer IDs are unique;
- every matched candidate passes the current exact variant gate when re-evaluated against Best Buy source data.

The current committed `docs/LATEST_AMAZON_EXTRACTION_REPORT.md` records:

- 9 candidate/match rows;
- 2 matched candidates and 7 rejected candidates;
- 2 Amazon product rows, both detail verified;
- 13 new-condition offers;
- all structural and semantic checks passing.

However, its separate known-ASIN diagnostic check is **not fully passing**: two expected ASINs are missing from the observed latest candidate set. This is a coverage/recovery limitation and must not be hidden by the passing structural checks.

The current report therefore supports correctness of the rows that were produced under implemented checks, but not exhaustive recovery of every known expected ASIN.

## Safe Recovery Procedure

1. Identify the failed/current Amazon `run_id` from workflow output or `manifests/amazon-extract-<run_id>.json`.
2. Inspect `raw/amazon/date=.../run_id=<run_id>/probe.json` first. For an unhealthy search run, this is intentionally persisted before the pipeline raises.
3. Check `search_health` for block signals, HTTP statuses, navigation errors, products without searches, page/query counts, and result count.
4. Do not rerun downstream matching against Amazon latest merely because stable files exist; confirm their `run_id`/observation timestamp corresponds to the intended acquisition run.
5. If the issue is search blocking or navigation instability, use a bounded rerun (fewer products indirectly via upstream scope, fewer queries/pages/results/candidates where appropriate) before broad coverage. Do not repeatedly hammer Amazon.ca or simply raise browser/runtime limits without evidence.
6. If a candidate was prefilter rejected, inspect the explicit contradiction reason before changing variant logic.
7. If detail resolution failed but search fallback matched, treat that row as search-verified rather than pretending buy-box/offers were recovered.
8. If an expected ASIN is absent, distinguish "not discovered in search", "prefilter rejected", "detail failed", and "normalization rejected" using raw evidence and match rows.
9. After recovery, confirm manifest status, raw evidence, latest/history run IDs, verification-level counts, and the Amazon validation report/checks.

Do not manually insert ASIN/product rows into S3 to bypass discovery/verification gates.

## Security and External Dependencies

The subsystem uses public Amazon.ca pages through Playwright and does not use a repository-stored Amazon customer credential/API key in the inspected production path. AWS access is separate and uses secret-backed credentials to read Best Buy inputs and write Amazon evidence/data products.

Raw browser evidence can contain considerably more retailer-page/network metadata than normalized tables and must remain under the S3 access boundary. Never publish AWS secret values or any browser/session secrets if future probes introduce them.

Exact live AWS IAM/bucket policy remains outside repository-verifiable scope.

## Known Limitations

- Amazon acquisition depends on retailer browser behavior and can encounter challenge/error pages.
- Search is browser-driven and intentionally paced; broad exhaustive settings can be runtime-expensive.
- Current phone-family and colour rules are finite enumerations, not a universal product ontology.
- `candidate_phone_family_missing` is allowed through the prefilter, so some ambiguity is intentionally deferred to detail evidence.
- Search fallback at score 90 is a deterministic repository rule, not proof of universal equivalence quality.
- Search-verified accepted products have no detail-resolved buy-box or offer data.
- Conditional publication can leave stale stable latest product/offer objects after a healthy run with zero normalized rows in that collection.
- The latest committed validation report has passing structural/semantic checks but failing known-ASIN coverage diagnostics.
- Older zero-result successful manifests in `LATEST_AMAZON_RUN_DIAGNOSTICS.md` reflect historical implementation before the current health gate.
- There is no current official Amazon API integration in the inspected production path.

## Next Safe Development Action

Document the product matching/confidence-scoring engine from `matching/score.py`, `matching/models.py`, `pipeline/product_matching.py`, workflow, tests, and current validation report. Keep acquisition candidate scores and verification levels separate from the downstream final `matched`/`review`/`rejected` product-match states.

## Related Documents

- [Best Buy product and Marketplace-offer extraction](/projects/systems/bb-comp-prices-bestbuy-extraction/)
- [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)
- [bb-comp-prices orchestration/security boundary](/projects/systems/bb-comp-prices-orchestration-security/)
- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main` commit `d24c5bd98a6764bd75476fbf31c6441657305640`; `competitors/amazon_probe.py`; `amazon_details_probe.py`; `amazon_variant.py`; `amazon_normalize.py`; `pipeline/amazon_search_health.py`; `pipeline/amazon_extract.py`; `pipeline/amazon_validation.py`; `scripts/run_amazon_exhaustive.py`; `.github/workflows/amazon_extract.yml`; `docs/LATEST_AMAZON_EXTRACTION_REPORT.md`; `docs/LATEST_AMAZON_RUN_DIAGNOSTICS.md` as explicitly historical diagnostic evidence.
- Verified by: High Director
- Verification scope: search generation/acquisition, health gating, candidate/detail scoring, exact variant rejection, detail recovery, search fallback, offer normalization, conditional S3 publication, workflow/runtime/security boundary, current validation status, and safe recovery.
