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

Inspect every repository in the authoritative owner repository list and identify concrete technical items that should receive full documentation on this site. Group related files into real systems/components; do not turn every source file into a separate documentation target.

This initiative is discovery/inventory only. Full documentation begins after owner-wide discovery is complete enough to understand dependencies and priorities.

## Target categories

Repository; system/application; data pipeline/ETL; API/service; AWS/cloud component; external integration; automation/workflow; data product/schema; Appsmith/Power BI/Power Automate; agent/GPT/action; deployment/build infrastructure; security/authentication boundary; runbook/recovery procedure; architecture decision; historical/retired implementation.

## Scan method

For each repository: inspect the complete tree, README/configuration/workflows/deployment files, executable entry points, cloud/API integrations, data inputs/outputs, authentication/configuration boundaries, tests/validation, and current-vs-historical evidence. Record exact evidence paths and external-source gaps. Never guess source that can be inspected directly.

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

This is the complete discovery scope unless the owner later supplies a changed list.

## Scan status

| Repository | Status | Result |
|---|---|---|
| `eirepolitic.github.io` | Complete | Documentation platform/High Director already covered; AutoDoc/IPA plus historical pipeline candidates identified |
| `eirepolitic-data-pipeline` | Complete | 13 major target groups across Oireachtas platform, data products, orchestration, media, LLM/member analytics, maintenance/legacy |
| `bb-comp-prices` | Complete; publication gate pending | 12 major target groups across competitor-pricing architecture, Best Buy/Amazon/Walmart acquisition, matching, storage, orchestration, validation/probes |
| `degenerate_investigator` | Next after Pages gate | Pending |
| `Overlord` | Pending | Pending |
| `autodoc` | Pending | Pending |

## Repository 1 — `eirepolitic.github.io`

Already fully documented/maintenance-only real targets:

- documentation repository/site;
- validation/publication/search subsystems;
- High Director and GitHub/AWS/Google integrations.

New/verification-required targets:

1. **AutoDoc Appsmith application/public embed** — evidence `autodoc.md`, `assets/projects/autodoc/`; authoritative Appsmith configuration will later be needed.
2. **Irish Politics Analytics umbrella architecture/index** — evidence `projects/ipa-overview.md`.
3. **Constituency Images Indexer** — historical pipeline.
4. **Debate Issue Classifier** — historical Oireachtas/OpenAI pipeline.
5. **LLM Column Creator** — historical reusable LLM processing framework.
6. **Member Images Pipeline** — historical member/image pipeline.
7. **Member Summaries Table** — historical member enrichment/data product.
8. **S3 Column Deleter** — historical destructive data-maintenance utility.

The six historical pipeline items are implementation-lineage records, not independent unknown systems; repository 2 contains the relevant current/legacy source lineage.

## Repository 2 — `eirepolitic-data-pipeline`

Major documentation targets:

1. **Repository overview** — central Irish Politics Analytics data-platform repository.
2. **Unified Oireachtas Data Platform** — `configs/oireachtas/`, `extract/oireachtas/`, `process/oireachtas/`, Oireachtas workflows.
3. **Oireachtas canonical data-product catalogue** — registry includes houses, constituencies, parties, members, memberships, offices, sources, debates, speeches, votes, questions, legislation.
4. **Oireachtas refresh/validation orchestration** — `.github/workflows/oireachtas_*.yml`, `docs/oireachtas_packet_status.md`.
5. **Oireachtas write policies/downstream contracts** — `configs/oireachtas/write_policies.yml`, `downstream_contracts.yml`.
6. **Instagram/constituency campaign rendering system** — `instagram/`, `instagram/README.md`, campaign workflow.
7. **AI member-profile/Instagram content workflow** — separate AI content stage where distinct from rendering.
8. **Member Profile Metrics Builder** — `process/build_member_profile_metrics.py`, workflow.
9. **Reusable LLM Task Runner Framework** — `process/llm_table_runner.py`, `tasks/`, controller template; current source lineage for archived LLM Column Creator.
10. **Debate/speech classification and enrichment lineage** — distinguish current unified platform from retained legacy scripts.
11. **Member enrichment/image/summaries lineage** — successor mapping for archived member pipelines.
12. **Data maintenance utilities** — destructive/repair/backfill helpers; group unless independently scheduled/security-sensitive.
13. **Experimental/editorial content generation workflows** — e.g. `ridiculous_sentences_weekly.yml`, documented as active vs historical only after status verification.

Preliminary priority: Oireachtas platform/data contracts/orchestration P0; active media/member/LLM systems P1; utilities P2; retired lineage P3.

## Repository 3 — `bb-comp-prices`

Detailed canonical discovery page: [Repository Scan — bb-comp-prices]({{ '/projects/high-director/repository-scan-bb-comp-prices/' | relative_url }}).

Major targets isolated:

1. `bb-comp-prices` repository.
2. Competitor Pricing Platform architecture.
3. Best Buy Marketplace category discovery.
4. Best Buy product/Marketplace-offer extraction.
5. Amazon.ca competitor acquisition/recovery system.
6. Walmart.ca competitor acquisition/probe system.
7. Product matching/confidence-scoring engine.
8. End-to-end pipeline orchestrator/CLI.
9. S3 historical storage/data-product model.
10. Probe/diagnostics/extraction-research framework.
11. Validation/data-quality framework.
12. Python package/CLI/configuration/developer layer.

Verified shared configuration includes Python >=3.12, `ca-central-1`, S3 bucket `eirepolitic-data`, prefix `bb-comp-prices`, GitHub Actions AWS credential secret names, optional Playwright browser automation, and substantial fixture/unit validation.

Current evidence is stronger than `docs/BUILD_PLAN.md` for implemented state; proposed/deferred plan items must not be presented as deployed without source/workflow/report confirmation.

## Cross-repository relationships discovered

- `eirepolitic.github.io` is the documentation system and contains historical records for several `eirepolitic-data-pipeline` components.
- `eirepolitic-data-pipeline` is the main Irish Politics Analytics data-platform implementation repository discovered so far.
- `bb-comp-prices` reuses the AWS/S3 configuration pattern from `eirepolitic-data-pipeline` but is a distinct competitor-pricing system and should not be folded into the Oireachtas platform.
- AutoDoc appears both as a documentation-site embed and as a separately listed repository; the `autodoc` repository scan will determine the code/configuration boundary versus the external Appsmith application.

## Priority model

After all repositories are scanned:

- **P0 — foundational:** umbrella architecture, repositories, shared infrastructure, security/authentication, central data platforms.
- **P1 — active operational:** deployed applications, pipelines, APIs, automations, dashboards, agents.
- **P2 — supporting:** libraries, maintenance utilities, schemas/data products, deployment tooling.
- **P3 — historical:** retired/archived systems and experiments requiring authoritative preservation/successor mapping.

Do not finalize owner-wide priorities until all six repositories are scanned.

## Publication discipline

After each repository scan:

1. update this persistent plan and/or a linked repository-scan page;
2. run documentation validation;
3. merge only after validation passes;
4. confirm matching GitHub Pages deployment succeeds;
5. only then scan the next repository.

## Current next safe action

Complete the `bb-comp-prices` validation/merge/Pages gate. Then inspect `degenerate_investigator` completely and persist its target inventory in a separate focused PR.
