---
title: Build Your Own Sly Director — 07 — Test Sly Director in Cowork
summary: Prove that Cowork can use both GitHub and AWS and complete a multi-step workflow without repeated handoffs.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 87
permalink: /docs/high-director/build-your-own-claude/07-end-to-end-testing/
---

# Chapter 7 — Test Sly Director in Cowork

## Goal

Confirm that Sly Director can keep working through a multi-step task in Cowork using both GitHub and AWS.

Cowork is Claude's long-running work mode. It can continue through multiple tool calls and validation steps instead of handing the job back after each action.

## Step 1 — Open Sly Director in Cowork

1. Open Claude.
2. Open the **Sly Director** Project.
3. Start a **Cowork** session from the Project.
4. In the mode selector near the message box, choose:

```text
Automatically approve
```

5. Open the connector menu and enable:

```text
Sly Director GitHub
AWS MCP
```

## Step 2 — Do a quick GitHub check

Send:

```text
Using the Sly Director GitHub connector, inspect claude-director-test and report:
- the default branch
- the current file list
- the contents of sly-director-test.md if it exists

Use the connector directly. Do not ask me to reconnect unless authentication genuinely fails.
```

A fresh Cowork session may briefly show the GitHub connector as `not_connected` while its tools load. In live testing it recovered after roughly 30 seconds and a refresh/retry. Do not rebuild the connector unless it stays unavailable.

## Step 3 — Run the autonomous test

Send:

```text
Act as Sly Director and complete this task independently.

Using Sly Director GitHub and AWS MCP:
1. inspect the repository claude-director-test;
2. inspect the current AWS Lambda function sly-director-github-mcp in us-east-2;
3. create a working branch and add a file named cowork-autonomy-test.md confirming that the Sly Director Cowork workflow is operational;
4. create a non-draft pull request into main;
5. inspect the GitHub Actions validation and correct recoverable failures if needed;
6. merge the pull request when validation succeeds;
7. verify cowork-autonomy-test.md exists on main;
8. re-check the AWS Lambda and confirm its state is Active, its handler is src.lambda_entry.handler, and its last update status is Successful;
9. do not modify AWS resources;
10. return to me when the requested outcome is complete or when a genuine blocker requires my decision.

Progress reports are informational. Continue working after them unless you actually need input from me.
```

## Step 4 — Check the result

The test passes when Cowork reports that it:

```text
created a working branch
created a pull request
waited for GitHub Actions
merged after validation succeeded
verified the file on main
checked the AWS Lambda before/after
completed without routine “continue” prompts
```

The branch name will normally begin with:

```text
sly/
```

because the GitHub connector adds that prefix automatically.

## Step 5 — Clean up the test branch

After the pull request is merged, delete the temporary `sly/cowork-autonomy-test` branch if it still exists. Deleting a merged branch does not remove its changes from `main`.

Sly Director is now fully operational.

Continue to [Chapter 8 — Daily Operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}).
