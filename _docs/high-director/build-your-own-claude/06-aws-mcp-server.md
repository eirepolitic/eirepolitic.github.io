---
title: Build Your Own High Director — Claude Edition 06 — AWS MCP Server
summary: Connect Claude to the managed AWS MCP Server using browser OAuth.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 86
permalink: /docs/high-director/build-your-own-claude/06-aws-mcp-server/
---

# Chapter 6 — Connect Claude to AWS MCP

## Goal

Connect the High Director Project to AWS using the managed AWS MCP Server.

## Complete this step

1. Keep the AWS console open in the root-user session from Chapter 5.
2. Open [Claude](https://claude.ai/) in another browser tab.
3. Open **Customize → Connectors**.
4. Select **+** or **Add connector**.
5. Select **Add custom connector**.
6. Enter:

```text
Name: AWS MCP
Remote MCP server URL: https://aws-mcp.us-east-1.api.aws/mcp
```

7. Continue to **Authentication type**.
8. Select:

```text
OAuth
```

9. Continue to the OAuth client choice.
10. Select:

```text
Register automatically
```

11. Leave any optional OAuth Client ID or Client Secret fields empty.
12. Select **Add** or **Save**.
13. Open **Projects → High Director**.
14. Start a new chat.
15. Select the **+** button near the message box.
16. Open **Connectors**.
17. Enable **AWS MCP**.
18. Send:

```text
Using the AWS connector, identify the AWS account and AWS identity available to you.
```

19. When AWS opens, confirm the correct AWS account.
20. Complete AWS sign-in if requested.
21. Approve the AWS MCP authorization.
22. Return to Claude.
23. Send:

```text
Using AWS MCP, list the S3 buckets visible to this AWS identity and tell me which AWS identity you are using.
```

## What you should see

Claude should identify the AWS account/identity and return the visible S3 buckets. An empty bucket list is a successful connection if the account has no buckets.

Continue to [Chapter 7 — End-to-End Testing]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }}).

<details>
<summary>Additional information</summary>

Use these connector settings exactly:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

AWS MCP supports automatic OAuth client registration for this flow. The other Claude choices are intended for different OAuth integration models.

The AWS MCP endpoint shown above is currently the managed `us-east-1` endpoint. Your workloads can still use the preferred `us-east-2` region from Chapter 5.

If you chose the optional `ClaudeHighDirectorRole` path in Chapter 5, keep that role session active instead of root before triggering OAuth.

AWS continues to enforce whatever permissions belong to the AWS identity that authorized the connection.

</details>

<details>
<summary>Optional: AWS service permissions for an IAM role</summary>

This section applies only if you used `ClaudeHighDirectorRole` instead of root.

If OAuth succeeds but an AWS operation returns `AccessDenied`:

1. Open **IAM → Roles → ClaudeHighDirectorRole**.
2. Open **Permissions**.
3. Select **Add permissions → Attach policies**.
4. Add the policy required for the AWS service Claude needs.

Common examples:

```text
AmazonS3FullAccess
AWSLambda_FullAccess
CloudWatchFullAccessV2
AWSStepFunctionsFullAccess
```

Some operations also require `iam:PassRole` when Claude assigns an execution role to an AWS service.

</details>

<details>
<summary>Troubleshooting</summary>

If the AWS authorization window does not appear, edit/re-add the connector using:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

Keep:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

If an IAM identity reports missing OAuth permissions, the relevant managed policy is:

```text
AWSMCPSignInOAuthAccessPolicy
```

Useful prompt:

```text
I am connecting Claude to the AWS managed MCP Server.
Authentication type: OAuth
OAuth client: Register automatically
AWS identity: [root / ClaudeHighDirectorRole / other]
I am stuck at: [connector creation / OAuth / authorization / AWS query]
Exact non-secret error: [paste it]
Give me the smallest browser-only fix.
```

</details>
