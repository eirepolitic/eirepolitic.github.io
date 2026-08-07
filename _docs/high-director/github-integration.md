---
title: High Director GitHub Integration
summary: Verified and observable GitHub integration surface used by High Director, including repository operations, documentation validation, pull-request discipline, and Pages deployment verification.
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

This page is the canonical source for the GitHub integration behavior currently available to High Director and the repository workflows used to publish documentation.

It distinguishes the configured/observed operation surface from the connector implementation, authentication model, hosting, and schema source, which remain unverified until authoritative external configuration is supplied.

## Repository addressing rule

**User-supplied authoritative operating rule:** the repository owner is configured in the integration backend. GitHub operations must pass only the repository name in the `repo` parameter.

For this documentation initiative, the repository value is:

```text
eirepolitic.github.io
```

No `owner/repo` value is passed to this integration.

## Configured GitHub operation surface

The current High Director environment exposes the following GitHub operations.

### Repository content

| Operation | Purpose | Evidence |
|---|---|---|
| `getFile` | Read a file at a repository path/ref | Exercised successfully |
| `listRepoTree` | List repository tree contents | Exercised successfully |
| `searchRepoContents` | Search repository file contents | Exercised successfully |
| `previewUpsertFile` | Preview a file create/update without writing | Configured; not required in Phase 3 |
| `applyUpsertFile` | Create/update a file on a branch | Exercised successfully |
| `previewDeleteFile` | Preview a file deletion | Configured; not exercised |
| `applyDeleteFile` | Delete a file on a branch | Configured; not exercised |

### Branches and pull requests

| Operation | Purpose | Evidence |
|---|---|---|
| `listBranches` | List repository branches | Configured |
| `createBranch` | Create a branch from another branch | Exercised successfully |
| `listPullRequests` | List pull requests | Exercised successfully |
| `createPullRequest` | Open a pull request | Exercised successfully |
| `getPullRequest` | Read pull-request state/details | Exercised successfully |
| `updatePullRequest` | Change PR metadata/base/state fields | Configured |
| `closePullRequest` | Close a pull request | Configured |
| `mergePullRequest` | Merge a pull request | Exercised successfully |

### GitHub Actions

| Operation | Purpose | Evidence |
|---|---|---|
| `listWorkflows` | List configured workflows | Exercised successfully |
| `listWorkflowRuns` | List workflow runs | Exercised successfully |
| `getWorkflowRun` | Read workflow-run state | Exercised successfully |
| `listWorkflowRunJobs` | Inspect jobs and steps | Exercised successfully |
| `getWorkflowRunLogs` | Obtain workflow-run log download information | Configured |
| `listWorkflowRunArtifacts` | List workflow-run artifacts | Configured |
| `dispatchWorkflow` | Start a workflow that supports `workflow_dispatch` | Exercised successfully |
| `enableWorkflow` | Enable a workflow | Configured; not exercised |
| `disableWorkflow` | Disable a workflow | Configured; not exercised |

### Actions variables and secrets

| Operation | Purpose | Evidence |
|---|---|---|
| `setVariable` | Create/update a repository Actions variable | Configured; not exercised |
| `deleteVariable` | Delete a repository Actions variable | Configured; not exercised |
| `setSecret` | Store a repository Actions secret | Configured; not exercised |
| `deleteSecret` | Delete a repository Actions secret | Configured; not exercised |

The configured secret-write operation does not return the secret value. No secret values are required or published by this documentation initiative.

## Operation-surface evidence classification

- **Exercised successfully** means the operation was called successfully during the High Director documentation initiative.
- **Configured** means the operation is present in the current integration surface but was not required to prove Phase 3 documentation behavior.
- Neither status proves the connector's internal code, hosting, authentication flow, OpenAPI schema source, Lambda implementation, API Gateway configuration, or IAM model.

## Documentation validation workflow

### Verified implementation

Repository path:

```text
.github/workflows/validate-documentation.yml
```

Workflow name:

```text
Validate documentation
```

GitHub workflow ID observed on 2026-08-06:

```text
328299040
```

Triggers:

- pull requests touching documentation/site paths defined by the workflow;
- manual `workflow_dispatch`.

Permissions declared by the workflow:

```yaml
permissions:
  contents: read
```

Execution environment and steps:

1. `ubuntu-latest`
2. `actions/checkout@v4`
3. `actions/setup-python@v5`
4. Python `3.12`
5. install `PyYAML==6.0.2`
6. run `python scripts/validate_docs.py`

## Documentation validator

Verified repository path:

```text
scripts/validate_docs.py
```

The validator checks, among other items:

- required front-matter fields;
- allowed section names;
- allowed document types;
- allowed status values;
- `YYYY-MM-DD` date formatting;
- archive metadata rules;
- permalink formatting and duplicates;
- Markdown/HTML local references;
- `related` metadata references.

A validation error returns a non-zero exit status and blocks the documentation merge process by policy.

## GitHub Pages deployment workflow

The repository exposes the GitHub-managed Pages workflow as:

```text
name: pages-build-deployment
path: dynamic/pages/pages-build-deployment
workflow ID observed: 235033235
```

This is a GitHub-managed dynamic workflow rather than a workflow file stored at `.github/workflows/` in this repository.

Observed deployment jobs include:

1. build;
2. report build status;
3. deploy.

Successful runs for this initiative include Pages deployments #136, #137, and #138.

## Verified documentation change flow

The documentation initiative uses this sequence:

1. inspect authoritative repository evidence;
2. create a focused branch;
3. make the documentation change on that branch;
4. open a focused pull request;
5. run/observe `Validate documentation`;
6. confirm validation succeeds;
7. merge the pull request;
8. identify the Pages run whose `head_sha` matches the merged commit;
9. confirm the Pages workflow completes with `conclusion: success`;
10. only then begin the next major documentation phase.

This flow was successfully exercised for PRs #29, #30, and #31.

## Failure handling

### Validation failure

Do not merge. Inspect the validation job/steps and correct only the documentation defect. Rerun validation until it succeeds.

### Pages build/deployment failure

Do not begin the next major documentation phase. Inspect the failed job/step and repository change. Correct through a focused PR when a repository change is required.

### GitHub integration call failure

Treat the returned API/integration error as the authoritative immediate diagnostic. Do not guess that repository formatting is wrong unless the response explicitly indicates that cause.

## Security and access boundaries

Verified or authoritative current rules:

- the repository owner is configured in the backend rather than passed by the agent;
- secret values must not be published in documentation;
- configured secret operations do not expose stored secret values back through the integration;
- documentation changes use branches and pull requests rather than direct mutation of `main`.

Still unknown/unverified:

- connector authentication method;
- token or app type;
- GitHub App installation configuration;
- OAuth scopes or token scopes;
- backend hosting;
- connector source code;
- Action/OpenAPI schema source;
- AWS Lambda/API Gateway implementation, if any;
- IAM roles/policies/trust relationships.

## Known limitations

- The configured operation surface describes what High Director can request, not the internal implementation.
- Configured-but-unexercised operations are not claimed as successfully tested behavior.
- GitHub-managed Pages internals are outside this repository.
- Workflow IDs are observed identifiers and may change if workflows are recreated.

## Verification record

Verified on 2026-08-06 through direct inspection of `.github/workflows/validate-documentation.yml`, `scripts/validate_docs.py`, workflow inventory, workflow runs/jobs, PRs #29–#31, Pages deployments #136–#138, and the configured GitHub operation surface available to High Director.

## Next safe action

Complete the Phase 3 validation/merge/Pages gate. After successful deployment, the repository/direct-observation work is sufficient to request the first authoritative external source: the High Director ChatGPT configuration and instructions.
