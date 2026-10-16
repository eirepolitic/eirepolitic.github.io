---
title: Revenue Investigation — Wave 5 Stage 2 Viability Filter
summary: Evidence-based filtering of Wave 5 distribution-first ideas, emphasizing marketplace or search discovery and low dependence on outbound sales.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 227
permalink: /projects/notes/revenue-investigation-wave-5-stage-2-viability-filter/
tags: [revenue-investigation, research, inbound, marketplaces, self-serve, wave-5]
---

# Wave 5 Stage 2 — Viability Filter

## Scoring

Scored 20 candidates on: built-in/inbound distribution, pain severity, willingness to pay, implementation simplicity, maintenance burden, competitive crowding and ability to validate without sustained cold outreach.

## Findings that changed scores

- GitHub Marketplace already contains documentation-example validators, which lowers novelty for README example verification.
- Chrome Web Store already has capable table-extraction extensions, including CSV/XLSX/JSON export, so a generic table extractor is crowded.
- Zapier Formatter already handles many common data-normalization tasks; a generic CSV-validation connector needs a much narrower wedge.
- RFP compliance-matrix generation is clearly monetizable, but several free and paid products already exist, including free browser tools and paid products around US$100 per one-off RFP or US$150–$500/month.
- Canada's Canadian Importers Database is current, public and downloadable. It explicitly provides importer lists by product, city and country. That makes raw-data resale weak, but creates room for convenience, cleanup and packaged analysis.
- The 2024 CID open dataset warns that Excel can strip leading zeros from HS codes, directly confirming the broader "identifier corruption" pain behind the leading-zero preservation utility.

## Ranking

| Rank | Idea | Distribution | Competition | Build/maintenance | Monetization | Verdict |
|---|---|---|---|---|---|---|
| 1 | I2 Excel/CSV leading-zero preservation converter | Strong SEO/self-serve | Moderate, fragmented | Very low | One-off + batch subscription | Advance |
| 2 | L5 importer-report self-serve lookup | Strong search/data pages | Moderate; government source is free | Low-medium | Pay-per-report / credits | Advance |
| 3 | J1 Canadian business-day API | API/search distribution | Moderate | Low-medium, recurring updates | Usage/subscription | Advance |
| 4 | B3 environment-variable documentation checker | GitHub distribution | Moderate | Low | Free Action + paid team features | Advance |
| 5 | L2 sponsor report self-serve generator | Creator SEO/community | Moderate | Low | Per-report / subscription | Advance |
| 6 | I1 CSV delimiter/encoding repair | Strong SEO | High | Very low | Freemium/batch | Advance cautiously |
| 7 | H3 product-manual metadata Actor | Apify built-in discovery | Low-moderate | Medium | Pay per run | Advance cautiously |
| 8 | F2 Shopify product-weight anomaly checker | App Store | Moderate | Medium | Monthly app fee | Advance cautiously |
| 9 | C5 Canva multilingual layout fit checker | Canva discovery | Low-moderate | Medium-high | Canva/external billing | Hold |
| 10 | E3 WordPress stale-download detector | Plugin directory | Moderate | Medium | Freemium/SaaS | Hold |
| 11 | B5 API example drift checker | GitHub | Moderate | Medium | Subscription | Hold |
| 12 | G1 public-dataset Zapier connector | Zapier directory | Dataset-dependent | Medium | Subscription | Hold |
| 13 | A3 Confluence orphan-page finder | Atlassian Marketplace | Moderate-high | Medium | Monthly app fee | Hold |
| 14 | A1 Jira attachment hygiene | Atlassian Marketplace | Moderate-high | Medium | Monthly app fee | Hold |
| 15 | J3 NAICS/NOC lookup API | API/search | Moderate | Medium updates | Usage | Hold |
| 16 | D3 citation capture extension | Chrome Store | High | Low-medium | Freemium | Drop |
| 17 | D1 clean table extractor | Chrome Store | High and direct | Low | Hard to differentiate | Drop |
| 18 | G4 CSV validation connector | Zapier | High substitution | Low-medium | Weak | Drop |
| 19 | B1 README example verifier | GitHub | Direct existing substitute | Low | Weak differentiation | Drop |
| 20 | L3 RFP compliance-matrix self-serve tool | Search | High and price-pressured | Medium | Proven but crowded | Drop for this wave |

## Stage 3 shortlist

1. Excel/CSV leading-zero preservation converter
2. Importer-report self-serve lookup
3. Canadian business-day API
4. Environment-variable documentation checker
5. Sponsor report self-serve generator

## Sources checked

- GitHub Marketplace Actions Example Checker
- Chrome Web Store Table Extractor listings
- Zapier Formatter documentation
- Government of Canada Canadian Importers Database and Open Government 2024 CID dataset
- GovHub, TenderOS, Projectory AI, RFP Matrix and SourceGent compliance-matrix offerings

## Verification record

- Last verified: 2026-10-16
- Stage 2 status: complete
