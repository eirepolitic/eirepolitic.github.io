---
title: Build Your Own High Director 04 — AWS Account and Safety
summary: Prepare the AWS account, select the deployment region, create a cost budget, and verify browser-based CloudShell before deploying the Lambda wrapper.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 64
permalink: /docs/high-director/build-your-own/04-aws-account-and-safety/
---

# Chapter 4 — Create and Prepare AWS

## Goal

At the end of this chapter you will have:

- access to the correct AWS account;
- the AWS region set to `us-east-2` for this build;
- a basic cost-monitoring budget or alert configured;
- AWS CloudShell working in your browser.

You will not deploy the Lambda until Chapter 5.

## Important billing note

AWS is a metered cloud platform. Some services have free usage allowances, but a budget is a notification tool, not a guarantee that AWS will stop all spending automatically.

Do not enter false identity information, bypass an account requirement, or continue with an account you are not authorized to use. If AWS requires an account owner, payment method, verification step, or other eligibility requirement, follow the current AWS instructions for your account and country.

## Step 1 — Sign in and confirm the account

1. Open the [AWS Management Console](https://console.aws.amazon.com/).
2. Sign in to the AWS account you intend to use.
3. Look at the account menu in the upper-right area.
4. Confirm you recognize the account name or account identifier.
5. If you are in an employer, school, family, or other person's AWS account, stop unless you have explicit permission to create resources and incur possible charges.

## Step 2 — Select the deployment region

The verified High Director deployment uses AWS region:

```text
us-east-2
```

Its AWS display name is normally **US East (Ohio)**.

1. In the AWS console's top navigation bar, find the current region selector.
2. Open it.
3. Select **US East (Ohio)**.
4. Confirm the region selector now shows **Ohio** or the equivalent current AWS wording.

Using the same region as the verified implementation reduces unnecessary setup differences.

## Step 3 — Create a cost budget

AWS currently provides budget templates and custom budgets in Billing and Cost Management. A simple budget is useful because this guide is aimed at people who may be new to metered cloud services.

1. Use the AWS search box at the top of the console.
2. Search for **Billing and Cost Management**.
3. Open **Billing and Cost Management**.
4. In the left navigation, select **Budgets**.
5. Select **Create budget**.
6. If AWS offers **Use a template (simplified)**, select it.
7. Choose either a **Zero spend budget** or a **Monthly cost budget**, depending on the options AWS currently shows and your own spending tolerance.
8. Enter a clear name such as:

```text
high-director-learning-budget
```

9. Enter an email address that you regularly read for budget notifications.
10. If you choose a monthly cost budget, enter a budget amount that reflects the maximum spending level at which you want to be warned. This is your financial decision; the guide does not choose a spending limit for you.
11. Review the screen carefully.
12. Select **Create budget**.

Official AWS reference: [Creating a budget](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-create.html).

### Important limitation

A normal AWS Budget sends alerts. It does not necessarily prevent spending immediately when the threshold is reached, and cost data or notifications can be delayed.

## Step 4 — Find AWS CloudShell

AWS CloudShell is a browser-based command environment supplied by AWS. It is pre-authenticated to the AWS account you are signed in to, so this guide can use AWS command-line tools without installing anything on your computer.

Official AWS reference: [Getting started with AWS CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/getting-started.html).

1. Return to the main AWS Management Console.
2. Confirm the selected region is still **US East (Ohio)**.
3. Look for the **CloudShell** icon in the top navigation bar or console footer.
4. Select **CloudShell**.
5. If AWS asks you to initialize or open the environment, follow the on-screen prompt.
6. Wait for a command prompt to appear.

The prompt may look different from examples in screenshots. That is fine.

## Step 5 — Verify CloudShell without changing anything

Click inside the CloudShell terminal.

Type or paste this command exactly, then press **Enter**:

```bash
aws sts get-caller-identity
```

AWS should return a small JSON result containing fields such as `UserId`, `Account`, and `Arn`.

This command does not create a resource. It simply confirms which AWS identity CloudShell is using.

Do not publish the returned AWS account number. It is not a password, but it is unnecessary to expose it in screenshots or troubleshooting messages.

## Step 6 — Verify the selected region in CloudShell

Paste:

```bash
aws configure get region
```

If the result is:

```text
us-east-2
```

you are aligned with the guide.

If it is blank or another region, use the AWS console region selector to choose **US East (Ohio)** and reopen CloudShell. Do not start creating resources in multiple regions just to test.

## Step 7 — Create a working folder in CloudShell

Paste these commands one at a time:

```bash
mkdir -p ~/high-director-build
```

Then:

```bash
cd ~/high-director-build
```

Then:

```bash
pwd
```

You should see a path ending in:

```text
/high-director-build
```

This folder exists inside your AWS CloudShell environment, not on your local computer.

## Step 8 — Record the non-secret AWS setup values

Add these items to your private setup note:

```text
AWS region: us-east-2
AWS budget created: yes
CloudShell identity check successful: yes
CloudShell working folder: ~/high-director-build
```

Do not record AWS passwords, secret keys, session credentials, or other secrets.

## What you should see

You should now have:

- the AWS console set to US East (Ohio);
- a budget visible under Billing and Cost Management → Budgets;
- an AWS CloudShell prompt;
- a successful result from `aws sts get-caller-identity`;
- the `~/high-director-build` CloudShell folder.

No Lambda function is required yet.

## If you do not see this

Check the smallest failing piece only:

1. If **Budgets** is unavailable, confirm you are authorized to view billing information in this AWS account.
2. If **CloudShell** is unavailable, confirm the selected region supports CloudShell and that your AWS identity has permission to use it.
3. If `aws sts get-caller-identity` returns an authorization error, copy only the error text and do not expose AWS credentials.
4. If you are unsure which AWS account you are in, stop before creating resources and verify the account owner.

Do not create access keys to fix a CloudShell problem. CloudShell is already authenticated through your AWS console session.

## Ask ordinary ChatGPT this

```text
I am using the AWS Management Console in a browser to prepare a Lambda deployment. I am not installing anything locally.

AWS region I intend to use: us-east-2 (US East Ohio)
Step that failed: [budget / CloudShell / sts identity check / region check]
What I clicked or ran: [describe it]
Exact non-secret error text: [paste it]

Do not ask me for AWS passwords, access keys, secret keys, session tokens, account payment information, or other credentials. Give me current AWS-console click-by-click troubleshooting steps and explain any command you ask me to run before I run it.
```

## Next chapter

Continue to [Chapter 5 — Deploy the GitHub wrapper Lambda]({{ '/docs/high-director/build-your-own/05-deploy-lambda/' | relative_url }}).
