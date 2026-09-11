---
title: Build Your Own High Director — Claude Edition 01 — Accounts and Prerequisites
summary: Create or verify the Claude, GitHub, and AWS accounts required for the browser-only Claude edition before changing repositories or cloud infrastructure.
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

At the end of this chapter you will know whether you have the three accounts needed for the core build:

```text
Claude
GitHub
AWS
```

Do not create AWS resources or change GitHub permissions yet.

## Step 1 — Create or sign in to Claude

Open [Claude](https://claude.ai/) in a desktop web browser.

### Do you already have a Claude account?

If **yes**:

1. Sign in.
2. Confirm you can open a normal Claude conversation.
3. Continue to Step 2.

If **no**:

1. Open `claude.ai`.
2. Choose the current sign-in method offered for your account, such as email or Google.
3. Complete Anthropic's account-verification flow.
4. Sign in.

Do not create an Anthropic Console/API account for this guide unless you independently need API access. Claude Pro does not include Claude API billing, and the primary build does not require the API.

## Step 2 — Check whether you already have Pro

In Claude:

1. Select your initials or account menu.
2. Open **Settings**.
3. Open **Billing** or the current plan/billing area.
4. Look for your current plan.

### If the plan says Pro

Continue to Step 3.

### If the plan is Free

As verified on 2026-09-10, Anthropic lists Claude Pro at:

```text
USD $20/month when billed monthly
USD $200/year when billed annually
```

Pricing can differ by country, currency, taxes, and platform.

Official references:

- [Choose a Claude plan](https://support.claude.com/en/articles/11049762-choose-a-claude-plan)
- [Sign up for Pro](https://support.claude.com/en/articles/8325609-how-do-i-sign-up-for-the-pro-plan)

If you want to continue with Pro:

1. In **Settings → Billing**, select **Upgrade plan**.
2. Select **Get Pro plan**.
3. Choose monthly or annual billing based on your own preference.
4. Review the current price shown to you before paying.
5. Complete the payment process only if you are authorized to make that purchase.
6. Return to Claude after the upgrade.
7. Confirm the account now shows **Pro**.

Do not purchase Max just for this guide. Start with Pro. Upgrade only later if your actual usage requires more capacity.

## Step 3 — Verify the features this guide needs

The primary build depends on these Claude features:

```text
Projects
Claude Code
Custom connectors / remote MCP
```

### Check Projects

1. Look in the Claude sidebar for **Projects**.
2. Open it.
3. Confirm you can create a project.

### Check Claude Code

Claude Pro includes Claude Code. The guide uses **Claude Code on the web**, not the terminal version.

Look for Claude Code in the Claude interface or open Anthropic's Claude Code web entry point from the Claude product interface.

You do not need to install the Claude Code CLI.

### Check Connectors

1. Open the Claude customization/settings area.
2. Find **Connectors**.
3. Confirm there is an option to add or manage connectors.
4. On an individual Pro account, look for **Add custom connector** or equivalent wording.

Anthropic currently documents remote custom connectors for Pro users.

Official reference: [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

## Step 4 — Check GitHub

Open [GitHub](https://github.com/).

### Do you already have an account?

If **yes**:

1. Sign in.
2. Select your profile picture.
3. Confirm the username is the account you want Claude Code to work with.
4. Record the username in a private setup note.

If **no**:

1. Select **Sign up**.
2. Follow GitHub's account-creation prompts.
3. Verify your email address.
4. Sign in.
5. Record your username.

Do not create a GitHub personal access token. The primary Claude Code web path does not require you to manually create one.

## Step 5 — Enable GitHub two-factor authentication

1. In GitHub, open your profile menu.
2. Select **Settings**.
3. Select **Password and authentication**.
4. Find **Two-factor authentication**.
5. Follow GitHub's current setup flow.
6. Store recovery information safely.

## Step 6 — Check AWS

Open the [AWS Management Console](https://console.aws.amazon.com/).

### Do you already control an AWS account?

If **yes**:

1. Sign in.
2. Confirm it is the account you intend to use.
3. Do not create resources yet.

If **no**:

1. Use AWS's official account-creation flow.
2. Complete the required identity, contact, payment, and verification steps shown by AWS.
3. Choose only services/support options you understand and intend to pay for.
4. Sign in to the AWS Management Console.
5. Do not create resources yet.

AWS signup requirements vary and can change. Follow the current AWS screens rather than trying to bypass an eligibility, payment, or identity requirement.

## Step 7 — Create a private setup note

Record only non-secret information:

```text
Claude plan: Pro
GitHub username:
AWS account access confirmed: yes/no
Preferred AWS region: us-east-2
```

Do not put passwords, AWS credentials, OAuth tokens, GitHub credentials, recovery codes, or payment data in the note.

## What you should see

You should now have:

- Claude Pro;
- access to Projects;
- access to Claude Code;
- access to custom connectors;
- a working GitHub account with two-factor authentication;
- access to an AWS account you control.

## If you do not see this

Resolve only the missing account/feature before continuing.

Do not buy Max, create API keys, create GitHub PATs, or create AWS access keys to solve an ordinary account-navigation problem.

## Ask ordinary Claude or ChatGPT this

```text
I am following a browser-only guide to build a High Director-style setup using Claude Pro, Claude Code on the web, GitHub, and the AWS managed MCP Server.

I am stuck at the account/prerequisite stage.
Service: [Claude / GitHub / AWS]
What I clicked: [describe it]
What I expected: [describe it]
What I see: [describe it]
Exact non-secret error: [paste it]

Do not ask me for passwords, OAuth tokens, AWS credentials, payment details, recovery codes, or other secrets. Check the current official documentation and give me click-by-click browser instructions.
```

## Next chapter

Continue to [Chapter 2 — Create and prepare GitHub]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }}).
