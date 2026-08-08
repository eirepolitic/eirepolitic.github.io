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

## Evidence and Governance

Current backend workflows/Python outrank persisted artifacts and historical prose. Current sanitized Appsmith export outranks the historical Appsmith handoff. Secret values are never persisted.

Every component requires: fresh `docs/autodoc-*` branch -> focused PR -> latest-head `Validate documentation` success -> merge -> matching Pages build/deploy success -> next component.

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

**P0 and P1 are complete.**

## Active Component

```text
P2 target 44: Generated/reviewed artifact lifecycle and manual recovery
Branch: docs/autodoc-artifact-lifecycle
Draft: _docs/runbooks/recover-autodoc-artifacts.md
```

Verified lifecycle:

```text
base config
-> enriched JSON
-> section summary CSV
-> generated/raw Markdown
-> reviewed Markdown
-> optional website publication copy
```

Separate registry:

```text
doc_configs/<project>/_index.json
```

Recovery principle: identify the last valid persisted artifact, correct the actual upstream cause, and rerun only the smallest necessary downstream stage. `_index.json` is registry state and should be rebuilt independently when stale.

Manual recovery workflows currently cover enrichment, extraction, rendering, review, and index rebuild. Publication remains separate and should not be used to diagnose upstream generation failures.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. Values/raw export were not committed. Credential rotation/revocation remains an explicit security/access action requiring user approval/handling.

## Publication Mismatch

**CURRENT VERIFIED BEHAVIOR:** AutoDoc publication directly clones/writes/pushes `eirepolitic.github.io` using `WEBSITE_PAT`.

**CURRENT DOCUMENTATION GOVERNANCE:** branch/PR -> validation -> merge -> matching Pages success -> live verification.

No redesign is approved.

## Remaining Sequence

1. P2 generated/reviewed lifecycle and manual recovery — **active**.
2. P3 historical `docs/eirepolitic/pipeline/*` classification.
3. Final current-`main` consistency review and workstream closeout.

## Next Safe Development Action

Validate/publish the P2 recovery runbook. After matching Pages success, create a fresh P3 branch to classify historical `docs/eirepolitic/pipeline/*` raw/reviewed artifacts as historical generated evidence rather than current Irish Politics implementation authority.

Do not change models, prompts, recovery workflows, overwrite semantics, credentials/permissions, or publication architecture without explicit approval.

## Related Documents

- [AutoDoc template/Markdown rendering](/projects/systems/autodoc-template-markdown-rendering/)
- [AutoDoc review/concision](/projects/systems/autodoc-review-concision/)
- [Recover AutoDoc artifacts](/projects/runbooks/recover-autodoc-artifacts/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Unverified external state: PAT scopes, Appsmith workspace membership, OpenAI account/service limits, repository-rule enforcement.
