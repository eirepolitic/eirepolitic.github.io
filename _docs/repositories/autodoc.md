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

`autodoc` is the source repository for AutoDoc, a configuration-driven documentation-generation system. It persists configuration and intermediate artifacts in Git, resolves configured source assets, extracts section facts through OpenAI, renders Markdown from base/type templates, optionally creates a separate LLM review/concision artifact, and can publish reviewed Markdown into `eirepolitic.github.io`.

GitHub Actions are the operational control plane. Current stage entry points live under `process/`; persistent project state lives under `doc_configs/` and `docs/`.

Current Appsmith implementation is verified from the sanitized user-supplied `2026-08-07` export. That captured live source supersedes the older repository handoff for current Appsmith behavior. Current backend workflows/Python remain authoritative for backend behavior.

## Current Implementation State

Verified current repository capabilities:

- current Appsmith `Submit` and `DocsViewer` integration with GitHub;
- base configuration and project registry under `doc_configs/<project>/`;
- enrichment via `process/enrich_configs.py`;
- section-fact extraction via `process/section_extract.py`;
- Markdown rendering via `process/render_sections.py`;
- review/concision via `process/review_doc.py`;
- registry rebuild via `process/update_index.py`;
- automatic orchestration via `.github/workflows/autodoc_pipeline.yml`;
- manual/recovery workflows for enrichment, extraction, rendering, review, and index rebuild;
- reviewed-document publication via `.github/workflows/publish_to_website.yml`;
- retained base/enriched configs, summary CSVs, generated Markdown, reviewed Markdown, and historical generated artifact families.

## Source of Truth

For current backend behavior:

```text
current workflow/Python source
  > current persisted config/intermediate state
  > generated/reviewed artifacts
  > historical handoff/generated prose
```

For Appsmith behavior:

```text
sanitized 2026-08-07 live export
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
templates/base.md
templates/types/*.md
doc_configs/
docs/
```

## Repository Structure

```text
autodoc/
├── .github/workflows/          Actions orchestration/recovery/publication
├── doc_configs/<project>/      base/enriched configs, summaries, _index.json
├── docs/                       generated/raw and reviewed Markdown
├── process/                    stage implementations
├── templates/                  base + type section templates
└── requirements.txt
```

## Persisted Artifact Lifecycle

```text
doc_configs/<project>/<doc_key>.json
  -> <doc_key>.enriched.json
  -> summaries/<doc_key>.csv
  -> docs/<project>/<type>/<doc_key>.md
  -> docs/<project>/<type>/reviewed/<doc_key>.md
  -> optional website publication copy
```

Separate registry:

```text
doc_configs/<project>/_index.json
```

The index is rebuildable from base configs and Git history; it is not the sole source of project truth.

## Automatic Pipeline

Current automatic stage sequence is:

```text
enrich -> extract -> render
```

It does **not** automatically run review. Review and publication are separate dispatch boundaries.

Automatic runs are serialized through concurrency group `autodoc-pipeline`, exclude bot-authored Actions commits from recursive processing, and write generated state back to `autodoc` when changed.

## Stage Boundaries

### Enrichment

Supports `pasted`, `github_path`, and `github_url`. Recognized GitHub URL forms use the GitHub Contents API; non-recognized `github_url` locators currently fall back to generic HTTP GET. Resolved content and metadata are persisted into enriched JSON.

### Extraction

Uses hard-coded `gpt-4.1-mini` with `temperature=0`. The current prompt sends the section title and full enriched JSON for every H2 section. The section-template body is passed into the function but is not interpolated into the current prompt. Output is a two-column CSV: `section_title,extracted_facts`.

### Rendering

Uses `gpt-4.1-mini` with `temperature=0` for sections that have facts. It sends section title, section-template body, and extracted facts—not enriched JSON. Empty-fact sections emit `_TBD (no extracted facts provided for this section)._`. Current generated front matter uses `layout: default`.

### Review/concision

The standard review workflow sets `AUTODOC_MODEL=gpt-4.1`. The entire generated Markdown document is sent in one OpenAI request and returned output is written directly to the separate `reviewed/` path. `reviewed` is an LLM artifact state, not human/factual approval.

## Appsmith Boundary

The verified Appsmith export contains two pages:

```text
Submit
DocsViewer
```

Current Appsmith can:

- create/load base configs;
- maintain `_index.json` immediately after submit;
- create project `.gitkeep` state;
- read/edit raw/reviewed Markdown;
- dispatch `review_doc.yml`;
- dispatch `publish_to_website.yml`.

The current backend index rebuild remains the deterministic registry reconciliation path.

The supplied export contained two distinct GitHub PAT values. No token values or raw export were committed. Credential rotation/revocation remains a separate security/access action.

## Publication Boundary

`publish_to_website.yml` requires a reviewed source file, clones `eirepolitic.github.io` using secret name `WEBSITE_PAT`, copies into `projects/<dest_type>/<doc_key>.md`, commits if changed, and pushes directly.

This is **CURRENT VERIFIED BEHAVIOR**.

Current documentation governance instead requires branch/PR -> `Validate documentation` -> merge -> matching Pages success. The mismatch is documented; no redesign has been made.

## Manual Recovery

Current recovery workflows support bounded reruns for:

- enrichment;
- extraction;
- rendering;
- review;
- `_index.json` rebuild.

Safe recovery principle: identify the last valid persisted artifact, repair the actual upstream cause, and rerun only the smallest necessary downstream stage.

## Historical Generated Artifacts

`docs/eirepolitic/pipeline/` retains six raw/reviewed AutoDoc artifact pairs. They are historical generated evidence, not current Irish Politics implementation authority. Current `eirepolitic.github.io` archive pages reconcile those legacy documents against current `eirepolitic-data-pipeline` source.

## Security and Access

Secret/token names that may be documented include:

```text
OPENAI_API_KEY
GITHUB_TOKEN
AUTODOC_GITHUB_TOKEN
WEBSITE_PAT
```

Values must never be published.

Trust boundaries include Appsmith -> GitHub, Actions -> configured asset hosts, Actions -> OpenAI, Actions -> `autodoc` writes, and publication -> `eirepolitic.github.io`.

## Known Limitations

- Exact live PAT scopes, repository rules, and Appsmith workspace membership are not proven by checked-in source/export structure.
- `github_url` can fall back to arbitrary reachable HTTP/HTTPS hosts.
- Extraction repeatedly sends full enriched JSON and does not currently use the passed section-template body.
- Rendering has no local retry loop and uses `_TBD` rather than failing for missing facts.
- Review has no post-response factual/structural validator.
- Direct website publication remains misaligned with current documentation PR governance.
- Historical generated artifacts can preserve obsolete implementation descriptions.

## Next Safe Development Action

For future AutoDoc changes, start from the relevant stage/system page and verify current `autodoc/main` source before modifying implementation. Use the artifact-recovery runbook for failed/stale outputs, and treat security/access/model/publication changes as explicit design decisions rather than documentation cleanup.

## Related Documents

- [AutoDoc system architecture](/projects/systems/autodoc/)
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
- Verified against: current AutoDoc component documentation; current `autodoc/main` workflows/Python/config/artifact tree; sanitized Appsmith live-source record; current publication/recovery/archive documentation.
- Verified by: High Director
- Verification scope: repository role, stage lifecycle, Appsmith boundary, automatic/manual operation, security/publication boundaries, recovery, and historical artifact classification.
- Unverified areas: live external credential scopes/account membership and external-service availability.
