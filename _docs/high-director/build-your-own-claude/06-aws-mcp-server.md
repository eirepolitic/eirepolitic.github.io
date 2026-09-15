---
title: Build Your Own Sly Director — 06 — Connect AWS MCP
summary: Connect Sly Director to the managed AWS MCP Server using browser OAuth.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 86
permalink: /docs/high-director/build-your-own-claude/06-aws-mcp-server/
---

# Chapter 6 — Connect AWS MCP

## Goal

Give the **Sly Director Project** direct AWS tools in addition to the **Sly Director GitHub** connector built in Chapter 5.

## Step 1 — Check which AWS identity will authorize the connector

Open AWS CloudShell and run:

```bash
aws sts get-caller-identity \
  --query Arn \
  --output text \
  --no-cli-pager
```

If the result is an IAM user or role, that identity must be allowed to perform the AWS Sign-In OAuth actions used by AWS MCP. The simplest supported setup is to attach the AWS managed policy:

```text
AWSMCPSignInOAuthAccessPolicy
```

That policy grants the OAuth authorization/token permissions required by AWS MCP. It does **not** give the identity extra permissions to AWS services; AWS MCP continues to use the identity's existing IAM permissions for AWS API calls.

If the result is the AWS account **root user**, AWS documents that no additional IAM permission is required for the OAuth flow.

Do not use root for normal autonomous Sly Director operation. AWS MCP uses the permissions of the signed-in AWS identity, so a root connection would give the agent root-level AWS authority. Create or use a scoped IAM identity before substantial Cowork automation.

## Step 2 — Add the AWS MCP connector

1. Open Claude.
2. Open **Customize → Connectors**.
3. Select **Add custom connector**.
4. Enter:

```text
Name: AWS MCP
Remote MCP server URL: https://aws-mcp.us-east-1.api.aws/mcp
```

5. Set **Authentication type** to:

```text
OAuth
```

6. Set **OAuth client** to:

```text
Register automatically
```

7. Leave optional Client ID/Secret fields empty.
8. Save the connector.
9. Open **Projects → Sly Director**.
10. Start a new chat.
11. Select **+ → Connectors**.
12. Enable **AWS MCP**.
13. Ask:

```text
Using the AWS connector, identify the AWS account and AWS identity available to you.
```

14. Complete the AWS authorization flow when it opens.
15. Return to Claude and ask:

```text
Using AWS MCP, list the S3 buckets visible to this AWS identity and tell me which AWS identity you are using.
```

## What you should see

Sly Director should identify the AWS account/identity and return the visible S3 buckets. An empty list is still a successful connection.

At this point Sly Director has both primary tool connections:

```text
Sly Director GitHub: connected
AWS MCP: connected
```

Continue to [Chapter 7 — Configure Cowork]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }}).

<details>
<summary>Why the AWS MCP endpoint is us-east-1</summary>

AWS currently publishes the managed AWS MCP Server in US East (N. Virginia), `us-east-1`, and Europe (Frankfurt), `eu-central-1`.

The MCP server endpoint region is separate from the region where your normal AWS resources run. This guide's existing Lambda workload can remain in `us-east-2`.

</details>

<details>
<summary>If the AWS authorization page does not open</summary>

Edit/re-add the connector using:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

Keep:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

</details>

<details>
<summary>Why not use the root user for Cowork</summary>

AWS MCP forwards operations using the permissions of the AWS identity that authorized the connection. Root therefore has effectively unrestricted account authority.

Use root only, if necessary, for a short connector verification. Before allowing Cowork to perform substantial AWS work, reconnect AWS MCP using a dedicated IAM identity with only the permissions Sly Director actually needs.

</details>
