---
title: High Director GitHub Action OpenAPI Schema
summary: Sanitized authoritative OpenAPI schema for the High Director GitHub GPT wrapper Action, including authentication declaration, routes, operation IDs, request schemas, and responses.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 20
permalink: /projects/high-director/github-action-openapi-schema/
---

# High Director GitHub Action OpenAPI Schema

## Purpose

This page preserves the sanitized authoritative OpenAPI schema supplied by the system owner for the private AWS Lambda URL-backed High Director Action.

## Evidence classification

**User-supplied authoritative source.**

The source was supplied on 2026-08-06 as a complete OpenAPI document plus the GPT Action authentication selection `API Key`.

## Sanitization

The original schema contained a private AWS Lambda Function URL hostname in `servers[0].url`. That hostname is replaced below with:

```text
https://PRIVATE-LAMBDA-URL-REDACTED.invalid
```

No API key value, token, password, credential, personal identifier, or other secret was present in the supplied schema. All paths, operation IDs, schema property names, authentication structure, and response definitions are preserved.

## Schema identity

| Field | Authoritative value |
|---|---|
| OpenAPI version | `3.1.0` |
| API title | `GitHub GPT Wrapper` |
| API version | `0.2.1` |
| Authentication type selected in GPT UI | `API Key` |
| OpenAPI security scheme | `ApiKeyAuth` |
| API-key location | HTTP header |
| API-key header name | `X-API-Key` |
| Operation count | `28` |
| Server | Private AWS Lambda Function URL; hostname redacted from publication |

The schema description states that the wrapper supports repository file access, repository browsing, preview/apply file changes, pull-request management, workflow inspection/control, and repository Actions variables/secrets for a single GitHub owner.

## Operation catalogue

| Operation ID | Method | Path |
|---|---|---|
| `getFile` | `GET` | `/repos/{repo}/files` |
| `listRepoTree` | `GET` | `/repos/{repo}/tree` |
| `searchRepoContents` | `GET` | `/repos/{repo}/search` |
| `previewUpsertFile` | `POST` | `/repos/{repo}/files/preview-upsert` |
| `applyUpsertFile` | `POST` | `/repos/{repo}/files/apply-upsert` |
| `previewDeleteFile` | `POST` | `/repos/{repo}/files/preview-delete` |
| `applyDeleteFile` | `POST` | `/repos/{repo}/files/apply-delete` |
| `listBranches` | `GET` | `/repos/{repo}/branches` |
| `createBranch` | `POST` | `/repos/{repo}/branches` |
| `listPullRequests` | `GET` | `/repos/{repo}/pull-requests` |
| `createPullRequest` | `POST` | `/repos/{repo}/pull-requests` |
| `getPullRequest` | `GET` | `/repos/{repo}/pull-requests/{number}` |
| `updatePullRequest` | `PATCH` | `/repos/{repo}/pull-requests/{number}` |
| `closePullRequest` | `POST` | `/repos/{repo}/pull-requests/{number}/close` |
| `mergePullRequest` | `POST` | `/repos/{repo}/pull-requests/{number}/merge` |
| `listWorkflows` | `GET` | `/repos/{repo}/workflows` |
| `listWorkflowRuns` | `GET` | `/repos/{repo}/workflows/{workflow_id}/runs` |
| `getWorkflowRun` | `GET` | `/repos/{repo}/workflow-runs/{run_id}` |
| `listWorkflowRunJobs` | `GET` | `/repos/{repo}/workflow-runs/{run_id}/jobs` |
| `getWorkflowRunLogs` | `GET` | `/repos/{repo}/workflow-runs/{run_id}/logs` |
| `listWorkflowRunArtifacts` | `GET` | `/repos/{repo}/workflow-runs/{run_id}/artifacts` |
| `dispatchWorkflow` | `POST` | `/repos/{repo}/workflows/{workflow_id}/dispatch` |
| `enableWorkflow` | `POST` | `/repos/{repo}/workflows/{workflow_id}/enable` |
| `disableWorkflow` | `POST` | `/repos/{repo}/workflows/{workflow_id}/disable` |
| `setVariable` | `PUT` | `/repos/{repo}/variables/{name}` |
| `deleteVariable` | `DELETE` | `/repos/{repo}/variables/{name}` |
| `setSecret` | `PUT` | `/repos/{repo}/secrets/{name}` |
| `deleteSecret` | `DELETE` | `/repos/{repo}/secrets/{name}` |

## Request schemas

The authoritative component schemas are:

- `UpsertRequest`
- `DeleteRequest`
- `PullRequestCreateRequest`
- `PullRequestMergeRequest`
- `PullRequestUpdateRequest`
- `PullRequestCloseRequest`
- `BranchCreateRequest`
- `DispatchWorkflowRequest`
- `VariableSetRequest`
- `SecretSetRequest`
- `SuccessResponse`
- `ErrorResponse`

The full field definitions are preserved in the sanitized source below.

## Authentication model verified by this source

The GPT Action is configured as **API Key** authentication. The OpenAPI document declares:

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

This verifies the client-to-wrapper authentication declaration. It does **not** establish how the wrapper authenticates onward to GitHub; backend GitHub credentials, token type, permissions, IAM configuration, and secret storage remain unverified.

## Response model

All documented operations use shared success/error responses:

- `SuccessResponse` requires `ok: true` and may include `message` plus an object `result`.
- `ErrorResponse` requires `error`, `message`, and integer `status`, and may include an object `details`.
- `setSecret` explicitly states that the plaintext secret is stored on GitHub and is never returned by the API.

## Sanitized authoritative OpenAPI source

```yaml
openapi: 3.1.0
info:
  title: GitHub GPT Wrapper
  version: 0.2.1
  description: >
    Wrapper API for a custom GPT to read files, browse repos, preview and apply file changes on branches, manage pull
    requests, inspect workflow runs, and manage repository variables and secrets for a single GitHub owner.
servers:
  - url: https://PRIVATE-LAMBDA-URL-REDACTED.invalid
security:
  - ApiKeyAuth: []
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
  schemas:
    UpsertRequest:
      type: object
      required:
        - path
        - content
        - commit_message
      properties:
        path:
          type: string
        content:
          type: string
        commit_message:
          type: string
        base_branch:
          type: string
        branch_name:
          type: string
    DeleteRequest:
      type: object
      required:
        - path
        - commit_message
      properties:
        path:
          type: string
        commit_message:
          type: string
        base_branch:
          type: string
        branch_name:
          type: string
    PullRequestCreateRequest:
      type: object
      required:
        - title
        - head_branch
      properties:
        title:
          type: string
        body:
          type: string
        head_branch:
          type: string
        base_branch:
          type: string
        draft:
          type: boolean
          default: true
    PullRequestMergeRequest:
      type: object
      properties:
        commit_title:
          type: string
        commit_message:
          type: string
        merge_method:
          type: string
          enum:
            - merge
            - squash
            - rebase
          default: merge
        sha:
          type: string
    PullRequestUpdateRequest:
      type: object
      properties:
        title:
          type: string
        body:
          type: string
        base_branch:
          type: string
        state:
          type: string
          enum:
            - open
            - closed
    PullRequestCloseRequest:
      type: object
      properties:
        state_reason:
          type: string
          enum:
            - completed
            - not_planned
          default: completed
    BranchCreateRequest:
      type: object
      required:
        - new_branch
      properties:
        new_branch:
          type: string
        from_branch:
          type: string
    DispatchWorkflowRequest:
      type: object
      required:
        - ref
      properties:
        ref:
          type: string
        inputs:
          type: object
          additionalProperties: true
    VariableSetRequest:
      type: object
      required:
        - value
      properties:
        value:
          type: string
    SecretSetRequest:
      type: object
      required:
        - plaintext_value
      properties:
        plaintext_value:
          type: string
    SuccessResponse:
      type: object
      required:
        - ok
      properties:
        ok:
          type: boolean
          enum:
            - true
        message:
          type: string
        result:
          type: object
          additionalProperties: true
    ErrorResponse:
      type: object
      required:
        - error
        - message
        - status
      properties:
        error:
          type: string
        message:
          type: string
        status:
          type: integer
        details:
          type: object
          additionalProperties: true
responses:
  Success:
    description: Successful response
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/SuccessResponse"
  Error:
    description: Error response
    content:
      application/json:
        schema:
          $ref: "#/components/schemas/ErrorResponse"
paths:
  /repos/{repo}/files:
    get:
      operationId: getFile
      summary: Get a file from a repository
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: path
          in: query
          required: true
          schema:
            type: string
        - name: ref
          in: query
          required: false
          schema:
            type: string
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/tree:
    get:
      operationId: listRepoTree
      summary: List repository tree contents for a ref
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: ref
          in: query
          required: false
          schema:
            type: string
        - name: recursive
          in: query
          required: false
          schema:
            type: boolean
            default: true
        - name: path_prefix
          in: query
          required: false
          schema:
            type: string
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/search:
    get:
      operationId: searchRepoContents
      summary: Search code contents inside a repository
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: q
          in: query
          required: true
          schema:
            type: string
        - name: per_page
          in: query
          required: false
          schema:
            type: integer
            default: 25
        - name: page
          in: query
          required: false
          schema:
            type: integer
            default: 1
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/files/preview-upsert:
    post:
      operationId: previewUpsertFile
      summary: Preview a file create or update without writing to GitHub
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpsertRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/files/apply-upsert:
    post:
      operationId: applyUpsertFile
      summary: Create or update a file on a branch
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UpsertRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/files/preview-delete:
    post:
      operationId: previewDeleteFile
      summary: Preview a file deletion without writing to GitHub
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DeleteRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/files/apply-delete:
    post:
      operationId: applyDeleteFile
      summary: Delete a file on a branch
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DeleteRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/branches:
    get:
      operationId: listBranches
      summary: List repository branches
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: protected
          in: query
          required: false
          schema:
            type: boolean
        - name: per_page
          in: query
          required: false
          schema:
            type: integer
            default: 100
        - name: page
          in: query
          required: false
          schema:
            type: integer
            default: 1
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
    post:
      operationId: createBranch
      summary: Create a repository branch
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/BranchCreateRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/pull-requests:
    get:
      operationId: listPullRequests
      summary: List pull requests
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: state
          in: query
          required: false
          schema:
            type: string
            default: open
        - name: head
          in: query
          required: false
          schema:
            type: string
        - name: base
          in: query
          required: false
          schema:
            type: string
        - name: per_page
          in: query
          required: false
          schema:
            type: integer
            default: 30
        - name: page
          in: query
          required: false
          schema:
            type: integer
            default: 1
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
    post:
      operationId: createPullRequest
      summary: Open a pull request from a branch to the base branch
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PullRequestCreateRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/pull-requests/{number}:
    get:
      operationId: getPullRequest
      summary: Get a pull request
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: number
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
    patch:
      operationId: updatePullRequest
      summary: Update a pull request
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: number
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PullRequestUpdateRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/pull-requests/{number}/close:
    post:
      operationId: closePullRequest
      summary: Close a pull request
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: number
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PullRequestCloseRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/pull-requests/{number}/merge:
    post:
      operationId: mergePullRequest
      summary: Merge a pull request
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: number
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/PullRequestMergeRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflows:
    get:
      operationId: listWorkflows
      summary: List repository workflows
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflows/{workflow_id}/runs:
    get:
      operationId: listWorkflowRuns
      summary: List workflow runs for a workflow
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: workflow_id
          in: path
          required: true
          schema:
            type: string
        - name: branch
          in: query
          required: false
          schema:
            type: string
        - name: event
          in: query
          required: false
          schema:
            type: string
        - name: status
          in: query
          required: false
          schema:
            type: string
        - name: per_page
          in: query
          required: false
          schema:
            type: integer
            default: 20
        - name: page
          in: query
          required: false
          schema:
            type: integer
            default: 1
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflow-runs/{run_id}:
    get:
      operationId: getWorkflowRun
      summary: Get workflow run details
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: run_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflow-runs/{run_id}/jobs:
    get:
      operationId: listWorkflowRunJobs
      summary: List jobs for a workflow run
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: run_id
          in: path
          required: true
          schema:
            type: integer
        - name: per_page
          in: query
          required: false
          schema:
            type: integer
            default: 100
        - name: page
          in: query
          required: false
          schema:
            type: integer
            default: 1
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflow-runs/{run_id}/logs:
    get:
      operationId: getWorkflowRunLogs
      summary: Get a download URL for workflow run logs
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: run_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflow-runs/{run_id}/artifacts:
    get:
      operationId: listWorkflowRunArtifacts
      summary: List artifacts for a workflow run
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: run_id
          in: path
          required: true
          schema:
            type: integer
        - name: per_page
          in: query
          required: false
          schema:
            type: integer
            default: 100
        - name: page
          in: query
          required: false
          schema:
            type: integer
            default: 1
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflows/{workflow_id}/dispatch:
    post:
      operationId: dispatchWorkflow
      summary: Dispatch a workflow that supports workflow_dispatch
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: workflow_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DispatchWorkflowRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflows/{workflow_id}/enable:
    post:
      operationId: enableWorkflow
      summary: Enable a workflow
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: workflow_id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/workflows/{workflow_id}/disable:
    post:
      operationId: disableWorkflow
      summary: Disable a workflow
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: workflow_id
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/variables/{name}:
    put:
      operationId: setVariable
      summary: Create or update a repository Actions variable
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: name
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/VariableSetRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
    delete:
      operationId: deleteVariable
      summary: Delete a repository Actions variable
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: name
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
  /repos/{repo}/secrets/{name}:
    put:
      operationId: setSecret
      summary: Create or update a repository Actions secret
      description: Stores the secret on GitHub. The secret value is never returned by the API.
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: name
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/SecretSetRequest"
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
    delete:
      operationId: deleteSecret
      summary: Delete a repository Actions secret
      parameters:
        - name: repo
          in: path
          required: true
          schema:
            type: string
        - name: name
          in: path
          required: true
          schema:
            type: string
      responses:
        "200":
          $ref: "#/responses/Success"
        default:
          $ref: "#/responses/Error"
```

## Security boundaries

Verified from this source:

- calls to this Action require an API key in the `X-API-Key` header;
- the wrapper is hosted behind a private AWS Lambda Function URL hostname;
- the API exposes write-capable GitHub operations, including file mutation, PR merge, workflow enable/disable, variable mutation, and secret mutation;
- the server URL is infrastructure-sensitive and is not published;
- the schema accepts secret plaintext only on the `setSecret` request and documents that it is not returned.

Still unverified:

- API-key value, storage, rotation, or issuer;
- Lambda Function URL auth mode at the AWS layer;
- Lambda source code and handler;
- GitHub credential type and permissions;
- IAM role/policies;
- rate limiting, logging, monitoring, or WAF controls;
- API Gateway use; the schema points directly to a Lambda Function URL and does not itself establish API Gateway.

## Provenance

- Source supplied by: system owner
- Supplied: `2026-08-06`
- Source type: GPT Action OpenAPI schema + Action authentication selection
- Original private server hostname: intentionally not published
- Technical structure retained: yes

## Related Documents

- [High Director GPT Configuration]({{ '/projects/high-director/gpt-configuration/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director Capability and Component Inventory]({{ '/docs/high-director/capability-component-inventory/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
