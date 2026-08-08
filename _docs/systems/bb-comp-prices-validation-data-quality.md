---
title: bb-comp-prices validation and data-quality framework
summary: Current CI, runtime publication guards, search-health gates, dataset validation generators, reports, and known validation gaps across the competitor-pricing platform.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 38
permalink: /projects/systems/bb-comp-prices-validation-data-quality/
tags:
  - validation
  - data-quality
  - pytest
  - reports
---

# bb-comp-prices validation and data-quality framework

## Summary

`bb-comp-prices` uses several different validation layers. They must not be conflated:

1. repository CI validates source/configuration before code changes merge;
2. typed models and producer guards validate records/runtime conditions while a pipeline runs;
3. hard publication/health gates prevent known-bad situations from replacing current data in specific stages;
4. generated `LATEST_*REPORT.md` files inspect already-published S3 datasets and commit human-readable validation evidence to the repository.

Most generated validation reports are **post-publication diagnostics**, not transaction gates. A report workflow failing or detecting a bad check does not automatically roll back an S3 publication.

## Source of Truth

- CI: `.github/workflows/test.yml`;
- configuration validation: `src/bb_comp_prices/config.py`, CLI `validate-config`;
- typed records: `src/bb_comp_prices/models.py`, `src/bb_comp_prices/matching/models.py`;
- category validation: `src/bb_comp_prices/pipeline/category_validation.py`;
- Best Buy extraction validation: `src/bb_comp_prices/pipeline/extraction_validation.py`;
- Amazon validation: `src/bb_comp_prices/pipeline/amazon_validation.py`;
- Amazon hard health gate: `src/bb_comp_prices/pipeline/amazon_search_health.py` and `amazon_extract.py`;
- matching validation generator: `scripts/generate_matching_validation.py`;
- report generators: `scripts/generate_category_validation.py`, `generate_extraction_validation.py`, `generate_amazon_validation.py`, `generate_matching_validation.py`;
- workflows: `.github/workflows/generate_category_validation.yml`, `generate_extraction_validation.yml`, `generate_amazon_validation.yml`, `generate_matching_validation.yml`;
- current reports: `docs/LATEST_CATEGORY_DISCOVERY_REPORT.md`, `LATEST_EXTRACTION_REPORT.md`, `LATEST_AMAZON_EXTRACTION_REPORT.md`, `LATEST_PRODUCT_MATCHING_REPORT.md`.

## Validation Layers

### Source/CI validation

`.github/workflows/test.yml` runs on pushes to `main`, pull requests, and manual dispatch. Under Python 3.12 it runs:

```bash
ruff check .
pytest --cov=bb_comp_prices --cov-report=term-missing
bb-comp-prices --config config/settings.yaml validate-config
```

This is the primary automated regression gate for executable source. The current unit tree covers configuration, Best Buy parsing/discovery/offers, Amazon acquisition/search-health/recovery/normalization/variant logic, matching, Walmart probes, and orchestration helpers.

CI does not prove live retailer reachability or current S3 dataset quality because unit tests are not the same as live workflow execution.

### Typed-record validation

Current published records are constructed through Pydantic models before generic tabular publication. This protects required fields/enums/types at object-construction time, but it is not a substitute for semantic cross-row validation.

Examples include:

- `BestBuyProductRecord`/`BestBuyOfferRecord`;
- `BestBuyCategoryProductRecord`;
- `AmazonMatchRecord`, `AmazonProductRecord`, `AmazonOfferRecord`;
- `ProductMatchRecord`;
- `RunManifest`.

### Producer/runtime guards

Individual producers enforce additional conditions before/around publication.

Examples:

- generic CSV/Parquet writer refuses an empty record list;
- Best Buy extraction raises if the overall run produced no normalized products or no offers;
- category discovery retains failed classifications explicitly and only publishes the filtered Marketplace-new subset when at least one row qualifies;
- discovered-batch loader requires `bestbuy_product_id` and `pdp_url` columns;
- Amazon and matching require compatible upstream S3 Parquet inputs.

Conditional writes create an important operational caveat: when a collection is empty and its writer is skipped, an older stable `latest/` object can remain. Validation and consumers must inspect run IDs/timestamps rather than using object existence as freshness proof.

## Hard Publication Gate: Amazon Search Health

Amazon has the clearest current live acquisition health gate.

`summarize_amazon_search_health()` requires:

- at least one search result overall;
- all searched pages to be healthy;
- every source Best Buy product to have received searches.

When unhealthy, `run_amazon_extract()` first persists raw search evidence then raises `AmazonSearchUnavailableError` **before** publishing new Amazon latest datasets.

This is a production guard, unlike a generated Markdown validation report.

A historical Amazon diagnostics report contains zero-result runs recorded as successful before the current gate existed. Those historical manifests are not proof of current success semantics.

## Category Discovery Validation

`pipeline/category_validation.py` compares current full-category and filtered Marketplace datasets in both CSV and Parquet.

Implemented checks include:

- CSV/Parquet row-count equality for full output;
- CSV/Parquet row-count equality for filtered Marketplace output;
- product ID set equality between formats;
- unique discovered product IDs;
- filtered IDs are a subset of full IDs;
- all filtered rows are Marketplace;
- all filtered rows are new condition;
- ownership-classification counts balance across classified rows.

Current committed `docs/LATEST_CATEGORY_DISCOVERY_REPORT.md` records 57 classified rows, 27 Marketplace across conditions, 3 Marketplace-new rows, zero failed classifications, and all implemented checks passing for that observed dataset.

These checks verify internal consistency/classification invariants, not exhaustive Best Buy catalogue coverage.

## Best Buy Extraction Validation

`pipeline/extraction_validation.py` compares `latest/bestbuy_products.*` and `latest/bestbuy_offers.*`.

Implemented checks include:

- product CSV/Parquet row-count equality;
- offer CSV/Parquet row-count equality;
- product ID set equality;
- offer ID set equality;
- all products are Marketplace;
- every published product has offers and every offer references a published product;
- exactly one recommended offer per product;
- positive item prices;
- unique product IDs;
- unique offer IDs.

Current committed `docs/LATEST_EXTRACTION_REPORT.md` records 7 products and 22 offers with all implemented checks passing for that observed latest publication.

A producer can still complete with record-level errors when enough other products/offers succeeded; the error object/manifest must be reviewed in addition to the validation report.

## Amazon Validation

`pipeline/amazon_validation.py` validates current Amazon match/product/offer data across CSV and Parquet plus semantic relationships to current Best Buy products.

Implemented checks documented from current source include:

- cross-format consistency;
- matched Best Buy IDs have normalized Amazon product rows;
- offer ASINs belong to matched candidates;
- search-verified candidates have no offers;
- search-verified products have no buy-box seller and remain `detail_resolved=false`;
- detail-verified products are resolved;
- all normalized offers are new condition;
- offer prices are positive;
- offer IDs are unique;
- matched candidates still pass the current exact Amazon variant gate when re-evaluated.

The current committed `docs/LATEST_AMAZON_EXTRACTION_REPORT.md` shows the structural/semantic checks passing for 9 candidate rows, 2 matched products, and 13 offers.

However, its separate known-ASIN coverage diagnostic is **not fully passing**: two expected ASINs are absent. The report therefore supports quality of produced rows under implemented invariants, but not exhaustive known-candidate recovery.

## Product Matching Validation

There is no `pipeline/matching_validation.py` module in current source. Product-match report validation is implemented directly in `scripts/generate_matching_validation.py`.

It reads `latest/product_matches.csv` and `.parquet` and checks:

- CSV/Parquet row counts match;
- `(bestbuy_product_id, competitor_source, competitor_product_id)` pairs are unique;
- scores are within `0..100`;
- rows whose status is `matched` have no contradiction values.

It then writes `docs/LATEST_PRODUCT_MATCHING_REPORT.md`.

The committed report is currently **stale relative to executable matching logic**. It contains generic `attribute_score` dispositions from an older current-data state, while the present `_assess_amazon_product()` and unit tests apply authoritative Amazon exact-variant and verification-level overrides.

Therefore:

- the generator's four structural checks remain valid as code;
- the committed report should not be cited as current proof of Amazon match/review/reject behavior until regenerated from outputs produced by the current matching implementation.

## Generated Validation Workflow Pattern

Each `generate_*validation.yml` workflow is a manually dispatched report generator. It installs the package, uses AWS credentials to read stable current S3 datasets, runs its generator, and commits the resulting Markdown report into `bb-comp-prices` source when changed.

These workflows are observational/reporting jobs. They do not run automatically as a mandatory downstream gate after each production extraction/matching workflow in the current repository architecture.

Therefore a fresh production `latest/` object can exist before its matching Markdown validation report has been regenerated.

## Interpreting `LATEST_*` Correctly

Before citing a `LATEST_*REPORT.md` as current evidence, verify all of the following:

1. the report generation logic still matches current production schemas/rules;
2. the underlying S3 `latest/` dataset was produced by the intended current implementation;
3. the report has been regenerated after that publication;
4. any diagnostic checks outside the aggregate `all checks passed` field are also read and reported;
5. run IDs/timestamps or current source state do not reveal stale stable-object behavior.

Filename alone is insufficient evidence of freshness.

## Failure and Recovery

### CI failure

Do not merge executable-source changes until Ruff/tests/config validation pass. Fix the code/test/config defect rather than weakening checks merely to clear CI.

### Runtime producer guard failure

Inspect the run manifest/raw evidence/errors and the producer-specific page. Determine whether partial S3 history/latest writes occurred before rerunning.

### Amazon health-gate failure

Use the preserved raw Amazon probe evidence. Do not repeatedly rerun blocked/unhealthy search or manually publish normalized Amazon rows around the gate.

### Generated report check fails

A failed check means the current S3 publication needs investigation; it does not automatically mean the report generator is wrong. Compare CSV/Parquet datasets, source implementation, run IDs, and known stale-object behavior.

### Report is stale

Regenerate only after confirming current upstream datasets are the intended ones. A regenerated report against an older stable `latest/` object can still be technically fresh but semantically misleading.

## Security Boundary

Validation workflows read S3 using secret-backed AWS credentials. Credential values must never be included in reports or diagnostics.

Reports may publish product IDs, ASINs, retailer URLs, match evidence/reasons, counts, and S3 object URIs. They should not be extended to dump raw session/authentication data.

Validation does not establish live IAM/bucket policy correctness; it operates within whatever permissions the executing credential currently has.

## Known Limitations

- Validation is distributed across CI, Pydantic models, producer guards, health gates, and separate report generators rather than one unified framework/API.
- Most `LATEST_*` reports are manual post-publication checks, not mandatory transaction gates.
- Conditional latest publication can leave stale stable objects that a validation generator may read later.
- Category/Best Buy checks emphasize internal consistency, not complete retailer-catalogue coverage.
- Amazon's current report has a known-ASIN coverage failure despite passing structural/semantic invariants.
- The committed product-matching report is stale relative to current authoritative Amazon matching logic.
- There is no equivalent production Walmart data-quality validation because no production Walmart dataset exists.
- No repository mechanism currently binds each generated report to an immutable upstream S3 object version/checksum.

## Next Safe Development Action

Document the Python package, CLI, configuration, developer workflow, and executable/script reference. Include exact console commands/options, environment overrides, optional browser dependencies, CI commands, module boundaries, and safe extension points without changing architecture.

## Related Documents

- [bb-comp-prices diagnostics, probes, and extraction research](/projects/systems/bb-comp-prices-diagnostics-research/)
- [bb-comp-prices product matching and confidence scoring](/projects/systems/bb-comp-prices-product-matching/)
- [Amazon.ca competitor acquisition and recovery](/projects/systems/bb-comp-prices-amazon-acquisition/)
- [Best Buy product and Marketplace-offer extraction](/projects/systems/bb-comp-prices-bestbuy-extraction/)
- [Best Buy Marketplace category discovery](/projects/systems/bb-comp-prices-bestbuy-category-discovery/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `bb-comp-prices` CI/test tree; `category_validation.py`; `extraction_validation.py`; `amazon_validation.py`; `amazon_search_health.py`; `scripts/generate_matching_validation.py`; validation generators/workflows; current committed `LATEST_*REPORT.md` files; current producer/persistence behavior documented earlier in this workstream.
- Verified by: High Director
- Verification scope: CI, typed/runtime validation, hard publication gates, post-publication checks, current report status, recovery semantics, and known validation gaps.
