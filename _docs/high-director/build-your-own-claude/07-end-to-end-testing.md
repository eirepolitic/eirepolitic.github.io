---
title: Build Your Own Sly Director — 07 — Configure Cowork
summary: Configure Cowork as Sly Director's long-running autonomous execution mode and test both primary connectors together.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 87
permalink: /docs/high-director/build-your-own-claude/07-end-to-end-testing/
---

# Chapter 7 — Configure Cowork

## Goal

Make Cowork the mode Sly Director uses for substantial work that should continue without repeated `continue` prompts.

## First verify the GitHub connector in Cowork

1. Open Claude.
2. Select **Cowork**.
3. Open **Projects** in Cowork.
4. Import or open the existing **Sly Director** Project.
5. Start a task inside the Sly Director Cowork Project.
6. Enable **Sly Director GitHub**.
7. Set the approval mode to:

```text
Automatically approve
```

8. Send:

```text
Using the Sly Director GitHub connector, inspect claude-director-test and report:
- the default branch
- the current file list
- the contents of sly-director-test.md

Use the connector directly. Do not ask me to reconnect unless authentication genuinely fails.
```

9. Confirm Cowork can read the repository through the connector.

A fresh Cowork session may briefly report that the connector is `not_connected` or fail to load its deferred tools immediately. During live verification, the connector became available about 30 seconds later and worked after a refresh/retry without any configuration change. Treat a short startup delay as transient unless the connector remains unavailable.

## Complete the autonomous end-to-end test

1. In the same Sly Director Cowork Project, enable:

```text
Sly Director GitHub
AWS MCP
```

2. Keep the approval mode set to:

```text
Automatically approve
```

3. Send:

```text
Act as Sly Director and complete this task independently.

Using Sly Director GitHub and AWS MCP:
1. inspect the repository claude-director-test;
2. inspect the current AWS Lambda function sly-director-github-mcp in us-east-2;
3. create a working branch and add a file named cowork-autonomy-test.md confirming that the Sly Director Cowork workflow is operational;
4. create a non-draft pull request into main;
5. inspect relevant GitHub Actions validation and correct recoverable failures if needed;
6. merge the pull request when validation succeeds;
7. verify cowork-autonomy-test.md exists on main;
8. re-check the AWS Lambda and confirm its state is Active, its handler is src.lambda_entry.handler, and its last update status is Successful;
9. do not modify AWS resources;
10. return to me when the requested outcome is complete or when a genuine blocker requires my decision.

Progress reports are informational. Continue working after them unless you actually need input from me.
```

4. Let Cowork run.
5. You may leave and return later to the same task.

## Live-verified result

The full Cowork autonomy test has been completed successfully.

Verified behavior:

```text
GitHub connector startup delay handled without user intervention
working branch created
file committed
non-draft pull request created
GitHub Actions run inspected
validation passed
pull request squash-merged
file verified on main
AWS Lambda inspected before and after the GitHub workflow
AWS Lambda remained Active
handler remained src.lambda_entry.handler
last update status remained Successful
no AWS resources were modified
no routine continue/approval prompt was required
```

The verified GitHub test used a server-side-prefixed branch:

```text
sly/cowork-autonomy-test
```

and successfully completed the repository workflow through merge and final verification.

## What you should see

Sly Director should continue through multiple implementation and validation steps without requiring you to repeatedly type `continue`.

The final report should confirm both sides of the system:

```text
Sly Director GitHub: repository workflow completed
AWS MCP: AWS query completed
Cowork: continued through the plan without routine handoffs
```

Continue to [Chapter 8 — Daily Operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}).

<details>
<summary>Why Automatically approve</summary>

This is the recommended Sly Director mode for substantial work because Cowork can keep progressing without stopping for every connector action, while still escalating when it cannot proceed safely or needs a genuine decision.

</details>

<details>
<summary>If Sly Director GitHub says not_connected at startup</summary>

Wait roughly 30 seconds, refresh or retry connector discovery, and try the same request again. The live-tested connector recovered this way without reconnecting or changing configuration.

If it remains unavailable after repeated retries, then open Claude's connector settings and confirm **Sly Director GitHub** still shows connected before troubleshooting authentication again.

</details>

<details>
<summary>Cleanup after the autonomy test</summary>

After the pull request has been merged and the final state is verified, delete the temporary test branch if it still exists:

```text
sly/cowork-autonomy-test
```

Deleting the merged branch does not remove the merged changes from `main`.

</details>
