---
title: High Director GitHub Integration
summary: Verified GitHub GPT Action contract, authentication declaration, operation surface, repository rules, documentation validation, and Pages deployment workflow.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
order: 18
---

# High Director GitHub Integration

## Purpose

This page is the canonical source for the High Director GitHub integration behavior. The Action contract is now verified from a user-supplied authoritative OpenAPI schema; backend Lambda source, GitHub credential type, IAM, and secret storage remain unverified.

## Repository addressing rule

**User-supplied authoritative operating rule:** the GitHub owner is already configured in the backend. The Action must receive repository name only in the `repo` parameter.

For this documentation initiative:

```text
eirepolitic.github.io
```

Do not pass `owner/repo`.

## Authoritative Action identity

| Field | Verified value |
|---|---|
| OpenAPI title | `GitHub GPT Wrapper` |
| OpenAPI version | `0.2.1` |
| OpenAPI specification | `3.1.0` |
| GPT authentication selection | `API Key` |
| Security scheme | `ApiKeyAuth` |
| API-key header | `X-API-Key` |
| Server type | AWS Lambda Function URL; hostname redacted |
| Operation count | `28` |

The complete sanitized authoritative schema is preserved in [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }}).

## Operation groups

The schema defines operations for:

- reading files, repository trees, and repository search;
- previewing and applying file creates/updates/deletes;
- listing and creating branches;
- listing, creating, reading, updating, closing, and merging pull requests;
- listing workflows and workflow runs;
- inspecting workflow runs, jobs, logs, and artifacts;
- dispatching, enabling, and disabling workflows;
- creating/updating/deleting GitHub Actions variables;
- creating/updating/deleting GitHub Actions secrets.

Exact operation IDs, HTTP methods, paths, request schemas, and response schemas are canonicalized in the OpenAPI-schema page rather than duplicated here.

## Authentication boundary

Verified client-to-wrapper authentication:

```yaml
security:
  - ApiKeyAuth: []

components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

This verifies only how the GPT Action authenticates to the wrapper. It does not establish:

- the API-key value, storage, or rotation process;
- Lambda Function URL AWS authorization mode;
- how the wrapper authenticates to GitHub;
- whether GitHub uses a PAT, GitHub App, installation token, or other credential;
- IAM role/policy details.

## Response contract

The schema defines shared `SuccessResponse` and `ErrorResponse` objects.

- success requires `ok: true` and may include `message` and object `result`;
- errors require `error`, `message`, and integer `status`, and may include object `details`;
- `setSecret` accepts `plaintext_value` and explicitly states that the secret value is not returned by the API.

## Observed operation status

The following schema-defined operations have been exercised successfully during this documentation initiative:

- `getFile`
- `listRepoTree`
- `searchRepoContents`
- `applyUpsertFile`
- `createBranch`
- `listPullRequests`
- `createPullRequest`
- `getPullRequest`
- `mergePullRequest`
- `listWorkflows`
- `listWorkflowRuns`
- `getWorkflowRun`
- `listWorkflowRunJobs`
- `dispatchWorkflow`

Other schema-defined operations are configured but are not claimed as tested unless separately recorded.

## Documentation validation workflow

Verified repository path:

```text
.github/workflows/validate-documentation.yml
```

Workflow name:

```text
Validate documentation
```

Observed workflow ID on 2026-08-06:

```text
328299040
```

The workflow runs on `ubuntu-latest`, checks out the repository, configures Python 3.12, installs `PyYAML==6.0.2`, and runs:

```text
python scripts/validate_docs.py
```

The validator checks required metadata, allowed section/type/status values, dates, archive rules, permalinks, local references, and related-document references.

## GitHub Pages deployment

The repository exposes GitHub's managed Pages workflow as:

```text
name: pages-build-deployment
path: dynamic/pages/pages-build-deployment
workflow ID observed: 235033235
```

The documentation initiative treats a major phase as complete only after the Pages run for the merged commit finishes with `conclusion: success`.

## Verified documentation change flow

1. inspect authoritative evidence;
2. create a focused branch;
3. make the documentation change;
4. open a focused PR;
5. run/observe documentation validation;
6. confirm validation succeeds;
7. merge the PR;
8. confirm the matching Pages deployment succeeds;
9. begin the next major documentation step.

## Failure handling

### Validation failure

Do not merge. Inspect the failed validation step, correct the documentation defect, and rerun validation.

### Pages failure

Do not begin the next major documentation phase. Inspect the failed build/deploy job and correct through a focused PR if repository changes are needed.

### GitHub integration call failure

Use the returned API/integration error as the immediate diagnostic. Do not guess that repository format is wrong unless the error explicitly says so.

## Security boundaries

Verified:

- GPT-to-wrapper calls use an API key in `X-API-Key`;
- the wrapper server is an AWS Lambda Function URL;
- the owner is configured in the backend and is not passed in `repo`;
- the Action is write-capable, including PR merge, workflow enable/disable, variable changes, and secret changes;
- secret values must not be published;
- the private Lambda hostname is intentionally omitted from this site.

Still unverified:

- Lambda source/handler/runtime;
- API-key value/storage/rotation;
- GitHub backend credential type and permissions;
- IAM roles/policies/trust relationships;
- logging/monitoring/rate limiting/WAF controls;
- API Gateway use. The supplied schema points directly to a Lambda Function URL and does not itself establish API Gateway.

## Verification record

Verified on 2026-08-06 from repository workflow definitions, successful GitHub integration operations, and the user-supplied `GitHub GPT Wrapper` OpenAPI 3.1.0 schema version `0.2.1` with API-key authentication.
