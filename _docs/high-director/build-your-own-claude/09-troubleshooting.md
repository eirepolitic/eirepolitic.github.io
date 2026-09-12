---
title: Build Your Own High Director — Claude Edition 09 — Troubleshooting
summary: Troubleshoot the single-chat High Director setup one connector or permission layer at a time.
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

Identify the failing layer before changing the architecture.

## Complete this step

1. Copy the exact non-secret error.
2. Identify the failing layer:

```text
High Director Project instructions
GitHub MCP connector
GitHub repository permissions/rules
GitHub Actions/workflow
AWS MCP connector
AWS OAuth
AWS service permission
```

3. Fix only that layer.
4. Retry the same operation from the High Director Project chat.
5. Confirm the result before changing anything else.

## Quick fixes

### High Director does not use GitHub tools

1. Confirm **GitHub MCP** is enabled for the chat.
2. Ask explicitly:

```text
Use the connected GitHub MCP tools to inspect and operate this repository directly from this High Director chat.
```

### GitHub MCP can read but cannot write

Check the exact connector error, GitHub authorization, repository access, and repository rules.

### GitHub change is made but validation fails

Ask High Director to inspect the relevant GitHub Actions run and logs, diagnose the failure, make the correction, and rerun/observe validation where the tools permit.

### AWS MCP will not authenticate

Confirm:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

### AWS authorization page does not open

Retry the AWS connector with:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

### AWS OAuth works but an AWS operation returns AccessDenied

The connector works. The active AWS identity lacks permission for that AWS action.

## What you should see

You should be able to identify one failing connector/permission layer without moving the whole task into another Claude surface.

Continue to [Chapter 10 — Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }}).

<details>
<summary>When Claude Code is actually the right fallback</summary>

Use Claude Code when the exact failure is that GitHub MCP cannot provide a required execution capability, such as a cloned working tree or arbitrary shell/test command.

A GitHub authentication or permission problem is not, by itself, a reason to move the task to Claude Code.

</details>

<details>
<summary>Troubleshooting prompt</summary>

```text
I am troubleshooting my single-chat Claude High Director setup.
Failing layer: [Project / GitHub MCP / GitHub repository / GitHub Actions / AWS MCP / AWS OAuth / AWS permission]
Last operation that worked: [describe]
Exact non-secret error: [paste]
Expected result: [describe]
Observed result: [describe]
Keep the normal workflow inside the High Director Project chat and identify the smallest fix.
```

</details>
