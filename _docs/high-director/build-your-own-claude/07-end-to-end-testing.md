---
title: Build Your Own High Director — Claude Edition 07 — End-to-End Testing
summary: Verify GitHub and AWS can both be operated from the same High Director Project chat.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 87
permalink: /docs/high-director/build-your-own-claude/07-end-to-end-testing/
---

# Chapter 7 — Single-Chat End-to-End Test

## Goal

Prove that one High Director Project chat can investigate GitHub, change a repository, and use AWS.

## Complete this step

1. Open **Projects → High Director**.
2. Start one new chat.
3. Enable both connectors from the **+ → Connectors** menu:

```text
GitHub MCP
AWS MCP
```

4. Send this single task:

```text
Using the connected GitHub and AWS tools, investigate the repository claude-director-test and the AWS account available through AWS MCP.

Then:
1. summarize the current repository contents;
2. create a file named single-chat-test.md containing a short note that the Claude High Director single-chat workflow is working;
3. complete the repository-side workflow as far as the available GitHub tools and repository permissions permit;
4. list the S3 buckets visible to the connected AWS identity;
5. report the final GitHub and AWS state.

Complete the work from this High Director conversation without sending me to Claude Code unless a required capability is genuinely unavailable through the connected tools.
```

5. Let Claude use both connectors.
6. Open GitHub and confirm `single-chat-test.md` exists in the intended final state.
7. Confirm Claude returned the AWS S3 result in the same conversation.

## What you should see

One High Director chat should complete both paths:

```text
High Director chat
├─ GitHub MCP → repository investigation and change
└─ AWS MCP → AWS query
```

Continue to [Chapter 8 — Daily Operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}).

<details>
<summary>Additional information</summary>

This is the defining test for the redesigned Claude edition. If you must manually transfer a plan into Claude Code for ordinary repository work, the core one-chat design is not functioning as intended.

Claude Code remains a valid optional escalation path for tasks that need shell execution or a full cloned-repository environment.

</details>

<details>
<summary>Troubleshooting</summary>

If AWS works but GitHub cannot write, focus on GitHub MCP authorization/tools.

If GitHub works but AWS fails, focus on AWS MCP/OAuth.

If Claude ignores an enabled connector, explicitly say:

```text
Use the connected GitHub MCP tools to perform the repository operation directly from this chat.
```

</details>
