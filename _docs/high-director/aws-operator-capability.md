---
title: High Director AWS Operator Capability
summary: Verified broad AWS administration capability implemented through GitHub Actions, STS role assumption, temporary credentials, and the HighDirectorAwsAdmin role.
section: high-director
doc_type: agent
status: active
created: 2026-09-26
updated: 2026-09-26
last_verified: 2026-09-26
owner: High Director
order: 18
permalink: /docs/high-director/aws-operator-capability/
source_of_truth:
  - Eirepolitic-data-pipeline/infra/publishing/github_aws_bootstrap.yml
  - Eirepolitic-data-pipeline/.github/workflows/deploy_instagram_publisher_lambda.yml
---

# High Director AWS Operator Capability

High Director has broad AWS administrative capability through GitHub Actions.

This capability is **not** a third GPT Builder Action and is **not** a direct AWS API connector inside ChatGPT. It is an operational path layered onto the existing GitHub integration.

## Runtime path

```text
High Director
  -> GitHub repository action
  -> GitHub Actions workflow
  -> dedicated IAM user credentials
  -> sts:AssumeRole
  -> HighDirectorAwsAdmin
  -> temporary STS credentials
  -> AWS APIs
```

The long-lived GitHub credentials remain attached to the dedicated IAM user:

`github-eirepolitic-instagram-deployer`

That identity is used to assume:

`HighDirectorAwsAdmin`

The role carries the AWS-managed policy:

`AdministratorAccess`

The resulting role session uses temporary STS credentials. The default session duration configured by the bootstrap is one hour.

## Bootstrap

The one-time bootstrap is defined in:

`Eirepolitic-data-pipeline/infra/publishing/github_aws_bootstrap.yml`

The bootstrap creates:

- `HighDirectorAwsAdmin`
- a managed policy allowing the dedicated GitHub deployer user to call `sts:AssumeRole` on that role

The role trust policy permits the dedicated deployer user to assume the role.

## Workflow control

The initial broad-AWS workflow path is implemented in:

`Eirepolitic-data-pipeline/.github/workflows/deploy_instagram_publisher_lambda.yml`

That workflow:

1. loads the existing dedicated GitHub AWS access-key pair;
2. discovers the AWS account ID;
3. assumes `HighDirectorAwsAdmin`;
4. masks the returned temporary access key, secret key and session token;
5. places those temporary credentials in the job environment;
6. verifies the assumed-role identity;
7. performs the selected AWS operation.

The repository variable:

`HIGH_DIRECTOR_AWS_OPERATION`

allows High Director to select an operation programmatically when the GitHub dispatch interface cannot pass workflow inputs directly.

The default resting value is intended to be the non-mutating:

`infrastructure-status`

## Verified operations

As of 2026-09-26, the following were verified end-to-end through the assumed admin role:

- AWS identity/status inspection
- CloudFormation deployment of the Instagram publication ledger
- CloudFormation deployment of EventBridge Scheduler/SQS/CloudWatch support resources
- read-only invocation of the Instagram publisher Lambda healthcheck

This demonstrates that High Director can drive broad AWS work by creating or modifying repository workflows and dispatching them through the existing GitHub integration.

## Scope and limitations

`AdministratorAccess` gives the assumed role broad permissions across AWS services and resources within the account, subject to higher-level AWS controls such as service control policies, account restrictions and root-only operations.

High Director therefore has the technical authority to perform most AWS engineering tasks that can be expressed through GitHub Actions and the AWS CLI/SDK.

This does **not** mean every destructive or production-sensitive action is automatically approved. Project-specific approval gates still apply independently of IAM capability.

For example, the Instagram publishing project still requires explicit Gate 4 approval before the first visible `/media_publish` operation and separate Gate 5 approval before general production scheduling/publishing enablement.

## Security implications

The broad role can manage IAM, Secrets Manager and other sensitive services. This is intentional.

The security boundary is therefore primarily:

- control of the dedicated GitHub repository and workflows;
- protection of the dedicated long-lived deployer credentials;
- the `sts:AssumeRole` trust relationship;
- GitHub branch/review protections;
- project-specific approval gates;
- AWS account-level controls above IAM where present.

Because the GitHub deployer still uses long-lived access keys for bootstrap authentication, those credentials should be rotated periodically and treated as high-value credentials even though actual AWS work is performed with temporary role sessions.

## Relationship to the original GPT configuration

The original High Director GPT Builder record documented two Actions:

- GitHub
- Google Workspace

That historical record remains correct.

The AWS operator capability is a later runtime extension implemented through the GitHub Action path. Documentation should not rewrite the original Builder configuration as though an AWS Action existed there.

## Related Documents

- [High Director Overview]({{ '/projects/high-director/' | relative_url }})
- [High Director Capability and Component Inventory]({{ '/projects/high-director/capability-component-inventory/' | relative_url }})
- [High Director Security and Configuration Reference]({{ '/projects/high-director/security-configuration-reference/' | relative_url }})
- [Additional AWS Capabilities Addendum]({{ '/docs/high-director/build-your-own/addendum-additional-aws-capabilities/' | relative_url }})
