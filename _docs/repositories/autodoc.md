---
title: autodoc
summary: Repository architecture and operational boundaries for the AutoDoc documentation-generation system.
section: repositories
doc_type: repository
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 31
permalink: /projects/repositories/autodoc/
tags:
  - autodoc
  - python
  - github-actions
  - openai
  - appsmith
  - documentation
---

# autodoc

## Summary

`autodoc` is the source repository for AutoDoc, a configuration-driven documentation-generation system. Its current backend connects repository-hosted project configuration to source enrichment, OpenAI-backed section-fact extraction, template-based Markdown rendering, OpenAI-backed review/concision, retained generated/reviewed artifacts, and optional publication of a reviewed Markdown file into `eirepolitic.github.io`.

The system is not a single Python command. GitHub Actions workflows are the operational control plane and call focused Python stage entry points under `process/`. Project configuration and intermediate artifacts are persisted inside the repository under `doc_configs/` and `docs/`.

The Appsmith intake/configuration UI is an upstream client of this repository boundary. Repository evidence contains a detailed handoff describing the captured Appsmith implementation, but exact current live Appsmith state has not yet been verified. Current backend workflows and Python source take precedence over older handoff descriptions when they conflict.

## Current Implementation State

Verified current implementation areas include:

- configuration/index files under `doc_configs/<owner>/`;
- asset enrichment via `process/enrich_configs.py`;
- section-fact extraction via `process/section_extract.py`;
- template/Markdown rendering via `process/render_sections.py`;
- review/concision via `process/review_doc.py`;
- owner index rebuilding via `process/update_index.py`;
- automatic orchestration in `.github/workflows/autodoc_pipeline.yml`;
- manual/recovery workflows for enrichment, extraction, rendering, review, index rebuild, and publication;
- reviewed Markdown website publication via `.github/workflows/publish_to_website.yml`;
- retained base/enriched configs, section-summary CSVs, generated Markdown, and reviewed Markdown.

The repository also contains historical generated documentation for projects outside the AutoDoc system itself. Those artifacts are outputs/evidence, not stronger authority than current workflow/Python source.

## Source of Truth

- Repository: `autodoc`.
- Default branch: `main`.
- Automatic pipeline: `.github/workflows/autodoc_pipeline.yml`.
- Manual stage workflows: `.github/workflows/enrich_configs.yml`, `section_extract.yml`, `render_docs.yml`, `review_doc.yml`, `index_rebuilder.yaml`, `publish_to_website.yml`.
- Python stage entry points: `process/enrich_configs.py`, `section_extract.py`, `render_sections.py`, `review_doc.py`, `update_index.py`.
- Runtime dependencies: `requirements.txt`.
- Base/type templates: `templates/base.md` and `templates/types/*.md`.
- Project configuration/registry: `doc_configs/<owner>/*.json`, `*.enriched.json`, `_index.json`, and `summaries/*.csv`.
- Generated/reviewed Markdown: repository `docs/` tree.
- Documentation discovery evidence: `_docs/high-director/repository-scan-autodoc.md` in `eirepolitic.github.io`.

Evidence precedence for current backend behavior is executable workflow/Python source first, then current persisted configuration/intermediate artifacts, then generated/reviewed outputs, then historical handoff text.

## Repository Structure

```text
autodoc/
├── .github/workflows/
│   ├── autodoc_pipeline.yml       # automatic multi-stage orchestration
│   ├── enrich_configs.yml         # manual enrichment/recovery stage
│   ├── section_extract.yml        # manual extraction/recovery stage
│   ├── render_docs.yml            # manual render/recovery stage
│   ├── review_doc.yml             # manual review/recovery stage
│   ├── index_rebuilder.yaml       # manual owner index rebuild
│   └── publish_to_website.yml     # reviewed Markdown -> website repository
├── doc_configs/
│   └── <owner>/
│       ├── <slug>.json            # base configuration
│       ├── <slug>.enriched.json   # enrichment output
│       ├── _index.json            # owner project registry
│       └── summaries/<slug>.csv   # section-fact extraction output
├── docs/                           # generated and reviewed Markdown artifacts
├── process/
│   ├── enrich_configs.py
│   ├── section_extract.py
│   ├── render_sections.py
│   ├── review_doc.py
│   └── update_index.py
├── templates/
│   ├── base.md
│   └── types/                      # generic, pipeline, dataset, dashboard, investigation
└── requirements.txt
```

## Inputs and Outputs

### Inputs

Primary inputs are:

- a base project JSON configuration under `doc_configs/<owner>/<slug>.json`;
- the owner/slug or config path selected by workflow dispatch/automatic orchestration;
- configured asset references that enrichment resolves from supported source modes;
- Markdown templates under `templates/`;
- OpenAI API access for extraction and review stages;
- GitHub repository access for config/artifact commits and source resolution;
- a reviewed Markdown path for website publication.

The exact base/enriched config schema and supported asset-source modes are documented separately because they are stage contracts rather than repository-overview details.

### Outputs

Persistent outputs include:

- `doc_configs/<owner>/<slug>.enriched.json`;
- `doc_configs/<owner>/summaries/<slug>.csv`;
- generated Markdown in `docs/`;
- reviewed Markdown in `docs/` using the review-stage naming/path convention;
- rebuilt `doc_configs/<owner>/_index.json`;
- optionally, a copied reviewed Markdown file committed to `eirepolitic.github.io` by the publication workflow.

Stage workflows also produce GitHub Actions logs and commit history. Those are operational evidence but not a replacement for repository-persisted stage outputs.

## Dependencies

`requirements.txt` is the authoritative Python dependency declaration for the current backend. Verified external platform dependencies include:

- GitHub Actions;
- GitHub repository/content APIs and git operations;
- OpenAI API;
- configured HTTP/GitHub asset sources;
- Appsmith as the captured upstream intake/configuration UI;
- `eirepolitic.github.io` as the reviewed-document publication target.

Exact package versions and model names belong to the stage-specific pages and should be re-verified there before publication.

## Configuration

Configuration is repository-hosted rather than centralized in one runtime settings file. The core persisted families are:

| Path | Role |
| --- | --- |
| `doc_configs/<owner>/<slug>.json` | Base project configuration/intake contract |
| `doc_configs/<owner>/<slug>.enriched.json` | Base configuration plus resolved asset content/metadata |
| `doc_configs/<owner>/_index.json` | Owner-scoped project registry used by intake/discovery flows |
| `doc_configs/<owner>/summaries/<slug>.csv` | Section-fact extraction contract consumed by rendering |
| `templates/base.md` | Common Markdown section skeleton |
| `templates/types/<type>.md` | Optional type-specific section extension |

`process/update_index.py` rebuilds `_index.json` from base configuration files and derives each registry entry's `updated_at` from the latest Git commit timestamp for that config file, not from the config JSON's own `updated_at` value.

## Local Development

The current repository is primarily operated through GitHub Actions. Local execution of a stage requires the dependencies from `requirements.txt`, the expected config/intermediate files, and any required environment variables/credentials for that stage.

Do not run OpenAI-backed or repository-writing stages merely to test documentation. Use existing source and artifacts first. Any cost-bearing API execution or access-control change requires an explicit reason and approval where it changes operation rather than documentation.

## Deployment and Release

AutoDoc is job-oriented rather than deployed as a long-running service. GitHub Actions workflows execute individual or automatic stage sequences and commit durable results back to the `autodoc` repository.

The reviewed-document publication workflow is a separate boundary: `.github/workflows/publish_to_website.yml` clones `eirepolitic.github.io` using the configured `WEBSITE_PAT`, copies a reviewed Markdown file, commits, and pushes it to the website repository.

This is **CURRENT VERIFIED BEHAVIOR**. It must not be confused with **CURRENT DOCUMENTATION GOVERNANCE**, which requires branch/PR, `Validate documentation`, merge, then matching Pages success for documentation changes. The current AutoDoc publication workflow does not implement that governance sequence.

## Validation

Validation of this repository overview is documentary: claims are checked against the current repository tree, workflow YAML, Python stage files, templates, configuration artifacts, and publication workflow.

For changes to `eirepolitic.github.io`, the required documentation gate is:

1. focused PR;
2. successful `Validate documentation` workflow;
3. merge;
4. successful matching GitHub Pages deployment for the merge commit.

No AutoDoc implementation change is implied by documenting a mismatch or limitation.

## Operations

The automatic pipeline is controlled by `.github/workflows/autodoc_pipeline.yml`. Current source serializes automatic runs with an AutoDoc-specific concurrency group and excludes bot-authored commits from recursively retriggering the pipeline.

Manual workflows provide stage-level recovery for enrichment, extraction, rendering, review, and index rebuild. These paths are important operationally because persistent intermediate files allow recovery from later-stage failures without necessarily recreating every earlier stage.

Detailed triggers, permissions, stage chaining, trust boundaries, and rerun rules belong to the orchestration/security and artifact-lifecycle pages.

## Failure Modes

- **Invalid or missing base configuration:** downstream stages cannot locate required project metadata/assets. Verify the exact config path and schema before rerun.
- **Asset resolution failure:** enrichment records per-asset success/error information and can continue past an individual unresolved asset; inspect the enriched config before continuing.
- **Missing enriched config or summary CSV:** extraction/rendering cannot satisfy their stage contract and fail rather than inventing missing state.
- **OpenAI/API failure:** extraction/review can fail after retry/error handling; preserve existing intermediate artifacts and rerun only the failed stage where safe.
- **Index drift:** rebuild `_index.json` with the dedicated workflow/process rather than manually guessing registry entries.
- **Publication-path failure:** `publish_to_website.yml` validates the reviewed source path before copying/pushing; inspect the workflow error and reviewed artifact rather than bypassing path checks.
- **Website governance mismatch:** a direct AutoDoc publication push may not have passed the current PR/validation discipline. Treat that as a governance gap to document, not authorization to redesign the workflow.

## Security and Access

Secret/token names visible in the current system may be documented, including `OPENAI_API_KEY`, `GITHUB_TOKEN`, `AUTODOC_GITHUB_TOKEN`, and `WEBSITE_PAT`. Their values must never be published.

Verified trust boundaries include:

- Appsmith/caller to GitHub-hosted config/index files;
- GitHub Actions runner to `autodoc` repository contents;
- enrichment runner to configured source hosts/repositories;
- extraction/review runner to OpenAI;
- publication runner to `eirepolitic.github.io` using `WEBSITE_PAT`.

Workflow-declared permissions establish intended GitHub token capabilities for a run, but do not prove the exact live scope of external PATs or Appsmith credentials.

## Known Limitations

- Exact current live Appsmith UI/actions/settings are not yet verified; repository handoff evidence is captured-state authority only.
- Current backend source has drifted from portions of the historical handoff, including older generation workflow/script references.
- Generated/reviewed documents are derived outputs and may contain stale historical implementation descriptions.
- Current website publication bypasses the newer documentation PR/validation/Pages governance path.
- Live PAT scopes, GitHub repository rules, and Appsmith access-control state are outside repository proof unless separately supplied as sanitized authoritative evidence.

## Outstanding Work

The persistent AutoDoc workstream plan tracks the remaining component pages. Immediate next components are the Appsmith/config/index boundary, automatic pipeline/trust model, and reviewed-document publication boundary, followed by the individual P1 stages and artifact lifecycle/recovery.

## Next Safe Development Action

Finish and publish the focused repository/system architecture documentation through the required validation/merge/Pages gate. Then verify the Appsmith/config/index boundary in a separate focused branch, using repository handoff evidence first and requesting a current live Appsmith source only where exact current state is necessary.

## Related Documents

- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)
- [Repository scan — AutoDoc](/projects/high-director/repository-scan-autodoc/)
- [AutoDoc system architecture](/projects/systems/autodoc/)
- [AutoDoc project landing page](/autodoc/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc` `main` tree; primary workflow files; `process/enrich_configs.py`, `section_extract.py`, `render_sections.py`, `review_doc.py`, `update_index.py`; `doc_configs/autodoc/`; full template set; generated/reviewed artifact directories; `requirements.txt`; AutoDoc repository scan and current documentation publishing runbooks.
- Verified by: High Director
- Verification scope: repository purpose, structure, source-of-truth hierarchy, stage boundaries, artifacts, operations, security/publication boundaries, and known drift.
- Unverified areas: exact current live Appsmith configuration and external credential/access-policy state.
