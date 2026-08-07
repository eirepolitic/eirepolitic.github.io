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
| `bb-comp-prices` | Complete | 12 major target groups; PR #56 / Pages #162 |
| `degenerate_investigator` | Complete | 13 major target groups; PR #57 / Pages #163 |
| `Overlord` | Complete | 4 real target groups; PR #58 / Pages #164 |
| `autodoc` | Complete; publication gate pending | 11 major target groups across Appsmith intake, config/index, enrichment, LLM generation/review, orchestration, artifacts, publication/security |

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

## Repository 5 — `Overlord`

Detailed scan: [Repository Scan — Overlord]({{ '/projects/high-director/repository-scan-overlord/' | relative_url }}).

Real targets:

1. Repository/task-record system.
2. Markdown task-record schema.
3. Versioned task/project/meeting template system.
4. Work/personal context partition.

The eight `tasks/work/test-task-*` files are fixtures/examples, not separate documentation targets. No executable code, workflows, APIs, cloud infrastructure, or external integrations are present in the current tree.

## Repository 6 — `autodoc`

Detailed scan: [Repository Scan — autodoc]({{ '/projects/high-director/repository-scan-autodoc/' | relative_url }}).

Major targets:

1. `autodoc` repository/system overview.
2. AutoDoc Appsmith intake/configuration application.
3. GitHub-backed configuration schema and project index registry.
4. Asset enrichment/source-resolution stage.
5. LLM section-fact extraction stage.
6. Template and Markdown rendering system.
7. LLM review/concision stage.
8. Automatic AutoDoc creation-pipeline orchestrator plus manual recovery workflows.
9. Generated/reviewed documentation artifact lifecycle.
10. Reviewed-document website publication workflow.
11. AutoDoc security/credential/trust boundaries.

Important verified control boundary: `publish_to_website.yml` currently clones `eirepolitic.github.io` using `WEBSITE_PAT` and pushes a reviewed Markdown file directly. That is not equivalent to the newer website discipline requiring a focused PR, documentation validation, merge, and matching Pages verification. This is a future architecture/operations decision candidate, not a discovery-time implementation change.

The Appsmith technical handoff persisted in `doc_configs/autodoc/autodoc_app.json` provides detailed configuration evidence, but the live external Appsmith application remains a later verification source for exact current widget/query/action state.

## Cross-repository relationships discovered

- `eirepolitic.github.io` is the persistent documentation site/source of truth.
- `eirepolitic-data-pipeline` is the principal Irish Politics Analytics/Oireachtas data-platform repository and contains implementation lineage for historical pages in the documentation repo and AutoDoc artifact corpus.
- `bb-comp-prices` reuses an AWS/S3 pattern from `eirepolitic-data-pipeline` but is a distinct competitor-pricing platform.
- `degenerate_investigator` is a distinct UFC analytics/ML system using AWS/S3, UFC Stats, The Odds API, OpenAI, and GitHub Actions.
- `Overlord` currently has no verified integration relationship to High Director or other repositories.
- `autodoc` connects the external Appsmith intake UI, GitHub configuration/content, OpenAI-backed generation, and `eirepolitic.github.io` publication.
- Historical AutoDoc-generated `docs/eirepolitic/pipeline/*` files are documentation artifacts, not source implementations; current/legacy source in `eirepolitic-data-pipeline` is stronger implementation evidence.

## Priority model

Owner-wide consolidation will assign final priorities using:

- **P0 — foundational:** umbrella architecture, repositories, shared infrastructure, security/authentication, central data platforms, unsafe/outdated publication boundaries.
- **P1 — active operational:** deployed applications, pipelines, APIs, automations, dashboards, agents.
- **P2 — supporting:** libraries, maintenance utilities, schemas/data products, diagnostics, deployment tooling.
- **P3 — historical:** retired/archived systems and experiments requiring preservation/successor mapping.

## Publication discipline

After each repository scan: update this plan and/or a linked scan page, run validation, merge only after success, confirm the matching Pages deployment, then move to the next repository or consolidation step.

## Current next safe action

Complete the `autodoc` validation/merge/Pages gate. Then perform one owner-wide consolidation/prioritization review that deduplicates all discovered targets, assigns final P0–P3 priorities, defines documentation waves, and lists any external authoritative source required for each future full-documentation initiative.
