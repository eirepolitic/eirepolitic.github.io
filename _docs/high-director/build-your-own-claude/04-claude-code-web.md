---
title: Build Your Own Sly Director — 04 — Connect GitHub MCP
summary: Connect the official GitHub MCP connector directly to the Sly Director Project.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Connect GitHub MCP

## Goal

Give the **Sly Director Project** direct GitHub tools so it can investigate and modify repositories.

## Complete this step

1. Open normal Claude.
2. Open **Customize → Connectors**.
3. Search for:

```text
GitHub MCP
```

4. Select **GitHub MCP — The Official GitHub MCP Server**.
5. Select **Connect**, **Add**, or the current equivalent.
6. Complete the GitHub sign-in/authorization flow.
7. Grant access to the GitHub account and repositories you want Sly Director to operate.
8. Return to Claude.
9. Open **Projects → Sly Director**.
10. Start a new chat.
11. Select **+ → Connectors**.
12. Enable **GitHub MCP**.
13. Ask:

```text
Using GitHub MCP, inspect the repository claude-director-test. List the files in the default branch and read README.md and claude-test.txt.
```

14. After that succeeds, ask in the same chat:

```text
Using GitHub MCP, create a file named github-mcp-test.md containing:

# GitHub MCP test
This file was created from the Sly Director Project through GitHub MCP.

Complete the repository-side workflow as far as the available GitHub tools and repository permissions allow without waiting for my approval.
```

15. Open GitHub and confirm the change reached the repository.

## What you should see

The Sly Director Project should be able to read and modify the test repository directly.

Continue to [Chapter 5 — Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).

<details>
<summary>Additional information</summary>

The official GitHub MCP Server exposes repository, pull-request, issue, workflow/Actions, and other GitHub capabilities.

Claude Code is not required for normal Sly Director repository operation. It remains a specialist fallback for tasks that need its repository-oriented development environment.

</details>
