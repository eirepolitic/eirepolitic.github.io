---
title: Build Your Own High Director — Claude Edition 05 — Prepare AWS
summary: Prepare the AWS account for the browser-only Claude AWS MCP connection.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 85
permalink: /docs/high-director/build-your-own-claude/05-aws-account-and-safety/
---

# Chapter 5 — Prepare AWS

## Goal

Prepare your AWS account before connecting Claude.

## Complete this step

1. Open the [AWS Management Console](https://console.aws.amazon.com/).
2. Sign in with the AWS account you want Claude to operate.
3. For this guide's simplest path, sign in as the **root user**.
4. In the region selector, choose:

```text
US East (Ohio) — us-east-2
```

5. Search for **Billing and Cost Management**.
6. Open **Budgets**.
7. Select **Create budget**.
8. Choose a simple monthly-cost or zero-spend template.
9. Name it:

```text
claude-high-director-budget
```

10. Enter an email address you monitor.
11. Create the budget.
12. Leave the AWS console open in this root-user session.

## What you should see

You should now have:

```text
AWS account: signed in as root
Preferred workload region: us-east-2
Budget alert: created
```

Continue to [Chapter 6 — Connect Claude to AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).

<details>
<summary>Additional information</summary>

The root-user path is intentionally the simplest path in this guide. AWS MCP can use AWS Sign-in OAuth with the active AWS identity.

The High Director Project instructions already state that root-authenticated AWS MCP access is an intentional choice for this environment, so Claude should not repeatedly add generic root-account warnings unless root use is directly relevant to a problem.

`us-east-2` is the preferred region for workloads in this guide. The managed AWS MCP endpoint itself currently uses a separate AWS endpoint region in Chapter 6.

A budget sends alerts; it does not automatically stop AWS spending.

</details>

<details>
<summary>Optional: use a dedicated IAM role instead of root</summary>

Use this only if you want Claude's permissions separated from root.

### Create the role

1. Sign in with an IAM identity that can manage IAM.
2. Open **IAM → Roles → Create role**.
3. Select **AWS account**.
4. Select **This account**.
5. Continue to permissions.
6. Attach:

```text
AWSMCPSignInOAuthAccessPolicy
AmazonS3ReadOnlyAccess
```

7. Name the role:

```text
ClaudeHighDirectorRole
```

8. Select **Create role**.

### Allow your IAM user to assume it

1. Open **IAM → Users**.
2. Select your IAM user.
3. Open **Permissions → Add permissions → Create inline policy**.
4. Select **JSON**.
5. Paste this, replacing `YOUR_ACCOUNT_ID`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::YOUR_ACCOUNT_ID:role/ClaudeHighDirectorRole"
    }
  ]
}
```

6. Name the policy:

```text
AllowAssumeClaudeHighDirectorRole
```

7. Create the policy.

### Switch into the role

1. Open the AWS identity menu in the upper-right corner.
2. Select **Switch role** or **Add session → Switch role**.
3. Enter your AWS account ID.
4. Enter:

```text
ClaudeHighDirectorRole
```

5. Select **Switch Role**.
6. Keep that role session active when you complete Chapter 6.

### Add more AWS permissions later

Open **IAM → Roles → ClaudeHighDirectorRole → Permissions → Add permissions** and attach only the service permissions needed by the project.

Some AWS deployments also require `iam:PassRole` when Claude assigns an execution role to services such as Lambda or Step Functions.

</details>

<details>
<summary>Troubleshooting</summary>

If AWS sign-in or billing setup fails, preserve the exact AWS error before changing account configuration.

If the optional IAM role cannot be assumed, verify both:

```text
role trust permits the AWS account
IAM user has sts:AssumeRole for ClaudeHighDirectorRole
```

Useful prompt:

```text
I am preparing AWS for a Claude AWS MCP connection.
AWS identity: [root / ClaudeHighDirectorRole / other]
I am stuck at: [sign-in / budget / role creation / switch role]
Exact non-secret error: [paste it]
Give me exact AWS-console click-by-click steps.
```

</details>
