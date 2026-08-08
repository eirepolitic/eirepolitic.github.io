---
title: AutoDoc pipeline orchestration and trust boundaries
summary: Current verified GitHub Actions orchestration for AutoDoc, including automatic config-change processing, manual recovery workflows, repository/OpenAI/source trust boundaries, and review separation.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 33
permalink: /projects/systems/autodoc-pipeline-orchestration/
tags:
  - autodoc
  - github-actions
  - pipeline
  - security
  - openai
---

# AutoDoc pipeline orchestration and trust boundaries

## Summary

AutoDoc's current automatic backend is a GitHub Actions pipeline triggered by pushes that touch JSON below `doc_configs/`. It identifies base-config JSON files changed by the triggering commit, then runs enrichment, section-fact extraction, and Markdown rendering for each changed document. It subsequently rebases generated changes onto current `main`, rebuilds affected project indexes, commits generated outputs, and pushes them to the `autodoc` repository.

The automatic workflow **does not run the review/concision stage**. Reviewed Markdown is produced through the separate `Review Documentation` workflow, currently dispatched manually or by the Appsmith `DocsViewer` page. Website publication is another separate workflow boundary.

This separation is important for both artifact lifecycle and trust: a generated Markdown file is not automatically a reviewed document merely because the automatic pipeline completed.

## Source of Truth

Current workflow source:

- `.github/workflows/autodoc_pipeline.yml`
- `.github/workflows/enrich_configs.yml`
- `.github/workflows/section_extract.yml`
- `.github/workflows/render_docs.yml`
- `.github/workflows/review_doc.yml`
- `.github/workflows/index_rebuilder.yaml`

Current stage source:

- `process/enrich_configs.py`
- `process/section_extract.py`
- `process/render_sections.py`
- `process/review_doc.py`
- `process/update_index.py`

The website-publication workflow is documented as a separate boundary because it crosses into `eirepolitic.github.io` using a separate credential.

## Automatic Workflow

File:

```text
.github/workflows/autodoc_pipeline.yml
```

Workflow name:

```text
AutoDoc Pipeline (Enrich → Extract → Render)
```

### Trigger

```yaml
on:
  push:
    paths:
      - "doc_configs/**/*.json"
```

Any qualifying JSON path can trigger the workflow, including derived JSON changes at the GitHub trigger level. The workflow itself then filters the triggering commit's file list so only base-config JSON paths are processed.

### Permissions

```yaml
permissions:
  contents: write
```

The workflow can write repository contents because it commits generated outputs and index files back to `autodoc`.

### Concurrency

```text
group: autodoc-pipeline
cancel-in-progress: false
```

Automatic runs are serialized into one AutoDoc pipeline concurrency group; a new run does not cancel an existing run.

### Bot recursion guard

The job runs only when:

```text
github.actor != 'github-actions[bot]'
```

Generated commits authored/pushed by GitHub Actions therefore do not recursively run the same automatic pipeline path.

## Automatic Changed-Config Detection

The workflow inspects only the triggering commit:

```text
git show --name-only --pretty='' <github.sha>
```

It retains paths matching:

```text
doc_configs/.+\.json
```

then excludes:

```text
doc_configs/<project>/_index.json
*.enriched.json
```

The remaining paths are treated as base config changes. For each path, the project is taken from path component 2 and `doc_key` from the filename without `.json`.

### Consequences

- `_index.json` commits do not become processing targets.
- Enriched-config commits do not become processing targets.
- The pipeline processes only base configs included in the triggering commit's file list, not every config in the repository.
- Multiple base config changes in one commit are processed sequentially by the shell loop in one Actions job.

## Automatic Stage Sequence

For every changed base config:

```text
python process/enrich_configs.py --project <project> --doc-key <doc_key> --overwrite
PROJECT=<project> DOC_KEY=<doc_key> python process/section_extract.py
PROJECT=<project> DOC_KEY=<doc_key> python process/render_sections.py
```

The automatic workflow does not call `process/review_doc.py`.

### Stage 1: enrichment

Consumes:

```text
doc_configs/<project>/<doc_key>.json
```

Produces/updates:

```text
doc_configs/<project>/<doc_key>.enriched.json
```

`--overwrite` means the automatic path replaces/recreates the enriched result for the changed base config rather than preserving an existing enriched artifact unchanged.

### Stage 2: section extraction

Consumes current base/enriched configuration and sends constructed source/context material to OpenAI through `process/section_extract.py`.

Produces:

```text
doc_configs/<project>/summaries/<doc_key>.csv
```

### Stage 3: render

Consumes the project config, enriched context/summary contract, and templates through `process/render_sections.py`.

Produces generated Markdown under `docs/` according to project/type/doc-key path conventions.

## Automatic Runtime Environment

Runner:

```text
ubuntu-latest
```

Python:

```text
3.11
```

Dependency installation:

```text
python -m pip install --upgrade pip
pip install -r requirements.txt || true
pip install openai requests
```

The automatic workflow deliberately tolerates failure of `pip install -r requirements.txt` because of `|| true`, then explicitly installs `openai` and `requests`. This means a requirements-file installation failure does not itself stop the run; a later stage can still fail if another required dependency is absent.

## Automatic Environment and Secret Names

The processing step sets:

```text
OPENAI_API_KEY <- secrets.OPENAI_API_KEY
GITHUB_TOKEN <- secrets.AUTODOC_GITHUB_TOKEN || secrets.GITHUB_TOKEN
GITHUB_REPO = eirepolitic/autodoc
GITHUB_REF = main
```

Only names and roles are documented. Secret values must never be published.

The checkout step separately uses `secrets.GITHUB_TOKEN` and fetches full history with `fetch-depth: 0`.

## Rebase and Generated-State Handling

After all changed documents are processed, the workflow:

1. configures commit identity as `github-actions[bot]`;
2. stages all local generated changes;
3. stashes generated changes including untracked files;
4. fetches current `origin/main`;
5. rebases/pulls onto current `main`;
6. restores the generated stash.

The stash restore command is:

```text
git stash pop || true
```

Therefore a non-zero stash-pop result does not itself stop the workflow at that line. Subsequent index generation/staging/commit steps operate on the resulting worktree state. This is a verified control-flow fact; this documentation does not infer that every stash conflict is silently safe.

The preceding `git pull --rebase origin main` is not suppressed; a failed rebase stops the shell step because `set -euo pipefail` is enabled.

## Authoritative Index Regeneration

After rebase/restore, the workflow determines the distinct affected project folders and runs:

```text
python process/update_index.py --project <project>
```

for each project.

This happens after the generated changes are restored and after rebase onto latest `main`. The regenerated `_index.json` is the backend reconciliation state for the affected project.

This is stronger backend authority than an immediately Appsmith-written registry entry when the two differ.

## Automatic Commit/Push Boundary

The workflow stages generated artifacts from:

```text
doc_configs/**.enriched.json
doc_configs/**/summaries/*.csv
doc_configs/**/_index.json
docs/**
```

If no staged differences exist, it exits successfully with `No changes to commit.`

Otherwise it commits:

```text
AutoDoc pipeline outputs
```

and runs:

```text
git push
```

This is a direct repository-write boundary to `autodoc` `main`, governed by workflow/token permissions and repository rules external to this file.

## Review Is a Separate Workflow

File:

```text
.github/workflows/review_doc.yml
```

Workflow name:

```text
Review Documentation
```

Trigger:

```text
workflow_dispatch
```

Required inputs:

```text
project
type
doc_key
overwrite
```

Permissions:

```text
contents: write
```

Runtime model setting in the workflow:

```text
AUTODOC_MODEL = gpt-4.1
```

The review workflow supplies `OPENAI_API_KEY`, calls:

```text
python process/review_doc.py
```

then stages `docs/`, commits reviewed output when changed, and pushes.

Because review is separate from the automatic path, operators and Appsmith must not treat generated Markdown existence as reviewed-state proof.

## Manual Recovery Workflows

### Enrichment

File/name:

```text
.github/workflows/enrich_configs.yml
Enrich AutoDoc Configs (Manual)
```

Trigger: `workflow_dispatch`.

Inputs:

```text
project      optional; blank = all
doc_key      optional; blank = all in project
overwrite    required, default false
only_missing required, default false
```

Concurrency:

```text
enrich-autodoc-configs
cancel-in-progress: false
```

Permissions: `contents: write`.

Token/environment names include `AUTODOC_GITHUB_TOKEN` fallback to `GITHUB_TOKEN`, `GITHUB_REPO`, and `GITHUB_REF`.

The workflow commits only enriched JSON outputs when changed.

### Extraction

File/name:

```text
.github/workflows/section_extract.yml
Extract Section Facts
```

Trigger: `workflow_dispatch` with required `project` and `doc_key`.

Concurrency:

```text
extract-section-facts
cancel-in-progress: false
```

Permissions: `contents: write`.

Uses `OPENAI_API_KEY`, runs `process/section_extract.py`, and commits the specific summary CSV.

### Render

File/name:

```text
.github/workflows/render_docs.yml
Render Docs from Section Summaries
```

Trigger: `workflow_dispatch` with required `project` and `doc_key`.

Concurrency:

```text
render-docs
cancel-in-progress: false
```

Permissions: `contents: write`.

The workflow also exports `OPENAI_API_KEY` even though the exact current use of that environment variable is determined by `process/render_sections.py`; the workflow then commits changes under `docs/`.

### Index rebuild

File/name:

```text
.github/workflows/index_rebuilder.yaml
Rebuild _index.json (Manual)
```

Trigger: `workflow_dispatch` with required `project`.

Concurrency:

```text
rebuild-index
cancel-in-progress: false
```

Permissions: `contents: write`.

Runs:

```text
python process/update_index.py --project <project>
```

then stages only that project's `_index.json`, commits if changed, rebases onto current `main`, and pushes.

### Review

`Review Documentation` is also a manual/recovery boundary. Current Appsmith `DocsViewer` dispatches it directly with `overwrite: "true"`.

## Trust Boundaries

### 1. Appsmith/config producer -> `autodoc` repository

A base-config write can trigger the automatic pipeline. Configuration therefore controls project/type/context and asset references that downstream stages will process.

This is both an input-validation and repository-write trust boundary.

### 2. `autodoc` config -> external source resolvers

Enrichment reads configured `pasted`, `github_path`, and `github_url` sources. The Actions runner can therefore make source-resolution requests based on repository configuration.

Exact resolver/host rules are documented in the enrichment stage page.

### 3. Actions runner -> GitHub repository write

All current stage/recovery workflows documented here declare `contents: write`. They commit generated/intermediate state back to the repository.

Workflow permission declarations prove requested workflow permissions; they do not prove external PAT scopes or repository-rule outcomes.

### 4. Actions runner -> OpenAI

Extraction and review cross the OpenAI trust boundary using `OPENAI_API_KEY`. Project/source/document content can be included in constructed prompts according to current Python code.

Do not place secrets/private user data in AutoDoc source/config context merely because it is technically readable by the runner.

### 5. Generated -> reviewed artifact boundary

Automatic completion yields generated Markdown, not reviewed Markdown. Review is a separately dispatched OpenAI-backed stage with its own write boundary.

### 6. Reviewed -> website publication boundary

Publication is not part of this automatic workflow and is documented separately. It crosses into `eirepolitic.github.io` using `WEBSITE_PAT` and currently has a governance mismatch with the newer PR/validation/merge/Pages discipline.

## Failure Behavior

### No base configs survive the change filter

All processing/rebase/index/commit steps with the changed-files condition are skipped; the run can complete without generated output.

### Enrichment/extraction/render command fails

The processing shell uses `set -euo pipefail`. An unsuppressed stage command failure stops the processing step and prevents later workflow steps from completing normally.

### Requirements installation fails

`pip install -r requirements.txt` failure is suppressed in the automatic workflow. The run proceeds to explicit `openai requests` installation and can fail later if another missing dependency is required.

### Rebase fails

`git pull --rebase origin main` is unsuppressed and stops the generated-state step on failure.

### Stash restore reports failure/conflict

`git stash pop || true` suppresses the non-zero exit at that command. Inspect worktree/index state and downstream run results before treating outputs as clean.

### Nothing changed after generation

Commit step exits successfully without creating a new commit.

### Manual stage rerun writes output

Manual workflows commit their stage outputs directly to `autodoc`. Confirm the upstream artifact is valid before rerunning a downstream stage; do not use a later-stage rerun to hide a bad base/enriched/summary contract.

## Recovery Principles

1. Identify the last valid persisted artifact.
2. Fix the actual upstream configuration/source/API issue.
3. Use the smallest applicable manual workflow.
4. Verify the resulting artifact before continuing downstream.
5. Rebuild `_index.json` from base configs if registry state is suspect.
6. Do not label generated Markdown as reviewed without a successful review-stage result.
7. Do not publish merely to test whether an earlier stage is valid.

## Security Notes

Secret names that may be documented:

```text
OPENAI_API_KEY
GITHUB_TOKEN
AUTODOC_GITHUB_TOKEN
```

Values must never be published.

The supplied current Appsmith export also contained two exposed GitHub PAT values. That credential finding is documented separately and does not change the workflow trust model described here.

## Known Limitations

- Repository source does not prove exact live PAT/token scopes or branch-protection behavior.
- The automatic workflow's name and implementation end at render; review is separate.
- Workflow concurrency groups are stage-specific; manual workflows are not globally serialized with the automatic pipeline by a single shared group.
- Runtime OpenAI/source-host outcomes are external dependencies and can fail independently of repository correctness.

## Next Safe Development Action

Publish this orchestration/trust component through documentation validation, merge, and matching Pages deployment. Then document the reviewed-document website-publication boundary as a separate focused component, preserving current direct-push behavior versus current documentation governance without redesigning it.

## Related Documents

- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc` `main` versions of `autodoc_pipeline.yml`, `enrich_configs.yml`, `section_extract.yml`, `render_docs.yml`, `review_doc.yml`, and `index_rebuilder.yaml`; current stage Python files for stage-boundary cross-checks; current Appsmith documentation for dispatch boundary.
- Verified by: High Director
- Verification scope: triggers, permissions, concurrency, config filtering, automatic stage order, generated-state rebase/index/commit handling, manual recovery workflows, review separation, trust boundaries, and failure behavior.
- Not verified: live external token scopes, repository-rule enforcement, or runtime external-service availability.
