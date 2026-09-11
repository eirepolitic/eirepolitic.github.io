---
title: Build Your Own High Director — Claude Edition
summary: A zero-assumed-knowledge, browser-only guide for building a High Director-style personal agent using Claude Pro, Claude Projects, Claude Code on the web, GitHub, and the managed AWS MCP Server.
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

## What this guide does

This is the Claude/Anthropic counterpart to [Build Your Own High Director]({{ '/docs/high-director/build-your-own/' | relative_url }}).

It is written for a person who may have no GitHub repositories, no AWS account, no knowledge of Git, no programming experience, and no locally installed development tools.

The entire primary path is browser-based.

## Cheapest and easiest architecture

The recommended implementation is:

```text
You
 |
 v
Claude Pro
 |
 +-- Claude Project
 |     persistent High Director instructions
 |
 +-- Claude Code on the web
 |     primary repository modifier/operator
 |     file changes
 |     tests
 |     branches / pull requests when useful
 |     automated repository completion
 |
 +-- Custom connector
       |
       v
   AWS managed MCP Server
       |
       v
   Your AWS account
   S3 / Lambda / CloudWatch /
   Step Functions / other AWS services
```

This design intentionally avoids rebuilding the custom AWS Lambda GitHub gateway used by the ChatGPT edition.

## Repository operating model

The Claude edition assumes the agent is the primary modifier and operator of its connected repositories.

Normal repository changes should not require the user to inspect or approve each pull request or merge.

Claude may still use branches, pull requests, CI checks, and merges when they improve traceability, isolation, rollback, or automated verification. Those mechanisms are repository-control tools, not mandatory human approval gates.

Where Claude Code web produces a pull request, the intended long-term repository workflow is:

```text
Claude implementation
→ automated tests/checks
→ automated merge/completion where supported
→ Claude verifies final repository state
```

If a simpler supported direct-write path is appropriate for a repository, the agent may use that instead.

## Why this architecture was chosen

As verified on 2026-09-10:

- Claude Pro costs USD $20/month when billed monthly or USD $200/year when billed annually.
- Claude Code is included with Claude Pro.
- Claude Projects provide persistent project instructions and project knowledge.
- Claude supports remote MCP connectors on Pro.
- AWS provides a managed AWS MCP Server at no additional charge beyond the AWS resources the agent uses.
- AWS recommends OAuth for human users working through web clients and states that no local MCP proxy is required for that path.

Official references:

- [Claude pricing](https://claude.com/pricing)
- [Claude Pro](https://support.claude.com/en/articles/8325606-what-is-the-pro-plan)
- [Claude Projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects)
- [Claude custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [AWS MCP Server setup](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/getting-started-aws-mcp-server.html)
- [AWS MCP Server overview and pricing](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/what-is-agent-toolkit.html)

## Important difference from the ChatGPT edition

The ChatGPT implementation needs a custom Action, OpenAPI schema, Function URL, application API key, GitHub personal access token, and Lambda wrapper because the custom GPT needs a bridge to GitHub.

The Claude edition does not use that bridge for normal repository development.

Claude Code handles repository work directly through its GitHub integration. The AWS integration uses AWS's managed MCP server instead of another custom Lambda gateway.

That means the Claude edition has fewer credentials and fewer moving parts.

## What you will be able to do

After the core guide is complete, you should be able to:

- keep High Director-style instructions in a Claude Project;
- ask Claude to plan technical work in beginner-friendly language;
- use Claude Code on the web as the main operator of GitHub repositories;
- create and edit code and documentation;
- run tests in Claude Code's cloud environment;
- use branches and pull requests when useful without making the user a routine approval gate;
- configure repository changes to complete automatically where supported;
- create new GitHub repositories through the GitHub website and then hand them to Claude Code;
- connect Claude to AWS through the managed AWS MCP Server;
- let Claude inspect or operate AWS resources only within the permissions of the AWS identity you authorize.

## What this guide does not assume

You do not need:

- Python installed locally;
- Git installed locally;
- an AWS CLI installation;
- VS Code or another IDE;
- a local terminal;
- an Anthropic API account;
- paid Claude API usage;
- a custom Lambda gateway for GitHub;
- a GitHub personal access token for the primary Claude Code path.

Claude Pro and Claude API billing are separate products. This guide uses the Claude Pro subscription and does not require API billing for the primary path.

## Before you start

Answer these questions.

### Do you already have a Claude account?

- **Yes:** Chapter 1 will verify the plan and available features.
- **No:** Chapter 1 starts from account creation.

### Do you already have Claude Pro?

- **Yes:** continue with the verification steps in Chapter 1.
- **No:** Chapter 1 shows the current upgrade path and tells you what to verify before paying.

### Do you already have GitHub?

- **Yes:** Chapter 2 will create a disposable test repository if needed.
- **No:** Chapter 2 includes GitHub account creation.

### Do you already have AWS?

- **Yes:** Chapter 5 starts with account and billing checks.
- **No:** Chapter 5 includes AWS account creation guidance.

## Core chapters

Follow these in order for the first build:

1. [Accounts and prerequisites]({{ '/docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/' | relative_url }})
2. [Create and prepare GitHub]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }})
3. [Create the High Director Claude Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }})
4. [Connect and use Claude Code on the web]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }})
5. [Create and prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }})
6. [Connect Claude to the AWS MCP Server]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }})
7. [End-to-end testing]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }})
8. [Daily operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }})
9. [Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }})
10. [Maintenance and access review]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }})

Optional addenda:

- [Google Workspace and other Claude connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Advanced custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})

## Standard checkpoint format

Every major chapter ends with:

### What you should see

The expected successful state.

### If you do not see this

The smallest safe checks to perform.

### Ask ordinary Claude or ChatGPT this

A copy/paste troubleshooting prompt that excludes credentials and private information.

## Credential rule

Never paste these values into documentation or an ordinary troubleshooting conversation:

- passwords;
- AWS access keys or secret keys;
- OAuth tokens;
- GitHub credentials;
- private repository secrets;
- payment information.

The primary architecture is deliberately designed so you do not need to manually create a GitHub PAT or a custom application API key.
