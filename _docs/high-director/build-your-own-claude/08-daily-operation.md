---
title: Build Your Own High Director — Claude Edition 08 — Daily Operation
summary: Use normal High Director chat for quick work and Cowork for substantial autonomous execution.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 88
permalink: /docs/high-director/build-your-own-claude/08-daily-operation/
---

# Chapter 8 — Daily Operation

## Goal

Use one High Director identity while choosing the execution mode that matches the size of the task.

## Use normal High Director chat for quick work

Use normal Project chat when you want:

```text
questions
planning/discussion
small investigations
small repository changes
quick AWS queries or changes
interactive troubleshooting
```

### Complete a normal chat task

1. Open **Projects → High Director**.
2. Enable the connectors needed for the task.
3. Give High Director the request.
4. Continue interacting normally.

## Use Cowork for substantial work

Use Cowork when the task:

```text
has many implementation steps
may take an extended period
requires investigation + implementation + validation loops
can benefit from parallel workstreams
would otherwise require repeated "continue" prompts
should keep running while you are away
```

### Complete a substantial task

1. Open the **High Director** Cowork Project.
2. Enable **GitHub MCP** and/or **AWS MCP**.
3. Select **Automatically approve**.
4. Give High Director the final objective and constraints.
5. Tell it to continue through the approved plan until the outcome is complete or a genuine blocker requires you.
6. Let Cowork run independently.
7. Return later to the same task to review the completed result or answer a genuine question.

A useful task format is:

```text
Complete this objective independently: [objective].

Inspect the existing repository/infrastructure first. Form the plan, execute it, validate the result, diagnose and correct recoverable failures, and verify the final state.

Use parallel workstreams where useful. Progress reports are informational; continue working after them. Return to me when the requested outcome is complete or when a genuine decision, unavailable permission, unavailable capability, or unrecoverable blocker requires me.
```

## What you should see

Your operating model should be:

```text
High Director
├─ normal chat → quick/interactively supervised work
└─ Cowork → substantial autonomous work
```

You should no longer need to manually coordinate multiple chat instances or type `continue` throughout an already-approved implementation plan.

Continue to [Chapter 9 — Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }}).

<details>
<summary>How this replaces the manual multi-chat delegation pattern</summary>

Earlier High Director instructions suggested manually opening several chat instances for large plans and later returning to the original chat to reconcile their work.

Cowork can coordinate parallel sub-agents internally. The user should normally give the substantial task to one High Director Cowork task and let Cowork decide whether parallel workstreams are useful.

</details>

<details>
<summary>When Claude Code is still useful</summary>

Claude Code remains a specialist fallback if a task specifically requires repository-development capabilities that the Cowork + MCP toolset cannot provide.

It is no longer the standard implementation path or the normal solution to long-running work.

</details>
