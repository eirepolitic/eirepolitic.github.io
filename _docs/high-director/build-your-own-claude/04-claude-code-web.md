---
title: Build Your Own Sly Director — 04 — Connect GitHub MCP
summary: Connect the official GitHub MCP connector directly to the Sly Director Project so repository work can stay in one place.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Connect GitHub MCP to Sly Director

## Goal

Give the **Sly Director Project** direct GitHub tools so it can investigate and modify repositories without switching to Claude Code.

## Complete this step

1. Open normal Claude.
2. Open **Customize → Connectors**.
3. Search the connector directory for:

```text
GitHub MCP
```

4. Select **GitHub MCP — The Official GitHub MCP Server**.
5. Select **Connect**, **Add**, or the current equivalent.
6. Complete the GitHub sign-in/authorization flow Claude opens.
7. Grant access to the GitHub account and repositories you want Sly Director to operate.
8. Return to Claude.
9. Open **Projects → Sly Director**.
10. Start a new chat.
11. Select the **+** button near the message box.
12. Open **Connectors**.
13. Enable **GitHub MCP**.
14. Ask:

```text
Using GitHub MCP, inspect the repository claude-director-test. List the files in the default branch and read README.md and claude-test.txt.
```

15. After that succeeds, ask in the **same chat**:

```text
Using GitHub MCP, create a new file named github-mcp-test.md containing:

# GitHub MCP test
This file was created from the Sly Director Project through GitHub MCP.

Use the repository workflow that gives the clearest history with the least unnecessary overhead. Complete the change without waiting for my approval where the available GitHub tools and repository permissions allow it.
```

16. Open GitHub and confirm the change reached the repository.

## What you should see

The **Sly Director Project** should be able to:

```text
read repository files
investigate repository contents
create or update repository content
use branches / pull requests where appropriate
```

Continue to [Chapter 5 — Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).

<details>
<summary>Additional information</summary>

The official GitHub MCP Server is designed for multi-step GitHub workflows and exposes repository, pull-request, issue, workflow/Actions, and other GitHub capabilities.

The hosted GitHub MCP endpoint is:

```text
https://api.githubcopilot.com/mcp/
```

Using the connector-directory entry is preferred because Claude handles the host-side connector configuration and authentication flow.

Claude Code is no longer required for normal repository operation in this guide.

Use Claude Code only when a task specifically needs a cloned repository, shell commands, local build tools, or tests that cannot be run through GitHub Actions or other connected services.

Official reference: [GitHub MCP Server](https://github.com/github/github-mcp-server).

</details>

<details>
<summary>If GitHub MCP is missing from the connector directory</summary>

Claude currently lists **GitHub MCP — The Official GitHub MCP Server** as compatible with Claude and Claude Code.

If it is unavailable in your account, check current connector availability before falling back to a custom connector.

For a custom remote setup, the official hosted endpoint is:

```text
https://api.githubcopilot.com/mcp/
```

GitHub notes that OAuth support depends on the MCP host's GitHub OAuth/GitHub App integration. Prefer Claude's published connector-directory entry when available.

</details>

<details>
<summary>Troubleshooting</summary>

If Sly Director can read but cannot write, preserve the exact GitHub MCP error and check the GitHub authorization/repository permissions.

If a particular GitHub operation is unavailable, ask Sly Director which GitHub MCP tools are currently exposed before changing the architecture.

Useful prompt:

```text
I am using the official GitHub MCP connector inside my Claude Sly Director Project.
Repository: claude-director-test
Failing operation: [read / search / create file / branch / PR / merge / workflow]
Exact non-secret error: [paste it]
Identify whether this is connector authorization, repository permissions, repository rules, or a missing GitHub MCP tool.
```

</details>
