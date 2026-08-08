---
title: bb-comp-prices Python package, CLI, configuration, and developer reference
summary: Verified package layout, installation modes, console commands, standalone scripts, configuration/environment overrides, testing, and safe extension guidance for bb-comp-prices.
section: systems
doc_type: reference
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 39
permalink: /projects/systems/bb-comp-prices-developer-reference/
tags:
  - python
  - cli
  - configuration
  - developer
---

# bb-comp-prices Python package, CLI, configuration, and developer reference

## Summary

`bb-comp-prices` is a Python 3.12 package built with Hatchling and installed from `src/bb_comp_prices`. It exposes one console entry point, `bb-comp-prices`, for a limited set of current operations. Several important operational paths—end-to-end orchestration, product matching, discovery-driven batch extraction, validation report generation, and research probes—remain standalone scripts/workflows rather than CLI subcommands.

This distinction is important for maintenance: do not invent or document `bb-comp-prices` subcommands that do not exist in `src/bb_comp_prices/cli.py`.

## Package Metadata

Current `pyproject.toml` defines:

```text
name: bb-comp-prices
version: 0.1.0
requires-python: >=3.12
build backend: hatchling.build
console entry point: bb-comp-prices = bb_comp_prices.cli:main
```

Wheel packages are sourced from `src/bb_comp_prices`.

## Installation

Base editable install:

```bash
python -m pip install --upgrade pip
pip install -e .
```

Developer/test install:

```bash
pip install -e ".[dev]"
```

Browser-dependent install:

```bash
pip install -e ".[browser]"
python -m playwright install --with-deps chromium
```

For local development requiring both extras, install both explicitly, for example:

```bash
pip install -e ".[dev,browser]"
python -m playwright install --with-deps chromium
```

## Runtime Dependencies

Current version-bounded package dependencies are:

| Dependency | Current constraint | Primary role |
| --- | --- | --- |
| `beautifulsoup4` | `>=4.12,<5` | HTML parsing. |
| `boto3` | `>=1.34,<2` | AWS/S3 access. |
| `httpx` | `>=0.27,<1` | Shared synchronous HTTP client. |
| `lxml` | `>=5.2,<7` | HTML parser backend. |
| `pandas` | `>=2.2,<3` | Tabular transformations/CSV/Parquet loading. |
| `pyarrow` | `>=16,<22` | Parquet serialization. |
| `pydantic` | `>=2.8,<3` | Settings and record models. |
| `PyYAML` | `>=6,<7` | YAML configuration/input loading. |
| `rapidfuzz` | `>=3.9,<4` | Candidate/product title similarity. |
| `tenacity` | `>=8.5,<10` | Shared HTTP transport retry decorator. |

Optional extras:

- `browser`: Playwright `>=1.45,<2`;
- `dev`: pytest, pytest-cov, Ruff.

## Package Layout

```text
src/bb_comp_prices/
├── bestbuy/       # Best Buy page/API parsing, discovery, offer clients, probes
├── competitors/   # Amazon and Walmart acquisition/probe logic
├── matching/      # reusable product descriptors, scoring, assessment records
├── pipeline/      # stage pipelines, validation, orchestration, probe evidence
├── storage/       # S3 access plus CSV/Parquet writers
├── cli.py         # supported console subcommands
├── config.py      # Pydantic settings and AWS environment overrides
├── http.py        # shared retrying synchronous HTTP client
└── models.py      # persisted product/offer/run models
```

Prefer adding reusable logic under the appropriate package module. `scripts/` should remain thin operational/report wrappers rather than the only location containing business rules.

## Console Command Surface

Global syntax:

```bash
bb-comp-prices [--config PATH] <command> [command options]
```

`--config` defaults to `config/settings.yaml`.

### `validate-config`

```bash
bb-comp-prices --config config/settings.yaml validate-config
```

Loads settings through `load_settings()` and prints the resulting Pydantic model as formatted JSON. It does not test AWS connectivity or retailer endpoints.

### `s3-smoke`

```bash
bb-comp-prices --config config/settings.yaml s3-smoke
```

Creates a completed `RunManifest` and writes an S3 smoke manifest through `S3Storage.write_smoke_manifest()`. This verifies the package can write using the executing environment's configured AWS access; the dedicated GitHub Actions S3 smoke workflow performs additional AWS CLI identity/bucket checks.

### `bestbuy-probe`

```bash
bb-comp-prices --config config/settings.yaml bestbuy-probe \
  --products config/test_products.yaml
```

Options:

- `--products`, default `config/test_products.yaml`.

Runs `pipeline.bestbuy_probe.run_probe()` and writes a `bestbuy-probe-<run_id>.json` manifest in the generic manifest path.

### `bestbuy-extract`

```bash
bb-comp-prices --config config/settings.yaml bestbuy-extract \
  --products config/test_products.yaml
```

Options:

- `--products`, default `config/test_products.yaml`.

Runs the current Best Buy product/offer extraction pipeline and writes a manifest containing products/offers/errors counts, output URIs, and record-level errors as warnings when the overall pipeline succeeds.

### `bestbuy-category-discover`

```bash
bb-comp-prices --config config/settings.yaml bestbuy-category-discover \
  --categories config/test_categories.yaml \
  --max-products 100 \
  --max-show-more-clicks 10
```

Options:

- `--categories`, default `config/test_categories.yaml`;
- `--max-products`, integer, default `100`;
- `--max-show-more-clicks`, integer, default `10`.

Runs category discovery/classification and writes run counts for discovered, classified, Marketplace, Marketplace-new, Best Buy-owned, and errors.

Browser support/Chromium must be installed in the executing environment for this path.

### `amazon-extract`

```bash
bb-comp-prices --config config/settings.yaml amazon-extract \
  --max-queries-per-product 3 \
  --max-results-per-query 10 \
  --max-candidates-per-product 3 \
  --minimum-search-score 65 \
  --minimum-detail-score 65
```

CLI defaults are:

| Option | Type | Default |
| --- | --- | ---: |
| `--max-queries-per-product` | int | `3` |
| `--max-results-per-query` | int | `10` |
| `--max-candidates-per-product` | int | `3` |
| `--minimum-search-score` | float | `65.0` |
| `--minimum-detail-score` | float | `65.0` |

These CLI defaults differ from the exhaustive Amazon workflow/wrapper documented elsewhere, where zero-valued controls are used to mean unbounded/all in several dimensions. Always inspect the exact entry point being executed rather than assuming workflow and CLI defaults are identical.

Browser support/Chromium is required.

## Commands That Do Not Exist

Current `bb-comp-prices` CLI does **not** expose subcommands for:

- end-to-end orchestration;
- product matching;
- Best Buy discovered-batch extraction;
- Walmart probes;
- validation-report generation;
- browser/network/JavaScript/API research probes;
- Amazon isolated/baseline/recovery report generators.

These are currently invoked through standalone scripts and/or GitHub Actions workflows.

## Standalone Operational Scripts

Current run-oriented wrappers include:

| Script | Purpose |
| --- | --- |
| `scripts/run_end_to_end.py` | Multi-stage controller wrapper with end-to-end manifest. |
| `scripts/run_product_matching.py` | Product-matching wrapper and manifest/output summary. |
| `scripts/run_bestbuy_discovered_batch.py` | Reads current Marketplace discovery and extracts a bounded batch. |
| `scripts/run_amazon_exhaustive.py` | Broad/current Amazon acquisition wrapper used by the production-style Amazon workflow. |
| `scripts/run_amazon_baseline.py` | Older/baseline Amazon execution path retained for research/history. |

Report/probe generators use `scripts/generate_*.py` and should be treated as diagnostics/validation utilities rather than production CLI commands.

## Configuration Model

`src/bb_comp_prices/config.py` defines:

```text
AwsSettings
  region = ca-central-1
  bucket = eirepolitic-data
  prefix = bb-comp-prices

PipelineSettings
  aws
  user_agent = bb-comp-prices/0.1
  request_timeout_seconds = 30.0
  max_retries = 3
  default_postal_code = optional
```

Current `config/settings.yaml` supplies the same AWS defaults plus postal code `V5Y1L3`.

`load_settings(path)`:

1. reads YAML when a path is supplied;
2. validates through `PipelineSettings`;
3. applies only the current AWS environment overrides;
4. returns an immutable-style Pydantic model copy with those AWS values.

## Environment Overrides

Current loader-recognized overrides are:

| Environment variable | Overrides |
| --- | --- |
| `AWS_REGION` | `settings.aws.region` |
| `BB_COMP_S3_BUCKET` | `settings.aws.bucket` |
| `BB_COMP_S3_PREFIX` | `settings.aws.prefix` |

`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are used by boto3/AWS tooling as credential environment variables in GitHub Actions, but they are **not** manually read by `load_settings()`.

`AWS_DEFAULT_REGION` is also set in several workflows for AWS tooling/SDK compatibility, but `load_settings()` explicitly reads `AWS_REGION`, not `AWS_DEFAULT_REGION`.

Current loader does not provide environment overrides for:

- user agent;
- request timeout;
- max retries;
- default postal code.

Do not document unsupported `BB_COMP_*` variables without adding/test-verifying them in source.

## Shared HTTP Client

`src/bb_comp_prices/http.py::HttpClient` wraps `httpx.Client` with:

- configured user agent;
- `Accept-Language: en-CA,en;q=0.9`;
- HTML/JSON accept header;
- configured request timeout;
- redirect following enabled.

`get()` retries only `httpx.TimeoutException` and `httpx.TransportError` with exponential jitter and a **hard-coded three attempts**.

Although `PipelineSettings.max_retries` currently defaults to `3`, that setting is not wired into the decorator. Changing `max_retries` in YAML does not alter this shared client's attempt count in current source.

`get()` returns status/body metadata and does not call `raise_for_status()`. Callers are responsible for deciding whether status codes/content indicate success.

## Input Configuration Files

Current repository configuration includes purpose-specific YAML fixtures/inputs such as:

- `config/settings.yaml` — runtime settings;
- `config/test_products.yaml` — explicit Best Buy products used by CLI/workflows/probes;
- `config/test_categories.yaml` — Best Buy category inputs;
- `config/walmart_test_candidates.yaml` — known Walmart research candidates.

Treat files prefixed/test-oriented as operational fixtures or bounded inputs, not a universal retailer catalogue.

## Development and Test Commands

Repository CI is the safest local developer baseline:

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
ruff check .
pytest --cov=bb_comp_prices --cov-report=term-missing
bb-comp-prices --config config/settings.yaml validate-config
```

For browser paths:

```bash
pip install -e ".[dev,browser]"
python -m playwright install --with-deps chromium
```

The pytest configuration uses `tests/` as the test path and adds `-q`. Ruff targets Python 3.12, line length 100, and enables rule groups `E`, `F`, `I`, `UP`, `B`, and `SIM`.

## Adding or Changing Code Safely

### Add reusable source logic

Place retailer-specific parsing/acquisition under `bestbuy/` or `competitors/`, generic matching under `matching/`, pipeline composition/validation under `pipeline/`, and persistence under `storage/`.

Add focused unit tests before connecting new logic to a live workflow.

### Add a CLI command

When a function genuinely needs a console interface:

1. add the subparser/options in `build_parser()`;
2. add the execution branch in `main()`;
3. decide whether the command requires a `RunManifest` and durable outputs;
4. add argument/config tests where appropriate;
5. update this reference and any workflow invoking it.

Do not add a CLI command solely to mirror every research script.

### Add a persisted data product

Define/verify its typed record contract, historical/latest key behavior, downstream consumers, empty-result semantics, and validation before publishing it. Update the S3/data-product reference in the same implementation programme.

### Change retailer acquisition logic

Use the diagnostics/probe framework to establish the external contract, then move tested reusable logic into source. Preserve health/block detection and do not bypass challenge behavior with uncontrolled retries.

### Change matching logic

Keep candidate acquisition scores separate from final matching states. Add tests for exact/fuzzy evidence, contradictions, threshold boundaries, and Amazon-specific verification-state behavior.

## Manifests and Error Semantics

CLI paths for Best Buy probe/extraction/category and Amazon extraction create `RunManifest` objects and attempt to write them in `finally` blocks. On an exception, the manifest is marked failed before the exception is re-raised.

A failure while writing the final manifest can itself surface at process level, so GitHub logs/raw stage evidence may still be necessary during recovery.

`validate-config` does not write a manifest. `s3-smoke` writes its specialized date-partitioned smoke manifest.

## Security and Credentials

Never put credential values in YAML, product fixtures, scripts, manifests, generated reports, or documentation.

Repository-visible credential/configuration names may include:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
AWS_DEFAULT_REGION
BB_COMP_S3_BUCKET
BB_COMP_S3_PREFIX
```

The first two are secret values supplied by the environment. Exact live IAM permissions are not defined by this package reference and remain unverified from source alone.

## Common Development Failures

### `Configuration file not found`

`load_settings()` raises `FileNotFoundError` when the explicitly supplied path does not exist. Use a repository-relative/absolute path that exists.

### Browser import/runtime failure

Install `.[browser]` and Chromium. Base/development extras alone do not install Playwright unless browser is also requested.

### S3 access failure

Confirm the executing environment has valid AWS credentials, configured bucket/prefix, and required permissions. Do not print credentials while debugging.

### `latest/*.parquet` missing/stale

Amazon, matching, discovery-driven batch, and report generators depend on current stable S3 inputs. Verify upstream run IDs/history rather than fabricating replacement files.

### HTTP status error not automatically raised

The shared `HttpClient` returns non-2xx responses as `FetchResult`. Check the caller's explicit status/content handling before assuming retries or `httpx` exceptions should have occurred.

### Configured `max_retries` appears ignored

This is current implementation behavior for the shared HTTP client: its decorator is fixed at three attempts.

## Known Limitations

- The console CLI covers only a subset of operational workflows.
- CLI Amazon defaults differ from the exhaustive workflow defaults.
- `max_retries` is currently configuration surface without dynamic control of `HttpClient.get()` retry count.
- Settings environment overrides are limited to AWS region/bucket/prefix.
- Browser installation is external to the Python package itself; installing the Playwright library does not install Chromium binaries automatically.
- Several operational/report scripts duplicate orchestration concerns outside the main CLI rather than sharing one command registry.
- Live AWS IAM/bucket state and external retailer contracts cannot be proven by this developer reference alone.

## Next Safe Development Action

Document the superseded `bb-comp-prices` probes/experiments as one archive page. Classify retained Amazon baseline/isolated/recovery and older offer-contract experiments by current authority, and keep still-useful current diagnostics linked to the active diagnostics framework rather than incorrectly archiving them.

## Related Documents

- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)
- [bb-comp-prices orchestration/security boundary](/projects/systems/bb-comp-prices-orchestration-security/)
- [bb-comp-prices diagnostics, probes, and extraction research](/projects/systems/bb-comp-prices-diagnostics-research/)
- [bb-comp-prices validation and data-quality framework](/projects/systems/bb-comp-prices-validation-data-quality/)
- [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `bb-comp-prices` `pyproject.toml`; `src/bb_comp_prices/cli.py`; `config.py`; `http.py`; current package/script/workflow/test inventories; `config/settings.yaml`; current operational source documented by preceding workstream pages.
- Verified by: High Director
- Verification scope: packaging/dependencies, CLI commands/options/defaults, standalone-script boundary, settings/environment overrides, shared HTTP semantics, developer/test commands, extension points, security rules, and known implementation limitations.
