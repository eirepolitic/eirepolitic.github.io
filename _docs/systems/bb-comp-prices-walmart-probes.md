---
title: bb-comp-prices Walmart.ca acquisition and probe subsystem
summary: Verified Walmart.ca search/detail probe framework, identity-challenge behavior, current blocked production status, workflow operation, and safe research boundary.
section: systems
doc_type: pipeline
status: experimental
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 36
permalink: /projects/systems/bb-comp-prices-walmart-probes/
tags:
  - walmart
  - playwright
  - probes
  - experimental
---

# bb-comp-prices Walmart.ca acquisition and probe subsystem

## Summary

The current Walmart.ca implementation is an experimental probe/research subsystem, not a production acquisition pipeline. Repository source contains Playwright-based search and product-detail probes plus manual GitHub Actions workflows that regenerate Markdown evidence reports. The end-to-end orchestrator explicitly records Walmart as `blocked` rather than running a persisted Walmart extraction stage.

Current committed probe evidence shows Walmart.ca redirecting unattended search and product-detail requests to an identity-verification page. No current source publishes normalized Walmart products/offers to S3, and no current product-matching pipeline reads Walmart data.

## Source of Truth

- search probe: `src/bb_comp_prices/competitors/walmart_probe.py`;
- detail probe: `src/bb_comp_prices/competitors/walmart_details_probe.py`;
- search report generator: `scripts/generate_walmart_search_probe.py`;
- detail report generator: `scripts/generate_walmart_details_probe.py`;
- candidate fixtures: `config/walmart_test_candidates.yaml`;
- workflows: `.github/workflows/generate_walmart_search_probe.yml`, `.github/workflows/generate_walmart_details_probe.yml`;
- unit tests: `tests/unit/test_walmart_probe.py`, `tests/unit/test_walmart_details_probe.py`;
- current reports: `docs/WALMART_SEARCH_PROBE.md`, `docs/WALMART_DETAILS_PROBE.md`;
- current production boundary: `src/bb_comp_prices/pipeline/orchestrator.py`.

`docs/BUILD_PLAN.md` may describe intended Walmart acquisition architecture, but current executable source/workflows do not implement a persisted Walmart production pipeline.

## Current Maturity

Current state is:

```text
Best Buy latest products
  -> Walmart search probe (experimental)
     -> Markdown research report

Static known Walmart candidate URLs
  -> Walmart detail probe (experimental)
     -> Markdown research report

End-to-end orchestration
  -> Walmart selected
     -> blocked stage + warning
     -> no Walmart normalized output
```

Not currently implemented:

- durable `latest/walmart_products.*` publication;
- durable Walmart offer publication;
- Walmart candidate scoring/normalization equivalent to Amazon;
- Walmart search-health gate for production publication;
- Walmart-to-Best Buy persisted product matches;
- scheduled Walmart acquisition.

## Search Query Construction

`WalmartSearchInput` contains:

- `bestbuy_product_id`;
- source title;
- optional brand;
- optional model number;
- UPC tuple.

`build_walmart_queries()` generates identifier-first searches in this order:

1. each non-empty UPC;
2. brand + model when either is available;
3. full Best Buy title.

Queries are case-insensitively deduplicated and truncated to `max_queries`, default 3.

The committed unit test confirms this ordering and limit behavior.

## Search Probe Runtime

`probe_walmart_searches()` launches headless Chromium with:

- locale `en-CA`;
- timezone `America/Vancouver`;
- viewport `1440x1200`;
- a Chromium-style desktop user agent.

Search URL:

```text
https://www.walmart.ca/en/search?q=<url-encoded query>
```

Current defaults:

- up to 3 queries per product;
- up to 10 extracted results per query;
- 45-second navigation timeout.

After DOM content load, it attempts a 10-second `networkidle` wait and then waits an additional 3 seconds.

The page extractor tries several likely product-card selectors including `data-testid="product-tile"`, `data-automation-id="product-tile"`, `data-item-id`, and `data-product-id`. It then attempts to extract product ID, title, URL, price text, sponsored marker, and card text preview.

This extraction is exploratory DOM research, not a stable published Walmart schema.

## Search Probe Blocking Detection

The search probe currently detects body-text markers for:

- `verify you are human`;
- `are you a robot`;
- `access denied`;
- `request blocked`;
- `service unavailable`.

However, the currently committed `docs/WALMART_SEARCH_PROBE.md` shows repeated redirects to:

```text
https://www.walmart.ca/blocked?...
```

with page title `Verify Your Identity` and body text beginning `We like real shoppers, not robots!`, while the report records `Block signals: []`.

This is a verified diagnostic limitation: the search probe's marker set does not currently recognize the exact observed challenge wording or `/blocked` URL. The zero-result report therefore still clearly demonstrates blocking from final URL/title/body evidence even though its structured `block_signals` list is empty.

Do not interpret `block_signals=[]` in that report as a successful/clear Walmart search.

## Search Probe Input and Report Generation

`scripts/generate_walmart_search_probe.py` reads:

```text
latest/bestbuy_products.parquet
```

from configured S3, maps each row into `WalmartSearchInput`, runs the browser probe with 3 queries/product and 10 results/query, and writes:

```text
docs/WALMART_SEARCH_PROBE.md
```

The generator does not publish raw Walmart HTML/JSON or normalized Walmart rows to S3.

The search-probe workflow is manual dispatch only. It uses Python 3.12, installs `.[browser]` plus Chromium, injects AWS credentials because the generator reads Best Buy latest data from S3, then commits the generated Markdown report directly to `main` using the GitHub Actions bot identity.

Its repository permission is `contents: write`.

## Detail Probe

`probe_walmart_details()` receives explicit known candidate URLs rather than discovering candidates itself. The current test fixture `config/walmart_test_candidates.yaml` contains five candidate URLs across three Best Buy products, with research labels such as:

- `marketplace`;
- `walmart_retail`;
- `unknown`.

Those `expected_channel` values are fixture expectations for research comparison, not verified production classification.

For each candidate, the detail probe attempts to collect:

- final URL/status/navigation error;
- page title/body preview;
- block signals;
- product title;
- price;
- seller;
- fulfillment text;
- availability/add-to-cart state;
- JSON-LD blocks.

No normalization into `WalmartProductRecord`/`WalmartOfferRecord` exists in current source.

## Detail Block Detection

`detect_walmart_block_signals()` combines final URL, page title, and body text, and detects:

- `identity_challenge` — `press and hold the button below`;
- `robot_check` — `we like real shoppers, not robots`;
- `verify_identity` — `verify your identity`;
- `access_denied`;
- `request_blocked`;
- `blocked_url` when the final URL contains `/blocked?`.

The unit test explicitly verifies the current identity-challenge combination.

The committed `docs/WALMART_DETAILS_PROBE.md` shows all five known candidate PDPs redirected to the blocked identity-verification page. Each records status 200 from the challenge page, four block signals, no usable price/seller/fulfillment/availability, and no JSON-LD blocks.

This is current repository evidence that direct unattended PDP extraction was blocked in the observed probe environment.

## Detail Probe Workflow

`.github/workflows/generate_walmart_details_probe.yml` is manual dispatch only. It:

1. checks out `main`;
2. uses Python 3.12;
3. installs `.[browser]` and Chromium;
4. runs `scripts/generate_walmart_details_probe.py`;
5. commits `docs/WALMART_DETAILS_PROBE.md` directly to `main` when changed.

It has `contents: write` because the workflow commits the generated report. Unlike the search probe, the detail generator uses repository fixture URLs and does not currently require S3/AWS credentials.

## End-to-End Production Boundary

`run_end_to_end()` accepts `walmart` in the competitor selection but does not call either Walmart probe as a production stage. Instead it appends a blocked-stage record and warning explaining that unattended Walmart.ca search/PDP requests redirect to identity verification.

Therefore:

- selecting Walmart does not acquire Walmart prices;
- no Walmart S3 latest/history data product is produced;
- product matching continues to use Amazon products only;
- the schema allowance for `competitor_source="walmart"` is future/general model capacity, not evidence of active Walmart matching.

## Safe Research Procedure

When investigating Walmart behavior:

1. Use the existing manual probe workflows rather than adding Walmart to production orchestration.
2. Read final URL, page title, body preview, status, and block signals together; HTTP 200 can represent an identity challenge.
3. Do not repeatedly rerun blocked browser requests at high frequency or increase concurrency to defeat challenge behavior.
4. Use a small known candidate fixture when testing detail parsing changes.
5. Treat report results as environment/time-specific observations.
6. If Walmart page behavior changes, first update/prove block detection and extraction selectors in probes plus unit tests before creating any production normalization/persistence path.
7. Any proposal to introduce a production Walmart acquisition mechanism, third-party service, paid API, alternate network path, or anti-bot workaround is an architecture/cost/security decision and requires explicit review before implementation.

## Security Boundary

The search probe accesses Best Buy latest products through AWS credentials supplied by GitHub Secrets and makes public browser requests to Walmart.ca. The detail probe uses static repository URLs and public browser requests.

No Walmart authentication credential is present in the inspected implementation.

Generated reports can contain retailer URLs, page text previews, IDs, and diagnostic details. They must not be modified to capture or publish session cookies, challenge tokens, account identifiers, or credential values.

## Current Evidence

### Search report

`docs/WALMART_SEARCH_PROBE.md` shows all attempted UPC, brand/model, and title searches for the observed three Best Buy products redirecting to Walmart's blocked identity-verification page with zero extracted product cards.

The report's empty structured `block_signals` is an implementation limitation, not evidence that requests were unblocked.

### Detail report

`docs/WALMART_DETAILS_PROBE.md` shows all five explicit Walmart candidate URLs redirected to the same verification flow. The stronger detail detector correctly identifies the blocking signals.

Neither report proves Walmart is always inaccessible from every environment; they establish the observed repository-controlled probe behavior that led current orchestration to block production Walmart acquisition.

## Known Limitations

- Search and PDP probes are browser/DOM research utilities, not persisted acquisition stages.
- Search block-signal detection currently misses the exact observed identity challenge that the detail detector recognizes.
- Search extraction selectors are heuristic and currently have no positive committed example proving structured Walmart cards were extracted in the latest report.
- Detail fixture channel labels are expectations, not authoritative seller-channel classification.
- No current Walmart product/offer Pydantic persistence models or S3 product contract exist.
- No Walmart search-health publication gate or recovery system exists.
- No production matching consumes Walmart rows.
- Probe workflows directly commit generated reports to `main`; this is research automation rather than the documentation repository's focused-PR process.
- Current reports are point-in-time evidence and may become stale as Walmart changes its pages/challenge behavior.

## Next Safe Development Action

Document the cross-retailer probe/diagnostics/extraction-research framework, grouping Best Buy, Amazon, Walmart, browser-network, JS-contract, offers-page/API, and historical evidence generators by purpose and maturity. Keep individual probe scripts subordinate unless they are active separately operated subsystems.

## Related Documents

- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)
- [Amazon.ca competitor acquisition and recovery](/projects/systems/bb-comp-prices-amazon-acquisition/)
- [bb-comp-prices product matching and confidence scoring](/projects/systems/bb-comp-prices-product-matching/)
- [bb-comp-prices orchestration/security boundary](/projects/systems/bb-comp-prices-orchestration-security/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main`; `competitors/walmart_probe.py`; `competitors/walmart_details_probe.py`; `scripts/generate_walmart_search_probe.py`; `scripts/generate_walmart_details_probe.py`; `config/walmart_test_candidates.yaml`; both Walmart probe workflows; `tests/unit/test_walmart_probe.py`; `tests/unit/test_walmart_details_probe.py`; `docs/WALMART_SEARCH_PROBE.md`; `docs/WALMART_DETAILS_PROBE.md`; current end-to-end orchestrator.
- Verified by: High Director
- Verification scope: current probe implementation, challenge detection, query generation, detail extraction attempts, workflows/report generation, production blocked boundary, security limits, and safe research procedure.
