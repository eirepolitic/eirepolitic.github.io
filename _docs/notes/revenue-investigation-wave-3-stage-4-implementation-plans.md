---
title: Revenue Investigation — Wave 3 Stage 4 Implementation Plans
summary: Validation and acquisition plans for the two surviving Wave 3 ideas; no significant development authorized.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 221
permalink: /projects/notes/revenue-investigation-wave-3-stage-4-implementation-plans/
tags: [revenue-investigation, research, wave-3, implementation-plan]
---

# Revenue Investigation — Wave 3 Stage 4 Implementation Plans

## Recommendation

Wave 3 adds two credible Stage 4 concepts to the broader opportunity inventory:

1. **Recurring mystery-enquiry response monitoring for agencies/multi-location businesses** — strongest Wave 3 candidate.
2. **EDI-lite spreadsheet order translation for small suppliers** — credible but more likely to turn into custom integration work.

No Stage 5 build is authorized.

---

# Candidate W3-1 — Recurring mystery-enquiry response monitor

## Plain-English offer

“Once a month, we test whether your client/location actually responds to a new web enquiry and show you where leads are being lost.”

## Exact first customer

**Small digital-marketing agencies running paid search/local lead generation for 10–50 service-business clients or locations.**

Start with agencies rather than individual businesses because one buyer can bring many monitored locations.

## Initial monitored channel

Website enquiry/contact forms only.

Do not initially test phone, SMS, appointment bookings or regulated-service scenarios that could create unnecessary legal/operational complexity.

## MVP output

For each authorized client/location:

- form submitted successfully: yes/no;
- date/time of test;
- first response received: yes/no;
- minutes/hours to first response;
- response channel;
- basic follow-up count during the approved observation period;
- screenshots/evidence;
- comparison across locations/months;
- simple red/amber/green result.

## Safety/operating design

The paying agency/client must explicitly authorize testing.

Test messages should:

- identify themselves as routine service-quality enquiries where appropriate;
- avoid booking scarce appointments;
- avoid emergencies, health claims, legal claims, financial commitments or deceptive high-stakes scenarios;
- stop before a staff member spends material time preparing a quote or appointment unless the authorized test explicitly requires that step.

The product tests response operations, not employee honesty or protected characteristics.

## Proposed validation price — estimate

- free initial 5-location benchmark;
- CA$99/month for up to 10 monthly tests;
- CA$199/month for up to 25;
- optional per-location overage later.

## Semi-automated acquisition system

### Prospect discovery — automated

Build a prospect pool from public agency directories/search results.

The crawler visits agency sites and scores for:

- PPC/Google Ads/local lead-generation services;
- service-business client case studies;
- multi-location/franchise marketing;
- lead tracking/conversion language;
- team size consistent with a small/mid-size agency rather than an enterprise agency.

### Personalized reason — AI-assisted

For each agency, create a short factual note based only on its public site, e.g.:

“You advertise PPC for home-service businesses. We built a simple monthly check that verifies whether the enquiries your campaigns generate actually get answered.”

Do not invent client names or performance problems.

### Sample offer — automated

Instead of pretending to test clients without permission, outreach offers a **free authorized benchmark** covering up to five client/location forms.

This is important: prospecting automation discovers the agency, but actual mystery tests begin only after authorization.

### Outreach workflow

- qualify 50–100 agencies;
- manually review first 10 messages;
- send controlled compliant batches;
- one follow-up during validation;
- suppress opt-outs immediately;
- route positive replies to an intake form requesting authorized domains/forms.

### Reply triage

Automated categories:

- wants free benchmark;
- pricing question;
- wrong person/referral;
- not interested;
- unsubscribe;
- legal/privacy question;
- human review.

Only benchmark requests, pricing questions and unusual concerns reach the owner.

## Acquisition automation advantage

Unlike many B2B products, the qualifying evidence is public: agencies describe their client type and lead-generation services on their own websites. This makes list scoring and personalization highly automatable.

## Owner burden target

Before positive replies: **under 30 minutes/week**.

After validation: roughly **15–30 minutes/week** for exception review if test flows remain standardized.

## Estimated MVP cost

CA$0–$100 before sales using browser automation, a monitored inbox and existing hosting.

## Go / kill criteria

**Advance:** from the first 50 highly qualified agencies, obtain either:

- 3 paid pilots; or
- 5 agencies that complete an authorized free benchmark and explicitly ask about recurring monitoring.

**Kill/reshape:** fewer than 3 meaningful positive responses from 50 well-qualified agencies, or agencies say their existing call-tracking/CRM stack already gives equivalent evidence.

## Main failure mode

Agencies may view the service as a one-time audit rather than recurring monitoring. The test must specifically measure whether monthly evidence has enough client-retention/reporting value to justify a subscription.

---

# Candidate W3-2 — EDI-lite spreadsheet order translator

## Plain-English offer

“Your customers send purchase orders in different spreadsheets. We automatically convert each familiar format into the one clean file your staff already knows how to import.”

## Exact first customer

**Small specialty wholesalers/distributors with recurring B2B customers and manual spreadsheet order entry.**

Stage 5, if ever approved, should pick one vertical only. A useful starting research target would be small food-service, building-material or specialty-equipment distributors.

## Product boundary

The first product handles **CSV/XLSX files only**.

It does not:

- implement X12/EDIFACT;
- connect directly to retailer VANs;
- parse arbitrary scanned PDFs;
- post orders directly into the ERP;
- send acknowledgements/ASNs/invoices;
- replace mandatory EDI relationships.

This boundary is critical to keep support low.

## MVP workflow

For each recurring customer format:

1. supplier uploads 3–5 historical sample files;
2. define deterministic field mapping to supplier's standard import schema;
3. define SKU/customer/unit rules;
4. convert new files automatically;
5. flag missing/unknown data;
6. produce validated CSV/XLSX output;
7. retain source + output for review.

No silent guessing on quantities, product IDs or prices.

## Proposed validation price — estimate

- first mapping: CA$149 setup;
- additional customer format: CA$99–$199;
- recurring service: CA$39–$99/month depending on files/volume.

The economics only work if a mapping remains stable and setup can become semi-standardized.

## Semi-automated acquisition system

### Prospect discovery — automated

Use distributor/wholesaler directories and search results to identify small firms whose sites show:

- B2B/wholesale ordering;
- multiple customer/account types;
- downloadable order forms or price lists;
- sales/order desks;
- language suggesting orders by email/spreadsheet/PO.

### Qualification — automated plus AI

Score higher where the public site suggests order-entry administration but no sophisticated B2B portal/EDI stack.

The pain itself is often not visible, so personalization must remain cautious.

### Outreach approach

Use a diagnostic message rather than an assertion:

“We work on a narrow order-entry problem: recurring customers sending CSV/Excel POs in different layouts that staff then reformat manually. Is that still a workflow you deal with?”

If yes, offer to convert one real sample format free or at a nominal fee.

### Reply triage

- yes, manual reformatting exists → owner/intake;
- already uses EDI/portal → close;
- PDF/email only → tag as future product demand but do not expand MVP;
- wants ERP integration → tag but decline for validation phase;
- unsubscribe/not interested → suppress.

## Owner burden target

Prospecting: under **30 minutes/week**.

Pilot setup: initially 30–90 minutes per format. The concept should be killed if stable production mappings cannot be created much faster after the first few examples.

## Estimated MVP cost

CA$0–$100 plus existing hosting/storage.

## Go / kill criteria

**Advance:** 2 paying customers with at least 3 recurring file formats total, and average steady-state support under about 10 minutes per format/month.

**Kill/reshape:** prospects mostly need PDF/EDI/ERP integrations rather than spreadsheet translation, or each format requires substantial ongoing custom maintenance.

## Main failure mode

The customer problem may be real but too bespoke. If every customer requires consulting-style mapping and support, this does not meet the low-touch objective.

---

# Wave 3 comparison

| Factor | Mystery-enquiry monitor | EDI-lite translator |
|---|---|---|
| Build/test cost | **Very low** | Very low |
| Recurring potential | **High** | Good |
| Prospect identification | **Excellent** | Moderate |
| Automated personalization | **Excellent** | Moderate |
| Human setup burden | Very low | Higher |
| Error consequence | Low–medium | **Higher** |
| Scale without consulting | **Good** | Uncertain |
| Wave 3 rank | **1** | **2** |

## Combined opportunity inventory

After three waves:

- broad ideas generated: **180**;
- multiple categories deliberately explored;
- weak/crowded concepts rejected before development;
- Stage-4-level candidates now span data products, micro-tools, creator operations, field-service/installer products, procurement/RFP tooling and revenue-monitoring services.

No Stage 5 development is recommended yet because the current instruction is to continue building the opportunity pool.

## Verification record

- Last verified: 2026-10-16
- Stage 4 status: complete
- No significant development started.
- Proposed pricing and conversion thresholds are validation estimates, not proven economics.
