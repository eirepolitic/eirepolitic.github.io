---
title: eirepolitic-data-pipeline
summary: Implementation repository for Irish Politics Analytics, including the Unified Oireachtas Data Platform, downstream member analytics, Instagram content systems, reusable LLM tasks, maintenance utilities, and retained legacy workflows.
section: repositories
doc_type: repository
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: eirepolitic-data-pipeline
order: 20
permalink: /projects/repositories/eirepolitic-data-pipeline/
technologies:
  - Python
  - GitHub Actions
  - AWS S3
  - Oireachtas API
  - OpenAI API
  - pandas
  - PyArrow
  - YAML
  - Jinja2
  - Playwright
related:
  - /projects/systems/irish-politics-analytics/
  - /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
---

# eirepolitic-data-pipeline

## Summary

`eirepolitic-data-pipeline` is the principal implementation repository for Irish Politics Analytics. It contains the current Unified Oireachtas Data Platform, its production orchestration and validation controls, downstream member-profile analytics, Instagram/content rendering, a reusable LLM table runner, operational utilities, and older extraction/enrichment/editorial scripts retained for compatibility, rollback, experimentation, or historical lineage.

The repository root README contains only the repository title and is not an operational source of truth. Current implementation, configuration, workflows, tests, and observed workflow runs are stronger evidence.

## Current Implementation State

**Verified implementation:** the current Oireachtas foundation is organized as a Python package under `extract/oireachtas/`, configured by `configs/oireachtas/`, supported by `process/oireachtas_*.py`, tested under `tests/test_oireachtas_*.py`, and orchestrated by `.github/workflows/oireachtas_*.yml`.

**Verified implementation:** the repository also contains active/manual downstream entry points for member metrics, Instagram campaign rendering, and YAML-driven LLM tasks. Their detailed operating documentation is a later P1 workstream.

**Historical/legacy boundary:** older top-level extraction and processing scripts remain checked in beside the current Oireachtas package. File presence alone does not make those scripts the canonical current pipeline. Where current Oireachtas modules or compatibility adapters supersede them, the newer implementation is authoritative and the older file is retained as lineage until P3 reconciliation is complete.

## Source of Truth

| Concern | Authoritative source |
| --- | --- |
| Repository structure and implementation | current `main` tree and source files |
| Python dependencies | `requirements.txt` |
| Oireachtas configuration | `configs/oireachtas/*.yml` |
| Oireachtas table execution | `extract/oireachtas/build_table.py` and `extract/oireachtas/table_*.py` |
| Oireachtas publication/storage controls | `extract/oireachtas/batch.py`, `io_s3.py`, `merge.py`, `write_policies.py` |
| Oireachtas production orchestration | `.github/workflows/oireachtas_refresh_validation_orchestrator.yml` plus reusable refresh/validation workflows |
| Oireachtas regression/unit tests | `tests/test_oireachtas_*.py` |
| Member metrics | `process/build_member_profile_metrics.py` and `.github/workflows/build_member_profile_metrics_2025.yml` |
| Instagram system | `instagram/`, `process/instagram_*.py`, Instagram workflow files |
| Reusable LLM runner | `process/llm_table_runner.py`, `tasks/*.yml`, `.github/workflows/llm_task_controller_template.yml` |
| Implementation-era Oireachtas plans/handoffs | `docs/oireachtas_*.md`; supporting or historical evidence only unless confirmed by current code/runtime |

## Repository Structure

```text
.github/workflows/    GitHub Actions controllers, tests, trials, maintenance and legacy workflows
configs/              Checked-in configuration; currently centred on configs/oireachtas/
docs/                 Oireachtas plans, diagnostics, decisions, handoffs and validation evidence
extract/              Source acquisition and canonical Oireachtas package plus older extraction scripts
instagram/            Campaign specifications, renderer, templates, mappings and media generators
process/              Downstream processing, Oireachtas operational helpers, metrics, rendering, LLM and utilities
tasks/                YAML task definitions for the generic LLM table runner
tests/                Oireachtas and Instagram automated tests and fixtures
requirements.txt      Shared Python dependency list
README.md              Title only; not an implementation guide
```

### `configs/`

`configs/oireachtas/` currently contains four configuration sources:

- `api_params.yml`: Oireachtas API defaults, endpoint aliases, default Dáil/house settings, S3 defaults, review settings.
- `tables.yml`: canonical table registry, including layer, status, cadence, endpoint, primary key, description and exact columns.
- `write_policies.yml`: write strategy and selected relationship/time-validity rules.
- `downstream_contracts.yml`: compatibility dataset contracts and comparison thresholds.

### `extract/`

The current canonical Oireachtas implementation is `extract/oireachtas/`. Important groups include:

- API/client/discovery: `client.py`, `discovery.py`, `partitioned_fetch.py`.
- schema/config loading: `schemas.py`, `write_policies.py`.
- storage/publication: `io_s3.py`, `batch.py`, `merge.py`, `history_dedupe.py`.
- table builders: `table_*.py` for silver, gold and control products.
- debate XML parsing: `xml_debates.py`.
- downstream compatibility/cutover checks: `downstream_compat.py`, `compat_comparison.py`, `cutover_comparison.py`, `mismatch_review.py`, `contracts.py`.
- current enrichment replacements: `enrichment_constituency_images.py`, `enrichment_member_photo_urls.py`, `enrichment_member_summaries.py`, `enrichment_speech_issue_labels.py`.
- review/evidence: `review.py`, `member_profile_trial_report.py`.

Older top-level files such as `extract/monthly_extract.py`, `extract/monthly_members_extract.py`, and `extract/debates_xml_to_csv_s3.py` are not treated as the canonical unified implementation merely because they remain in the repository.

### `process/`

The current tree contains several distinct responsibilities:

- Oireachtas operations: `oireachtas_batch_control.py`, `oireachtas_refresh_inputs.py`, `oireachtas_seed_candidate.py`, `oireachtas_reassemble_candidate.py`, contract staging/validation, consumer smoke, audit and validation-repair helpers.
- Member analytics: `build_member_profile_metrics.py` plus a small historical/compatibility wrapper `build_member_profile_metrics_2025.py`.
- Instagram/content: `instagram_render_campaign.py`, `instagram_render_post.py`, `instagram_template_pipeline.py`, preview, copy-pack, media, queue and AI-edit helpers.
- Generic LLM execution: `llm_table_runner.py`.
- Retained legacy/enrichment utilities: `constituency_images_indexer.py`, `members_background_summarizer.py`, `members_photo_urls.py`, `speech_issue_classifier.py`, `delete_s3_column.py`, debate conversion/build scripts.
- Editorial/experimental workflows: `ridiculous_sentences_experiments.py`, `ridiculous_sentences_weekly.py`.

Status and successor mapping for retained legacy/editorial files is deferred to the assigned P2/P3 documentation rather than guessed here.

### `instagram/`

The current tree includes:

- `campaigns/` for campaign-specific briefs, render specs, fixture data and review records;
- `renderer/` for local deterministic rendering and data/context handling;
- `templates/` for HTML/CSS and JSON layout/palette/schema assets;
- `media_generators/` for reusable chart/table image generators;
- `mappings/` for external-template mappings;
- `specs/` for test/input specifications;
- implementation notes for deterministic and AI image approaches.

The repository page establishes location and ownership only; detailed rendering/content behavior is documented separately under P1.

### `tasks/`

The task directory currently contains `Absence_Reasons.yml`, `In_Government.yml`, and `llm_task_template.yml`. The generic template demonstrates an S3 input/output contract, selected/id/prompt-variable columns, prompt, OpenAI model/tool settings, retry/autosave settings, write mode and output validation.

## Primary Entry Points

### Unified Oireachtas tables

```bash
python -m extract.oireachtas.build_table --list-tables
python -m extract.oireachtas.build_table --table <table_name> --mode test
```

For requested candidate publication, a valid immutable batch ID is required. Production orchestration should normally use the GitHub Actions controller rather than ad-hoc manual publication.

### Oireachtas batch control

`process/oireachtas_batch_control.py` is the command-line control surface used by workflows to inspect, assemble, promote and roll back immutable Oireachtas batches.

### Member Profile Metrics Builder

```bash
python process/build_member_profile_metrics.py
```

The script derives its target year and S3 input/output paths from environment variables. Its current default inputs are the unified Oireachtas compatibility datasets for members, votes, photos and classified debate issues. When `OIREACHTAS_BATCH_ID` is set, outputs are written into that candidate batch under `consumers/member_profile_metrics/`; otherwise it retains legacy `processed/members/` output paths.

### Reusable LLM Task Runner

```bash
python process/llm_table_runner.py <task_config.yml>
```

The runner reads CSV from S3, resolves an ID, renders up to five prompt variables, calls the OpenAI Responses API, validates/repairs output, autosaves progress and writes CSV plus Parquet. It supports resumable missing-value fills, explicit overwrite, `full_table` or `processed_only` writes, optional web search, retry/backoff and simple output validation.

### Instagram campaign rendering

`process/instagram_render_campaign.py` is used by `.github/workflows/instagram_campaign_render.yml`. That manual workflow renders a selected campaign spec, builds a copy pack and gated publish queue, and can optionally upload review previews to S3. The workflow explicitly states that it does not publish, schedule or approve Instagram content.

## Workflow Families

The repository has a large GitHub Actions surface. Treat workflows by family rather than assuming every active workflow has equal production status.

### Current Oireachtas production/control family

The current production controller is `o...refresh_validation_orchestrator.yml`, supported by reusable refresh/validation workflows, cadence wrappers, compatibility/consumer validation, batch-control, release-readiness and repair/test workflows.

Scheduled production behavior is described in the Irish Politics Analytics architecture and will receive a dedicated P0 runbook.

### Downstream/manual operational family

Examples verified in source include:

- `build_member_profile_metrics_2025.yml` — manual, target-year member metrics builder with optional candidate batch ID.
- `instagram_campaign_render.yml` — manual campaign render/review workflow.
- `llm_task_controller_template.yml` — manual LLM task controller using AWS and OpenAI credentials.

### Trial, repair, patch, legacy and editorial workflows

The workflow tree also contains enrichment trials, validation fixes, repair CI, historical manual extractors, destructive maintenance, Instagram experiments/patch workflows, and editorial generation. `state: active` in GitHub only means the workflow file is enabled; it does not prove that the workflow is current production architecture. Those files require target-specific status reconciliation in P2/P3.

## Dependencies and Runtime

`requirements.txt` currently declares:

```text
requests
boto3
pandas
openai>=1.99.2
pyarrow
pyyaml
beautifulsoup4
jinja2
playwright
pillow
matplotlib
cairosvg
```

Different workflow families use different Python versions. Current Oireachtas production workflows and the member-metrics workflow use Python 3.12. The inspected Instagram campaign render and generic LLM task controller use Python 3.11. Do not assume one repository-wide interpreter version without checking the controlling workflow.

There is no package lockfile or pinned full dependency set in the inspected root; most dependencies are unpinned except the minimum OpenAI version. This is a reproducibility limitation.

## External Services and Data Sources

Verified repository integrations include:

- public Oireachtas API and Oireachtas-hosted source files;
- AWS S3;
- GitHub Actions and GitHub artifact storage;
- OpenAI Responses API for LLM-based workflows;
- external/template-provider mappings in the Instagram subsystem, alongside a local deterministic renderer.

Presence of provider mapping/spec files does not prove a particular external provider is required for every current Instagram path.

## Storage and Data Boundaries

The current unified Oireachtas data foundation defaults to bucket `eirepolitic-data` in `ca-central-1`, with canonical logical products and compatibility products under `processed/oireachtas_unified/` and immutable production candidates under `processed/oireachtas_unified/batches/<batch_id>/`.

Other repository components retain older or separate S3 prefixes, for example legacy member metric and LLM task paths under `processed/members/` and Instagram preview paths. Do not silently rewrite those paths into the unified namespace; migration/cutover state must be established from the component implementation.

## Authentication and Security

Verified workflow credential names include:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION` in workflows that source region from a secret
- `OPENAI_API_KEY` for LLM workflows

Current Oireachtas production workflows use non-secret checked-in region/bucket values and AWS access-key secrets. The exact live IAM permissions behind those credentials are not proven by this repository and remain an external AWS verification item if exact access control becomes necessary.

Never commit secret values, private URLs tied to individuals, personal account identifiers or credentials. Document secret **names** and trust boundaries only.

## Tests and Validation

The `tests/` tree currently contains Instagram renderer fixtures/tests and a focused Oireachtas suite covering:

- immutable batch control;
- business-key merge behavior;
- compatibility adapters;
- control manifest counts;
- downstream contracts;
- history deduplication;
- API pagination and partitioned fetch;
- refresh orchestration and table order;
- repair regressions;
- candidate seeding;
- write semantics.

Repository-level workflow validation also includes dedicated Oireachtas CI/test/acceptance workflows and runtime validation inside refresh pipelines.

Testing is not uniform across every legacy, Instagram, LLM and editorial script; absence of a matching unit test should not be interpreted as validation.

## Safe Change and Deployment Procedure

For Oireachtas production changes:

1. Identify the implementation and configuration files controlling the behavior; do not update handoff/planning Markdown as a substitute for code.
2. Update or add focused tests for merge, orchestration, contract or schema behavior when applicable.
3. Use `--mode test` or dedicated CI/test workflows for table-level changes before candidate publication.
4. Use the immutable candidate-batch path for production-sized validation rather than writing directly to logical production objects.
5. Run downstream contracts, compatibility/mismatch validation and consumer smoke checks when the changed data can affect consumers.
6. Promote only a `validated` batch.
7. Verify the production pointer after promotion. Use the batch rollback controls if validation of the promoted pointer fails or an approved rollback is required.
8. Preserve previous/legacy paths until the relevant cutover/successor decision is verified.

For downstream/manual components, use the component’s controlling workflow and review outputs. Do not infer that a manual render/LLM workflow publishes externally unless its implementation explicitly does so.

## Troubleshooting Orientation

Start from the controlling workflow and its generated artifacts/logs, then trace to the called Python module and configuration. For Oireachtas failures, also inspect the candidate batch manifest, table DQ output, downstream-contract results and production/previous pointers.

Common repository-wide causes include missing AWS/OpenAI credentials, incompatible dependency changes, malformed YAML/configuration, missing S3 objects/columns, Oireachtas source/API failures, and stale assumptions in older scripts about pre-unified S3 keys.

## Historical and Successor Map

The repository intentionally contains implementation generations side by side. At repository level:

- `extract/oireachtas/` is the current canonical unified Oireachtas extraction/table framework.
- current `extract/oireachtas/enrichment_*` and compatibility adapters coexist with earlier `process/` enrichment scripts.
- `process/llm_table_runner.py` is the current reusable framework target; the archived LLM Column Creator is predecessor documentation, not a competing current architecture page.
- archive pages for constituency images, debate issue classification, member images, member summaries and S3 column deletion remain historical records until their retained source/workflow status is reconciled under P2/P3.

No stronger active/retired claim is made here without target-specific evidence.

## Known Limitations

- Root README documentation is effectively absent.
- Shared dependencies are not comprehensively pinned.
- Workflow enablement is not the same as production intent; the repository contains many trials, patches, legacy/manual tools and experiments.
- Python runtime versions differ by workflow family.
- Exact live AWS IAM/S3 account controls are external to checked-in source.
- Detailed per-table Oireachtas lineage and detailed P1/P2/P3 component operation are intentionally delegated to dedicated documentation rather than duplicated here.

## Next Safe Development Action

Document the Unified Oireachtas Data Platform as the canonical P0 system beneath the Irish Politics Analytics umbrella. That document should define extraction, normalized table layers, dependency/lineage behavior, batch publication, compatibility outputs, validation and recovery using current implementation and configuration.

## Related Documents

- [Irish Politics Analytics](/projects/systems/irish-politics-analytics/)
- [IPA / Oireachtas documentation workstream plan](/projects/high-director/ipa-oireachtas-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: full `eirepolitic-data-pipeline` repository tree; `requirements.txt`; `configs/`; `extract/`; `process/`; `instagram/`; `tasks/`; `tests/`; `docs/`; Oireachtas workflow tree; `build_member_profile_metrics_2025.yml`; `instagram_campaign_render.yml`; `llm_task_controller_template.yml`; `process/build_member_profile_metrics.py`; `process/llm_table_runner.py`; `tasks/llm_task_template.yml`; current Oireachtas core implementation/configuration inspected for the umbrella architecture.
- Verification scope: repository purpose, structure, implementation families, primary entry points, dependency/runtime model, workflow families, security boundary, testing, safe change procedure and active-versus-legacy classification rules.
