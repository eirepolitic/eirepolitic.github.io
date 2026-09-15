---
title: Build Your Own Sly Director
summary: Beginner-friendly, browser-based guide to building the live-verified Sly Director setup with Claude, GitHub, AWS, WorkOS AuthKit, and Cowork.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 80
permalink: /docs/high-director/build-your-own-claude/
---

# Build Your Own Sly Director

This guide shows you how to build the same Sly Director setup that has been tested end to end.

You do **not** need to be a programmer. Every chapter tells you what to click, what to enter, and what result to expect.

## What you are building

Sly Director is one Claude Project that can work in two modes:

```text
Normal Claude chat
→ quick questions and smaller tasks

Cowork
→ longer jobs that should keep working without repeated “continue” prompts
```

Sly Director gets two important connections:

```text
Sly Director GitHub
→ reads and changes GitHub repositories
→ creates branches and pull requests
→ checks GitHub Actions
→ merges validated work

AWS MCP
→ inspects and manages AWS resources
```

The GitHub connection is protected by WorkOS AuthKit and runs from a small AWS Lambda function.

## Accounts you will need

You will create or use:

- a Claude account with Cowork access;
- a GitHub account;
- an AWS account;
- a WorkOS account.

The guide starts from zero and walks through each one.

## Build it in this order

1. [Create the required accounts and check access]({{ '/docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/' | relative_url }})
2. [Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }})
3. [Create the Sly Director Claude Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }})
4. [Prepare AWS and create the Sly Director AWS administrator user]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }})
5. [Build the Sly Director GitHub connector]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }})
6. [Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }})
7. [Test the full setup in Cowork]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }})
8. [Use Sly Director day to day]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }})
9. [Troubleshoot common problems]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }})
10. [Maintain the setup]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }})

## What success looks like

At the end, you can give Cowork one outcome such as:

```text
Inspect this repository and the related AWS resources. Find the problem, implement the best practical fix, validate it, correct recoverable failures, complete the repository workflow, and return when the requested outcome is finished or you genuinely need a decision from me.
```

Sly Director can then use GitHub and AWS directly and continue through multiple steps without handing the task back to you after every action.

> This guide intentionally contains only the working setup. Historical Cognito experiments and development-only debugging notes have been removed from the main build path.
