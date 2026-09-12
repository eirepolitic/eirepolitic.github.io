---
title: Build Your Own High Director — Claude Edition
summary: Browser-only setup guide for a High Director-style system using one Claude Project, GitHub MCP, AWS MCP, and Cowork for long-running autonomous execution.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 80
permalink: /docs/high-director/build-your-own-claude/
---

# Build Your Own High Director — Claude Edition

This edition is designed around one High Director identity with two ways to work:

```text
High Director Project
├─ Normal chat
│  └─ quick, interactive, supervised work
└─ Cowork
   └─ long-running, autonomous execution

Both use:
├─ GitHub MCP
└─ AWS MCP
```

The goal is to preserve the same mental model as the OpenAI High Director—you give High Director the objective—but remove the need to repeatedly type `continue` throughout a long implementation plan.

For substantial work, Cowork is the primary execution mode. Cowork can keep working in the cloud, break complex work into subtasks, coordinate parallel workstreams, run code/shell commands in its isolated environment, and continue after you step away.

## Architecture

```text
Claude Pro
└─ High Director Project
   ├─ project instructions
   ├─ project memory/context
   ├─ GitHub MCP
   ├─ AWS MCP
   │
   ├─ Normal chat
   │  └─ questions / planning / quick changes
   │
   └─ Cowork — PRIMARY FOR SUBSTANTIAL WORK
      ├─ long-running tasks
      ├─ automatic approval mode
      ├─ sub-agent coordination
      ├─ isolated code/shell execution
      ├─ GitHub + AWS connectors
      └─ scheduled recurring tasks

Optional later
├─ High Director Skill
├─ High Director Plugin
└─ Claude Code for specialist repository-shell work
```

## Complete the guide in this order

1. [Accounts and prerequisites]({{ '/docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/' | relative_url }})
2. [Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }})
3. [Create the High Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }})
4. [Connect GitHub MCP to High Director]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }})
5. [Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }})
6. [Connect Claude to AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }})
7. [Configure Cowork for autonomous High Director work]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }})
8. [Daily operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }})
9. [Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }})
10. [Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }})

Optional upgrades:

- [Skills, Plugins, scheduling, and specialist tools]({{ '/docs/high-director/build-your-own-claude/addendum-enhancements/' | relative_url }})
- [Google Workspace and other connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})

## What you need

- Claude Pro
- GitHub account
- AWS account
- web browser

<details>
<summary>How this relates to Overlord</summary>

The Overlord project was designed around durable orchestration: plans split into dependent tasks, retries/resume, state preservation, delegated execution, validation loops, and returning to the owner only when a genuine decision was needed.

Cowork now supplies much of that execution/orchestration layer directly inside Claude:

```text
Overlord goal                         Claude/Cowork equivalent
----------------------------------    ----------------------------------
durable long-running work             cloud Cowork sessions
task decomposition                     Cowork subtasks
parallel delegated workers             Cowork sub-agent coordination
resume after interruption              cloud session persistence
validation/retry loop                  High Director instructions + Cowork
owner interruption only when needed    Automatically approve mode
recurring autonomous work              Cowork scheduled tasks
```

Overlord-style rules are still valuable as High Director instructions and, later, a High Director Skill. Cowork replaces much of the custom execution machinery rather than the operating principles.

</details>

<details>
<summary>Additional information</summary>

Cowork runs cloud sessions remotely. Work can continue when your computer is closed, and the same session can be opened from web, desktop, or mobile.

Normal Project chat remains useful for quick work and discussion. Cowork is the preferred path when the task has many implementation steps, may take a long time, benefits from parallel work, or would otherwise require repeated `continue` prompts.

Claude Code remains a specialist fallback when a task specifically needs its repository-oriented development environment.

Official references:

- [Get started with Claude Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork)
- [Projects in Claude Cowork](https://support.claude.com/en/articles/14116274-organize-your-tasks-with-projects-in-claude-cowork)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html)

</details>
