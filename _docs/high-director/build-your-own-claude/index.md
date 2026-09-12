---
title: Build Your Own High Director — Claude Edition
summary: Browser-only setup guide for a single-chat High Director-style agent using Claude Pro, Claude Projects, GitHub MCP, and AWS MCP.
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

This edition is designed to match the interaction model of the OpenAI High Director:

```text
ONE High Director chat
├─ investigate GitHub repositories
├─ read and change repository files
├─ create branches and pull requests
├─ inspect and operate GitHub workflows
├─ use AWS
├─ troubleshoot
└─ continue the same project conversation
```

The main interface is the **High Director Project in normal Claude**.

Claude Code is optional and is only used when a task specifically benefits from a full cloned-repository shell environment.

## Architecture

```text
Claude Pro
└─ High Director Project — PRIMARY INTERFACE
   ├─ Project instructions
   ├─ GitHub MCP connector
   │  └─ repositories / branches / PRs / Actions
   └─ AWS MCP connector
      └─ AWS account

Optional upgrades
├─ High Director Skill
├─ Cowork
├─ Claude Code
└─ Plugins
```

## Complete the guide in this order

1. [Accounts and prerequisites]({{ '/docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/' | relative_url }})
2. [Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }})
3. [Create the High Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }})
4. [Connect GitHub MCP to High Director]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }})
5. [Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }})
6. [Connect Claude to AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }})
7. [Run the single-chat end-to-end test]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }})
8. [Daily operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }})
9. [Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }})
10. [Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }})

Optional upgrades:

- [Skills, Cowork, Claude Code, and Plugins]({{ '/docs/high-director/build-your-own-claude/addendum-enhancements/' | relative_url }})
- [Google Workspace and other connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})

## What you need

- Claude Pro
- GitHub account
- AWS account
- web browser

<details>
<summary>Additional information</summary>

The official GitHub MCP Server provides tools for repository files, branches, pull requests, issues, releases, code/security features, and GitHub Actions. Claude's connector system makes remote MCP tools available inside ordinary Claude conversations.

This is what makes the single-chat design possible: GitHub and AWS are both tools of the same High Director Project conversation.

Claude Code remains useful, but it is no longer the normal repository path. It is an optional specialist environment for tasks that need a cloned repository, shell commands, local builds, or tests that cannot be performed through GitHub Actions.

Official references:

- [Claude custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [GitHub MCP Server](https://github.com/github/github-mcp-server)
- [AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html)

</details>
