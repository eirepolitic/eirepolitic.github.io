---
title: High Director GitHub Wrapper Lambda
summary: Authoritative source-package analysis for the AWS Lambda implementation behind the High Director GitHub Action, including code structure, deployment configuration, authentication, data flow, dependencies, drift, and failure modes.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 21
permalink: /projects/high-director/github-wrapper-lambda/
---

# High Director GitHub Wrapper Lambda

## Purpose

This page documents the user-supplied authoritative Lambda deployment/source package behind the High Director GitHub Action. Live deployed AWS settings are canonicalized separately in [High Director GitHub Wrapper Live AWS Configuration]({{ '/projects/high-director/github-wrapper-live-aws-configuration/' | relative_url }}).

## Evidence classification

**User-supplied authoritative source package**, supplied on 2026-08-06.

Package SHA-256:

```text
07bf8a5dbd5d688e472b6e11f9aa68f6b84b155bf7cd0e265bf5d43524943554
```

The package contained first-party application/configuration files plus bundled third-party Python dependencies. Third-party dependency source files are not republished; exact pinned dependency versions are preserved from `requirements.txt`.

## First-party source inventory

| Source file | Role | Original SHA-256 | Publication treatment |
|---|---|---|---|
| `src/app.py` | FastAPI/Mangum Lambda application | `3a6ac1d69c2571c403aa01746c1c2d55df2c266de5ddfc789df2199e4876c5f0` | Analyzed and structurally documented; no embedded secret values found |
| `template.yaml` | AWS SAM deployment template | `28df2995b2975f1afe6f7e1d20e5d1cb714f00bb4665c12c566128f5d869739a` | Published unchanged |
| `samconfig.toml` | SAM deployment configuration | `03561a4d9181a8e1eb69be5371852935713ab76049f9057b4182f4c4b576d74a` | GitHub owner value redacted |
| `requirements.txt` | Pinned Python dependencies | `9fd3783460ea49eb8cd5598730668ee80bc1c6524e6989789b0e1529eb944316` | Published unchanged |
| `README.md` | Starter/deployment documentation | `07910fd0dde146b5f23b020efe04e312c42490200ab0ea244b8c0ea0261862e2` | Published unchanged; treated as historical/starter guidance where it conflicts with implementation |
| `openapi.yaml` | Bundled older Action schema | `69242ee384c8ed447a75648554ac193bf5a6eda5ba40894b47ecb50be923f9d6` | Private Lambda URL redacted; indentation normalized for readability because the packaged file is malformed YAML |

Sanitized source/configuration assets are under:

```text
assets/high-director/github-wrapper-source/
```

The source package itself is not published because it includes vendored third-party binaries/modules and private deployment-specific material.

## Application identity

`src/app.py` defines:

```text
APP_NAME = github-gpt-wrapper
APP_VERSION = 0.3.0
GITHUB_API = https://api.github.com
```

The application uses FastAPI and is adapted to Lambda through Mangum:

```text
handler = src.app.handler
```

## Deployment configuration

The supplied SAM template declares:

| Setting | Value |
|---|---|
| Resource logical ID | `GithubGptWrapper` |
| Resource type | `AWS::Serverless::Function` |
| Handler | `src.app.handler` |
| Runtime | `python3.13` |
| Memory | `512 MB` |
| Timeout | `30 seconds` |
| Function URL auth | `NONE` |
| Function URL invoke mode | `BUFFERED` |

The live AWS Console source supplied later confirms Python 3.13, handler `src.app.handler`, architecture `x86_64`, Function URL auth `NONE`, invoke mode `BUFFERED`, and CORS disabled. Live memory/timeout were not part of that source set.

The template declares five deployment parameters:

- `GithubOwner`
- `GithubToken` (`NoEcho: true`)
- `AppApiKey` (`NoEcho: true`)
- `DefaultBaseBranch` (default `main`)
- `BranchPrefix` (default `gpt`)

The supplied `samconfig.toml` records:

- stack name `github-gpt-wrapper`;
- region `us-east-2`;
- `CAPABILITY_IAM`;
- default base branch `main`;
- branch prefix `gpt`.

The owner value in `samconfig.toml` is intentionally redacted from the published copy.

## Runtime environment variables

`src/app.py` consumes:

| Variable | Requirement/default | Purpose |
|---|---|---|
| `GITHUB_OWNER` | required | Single GitHub owner enforced by backend path construction |
| `GITHUB_TOKEN` | required | Bearer credential for GitHub REST API |
| `APP_API_KEY` | required | Application-level API key compared with incoming `X-API-Key` |
| `BRANCH_PREFIX` | default `gpt` | Prefix for automatically generated branch names |
| `DEFAULT_BASE_BRANCH` | optional | Explicit base branch override; repository default used when unset |
| `GITHUB_API_VERSION` | default `2022-11-28` | `X-GitHub-Api-Version` request header |
| `REQUEST_TIMEOUT` | default `30` | HTTPX timeout seconds |

The live AWS Console confirms the deployed presence of `APP_API_KEY`, `BRANCH_PREFIX`, `DEFAULT_BASE_BRANCH`, `GITHUB_OWNER`, and `GITHUB_TOKEN`. No values were supplied or published.

The code refuses to start when `GITHUB_OWNER`, `GITHUB_TOKEN`, or `APP_API_KEY` is missing.

## Authentication model

### GPT to Lambda wrapper

The SAM template and live AWS Console both show Lambda Function URL `AuthType: NONE`. AWS therefore does not require IAM authentication at the Function URL layer.

The application itself enforces an API key by comparing incoming `X-API-Key` with the `APP_API_KEY` environment variable. Invalid/missing values return application error `401 unauthorized`.

### Lambda wrapper to GitHub

The wrapper sends:

```text
Authorization: Bearer <GITHUB_TOKEN>
Accept: application/vnd.github+json
X-GitHub-Api-Version: <GITHUB_API_VERSION>
User-Agent: github-gpt-wrapper
```

The SAM parameter description and README identify `GithubToken` as a fine-grained GitHub personal access token. The package does not expose the token value.

## Owner boundary

The code builds GitHub REST paths as:

```text
/repos/{GITHUB_OWNER}/{repo}/...
```

`normalize_repo_name()` rejects any `repo` value containing `/`, returning a 400 error that instructs callers to pass repository name only rather than `owner/repo`.

This directly implements the High Director instruction that the owner is configured in the backend.

## Application route inventory

The application source exposes 31 HTTP routes including `/health`:

- file read/tree/search;
- preview/apply upsert;
- preview/apply delete;
- branch list/create/delete;
- pull-request create/list/get/update/close/merge;
- workflow list/run inspection/logs/artifacts;
- artifact metadata;
- workflow dispatch/enable/disable;
- repository Actions variable set/delete;
- repository Actions secret set/delete.

The current GPT Action schema v0.2.1 exposes 28 operations and does not expose these application routes:

- `GET /health`
- `DELETE /repos/{repo}/branches/{branch_name:path}`
- `GET /repos/{repo}/artifacts/{artifact_id}`

Therefore **application capability is broader than the currently configured GPT Action surface**.

## Version and schema drift

| Artifact | Version/status |
|---|---|
| `src/app.py` FastAPI app | `0.3.0` |
| Current GPT Action schema supplied separately | `0.2.1` |
| Bundled package `openapi.yaml` | `0.2.0` |

The bundled v0.2.0 schema contains 30 `operationId` declarations, including branch deletion and artifact metadata, but it is malformed YAML as packaged due to indentation near the first `paths` entry. The current v0.2.1 GPT schema is therefore the canonical Action contract for what the GPT can call today.

## File-change behavior

Preview endpoints calculate unified diffs without writing.

Apply endpoints resolve a base branch, sanitize/generate a target branch, create it if needed, call GitHub's contents API, and return commit/content metadata.

## Direct-default-branch boundary

The README says never write directly to the default branch. **The application code does not enforce that rule for file writes.** A caller that explicitly supplies the default branch as `branch_name` can cause an apply endpoint to write there because `ensure_branch_exists()` accepts an existing branch.

Branch deletion does explicitly refuse to delete the repository default branch.

## Pull-request behavior

The wrapper can create/list/get/update/close/merge pull requests. Merge methods are `merge`, `squash`, and `rebase`, with optional commit title/message and expected SHA.

This confirms that README statements saying the starter "does not merge PRs" are historical/outdated relative to `src/app.py` 0.3.0.

## Workflow behavior

The wrapper can list workflows, inspect runs/jobs/logs/artifacts, fetch artifact metadata, dispatch workflows, and enable/disable workflows.

## Repository variables and secrets

Variables are created through the GitHub Actions variables API; a `409` create conflict triggers an update path.

For secrets, the wrapper fetches the repository Actions public key, encrypts supplied plaintext using PyNaCl `SealedBox`, sends the encrypted value/key ID to GitHub, and does not return the plaintext.

## Error model and failure modes

Verified failure classes include:

- `400 bad_request`;
- `401 unauthorized`;
- `404 not_found`;
- `422 validation_error`;
- upstream GitHub status codes surfaced as `github_error`;
- `502 github_transport_error`;
- `504 github_timeout`;
- `500 internal_error`.

## Dependencies

```text
fastapi==0.115.12
mangum==0.19.0
httpx==0.28.1
PyNaCl==1.5.0
pydantic==2.11.3
```

Bundled third-party modules in the deployment package are implementation dependencies, not High Director-owned source, and are not copied into the documentation repository.

## README drift

Verified drift includes:

- README manual deployment path says Python 3.12; SAM and live runtime are Python 3.13;
- README says the starter does not merge PRs; application v0.3.0 implements PR merge;
- README proposes mandatory preview/user approval; application does not enforce preview-before-apply;
- README says never write directly to `main`; apply endpoints do not enforce that restriction.

Use current source/live configuration as authoritative over README guidance when they conflict.

## Live execution role

The live AWS Console source verifies execution role:

```text
github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo
```

The supplied permissions view shows attached managed policy `AWSLambdaBasicExecutionRole`. The supplied trust policy permits `lambda.amazonaws.com` to call `sts:AssumeRole`.

See the live-AWS configuration page for the canonical security-boundary record.

## Sanitization record

- private Lambda Function URL hostname removed;
- literal GitHub owner value replaced with `REDACTED_OWNER` in published `samconfig.toml`;
- AWS account ID omitted from live-configuration publication;
- no API key, GitHub PAT, AWS credential, password, private key, personal email, or token value is published;
- vendored third-party dependencies/binaries excluded.

## What remains unverified

- exact deployed Lambda function name;
- live memory and timeout;
- current environment-variable values;
- API-key creation/storage/rotation process;
- exact GitHub fine-grained PAT permissions actually granted;
- whether additional/inline execution-role policies exist beyond the supplied view;
- CloudWatch log retention/alarms/monitoring;
- Function URL resource-policy details;
- deployment history/versioning/aliases/reserved concurrency/dead-letter configuration.

## Related Documents

- [High Director GitHub Wrapper Live AWS Configuration]({{ '/projects/high-director/github-wrapper-live-aws-configuration/' | relative_url }})
- [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director GPT Configuration]({{ '/projects/high-director/gpt-configuration/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
