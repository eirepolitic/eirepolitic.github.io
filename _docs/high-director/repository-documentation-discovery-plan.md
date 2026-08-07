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

Systematically inspect every accessible GitHub repository owned by the configured GitHub integration and identify the concrete technical items that should receive full documentation on this site.

This initiative is discovery/inventory only. It does not redesign systems or begin full documentation of each discovered item until the cross-repository inventory is sufficiently complete and the relevant authoritative source is available.

## Documentation target categories

A repository scan should isolate real implementation targets that fit one or more of these categories:

- repository;
- system/application;
- data pipeline/ETL workflow;
- service/API;
- AWS/Lambda/cloud component;
- external integration;
- automation/workflow;
- data product/dataset/schema;
- Appsmith/Power BI/Power Automate application or flow;
- agent/GPT/action;
- deployment/build infrastructure;
- security/authentication boundary;
- operational runbook/recovery procedure;
- architecture decision;
- historical/retired implementation that still needs authoritative archival documentation.

Templates, generic CSS/layout files, empty placeholders, decorative assets, and duplicate documentation pages are not separate documentation targets unless they implement a meaningful subsystem.

## Scan method

For each repository:

1. inspect the complete repository tree;
2. inspect README/configuration/workflow/deployment files;
3. identify executable code and entry points;
4. identify GitHub Actions and scheduled/manual workflows;
5. identify cloud/service/API integrations;
6. identify data inputs, outputs, tables, buckets, schemas, and datasets;
7. identify external applications and embedded services;
8. identify security/authentication/configuration boundaries;
9. group related files into real technical components rather than documenting each file separately;
10. record exact evidence paths and current verification state;
11. distinguish current implementation from historical/archived references;
12. flag external source/configuration that will later require user retrieval.

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

This list is the discovery scope. Do not guess additional repository names.

## Repository scan status

| Repository | Scan status | Result |
|---|---|---|
| `eirepolitic.github.io` | Complete | 10 real targets/groups identified; 8 new/verification-required and 2 already fully documented groups |
| `eirepolitic-data-pipeline` | Complete | 13 major documentation targets/groups identified across the Oireachtas platform, data products, media generation, reusable LLM processing, member analytics, and legacy utilities |
| `bb-comp-prices` | Next | Pending |
| `degenerate_investigator` | Pending | Pending |
| `Overlord` | Pending | Pending |
| `autodoc` | Pending | Pending |

## Repository 1 — `eirepolitic.github.io`

### Already fully documented / maintenance-only

- `eirepolitic.github.io` repository and documentation site.
- Documentation validation/publication subsystem.
- Documentation search-index subsystem.
- High Director and its GitHub/AWS/Google integrations.

### New/verification-required targets

1. **AutoDoc Appsmith application / public embed** — application, Appsmith integration, external connection, UI/embed, security/privacy boundary, deployment/runbook.
   - Evidence: `autodoc.md`, `assets/projects/autodoc/`.
   - External authoritative Appsmith configuration will be required when full documentation begins.

2. **Irish Politics Analytics umbrella architecture/index** — portfolio/system architecture, repository map, cross-system data flows.
   - Evidence: `projects/ipa-overview.md`.

3. **Constituency Images Indexer** — historical pipeline, AWS S3, Glue/Athena, GitHub Actions.
   - Historical source: `process/constituency_images_indexer.py`, `.github/workflows/constituency_images_index.yml`.

4. **Debate Issue Classifier** — historical Oireachtas/OpenAI pipeline, S3/Athena, GitHub Actions.
   - Historical source: `extract/monthly_extract.py`, `extract/debates_xml_to_csv_s3.py`, `process/speech_issue_classifier.py`.

5. **LLM Column Creator** — reusable OpenAI/YAML/S3 processing framework.
   - Historical source: `process/llm_table_runner.py`, `tasks/`, `.github/workflows/llm_task_controller_template.yml`.

6. **Member Images Pipeline** — scraping/Oireachtas/S3 pipeline.
   - Historical source: `process/members_photo_urls.py`, `.github/workflows/member_photo_urls.yml`.

7. **Member Summaries Table** — Oireachtas/OpenAI enrichment pipeline and S3/Glue/Athena data product.

8. **S3 Column Deleter** — destructive maintenance utility for CSV/Parquet datasets.

The six historical items above are matched against repository 2 below before deciding final current-vs-archived documentation treatment.

## Repository 2 — `eirepolitic-data-pipeline`

### Repository role

**Target:** `eirepolitic-data-pipeline` repository.

**Categories:** repository, central data platform, orchestration, data products, integrations, deployment/operations.

This repository is a major Irish Politics Analytics implementation repository and should receive its own repository page plus an umbrella system architecture page linking its subsystems.

### Target 1 — Unified Oireachtas Data Platform

**Categories:** data platform, ETL/ELT framework, Oireachtas API integration, S3 lakehouse-style storage, schema/configuration framework, validation/orchestration.

Key evidence:

```text
configs/oireachtas/tables.yml
configs/oireachtas/api_params.yml
configs/oireachtas/write_policies.yml
configs/oireachtas/downstream_contracts.yml
process/oireachtas/
extract/oireachtas/
.github/workflows/oireachtas_*.yml
docs/oireachtas_packet_status.md
```

The table registry defines the central canonical datasets, cadence, status, keys, source endpoints, and columns. The platform includes raw/extract, canonical/build, validation, backfill, and refresh orchestration behavior.

This is **P0 foundational** once owner-wide priorities are finalized.

### Target 2 — Oireachtas Canonical Data Product Catalogue

**Categories:** data products, schemas, contracts, update cadence, lineage.

Canonical registry evidence: `configs/oireachtas/tables.yml`.

Confirmed table groups include:

- houses;
- constituencies;
- parties;
- members;
- memberships;
- offices;
- sources;
- debates;
- speeches;
- votes;
- questions;
- legislation.

Each table should not automatically become a separate top-level page. Use one canonical data-product catalogue, with subordinate pages only for unusually complex tables or downstream contracts.

### Target 3 — Oireachtas Refresh/Validation Orchestration

**Categories:** GitHub Actions, scheduler/orchestrator, validation, operational runbook, failure recovery.

Evidence:

```text
.github/workflows/oireachtas_refresh_validation_orchestrator.yml
.github/workflows/oireachtas_*.yml
docs/oireachtas_packet_status.md
```

Document scheduling/manual dispatch, dependency order, validation gates, packet/cutover process, and operational status evidence.

### Target 4 — Oireachtas Write Policies and Downstream Contracts

**Categories:** data-governance/configuration, write safety, downstream dependencies, compatibility contract.

Evidence:

```text
configs/oireachtas/write_policies.yml
configs/oireachtas/downstream_contracts.yml
```

This should be documented as one shared control/configuration subsystem rather than duplicated across each pipeline page.

### Target 5 — Instagram / Constituency Campaign Rendering System

**Categories:** media-generation application, data-to-visual pipeline, external template-provider integration, local rendering fallback, GitHub Actions.

Evidence:

```text
instagram/
instagram/README.md
.github/workflows/instagram_campaign_render.yml
```

Verified characteristics:

- YAML campaign/content specs;
- constituency/member political data inputs;
- external template-provider support;
- local deterministic rendering fallback;
- generated image outputs;
- workflow-driven campaign rendering.

This merits a full application/system page plus configuration/deployment/runbook coverage.

### Target 6 — AI Member Profile / Instagram Content Workflow

**Categories:** AI content-generation workflow, member analytics, media generation, GitHub Actions, external AI integration.

Evidence:

```text
.github/workflows/instagram_option5_member_profile_ai.yml
instagram/
```

Keep separate from the general rendering engine if the AI-generation stage has distinct prompts/models/configuration/data flow.

### Target 7 — Member Profile Metrics Builder

**Categories:** analytics pipeline, member data product, GitHub Actions.

Evidence:

```text
process/build_member_profile_metrics.py
.github/workflows/build_member_profile_metrics_2025.yml
```

Document metric definitions, input tables, output schema, period/year assumptions, scheduling, and downstream consumers.

### Target 8 — Reusable LLM Task Runner Framework

**Categories:** reusable processing framework, OpenAI integration, YAML task definitions, data enrichment, GitHub Actions.

Evidence:

```text
process/llm_table_runner.py
tasks/
.github/workflows/llm_task_controller_template.yml
```

This is the current authoritative match for the archived **LLM Column Creator** record in repository 1. Treat the archive page as historical context and this repository as the implementation source of truth.

### Target 9 — Debate / Speech Classification and Enrichment Pipelines

**Categories:** Oireachtas ingestion, NLP/LLM classification, speech/debate enrichment, GitHub Actions, data products.

Evidence includes historical/current files under:

```text
extract/
process/
.github/workflows/
```

This group includes the implementation lineage behind the archived **Debate Issue Classifier**. During full documentation, distinguish current unified-Oireachtas replacements from legacy scripts that remain in the repository.

### Target 10 — Member Enrichment Pipelines

**Categories:** member extraction/enrichment, web/API integration, AI summarization, image URL processing, data products.

This group includes the source lineage for archived:

- Member Images Pipeline;
- Member Summaries Table.

Do not document legacy scripts as separate current systems if they have been superseded by the unified Oireachtas/member platform. Preserve successor mapping.

### Target 11 — Constituency Image/Asset Indexing

**Categories:** constituency asset pipeline, S3/data product, GitHub Actions.

Matches the archived **Constituency Images Indexer**. Verify current source/workflow files during full documentation and mark retired pieces explicitly.

### Target 12 — Data Maintenance Utilities

**Categories:** operational utilities, destructive mutation tooling, repair/backfill helpers.

Includes the source lineage for archived **S3 Column Deleter** and other one-off/maintenance scripts under `process/`, `scripts/`, and workflow files.

These should generally be grouped in an operational utilities/runbook page rather than each becoming a top-level system page unless a utility is independently scheduled or security-sensitive.

### Target 13 — Experimental / Editorial Content Generation Workflows

**Categories:** LLM/editorial automation, scheduled workflow, content product, experimentation.

Evidence:

```text
.github/workflows/ridiculous_sentences_weekly.yml
```

Document as a separate experimental/editorial automation only if still active. If experimental/retired, preserve as historical implementation rather than mixing with the core data platform.

### Repository 2 cross-cutting documentation requirements

Full documentation should also capture shared dependencies and boundaries evident from repository configuration/code:

- Python dependency stack from `requirements.txt`;
- GitHub Actions secrets/variables **names only**, never values;
- AWS/S3 storage conventions;
- Oireachtas API endpoints/parameters;
- OpenAI/LLM integrations where present;
- table naming, write modes, and downstream contracts;
- generated artifacts and output locations;
- scheduled/manual workflow triggers;
- validation/cutover/rollback procedures;
- legacy-to-current successor mapping.

### Repository 2 priority candidates

Preliminary priority pending complete owner scan:

- **P0:** repository overview; Unified Oireachtas Data Platform; data-product catalogue; orchestration; write policies/downstream contracts.
- **P1:** Instagram/media system; AI member profile workflow; member profile metrics; active LLM task framework.
- **P2:** shared enrichment and maintenance utilities.
- **P3:** retired/legacy scripts and archived pipeline lineage after successor mapping.

## Owner-wide target relationship discovered so far

The six archived pipeline pages from repository 1 are **not six unrelated unknown systems** anymore. Repository 2 contains their implementation lineage. Final documentation should avoid duplication by using current repository implementation as source of truth and linking archived pages as historical records/successor maps.

## Priority model

After all repositories are scanned, rank targets using:

- **P0 — foundational:** umbrella architecture, repositories, shared infrastructure, security/authentication, central data platform components.
- **P1 — active operational:** currently deployed applications, pipelines, APIs, automations, dashboards, agents.
- **P2 — supporting:** shared libraries, maintenance utilities, data schemas/products, deployment tooling.
- **P3 — historical:** retired/archived systems requiring authoritative preservation or successor mapping.

Do not finalize owner-wide priority ordering until all six repositories are scanned.

## Current next safe action

Validate/merge/deploy this repository-2 inventory. After the resulting Pages deployment succeeds, inspect `bb-comp-prices` completely and update this persistent inventory in a separate focused PR.
