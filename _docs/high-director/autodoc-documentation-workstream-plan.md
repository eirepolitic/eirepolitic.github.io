---
title: AutoDoc documentation workstream plan
summary: Persistent High Director plan for documenting AutoDoc from verified repository evidence through focused validated pull requests and matching Pages deployments.
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
tags:
  - high-director
  - autodoc
  - documentation
---

# AutoDoc documentation workstream plan

## Purpose

This page is the persistent continuation plan for the complete AutoDoc documentation workstream. It coordinates evidence review, page creation, validation, merge, Pages deployment checks, and live-source requests so another capable agent can continue without conversation history.

## Current State

The workstream is active. Repository discovery material exists at `_docs/high-director/repository-scan-autodoc.md`. The owner-wide catalogue assigns these AutoDoc targets:

- P0: `autodoc` repository/system architecture; Appsmith intake/configuration application; configuration schema/project-index registry; creation-pipeline orchestration/trust boundaries; reviewed-document website-publication boundary.
- P1: asset enrichment/source resolution; LLM section-fact extraction; template/Markdown rendering; LLM review/concision.
- P2: generated/reviewed artifact lifecycle and manual recovery workflows.
- P3: historical AutoDoc-generated `docs/eirepolitic/pipeline/*` artifacts.

The repository/system architecture foundation is complete and published:

```text
PR: #76
Validation: run #126 / success
Merge commit: dd410f89e5b0259b7224593c3feaf6b136ba1a1c
Pages: run #182 / success for the merge commit
```

Published foundation pages are `_docs/repositories/autodoc.md` and `_docs/systems/autodoc.md`.

The active component is the Appsmith/configuration/index boundary on branch `docs/autodoc-appsmith-config-index`. Current repository evidence is sufficient to document the base/enriched JSON and `_index.json` contracts. Exact current live Appsmith widget/query/action state now requires one coherent sanitized Appsmith source before that portion can be called current implementation.

Current backend source takes precedence over historical handoff text. The Appsmith handoff embedded in AutoDoc config evidence is authoritative for the captured implementation at the time of capture, but does not prove exact current live Appsmith state.

No major component is complete until its focused pull request passes `Validate documentation`, is merged, and the matching GitHub Pages deployment succeeds for the merge commit.

## Scope

### Included

- Documentation repository: `eirepolitic.github.io`.
- Source repository: `autodoc`.
- All catalogue targets assigned to the AutoDoc workstream.
- Appsmith intake/configuration behavior evidenced by the repository handoff and, when needed, current live Appsmith exports supplied in sanitized form.
- GitHub configuration/index contracts; source enrichment; OpenAI extraction/rendering/review; generated/reviewed Markdown; publication to the documentation website.
- Exact repository/file/function paths; workflow names/triggers/permissions; JSON/CSV contracts; template types; model/configuration names; artifact paths; secret/PAT names only; external hosts; trust boundaries; failure behavior; rerun/recovery procedures; publication behavior.

### Excluded

- Routine edits to `_docs/high-director/documentation-target-catalogue.md`; it is read-only coordination input.
- Full Irish Politics Analytics implementation, `bb-comp-prices`, `degenerate_investigator`, or Overlord except where AutoDoc cross-references require them.
- Architecture, security, cost, access-control, credential, or irreversible implementation changes without explicit approval.
- Secret values, personal emails/account IDs, private keys, private user data, or token values.
- Treating generated documentation as implementation authority when current executable source contradicts it.

## Source of Truth

- Documentation standard: `DOCUMENTATION_STANDARD.md`.
- Templates: full `_templates/` directory.
- Scope coordination: `_docs/high-director/documentation-target-catalogue.md`.
- Discovery plan: `_docs/high-director/repository-documentation-discovery-plan.md`.
- Existing AutoDoc scan: `_docs/high-director/repository-scan-autodoc.md`.
- Public project landing page: `autodoc.md`.
- Publication governance: `_docs/runbooks/documentation-site-operations.md`, `_docs/runbooks/publish-documentation-change.md`, and `.github/workflows/validate-documentation.yml`.
- AutoDoc executable backend: current `autodoc` workflows and `process/*.py` files.
- Appsmith captured-state evidence: AutoDoc configuration/handoff material, with current live Appsmith taking precedence if later supplied and verified.

Evidence precedence for backend claims is: current executable workflow/Python source > current configuration/artifact contracts > generated/reviewed outputs > historical handoff text. For Appsmith, a current sanitized live export is stronger than the captured repository handoff. Conflicts must be preserved as drift/history rather than silently overwritten.

## Verified Foundation

Current source verifies these top-level boundaries:

1. Appsmith/caller creates or updates base project configuration and historically also maintained an owner `_index.json` registry through the GitHub Contents API.
2. `autodoc` GitHub Actions and Python stages enrich configured assets, extract section facts with OpenAI, render Markdown, review/concisely rewrite generated Markdown, and write stage artifacts back to the repository.
3. `publish_to_website.yml` accepts a reviewed AutoDoc Markdown path, clones `eirepolitic.github.io` using `WEBSITE_PAT`, copies the reviewed file into the website repository, and pushes directly.
4. Current documentation governance separately requires focused branch/PR, `Validate documentation`, merge, then matching Pages success. The current AutoDoc publication workflow does not implement those governance gates.

Verified process entry points include:

- `process/enrich_configs.py`
- `process/section_extract.py`
- `process/render_sections.py`
- `process/review_doc.py`
- `process/update_index.py`

Verified workflow files include:

- `.github/workflows/autodoc_pipeline.yml`
- `.github/workflows/enrich_configs.yml`
- `.github/workflows/section_extract.yml`
- `.github/workflows/render_docs.yml`
- `.github/workflows/review_doc.yml`
- `.github/workflows/index_rebuilder.yaml`
- `.github/workflows/publish_to_website.yml`

Verified configuration/index facts now include:

- base configs at `doc_configs/<project>/<doc_key>.json` with observed top-level fields `project`, `type`, `title`, `doc_key`, `context`, `updated_at`, and `assets`;
- current enrichment source modes `pasted`, `github_path`, and `github_url`;
- enriched configs at `<doc_key>.enriched.json` with per-asset resolution fields plus `_enrichment` metadata;
- `_index.json` entries containing `doc_key`, `title`, `type`, and Git-derived `updated_at`;
- `process/update_index.py` as the authoritative deterministic registry rebuilder.

## Work Sequence

Use focused branches named `docs/autodoc-*`. Planned sequence:

1. Repository/system architecture foundation — **complete via PR #76 / Pages #182**.
2. Appsmith intake/configuration application plus base-config and `_index.json` boundary — **active**.
3. Automatic pipeline orchestration and trust/security boundaries.
4. Reviewed-document website-publication boundary and governance mismatch.
5. Enrichment/source resolution.
6. Section-fact extraction.
7. Template/Markdown rendering.
8. Review/concision.
9. Artifact lifecycle/manual recovery.
10. Historical generated artifacts and final cross-page consistency review.

The Appsmith component must not invent live state. When exact current UI/settings are necessary, request one coherent live source at a time with explicit click-by-click export/copy instructions and a clear list of secret/private fields not to include.

## Security and Access

Technically necessary names may be documented, including `OPENAI_API_KEY`, `GITHUB_TOKEN`, `AUTODOC_GITHUB_TOKEN`, and `WEBSITE_PAT`. Values must never be requested, copied, stored, or published.

Current source establishes trust boundaries among GitHub Actions runners, GitHub repository contents, OpenAI API calls, configured external asset hosts, and the documentation repository. Repository workflow definitions prove configured credential names and declared permissions, not the exact live GitHub/Appsmith access policy outside source.

## Publication Governance

For each focused documentation pull request:

1. Open the PR from `docs/autodoc-*` into `main`.
2. Confirm `Validate documentation` succeeds.
3. Merge only after validation succeeds.
4. Identify the merge commit.
5. Confirm the matching GitHub Pages deployment succeeds for that merge commit.
6. Only then begin the next major AutoDoc component.

This governance applies to this documentation workstream even though current AutoDoc `publish_to_website.yml` uses a separate direct-push mechanism. Documentation must label the latter **CURRENT VERIFIED BEHAVIOR** and the former **CURRENT DOCUMENTATION GOVERNANCE**.

## Failure Modes and Recovery

- **Documentation branch becomes stale:** compare with current `main`; synchronize before final cross-cutting edits.
- **Validation failure:** inspect the `Validate documentation` run and fix metadata, links, placeholders, or structural errors before merge.
- **Pages deployment failure:** do not begin the next major component; inspect the matching Pages run and repair the site/documentation issue first.
- **Backend source conflicts with handoff:** use current executable source for current backend behavior and retain the handoff discrepancy as historical/drift evidence.
- **Appsmith current-state ambiguity:** do not infer. Request one sanitized live Appsmith source using explicit UI steps.
- **Secret exposure risk:** publish names/roles only; never values.

## Known Limitations

- Exact current live Appsmith configuration has not yet been verified.
- Repository source establishes expected GitHub/OpenAI/publication behavior but does not prove all live external account permissions or credential scopes.
- Some generated/reviewed artifacts are historical observations and may not represent current source behavior.
- The direct website publication workflow conflicts with current documentation governance; this workstream documents the mismatch but does not redesign it without approval.
- No formal JSON Schema or centralized config validator was found; the current config/index contract is consumer-enforced.

## Outstanding Work

1. Obtain one coherent sanitized current AutoDoc Appsmith application source and compare it to the repository handoff.
2. Complete the Appsmith intake/configuration page and finish the config/index focused PR.
3. Publish orchestration/trust-boundary documentation from current workflows and process code.
4. Publish the website-publication boundary with verified current behavior versus current governance.
5. Complete P1 stage documentation.
6. Complete P2 lifecycle/recovery documentation.
7. Classify and document P3 historical artifacts.
8. Synchronize with current `main` and perform final cross-page/link/evidence consistency review.

## Next Safe Development Action

Request a single sanitized export/source of the current live AutoDoc Appsmith application. Compare widgets, queries, JS Objects, bindings, datasource/authentication shape, and submit/load behavior with the captured handoff; persist the sanitized evidence and drift record in `eirepolitic.github.io`; then complete and validate the focused Appsmith/config/index PR.

## Handoff Notes

- Keep this page synchronized with completed PRs, merge commits, validation runs, Pages runs, and next safe action.
- Use repository name only with the GitHub integration; owner configuration is external.
- Do not edit parallel workstream plans during routine work.
- Persist sanitized authoritative source evidence into `eirepolitic.github.io`; do not leave it only in chat.
- Do not modify AutoDoc implementation merely because the documentation identifies drift or a governance mismatch.

## Related Documents

- [Documentation target catalogue](/projects/high-director/documentation-target-catalogue/)
- [Repository documentation discovery plan](/projects/high-director/repository-documentation-discovery/)
- [Repository scan — AutoDoc](/projects/high-director/repository-scan-autodoc/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [Documentation site operations](/docs/runbooks/documentation-site-operations/)
- [Publish a documentation change](/projects/runbooks/publish-documentation-change/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `eirepolitic.github.io` `main`; foundation PR #76, validation run #126, merge commit `dd410f89e5b0259b7224593c3feaf6b136ba1a1c`, Pages run #182; current `autodoc` tree; primary workflows and `process/*.py`; `doc_configs/autodoc/autodoc_app.json`, `autodoc_creation_pipeline.json`, enriched config, and `_index.json`.
- Verified by: High Director
- Verification scope: workstream progress, foundation publication gate, current config/enriched/index contracts, evidence hierarchy, security/publication constraints, and next live-source requirement.
- Unverified areas: exact current live Appsmith configuration and external account permission state.
