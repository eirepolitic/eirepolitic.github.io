---
title: Revenue Investigation — Stage 3 Deep Investigation
summary: Deep investigation of the five Stage 2 survivors, including current competitors, pricing, demand evidence, acquisition, operating burden, risks, failure modes and minimum viable tests.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 212
permalink: /projects/notes/revenue-investigation-stage-3-deep-investigation/
tags:
  - revenue-investigation
  - research
  - online-business
  - automation
  - ai-agents
---

# Revenue Investigation — Stage 3 Deep Investigation

## Decision summary

Stage 3 investigated the five business directions that survived Stage 2. Two should advance to concrete implementation planning, one should be retained as a distribution mechanism, and two should be stopped for now.

| Direction | Stage 3 decision | Why |
|---|---|---|
| **Open-data intelligence product** | **ADVANCE** | Strong automation fit, legally reusable source material exists, low infrastructure cost, and comparable data-intelligence products prove businesses pay for useful data packaging. The specific dataset/niche still needs selection. |
| **Niche embeddable calculator / micro-tool** | **ADVANCE** | Businesses already pay for calculators and lead-capture tools. A single narrow tool can be built and licensed repeatedly. Generic calculator builders are crowded, so niche selection is the main problem. |
| **Paid Apify Actor** | **RETAIN AS CHANNEL** | Real low-touch marketplace with usage-based billing and demonstrated creator revenue, but 89,000+ Actors means “build an Actor” is not itself a market. Use Apify only if a specific unmet automation is found. |
| **Tender/RFP filtering service** | **STOP FOR NOW** | The proposed differentiation already exists in Canada at about CA$50/month, alongside mature procurement platforms. A much narrower vertical would need separate evidence. |
| **Standalone spreadsheet pack** | **STOP AS BUSINESS; RETAIN AS MVP FORMAT** | Very cheap and fast to create, but generic business calculators/templates are heavily commoditized. Better used to prototype a future micro-tool before software is built. |

The strongest overall fit with the project objective is therefore **(1) a deliberately narrow data/intelligence product and (2) a deliberately narrow embeddable business tool**.

---

## 1. Open-data intelligence product — ADVANCE

### Plain-English description

Take information that governments already publish, clean it up, combine it, and package it around a specific business decision.

The customer is **not paying for secret data**. They are paying to avoid finding, understanding, filtering and repeatedly processing awkward source files themselves.

### Evidence of usable raw material

**Fact:** Canada's Open Government Licence explicitly permits commercial use, copying, modifying, publishing and redistribution, with attribution and stated exceptions such as personal information and third-party rights.

Source: https://open.canada.ca/en/open-government-licence-canada

**Fact:** the federal Open Government Portal currently exposes tens of thousands of datasets under open licences.

Source: https://search.open.canada.ca/opendata/

**Fact:** the City of Vancouver's current business-licence dataset is updated daily and includes fields such as business name, business type, status, issue date, address where publishable, employee count and licence fee. It is licensed under the Open Government Licence – Vancouver.

Source: https://opendata.vancouver.ca/explore/dataset/business-licences/

**Fact:** the federal Canadian Importers Database provides lists of companies importing goods into Canada by product, city and source country. The 2024 files were published in September 2026 under the Open Government Licence – Canada.

Sources:
- https://ised-isde.canada.ca/site/ised/en/research-and-business-intelligence/canadian-importers-database
- https://open.canada.ca/data/en/dataset/e5eae1d4-687c-4db2-9273-a8d2d711144c

### Important finding: generic permit leads are already crowded

The Stage 2 example of building-permit leads is **not recommended as the first product**.

Current competitors include:

- PermitProspect, beginning around CA$49/month;
- PermitPulse, with plans around CA$79–$399/month;
- SiteWire, covering permit activity across dozens of Canadian cities;
- Van Permit Audit, offering simple trade/city permit feeds at CA$97/month; and
- at least one recently published Apify Actor selling Vancouver permit/new-business leads for $5 per 1,000 records.

Sources:
- https://permitprospect.ca/
- https://www.permitpulse.ca/
- https://www.sitewire.ca/
- https://www.vanpermitaudit.ca/leads
- https://apify.com/canada-dd/vancouver-building-permits-leads

**Conclusion:** this is good evidence that businesses pay for cleaned public data, but poor evidence for entering the generic Canadian permit-lead market now.

### More promising product shapes

#### Option A — Canadian importer / market-entry report

**What it is:** a customer chooses a product category and receives a clean report showing major Canadian importers, locations, source countries, market concentration and selected trends.

**Likely customer:** overseas manufacturers/exporters, Canadian suppliers, freight/logistics companies, consultants and market-entry firms.

**Why they might pay:** the government source is free but requires knowing product classification codes and working through awkward tables/files. A finished business-oriented report is easier to buy and use.

**Demand proxy:** commercial global trade-intelligence products charge meaningful amounts. Volza lists plans from roughly US$1,500/year and ImportGenius pricing reported by G2 begins around US$125/month on annual billing. These products provide much richer data than the proposed MVP, so they validate the category—not our proposed price.

Sources:
- https://www.volza.com/pricing/
- https://www.g2.com/products/importgenius/pricing

**Estimated MVP pricing (not validated):** CA$29–$99 for a pre-built narrow report; CA$99–$299 for a self-service/custom generated report. The lower price reflects the fact that the underlying Canadian dataset is free and annual rather than shipment-level.

**Automation:** very high. Download source data → normalize product codes → generate tables/charts → generate plain-English notes → export PDF/CSV → payment/delivery.

**Ongoing burden:** low if sold as annual reports; moderate if contact enrichment and frequent updates are added.

**Main risks:** buyers may simply use the government source; annual data may be too stale for prospecting; product classification is confusing; free global competitors may satisfy many users.

**Minimum viable test:** create three polished sample reports for real product categories and a simple purchase/waitlist page. Do **not** build a full application first. Measure whether prospects request/download samples or purchase a report.

#### Option B — new-business/opening signal feed

**What it is:** a small, filtered recurring feed of newly issued business licences or other official opening/expansion signals for one type of B2B seller.

**Example:** each week, a signage/POS/security/waste-services company receives newly licensed relevant businesses in its territory rather than searching city records itself.

**Evidence:** Vancouver's current licence dataset is updated daily and contains enough structured business fields to support this type of feed.

Source: https://opendata.vancouver.ca/explore/dataset/business-licences/

**Estimated pricing (not validated):** CA$39–$99/month for one territory/use case if the records reliably produce sales opportunities.

**Automation:** very high after setup: collect daily changes → filter by target type → de-duplicate → score → email/export.

**Ongoing burden:** low technically; moderate data-source maintenance as additional municipalities are added.

**Main risks:** a single city may be too small; some addresses are intentionally withheld; customers may demand contact enrichment; outreach use raises anti-spam/compliance questions.

**Compliance note:** CASL requires senders of commercial electronic messages to have a valid consent basis, identify themselves and provide unsubscribe functionality. Public availability of an email address alone is not automatically sufficient. A data product should therefore avoid promising that records are automatically lawful cold-email targets.

Sources:
- https://crtc.gc.ca/eng/com500/guide.htm
- https://crtc.gc.ca/eng/com500/faq500.htm

**Minimum viable test:** manually generate one week's feed for one city and one buyer type. Show the sample to 10–20 potential customers and ask for a paid pilot before building a multi-city pipeline.

### Customer acquisition

This remains the largest uncertainty.

Plausible low-capital channels:

- search pages targeting very specific queries such as Canadian importers for a product category;
- a free sample report that leads to paid full reports;
- partnerships with export consultants, freight forwarders or agencies;
- carefully compliant targeted outreach during validation;
- marketplaces/API channels only after a product proves useful.

### Likely failure modes

1. The source is free and customers see too little added value.
2. The chosen dataset updates too slowly to drive recurring subscriptions.
3. Data cleaning is easy but customer acquisition is expensive.
4. The product becomes an enrichment/contact-data business, increasing cost and legal risk.
5. A government schema or portal changes and requires maintenance.

### Stage 3 judgment

**Advance to Stage 4.** The strongest first implementation plan should compare the two MVPs above: **importer/market-entry reports** versus a **narrow new-business signal feed**. No large dashboard should be built before one of those tests shows demand.

---

## 2. Niche embeddable calculator / micro-tool — ADVANCE

### Plain-English description

Build one small calculator or estimator that a business can place on its website under its own branding.

The customer pays because the tool saves staff time, gives website visitors an immediate answer, or turns visitors into better sales enquiries.

### Market evidence

**Fact:** generic calculator/lead-capture platforms already charge recurring subscriptions. LeadsCalc lists a free tier and paid plans around US$15 and US$39/month on annual billing.

Source: https://www.leadscalc.com/pricing

**Fact:** specialized contractor calculator products charge materially more. TradeCalcs lists contractor-focused hosted tools around US$99/month, US$249/month and an agency tier around US$799/month.

Source: https://tradecalcs.com/

**Fact:** there are also newer generic embed builders such as Estimatly, reinforcing that the horizontal “calculator builder” itself is already competitive.

Source: https://www.estimatlyapp.com/

### Niches explicitly rejected for the first test

Current search evidence shows many live calculators already exist for:

- general contractors/remodelling;
- commercial cleaning; and
- managed IT services.

Examples:
- https://tradecalcs.com/
- https://servicemarginlab.com/tools/commercial-cleaning-quote-profit-calculator
- https://revotech-networks.com/pricing/

These niches may still support a differentiated tool, but they are **not** attractive first choices for a three-day sprint.

### What the viable version needs

The product should solve a calculation that is:

1. tied closely to money (price, savings, margin, eligibility, quantity or ROI);
2. repeated often by businesses;
3. explainable with a small number of inputs;
4. valuable enough that a lead or saved staff hour matters; and
5. specific enough that generic form builders are inconvenient.

Examples of *shapes* to investigate in Stage 4—not recommendations yet:

- industry-specific quote estimator;
- savings/ROI calculator for a specialized B2B service;
- capacity/quantity calculator that converts directly into a sales enquiry;
- eligibility/pre-qualification calculator;
- margin/pricing calculator sold internally to small firms rather than embedded publicly.

### Pricing model

**Market fact:** comparable generic tools span from low double-digit monthly prices to hundreds per month when specialized, managed or agency-oriented.

**Estimated starting model (not validated):** CA$19–$49/month self-service, or CA$99–$299 one-time setup plus CA$19–$79/month for a niche product. Another option is one-time licensing for a simple static widget.

### Customer acquisition

Likely channels:

- direct outreach to businesses in one narrowly defined industry;
- partnerships with web-design/marketing agencies serving that industry;
- SEO around the calculation itself, with a free demo visible before purchase;
- niche associations/directories once proof exists.

The agency route may be particularly attractive because one agency can reuse a licensed tool across multiple clients, reducing the number of relationships needed.

### Implementation complexity

Low to moderate.

A basic version only needs:

- inputs;
- calculation rules;
- branded result;
- optional lead form;
- an embed code;
- simple configuration; and
- payment/licensing.

AI is useful for setup assistance, copying rules from a customer's existing spreadsheet, generating explanations and support documentation. The actual price calculation should remain deterministic rather than letting an LLM invent numbers.

### Ongoing operating burden

Potentially low if:

- calculations are customer-configurable;
- no regulated advice is given;
- there are few external integrations; and
- the tool does not promise exact final quotes where a site inspection is required.

### Likely failure modes

1. We choose a niche that already has excellent free calculators.
2. Buyers see the tool as a website feature worth $10, not a business product worth $50+.
3. Every customer wants custom logic, turning software into consulting.
4. Wrong estimates create customer disputes.
5. Acquisition requires continuous sales calls, violating the low-touch objective.

### Minimum viable test

Before building a platform:

1. choose one narrow business type;
2. build one working demo calculator;
3. create a simple landing page showing the result and proposed price;
4. approach 20–30 likely buyers or 5–10 agencies serving that niche;
5. require at least a small number of paid pilots or strong purchase intent before adding multi-tenant features.

### Stage 3 judgment

**Advance to Stage 4.** Stage 4 should first select the niche using evidence, then plan only the single-tool MVP. Do not build a generic calculator platform.

---

## 3. Paid Apify Actor — RETAIN AS CHANNEL, NOT PRIMARY BUSINESS

### Plain-English description

Apify is an online marketplace where developers publish small automated programs (“Actors”). Customers run them and can pay based on usage. Apify handles hosting and billing.

### Evidence

**Fact:** Apify currently lists roughly 89,000 Actors. Major categories are extremely crowded; its developer-tools category alone lists over 24,000 Actors.

Sources:
- https://apify.com/store
- https://apify.com/store/categories/developer-tools

**Fact:** top Actors demonstrate substantial usage. For example, Apify's Website Content Crawler reports well over 100,000 total users and thousands of monthly active users.

Source: https://apify.com/apify/website-content-crawler

**Fact:** Apify's current pay-per-event model pays creators according to the published formula `80% of revenue - platform costs`, with Apify handling billing and payouts.

Sources:
- https://docs.apify.com/actors/publishing/monetize
- https://help.apify.com/en/articles/12800725-ship-your-actor-and-get-paid

**Fact:** Apify states that some independent creators earn more than US$1,000/month and its most successful independent creators exceed US$10,000 monthly recurring revenue. This is platform-reported, not independently verified.

Source: https://help.apify.com/en/articles/8684010-make-money-publishing-your-actors-on-apify-store

### Market problem

The marketplace proves revenue is possible but does **not** tell us what to build. Generic social-media, Google Maps, website-crawling and common e-commerce scraping categories already have very large incumbents.

### Better role in this project

Treat Apify as a **distribution and billing channel** for a product discovered elsewhere.

Possible example: if the importer/open-data research produces a useful automated lookup/transform, publish an Actor/API version after validating the underlying user need.

### Minimum viable test

Search Apify for a very specific task only after Stage 4 chooses a problem. Compare existing Actors by users, reviews, recency and price. Build only if the task has observable demand and weak existing implementations.

### Stage 3 judgment

**Do not advance as a standalone implementation plan.** Keep it available as a deployment channel for the open-data or automation product.

---

## 4. Tender/RFP filtering — STOP FOR NOW

### Plain-English description

Monitor procurement websites and email each customer only the contracts that match its business.

### Evidence that changed the decision

**Fact:** CanadaBuys already provides searchable federal opportunities and allows users to create email notifications for searches.

Source: https://canadabuys.canada.ca/en/tender-opportunities

**Fact:** MERX currently offers Canadian tender subscriptions from roughly CA$30/month for one province on annual billing through CA$80/month for national coverage on annual billing; monthly pricing is higher.

Source: https://www.merx.com/public/pricing

**Fact:** bids&tenders offers supplier subscriptions and daily opportunity notifications, with plans currently listed from CA$549/year to CA$1,999/year depending on agency coverage.

Source: https://bidsandtenders.com/suppliers-plans/

**Most important fact:** TenderBridge already offers essentially the Stage 2 differentiated concept: monitoring 180+ Canadian sources, AI relevance scoring, daily matched emails and bid/no-bid analysis for CA$49.99/month (CA$39.99/month annually).

Sources:
- https://tenderbridge.ca/
- https://tenderbridge.ca/bc-tenders/

### Revenue model

The existing market demonstrates willingness to pay from roughly tens to hundreds of dollars per month. The problem is not monetization; it is differentiation.

### Customer acquisition and burden

A new entrant would need to convince suppliers to switch from free government alerts or established tender platforms. Maintaining 100+ sources also creates ongoing parser/source-change work.

### Likely failure modes

1. Existing services already provide adequate matching.
2. Source ingestion becomes a maintenance treadmill.
3. Buyers need bid-writing/workflow features, expanding scope.
4. Acquisition cost overwhelms a CA$40–$50/month subscription.

### Minimum viable test if revisited

Do not build a broad service. Select one narrow profession and manually produce a one-week “only opportunities you can actually bid on” digest. Proceed only if existing tools demonstrably fail that group.

### Stage 3 judgment

**Stop for now.** Evidence is not strong enough to justify competing directly with a product that already implements our Stage 2 thesis.

---

## 5. Spreadsheet/model pack — STOP AS STANDALONE BUSINESS

### Plain-English description

Sell a ready-made spreadsheet that performs one useful calculation or workflow.

### Evidence

**Fact:** Etsy currently shows more than 5,000 results for pricing-calculator spreadsheets, with many visible listings priced around US$1–$15 and established listings showing thousands of reviews/sales signals.

Source: https://www.etsy.com/market/pricing_calculator_spreadsheet

This makes the generic small-business calculator/template market strongly commoditized.

### Where it remains useful

A spreadsheet is an excellent **prototype format**.

For example, before building an embeddable pricing calculator, build the calculation in a spreadsheet and test it with real users. If nobody will pay for the spreadsheet or the output it creates, software is unlikely to fix the underlying demand problem.

### Minimum viable test

When Stage 4 selects a micro-tool niche, create the calculation logic as a spreadsheet first and test the outputs with potential buyers. Do not launch a broad spreadsheet-template store as the primary business.

### Stage 3 judgment

**Stop as an independent business direction; retain as a cheap validation tool.**

---

## Cross-cutting findings

### The hard part is distribution, not code

Across the surviving ideas, the technical MVP is inexpensive. The biggest commercial uncertainty is finding customers cheaply enough.

This is why Stage 4 should avoid “build first” plans. Each plan must begin with a demand test and a clear route to the first 5–10 paying customers.

### AI should reduce labour, not invent facts

Good uses of AI here include:

- classifying/filtering records;
- summarizing official source material;
- generating draft reports;
- producing documentation/support answers;
- matching products or businesses to categories; and
- detecting unusual records for review.

Critical numerical calculations, source licensing, final customer-facing factual claims and compliance rules should be deterministic or source-backed.

### Low-touch does not mean no legal/platform obligations

Open licences still require attribution and exclude certain rights/personal information. Commercial email in Canada remains subject to CASL. Scraping products may also inherit target-site terms and blocking risk. These constraints need to be designed around rather than assumed away.

---

## Recommended Stage 4 implementation-plan candidates

### Candidate A — Canadian importer / market-entry report MVP

**Goal:** test whether businesses will pay for a simple, polished decision product built from official Canadian importer/open trade data.

**First test:** 3 sample product-category reports + landing page + payment/waitlist; no dashboard.

**Why first:** extremely low capital, legally straightforward source material, almost fully automatable, and no recurring operational promise is required initially.

### Candidate B — new-business signal feed MVP

**Goal:** test whether a very specific B2B seller will pay to receive newly relevant local businesses from official licensing/opening data.

**First test:** one city + one customer type + one weekly manually reviewed feed.

**Why second:** stronger recurring-revenue potential than static reports, but greater data-maintenance and customer-acquisition burden.

### Candidate C — one niche embeddable calculator

**Goal:** find one business calculation where a website visitor's answer is commercially valuable enough to justify a recurring licence.

**First test:** select niche → spreadsheet logic → single web demo → paid-pilot outreach. No generic platform.

**Why third:** attractive recurring economics and low marginal operating burden if the niche is right, but niche selection remains unvalidated.

### Apify

Use only as an optional publication/billing channel for a validated automation from Candidates A/B/C; do not create an Actor merely to have an Actor product.

---

## Stage 4 gate

Before any significant development, Stage 4 should produce implementation plans for Candidates A, B and C containing:

- exact proposed customer;
- exact product/output;
- first acquisition channel;
- MVP scope;
- estimated out-of-pocket cost;
- build steps;
- automation architecture;
- measurement/kill criteria; and
- legal/platform checks.

The implementation plans should then be presented for approval before Stage 5 development begins.

## Verification record

- Last verified: `2026-10-16`
- Verified by: High Director
- Current-source areas checked: Canadian open-data licensing and datasets; Vancouver open data; Canadian permit-data competitors; Canadian procurement/tender competitors; Apify marketplace/monetization; calculator/estimator products; spreadsheet marketplaces; Canadian anti-spam guidance; trade-intelligence pricing.
- Facts, assumptions and estimates are separated throughout this note.
- Not yet validated: willingness to pay for the exact importer report, business-opening feed or chosen calculator niche; customer acquisition cost; conversion rate; actual revenue; precise Stage 4 product pricing.
