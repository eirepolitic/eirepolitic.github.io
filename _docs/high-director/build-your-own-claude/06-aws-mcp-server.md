---
title: Build Your Own Sly Director — 06 — Connect AWS MCP
summary: Connect Claude to AWS using the dedicated sly-director-admin identity.
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

Give Sly Director direct AWS tools.

AWS MCP is a managed AWS service that lets Claude call AWS APIs using the permissions of the AWS identity you sign in with.

This guide uses the `sly-director-admin` user created in Chapter 4.

## Step 1 — Make sure you are signed in as the right AWS user

1. Sign out of any AWS root session.
2. Open the IAM sign-in URL you saved in Chapter 4.
3. Sign in as:

```text
sly-director-admin
```

4. Leave that AWS tab open.

## Step 2 — Add AWS MCP to Claude

1. Open **Claude → Customize → Connectors**.
2. Select **Add custom connector**.
3. Name it:

```text
AWS MCP
```

4. For the remote MCP server URL, enter:

```text
https://aws-mcp.us-east-1.api.aws/mcp
```

5. Save/add the connector.
6. Select **Connect**.
7. When AWS opens, confirm you are signing in as `sly-director-admin`.
8. Approve the AWS authorization.
9. Return to Claude.

The AWS MCP server itself is in `us-east-1`. That does not move your resources; your Lambda can remain in `us-east-2`.

## Step 3 — Verify the AWS identity

1. Open **Projects → Sly Director**.
2. Start a normal chat.
3. Enable **AWS MCP** from the connector menu.
4. Send:

```text
Using AWS MCP, inspect the AWS account without making any changes.

Report:
- the AWS account ID
- the AWS identity ARN you are using
- available AWS regions
- S3 buckets
- Lambda functions in us-east-2
- details for sly-director-github-mcp if present

Do not create, update, or delete anything.
```

5. Confirm the identity ARN contains:

```text
user/sly-director-admin
```

It should not say `root`.

6. Confirm the `sly-director-github-mcp` Lambda is **Active** and uses:

```text
src.lambda_entry.handler
```

## Step 4 — Check that the GitHub connector requires login

The Lambda Function URL is public so Claude can discover the OAuth information, but the actual `/mcp` endpoint must reject requests that are not signed in.

1. Open AWS CloudShell.
2. Paste:

```bash
curl -i \
  -X POST \
  -H 'content-type: application/json' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"unauthenticated-check","version":"1"}}}' \
  "$(aws lambda get-function-url-config --function-name sly-director-github-mcp --region us-east-2 --query FunctionUrl --output text --no-cli-pager)mcp"
```

3. Confirm the response begins with:

```text
HTTP/1.1 401 Unauthorized
```

and includes an authentication-required message.

That confirms AuthKit is protecting the GitHub connector.

You now have both primary connections:

```text
Sly Director GitHub: connected
AWS MCP: connected
```

Continue to [Chapter 7 — Test Sly Director in Cowork]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }}).
