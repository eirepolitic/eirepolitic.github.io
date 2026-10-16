---
title: Revenue Investigation — Wave 3 Stage 3 Deep Investigation
summary: Deep investigation of the two Wave 3 survivors: recurring mystery-enquiry monitoring and EDI-lite order translation.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 220
permalink: /projects/notes/revenue-investigation-wave-3-stage-3-deep-investigation/
tags: [revenue-investigation, research, wave-3, deep-investigation]
---

# Revenue Investigation — Wave 3 Stage 3 Deep Investigation

## Decision summary

| Candidate | Decision | Why |
|---|---|---|
| **Recurring mystery-enquiry response monitor** | **ADVANCE** | Clear revenue-linked problem, observable demand, simple recurring service, and prospecting can be automated from agency/client directories or multi-location brands. |
| **EDI-lite order translator** | **ADVANCE CAUTIOUSLY** | Small suppliers demonstrably face an expensive gap between manual order entry and full EDI. However, current alternatives already exist, so the product must stay narrowly focused on one file/order pattern or vertical. |

---

## 1. Recurring mystery-enquiry response monitor — ADVANCE

### Plain-English product

A service that periodically submits a realistic test enquiry to a company's public lead channel and measures what happens next.

Example: a dental group has 12 locations. Once a month the system submits a test enquiry to each location, then reports:

- whether anyone replied;
- how long the first reply took;
- which channel was used;
- whether follow-up happened;
- whether the enquiry was handled consistently across locations.

The value is finding revenue leaks that ordinary website uptime monitoring cannot see.

### Evidence of demand

- Clearline published a 2026 study mystery-shopping 53 Canadian car dealerships and found average response time above nine hours, with nearly a third never responding. Source: https://www.useclearline.com/blog/mystery-shop-dealership-lead-response-study-2026
- HireAiGO is currently running a large mystery-shop study of thousands of gyms, indicating active commercial interest in lead-response performance. Source: https://hireaigo.com/study
- Local Revenue Ops currently sells a US$99 one-off lead-response/mystery-shop audit to local service businesses. Source: https://localrevenueops.com/

These prove the problem and willingness to pay for audits. The gap is a **recurring, automated, multi-location monitoring layer** rather than a one-time consulting audit.

### Best first customer

**Marketing agencies managing paid lead generation for 10–50 local-service clients or locations.**

Why agencies first:

- one sale can cover many monitored locations;
- they already care about lead conversion and response time;
- they can use the report as evidence in client reviews;
- the agency, rather than each small business, becomes the buyer.

Possible first vertical: dental, HVAC, legal, home services, gyms or auto dealerships. Stage 4 should choose one vertical for initial testing.

### Revenue model estimate

Not validated:

- CA$10–$25 per monitored location/test;
- CA$99–$249/month agency starter tier;
- higher tier for more locations/frequency.

### Operating burden

Low if the test channels are standardized and permitted:

- website form;
- published enquiry email;
- optionally permitted web chat.

Phone/SMS should be excluded from the first version because consent, recording and telecom complexity increase quickly.

### Main constraints

- tests must not create fake bookings, consume scarce appointment slots or materially waste staff time;
- test identities/messages must be designed so staff can safely respond without being deceived into financial/medical/legal action;
- some forms use CAPTCHAs or anti-bot controls;
- the buyer may prefer fixing lead handling rather than monitoring it;
- businesses may object if monitoring is not clearly authorized by the paying customer.

### Minimum viable test

Offer one agency a free benchmark of 5–10 client/location forms, with explicit agency authorization. Produce a simple response-time report. Then offer monthly monitoring.

### Acquisition advantage

Agencies are straightforward to identify through public directories and agency websites. The prospecting system can automatically look for agencies advertising PPC, local lead generation or multi-location marketing, score likely fit, and create a sample audit offer.

### Stage 3 judgment

**Advance to Stage 4.** This is the strongest Wave 3 opportunity.

---

## 2. EDI-lite order translator — ADVANCE CAUTIOUSLY

### Plain-English product

A small supplier receives purchase orders from customers in several spreadsheet/CSV/email formats. Staff manually retype those orders into one standard internal spreadsheet or accounting/ERP import format.

The product learns each customer's file layout and converts it automatically into the supplier's standard order format.

It is **not full EDI**. It is a bridge for relationships where formal EDI is too expensive or unnecessary.

### Market evidence

- PlainEDI explicitly positions simple CSV conversion as a lower-complexity alternative for smaller vendors. Source: https://plainedi.com/guides/plainedi-vs-orderful-vs-sps-commerce
- Modusbridge markets “EDI-grade automation without EDI” to small distributors, converting emailed/PDF orders into structured records. Source: https://www.modusbridge.com/solutions/edi-alternative
- TebcoForge's 2026 analysis describes small suppliers being quoted hundreds per month plus setup fees for traditional EDI and frames this as poorly matched to low-volume relationships. Source: https://tebcoforge.com/blog/sps-commerce-alternative-for-small-suppliers-what-edi-software-actually-costs-in-2026/
- DynamoDocs combines EDI with emailed/PDF PO ingestion, further validating demand but also showing active competition. Source: https://dynamodocs.app/answers/edi-alternative-for-purchase-orders

### Narrow gap

Do not build an EDI platform or generic AI PO reader.

Focus on **repeatable spreadsheet/CSV order translation for one vertical**, where customers send predictable but inconsistent files.

Possible vertical shapes:

- food-service suppliers;
- building-material distributors;
- promotional-product suppliers;
- specialty wholesalers;
- small manufacturers selling to a handful of larger accounts.

The customer supplies sample files and the target import schema. The product creates a mapping profile and flags exceptions rather than guessing.

### Revenue estimate

Not validated:

- CA$100–$300 one-time mapping/setup per customer format;
- CA$29–$99/month for recurring conversion volume;
- or usage-based pricing per file/order.

### Automation

Very high after mapping:

`incoming file → identify customer format → map columns/codes → validate quantities/SKUs → flag exceptions → output standard CSV → archive`

AI is useful only for ambiguous headers/notes; deterministic mappings should handle production conversion.

### Operating burden

Potentially low for stable CSV/Excel formats, but higher if customers frequently change templates or send PDFs/scans.

### Main risks

- established tools already solve much of the problem;
- every customer format becomes custom support work;
- incorrect order conversion has direct financial consequences;
- ERP integration requests expand scope;
- true EDI becomes necessary as the buyer grows.

### Minimum viable test

Find one small distributor that receives at least three recurring customer-specific spreadsheet order formats. Offer to automate one format only. Measure mapping/setup time, exception rate and hours saved.

### Acquisition

Potential prospects can be found through wholesale/distributor directories, but qualification is harder because the pain is not publicly visible. Semi-automated outreach should therefore target operational roles at firms whose websites indicate wholesale/distribution activity and use a short diagnostic question rather than pretending to know their order process.

### Stage 3 judgment

**Advance to Stage 4, but below mystery-enquiry monitoring.** The problem is real; the risk is drifting into bespoke integration consulting.

---

## Stage 4 candidates

1. Recurring mystery-enquiry response monitor for agencies/multi-location businesses.
2. EDI-lite spreadsheet order translator for one narrowly chosen wholesale vertical.

No development should start before Stage 4 plans are reviewed.

## Verification record

- Last verified: 2026-10-16
- Stage 3 status: complete
- Pricing estimates remain unvalidated.
