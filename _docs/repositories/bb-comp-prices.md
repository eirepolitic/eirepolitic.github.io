---
title: bb-comp-prices
summary: Python 3.12 competitor-pricing data platform for Best Buy Canada Marketplace discovery/extraction, Amazon.ca acquisition, product matching, validation, diagnostics, and S3 publication.
section: repositories
doc_type: repository
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 30
permalink: /projects/repositories/bb-comp-prices/
tags:
  - python
  - aws
  - s3
  - best-buy
  - amazon
  - walmart
  - data-pipeline
---

# bb-comp-prices

## Summary

`bb-comp-prices` is the source repository for a Python data platform that collects Best Buy Canada Marketplace product and seller-offer evidence, acquires Amazon.ca competitor candidates and offers, assesses product equivalence, validates pipeline outputs, and publishes current and historical CSV/Parquet products to Amazon S3.

The current implementation is not uniform across all retailers. Best Buy extraction, Amazon.ca acquisition, and Amazon-backed product matching have executable package pipelines and GitHub Actions workflows. Walmart.ca currently has source-specific probe/research code and generated evidence, but no equivalent persisted Walmart production pipeline was found on `main`.

## Current Implementation State

The verified default branch is `main` at source commit `d24c5bd98a6764bd75476fbf31c6441657305640`.

Implemented current paths include:

- Best Buy category browser discovery and classification under `src/bb_comp_prices/bestbuy/` and `src/bb_comp_prices/pipeline/category_discovery.py`.
- Best Buy Marketplace PDP/offer extraction under `src/bb_comp_prices/bestbuy/` and `src/bb_comp_prices/pipeline/bestbuy_extract.py`.
- Amazon.ca search, candidate filtering, detail resolution, normalization, search-health checks, and persisted extraction under `src/bb_comp_prices/competitors/amazon_*.py` and `src/bb_comp_prices/pipeline/amazon_*.py`.
- Product matching under `src/bb_comp_prices/matching/` and `src/bb_comp_prices/pipeline/product_matching.py`.
- S3 storage/writer helpers under `src/bb_comp_prices/storage/`.
- CLI/controller paths under `src/bb_comp_prices/cli.py`, `src/bb_comp_prices/pipeline/orchestrator.py`, and `scripts/run_end_to_end.py`.
- Automated unit tests under `tests/unit/` and CI in `.github/workflows/test.yml`.
- Source-specific diagnostics, probes, validation generators, and retained evidence under `scripts/`, `.github/workflows/generate_*.yml`, and `docs/`.

`docs/BUILD_PLAN.md` is architecture/planning evidence, not proof that every described phase is operational. Current executable source, workflow definitions, configuration, and current reports take precedence.

## Source of Truth

- Repository: `bb-comp-prices`.
- Default branch: `main`.
- Package metadata and dependency contract: `pyproject.toml`.
- Runtime configuration: `config/settings.yaml` via `src/bb_comp_prices/config.py`.
- CLI entry point: `bb_comp_prices.cli:main` declared as `bb-comp-prices` in `pyproject.toml`.
- End-to-end controller: `src/bb_comp_prices/pipeline/orchestrator.py` and `scripts/run_end_to_end.py`.
- End-to-end workflow: `.github/workflows/end_to_end.yml`.
- CI workflow: `.github/workflows/test.yml`.
- Core records: `src/bb_comp_prices/models.py` and `src/bb_comp_prices/matching/models.py`.
- S3 access/writers: `src/bb_comp_prices/storage/s3.py`, `src/bb_comp_prices/storage/writers.py`.
- Published architecture/discovery evidence: `_docs/high-director/repository-scan-bb-comp-prices.md` in `eirepolitic.github.io`.

Generated `docs/LATEST_*REPORT.md` and probe reports are validation/observation evidence; they do not override executable source.

## Repository Structure

```text
bb-comp-prices/
├── .github/workflows/        # CI, manual pipeline workflows, validation/probe workflows
├── config/                   # YAML runtime settings and category/test inputs
├── docs/                     # build plan plus generated validation/probe evidence
├── scripts/                  # executable pipeline wrappers and report/probe generators
├── src/bb_comp_prices/
│   ├── bestbuy/              # Best Buy discovery, PDP parsing, offers/availability, probes
│   ├── competitors/          # Amazon and Walmart source-specific acquisition/probe logic
│   ├── matching/             # generic scoring descriptors and assessment logic
│   ├── pipeline/             # executable pipeline stages, validation, orchestration
│   ├── storage/              # S3 key/object and CSV/Parquet writer helpers
│   ├── cli.py                # console interface
│   ├── config.py             # settings models/loader
│   ├── http.py               # retrying HTTP client and response wrapper
│   └── models.py             # persisted product/offer/match record models
├── tests/unit/               # unit coverage for active parsing/acquisition/matching/orchestration logic
├── pyproject.toml            # package/runtime/dependency/tool configuration
└── README.md                 # minimal repository heading only
```

## Inputs and Outputs

### Inputs

Primary inputs are public retailer pages/endpoints, local YAML configuration, GitHub Actions dispatch parameters, and existing S3 data products from earlier stages.

- Best Buy category discovery navigates configured Best Buy Canada category URLs in Chromium via Playwright and collects product links.
- Best Buy extraction receives product IDs/URLs, retrieves PDP HTML, reads Best Buy embedded state, calls the Best Buy offers/seller endpoints, and applies Marketplace/new-condition checks.
- Amazon extraction reads `latest/bestbuy_products.parquet` from S3, generates/searches Amazon.ca candidates, performs candidate and variant gates, resolves detail evidence where possible, and normalizes accepted records.
- Product matching reads current Best Buy and Amazon Parquet products from S3.
- Runtime defaults come from `config/settings.yaml`; GitHub Actions may supply stage-specific numeric controls.

No repository evidence inspected for this page establishes that retailer inputs contain private user data. The configured postal code is operational location context and should not be treated as an authentication credential.

### Outputs

Current executable pipelines publish S3 objects below the configured `bb-comp-prices` prefix. Verified output families include:

- raw Best Buy PDP HTML and offers JSON;
- historical and latest Best Buy product/offer CSV and Parquet datasets;
- raw Amazon search/detail/probe evidence JSON;
- historical and latest Amazon match/product/offer CSV and Parquet datasets;
- historical and latest product-match CSV and Parquet datasets;
- stage-specific error/summary objects where implemented.

Detailed S3 key contracts and lineage belong to the dedicated storage/data-product page.

## Dependencies

The package requires Python `>=3.12` and version-bounded runtime dependencies declared in `pyproject.toml`:

- `beautifulsoup4`, `lxml` for HTML parsing;
- `boto3` for S3 access;
- `httpx` plus `tenacity` for HTTP/retry behavior;
- `pandas`, `pyarrow` for tabular CSV/Parquet processing;
- `pydantic` for typed records/settings;
- `PyYAML` for configuration;
- `rapidfuzz` for fuzzy matching.

Optional `browser` dependencies install Playwright. GitHub Actions workflows that use browser discovery/acquisition install Chromium explicitly. Optional `dev` dependencies are `pytest`, `pytest-cov`, and `ruff`.

External/platform dependencies are GitHub Actions, Best Buy Canada, Amazon.ca, Walmart.ca for probe paths, Amazon S3, and network access from the executing environment.

## Configuration

The primary configuration file is `config/settings.yaml`.

| Name | Location | Purpose | Required | Verified value/example |
| --- | --- | --- | --- | --- |
| `aws.region` | `config/settings.yaml` | AWS client region | Yes | `ca-central-1` |
| `aws.bucket` | `config/settings.yaml` | S3 data bucket | Yes | `eirepolitic-data` |
| `aws.prefix` | `config/settings.yaml` | Platform object prefix | Yes | `bb-comp-prices` |
| `user_agent` | `config/settings.yaml` | HTTP user-agent value | Yes | `bb-comp-prices/0.1` |
| `request_timeout_seconds` | `config/settings.yaml` | HTTP timeout | Yes | `30` |
| `max_retries` | `config/settings.yaml` | HTTP retry limit | Yes | `3` |
| `default_postal_code` | `config/settings.yaml` | Canadian shipping/location context | No/defaulted | `V5Y1L3` |
| `AWS_ACCESS_KEY_ID` | GitHub Actions secret | AWS authentication | Required for S3-writing workflows | name only |
| `AWS_SECRET_ACCESS_KEY` | GitHub Actions secret | AWS authentication | Required for S3-writing workflows | name only |

Exact secret values are outside the repository and must never be published.

## Local Development

The repository's verified CI path provides the supported setup/test sequence:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
ruff check .
pytest --cov=bb_comp_prices --cov-report=term-missing
bb-comp-prices --config config/settings.yaml validate-config
```

Browser-dependent paths additionally require:

```bash
pip install -e ".[browser]"
python -m playwright install --with-deps chromium
```

Running an S3-writing or live retailer stage also requires valid AWS credentials/network access and the expected upstream S3 inputs. Use stage-specific workflows or CLI help rather than guessing parameters.

## Deployment and Release

There is no separately packaged application deployment verified from repository source. Operational execution is job-oriented: GitHub Actions or local CLI/scripts execute pipeline stages and publish data products to S3.

`.github/workflows/test.yml` runs on pushes to `main`, pull requests, and manual dispatch. It installs Python 3.12, lints with Ruff, runs unit tests with coverage, and validates configuration.

Production-capable stage workflows inspected for this page are manually dispatched rather than scheduled. Examples include:

- `.github/workflows/bestbuy_category_discover.yml`;
- `.github/workflows/amazon_extract.yml`;
- `.github/workflows/product_matching.yml`;
- `.github/workflows/end_to_end.yml`.

Browser workflows install the `browser` extra plus Chromium. AWS-writing workflows inject `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` from GitHub Secrets and set `AWS_REGION`/`AWS_DEFAULT_REGION` to `ca-central-1`.

## Validation

Repository CI is authoritative for code-level validation:

```bash
ruff check .
pytest --cov=bb_comp_prices --cov-report=term-missing
bb-comp-prices --config config/settings.yaml validate-config
```

The current test tree covers configuration, Best Buy parsing/discovery/offers, Amazon search/detail/recovery/normalization/variant/health logic, product matching, Walmart probes, and orchestration helper behavior.

The repository also contains generated validation/report workflows for category discovery, Best Buy extraction, Amazon extraction, and matching. Those reports are useful observed evidence but should be read with their generation date and source commit in mind.

## Operations

The platform is operated through focused GitHub Actions workflows or the CLI/scripts. Current evidence does not show a cron/scheduled production workflow on `main`; manual dispatch is the verified trigger for the major live stages inspected here.

The end-to-end controller provides a higher-level stage path, while individual workflows allow isolated reruns and investigation. Generated workflow artifacts and GitHub job summaries retain execution summaries for bounded periods; S3 holds the durable pipeline data/evidence outputs.

Detailed safe rerun and failure procedures belong to the end-to-end orchestration/security runbook page.

## Failure Modes

- **Retailer HTML/API contract change:** parsing or probes fail, produce missing fields, or reject records. Inspect the relevant source-specific probe/report before changing production parsing.
- **Browser/navigation failure:** Playwright workflows can fail on navigation, challenge pages, timeout, or lazy-loading behavior. Inspect workflow summary/artifacts and source-specific probes.
- **AWS authentication/authorization failure:** S3 reads/writes fail. Confirm secret names are configured and check workflow/AWS error messages; do not expose values.
- **Missing upstream data product:** Amazon or matching stages can fail when expected `latest/*.parquet` inputs are absent or incompatible. Verify the prior stage and S3 key contract before rerunning downstream work.
- **Amazon search-health failure:** `run_amazon_extract` persists raw search evidence before raising when search output is unhealthy; use that evidence rather than repeatedly retrying blindly.
- **Product-definition contradiction:** candidate matching intentionally rejects or sends candidates to review; this is a data-quality result, not necessarily a transport failure.

## Security and Access

The repository stores configuration names and non-secret operational settings. AWS credential values are supplied through GitHub Secrets and are not present in inspected source.

Security boundaries verified from repository source include:

- GitHub Actions runner to AWS S3 using secret-backed AWS credentials;
- public retailer HTTP/browser access from the executing environment;
- optional Playwright/Chromium execution for browser-dependent paths;
- S3 bucket/prefix permissions controlling durable data access.

Repository evidence proves configured names and expected interfaces, not the exact current live IAM policy. Live IAM/S3 state must not be inferred from the build plan or workflow alone.

## Known Limitations

- `README.md` currently contains only the repository heading; technical continuity depends on source and external documentation.
- Major live workflows inspected for this page are manual dispatches; no current scheduled production cadence was verified.
- Retailer acquisition depends on external page/API behavior and can be affected by challenges, layout changes, localization, or network conditions.
- Walmart implementation is presently probe/research maturity in the verified tree, not equivalent to the persisted Amazon pipeline.
- Matching is deterministic rules/scoring with explicit variant gates; repository evidence does not justify claims of general product-matching accuracy beyond the tested/validated cases.
- Exact live S3 inventory, IAM policy, object retention/lifecycle, and deployed account state were not inspected for this page.

## Outstanding Work

Documentation work remaining for this platform is tracked in the persistent `bb-comp-prices` documentation workstream plan. The immediate subordinate pages are:

1. S3 storage and data-product model.
2. End-to-end orchestration and security/configuration boundary.
3. Best Buy category discovery and extraction.
4. Amazon.ca acquisition/recovery.
5. Product matching/confidence scoring.
6. Walmart probes, diagnostics/research, validation/data quality, developer reference, and superseded experiments.

## Next Safe Development Action

Document the S3 storage/data-product contract from current executable source before changing any implementation. Verify `src/bb_comp_prices/storage/s3.py`, `src/bb_comp_prices/storage/writers.py`, all current pipeline `storage.key(...)`/direct S3 reads, `src/bb_comp_prices/models.py`, and `config/settings.yaml`; then publish a data/schema page that separates implemented keys from build-plan-only paths.

## Related Documents

- [bb-comp-prices documentation workstream plan](/projects/high-director/bb-comp-prices-documentation-workstream-plan/)
- [Repository scan — bb-comp-prices](/projects/high-director/repository-scan-bb-comp-prices/)
- [Documentation target catalogue](/projects/high-director/documentation-target-catalogue/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main` commit `d24c5bd98a6764bd75476fbf31c6441657305640`; complete repository tree; `pyproject.toml`; `config/settings.yaml`; `README.md`; `.github/workflows/test.yml`, `bestbuy_category_discover.yml`, `amazon_extract.yml`, `product_matching.yml`, `end_to_end.yml`; core package/pipeline/storage/matching files; tests/scripts/workflow inventories; `docs/BUILD_PLAN.md` as lower-precedence planning evidence.
- Verified by: High Director
- Verification scope: repository purpose, current maturity by subsystem, structure, dependencies, configuration, execution model, validation, S3 dependency, security boundary, and limitations. Live AWS/IAM state was not verified.
