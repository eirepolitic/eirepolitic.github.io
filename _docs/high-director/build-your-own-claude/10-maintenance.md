---
title: Build Your Own Sly Director — 10 — Maintenance
summary: Maintain the Sly Director Project, Cowork tasks, schedules, GitHub MCP, and AWS MCP.
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

Keep Sly Director, its Cowork work, connectors, schedules, access, and costs under control.

## Complete this step

Once a month:

1. Open **Projects → Sly Director** and confirm the current instructions are saved.
2. Open the **Sly Director** Cowork Project and confirm it still has the intended context/instructions.
3. Confirm **GitHub MCP** and **AWS MCP** are connected.
4. Run one harmless GitHub read and one harmless AWS query.
5. Review recent Cowork tasks for recurring failures or unnecessary interruptions.
6. Review every scheduled task.
7. Pause or remove scheduled tasks you no longer want.
8. Review GitHub repository access.
9. Review open branches/pull requests and GitHub Actions failures from recent work.
10. Review AWS charges and budget alerts.
11. Check for AWS resources from old tests that are still running.
12. Review any Sly Director Skills or Plugins and remove obsolete ones.

## What you should see

```text
Sly Director Project: working
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

If Cowork repeatedly stops for the same unnecessary question, improve the Sly Director instructions, future Operator Skill, connector permissions, validation, or task instructions rather than accepting the interruption as normal.

</details>
