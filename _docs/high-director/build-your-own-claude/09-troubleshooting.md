---
title: Build Your Own Sly Director — 09 — Troubleshooting
summary: Troubleshoot Sly Director one connector, authentication, permission, or execution layer at a time.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 89
permalink: /docs/high-director/build-your-own-claude/09-troubleshooting/
---

# Chapter 9 — Troubleshooting

## Goal

Fix the failing layer without redesigning the whole system.

## Complete this step

1. Copy the exact non-secret error.
2. Identify the failing layer:

```text
Sly Director Project instructions
Cowork
Sly Director GitHub connector
Cognito OAuth/login
Lambda / MCP service
GitHub token permissions
GitHub repository rules
GitHub Actions
AWS MCP
AWS OAuth
AWS service permission
```

3. Fix only that layer.
4. Retry the same operation.
5. Confirm the result before changing anything else.

## Quick fixes

### Sly Director GitHub is missing from the chat

1. Open **Customize → Connectors**.
2. Confirm **Sly Director GitHub** exists and is connected.
3. Return to the Sly Director chat or Cowork task.
4. Select **+ → Connectors**.
5. Enable **Sly Director GitHub**.

### The GitHub connector does not open or respond

Open the Lambda health URL from Chapter 5:

```text
https://YOUR-FUNCTION-URL/health
```

If the health page fails, open:

```text
AWS → Lambda → sly-director-github-mcp → Monitor → View CloudWatch logs
```

Inspect the newest error.

### Claude authentication fails

Check the Cognito app client:

```text
Callback URL: https://claude.ai/api/mcp/auth_callback
OAuth flow: Authorization code grant
Scope: openid
```

Then confirm Claude's custom connector contains the same Cognito Client ID and Client secret.

### The connector returns HTTP 421

Open:

```text
AWS → Lambda → sly-director-github-mcp → Configuration → Environment variables
```

Confirm `PUBLIC_MCP_URL` exactly equals the Function URL plus `/mcp`.

Example:

```text
https://abc123.lambda-url.us-east-2.on.aws/mcp
```

### GitHub returns 403

Open GitHub's fine-grained token settings and check:

1. `claude-director-test` is one of the selected repositories.
2. The token has the repository permissions from Chapter 5.
3. The token has not expired.

### GitHub returns 404 for a private repository

A private repository that is missing from the fine-grained token's repository list can appear unavailable. Add the repository to the token's allowed repositories and retry.

### Workflow-file changes fail

Confirm the GitHub token has:

```text
Workflows: Read and write
Contents: Read and write
```

### Cowork stops unnecessarily

Check whether Cowork actually needs a decision. If it is only reporting progress, remind it:

```text
Progress updates are informational. Continue through the approved plan until the requested outcome is complete or a genuine blocker requires me.
```

If the same interruption keeps recurring, improve the Sly Director Project instructions rather than accepting the interruption as normal.

### AWS MCP will not authenticate

Confirm:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

If the AWS authorization window still does not open, retry using:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

## What you should see

You should be able to name one failing layer and correct it without changing Sly Director's basic architecture.

Continue to [Chapter 10 — Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }}).

<details>
<summary>Claude Code fallback</summary>

Use Claude Code only when a task genuinely requires a repository-development capability unavailable through Cowork plus the connected tools, such as a specific repository-local development workflow.

A Cognito, Lambda, connector, or GitHub-token problem should be fixed at that layer rather than bypassed with Claude Code.

</details>
