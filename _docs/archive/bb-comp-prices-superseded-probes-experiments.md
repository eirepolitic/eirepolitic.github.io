---
title: Superseded bb-comp-prices probes and experiments
summary: Historical Amazon baseline, isolated-search, offer-contract, and diagnostic experiments retained for research context but superseded as current operational authority.
section: archive
doc_type: reference
status: archived
created: 2026-08-07
updated: 2026-08-07
archived_date: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
order: 55
permalink: /projects/archive/bb-comp-prices-superseded-probes-experiments/
repository: bb-comp-prices
system: Competitor Pricing Platform
superseded_by: /projects/systems/bb-comp-prices-diagnostics-research/
archive_reason: Current production pipelines, health gates, validated clients, and active diagnostics now supersede these experiments as operational authority.
tags:
  - bb-comp-prices
  - archive
  - probes
  - experiments
---

# Superseded bb-comp-prices probes and experiments

> This page preserves historical context. It must not be treated as the current implementation unless explicitly stated.

## Archive Summary

`bb-comp-prices` retains several experiments that were useful while retailer acquisition contracts were being discovered but are no longer authoritative for current production operation. They remain in the source repository because they preserve valuable evidence about earlier failure modes, search strategies, API/DOM discovery, and the reasoning that led to today's production clients and health gates.

This archive does **not** mean every probe in the repository is obsolete. Current Walmart challenge probes and targeted diagnostics remain active because they still support present operational decisions. The active framework is documented at [bb-comp-prices diagnostics, probes, and extraction research](/projects/systems/bb-comp-prices-diagnostics-research/).

## Archive Status

- Archived on: `2026-08-07`
- Archive reason: current production pipelines, tests, health gates, and active diagnostic framework supersede these experiments as implementation authority.
- Replacement: [bb-comp-prices diagnostics, probes, and extraction research](/projects/systems/bb-comp-prices-diagnostics-research/)
- Current recommendation: use current production source and the active diagnostic framework first; consult these experiments only when historical context is relevant.

## Historical Context

The platform developed retailer acquisition iteratively. Early work had to determine:

- which Best Buy fields/API routes exposed Marketplace products and alternate offers;
- whether browser-rendered pages, JavaScript bundles, or direct APIs were the most stable offer source;
- how Amazon.ca behaved under different browser-session/query pacing strategies;
- how to distinguish zero-result retailer failure from a legitimate zero-match run;
- how known ASINs could be recovered when search/detail behavior was incomplete.

The resulting experimental reports were intentionally concrete and evidence-heavy. As production source matured, their role changed from candidate implementation guidance to historical research evidence.

## Last Known Implementation State

### Amazon isolated-session baseline

Retained source:

- `src/bb_comp_prices/competitors/amazon_isolated_probe.py`;
- `scripts/run_amazon_baseline.py`;
- `.github/workflows/amazon_baseline_extract.yml`;
- `scripts/generate_amazon_isolated_baseline.py`;
- `.github/workflows/generate_amazon_isolated_baseline.yml`;
- `docs/AMAZON_ISOLATED_BASELINE.md`.

The isolated probe uses one cleaned core-title query per Best Buy product, one first search page, a fresh browser context per product, and long request spacing. `run_amazon_baseline.py` patches the production Amazon pipeline's search function with this isolated probe, fixes query/page coverage to one first page, and labels the resulting manifest `amazon-baseline-extract` with a warning that coverage is not exhaustive.

The retained report demonstrates that this strategy could return healthy first-page results for the observed Pixel, iPhone, and Samsung inputs. It also shows why first-page search alone was insufficient as a production contract: result sets include renewed products, accessories, nearby variants, other capacities/colours, and unrelated products requiring stronger candidate/variant filtering.

The current production replacement is `pipeline/amazon_extract.py` plus `competitors/amazon_probe.py`, `amazon_variant.py`, detail recovery, search-health gating, and the exhaustive/current workflow documented in [Amazon.ca competitor acquisition and recovery](/projects/systems/bb-comp-prices-amazon-acquisition/).

### Historical Amazon zero-result/run diagnostics

Retained source:

- `scripts/generate_amazon_run_diagnostics.py`;
- `.github/workflows/generate_amazon_run_diagnostics.yml`;
- `docs/LATEST_AMAZON_RUN_DIAGNOSTICS.md`.

The committed diagnostic contains older runs where zero Amazon search results could still appear in manifests reported as succeeded. That behavior predates the current `pipeline/amazon_search_health.py` hard gate.

It is superseded as a description of success semantics. Current Amazon source requires positive search evidence, healthy pages, and search coverage for every source product before publication proceeds.

### Known-ASIN recovery experiments

Retained source:

- `scripts/generate_amazon_known_asin_recovery.py`;
- `.github/workflows/generate_amazon_known_asin_recovery.yml`;
- `docs/AMAZON_KNOWN_ASIN_RECOVERY.md`.

These experiments remain useful when investigating known candidate recovery, but they do not define current matching acceptance or publication. Current Amazon candidate/detail/search-fallback logic and the current Amazon validation report are authoritative.

The current validation evidence still reports missing expected ASINs, so this historical work remains relevant research context even though it is not a production subsystem.

### Early Best Buy alternate-offer contract experiments

Retained research reports/generators include:

- `docs/OFFERS_PAGE_PROBE.md` / `scripts/generate_offers_page_probe.py`;
- `docs/OFFERS_BROWSER_NETWORK_PROBE.md` / `scripts/generate_browser_network_probe.py`;
- `docs/OFFERS_JS_CONTRACT_PROBE.md` / `scripts/generate_js_contract_probe.py`;
- `docs/OFFERS_API_PROBE.md` / `scripts/generate_offers_api_probe.py`;
- their corresponding `generate_*` GitHub Actions workflows.

These experiments investigated the rendered alternate-offers page, browser network traffic, same-origin JavaScript bundles, and direct API behavior. Their production-authority role is superseded by `src/bb_comp_prices/bestbuy/offers_client.py` and `pipeline/bestbuy_extract.py`, which currently implement the normalized all-offers path and seller enrichment.

The reports remain useful if Best Buy changes its offer contract and current production behavior needs to be rediscovered.

### Early category/PDP evidence reports

`docs/CATEGORY_DISCOVERY_PROBE.md` and `docs/LIVE_PROBE_EVIDENCE.md` preserve exploratory evidence about category/PDP behavior. Parts of their findings are now embedded in current category discovery and PDP parsing.

They are not archived as unusable files; they are superseded only as the **source of current implementation truth**. Current `bestbuy/category_discovery.py`, `pipeline/category_discovery.py`, `bestbuy/initial_state.py`, tests, and current validation reports take precedence.

## Source of Truth

For current operation, use this precedence:

1. current executable source/workflows and current tests;
2. current validation reports that are aligned with current source;
3. active targeted probe evidence;
4. the historical experiments listed on this page;
5. `docs/BUILD_PLAN.md` for planned/intended architecture only.

For historical questions about an experiment itself, the retained source script/module plus the report generated by its matching workflow are the authoritative historical pair.

## Why It Was Archived

These experiments were archived from current operational authority because one or more of the following became true:

- a production client/parser now implements the discovered contract directly;
- a broader current pipeline supersedes the experiment's deliberately narrow coverage;
- a hard health/data-quality gate now makes the older run semantics invalid;
- current tests/variant rules provide stronger correctness evidence than the experiment;
- the report is retained for diagnosis/history rather than routine operation.

No source files were deleted as part of this documentation workstream.

## Successor or Replacement

| Historical area | Current authority |
| --- | --- |
| Amazon isolated first-page baseline | `amazon_extract.py`, current Amazon probe/detail/variant/health logic, exhaustive workflow |
| Older zero-result Amazon run diagnostics | `amazon_search_health.py` + current Amazon manifests/raw evidence |
| Known-ASIN recovery experiment | Current Amazon acquisition + current validation/diagnostic framework |
| Best Buy offers page/network/JS exploration | `bestbuy/offers_client.py` + `bestbuy_extract.py` |
| Category/PDP exploratory evidence | Current category/PDP parser pipeline and current validation |

The active umbrella documentation is [bb-comp-prices diagnostics, probes, and extraction research](/projects/systems/bb-comp-prices-diagnostics-research/).

## Security Considerations

Historical reports can contain retailer URLs, page excerpts, network-response snippets, IDs, and S3 object references. Retaining these reports does not justify adding authentication/session data to future reports.

Do not preserve or publish:

- AWS credential values;
- browser cookies/session tokens;
- authorization headers;
- retailer challenge tokens;
- private account identifiers.

If an old experiment is rerun for research, apply the current security and safe-probe rules rather than copying historical behavior blindly.

## Known Limitations

- Retained experiments are executable source in some cases; `archived` here means superseded as operational/documentation authority, not necessarily physically disabled.
- Historical retailer observations may no longer reproduce because external pages/APIs change.
- The Amazon isolated baseline intentionally used narrow one-query/one-page coverage and cannot establish exhaustive competitor coverage.
- Historical Amazon run diagnostics predate the current search-health gate.
- Offer-contract reports may contain selectors/routes that have changed since the current production client was established.
- Some current reports with historical content use names such as `LATEST_*`; filename alone does not establish semantic currency.
- Current Walmart search/detail probes are **not** part of this superseded archive; they remain active diagnostics for the present blocked production state.

## Outstanding Historical Questions

- Exact source commits/timestamps for every generated probe report are not embedded uniformly in the report bodies.
- Some retained experiment workflows can still be manually dispatched; repository source does not mark them deprecated in workflow metadata.
- The current matching validation report should be regenerated separately; its staleness is a current validation gap, not merely an archived experiment.

## Next Safe Action

When encountering one of these historical scripts or reports, first read the current retailer/platform page and the active diagnostics framework. Only rerun a historical experiment when it answers a specific current diagnostic question that the active production evidence cannot answer. Do not reconnect a baseline/experiment to production publication without a deliberate architecture review, current tests, and current validation.

## Related Documents

- [bb-comp-prices diagnostics, probes, and extraction research](/projects/systems/bb-comp-prices-diagnostics-research/)
- [Amazon.ca competitor acquisition and recovery](/projects/systems/bb-comp-prices-amazon-acquisition/)
- [Best Buy product and Marketplace-offer extraction](/projects/systems/bb-comp-prices-bestbuy-extraction/)
- [Best Buy Marketplace category discovery](/projects/systems/bb-comp-prices-bestbuy-category-discovery/)
- [bb-comp-prices validation and data-quality framework](/projects/systems/bb-comp-prices-validation-data-quality/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `bb-comp-prices` source tree; `amazon_isolated_probe.py`; `run_amazon_baseline.py`; `amazon_baseline_extract.yml`; `AMAZON_ISOLATED_BASELINE.md`; Amazon diagnostic/recovery generators/workflows/reports; Best Buy offer-contract probe generators/reports; current production/diagnostic documentation created in this workstream.
- Verified by: High Director
- Verification scope: historical role, current replacement/authority, retained file/workflow paths, narrow Amazon baseline behavior, older success-semantics conflict, and security/continuation guidance.
- Unverified areas: exact historical source commit associated with every generated report where the report body does not record it.
