---
title: High Director Capability and Component Inventory
summary: Evidence-classified inventory of High Director capabilities, components, verification status, and remaining known limitations.
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

This page is the canonical capability/component inventory for High Director. It separates authoritative GPT configuration, Action contracts, Lambda implementation, live AWS configuration, observed runtime behavior, and remaining known limitations.

## Capability inventory

| Capability | Evidence status | Evidence | Current boundary |
|---|---|---|---|
| Data-pipeline/infrastructure design and troubleshooting assistance | User-supplied authoritative GPT instructions | GPT Instructions supplied 2026-08-06 | Instructional purpose verified; execution depends on configured tools |
| Python, GitHub, YAML, Appsmith, Power BI, Power Automate, and AWS assistance | User-supplied authoritative GPT instructions | GPT Instructions | Intended assistance areas; not all are direct integrations |
| GitHub repository/file/branch/PR/workflow/variable/secret operations | User-supplied Action schema + Lambda source | Current GPT schema v0.2.1 and `src/app.py` v0.3.0 | GPT exposes 28 operations; Lambda implements a broader 31-route surface |
| GitHub Action API-key authentication | User-supplied Action schema + Lambda source + live AWS config | `X-API-Key` matched against live `APP_API_KEY` environment-variable key | Key value/storage/rotation intentionally unpublished/unverified |
| Single-owner GitHub scoping | User-supplied GPT instructions + Lambda source + live AWS config | `GITHUB_OWNER` backend env var present; slash-containing repo names rejected | Current owner value intentionally unpublished |
| GitHub REST authentication | User-supplied Lambda source + live AWS config | `GITHUB_TOKEN` environment-variable key present; code sends Bearer token | Actual PAT permissions/rotation unverified |
| Public Lambda Function URL transport | User-supplied live AWS config | `Auth type: NONE`, `BUFFERED`, CORS not enabled | App-level API key remains the effective request gate |
| Gmail profile/search/read/attachment/send operations | User-supplied Google Workspace Action + OAuth config | Five Gmail operations; scopes `gmail.readonly` and `gmail.send` | Token storage/refresh and connected account identity unverified |
| Google Calendar list/read/create/update/delete/move operations | User-supplied Google Workspace Action + OAuth config | Seven Calendar operations; scopes `calendar.events` and `calendar.calendarlist.readonly` | Token storage/refresh and connected account identity unverified |
| Inspect/update `eirepolitic.github.io` and manage PRs/workflows | Observable runtime evidence | Successfully exercised throughout initiative | Backend credential values remain private |
| Verify GitHub Pages deployments | Observable runtime evidence | Successful initiative Pages deployments through #157 before final consistency review | GitHub Pages platform internals external |
| Maintain/troubleshoot/handoff High Director documentation | Verified documentation implementation | Canonical runbooks, plan, validator, source inventory, verification records | Some external recovery/monitoring procedures remain explicitly unverified |

## Component inventory

| Component | Status | What is verified | What remains unknown |
|---|---|---|---|
| High Director GPT configuration | User-supplied authoritative source | Name, description, complete Instructions, conversation starters, recommended model, visible Knowledge state, 2 configured Actions | Capability toggles; hidden platform configuration |
| `eirepolitic.github.io` documentation repository | Verified implementation | Structure, Jekyll config, documentation, templates, validator workflow, source snapshots | No material documentation-site gap identified |
| GitHub GPT Wrapper Action contract | User-supplied authoritative source | OpenAPI 3.1.0, current API version 0.2.1, 28 operation IDs/routes, request/response schemas, API-key auth, Lambda Function URL server | Current Action schema does not expose all Lambda routes |
| GitHub wrapper Lambda application | User-supplied authoritative source package | FastAPI/Mangum `src/app.py` v0.3.0, 31 routes, GitHub REST calls, error handling, secret encryption | Monitoring/rollback automation; physical function-name confirmation |
| GitHub wrapper live Lambda runtime | User-supplied authoritative live AWS config | Python 3.13, handler `src.app.handler`, architecture `x86_64`, runtime updates `Auto` | Live memory/timeout not separately supplied |
| GitHub wrapper Function URL | User-supplied authoritative live AWS config | Public URL, AWS auth `NONE`, invoke mode `BUFFERED`, CORS not enabled | Resource-policy details, perimeter/monitoring controls |
| GitHub wrapper environment contract | Source + live AWS config | Live keys `APP_API_KEY`, `BRANCH_PREFIX`, `DEFAULT_BASE_BRANCH`, `GITHUB_OWNER`, `GITHUB_TOKEN` | Values intentionally unpublished; rotation/lifecycle procedures |
| GitHub wrapper execution role | User-supplied authoritative live IAM config | Role name `github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo`; visible attached `AWSLambdaBasicExecutionRole`; trust principal `lambda.amazonaws.com` | Complete attached/inline policy inventory beyond supplied view |
| GitHub backend credential model | User-supplied authoritative source package | `GITHUB_TOKEN` used as Bearer token; template/README describe fine-grained GitHub PAT | Actual granted permissions, token storage/rotation |
| Google Workspace Action | User-supplied authoritative Action/OAuth config | OpenAPI 3.1.0, `Google Workspace API` v1.2.0, OAuth, 12 Gmail/Calendar operations, Google auth/token endpoints, four explicit scopes | Client identity, token lifecycle, connected account, consent/admin configuration |
| Runtime architecture/data flows | Verified consolidated documentation | Trust paths, GitHub/AWS/Google flows, secret flow, documentation-control flow | Platform-internal behavior not exposed by authoritative sources |
| Operations/troubleshooting/handoff | Verified documentation derived from authoritative implementation + exercised docs workflow | Normal maintenance, source-derived deploy procedure, failure triage, evidence capture, continuation | Credential rotation, automated rollback, OAuth reconnect/revocation, monitoring controls not fully verified |
| Documentation validation workflow | Verified implementation | `.github/workflows/validate-documentation.yml` and successful runs | GitHub-hosted runner internals |
| GitHub Pages publication path | Verified operational behavior | Repeated successful builds/deployments after merged PRs | GitHub-hosted platform internals |
| API Gateway integration | Not established | GitHub Action and SAM/live configuration use Lambda Function URL directly | Whether a future/other High Director component uses API Gateway |

## Verified Google OAuth boundary

Authorization URL:

```text
https://accounts.google.com/o/oauth2/v2/auth
```

Token URL:

```text
https://oauth2.googleapis.com/token
```

Token exchange method: default POST request.

Configured scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

## Verified implementation drift

- Lambda application: `0.3.0`.
- Current GPT GitHub Action schema: `0.2.1`.
- Bundled package OpenAPI: `0.2.0` and malformed as packaged.
- Lambda exposes `/health`, branch deletion, and artifact metadata beyond the current GPT Action surface.
- README says PR merge is unsupported, but Lambda v0.3.0 implements merge.
- README says direct writes to the default branch should not occur, but apply endpoints do not technically enforce that restriction.

The current GPT schema remains the canonical callable GitHub Action contract; Lambda source remains canonical for backend behavior.

## Source register

| Authoritative source | Status |
|---|---|
| High Director GPT configuration and instructions | **Supplied and documented** |
| Private Lambda-backed GitHub Action OpenAPI schema | **Supplied and documented** |
| GitHub wrapper Lambda source/deployment package | **Supplied and documented** |
| Live Lambda/IAM configuration | **Supplied and documented** |
| Google Workspace Action OpenAPI schema | **Supplied and documented** |
| Google Workspace OAuth endpoints/scopes | **Supplied and documented** |

There is **no currently required external source** blocking completion of this documentation initiative. Additional source should be requested only when a concrete future task is blocked by an unresolved evidence gap.

## Known limitations

- GPT Builder capability toggles were not visible in the supplied screenshots.
- Live Lambda memory and timeout remain unverified from the console, though the SAM template declares 512 MB and 30 seconds.
- API-key, GitHub-token, OAuth Client ID/Secret, and OAuth token values are intentionally not requested/published.
- API-key and GitHub PAT rotation procedures are not verified.
- Actual fine-grained GitHub PAT permissions are unverified.
- Complete execution-role policy inventory is not proven beyond supplied visible IAM evidence.
- Function URL resource-policy, CloudWatch retention/alarms, WAF/rate limiting, retry/dead-letter, and other monitoring/perimeter controls are unverified.
- Google OAuth token storage/refresh behavior, connected-account identity, reconnect/revocation, and consent/admin configuration are unverified.

## Verification record

Reviewed on 2026-08-06 using repository evidence, successful GitHub integration operations, authoritative GPT configuration, GitHub Action schema, GitHub wrapper Lambda package/live AWS configuration, Google Workspace Action/OAuth configuration, runtime/security/code documentation, and initiative workflow history through Phase 9.

## Initiative status

Current phase status and the next safe development action are maintained only in `_docs/high-director/high-director-documentation-initiative-plan.md`.
