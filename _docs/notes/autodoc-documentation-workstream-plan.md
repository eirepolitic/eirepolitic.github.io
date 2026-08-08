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

## Active Component

```text
P1 target 37: LLM review/concision
Branch: docs/autodoc-review-concision
Draft: _docs/systems/autodoc-review-concision.md
```

Verified review facts:

- source `docs/<project>/<type>/<doc_key>.md`;
- target `docs/<project>/<type>/reviewed/<doc_key>.md`;
- `AUTODOC_MODEL` defaults to `gpt-4.1`; standard workflow explicitly sets `gpt-4.1`;
- entire generated Markdown is sent in one request with `max_output_tokens=12000`;
- prompt asks for concision while preserving formatting/headings/order and removing cross-section repetition;
- no post-review factual/Markdown/front-matter validator and no retry loop;
- current Appsmith dispatch sends `overwrite: "true"`;
- existing reviewed file plus overwrite=false skips before source read;
- workflow stages `docs/` broadly;
- workflow commit step references `$DOC_KEY` outside the step where that env variable is defined, so current source does not establish a populated doc key in the commit message;
- reviewed artifact is LLM concision state, not human/factual/publication approval.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. Values/raw export were not committed. Credential rotation/revocation remains an explicit security/access action requiring user approval/handling.

## Publication Mismatch

**CURRENT VERIFIED BEHAVIOR:** AutoDoc publication directly clones/writes/pushes `eirepolitic.github.io` using `WEBSITE_PAT`.

**CURRENT DOCUMENTATION GOVERNANCE:** branch/PR -> validation -> merge -> matching Pages success -> live verification.

No redesign is approved.

## Remaining Sequence

1. P1 review/concision — **active**.
2. P2 generated/reviewed lifecycle and manual recovery.
3. P3 historical `docs/eirepolitic/pipeline/*` classification.
4. Final current-`main` consistency review.

## Next Safe Development Action

Validate/publish review/concision. After matching Pages success, create a fresh P2 lifecycle/recovery branch.

Do not change models, prompts, overwrite/approval semantics, credentials/permissions, or publication architecture without explicit approval.

## Related Documents

- [AutoDoc section-fact extraction](/projects/systems/autodoc-section-fact-extraction/)
- [AutoDoc template/Markdown rendering](/projects/systems/autodoc-template-markdown-rendering/)
- [AutoDoc review/concision](/projects/systems/autodoc-review-concision/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Unverified external state: PAT scopes, Appsmith workspace membership, OpenAI account/service limits, repository-rule enforcement.
