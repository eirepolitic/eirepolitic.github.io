---
title: Revenue Investigation — Wave 4 Stage 3 E-commerce Deep Investigation
summary: Deep investigation of five Wave 4 e-commerce finalists, reducing them to three Stage 4 candidates.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 224
permalink: /projects/notes/revenue-investigation-wave-4-stage-3-deep-investigation/
tags: [revenue-investigation, research, ecommerce, wave-4, deep-investigation]
---

# Revenue Investigation — Wave 4 Stage 3 Deep Investigation

## Decision summary

| Candidate | Decision | Plain-English reason |
|---|---|---|
| **Amazon SAFE-T claim/evidence workflow** | **ADVANCE** | Amazon has strict claim windows and evidence requirements. A small seller tool can save real money without becoming a full marketplace platform. |
| **AI product-answer accuracy monitor** | **ADVANCE** | Generic AI-readiness audits are already crowded, but monitoring whether AI assistants give wrong product answers is a narrower ongoing problem tied to brand accuracy. |
| **DIM-weight / packaging-cost optimizer** | **ADVANCE CAUTIOUSLY** | Packaging cost is real and measurable, but generic cartonization software already exists. The viable version must target smaller merchants that only need an occasional diagnostic rather than warehouse software. |
| 3PL billing variance checker | **STOP** | Current competitors now offer nearly the exact invoice-versus-contract audit, including fixed-fee and contingency models. Entry evidence is weak despite strong demand. |
| Amazon listing-change evidence monitor | **STOP** | SellerSonar and other tools already monitor titles, bullets, descriptions and images at low monthly prices. |

## 1. Amazon SAFE-T claim/evidence workflow — ADVANCE

### Product

A small workflow that helps Amazon seller-fulfilled merchants identify potentially eligible reimbursement cases, gather the required evidence and avoid missing Amazon's deadlines.

It should **not** automatically assert that a seller is entitled to reimbursement. It prepares a reviewable packet and deadline queue.

### Current evidence

Amazon Canada's current SAFE-T policy gives eligible seller-fulfilled sellers a 30-day filing window in relevant cases and requires sufficient documentation. Amazon may also require a response within seven days during investigation. Source: https://sellercentral.amazon.ca/help/hub/reference/external/G202175000?locale=en-CA

This means missed deadlines or incomplete evidence can directly cost a merchant money.

### Narrow customer

Small-to-mid-size Amazon FBM/SFP sellers with enough return volume that SAFE-T administration is recurring, but not large enough to have dedicated reimbursement staff/software.

### Product boundary

- import/export data and seller-supplied evidence;
- deadline and eligibility checklist;
- order-specific evidence packet;
- draft factual claim summary;
- follow-up reminder if Amazon requests more evidence;
- no automated submission without seller review;
- no promise of reimbursement.

### Pricing estimate

Not validated:

- CA$29–$79/month depending on claim volume; or
- low per-case pricing such as CA$5–$15 per prepared packet.

### Acquisition

Potential prospect sources include Amazon seller communities, agencies, prep centres, FBM service providers and public brand/storefront discovery. Direct seller email discovery is less clean than agency prospecting, so partnerships/referrals may be especially valuable.

### Main risks

- Amazon could change workflow or expose better native automation;
- seller exports may not contain enough evidence;
- merchants may prefer contingency recovery services;
- policy interpretation creates platform/account risk if handled carelessly.

### Minimum test

Work through 10–20 historical/publicly described SAFE-T cases using Amazon's current rules and a mock packet format. Then interview/offer free packet preparation to a small number of FBM sellers or Amazon agencies.

### Judgment

**Advance.** Strong money-recovery value, but compliance with Amazon policy must be deterministic and conservative.

---

## 2. AI product-answer accuracy monitor — ADVANCE

### Product

A recurring monitor that asks AI-shopping/search tools common questions about a merchant's products and checks whether the answers match the merchant's verified product facts.

Example: a brand sells a waterproof backpack. The system periodically asks questions such as capacity, waterproof rating, laptop size, return policy and compatible use cases, then flags answers that are wrong, missing or unsupported.

### Why this is different from an AI-readiness audit

A readiness audit asks: “Is your catalog structured properly?”

This product asks: **“What are AI assistants actually telling shoppers about your products right now, and is it correct?”**

That is ongoing monitoring rather than a one-time score.

### Current evidence

Shopify's 2026 guidance emphasizes that product data must increasingly be machine-readable because AI tools are influencing product discovery and purchase decisions. AI-referred orders grew strongly in 2026. Source: current Shopify 2026 product-data guidance.

Generic AI-commerce readiness products already exist, including paid and open-source audit tools, so a broad audit is not recommended. Current monitoring vendors also track brand/product visibility in AI answers, proving the category is forming.

### Exact first customer

Small/mid-size brands with **technical or specification-heavy products** where a wrong AI answer can directly cause lost sales or returns—for example outdoor equipment, electronics accessories, tools or specialty home products.

### MVP boundary

- merchant provides 10–50 verified product facts;
- system defines a fixed question set;
- monitor a small number of supported AI/search surfaces;
- capture answer + date/source;
- compare statements to verified facts;
- classify correct / missing / questionable / incorrect;
- send a concise weekly/monthly report.

Do not attempt to manipulate or “optimize” AI rankings in the MVP.

### Pricing estimate

Not validated:

- CA$49–$99/month for a small catalog/limited query set;
- agency tier later if monitoring proves useful.

### Acquisition advantage

Prospects can be semi-automatically identified from Shopify/DTC brand directories and public catalogs. Product complexity can be scored automatically: more specifications, compatibility rules and technical claims imply higher risk from incorrect AI answers.

A personalized sample can test 3–5 public product questions and show the brand any discrepancy found.

### Main risks

- AI answer surfaces change frequently;
- automated querying may face terms/rate restrictions;
- answers can vary by location/session;
- brands may care about visibility more than factual accuracy;
- attribution between a corrected catalog and improved AI answer may be hard to prove.

### Minimum test

Choose 20 product brands with specification-heavy catalogs, run a controlled sample question set, and determine whether material answer errors are common enough to create a saleable report.

### Judgment

**Advance.** Novel enough to retain, but it needs a conservative technical/terms review before any automated large-scale querying.

---

## 3. DIM-weight / packaging-cost optimizer — ADVANCE CAUTIOUSLY

### Product

A merchant uploads order history, product dimensions and box sizes. The service shows which orders are paying avoidable dimensional-weight charges and suggests smaller box choices or packaging changes.

### Evidence

Shopify documents dimensional weight as a carrier billing factor for major carriers including FedEx, UPS and Canada Post. Source: https://help.shopify.com/en/manual/fulfillment/setup/packaging/packages-and-weights

Cartonization and box-optimization products already exist, including free tools and larger warehouse/WMS products. Therefore the opportunity is **not** another full packing engine.

### Narrow gap

Sell a **periodic savings diagnostic** to merchants shipping enough parcels to feel DIM cost but too small to buy warehouse optimization software.

Example output:

- “These 4 box sizes caused most DIM-weight loss last quarter.”
- “Replacing box B with a smaller standard carton for these SKUs would have reduced billable weight on X% of affected orders.”

### Customer

Shopify/DTC merchants shipping bulky but light products: home goods, supplements multipacks, apparel bundles, hobby products, accessories.

### Pricing estimate

Not validated:

- CA$49–$149 one-off diagnostic;
- optional CA$29–$59/month monitoring later.

### Main risks

- merchant data may lack accurate package dimensions;
- damage/fragility constraints make theoretical smaller boxes unusable;
- free calculators cover very small sellers;
- large sellers already have WMS/cartonization software.

### Minimum test

Take one real/synthetic order export plus merchant box catalog and produce a savings report manually. Validate whether the suggested savings are large enough to support at least a CA$50–$100 diagnostic price.

### Judgment

**Advance cautiously.** This is attractive only as a simple diagnostic product for the “too small for WMS software” segment.

---

## 4. 3PL billing variance checker — STOP

The market is now visibly crowded. Current products such as WareAudit, Auditario, billsharp and others already audit 3PL invoices against rate cards/contracts and produce dispute evidence, with pricing ranging from fixed monthly fees to recovery-share models.

Examples:
- https://wareaudit.com/
- https://auditario.com/
- https://www.billsharp.co/

This is strong proof that the problem is valuable, but a weak reason to enter now without a much narrower niche.

---

## 5. Amazon listing-change monitor — STOP

SellerSonar currently monitors Amazon title, bullets, descriptions, brand and images and offers entry pricing around US$20/month for hundreds of ASINs. Source: https://sellersonar.com/alerts/content-changes/

That directly overlaps the proposed Wave 4 concept, so it is removed.

## Stage 4 candidates

Proceed to implementation planning for:

1. Amazon SAFE-T evidence workflow;
2. AI product-answer accuracy monitoring; and
3. DIM-weight packaging savings diagnostic.

No development should begin before the Stage 4 plans are reviewed.

## Plain-English Stage 3 recap

Five ideas survived the first filter. Two were dropped because current competitors already offer almost exactly the same service. The three left are all e-commerce problems tied to money: recovering Amazon reimbursements, preventing bad AI product information, and reducing shipping cost caused by oversized packaging.

## Verification record

- Last verified: 2026-10-16
- Stage 3 status: complete
- Pricing estimates remain unvalidated.
