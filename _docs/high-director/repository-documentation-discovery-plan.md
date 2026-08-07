---
title: Repository Documentation Discovery Initiative
summary: Persistent cross-repository inventory plan for identifying every system, pipeline, data product, integration, workflow, service, application, repository, and supporting component that merits full technical documentation.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 29
permalink: /projects/high-director/repository-documentation-discovery/
---

# Repository Documentation Discovery Initiative

## Purpose

Inspect every repository in the authoritative owner repository list and identify concrete technical items that should receive full documentation on this site. Group related files into real systems/components rather than documenting every source file independently.

## Authoritative repository list

Supplied by the system owner on 2026-08-07:

```text
eirepolitic.github.io
eirepolitic-data-pipeline
bb-comp-prices
degenerate_investigator
Overlord
autodoc
```

## Scan status

| Repository | Status | Result |
|---|---|---|
| `eirepolitic.github.io` | Complete | Documentation platform/High Director already covered; AutoDoc/IPA plus historical pipeline candidates identified |
| `eirepolitic-data-pipeline` | Complete | 13 major target groups across Oireachtas platform, data products, orchestration, media, LLM/member analytics, maintenance/legacy |
| `bb-comp-prices` | Complete | 12 major target groups; detailed scan page published after PR #56 / Pages #162 |
| `degenerate_investigator` | Complete; publication gate pending | 13 major target groups across UFC ingestion/history, odds/news enrichment, feature engineering, training, scoring, reports, storage/orchestration |
| `Overlord` | Next after Pages gate | Pending |
| `autodoc` | Pending | Pending |

## Repository 1 — `eirepolitic.github.io`

Already fully documented/maintenance-only real targets:

- documentation repository/site;
- validation/publication/search subsystems;
- High Director and GitHub/AWS/Google integrations.

New/verification-required targets:

1. AutoDoc Appsmith application/public embed.
2. Irish Politics Analytics umbrella architecture/index.
3. Constituency Images Indexer — historical implementation lineage.
4. Debate Issue Classifier — historical implementation lineage.
5. LLM Column Creator — historical implementation lineage.
6. Member Images Pipeline — historical implementation lineage.
7. Member Summaries Table — historical implementation lineage.
8. S3 Column Deleter — historical maintenance utility.

Repository 2 contains the current/legacy implementation lineage for the six historical pipeline records above.

## Repository 2 — `eirepolitic-data-pipeline`

Major targets:

1. Repository overview / Irish Politics Analytics data platform.
2. Unified Oireachtas Data Platform.
3. Oireachtas canonical data-product catalogue.
4. Oireachtas refresh/validation orchestration.
5. Oireachtas write policies/downstream contracts.
6. Instagram/constituency campaign rendering system.
7. AI member-profile/Instagram content workflow.
8. Member Profile Metrics Builder.
9. Reusable LLM Task Runner Framework.
10. Debate/speech classification and enrichment lineage.
11. Member enrichment/image/summaries lineage.
12. Data maintenance utilities.
13. Experimental/editorial content generation workflows.

Preliminary priority: Oireachtas platform/data contracts/orchestration P0; active media/member/LLM systems P1; utilities P2; retired lineage P3.

## Repository 3 — `bb-comp-prices`

Detailed scan: [Repository Scan — bb-comp-prices]({{ '/projects/high-director/repository-scan-bb-comp-prices/' | relative_url }}).

Major targets:

1. Repository overview.
2. Competitor Pricing Platform architecture.
3. Best Buy Marketplace category discovery.
4. Best Buy product/Marketplace-offer extraction.
5. Amazon.ca competitor acquisition/recovery.
6. Walmart.ca competitor acquisition/probes.
7. Product matching/confidence-scoring engine.
8. End-to-end orchestrator/CLI.
9. S3 historical storage/data-product model.
10. Probe/diagnostics/extraction-research framework.
11. Validation/data-quality framework.
12. Python package/CLI/configuration/developer layer.

## Repository 4 — `degenerate_investigator`

Detailed scan: [Repository Scan — degenerate_investigator]({{ '/projects/high-director/repository-scan-degenerate-investigator/' | relative_url }}).

Major targets:

1. Repository overview / UFC analytics system.
2. Current UFC event/fighter ingestion.
3. Historical fight/fighter-profile ingestion.
4. Current MMA odds ingestion.
5. Fighter recent-news OpenAI/web-search enrichment.
6. Matchup feature engineering.
7. Historical training-dataset builder.
8. UFC winner-model training.
9. Target-event scoring with trained-model/heuristic fallback distinction.
10. Fight analysis report generator.
11. S3-to-repository report publication workflow.
12. S3 storage/shared I/O/data-product conventions.
13. GitHub Actions pipeline orchestration and security/configuration boundary.

The repository explicitly states it does not include staking logic or bookmaker-targeted betting recommendations. Documentation should remain technical/analytical and preserve that boundary.

## Cross-repository relationships discovered

- `eirepolitic.github.io` is the documentation system and contains historical records for several `eirepolitic-data-pipeline` components.
- `eirepolitic-data-pipeline` is the main Irish Politics Analytics data-platform implementation repository discovered so far.
- `bb-comp-prices` reuses an AWS/S3 configuration pattern from `eirepolitic-data-pipeline` but is a distinct competitor-pricing system.
- `degenerate_investigator` is a distinct AWS/S3 analytics/ML system with UFC Stats, The Odds API, OpenAI web search/reporting, and GitHub Actions dependencies.
- AutoDoc appears as both a site embed and a separately listed repository; its repository scan will determine the code/configuration boundary versus the external Appsmith application.

## Priority model

After all repositories are scanned:

- **P0 — foundational:** umbrella architecture, repositories, shared infrastructure, security/authentication, central data platforms.
- **P1 — active operational:** deployed applications, pipelines, APIs, automations, dashboards, agents.
- **P2 — supporting:** libraries, maintenance utilities, schemas/data products, deployment tooling.
- **P3 — historical:** retired/archived systems and experiments requiring preservation/successor mapping.

Do not finalize owner-wide priorities until all six repositories are scanned.

## Publication discipline

After each repository scan: update this plan and/or a linked scan page, run validation, merge only after success, confirm the matching Pages deployment, then move to the next repository.

## Current next safe action

Complete the `degenerate_investigator` validation/merge/Pages gate. Then inspect `Overlord` completely and persist its target inventory in a separate focused PR.
