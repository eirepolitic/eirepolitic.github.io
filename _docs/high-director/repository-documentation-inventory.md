---
title: High Director Repository Documentation Inventory
summary: Current inventory of canonical High Director documentation, supporting runbooks/source assets, archived initiative records, and unresolved evidence gaps.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-07
last_verified: 2026-08-07
order: 16
---

# High Director Repository Documentation Inventory

## Purpose

This page is the canonical map of documentation whose primary subject is the High Director agent. It distinguishes current High Director implementation/reference pages from supporting runbooks, documentation-site material, archived project records, and remaining unknowns.

Conversation history is not a source of truth when the relevant material has been persisted here.

## Current High Director canonical pages

The active High Director website section contains **14 pages**:

| File | Canonical subject | Evidence basis |
|---|---|---|
| `_docs/high-director/overview.md` | High-level entry point and current verified scope | Links current canonical sources |
| `_docs/high-director/gpt-configuration.md` | GPT identity, user-authored instructions, conversation starters, recommended model, visible Knowledge/Action state | User-supplied authoritative GPT Builder source |
| `_docs/high-director/capability-component-inventory.md` | Capability/component inventory, boundaries, limitations, conditional source gaps | Authoritative sources + observed runtime evidence |
| `_docs/high-director/github-integration.md` | GitHub Action behavior, repository rule, authentication boundary, docs workflow behavior | Action schema + Lambda source + observed operations |
| `_docs/high-director/github-action-openapi-schema.md` | Current GitHub GPT Action OpenAPI contract | User-supplied authoritative Action schema |
| `_docs/high-director/github-wrapper-lambda.md` | GitHub wrapper Lambda application/deployment implementation | User-supplied authoritative source package |
| `_docs/high-director/github-wrapper-live-aws-configuration.md` | Live Lambda runtime, Function URL, environment-key, execution-role/IAM evidence | User-supplied authoritative live AWS/IAM source |
| `_docs/high-director/google-workspace-action.md` | Google Workspace Action contract and OAuth boundary | User-supplied authoritative Action/OAuth configuration |
| `_docs/high-director/runtime-architecture.md` | Verified runtime architecture and trust boundaries | Consolidated authoritative implementation/configuration evidence |
| `_docs/high-director/data-flows.md` | GitHub, AWS, Google Workspace, secret, failure, and documentation-control flows | Consolidated authoritative evidence |
| `_docs/high-director/security-configuration-reference.md` | Authentication, authorization, IAM, OAuth, secrets, configuration, security limitations | Consolidated authoritative/live evidence |
| `_docs/high-director/code-and-dependency-reference.md` | Source files, classes/functions/routes, dependencies, source assets, hashes, rebuild boundaries | Authoritative Lambda package + repository source assets |
| `_docs/high-director/repository-documentation-inventory.md` | Canonical documentation/source map | Current repository documentation state |
| `_docs/high-director/verification-record.md` | Provenance, sanitization, PR/Pages verification, and known verification boundaries | Repository and workflow evidence |

These are the only pages intended to appear in the active High Director section. A file's physical directory is not itself the navigation classification; front-matter `section` is authoritative for section placement.

## Supporting current documentation outside High Director

| File | Section | Canonical subject |
|---|---|---|
| `_docs/runbooks/high-director-operations-and-deployment.md` | Runbooks | Normal operation, maintenance, deployment/update procedure, validation and rollback boundaries |
| `_docs/runbooks/high-director-troubleshooting-and-handoff.md` | Runbooks | Failure diagnosis, evidence capture, safe recovery boundaries, handoff and continuation |
| `_docs/systems/documentation-site.md` | Systems | Current documentation-site architecture, rendering, search, validation, deployment and change-management model |
| `_docs/repositories/eirepolitic-github-io.md` | Repositories | Documentation repository implementation |
| `_docs/decisions/use-metadata-driven-static-documentation.md` | Architecture Decisions | Documentation architecture decision |
| `DOCUMENTATION_STANDARD.md` | Repository standard | Documentation metadata/classification/content rules |
| `_templates/high-director-template.md` | Template | High Director-specific page structure and evidence discipline |

## Archived records still physically under `_docs/high-director/`

The following files intentionally remain at their historical filesystem paths for relative-link/default-URL compatibility, but their front matter is `section: archive` and they are **not** active High Director navigation entries:

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

`site-architecture.md` is specifically superseded by `_docs/systems/documentation-site.md` for current documentation-site architecture.

## Active coordination moved to Notes

These records were physically moved to `_docs/notes/` because they remain active coordination/reference material but are not about High Director itself:

- `_docs/notes/autodoc-documentation-workstream-plan.md`
- `_docs/notes/documentation-target-catalogue.md`
- `_docs/notes/repository-scan-autodoc.md`
- `_docs/notes/high-director-section-cleanup-plan.md`

Their established public permalinks were preserved where needed so existing links remain stable.

## Sanitized supporting source assets

The repository contains sanitized first-party source/configuration material derived from the authoritative GitHub wrapper deployment package:

```text
assets/high-director/github-wrapper-source/README.md
assets/high-director/github-wrapper-source/openapi.yaml
assets/high-director/github-wrapper-source/requirements.txt
assets/high-director/github-wrapper-source/samconfig.toml
assets/high-director/github-wrapper-source/template.yaml
assets/high-director/github-wrapper-source/src/app.py.part01
assets/high-director/github-wrapper-source/src/app.py.part02
assets/high-director/github-wrapper-source/src/app.py.part03
assets/high-director/github-wrapper-source/src/app.py.part04
```

Sanitization and source hashes are canonicalized in `_docs/high-director/code-and-dependency-reference.md` and `_docs/high-director/github-wrapper-lambda.md`.

## Evidence now established

The documentation repository contains authoritative or verified records for:

- High Director purpose, responsibilities, behavioral rules, and operating model encoded in the user-authored GPT instructions;
- configured GitHub and Google Workspace Action contracts;
- GitHub Action API-key authentication declaration;
- Google OAuth endpoints, token exchange method, and configured scopes;
- GitHub wrapper Lambda source, dependencies, routes, failure handling, deployment template, and environment-variable contract;
- live Lambda runtime/handler/architecture/Function URL settings and supplied IAM evidence;
- GitHub and Google Workspace data flows/trust boundaries;
- secret-handling behavior;
- code/dependency references and persistent sanitized source assets;
- operating/deployment and troubleshooting/recovery/handoff procedures;
- documentation validation and Pages publication workflow.

Where external implementation/configuration was supplied by the system owner, the sanitized persisted copy/documentation is explicitly classified as **user-supplied authoritative source**.

## Current unresolved evidence gaps

No external source is currently required to maintain the existing High Director documentation set. Remaining limitations are explicit known unknowns/private boundaries, including:

- GPT Builder capability-toggle state;
- secret/credential values and rotation procedures;
- exact GitHub PAT permission grants;
- complete execution-role policy inventory beyond supplied visible IAM evidence;
- live Lambda memory/timeout confirmation;
- Function URL resource-policy and monitoring/alerting details;
- Google OAuth token storage/refresh, connected-account identity, reconnect/revocation, and consent/admin configuration;
- monitoring/perimeter controls not verified by authoritative source.

Request new external evidence only when a concrete maintenance/troubleshooting task is blocked by one of these gaps.

## Canonical-source map

| Subject | Canonical source |
|---|---|
| High Director entry point | `_docs/high-director/overview.md` |
| GPT configuration/instructions | `_docs/high-director/gpt-configuration.md` |
| Capability/component inventory | `_docs/high-director/capability-component-inventory.md` |
| GitHub integration | `_docs/high-director/github-integration.md` |
| GitHub Action schema | `_docs/high-director/github-action-openapi-schema.md` |
| GitHub wrapper backend | `_docs/high-director/github-wrapper-lambda.md` |
| Live AWS/IAM configuration | `_docs/high-director/github-wrapper-live-aws-configuration.md` |
| Google Workspace Action/OAuth | `_docs/high-director/google-workspace-action.md` |
| Runtime architecture | `_docs/high-director/runtime-architecture.md` |
| Data flows | `_docs/high-director/data-flows.md` |
| Security/configuration | `_docs/high-director/security-configuration-reference.md` |
| Code/dependencies/source assets | `_docs/high-director/code-and-dependency-reference.md` |
| Documentation/source inventory | `_docs/high-director/repository-documentation-inventory.md` |
| Verification/provenance | `_docs/high-director/verification-record.md` |
| Operations/deployment | `_docs/runbooks/high-director-operations-and-deployment.md` |
| Troubleshooting/handoff | `_docs/runbooks/high-director-troubleshooting-and-handoff.md` |
| Documentation-site architecture | `_docs/systems/documentation-site.md` |
| Historical High Director documentation-build ledger | `_docs/high-director/high-director-documentation-initiative-plan.md` (`section: archive`) |

## Duplication rule

Overview and inventory pages may summarize a subject only enough to navigate. Exact configuration, schemas, code behavior, security controls, data flows, procedures, and verification state belong to their canonical subject pages above.

Project/workstream plans, repository scans, or other records do not become High Director documentation merely because High Director created or coordinated them.

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current deployed documentation tree after the High Director section cleanup; canonical High Director pages; supporting runbooks; Systems documentation-site page; Notes coordination records; archived completion/discovery records.
- Verified by: High Director
- Verification scope: active 14-page High Director set, current canonical ownership, archived compatibility records, Notes moves, source assets, and remaining evidence gaps.
