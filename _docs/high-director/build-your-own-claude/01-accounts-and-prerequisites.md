---
title: Build Your Own Sly Director — 01 — Accounts and Access
summary: Create the four accounts needed for Sly Director and confirm the required features are available.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 81
permalink: /docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/
---

# Chapter 1 — Create the Required Accounts

## Goal

Make sure you can sign in to the four services used by Sly Director.

You need:

```text
Claude
GitHub
AWS
WorkOS
```

You do not need to connect them yet.

## Step 1 — Claude

1. Open Claude in your browser.
2. Create an account or sign in.
3. Confirm you can see **Projects**.
4. Confirm you can open **Cowork**.

Cowork is the part of Claude that will handle longer, multi-step jobs later in the guide.

If Cowork is not available on your account, stop here and choose a Claude plan that includes it before continuing.

## Step 2 — GitHub

1. Open GitHub.
2. Create an account or sign in.
3. Confirm you can open your profile page.

GitHub will store the code and files Sly Director works on.

## Step 3 — AWS

1. Open the AWS website.
2. Create an AWS account if you do not already have one.
3. Sign in to the **AWS Management Console** as the account owner/root user for this initial setup only.
4. Confirm you can see the AWS Console home page.

AWS will run the small GitHub connector and provide Sly Director with AWS tools.

> Later in the guide you will create a separate administrator user for Sly Director. Do not use the root account for the final Claude connection.

## Step 4 — WorkOS

1. Open WorkOS.
2. Create an account or sign in.
3. Create your first team/project if WorkOS asks you to do so.
4. Confirm you can reach the WorkOS Dashboard.

WorkOS AuthKit will provide the sign-in screen that protects your custom GitHub connector.

## Step 5 — Keep these accounts open

For the rest of the guide, it is easiest to keep separate browser tabs open for:

```text
Claude
GitHub
AWS
WorkOS
```

You are ready for Chapter 2 when all four accounts work.

Continue to [Chapter 2 — Create the GitHub Test Repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }}).
