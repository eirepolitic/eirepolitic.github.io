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

## The whole plan

Build **one Claude Project called Sly Director**.

Use it in two ways:

```text
Sly Director
├─ Normal chat → quick questions, planning, small changes
└─ Cowork → substantial jobs that should keep working without you

Both use:
├─ GitHub MCP → repositories, files, branches, PRs, Actions
└─ AWS MCP → AWS resources and operations
```

That is the entire operating model.

For a small job, talk to **Sly Director** normally.

For a large job, open **Sly Director in Cowork**, give it the final objective, select **Automatically approve**, and let it continue through planning, implementation, validation, corrections, and final verification until the work is finished or it genuinely needs you.

The later **Sly Director Operator Skill** is an improvement to this same setup. It is a later implementation step in this guide, not something you need to build separately before continuing.

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

Optional later:

- [Skills, Plugins, scheduling, and specialist tools]({{ '/docs/high-director/build-your-own-claude/addendum-enhancements/' | relative_url }})
- [Google Workspace and other connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})

## What success looks like

For a substantial job, you should be able to give Sly Director one objective such as:

```text
Investigate this repository and the related AWS infrastructure. Find the cause of the problem, implement the best practical fix, validate it, correct recoverable failures, finish the repository workflow, verify the final state, and return to me when the job is complete or you genuinely need a decision from me.
```

Sly Director should then continue working in Cowork instead of repeatedly stopping just to make you type `continue`.

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
