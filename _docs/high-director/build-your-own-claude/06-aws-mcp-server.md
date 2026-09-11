---
title: Build Your Own High Director — Claude Edition 06 — AWS MCP Server
summary: Connect Claude Pro to the managed AWS MCP Server using a remote custom connector and browser OAuth, then verify safe AWS read access.
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

Connect the High Director Claude Project to AWS without deploying your own MCP server, Lambda gateway, or local proxy.

AWS documents the managed AWS MCP Server as available at no additional charge. You still pay normal AWS charges for resources Claude creates or uses.

## Step 1 — Confirm the managed endpoint

AWS's managed MCP endpoint format is region-specific. For the AWS MCP Server endpoint documented for `us-east-1`, AWS currently uses:

```text
https://aws-mcp.us-east-1.api.aws/mcp
```

AWS documentation states that you may use the endpoint for your preferred supported MCP Server region. The MCP Server region is the server endpoint location; it does not force every downstream AWS resource to be in that same region.

Official reference: [OAuth authentication for AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/oauth-authentication.html).

For the first setup, use the endpoint currently shown by AWS's setup documentation unless AWS has changed it.

## Step 2 — Open Claude Connectors

1. Open Claude in your browser.
2. Open **Customize** or the current customization area.
3. Select **Connectors**.
4. Select **+**.
5. Select **Add custom connector**.

Anthropic currently documents this path for individual Pro and Max users.

## Step 3 — Add the AWS MCP Server URL

In the connector URL field, paste the AWS MCP Server endpoint from the current AWS documentation.

For the currently documented `us-east-1` endpoint:

```text
https://aws-mcp.us-east-1.api.aws/mcp
```

Do not enter an AWS password, access key, or secret key in the connector URL.

If Claude offers optional OAuth Client ID/Secret fields, leave them empty for the normal AWS-managed discovery flow unless current AWS/Anthropic documentation specifically instructs otherwise.

Name the connector something recognizable if Claude offers a name field:

```text
AWS MCP
```

Select **Add**.

## Step 4 — Enable the connector in a High Director chat

1. Open your **High Director** project.
2. Start a new chat.
3. Select the **+** button near the message field.
4. Open **Connectors**.
5. Enable **AWS MCP**.

## Step 5 — Trigger the OAuth flow with a harmless request

Ask:

```text
Using the AWS connector, identify the AWS account/identity context available to you and tell me which AWS region I asked you to prefer. Do not create, modify, or delete any AWS resource.
```

The first tool use should cause an AWS authorization/sign-in flow if the connector is not already authorized.

## Step 6 — Complete AWS Sign-in

When AWS opens:

1. Confirm you are signing in to the intended AWS account.
2. Authenticate normally.
3. Review the consent/authorization screen.
4. Authorize the connection only if it is clearly for the AWS MCP Server and the account is correct.
5. Return to Claude.

AWS states that OAuth tokens are short-lived and that the browser flow relies on your existing IAM identity and permissions.

## Step 7 — If AWS reports missing OAuth-sign-in permission

AWS currently documents these permissions as prerequisites for the OAuth connection:

```text
signin:AuthorizeOAuth2Access
signin:CreateOAuth2Token
```

AWS provides a managed policy named:

```text
AWSMCPSignInOAuthAccessPolicy
```

Do not attach that policy preemptively if the connection already works.

If the exact AWS error says the identity lacks the OAuth-sign-in permission:

1. preserve the exact error;
2. open AWS IAM;
3. identify the IAM user/role you are actually using;
4. add the AWS-documented OAuth access policy only if you are authorized to manage that identity and the permission is genuinely missing;
5. retry the connection.

Do not attach `AdministratorAccess` to solve an OAuth permission error.

## Step 8 — Test AWS documentation/knowledge access first

Ask:

```text
Using the AWS connector, explain what Amazon S3 is and identify the AWS region us-east-2. Do not call any resource-changing API.
```

The managed MCP Server includes AWS knowledge capabilities that can be used without creating resources.

## Step 9 — Test a read-only account/resource query

Ask a query appropriate to resources you already have. For a new account, use something such as:

```text
Using the AWS connector, check whether I currently have any S3 buckets visible to this AWS identity. Do not create or modify anything.
```

If there are none, a result showing no buckets is a successful connection test.

## Step 10 — Do not begin with resource creation

Before letting Claude create S3 buckets, Lambda functions, databases, or other resources, first verify:

```text
correct AWS account
correct connector
read-only query works
cost implications understood
intended AWS region known
```

The MCP Server can reach AWS APIs allowed by your IAM identity. Treat it like a powerful cloud interface, not a read-only documentation plugin.

## What you should see

You should have an **AWS MCP** custom connector in Claude, successfully authenticated through AWS Sign-in, with a harmless read-only AWS query working.

## If you do not see this

Use the error layer:

- Claude cannot add the URL → check custom connector support and the current endpoint.
- OAuth never starts → check the MCP URL and current Claude connector behavior.
- AWS returns authorization error for OAuth → check the two documented `signin:` permissions.
- OAuth succeeds but AWS API calls return `AccessDenied` → investigate the specific downstream AWS permission, not connector authentication.
- AWS call works but returns no resources → that may simply be the correct state of the account.

## Ask ordinary Claude or ChatGPT this

```text
I am connecting Claude Pro to the AWS managed MCP Server using a remote custom connector and browser OAuth.

I am not using AWS access keys, a local proxy, or a custom Lambda gateway.
Failing stage: [add connector / OAuth sign-in / OAuth permission / AWS API call]
Exact sanitized error: [paste it]

Do not ask for AWS credentials or tokens. Distinguish connector/OAuth failure from downstream IAM AccessDenied. Use current AWS MCP Server and Claude custom connector documentation and give me the smallest browser-only fix first.
```

## Next chapter

Continue to [Chapter 7 — End-to-end testing]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }}).
