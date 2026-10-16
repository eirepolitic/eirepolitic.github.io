---
title: Revenue Investigation — Wave 2 Stage 1 Idea Pool
summary: Second independent pool of 60 low-touch, low-capital online business ideas, deliberately avoiding near-duplicates from the first revenue-investigation pool.
section: notes
doc_type: note
status: active
created: 2026-10-16
updated: 2026-10-16
last_verified: 2026-10-16
owner: High Director
order: 214
permalink: /projects/notes/revenue-investigation-wave-2-stage-1-idea-pool/
tags:
  - revenue-investigation
  - research
  - online-business
  - automation
  - ai-agents
  - wave-2
---

# Revenue Investigation — Wave 2 Stage 1 Idea Pool

## Purpose

Wave 2 expands the opportunity pool rather than beginning development. It adds **60 further ideas** that are materially different from the first pool or use a meaningfully different buyer, distribution channel, or value mechanism.

This is deliberately broad. No idea in this document is assumed viable until later stages.

## Current ecosystem facts used only as Stage 1 context

- Atlassian supports paid marketplace apps and, as of October 2026, pays Forge app partners under its published Marketplace revenue-sharing structure. Source: https://developer.atlassian.com/platform/marketplace/pricing-payment-and-billing/
- Canva supports public marketplace apps, external paid subscriptions, and a Premium Apps Program where approved developers can earn based on app usage. Sources: https://www.canva.dev/docs/apps/monetization/ and https://www.canva.dev/docs/apps/premium-apps/
- Shopify has mature app categories covering product-feed validation, returns analytics, catalog cleanup and many other merchant workflows, showing both demand and substantial competition. Source: https://apps.shopify.com/
- Zapier's developer platform allows companies/developers to publish integrations for APIs, providing another possible low-touch distribution channel. Source: https://help.zapier.com/hc/en-us/articles/8496275663501-Request-to-add-a-new-app-to-Zapier

These facts validate distribution mechanisms, not any specific Wave 2 opportunity.

## Pool of 60

### A. Platform-native apps and extensions

| ID | Idea | What it sells | Who pays | Why pay | What can be automated |
|---|---|---|---|---|---|
| W2-A1 | Jira release-evidence packer | Turns completed Jira work into release notes, change evidence and customer-facing summaries | Software teams | Removes repetitive release documentation | Ticket selection, summarization, grouping, formatting and scheduled exports |
| W2-A2 | Confluence terminology consistency checker | Finds conflicting names, acronyms and definitions across internal documentation | Teams using Confluence | Reduces confusing/inconsistent documentation | Page scanning, entity extraction, contradiction flags and glossary suggestions |
| W2-A3 | Canva variable-data document generator | Creates many certificates, labels, cards or localized variants from a CSV inside Canva | Educators, events, small businesses, agencies | Eliminates repetitive copy/paste design work | CSV mapping, page duplication, text/image replacement and export |
| W2-A4 | Shopify product-upload preflight | Checks a merchant's product CSV before import for broken handles, variants, images, categories and required fields | Shopify merchants/agencies | Prevents failed or messy catalog imports | CSV validation, error explanation and corrected export |
| W2-A5 | QuickBooks import preflight | Checks bank/journal/customer/vendor import files before they are uploaded | Bookkeepers and small firms | Avoids failed imports and cleanup | Schema checks, duplicates, date/currency cleanup and mapped export |

### B. E-commerce/back-office intelligence

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-B1 | Returns root-cause report | Explains which products lose the most money to returns and why | Online merchants | Helps fix costly products/listings | Import return data, group reasons, calculate loss, generate actions |
| W2-B2 | Marketplace fee reconciler | Reconciles marketplace payout/fee exports against expected sales economics | Marketplace sellers | Finds hidden fee leakage and accounting discrepancies | Import, matching, variance rules and monthly report |
| W2-B3 | Bundle profitability analyzer | Calculates real margin of bundles/kits across component costs, discounts and returns | Online sellers | Prevents unprofitable bundles | Cost ingestion, scenario calculations and alerts |
| W2-B4 | Dead-stock action planner | Identifies slow inventory and recommends discount/bundle/liquidation priorities | Small retailers | Frees cash tied up in stock | Sales-velocity analysis, age bands and action queues |
| W2-B5 | Supplier catalog normalizer | Converts messy supplier spreadsheets/PDF exports into store-ready structured catalog files | Retailers/distributors | Saves repeated manual product setup | Parsing, taxonomy mapping, image/link checks and normalized output |

### C. Revenue-path monitoring utilities

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-C1 | End-to-end lead-form monitor | Submits a synthetic enquiry and verifies the form and delivery path actually work | Agencies and lead-driven businesses | Broken forms silently lose revenue | Browser checks, synthetic submission, inbox verification and alerts |
| W2-C2 | Booking-flow smoke tester | Periodically tests whether an appointment/reservation flow can reach a valid confirmation state | Clinics, salons, service businesses, agencies | Booking failures can go unnoticed | Browser automation, test-slot logic, screenshots and alerts |
| W2-C3 | Checkout/promo-code smoke tester | Tests checkout-critical paths and selected discount codes without completing real purchases | E-commerce merchants/agencies | Detects revenue-breaking storefront changes | Browser scripts, cart setup, promo validation and failure alerts |
| W2-C4 | Lead-notification delivery monitor | Confirms that website leads reach the intended mailbox/CRM rather than only checking the public form | Agencies/SMBs | Catches downstream email/webhook failure | Unique test identities, inbox/webhook verification and incident alerts |
| W2-C5 | Multi-site conversion-path monitor for agencies | White-label dashboard showing whether key client forms/booking flows still work | Web/marketing agencies | Protects client lead generation with one recurring service | Scheduled checks, client grouping, alerts and branded reports |

### D. Document workflow automation

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-D1 | RFP compliance-matrix generator | Extracts every requirement from an RFP into a reviewable matrix | Small firms/consultants bidding on work | Prevents missed requirements | PDF/DOC ingestion, requirement extraction, categorization and export |
| W2-D2 | Supplier quote comparison normalizer | Turns differently formatted supplier quotes into one apples-to-apples table | Procurement teams/SMBs | Saves manual comparison and exposes hidden differences | Document extraction, unit normalization, exception flags and ranking |
| W2-D3 | Security-questionnaire evidence assistant | Drafts questionnaire answers only from a company's approved evidence library | Small B2B software firms | Speeds repetitive customer due diligence | Q&A matching, citation retrieval, confidence scoring and review queue |
| W2-D4 | PO-versus-invoice discrepancy checker | Compares purchase orders, receipts and invoices and highlights mismatches | Small finance/operations teams | Prevents overpayment and manual reconciliation | Document extraction, line matching, tolerances and exception reports |
| W2-D5 | Decision/action register generator | Converts meeting transcripts or notes into decisions, owners, deadlines and follow-up status | Small teams | Stops commitments disappearing in notes | Extraction, owner/date matching, reminders and weekly digest |

### E. Finance/admin micro-tools

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-E1 | Accounts-receivable reminder workflow | Creates and tracks polite payment reminders from an aging report | Small businesses | Reduces manual chasing | Import aging file, sequence drafts, due dates and reply status |
| W2-E2 | SaaS spend visibility report | Finds recurring software subscriptions from ledger/statement exports | Small businesses | Identifies forgotten/duplicate software costs | Merchant detection, recurrence grouping and savings report |
| W2-E3 | Expense-evidence completeness checker | Finds transactions missing receipts, descriptions or approvals before month-end | Bookkeepers/SMBs | Reduces closing cleanup | Transaction-to-document matching and missing-item reminders |
| W2-E4 | Job-profitability pack | Combines time, materials and invoices into job/customer profitability reports | Service businesses | Reveals which work actually makes money | File imports, matching, margin calculations and monthly reports |
| W2-E5 | Monthly variance explainer | Converts current/prior P&L exports into a plain-English exception report | Small business owners | Saves time understanding financial changes | Variance thresholds, narrative drafts and chart generation |

### F. Asset and operations tools

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-F1 | QR equipment manual/service page | One QR code on equipment opens manuals, service history and contact instructions | Small facilities, landlords, equipment suppliers | Stops staff hunting for documents | Page generation, QR creation, document linking and reminders |
| W2-F2 | Calibration/evidence vault | Stores calibration/inspection certificates and flags missing evidence | Small labs, workshops, manufacturers | Avoids spreadsheet/document chaos | Document metadata extraction, expiry detection and reminders |
| W2-F3 | Consumables reorder predictor | Estimates when supplies will run out from simple usage logs | Small clinics, workshops, hospitality operators | Reduces emergency orders and excess stock | Usage-rate calculation, reorder thresholds and alerts |
| W2-F4 | Turnover photo-report generator | Turns timestamped property/equipment photos into standardized handover/turnover reports | Property managers, rental operators | Cuts repetitive report writing | Photo grouping, captions, issue flags and PDF generation |
| W2-F5 | Maintenance-log digitizer | Converts old maintenance PDFs/spreadsheets into searchable equipment histories | Small asset-heavy businesses | Makes legacy maintenance records usable | Extraction, asset matching, date parsing and searchable export |

### G. Creator/publisher monetization operations

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-G1 | Sponsorship inventory/rate-card manager | Tracks available ad slots, past sponsor pricing and renewal opportunities | Newsletters, podcasts, creators | Prevents unsold inventory and scattered spreadsheets | Inventory calendar, rate suggestions, reminders and invoices/export |
| W2-G2 | Affiliate-link health checker | Finds dead, redirected or no-longer-monetized affiliate links across a publisher's archive | Publishers/content sites | Broken affiliate links directly lose revenue | Crawl content, test links, merchant status and replacement queue |
| W2-G3 | Content-rights/license expiry tracker | Tracks usage rights for licensed photos, clips, music and UGC | Agencies, publishers, brands | Prevents expired/unclear usage | Asset metadata, expiry rules, alerts and evidence archive |
| W2-G4 | Sponsor proof-of-performance report | Finds sponsor mentions/placements across episodes/issues and creates delivery evidence | Podcasts/newsletters/agencies | Makes sponsor reporting easy | Transcript/content scanning, timestamps, screenshots and report generation |
| W2-G5 | Archive licensing catalog | Turns a creator/publisher archive into a searchable catalog of reusable/licensable assets | Publishers, photographers, niche media | Creates revenue from existing material | Metadata extraction, tagging, preview pages and licensing delivery |

### H. Specialized reference and public-data products

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-H1 | Product-recall feed/API for merchants | Normalized recall notices matched to product categories/SKUs | Retailers, marketplaces, service firms | Avoids manually checking multiple recall sources | Source ingestion, normalization, matching and alerts |
| W2-H2 | Trademark filing watchlists | New trademark applications matching selected brands/terms/classes | Brand owners, agencies, law-firm support teams | Finds potentially relevant filings earlier | Public filing ingestion, fuzzy matching and scheduled reports |
| W2-H3 | Awarded-contract intelligence database | Clean history of who won public contracts, for how much and for what | Suppliers, consultants, market researchers | Helps benchmark buyers, incumbents and contract values | Award-data ingestion, entity matching, categorization and search/export |
| W2-H4 | Charity/nonprofit benchmark dataset | Turns public charity filings into peer benchmarks on revenue, staffing and spending | Nonprofits, fundraisers, vendors, researchers | Makes public filings easier to compare | Filing extraction, normalization, ratios and benchmark reports |
| W2-H5 | Patent-expiry/opportunity brief | Tracks patent expiry/technology status for one narrowly defined non-medical product field | Manufacturers, investors, consultants | Reduces patent landscape research | Public patent data ingestion, dates, family matching and reports |

### I. Developer/test-data products

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-I1 | Synthetic business dataset packs | Realistic but non-personal test datasets for common business workflows | Developers, software vendors, trainers | Saves creating safe demo/test data | Schema-driven generation, validation and versioned downloads |
| W2-I2 | Industry-specific mock APIs | Hosted fake APIs that behave like realistic industry systems | Developers, bootcamps, QA teams | Enables demos/tests without live vendor accounts | Deterministic endpoints, scenario generation and usage metering |
| W2-I3 | CSV import regression fixtures | Libraries of deliberately messy files for testing accounting/CRM/e-commerce importers | Software QA teams | Finds edge cases before customers do | File generation, expected-output manifests and test automation |
| W2-I4 | Document-extraction evaluation packs | Labeled invoice/table/form document sets for testing extraction systems | AI/document-software teams | Gives repeatable accuracy benchmarks | Dataset generation/curation, scoring scripts and reports |
| W2-I5 | Redaction/anonymization test corpus | Synthetic documents containing controlled PII-like patterns for validating redaction software | Security/document vendors | Tests whether redaction misses common patterns | Synthetic document generation, ground truth and automated scoring |

### J. Sales/marketing operations utilities

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-J1 | Testimonial permission/evidence tracker | Stores customer permission, approved quote, allowed channels and expiry | Agencies/marketing teams | Reduces rights confusion around testimonials | Intake links, evidence storage and expiry reminders |
| W2-J2 | UTM/link governance checker | Scans campaign links for broken or inconsistent tracking parameters | Marketing teams/agencies | Prevents bad attribution data | Link parsing, naming-rule checks and correction suggestions |
| W2-J3 | Campaign proof archive | Captures dated screenshots/versions of important landing pages and ads | Agencies/regulated marketing teams | Creates evidence of exactly what was published | Scheduled captures, versioning, tagging and export |
| W2-J4 | Lead-source reconciliation report | Matches website/form/CRM exports and reports where leads disappear or are duplicated | Small marketing teams/agencies | Finds broken handoffs and bad attribution | File matching, dedupe, funnel variance and report generation |
| W2-J5 | Proposal follow-up queue | Tracks sent proposals and creates timed follow-up tasks/messages | Freelancers, agencies, consultants | Stops proposals going cold | Proposal detection/import, schedule, draft follow-ups and status tagging |

### K. Procurement and supplier utilities

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-K1 | Freight-quote normalizer | Converts carrier/freight quotes into one comparable landed-cost table | Importers, manufacturers, distributors | Quotes use different fees/units | Extraction, fee normalization, scenario comparison and ranking |
| W2-K2 | Vendor-onboarding completeness checker | Checks supplier onboarding packets for missing documents/fields | Procurement/finance teams | Reduces back-and-forth | Document checklist, extraction, missing-item email drafts and status |
| W2-K3 | MOQ/lead-time comparison workspace | Normalizes minimum order, lead time, price breaks and terms from supplier quotations | Buyers/product businesses | Speeds sourcing decisions | Quote parsing, unit normalization and scenario analysis |
| W2-K4 | BOM quote comparison tool | Compares multi-line component quotes against one bill of materials | Small manufacturers/hardware firms | Manual line matching is slow/error-prone | Part-number normalization, substitutions, variance flags and totals |
| W2-K5 | Supplier document chase portal | Automatically requests and tracks missing insurance/tax/banking/certification files | Small procurement teams | Removes repeated email chasing | Request links, reminders, document receipt and status dashboard |

### L. Consumer/prosumer utilities

| ID | Idea | What it sells | Who pays | Why pay | Automation |
|---|---|---|---|---|---|
| W2-L1 | Home-service quote comparison assistant | Turns roofing/HVAC/renovation quotes into a side-by-side scope/price comparison | Homeowners | Quotes are hard to compare | PDF extraction, line grouping, missing-scope flags and questions list |
| W2-L2 | Wedding/vendor quote comparison assistant | Normalizes venue/catering/photo/vendor proposals | Couples/planners | Saves spreadsheet work and exposes exclusions | Proposal extraction, category mapping and comparison report |
| W2-L3 | Household manual/warranty QR vault | Stores appliance manuals, receipts and warranty dates behind household QR labels | Homeowners/landlords | Keeps records accessible at the item | Document extraction, reminders, QR labels and searchable archive |
| W2-L4 | Hobby collection provenance vault | Stores purchase records, certificates, photos and ownership history for collectibles | Collectors | Protects documentation for resale/insurance | Metadata extraction, item records and exportable provenance pack |
| W2-L5 | Moving account-transfer organizer | Tracks utilities, services, addresses and account changes during a move | Consumers/relocation firms | Moving requires many repetitive updates | Checklist generation, reminders, document storage and progress dashboard |

## Categories represented

Wave 2 adds 12 families:

1. platform-native apps/extensions;
2. e-commerce/back-office intelligence;
3. revenue-path monitoring;
4. document workflow automation;
5. finance/admin utilities;
6. asset/operations tools;
7. creator monetization operations;
8. specialized reference/public-data products;
9. developer/test-data products;
10. sales/marketing operations utilities;
11. procurement/supplier utilities; and
12. consumer/prosumer utilities.

## Deliberate non-duplicates from Wave 1

- No new generic template stores, newsletters, directories, affiliate-review sites or print-on-demand variants.
- Monitoring ideas are limited to **business-critical transactional paths** rather than generic website/change monitoring.
- Public-data concepts focus on recalls, awarded contracts, filings and benchmarks rather than the permit/importer concepts already under active investigation.
- Marketplace ideas focus on embedded workflow apps rather than another generic scraper/Actor concept.
- Spreadsheet-like concepts are framed as workflow products or validation mechanisms, not standalone template stores.
- Lead-generation concepts are deliberately sparse in this wave; the emphasis is on products that can acquire customers without becoming lead-resale businesses.

## Candidates recommended for Stage 2

The following 18 deserve scoring before deeper investigation:

- W2-A3 Canva variable-data document generator;
- W2-A4 Shopify product-upload preflight;
- W2-A5 QuickBooks import preflight;
- W2-B1 returns root-cause report;
- W2-B2 marketplace fee reconciler;
- W2-C5 agency conversion-path monitor;
- W2-D1 RFP compliance-matrix generator;
- W2-D2 supplier quote comparison normalizer;
- W2-D4 PO-versus-invoice discrepancy checker;
- W2-E2 SaaS spend visibility report;
- W2-E4 job-profitability pack;
- W2-F1 QR equipment manual/service page;
- W2-G2 affiliate-link health checker;
- W2-G4 sponsor proof-of-performance report;
- W2-H3 awarded-contract intelligence database;
- W2-I1 synthetic business dataset packs;
- W2-K1 freight-quote normalizer; and
- W2-K4 BOM quote comparison tool.

These were chosen because each has a concrete payer, a bounded problem and a plausible low-capital MVP. Stage 2 should still reject aggressively where current competition or operating burden makes the idea unattractive.

## Verification record

- Last verified: 2026-10-16
- Stage 1 status: complete
- Market demand for individual ideas: not yet validated
- Current-platform facts checked: Atlassian Marketplace, Canva Apps, Shopify App Store and Zapier developer/distribution mechanisms.
