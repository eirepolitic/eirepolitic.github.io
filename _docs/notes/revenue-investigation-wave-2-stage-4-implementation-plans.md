---
title: Revenue Investigation — Wave 2 Stage 4 Implementation Plans
summary: Concrete validation and acquisition plans for the three surviving Wave 2 business ideas; no significant development authorized.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 217
permalink: /projects/notes/revenue-investigation-wave-2-stage-4-implementation-plans/
tags: [revenue-investigation, research, wave-2, implementation-plan]
---

# Revenue Investigation — Wave 2 Stage 4 Implementation Plans

## Recommendation

No development should start yet. Wave 2 produces three additional ideas worth retaining beside the Wave 1 finalists.

Current Wave 2 order:

1. **Sponsor proof/report generator** — strongest low-touch customer-acquisition fit.
2. **Installer QR equipment handover pages** — simple recurring/usage product with a very identifiable customer base.
3. **RFP requirement extractor** — clear value and demonstrated pricing, but higher accuracy/trust expectations.

---

# Shared acquisition design

All three should use the same operating philosophy:

`public prospect source → website/content inspection → fit score → permitted contact-route evidence → personalized sample → controlled outreach → automated follow-up/reply triage → owner only handles interest`

Routine list building, website research, personalization, follow-up scheduling and inbox classification should be automated or AI-assisted.

For Canadian commercial email, retain the CASL evidence rules documented in Wave 1 Stage 4. Do not treat a third-party directory address alone as permission to mass email. Verify the contact route/basis and store suppression/unsubscribe evidence.

Initial validation should use small, high-quality batches rather than high-volume blasting.

---

# Candidate W2-1 — Sponsor proof/report generator

## Plain-English offer

“Send your sponsor a professional proof-of-delivery report without manually assembling screenshots and stats.”

The product creates a branded PDF/share page after a sponsored newsletter issue or podcast episode.

## Exact first customer

Independent newsletters that visibly sell sponsorships and have approximately 1–8 paid placements per month.

Start with newsletters before podcasts because issue pages, ad links and campaign exports are simpler than podcast attribution.

## Initial output

For one sponsor placement:

- publication/issue name and date;
- sponsor name;
- screenshot/proof of placement;
- audience/send figure supplied by publisher;
- sponsor-link clicks supplied by publisher/export;
- calculated CTR where applicable;
- tracked link/UTM details;
- short factual delivery summary;
- renewal-ready PDF/share URL.

No attempt should be made to invent impressions or infer unavailable metrics.

## MVP scope

Before any platform integrations:

1. upload one CSV/export or enter a few metrics manually;
2. paste issue/archive URL;
3. paste sponsor name/link;
4. generate one branded report;
5. export PDF/share page.

No booking CRM, invoicing, marketplace or ad server.

## Proposed test pricing — estimate

- first report free;
- CA$15/report pay-as-you-go;
- CA$39/month for up to 5 reports;
- CA$79/month for a higher-volume publisher later.

## Semi-automated customer acquisition

### Prospect source — automated

- seed from BeeDirectory and other newsletter directories;
- inspect public issue archives;
- detect sponsor/ad language such as “sponsored by,” “partner,” “presented by,” or recurring ad blocks;
- record visible frequency and estimated sponsor activity.

BeeDirectory currently lists hundreds of newsletters, including sponsorship pricing for many entries. Source: https://bee-directory.com/search

### Qualification — automated

High score when:

- newsletter visibly runs paid sponsors;
- sponsor placements recur;
- publication appears independently operated rather than a large media company;
- sponsor reporting is not already clearly provided by a sophisticated ad platform;
- contact route is publicly provided for partnerships/advertising/business enquiries.

### Personalized sample — mostly automated

For each strong prospect:

1. select one recent sponsored issue;
2. capture the public issue/placement evidence;
3. create a **mock layout** showing how their sponsor report could look;
4. clearly label unknown/private metrics as placeholders rather than guesses.

### Outreach message

Very short: “I noticed you run paid sponsorships. I made a sample of what a sponsor-delivery report for your [issue] could look like. If useful, the first real report is free.”

No need for a sales call unless they want one.

### Reply triage

- wants free report → automated intake link;
- asks price → automated standard response + owner notification only if unusual;
- interested in recurring → owner notification;
- not interested/unsubscribe → suppression;
- asks integration → tag requested platform for product roadmap.

## Owner burden target

Under **30 minutes/week** before positive replies, plus any genuinely useful buyer conversations.

## Estimated MVP cost

CA$0–$75 using existing hosting/code infrastructure plus optional domain/business email.

## Go/kill threshold

**Advance:** 3 paying recurring users or 5 publishers who use a free report and explicitly request another from the first 40 strong prospects.

**Kill/reshape:** fewer than 3 meaningful positive responses from 40 well-qualified publishers shown personalized samples.

## Main risk

The work is useful but not valuable enough to pay for because creators can continue using screenshots. The validation test should answer this before integrations are built.

---

# Candidate W2-2 — Installer QR equipment handover pages

## Plain-English offer

“Put one branded QR label on every system you install so your customer always has the correct manual, warranty details and your service contact.”

## Exact first customer

Independent BC HVAC/plumbing contractors that install heat pumps, furnaces, boilers or similar equipment and expect future service work from the same customer.

## Customer value

This is not mainly a document-management product. It is an **aftercare and customer-retention tool**:

- customer stops losing manuals;
- contractor gives a more professional handover;
- contractor's service contact remains physically attached to the equipment;
- future service/warranty reminders can point back to the installer.

## MVP output

One mobile-friendly page per installed asset containing:

- contractor logo/contact;
- equipment make/model;
- customer-safe installation date/reference;
- manufacturer manual link/file;
- warranty link/basic notes;
- “request service” link;
- QR label PDF.

Avoid storing home addresses or unnecessary customer personal information in the first version.

## Prospect pool

- BC Plumbing & HVAC Association lists 53+ active members. Source: https://bcpha.org/members
- Mechanical Contractors Association of Canada directory has hundreds of members. Source: https://members.mcac.ca/member-directory/Find
- MCABC/RSES provide additional contractor discovery sources.

## Proposed test pricing — estimate

Two models to test:

- CA$29/month including 10 new equipment pages per month; or
- CA$3 per newly created equipment page with a small minimum purchase.

First pilot: 5 equipment pages for CA$20–$25 to establish willingness to pay.

## Semi-automated customer acquisition

### Prospect generation

- import contractor names/websites from industry directories;
- visit websites automatically;
- score firms that actively advertise installations/replacements and maintenance/service;
- prioritize independent/local firms with repeat-service economics.

### Personalized demo

For each top prospect:

1. identify one equipment brand they publicly say they install;
2. use a public manufacturer manual for a common model;
3. create a demonstration QR handover page using the contractor's public logo/name and **clearly mark it as a demo**;
4. generate a label mockup.

The outreach therefore shows the finished concept rather than describing software.

### Outreach

“Your site shows you install [brand]. I mocked up a QR handover page your technician could leave on each installation: manual + warranty + your service contact. Here is the demo.”

Interested contractor receives a simple pilot intake form rather than a meeting requirement.

### Automation after sale

- intake form collects contractor + equipment data;
- manual lookup suggests likely document;
- contractor confirms correct manual;
- page + QR PDF generated automatically;
- optional annual service reminder added later.

## Owner burden target

Validation: under **45 minutes/week** plus interested replies.

Validated operation: target under **5 minutes manual review per new page**, eventually less with model/manual matching.

## Estimated MVP cost

CA$0–$75 plus printed label samples if desired.

## Go/kill threshold

**Advance:** 3 paid contractor pilots or 5 contractors willing to use the QR page on a live installation from 30 qualified prospects.

**Kill/reshape:** fewer than 3 positive responses from 30 contractors shown a relevant branded demo, or contractors consistently say customers/manufacturers already solve the handover problem.

## Main risk

Installer sees the QR page as “nice to have” rather than something worth paying for. Retention/service-call value must be central to the pitch.

---

# Candidate W2-3 — Lightweight RFP requirement extractor

## Plain-English offer

“Upload a long RFP and get an Excel checklist showing every requirement, deadline, mandatory form and where it appears.”

It does not promise to write or guarantee the bid.

## Exact first customer

Small Canadian firms that have evidence of government/institutional contract activity but are not large enough to maintain a dedicated proposal department.

Possible first verticals: IT services, engineering/technical consulting, training or business services. Stage 5 validation should select only one vertical first.

## MVP output

Excel/CSV matrix with:

- source page/section;
- requirement text;
- requirement type;
- mandatory vs informational;
- due date/time where present;
- required attachment/form;
- evaluation/scoring reference if stated;
- owner/status columns left blank for customer use;
- confidence/needs-review flag.

Every extracted item should link back to its source page/section.

## Competitor anchor

RFP Matrix currently lists roughly US$100 for a single-RFP product and US$150+/month subscriptions, proving willingness to pay but also defining a clear incumbent. Source: https://rfpmatrix.com/

The proposed MVP therefore competes on **narrower scope, source traceability and lower one-off cost**, not broader features.

## Proposed test pricing — estimate

- CA$39 for a typical RFP up to a defined page limit;
- CA$79 larger-document tier;
- first validation sample free on a public RFP.

## Semi-automated customer acquisition

### Prospect generation

- use public Canadian contract-award/supplier sources to identify smaller companies that have won government work;
- filter to categories where repeated RFP bidding is likely;
- visit company sites to estimate size/service fit;
- prioritize firms without an obvious full proposal department.

GovMarket exposes a searchable Canadian supplier dataset suitable for discovery. Source: https://www.govmarket.ca/suppliers

### Personalized sample

For a strong prospect:

1. find a current/recent public solicitation in the same service category;
2. process several pages or the entire public RFP;
3. generate a sample requirement matrix;
4. send a screenshot/link showing the actual output.

Do not imply the company intends to bid on that exact RFP unless evidence says so.

### Acquisition automation

AI handles company/category matching, public-RFP matching and first-draft personalization. The system queues only prospects where there is a credible relationship between their services and the sample RFP category.

Replies requesting document processing can be routed into an upload/payment workflow. Owner only handles unusual security questions, large documents or enterprise requests.

## Accuracy/review design

This product has the strictest human-quality gate of the three Wave 2 candidates.

Before charging:

- test against at least 10 public RFPs;
- manually compare extracted mandatory requirements/deadlines/forms;
- define measurable recall/error thresholds;
- always label output as an extraction aid requiring bidder review;
- never claim that using it guarantees compliance or eligibility.

## Owner burden target

Validation may require **1–2 hours/week** because output accuracy must be manually audited. If validated, routine documents should become mostly automated with exceptions reviewed.

## Estimated MVP cost

CA$0–$100 excluding AI/API usage; per-document model cost should be measured during testing and built into price.

## Go/kill threshold

**Advance:** 2 paid one-off jobs plus at least 5 serious sample requests from 40 qualified prospects, with extraction accuracy high enough that manual review is short.

**Kill/reshape:** low buyer interest, or manual QA consistently takes more than roughly 10–15 minutes per normal document at the proposed price.

## Main risk

A single missed requirement can damage trust. This idea should be abandoned if reliability requires substantial human proposal expertise per job.

---

# Wave 2 comparison

| Factor | Sponsor report | QR handover | RFP extractor |
|---|---|---|---|
| MVP cost | Very low | Very low | Low |
| Prospect identification | **Very easy** | **Easy** | Easy |
| Personalized sample automation | **Excellent** | **Excellent** | Good |
| Recurring revenue | Good | **Good** | Medium |
| Ongoing support | Very low | Very low | Medium |
| Accuracy/liability burden | Low | Low | **Higher** |
| Owner time if validated | Very low | Very low | Low–medium |
| Wave 2 rank | **1** | **2** | **3** |

## Combined pool implication

Wave 2 adds three credible concepts to the Wave 1 Stage 4 list. At this point, the goal should remain **building the opportunity inventory**, not selecting a build prematurely.

No Stage 5 development is recommended until the owner decides the pool is broad enough or asks for a cross-wave ranking.

## Verification record

- Last verified: 2026-10-16
- Stage 4 status: complete
- No significant development started.
- All proposed prices and conversion thresholds are estimates for validation, not established market facts.
