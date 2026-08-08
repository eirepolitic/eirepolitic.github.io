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
| P2 artifact lifecycle/recovery | #132 | #249 success | `c2e4c491d8a43a2425369b9b03154fdc295c34d7` | #236 success |

**P0, P1, and P2 are complete.**

## Active Component

```text
P3 target 56: Historical docs/eirepolitic/pipeline/* artifact classification
Branch: docs/autodoc-historical-artifacts
Draft: _docs/archive/autodoc-eirepolitic-generated-artifacts.md
```

Verified current artifact inventory contains six `pipeline` document keys, each with both raw and `reviewed/` Markdown:

```text
constituency_images_indexer
debate_issue_classifier
llm_column_creator
member_images_pipeline
member_summaries_table
s3_column_deleter
```

Current classification:

- these are derived AutoDoc documentation artifacts with complete base/enriched/summary/raw/reviewed provenance retained in `autodoc`;
- `reviewed/` is AutoDoc LLM-concision state, not human/factual approval;
- their generated prose is historical evidence, not current Irish Politics implementation authority;
- current `eirepolitic.github.io` already contains dedicated source-reconciled archive/lineage pages for all six;
- current implementation questions should use `eirepolitic-data-pipeline` source plus those reconciled archive records.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. Values/raw export were not committed. Credential rotation/revocation remains an explicit security/access action requiring user approval/handling.

## Publication Mismatch

**CURRENT VERIFIED BEHAVIOR:** AutoDoc publication directly clones/writes/pushes `eirepolitic.github.io` using `WEBSITE_PAT`.

**CURRENT DOCUMENTATION GOVERNANCE:** branch/PR -> validation -> merge -> matching Pages success -> live verification.

No redesign is approved.

## Remaining Sequence

1. P3 historical artifact classification — **active**.
2. Final current-`main` cross-page/link/evidence consistency review and workstream closeout.

## Next Safe Development Action

Validate/publish the P3 archive index. After matching Pages success, create one final fresh branch from current `main` for consistency review, stale-status correction, cross-link repair if required, and persistent-plan closeout.

Do not change historical Irish Politics implementation, AutoDoc models/prompts/workflows, credentials/permissions, or publication architecture without explicit approval.

## Related Documents

- [Recover AutoDoc artifacts](/projects/runbooks/recover-autodoc-artifacts/)
- [Historical AutoDoc Irish Politics artifacts](/projects/archive/autodoc-eirepolitic-generated-artifacts/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [AutoDoc repository](/projects/repositories/autodoc/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Unverified external state: PAT scopes, Appsmith workspace membership, OpenAI account/service limits, repository-rule enforcement, exact historical run IDs for every archived artifact pair.
