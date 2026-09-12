---
title: Build Your Own High Director — Claude Edition 08 — Daily Operation
summary: Operate GitHub and AWS from the same High Director Project chat during normal use.
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

Use one High Director Project chat as the normal interface for repository, AWS, planning, investigation, and troubleshooting work.

## Complete this step

1. Open **Projects → High Director**.
2. Start or continue a High Director chat.
3. Enable the connectors needed for the task:

```text
GitHub MCP
AWS MCP
```

4. Give High Director the complete task.

Example:

```text
Investigate repository [repository name], determine the cause of [problem], implement the best practical solution, run or inspect the relevant GitHub validation, correct failures where practical, complete the repository workflow, and make any required AWS changes. Report the final state when finished.
```

5. Let High Director inspect and operate GitHub/AWS directly from that conversation.
6. Continue follow-up work in the same Project/chat when useful.

## What you should see

Normal use should look like:

```text
You
↓
High Director Project chat
├─ GitHub MCP
└─ AWS MCP
```

The normal workflow should not require copying a plan into Claude Code.

Continue to [Chapter 9 — Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }}).

<details>
<summary>Optional: use Cowork for a larger task</summary>

Cowork is an optional agentic execution mode for longer or more complex work. It can use Projects, connectors, skills, plugins, cloud sessions, sub-agent coordination, and scheduled tasks.

Use it when the task benefits from extended execution or parallel workstreams.

From the same High Director Project, start a **Cowork** task rather than a normal chat task when available. The Project provides the instructions/context and the same connectors can be used in Cowork.

Cowork is an enhancement to High Director, not a replacement for the Project architecture.

</details>

<details>
<summary>Optional: use Claude Code</summary>

Use Claude Code only when a repository task requires capabilities GitHub MCP cannot provide, such as:

```text
full repository clone
arbitrary shell commands
local build toolchains
local test execution not available through GitHub Actions
interactive development environment work
```

Return the result to High Director afterward if the broader task also involves AWS or other connected systems.

</details>
