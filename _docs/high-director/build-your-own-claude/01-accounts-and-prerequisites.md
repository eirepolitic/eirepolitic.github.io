---
title: Build Your Own Sly Director — 01 — Accounts and Prerequisites
summary: Confirm Claude, Cowork, GitHub, and AWS are available for the Sly Director build.
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

Confirm you can access the accounts and Claude features required for Sly Director.

## Complete this step

### Claude

1. Open [Claude](https://claude.ai/).
2. Sign in or create an account.
3. Open **Settings → Billing**.
4. Confirm your plan is **Pro** or another paid plan that includes Cowork.
5. Confirm you can access **Projects**.
6. Confirm **Cowork** is available as a mode.
7. Open **Customize → Connectors**.
8. Confirm you can select **Add custom connector**.

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
Custom connectors: available
GitHub account: working
AWS account: working
```

Continue to [Chapter 2 — Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }}).

<details>
<summary>Additional information</summary>

Cowork is the feature used to remove the repeated `continue` loop from substantial Sly Director work. Cloud Cowork sessions can continue while you step away and can be reopened later.

Sly Director does not depend on finding a prebuilt GitHub MCP connector in Claude's connector directory. Chapter 5 builds its own remote **Sly Director GitHub** connector.

</details>
