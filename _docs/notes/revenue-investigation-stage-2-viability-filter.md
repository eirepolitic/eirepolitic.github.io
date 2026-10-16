---
title: Revenue Investigation — Stage 2 Viability Filter
summary: Evidence-based filtering of the Stage 1 online-business pool, with scores, eliminations and the recommended Stage 3 shortlist.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 211
permalink: /projects/notes/revenue-investigation-stage-2-viability-filter/
tags:
  - revenue-investigation
  - research
  - online-business
  - automation
  - ai-agents
---

# Revenue Investigation — Stage 2 Viability Filter

## Purpose

Stage 2 filters the 15 candidates advanced from Stage 1. This is still a screening exercise, not full market validation. The goal is to reject models that conflict with the low-touch/low-capital objective or that already show obvious competitive, legal, platform, or operating disadvantages.

Source pool: [`revenue-investigation-stage-1-idea-pool.md`](/projects/notes/revenue-investigation-stage-1-idea-pool/)

## Scoring method

Each candidate receives an **estimate from 1 to 5** on six dimensions. A higher score is better.

- **Startup cost:** 5 = minimal outside spend; 1 = substantial capital/data/tool spend.
- **Time to first revenue:** 5 = plausible to test/sell in days; 1 = long build or market-creation cycle.
- **Ongoing human effort:** 5 = can operate with little routine intervention; 1 = requires frequent manual work/sales/service.
- **Automation potential:** 5 = most delivery and operations can be automated; 1 = automation contributes little.
- **Legal/platform risk:** 5 = comparatively low; 1 = material data, scraping, privacy, liability or platform dependency.
- **Expected upside:** 5 = plausible meaningful recurring revenue if a niche is found; 1 = structurally low ceiling.

The scores are **estimates**, not facts. Current external evidence is used to identify enabling infrastructure, incumbent pricing, market crowding and obvious constraints.

## Current evidence that materially changed the filter

### Facts

1. **A simple Canadian tender-alert product is not enough.** CanadaBuys already lets users search tenders, create email notifications and access procurement/contracting data. A commercial product would need to add cross-source coverage, niche matching, prioritization, summaries or workflow—not merely send alerts. Source: [CanadaBuys tender opportunities](https://canadabuys.canada.ca/en/tender-opportunities).
2. **Public data is unusually attractive as raw material.** Canada's Open Government Licence permits commercial reuse, modification and redistribution with attribution, subject to stated exceptions. The federal Open Government Portal currently exposes more than 48,000 records. Sources: [Open Government Licence — Canada](https://open.canada.ca/en/open-government-licence-canada), [Open Government Portal](https://search.open.canada.ca/opendata/).
3. **Generic price monitoring is already a mature paid category.** Prisync advertises competitor price/stock monitoring starting at $99/month for up to 100 products. Source: [Prisync price intelligence](https://prisync.com/price-intelligence-software/).
4. **Generic website/change monitoring is inexpensive and feature-rich.** Visualping starts free and lists paid personal plans from $14/month; ChangeTower lists paid plans from $12/month; Little Warden lists automated technical checks from £24.99/month. Sources: [Visualping pricing](https://visualping.io/pricing), [ChangeTower](https://changetower.com/), [Little Warden pricing](https://littlewarden.com/pricing).
5. **Sales-signal products already have strong incumbents.** Apollo includes buying-intent features and starts its paid Basic plan at $49/user/month when billed annually. Sources: [Apollo pricing](https://www.apollo.io/pricing), [Apollo Buying Intent](https://knowledge.apollo.io/hc/en-us/articles/8047704465933-Buying-Intent-Overview).
6. **Notion templates have very low entry cost but heavy supply.** Notion's marketplace search currently advertises 70,000+ templates, with major categories containing thousands to tens of thousands of entries. Direct Marketplace selling also requires creator/payment approval, which Notion says may take a few months. Sources: [Notion Marketplace](https://www.notion.com/templates), [Selling templates on Marketplace](https://www.notion.com/help/selling-on-marketplace).
7. **Apify provides a real low-touch distribution/monetization channel, but it is crowded.** Apify allows paid Actors using pay-per-event monetization and currently lists more than 88,000 Actors. Apify documents creator profit as 80% of pay-per-event revenue minus underlying platform costs. Sources: [Apify Store](https://apify.com/store/categories), [Monetize Actors](https://docs.apify.com/actors/publishing/monetize), [Actor pricing and costs](https://docs.apify.com/actors/publishing/monetize/pricing-and-costs).
8. **Businesses demonstrably pay for embeddable calculators/forms.** Outgrow sells calculator/form software from low double-digit monthly prices through enterprise tiers; involve.me sells calculator/quote tooling starting at $29/month when billed annually and states that more than 4,500 businesses use its quote calculator tooling daily. Sources: [Outgrow pricing](https://outgrow.co/pricing/), [involve.me pricing](https://www.involve.me/pricing), [involve.me price quote calculator](https://www.involve.me/price-quote-calculator).
9. **Paid information products have inexpensive distribution.** Substack charges 10% of paid-subscription revenue plus payment-processing fees, while beehiiv reports paid-subscription revenue on its platform reached $19 million in 2025. Sources: [Substack pricing](https://support.substack.com/hc/en-us/articles/360037607131-How-much-does-Substack-cost), [beehiiv State of Paid Newsletters 2026](https://www.beehiiv.com/blog/the-state-of-paid-newsletters-2026).

### Assumptions and estimates

- Customer acquisition is likely to be harder than building the product for most candidates.
- Narrow B2B products should generally have better revenue economics than broad consumer products, but this has not yet been verified for a specific niche.
- Data products built only from clearly reusable/open data should have materially lower legal/platform risk than products dependent on scraping protected commercial websites.
- A small digital product can reach first revenue faster than SaaS, but its likely revenue ceiling is lower unless it becomes a portfolio or funnel into higher-value products.

## Scorecard

| Candidate | Cost | First revenue | Low human effort | Automation | Low risk | Upside | Total /30 | Stage 2 decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **A1 Operational spreadsheet/model packs** | 5 | 5 | 5 | 4 | 5 | 2 | **26** | Advance as fast-test option |
| **E1 Cleaned public-data feed** | 5 | 3 | 4 | 5 | 5 | 4 | **26** | **Advance** |
| **C3 Tender/RFP alert service** | 4 | 4 | 4 | 5 | 4 | 4 | **25** | **Advance, but only differentiated version** |
| **K1 Paid Apify Actor** | 5 | 5 | 4 | 5 | 3 | 3 | **25** | **Advance** |
| **L4 White-label micro-tool licensing** | 4 | 4 | 4 | 5 | 4 | 4 | **25** | **Advance** |
| **E5 Permit/property/business-activity dataset** | 4 | 3 | 4 | 5 | 4 | 4 | **24** | **Advance; investigate with E1** |
| B2 Data-backed market brief | 5 | 4 | 3 | 4 | 4 | 3 | 23 | Keep as validation/product format, not separate priority |
| A2 Notion/knowledge-work systems | 5 | 3 | 5 | 4 | 4 | 2 | 23 | Do not deep-dive now; crowded |
| I2 Competitor/change monitor | 5 | 4 | 4 | 5 | 3 | 2 | 23 | Reject generic version; cheap incumbents |
| F2 Website QA/content-drift report | 5 | 4 | 4 | 5 | 4 | 2 | 24 | Reject generic version; mature low-cost tools already cover much of value |
| C5 Trigger-event prospecting alerts | 3 | 3 | 3 | 5 | 2 | 5 | 21 | Reject for now; data/privacy/acquisition burden |
| E3 Regulation/filing change feed | 4 | 3 | 3 | 5 | 2 | 4 | 21 | Reject for now; accuracy/liability burden |
| E2 Competitor price/availability feed | 3 | 3 | 3 | 5 | 2 | 4 | 20 | Reject; mature market plus scraping/maintenance risk |
| I1 Compliance/renewal deadline tracker | 4 | 3 | 3 | 4 | 2 | 4 | 20 | Reject for now; rule maintenance/liability conflicts with low-touch goal |
| H1 Niche vendor directory | 4 | 2 | 2 | 4 | 4 | 4 | 20 | Reject for now; two-sided acquisition creates too much human work |

## Recommended Stage 3 shortlist

### 1. E1 + E5 — Commercial product built from open public data

**Plain-English version:** take information the government publishes for free, clean it up, combine it and deliver it in a form businesses can actually use.

Example: instead of making a contractor search multiple government sites for new permits or business licences, send a clean weekly list of newly relevant projects/leads in their area.

Why it advances: low source cost, strong automation fit and comparatively favorable licensing when using data covered by an open-government licence.

Stage 3 question: **which specific dataset creates enough business value that somebody will pay for the cleaned/combined version?**

### 2. C3 — Highly filtered tender/RFP opportunity service

**Plain-English version:** monitor government/business contract opportunities and tell a specific type of company only about the few opportunities that actually fit them.

Example: a weekly email for a specific trade that says, "these 6 public contracts are relevant to your company; here is the deadline, estimated fit and why it matches."

Why it advances: clear business value and high automation potential.

Critical caveat: free tender alerts already exist. Stage 3 must prove value beyond free notifications—likely cross-portal aggregation, niche filtering and useful summaries.

### 3. K1 — Paid Apify Actor

**Plain-English version:** publish a small online robot in an existing marketplace. Customers pay when they run it to collect or transform information.

Example: a tool that takes a public directory or website and returns a clean spreadsheet in a specific format.

Why it advances: almost no sales administration is required once listed, and the marketplace handles usage-based charging.

Critical caveat: the marketplace already has more than 88,000 Actors, so Stage 3 must find an underserved task rather than build another generic scraper.

### 4. L4 — Niche white-label micro-tool

**Plain-English version:** build one small useful calculator or form that many businesses can put on their own websites under their own brand.

Example: an instant price estimator for one trade or service where customers currently have to phone/email for a rough quote.

Why it advances: businesses already pay for calculator/form tools, and one well-chosen niche tool could be sold repeatedly with automated setup.

Critical caveat: generic calculator builders are mature. The opportunity has to come from solving a specific industry's problem better, not from building another general calculator platform.

### 5. A1 — Operational spreadsheet/model pack

**Plain-English version:** sell a ready-made spreadsheet that does a useful job for a narrow type of customer.

Example: a quoting/profit calculator for a particular service business.

Why it advances: cheapest and fastest candidate to test, little support is required, and it could validate a problem before building software.

Critical caveat: likely lower revenue ceiling and difficult discoverability unless the niche/problem is unusually specific.

## Candidates removed from the immediate path

### Rejected because existing generic tools are already cheap/strong

- E2 competitor price monitoring;
- F2 generic website QA/content monitoring; and
- I2 generic competitor/change monitoring.

These are technically easy but would require strong niche differentiation to avoid competing directly with mature low-cost products.

### Rejected because they conflict with the low-touch objective

- H1 niche vendor directory: requires building both supplier and buyer sides;
- C5 sales-trigger alerts: likely requires expensive data/enrichment plus careful privacy/outreach handling;
- I1 compliance tracker and E3 regulatory feed: accuracy expectations and liability create ongoing review burden.

### Deprioritized rather than rejected

- A2 Notion templates: very low cost but extreme marketplace crowding and possible approval delay;
- B2 data-backed market brief: useful as a **test format** for E1/E5. Before building a data platform, a paid report or email can test whether anyone actually values the information.

## Recommended Stage 3 order

1. **Open-data product (E1/E5 combined)** — highest strategic fit; first identify 3–5 concrete datasets/niches.
2. **Paid Apify Actor (K1)** — inspect marketplace demand/competition and identify underserved tasks using public marketplace metrics.
3. **White-label niche micro-tool (L4)** — identify industries where an instant calculator/estimator has obvious monetary value.
4. **Tender/RFP filtering (C3)** — test whether narrow aggregation/filtering beats the free government alert experience.
5. **Spreadsheet pack (A1)** — use as the simplest, cheapest fast test and possibly as an MVP for the micro-tool concept.

Stage 3 should investigate these concepts with actual competitors, customer/problem evidence, pricing, acquisition routes, implementation burden, likely failure modes and a minimum viable test. No significant development should begin before the resulting evidence and implementation recommendation are presented for approval.

## Verification record

- Last verified: `2026-10-16`
- Verified by: High Director
- Verification scope: current platform pricing/features, open-data licensing/availability, marketplace crowding and obvious incumbent alternatives used for Stage 2 filtering.
- Not yet verified: demand for a specific open dataset, niche, tender vertical, Apify task, calculator niche or spreadsheet product; realistic customer acquisition cost; conversion; revenue; jurisdiction-specific legal advice.
