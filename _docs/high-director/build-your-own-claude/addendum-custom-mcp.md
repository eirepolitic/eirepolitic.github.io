---
title: "Build Your Own High Director — Claude Edition — Addendum B: Custom MCP"
summary: Build a custom remote MCP server only when an existing connector or Claude Code cannot provide the needed capability.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 92
permalink: /docs/high-director/build-your-own-claude/addendum-custom-mcp/
---

# Addendum B — Custom MCP Servers

## Goal

Decide whether a custom MCP server is actually needed before building one.

## Complete this step

1. Write down the exact capability Claude needs.
2. Check whether it is already available through:

```text
Claude Code
an official Claude connector
an existing remote MCP connector
AWS managed MCP Server
```

3. If none of those provide the capability, define:

```text
required operations
read vs write operations
authentication method
hosting location
permissions
cost
logging
```

4. Build and test the custom MCP server separately from the existing GitHub and AWS integrations.
5. Add it in Claude through **Customize → Connectors → Add custom connector**.
6. Test one harmless operation first.

## What you should see

The custom MCP server should appear as its own connector and remain independent from Claude Code and AWS MCP.

<details>
<summary>Additional information</summary>

A custom MCP server adds hosting, authentication, network exposure, tool schemas, authorization logic, monitoring, and maintenance.

Use it only when the required capability is unavailable through the simpler options above.

A sensible test order is:

```text
connectivity
→ authentication
→ harmless read
→ normal read operations
→ disposable write
→ verification
```

The original ChatGPT High Director Lambda wrapper should be treated as a separate implementation rather than something that must be ported into Claude.

</details>

<details>
<summary>Planning prompt</summary>

```text
I have a working Claude High Director setup using Claude Code for GitHub and AWS MCP for AWS.
Missing capability: [describe]
Check whether an existing connector or MCP service already provides it. If not, define the smallest custom MCP design, authentication model, permissions, hosting choice, cost, and test plan.
```

</details>
