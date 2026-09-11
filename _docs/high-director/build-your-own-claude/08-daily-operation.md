---
title: Build Your Own High Director — Claude Edition 08 — Daily Operation
summary: Use the High Director Project, Claude Code, GitHub, and AWS MCP together after setup.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 88
permalink: /docs/high-director/build-your-own-claude/08-daily-operation/
---

# Chapter 8 — Daily Operation

## Goal

Use the correct Claude surface for each type of work.

## Complete this step

### For planning or AWS work

1. Open **Projects → High Director**.
2. Describe what you want built or changed.
3. Let Claude identify any required architecture, cost, or permission decisions.
4. Enable **AWS MCP** when AWS access is needed.
5. Let Claude perform the requested AWS work.
6. Verify the result in the AWS console when appropriate.

### For repository work

1. Open Claude Code on the web.
2. Select the repository.
3. Give Claude the task and acceptance criteria.
4. Let Claude inspect, edit, test, and complete the repository workflow.
5. Verify the final repository state in GitHub.

## What you should see

Normal operation should look like:

```text
Planning/AWS → High Director Project
Repository implementation → Claude Code
```

Continue to [Chapter 9 — Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }}).

<details>
<summary>Additional information</summary>

Claude is the intended primary repository operator. Routine user approval of pull requests or merges is not part of the normal workflow.

Branches and pull requests may still be useful for automated checks, history, rollback, or repository rules.

For new repositories, create the repository in GitHub first, make sure the Claude GitHub App can access it, then open it in Claude Code.

Claude Pro and Claude Code share plan usage. A usage-limit message is a Claude-plan issue, not a GitHub or AWS authentication failure.

</details>

<details>
<summary>Useful prompts</summary>

Repository task:

```text
Inspect this repository and implement the following requirement: [requirement]. Run the relevant checks and complete the repository workflow as far as the available tooling permits.
```

AWS task:

```text
Using AWS MCP, complete this task: [task]. Use us-east-2 for new workload resources unless the service or requirement needs another region.
```

</details>
