---
title: Build Your Own High Director — Claude Edition 10 — Maintenance and Access Review
summary: Maintain the Claude edition by reviewing subscription usage, GitHub authorization, AWS MCP OAuth access, IAM permissions, costs, and connector revocation.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 90
permalink: /docs/high-director/build-your-own-claude/10-maintenance/
---

# Chapter 10 — Maintenance and Access Review

## Goal

Keep the setup working with clean permissions and controlled cost.

## Monthly checklist

Review:

1. Claude plan and usage.
2. GitHub repositories authorized for Claude Code.
3. Open pull requests/branches created by Claude Code.
4. AWS Billing and Cost Management.
5. AWS budget notifications.
6. AWS MCP connector still points to the official managed endpoint.
7. IAM permissions granted to the AWS identity used through MCP.
8. CloudTrail activity if you need to audit AWS changes.

## Claude subscription

Claude Pro currently includes Claude Code and shares usage across Claude/Claude Code.

If usage becomes a recurring limitation:

1. Check **Settings → Usage** or the current usage view.
2. Decide whether the problem is occasional or persistent.
3. Compare optional usage credits or higher plans only if needed.

GitHub and AWS permissions are managed separately from the Claude subscription tier.

## Review GitHub authorization

Periodically review which repositories Claude Code can access.

In GitHub:

1. Open **Settings**.
2. Find the installed/authorized GitHub Apps or integrations area.
3. Open the Anthropic/Claude Code integration.
4. Review repository access.
5. Remove repositories Claude no longer needs.

If you create a new repository and Claude Code cannot see it, add that repository to the App's access.

## Review old branches and pull requests

Claude Code tasks can leave branches or PRs after testing.

Periodically:

1. Open each active repository.
2. Review **Pull requests**.
3. Close obsolete test PRs.
4. Review branches and delete obsolete merged/test branches where appropriate.

## Review AWS cost

1. Open **Billing and Cost Management**.
2. Review current charges by service.
3. Check whether resources created during experiments are still running.
4. Delete resources you understand and no longer need.

Remember: the AWS MCP Server itself is documented as no additional charge, but the AWS resources it creates or uses are billed normally.

## Review AWS IAM

The AWS MCP Server uses your existing IAM authorization.

If you added permissions during setup or later work:

1. Open IAM.
2. Identify the user/role used for AWS MCP OAuth.
3. Review attached policies.
4. Remove temporary permissions that are no longer needed.
5. Keep the AWS MCP OAuth sign-in permissions only if you still use the connector.

## Revoke the AWS MCP connection

If you no longer want Claude connected to AWS:

1. In Claude, open **Customize → Connectors**.
2. Disable or remove the **AWS MCP** connector.
3. In AWS, review the identity/policies used for MCP access.
4. Remove MCP-specific OAuth permission if it is no longer required and doing so will not affect another approved use.
5. Review CloudTrail if you need an audit trail of recent MCP-originated activity.

## Reconnect after authorization changes

If you intentionally change AWS identity permissions:

1. Make one IAM change at a time.
2. Retry a harmless read operation through AWS MCP.
3. Test the intended operation.
4. Verify the AWS result directly in the AWS console.

## Update Project instructions

When you want to change High Director behavior:

1. Open the Project.
2. Edit **Project instructions**.
3. Change only the behavior you intend to change.
4. Save.
5. Start a fresh project chat and test the new behavior.

## Retire the entire setup

If you no longer want the Claude edition:

1. Remove/disable the AWS MCP connector in Claude.
2. Remove Claude Code repository authorization in GitHub.
3. Close/delete obsolete test PRs and branches.
4. Delete `claude-director-test` if you no longer need it.
5. Review AWS for resources created through testing.
6. Review AWS billing afterward.
7. Downgrade/cancel Claude Pro if you no longer want the paid features.

## Ask ordinary Claude or ChatGPT this

```text
I maintain a browser-only Claude High Director setup using Claude Pro, Claude Code web, GitHub, and the AWS managed MCP Server with OAuth.

Maintenance task: [review access / remove repository / revoke AWS connector / reduce IAM / review cost / retire setup]
Current working state: [describe]

Give me a change-one-thing-at-a-time procedure that preserves unrelated GitHub/AWS access.
```

## Core guide complete

If Chapters 1–10 pass, the core Claude edition is ready for normal use.

Optional extensions:

- [Google Workspace and other Claude connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Advanced custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})
