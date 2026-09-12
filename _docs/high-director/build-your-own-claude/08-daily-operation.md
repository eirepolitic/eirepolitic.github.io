---
title: Build Your Own Sly Director — 08 — Daily Operation
summary: Use Sly Director normal chat for quick work and Cowork for substantial autonomous execution.
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

Use one Sly Director identity and choose the right mode for the size of the task.

## Quick work

Use normal **Sly Director** Project chat for:

```text
questions
planning
a small investigation
a small repository change
a quick AWS task
interactive troubleshooting
```

## Substantial work

Use **Sly Director in Cowork** when the task:

```text
has many steps
may run for a long time
requires investigation + implementation + validation
can benefit from parallel work
would otherwise require repeated "continue" prompts
should keep running while you are away
```

### Start a substantial task

1. Open the **Sly Director** Cowork Project.
2. Enable **GitHub MCP** and/or **AWS MCP**.
3. Select **Automatically approve**.
4. Give Sly Director the final objective and constraints.
5. Tell it to continue until complete or genuinely blocked.
6. Let Cowork run independently.
7. Return later to review the result or answer a genuine question.

Use this pattern:

```text
Complete this objective independently: [objective].

Inspect the existing repository/infrastructure first. Form the plan, execute it, validate the result, diagnose and correct recoverable failures, and verify the final state.

Use parallel workstreams where useful. Progress reports are informational; continue working after them. Return to me when the requested outcome is complete or when a genuine decision, unavailable permission, unavailable capability, or unrecoverable blocker requires me.
```

## What you should see

```text
Sly Director
├─ normal chat → quick/interactively supervised work
└─ Cowork → substantial autonomous work
```

Continue to [Chapter 9 — Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }}).
