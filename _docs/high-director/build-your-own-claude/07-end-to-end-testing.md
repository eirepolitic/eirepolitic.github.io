---
title: Build Your Own High Director — Claude Edition 07 — End-to-End Testing
summary: Verify the Claude Project, GitHub workflow, and AWS MCP connection.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 87
permalink: /docs/high-director/build-your-own-claude/07-end-to-end-testing/
---

# Chapter 7 — End-to-End Testing

## Goal

Verify the three parts of the setup work together.

## Complete this step

### Test 1 — High Director Project

1. Open **Projects → High Director**.
2. Ask:

```text
I want to build a small data-import tool in GitHub and eventually deploy it on AWS. Plan the decisions we need before implementation.
```

### Test 2 — Claude Code repository change

1. Open Claude Code on the web.
2. Select `claude-director-test`.
3. Ask:

```text
Create a file named end-to-end-test.md containing a short explanation that this is the Claude edition end-to-end test. Verify the change, run relevant checks, and complete the repository-side workflow as far as the available tooling permits. Proceed without waiting for my approval.
```

4. Confirm the file appears in GitHub through the repository workflow.

### Test 3 — AWS MCP

1. Return to **Projects → High Director**.
2. Enable **AWS MCP** for the chat.
3. Ask:

```text
Using AWS MCP, list the S3 buckets visible to this AWS identity and identify the AWS account and identity you are using.
```

## What you should see

All three should work:

```text
High Director Project: follows project instructions
Claude Code: can modify the test repository
AWS MCP: can query the AWS account
```

Continue to [Chapter 8 — Daily Operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}).

<details>
<summary>Additional information</summary>

An empty S3 bucket list still proves the AWS connection works.

The GitHub test succeeds when the requested file reaches the intended repository state. Branches and pull requests may appear as part of that workflow.

Use the High Director Project for planning and AWS work. Use Claude Code for repository implementation.

</details>

<details>
<summary>Troubleshooting</summary>

Identify which of the three layers failed:

```text
Project behavior
GitHub / Claude Code
AWS MCP
```

Fix only that layer.

Useful prompt:

```text
I am testing my Claude High Director setup.
Working test: [Project / GitHub / AWS]
Failing test: [Project / GitHub / AWS]
Exact non-secret error: [paste it]
Identify the failing layer and give me the smallest fix.
```

</details>
