---
title: Build Your Own Sly Director — 07 — Configure Cowork
summary: Configure Cowork as Sly Director's long-running autonomous execution mode.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 87
permalink: /docs/high-director/build-your-own-claude/07-end-to-end-testing/
---

# Chapter 7 — Configure Cowork

## Goal

Make Cowork the mode Sly Director uses for substantial work that should continue without repeated `continue` prompts.

## Complete this step

1. Open Claude.
2. Select **Cowork**.
3. Open **Projects** in Cowork.
4. Import or open the existing **Sly Director** Project.
5. Start a task inside the Sly Director Cowork Project.
6. Enable:

```text
GitHub MCP
AWS MCP
```

7. Set the approval mode to:

```text
Automatically approve
```

8. Send:

```text
Act as Sly Director and complete this task independently.

Using GitHub MCP and AWS MCP:
1. inspect the repository claude-director-test;
2. summarize its current state;
3. create a file named cowork-autonomy-test.md confirming that the Sly Director Cowork workflow is operational;
4. complete the repository-side workflow as far as the connected GitHub tools and repository permissions allow;
5. inspect relevant validation and correct recoverable failures if needed;
6. list the S3 buckets visible to the connected AWS identity;
7. verify the final repository and AWS state;
8. return to me when the requested outcome is complete or when a genuine blocker requires my decision.

Progress reports are informational. Continue working after them unless you actually need input from me.
```

9. Let Cowork run.
10. You may leave and return later to the same task.

## What you should see

Sly Director should continue through multiple steps and validation loops without requiring you to repeatedly type `continue`.

Continue to [Chapter 8 — Daily Operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}).

<details>
<summary>Why Automatically approve</summary>

This is the recommended Sly Director mode for substantial work because Cowork can keep progressing without stopping for every connector action, while still escalating when it cannot proceed safely or needs a genuine decision.

</details>
