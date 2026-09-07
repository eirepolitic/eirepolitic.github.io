---
title: Build Your Own High Director 01 — Accounts and Prerequisites
summary: Determine which accounts you already have, which ones you need, and whether your ChatGPT account can create or edit a custom GPT before you build anything.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 61
permalink: /docs/high-director/build-your-own/01-accounts-and-prerequisites/
---

# Chapter 1 — Accounts and Prerequisites

## Goal

At the end of this chapter you should know whether you can complete the build and which accounts you still need to create.

Do not create AWS resources or GitHub credentials until you finish this chapter.

## What you need for the core build

You need access to:

1. a web browser;
2. an email account you can receive verification messages at;
3. a ChatGPT account that can either edit an existing custom GPT or create a new one in an eligible workspace;
4. a GitHub account;
5. an AWS account that you control.

Google is optional and is not required for the core build.

## Step 1 — Check your ChatGPT situation

Open ChatGPT in a desktop web browser.

### Do you already own a custom GPT that you can edit?

If **yes**:

1. Open **Explore GPTs** in the ChatGPT sidebar.
2. Open **My GPTs**.
3. Find the GPT you own.
4. Open it.
5. Select **Edit GPT**.
6. If the editor opens, you have passed this check.
7. Do not change anything yet.
8. Return to this chapter.

If **no**, continue below.

### Are you in a Business, Enterprise, or Edu workspace?

As verified on 2026-09-07, OpenAI's current help documentation states that personal Free, Go, Plus, and Pro accounts cannot create new GPTs. New GPT creation is available in Business, Enterprise, and Edu workspaces when the workspace settings and your permissions allow it.

Official reference: [OpenAI — Creating and editing GPTs](https://help.openai.com/en/articles/8554397-creating-a-gpt).

If you are already in an eligible workspace:

1. In ChatGPT, use the workspace selector if one is shown.
2. Select the Business, Enterprise, or Edu workspace.
3. Open **Explore GPTs**.
4. Look for **Create**.
5. If **Create** is present, you have passed this check.
6. Do not create the GPT yet; Chapter 7 will provide the exact configuration.

If you are not in an eligible workspace:

1. Do **not** buy a plan until you have checked its current price, terms, account eligibility, and whether it supports GPT creation for your account.
2. Read the current OpenAI plan information presented in ChatGPT or on OpenAI's official pricing pages.
3. If you are not authorized to purchase or administer the account yourself, ask the account owner or responsible adult/administrator to handle the subscription decision.
4. Continue only after you have a workspace where **Explore GPTs → Create** is available, or an existing GPT you are allowed to edit.

### Stop condition

If you cannot create a GPT and do not have an existing editable GPT, stop here. The GitHub and AWS pieces can be built independently, but you will not be able to connect them to a new custom GPT until the ChatGPT account requirement is resolved.

## Step 2 — Check whether you have a GitHub account

Open [GitHub](https://github.com/) in your browser.

### Do you see your profile picture or avatar in the upper-right area?

If **yes**:

1. Select your avatar.
2. Confirm the displayed account name is the account you want the future GPT to control.
3. Write the GitHub username in a private note for later. A username is not a secret.
4. Sign out if this is a shared computer, then sign back in to verify you know how to access the account.

If **no**:

1. Select **Sign up**.
2. Follow GitHub's prompts to create an account.
3. Use an email address you control.
4. Choose a username you are comfortable using in repository URLs.
5. Create a strong, unique password.
6. Complete GitHub's email verification.
7. Sign in.
8. Write down the username in a private note.

Do not create a personal access token yet. Chapter 3 handles that separately so the permission choices are deliberate.

## Step 3 — Turn on two-factor authentication for GitHub

Two-factor authentication protects the account that the future GPT will be able to modify.

1. In GitHub, select your profile picture.
2. Select **Settings**.
3. In the left sidebar, select **Password and authentication**.
4. Find the **Two-factor authentication** section.
5. Follow GitHub's current setup flow.
6. Store recovery codes in a safe location that is not a public repository.
7. Return to GitHub Settings when finished.

If your screen wording differs, use GitHub's settings search or current two-factor authentication help page rather than guessing.

## Step 4 — Check whether you have an AWS account

Open the [AWS Management Console](https://console.aws.amazon.com/).

### Can you sign in to an AWS account you control?

If **yes**:

1. Sign in.
2. Confirm you are in the intended account.
3. Do not create a Lambda function yet.
4. Chapter 4 will perform the account-safety and billing checks first.

If **no**:

1. Open the AWS account creation flow from the official AWS site.
2. Follow the prompts for email, account name, contact information, payment method if required, identity verification, and support-plan selection.
3. Read every price or billing statement shown during signup.
4. Do not choose a paid support tier simply for this guide unless you independently want it.
5. Finish signup and sign in to the AWS Management Console.
6. Do not create resources yet.

AWS account signup requirements can vary by country and can change. Follow AWS's current on-screen requirements. Do not try to work around an eligibility, identity, payment, or age requirement.

## Step 5 — Create a private setup record

Create a private note using a trusted notes application. Do not put this note in a public GitHub repository.

Record only these non-secret items for now:

```text
ChatGPT path: existing editable GPT / eligible workspace
GitHub username:
AWS account access confirmed: yes/no
Preferred AWS region: us-east-2
Default Git branch: main
Future branch prefix: gpt
```

For this guide, use `us-east-2` unless you have a specific reason to use another AWS region. That matches the verified High Director deployment and reduces unnecessary differences during the first build.

Do **not** put passwords, personal access tokens, API keys, AWS secret keys, recovery codes, or OAuth secrets in this setup record.

## What you should see

You should now have:

- a ChatGPT path that permits editing or creating the GPT;
- a working GitHub account with its username recorded;
- two-factor authentication configured for GitHub;
- access to an AWS account;
- no Lambda resources or GitHub token created yet.

## If you do not see this

Do not compensate by creating extra accounts, changing permissions randomly, or purchasing unrelated services.

Resolve only the failed account check. Use the service's official account-help pages if the problem is login, verification, billing, workspace permission, or account eligibility.

## Ask ordinary ChatGPT this

Copy this prompt into a normal ChatGPT conversation. Replace the bracketed text, but do not paste secrets.

```text
I am following a browser-only guide to build a custom GPT that connects to GitHub through AWS Lambda.

I am stuck at the account/prerequisite stage.
Service: [ChatGPT / GitHub / AWS]
What I clicked: [describe the clicks]
What I expected to see: [describe it]
What I actually see: [describe it]
Exact non-secret error text: [paste it]

Do not ask me to paste passwords, API keys, tokens, recovery codes, payment information, or other secrets. Give me click-by-click troubleshooting steps using the current interface.
```

## Next chapter

Continue to [Chapter 2 — Create and prepare GitHub]({{ '/docs/high-director/build-your-own/02-github-account-and-first-repository/' | relative_url }}).
