---
title: Sly Director — Claude Custom Connector Current UI
summary: Current Claude custom connector choices for the WorkOS AuthKit production MCP connection.
section: high-director
doc_type: reference
status: active
created: 2026-09-14
updated: 2026-09-14
last_verified: 2026-09-14
order: 87
permalink: /docs/high-director/build-your-own-claude/claude-custom-connector-current-ui/
---

# Claude Custom Connector — Current UI

When adding the **Sly Director GitHub** custom connector in Claude, enter the remote MCP URL ending in `/mcp`.

Claude should detect OAuth automatically.

Use these choices:

```text
Authentication
● Sign in now

OAuth client
● Use Claude’s published identity

Request headers
leave empty

Advanced
leave unchanged
```

`Use Claude’s published identity` is Claude's CIMD option. Use it when Claude shows it as **Detected**.

Do not switch to **Register automatically** unless the CIMD path fails. That option uses Dynamic Client Registration instead and is only the compatibility fallback for this guide.

Do not choose **Use your own OAuth client** for the normal Sly Director build.

After selecting the options above, save/add the connector and complete the WorkOS AuthKit sign-in flow that opens.

<details>
<summary>Why DCR is still enabled in WorkOS</summary>

WorkOS keeps both Client ID Metadata Document (CIMD) and Dynamic Client Registration (DCR) enabled for compatibility. Claude's current UI can detect CIMD and use its published identity directly, so CIMD is the preferred path when available.

</details>
