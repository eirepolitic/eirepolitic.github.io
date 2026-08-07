---
title: Repository Scan — bb-comp-prices
summary: Documentation-target inventory for the Best Buy marketplace competitor-pricing repository.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 31
permalink: /projects/high-director/repository-scan-bb-comp-prices/
---

# Repository Scan — `bb-comp-prices`

## Repository role

`bb-comp-prices` is a Python 3.12 data platform for discovering Best Buy Canada Marketplace products/offers, acquiring competitor product/offer evidence from Amazon.ca and Walmart.ca, matching equivalent products, validating the results, and persisting historical/current outputs to Amazon S3.

Authoritative repository evidence inspected includes the complete tree plus `docs/BUILD_PLAN.md`, `pyproject.toml`, `config/settings.yaml`, current validation reports, the end-to-end workflow, source package structure, tests, scripts, and probe/report inventory.

## Documentation targets

### 1. `bb-comp-prices` repository

**Categories:** repository, system/application, data platform, deployment/operations.

A repository page should document purpose, package structure, supported runtime, configuration, workflows, testing, S3 dependency, current maturity, and ownership of the subordinate systems below.

### 2. Competitor Pricing Platform Architecture

**Categories:** system architecture, cross-source data flow, orchestration, security/configuration boundary.

Core flow verified from `docs/BUILD_PLAN.md` and implementation structure:

```text
GitHub Actions / CLI
  -> Best Buy discovery/extraction
  -> Amazon/Walmart competitor acquisition
  -> product matching/confidence scoring
  -> validation/manifests
  -> CSV/Parquet on S3
```

This should be the umbrella system page rather than repeating architecture in every component.

### 3. Best Buy Marketplace Category Discovery

**Categories:** discovery pipeline, browser/HTTP extraction, marketplace classification, data product.

Evidence:

```text
src/bb_comp_prices/bestbuy/category_discovery.py
src/bb_comp_prices/bestbuy/category_browser_probe.py
src/bb_comp_prices/pipeline/category_discovery.py
src/bb_comp_prices/pipeline/category_validation.py
.github/workflows/bestbuy_category_discover.yml
.github/workflows/generate_category_discovery_probe.yml
.github/workflows/generate_category_validation.yml
docs/LATEST_CATEGORY_DISCOVERY_REPORT.md
```

Current evidence shows discovery/classification of Best Buy-owned vs Marketplace products and filtering to new-condition Marketplace products.

### 4. Best Buy Product and Marketplace Offer Extraction

**Categories:** extraction pipeline, Best Buy integration, offer normalization, validation, S3 data products.

Evidence:

```text
src/bb_comp_prices/bestbuy/parse_product.py
src/bb_comp_prices/bestbuy/offers_client.py
src/bb_comp_prices/bestbuy/availability_client.py
src/bb_comp_prices/pipeline/bestbuy_extract.py
.github/workflows/bestbuy_extract.yml
.github/workflows/bestbuy_discovered_batch_extract.yml
docs/LATEST_EXTRACTION_REPORT.md
```

Current validated outputs include Best Buy product and Marketplace offer CSV/Parquet datasets under `s3://eirepolitic-data/bb-comp-prices/latest/`.

### 5. Amazon.ca Competitor Acquisition and Recovery System

**Categories:** competitor extraction, Amazon integration, browser/HTTP probing, normalization, recovery/diagnostics, validation.

Evidence:

```text
src/bb_comp_prices/competitors/amazon_probe.py
src/bb_comp_prices/competitors/amazon_details_probe.py
src/bb_comp_prices/competitors/amazon_isolated_probe.py
src/bb_comp_prices/competitors/amazon_normalize.py
src/bb_comp_prices/competitors/amazon_variant.py
src/bb_comp_prices/pipeline/amazon_extract.py
src/bb_comp_prices/pipeline/amazon_search_health.py
src/bb_comp_prices/pipeline/amazon_validation.py
scripts/run_amazon_baseline.py
scripts/run_amazon_exhaustive.py
.github/workflows/amazon_*.yml
.github/workflows/generate_amazon_*.yml
docs/AMAZON_*.md
docs/LATEST_AMAZON_EXTRACTION_REPORT.md
```

This is large enough to merit its own component page with subordinate diagnostics/history sections. The current report shows matched/rejected candidates, detail verification, normalized offers, variant gates, and known-ASIN diagnostics.

### 6. Walmart.ca Competitor Acquisition / Probe System

**Categories:** competitor extraction, Walmart integration, search/detail probing, validation/research evidence.

Evidence:

```text
src/bb_comp_prices/competitors/walmart_probe.py
src/bb_comp_prices/competitors/walmart_details_probe.py
scripts/generate_walmart_search_probe.py
scripts/generate_walmart_details_probe.py
.github/workflows/generate_walmart_search_probe.yml
.github/workflows/generate_walmart_details_probe.yml
docs/WALMART_SEARCH_PROBE.md
docs/WALMART_DETAILS_PROBE.md
```

Document separately from Amazon because source behavior, extraction methods, failure modes, and maturity differ.

### 7. Product Matching and Confidence-Scoring Engine

**Categories:** matching engine, data-quality logic, scoring/model rules, review workflow, data product.

Evidence:

```text
src/bb_comp_prices/matching/models.py
src/bb_comp_prices/matching/score.py
src/bb_comp_prices/pipeline/product_matching.py
scripts/run_product_matching.py
scripts/generate_matching_validation.py
.github/workflows/product_matching.yml
.github/workflows/generate_matching_validation.yml
docs/LATEST_PRODUCT_MATCHING_REPORT.md
```

Full documentation should cover candidate inputs, exact/fuzzy evidence, contradiction handling, thresholds, `matched`/`review`/`rejected` states, validation, and manual-review boundaries.

### 8. End-to-End Pipeline Orchestrator

**Categories:** orchestration, GitHub Actions, CLI/controller, operational runbook.

Evidence:

```text
src/bb_comp_prices/pipeline/orchestrator.py
scripts/run_end_to_end.py
.github/workflows/end_to_end.yml
src/bb_comp_prices/cli.py
```

The current workflow supports selectable stages/competitors, bounded category and Amazon search parameters, matching thresholds, Playwright/Chromium installation, AWS credentials from GitHub Secrets, concurrency control, a 240-minute timeout, and retained summary artifacts.

### 9. S3 Storage, Historical Data Model, and Published Data Products

**Categories:** storage subsystem, AWS/S3 integration, data model, CSV/Parquet products, manifests/history.

Evidence:

```text
src/bb_comp_prices/storage/s3.py
src/bb_comp_prices/storage/writers.py
src/bb_comp_prices/models.py
config/settings.yaml
docs/BUILD_PLAN.md
```

Verified configuration:

```text
region: ca-central-1
bucket: eirepolitic-data
prefix: bb-comp-prices
```

Planned/implemented data-product families include Best Buy products/offers, Amazon/competitor products/offers, product matches, raw evidence, latest exports, manifests, and diagnostics. Exact current-vs-planned S3 layout should be verified when full documentation begins.

### 10. Probe / Diagnostics / Extraction-Research Framework

**Categories:** diagnostic tooling, browser/network research, endpoint/JS-contract probing, evidence reports, failure analysis.

Evidence is extensive under:

```text
src/bb_comp_prices/bestbuy/*probe.py
src/bb_comp_prices/competitors/*probe.py
scripts/generate_*probe.py
.github/workflows/generate_*probe.yml
docs/*PROBE*.md
docs/LIVE_PROBE_EVIDENCE.md
```

This should be grouped into one technical research/diagnostics subsystem rather than documenting every probe script independently. Individual probe pages belong only where a source-specific investigation remains operationally important.

### 11. Validation and Data-Quality Framework

**Categories:** validation subsystem, tests, report generation, data-quality controls.

Evidence:

```text
src/bb_comp_prices/pipeline/*validation.py
scripts/generate_*validation.py
.github/workflows/generate_*validation.yml
tests/unit/
docs/LATEST_*REPORT.md
```

Document validation invariants, fixture/unit-test coverage, row-count/schema/duplicate/price checks, variant gates, and how validation reports relate to deployment/readiness decisions.

### 12. Python Package / CLI / Configuration Layer

**Categories:** code reference, configuration, developer interface, dependencies.

Evidence:

```text
pyproject.toml
src/bb_comp_prices/cli.py
src/bb_comp_prices/config.py
src/bb_comp_prices/http.py
config/
```

Verified package metadata:

```text
name: bb-comp-prices
version: 0.1.0
Python: >=3.12
CLI: bb-comp-prices = bb_comp_prices.cli:main
```

Dependencies include BeautifulSoup, boto3, HTTPX, lxml, pandas, pyarrow, Pydantic, PyYAML, RapidFuzz, Tenacity, with optional Playwright and developer/test tooling.

## Cross-cutting security/configuration targets

These belong in the repository/system security/configuration documentation rather than separate pages unless future evidence warrants it:

- GitHub Actions secrets `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` — names only;
- S3 bucket/prefix permissions;
- direct website access and challenge/CAPTCHA detection policy;
- configurable postal-code/location context;
- user-agent, request timeout, retries, and concurrency/rate controls;
- browser automation boundary;
- prohibition on bypassing access controls, stated in the build plan.

## Historical/planned-vs-current boundary

`docs/BUILD_PLAN.md` contains both architecture and phased plans. It must not be treated as proof that every proposed phase is fully deployed. Current source files, workflows, tests, and latest validation reports are stronger evidence for implemented behavior.

The large set of probe reports/workflows reflects active development/research history. Full documentation should distinguish:

- current production/operational pipeline behavior;
- current validation/probe tooling;
- superseded experiments;
- deferred scale/scheduling decisions.

## Preliminary priority

- **P0:** repository overview; platform architecture; S3/data-product model; end-to-end orchestration/security boundary.
- **P1:** Best Buy discovery/extraction; Amazon competitor acquisition; product matching/validation.
- **P2:** Walmart acquisition; probe/diagnostics framework; package/CLI/config developer reference.
- **P3:** superseded probes and historical development experiments after lineage review.

Final owner-wide priority is deferred until all repositories are scanned.

## Verification record

Verified on 2026-08-07 from the complete repository tree and representative authoritative implementation/configuration/workflow/report files. No secret values were inspected or published.

## Related Documents

- [Repository Documentation Discovery Initiative]({{ '/projects/high-director/repository-documentation-discovery/' | relative_url }})
