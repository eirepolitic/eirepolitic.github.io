---
title: "Build Your Own High Director — Addendum B: Additional AWS Capabilities"
summary: Extend the completed High Director-style system cautiously, starting with existing unexposed wrapper routes and separating new AWS-service integrations from the verified core build.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 74
permalink: /docs/high-director/build-your-own/addendum-additional-aws-capabilities/
---

# Addendum B — Additional AWS Capabilities

## Purpose

This addendum separates two very different kinds of extension:

1. **existing wrapper capabilities that already exist in the verified Lambda code but are not exposed by the current GPT Action schema**;
2. **new AWS-service capabilities such as Amazon S3**, which require new backend code and IAM permissions and therefore should not be treated as a harmless schema edit.

Complete the core guide before using this addendum.

## Level 1 — Existing backend routes you can expose without changing Lambda code

The verified Lambda application version `0.3.0` contains 31 HTTP routes, while the current GPT Action schema exposes 28 operations.

These three Lambda routes already exist but are not part of the current v0.2.1 GPT Action schema:

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/health` | Return wrapper service/version/owner health information |
| `DELETE` | `/repos/{repo}/branches/{branch_name:path}` | Delete a repository branch; backend refuses to delete the repository default branch |
| `GET` | `/repos/{repo}/artifacts/{artifact_id}` | Retrieve metadata for a workflow-run artifact |

Adding these operations to a GPT Action requires an OpenAPI schema change but no Lambda source-code change.

### Important compatibility rule

Do not replace the working 28-operation schema immediately.

Instead:

1. keep a copy of the known-working v0.2.1 schema;
2. edit only a duplicate;
3. add one operation at a time;
4. validate the schema in the GPT editor;
5. test the new operation in `director-test`;
6. keep the change only after existing operations still work.

That makes rollback as simple as restoring the previously working schema.

## Optional operation 1 — Health

The existing Lambda health route is:

```text
GET /health
```

It returns basic information similar to:

```text
service = github-gpt-wrapper
version = 0.3.0
owner = configured GitHub owner
```

Unlike the protected GitHub routes, the current application source does not require `X-API-Key` on `/health`.

This route is useful for diagnostics but does not add repository functionality.

## Optional operation 2 — Branch deletion

The existing Lambda branch-deletion route can delete a non-default branch.

The backend explicitly refuses to delete the repository's default branch.

Use branch deletion only after confirming the branch name and whether any unmerged work is still needed. A deleted branch should not be used as a routine cleanup test against an important repository.

For the first test:

1. create a disposable branch in `director-test`;
2. confirm the branch exists;
3. call the branch-delete operation;
4. confirm the branch disappears;
5. confirm `main` remains intact.

## Optional operation 3 — Artifact metadata

The existing artifact route returns metadata for a specific GitHub Actions artifact ID.

This complements the currently exposed operation that lists artifacts for a workflow run.

A safe test requires a workflow that actually produced an artifact:

1. use `listWorkflowRunArtifacts` to obtain an artifact ID;
2. call the added artifact-metadata operation with that ID;
3. compare the result with GitHub's Actions interface.

Do not invent an artifact ID or use an unrelated production workflow solely for this test.

## Level 2 — New AWS-service control is a separate extension

Amazon S3, Step Functions, CloudWatch, invoking other Lambda functions, and similar AWS-service operations are **not** part of the verified GitHub wrapper Action contract documented by the core guide.

Adding them requires at least:

```text
new API routes
new request/response models
new AWS SDK calls
new IAM permissions
new Action schema operations
new tests
new security boundaries
```

For that reason, do not add broad AWS permissions to `github-gpt-wrapper` merely to make experimentation convenient.

## Recommended architecture for new AWS capabilities

The simplest low-risk extension is to keep the proven GitHub wrapper unchanged and create a **separate Lambda + separate GPT Action** for AWS operations.

That preserves the working GitHub path:

```text
GPT
  ├── GitHub Action → existing github-gpt-wrapper Lambda → GitHub
  └── AWS Action    → separate AWS-control Lambda → selected AWS services
```

Benefits:

- GitHub code and permissions remain unchanged;
- AWS permissions can be limited to the exact service/resources needed;
- failures in a new S3 feature do not require modifying the known-working GitHub wrapper;
- the new Action can be tested and removed independently;
- logs and troubleshooting remain easier to separate.

This is an architectural extension, so decide its scope before implementation.

## First AWS extension to consider — S3

Amazon S3 is a practical first extension because many data-pipeline projects need to inspect or move files in object storage.

Before building an S3 Action, decide exactly which operations are required.

For a beginner-friendly first version, a narrow capability set could be:

```text
list approved buckets or use one configured bucket
list objects under a prefix
get object metadata
read small text objects
upload a supplied text object
```

Do not begin with unrestricted delete, bucket-policy, public-access, replication, lifecycle, encryption-policy, or cross-account administration operations.

Those capabilities materially increase the security and recovery burden.

## S3 decisions required before implementation

Answer these questions first:

1. Should the Action access one S3 bucket or multiple buckets?
2. Should the bucket name be fixed in Lambda configuration, or supplied by the GPT?
3. Should it be read-only initially, or read/write?
4. What object prefixes should be accessible?
5. What maximum object size should the Action read or write directly?
6. Should delete operations exist at all?
7. Does the data contain private or regulated information that should not pass through ChatGPT?
8. Which AWS region contains the bucket?

Do not implement IAM policy until these questions have answers.

## Safer first S3 design

For a personal beginner build, the narrowest useful design is usually:

```text
one configured bucket
one configured prefix
list/read metadata
small text-file read/write only
no delete operation
no bucket-policy modification
no public-access modification
```

The Lambda execution role can then be restricted to only the object operations and resources required by that design.

## Why not attach broad AWS administrator access?

A Lambda function only needs the permissions required for its code.

Giving the Lambda broad administrator permissions would make an application bug, leaked Action credential, or mistaken GPT request much more consequential than necessary.

Do not attach `AdministratorAccess` merely because it avoids an IAM error.

If an AWS call returns `AccessDenied`, treat the exact denied action/resource as evidence and decide whether that permission is genuinely part of the intended feature before adding it.

## Other reasonable future extensions

After a separate AWS Action is working and tested, possible additions include:

### Invoke a specific Lambda function

Useful when another Lambda already performs a known job. Restrict invocation to explicit approved function ARNs rather than all Lambda functions.

### Start or inspect a specific Step Functions state machine

Useful for data pipelines. Keep start/read operations scoped to explicitly approved state machines.

### Read CloudWatch Logs for selected workloads

Useful for troubleshooting. Begin read-only and restrict log groups rather than granting general CloudWatch administration.

### Read selected AWS service configuration

Read-only inventory endpoints can be useful before adding mutation operations.

Each new service should have its own test repository/workload or other disposable test target where practical.

## What counts as an easy addition?

For this guide, an addition is considered low-risk only when it meets all of these conditions:

```text
existing backend behavior already verified
no new IAM permission required
no new credential required
no change to existing GitHub operations
reversible by restoring the previous Action schema
can be tested on disposable data
```

The three existing unexposed wrapper routes meet most of that standard.

A new S3 integration does **not**. It is useful, but it is a real new component and should be built as a separately planned extension.

## What you should see

After a Level 1 schema-only extension, the original 28 operations should still work and the added route should work in isolation.

After any future separate AWS Action is built, the GPT editor should show two distinct external systems:

```text
GitHub Action → github-gpt-wrapper
AWS Action → separate AWS-control Lambda
```

A failure in one should not require changing the other's credentials or permissions.

## If you do not see this

- If the GPT schema stops validating after a Level 1 addition, restore the known-working schema and re-add only the failing operation.
- If an existing GitHub operation stops working after a schema edit, restore the original v0.2.1 schema before changing Lambda.
- If a new AWS Lambda returns `AccessDenied`, identify the exact AWS API action and resource before modifying IAM.
- If a proposed fix requires broad IAM permissions, stop and narrow the design first.
- If S3 data is too large or sensitive to pass through the GPT Action safely, redesign the workflow rather than increasing limits blindly.

## Ask ordinary ChatGPT this

```text
I have a working custom GPT → AWS Lambda → GitHub integration and I want to extend it without breaking the existing GitHub wrapper.

Extension I want: [existing health / branch-delete / artifact-metadata route, or new AWS service]
Current GitHub integration status: working
Does this require new Lambda code? [yes/no/unknown]
Does this require new IAM permissions? [yes/no/unknown]
Exact sanitized error if one exists: [paste it]

Preserve the existing GitHub wrapper unless the extension absolutely requires changing it. Do not ask for API keys, GitHub tokens, AWS credentials, secret values, or private data. If this is a new AWS-service capability, first help me define the smallest operation set and IAM boundary before writing implementation steps.
```

## Source of truth

Existing unexposed routes are verified from [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }}).

New S3 and other AWS-service integrations described here are **proposed extension patterns**, not claims about the currently verified High Director GitHub wrapper.
