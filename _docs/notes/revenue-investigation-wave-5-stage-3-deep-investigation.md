---
title: Revenue Investigation — Wave 5 Stage 3 Deep Investigation
summary: Deep investigation of five distribution-first concepts that can be discovered and purchased without continuous outbound prospecting.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 228
permalink: /projects/notes/revenue-investigation-wave-5-stage-3-deep-investigation/
tags: [revenue-investigation, research, inbound, self-serve, automation, wave-5]
---

# Wave 5 Stage 3 — Deep Investigation

## 1. Excel/CSV leading-zero preservation converter

### Problem
Spreadsheet software can silently reinterpret identifiers such as HS codes, SKUs, account IDs and postal-like fields as numbers, stripping leading zeros. The Government of Canada's 2024 Canadian Importers Database explicitly warns that default Excel import behaviour can remove leading zeros from HS6 and HS10 codes.

### Product
A self-serve web utility that accepts CSV/XLSX, detects columns likely to contain identifiers, previews risky transformations, and exports a corrected file with those columns forced to text. Optional batch mode and reusable schemas become paid features.

### Why distribution can be inbound
The problem is search-shaped: users already search for variants of "Excel removes leading zeros", "CSV leading zero lost", and similar repair queries. Free single-file conversion can acquire search traffic; paid features solve repeat/bulk use.

### Monetization hypothesis
- Free: one file, size cap, manual confirmation.
- CA$9 one-off: large file or multi-file job.
- CA$12–19/month: saved schemas, batch conversion, API access.

### Risks
- Many users can solve the problem manually once they understand it.
- Must avoid altering data silently; preview and explicit column typing are essential.
- Commodity utility economics require low hosting cost and organic acquisition.

### Validation test
Publish a narrow landing/tool page for 3–5 specific search intents. Go if 10+ users complete conversions and at least 2 pay for bulk/large-file handling within the first 100 qualified tool sessions.

## 2. Canadian importer-report self-serve lookup

### Problem
ISED's Canadian Importers Database is free and useful but oriented around raw lists and search screens. The data is current, downloadable and categorized by product, city and country. A buyer who wants a quick market-entry or prospecting brief still has to choose HS codes, clean names, interpret location concentration and assemble a usable report.

### Product
A self-serve lookup where a user enters a product/HS code and receives a preview showing importer count and geography. A paid report provides cleaned importer names, location grouping, source date, HS descriptions, concentration summary and export. It must clearly state that it is repackaged public data, not proprietary shipment intelligence.

### Why distribution can be inbound
Each HS/product category can support a search-indexable landing page. Searches around "Canadian importers of X" map directly to the government dataset and a paid convenience layer.

### Monetization hypothesis
- Free preview.
- CA$12–25 per category report.
- CA$49–99 credit pack for repeat researchers/exporters.

### Risks
- Raw source is free, so value must come from speed, cleaning and interpretation.
- Government source structure can change.
- Avoid implying real-time shipment data; CID is summary data with publication lag.

### Validation test
Create 10 product-category landing pages using current CID data. Go if pages generate 50 qualified visits and 3 paid report purchases without direct sales outreach.

## 3. Canadian business-day API

### Problem
Canadian software frequently needs to calculate due dates excluding weekends and statutory holidays. The rules differ by province/territory, and some observed/public holidays differ from simple fixed-date rules.

### Product
A tiny API plus browser utility: `is_business_day`, `add_business_days`, `business_days_between`, with jurisdiction, observed-date logic, provenance, and versioned annual calendars.

### Why distribution can be inbound
Developers search for holiday/business-day libraries and APIs when implementing deadline, payroll, support or logistics logic. Documentation and code examples can rank in search and developer directories.

### Monetization hypothesis
- Free: 1,000 requests/month.
- CA$9/month: 20k requests.
- CA$29/month: 100k requests + SLA/history.

### Risks
- Open-source libraries and generic holiday APIs are substitutes.
- Requires annual verification and careful wording for jurisdiction-specific holidays.
- Legal/contractual deadlines can have special rules beyond generic business-day arithmetic; documentation must disclaim legal interpretation.

### Validation test
Ship a static API documentation page and free calculator first. Go if 20 developers create API keys and 3 exceed the free tier or request paid limits within 60 days.

## 4. Environment-variable documentation checker for GitHub

### Problem
Repositories commonly drift between variables referenced in code, `.env.example`, deployment configuration and human documentation. Missing or obsolete variables cause setup and deployment failures.

### Product
A GitHub Action that scans configurable file patterns, extracts environment-variable references, compares them with `.env.example` and/or a declared manifest, and posts a pull-request check showing undocumented, unused and newly introduced variables. Paid team tier could add organization policies and historical drift.

### Why distribution can be inbound
GitHub Actions can be installed directly from Marketplace/search and demonstrated with a copy-paste workflow. The free open-source Action itself is the acquisition channel.

### Monetization hypothesis
- Free Action for public/small repositories.
- CA$5–15/month per organization for policy packs, dashboard/history and private-org support.

### Risks
- Many languages access environment variables differently; scope must start narrow.
- GitHub Marketplace contains numerous `.env` helpers, even if most create/load variables rather than checking documentation drift.
- Free open-source users may not convert.

### Validation test
Release a Python/Node-focused Action. Go if 25 repositories install it and 3 teams request or prepay for organization-level policy/history features.

## 5. Sponsor proof-of-delivery self-serve generator

### Problem
Small newsletter and podcast publishers often need to show sponsors what was delivered, but assembling screenshots, placement details and publisher-supplied metrics into a presentable report is repetitive.

### Product
A self-serve page where the publisher enters issue/episode URL, sponsor, campaign dates and their own reach/click metrics. The system captures factual placement evidence and generates a branded PDF/share page. Metrics are always explicitly publisher-supplied and never inferred.

### Why distribution can be inbound
This can target creator search terms, newsletter communities and template-style discovery. The output is immediately understandable, and the free report can carry a small attribution link that creates product-led discovery.

### Monetization hypothesis
- Free: one watermarked report.
- CA$12 per clean report.
- CA$29–49/month for branding, saved sponsors and history.

### Risks
- Creator willingness to pay may be low.
- Screenshot capture can break on paywalled/email-only issues.
- Must never present estimated metrics as verified delivery data.

### Validation test
Launch free report creation with paid removal/branding. Go if 30 reports are generated organically and 3 creators pay or create a second report within 30 days.

## Stage 3 rank

1. Excel/CSV leading-zero preservation converter
2. Canadian importer-report self-serve lookup
3. Environment-variable documentation checker
4. Canadian business-day API
5. Sponsor proof-of-delivery self-serve generator

## Advance to Stage 4

Advance the top three. They have the best combination of low build cost, clear self-serve value and a credible acquisition channel that does not require an owner to keep sending cold outreach.

## Verification record

- Last verified: 2026-10-16
- Stage 3 status: complete
