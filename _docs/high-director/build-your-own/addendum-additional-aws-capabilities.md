---
title: "Build Your Own High Director — Addendum B: Additional AWS Capabilities"
summary: Extend High Director with AWS capabilities, including the verified broad-admin GitHub Actions pattern now used by the Eirepolitic deployment and narrower alternatives for personal builds.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-26
last_verified: 2026-09-26
order: 74
permalink: /docs/high-director/build-your-own/addendum-additional-aws-capabilities/
---

# Build Your Own High Director — Addendum B: Additional AWS Capabilities

## What changed

The original High Director build used two GPT Builder Actions:

- GitHub
- Google Workspace

AWS was initially documented as a future extension, with a separate narrow AWS-control service recommended for safety.

On 2026-09-26, the production High Director deployment adopted a different operational model: **broad AWS administration through GitHub Actions**.

No third GPT Builder Action was added. High Director reaches AWS indirectly through the existing GitHub integration.

## Verified production architecture

```text
High Director
  -> GitHub Action
  -> repository workflow
  -> dedicated GitHub AWS IAM user
  -> sts:AssumeRole
  -> HighDirectorAwsAdmin
  -> temporary STS credentials
  -> AWS APIs
```

The dedicated long-lived IAM user is:

`github-eirepolitic-instagram-deployer`

It assumes:

`HighDirectorAwsAdmin`

The role uses the AWS-managed policy:

`AdministratorAccess`

The bootstrap and workflow are maintained in the `Eirepolitic-data-pipeline` repository:

```text
infra/publishing/github_aws_bootstrap.yml
.github/workflows/deploy_instagram_publisher_lambda.yml
```

The bootstrap role session defaults to one hour.

## Why this pattern was chosen

The system owner explicitly wanted High Director to be able to perform nearly any AWS-related task needed in future without repeatedly returning to IAM setup.

The chosen pattern therefore optimizes for:

- broad future AWS coverage;
- reuse of the already-proven GitHub integration;
- temporary STS credentials for the actual administrative work;
- one reusable operational trust path instead of many service-specific IAM grants;
- repository-visible workflow definitions and GitHub audit history.

The long-lived GitHub access keys do **not** themselves perform broad administrative operations directly. They authenticate the dedicated IAM user, which is allowed to assume the administrator role.

## Programmatic operation selection

The current workflow supports a repository Actions variable:

`HIGH_DIRECTOR_AWS_OPERATION`

This exists because the High Director GitHub dispatch operation can dispatch a workflow and ref but cannot pass workflow inputs directly.

The workflow resolves its operation from:

1. a normal manual `workflow_dispatch` input, when supplied;
2. `HIGH_DIRECTOR_AWS_OPERATION`;
3. a non-mutating default of `infrastructure-status`.

High Director can therefore:

1. set the repository variable;
2. dispatch the workflow;
3. inspect the run/jobs;
4. diagnose/fix the repository workflow if required;
5. restore the variable to `infrastructure-status` afterward.

## Verified AWS operations

The production path was exercised successfully on 2026-09-26 for:

- assuming `HighDirectorAwsAdmin` from GitHub Actions;
- AWS caller-identity/status inspection;
- CloudFormation deployment of a DynamoDB publication ledger;
- CloudFormation deployment of EventBridge Scheduler, SQS DLQ, IAM and CloudWatch support resources;
- read-only Lambda invocation for the Instagram publisher healthcheck.

These successful operations verify the trust path itself, not only the YAML definitions.

## Broad authority does not remove approval gates

`AdministratorAccess` is a technical capability, not a blanket approval for every production action.

Project-specific approval gates still apply independently.

For example, the Instagram publishing project retains:

- Gate 4 before the first visible `/media_publish` operation;
- Gate 5 before general production scheduling/publishing enablement.

A workflow capable of performing an operation does not itself constitute approval to perform that operation.

## Security trade-off

This design is intentionally more powerful than the original narrow-extension recommendation.

The assumed role can administer sensitive AWS services including IAM and Secrets Manager. Repository/workflow compromise could therefore become AWS-account compromise within the permissions available to `HighDirectorAwsAdmin`.

The main controls are:

- dedicated GitHub deployer identity;
- `sts:AssumeRole` separation between long-lived bootstrap credentials and broad temporary credentials;
- temporary STS sessions;
- repository access controls and branch/review protections;
- GitHub workflow history;
- project approval gates;
- higher-level AWS controls such as SCPs where present;
- credential rotation for the long-lived bootstrap access keys.

Do not publish or log the long-lived keys or returned STS credentials.

## If you are building your own High Director

You do **not** need to copy the broad-admin model.

Choose between two patterns deliberately.

### Option A — narrow AWS role

Use this when:

- the system has one or two known AWS jobs;
- the account contains unrelated sensitive workloads;
- you want IAM to enforce the narrowest possible boundary;
- you do not expect the agent to perform general infrastructure administration.

Example:

```text
GitHub Actions
  -> assume project-specific deployment role
  -> limited CloudFormation/S3/Lambda permissions
```

This remains the safer default for a small personal build.

### Option B — broad operator role

Use this when:

- the system owner explicitly wants general AWS administration;
- repeated future service expansion is expected;
- repository/workflow governance is trusted as the main change-control plane;
- the owner accepts the increased blast radius.

Example:

```text
GitHub Actions
  -> dedicated bootstrap IAM user
  -> sts:AssumeRole
  -> administrator role
  -> temporary AWS session
```

The Eirepolitic High Director deployment uses this model.

## Recommended bootstrap sequence for the broad model

1. Create a dedicated IAM user for GitHub bootstrap authentication.
2. Store its access key and secret access key as repository secrets; never commit them.
3. Create an assumable role such as `HighDirectorAwsAdmin`.
4. Attach the desired broad policy to that role.
5. Restrict the IAM user to `sts:AssumeRole` for that role wherever practical.
6. In the GitHub workflow, load the bootstrap credentials.
7. Call `aws sts assume-role`.
8. mask the returned access key, secret key and session token;
9. export the temporary credentials for the remainder of the job;
10. verify the caller identity before making changes;
11. perform the intended AWS operation;
12. leave safe/non-mutating workflow defaults in place after the run.

## Do not confuse this with a direct AWS GPT integration

The current High Director AWS operator capability is not:

- an AWS MCP server connected directly to ChatGPT;
- a third GPT Builder Action;
- an AWS SDK running inside the GPT;
- an extension of the GitHub wrapper Lambda's own execution role.

The GitHub wrapper remains a GitHub integration. AWS administration happens in a separate GitHub Actions job after that job authenticates to AWS.

## Future alternatives

A direct managed AWS MCP connection may be preferable later if the ChatGPT workspace supports the required write-capable MCP mode and the operator wants to reduce reliance on bespoke GitHub workflows.

A separate narrow AWS-control Action/Lambda also remains valid when direct AWS tools are required but broad GitHub-driven administration is not acceptable.

Do not add broad AWS permissions to the existing GitHub-wrapper Lambda execution role merely for convenience. Keep the GitHub wrapper backend and the AWS operator runtime as separate trust paths.

## Canonical production reference

See [High Director AWS Operator Capability]({{ '/docs/high-director/aws-operator-capability/' | relative_url }}) for the verified production implementation and [High Director Capability and Component Inventory]({{ '/projects/high-director/capability-component-inventory/' | relative_url }}) for its current evidence classification.
