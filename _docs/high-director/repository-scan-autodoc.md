---
title: Repository Scan — autodoc
summary: Documentation-target inventory for the AutoDoc Appsmith intake, GitHub-backed configuration, LLM documentation-generation, review, and website-publication system.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 34
permalink: /projects/high-director/repository-scan-autodoc/
---

# Repository Scan — `autodoc`

## Repository role

`autodoc` is a documentation-generation system built around a GitHub-backed configuration registry, an external Appsmith intake/configuration UI, Python enrichment/generation stages, OpenAI calls, GitHub Actions orchestration, generated/reviewed Markdown, and a workflow that can publish reviewed documents into `eirepolitic.github.io`.

The repository also contains historical/generated documentation for several older `eirepolitic` pipelines. Those generated files are evidence/artifacts, not separate current implementations.

## Documentation targets

### 1. `autodoc` repository

**Categories:** repository, documentation automation system, AI pipeline, deployment/operations.

Document the repository layout, current maturity, workflow inventory, Python runtime/dependencies, config/document artifact lifecycle, secrets/configuration names, and links to the components below.

### 2. AutoDoc Appsmith Intake and Configuration Application

**Categories:** Appsmith application, user interface, GitHub integration, authentication boundary, external connection.

Repository evidence:

```text
doc_configs/autodoc/autodoc_app.json
doc_configs/autodoc/autodoc_app.enriched.json
docs/autodoc/generic/autodoc_app.md
docs/autodoc/generic/reviewed/autodoc_app.md
```

The source config contains a pasted technical handoff describing an Appsmith app that:

- captures project/type/title/context and up to five source assets;
- supports new and rerun/edit modes;
- reads/writes `doc_configs/<project>/<doc_key>.json` and `_index.json` through the GitHub Contents API;
- uses a fine-grained GitHub PAT in Appsmith query authentication;
- relies on GitHub commits to trigger the backend pipeline rather than directly dispatching Actions.

The external live Appsmith application itself is **not directly inspectable from this repository**. Full documentation should use the repository handoff as source evidence and later compare it with live Appsmith configuration before claiming current widget/query/action state.

This is the current authoritative implementation relationship behind the `/autodoc/` Appsmith embed already identified in `eirepolitic.github.io`.

### 3. AutoDoc Configuration Schema and Project Index Registry

**Categories:** configuration model, metadata registry, GitHub-backed data store, index lifecycle.

Evidence:

```text
doc_configs/<project>/<doc_key>.json
doc_configs/<project>/<doc_key>.enriched.json
doc_configs/<project>/_index.json
process/update_index.py
.github/workflows/index_rebuilder.yaml
```

Observed base config fields include:

```text
project
type
title
doc_key
context
updated_at
assets[]
```

Assets contain source/type/locator/content metadata. Enriched files add resolved source content and enrichment metadata. `_index.json` is rebuilt from base configs and stores document key/title/type/last-updated metadata for project-level selection.

This should be one canonical configuration/data-model page rather than separate pages per JSON file.

### 4. Asset Enrichment / Source Resolution Stage

**Categories:** ingestion/enrichment pipeline, GitHub API integration, external HTTP retrieval, source provenance.

Evidence:

```text
process/enrich_configs.py
.github/workflows/enrich_configs.yml
```

Verified source modes:

```text
pasted
github_path
github_url
```

The implementation resolves GitHub blob/raw URLs through the GitHub Contents API where possible, supports generic HTTP GET for other URLs, preserves text line structure, represents binary content as base64, records resolution metadata/errors, and writes `.enriched.json`.

Full documentation should cover private-repository access, token handling, binary/text behavior, provenance metadata, error modes, and external-URL trust/security boundaries.

### 5. LLM Section-Fact Extraction Stage

**Categories:** OpenAI integration, documentation-generation pipeline, template processing, intermediate data product.

Evidence:

```text
process/section_extract.py
.github/workflows/section_extract.yml
```

The stage merges the base and type templates, splits documentation into H2 sections, sends the full enriched JSON to `gpt-4.1-mini` for facts-only section extraction, retries rate limits, and writes:

```text
doc_configs/<project>/summaries/<doc_key>.csv
```

The CSV is a distinct intermediate data product and should be documented as part of the pipeline contract.

### 6. Template and Markdown Rendering System

**Categories:** template system, OpenAI integration, document renderer, generated artifact model.

Evidence:

```text
templates/base.md
templates/types/generic.md
templates/types/pipeline.md
templates/types/dataset.md
templates/types/dashboard.md
templates/types/investigation.md
process/render_sections.py
.github/workflows/render_docs.yml
```

The renderer:

- merges base/type templates;
- fills document metadata placeholders;
- reads section-fact CSV output;
- calls `gpt-4.1-mini` section-by-section using only provided facts;
- adds/updates YAML front matter;
- writes generated Markdown to `docs/<project>/<type>/<doc_key>.md`.

Document template ownership, allowed types, section contracts, front-matter behavior, and missing-fact handling.

### 7. LLM Review / Concision Stage

**Categories:** review workflow, OpenAI integration, generated-document lifecycle.

Evidence:

```text
process/review_doc.py
.github/workflows/review_doc.yml
```

The review stage uses a configurable model (workflow currently sets `gpt-4.1`) to make generated Markdown more concise while instructing it not to change headings/format/order. Reviewed outputs are written under:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

This reviewed-artifact state should be explicitly separated from generated/unreviewed Markdown.

### 8. Automatic AutoDoc Creation Pipeline Orchestrator

**Categories:** GitHub Actions orchestration, AI pipeline, repository write automation, operational runbook.

Evidence:

```text
.github/workflows/autodoc_pipeline.yml
doc_configs/autodoc/autodoc_creation_pipeline.json
```

Current automatic pipeline trigger:

```text
push paths: doc_configs/**/*.json
```

The workflow identifies changed base configs, runs enrichment → section extraction → rendering, regenerates affected project indexes, commits generated/enriched/summaries/docs artifacts, rebases against current `main`, and pushes outputs back to the repository.

Important implementation details:

- `github.actor != 'github-actions[bot]'` prevents bot-generated commits from recursively processing themselves;
- the workflow has `contents: write`;
- `OPENAI_API_KEY`, `AUTODOC_GITHUB_TOKEN`/`GITHUB_TOKEN` are used by the pipeline;
- manual stage-specific workflows also exist for enrichment, extraction, rendering, review, and index rebuilding.

The automatic orchestrator and manual recovery/re-run workflows should be documented together with stage dependencies and concurrency behavior.

### 9. Generated / Reviewed Documentation Artifact Store

**Categories:** data product, documentation lifecycle, generated content repository.

Evidence:

```text
docs/<project>/<type>/<doc_key>.md
docs/<project>/<type>/reviewed/<doc_key>.md
doc_configs/<project>/summaries/*.csv
```

Document lifecycle states should distinguish:

1. base config;
2. enriched config;
3. section-fact summaries;
4. generated Markdown;
5. reviewed Markdown;
6. externally published website copy.

The existing `docs/eirepolitic/pipeline/*` files are generated/historical documentation artifacts for older pipeline configs, not source code for those pipelines.

### 10. Website Publication Workflow

**Categories:** cross-repository deployment, GitHub authentication, documentation publishing, security/control boundary.

Evidence:

```text
.github/workflows/publish_to_website.yml
```

The current manual workflow:

- requires project/type/doc_key/destination inputs;
- selects a reviewed Markdown file;
- uses `WEBSITE_PAT` to clone `eirepolitic.github.io`;
- copies the file into `projects/<dest_type>/<doc_key>.md`;
- commits and pushes directly to the website repository.

**Important control mismatch:** the newer documentation discipline for `eirepolitic.github.io` requires focused branches/PRs, documentation validation before merge, and matching Pages verification. This AutoDoc publisher currently performs a direct push rather than that newer gated flow.

This is a high-priority architecture/operations documentation item and a future design decision candidate. Do **not** change the workflow during discovery without an explicit architecture/security decision.

### 11. AutoDoc Security and Credential Boundaries

**Categories:** security/authentication, secrets, trust boundaries.

Non-secret credential/configuration names observed across source/workflows:

```text
OPENAI_API_KEY
GITHUB_TOKEN
AUTODOC_GITHUB_TOKEN
WEBSITE_PAT
```

The Appsmith handoff also describes a fine-grained GitHub PAT used by Appsmith. No secret values are present in the inspected repository material.

Full documentation should cover:

- Appsmith → GitHub Contents API credential storage and permissions;
- GitHub Actions token/PAT permissions;
- AutoDoc → source-repository access when resolving private assets;
- OpenAI data sent during extraction/render/review;
- cross-repository website publication permissions;
- external URL retrieval and potential sensitive-source ingestion;
- secret/publication sanitization rules.

## Items that are not separate implementation targets

The following are artifacts/fixtures rather than independent systems:

- individual generated docs under `docs/eirepolitic/pipeline/`;
- individual `.enriched.json` files;
- individual section-summary CSV files;
- `.gitkeep` placeholders;
- the `null` file unless future evidence establishes a functional role.

Historical generated docs/configs may be useful provenance when documenting predecessor pipelines, but the implementation source of truth is the actual source repository where available.

## Current-vs-historical evidence boundary

The pasted Appsmith handoff inside `autodoc_app.json` describes some earlier workflow/file names (for example a `generate_docs.yml`/`generate_docs.py` flow) that do not match the current repository tree. Current Python/workflow files are stronger evidence for the backend pipeline as it exists today.

Therefore full documentation should:

- treat the handoff as authoritative evidence for Appsmith UI/query behavior unless live Appsmith configuration later supersedes it;
- treat current repository workflows/scripts as authoritative for backend implementation;
- explicitly record drift between historical handoff text and current pipeline files.

## Preliminary priority

- **P0:** repository/system architecture; Appsmith ↔ GitHub boundary; configuration model; automatic pipeline; security boundaries; website publication/control mismatch.
- **P1:** asset enrichment, LLM section extraction, rendering/templates, review lifecycle.
- **P2:** manual stage workflows/index recovery, generated artifact store/developer reference.
- **P3:** historical generated docs/config artifacts after predecessor mapping.

Final owner-wide priority will be assigned during the post-scan consolidation.

## Verification record

Verified on 2026-08-07 from the complete repository tree plus the current automatic/manual workflows, AutoDoc base configs, enrichment/index/extraction/render/review Python implementations, templates, requirements, and website publication workflow. No secret values were inspected or published. The live external Appsmith app remains a later verification source for exact current UI/query configuration.

## Related Documents

- [Repository Documentation Discovery Initiative]({{ '/projects/high-director/repository-documentation-discovery/' | relative_url }})
- [Repository Scan — bb-comp-prices]({{ '/projects/high-director/repository-scan-bb-comp-prices/' | relative_url }})
- [Repository Scan — degenerate_investigator]({{ '/projects/high-director/repository-scan-degenerate-investigator/' | relative_url }})
- [Repository Scan — Overlord]({{ '/projects/high-director/repository-scan-overlord/' | relative_url }})
