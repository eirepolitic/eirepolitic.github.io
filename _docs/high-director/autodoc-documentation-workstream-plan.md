---
title: AutoDoc documentation workstream plan
summary: Persistent continuation plan for the complete AutoDoc documentation workstream, including evidence hierarchy, completed publication gates, current component, security findings, and next safe action.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 104
permalink: /projects/high-director/autodoc-documentation-workstream-plan/
repository: eirepolitic.github.io
system: AutoDoc
tags:
  - high-director
  - autodoc
  - documentation
---

# AutoDoc documentation workstream plan

## Purpose

This is the persistent continuation record for the complete AutoDoc documentation workstream. It must remain synchronized with completed focused PRs, validation runs, merge commits, Pages deployments, authoritative source supplied by the user, security findings, and the next safe documentation action.

The owner-wide documentation target catalogue is read-only scope coordination during routine AutoDoc work.

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

- Generated/reviewed documentation artifact lifecycle and manual recovery workflows.

### P3

- Historical AutoDoc-generated `docs/eirepolitic/pipeline/*` artifacts.

Excluded except for necessary cross-reference: full Irish Politics Analytics implementation, `bb-comp-prices`, `degenerate_investigator`, and Overlord.

## Evidence Hierarchy

For current backend behavior:

```text
current workflows/Python source
  > current config/intermediate contracts
  > current generated/reviewed artifacts
  > historical handoff/generated prose
```

For Appsmith:

```text
current sanitized live export
  > historical repository handoff
```

The user-supplied AutoDoc Appsmith export dated `2026-08-07` is now the authoritative captured current Appsmith source. It is persisted only through the sanitized evidence record `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`; the raw export is not committed because it contained credentials.

Conflicts are retained as drift/history rather than silently overwritten.

## Completed Components

### 1. Repository/system architecture

Published pages:

```text
_docs/repositories/autodoc.md
_docs/systems/autodoc.md
```

Publication gate:

```text
PR #76
Validate documentation run #126: success
merge: dd410f89e5b0259b7224593c3feaf6b136ba1a1c
Pages run #182: success for that merge commit
```

### 2. Appsmith/configuration/index boundary

Published pages/evidence:

```text
_docs/systems/autodoc-appsmith-intake.md
_docs/data/autodoc-configuration-and-project-index.md
_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md
```

Stale PR `#120` was closed without merge after current `main` advanced and the branch became non-clean. The component was rebuilt from current `main` and published through:

```text
PR #121
Validate documentation run #231: success
merge: 382093fb826520c0b99dc08b4b609d7f0c40f4f1
Pages run #225: success for that merge commit
```

Current verified Appsmith drift includes a second `DocsViewer` page, direct dispatch of review/publication workflows, automatic project `.gitkeep` creation, `create` mode value, and current staged backend references rather than the historical single-generator design.

## Active Component

Current branch:

```text
docs/autodoc-pipeline-trust
```

Current target:

```text
P0 AutoDoc creation-pipeline orchestration and trust boundaries
```

Current draft page:

```text
_docs/systems/autodoc-pipeline-orchestration.md
```

Verified key facts:

- `autodoc_pipeline.yml` triggers on pushes touching `doc_configs/**/*.json`.
- It filters the triggering commit to base configs, excluding `_index.json` and `*.enriched.json`.
- Automatic sequence is **enrich -> extract -> render**.
- Automatic sequence does **not** call `review_doc.py`.
- Automatic concurrency group is `autodoc-pipeline`, with `cancel-in-progress: false`.
- Bot-authored GitHub Actions commits are excluded from the automatic job.
- Current automatic/manual stage workflows declare `contents: write` where they commit outputs.
- Automatic processing uses `OPENAI_API_KEY` and `AUTODOC_GITHUB_TOKEN || GITHUB_TOKEN` by name only.
- Generated changes are stashed, rebased onto current `main`, restored, followed by authoritative `_index.json` regeneration for affected projects.
- Review is a separate `workflow_dispatch` boundary and currently sets `AUTODOC_MODEL=gpt-4.1`.

## Security Findings

The supplied Appsmith export contained two distinct GitHub PAT values repeated in exported datasource/action definitions.

Documentation handling:

- values were not reproduced;
- values were not committed;
- raw export was not committed;
- only the existence/location/role of the credential exposure was persisted.

Security action still required outside this documentation workstream:

```text
rotate/revoke both exposed GitHub PATs and replace the active Appsmith credential configuration
```

This is a security/access-control change and requires explicit user approval/handling. Do not perform credential changes merely because the documentation recorded the finding.

## Publication Governance

Every focused AutoDoc documentation component follows:

1. create/sync a focused `docs/autodoc-*` branch from current `main`;
2. open PR;
3. confirm `Validate documentation` succeeds;
4. merge;
5. identify merge commit;
6. confirm matching GitHub Pages deployment succeeds for that exact commit;
7. only then begin the next major component.

If a branch becomes non-clean because `main` advanced, do not force the merge. Rebuild/synchronize from current `main` and close the stale PR if necessary.

## Publication Architecture Mismatch

Keep these labels distinct in all documentation:

### CURRENT VERIFIED BEHAVIOR

Current `autodoc/.github/workflows/publish_to_website.yml` clones `eirepolitic.github.io` using `WEBSITE_PAT`, copies a reviewed Markdown file, commits it, and pushes directly.

### CURRENT DOCUMENTATION GOVERNANCE

Documentation changes require branch/PR -> validation -> merge -> matching Pages success.

Do not redesign the workflow or Appsmith dispatch path without explicit architecture/security approval.

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
11. Final cross-page consistency and current-`main` synchronization.

## Failure/Recovery Rules

- Backend/handoff conflict: current executable backend wins; retain handoff as drift.
- Appsmith/live-handoff conflict: supplied live export wins for current Appsmith; retain historical handoff.
- Stale `_index.json`: rebuild from base configs through `process/update_index.py`.
- Failed documentation validator: correct reported documentation errors before merge.
- Failed Pages deployment: do not start the next major component until the matching deployment issue is resolved.
- Branch conflict/non-clean merge: recreate/sync focused branch from current `main`; do not force unrelated changes.
- Secret found in supplied source: sanitize/persist only safe evidence; never commit the secret-bearing source.

## Outstanding Work

- Complete and publish orchestration/trust page.
- Document publication boundary with exact `publish_to_website.yml` trigger/inputs/path checks/permissions/token boundary/overwrite behavior/direct push and governance mismatch.
- Complete P1 stage pages with exact models, prompts/configuration, source modes, intermediate CSV contract, templates, retry/error behavior, and outputs.
- Complete P2 artifact lifecycle/manual recovery runbook.
- Complete P3 historical artifact classification.
- Perform final main-sync/link/evidence consistency review.

## Next Safe Development Action

Open and validate the focused orchestration/trust PR. Merge only after `Validate documentation` succeeds, then confirm matching Pages success. After that, create a fresh branch from `main` for the reviewed-document website-publication boundary.

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
- Verified against: current `eirepolitic.github.io` `main`; PR/validation/merge/Pages records above; current `autodoc` workflows/Python/configs; user-supplied Appsmith export via sanitized evidence record.
- Unverified external state: exact PAT scopes, current Appsmith workspace membership, repository-rule enforcement, external service availability.
