---
title: Build Your Own Sly Director — 06 — Connect AWS MCP
summary: Connect Sly Director to the managed AWS MCP Server using browser OAuth.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 86
permalink: /docs/high-director/build-your-own-claude/06-aws-mcp-server/
---

# Chapter 6 — Connect AWS MCP

## Goal

Give the **Sly Director Project** direct AWS tools in addition to the **Sly Director GitHub** connector built in Chapter 5.

## Complete this step

1. Keep the AWS session from Chapter 4 available.
2. Open Claude.
3. Open **Customize → Connectors**.
4. Select **Add custom connector**.
5. Enter:

```text
Name: AWS MCP
Remote MCP server URL: https://aws-mcp.us-east-1.api.aws/mcp
```

6. Set **Authentication type** to:

```text
OAuth
```

7. Set **OAuth client** to:

```text
Register automatically
```

8. Leave optional Client ID/Secret fields empty.
9. Save the connector.
10. Open **Projects → Sly Director**.
11. Start a new chat.
12. Select **+ → Connectors**.
13. Enable **AWS MCP**.
14. Ask:

```text
Using the AWS connector, identify the AWS account and AWS identity available to you.
```

15. Complete the AWS authorization flow when it opens.
16. Return to Claude and ask:

```text
Using AWS MCP, list the S3 buckets visible to this AWS identity and tell me which AWS identity you are using.
```

## What you should see

Sly Director should identify the AWS account/identity and return the visible S3 buckets. An empty list is still a successful connection.

At this point Sly Director has both primary tool connections:

```text
Sly Director GitHub: connected
AWS MCP: connected
```

Continue to [Chapter 7 — Configure Cowork]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }}).

<details>
<summary>Additional information</summary>

Use these AWS connector settings exactly:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

The AWS MCP endpoint uses `us-east-1`, while this guide's normal AWS workload region is `us-east-2`. Those are separate choices.

</details>

<details>
<summary>If the AWS authorization page does not open</summary>

Edit/re-add the connector using:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

Keep:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

</details>
