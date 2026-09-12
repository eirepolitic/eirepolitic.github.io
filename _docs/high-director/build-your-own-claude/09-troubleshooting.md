---
title: Build Your Own Sly Director — 09 — Troubleshooting
summary: Troubleshoot Sly Director one connector or permission layer at a time.
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
GitHub MCP
GitHub repository rules/permissions
GitHub Actions
AWS MCP
AWS OAuth
AWS service permission
```

3. Fix only that layer.
4. Retry the same operation.
5. Confirm the result before changing anything else.

## Quick fixes

### Sly Director does not use GitHub tools

Confirm **GitHub MCP** is enabled and ask:

```text
Use the connected GitHub MCP tools to inspect and operate this repository directly.
```

### Cowork stops unnecessarily

Check whether it actually needs a decision or whether the Sly Director instructions/approval mode should be improved. Progress updates should not be treated as requests to continue.

### AWS MCP will not authenticate

Confirm:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

## What you should see

You should be able to identify one failing layer and correct it without changing Sly Director's basic architecture.

Continue to [Chapter 10 — Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }}).

<details>
<summary>Claude Code fallback</summary>

Use Claude Code only when a task genuinely requires a capability unavailable through Cowork plus the connected tools, such as a specific repository-local development workflow.

</details>
