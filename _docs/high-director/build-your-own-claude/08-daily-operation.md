---
title: Build Your Own Sly Director — 08 — Daily Operation
summary: Use normal Claude chat for quick work and Cowork for longer autonomous jobs.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 88
permalink: /docs/high-director/build-your-own-claude/08-daily-operation/
---

# Chapter 8 — Use Sly Director Day to Day

## The simple rule

Use **normal Claude chat** for quick, interactive work.

Use **Cowork** when you want Sly Director to keep working through a longer task without repeated handoffs.

## Normal chat

Good examples:

```text
Explain this error.
Inspect this repository and tell me what is wrong.
Show me the current Lambda configuration.
Plan the safest way to make this change.
```

Normal chat is best when you expect to discuss the work as it happens.

## Cowork

Good examples:

```text
Investigate this failure, implement the fix, validate it, correct recoverable problems, complete the pull-request workflow, and verify the final state.
```

or:

```text
Review this repository and the related AWS resources. Make the requested change, test it, finish the GitHub workflow, and return when the outcome is complete or a genuine decision is required.
```

Before starting a substantial Cowork task:

1. Open the **Sly Director** Project.
2. Start a **Cowork** session.
3. Choose **Automatically approve** if you want Cowork to continue through routine actions without asking each time.
4. Enable the connectors the task needs:

```text
Sly Director GitHub
AWS MCP
```

5. Describe the outcome you want, not every individual click or command.

## A useful default Cowork prompt

```text
Complete this task independently.

First inspect the relevant repository, AWS resources, documentation, and errors. Work out a practical plan, make the required changes, validate them, correct recoverable failures, complete the repository workflow, and verify the final state.

Use Sly Director GitHub and AWS MCP directly when needed.

Progress updates are informational. Continue working unless a genuine decision or blocker requires me.
```

## When to stay closer to the task

Use normal chat or Cowork's **Manually approve** mode when the task has consequences you want to review personally before each action.

Continue to [Chapter 9 — Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }}).
