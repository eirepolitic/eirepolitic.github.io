---
title: Build Your Own Sly Director — 01 — Accounts and Prerequisites
summary: Confirm Claude Pro, Cowork, GitHub MCP, GitHub, and AWS are available for the Sly Director build.
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

Confirm you can access the features required for the Cowork-first Sly Director setup.

## Complete this step

### Claude

1. Open [Claude](https://claude.ai/).
2. Sign in or create an account.
3. Open **Settings → Billing**.
4. Confirm your plan is **Pro** or another paid plan that includes Cowork.
5. Confirm you can access **Projects**.
6. In the Claude message box, confirm **Cowork** is available as a mode.
7. Open **Customize → Connectors**.
8. Confirm you can browse/add connectors.
9. Search for:

```text
GitHub MCP
```

10. Confirm **GitHub MCP — The Official GitHub MCP Server** is available.

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
Claude paid plan: yes
Projects: available
Cowork: available
Connectors: available
GitHub MCP: available
GitHub account: working
AWS account: working
```

Continue to [Chapter 2 — Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }}).

<details>
<summary>Additional information</summary>

Cowork is the key feature used to remove the repeated `continue` loop from substantial Sly Director work. Cloud Cowork sessions can continue while you step away and can be reopened from another supported device.

Normal Claude Project chat remains part of the system for quick work and discussion.

</details>

<details>
<summary>Troubleshooting</summary>

If Cowork is missing, verify the current Claude plan/product availability before continuing because Chapter 7 depends on Cowork for long-running autonomous execution.

If GitHub MCP is missing, verify current connector availability before Chapter 4.

</details>
