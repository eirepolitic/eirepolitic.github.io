---
title: Build Your Own Sly Director — 04 — GitHub Access
summary: Configure Sly Director's GitHub write access using a custom remote MCP bridge because the normal Claude GitHub integration is context-oriented and the required official GitHub MCP connector is not available in the connector directory.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Give Sly Director GitHub Access

## Goal

Give Sly Director the GitHub tools it needs to investigate repositories, change files, use branches and pull requests, and inspect GitHub Actions from normal Claude and Cowork.

## Current situation

You may already have Claude's normal **GitHub integration** connected. Keep it.

That integration is useful for repository context, but it is not the full GitHub operation layer required by Sly Director.

The previously documented connector:

```text
GitHub MCP — The Official GitHub MCP Server
```

is not currently available in the connector directory used by this setup. Therefore this guide no longer depends on finding it there.

## The replacement design

Sly Director will use a **custom remote MCP connector** that we control:

```text
Sly Director / Cowork
        ↓
Claude custom remote MCP connector
        ↓
Sly Director GitHub MCP bridge
        ↓
existing GitHub backend / GitHub API
        ↓
GitHub repositories and Actions
```

The recommended implementation is a small AWS-hosted MCP adapter that reuses the GitHub functionality already built for the OpenAI High Director instead of recreating all GitHub operations.

## What you should do now

Keep your existing Claude **GitHub integration** connected.

Record your current state:

```text
Normal Claude GitHub integration: connected
Official GitHub MCP directory connector: unavailable
Sly Director GitHub MCP bridge: not built yet
```

The next implementation step is to build the Sly Director GitHub MCP bridge and then add its public remote MCP URL through:

```text
Claude → Customize → Connectors → + → Add custom connector
```

Once that bridge is connected, both normal Sly Director chat and Cowork can use the same GitHub operation tools.

## What you should see when Chapter 4 is complete

Eventually Claude should contain two separate GitHub-related connections:

```text
GitHub
→ existing Claude integration
→ useful repository context

Sly Director GitHub
→ custom remote MCP connector
→ repository write / branch / PR / Actions operations
```

Chapter 4 is complete only after the custom **Sly Director GitHub** connector can successfully read and modify the `claude-director-test` repository.

<details>
<summary>Why we are not connecting directly to GitHub's hosted MCP endpoint</summary>

GitHub provides a hosted MCP server with the GitHub tools Sly Director needs. However, GitHub's remote MCP authentication depends on the MCP host providing the required GitHub authentication integration.

The current Claude setup does not provide the required ready-to-use GitHub MCP connector in the connector directory, so directly pasting the hosted endpoint would leave an authentication gap.

A bridge that we control gives us a stable authentication boundary and lets us reuse the GitHub backend already proven by the OpenAI High Director implementation.

</details>

<details>
<summary>Why the bridge must be remote</summary>

Claude custom connectors used by claude.ai and Cowork connect from Anthropic's cloud infrastructure. The MCP server therefore needs a public internet endpoint.

A local MCP server running only on your computer would not provide the shared normal-chat + Cowork architecture required by Sly Director.

</details>

<details>
<summary>Authentication requirement</summary>

The MCP bridge should have its own authenticated Claude-facing connection rather than exposing the GitHub backend publicly without protection.

The implementation chapter will define the simplest supported authentication method before deployment. GitHub credentials remain on the server side and should not be pasted into Claude conversations.

</details>

## Next chapter

After the GitHub bridge is implemented and connected, continue to [Chapter 5 — Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).
