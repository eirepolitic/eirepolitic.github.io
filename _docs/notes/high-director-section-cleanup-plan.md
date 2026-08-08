---
title: High Director documentation section cleanup plan
summary: Completion and maintenance record for narrowing the High Director section to the agent itself and relocating unrelated coordination, historical, and documentation-site material.
section: notes
doc_type: note
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 110
permalink: /projects/notes/high-director-section-cleanup-plan/
tags:
  - high-director
  - documentation
  - information-architecture
  - cleanup
---

# High Director documentation section cleanup plan

## Current State

The information-architecture cleanup is implementation-complete and at its final closeout gate.

The active **High Director** website section is now intentionally limited to **14 pages** whose primary subject is the High Director agent itself: configuration, capabilities, integrations, runtime architecture, security/configuration, code/dependencies, documentation/source inventory, and verification.

Active coordination records that are not about High Director were moved to **Notes**. Completed workstreams, discovery records, documentation-site/build initiatives, and the predecessor documentation-site architecture page were reclassified to **Archive**. Current documentation-site architecture is owned by **Systems → Eire Politic Documentation Site**.

## Classification Rule

Pages are classified by their **primary subject**, not by the tool, agent, person, or process that authored, coordinated, or executed the work.

High Director is not a general project-management bucket.

## Final Active High Director Set

The canonical active set is:

1. `overview.md`
2. `gpt-configuration.md`
3. `capability-component-inventory.md`
4. `github-integration.md`
5. `github-action-openapi-schema.md`
6. `github-wrapper-lambda.md`
7. `github-wrapper-live-aws-configuration.md`
8. `google-workspace-action.md`
9. `runtime-architecture.md`
10. `data-flows.md`
11. `security-configuration-reference.md`
12. `code-and-dependency-reference.md`
13. `repository-documentation-inventory.md`
14. `verification-record.md`

The canonical detailed map is `_docs/high-director/repository-documentation-inventory.md`.

## Active Coordination Moved to Notes

The following records were physically moved from `_docs/high-director/` to `_docs/notes/` and reclassified as Notes:

- `autodoc-documentation-workstream-plan.md`
- `documentation-target-catalogue.md`
- `repository-scan-autodoc.md`

Established public permalinks were retained so existing public links continue to resolve.

This cleanup plan itself also lives in Notes while the final closeout gate is being recorded.

## Completed Records Reclassified to Archive

These completed records remain physically under `_docs/high-director/` for compatibility but use `section: archive`, `status: archived`, and archive metadata, so they no longer appear in the active High Director section:

- `bb-comp-prices-documentation-workstream-plan.md`
- `degenerate-investigator-documentation-workstream-plan.md`
- `ipa-oireachtas-documentation-workstream-plan.md`
- `overlord-documentation-workstream-plan.md`
- `repository-documentation-discovery-plan.md`
- `repository-scan-bb-comp-prices.md`
- `repository-scan-degenerate-investigator.md`
- `repository-scan-overlord.md`
- `site-rebuild-plan.md`
- `documentation-section-template-plan.md`
- `example-documents-plan.md`
- `high-director-documentation-initiative-plan.md`
- `site-architecture.md`

### Why archive-in-place was used

The initial plan expected completed records to move physically into `_docs/archive/`. During migration, inbound-link auditing showed that many current pages referenced these historical files by relative filesystem path.

The site navigation is metadata-driven, not folder-driven. Reclassifying those records in place therefore provides the desired website information architecture while preserving existing relative links and default URLs. This was safer than forcing large unrelated link rewrites solely to change physical folders.

A later URL/folder-normalization initiative may physically relocate them if the site first gains an explicit redirect strategy.

## Documentation Site Consolidation

The former `_docs/high-director/site-architecture.md` page was superseded and reclassified as Archive.

Unique current material was consolidated into `_docs/systems/documentation-site.md`, including:

- rendering/layout asset ownership;
- navigation/discovery behavior;
- search-index behavior;
- documentation validation responsibilities;
- branch/PR/merge/exact-SHA Pages change-management flow;
- URL-migration constraints.

The Systems page is now the canonical current documentation-site architecture reference.

## Governance Changes Completed

- `_templates/high-director-template.md` now applies only when the primary subject is High Director itself.
- `_data/docs_sections.yml` describes High Director as configuration/capabilities/integrations/runtime/security/implementation/verification rather than a build-plan bucket.
- `DOCUMENTATION_STANDARD.md` now includes the primary-subject classification rule and lifecycle guidance for active coordination versus completed workstreams.
- Notes explicitly supports active coordination material.

## Final Reference Audit

The closeout audit identified and corrected two current-authority issues caused by the classification changes:

- `_docs/high-director/overview.md` no longer presents the archived High Director documentation-build plan as the current phase/status authority; it points to the current inventory and verification record.
- `_docs/high-director/repository-documentation-inventory.md` now contains the actual 14-page active set, treats the completed initiative/site-architecture records as archive, and points documentation-site architecture to Systems.

It also corrected `_docs/repositories/autodoc.md` so the AutoDoc discovery source path is `_docs/notes/repository-scan-autodoc.md` rather than its former High Director filesystem location.

Public AutoDoc catalogue/workstream/scan URLs remain unchanged by design.

## Delivery Ledger

| Phase | PR | Merge / deployed state | Pages gate |
| --- | ---: | --- | ---: |
| 1 — governance | #117 | `8b9996900dc89c734478cc6825361102dfd898c1` | #222 success |
| 2 — active coordination to Notes | #118 | `93f8f1b6a89bdc643ce057928f7dd594e8bdee6d` | #223 success |
| 3A — completed repository workstreams to Archive | #119 | `321889b5c34d0be4ba7941dc276549e52bd964ff` | #224 success |
| 3B — discovery/build initiatives to Archive | #122 | `5ac539de93597dcf7b1c3fa0b781d1a7a00d9547` | #226 success |
| 4 — documentation-site architecture consolidation | #124 | `d9c0daffaa484a69afff57422fcd9b3f85ab7c89` | #227 cancelled as superseded; newer main #228 success and verified to contain Phase 4 changes |
| 5 — final audit and closeout synchronization | closeout branch | current change set | pending final validation/merge/Pages gate |

Phase 4's exact deployment #227 was cancelled after a newer `main` commit superseded it. Before accepting the newer deployment, both Phase 4 files were re-read from newer `main` and confirmed present unchanged. Pages #228 then succeeded for that newer state.

## URL and Compatibility Decisions

- No new top-level Workstreams/Programmes section was introduced; existing Notes and Archive sections solve the current classification problem with less site churn.
- The site does not currently use `jekyll-redirect-from` or another redirect plugin.
- Existing public permalinks were therefore preserved wherever practical.
- Archive-in-place was used where physical moves would break numerous relative references.
- Physical folder location should not be interpreted as website section membership; front-matter `section` controls category placement.

## Security and Access

This cleanup changed documentation classification and content only. It did not alter High Director runtime behavior, credentials, IAM, OAuth scopes, access controls, architecture, or cost-bearing infrastructure.

No secret values, private account identifiers, tokens, keys, or personal data were introduced.

## Maintenance Rules

Future documentation should follow these rules:

- High Director pages must be primarily about High Director itself.
- Active owner-wide/repository documentation coordination belongs in Notes unless a dedicated programme section is deliberately introduced later.
- Completed workstream/discovery/build plans belong in Archive.
- Repository/system implementation pages belong in their subject sections even when High Director creates them.
- Documentation-site architecture belongs in Systems.
- Preserve stable public URLs during category changes unless an explicit redirect mechanism exists.

## Remaining Work

Only the closeout publication gate remains for this cleanup record and final reference corrections:

1. run `Validate documentation` on the closeout branch;
2. merge only after validation succeeds;
3. confirm the matching or safely superseding Pages deployment contains the closeout changes.

After that, the cleanup is maintenance-only.

## Related Documents

- [High Director overview](/projects/high-director/)
- [High Director documentation inventory](/docs/high-director/repository-documentation-inventory/)
- [High Director verification record](/projects/high-director/verification-record/)
- [Documentation site](/projects/systems/documentation-site/)
- [Documentation target catalogue](/projects/high-director/documentation-target-catalogue/)
- [Documentation standard](/DOCUMENTATION_STANDARD.md)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: deployed `main` through Pages #228; current High Director canonical pages; Notes moves; archive-in-place records; `_templates/high-director-template.md`; `_data/docs_sections.yml`; `DOCUMENTATION_STANDARD.md`; `_docs/systems/documentation-site.md`; current AutoDoc repository page.
- Verified by: High Director
- Verification scope: section classification, 14-page active set, URL/link compatibility strategy, documentation-site ownership, stale current-authority references, and delivery/deployment ledger through Phase 4.
