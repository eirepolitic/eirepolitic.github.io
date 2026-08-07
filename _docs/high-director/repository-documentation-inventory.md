---
title: High Director Repository Documentation Inventory
summary: Current inventory of High Director documentation, canonical fact locations, evidence status, historical records, supporting source assets, and unresolved evidence gaps.
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

This page is the canonical map of High Director documentation now persisted in `eirepolitic.github.io`. It distinguishes repository implementation, sanitized user-supplied authoritative sources, observed runtime evidence, historical initiative records, and remaining unknowns.

Conversation history is not a source of truth when the relevant material has been persisted here.

## Current High Director canonical pages

| File | Canonical subject | Evidence basis |
|---|---|---|
| `_docs/high-director/overview.md` | High-level entry point and current verified scope | Links current canonical sources |
| `_docs/high-director/gpt-configuration.md` | GPT identity, full user-authored Instructions, conversation starters, recommended model, visible Knowledge/Action state | User-supplied authoritative GPT Builder source |
| `_docs/high-director/capability-component-inventory.md` | Capability/component inventory, boundaries, limitations, conditional source gaps | Authoritative sources + observed runtime evidence |
| `_docs/high-director/github-integration.md` | GitHub Action behavior, repository rule, authentication boundary, docs workflow behavior | Action schema + Lambda source + observed operations |
| `_docs/high-director/github-action-openapi-schema.md` | Current GitHub GPT Action OpenAPI contract v0.2.1 | User-supplied authoritative Action schema |
| `_docs/high-director/github-wrapper-lambda.md` | GitHub wrapper Lambda application/deployment implementation | User-supplied authoritative source package |
| `_docs/high-director/github-wrapper-live-aws-configuration.md` | Live Lambda runtime, Function URL, environment-key, execution-role/IAM evidence | User-supplied authoritative live AWS/IAM source |
| `_docs/high-director/google-workspace-action.md` | Google Workspace Action contract and OAuth boundary | User-supplied authoritative Action/OAuth configuration |
| `_docs/high-director/runtime-architecture.md` | Verified runtime architecture and trust boundaries | Consolidated authoritative implementation/configuration evidence |
| `_docs/high-director/data-flows.md` | GitHub, AWS, Google Workspace, secret, failure, and documentation-control flows | Consolidated authoritative evidence |
| `_docs/high-director/security-configuration-reference.md` | Authentication, authorization, IAM, OAuth, secrets, configuration, security limitations | Consolidated authoritative/live evidence |
| `_docs/high-director/code-and-dependency-reference.md` | Source files, classes/functions/routes, dependencies, source assets, hashes, rebuild boundaries | Authoritative Lambda package + repository source assets |
| `_docs/high-director/high-director-documentation-initiative-plan.md` | Initiative progress, verification gates, outstanding work, next safe action | Persistent project-state record |
| `_docs/high-director/verification-record.md` | Consolidated initiative provenance, sanitization, PR/Pages verification, and closure evidence | Repository and workflow evidence |
| `_docs/high-director/site-architecture.md` | Documentation-site architecture | Verified documentation-site implementation |

## Canonical runbooks

| File | Canonical subject |
|---|---|
| `_docs/runbooks/high-director-operations-and-deployment.md` | Normal operation, maintenance, deployment/update procedure, validation and rollback boundaries |
| `_docs/runbooks/high-director-troubleshooting-and-handoff.md` | Failure diagnosis, evidence capture, safe recovery boundaries, handoff and continuation |
| `_docs/runbooks/publish-documentation-change.md` | General repository documentation publishing procedure |
| `_docs/runbooks/documentation-site-operations.md` | Documentation-site operations |

## Historical initiative records

These files remain useful as historical/verification records but are not current runtime sources of truth:

| File | Historical role |
|---|---|
| `_docs/high-director/site-rebuild-plan.md` | Completed documentation-site rebuild plan |
| `_docs/high-director/documentation-section-template-plan.md` | Completed documentation-template initiative |
| `_docs/high-director/example-documents-plan.md` | Completed real Example Documents initiative |

## Supporting repository implementation

| File | Canonical subject |
|---|---|
| `DOCUMENTATION_STANDARD.md` | Repository-wide documentation rules/metadata |
| `_templates/high-director-template.md` | High Director document structure/evidence discipline |
| `_docs/systems/documentation-site.md` | Documentation-site system record |
| `_docs/repositories/eirepolitic-github-io.md` | Documentation repository record |
| `_docs/decisions/use-metadata-driven-static-documentation.md` | Documentation architecture decision |
| `.github/workflows/validate-documentation.yml` | Documentation validation workflow |
| `scripts/validate_docs.py` | Documentation validator implementation |
| `_config.yml` | Jekyll collection/permalink/site configuration |
| `_data/docs_sections.yml` | Documentation navigation definitions |
| `docs/high-director.md` | High Director section landing route |

## Sanitized supporting source assets

The repository now contains sanitized first-party source/configuration material derived from the authoritative GitHub wrapper deployment package:

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

The documentation repository now contains authoritative or verified records for:

- High Director purpose, responsibilities, behavioral rules, and operating model encoded in the user-authored GPT instructions;
- configured GitHub and Google Workspace Action contracts;
- GitHub Action API-key authentication declaration;
- Google OAuth endpoints, token exchange method, and four configured scopes;
- GitHub wrapper Lambda source, dependencies, routes, failure handling, deployment template, and environment-variable contract;
- live Lambda runtime/handler/architecture/Function URL settings and supplied IAM evidence;
- GitHub and Google Workspace data flows/trust boundaries;
- secret-handling behavior;
- code/dependency references and persistent sanitized source assets;
- operating/deployment runbook;
- troubleshooting/recovery/handoff runbook;
- documentation validation and Pages publication workflow.

These facts are not all directly derivable from the repository's original implementation. Where external implementation/configuration was supplied by the system owner, the sanitized persisted copy/documentation is explicitly classified as **user-supplied authoritative source**.

## Current unresolved evidence gaps

No external source is currently required to complete the documentation initiative. Remaining limitations are explicit known unknowns/private boundaries, including:

- GPT Builder capability-toggle state;
- secret/credential values and rotation procedures;
- exact GitHub PAT permission grants;
- complete execution-role policy inventory beyond the supplied visible IAM evidence;
- live Lambda memory/timeout confirmation;
- Function URL resource-policy and monitoring/alerting details;
- Google OAuth token storage/refresh, connected-account identity, reconnect/revocation, and consent/admin configuration;
- monitoring/perimeter controls not verified by authoritative source.

Request a new external source only if a concrete future maintenance/troubleshooting task is blocked by one of these gaps.

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
| Operations/deployment | `_docs/runbooks/high-director-operations-and-deployment.md` |
| Troubleshooting/handoff | `_docs/runbooks/high-director-troubleshooting-and-handoff.md` |
| Initiative status/next action | `_docs/high-director/high-director-documentation-initiative-plan.md` |
| Initiative verification/provenance | `_docs/high-director/verification-record.md` |
| Documentation-site architecture | `_docs/high-director/site-architecture.md` |

## Duplication rule

Overview and inventory pages may summarize a subject only enough to navigate. Exact configuration, schemas, code behavior, security controls, data flows, procedures, and project state belong only to their canonical pages above.

## Verification record

Reviewed on 2026-08-06 against the current repository tree, authoritative source-derived pages/assets, runbooks, workflow history, and Phase 10 consistency audit.
