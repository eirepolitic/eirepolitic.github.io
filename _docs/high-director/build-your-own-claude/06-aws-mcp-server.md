---
title: Build Your Own High Director — Claude Edition 06 — AWS MCP Server
summary: Connect Claude Pro to the managed AWS MCP Server using a remote custom connector, browser OAuth, and the AWS identity or role prepared in Chapter 5.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 86
permalink: /docs/high-director/build-your-own-claude/06-aws-mcp-server/
---

# Chapter 6 — Connect Claude to the AWS MCP Server

## Goal

Connect the High Director Claude Project to AWS using the managed AWS MCP Server and the AWS identity prepared in Chapter 5.

AWS documents the managed AWS MCP Server as available at no additional charge. Normal AWS resource charges still apply to services Claude creates or uses.

## Step 1 — Confirm which AWS identity Claude will use

Use the path you selected in Chapter 5.

### Path A — Existing IAM identity

Remain signed in with the IAM user, IAM Identity Center identity, or federated role whose AWS permissions you want Claude to inherit.

That identity needs:

```text
AWSMCPSignInOAuthAccessPolicy
+ the AWS service permissions Claude needs
```

### Path B — `ClaudeHighDirectorRole`

Switch into the role before starting OAuth:

1. Open the AWS console.
2. Select the account/identity menu in the upper-right corner.
3. Select **Switch role** or **Add session → Switch role**.
4. Enter your 12-digit AWS account ID.
5. Enter:

```text
ClaudeHighDirectorRole
```

6. Select **Switch Role**.
7. Confirm the upper-right AWS menu now identifies the role session.

The OAuth session will use the permissions of the active AWS identity/role.

## Step 2 — Add the MCP OAuth policy to an existing IAM user if needed

Skip this step if:

- you created `ClaudeHighDirectorRole` in Chapter 5; or
- your existing identity already has `signin:AuthorizeOAuth2Access` and `signin:CreateOAuth2Token`.

For a normal IAM user:

1. Open **AWS Console → IAM**.
2. Select **Users**.
3. Select the IAM user that will authorize Claude.
4. Open **Permissions**.
5. Select **Add permissions**.
6. Choose **Attach policies directly**.
7. Search for:

```text
AWSMCPSignInOAuthAccessPolicy
```

8. Select the policy checkbox.
9. Select **Next** or **Add permissions**, depending on the current IAM screen.
10. Confirm the policy is listed under the user's permissions.

For an IAM Identity Center or federated identity, grant the equivalent AWS managed policy/action through the permission set or identity mechanism that controls that session.

## Step 3 — Confirm the managed MCP endpoint

AWS's managed MCP endpoint is region-specific. AWS currently documents this `us-east-1` endpoint:

```text
https://aws-mcp.us-east-1.api.aws/mcp
```

Official reference: [OAuth authentication for AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/oauth-authentication.html).

The MCP Server endpoint region and the region of the AWS resources Claude operates can be different.

## Step 4 — Open Claude Connectors

1. Open normal Claude in your browser.
2. Open **Customize** or the current customization area.
3. Select **Connectors**.
4. Select **+**.
5. Select **Add custom connector**.

## Step 5 — Add the AWS MCP Server

1. In the connector URL field, enter:

```text
https://aws-mcp.us-east-1.api.aws/mcp
```

2. If Claude offers optional OAuth Client ID/Secret fields, leave them empty for the AWS-managed OAuth discovery flow unless current AWS/Anthropic documentation specifically requires values.
3. Name the connector:

```text
AWS MCP
```

4. Select **Add**.

If the OAuth flow fails to start with the normal endpoint, AWS documents this compatibility endpoint for clients that need an explicit OAuth trigger:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

## Step 6 — Enable the connector in High Director

1. Open the **High Director** Project in normal Claude.
2. Start a new chat.
3. Select the **+** button near the message field.
4. Open **Connectors**.
5. Enable **AWS MCP**.

## Step 7 — Trigger AWS OAuth

Ask:

```text
Using the AWS connector, identify the AWS account and IAM identity/role available to you, and tell me which AWS region I asked you to prefer.
```

The first AWS MCP tool use should open AWS Sign-in/authorization.

## Step 8 — Complete AWS authorization

When AWS opens:

1. Confirm the AWS account is the one from Chapter 5.
2. Confirm the active identity matches the path you chose:

```text
existing IAM identity
or
ClaudeHighDirectorRole
```

3. Authenticate if AWS requests it.
4. Review the consent screen.
5. Authorize the AWS MCP connection.
6. Return to Claude.

AWS issues short-lived OAuth tokens and continues to enforce the IAM permissions of the identity/role that authorized the session.

## Step 9 — Test the initial permissions

### If you used `ClaudeHighDirectorRole`

The role was configured with `AmazonS3ReadOnlyAccess`, so ask:

```text
Using the AWS connector, list the S3 buckets visible to this AWS identity and identify the current AWS identity/role.
```

A result showing zero buckets is still a successful permission test when the account contains no buckets.

### If you used an existing IAM identity

Ask for a resource query that matches permissions the identity already has. For example:

```text
Using the AWS connector, list the S3 buckets visible to this AWS identity and identify the current AWS identity/role.
```

## Step 10 — Understand OAuth errors vs AWS-service errors

### OAuth permission error

If AWS reports that the identity lacks:

```text
signin:AuthorizeOAuth2Access
signin:CreateOAuth2Token
```

verify that `AWSMCPSignInOAuthAccessPolicy` is attached to the active identity/role.

### `AccessDenied` after OAuth succeeds

OAuth is working. The active AWS identity/role is missing permission for the requested downstream AWS action.

For a dedicated role:

1. Open **IAM → Roles → ClaudeHighDirectorRole**.
2. Open **Permissions**.
3. Select **Add permissions → Attach policies**.
4. Add the policy corresponding to the service Claude needs.
5. Retry the original operation.

Examples:

```text
S3 operations          → AmazonS3FullAccess
Lambda operations      → AWSLambda_FullAccess
CloudWatch operations  → CloudWatchFullAccessV2
Step Functions         → AWSStepFunctionsFullAccess
```

For tighter control, replace broad service policies with customer-managed policies scoped to specific actions/resources once the required operation is known.

## Step 11 — `iam:PassRole` when AWS services need execution roles

Some AWS services create resources that run under their own IAM execution role. Lambda and Step Functions are common examples.

In those cases the Claude identity may also need:

```text
iam:PassRole
```

on the specific execution role being assigned to the AWS service.

Treat the **ClaudeHighDirectorRole** and a service's **execution role** as different roles:

```text
ClaudeHighDirectorRole
→ what Claude itself may do through AWS MCP

Lambda/Step Functions execution role
→ what the deployed AWS workload may do while it runs
```

The relevant AWS service policy may already include appropriately scoped `iam:PassRole`; when an `AccessDenied` error names `iam:PassRole`, use the named execution role to scope the permission.

## Step 12 — Verify the connection

Confirm:

```text
correct AWS account
correct IAM identity/role
AWS MCP connector connected
OAuth succeeds
initial AWS resource query succeeds
preferred workload region recorded as us-east-2
```

## What you should see

Claude should be able to identify the AWS account and active identity/role and successfully perform an AWS query allowed by that identity.

If you used the dedicated role, the identity should resolve to a session based on:

```text
ClaudeHighDirectorRole
```

## If you do not see this

Use the failing layer:

- connector URL rejected → check the current AWS MCP endpoint;
- OAuth never starts → try AWS's documented `?oauth=initialize` compatibility endpoint;
- OAuth permission denied → check `AWSMCPSignInOAuthAccessPolicy` on the active identity/role;
- role switch denied → check role trust plus the user's `sts:AssumeRole` policy;
- OAuth succeeds and service call returns `AccessDenied` → add the permission for the specific AWS action/service to the active identity/role;
- correct query returns zero resources → verify account, region, and whether the resources exist.

## Ask ordinary Claude or ChatGPT this

```text
I am connecting Claude Pro to the AWS managed MCP Server using browser OAuth.

AWS identity path: [existing identity / ClaudeHighDirectorRole]
Active identity/role: [name]
Failing stage: [switch role / add connector / OAuth / AWS service call / iam:PassRole]
Exact sanitized AWS error: [paste it]

Identify whether the failure is role assumption, AWS MCP OAuth, or downstream AWS service authorization. Give me exact AWS-console steps for the smallest required permission change.
```

## Next chapter

Continue to [Chapter 7 — End-to-end testing]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }}).
