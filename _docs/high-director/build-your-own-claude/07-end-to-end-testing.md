---
title: Build Your Own Sly Director — 07 — Configure Cowork
summary: Configure Cowork as the long-running autonomous execution mode for substantial Sly Director work.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 87
permalink: /docs/high-director/build-your-own-claude/07-end-to-end-testing/
---

# Chapter 7 — Configure Cowork for Autonomous Sly Director Work

## Goal

Use the **Sly Director Project in Cowork** so substantial plans can continue for extended periods without requiring repeated `continue` prompts.

## Complete this step

### 1 — Open Cowork

1. Open Claude on the web, desktop, or mobile.
2. In the message box, select:

```text
Cowork
```

### 2 — Create the Cowork version of the Sly Director Project

If your existing **Sly Director** Project is already available in Cowork, open it and continue to Step 3.

If Cowork asks you to create/import a project:

1. Open **Projects** in Cowork.
2. Select the **+** button.
3. Select:

```text
Import from project
```

4. Search for:

```text
Sly Director
```

5. Select the existing Sly Director Claude Project.
6. Name the Cowork project:

```text
Sly Director
```

7. Select **Create**.

The imported Cowork Project carries the existing Project instructions and files/context into Cowork.

### 3 — Enable the Sly Director connectors

1. Start a task inside the **Sly Director** Cowork Project.
2. Select the **+** button near the message box.
3. Enable:

```text
GitHub MCP
AWS MCP
```

### 4 — Set the approval mode

1. Find the Cowork mode selector in the message box.
2. Select:

```text
Automatically approve
```

This is the recommended Sly Director mode for substantial work. Claude can keep working instead of stopping for every connector action, while still reviewing actions and pausing when it cannot find a safe path forward.

### 5 — Run the autonomous test

Send:

```text
Act as Sly Director and complete this task independently.

Using GitHub MCP and AWS MCP:
1. inspect the repository claude-director-test;
2. summarize its current state;
3. create a file named cowork-autonomy-test.md containing a short note that the Cowork Sly Director workflow is operational;
4. complete the repository-side workflow as far as the connected GitHub tools and repository permissions allow;
5. inspect any relevant GitHub validation or workflow result and correct recoverable failures if needed;
6. list the S3 buckets visible to the connected AWS identity;
7. verify the final repository and AWS state;
8. return to me when the requested outcome is complete or when a genuine blocker requires my decision.

Progress reports are informational. Continue working after them unless you actually need input from me.
```

6. Review Claude's proposed approach.
7. Let the Cowork task run.
8. You may close the browser/computer after the task is running in a cloud session.
9. Return later from web, desktop, or mobile and open the same Cowork task.

## What you should see

The Cowork task should be able to continue through multiple implementation/validation steps without requiring you to repeatedly type `continue`.

The final result should include:

```text
GitHub repository inspected
repository change completed or exact blocker reported
validation inspected where available
AWS query completed
final state reported
```

Continue to [Chapter 8 — Daily Operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}).

<details>
<summary>Why Automatically approve is the recommended mode</summary>

Cowork currently offers three approval modes:

```text
Manually approve
Automatically approve
Skip all approvals
```

**Automatically approve** is the default recommendation for Sly Director because Claude keeps working without asking about every action, while still reviewing connector/tool actions and blocking or escalating when necessary.

**Manually approve** creates more interruptions and is better for work where you want to inspect each action.

**Skip all approvals** removes Cowork's automatic action review and is therefore not the default Sly Director mode.

</details>

<details>
<summary>What Cowork contributes beyond normal chat</summary>

Cowork cloud sessions can:

```text
keep running after you step away
work for extended periods without normal conversation timeouts interrupting progress
create a plan
break work into subtasks
run code and shell commands in an isolated cloud environment
coordinate multiple workstreams/sub-agents in parallel
use connectors and plugins
retain task/project context and memory
```

This is the part of the Claude architecture that most directly replaces the manual continuation/orchestration layer that Overlord was designed to provide.

</details>

<details>
<summary>Current limitation to understand</summary>

Cowork can still pause if it genuinely needs a decision, encounters a permission/capability it cannot resolve, hits an approval block, or reaches account usage limits.

The objective is not unlimited unattended execution. The objective is to remove artificial handoffs where the system merely finished one response and needs the user to say `continue` before proceeding with an already-approved plan.

</details>
