---
title: Revenue Investigation — Cross-Wave Master Ranking
summary: Decision-oriented ranking of the strongest opportunities after reconsidering all 300 ideas across five waves, with heavier weight on inbound/self-serve acquisition and low owner burden.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 230
permalink: /projects/notes/revenue-investigation-cross-wave-master-ranking/
tags: [revenue-investigation, research, master-ranking, validation, inbound, automation]
---

# Revenue Investigation — Cross-Wave Master Ranking

## Scope

All 300 original ideas from Waves 1–5 were reconsidered at a decision level using their prior stage outcomes plus a second-chance lens. Exact rank numbers are assigned only to the serious contenders because ranking weak Stage-1 ideas as, for example, #184 vs #185 would create false precision.

No Stage 5 build, payment setup, launch or customer outreach is authorized by this document.

## Current weighting

The user's newer preference for avoiding repeated lead chasing materially changes the scoring.

- customer pain / willingness to pay: 25%
- inbound or built-in distribution: 20%
- build/test simplicity: 15%
- automation / low owner burden: 15%
- revenue upside / repeat use: 10%
- competition / defensibility: 10%
- platform, legal and operational risk: 5%

Scores are comparative research scores, not measured market demand.

## Competition checks that changed the result

- Free browser tools now exist specifically for preserving leading zeros in CSV/Excel workflows, so the leading-zero utility remains attractive as a test but has a low pricing ceiling.
- Canada already has a free public holiday API and general business-day APIs, weakening the Canadian business-day API as a paid standalone product.
- QR equipment/manual/service workflows are now offered by several current field-service/asset products, reducing novelty of the QR handover idea.
- FormHeartbeat is a direct current product for end-to-end agency lead-form monitoring, weakening the mystery-enquiry/lead-path category.
- Shopify CSV preflight has multiple free browser-based implementations, substantially weakening that opportunity.
- Newsletter sponsor reporting has at least one direct current specialist, BannerTrackr, which confirms the problem while making differentiation important.
- Canadian importer search is becoming more competitive: current examples include hscode.ca, TariffPlus and broad paid trade-data providers. However, the official Canadian Importers Database remains current, open, structured and search-aligned, so a sharply scoped convenience product still merits testing.

## Master contender ranking

| Rank | Opportunity | Score /100 | Acquisition profile | Primary concern | Decision |
|---|---|---:|---|---|---|
| 1 | Canadian importer self-serve lookup | 76.0 | SEO/data pages/self-serve | Free government source + emerging competitors | **Validate first** |
| 2 | Excel/CSV leading-zero preservation converter | 74.5 | Search-driven/self-serve | Free substitutes cap willingness to pay | **Validate cheaply** |
| 3 | Sponsor proof-of-delivery generator | 74.0 | Creator search/product-led sharing | Direct specialist competition; low-end creator budgets | **Validate** |
| 4 | Product-spec contradiction checker | 74.0 | Shopify/app-store/content inbound possible | Needs deeper competition/product-boundary research | **Second-chance promote** |
| 5 | Product-manual metadata Apify Actor | 72.0 | Apify marketplace | Buyer demand not yet demonstrated | Research before build |
| 6 | GitHub environment-variable documentation checker | 71.5 | GitHub Marketplace/free Action | Free/open-source substitutes; monetization uncertain | Hold/cheap experiment |
| 7 | Vancouver/BC new-business signal feed for sign companies | 71.0 | Mostly outbound, later referrals | Requires initial prospecting; licence timing uncertainty | Strong business, weaker fit to new acquisition preference |
| 8 | Affiliate-link health checker | 71.0 | Search/plugin/inbound | Direct specialist tools already exist | Hold unless narrower wedge found |
| 9 | DIM-weight packaging diagnostic | 70.0 | Calculator/SEO → paid audit | Current free/paid optimization competitors; infrequent need | Hold |
| 10 | Public-PDF table extraction Apify Actor | 68.5 | Apify marketplace | Commodity extraction category | Hold |
| 11 | Canadian business-day API | 67.5 | Developer search/API directories | Strong free substitute | Drop as standalone paid API |
| 12 | Amazon SAFE-T workflow | 66.5 | Agency/service-provider sales | Amazon policy/platform dependence + outreach | Retain, do not prioritize |
| 13 | Shopify product-upload preflight | 66.5 | Search/App Store | Multiple current free tools | Drop unless materially narrowed |
| 14 | Mystery-enquiry response monitor | 66.0 | Agency direct sales | Direct current competitor + outbound acquisition | Hold |
| 15 | Installer QR equipment handover pages | 65.0 | Contractor sales/referrals | Crowded field-service/asset category | Hold |
| 16 | RFP requirement extractor | 63.5 | Search/self-serve possible | Crowded and trust-sensitive | Hold/drop |
| 17 | AI product-answer accuracy monitor | 63.0 | Brand outbound/agency channels | Fast-changing surfaces/platform terms | Watch, not first build |
| 18 | Commercial-laundry instant estimate widget | 62.5 | Direct operator sales | Customized pricing + outbound dependence | Hold |
| 19 | EDI-lite spreadsheet order translator | 62.0 | Direct B2B sales | High chance of becoming custom integration work | Drop for low-touch objective |

## What rose from the second-chance review

### Product-spec contradiction checker
This deserves re-entry despite not reaching the original Stage 4. The narrower product would compare factual product specifications across product pages, manuals and sales channels, then report exact conflicts with source citations. It has stronger potential willingness to pay than generic catalog-cleanup tools and can potentially use Shopify/app-store distribution. It still needs a proper current competitor check before Stage 4 treatment.

### Product-manual metadata Actor
This fits the user's newer acquisition preference unusually well because Apify itself can be the discovery/billing channel. The problem is not technical feasibility; it is whether enough users need repeated model/revision/document metadata extraction to produce meaningful paid usage. Validate marketplace search demand before building.

## Top three validation portfolio

### Test 1 — Canadian importer self-serve lookup

**Why first:** highest balance of useful data, search-aligned acquisition, automation and plausible one-off payments.

Proposed validation, not yet authorized to build:

1. Select 10 product/HS categories with meaningful importer counts.
2. Create factual preview pages from the September 2026 Canadian Importers Database release.
3. Show only a small preview and the exact source/year.
4. Offer a CA$15 cleaned XLSX/CSV report or an interest/preorder action.
5. Measure visits, preview-to-purchase intent and which category pages attract search impressions.

**Go:** 3 paid report purchases from 50 qualified visits, with at least 2 originating without direct outreach.

**Budget:** roughly CA$0–$60 using existing infrastructure.

### Test 2 — Leading-zero preservation converter

**Why second:** fastest and cheapest way to test whether a search-shaped data problem can monetize without sales effort.

Proposed validation:

1. One browser-only CSV/XLSX tool.
2. Detect risky identifier columns and preview exact before/after output.
3. Free small conversion; CA$9 large/batch conversion.
4. Build specific search pages for HS codes, SKUs, account IDs and other identifiers.

**Go:** 10 completed exports and 2 paid conversions from the first 100 qualified sessions.

**Budget:** approximately CA$0–$40.

**Important:** current free substitutes mean this is a fast experiment, not something to overbuild.

### Test 3 — Sponsor proof-of-delivery generator

**Why third:** the underlying problem is proven enough that a specialist current competitor exists, and publishers can understand the output instantly. A simpler product can target low-volume publishers that do not need a full ad-tracking platform.

Proposed validation:

1. Self-serve issue URL + sponsor name + publisher-supplied metrics.
2. Generate factual placement evidence and one clean PDF/share page.
3. First report free; test CA$12/report and CA$29/month.
4. Allow a small product attribution link on free reports for product-led discovery.

**Go:** 30 organically generated reports and 3 paying/repeat publishers in 30 days.

**Budget:** approximately CA$0–$75.

## Recommended sequence

Do not build all three at once.

1. Run the **importer lookup validation** first because it has the best current composite score and the 2024 source dataset was only published in September 2026.
2. If it fails its go threshold, run the **leading-zero converter** because it is extremely cheap to test.
3. If both fail or cap out at trivial economics, test the **sponsor report generator**.
4. Keep **product-spec contradiction checker** as the best second-chance candidate for another Stage 3 investigation before development.

## Current source checks

- Canadian Importers Database: https://ised-isde.canada.ca/site/ised/en/research-and-business-intelligence/canadian-importers-database
- Open Government CID 2024 release: https://open.canada.ca/data/en/dataset/e5eae1d4-687c-4db2-9273-a8d2d711144c
- Microsoft Excel leading-zero guidance: https://support.microsoft.com/en-us/excel/format-numbers-to-keep-leading-zeros-in-excel-for-the-web
- Current free leading-zero examples: https://www.exceltutorial.net/leading-zero-preserver/ and https://sheetreserve.com/spreadsheet-tools/csv-leading-zeros
- BannerTrackr: https://bannertrackr.com/
- Current QR-equipment competition examples: https://tradeify.app/for-hvac and https://scanmyequipment.com/
- FormHeartbeat: https://formheartbeat.com/
- Canada Holidays API: https://canada-holidays.ca/api
- Current Shopify CSV-preflight examples: https://merchpreflight.com/ and https://tools.tnaado.ca/creator/shopify-product-csv-preflight/
- Current Canadian importer/search competition examples: https://hscode.ca/en/about/ and https://tariffplus.com/importers/ca/

## Approval gate

This ranking completes the cross-wave decision step. It does **not** authorize Stage 5.

If Stage 5 is approved, the recommended first project is the smallest possible importer-lookup validation artifact, not a full SaaS application.
