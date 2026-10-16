---
title: Revenue Investigation — Stage 4 Implementation Plans
summary: Concrete low-capital implementation and customer-acquisition plans for the three Stage 3 survivors, with explicit approval gate before significant development.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 213
permalink: /projects/notes/revenue-investigation-stage-4-implementation-plans/
tags:
  - revenue-investigation
  - research
  - online-business
  - automation
  - ai-agents
---

# Revenue Investigation — Stage 4 Implementation Plans

## Decision summary

Stage 4 converts the three surviving concepts into testable implementation plans. No significant product development is authorized yet.

Recommended order:

1. **New-business signal feed for sign companies** — best combination of recurring revenue, simple data source, clearly identifiable buyers and highly automatable sales validation.
2. **Canadian importer intelligence packs** — cheapest product to create and deliver, with a strong legal/open-data foundation; demand and repeat purchase remain less certain.
3. **Commercial-laundry instant estimate widget** — attractive recurring software model with a large identifiable prospect pool, but requires more product work and pricing customization.

The acquisition design for all three is deliberately **semi-automated rather than high-volume blind cold email**. Automation should remove research, scoring, drafting, follow-up and inbox sorting; the owner should only handle qualified interest.

---

# Common customer-acquisition system

## Objective

Build one reusable acquisition pipeline that can support any of the three products.

### Pipeline

`public/industry prospect source → company website → automated fit scoring → contact/compliance evidence → AI-personalized draft → controlled send queue → follow-up → reply classification → owner handoff`

### What is automated

- importing prospect/company lists from permitted public directories;
- visiting company websites and extracting business/service information;
- detecting whether the site already has the product feature we are proposing;
- scoring likely fit;
- preparing a short personalized reason for contact;
- preparing a sample/report/link specific to the prospect where possible;
- maintaining follow-up dates;
- classifying replies;
- maintaining unsubscribe/suppression records; and
- reporting funnel metrics.

### What requires human review

- first outreach batch for any new segment;
- ambiguous consent/contact situations;
- unusual factual claims created by AI;
- pricing negotiations;
- interested prospects; and
- complaints or legal/platform issues.

### Canadian outbound compliance design

For Canadian commercial email, CASL remains a hard design constraint.

The CRTC states that conspicuous publication may create implied consent only where the recipient caused the address to be publicly published, there is no statement against unsolicited commercial messages, and the message is relevant to the recipient's business role. The sender bears the burden of keeping evidence of that basis.

Sources:
- https://crtc.gc.ca/eng/com500/guide.htm
- https://crtc.gc.ca/eng/com500/faq500.htm

The prospecting system therefore should store, for every outbound email that relies on conspicuous publication:

- recipient address;
- source URL;
- date discovered;
- evidence that the address was publicly published by the business/recipient;
- whether any no-solicitation statement was present;
- why the message is relevant to the recipient's role; and
- unsubscribe/suppression status.

A third-party list containing an email address is **not** by itself sufficient evidence of conspicuous publication under the CRTC guidance. Directory data can seed company discovery, but the system should verify the contact route on the organization's own published material before relying on this basis.

Every commercial outreach message must include required sender identification/contact information and an unsubscribe mechanism unless a specific exemption applies.

### Sending infrastructure

For initial validation, use a normal business mailbox at deliberately low volume with individualized messages. The automation prepares the queue; it should not automatically blast thousands of recipients.

Do **not** use Amazon SES as a cold-list blasting engine. AWS itself recommends sending to people who want the mail and monitors unsolicited/complaint-heavy sending. SES is better suited later to opted-in product delivery, alerts and customer communications.

Sources:
- https://docs.aws.amazon.com/ses/latest/dg/tips-and-best-practices.html
- https://docs.aws.amazon.com/ses/latest/dg/faqs-enforcement.html

### Validation-scale target

For each concept:

- build a pool of 50–150 plausible prospects automatically;
- qualify the best 20–60;
- review the first 10 messages manually;
- then send small controlled daily batches;
- stop immediately on opt-out;
- send only qualified/positive replies to the owner.

The target is **qualified customer conversations per hour of owner attention**, not maximum email volume.

---

# Candidate A — Canadian importer intelligence packs

## Product

A simple report built from official Canadian importer and trade data.

A buyer chooses a product category and receives a clean package such as:

- major Canadian importers in that category;
- city/province;
- important source countries;
- product/HS-code explanation;
- category-level Canadian import trend/context where available;
- CSV of the underlying usable company list; and
- source/licence attribution.

No private contact enrichment is included in the first version.

## Exact initial customer

**Small Canadian customs brokers, freight forwarders and trade consultants** that want a low-cost prospecting/market-intelligence aid for identifying companies importing particular goods.

This is narrower and easier to validate than attempting to market directly to manufacturers across many countries.

## Why this customer is reachable

**Fact:** CBSA publishes an official list of licensed Canadian customs brokers containing company names, websites and business email addresses.

Source: https://www.cbsa-asfc.gc.ca/services/cb-cd/cb-cd-eng.html

**Fact:** CIFFA publishes a current member directory containing Canadian freight forwarders, service descriptions and company/contact information.

Source: https://www.ciffa.com/member-directory/

These directories are used for **company discovery**. Any electronic outreach still follows the compliance evidence rules above.

## Data source

**Fact:** ISED's 2024 Canadian Importers Database was released in September 2026 as open data and includes major importer lists by HS6/HS10 product, city and country. The CID identifies companies that collectively account for up to 80% of imports for the selected product, subject to confidentiality thresholds.

Sources:
- https://ised-isde.canada.ca/site/ised/en/research-and-business-intelligence/canadian-importers-database
- https://open.canada.ca/data/en/dataset/e5eae1d4-687c-4db2-9273-a8d2d711144c

**Fact:** ISED's Trade Data Online has more current category-level trade data and reports current data through July 2026, updated monthly/annually.

Source: https://ised-isde.canada.ca/site/ised/en/canadian-importers-database/trade-data-online

## MVP scope

Do not build a dashboard.

Build only:

1. one Python process that reads the official CID spreadsheets without corrupting leading-zero HS codes;
2. a lookup for HS6/HS10 descriptions;
3. report generation to CSV + a simple PDF/HTML report;
4. three pre-built sample categories;
5. one landing page explaining the product and showing a sample; and
6. a Stripe Payment Link or simple interest form.

Stripe Payment Links currently require no custom checkout code and use standard Stripe transaction pricing.

Source: https://stripe.com/en-ca/payments/payment-links

## Proposed test price — estimate, not validated

- CA$39–$79 for a pre-built category pack;
- CA$99–$149 for a custom category pack; or
- CA$199 pilot bundle for several categories for a broker/consultant.

The first objective is willingness-to-pay evidence, not price optimization.

## Semi-automated acquisition plan

### Prospect generation — automated

- Import company names/websites from the CBSA broker list and CIFFA directory.
- Remove large global firms initially; prioritize independent/small Canadian brokers and forwarders.
- Visit each website.
- Score whether the firm explicitly markets import, customs, prospecting, market-entry or specialized industry services.

### Personalization — AI-assisted

For each high-fit firm, generate one short factual message around an immediately visible example:

- identify one product/vertical they mention;
- generate a tiny sample importer snapshot for that category; and
- explain that the full report is based on official Canadian data.

The AI may draft wording but cannot invent customer names, capabilities or data values.

### Outreach — controlled

- Only use a contact route with a documented permissible basis.
- Initial batch: 10 manually reviewed prospects.
- If no compliance/deliverability problems, progress to roughly 10–20 qualified messages per business day during the test.
- One follow-up only during validation unless the recipient engages.

### Reply triage — automated

Classify as:

- interested/sample requested;
- pricing question;
- wrong person/referral;
- not interested;
- unsubscribe;
- unclear/human review.

Only the first three should normally reach the owner.

## Estimated owner burden

During validation: approximately **30–60 minutes per week** plus conversations with interested prospects.

If validated: most report generation, delivery and routine support can be automated.

## Estimated out-of-pocket MVP cost

**CA$0–$50 before sales**, excluding an optional domain/business mailbox already in use.

Main costs are payment-processing fees and optionally hosting/domain/email. Data is open and the initial computation is trivial.

## Main failure modes

- customers already know how to use CID themselves;
- annual company data is too stale for sales prospecting;
- a simple company list is not valuable without contact enrichment;
- buyers want shipment-level data that CID does not contain; or
- outreach response is too weak to justify acquisition effort.

## Go / kill criteria

**Advance:** at least 2 paid pilots or 5 qualified buyer conversations from the first 60 properly qualified prospects.

**Kill or materially reshape:** zero purchases and fewer than 3 genuine positive replies after 60 good-fit prospects have received compliant, personalized outreach.

---

# Candidate B — New-business signal feed for BC sign companies

## Product

A weekly email/CSV showing **newly licensed businesses that are likely to need commercial signage**, beginning with Vancouver.

Example records:

- new restaurant;
- retailer;
- fitness/wellness business;
- office/service location; and
- other public-facing business where a new opening creates a likely signage requirement.

Each record includes only available/open-data fields, source attribution and a simple relevance score.

## Exact initial customer

**Independent BC commercial sign manufacturers/installers**, especially companies that sell exterior signs, channel letters, window graphics, wayfinding and storefront signage.

## Why this customer is reachable

**Fact:** the BC Sign Association publicly lists many current member companies, including numerous sign manufacturers/installers.

Source: https://www.bcsignassociation.org/membership

**Fact:** the broader Sign Association of Canada provides member profiles/directories for Canadian sign producers and installers.

Sources:
- https://sac-ace.ca/membership/
- https://sacmembership.sac-ace.ca/

This creates a finite, understandable first prospect market rather than requiring generic lead-list purchasing.

## Data source

**Fact:** Vancouver's business-licence open dataset is updated daily and includes fields such as licence status, issue date, business name where publishable, business type/subtype and address fields subject to privacy rules.

Source: https://opendata.vancouver.ca/explore/dataset/business-licences/

## MVP scope

One city only: **Vancouver**.

Build:

1. scheduled download/API query for issued licences;
2. incremental detection of newly issued/relevant records;
3. deterministic category filters;
4. AI classification only for ambiguous business descriptions;
5. simple score for likely signage relevance;
6. weekly HTML email + CSV export;
7. a customer-specific territory/category filter; and
8. Stripe subscription/payment link.

No CRM, mapping dashboard, multi-city portal or contact enrichment in the first version.

## Proposed test price — estimate, not validated

- CA$29/month beta;
- intended normal Vancouver price: CA$49/month;
- potential later multi-city tier: CA$79–$129/month.

## Semi-automated acquisition plan

This is the strongest outbound test because the sales message can contain **the product itself**.

### Prospect generation — automated

- Seed BC sign companies from BCSA/SAC directories.
- Visit company websites.
- Score for: commercial storefront signage, geographic service area, local sales focus and absence of an obvious competing lead-intelligence product.
- Locate a permitted business contact route and save supporting evidence.

### Prospect-specific sample — automated

For each sign company:

- infer its service region from the website;
- select 3–5 recent relevant Vancouver licence records;
- format them into a tiny sample feed; and
- state exactly why those records could matter to a sign shop.

This makes the outreach materially more concrete than a generic software pitch.

### Outreach — AI-assisted / controlled

Message shape:

- one sentence showing we understand the sign company's service;
- 3–5 actual recent sample businesses;
- one sentence explaining that a weekly filtered version can be delivered automatically;
- link to sample/subscription;
- required identity/unsubscribe information.

The owner reviews the first batch. After quality is proven, the prospect pipeline can prepare and queue subsequent compliant messages automatically.

### Reply handling — automated

- interested → owner notification;
- asks for another city → tag demand by municipality;
- requests different business types → record feature demand;
- unsubscribe/not interested → suppress immediately;
- ambiguous → owner review.

## Estimated owner burden

Validation: **less than one hour per week** excluding positive sales conversations.

Validated operation: likely **15–30 minutes per week** for data-quality review if the source remains stable.

## Estimated out-of-pocket MVP cost

**CA$0–$50 before sales** if existing hosting/GitHub/AWS resources are used.

The first version needs no paid data source.

## Main failure modes

- Vancouver alone produces too few valuable openings;
- a licence may be issued after a sign vendor has already been selected;
- sign companies obtain new-business information through existing local networks;
- prospects demand phone/email contact enrichment;
- expansion becomes difficult because municipal data formats/licences differ; or
- relevance scoring creates too much noise.

## Go / kill criteria

**Advance:** 3 paid beta customers from the first 30–40 properly qualified BC sign companies, or at least 5 prospects explicitly asking to trial the feed.

**Kill/reshape:** fewer than 3 positive responses after 40 good-fit prospects receive real sample leads, or sample customers report that the licence records arrive too late to be commercially useful.

## Expansion only after validation

If Vancouver works:

1. add Burnaby/Surrey/Richmond only where usable licensing/opening data exists and licence terms permit;
2. add territory matching;
3. add other buyer verticals only after separately validating their timing/value;
4. consider Apify/API distribution later.

---

# Candidate C — Commercial-laundry instant estimate widget

## Product

A small calculator commercial laundry/linen companies embed on their website.

A prospective customer enters simple facts such as:

- business type;
- estimated laundry volume;
- item type or service type;
- pickups per week;
- postal/ZIP area; and
- optional special handling.

The widget returns an **estimated weekly/monthly range**, clearly marked as non-binding, then captures the enquiry.

The laundry provider controls its own rates, service zones, minimums and assumptions.

## Exact initial customer

**Independent commercial laundry and linen-service operators** serving hotels, restaurants, gyms, clinics, salons and other local businesses.

Avoid the largest national operators initially.

## Evidence supporting this niche

Current commercial-laundry sites frequently still use manual quote forms and promise a later response rather than giving an immediate estimate. Examples found during Stage 4 include Greater Vancouver commercial laundries that ask users to provide volume/frequency and then return a custom quote.

Examples:
- https://www.happylaundry.ca/get-a-general-laundry-quote
- https://www.sampanlaundry.com/commercial-laundry-drycleaning/
- https://www.thelaundrybrothers.com/business

At least one current operator, Purple Hamper, already uses an instant commercial quote calculator, which is useful evidence that this workflow is practical rather than hypothetical.

Source: https://purplehamper.com/linen-service

**Fact:** the TRSA/LinenServices directory currently exposes a large prospect pool: more than 1,700 TRSA directory results, including more than 100 Canadian listings, while the wider linen-services directory contains thousands of service listings.

Sources:
- https://www.linenservices.com/trsa-member-directory
- https://www.trsa.org/about-trsa/join-trsa/member-benefits/trsa-members/

This does not prove purchase demand for our widget, but it makes customer discovery straightforward.

## MVP scope

Do **not** build a generic calculator SaaS platform.

Build one configurable embeddable widget with:

1. business type;
2. weekly weight/volume;
3. pickup frequency;
4. service-zone/postal-code check;
5. provider-configured per-pound/per-item ranges;
6. minimum order/route charge;
7. estimated weekly/monthly range;
8. enquiry capture; and
9. simple HTML/JavaScript embed.

For the first 3 customers, configuration can be a developer-edited JSON/YAML file rather than an admin dashboard.

## Proposed test price — estimate, not validated

- CA$99 one-time setup + CA$29/month beta; or
- CA$39/month with no setup for the first few pilots.

Only introduce higher tiers after buyers prove the widget produces useful enquiries.

## Semi-automated acquisition plan

### Prospect generation — automated

- Seed companies from TRSA/LinenServices and regional searches.
- Visit each company's site.
- Detect whether it serves commercial accounts.
- Detect whether its current quote path is manual, e.g. “request a quote,” “we reply within one business day,” or a contact form without an instant estimate.
- Exclude sites already offering a good instant calculator.

### Fit scoring — automated

Higher score for companies that:

- explicitly price by weight/volume/frequency;
- serve multiple business verticals;
- publish a commercial quote form;
- have meaningful local route coverage; and
- appear independent enough for a short buying cycle.

### Personalized demo — AI-assisted

For the best prospects, automatically configure a **demonstration** from only public information on their website, clearly marking any unknown rates as sample values.

The message can say, in substance: your current commercial quote page asks customers for volume and pickup frequency, but they wait for a reply; here is what an instant estimate experience could look like.

No claim should imply that the sample prices are the prospect's actual prices unless they supplied them.

### Outreach and reply triage

Use the common compliant workflow. The owner's attention is needed only for interested companies, pricing/customization questions and pilots.

## Estimated owner burden

Validation: roughly **one hour per week** plus interested conversations.

At scale: target **under 15 minutes of routine setup per customer** once a self-service configuration form exists.

## Estimated out-of-pocket MVP cost

Approximately **CA$0–$100 before sales**, depending on hosting/domain/business email already available.

The widget itself can be static code with a tiny backend only for lead capture/configuration.

## Main failure modes

- each laundry company prices too differently, turning every setup into consulting;
- providers intentionally avoid showing any price before reviewing the account;
- estimated prices reduce leads rather than increase them;
- the buyer values the widget at too little to support acquisition costs;
- route/postal-code logic becomes complex; or
- generic quote-builder products are “good enough.”

## Go / kill criteria

**Advance:** 3 paid pilots from 40 highly qualified operators, or 5 strong pilot requests including willingness to provide their pricing rules.

**Kill/reshape:** zero paid pilots after 40 strong prospects, or repeated feedback that commercial laundry pricing cannot be safely reduced to an estimate range.

---

# Comparative recommendation

| Factor | Importer packs | New-business sign feed | Laundry quote widget |
|---|---|---|---|
| Build cost | Very low | Very low | Low |
| First test speed | Very fast | Very fast | Fast |
| Recurring revenue potential | Low–medium | **High** | **High** |
| Ongoing human work | Very low | Very low | Low if standardized |
| Acquisition automation | High | **Very high** | **Very high** |
| Data/legal risk | Low | Low–medium | Low |
| Main uncertainty | Will buyers pay for repackaged free data? | Do licences arrive early enough to be useful? | Will providers expose estimated pricing? |
| Stage 4 rank | 2 | **1** | 3 |

## Recommendation for Stage 5 if approved

Do **not** build all three.

Recommended first development sequence:

1. Build the **data extraction + sample generator** for Candidate B only.
2. Generate a real sample of recent Vancouver business licences relevant to sign companies.
3. Build the semi-automated prospecting/scoring pipeline for the initial BCSA/SAC prospect set.
4. Produce a landing/sample page and payment link.
5. Prepare—but do not blindly dispatch—an initial compliant outreach batch.
6. Review evidence before expanding to multi-city development.

Candidate A can reuse much of the same report-generation/acquisition infrastructure afterward. Candidate C should remain unbuilt until either the data-product test is exhausted or there is a decision to run two separate validation tracks.

---

# Approval gate

Stage 4 is complete when these plans are reviewed.

**No significant Stage 5 development should begin without owner approval.**

If Candidate B is approved, Stage 5 should begin with the smallest possible working sample and acquisition pipeline, not a production SaaS application.

## Verification record

- Last verified: `2026-10-16`
- Verified by: High Director
- Current sources checked: Canadian Importers Database; ISED Trade Data Online; CBSA customs-broker directory; CIFFA directory; Vancouver business-licence open data; BC Sign Association and Sign Association of Canada; commercial-laundry operator quote flows; TRSA/LinenServices directories; CRTC CASL guidance; AWS SES sending guidance; Stripe Canada.
- Facts, estimates and proposed pricing are labeled separately.
- Not yet validated: purchase intent for any exact offer, final price, conversion rate, ROI for customers, timing value of business licences, actual laundry-provider willingness to expose estimates, or jurisdiction-specific legal advice for a scaled outbound program.
