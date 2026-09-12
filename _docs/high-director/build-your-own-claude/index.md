---
title: Build Your Own Sly Director
summary: Browser-only setup guide for Sly Director using one Claude Project, GitHub MCP, AWS MCP, and Cowork for long-running autonomous execution.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 80
permalink: /docs/high-director/build-your-own-claude/
---

# Build Your Own Sly Director

Sly Director is the Claude-based counterpart to the OpenAI High Director.

The plan is simple:

```text
Sly Director Project
├─ Normal chat → quick, interactive work
├─ Cowork → substantial autonomous work
├─ GitHub MCP → repository access and operation
└─ AWS MCP → AWS access and operation
```

Use the **Sly Director Project** as the persistent identity and context.

Use **normal chat** when the job is small or you want to work interactively.

Use **Cowork** when the job is substantial and should keep progressing without repeated `continue` prompts. Cowork can work in the cloud, break work into subtasks, coordinate parallel workstreams, run code/shell commands in its isolated environment, use the connected GitHub/AWS tools, and continue after you step away.

That is the entire operating model.

## Build it in this order

1. [Confirm Claude, Cowork, GitHub, and AWS access]({{ '/docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/' | relative_url }})
2. [Create a GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }})
3. [Create the Sly Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }})
4. [Connect GitHub MCP]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }})
5. [Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }})
6. [Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }})
7. [Configure Cowork for autonomous Sly Director work]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }})
8. [Use Sly Director day to day]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }})
9. [Troubleshoot]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }})
10. [Maintain the setup]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }})

Optional upgrades:

- [Skills, Plugins, scheduling, and specialist tools]({{ '/docs/high-director/build-your-own-claude/addendum-enhancements/' | relative_url }})
- [Google Workspace and other connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})

<details>
<summary>How this relates to Overlord</summary>

Overlord was designed to preserve state, split plans into dependent tasks, resume after interruption, retry failed work, validate results, and only return to the owner for genuine decisions.

Cowork now provides much of that execution layer directly. Sly Director keeps the useful Overlord operating principles while relying on Cowork for long-running execution and sub-agent coordination.

</details>

<details>
<summary>Optional later upgrades</summary>

After the core setup works, a **Sly Director Operator Skill** can hold the detailed execution procedure so it loads when needed rather than living entirely in Project instructions.

A future **Sly Director Plugin** can package Skills, connectors, and Cowork specialists together.

Claude Code remains a specialist fallback when a task genuinely requires its repository-oriented development environment.

</details>
