---
title: AutoDoc
summary: System architecture for the configuration-driven AutoDoc documentation-generation pipeline from verified Appsmith intake through generated/reviewed artifact publication.
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

AutoDoc is a repository-backed documentation-generation system implemented in `autodoc`. It accepts project configuration through the verified Appsmith/GitHub boundary, resolves source assets, extracts section facts with OpenAI, renders Markdown from base/type templates, optionally produces a separate LLM review/concision artifact, retains all major stages in Git, and can publish reviewed Markdown into `eirepolitic.github.io`.

The system crosses distinct trust boundaries: Appsmith -> GitHub configuration, Actions -> source hosts, Actions -> OpenAI, Actions -> repository writes, and AutoDoc publication -> documentation repository.

## Current Implementation State

Current Appsmith behavior is verified from the sanitized user-supplied export dated `2026-08-07`. It supersedes the older repository handoff for current Appsmith claims.

Current backend behavior is verified from current `autodoc` workflows/Python source.

Critical governance distinction:

- **CURRENT VERIFIED BEHAVIOR:** `publish_to_website.yml` directly clones and pushes reviewed Markdown into `eirepolitic.github.io` using `WEBSITE_PAT`.
- **CURRENT DOCUMENTATION GOVERNANCE:** documentation changes use branch/PR, successful `Validate documentation`, merge, and successful matching Pages deployment.

No architecture redesign was made by this documentation workstream.

## System Boundary

Included:

- Appsmith `Submit`/`DocsViewer` intake/control surface;
- `doc_configs/<project>/` configuration/intermediate/registry state;
- GitHub Actions orchestration and recovery workflows;
- Python stage processors;
- Markdown templates;
- raw/reviewed Markdown artifacts;
- optional reviewed-document publication into `eirepolitic.github.io`.

Outside the AutoDoc implementation boundary:

- the implementation of systems AutoDoc documents;
- GitHub/Appsmith/OpenAI account administration beyond required interfaces/secret names;
- GitHub Pages internals beyond documentation deployment verification.

## Authoritative Sources

Backend precedence:

```text
current workflows/Python
  > current persisted stage artifacts
  > generated/reviewed documents
  > historical handoff/generated prose
```

Appsmith precedence:

```text
sanitized live export dated 2026-08-07
  > historical repository handoff
```

Primary implementation paths:

```text
.github/workflows/autodoc_pipeline.yml
.github/workflows/enrich_configs.yml
.github/workflows/section_extract.yml
.github/workflows/render_docs.yml
.github/workflows/review_doc.yml
.github/workflows/index_rebuilder.yaml
.github/workflows/publish_to_website.yml
process/enrich_configs.py
process/section_extract.py
process/render_sections.py
process/review_doc.py
process/update_index.py
templates/
doc_configs/
docs/
```

## Architecture Overview

```text
Appsmith Submit / DocsViewer
        |
        v
GitHub repository state
  base config + _index.json
        |
        v
AutoDoc Actions control plane
        |
        +--> enrichment
        |      -> enriched JSON
        |
        +--> extraction
        |      -> summary CSV
        |      -> OpenAI
        |
        +--> rendering
        |      -> raw Markdown
        |      -> OpenAI for fact-bearing sections
        |
        +--> separate review
               -> reviewed Markdown
               -> OpenAI
                       |
                       v
             optional publication
             WEBSITE_PAT boundary
                       |
                       v
              eirepolitic.github.io
```

The automatic push-triggered pipeline currently ends at render. Review and publication are separate dispatches.

## Appsmith Intake and Control

The verified application has two pages:

```text
Submit
DocsViewer
```

`Submit` can create/load base configs, maintain an immediate `_index.json` entry, and create a project `.gitkeep` path.

`DocsViewer` can discover documents, read/edit Markdown, dispatch `review_doc.yml`, check reviewed-file state, and dispatch `publish_to_website.yml`.

Current Appsmith config/index writes are not the final registry authority: `process/update_index.py` can deterministically rebuild `_index.json` from base configs and Git history.

The supplied export contained two distinct GitHub PAT values. Values/raw export were not persisted in documentation. Credential rotation/revocation remains a separate security/access action.

## Artifact Lifecycle

```text
base config
-> enriched JSON
-> section-summary CSV
-> generated/raw Markdown
-> reviewed Markdown
-> optional website copy
```

Separate registry:

```text
_index.json
```

Persistent intermediate state allows bounded recovery instead of always restarting the whole chain.

## Asset Enrichment

`process/enrich_configs.py` supports:

```text
pasted
github_path
github_url
```

Recognized GitHub blob/raw URLs use the GitHub Contents API. Other `github_url` values currently fall through to generic HTTP GET. Text/binary content, provenance metadata, per-asset success/error state, and timestamps are persisted into enriched JSON.

Individual asset failures are normally captured rather than causing the entire config to fail.

## Section-Fact Extraction

`process/section_extract.py`:

- requires base + enriched config;
- discovers sections from H2 headings in merged templates;
- uses hard-coded `gpt-4.1-mini`, `temperature=0`;
- sends full enriched JSON for every section;
- currently does not interpolate the passed section-template body into the extraction prompt;
- retries rate-limit-like failures up to eight attempts;
- writes `section_title,extracted_facts` CSV rows.

## Template/Markdown Rendering

`process/render_sections.py`:

- merges `templates/base.md` plus optional type template;
- deterministically replaces only title/project/type/generated-at placeholders;
- uses section-template body + extracted facts as LLM input;
- uses `gpt-4.1-mini`, `temperature=0`;
- skips OpenAI for blank-fact sections and emits a fixed `_TBD` marker;
- ensures current front matter with `layout: default`;
- writes raw Markdown under `docs/<project>/<type>/<doc_key>.md`.

## Review/Concision

`process/review_doc.py`:

- reads the whole generated Markdown document;
- uses `AUTODOC_MODEL`, standard workflow value `gpt-4.1`;
- sends the full document in one request;
- requests concision while preserving formatting/headings/order;
- performs no factual or structural post-response validation;
- writes `docs/<project>/<type>/reviewed/<doc_key>.md`.

`reviewed` is an LLM artifact state, not human/factual/publication approval.

## Automatic Orchestration

`autodoc_pipeline.yml` triggers on qualifying config JSON pushes, filters to changed base configs, and runs:

```text
enrich -> extract -> render
```

It serializes automatic runs with concurrency group `autodoc-pipeline`, prevents bot-authored output commits from recursively processing, rebases generated changes onto current `main`, regenerates affected indexes, and commits/pushes outputs when changed.

## Manual Recovery

Manual workflows support bounded reruns for:

- enrichment;
- extraction;
- rendering;
- review;
- index rebuild.

Recovery rule: find the last valid persisted artifact, repair the actual upstream cause, then rerun the smallest necessary downstream stage.

## Publication Boundary

`publish_to_website.yml`:

- is manually dispatchable and currently called by Appsmith;
- requires reviewed Markdown at the expected path;
- validates selected path inputs;
- uses secret name `WEBSITE_PAT` for the website clone/push;
- copies to `projects/<dest_type>/<doc_key>.md`;
- commits/pushes directly if changed;
- does not create a branch/PR, run the documentation validator, merge through governance, or wait for Pages.

This is the documented implementation/governance mismatch.

## Historical Generated Artifacts

AutoDoc retains six Irish Politics `pipeline` artifact families with base/enriched/summary/raw/reviewed provenance. Their generated prose is archived historical evidence, not current Irish Politics implementation authority.

Current dedicated archive/lineage pages in `eirepolitic.github.io` reconcile those artifacts against current `eirepolitic-data-pipeline` source.

## Trust and Security Boundaries

### Appsmith -> GitHub

Appsmith can write configuration/registry state and dispatch workflows. Exported credential exposure proves raw Appsmith exports must be treated as sensitive until sanitized.

### Actions -> source hosts

Enrichment can fetch configured GitHub and generic HTTP sources. Source configuration therefore controls external retrieval and persistence.

### Actions -> OpenAI

Extraction, rendering for fact-bearing sections, and review send document-derived content to OpenAI. `OPENAI_API_KEY` is a secret name only.

### Actions -> repository writes

Automatic/manual workflows commit intermediate/generated artifacts to `autodoc` with declared write permissions where applicable.

### AutoDoc -> documentation repository

Publication crosses repositories through `WEBSITE_PAT` and currently bypasses the documentation PR/validation gate.

## Failure and Recovery Model

- base contract errors must be fixed at base config;
- per-asset enrichment failures are inspected through `resolved_ok`/`resolved_error`;
- failed extraction can leave an older CSV on disk, so existence is not latest-run proof;
- `_TBD` rendering usually indicates missing extracted facts rather than a renderer-only problem;
- review failures leave raw Markdown available for rerun;
- stale `_index.json` is rebuilt from base configs;
- publication should never be used to diagnose upstream generation failures.

## Known Limitations

- exact live external PAT scopes/repository rules/Appsmith membership remain external state;
- generic HTTP fallback broadens the enrichment source-host boundary;
- extraction repeats full enriched JSON per section and currently ignores section body text;
- renderer has no local retry loop;
- review has no factual/structural output validator;
- review workflow stages `docs/` broadly and its commit-message `$DOC_KEY` is step-scoped incorrectly in current source;
- direct publication remains misaligned with current documentation governance;
- historical generated documents can preserve obsolete claims.

## Next Safe Development Action

For future AutoDoc implementation work, start from the component page that owns the relevant stage and verify current `autodoc/main` source. Use the recovery runbook for stale/failed artifacts. Treat model/prompt, credentials/access, source-host policy, and publication architecture as explicit design decisions requiring approval.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)
- [AutoDoc section-fact extraction](/projects/systems/autodoc-section-fact-extraction/)
- [AutoDoc template/Markdown rendering](/projects/systems/autodoc-template-markdown-rendering/)
- [AutoDoc review/concision](/projects/systems/autodoc-review-concision/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)
- [Recover AutoDoc artifacts](/projects/runbooks/recover-autodoc-artifacts/)
- [Historical AutoDoc Irish Politics artifacts](/projects/archive/autodoc-eirepolitic-generated-artifacts/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: completed AutoDoc component documentation, current `autodoc/main`, sanitized Appsmith live-source record, artifact/recovery/archive records, and current publication governance documentation.
- Verified by: High Director
- Verification scope: current system boundary, Appsmith/backend authority, lifecycle, stages, orchestration, recovery, trust/security, publication mismatch, and historical artifact classification.
- Unverified areas: external credential scopes/account membership and service availability.
