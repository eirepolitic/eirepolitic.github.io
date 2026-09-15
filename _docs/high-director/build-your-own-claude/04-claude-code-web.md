---
title: Build Your Own Sly Director — 04 — Prepare AWS
summary: Create the dedicated AWS administrator identity Sly Director will use and confirm the working region.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Prepare AWS

## Goal

Create a dedicated AWS administrator user for Sly Director and choose the AWS region used by this guide.

The AWS root user owns the account. Sly Director should use a separate administrator identity so its activity is easy to identify and its access can be disabled independently if needed.

## Step 1 — Select the AWS region

1. Sign in to the AWS Management Console as the account owner/root user.
2. In the top-right region menu, select:

```text
US East (Ohio) — us-east-2
```

The GitHub connector Lambda will run in this region.

## Step 2 — Create the Sly Director IAM user

1. In the AWS search bar, enter **IAM**.
2. Open **IAM**.
3. Select **Users**.
4. Select **Create user**.
5. For **User name**, enter:

```text
sly-director-admin
```

6. Select **Provide user access to the AWS Management Console**.
7. Select **I want to create an IAM user**.
8. Create or generate a password and store it privately.
9. Select **Next**.
10. Choose **Attach policies directly**.
11. Search for and select both:

```text
AdministratorAccess
AWSMCPSignInOAuthAccessPolicy
```

12. Select **Next**.
13. Review the settings.
14. Select **Create user**.
15. Save the IAM sign-in URL, username, and password somewhere private.

`AdministratorAccess` gives Sly Director broad AWS administration capability. `AWSMCPSignInOAuthAccessPolicy` allows the browser sign-in flow used by AWS MCP.

## Step 3 — Sign in as Sly Director

1. Sign out of the root AWS session.
2. Open the IAM sign-in URL you saved.
3. Sign in as:

```text
sly-director-admin
```

4. Confirm the AWS Console opens.
5. Confirm the region is still:

```text
US East (Ohio) — us-east-2
```

Use this IAM user for the remaining AWS steps in the guide.

Continue to [Chapter 5 — Build the Sly Director GitHub Connector]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).
