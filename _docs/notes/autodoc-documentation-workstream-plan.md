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

Persistent continuation plan for the complete AutoDoc documentation workstream. It tracks evidence authority, sanitized source, focused PRs, validation/merge/Pages gates, security findings, current component, and next safe action.

The owner-wide target catalogue remains read-only scope coordination during routine AutoDoc work.

## Assigned Scope

- **P0:** repository/system architecture; Appsmith intake/configuration; config schema/project index; pipeline orchestration/trust; reviewed-document website publication.
- **P1:** enrichment/source resolution; LLM section-fact extraction; template/Markdown rendering; LLM review/concision.
- **P2:** generated/reviewed artifact lifecycle and manual recovery.
- **P3:** historical `docs/eirepolitic/pipeline/*` artifacts.

Full Irish Politics Analytics, `bb-comp-prices`, `degenerate_investigator`, and Overlord remain outside this workstream except for required cross-references.

## Evidence Hierarchy

For backend claims:

```text
current workflow/Python source
  > current config/intermediate contracts
  > generated/reviewed outputs
  > historical handoff/generated prose
```

For Appsmith claims:

```text
current sanitized live export
  > historical repository handoff
```

The user-supplied `2026-08-07` Appsmith export is current captured-state authority for Appsmith. The raw export is not committed because it contained credentials. Sanitized evidence is persisted at `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`.

Conflicting older evidence is retained as drift/history rather than silently overwritten.

## Completed Components

### Repository/system architecture

```text
Docs:
  _docs/repositories/autodoc.md
  _docs/systems/autodoc.md
PR #76
Validate documentation #126: success
Merge: dd410f89e5b0259b7224593c3feaf6b136ba1a1c
Pages #182: success for merge commit
```

### Appsmith/configuration/index boundary

```text
Docs:
  _docs/systems/autodoc-appsmith-intake.md
  _docs/data/autodoc-configuration-and-project-index.md
  _docs/high-director/autodoc-appsmith-live-source-2026-08-07.md
Stale PR #120: closed without merge after branch became non-clean
Replacement PR #121
Validate documentation #231: success
Merge: 382093fb826520c0b99dc08b4b609d7f0c40f4f1
Pages #225: success for merge commit
```

Verified live Appsmith drift includes `DocsViewer`, direct review/publication workflow dispatch, `.gitkeep` project creation, create value `create`, and current staged backend behavior replacing historical generator descriptions.

### Automatic pipeline orchestration/trust boundaries

```text
Doc:
  _docs/systems/autodoc-pipeline-orchestration.md
PR #123
Validate documentation #240: success
Merge: 39b3729389d03de9ea3f09e01a010245c2838e26
Pages #228: success for merge commit
```

Verified automatic sequence is `enrich -> extract -> render`; review remains separate. The component documents config filtering, `contents: write`, concurrency, bot recursion guard, secret names, rebase/stash/index regeneration, manual recovery workflows, and trust boundaries.

## Active Component

Branch:

```text
docs/autodoc-publication-boundary
```

Target:

```text
P0 reviewed-document website publication boundary
```

Draft page:

```text
_docs/systems/autodoc-publication-boundary.md
```

Current verified publication facts:

- workflow: `.github/workflows/publish_to_website.yml`, name `Publish reviewed doc to website`;
- trigger: `workflow_dispatch`;
- required inputs: `project`, `type`, `doc_key`, `dest_type`; optional `overwrite`, default `"true"`;
- source workflow permissions: `contents: read`;
- reviewed source path: `docs/<project>/<type>/reviewed/<doc_key>.md`;
- rejects empty values, values containing `..`, or leading `/`; additionally `dest_type` cannot contain `/`;
- requires source reviewed file and pre-existing website destination directory;
- cross-repository write credential name: `WEBSITE_PAT` only;
- destination: `projects/<dest_type>/<doc_key>.md`;
- overwrite=false blocks an existing destination; current Appsmith dispatch uses overwrite=true;
- identical content produces no commit;
- changed content is committed and directly `git push`ed in the cloned website repository;
- workflow does not create a branch/PR, run documentation validation, merge through governance, or wait for matching Pages success.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values repeated in datasource/action definitions.

Completed documentation response:

- values not reproduced;
- values not committed;
- raw export not committed;
- sanitized implementation/security evidence persisted.

Outstanding security action requiring explicit user handling/approval:

```text
rotate/revoke both exposed GitHub PATs and replace the active Appsmith credential configuration
```

Do not perform credential rotation/storage/access changes automatically.

## Publication Governance

For every focused component:

1. branch from current `main` using `docs/autodoc-*`;
2. open focused PR;
3. confirm `Validate documentation` succeeds on latest head;
4. merge;
5. identify merge commit;
6. confirm matching Pages build/deploy succeeds for that exact commit;
7. only then begin the next major component.

If parallel work makes a branch non-clean, do not force the merge; rebuild/synchronize from current `main`.

## Publication Architecture Mismatch

### CURRENT VERIFIED BEHAVIOR

`publish_to_website.yml` clones `eirepolitic.github.io` using `WEBSITE_PAT`, copies reviewed Markdown under `projects/<dest_type>/`, commits if changed, and pushes directly.

### CURRENT DOCUMENTATION GOVERNANCE

Material documentation changes require branch/PR -> `Validate documentation` -> merge -> matching Pages build/deploy success -> live verification.

The workflow does not currently implement that governance. Document the mismatch; do not redesign it without explicit architecture/security approval.

## Work Sequence

1. Repository/system architecture — **complete**.
2. Appsmith/config/index — **complete**.
3. Automatic pipeline orchestration/trust — **complete**.
4. Reviewed-document website publication — **active**.
5. Asset enrichment/source resolution.
6. LLM section-fact extraction.
7. Template/Markdown rendering.
8. LLM review/concision.
9. Generated/reviewed lifecycle and manual recovery.
10. Historical `docs/eirepolitic/pipeline/*` artifact classification.
11. Final current-`main` synchronization and cross-page consistency review.

## Failure and Recovery Rules

- Current executable backend wins over historical backend prose; retain drift evidence.
- Current sanitized live Appsmith export wins over historical Appsmith handoff.
- Stale registry: rebuild `_index.json` from base configs using `process/update_index.py`.
- Validation failure: fix the reported documentation issue; never merge around the gate.
- Pages failure: do not begin the next major component.
- Non-clean branch: sync/rebuild from current `main`, do not force unrelated changes.
- Secret-bearing supplied source: persist only sanitized evidence.

## Outstanding Work

- Validate, merge, and deploy the publication-boundary component.
- Complete P1 stage documentation with exact resolver modes, CSV contracts, templates, OpenAI models/configuration, retries/error behavior, and artifact paths.
- Complete P2 lifecycle/manual recovery runbook.
- Complete P3 historical artifact classification.
- Perform final current-`main` and cross-page/link/evidence consistency review.

## Next Safe Development Action

Open the focused publication-boundary PR, confirm `Validate documentation`, merge, and confirm matching Pages success. Then start asset enrichment/source resolution on a fresh branch from updated `main`.

Do not rotate credentials, change PAT scopes/storage, alter workflow permissions, change models, modify publication architecture, or change Appsmith access control without explicit approval.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [Sanitized Appsmith live source](/projects/high-director/autodoc-appsmith-live-source-2026-08-07/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Verified against: current `eirepolitic.github.io` `main`; gate records above; current `autodoc` workflows/Python/configs; sanitized Appsmith evidence; current documentation publishing runbooks.
- Unverified external state: exact PAT scopes, current Appsmith workspace membership, repository-rule enforcement, and external-service availability.
