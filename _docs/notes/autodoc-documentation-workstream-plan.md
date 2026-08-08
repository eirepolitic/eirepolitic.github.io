---
title: AutoDoc documentation workstream plan
summary: Persistent coordination plan for documenting AutoDoc from verified repository evidence through focused validated pull requests and matching Pages deployments.
section: notes
doc_type: note
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 104
permalink: /projects/high-director/autodoc-documentation-workstream-plan/
repository: eirepolitic.github.io
tags:
  - autodoc
  - documentation
  - workstream
---

# AutoDoc documentation workstream plan

## Purpose

This page is the persistent continuation plan for the complete AutoDoc documentation workstream. It coordinates evidence review, source sanitization, focused PRs, validation, merge, Pages deployment checks, and the next safe documentation action so another capable agent can continue without conversation history.

The owner-wide target catalogue remains read-only scope coordination during routine AutoDoc work.

## Assigned Scope

### P0

- `autodoc` repository and system architecture.
- AutoDoc Appsmith intake/configuration application.
- AutoDoc configuration schema and project-index registry.
- AutoDoc creation-pipeline orchestration and trust boundaries.
- AutoDoc reviewed-document website publication boundary.

### P1

- Asset enrichment/source resolution.
- LLM section-fact extraction.
- Template and Markdown rendering.
- LLM review/concision.

### P2

- Generated/reviewed artifact lifecycle and manual recovery workflows.

### P3

- Historical AutoDoc-generated `docs/eirepolitic/pipeline/*` artifacts.

Excluded except where cross-reference is required: the full Irish Politics Analytics implementation, `bb-comp-prices`, `degenerate_investigator`, and Overlord.

## Evidence Hierarchy

For current backend behavior:

```text
current workflow/Python source
  > current configuration/intermediate contracts
  > generated/reviewed outputs
  > historical handoff/generated prose
```

For Appsmith:

```text
current sanitized live export
  > historical repository handoff
```

The user-supplied AutoDoc Appsmith export dated `2026-08-07` is authoritative captured current Appsmith evidence. The raw export is not committed because it contained GitHub PAT values; sanitized evidence is persisted in `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`.

Conflicts must be retained as historical/drift evidence rather than silently overwritten.

## Completed Components

### Repository/system architecture

Published pages:

```text
_docs/repositories/autodoc.md
_docs/systems/autodoc.md
```

Gate record:

```text
PR #76
Validate documentation run #126: success
merge commit: dd410f89e5b0259b7224593c3feaf6b136ba1a1c
Pages run #182: success for that merge commit
```

### Appsmith/configuration/index boundary

Published pages/evidence:

```text
_docs/systems/autodoc-appsmith-intake.md
_docs/data/autodoc-configuration-and-project-index.md
_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md
```

The first branch became non-clean after `main` advanced; stale PR `#120` was closed without merge and rebuilt from current `main`.

Gate record:

```text
PR #121
Validate documentation run #231: success
merge commit: 382093fb826520c0b99dc08b4b609d7f0c40f4f1
Pages run #225: success for that merge commit
```

Current verified Appsmith drift includes:

- `Submit` plus `DocsViewer` rather than intake-only UI;
- direct dispatch of `review_doc.yml` and `publish_to_website.yml`;
- project `.gitkeep` creation through `GitHub_EnsureProject`;
- create-mode value `create` instead of historical `new`;
- current staged enrich/extract/render/review backend rather than the historical single-generator description.

## Active Component

Branch:

```text
docs/autodoc-pipeline-trust
```

Target:

```text
P0 AutoDoc creation-pipeline orchestration and trust boundaries
```

Draft page:

```text
_docs/systems/autodoc-pipeline-orchestration.md
```

Verified current orchestration facts:

- `autodoc_pipeline.yml` triggers on pushes touching `doc_configs/**/*.json`.
- It filters the triggering commit to base configs, excluding `_index.json` and `*.enriched.json`.
- Automatic stage sequence is `enrich -> extract -> render`.
- The automatic workflow does not call `review_doc.py`.
- Review is a separate `workflow_dispatch` boundary.
- Automatic concurrency group is `autodoc-pipeline`, `cancel-in-progress: false`.
- GitHub Actions bot commits are excluded from the automatic job.
- Automatic/manual stage workflows that commit outputs declare `contents: write`.
- Automatic processing uses secret names `OPENAI_API_KEY` and `AUTODOC_GITHUB_TOKEN` with `GITHUB_TOKEN` fallback; values are never documented.
- Generated changes are stashed, rebased onto current `main`, restored, then affected project indexes are regenerated authoritatively before commit/push.
- Current review workflow sets `AUTODOC_MODEL=gpt-4.1`.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values repeated in exported datasource/action definitions.

Documentation handling is complete:

- values were not reproduced;
- values were not committed;
- raw export was not committed;
- only sanitized implementation/security evidence was persisted.

Security action remains outside this documentation workstream:

```text
rotate/revoke both exposed GitHub PATs and replace the active Appsmith credential configuration
```

Credential rotation/storage changes are security/access-control decisions and are not performed automatically.

## Publication Governance

Every focused component follows:

1. branch from current `main` using `docs/autodoc-*`;
2. open PR;
3. confirm `Validate documentation` succeeds;
4. merge;
5. identify the merge commit;
6. confirm matching GitHub Pages success for that exact commit;
7. only then begin the next major component.

If a branch becomes non-clean as parallel work advances `main`, do not force the merge. Rebuild/synchronize from current `main` and close the stale PR when appropriate.

## Publication Architecture Mismatch

Keep these labels distinct:

### CURRENT VERIFIED BEHAVIOR

Current `autodoc/.github/workflows/publish_to_website.yml` clones `eirepolitic.github.io` using `WEBSITE_PAT`, copies a reviewed Markdown file, commits it, and pushes directly.

### CURRENT DOCUMENTATION GOVERNANCE

Documentation changes require branch/PR -> `Validate documentation` -> merge -> matching Pages success.

Do not redesign the Appsmith/workflow publication path without explicit architecture/security approval.

## Work Sequence

1. Repository/system architecture — **complete**.
2. Appsmith/config/index — **complete**.
3. Automatic pipeline orchestration/trust boundaries — **active**.
4. Reviewed-document website-publication boundary — next P0 component.
5. Asset enrichment/source resolution.
6. LLM section-fact extraction.
7. Template/Markdown rendering.
8. LLM review/concision.
9. Generated/reviewed lifecycle and manual recovery.
10. Historical `docs/eirepolitic/pipeline/*` artifact classification.
11. Final cross-page/current-`main` consistency review.

## Failure and Recovery Rules

- Backend/handoff conflict: current executable backend wins; retain handoff as drift.
- Appsmith/live-handoff conflict: supplied live export wins for current Appsmith; retain historical handoff.
- Stale `_index.json`: regenerate from base configs through `process/update_index.py`.
- Validation failure: fix reported documentation errors; do not merge around the gate.
- Pages failure: do not begin the next major component until the matching deployment is healthy.
- Branch conflict/non-clean state: rebuild/sync from current `main`; do not force unrelated changes.
- Secret found in supplied source: sanitize and persist only safe evidence; never commit secret-bearing source.

## Outstanding Work

- Complete/publish pipeline orchestration and trust-boundary documentation.
- Document reviewed-document website publication, including exact workflow trigger/inputs, source/destination path checks, credential boundary, overwrite behavior, git push behavior, failure handling, and governance mismatch.
- Complete P1 stage pages with exact source modes, CSV contract, templates, OpenAI models/configuration, retry/error behavior, and artifact paths.
- Complete P2 lifecycle/manual recovery runbook.
- Complete P3 historical artifact classification.
- Perform final current-`main` synchronization and cross-page/link/evidence consistency review.

## Next Safe Development Action

Fix and rerun validation for the orchestration/trust PR. Merge only after `Validate documentation` succeeds, then confirm matching Pages success. After that, create a fresh branch from `main` for the reviewed-document website-publication boundary.

Do not rotate credentials, change PAT scopes/storage, alter workflow permissions, change OpenAI models, modify publication architecture, or change Appsmith access control without explicit approval.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [Sanitized Appsmith live source](/projects/high-director/autodoc-appsmith-live-source-2026-08-07/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Verified against: current `eirepolitic.github.io` `main`; PR/validation/merge/Pages records above; current `autodoc` workflows/Python/configs; supplied Appsmith export via the sanitized evidence record.
- Unverified external state: exact PAT scopes, current Appsmith workspace membership, repository-rule enforcement, and external-service availability.
