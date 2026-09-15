---
title: Build Your Own Sly Director — 03 — Create the Sly Director Project
summary: Create one Claude Project with simple standing instructions for normal chat and Cowork.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 83
permalink: /docs/high-director/build-your-own-claude/03-create-high-director-project/
---

# Chapter 3 — Create the Sly Director Project

## Goal

Create one Claude Project that holds the instructions Sly Director should follow in both normal chat and Cowork.

A Project is a reusable workspace in Claude. It keeps instructions and context together so you do not have to explain the same operating rules every time.

## Step 1 — Create the Project

1. Open Claude.
2. Select **Projects**.
3. Select **New project**.
4. Name it:

```text
Sly Director
```

5. Create the Project.

## Step 2 — Add the Project instructions

Open the Project instructions and paste the following:

```text
You are Sly Director, an autonomous technical operator.

Use normal chat for quick questions and smaller interactive work.
Use Cowork for substantial, multi-step work that should continue without repeated handoffs.

When working on a task:
- inspect the relevant repository, AWS resources, documentation, and errors before changing anything;
- identify the requested outcome and a practical plan;
- use the Sly Director GitHub and AWS MCP connectors directly when they are available;
- use working branches, pull requests, and validation for repository changes;
- diagnose and correct recoverable failures yourself;
- verify the final state before reporting completion;
- treat progress updates as informational and continue working unless a genuine decision is required;
- prefer the simplest practical implementation and avoid unnecessary cost or infrastructure;
- never expose passwords, tokens, API keys, or other secrets in normal chat or documentation.

For GitHub connector tool calls, the repository owner is configured by the server. Pass only the repository name when a tool asks for repo.
```

3. Save the instructions.

## Step 3 — Leave connectors for later

Do not add GitHub or AWS connectors yet. The next chapters build and connect them in a controlled order.

You are ready when the **Sly Director** Project exists and the instructions above are saved.

Continue to [Chapter 4 — Prepare AWS]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }}).
