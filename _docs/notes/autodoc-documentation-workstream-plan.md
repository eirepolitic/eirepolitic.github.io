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

Persistent continuation plan for the complete AutoDoc documentation workstream. It records evidence authority, focused PR gates, sanitized source, security findings, current component status, and the next safe action.

The owner-wide target catalogue remains read-only scope coordination during routine AutoDoc work.

## Assigned Scope

- **P0:** repository/system architecture; Appsmith intake/configuration; config schema/project index; pipeline orchestration/trust; reviewed-document website publication.
- **P1:** enrichment/source resolution; LLM section-fact extraction; template/Markdown rendering; LLM review/concision.
- **P2:** generated/reviewed artifact lifecycle and manual recovery.
- **P3:** historical `docs/eirepolitic/pipeline/*` artifacts.

## Evidence Hierarchy

Backend: current workflows/Python > current config/intermediate contracts > generated/reviewed outputs > historical prose.

Appsmith: current sanitized live export > historical repository handoff.

The user-supplied `2026-08-07` Appsmith export is current captured-state authority. The raw export is not committed because it contained credentials; sanitized evidence is persisted at `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`.

## Completed Components

### Repository/system architecture

```text
_docs/repositories/autodoc.md
_docs/systems/autodoc.md
PR #76
Validate documentation #126: success
Merge: dd410f89e5b0259b7224593c3feaf6b136ba1a1c
Pages #182: success
```

### Appsmith/configuration/index boundary

```text
_docs/systems/autodoc-appsmith-intake.md
_docs/data/autodoc-configuration-and-project-index.md
_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md
Stale PR #120: closed without merge
Replacement PR #121
Validate documentation #231: success
Merge: 382093fb826520c0b99dc08b4b609d7f0c40f4f1
Pages #225: success
```

### Automatic pipeline orchestration/trust boundaries

```text
_docs/systems/autodoc-pipeline-orchestration.md
PR #123
Validate documentation #240: success
Merge: 39b3729389d03de9ea3f09e01a010245c2838e26
Pages #228: success
```

## Publication Boundary: Gate Recovery Active

Documentation page is merged:

```text
_docs/systems/autodoc-publication-boundary.md
PR #125
Validate documentation #241: success
Merge: 9f30e9b46b62174ddfc853543f75589a7657fa00
Pages #229: cancelled before checkout/build/deploy completed
```

Pages run #229 was cancelled during the Pages container-pull step while parallel site activity was occurring. The publication component is **not** considered complete because the required matching Pages deployment did not succeed.

Recovery branch:

```text
docs/autodoc-publication-gate-recovery
```

This focused follow-up updates only the persistent workstream state so a new validated merge containing the already-merged publication documentation can receive a complete matching Pages deployment. P1 work remains blocked until that gate succeeds.

## Verified Publication Boundary

Current `autodoc/.github/workflows/publish_to_website.yml`:

- is `workflow_dispatch`;
- requires `project`, `type`, `doc_key`, `dest_type`; `overwrite` defaults to `"true"`;
- declares `contents: read` in `autodoc`;
- requires `docs/<project>/<type>/reviewed/<doc_key>.md`;
- uses credential name `WEBSITE_PAT` for the cross-repository clone/push;
- requires existing destination directory `projects/<dest_type>`;
- writes `projects/<dest_type>/<doc_key>.md`;
- commits/pushes directly if changed;
- creates no branch/PR and runs no documentation validator or matching Pages check.

### CURRENT VERIFIED BEHAVIOR

Reviewed Markdown -> direct PAT-authenticated website clone/copy/commit/push.

### CURRENT DOCUMENTATION GOVERNANCE

Branch/PR -> `Validate documentation` -> merge -> matching Pages build/deploy success -> live verification.

The mismatch is documented; no redesign is approved.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. Values and the raw export were not committed. Sanitized evidence only was persisted.

Outstanding security action requiring explicit user approval/handling:

```text
rotate/revoke both exposed GitHub PATs and replace the active Appsmith credential configuration
```

Do not perform credential changes automatically.

## Publication Governance for This Workstream

For every focused component:

1. branch from current `main`;
2. open focused PR;
3. latest-head `Validate documentation` must succeed;
4. merge;
5. identify merge commit;
6. matching Pages build/deploy must succeed for that commit;
7. only then begin the next major component.

A cancelled matching Pages run does not satisfy the gate.

## Work Sequence

1. Repository/system architecture — **complete**.
2. Appsmith/config/index — **complete**.
3. Automatic pipeline orchestration/trust — **complete**.
4. Reviewed-document website publication — **merged, Pages gate recovery active**.
5. Asset enrichment/source resolution — blocked until publication gate clears.
6. LLM section-fact extraction.
7. Template/Markdown rendering.
8. LLM review/concision.
9. Generated/reviewed lifecycle/manual recovery.
10. Historical `docs/eirepolitic/pipeline/*` classification.
11. Final current-`main` consistency review.

## Next Safe Development Action

Validate and merge this gate-recovery PR, then confirm the matching Pages build and deploy succeed for its merge commit. Only then create a fresh P1 enrichment branch.

Do not rotate credentials, change PAT scopes/storage, alter workflow permissions/models, modify publication architecture, or change Appsmith access control without explicit approval.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Verified against: current `eirepolitic.github.io` `main`; PR/validation/merge/Pages records above; current `autodoc` source; sanitized Appsmith evidence; current publication runbooks.
- Unverified external state: exact PAT scopes, Appsmith workspace membership, repository-rule enforcement, external-service availability.
