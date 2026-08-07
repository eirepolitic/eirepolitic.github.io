---
title: bb-comp-prices Best Buy product and Marketplace-offer extraction
summary: Verified Best Buy Marketplace PDP parsing, all-offer acquisition, seller enrichment, publication, validation, and recovery behavior.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 33
permalink: /projects/systems/bb-comp-prices-bestbuy-extraction/
tags:
  - best-buy
  - marketplace
  - extraction
  - offers
---

# bb-comp-prices Best Buy product and Marketplace-offer extraction

## Summary

The Best Buy extraction subsystem normalizes new-condition Best Buy Canada Marketplace products from PDP embedded state and collects the full Marketplace offer list from Best Buy APIs. It enriches sellers when seller detail/review endpoints succeed, records partial enrichment failures, and publishes product/offer history plus stable latest datasets.

The current production extraction does not rely only on the PDP recommended offer. `parse_recommended_offer()` validates and normalizes the product/recommended-offer context, but `run_bestbuy_extract()` then calls the offers API and publishes the parsed Marketplace offer list returned by `parse_offer_records()`.

## Source of Truth

- pipeline: `src/bb_comp_prices/pipeline/bestbuy_extract.py`;
- PDP parser: `src/bb_comp_prices/bestbuy/parse_product.py::parse_recommended_offer`;
- embedded-state parser: `src/bb_comp_prices/bestbuy/initial_state.py`;
- offers/seller/review client: `src/bb_comp_prices/bestbuy/offers_client.py`;
- product/offer models: `src/bb_comp_prices/models.py`;
- explicit-input workflow: `.github/workflows/bestbuy_extract.yml`;
- discovery-driven workflow: `.github/workflows/bestbuy_discovered_batch_extract.yml` and `src/bb_comp_prices/pipeline/bestbuy_discovered_batch.py`;
- validation: `src/bb_comp_prices/pipeline/extraction_validation.py` and `docs/LATEST_EXTRACTION_REPORT.md`.

## Inputs

`run_bestbuy_extract()` receives a YAML product list with `bestbuy_product_id` and `url`. Two current operational paths supply it:

1. `.github/workflows/bestbuy_extract.yml` uses `config/test_products.yaml` directly.
2. The discovered-batch path reads `latest/bestbuy_marketplace_discovery.parquet`, extracts unique product IDs/PDP URLs, writes a temporary product YAML, and passes that list into extraction. Its workflow exposes `limit`, default `25`, uses concurrency group `bb-comp-prices-bestbuy-discovered-batch`, `cancel-in-progress: false`, and a 90-minute timeout.

The extraction workflow itself is manual (`workflow_dispatch`) and uses Python 3.12 without Playwright; acquisition is through shared HTTP/API clients.

## PDP Validation and Product Normalization

For each input product, the pipeline fetches the PDP, persists the raw HTML, and calls `parse_recommended_offer()`.

The parser requires:

- `window.__INITIAL_STATE__` to parse successfully;
- state path `product.product` to be a dictionary;
- `isMarketplace` to be truthy;
- condition from `grade` or `condition` to normalize exactly to `new` or `brand new`;
- seller ID and seller name;
- non-empty SKU;
- non-null `priceWithoutEhf` for the recommended offer.

If any of these checks fails, the product is not added to the normalized product list.

Normalized `BestBuyProductRecord` fields include SKU/product ID, URLs, title, brand, model number, manufacturer part number, UPCs, category path, description, condition, online-only flag, image URLs, customer rating/count, run/timestamp, and raw evidence URI.

The parser also constructs a PDP recommended-offer record, but `run_bestbuy_extract()` discards that returned offer object (`product, _ = ...`) and uses the offers API output for the published offer collection.

## Offers API and Seller Enrichment

For every successfully parsed product, `BestBuyOffersClient.get_offers()` calls:

```text
https://www.bestbuy.ca/api/offers/v1/products/<product_id>/offers?postalCode=<postal>
```

The response must be HTTP 200 and a JSON list. The raw list is saved with product/postal context.

The pipeline collects every Marketplace `sellerId` in that response and attempts two enrichment calls per unique seller:

```text
/api/seller/v1/sellers/<seller_id>?accept-language=en-CA
/api/reviews/v2/sellers/<seller_id>/review-summary?accept-language=en-CA
```

Seller detail and review failures are non-fatal: each is appended to the run error list and parsing continues with missing enrichment values.

## Offer Normalization

`parse_offer_records()` ignores non-Marketplace API rows and rows missing `sellerId` or `offerId`.

For each accepted Marketplace offer:

- item price is `salePrice` when present, otherwise `regularPrice`;
- `regular_price_cad` is retained separately when present;
- shipping price is only known as `0.0` when seller detail evidence says free shipping is offered; otherwise it is `null` rather than guessed;
- total price is only calculated when shipping price is known;
- seller name precedence is API `sellerNameEn` -> seller `displayName` -> seller `name` -> seller ID;
- `is_recommended_offer` comes from API `isWinner`;
- seller rating/count come from review-summary `averageRating`/`reviewCount` when available;
- offer URL is the canonical product URL or original PDP URL;
- `raw_s3_uri` points to the saved offers payload.

`condition` is copied from the validated product condition. The offers parser itself does not apply a separate per-offer condition field/gate.

If a successfully parsed product yields no normalized Marketplace offers, that product iteration records an error. Because the product was appended before the offers call, a partial run can contain a normalized product whose offer acquisition failed. However, publication proceeds only if the run has at least one product and at least one offer overall.

## Outputs

Raw evidence:

```text
raw/bestbuy/pdp/date=YYYY-MM-DD/run_id=<run_id>/product_id=<id>.html
raw/bestbuy/offers/date=YYYY-MM-DD/run_id=<run_id>/product_id=<id>.json
```

Historical and latest datasets:

```text
curated/bestbuy_products_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
curated/bestbuy_offers_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
latest/bestbuy_products.{csv,parquet}
latest/bestbuy_offers.{csv,parquet}
```

When any errors were collected:

```text
errors/bestbuy/date=YYYY-MM-DD/run_id=<run_id>.json
```

The CLI writes a separate run manifest with row counts, output URIs, and errors converted to warnings when the pipeline itself completes successfully.

## Partial-Success Semantics

Exceptions are caught per input product, so one product failure does not abort the remaining input list. Seller enrichment exceptions are also non-fatal.

After processing all inputs:

```text
if products is empty OR offers is empty -> raise RuntimeError
otherwise                               -> publish all accumulated products/offers
```

Therefore, a successful pipeline return does not mean every requested product completed without errors. Operators must inspect `error_count`, `errors`, and the error object/manifest.

A later successful partial run overwrites `latest/bestbuy_products.*` and `latest/bestbuy_offers.*` with that run's accumulated records. These latest objects are not a merge with the previous latest set.

## Validation

`build_extraction_validation_markdown()` reads CSV and Parquet forms of the latest products/offers and checks:

- product row counts match between formats;
- offer row counts match;
- product ID sets match;
- offer ID sets match;
- all products are Marketplace;
- every published product ID has offers and vice versa;
- exactly one `is_recommended_offer` row per product;
- all item prices are positive;
- product IDs are unique;
- offer IDs are unique.

The current committed `docs/LATEST_EXTRACTION_REPORT.md` records 7 product rows, 22 offer rows, and all implemented checks passing. This is evidence for that observed latest dataset only; it is not a guarantee that future Best Buy responses will satisfy the same shape or coverage.

## Workflow Operation

### Explicit test-product workflow

`.github/workflows/bestbuy_extract.yml`:

- manual dispatch only;
- Python 3.12;
- installs base package;
- executes `bb-comp-prices ... bestbuy-extract --products config/test_products.yaml`;
- uploads `extraction-results.json` for 14 days;
- writes the JSON into the job summary.

### Discovery-driven batch workflow

`.github/workflows/bestbuy_discovered_batch_extract.yml`:

- manual dispatch with `limit`, default 25;
- concurrency group prevents cancel-in-progress replacement;
- timeout 90 minutes;
- reads current filtered discovery Parquet via the batch script;
- runs extraction on the generated bounded list;
- uploads summary artifact for 30 days with `if: always()`.

Neither workflow is scheduled in current source.

## Safe Rerun and Recovery

1. Identify the failed `run_id` and inspect the GitHub workflow error/result.
2. Inspect `errors/bestbuy/date=.../run_id=<run_id>.json` and the CLI/end-to-end manifest when present.
3. For a product parse failure, inspect its raw PDP HTML and initial-state/parser assumptions.
4. For offers failures, inspect the saved offers payload when it exists and distinguish offers-endpoint failure from seller-enrichment failure.
5. A seller detail/review error does not require rerunning a complete extraction unless missing enrichment is operationally important; the normalized offer can still exist.
6. Before rerunning a discovery-driven batch, verify the `latest/bestbuy_marketplace_discovery.parquet` being consumed is the intended discovery result, because an empty newer discovery run may leave an older latest object in place.
7. Prefer the smallest bounded input set needed to confirm recovery before replacing broad `latest/` outputs.
8. After success, confirm product/offer counts, errors, history objects, latest objects, and validation evidence.

Do not manually fabricate S3 normalized rows to bypass parser/API failures.

## Security and External Dependencies

The subsystem calls public Best Buy Canada PDP, offers, seller, and review endpoints. It writes raw responses and normalized data to S3 using GitHub secret-backed AWS credentials. No Best Buy authentication credential is present in the inspected implementation.

Raw responses can contain more retailer metadata than curated products; protect them under the same S3 access boundary. Never add AWS credential values to product YAML, manifests, errors, or documentation.

## Known Limitations

- PDP extraction is coupled to Best Buy `window.__INITIAL_STATE__` and `product.product` fields.
- Only Marketplace products with strictly new/brand-new condition pass PDP normalization.
- Published offers use the offers API, while product condition is inherited from the PDP; no separate offer-condition validation is applied in `parse_offer_records()`.
- Non-free shipping cost is not derived; it remains null, so total price may be null.
- Seller detail/review enrichment is best-effort and can be missing in otherwise successful offers.
- Per-product failures can produce a successful partial run when some other products/offers succeeded.
- `latest/` is replaced by the current run's records rather than merged with previous coverage.
- The current validation report covers one observed latest dataset and does not establish exhaustive Marketplace coverage.
- Retailer endpoint contracts are external and can change without repository changes.

## Next Safe Development Action

Document Amazon.ca acquisition/recovery from current search, prefilter, search-health, detail-recovery, normalization, exhaustive wrapper, workflow, and validation/report evidence. Treat Amazon fallback/search verification states separately from exact detail verification and do not infer quality beyond repository rules and current reports.

## Related Documents

- [Best Buy Marketplace category discovery](/projects/systems/bb-comp-prices-bestbuy-category-discovery/)
- [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)
- [bb-comp-prices orchestration/security boundary](/projects/systems/bb-comp-prices-orchestration-security/)
- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main` commit `d24c5bd98a6764bd75476fbf31c6441657305640`; `pipeline/bestbuy_extract.py`; `bestbuy/parse_product.py`; `bestbuy/offers_client.py`; `bestbuy/initial_state.py`; `pipeline/bestbuy_discovered_batch.py`; `pipeline/extraction_validation.py`; `.github/workflows/bestbuy_extract.yml`; `.github/workflows/bestbuy_discovered_batch_extract.yml`; `docs/LATEST_EXTRACTION_REPORT.md`.
- Verified by: High Director
- Verification scope: PDP gates, product normalization, all-offer API acquisition, seller enrichment, output/publication behavior, partial failures, workflows, validation, security boundary, rerun procedure, and limitations.
