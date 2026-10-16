---
title: Revenue Investigation — Wave 5 Stage 2 Commercial Filter
summary: Commercial viability filter for 20 inbound/self-serve opportunities, emphasizing actual monetization and customer discovery.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 227
permalink: /projects/notes/revenue-investigation-wave-5-stage-2-commercial-filter/
tags: [revenue-investigation, research, inbound, wave-5, viability]
---

# Wave 5 — Stage 2 Commercial Filter

## Decision standard

For each concept answer: **who pays, why not use a free tool, how do they find us without cold outreach, and how many buyers are required for a meaningful gross monthly target?** A marketplace listing is a *possible* discovery channel, not proof of demand. All prices below are hypotheses, in CAD, before fees, hosting and tax. Customer counts are arithmetic, not forecasts.

Target example: CA$1,000/month gross. Monthly subscribers needed = ceiling(1000 / monthly price). One-off orders needed each month = ceiling(1000 / price per order). A marketplace that does not handle billing would require our own checkout.

## Twenty-candidate commercial screen

| ID | Who pays / proposed price | Why pay rather than free? | Inbound path | Buyers/orders for CA$1k gross/mo | Decision |
|---|---|---|---|---:|---|
| A1 Jira attachment hygiene | Jira admins, $19/mo | Recurring team-wide reporting, duplicate detection | Atlassian Marketplace | 53 | Hold: platform permissions and existing cleanup apps |
| A3 Confluence orphan pages | Knowledge admins, $19/mo | Scheduled ownership/link checks and digest | Atlassian Marketplace | 53 | Hold: incumbent knowledge-management tools |
| B1 README example verifier | API/docs teams, $29/mo | Hosted multi-repo checks and PR annotations | GitHub Marketplace, Action discovery | 35 | **Advance cautiously**; many free CI alternatives |
| B3 Env-var docs checker | Dev teams, $12/mo | Scheduled cross-repo reporting vs simple scripts | GitHub Action/Marketplace | 84 | Reject: free tooling easy to reproduce |
| B5 API example drift | API teams, $39/mo | Repeatable checks with evidence/history | GitHub Action/Marketplace | 26 | **Advance cautiously**; strong free alternatives |
| C5 Canva translation layout fit | Agencies, $12/mo equivalent | Batch multilingual overflow detection | Canva Apps | 84 | Hold: API feasibility and program payout unclear |
| D1 Table extractor | Analysts, $6/mo | Saved extraction recipes/bulk export | Chrome Web Store | 167 | Reject: many free alternatives |
| D3 Citation capture | Researchers, $5/mo | Sync/export/workspace features | Chrome Web Store | 200 | Reject: strong free citation managers |
| E3 WordPress stale downloads | Associations/agencies, $29/year | Scheduled dated document audits | WordPress plugin directory/search | 414 annual sales to average $1k/mo | **Advance cautiously**; maintenance/security burden |
| F2 Shopify weight anomaly | Merchants, $9/mo | Ongoing scans, bulk alerts, audit history | Shopify App Store | 112 | **Advance cautiously**; verify whether native/bundled tools already suffice |
| G1 Public dataset connector | Automation users, $15/mo | Reliable maintained changes/triggers | Zapier directory/search | 67 | Hold: narrow dataset demand and Zapier discovery uncertain |
| G4 CSV validation connector | Operations teams, $19/mo | Saved rules, scheduled checks, audit trail | Zapier directory | 53 | Reject: common free alternatives and platform cost |
| H3 Manual metadata Actor | Catalog/data operators, $0.10/document | Reliable structured extraction in batch | Apify Store | 10,000 paid docs | **Advance cautiously**; compute margin and volume risk |
| I1 CSV encoding repair | Office users, $9 one-off | Large-file private/batch repair | Google search | 112 orders/mo | Reject: free tools and difficult SEO |
| I2 Leading-zero converter | Office users, $9 one-off | No silent ID corruption, batch validation | Google search | 112 orders/mo | Hold: useful but low willingness to pay |
| J1 Canadian business-day API | Developers, $19/mo | Maintained provincial rules and provenance | API directories/search/docs | 53 | **Advance cautiously**; correctness/liability and free APIs |
| J3 NAICS/NOC lookup API | Data developers, $19/mo | Versioned Canadian crosswalks and bulk matching | Search/API directories | 53 | Hold: public datasets and free alternatives |
| L2 Sponsor report generator | Newsletter/podcast publishers, $19/report | Branded proof and easy repeated reporting | Creator searches/marketplaces | 53 orders/mo | **Advance**; validate discoverability and need |
| L3 RFP compliance matrix | Occasional bidders, $29/document | Fast cited checklist without manual work | High-intent Google searches | 35 orders/mo | **Advance**; privacy/accuracy and search competition |
| L5 Importer report lookup | Exporters/trade researchers, $49/report | Clean niche filtering, downloadable result | Search pages by product category | 21 orders/mo | **Advance**; freshness/free-source substitution risk |

## Ranking after commercial reality check

1. **L3 self-serve RFP compliance matrix:** high-intent one-off purchase, clear before/after output, only 35 monthly purchases needed for illustrative CA$1k gross. Must prove source citations and protect uploaded confidential files.
2. **L5 self-serve importer report:** higher order value and existing public source; only 21 orders/month needed, but search demand and annual-data usefulness are unproven.
3. **L2 sponsor report generator:** easy self-serve purchase and repeat need; creator acquisition via organic search is plausible but not automatic.
4. **F2 Shopify product-weight anomaly checker:** platform-native recurring billing; requires 112 subscribers at CA$9 and app-store ranking/retention. A free tier could cost more than it converts.
5. **B5 API example drift checker:** recurring technical need, but free open-source alternatives and GitHub CI competition are formidable.

Secondary watchlist: B1 README example verifier, H3 manual metadata Actor, J1 business-day API, E3 stale-download plugin. All require stronger competitive or channel proof.

## Critical conclusion

The Shopify example is **not automatically a good business**: at $9/month it needs 112 active paying merchants just to reach CA$1,000 gross/month, and listing the app does not ensure discovery. It should rank below higher-ticket self-serve tools until search/app-store competition and merchant willingness to pay are tested.

## Stage 3 instructions

Deep-investigate L3, L5, L2, F2 and B5. Verify direct competitors, marketplace/search discovery feasibility, support burden, customer economics and a low-cost validation route. No Stage 5 development or outreach is authorized.

## Verification

Stage 2 completed 2026-10-16. Prices, conversion, search volume, demand and channel traction are hypotheses, not measured results. Platform/channel mechanics from Stage 1; competitor checks require fresh independent verification before launch.
