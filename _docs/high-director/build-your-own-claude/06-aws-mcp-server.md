---
title: Build Your Own Sly Director — 06 — Connect AWS MCP
summary: Connect Sly Director to the managed AWS MCP Server using a dedicated administrator IAM identity and browser OAuth.
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

This guide uses a dedicated IAM user with administrator permissions rather than authorizing Cowork as the AWS account root user.

## Step 1 — Check which AWS identity you are using now

Open AWS CloudShell and run:

```bash
aws sts get-caller-identity \
  --query Arn \
  --output text \
  --no-cli-pager
```

If this reports the AWS account root user, continue to Step 2 and create the dedicated Sly Director administrator identity.

## Step 2 — Create the Sly Director administrator IAM user

1. In the AWS console, search for **IAM** and open it.
2. Select **Users**.
3. Select **Create user**.
4. For **User name**, enter:

```text
sly-director-admin
```

5. Select **Provide user access to the AWS Management Console — optional**.
6. Select **I want to create an IAM user**.
7. Create or generate a console password and store it privately. Do not paste the password into Claude, ChatGPT, GitHub, or the documentation.
8. On **Set permissions**, choose **Attach policies directly**.
9. Select:

```text
AdministratorAccess
AWSMCPSignInOAuthAccessPolicy
```

10. Continue to **Review and create**.
11. Select **Create user**.
12. Save the IAM user's sign-in URL, username, and password privately.

`AdministratorAccess` grants full IAM-authorized access to AWS services and resources. Some account actions remain root-only by AWS design, so this identity is not literally the root user.

`AWSMCPSignInOAuthAccessPolicy` grants the OAuth authorization/token actions used by AWS MCP. No access keys are required for this browser OAuth setup.

## Step 3 — Add the AWS MCP connector

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

14. When AWS authorization opens, sign in as the IAM user:

```text
sly-director-admin
```

Do not authorize the connector using the root user.

15. Complete the AWS authorization flow.
16. Return to Claude and ask:

```text
Using AWS MCP, list the S3 buckets visible to this AWS identity and tell me which AWS identity you are using.
```

## What you should see

Sly Director should identify an IAM user similar to:

```text
arn:aws:iam::<account-id>:user/sly-director-admin
```

It should also be able to query AWS resources allowed by `AdministratorAccess`.

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
<summary>Why use an administrator IAM user instead of root</summary>

`AdministratorAccess` grants all IAM-authorized actions on all AWS services and resources. AWS still reserves a small set of account-level actions for the root user.

Using a dedicated IAM identity prevents the connector from authenticating as root while still providing the broad AWS API authority required by this Sly Director configuration.

</details>
