---
title: bb-comp-prices S3 storage and data products
summary: Physical S3 contract for current bb-comp-prices raw evidence, historical datasets, latest datasets, manifests, errors, and CSV/Parquet serialization.
section: data
doc_type: reference
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 30
permalink: /projects/data/bb-comp-prices-data-products/
tags:
  - s3
  - csv
  - parquet
  - data-contract
  - aws
---

# bb-comp-prices S3 storage and data products

## Summary

`bb-comp-prices` stores durable pipeline evidence and published datasets in Amazon S3. The configured physical root is:

```text
s3://eirepolitic-data/bb-comp-prices/
```

This page documents only paths and schemas verified from current executable source on `bb-comp-prices` `main`. Build-plan paths that are not produced or consumed by current code are not presented as implemented.

The main storage families are:

- `raw/` — source evidence and probe payloads;
- `curated/` — date/run-partitioned historical CSV/Parquet datasets;
- `latest/` — overwrite-style current CSV/Parquet datasets used by downstream stages;
- `errors/` — stage-specific JSON error collections;
- `manifests/` — run/smoke metadata written by CLI paths.

## Current Implementation State

The verified storage helper is `src/bb_comp_prices/storage/s3.py`. `S3Storage.key()` prepends the configured `aws.prefix`, strips leading/trailing slashes from path parts, and joins them with `/`. `put_bytes()`, `put_text()`, and `put_json()` write directly with `boto3.client("s3", region_name=settings.region)` and return an `s3://...` URI.

Tabular publication is implemented by `src/bb_comp_prices/storage/writers.py::write_csv_and_parquet()`. Each non-empty Pydantic record collection is written twice from the same logical rows:

- `<base_key>.csv` with UTF-8 CSV content;
- `<base_key>.parquet` using pandas/PyArrow.

For CSV only, list and dictionary values are compact JSON strings. Parquet preserves those values through the pandas/PyArrow representation. Consumers must not assume nested fields have identical physical representation across the two formats.

No repository source inspected for this page defines S3 lifecycle policies, object retention rules, versioning, server-side encryption settings, or deletion automation. Those live-bucket properties remain unverified.

## Source of Truth

- Storage configuration: `config/settings.yaml`.
- Settings model/loader: `src/bb_comp_prices/config.py`.
- S3 key/write implementation: `src/bb_comp_prices/storage/s3.py`.
- CSV/Parquet implementation: `src/bb_comp_prices/storage/writers.py`.
- Canonical persisted record models: `src/bb_comp_prices/models.py` and `src/bb_comp_prices/matching/models.py`.
- Best Buy category producer: `src/bb_comp_prices/pipeline/category_discovery.py`.
- Best Buy extraction producer: `src/bb_comp_prices/pipeline/bestbuy_extract.py`.
- Best Buy probe producer: `src/bb_comp_prices/pipeline/bestbuy_probe.py`.
- Amazon producer/consumer: `src/bb_comp_prices/pipeline/amazon_extract.py`.
- Product-match producer/consumer: `src/bb_comp_prices/pipeline/product_matching.py`.
- Discovered-product consumer: `src/bb_comp_prices/pipeline/bestbuy_discovered_batch.py`.
- Run manifest producer: `src/bb_comp_prices/cli.py`.
- S3 smoke path: `.github/workflows/s3_smoke.yml` and `S3Storage.write_smoke_manifest()`.

When these sources conflict with `docs/BUILD_PLAN.md`, current executable source wins.

## Ownership and Lifecycle

The `bb-comp-prices` pipelines produce these objects. GitHub Actions and local CLI/script execution can write them when valid AWS credentials and S3 permissions are present.

Historical curated products use both a UTC-derived date partition and a pipeline `run_id`:

```text
curated/<dataset>_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
```

Current products use stable `latest/` object names:

```text
latest/<dataset>.{csv,parquet}
```

The writer uses `put_object`, so a later successful write to the same `latest/` key replaces the visible object at that key unless bucket versioning preserves older versions externally. Bucket versioning was not verified from repository source.

No retention/deletion SLA is encoded in the inspected source. Historical partition naming should therefore be understood as an append-oriented naming convention, not proof of an enforced retention policy.

## Data Flow

```text
Best Buy category/browser evidence
  -> raw/bestbuy/category_*
  -> curated/bestbuy_category_products_history
  -> latest/bestbuy_category_products
  -> curated/bestbuy_marketplace_discovery_history
  -> latest/bestbuy_marketplace_discovery
       -> bestbuy_discovered_batch consumer
       -> Best Buy extraction

Best Buy PDP + offers evidence
  -> raw/bestbuy/pdp + raw/bestbuy/offers
  -> curated/bestbuy_products_history + curated/bestbuy_offers_history
  -> latest/bestbuy_products + latest/bestbuy_offers
       -> Amazon extraction reads latest/bestbuy_products.parquet

Amazon search/detail evidence
  -> raw/amazon/.../probe.json
  -> curated/amazon_matches_history
  -> latest/amazon_matches
  -> curated/amazon_products_history + curated/amazon_offers_history
  -> latest/amazon_products + latest/amazon_offers
       -> product matching reads latest/amazon_products.parquet

Product matching
  -> curated/product_matches_history
  -> latest/product_matches
```

Manifests and error JSON are side-channel operational evidence rather than tabular business products.

## Implemented S3 Path Catalogue

All keys below are relative to `s3://eirepolitic-data/bb-comp-prices/`.

| Path pattern | Format | Producer | Meaning/update behavior |
| --- | --- | --- | --- |
| `raw/bestbuy/pdp/date=YYYY-MM-DD/run_id=<run_id>/product_id=<id>.html` | HTML | `bestbuy_probe.py`, `bestbuy_extract.py` | Captured Best Buy PDP response for a product/run. |
| `raw/bestbuy/pdp/date=YYYY-MM-DD/run_id=<run_id>/product_id=<id>.probe.json` | JSON | `bestbuy_probe.py` | Probe analysis linked to the captured PDP. |
| `raw/bestbuy/category_availability/date=YYYY-MM-DD/run_id=<run_id>/category_id=<id>.json` | JSON | `category_discovery.py` | Availability/seller evidence for discovered category products. |
| `raw/bestbuy/category_classification/date=YYYY-MM-DD/run_id=<run_id>/product_id=<id>.html` | HTML | `category_discovery.py` | PDP evidence fetched when Marketplace condition cannot be classified from listing title alone. |
| `raw/bestbuy/offers/date=YYYY-MM-DD/run_id=<run_id>/product_id=<id>.json` | JSON | `bestbuy_extract.py` | Offers endpoint payload plus product/postal context. |
| `raw/amazon/date=YYYY-MM-DD/run_id=<run_id>/probe.json` | JSON | `amazon_extract.py` | Search-health, search reports, prefilter rejections, and detail reports. Written even before an unhealthy-search exception is raised. |
| `curated/bestbuy_category_products_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `category_discovery.py` | All discovered category records, including classification failures. |
| `latest/bestbuy_category_products.*` | CSV + Parquet | `category_discovery.py` | Latest all-category classification output. |
| `curated/bestbuy_marketplace_discovery_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `category_discovery.py` | Filtered classified Marketplace + new-condition products. |
| `latest/bestbuy_marketplace_discovery.*` | CSV + Parquet | `category_discovery.py` | Current filtered discovery input used by batch extraction. |
| `curated/bestbuy_products_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `bestbuy_extract.py` | Historical normalized Best Buy products. |
| `latest/bestbuy_products.*` | CSV + Parquet | `bestbuy_extract.py` | Current Best Buy products; Parquet is an Amazon and matching input. |
| `curated/bestbuy_offers_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `bestbuy_extract.py` | Historical normalized Best Buy Marketplace offers. |
| `latest/bestbuy_offers.*` | CSV + Parquet | `bestbuy_extract.py` | Current Best Buy offers. |
| `curated/amazon_matches_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `amazon_extract.py` | Search/detail candidate assessment records, including rejected candidates. |
| `latest/amazon_matches.*` | CSV + Parquet | `amazon_extract.py` | Current Amazon candidate assessment output. |
| `curated/amazon_products_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `amazon_extract.py` | Historical normalized Amazon products. |
| `latest/amazon_products.*` | CSV + Parquet | `amazon_extract.py` | Current normalized Amazon products; Parquet is the product-matching candidate input. |
| `curated/amazon_offers_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `amazon_extract.py` | Historical normalized Amazon offers. |
| `latest/amazon_offers.*` | CSV + Parquet | `amazon_extract.py` | Current normalized Amazon offers. |
| `curated/product_matches_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.*` | CSV + Parquet | `product_matching.py` | Historical cross-source product assessments. |
| `latest/product_matches.*` | CSV + Parquet | `product_matching.py` | Current matched/review/rejected cross-source assessments. |
| `errors/bestbuy/date=YYYY-MM-DD/run_id=<run_id>.json` | JSON | `bestbuy_extract.py` | Non-fatal/record-level Best Buy extraction errors when any occurred. |
| `errors/bestbuy_category_discovery/date=YYYY-MM-DD/run_id=<run_id>.json` | JSON | `category_discovery.py` | Category classification errors when any occurred. |
| `manifests/<pipeline>-<run_id>.json` | JSON | `cli.py::_write_manifest` | CLI run status, inputs, counts, warnings/errors and output URIs. |
| `manifests/date=YYYY-MM-DD/smoke-YYYYMMDDTHHMMSSZ.json` | JSON | `S3Storage.write_smoke_manifest` | Successful S3 smoke-test manifest. |

`.*` above means both `.csv` and `.parquet` are written from the same record collection.

## Published Schemas

### Best Buy category product

Canonical model: `src/bb_comp_prices/models.py::BestBuyCategoryProductRecord`.

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `run_id` | string | Yes | Pipeline run identifier. |
| `observed_at_utc` | datetime | Yes | Observation timestamp in UTC. |
| `category_id` | string | Yes | Configured category identifier. |
| `category_url` | string | Yes | Source category URL. |
| `source_position` | integer | Yes | Discovery order within the source collection. |
| `bestbuy_product_id` | string | Yes | Best Buy product identifier. |
| `pdp_url` | string | Yes | Product detail URL. |
| `title` | string/null | No | Listing/PDP title when available. |
| `condition` | string/null | No | Observed/inferred condition. |
| `is_marketplace` | boolean/null | No | Marketplace ownership classification. |
| `is_new_condition` | boolean/null | No | Whether the condition is accepted as new. |
| `classification_status` | `classified`/`failed` | Yes | Classification result. |
| `classification_error` | string/null | No | Failure text for failed records. |
| `raw_s3_uri` | string/null | No | Raw classification evidence URI when a PDP was fetched. |

`latest/bestbuy_marketplace_discovery.*` uses this same schema but contains only records that are `classified`, `is_marketplace == true`, and `is_new_condition == true`.

### Best Buy product

Canonical model: `BestBuyProductRecord`.

Key fields are `run_id`, `observed_at_utc`, `bestbuy_product_id`, `web_code`, `pdp_url`, `canonical_url`, `title`, `brand`, `model_number`, `manufacturer_part_number`, `upcs`, `category_path`, `description`, `condition`, `is_marketplace`, `is_online_only`, `image_urls`, `customer_rating`, `customer_rating_count`, and `raw_s3_uri`.

`upcs`, `category_path`, and `image_urls` are list fields. In CSV they are JSON text; in Parquet they retain nested/list representation through the writer.

### Best Buy offer

Canonical model: `BestBuyOfferRecord`.

Each row identifies one Marketplace offer using `bestbuy_product_id` plus `offer_id`, with seller identity, condition, item/regular/shipping/total CAD prices, availability/purchasability, recommended/free-shipping flags, seller rating/review count, URLs, timestamps/run ID, and raw evidence URI.

### Amazon candidate match

Canonical model: `AmazonMatchRecord`.

Each row is a Best Buy-to-ASIN candidate assessment with search/detail scores and verification state. `match_status` is limited to `matched` or `rejected` at this acquisition stage; the later cross-source product-matching product has a separate three-state contract.

Fields: `run_id`, `observed_at_utc`, `bestbuy_product_id`, `asin`, `amazon_url`, `amazon_title`, `candidate_score`, `detail_score`, `search_method`, `search_query`, `verification_level` (`detail` or `search`), `detail_resolved`, `match_status`, `rejection_reason`.

### Amazon product

Canonical model: `AmazonProductRecord`.

Fields: `run_id`, `observed_at_utc`, `bestbuy_product_id`, `asin`, `product_url`, `title`, `verification_level`, `detail_resolved`, `availability`, `search_price_cad`, `buy_box_price_cad`, `buy_box_seller`, `buy_box_ships_from`, `match_score`, `raw_s3_uri`.

### Amazon offer

Canonical model: `AmazonOfferRecord`.

Each row is an ASIN offer with `bestbuy_product_id`, `asin`, `offer_id`, position, condition, item price CAD, seller, ship origin, Amazon-retail/FBA flags, URL, run/timestamp, and raw evidence URI.

### Product match

Canonical model: `src/bb_comp_prices/matching/models.py::ProductMatchRecord`.

| Field | Type | Required | Contract |
| --- | --- | --- | --- |
| `run_id` | string | Yes | Matching run identifier. |
| `observed_at_utc` | datetime | Yes | UTC assessment timestamp. |
| `bestbuy_product_id` | string | Yes | Source product identifier. |
| `competitor_source` | `amazon`/`walmart` | Yes | Model permits both sources; current pipeline populates Amazon. |
| `competitor_product_id` | string | Yes | Competitor identifier; ASIN for current Amazon pipeline. |
| `competitor_url` | string/null | No | Candidate URL. |
| `match_status` | `matched`/`review`/`rejected` | Yes | Final assessment state. |
| `match_method` | string | Yes | Rule/gate used for the assessment. |
| `match_score` | float | Yes | Assessment score. |
| `identifier_evidence` | object | Yes | UPC/model evidence. |
| `attribute_evidence` | object | Yes | Brand/title/variant and other attribute evidence. |
| `contradictions` | list[string] | Yes | Product-defining conflicts. |
| `review_reason` | string | Yes | Human-readable disposition reason. |

In CSV the evidence objects and contradiction list are JSON strings.

### Run manifest

Canonical model: `RunManifest` in `src/bb_comp_prices/models.py`.

Fields are `run_id`, `pipeline`, `status` (`started`, `succeeded`, `failed`), `started_at_utc`, `completed_at_utc`, optional `git_sha`, `inputs`, `row_counts`, `warnings`, `errors`, and `outputs`.

The current CLI writes these manifests for `bestbuy-probe`, `bestbuy-extract`, `bestbuy-category-discover`, and `amazon-extract`. The `s3-smoke` command uses the same logical model but writes it under the date-partitioned smoke key.

## Keys and Relationships

- `run_id` links records, raw evidence, historical partitions, errors, and manifests produced by the same CLI run when that path is used.
- `bestbuy_product_id` is the primary cross-stage Best Buy product identifier.
- `AmazonProductRecord.bestbuy_product_id` and `AmazonMatchRecord.bestbuy_product_id` retain the Best Buy source association used during acquisition.
- `asin` identifies the Amazon candidate/product/offer.
- `BestBuyOfferRecord.offer_id` is generated as `<bestbuy_product_id>:<seller_id>` for the recommended/PDP path and follows the normalized offer implementation for other Marketplace offers.
- `ProductMatchRecord` relates one Best Buy product to one competitor product assessment.
- Historical data is partitioned by observation date and run ID, but no uniqueness enforcement exists at S3 object-store level.
- `latest/` is a publication pointer by stable object name, not a relational view. Consumers read specific object keys directly.

## Business and Transformation Rules

- All observation timestamps used by the inspected producers are created with `datetime.now(UTC)`.
- Historical date partitions are derived from that UTC timestamp.
- Best Buy Marketplace discovery latest/history filtered products require successful classification plus Marketplace ownership and new condition.
- `bestbuy_discovered_batch.py` reads `latest/bestbuy_marketplace_discovery.parquet`, requires `bestbuy_product_id` and `pdp_url`, deduplicates by product ID, and optionally limits rows.
- Amazon extraction reads `latest/bestbuy_products.parquet`; it does not consume the CSV form.
- Product matching reads `latest/bestbuy_products.parquet` and `latest/amazon_products.parquet`.
- `write_csv_and_parquet()` refuses an empty record collection. Some producers therefore conditionally skip a dataset family when there are no records rather than writing an empty file.
- Best Buy extraction raises if no normalized products or no offers were produced, preventing publication of empty core datasets.
- Amazon extraction writes raw search evidence before failing the search-health gate, preserving diagnostics for recovery.

## Data Quality and Validation

Schema construction is enforced through Pydantic models before tabular writes. Additional stage-specific validation exists under `src/bb_comp_prices/pipeline/*validation.py`, `tests/unit/`, `scripts/generate_*validation.py`, and `.github/workflows/generate_*validation.yml`; those checks are documented in the dedicated validation framework page.

Storage-specific safeguards verified here include:

- empty tabular record collections raise in `write_csv_and_parquet()`;
- required upstream columns are checked by `bestbuy_discovered_batch.py`;
- direct downstream Parquet reads fail if expected keys/columns are absent or incompatible;
- the S3 smoke workflow checks credential presence, calls `aws sts get-caller-identity`, checks bucket accessibility with `head-bucket`, then writes a smoke manifest.

## Configuration

| Setting | Source | Verified value | Use |
| --- | --- | --- | --- |
| `aws.region` | `config/settings.yaml` | `ca-central-1` | Boto3 client region. |
| `aws.bucket` | `config/settings.yaml` | `eirepolitic-data` | Object bucket. |
| `aws.prefix` | `config/settings.yaml` | `bb-comp-prices` | Root key prefix prepended by `S3Storage.key()`. |
| `AWS_ACCESS_KEY_ID` | GitHub Actions secret | value not documented | AWS authentication. |
| `AWS_SECRET_ACCESS_KEY` | GitHub Actions secret | value not documented | AWS authentication. |

## Security and Access

Repository source establishes the configured bucket/prefix and the GitHub Actions secret names, but not the exact live IAM permissions or bucket policy.

The current GitHub Actions S3-writing boundary uses `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` from GitHub Secrets. The S3 smoke workflow validates identity and bucket accessibility before writing its manifest.

Raw retailer HTML/JSON may contain source-site data beyond the normalized fields. Treat raw objects as evidence requiring the same storage access discipline as curated data. No secret values should be written into manifests, errors, raw evidence wrappers, or documentation.

Exact bucket encryption, versioning, lifecycle, public-access-block, and IAM state remain unverified and should only be documented after sanitized authoritative AWS evidence is obtained if operationally necessary.

## Failure Modes

- **Missing upstream latest object:** downstream `get_object` fails. Re-run/verify the producer stage rather than creating placeholder files.
- **Schema drift:** pandas/Pydantic/consumer required-column errors can surface when producer fields change. Change producer and consumers together and preserve compatibility where required.
- **Partial source success:** Best Buy category/extraction can emit errors while still publishing successful records. Inspect the corresponding `errors/` object and run manifest before treating a run as complete coverage.
- **Unhealthy Amazon search:** raw `probe.json` is intentionally persisted before the pipeline raises. Use it for diagnosis.
- **Empty result set:** the generic CSV/Parquet writer raises on empty records; conditional producers may simply omit optional products such as Amazon offers/products when none qualify.
- **Latest overwrite:** a successful later publication replaces the stable `latest/` key. Recovering a prior latest version depends on historical curated objects or live bucket versioning; versioning itself is unverified.
- **AWS permission/credential failure:** S3 calls fail before/while reading or writing. Use workflow errors and the S3 smoke test; do not log credential values.

## Known Limitations

- Live S3 object inventory was not inspected, so this page documents executable key contracts rather than asserting every possible object currently exists.
- No repository-enforced retention, lifecycle, versioning, encryption, replication, or deletion policy was found.
- Historical filenames use a fixed `part-00000`; there is no current multi-part/sharded writer abstraction in `write_csv_and_parquet()`.
- `latest/` publication is direct object replacement with no repository-level transaction across the paired CSV/Parquet objects or across multiple dataset families.
- CSV nested values are JSON strings while Parquet retains nested values, so format-switching consumers must parse accordingly.
- `ProductMatchRecord.competitor_source` permits `walmart`, but the current persisted product-matching pipeline inspected for this page reads Amazon products only. The model allowance is not proof of an active Walmart publication flow.

## Outstanding Work

- Document stage-specific data-quality rules and latest validation reports under the validation framework target.
- Document exact orchestration/retry boundaries around these producers and consumers.
- If future operations require exact bucket-policy/lifecycle/versioning guarantees, verify live AWS state using sanitized authoritative evidence before adding those guarantees here.
- Keep this catalogue synchronized when a producer introduces a new persisted path or changes a schema/key contract.

## Next Safe Development Action

Document the end-to-end orchestration/security boundary from current `src/bb_comp_prices/pipeline/orchestrator.py`, `scripts/run_end_to_end.py`, `src/bb_comp_prices/cli.py`, `src/bb_comp_prices/config.py`, `.github/workflows/end_to_end.yml`, and the individual stage workflows. Preserve the S3 dependencies documented here and do not change storage architecture as part of that documentation step.

## Related Documents

- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)
- [bb-comp-prices documentation workstream plan](/projects/high-director/bb-comp-prices-documentation-workstream-plan/)
- [Repository scan — bb-comp-prices](/projects/high-director/repository-scan-bb-comp-prices/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main` commit `d24c5bd98a6764bd75476fbf31c6441657305640`; `config/settings.yaml`; `src/bb_comp_prices/storage/s3.py`; `storage/writers.py`; `models.py`; `matching/models.py`; `pipeline/category_discovery.py`; `pipeline/bestbuy_extract.py`; `pipeline/bestbuy_probe.py`; `pipeline/bestbuy_discovered_batch.py`; `pipeline/amazon_extract.py`; `pipeline/product_matching.py`; `cli.py`; `.github/workflows/s3_smoke.yml`.
- Verified by: High Director
- Verification scope: configured bucket/prefix/region, implemented object-key patterns, physical formats, current record schemas, run linkage, current downstream reads, overwrite/history behavior implied by source, smoke-test access checks, and unverified live-cloud properties.
