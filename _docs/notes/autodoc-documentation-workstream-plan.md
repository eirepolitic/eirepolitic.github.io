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

Persistent continuation plan for the AutoDoc documentation workstream. The owner-wide target catalogue remains read-only coordination input.

## Evidence Rules

- Current backend workflows/Python outrank persisted artifacts and historical prose.
- Current sanitized live Appsmith export outranks the historical Appsmith handoff for Appsmith behavior.
- Conflicts remain documented as drift/history.
- Secret values are never persisted; only technically necessary secret names may be documented.

## Completed P0

| Component | PR | Validation | Merge | Pages |
| --- | --- | --- | --- | --- |
| Repository/system architecture | #76 | #126 success | `dd410f89e5b0259b7224593c3feaf6b136ba1a1c` | #182 success |
| Appsmith/config/index | #121 | #231 success | `382093fb826520c0b99dc08b4b609d7f0c40f4f1` | #225 success |
| Pipeline orchestration/trust | #123 | #240 success | `39b3729389d03de9ea3f09e01a010245c2838e26` | #228 success |
| Website publication | #125 | #241 success | `9f30e9b46b62174ddfc853543f75589a7657fa00` | #229 cancelled |
| Publication gate recovery | #127 | #244 success | `d6a01ff442bf21e1cecded8eddf8251415b5bb7f` | #231 success |

P0 is complete. The publication recovery merge contains the already-merged publication page and supplied the required successful matching Pages gate.

## Completed P1 Components

### Asset enrichment/source resolution

```text
Doc: _docs/systems/autodoc-asset-enrichment.md
PR #128
Validate documentation #245: success
Merge: a92c16d8579f7cd0ea1dcbd962d209994241187b
Pages #232: success
```

Key verified facts include `pasted`, `github_path`, and `github_url` modes; generic HTTP fallback for non-recognized `github_url` locators; GitHub Contents API behavior; persisted text/binary contracts; per-asset error tolerance; overwrite/only-missing behavior; and source-resolution privacy/security boundaries.

## Active Component

```text
P1 target 35: LLM section-fact extraction
Branch: docs/autodoc-section-extraction
Draft: _docs/systems/autodoc-section-fact-extraction.md
```

Current verified facts:

- required base config plus enriched config;
- section list comes from H2 headings in merged base/type templates;
- current model hard-coded as `gpt-4.1-mini`, `temperature=0`;
- full enriched JSON is sent for every section with no source-code truncation;
- current prompt uses section title but does not interpolate the passed section-template body despite the function signature/docstring;
- rate-limit errors retry up to eight attempts with parsed delay or exponential fallback plus jitter;
- six-second throttle between successful section calls;
- output overwrites `doc_configs/<project>/summaries/<doc_key>.csv`;
- CSV has exactly `section_title,extracted_facts`, one row per H2 section;
- bullet syntax/factual correctness are requested but not programmatically validated;
- rows are written only after all sections finish, so a failed run can leave an older CSV on disk.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. They were not reproduced or committed; the raw export was not committed.

Outstanding security action requiring explicit approval/handling:

```text
rotate/revoke both exposed GitHub PATs and replace the active Appsmith credential configuration
```

## Publication Mismatch

**CURRENT VERIFIED BEHAVIOR:** `publish_to_website.yml` directly clones/writes/pushes `eirepolitic.github.io` using `WEBSITE_PAT`.

**CURRENT DOCUMENTATION GOVERNANCE:** branch/PR -> `Validate documentation` -> merge -> matching Pages success -> live verification.

No redesign is approved.

## Workstream Gate

For each component: fresh branch from current `main` -> focused PR -> latest-head validation success -> merge -> matching Pages build/deploy success -> next component.

## Work Sequence

1. P0 architecture — **complete**.
2. P0 Appsmith/config/index — **complete**.
3. P0 orchestration/trust — **complete**.
4. P0 publication — **complete after recovery**.
5. P1 enrichment — **complete**.
6. P1 extraction — **active**.
7. P1 template/Markdown rendering.
8. P1 review/concision.
9. P2 artifact lifecycle/manual recovery.
10. P3 historical artifact classification.
11. Final consistency review.

## Next Safe Development Action

Validate/publish extraction. After matching Pages success, create a fresh branch for template/Markdown rendering.

Do not change models, prompts/context selection, retry policy, source-host policy, credentials/permissions, publication architecture, or Appsmith access control without explicit approval.

## Related Documents

- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)
- [AutoDoc section-fact extraction](/projects/systems/autodoc-section-fact-extraction/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Unverified external state: PAT scopes, Appsmith workspace membership, external service/account limits, repository-rule enforcement.
