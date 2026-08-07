---
title: High Director Capability and Component Inventory
summary: Evidence-classified inventory of High Director capabilities, components, verification status, and prioritized missing authoritative sources.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
order: 17
---

# High Director Capability and Component Inventory

## Purpose

This page is the canonical capability/component inventory for the High Director documentation initiative. It separates authoritative GPT configuration, Action contracts, Lambda implementation, live AWS configuration, observed runtime behavior, and remaining unknowns.

## Capability inventory

| Capability | Evidence status | Evidence | Current boundary |
|---|---|---|---|
| Data-pipeline/infrastructure design and troubleshooting assistance | User-supplied authoritative GPT instructions | GPT Instructions supplied 2026-08-06 | Instructional purpose verified; execution depends on configured tools |
| Python, GitHub, YAML, Appsmith, Power BI, Power Automate, and AWS assistance | User-supplied authoritative GPT instructions | GPT Instructions | Intended assistance areas; not all are direct integrations |
| GitHub repository/file/branch/PR/workflow/variable/secret operations | User-supplied Action schema + Lambda source | Current GPT schema v0.2.1 and `src/app.py` v0.3.0 | GPT exposes 28 operations; Lambda implements a broader 31-route surface |
| GitHub Action API-key authentication | User-supplied Action schema + Lambda source + live AWS config | `X-API-Key` matched against live `APP_API_KEY` environment-variable key | Key value/storage/rotation unknown |
| Single-owner GitHub scoping | User-supplied GPT instructions + Lambda source + live AWS config | `GITHUB_OWNER` backend env var present; slash-containing repo names rejected | Current owner value intentionally unpublished |
| GitHub REST authentication | User-supplied Lambda source + live AWS config | `GITHUB_TOKEN` environment-variable key present; code sends Bearer token | Actual PAT permissions/rotation unknown |
| Public Lambda Function URL transport | User-supplied live AWS config | `Auth type: NONE`, `BUFFERED`, CORS not enabled | App-level API key remains the effective request gate |
| Gmail profile/search/read/attachment/send operations | User-supplied Google Workspace Action schema | Five Gmail operation IDs; OAuth selected | OAuth scopes/endpoints and token lifecycle unverified |
| Google Calendar list/read/create/update/delete/move operations | User-supplied Google Workspace Action schema | Seven Calendar operation IDs; OAuth selected | OAuth scopes/endpoints and token lifecycle unverified |
| Inspect/update `eirepolitic.github.io` and manage PRs/workflows | Observable runtime evidence | Successfully exercised during initiative | Backend credential values remain private |
| Verify GitHub Pages deployment | Observable runtime evidence | Pages deployments #136–#146 succeeded | GitHub Pages internals external |

## Component inventory

| Component | Status | What is verified | What remains unknown |
|---|---|---|---|
| High Director GPT configuration | User-supplied authoritative source | Name, description, complete Instructions, conversation starters, recommended model, visible Knowledge state, 2 visible Actions | Capability toggles; hidden platform configuration |
| `eirepolitic.github.io` documentation repository | Verified implementation | Structure, Jekyll config, documentation, templates, validator workflow | No material documentation-site gap identified |
| GitHub GPT Wrapper Action contract | User-supplied authoritative source | OpenAPI 3.1.0, current API version 0.2.1, 28 operation IDs/routes, request/response schemas, API-key auth, Lambda Function URL server | Current Action schema does not expose all Lambda routes |
| GitHub wrapper Lambda application | User-supplied authoritative source package | FastAPI/Mangum `src/app.py` v0.3.0, 31 routes, GitHub REST calls, error handling, secret encryption | Physical Lambda name; monitoring/alarms |
| GitHub wrapper live Lambda runtime | User-supplied authoritative live AWS config | Python 3.13, handler `src.app.handler`, architecture `x86_64`, runtime updates `Auto` | Live memory/timeout not yet supplied |
| GitHub wrapper Function URL | User-supplied authoritative live AWS config | Public URL, AWS auth `NONE`, invoke mode `BUFFERED`, CORS not enabled | Resource-policy details |
| GitHub wrapper environment contract | Source + live AWS config | Live keys `APP_API_KEY`, `BRANCH_PREFIX`, `DEFAULT_BASE_BRANCH`, `GITHUB_OWNER`, `GITHUB_TOKEN` | Values intentionally unpublished; optional defaults not visible live |
| GitHub wrapper execution role | User-supplied authoritative live IAM config | Role name `github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo`; visible attached `AWSLambdaBasicExecutionRole`; trust principal `lambda.amazonaws.com` | Whether additional/inline policies exist beyond supplied view; full managed-policy JSON not supplied |
| GitHub backend credential model | User-supplied authoritative source package | `GITHUB_TOKEN` used as Bearer token; template/README describe fine-grained GitHub PAT | Actual granted permissions, token storage/rotation |
| Google Workspace Action | User-supplied authoritative Action configuration/schema | OpenAPI 3.1.0, `Google Workspace API` v1.2.0, OAuth selected, 12 Gmail/Calendar operations, public Google API servers | OAuth scopes, authorization/token URLs, client/token lifecycle configuration |
| Documentation validation workflow | Verified implementation | `.github/workflows/validate-documentation.yml` and successful runs | GitHub-hosted runner internals |
| GitHub Pages publication path | Verified operational behavior | Successful builds/deployments after merged PRs | GitHub-hosted platform internals |
| API Gateway integration | Not established | GitHub Action and SAM/live configuration use Lambda Function URL directly | Whether used by any other High Director component |

## Verified implementation drift

- Lambda application: `0.3.0`.
- Current GPT Action schema: `0.2.1`.
- Bundled package OpenAPI: `0.2.0` and malformed as packaged.
- Lambda exposes `/health`, branch deletion, and artifact metadata beyond the current GPT Action surface.
- README says PR merge is unsupported, but Lambda v0.3.0 implements merge.
- README says direct writes to the default branch should not occur, but apply endpoints do not technically enforce that restriction.

The current GPT schema remains the canonical callable GitHub Action contract; Lambda source remains canonical for backend implementation.

## Prioritized missing-source register

| Priority | Authoritative source | Status / reason |
|---:|---|---|
| 1 | High Director GPT configuration and instructions | **Supplied and documented** |
| 2 | Private Lambda-backed GitHub Action OpenAPI schema | **Supplied and documented** |
| 3 | GitHub wrapper Lambda source/deployment package | **Supplied and documented** |
| 4 | Live Lambda/IAM configuration | **Supplied and documented** |
| 5 | Google Workspace Action OpenAPI schema | **Supplied and documented** |
| 6 | Google Workspace OAuth configuration details | **Next source** — required to verify scopes plus authorization/token endpoints without requesting credentials |
| 7 | Additional external repository source/list | Required only if implementation references external repositories |
| 8 | Non-secret operational configuration/monitoring metadata | Required for deployment/runbook/troubleshooting completion where evidence shows it is used |

## Known limitations

- Capability toggles were not visible in the supplied GPT screenshots.
- Live Lambda memory and timeout remain unverified from the console, though the SAM template declares 512 MB and 30 seconds.
- API-key and GitHub-token values are intentionally not requested/published.
- Actual fine-grained PAT permissions are unverified.
- Google OAuth scopes and authorization/token endpoint configuration remain unverified.
- The supplied IAM view verifies one managed policy but does not prove the absence of additional/inline policies.

## Verification record

Verified on 2026-08-06 using repository evidence, successful GitHub integration operations, authoritative GPT configuration, GitHub Action schema, GitHub wrapper Lambda package/live AWS configuration, and the user-supplied Google Workspace Action schema with OAuth authentication selection.

## Initiative status

Current phase status and the next safe development action are maintained only in `_docs/high-director/high-director-documentation-initiative-plan.md`.
