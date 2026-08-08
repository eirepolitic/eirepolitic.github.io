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

## Scope

- **P0:** repository/system architecture; Appsmith intake/configuration; config schema/project index; pipeline orchestration/trust; reviewed-document website publication.
- **P1:** enrichment/source resolution; LLM section-fact extraction; template/Markdown rendering; LLM review/concision.
- **P2:** generated/reviewed artifact lifecycle and manual recovery.
- **P3:** historical `docs/eirepolitic/pipeline/*` artifacts.

Backend authority is current workflows/Python before current persisted contracts, generated outputs, or historical prose. Current sanitized live Appsmith export supersedes the older Appsmith handoff for present Appsmith behavior.

## Completed P0 Components

### Repository/system architecture

```text
PR #76
Validate documentation #126: success
Merge: dd410f89e5b0259b7224593c3feaf6b136ba1a1c
Pages #182: success
Docs: _docs/repositories/autodoc.md; _docs/systems/autodoc.md
```

### Appsmith/configuration/index

```text
Stale PR #120: closed without merge
Replacement PR #121
Validate documentation #231: success
Merge: 382093fb826520c0b99dc08b4b609d7f0c40f4f1
Pages #225: success
Docs: _docs/systems/autodoc-appsmith-intake.md
      _docs/data/autodoc-configuration-and-project-index.md
      _docs/high-director/autodoc-appsmith-live-source-2026-08-07.md
```

### Pipeline orchestration/trust

```text
PR #123
Validate documentation #240: success
Merge: 39b3729389d03de9ea3f09e01a010245c2838e26
Pages #228: success
Doc: _docs/systems/autodoc-pipeline-orchestration.md
```

### Reviewed-document website publication

Primary documentation merge:

```text
PR #125
Validate documentation #241: success
Merge: 9f30e9b46b62174ddfc853543f75589a7657fa00
Pages #229: cancelled before successful build/deploy
Doc: _docs/systems/autodoc-publication-boundary.md
```

Required gate recovery:

```text
PR #127
Validate documentation #244: success
Merge: d6a01ff442bf21e1cecded8eddf8251415b5bb7f
Pages #231: success for recovery merge
```

The recovery merge contains the already-merged publication documentation and completed the required build/deploy gate. **P0 is complete.**

## Active Component

```text
P1 target 34: Asset enrichment/source resolution
Branch: docs/autodoc-enrichment
Draft: _docs/systems/autodoc-asset-enrichment.md
```

Verified implementation source:

```text
autodoc/process/enrich_configs.py
autodoc/.github/workflows/enrich_configs.yml
autodoc/.github/workflows/autodoc_pipeline.yml
```

Key verified enrichment facts:

- supported source modes: `pasted`, `github_path`, `github_url`;
- recognized GitHub blob/raw URLs are fetched through GitHub Contents API;
- non-recognized `github_url` locators fall back to generic HTTP GET rather than a GitHub-only allowlist;
- GitHub/HTTP requests use a 60-second timeout;
- text stores canonical `resolved_content` plus `resolved_content_lines`;
- heuristic binary content is base64 persisted and flagged `binary_base64=true`;
- per-asset resolution failures are captured in enriched JSON and normally do not fail the configuration;
- config-level failures continue across a broad manual run but make process exit code `1`;
- automatic enrichment uses `--overwrite` before extraction;
- manual workflow supports project/doc filtering, overwrite, and `only_missing`;
- resolved content, final URL/provenance metadata, and errors can be persisted, making source configuration a security/privacy boundary.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. Values and the raw export were not committed; sanitized evidence only was persisted.

Outstanding security action requiring explicit user approval/handling:

```text
rotate/revoke both exposed GitHub PATs and replace the active Appsmith credential configuration
```

Do not perform credential changes automatically.

## Publication Architecture Mismatch

### CURRENT VERIFIED BEHAVIOR

`publish_to_website.yml` uses `WEBSITE_PAT` to clone `eirepolitic.github.io`, copy reviewed Markdown under `projects/<dest_type>/`, commit if changed, and push directly.

### CURRENT DOCUMENTATION GOVERNANCE

Material documentation changes require branch/PR -> `Validate documentation` -> merge -> matching Pages build/deploy success -> live verification.

The mismatch is documented; no redesign is approved.

## Workstream Gate

For every focused component:

1. branch from current `main`;
2. open focused PR;
3. latest-head `Validate documentation` succeeds;
4. merge;
5. record merge SHA;
6. matching Pages build/deploy succeeds for that SHA;
7. only then begin the next major component.

A failed or cancelled matching Pages run does not satisfy the gate.

## Work Sequence

1. P0 repository/system architecture — **complete**.
2. P0 Appsmith/config/index — **complete**.
3. P0 orchestration/trust — **complete**.
4. P0 website publication — **complete after gate recovery**.
5. P1 asset enrichment/source resolution — **active**.
6. P1 section-fact extraction.
7. P1 template/Markdown rendering.
8. P1 review/concision.
9. P2 generated/reviewed lifecycle and manual recovery.
10. P3 historical `docs/eirepolitic/pipeline/*` classification.
11. Final current-`main` consistency review.

## Next Safe Development Action

Validate and publish the enrichment component. After a successful matching Pages deployment, create a fresh branch for LLM section-fact extraction and its persisted CSV contract.

Do not change source-host policy, PAT scope/storage, workflow permissions, models, publication architecture, or Appsmith access control without explicit approval.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)
- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Verified against: current `eirepolitic.github.io` `main`; gate records above; current `autodoc` source; sanitized Appsmith evidence; current publication runbooks.
- Unverified external state: exact PAT scopes, Appsmith workspace membership, repository-rule enforcement, external-service availability.
