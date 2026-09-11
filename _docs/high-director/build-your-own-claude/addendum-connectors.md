---
title: "Build Your Own High Director — Claude Edition — Addendum A: Connectors"
summary: Add optional Claude connectors after the core GitHub and AWS setup works.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 91
permalink: /docs/high-director/build-your-own-claude/addendum-connectors/
---

# Addendum A — Google Workspace and Other Connectors

## Goal

Add another service to Claude using an existing connector.

## Complete this step

1. Open Claude.
2. Open **Customize → Connectors**.
3. Find the service you want to connect.
4. Select **Connect**.
5. Sign in to the service account you want Claude to use.
6. Complete the service's authorization screen.
7. Open a High Director chat.
8. Enable the connector from the **+ → Connectors** menu.
9. Ask Claude for one simple query to verify the connection.

## What you should see

The service should appear in Claude's connectors and respond to a simple request.

<details>
<summary>Additional information</summary>

Preferred order:

```text
official Claude connector
→ established remote MCP connector
→ custom MCP server
```

For Google Workspace, connector availability can vary by product/account. Use the official connector when it provides the capability you need.

Start with a simple read/query before relying on a connector for more complex actions.

</details>

<details>
<summary>Troubleshooting</summary>

Useful prompt:

```text
I want to connect [service] to Claude using the simplest browser-only method.
Current screen/error: [describe]
Give me the shortest current click-by-click setup steps.
```

</details>
