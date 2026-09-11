---
title: Build Your Own High Director — Claude Edition 09 — Troubleshooting
summary: Troubleshoot the setup one layer at a time.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 89
permalink: /docs/high-director/build-your-own-claude/09-troubleshooting/
---

# Chapter 9 — Troubleshooting

## Goal

Identify the failing layer before changing anything.

## Complete this step

1. Copy the exact non-secret error.
2. Identify which layer failed:

```text
Claude Project
Claude Code / GitHub
AWS MCP connector
AWS OAuth
AWS service permission
```

3. Fix only that layer.
4. Retry the same operation.
5. Confirm the result before changing anything else.

## Quick fixes

### Claude Project problem

Open **Projects → High Director → Project instructions** and confirm the current instruction block is saved.

### Claude Code cannot see a repository

Open GitHub's installed-app settings and confirm the Claude/Anthropic GitHub App has access to that repository.

### Claude Code can read but cannot write

Check the exact Claude Code error and the repository's rules/permissions.

### AWS MCP connector will not authenticate

Confirm the connector uses:

```text
Authentication type: OAuth
OAuth client: Register automatically
```

### AWS authorization page does not open

Retry the connector with:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

### AWS OAuth works but an AWS operation returns AccessDenied

The AWS connection works. The active AWS identity lacks permission for that specific AWS action.

## What you should see

You should be able to name one failing layer and one exact error before making a configuration change.

Continue to [Chapter 10 — Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }}).

<details>
<summary>Additional information</summary>

For GitHub, repository authorization and AWS permissions are separate systems.

For AWS, these are also separate layers:

```text
AWS MCP connector
→ OAuth authorization
→ AWS identity permissions
→ specific AWS resource
```

If you use the optional IAM-role path and role switching fails, verify the role trust and the caller's `sts:AssumeRole` permission.

If OAuth permission itself fails for an IAM identity, check for:

```text
AWSMCPSignInOAuthAccessPolicy
```

If the same repository mistake repeats, improve tests, repository instructions, or automation rather than adding routine manual approval to every change.

</details>

<details>
<summary>Troubleshooting prompt</summary>

```text
I am troubleshooting my Claude High Director setup.
Failing layer: [Claude Project / Claude Code / GitHub / AWS MCP / AWS OAuth / AWS service]
Last step that worked: [describe]
Exact non-secret error: [paste]
Expected result: [describe]
Observed result: [describe]
Identify the failing layer and give me the smallest browser-only fix.
```

</details>
