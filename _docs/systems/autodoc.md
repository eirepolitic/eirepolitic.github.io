---
title: AutoDoc
summary: System architecture for the configuration-driven AutoDoc documentation-generation pipeline from intake boundary through reviewed Markdown publication.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 31
permalink: /projects/systems/autodoc/
tags:
  - autodoc
  - github-actions
  - openai
  - appsmith
  - documentation
---

# AutoDoc

## Summary

AutoDoc is a repository-backed documentation-generation system whose current verified backend is implemented in the `autodoc` repository. It takes project configuration persisted under `doc_configs/`, enriches configured source assets, extracts section facts through OpenAI, renders Markdown from a base/type template contract, performs an OpenAI review/concision pass, retains generated/reviewed artifacts, and can publish a reviewed Markdown file into `eirepolitic.github.io`.

The system crosses several trust boundaries: Appsmith/caller to GitHub configuration, GitHub Actions to repository contents and configured asset sources, GitHub Actions to OpenAI, and the publication workflow from `autodoc` into the documentation repository.

## Current Implementation State

Current executable backend stages are implemented and repository-persisted. The full automatic path is orchestrated by `.github/workflows/autodoc_pipeline.yml`, with manual stage workflows providing rerun/recovery entry points.

The upstream Appsmith intake/configuration application is evidenced by a detailed repository handoff. That handoff is authoritative for the captured implementation at the time it was recorded, but exact current live Appsmith state is not yet verified. Current backend workflows/Python files outrank historical backend descriptions where they differ.

A separate governance distinction is critical:

- **CURRENT VERIFIED BEHAVIOR:** `publish_to_website.yml` directly clones and pushes a reviewed Markdown file into `eirepolitic.github.io` using `WEBSITE_PAT`.
- **CURRENT DOCUMENTATION GOVERNANCE:** documentation changes should use branch/PR, successful `Validate documentation`, merge, and successful matching GitHub Pages deployment.

The current publication workflow does not implement the newer governance sequence. This page records the mismatch without redesigning it.

## System Boundary

Included in AutoDoc:

- Appsmith intake/configuration boundary as evidenced by repository handoff/current live source when later supplied;
- `doc_configs/<owner>/` base/enriched configs, owner registry, and section-summary CSVs;
- AutoDoc GitHub Actions workflows;
- Python stage processors under `process/`;
- Markdown templates under `templates/`;
- generated/reviewed Markdown under `docs/`;
- reviewed-document publication into `eirepolitic.github.io`.

Outside the AutoDoc implementation boundary:

- the full downstream systems being documented by AutoDoc;
- GitHub/Appsmith/OpenAI account administration beyond the names/interfaces required by AutoDoc;
- the internal GitHub Pages build system of `eirepolitic.github.io`, except as the final documentation-governance verification gate.

## Authoritative Sources

For current backend behavior:

1. current `.github/workflows/*.yml`/`.yaml` in `autodoc`;
2. current `process/*.py` in `autodoc`;
3. current persisted config/intermediate/artifact files;
4. historical handoff/generated documentation.

For Appsmith behavior, current sanitized live Appsmith source takes precedence if supplied. Until then, the detailed repository handoff is authoritative only for its captured point in time.

Primary files:

- `.github/workflows/autodoc_pipeline.yml`
- `.github/workflows/enrich_configs.yml`
- `.github/workflows/section_extract.yml`
- `.github/workflows/render_docs.yml`
- `.github/workflows/review_doc.yml`
- `.github/workflows/index_rebuilder.yaml`
- `.github/workflows/publish_to_website.yml`
- `process/enrich_configs.py`
- `process/section_extract.py`
- `process/render_sections.py`
- `process/review_doc.py`
- `process/update_index.py`
- `templates/base.md`
- `templates/types/*.md`
- `doc_configs/<owner>/...`
- `docs/...`

## Architecture Overview

```text
Appsmith / configuration caller
        |
        v
GitHub repository boundary
  doc_configs/<owner>/<slug>.json
  doc_configs/<owner>/_index.json
        |
        v
GitHub Actions orchestration
  autodoc_pipeline.yml / manual workflows
        |
        +--> enrich_configs.py
        |      -> <slug>.enriched.json
        |
        +--> section_extract.py
        |      -> summaries/<slug>.csv
        |      -> OpenAI
        |
        +--> render_sections.py
        |      -> templates/base.md + templates/types/<type>.md
        |      -> generated Markdown
        |
        +--> review_doc.py
               -> OpenAI
               -> reviewed Markdown
                       |
                       v
             publish_to_website.yml
             WEBSITE_PAT trust boundary
                       |
                       v
              eirepolitic.github.io
```

## Components

### Intake and configuration boundary

Base configuration lives at `doc_configs/<owner>/<slug>.json`. The captured Appsmith handoff describes creating/updating this file and maintaining the owner `_index.json` through the GitHub Contents API. Exact current live Appsmith implementation is deferred to the dedicated Appsmith/config/index page.

### Owner registry

`process/update_index.py` rebuilds `doc_configs/<owner>/_index.json` from base configuration files. Enriched configs are not treated as separate projects. Registry ordering is deterministic by title, and each entry's `updated_at` is derived from the latest Git commit timestamp for the underlying base config.

### Asset enrichment

`process/enrich_configs.py` reads a base config, resolves configured assets from supported source modes, records resolution status/error information, and writes `<slug>.enriched.json`. Individual asset resolution failures are captured rather than necessarily aborting the whole enrichment pass.

### Section-fact extraction

`process/section_extract.py` consumes the enriched configuration, assembles source context by requested section, calls OpenAI, and writes `doc_configs/<owner>/summaries/<slug>.csv`. The CSV is an explicit persisted intermediate contract consumed by rendering.

### Template and Markdown rendering

`process/render_sections.py` combines `templates/base.md` with the selected `templates/types/<type>.md` extension. Verified type files are `generic.md`, `pipeline.md`, `dataset.md`, `dashboard.md`, and `investigation.md`. Rendering uses extracted section facts; a section without facts is emitted as `_TBD_` rather than fabricated content.

### Review/concision

`process/review_doc.py` consumes generated Markdown, calls OpenAI for a review/concision pass, and writes a reviewed Markdown artifact. Generated and reviewed artifacts are separate lifecycle states.

### Publication boundary

`.github/workflows/publish_to_website.yml` accepts a reviewed AutoDoc Markdown path, validates the expected source-path boundary, clones `eirepolitic.github.io` using `WEBSITE_PAT`, copies the reviewed file, commits, and pushes to the website repository.

This direct push is current implementation behavior, not evidence that the newer documentation governance was followed.

## Data Flow

1. A project base config is created/updated in `doc_configs/<owner>/<slug>.json`.
2. The owner registry may be maintained/rebuilt as `_index.json`.
3. Enrichment resolves configured source assets and writes `<slug>.enriched.json`.
4. Extraction converts enriched source evidence into section-scoped facts persisted as `summaries/<slug>.csv`.
5. Rendering maps those facts into the selected base/type Markdown section structure and writes generated Markdown.
6. Review/concision rewrites the generated document into a reviewed Markdown artifact.
7. Publication may copy the reviewed artifact into `eirepolitic.github.io` and push it directly.
8. Separately, current documentation governance expects PR validation, merge, and matching Pages success before a documentation change is considered complete.

## Inputs

- base project configuration JSON;
- asset references and source-mode configuration;
- selected document type/template structure;
- GitHub repository content available to configured resolvers;
- OpenAI API access for extraction/review stages;
- reviewed Markdown path for publication.

## Outputs

- enriched configuration JSON;
- section-summary CSV;
- generated Markdown;
- reviewed Markdown;
- owner `_index.json` registry rebuilds;
- optionally published Markdown in `eirepolitic.github.io`.

## External Dependencies

- GitHub repositories and GitHub Actions;
- GitHub API/git transport;
- OpenAI API;
- configured HTTP/source hosts used by enrichment;
- Appsmith for the captured intake/configuration UI;
- `eirepolitic.github.io` for publication;
- GitHub Pages for the documentation site's deployment verification.

The exact current availability, permissions, and live account configuration of those services are not inferred from repository source.

## Trust and Security Boundaries

### Appsmith/caller -> GitHub

The intake client can create/update repository-hosted configuration and historically the owner registry. This boundary can influence what downstream assets are fetched and what project configuration the pipeline processes. Token values must never be documented; only the required credential/interface names may be recorded.

### GitHub Actions -> configured asset sources

Enrichment causes Actions runners to read configured external/GitHub sources. Asset source configuration is therefore an input-trust boundary. The dedicated enrichment page documents exact supported modes, path handling, errors, and host behavior.

### GitHub Actions -> OpenAI

Extraction and review send constructed project/document context to OpenAI. `OPENAI_API_KEY` is a secret name only. Exact model/configuration details are documented in the stage pages from current source.

### GitHub Actions -> repository writes

Automatic/manual workflows commit stage outputs back to `autodoc`; the declared workflow permissions and token choice govern those writes. Bot-trigger suppression in the automatic workflow prevents its own output commits from recursively starting the same pipeline path.

### AutoDoc -> documentation repository

Publication uses `WEBSITE_PAT` to cross from `autodoc` into `eirepolitic.github.io`. This is a distinct repository-write boundary and currently bypasses the newer documentation PR/validation gate.

## Failure Behavior

- Enrichment can preserve per-asset resolution errors in the enriched output while allowing other assets to complete.
- Extraction/rendering require their expected upstream persisted stage files and fail when required contracts are absent or invalid.
- OpenAI-backed stages can fail on API/response errors; persisted earlier-stage outputs allow bounded rerun rather than full recreation where safe.
- Rendering uses `_TBD_` for a section with no extracted facts instead of inventing facts.
- Index rebuilding derives registry state from base configs and Git history rather than trusting an independently edited registry as the only source.
- Publication validates the reviewed artifact/path boundary before copying and pushing.

## Operations and Recovery

The automatic workflow provides the standard chained path. Manual workflows exist for enrichment, extraction, rendering, review, index rebuilding, and website publication so an operator can rerun a bounded stage after verifying its upstream artifact.

Safe recovery principle: identify the last valid persisted stage artifact, correct the actual cause, and rerun only the failed/downstream stage where the current workflow supports it. Do not delete or overwrite prior evidence solely to force a clean run.

Detailed commands/dispatch inputs and artifact naming belong to the dedicated lifecycle/recovery runbook.

## Current Documentation Governance

Documentation changes in `eirepolitic.github.io` are governed by:

1. focused branch and PR;
2. successful `Validate documentation`;
3. merge;
4. successful matching GitHub Pages deployment for the merge commit.

This workstream follows that discipline before beginning the next major AutoDoc component. The fact that `publish_to_website.yml` directly pushes does not override the documented site governance.

## Known Limitations

- Exact live Appsmith state is not yet verified.
- Historical Appsmith/backend handoff text contains drift from current backend source and must be dated/classified rather than treated as current implementation.
- Live PAT scopes, GitHub repository rules, OpenAI account settings, and Appsmith access policy are not proven by repository source.
- Direct website publication and current documentation governance are misaligned.
- Historical generated documentation can be stale and should not override current executable source.

## Next Safe Development Action

Publish this architecture foundation through the required documentation validation/merge/Pages gate. Then create a separate focused Appsmith/config/index page, using the captured repository handoff as historical authoritative evidence and requesting one live Appsmith source only where current implementation cannot be established safely from repository evidence.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)
- [Repository scan — AutoDoc](/projects/high-director/repository-scan-autodoc/)
- [Documentation site](/projects/systems/documentation-site/)
- [Publish a documentation change](/docs/runbooks/publish-documentation-change/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc` `main` repository tree; primary workflow files; all current `process/*.py` stage entry points; AutoDoc configs/intermediate artifacts; templates; generated/reviewed artifact directories; `requirements.txt`; documentation-site operations/publication runbooks and validator workflow.
- Verified by: High Director
- Verification scope: system boundary, components, data flow, trust boundaries, persistence model, failure/recovery model, and publication-governance mismatch.
- Unverified areas: exact current live Appsmith configuration and external credential/access-policy state.
