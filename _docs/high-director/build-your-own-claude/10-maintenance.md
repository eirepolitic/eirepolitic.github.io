---
title: Build Your Own High Director — Claude Edition 10 — Maintenance
summary: Maintain the High Director Project, Cowork tasks, schedules, GitHub MCP, and AWS MCP.
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

Keep the High Director Project, autonomous Cowork execution, connectors, schedules, access, and costs under control.

## Complete this step

Once a month:

1. Open **Projects → High Director** and confirm the current instructions are still saved.
2. Open the High Director **Cowork** Project and confirm it still has the intended Project context/instructions.
3. Open **Customize → Connectors** and confirm **GitHub MCP** and **AWS MCP** are connected.
4. Run one harmless GitHub read and one harmless AWS query.
5. Review recent Cowork tasks for recurring failures or unnecessary interruptions.
6. Open **Scheduled** and review every recurring task.
7. Pause or remove scheduled tasks you no longer want.
8. Review GitHub repository access granted to the GitHub connector.
9. Review open branches/pull requests and GitHub Actions failures created by recent work.
10. Open AWS **Billing and Cost Management** and review charges/budget alerts.
11. Check for AWS resources from old tests that are still running.
12. Review any High Director Skills or Plugins and remove obsolete ones.

## What you should see

```text
High Director Project: working
Cowork autonomous execution: working
GitHub MCP: working
AWS MCP: working
scheduled tasks: intentional
GitHub access: intentional
AWS cost: understood
```

The core guide is complete.

<details>
<summary>What to learn from Cowork interruptions</summary>

If Cowork repeatedly stops for the same kind of question, treat that as feedback on the High Director design.

Depending on the cause, improve:

```text
Project instructions
High Director Operator Skill
connector permissions
repository validation
acceptance criteria
scheduled-task instructions
```

The goal is to progressively reduce unnecessary owner intervention while preserving genuine decision points.

</details>

<details>
<summary>Maintenance prompt</summary>

```text
Review this High Director setup for maintenance.
Check recent Cowork work, connected GitHub and AWS capabilities, recurring interruptions, scheduled tasks, stale repository work, and AWS resources. Identify anything that should be corrected so substantial tasks can continue independently until completion or a genuine blocker.
```

</details>
