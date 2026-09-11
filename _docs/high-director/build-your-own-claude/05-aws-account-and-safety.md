---
title: Build Your Own High Director — Claude Edition 05 — AWS Account and Safety
summary: Prepare the AWS account, billing alerts, and permissions before connecting Claude to the managed AWS MCP Server.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 85
permalink: /docs/high-director/build-your-own-claude/05-aws-account-and-safety/
---

# Chapter 5 — Create and Prepare AWS

## Goal

Prepare AWS safely before giving Claude any AWS tool access.

## Step 1 — Sign in to the intended account

1. Open the [AWS Management Console](https://console.aws.amazon.com/).
2. Sign in.
3. Confirm the account is one you control and are authorized to use.

## Step 2 — Choose the working region

For consistency with the existing High Director documentation, use:

```text
us-east-2
```

AWS normally labels this **US East (Ohio)**.

1. Use the region selector in the AWS console.
2. Choose **US East (Ohio)**.

The AWS MCP Server itself can interact with AWS services across regions when your permissions allow it, but using one preferred region keeps beginner testing simpler.

## Step 3 — Create a billing budget

1. Search the AWS console for **Billing and Cost Management**.
2. Open it.
3. Select **Budgets**.
4. Select **Create budget**.
5. Use a simplified template if AWS offers one.
6. Choose a zero-spend or monthly-cost alert appropriate for your own spending tolerance.
7. Name it:

```text
claude-high-director-budget
```

8. Use an email address you actually monitor.
9. Review the settings.
10. Create the budget.

A budget is an alerting tool and does not guarantee that AWS automatically stops all spending.

## Step 4 — Understand the AWS MCP permission model

AWS's managed MCP Server does not replace IAM.

When Claude asks AWS to perform an operation, AWS still evaluates the permissions of the AWS identity you authorized.

AWS recommends least-privilege IAM permissions.

The MCP Server also adds AWS MCP context keys to calls and AWS CloudTrail records API calls, which helps distinguish MCP-originated AWS activity.

Official reference: [How AWS MCP Server works with IAM](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/security_iam_service-with-iam.html).

## Step 5 — Use browser OAuth

The recommended web-client path uses OAuth through AWS Sign-in.

AWS explicitly documents OAuth as the simple option for human users and web clients.

## Step 6 — Decide which AWS identity will authorize Claude

Use the AWS identity you normally use in the console and whose permissions you understand.

If you currently sign in as the AWS root user, create/use an appropriate IAM administrative identity for normal daily work.

Chapter 6 will establish whether the current identity can authorize the managed MCP connection.

## Step 7 — Record values

Add to your private setup note:

```text
AWS preferred region: us-east-2
AWS budget created: yes
AWS MCP authentication plan: OAuth through AWS Sign-in
```

## What you should see

You should have a working AWS console session and a budget/alert.

## If you do not see this

Resolve billing/account access before connecting Claude.

## Ask ordinary Claude or ChatGPT this

```text
I am preparing AWS for the managed AWS MCP Server using browser OAuth.

I am stuck at: [AWS sign-in / region / budget / IAM identity]
What I clicked: [describe it]
Exact non-secret error: [paste it]

Give me browser-only AWS-console steps using the permissions required for the intended operation.
```

## Next chapter

Continue to [Chapter 6 — Connect Claude to the AWS MCP Server]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).
