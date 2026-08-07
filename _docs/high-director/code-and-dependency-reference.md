---
title: High Director Code and Dependency Reference
summary: Canonical source-code, file, function, class, dependency, deployment-asset, and rebuild reference for the verified High Director supporting implementation.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 27
permalink: /projects/high-director/code-and-dependency-reference/
---

# High Director Code and Dependency Reference

## Purpose

This page is the canonical code/dependency inventory for the verified High Director supporting implementation. It records exact source files, classes, functions, dependencies, deployment assets, source hashes, and rebuild boundaries without publishing secrets.

## Evidence classification

- **User-supplied authoritative source package:** GitHub wrapper Lambda deployment package supplied 2026-08-06.
- **Verified repository implementation:** High Director documentation repository, validator, workflows, templates, and sanitized source assets.
- **User-supplied authoritative Action configuration:** GitHub and Google Workspace OpenAPI contracts.

## GitHub wrapper source package

Original deployment/source package SHA-256:

```text
07bf8a5dbd5d688e472b6e11f9aa68f6b84b155bf7cd0e265bf5d43524943554
```

Authoritative application source:

```text
src/app.py
SHA-256: 3a6ac1d69c2571c403aa01746c1c2d55df2c266de5ddfc789df2199e4876c5f0
Application version: 0.3.0
```

The application source contained no embedded API-key, GitHub-token, AWS-account, private-Lambda-hostname, or literal GitHub-owner values.

## Persistent sanitized source snapshot

The supplied `src/app.py` is preserved in four repository assets because the GitHub integration writes text files and the source is large:

```text
assets/high-director/github-wrapper-source/src/app.py.part01
assets/high-director/github-wrapper-source/src/app.py.part02
assets/high-director/github-wrapper-source/src/app.py.part03
assets/high-director/github-wrapper-source/src/app.py.part04
```

The parts contain the complete source in original line order. For byte-for-byte source reconstruction, use the original source SHA-256 above as the integrity check. The split boundaries occur after original lines 350, 700, and 1050; blank-line separators at split boundaries are formatting-only and do not alter Python semantics when reconstructed with normal blank-line separation.

Original chunk SHA-256 values before splitting:

| Part | Original line range | SHA-256 |
|---|---:|---|
| part01 | 1–350 | `c1e3ce16069e6ad772a02279dbfe8296316175d6d8f5bdcb37cd73d25b5dc7b3` |
| part02 | 351–700 | `5c428c543a107ff388176cbf1782ae228ea44cd25267c7b39e757fb4daca8abe` |
| part03 | 701–1050 | `4d0305178796d817b70ea2225e95ed3eab4928eb8b33e9fc46c42e8a291796b8` |
| part04 | 1051–1400 | `9ad6291a444f36d8150b2e9c56f148edf3fd92f81180ae405539c265c3eee87a` |

## Other persistent first-party assets

| Repository asset | Original package file | Purpose | Sanitization |
|---|---|---|---|
| `assets/high-director/github-wrapper-source/template.yaml` | `template.yaml` | AWS SAM function/deployment declaration | No secret values present |
| `assets/high-director/github-wrapper-source/samconfig.toml` | `samconfig.toml` | SAM deployment defaults | Literal GitHub owner replaced with `REDACTED_OWNER` |
| `assets/high-director/github-wrapper-source/requirements.txt` | `requirements.txt` | Pinned Python dependencies | No changes |
| `assets/high-director/github-wrapper-source/README.md` | `README.md` | Starter/deployment guidance | No secret values; documented as stale where source differs |
| `assets/high-director/github-wrapper-source/openapi.yaml` | bundled `openapi.yaml` v0.2.0 | Historical/bundled Action contract | Private Lambda URL redacted; indentation normalized because packaged YAML is malformed |

The current callable GitHub GPT Action contract is **not** the bundled v0.2.0 schema. The canonical current Action contract is `_docs/high-director/github-action-openapi-schema.md` (v0.2.1).

## Python application classes

`src/app.py` defines these application-owned classes:

```text
UpsertPreviewRequest
UpsertApplyRequest
DeletePreviewRequest
DeleteApplyRequest
PullRequestCreateRequest
PullRequestMergeRequest
PullRequestUpdateRequest
PullRequestCloseRequest
BranchCreateRequest
DispatchWorkflowRequest
VariableSetRequest
SecretSetRequest
AppError
```

The request classes are Pydantic models. `AppError` carries HTTP-style status/error/message/details fields for normalized API failures.

## Python helper functions

Verified helper functions in `src/app.py`:

```text
success
error_response
require_api_key
normalize_repo_name
sanitize_branch_name
auto_branch_name
gh_headers
gh_client
parse_response_body
gh_request
get_repo
get_default_branch
get_branch_sha
create_branch
delete_branch
ensure_branch_exists
get_file
get_commit_for_ref
get_tree_sha_for_ref
build_diff
put_file
delete_file_from_branch
get_repo_public_key
encrypt_secret
```

Key responsibilities:

- `require_api_key` — compares incoming `X-API-Key` with `APP_API_KEY`.
- `normalize_repo_name` — enforces repository-name-only input and rejects `/`.
- `gh_headers` / `gh_client` / `gh_request` — construct GitHub REST API requests and normalize upstream failures.
- `ensure_branch_exists` — creates a branch when absent.
- `build_diff` — produces unified file diffs for preview operations.
- `encrypt_secret` — uses PyNaCl `SealedBox` with the repository Actions public key.

## Exception handlers

```text
app_error_handler
http_exception_handler
validation_exception_handler
unhandled_exception_handler
```

These normalize application, FastAPI/Pydantic validation, HTTP, and unexpected exceptions to JSON response objects.

## HTTP route functions

The Lambda application defines 31 routes/functions:

```text
health
read_file
list_repo_tree
search_repo_contents
preview_upsert
apply_upsert
preview_delete
apply_delete
list_branches
create_branch_endpoint
delete_branch_endpoint
create_pull_request
list_pull_requests
get_pull_request
update_pull_request
close_pull_request
merge_pull_request
list_workflows
list_workflow_runs
get_workflow_run
list_workflow_run_jobs
get_workflow_run_logs
list_workflow_run_artifacts
get_artifact_metadata
dispatch_workflow
enable_workflow
disable_workflow
set_variable
remove_variable
set_secret
remove_secret
```

The GPT Action v0.2.1 exposes 28 operations; `health`, branch deletion, and artifact metadata are implemented by the Lambda but are not part of the current GPT-callable schema.

## Application constants/configuration

```text
APP_NAME = github-gpt-wrapper
APP_VERSION = 0.3.0
GITHUB_API = https://api.github.com
GITHUB_API_VERSION = environment value, default 2022-11-28
GITHUB_OWNER = required environment variable
GITHUB_TOKEN = required environment variable
APP_API_KEY = required environment variable
BRANCH_PREFIX = environment value, default gpt
DEFAULT_BASE_BRANCH = optional environment variable
REQUEST_TIMEOUT = environment value, default 30 seconds
```

Missing `GITHUB_OWNER`, `GITHUB_TOKEN`, or `APP_API_KEY` causes startup failure.

## Python dependencies

Pinned `requirements.txt`:

```text
fastapi==0.115.12
mangum==0.19.0
httpx==0.28.1
PyNaCl==1.5.0
pydantic==2.11.3
```

Dependency roles:

| Dependency | Role |
|---|---|
| FastAPI | HTTP application/routing/request handling |
| Mangum | Adapts ASGI/FastAPI to AWS Lambda events |
| HTTPX | GitHub REST API HTTP client |
| PyNaCl | GitHub Actions secret encryption with sealed boxes |
| Pydantic | Request-body validation/models |

Vendored third-party dependency source/binaries from the deployment zip are not republished as High Director-owned code.

## AWS deployment code

`template.yaml` declares:

```text
AWS::Serverless::Function logical ID: GithubGptWrapper
Runtime: python3.13
Handler: src.app.handler
Memory: 512 MB
Timeout: 30 seconds
Function URL AuthType: NONE
Invoke mode: BUFFERED
```

Environment parameters:

```text
GithubOwner
GithubToken (NoEcho)
AppApiKey (NoEcho)
DefaultBaseBranch
BranchPrefix
```

`samconfig.toml` records stack `github-gpt-wrapper`, region `us-east-2`, `CAPABILITY_IAM`, base branch `main`, and branch prefix `gpt`. The real GitHub owner value is intentionally redacted in the published copy.

## Live deployment comparison

Live AWS evidence confirms:

```text
Runtime: Python 3.13
Handler: src.app.handler
Architecture: x86_64
Runtime updates: Auto
Function URL auth: NONE
Invoke mode: BUFFERED
CORS: not enabled
```

Live environment-variable keys confirmed:

```text
APP_API_KEY
BRANCH_PREFIX
DEFAULT_BASE_BRANCH
GITHUB_OWNER
GITHUB_TOKEN
```

Live memory/timeout remain source/template-verified but were not separately captured from the AWS Console.

## GitHub Action contract dependencies

Current GitHub Action:

```text
OpenAPI: 3.1.0
Title: GitHub GPT Wrapper
Version: 0.2.1
Authentication: API Key
Header: X-API-Key
Server: private AWS Lambda Function URL
Operations: 28
```

Canonical schema: `_docs/high-director/github-action-openapi-schema.md`.

## Google Workspace Action code/configuration dependency

There is no user-supplied custom server code for the Google Workspace Action. The GPT Action calls public Google APIs directly through OAuth.

Verified contract:

```text
OpenAPI: 3.1.0
Title: Google Workspace API
Version: 1.2.0
Authentication: OAuth
Calendar operations: 7
Gmail operations: 5
```

Canonical schema/configuration record: `_docs/high-director/google-workspace-action.md`.

Configured OAuth scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

## Documentation-supporting code

High Director documentation itself relies on repository code/configuration including:

```text
.github/workflows/validate-documentation.yml
scripts/validate_docs.py
_config.yml
_data/docs_sections.yml
_templates/high-director-template.md
```

The validator is Python and uses `PyYAML==6.0.2` in the GitHub Actions workflow.

## Rebuild boundary

### GitHub wrapper

A rebuild requires the authoritative private source workspace containing the reconstructed/current `src/app.py`, `template.yaml`, `requirements.txt`, and deployment configuration plus non-public deployment parameter values.

Source-derived SAM sequence is documented in `_docs/runbooks/high-director-operations-and-deployment.md`.

Do not use the sanitized `samconfig.toml` directly for production because its owner value is redacted. Do not put `GITHUB_TOKEN` or `APP_API_KEY` into public repository files.

### Google Workspace Action

Rebuild/restore requires the documented OpenAPI schema, OAuth endpoints/scopes, plus private OAuth Client ID/Secret configured through the GPT Builder UI. Private OAuth credentials are intentionally not stored in this documentation repository.

## Known code limitations

- Lambda application v0.3.0 and current GPT schema v0.2.1 are version-drifted.
- Bundled OpenAPI v0.2.0 is older and malformed as packaged.
- preview-before-write is not server-enforced.
- direct default-branch writes are not blocked by apply endpoints when an existing default branch is explicitly selected.
- credential rotation procedures are not implemented/documented as code automation.
- monitoring/alerting/rollback automation remains unverified.

## Verification record

Verified on 2026-08-06 against the original user-supplied Lambda zip, exact `src/app.py` SHA-256, sanitized source/configuration assets, current Action schemas, live AWS configuration, and repository documentation tooling.

## Related Documents

- [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }})
- [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }})
- [High Director GitHub Wrapper Live AWS Configuration]({{ '/projects/high-director/github-wrapper-live-aws-configuration/' | relative_url }})
- [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})
- [Operate and Update High Director]({{ '/projects/runbooks/high-director-operations-and-deployment/' | relative_url }})
- [Troubleshoot and Hand Off High Director]({{ '/projects/runbooks/high-director-troubleshooting-and-handoff/' | relative_url }})
