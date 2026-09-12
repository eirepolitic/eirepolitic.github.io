---
title: "Build Your Own Sly Director — Custom MCP Servers"
summary: Build another custom remote MCP server only when Sly Director needs a capability not provided by the connectors already in the core setup.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 93
permalink: /docs/high-director/build-your-own-claude/addendum-custom-mcp/
---

# Custom MCP Servers

## Goal

Extend Sly Director only when the core connectors cannot provide the capability you need.

## Complete this step

1. Write down the exact missing capability.
2. Check whether it already exists through:

```text
Sly Director GitHub
AWS MCP
an official Claude connector
an existing remote MCP connector
a Sly Director Skill or Plugin
```

3. If none of those provide it, define the smallest custom MCP server that exposes only the required operations.
4. Add it through **Customize → Connectors → Add custom connector**.
5. Enable it in the **Sly Director** Project.
6. Test one harmless operation first.

## What you should see

The new MCP server should become another tool available to Sly Director without creating a separate operating interface.

<details>
<summary>Additional information</summary>

Chapter 5 already builds one custom MCP service: **Sly Director GitHub**. Use that implementation as a reference if a future capability also needs a custom cloud-hosted MCP endpoint.

A custom MCP server adds hosting, authentication, permissions, network exposure, monitoring, and maintenance. Prefer an existing connector whenever it satisfies the requirement.

</details>
