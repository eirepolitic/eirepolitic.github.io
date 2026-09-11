---
title: Build Your Own High Director — Claude Edition 01 — Accounts and Prerequisites
summary: Confirm the Claude, GitHub, and AWS accounts needed for the browser-only setup.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 81
permalink: /docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/
---

# Chapter 1 — Accounts and Prerequisites

## Goal

Confirm you can access Claude Pro, GitHub, and AWS.

## Complete this step

### Claude

1. Open [Claude](https://claude.ai/).
2. Sign in or create an account.
3. Open **Settings → Billing**.
4. Confirm your plan is **Pro**.
5. In Claude, confirm you can access **Projects**.
6. Open **Customize → Connectors** and confirm you can add connectors.

### GitHub

1. Open [GitHub](https://github.com/).
2. Sign in or create an account.
3. Record your GitHub username.

### AWS

1. Open the [AWS Management Console](https://console.aws.amazon.com/).
2. Sign in or create an AWS account.
3. Confirm you can reach the AWS console home page.

## What you should see

You should now have:

```text
Claude Pro: yes
Claude Projects: available
Claude Connectors: available
GitHub account: working
AWS account: working
```

Continue to [Chapter 2 — Create the GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }}).

<details>
<summary>Additional information</summary>

Claude Pro currently includes Claude Code. Claude API usage is billed separately and is not needed for this guide.

GitHub two-factor authentication is optional unless GitHub itself requires it for your account.

For AWS, use an account you control and are authorized to operate.

</details>

<details>
<summary>Troubleshooting</summary>

If one account or feature is missing, resolve only that item before continuing.

Useful prompt:

```text
I am following a browser-only Claude High Director setup guide.
Service: [Claude / GitHub / AWS]
I am stuck at: [describe step]
What I see: [describe screen]
Exact non-secret error: [paste it]
Give me current click-by-click browser instructions.
```

</details>
