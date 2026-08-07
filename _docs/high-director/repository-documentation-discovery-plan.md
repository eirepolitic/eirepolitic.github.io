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

## Repository discovery limitation

The configured GitHub Action exposes repository-scoped operations but does **not** expose an operation that lists all repositories for the configured owner.

Therefore complete owner-wide coverage requires an authoritative repository-name list from outside the current Action. Until that list is supplied, scanning proceeds with every repository name already known from persisted documentation or provided by the user.

Do not guess repository names.

## Repository scan status

| Repository | Scan status | Result |
|---|---|---|
| `eirepolitic.github.io` | Tree/content discovery complete | 10 distinct documentation targets/groups identified; existing fully documented components separated from new/verification-required targets |
| Other owner repositories | Awaiting authoritative repository-name list | Current GitHub Action cannot enumerate owner repositories |

## Repository 1 — `eirepolitic.github.io`

### Already fully documented / maintenance-only

These are real documentation targets, but the site already contains full current documentation and they do not require a new discovery-to-documentation initiative unless implementation changes:

| Target | Category | Evidence |
|---|---|---|
| `eirepolitic.github.io` repository | Repository | `_docs/repositories/eirepolitic-github-io.md` |
| Documentation site | System/application | `_docs/systems/documentation-site.md`, `_config.yml`, layouts/includes/assets |
| Documentation validation/publication system | Automation/build infrastructure | `.github/workflows/validate-documentation.yml`, `scripts/validate_docs.py`, Pages workflow, runbooks |
| Documentation search index | Data product/site subsystem | `_docs/data/documentation-search-index.md`, `search-index.json`, `assets/js/search.js` |
| High Director | Agent/integration/system | complete High Director canonical documentation set |

These remain inventory items because they are real components, but their documentation status is **complete/current** rather than a new full-documentation target.

### New full-documentation candidate — AutoDoc

**Target:** AutoDoc Appsmith application / public site embed.

**Categories:** application, Appsmith integration, external connection, UI/embed, security/privacy boundary, operating/deployment procedure.

Repository evidence:

```text
autodoc.md
assets/projects/autodoc/
```

Verified from `autodoc.md`:

- public unlinked web page at `/autodoc/`;
- embeds an Appsmith application in an iframe;
- external host: `app.appsmith.com`;
- iframe allows clipboard read/write and fullscreen;
- page notes third-party cookie/tracking-protection dependencies.

Full documentation should eventually cover:

- Appsmith application purpose and users;
- Appsmith pages/widgets/queries/actions;
- data sources/APIs;
- authentication/access model;
- environment variables/secrets;
- data flows;
- deployment/update process;
- iframe/public exposure/security boundary;
- failure modes/troubleshooting;
- repository/source relationship.

**Current evidence gap:** authoritative Appsmith application configuration is external to this repository and will require user retrieval when full documentation begins.

### New umbrella documentation candidate — Irish Politics Analytics

**Target:** Irish Politics Analytics portfolio/project ecosystem.

**Categories:** system/portfolio architecture, repository map, data-platform overview, cross-system data flows.

Repository evidence:

```text
projects/ipa-overview.md
```

The page currently states that the scope includes:

- data pipelines;
- speech classification;
- dashboards;
- analytical outputs.

This should become an umbrella architecture/index document once the owner-wide repository inventory identifies the actual repositories and systems belonging to it.

### Historical implementation candidates requiring authoritative source verification

The repository contains six archived pipeline records. Each is a distinct technical implementation candidate that should be matched against the current/retired source repository before deciding whether to create current documentation, authoritative archive documentation, or a replacement/successor record.

All six historical records identify former repository name `eirepolitic`.

#### Constituency Images Indexer

**Categories:** pipeline, AWS S3, Glue/Athena data product, GitHub Actions.

Historical source paths:

```text
process/constituency_images_indexer.py
.github/workflows/constituency_images_index.yml
```

Historical outputs:

```text
processed/constituencies/constituency_images.csv
processed/constituencies/parquets/constituency_images.parquet
```

Archive source: `_docs/archive/constituency-images-indexer.md`.

#### Debate Issue Classifier

**Categories:** pipeline, OpenAI integration, Oireachtas API ingestion, S3/Athena data product, GitHub Actions.

Historical source paths:

```text
extract/monthly_extract.py
extract/debates_xml_to_csv_s3.py
process/speech_issue_classifier.py
.github/workflows/monthly_extract.yml
.github/workflows/speech_issue_classifier.yml
```

Historical outputs:

```text
processed/debates/debate_speeches_classified.csv
processed/debates/parquets/debate_speeches_classified.parquet
```

Archive source: `_docs/archive/debate-issue-classifier.md`.

#### LLM Column Creator

**Categories:** reusable data-processing framework, OpenAI integration, YAML task configuration, S3 pipeline, GitHub Actions.

Historical source paths:

```text
process/llm_table_runner.py
tasks/
.github/workflows/llm_task_controller_template.yml
```

Archive source: `_docs/archive/llm-column-creator.md`.

#### Member Images Pipeline

**Categories:** web-scraping pipeline, Oireachtas integration, S3 data product, GitHub Actions.

Historical source paths:

```text
process/members_photo_urls.py
.github/workflows/member_photo_urls.yml
```

Historical outputs:

```text
processed/members/members_photo_urls.csv
processed/members/parquets/members_photo_urls.parquet
```

Archive source: `_docs/archive/member-images-pipeline.md`.

#### Member Summaries Table

**Categories:** extraction pipeline, OpenAI/web-search enrichment, S3/Glue/Athena data product, GitHub Actions.

Historical source paths:

```text
monthly_members_extract.py
members_background_summarizer.py
.github/workflows/members_background_summarizer.yml
```

Historical outputs:

```text
processed/members/members_summaries.csv
processed/members/parquets/members_summaries.parquet
```

Archive source: `_docs/archive/member-summaries-table.md`.

#### S3 Column Deleter

**Categories:** destructive data-maintenance utility, S3 CSV/Parquet mutation, GitHub Actions.

Historical source paths:

```text
process/delete_s3_column.py
.github/workflows/column_deleter.yml
```

Archive source: `_docs/archive/s3-column-deleter.md`.

### Repository 1 target summary

New/verification-required targets discovered in `eirepolitic.github.io`:

1. AutoDoc Appsmith application.
2. Irish Politics Analytics umbrella architecture/index.
3. Constituency Images Indexer.
4. Debate Issue Classifier.
5. LLM Column Creator.
6. Member Images Pipeline.
7. Member Summaries Table.
8. S3 Column Deleter.

Existing fully documented real targets retained in inventory:

9. `eirepolitic.github.io` repository/documentation site and its supporting validation/search/publication subsystems.
10. High Director and its GitHub/AWS/Google integrations.

## Priority model

Once all repositories are scanned, rank targets using:

- **P0 — foundational:** umbrella architecture, repositories, shared infrastructure, security/authentication, central data platform components.
- **P1 — active operational:** currently deployed applications, pipelines, APIs, automations, dashboards, agents.
- **P2 — supporting:** shared libraries, maintenance utilities, data schemas/products, deployment tooling.
- **P3 — historical:** retired/archived systems requiring authoritative preservation or successor mapping.

Do not assign final owner-wide priorities until repository discovery is complete enough to identify dependencies between targets.

## Current next safe action

Obtain an authoritative list of repository names for the configured GitHub owner. Then inspect repositories one by one, updating this page after each repository scan through small validated PRs.

Do not request source code manually for a repository that the GitHub Action can inspect directly.
