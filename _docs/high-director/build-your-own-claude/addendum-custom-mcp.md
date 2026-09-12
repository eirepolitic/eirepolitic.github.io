---
title: "Build Your Own High Director — Claude Edition — Addendum B: Custom MCP"
summary: Build a custom remote MCP server only when the official GitHub/AWS connectors and other existing connectors cannot provide the needed capability.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 93
permalink: /docs/high-director/build-your-own-claude/addendum-custom-mcp/
---

# Addendum B — Custom MCP Servers

## Goal

Decide whether a custom MCP server is actually needed before building one.

## Complete this step

1. Write down the exact capability High Director needs.
2. Check whether it is already available through:

```text
GitHub MCP
AWS MCP
an official Claude connector
an existing remote MCP connector
an installed Skill or Plugin
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

4. Build and test the custom MCP server separately.
5. Add it through **Customize → Connectors → Add custom connector**.
6. Enable it in the High Director Project chat.
7. Test one harmless operation first.

## What you should see

The new MCP server should appear as another tool available to the same High Director Project chat.

<details>
<summary>Additional information</summary>

The purpose of a custom MCP server in this design is to **extend the one-chat High Director**, not create another operating surface.

A custom server adds hosting, authentication, network exposure, tool schemas, authorization logic, monitoring, and maintenance, so prefer existing connectors first.

The original OpenAI High Director Lambda wrapper remains a separate implementation. The Claude edition now uses GitHub's official MCP server for normal GitHub operation rather than requiring that wrapper to be ported.

</details>

<details>
<summary>Planning prompt</summary>

```text
I have a working single-chat Claude High Director setup using GitHub MCP and AWS MCP.
Missing capability: [describe]
Check whether an existing connector, Skill, or Plugin already provides it. If not, define the smallest custom remote MCP design that can be added to the same High Director Project chat.
```

</details>
