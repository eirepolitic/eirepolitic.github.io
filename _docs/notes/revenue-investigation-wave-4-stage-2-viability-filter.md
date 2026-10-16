---
title: Revenue Investigation — Wave 4 Stage 2 E-commerce Viability Filter
summary: Evidence-based screening of 20 e-commerce candidates from the fourth 60-idea pool.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 223
permalink: /projects/notes/revenue-investigation-wave-4-stage-2-viability-filter/
tags: [revenue-investigation, research, ecommerce, wave-4, viability]
---

# Revenue Investigation — Wave 4 Stage 2 Viability Filter

## Method

Same screening dimensions as prior waves: startup cost, speed to first revenue, low ongoing human effort, automation potential, low legal/platform risk and upside. Higher is better. Scores are estimates, not validated economics.

## Evidence that changed the filter

- Amazon Canada SAFE-T claims have defined evidence and timing requirements, including a 30-day filing window and response deadlines. This creates a real administrative-loss problem, but the product must stay within Amazon's rules and cannot promise reimbursement. Source: https://sellercentral.amazon.ca/help/hub/reference/external/G202175000?locale=en-CA
- Generic parcel-audit software is already mature and often works on contingency. That weakens a broad shipping-audit product but leaves room for a narrower merchant-facing diagnostic or 3PL invoice checker. Source: https://www.auditshipment.com/blog/parcel-audit-software-comparison-2026
- Shopify's discount ecosystem is extremely crowded; the App Store currently lists more than 1,000 apps with discount-stacking features, including apps explicitly marketed around margin protection. Generic promotion-conflict detection is therefore rejected. Source: current Shopify App Store discount-stacking category.
- Generic quote-to-cart is already inexpensive: current Shopify apps begin below US$10/month and directly support accepted quotes becoming checkout-ready orders. Source: https://apps.shopify.com/request-quote-w3
- Product information management and catalog-quality software is a mature category. Shopify itself now frames PIM/product-data quality as core infrastructure for AI-ready commerce. Sources: current Shopify 2026 PIM/product-data guidance.
- Generic AI-shopping readiness audits already have free/open-source and paid competitors. Current examples include a US$99 catalog audit, open-source audit tooling and agencies selling readiness audits. This removes W4-L1 as a priority despite the market being new.
- AI-referred shopping is nevertheless material: Shopify reports AI-referred orders grew sharply in Q1 2026 and AI-referred shoppers converted better than organic-search referrals. That keeps narrower AI-answer accuracy monitoring interesting. Source: current Shopify 2026 product-data guidance.

## Scorecard

| Candidate | Cost | Speed | Low effort | Automation | Low risk | Upside | Total | Decision |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **W4-C1 Amazon SAFE-T evidence packer** | 5 | 4 | 4 | 5 | 3 | 4 | **25** | **Advance** |
| **W4-F5 3PL billing variance checker** | 4 | 3 | 4 | 5 | 5 | 4 | **25** | **Advance** |
| **W4-F3 DIM-weight packaging optimizer** | 4 | 3 | 4 | 5 | 5 | 4 | **25** | **Advance** |
| **W4-L5 AI product-answer accuracy monitor** | 5 | 3 | 4 | 5 | 4 | 4 | **25** | **Advance, narrow scope** |
| **W4-C4 unauthorized listing-change evidence monitor** | 4 | 4 | 4 | 5 | 4 | 3 | **24** | **Advance for Stage 3** |
| W4-B2 product-spec contradiction checker | 4 | 3 | 4 | 5 | 5 | 3 | 24 | Hold only as narrower add-on; PIM/data-quality market is mature |
| W4-F1 shipping surcharge audit | 4 | 4 | 4 | 5 | 5 | 3 | 25 | Reject generic version; parcel-audit market mature |
| W4-F4 carrier claim evidence packer | 4 | 4 | 4 | 5 | 4 | 3 | 24 | Deprioritize; parcel recovery/claims tools already common |
| W4-G1 promotion-overlap conflict detector | 5 | 5 | 5 | 5 | 5 | 1 | 26 | Reject; extremely crowded Shopify category |
| W4-I1 quote-to-cart converter | 5 | 5 | 5 | 4 | 5 | 1 | 25 | Reject; strong low-cost Shopify incumbents |
| W4-L1 AI-shopping catalog readiness audit | 5 | 5 | 5 | 5 | 5 | 2 | 27 | Reject generic version; category already forming rapidly |
| W4-B1 variant-image mismatch auditor | 5 | 4 | 4 | 5 | 5 | 2 | 25 | Deprioritize; likely feature rather than standalone business |
| W4-C2 reimbursement deadline tracker | 5 | 4 | 5 | 5 | 4 | 2 | 25 | Fold into SAFE-T/evidence product |
| W4-D4 warranty-claim intake packer | 4 | 3 | 4 | 5 | 4 | 3 | 23 | Deprioritize; overlaps mature warranty/RMA software |
| W4-D5 return-reason-to-PDP fix report | 5 | 4 | 4 | 5 | 5 | 2 | 25 | Useful feature but low differentiation from returns analytics |
| W4-E2 subscription stock-risk guard | 4 | 3 | 4 | 5 | 5 | 3 | 24 | Deprioritize; subscription platforms increasingly cover inventory/forecasting |
| W4-H1 product-seeding ROI reconciler | 4 | 3 | 3 | 5 | 4 | 4 | 23 | Hold; influencer/creator management category already crowded |
| W4-J1 pre-purchase question miner | 5 | 4 | 4 | 5 | 5 | 2 | 25 | Feature-level opportunity; helpdesk/review tools increasingly provide insight clustering |
| W4-K3 landed-cost drift monitor | 4 | 3 | 4 | 5 | 5 | 3 | 24 | Deprioritize; broad inventory/accounting tools can absorb it |
| W4-A2 bundle compatibility validator | 4 | 3 | 4 | 5 | 4 | 3 | 23 | Hold only for a very narrow compatibility-heavy category |

## Stage 3 shortlist

Advance five:

1. **Amazon SAFE-T / seller reimbursement evidence workflow**;
2. **3PL billing variance checker**;
3. **DIM-weight / packaging-cost optimizer**;
4. **AI product-answer accuracy monitor**; and
5. **marketplace listing-change evidence monitor**.

## Plain-English Stage 2 recap

Wave 4 started with 60 e-commerce ideas. Twenty looked strong enough to check seriously. Most of the obvious Shopify-style apps were removed because there are already many cheap competitors.

The survivors are mostly products that help a merchant **recover money, stop hidden costs, or prove something went wrong**. That is encouraging because the financial value is easier to explain than for a generic productivity app.

## Verification record

- Last verified: 2026-10-16
- Stage 2 status: complete
- Exact customer demand and conversion remain unvalidated.
