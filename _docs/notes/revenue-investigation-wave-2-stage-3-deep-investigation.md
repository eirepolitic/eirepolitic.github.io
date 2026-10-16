---
title: Revenue Investigation — Wave 2 Stage 3 Deep Investigation
summary: Deep investigation of five Wave 2 finalists, reducing them to three implementation-plan candidates.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 216
permalink: /projects/notes/revenue-investigation-wave-2-stage-3-deep-investigation/
tags: [revenue-investigation, research, wave-2, deep-investigation]
---

# Revenue Investigation — Wave 2 Stage 3 Deep Investigation

## Decision summary

| Candidate | Decision | Plain-English reason |
|---|---|---|
| **Sponsor proof/reporting automation** | **ADVANCE** | Small publishers repeatedly assemble sponsor reports by hand; prospect discovery is unusually automatable because sponsored newsletters/podcasts are publicly visible. |
| **Lightweight RFP requirement extractor** | **ADVANCE** | Paid competitors prove demand, but there is room below full proposal suites for a one-off extraction/checklist product aimed at occasional bidders. |
| **QR equipment handover pages via installers** | **ADVANCE** | The concept is proven, but the better business is not another facilities platform: sell a simple branded handover product through installers who can attach it to every job. |
| Specialized synthetic-data packs | **STOP** | Excellent free generators now cover realistic business datasets, referential integrity and multiple export formats. A paid pack needs a very narrow QA edge case and likely has limited upside. |
| PO/invoice discrepancy checker | **STOP** | Modern AP products already provide free/low-cost trials and full 2/3/4-way matching. Accuracy, fraud claims and accounting integrations would add support/risk inconsistent with the sprint objective. |

---

## 1. Sponsor proof/reporting automation — ADVANCE

### Product idea

A small tool/service for newsletters or podcasts that creates a clean sponsor-delivery report after an ad runs.

Instead of the publisher taking screenshots and manually copying numbers, the system produces a sponsor-ready page/PDF showing what was delivered: issue/episode, placement, audience/reach figures supplied by the publisher/platform, tracked clicks where available, links/screenshots and a short renewal summary.

### Demand evidence

- BannerTrackr explicitly describes the manual process of copying newsletter metrics and screenshots into sponsor reports, and sells sponsor-specific impression/click reporting. Source: https://bannertrackr.com/blog/newsletter-sponsor-report-template
- PodSEO includes sponsor-ready monthly reporting in paid podcast plans. Source: https://podseo.com/features/proof-and-reporting/
- Breaker markets advertiser-trust/reporting features for newsletters. Source: https://joinbreaker.ai/publishers
- Current creator discussion also describes manually compiling sponsor screenshots and performance numbers.

These competitors prove demand but also mean a generic analytics dashboard is not attractive.

### Narrow gap

**Do not build an analytics platform.** Build the simplest possible **proof-of-delivery / renewal pack** that works from uploaded exports, links and screenshots.

That avoids complex integrations at the beginning and targets publishers too small to justify an ad-server stack.

### Customer

Small sponsored newsletters and podcasts with roughly a few sponsors per month, where the creator/operator still handles ad operations personally.

### Customer acquisition advantage

Prospects are publicly observable.

- BeeDirectory currently lists hundreds of newsletters and their sponsorship information. Source: https://bee-directory.com/search
- Podcasts.ca provides a Canadian podcast directory and identifies sponsor history. Source: https://podcasts.ca/
- Podcast/newsletter archives can be scanned for sponsor language, giving a direct signal that the prospect already sells ads.

This supports a semi-automated prospect system that searches for **actual sponsors**, not merely generic creators.

### Pricing estimate

Not validated:

- CA$9–$19 per one-off report;
- CA$29–$59/month for recurring publisher use;
- CA$99–$199/month agency/multi-publication tier later.

### MVP test

No integrations. Generate three realistic sponsor-report examples and offer a free first report to 20 highly qualified publishers who visibly run sponsors. Ask for payment only for subsequent reports.

### Failure modes

- creators are satisfied with screenshots/email;
- newsletter/podcast platforms add equivalent sponsor exports;
- every platform reports incompatible metrics;
- tiny publishers do not value professional reports enough to pay;
- successful customers quickly need ad booking/invoicing/CRM, expanding scope.

### Judgment

**Advance.** Strong low-touch acquisition potential and very small MVP.

---

## 2. Lightweight RFP requirement/compliance extractor — ADVANCE

### Product idea

Upload an RFP PDF/Word file and receive a spreadsheet containing every important requirement, deadline, mandatory form, response instruction and evidence request.

The tool does **not** write the bid initially. It reduces the risk that a small bidder misses a requirement.

### Demand evidence

- RFP Matrix currently charges roughly US$100 for a single RFP and US$150+/month for subscriptions while offering requirement extraction and response drafting. Source: https://rfpmatrix.com/
- Current RFP guidance treats a compliance matrix as a core proposal-control document. Sources: https://www.cobl.ai/blog/compliance-matrix and https://rfp-software-tools.com/templates/rfp-compliance-matrix-template

### Narrow gap

Full proposal platforms are too much product for a company that bids occasionally.

The proposed product is **one job only**: turn a long solicitation into a trustworthy review checklist with page references.

Potential differentiator:

- one-off pricing rather than subscription;
- extract-only rather than AI-written answers;
- page/source references for every requirement;
- mandatory/deadline/forms flags;
- Excel output usable by the customer's existing workflow.

### Customer

Small Canadian service/technical firms that bid on government or institutional work occasionally rather than maintaining a dedicated proposal team.

### Prospect source

Government procurement data makes active bidders identifiable.

- GovMarket exposes a searchable Canadian government-supplier directory. Source: https://www.govmarket.ca/suppliers
- CanadaBuys and public contract-award datasets expose winning suppliers/categories.

A prospecting agent can identify small firms that have won relevant contracts recently, visit their websites, and score those likely to bid again.

### Pricing estimate

Not validated:

- CA$29–$49 for a small/simple RFP;
- CA$79–$129 for a larger extraction;
- optional CA$149–$249/month later for repeated use.

### MVP test

Process 5–10 public RFPs manually/semi-automatically and validate extraction accuracy. Then show a sample matrix to 20 recent government suppliers/proposal consultants and offer a paid one-off extraction.

### Operating burden

Low if positioned as **draft extraction requiring customer review**. Higher if marketed as guaranteed bid compliance or expanded into proposal drafting.

### Failure modes

- customers simply upload RFPs to ChatGPT/Claude themselves;
- extraction misses an important mandatory requirement;
- price is too low relative to human review/support burden;
- successful customers want full proposal collaboration features;
- confidential procurement documents create storage/security expectations.

### Judgment

**Advance, but keep claims narrow.** Source citations and repeatable extraction rules must be central.

---

## 3. QR equipment handover pages via installers — ADVANCE

### Product idea

Instead of selling asset-management software to facilities teams, sell a **digital handover add-on to installers**.

After an HVAC/plumbing/mechanical installation, the contractor puts one QR label on the installed unit. Scanning it opens a branded page containing the correct manual, warranty information, installer contact, model/serial number and basic service information.

### Market evidence

- ARC Facilities already provides QR access to equipment manuals, warranties, parts and service history, proving the workflow is useful. Source: https://www.arcfacilities.com/product/equipment/qr-codes-for-equipment-and-assets
- OpenQR describes the same equipment-manual use case and charges for dynamic QR capacity. Source: https://openqr.uk/solutions/asset-tagging/equipment-manuals

### Narrow gap

Do not compete with full facilities software.

The product is a **white-label customer handover/aftercare page** that helps installers look professional and keeps their service contact attached to the equipment they installed.

This changes the payer and value proposition:

- installer buys it;
- installer can include it in every installation;
- end customer uses it free;
- QR page can drive future service calls back to the installer.

### Customer

Independent HVAC/mechanical contractors doing replacement/installation work.

### Prospect availability

Prospect pools are straightforward:

- BC Plumbing & HVAC Association currently lists 53+ active members. Source: https://bcpha.org/members
- Mechanical Contractors Association of Canada has a directory with hundreds of members. Source: https://members.mcac.ca/member-directory/Find
- MCABC and RSES also maintain contractor/member directories.

### Pricing estimate

Not validated:

- CA$2–$5 per installed asset/page at volume;
- or CA$29–$79/month including a fixed number of active equipment pages;
- agency/installer branding included.

### MVP test

Create three demo equipment pages and printable QR labels using public manufacturer manuals. Show them to 20 independent HVAC installers and ask whether they would add the page/label to a real installation for a small paid pilot.

### Automation

High:

- installer uploads/pastes model/serial/customer-safe details;
- system finds or attaches supplied manual;
- generates branded page;
- generates QR/label PDF;
- reminders can later prompt warranty/service events.

Human review may be needed when matching a manual to a model.

### Failure modes

- contractors see no revenue benefit;
- customers rarely scan the code;
- every installation requires too much manual document hunting;
- manufacturers already provide strong QR/manual systems;
- storing customer/job details creates unnecessary privacy/security burden.

### Judgment

**Advance.** Best version is a simple aftercare/marketing add-on, not asset management.

---

## 4. Specialized synthetic test-data packs — STOP

Generic generators are now abundant and free. Postman and browser tools already generate realistic users, orders, transactions, invoices and related datasets. Some tools support reproducible data and referential integrity.

Sources:
- https://www.postman.com/tools/test-data-generator
- https://www.data-generator.io/
- https://seedbase.dev/sandbox

A viable paid product would need a highly specific test corpus such as a regulated document edge-case set or known parser failure suite. That may be useful later, but it is too narrow/uncertain for priority research.

---

## 5. PO/invoice discrepancy checker — STOP

The market already ranges from free extraction/matching allowances to full SMB tools around US$99/month and large AP platforms.

Examples:
- Lido offers automated PO/invoice/receipt matching with free page allowance. Source: https://www.lido.app/automations/match-purchase-orders-to-invoices
- MatchLedger markets four-way SMB matching around US$99/month. Source: https://matchmyledger.com/
- Finofo and other platforms provide full AP matching/approval workflows. Source: https://www.finofo.com/platform/accounts-payable

A tiny file-upload tool would have to compete on price while still carrying high accuracy/trust expectations. Stop for this workstream.

---

## Stage 4 candidates

Proceed to implementation planning for:

1. **Sponsor proof/report generator**;
2. **RFP requirement extractor**; and
3. **Installer QR handover pages**.

Each plan must include the previously agreed semi-automated customer-acquisition system and stop before significant development.

## Verification record

- Last verified: 2026-10-16
- Stage 3 status: complete
- Pricing is estimated unless explicitly attributed to a competitor.
- Exact demand/conversion remains unvalidated.
