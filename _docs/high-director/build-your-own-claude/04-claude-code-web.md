---
title: Build Your Own Sly Director — 04 — Connect GitHub MCP
summary: Distinguish Claude's normal GitHub integration from the GitHub MCP connector required for Sly Director repository operations.
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

## First — check which GitHub connection you already have

If **GitHub** already appears under your Claude connectors, that does **not automatically mean GitHub MCP is connected**.

Claude's normal **GitHub integration** is primarily for bringing repository files/content into Claude as context.

The connector this chapter requires is:

```text
GitHub MCP — The Official GitHub MCP Server
```

That connector provides the GitHub tools Sly Director needs for repository operations such as reading/writing files, branches, pull requests, and GitHub Actions.

## Complete this step

1. Open normal Claude.
2. Open **Customize → Connectors**.
3. Open the connector directory / add-connector view rather than only the list of connectors you already connected.
4. Search for:

```text
GitHub MCP
```

5. Look specifically for:

```text
GitHub MCP — The Official GitHub MCP Server
```

### If you see it

6. Select it.
7. Select **Connect**, **Add**, or the current equivalent.
8. Complete the GitHub sign-in/authorization flow.
9. Grant access to the GitHub account and repositories you want Sly Director to operate.
10. Return to Claude.
11. Open **Projects → Sly Director**.
12. Start a new chat.
13. Select **+ → Connectors**.
14. Enable **GitHub MCP**.
15. Ask:

```text
Using GitHub MCP, inspect the repository claude-director-test. List the files in the default branch and read README.md and claude-test.txt.
```

16. After that succeeds, ask in the same chat:

```text
Using GitHub MCP, create a file named github-mcp-test.md containing:

# GitHub MCP test
This file was created from the Sly Director Project through GitHub MCP.

Complete the repository-side workflow as far as the available GitHub tools and repository permissions allow without waiting for my approval.
```

17. Open GitHub and confirm the change reached the repository.

### If you cannot see GitHub MCP

Stop at this chapter for the moment.

Your existing **GitHub integration** is still useful, but it does not by itself prove that Sly Director has the full GitHub write/action toolset required by this design.

Do not replace it with an arbitrary custom connector configuration just to get past this step. The hosted GitHub MCP OAuth connection depends on host-side integration details, so the reliable path is to use Claude's official GitHub MCP connector when it is available to your account.

Record:

```text
Normal GitHub integration connected: yes
GitHub MCP visible in connector directory: no
```

Then verify current Claude connector availability before continuing with the single-chat repository-operation design.

## What you should see

When this chapter is complete, **GitHub MCP** should appear as a separate usable connector/tool in Sly Director, even if the normal **GitHub** integration is also connected.

Continue to [Chapter 5 — Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).

<details>
<summary>What is the difference?</summary>

Think of them like this:

```text
GitHub integration
→ gives Claude repository content/context
→ useful for reading and discussing code

GitHub MCP
→ gives Sly Director GitHub operation tools
→ required for the one-chat repository workflow in this guide
```

The official GitHub MCP Server exposes repository, pull-request, issue, workflow/Actions, and other GitHub capabilities.

Claude Code is not required for normal Sly Director repository operation once GitHub MCP is available. It remains a specialist fallback for tasks that need its repository-oriented development environment.

</details>
