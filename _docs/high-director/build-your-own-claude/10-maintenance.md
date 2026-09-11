---
title: Build Your Own High Director — Claude Edition 10 — Maintenance
summary: Keep the Claude, GitHub, and AWS setup working after initial setup.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 90
permalink: /docs/high-director/build-your-own-claude/10-maintenance/
---

# Chapter 10 — Maintenance

## Goal

Keep access, costs, and repository state under control.

## Complete this step

Once a month:

1. Open Claude **Settings** and review plan/usage.
2. Open GitHub settings and review repositories available to the Claude/Anthropic GitHub App.
3. Review open Claude-created pull requests and old branches.
4. Open AWS **Billing and Cost Management**.
5. Review current charges and budget alerts.
6. Check for AWS resources from old tests that are still running.
7. Confirm the AWS MCP connector still works with a simple query.

## What you should see

You should know:

```text
which repositories Claude can access
what AWS is currently costing
which test resources are still active
whether the AWS MCP connection still works
```

The core guide is complete.

<details>
<summary>Additional information</summary>

If you use the optional IAM-role path, periodically review the policies attached to `ClaudeHighDirectorRole` and remove permissions that are no longer needed.

If a new GitHub repository does not appear in Claude Code, add it to the Claude/Anthropic GitHub App's allowed repositories.

If you stop using AWS MCP, remove or disable the connector in Claude. If you used a dedicated IAM role, you can also remove MCP-specific IAM permissions when they are no longer needed.

If you stop using this setup entirely, remove Claude's GitHub access, delete obsolete test repositories/branches, review AWS resources and billing, then downgrade Claude Pro if desired.

</details>

<details>
<summary>Maintenance prompt</summary>

```text
I maintain a Claude High Director setup using Claude Pro, Claude Code, GitHub, and AWS MCP.
Maintenance task: [review access / remove repository / review AWS cost / retire setup]
Current state: [describe]
Give me the shortest click-by-click procedure.
```

</details>
