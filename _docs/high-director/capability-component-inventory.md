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

This page is the canonical capability/component inventory for the High Director documentation initiative. It separates authoritative GPT configuration, Action contracts, Lambda implementation, observed runtime behavior, and remaining unknowns.

## Capability inventory

| Capability | Evidence status | Evidence | Current boundary |
|---|---|---|---|
| Data-pipeline/infrastructure design and troubleshooting assistance | User-supplied authoritative GPT instructions | GPT Instructions supplied 2026-08-06 | Instructional purpose verified; execution depends on configured tools |
| Python, GitHub, YAML, Appsmith, Power BI, Power Automate, and AWS assistance | User-supplied authoritative GPT instructions | GPT Instructions | Intended assistance areas; not all are direct integrations |
| GitHub repository/file/branch/PR/workflow/variable/secret operations | User-supplied Action schema + Lambda source | Current GPT schema v0.2.1 and `src/app.py` v0.3.0 | GPT exposes 28 operations; Lambda implements a broader 31-route surface |
| GitHub Action API-key authentication | User-supplied Action schema + Lambda source | `X-API-Key` matched against `APP_API_KEY` | Key value/storage/rotation unknown |
| Single-owner GitHub scoping | User-supplied GPT instructions + Lambda source | `GITHUB_OWNER` backend env var; slash-containing repo names rejected | Current owner value intentionally unpublished |
| GitHub REST authentication | User-supplied Lambda source | `Authorization: Bearer <GITHUB_TOKEN>` | Actual PAT permissions/rotation unknown |
| Inspect/update `eirepolitic.github.io` and manage PRs/workflows | Observable runtime evidence | Successfully exercised during initiative | Backend credential values remain private |
| Verify GitHub Pages deployment | Observable runtime evidence | Pages deployments #136–#142 succeeded | GitHub Pages internals external |

## Component inventory

| Component | Status | What is verified | What remains unknown |
|---|---|---|---|
| High Director GPT configuration | User-supplied authoritative source | Name, description, complete Instructions, conversation starters, recommended model, visible Knowledge state, 2 visible Actions | Capability toggles; hidden platform configuration |
| `eirepolitic.github.io` documentation repository | Verified implementation | Structure, Jekyll config, documentation, templates, validator workflow | No material documentation-site gap identified |
| GitHub GPT Wrapper Action contract | User-supplied authoritative source | OpenAPI 3.1.0, current API version 0.2.1, 28 operation IDs/routes, request/response schemas, API-key auth, Lambda Function URL server | Current Action schema does not expose all Lambda routes |
| GitHub wrapper Lambda application | User-supplied authoritative source package | FastAPI/Mangum `src/app.py` v0.3.0, 31 routes, GitHub REST calls, error handling, secret encryption | Physical Lambda name; live runtime settings; monitoring |
| GitHub wrapper SAM deployment | User-supplied authoritative source package | `python3.13`, handler `src.app.handler`, 512 MB, 30 s, Function URL `AuthType: NONE`, region `us-east-2` in SAM config | Deployed-console confirmation; execution-role policy |
| GitHub backend credential model | User-supplied authoritative source package | `GITHUB_TOKEN` used as Bearer token; template/README describe fine-grained GitHub PAT | Actual granted permissions, token storage/rotation |
| `www.googleapis.com` Action | User-supplied authoritative existence evidence | One configured Action visibly targets `www.googleapis.com` | Exact schema/API product/operations/authentication/data flow |
| Documentation validation workflow | Verified implementation | `.github/workflows/validate-documentation.yml` and successful runs | GitHub-hosted runner internals |
| GitHub Pages publication path | Verified operational behavior | Successful builds/deployments after merged PRs | GitHub-hosted platform internals |
| API Gateway integration | Not established | GitHub Action and SAM template use Lambda Function URL directly | Whether used by any other High Director component |
| IAM configuration | Unknown / unverified | SAM deployment declares `CAPABILITY_IAM`; Lambda execution-role policy not supplied | Execution role, permissions, trust policy |

## Verified implementation drift

- Lambda application: `0.3.0`.
- Current GPT Action schema: `0.2.1`.
- Bundled package OpenAPI: `0.2.0` and malformed as packaged.
- Lambda exposes `/health`, branch deletion, and artifact metadata beyond the current GPT Action surface.
- README says PR merge is unsupported, but Lambda v0.3.0 implements merge.
- README says direct writes to the default branch should not occur, but apply endpoints do not technically enforce that restriction.

The current GPT schema remains the canonical callable Action contract; Lambda source remains canonical for backend implementation.

## Prioritized missing-source register

| Priority | Authoritative source | Status / reason |
|---:|---|---|
| 1 | High Director GPT configuration and instructions | **Supplied and documented** |
| 2 | Private Lambda-backed GitHub Action OpenAPI schema | **Supplied and documented** |
| 3 | GitHub wrapper Lambda source/deployment package | **Supplied and documented** |
| 4 | AWS Lambda IAM/execution-role and live function configuration | **Next source** — required to verify deployed security boundary, role permissions, Function URL configuration, runtime/handler, and environment-variable names without values |
| 5 | `www.googleapis.com` Action OpenAPI schema | Required to identify exact Google operations/authentication/data flow |
| 6 | Additional external repository source/list | Required only if implementation references external repositories |
| 7 | Non-secret operational configuration/monitoring metadata | Required for deployment/runbook/troubleshooting completion |

## Known limitations

- Capability toggles were not visible in the supplied GPT screenshots.
- Live AWS console configuration has not yet been compared with the SAM template.
- API-key and GitHub-token values are intentionally not requested/published.
- Actual fine-grained PAT permissions are unverified.
- The public Google Action remains identified only by hostname.

## Verification record

Verified on 2026-08-06 using repository evidence, successful GitHub integration operations, authoritative GPT configuration, current Action schema, and the user-supplied GitHub wrapper Lambda source/deployment package.

## Initiative status

Current phase status and the next safe development action are maintained only in `_docs/high-director/high-director-documentation-initiative-plan.md`.
