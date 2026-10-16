---
title: Revenue Investigation — Wave 5 Stage 1 Inbound-Distribution Idea Pool
summary: Fifth pool of 60 low-touch online business ideas designed around marketplaces, app stores, search-driven discovery and self-serve distribution rather than continuous outbound prospecting.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 226
permalink: /projects/notes/revenue-investigation-wave-5-stage-1-inbound-distribution-idea-pool/
tags: [revenue-investigation, research, inbound, marketplaces, self-serve, automation, wave-5]
---

# Revenue Investigation — Wave 5 Stage 1 Inbound-Distribution Idea Pool

## Purpose

Wave 5 changes the commercial constraint. The product should be discoverable primarily through an existing marketplace, app directory, search traffic, or self-serve product page. Ongoing cold outreach should not be required for the business to work.

Ideas can still use small amounts of outreach for initial validation, but Stage 2 will heavily penalize concepts that require continuous lead chasing.

## Current distribution facts

- Atlassian supports paid Marketplace apps and, as of October 2026, publishes revenue-sharing terms for Forge/Connect apps. Source: https://developer.atlassian.com/platform/marketplace/pricing-payment-and-billing/
- GitHub Marketplace supports paid Apps with flat-rate or per-unit monthly/annual plans and handles customer billing once publisher requirements are met. Source: https://docs.github.com/en/apps/github-marketplace/selling-your-app-on-github-marketplace/pricing-plans-for-github-marketplace-apps
- Canva supports external-paid apps and an approved Premium Apps Program with usage-based developer compensation. Source: https://www.canva.dev/docs/apps/monetization/
- Apify allows paid Actors with pay-per-event and other marketplace pricing models. Source: https://docs.apify.com/actors/publishing/monetize
- WordPress permits SaaS-backed plugins in its plugin directory, subject to its commercial/plugin guidelines. Source: https://developer.wordpress.org/plugins/wordpress-org/detailed-plugin-guidelines/
- Chrome extensions can charge externally, but current policies require transparent payments, privacy disclosures and narrow data collection tied to the extension's single purpose. Sources: https://developer.chrome.com/docs/webstore/program-policies and https://developer.chrome.com/blog/cws-policy-updates-2026

These facts validate distribution channels, not the individual ideas below.

## 60-idea pool

### A. Atlassian Marketplace apps

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-A1 | Jira attachment hygiene app | Detects duplicate, oversized, stale or badly named attachments and creates cleanup queues | Jira admins/teams | Reduces clutter/storage confusion | Atlassian Marketplace; scheduled scans and cleanup suggestions |
| W5-A2 | Jira due-date realism checker | Flags due dates that are inconsistent with dependency dates or unresolved blockers | Project teams | Prevents obviously impossible plans | Marketplace; rule-based dependency analysis and digest |
| W5-A3 | Confluence orphan-page finder | Finds pages with no meaningful incoming links, owner or recent use | Knowledge-base teams | Makes forgotten content visible | Marketplace; graph/activity analysis |
| W5-A4 | Confluence table normalizer | Standardizes inconsistent tables into reusable structured layouts/exports | Ops/documentation teams | Saves repetitive table cleanup | Marketplace; page parsing and one-click normalization |
| W5-A5 | Jira customer-ready release digest | Converts selected completed issues into a sanitized release summary without exposing internal ticket detail | Small SaaS teams | Saves manual release-note preparation | Marketplace; issue filtering, summarization and export |

### B. GitHub Marketplace apps / Actions

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-B1 | README example verifier | Runs code examples in README/docs and flags examples that no longer work | Open-source/commercial dev teams | Prevents stale documentation | GitHub Marketplace/Action; CI execution and PR comments |
| W5-B2 | Screenshot freshness bot | Detects UI changes and opens a PR when README/docs screenshots are outdated | SaaS/open-source teams | Keeps docs visually current | GitHub Action; browser screenshots + diff + PR |
| W5-B3 | Environment-variable documentation checker | Compares code/config usage with `.env.example` and docs, flagging missing/obsolete variables | Dev teams | Prevents deployment/config confusion | Marketplace; repository scan and PR check |
| W5-B4 | Migration-file risk summary | Summarizes database migration changes in pull requests and flags destructive patterns for review | Small software teams | Makes migrations easier to review | Marketplace; SQL/ORM diff parsing and PR summary |
| W5-B5 | API example drift checker | Verifies documented API request/response examples against an OpenAPI spec or test endpoint | API teams | Stops examples drifting from reality | Marketplace; schema comparison and CI report |

### C. Canva apps

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-C1 | Branded chart-card generator | Turns CSV rows into consistent branded chart/social cards | Marketers/report publishers | Fast recurring visual production | Canva Apps; data mapping and batch generation |
| W5-C2 | Product-spec card generator | Converts product CSV/spec sheets into consistent one-page product cards | Small manufacturers/retailers | Saves catalog sheet design work | Canva Apps; data import and layout fill |
| W5-C3 | Event badge/name-card formatter | Cleans attendee CSVs and creates print-ready badge/name-card pages | Event organizers | Removes manual layout work | Canva Apps; CSV cleaning, pagination and export |
| W5-C4 | Before/after case-study board builder | Turns paired images + metrics into standardized case-study graphics | Agencies/trades/fitness brands | Makes repeatable proof graphics | Canva Apps; asset pairing and template fill |
| W5-C5 | Multilingual layout fit checker | Flags translated text that overflows or breaks Canva designs | Agencies/global teams | Reduces localization rework | Canva Apps; text bounds checks and variant queue |

### D. Chrome Web Store extensions

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-D1 | Clean table extractor | Converts messy HTML tables into clean CSV/XLSX with column detection | Analysts/researchers | Saves copy/paste cleanup | Chrome Web Store; local extraction/export |
| W5-D2 | Web form field mapper | Lets users map recurring browser form fields to a reusable profile, with explicit local-only storage | Operations staff | Speeds repetitive non-sensitive data entry | Chrome store; browser autofill with user-controlled profiles |
| W5-D3 | Citation capture extension | Saves selected web claims with title, date, source URL and quote into a research file | Students/analysts/writers | Makes source capture consistent | Chrome store; one-click structured capture |
| W5-D4 | Product-spec comparison clipper | Lets shoppers/procurement users clip product specs from pages into a side-by-side local comparison | Technical buyers | Reduces tab/spreadsheet work | Chrome store; structured clipping and compare view |
| W5-D5 | Web invoice/receipt downloader index | Tracks invoices/receipts the user downloads from vendor portals and builds a local index | Freelancers/small-business admins | Helps month-end collection | Chrome store; download metadata + local index, no credential scraping |

### E. WordPress / WooCommerce plugins

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-E1 | WooCommerce product-manual block | Adds a structured manuals/downloads block tied to product/SKU metadata | Equipment/product sellers | Makes support documents easy to find | WordPress directory → paid SaaS/add-on; automated document mapping |
| W5-E2 | WooCommerce spec-table consistency checker | Finds conflicting product attributes/spec tables across similar SKUs | Specialty stores | Prevents bad product information | Plugin discovery; scheduled audits |
| W5-E3 | WordPress stale-download detector | Finds linked PDFs/files that have old version/date signals and flags them for review | Associations/document-heavy sites | Prevents obsolete documents staying live | Plugin directory; crawl + metadata rules |
| W5-E4 | WooCommerce accessory completeness block | Shows merchant-defined “required/optional accessories” rather than generic cross-sells | Technical retailers | Reduces missing-part orders | Plugin store; deterministic compatibility rules |
| W5-E5 | WordPress evidence snapshot service | Periodically creates dated screenshots/PDF evidence of selected public pages | Agencies/regulated-content teams | Keeps publication history | Free plugin + SaaS; scheduled capture/archive |

### F. Shopify App Store micro-apps

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-F1 | SKU naming convention auditor | Flags SKUs that violate a merchant-defined naming pattern | Growing Shopify stores | Prevents catalog/warehouse inconsistency | Shopify App Store; scheduled catalog checks |
| W5-F2 | Product-weight anomaly checker | Flags implausible/missing weights that can cause shipping-rate errors | Physical-goods merchants | Prevents fulfillment surprises | App Store; catalog statistics and exceptions |
| W5-F3 | Variant-option order checker | Finds products where option order/labels are inconsistent across the catalog | Apparel/configurable-product stores | Improves storefront consistency | App Store; catalog scan and fix queue |
| W5-F4 | Product-archive evidence exporter | Exports a dated product snapshot before products are archived/deleted | Regulated/seasonal brands | Keeps historical product evidence | App Store; scheduled/manual snapshot export |
| W5-F5 | Collection-rule explainer | Converts automated collection rules into a simple human-readable report and flags overlapping/conflicting rules | Larger Shopify catalogs | Makes merchandising logic easier to audit | App Store; rule parsing and diagnostics |

### G. Zapier / automation-directory integrations

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-G1 | Public-dataset connector | Maintained connector exposing one awkward government/open dataset as Zapier triggers/actions | Ops/research users | Avoids custom API work | Zapier directory; API normalization and scheduled triggers |
| W5-G2 | Document checksum/version connector | Trigger when a watched public document changes hash/version and pass metadata downstream | Compliance/research teams | Simple document monitoring inside existing workflows | Zapier directory; polling and version detection |
| W5-G3 | Structured-email parser connector | Turns one narrow recurring email format into clean fields for downstream Zaps | SMB operations | Eliminates manual copy/paste | Zapier directory; deterministic parser templates |
| W5-G4 | CSV validation connector | Accepts a CSV and returns pass/fail plus row-level validation errors based on reusable schemas | Ops/data teams | Adds validation before automations continue | Zapier directory; schema engine |
| W5-G5 | Business-hours/SLA calculator connector | Calculates business-time deadlines using configurable calendars/holidays | Support/ops teams | Avoids custom date logic | Zapier directory; rules engine |

### H. Apify Store Actors

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-H1 | Public PDF table extractor Actor | Takes public PDF URLs and returns normalized tables/CSV | Researchers/data teams | Saves repeated extraction work | Apify Store; pay per document/table |
| W5-H2 | Sitemap inventory Actor | Crawls a sitemap and outputs page type, metadata, status and content-size inventory | Agencies/site owners | Quick site inventory without full crawler setup | Apify Store; pay per page |
| W5-H3 | Product-manual metadata Actor | Given manufacturer manual URLs, extracts model numbers, revision dates and document metadata | Retailers/data teams | Automates document cataloging | Apify Store; pay per document |
| W5-H4 | Public meeting agenda/minutes Actor | Converts municipal/board agenda pages into structured dates, topics and document links | Researchers/local businesses | Avoids repeated portal checking | Apify Store; source-specific structured output |
| W5-H5 | Public directory dedupe Actor | Takes a directory URL/list and returns normalized organization names/domains with duplicates grouped | Researchers/marketers | Cleans public directory data | Apify Store; pay per record |

### I. Search-driven self-serve web utilities

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-I1 | CSV delimiter/encoding repair tool | Fixes broken encodings, delimiters, quotes and line endings in uploaded CSVs | General business/data users | Common painful file problem | SEO/inbound; free preview + paid large-file/batch export |
| W5-I2 | Excel leading-zero preservation converter | Converts IDs/postal/product codes safely between CSV/XLSX without stripping leading zeros | Ops/accounting/e-commerce users | Prevents silent identifier corruption | SEO/inbound; self-serve conversion |
| W5-I3 | Date-format ambiguity detector | Finds ambiguous dates and converts them to a chosen standard with exception review | International data users | Avoids month/day errors | Search utility; file upload and deterministic conversion |
| W5-I4 | PDF page-label renumbering utility | Renumbers page labels/bookmarks without changing visible pages | Legal/research/document users | Solves awkward PDF housekeeping | Search utility; local/server processing |
| W5-I5 | UTM campaign naming builder/validator | Generates and validates links against a saved naming convention | Small marketers | Prevents inconsistent analytics tags | SEO/inbound; free single use + paid saved schemas/bulk mode |

### J. Developer-facing self-serve APIs

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-J1 | Holiday/business-day API for Canadian jurisdictions | Returns statutory/business-day calendars with provenance and update dates | Developers/ops software | Avoids maintaining calendars | API directories/search; subscription/usage billing |
| W5-J2 | Canadian postal-code formatting/validation API lite | Normalizes syntax/province inference without claiming deliverability | Developers/form builders | Simple Canada-specific normalization | API marketplace/search; pay per request |
| W5-J3 | NAICS/NOC/industry-code lookup API | Search/normalize Canadian/US business/occupation classification codes | Developers/data teams | Saves maintaining classification datasets | API directory; usage billing |
| W5-J4 | Unit/packaging conversion API for commerce | Converts dimensional/weight/package units with rounding rules and metadata | E-commerce/dev tools | Removes recurring conversion bugs | API marketplaces/search; per request |
| W5-J5 | Public-source attribution formatter API | Converts source metadata into standard human-readable attribution/citation strings | Data publishers | Automates attribution requirements | API directory; usage billing |

### K. Marketplace-ready digital utilities / downloadable tools

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-K1 | CSV QA workbook + local checker bundle | Downloadable workbook/script that validates common business CSV problems offline | Analysts/admins | No subscription or data upload needed | Gumroad/Lemon Squeezy/search; instant delivery |
| W5-K2 | Product-spec normalization dictionary pack | Maintained mapping dictionaries for common units/attribute aliases in one niche | Catalog/data teams | Saves building normalization rules | Digital marketplace; versioned downloads |
| W5-K3 | E-commerce test-order fixture pack | Realistic synthetic order/refund/fulfillment CSVs for Shopify/WooCommerce QA | Developers/agencies | Faster testing without live customer data | Developer marketplaces/search; versioned pack |
| W5-K4 | Public-procurement sample-document corpus | Curated public RFP/addendum/award document set for training/testing extraction workflows | Proposal-tech developers/researchers | Saves collecting representative documents | Digital marketplace; licensed/source-attributed bundle |
| W5-K5 | Canadian address edge-case test pack | Synthetic Canadian address/postal cases for form/import QA | Developers/SaaS teams | Finds validation bugs | Digital marketplace/search; instant download |

### L. Self-serve niche generators with organic discovery

| ID | Idea | What it sells | Who pays | Why pay | Distribution / automation |
|---|---|---|---|---|---|
| W5-L1 | Equipment QR handover page generator | Self-serve version of the earlier QR concept: user creates a branded manual/service QR page without sales contact | Installers/DIY equipment sellers | Immediate useful output | Search/marketplace; pay per page or bundle |
| W5-L2 | Sponsor report generator | Self-serve version of Wave 2: publisher uploads stats and receives sponsor-ready report | Newsletter/podcast creators | No agency/sales call required | SEO/creator communities; pay per report/subscription |
| W5-L3 | RFP compliance-matrix self-serve tool | Upload public/private RFP and receive cited Excel checklist | Occasional bidders | One-off utility instead of sales process | Search/paid search/marketplaces; pay per document |
| W5-L4 | DIM-weight savings calculator + file audit | Free calculator attracts merchants; paid upload analyzes historical shipments | E-commerce merchants | Immediate shipping-cost diagnostic | SEO/inbound; free-to-paid funnel |
| W5-L5 | Importer-report self-serve lookup | Search a Canadian product category and buy/download a clean importer intelligence pack | Exporters/brokers/researchers | Avoids custom order/sales interaction | SEO/search pages; pay per report |

## Categories represented

Wave 5 uses 12 distribution-led families:

1. Atlassian Marketplace apps;
2. GitHub Marketplace apps/actions;
3. Canva apps;
4. Chrome extensions;
5. WordPress/WooCommerce plugins;
6. Shopify App Store micro-apps;
7. Zapier/integration-directory connectors;
8. Apify Store Actors;
9. search-driven self-serve utilities;
10. developer APIs;
11. downloadable technical utilities/data packs; and
12. self-serve versions of earlier validated concepts.

## Deliberate differences from Waves 1–4

- The primary design criterion is **inbound or marketplace distribution**, not outbound sales efficiency.
- Earlier strong ideas are only reused when the business model changes materially from bespoke/outbound to true self-service (W5-L1–L5).
- Generic template stores, newsletters, directories, affiliate sites, generic data dashboards and generic Shopify optimization apps remain excluded.
- Marketplace publication, SEO discoverability, free-to-paid utility funnels and built-in billing are treated as part of viability.

## Recommended Stage 2 candidates

Advance these 20 for evidence-based filtering:

- W5-A1 Jira attachment hygiene;
- W5-A3 Confluence orphan-page finder;
- W5-B1 README example verifier;
- W5-B3 environment-variable documentation checker;
- W5-B5 API example drift checker;
- W5-C5 Canva multilingual layout fit checker;
- W5-D1 clean table extractor;
- W5-D3 citation capture extension;
- W5-E3 WordPress stale-download detector;
- W5-F2 Shopify product-weight anomaly checker;
- W5-G1 public-dataset Zapier connector;
- W5-G4 CSV validation connector;
- W5-H3 product-manual metadata Actor;
- W5-I1 CSV encoding/delimiter repair;
- W5-I2 leading-zero preservation converter;
- W5-J1 Canadian business-day API;
- W5-J3 NAICS/NOC lookup API;
- W5-L2 sponsor report self-serve generator;
- W5-L3 RFP compliance-matrix self-serve tool; and
- W5-L5 importer-report self-serve lookup.

## Verification record

- Last verified: 2026-10-16
- Stage 1 status: complete
- Demand for individual ideas: not yet validated
- Distribution channels verified against current Atlassian, GitHub, Canva, Apify, WordPress and Chrome documentation.
