---
title: AutoDoc documentation workstream plan
summary: Persistent completed-work record for the AutoDoc documentation workstream, including evidence rules, publication gates, security findings, and future continuation guidance.
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

## Workstream Status

**Documentation scope P0-P3 is complete.**

This page remains active as the persistent handoff/evidence record because the documentation validator does not have a `completed` status and archived documents must live in the archive section. It is no longer an active build queue.

## Evidence Rules

- Current `autodoc` workflow/Python source is authority for backend behavior.
- Current persisted configuration/intermediate artifacts are supporting evidence.
- Generated/reviewed Markdown is derived evidence and can be stale.
- The sanitized Appsmith export supplied on `2026-08-07` is captured current authority for Appsmith behavior and supersedes the historical Appsmith handoff.
- Current executable source wins over historical/generated prose when they conflict.
- Secret values are never persisted in documentation.

## Completed Gates

| Component | PR | Validation | Merge | Pages |
| --- | --- | --- | --- | --- |
| P0 repository/system architecture | #76 | #126 success | `dd410f89e5b0259b7224593c3feaf6b136ba1a1c` | #182 success |
| P0 Appsmith/config/index | #121 | #231 success | `382093fb826520c0b99dc08b4b609d7f0c40f4f1` | #225 success |
| P0 orchestration/trust | #123 | #240 success | `39b3729389d03de9ea3f09e01a010245c2838e26` | #228 success |
| P0 publication | #125 | #241 success | `9f30e9b46b62174ddfc853543f75589a7657fa00` | #229 cancelled |
| P0 publication gate recovery | #127 | #244 success | `d6a01ff442bf21e1cecded8eddf8251415b5bb7f` | #231 success |
| P1 enrichment | #128 | #245 success | `a92c16d8579f7cd0ea1dcbd962d209994241187b` | #232 success |
| P1 extraction | #129 | #246 success | `1b848d8b3e7ddfb702ce65a6cf4c156f9c7f6ff7` | #233 success |
| P1 rendering | #130 | #247 success | `e00502b88868efb5a6d72dccbcfd78d2f5c9c83b` | #234 success |
| P1 review/concision | #131 | #248 success | `7d0ea3473335dfd0ddff1a5c2147ae0bbc484b8f` | #235 success |
| P2 artifact lifecycle/recovery | #132 | #249 success | `c2e4c491d8a43a2425369b9b03154fdc295c34d7` | #236 success |
| P3 historical artifact classification | #133 | #250 success | `aa1263959e76e4ed4392642cd2c8f934606b4d49` | #237 success |

The original publication merge's matching Pages run was cancelled; PR #127 intentionally supplied the required fresh validated merge and successful matching deployment before P1 began.

## Completed Documentation Map

### Foundation

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc system](/projects/systems/autodoc/)

### P0 boundaries

- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)
- [Sanitized Appsmith live source](/projects/high-director/autodoc-appsmith-live-source-2026-08-07/)

### P1 stages

- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)
- [AutoDoc section-fact extraction](/projects/systems/autodoc-section-fact-extraction/)
- [AutoDoc template/Markdown rendering](/projects/systems/autodoc-template-markdown-rendering/)
- [AutoDoc review/concision](/projects/systems/autodoc-review-concision/)

### P2 recovery

- [Recover AutoDoc artifacts](/projects/runbooks/recover-autodoc-artifacts/)

### P3 historical provenance

- [Historical AutoDoc Irish Politics artifacts](/projects/archive/autodoc-eirepolitic-generated-artifacts/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/) for current Irish Politics implementation authority.

## Key Current Facts

### Appsmith

Current captured app has `Submit` and `DocsViewer`, writes config/index state, can create project `.gitkeep`, and dispatches review/publication workflows. The older handoff's intake-only/no-Actions description is historical drift.

### Automatic pipeline

Current automatic chain is:

```text
enrich -> extract -> render
```

Review is separate.

### Enrichment

Sources are `pasted`, `github_path`, and `github_url`; non-recognized `github_url` values can fall through to generic HTTP GET.

### Extraction

Current model `gpt-4.1-mini`, full enriched JSON per section, rate-limit retries. Current prompt does not interpolate the passed section-template body.

### Rendering

Current model `gpt-4.1-mini`; section template + extracted facts are used. Blank facts produce `_TBD`; current generated front matter uses `layout: default`.

### Review

Standard workflow uses `gpt-4.1`, sends the whole generated document in one request, and writes a separate reviewed artifact. `reviewed` is not human/factual approval.

### Publication

**CURRENT VERIFIED BEHAVIOR:** direct clone/copy/commit/push into `eirepolitic.github.io` using `WEBSITE_PAT`.

**CURRENT DOCUMENTATION GOVERNANCE:** branch/PR -> `Validate documentation` -> merge -> matching Pages success -> live verification.

The mismatch remains intentionally documented and unresolved by this documentation workstream.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. The raw export and token values were not committed or reproduced.

Outstanding security action remains outside documentation scope:

```text
rotate/revoke both exposed GitHub PATs and replace the active Appsmith credential configuration
```

This requires explicit security/access handling. Documentation completion is not authorization to perform it.

## Historical Artifact Rule

The six retained `docs/eirepolitic/pipeline/*` raw/reviewed pairs are AutoDoc-derived historical evidence. Current Irish Politics claims must be verified against current `eirepolitic-data-pipeline` source and its reconciled archive/lineage documentation.

Do not regenerate historical pages merely to make them look current.

## Future Change Procedure

For future AutoDoc implementation changes:

1. identify the owning component page;
2. verify current `autodoc/main` executable source;
3. update implementation and documentation in focused changes;
4. preserve source-vs-historical drift explicitly;
5. use the recovery runbook for artifact failures;
6. treat credential/access/model/prompt/source-host/publication architecture changes as explicit design decisions;
7. publish documentation changes through the current PR/validation/merge/Pages governance.

## Known External/Unresolved State

The documentation does not prove:

- exact live GitHub PAT scopes;
- current Appsmith workspace membership/access policy;
- GitHub repository-rule enforcement outside source-visible configuration;
- OpenAI account quotas/billing/service availability;
- runtime availability of every configured external source.

These are external verification items when operationally required.

## Final Consistency Pass

Final branch:

```text
docs/autodoc-final-consistency
```

Final changes:

- refresh foundation repository/system pages so they no longer say Appsmith is unverified;
- replace stale early-workstream outstanding actions with future-operation guidance;
- add complete cross-links to P0-P3 component pages;
- close this persistent plan as a completed scope record.

The workstream is considered fully closed only after this final branch passes `Validate documentation`, merges, and receives successful matching Pages deployment.

## Next Safe Development Action

After the final closeout gate succeeds, no AutoDoc documentation target remains from the assigned P0-P3 catalogue. Future work should be driven by an implementation change, newly supplied authoritative state, a discovered documentation defect, or the outstanding credential-security action under explicit approval.

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Verified against: current `eirepolitic.github.io/main`; PR/validation/merge/Pages records above; current `autodoc/main`; sanitized Appsmith evidence; P0-P3 pages and artifact inventory.
- Remaining work before full closeout: final PR validation, merge, and matching Pages success only.
