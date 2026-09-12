---
title: Build Your Own High Director — Claude Edition 01 — Accounts and Prerequisites
summary: Confirm the Claude, GitHub, and AWS accounts needed for the single-chat browser setup.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 81
permalink: /docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/
---

# Chapter 1 — Accounts and Prerequisites

## Goal

Confirm you can access Claude Pro, GitHub, AWS, Projects, and connectors.

## Complete this step

### Claude

1. Open [Claude](https://claude.ai/).
2. Sign in or create an account.
3. Open **Settings → Billing**.
4. Confirm your plan is **Pro**.
5. Confirm you can access **Projects**.
6. Open **Customize → Connectors**.
7. Confirm you can browse/add connectors.
8. Search the connector directory for:

```text
GitHub MCP
```

9. Confirm **GitHub MCP — The Official GitHub MCP Server** is available.

### GitHub

1. Open [GitHub](https://github.com/).
2. Sign in or create an account.
3. Record your GitHub username.

### AWS

1. Open the [AWS Management Console](https://console.aws.amazon.com/).
2. Sign in or create an AWS account.
3. Confirm you can reach the AWS console home page.

## What you should see

```text
Claude Pro: yes
Projects: available
Connectors: available
GitHub MCP: available
GitHub account: working
AWS account: working
```

Continue to [Chapter 2 — Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }}).

<details>
<summary>Additional information</summary>

Claude Code and Cowork are useful optional capabilities, but neither is required for the core one-chat High Director setup.

The core design uses remote MCP connectors inside normal Claude chat:

```text
High Director Project
├─ GitHub MCP
└─ AWS MCP
```

</details>

<details>
<summary>Troubleshooting</summary>

If **GitHub MCP** is missing from the connector directory, verify current Claude connector availability before continuing because Chapter 4 depends on that connector for the single-chat interaction model.

</details>
