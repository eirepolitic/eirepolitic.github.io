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

## Active Component

```text
P1 target 36: Template and Markdown rendering
Branch: docs/autodoc-rendering
Draft: _docs/systems/autodoc-template-markdown-rendering.md
```

Verified current rendering facts:

- renderer: `process/render_sections.py`;
- model: hard-coded `gpt-4.1-mini`, `temperature=0`;
- requires base config, enriched config, and summaries CSV;
- base template plus optional `templates/types/<type>.md` extension;
- current type extensions: generic, pipeline, dataset, dashboard, investigation;
- only `{{title}}`, `{{project}}`, `{{type}}`, `{{generated_at}}` are replaced deterministically;
- section placeholder text remains in the template body and is supplied to the LLM as guidance;
- model receives section title + section template body + extracted facts, not enriched JSON;
- blank facts skip the model and emit `_TBD (no extracted facts provided for this section)._`;
- no renderer-local retry/backoff;
- front matter is ensured with current title and `layout: default`;
- generated output overwrites `docs/<project>/<type>/<doc_key>.md`;
- historical generated artifacts can contain older metadata such as `layout: doc` and are not current-source authority.

## Security Finding

The supplied Appsmith export contained two distinct GitHub PAT values. Values/raw export were not committed. Outstanding credential rotation/revocation requires explicit security/access approval and handling.

## Publication Mismatch

**CURRENT VERIFIED BEHAVIOR:** AutoDoc publication directly clones/writes/pushes `eirepolitic.github.io` using `WEBSITE_PAT`.

**CURRENT DOCUMENTATION GOVERNANCE:** branch/PR -> validation -> merge -> matching Pages success -> live verification.

No redesign is approved.

## Remaining Sequence

1. P1 rendering — **active**.
2. P1 review/concision.
3. P2 generated/reviewed lifecycle and manual recovery.
4. P3 historical artifact classification.
5. Final current-`main` consistency review.

## Next Safe Development Action

Validate/publish rendering. After matching Pages success, create a fresh branch for review/concision.

Do not change models, prompts/template semantics, front-matter/TBD policy, credentials/permissions, or publication architecture without explicit approval.

## Related Documents

- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)
- [AutoDoc section-fact extraction](/projects/systems/autodoc-section-fact-extraction/)
- [AutoDoc template/Markdown rendering](/projects/systems/autodoc-template-markdown-rendering/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)

## Verification Record

- Last verified: `2026-08-07` local programme date.
- Verified by: High Director.
- Unverified external state: PAT scopes, Appsmith workspace membership, OpenAI account/service limits, repository-rule enforcement.
