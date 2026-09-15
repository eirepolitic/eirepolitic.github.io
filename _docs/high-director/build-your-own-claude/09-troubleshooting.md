---
title: Build Your Own Sly Director — 09 — Troubleshooting
summary: Fix the small set of problems seen during the live-verified Sly Director build.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 89
permalink: /docs/high-director/build-your-own-claude/09-troubleshooting/
---

# Chapter 9 — Troubleshooting

Use this page only when the main guide does not behave as expected.

## GitHub connector briefly says `not_connected`

This can happen while Claude or Cowork is loading the remote connector.

1. Wait about 30 seconds.
2. Refresh/retry the connector tools.
3. Run the same request again.

If it still fails, open **Claude → Customize → Connectors** and confirm **Sly Director GitHub** shows connected.

## Claude says `No approval received.`

A tool call may occasionally return:

```text
No approval received.
```

If the previous connector calls worked, retry the same call once. During live testing, an immediate retry succeeded.

## WorkOS login only offers SSO

1. Open WorkOS **Production**.
2. Press **Ctrl+K** and search for **Authentication**.
3. Confirm **Email + Password** is enabled.
4. Confirm **Sign up** is enabled.
5. Save changes.
6. Return to Claude and select **Connect** again.

Your WorkOS Dashboard login is separate from the AuthKit user used by the connector.

## Claude authorizes successfully but the GitHub connector fails immediately afterward

First confirm the Lambda is using the current handler:

1. AWS → **Lambda → sly-director-github-mcp**.
2. Open **Code → Runtime settings**.
3. Confirm:

```text
src.lambda_entry.handler
```

If the handler is different, return to Chapter 5 and redeploy the current connector package.

## AWS MCP signs in with the wrong identity

1. Delete/disconnect the AWS MCP connector in Claude.
2. Sign out of the AWS root account.
3. Sign in to AWS as:

```text
sly-director-admin
```

4. Re-add/reconnect AWS MCP.
5. Ask Claude to report its AWS identity ARN.
6. Confirm it contains `user/sly-director-admin`.

## AWS MCP authorization does not start

Edit/re-add the connector using:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

Then connect again while signed in as `sly-director-admin`.

## GitHub token stops working

Fine-grained GitHub tokens can expire.

1. Create a replacement token with the same repository and permissions from Chapter 5.
2. Open AWS → **Lambda → sly-director-github-mcp → Configuration → Environment variables → Edit**.
3. Replace only `GITHUB_TOKEN`.
4. Save.
5. Re-test the GitHub connector in Claude.

Do not print or paste the token into chat.

## Need the Lambda error log

Open AWS CloudShell and run:

```bash
aws logs tail /aws/lambda/sly-director-github-mcp \
  --since 10m \
  --region us-east-2 \
  --format short \
  --no-cli-pager
```

Copy only the error text you need for troubleshooting. Do not share secrets if any appear.

Continue to [Chapter 10 — Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }}).
