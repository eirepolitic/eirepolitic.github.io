---
title: Revenue Investigation — Wave 5 Stage 4 Implementation Plans
summary: Implementation, validation and scalable acquisition plans for the three strongest Wave 5 inbound/self-serve concepts.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 229
permalink: /projects/notes/revenue-investigation-wave-5-stage-4-implementation-plans/
tags: [revenue-investigation, research, inbound, self-serve, acquisition, automation, wave-5]
---

# Wave 5 Stage 4 — Implementation Plans

No product is being built at this stage. These are implementation and validation plans only.

## Rank 1 — Excel/CSV leading-zero preservation converter

### Core promise
Upload a CSV/XLSX, identify columns at risk of losing leading zeros, preview the repair, and download a corrected file without changing unrelated values.

### MVP
- Browser upload for CSV/XLSX.
- Detect columns containing mixed-width digit strings, leading-zero values, long identifiers or known code patterns.
- Preview before/after values.
- User explicitly confirms which columns are text identifiers.
- Export corrected XLSX/CSV.
- No account for free tier.
- Paid checkout unlocks larger files, multi-file batch jobs and saved schemas.

### Suggested stack
- Static front end: Cloudflare Pages or GitHub Pages for landing/help pages.
- Processing: client-side where feasible using SheetJS/Papa Parse; serverless function only for oversized jobs.
- Payments: Stripe Payment Links or Lemon Squeezy.
- Analytics: privacy-conscious event tracking for upload, preview, export and checkout events.

### Estimated MVP cost
CA$0–$40/month until traffic is meaningful.

### Pricing test
- Free: one file under a size/row cap.
- CA$9: one large/batch conversion.
- CA$15/month: saved schemas + recurring batch use.

### Acquisition pipeline — inbound first
1. Programmatically generate useful landing/help pages for distinct search intents: Excel leading zeros, CSV leading zeros, HS code zeros, SKU zeros, account-number zeros.
2. Each page contains a working free example and links directly into the converter with the relevant detection rule preselected.
3. Search-console data feeds a weekly script that ranks queries by impressions, CTR, conversion and paid intent.
4. The script proposes factual page expansions from actual query wording; human approval is required before publishing new pages.
5. High-converting free users enter an automated in-product upgrade sequence based only on product usage, not scraped contact lists.
6. Optional validation outreach is limited to a small, manually approved sample of spreadsheet-heavy communities or businesses; no ongoing cold-lead engine is required.

### Validation threshold
GO if, within the first 100 qualified tool sessions:
- 10+ users complete a repair/export;
- 2+ users buy a large/batch conversion; and
- at least 25% of users who reach the preview complete an export.

KILL/REWORK if users search for the problem but consistently solve it manually without using the tool.

### Main risk
The problem is real but may be too easy to solve once explained. The product therefore needs to win on immediate repair, safety and batch convenience rather than education alone.

---

## Rank 2 — Canadian importer-report self-serve lookup

### Core promise
Search a Canadian product or HS code and instantly buy a cleaned, source-dated importer report assembled from official Canadian public data.

### MVP
- Ingest current Canadian Importers Database XLSX resources.
- Normalize HS6/HS10 descriptions while preserving leading zeros.
- Search by keyword or HS code.
- Free result page: description, source year, importer count band and geography preview.
- Paid report: importer names, city/province, product classification, source metadata, concentration summary and CSV/XLSX export.
- Prominent disclosure that the underlying data is Government of Canada public data and not real-time shipment intelligence.

### Suggested stack
- Python ingestion pipeline on GitHub Actions or AWS Lambda.
- SQLite/Postgres or compact generated JSON/parquet index depending dataset size.
- Static SEO landing pages generated per viable HS/product category.
- Stripe/Lemon Squeezy checkout with signed report-download links.

### Estimated MVP cost
CA$5–$60/month depending hosting/search approach.

### Pricing test
- Free preview.
- CA$15 single report.
- CA$49 five-report pack.
- CA$89 researcher/exporter credit pack.

### Acquisition pipeline — search/data pages rather than prospect chasing
1. Data ingestion automatically generates indexable product-category pages from official source descriptions and factual summary statistics.
2. Pages are scored for search value using query impressions, click-through rate, number of importers, and report-purchase conversion.
3. A weekly job identifies categories with rising search impressions or repeated on-site searches and creates candidate pages/report bundles.
4. Candidate content uses only official dataset facts plus clearly labeled derived aggregates; no invented company attributes or claims.
5. Paid-search experiments, if used, target only high-intent product/HS queries and stop automatically at a predefined cost-per-purchase ceiling.
6. A controlled validation outreach lane may identify export consultants, trade researchers or brokers from public directories, score them for fit, create a factual sample report for a relevant category, and queue only a small number for compliant/manual-approved contact. Replies are triaged and the owner is alerted only for qualified interest. This lane is optional and is not the primary acquisition engine.

### Validation threshold
GO if 10 initial category pages generate:
- 50+ qualified visits;
- 3+ paid report purchases; and
- at least 2 purchases occur without any direct outreach.

KILL/REWORK if users consistently leave for the free government source without valuing the cleaned report.

### Main risk
Because the source data is free, the paid product must save enough time to justify even a modest price. Convenience, preserved identifiers, clean exports and quick interpretation are the product—not exclusive data.

---

## Rank 3 — Environment-variable documentation checker for GitHub

### Core promise
A pull-request check that catches environment variables used in code but missing from `.env.example` or project documentation, plus obsolete variables that should be removed.

### MVP
- GitHub Action initially supporting Python and Node repositories.
- Configurable scan paths and ignore patterns.
- Extract common patterns such as `os.getenv`, `os.environ`, `process.env`, and selected framework patterns.
- Compare against `.env.example` or a declared manifest.
- PR annotation and concise Markdown summary.
- Default read-only operation; no secret values are read or stored.
- Free core Action; paid organization features only after adoption evidence.

### Suggested stack
- Python or TypeScript Action.
- GitHub Marketplace listing.
- Optional lightweight SaaS only for organization dashboards/history.

### Estimated MVP cost
Near CA$0 for the core Action; CA$10–$40/month if a hosted dashboard is added.

### Pricing test
- Free: core repository check.
- CA$9/month organization tier: saved policy sets + history.
- CA$29/month team tier: organization-wide dashboard and policy enforcement.

### Acquisition pipeline — product-led GitHub distribution
1. Publish the free Action with a copy-paste workflow and example failing/passing repository.
2. GitHub Marketplace/search, README SEO and public examples become the primary discovery layer.
3. Anonymous/aggregate telemetry is avoided by default; adoption is measured through public Marketplace/repository signals and opt-in hosted features.
4. A scheduled job monitors public issues/discussions and repository search terms related to missing env documentation, then produces a ranked list of recurring language/framework patterns to support next features.
5. For validation only, a prospect-discovery script may identify public repositories with `.env.example` plus obvious code/documentation mismatch, score them, create a factual local scan result, and prepare a non-spammy issue/PR suggestion only where repository contribution rules allow it. No automated mass issue creation.
6. Paid-upgrade prompts are shown only to users who voluntarily enable organization/history features; qualified support or upgrade requests alert the owner.

### Validation threshold
GO if within 60 days:
- 25 repositories install/use the Action;
- 5 repositories use it repeatedly across multiple PRs; and
- 3 organizations request or prepay for policy/history features.

KILL/REWORK if adoption occurs but no team expresses willingness to pay for anything beyond the free check.

### Main risk
The free Action may be useful but difficult to monetize. Paid value must be organization-level policy/history rather than withholding the basic checker.

## Overall recommendation

Build order if Stage 5 is later authorized:

1. Leading-zero converter — fastest and cheapest test of inbound search-driven demand.
2. Importer-report lookup — strongest connection to a current, structured Canadian dataset and naturally creates many search landing pages.
3. Environment-variable checker — strongest built-in marketplace distribution but less certain paid conversion.

## Verification record

- Last verified: 2026-10-16
- Stage 4 status: complete
- Stage 5: not started
