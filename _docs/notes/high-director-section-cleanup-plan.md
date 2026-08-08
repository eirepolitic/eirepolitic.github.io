---
title: High Director documentation section cleanup plan
summary: Plan to narrow the High Director section to the agent itself, relocate programme-management and historical material, consolidate documentation-site content, and preserve stable URLs during migration.
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

## Purpose

This plan corrects documentation information-architecture drift in `_docs/high-director/`. The section currently mixes documentation about the High Director agent itself with owner-wide documentation programmes, repository scans, completed workstreams, and documentation-site implementation material.

The target state is that **High Director** contains only pages whose primary subject is the High Director agent: its configuration, capabilities, integrations, runtime architecture, security boundaries, implementation references, and verification.

## Migration Principles

1. Preserve public URLs during the initial move because the site does not currently use a redirect plugin.
2. Change physical collection path and `section` together so navigation reflects the new category.
3. Keep active programme-management records under `Notes` unless a dedicated programme/workstream section is introduced later.
4. Move completed project/workstream/discovery records to `Archive`.
5. Consolidate documentation-site architecture into the existing `Systems -> Documentation site` page instead of maintaining a competing High Director page.
6. Do not move pages merely because High Director authored or coordinated them; classify by the page's primary subject.
7. Validate every focused PR before merge and confirm Pages deployment after merge.
8. Update internal links and related-document references as each migration is performed.

## Target High Director Scope

Pages that should remain in `_docs/high-director/`:

- `overview.md`
- `gpt-configuration.md`
- `capability-component-inventory.md`
- `github-integration.md`
- `github-action-openapi-schema.md`
- `github-wrapper-lambda.md`
- `github-wrapper-live-aws-configuration.md`
- `google-workspace-action.md`
- `runtime-architecture.md`
- `data-flows.md`
- `security-configuration-reference.md`
- `code-and-dependency-reference.md`
- `repository-documentation-inventory.md`
- `verification-record.md`

These pages directly describe the High Director agent, its implementation, integrations, trust boundaries, configuration, or verification.

## Pages to Move to Notes

Active programme-management material should move physically to `_docs/notes/`, change `section: notes`, and initially retain its existing permalink where practical:

- `autodoc-documentation-workstream-plan.md`
- `documentation-target-catalogue.md`
- `repository-scan-autodoc.md`

Reason: these are current coordination/discovery records, but their subject is a documentation programme or another repository rather than High Director itself.

## Pages to Move to Archive

Completed workstreams, completed discovery plans/scans, and completed documentation initiatives should move physically to `_docs/archive/`, use archive-compliant metadata, and retain their existing public permalink during the first migration:

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

Reason: these are historical project/programme records rather than current High Director configuration/reference material.

## Documentation Site Consolidation

`_docs/high-director/site-architecture.md` should not remain an active High Director page.

Migration:

1. Compare it with `_docs/systems/documentation-site.md`.
2. Merge any unique current architecture, navigation, validation, deployment, security, or change-management details into the system page.
3. Move the old High Director page to `_docs/archive/` as a superseded architecture record while retaining its current permalink.
4. Add an explicit successor link to `/projects/systems/documentation-site/`.
5. Update incoming references to use the system page when they mean current documentation-site architecture.

## Governance Changes

### High Director template

Tighten `_templates/high-director-template.md` so it is used only for documentation whose primary subject is the High Director agent itself.

Remove broad language that treats arbitrary “agent-assisted development plans” or generic continuation documents as High Director documentation.

### Section description

Update `_data/docs_sections.yml` so High Director is described as agent configuration/capabilities/integrations/runtime/security/verification, not as a general build-plan bucket.

### Documentation standard

Add a short classification rule to `DOCUMENTATION_STANDARD.md`:

> Classify a page by its primary subject, not by the tool/agent that authored, coordinated, or executed the work.

This prevents future project plans from being filed under High Director merely because High Director is performing them.

## Execution Phases

### Phase 1 — Governance

- create this persistent cleanup plan under Notes;
- tighten High Director template;
- tighten High Director section description;
- add primary-subject classification guidance to the documentation standard;
- validate, merge, deploy.

### Phase 2 — Active coordination moves

Move the current owner-wide/AutoDoc coordination records to Notes while preserving URLs. Update related links and validate.

### Phase 3 — Completed workstream/discovery archive moves

Move completed workstream plans, completed repository scans, and completed documentation initiatives to Archive. Add archive metadata and successor/current-authority links where applicable.

### Phase 4 — Documentation-site consolidation

Merge unique `site-architecture.md` content into the current Documentation site system page, then archive the superseded High Director architecture page.

### Phase 5 — Final audit

- enumerate `_docs/high-director/` again;
- confirm only High Director-subject pages remain;
- search for broken/stale internal references;
- run documentation validator;
- update this plan with the final page count and move ledger;
- merge/deploy closeout PR.

## Validation Requirements

Before each merge:

1. run the repository documentation validator;
2. fix missing metadata/internal links/category issues;
3. merge only after validation succeeds;
4. confirm the corresponding Pages deployment succeeds before beginning the next migration phase.

## Known Constraints

- The site currently does not use `jekyll-redirect-from` or another redirect plugin.
- Therefore initial category moves should retain existing permalinks to avoid breaking external bookmarks.
- Physical file location and front-matter `section` are what should change navigation/category placement during this cleanup.
- A later URL-normalization project can introduce canonical destination URLs plus redirects if desired.

## Next Safe Action

Complete Phase 1 governance changes on the current branch, validate them, and merge/deploy before moving any existing High Director pages.

## Related Documents

- [High Director overview](/projects/high-director/)
- [Documentation site](/projects/systems/documentation-site/)
- [Documentation target catalogue](/projects/high-director/documentation-target-catalogue/)
- [Documentation standard](/DOCUMENTATION_STANDARD.md)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `_docs/high-director/` inventory, `_templates/high-director-template.md`, `_data/docs_sections.yml`, `_config.yml`, `_docs/systems/documentation-site.md`, and `DOCUMENTATION_STANDARD.md`.
- Verified by: High Director
- Verification scope: current section population, classification problem, migration destinations, permalink/redirect constraint, governance changes, and phased execution plan.
