---
title: Build Your Own Sly Director — 04 — Prepare AWS
summary: Prepare the AWS account before building the Sly Director GitHub MCP service and connecting AWS MCP.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Prepare AWS

## Goal

Prepare the AWS account that will host the small GitHub MCP service and that Sly Director will later operate through AWS MCP.

## Complete this step

1. Open the [AWS Management Console](https://console.aws.amazon.com/).
2. Sign in to the AWS account you want Sly Director to use.
3. For the simplest version of this guide, sign in as the **root user**.
4. In the region selector in the upper-right corner, choose:

```text
US East (Ohio) — us-east-2
```

5. In the AWS search box, enter:

```text
Billing and Cost Management
```

6. Open **Billing and Cost Management**.
7. In the left navigation, select **Budgets**.
8. Select **Create budget**.
9. Choose a simple monthly-cost or zero-spend template.
10. Name the budget:

```text
sly-director-budget
```

11. Enter an email address you monitor for alerts.
12. Create the budget.
13. Return to the AWS console home page.
14. In the top navigation, select the **CloudShell** icon.
15. Confirm a CloudShell terminal opens successfully.
16. Leave the AWS console open.

## What you should see

```text
AWS account: signed in
Region: us-east-2
Budget: sly-director-budget
CloudShell: opens successfully
```

Continue to [Chapter 5 — Build the Sly Director GitHub MCP service]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).

<details>
<summary>Additional information</summary>

The guide uses AWS Lambda because it has no always-running server. The GitHub MCP service runs only when Claude/Cowork calls it.

CloudShell is an AWS-hosted terminal inside your browser. The guide uses it only to build the Lambda deployment zip from the published source files. You do not need to install Python or AWS tools on your own computer.

A budget sends alerts; it does not automatically stop AWS spending.

</details>

<details>
<summary>Optional: use a dedicated IAM identity instead of root</summary>

The main guide uses root because it is the shortest setup path for a personal installation.

If you prefer a separate IAM or IAM Identity Center administrator identity, use one that can create and configure Lambda, Cognito, IAM execution roles, Function URLs, CloudWatch Logs, and budgets. The rest of the guide is unchanged.

</details>
