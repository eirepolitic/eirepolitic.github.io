---
title: "Build Your Own Sly Director — Optional Connectors"
summary: Add optional services such as Google Workspace to Sly Director after GitHub and AWS are working.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 92
permalink: /docs/high-director/build-your-own-claude/addendum-connectors/
---

# Optional Connectors

## Goal

Add another service to the same Sly Director Project.

## Complete this step

1. Open Claude.
2. Open **Customize → Connectors**.
3. Find the service you want.
4. Select **Connect**.
5. Sign in and complete the service's authorization flow.
6. Open **Projects → Sly Director**.
7. Enable the connector from **+ → Connectors**.
8. Ask Sly Director for one simple query to verify the connection.

## What you should see

The new service should be available as another tool to Sly Director in normal chat and, where supported, Cowork.

<details>
<summary>Preferred order</summary>

```text
official Claude connector
→ established remote MCP connector
→ custom MCP server
```

</details>
