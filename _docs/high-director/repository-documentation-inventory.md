---
title: High Director Repository Documentation Inventory
summary: Repository-verifiable inventory of High Director documentation, canonical fact locations, evidence status, duplication, and source gaps.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
order: 16
---

# High Director Repository Documentation Inventory

## Purpose

This page records what `eirepolitic.github.io` can and cannot currently prove about the High Director agent. It is the canonical repository-only inventory for the High Director documentation initiative.

This inventory does not treat conversation history or inferred behavior as implementation evidence.

## Repository-verifiable High Director pages

| File | Current role | Evidence status | Canonical use |
|---|---|---|---|
| `_docs/high-director/overview.md` | High-level entry point for the agent documentation | Mixed; repository scope is verifiable, runtime implementation remains largely unverified | Agent documentation entry point only |
| `_docs/high-director/site-architecture.md` | Architecture of the documentation site | Verified implementation for the documentation site | Documentation-site architecture |
| `_docs/high-director/site-rebuild-plan.md` | Completed rebuild history and planning record | Historical behavior / completed work | Historical site-rebuild record |
| `_docs/high-director/documentation-section-template-plan.md` | Completed documentation-template initiative | Historical behavior / verification record | Template initiative history |
| `_docs/high-director/example-documents-plan.md` | Completed real-example documentation phase | Historical behavior / verification record | Example-document initiative history |
| `_docs/high-director/high-director-documentation-initiative-plan.md` | Persistent plan for documenting the High Director agent | Planned work plus verified initiative progress | Initiative plan and next-action source of truth |
| `_docs/high-director/repository-documentation-inventory.md` | Repository-only evidence inventory | Verified repository inspection | Canonical inventory of repository-verifiable High Director documentation |
| `_docs/high-director/capability-component-inventory.md` | Evidence-classified capability/component inventory | Repository + observable runtime evidence | Canonical capability/component and missing-source register |

## Supporting canonical documentation outside the High Director section

The following files describe the documentation platform and publishing process. They support High Director documentation work but do not prove the High Director agent runtime implementation.

| File | Canonical subject |
|---|---|
| `DOCUMENTATION_STANDARD.md` | Repository-wide documentation rules and required metadata |
| `_templates/high-director-template.md` | High Director document structure and evidence discipline |
| `_docs/systems/documentation-site.md` | Current documentation-site system record |
| `_docs/repositories/eirepolitic-github-io.md` | Documentation repository implementation record |
| `_docs/runbooks/documentation-site-operations.md` | Documentation-site operations |
| `_docs/runbooks/publish-documentation-change.md` | Documentation publishing procedure |
| `_docs/decisions/use-metadata-driven-static-documentation.md` | Architecture decision for the documentation platform |
| `_docs/notes/documentation-validation-findings.md` | Validation findings and known documentation-quality observations |
| `.github/workflows/validate-documentation.yml` | Documentation validation workflow definition |
| `_config.yml` | Jekyll collection, permalink, plugin, and site configuration |
| `_data/docs_sections.yml` | Documentation navigation section definitions |
| `docs/high-director.md` | High Director section landing route |

## Facts directly verified from this repository

The repository directly verifies that:

- the High Director has a dedicated documentation section and landing page;
- the documentation platform is a Jekyll/GitHub Pages knowledge base;
- documentation navigation is metadata-driven;
- the repository contains a validation workflow for documentation changes;
- the repository has established templates, example documents, publishing runbooks, and architecture records;
- prior documentation initiatives recorded successful validation and Pages deployment evidence;
- the current High Director documentation initiative has a persistent build plan.

These facts describe the documentation system and documentation process. They do not by themselves establish the High Director runtime architecture.

## Runtime claims not verified by this repository

The repository does not currently provide authoritative implementation evidence for:

- the complete High Director system prompt or instruction set;
- the complete capability catalogue;
- Python execution capabilities or implementation details;
- Power BI, Power Automate, Appsmith, or AWS integration behavior;
- custom ChatGPT Actions;
- OpenAPI action schemas;
- API Gateway routes;
- AWS Lambda functions or source code;
- IAM roles, policies, or trust relationships;
- authentication and authorization mechanisms;
- external API connections;
- runtime request/response data flows;
- external supporting repositories;
- production environment variables or configuration objects;
- external deployment procedures;
- runtime failure modes and recovery behavior.

Until authoritative sources are inspected, these subjects must be documented as **unknown / unverified**, not as verified implementation.

## Duplicate and overlapping material

No material duplicate source of truth was found among the current High Director pages, but several pages intentionally overlap at a high level:

- `overview.md` links the section together and should remain concise.
- `site-architecture.md` is authoritative only for documentation-site architecture.
- completed initiative plans are historical records and should not be reused as current runtime documentation.
- the active initiative plan owns project status, phases, outstanding work, and next safe action.
- this inventory owns repository-verifiable evidence classification and canonical file mapping.
- `capability-component-inventory.md` owns capability/component classification and the prioritized missing-source register.

Future pages should link to these sources rather than restating their details.

## Current canonical-source map

| Subject | Canonical source |
|---|---|
| High Director documentation entry point | `_docs/high-director/overview.md` |
| Documentation-site architecture | `_docs/high-director/site-architecture.md` |
| Documentation standard | `DOCUMENTATION_STANDARD.md` |
| High Director page structure | `_templates/high-director-template.md` |
| Documentation repository | `_docs/repositories/eirepolitic-github-io.md` |
| Documentation publishing | `_docs/runbooks/publish-documentation-change.md` |
| Initiative status and next action | `_docs/high-director/high-director-documentation-initiative-plan.md` |
| Repository-only High Director evidence inventory | `_docs/high-director/repository-documentation-inventory.md` |
| Capability/component inventory and missing-source register | `_docs/high-director/capability-component-inventory.md` |
| High Director runtime implementation | Not yet established |
| High Director action schema | Not yet established |
| High Director AWS implementation | Not yet established |
| High Director authentication model | Not yet established |

## Missing-source boundary

Repository inspection is sufficient for the documentation platform, its workflow, and its historical documentation initiatives. It is insufficient for the High Director runtime implementation.

The prioritized external-source dependency register is maintained in `_docs/high-director/capability-component-inventory.md`. Current initiative status and the next safe development action are maintained only in `_docs/high-director/high-director-documentation-initiative-plan.md`.

## Verification record

Verified on 2026-08-06 by direct inspection of the repository tree, High Director documents, documentation templates, repository standard, Jekyll configuration, section metadata, validation workflow, supporting system/repository/runbook records, completed initiative records, and Phase 2 capability/component evidence classification.
