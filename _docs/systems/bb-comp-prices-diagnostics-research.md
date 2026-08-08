---
title: bb-comp-prices diagnostics, probes, and extraction research
summary: Cross-retailer framework for live probes, browser/network research, JavaScript/API contract discovery, generated evidence, and safe promotion into production extraction logic.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 37
permalink: /projects/systems/bb-comp-prices-diagnostics-research/
tags:
  - diagnostics
  - probes
  - research
  - playwright
---

# bb-comp-prices diagnostics, probes, and extraction research

## Summary

`bb-comp-prices` contains a deliberate research layer used to understand retailer page/API contracts before production extraction logic is changed. It combines reusable probe functions under `src/bb_comp_prices/`, report generators under `scripts/`, manually dispatched GitHub Actions workflows, S3 raw evidence, and committed Markdown reports under `docs/`.

These probes are evidence-gathering utilities. A successful or failed probe report does not by itself establish a production contract. Production behavior is documented from current pipeline source/workflows and only uses probe findings once they have been promoted into tested executable logic.

## Source of Truth

Primary probe families are visible in:

- `src/bb_comp_prices/bestbuy/*probe.py`;
- `src/bb_comp_prices/competitors/amazon_*probe.py`;
- `src/bb_comp_prices/competitors/walmart_*probe.py`;
- `src/bb_comp_prices/pipeline/probe_evidence.py`;
- `scripts/generate_*probe.py` and Amazon diagnostic/recovery generators;
- `.github/workflows/generate_*probe.yml` and diagnostic workflows;
- `docs/*PROBE*.md`, `docs/LIVE_PROBE_EVIDENCE.md`, and Amazon diagnostic reports.

The complete current workflow and script inventories should be used when extending this page; individual historical probe scripts do not require separate top-level documentation pages unless they remain separately operated systems.

## Probe Families

### Best Buy PDP/live evidence

`bestbuy_probe.py` and `pipeline/probe_evidence.py` preserve and inspect PDP HTML plus parsed `window.__INITIAL_STATE__` evidence. `build_probe_evidence_markdown()` locates the most recent S3 `.probe.json` run under `raw/bestbuy/pdp/`, reloads its raw HTML, parses embedded state, enumerates Marketplace-related state paths, summarizes embedded-state marker counts, and writes `docs/LIVE_PROBE_EVIDENCE.md` through `scripts/generate_probe_evidence.py`.

This family is used to investigate parser breakage and discover durable source fields before modifying the production PDP parser.

### Best Buy category browser research

`bestbuy/category_discovery.py` is now part of current production discovery, while `scripts/generate_category_browser_probe.py` and `docs/CATEGORY_DISCOVERY_PROBE.md` retain browser-level exploratory evidence about category navigation, loading, links, and product discovery.

The production category pipeline is authoritative for current selectors/classification behavior. The retained browser report is supporting evidence and research history.

### Best Buy alternate-offer contract research

The repository retains several complementary research paths that led to the current offers API implementation:

- `generate_offers_page_probe.py` -> `docs/OFFERS_PAGE_PROBE.md` examines the alternate-offers page/rendered content;
- `generate_browser_network_probe.py` -> `docs/OFFERS_BROWSER_NETWORK_PROBE.md` captures relevant browser requests/responses while navigating the offers route;
- `generate_js_contract_probe.py` -> `docs/OFFERS_JS_CONTRACT_PROBE.md` scans same-origin JavaScript bundles for offer/API contract terms;
- `generate_offers_api_probe.py` -> `docs/OFFERS_API_PROBE.md` records direct API behavior.

The browser-network generator currently runs against the first configured test product and records method, URL, response status/resource/content type, response/body previews, request post data, and JSON shape for up to 50 captured responses.

The JavaScript-contract generator likewise uses the first configured test PDP, scans same-origin scripts, and records snippets around matching terms. These reports are contract-discovery aids, not executable API specifications.

Current production offer extraction is instead defined by `bestbuy/offers_client.py` and `pipeline/bestbuy_extract.py`.

### Amazon search/detail research and recovery

Current and historical Amazon research includes:

- `generate_amazon_search_probe.py` -> `docs/AMAZON_SEARCH_PROBE.md`;
- `generate_amazon_details_probe.py` -> `docs/AMAZON_DETAILS_PROBE.md`;
- `generate_amazon_isolated_baseline.py` -> `docs/AMAZON_ISOLATED_BASELINE.md`;
- `generate_amazon_known_asin_recovery.py` -> `docs/AMAZON_KNOWN_ASIN_RECOVERY.md`;
- `generate_amazon_run_diagnostics.py` -> `docs/LATEST_AMAZON_RUN_DIAGNOSTICS.md`.

Some of this evidence predates the current search-health gate and current exact-variant logic. Historical zero-result runs or older recovery outcomes must therefore be classified by date/source version and cannot override current `amazon_extract.py`, `amazon_search_health.py`, `amazon_variant.py`, and tests.

### Walmart research

`walmart_probe.py`, `walmart_details_probe.py`, their generators, and their two committed reports are still active probes because production acquisition remains blocked by the observed identity-verification challenge. See the dedicated Walmart subsystem page for the current structured-detector inconsistency and blocked production boundary.

## Workflow Pattern

Most research workflows are `workflow_dispatch` only and follow this pattern:

```text
manual dispatch
  -> checkout main
  -> Python 3.12
  -> install base or browser extra
  -> install Chromium when needed
  -> run scripts/generate_*.py
  -> write Markdown report under docs/
  -> git commit/push report to bb-comp-prices main when changed
```

Many report-generation workflows request `contents: write` specifically because they commit generated reports directly to `bb-comp-prices` `main`. Workflows that need current S3 products/evidence also inject the configured AWS credential secret names.

This source-repository research workflow is distinct from the `eirepolitic.github.io` documentation process, which uses focused documentation PRs and validation/deployment gates.

## Evidence Classes

Use the following hierarchy when interpreting probe material:

| Evidence class | Example | How to use it |
| --- | --- | --- |
| Current production source/workflow | `pipeline/amazon_extract.py` | Authoritative current implementation. |
| Current tests/current validation | `tests/unit/*`, `LATEST_*REPORT.md` when aligned with source | Verify implemented rules and observed data. |
| Current probe report | Walmart challenge report | Evidence of current observed retailer behavior; not a production contract. |
| Historical probe/diagnostic | older Amazon baseline/run diagnostics | Context/research history; mark stale/superseded when source changed. |
| Build plan | `docs/BUILD_PLAN.md` | Intended/planned architecture only unless confirmed elsewhere. |

A report filename containing `LATEST` does not guarantee semantic currency. Compare its methods/fields/results with current executable source and generation logic.

## Safe Promotion from Probe to Production

A probe finding should only become production behavior when all applicable steps are complete:

1. Reproduce the retailer behavior with a bounded probe and preserve enough evidence to distinguish a real contract from a transient challenge/page state.
2. Identify the least brittle source field/API/selector that satisfies the requirement.
3. Add or update reusable parser/client logic under `src/bb_comp_prices/`, rather than importing report-generation code into the production pipeline.
4. Add focused unit tests for the new contract, including known failure/challenge cases.
5. Add publication/health gates when bad evidence could overwrite stable latest data.
6. Run the relevant validation/report path on real current data.
7. Update the platform documentation and classify the old research path as current supporting evidence or superseded history.

Do not promote a single successful DOM selector or one observed network call into an unattended production dependency without tests and failure handling.

## Diagnostics During an Incident

For a retailer acquisition failure:

1. Start from the first failing production stage and its `run_id`/manifest/raw evidence.
2. Determine whether the failure is transport, challenge/blocking, page/API schema, normalization, variant/data-quality, or S3 publication.
3. Use an existing targeted probe before writing a new one.
4. Prefer a small known fixture/product over a broad retailer crawl.
5. Preserve final URL, status, page title, explicit block markers, and relevant raw response shape.
6. Never interpret HTTP 200 alone as success; Walmart's challenge is a verified example of a 200 response containing a block page.
7. Do not repeatedly retry blocked retailer requests at high concurrency.
8. Once the issue is understood, fix/test production logic separately from the probe/report generator.

## Security and Privacy Boundary

Probe workflows can collect raw HTML, body previews, JavaScript snippets, URLs, network response/request previews, and S3 evidence. They must not be expanded to publish:

- AWS credential values;
- cookies/session tokens;
- authorization headers;
- challenge tokens;
- private account identifiers;
- unrelated personal data returned by a browser session.

Browser probes should use unauthenticated/public retailer sessions unless an explicitly approved architecture requires otherwise.

Research that would require a third-party scraping service, paid proxy/network product, retailer account login, anti-bot bypass, or new AWS access pattern is an architecture/security/cost decision rather than routine probe maintenance.

## Known Limitations

- Many generated reports are point-in-time observations and may become stale quickly as retailer sites change.
- Several workflows commit generated reports directly to source `main`, which can create noise and concurrent Pages/documentation activity elsewhere.
- Report formats are human-readable Markdown rather than one normalized diagnostic schema.
- Historical Amazon reports can conflict with current health/verification behavior.
- Probe code has varying maturity; Walmart search block detection is a known example where report context is stronger than the structured detector.
- There is no centralized retention/version index for every generated report beyond Git history and any referenced S3 raw evidence.
- A probe passing does not guarantee the corresponding production pipeline will pass because inputs, selectors, thresholds, publication gates, and runtime context can differ.

## Next Safe Development Action

Document the validation/data-quality framework from the four current validation modules, their generators/workflows/reports, unit-test CI, and publication guards. Explicitly identify checks that are current, reports that are stale, and which failures prevent publication versus merely flag observed data.

## Related Documents

- [Walmart.ca acquisition and probe subsystem](/projects/systems/bb-comp-prices-walmart-probes/)
- [Amazon.ca acquisition and recovery](/projects/systems/bb-comp-prices-amazon-acquisition/)
- [Best Buy product and Marketplace-offer extraction](/projects/systems/bb-comp-prices-bestbuy-extraction/)
- [Best Buy Marketplace category discovery](/projects/systems/bb-comp-prices-bestbuy-category-discovery/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `bb-comp-prices` `scripts/`, `.github/workflows/`, `docs/`, probe modules under `bestbuy/` and `competitors/`, `pipeline/probe_evidence.py`, and current production pages documented earlier in this workstream.
- Verified by: High Director
- Verification scope: probe families, report-generation workflow pattern, Best Buy/Amazon/Walmart research roles, evidence precedence, safe promotion/recovery procedure, security boundary, and known limitations.
