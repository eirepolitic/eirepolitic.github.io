---
title: Build Your Own High Director — Claude Edition
summary: Browser-only setup guide for a High Director-style personal agent using Claude Pro, Claude Projects, Claude Code on the web, GitHub, and the managed AWS MCP Server.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 80
permalink: /docs/high-director/build-your-own-claude/
---

# Build Your Own High Director — Claude Edition

This guide is designed to be followed in order.

Each chapter is structured the same way:

```text
Goal
→ Complete this step
→ What you should see
→ Additional information (expand only if needed)
→ Troubleshooting (expand only if needed)
```

The main instructions contain only the shortest path needed to continue.

## Architecture

```text
Claude Pro
├─ High Director Project
│  └─ planning, instructions, AWS connector
├─ Claude Code on the web
│  └─ GitHub repository operation
└─ AWS MCP connector
   └─ AWS account
```

## Complete the guide in this order

1. [Accounts and prerequisites]({{ '/docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/' | relative_url }})
2. [Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }})
3. [Create the High Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }})
4. [Connect Claude Code to GitHub]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }})
5. [Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }})
6. [Connect Claude to AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }})
7. [Run end-to-end tests]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }})
8. [Daily operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }})
9. [Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }})
10. [Maintenance]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }})

Optional:

- [Google Workspace and other connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})

## What you need

- Claude Pro
- GitHub account
- AWS account
- web browser

<details>
<summary>Additional information</summary>

Claude Code is included with Claude Pro. Claude API billing is separate and is not required for this guide.

The primary setup uses Claude Code's GitHub integration and AWS's managed MCP Server, so it does not require the custom Lambda/OpenAPI bridge used by the ChatGPT edition.

Claude is intended to act as the primary repository operator. Branches and pull requests may still be used for tests, history, rollback, or repository rules, but routine user approval is not part of the intended workflow.

Official references:

- [Claude Pro](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)
- [Claude Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)
- [Claude custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [AWS MCP Server](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html)

</details>
