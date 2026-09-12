---
title: Build Your Own High Director — Claude Edition 10 — Maintenance
summary: Maintain the single-chat High Director Project, GitHub MCP, AWS MCP, and optional enhancements.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 90
permalink: /docs/high-director/build-your-own-claude/10-maintenance/
---

# Chapter 10 — Maintenance

## Goal

Keep the High Director Project and its connectors working with controlled access and cost.

## Complete this step

Once a month:

1. Open **Projects → High Director** and confirm the current instructions are still saved.
2. Open **Customize → Connectors** and confirm **GitHub MCP** and **AWS MCP** are connected.
3. In a High Director chat, run one harmless GitHub read and one harmless AWS query.
4. Review GitHub repository access granted to the GitHub connector.
5. Review open branches/pull requests and GitHub Actions failures created by recent work.
6. Open AWS **Billing and Cost Management** and review charges/budget alerts.
7. Check for AWS resources from old tests that are still running.
8. Review optional Skills, Cowork schedules, or Plugins you have added and remove anything you no longer use.

## What you should see

```text
High Director Project: working
GitHub MCP: working
AWS MCP: working
GitHub access: intentional
AWS cost: understood
Optional automation: intentional
```

The core guide is complete.

<details>
<summary>Additional information</summary>

The most important maintenance rule is to preserve the single-chat architecture. A connector authorization problem should be fixed at the connector/permission layer rather than redesigning normal operation around Claude Code.

Claude Code remains an optional specialist tool.

Cowork scheduled tasks should be reviewed periodically because they can continue running in the cloud on their configured schedule.

</details>

<details>
<summary>Maintenance prompt</summary>

```text
Review this High Director setup for maintenance.
Check the connected GitHub and AWS capabilities, identify stale repository work or AWS resources, and report any connector, cost, or automation issues that need attention.
```

</details>
