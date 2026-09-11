---
title: Build Your Own High Director — Claude Edition 05 — AWS Account and Safety
summary: Prepare the AWS account, billing alerts, and IAM identity or role used by Claude through the managed AWS MCP Server.
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

Prepare AWS and choose the AWS identity Claude will use through the managed AWS MCP Server.

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

The AWS MCP Server can interact with AWS services across regions when your permissions allow it. Using one preferred region keeps the first setup simpler.

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

8. Use an email address you monitor.
9. Review the settings.
10. Create the budget.

A budget is an alerting tool; AWS resource charges still depend on the services you create and use.

## Step 4 — Understand the AWS MCP permission model

AWS MCP uses the permissions of the AWS identity that authorizes the OAuth connection.

There are two separate permission layers:

```text
OAuth permission
→ allows the AWS identity to authorize AWS MCP

AWS service permissions
→ control what Claude can actually do in S3, Lambda, CloudWatch, Step Functions, and other services
```

AWS currently requires these OAuth actions:

```text
signin:AuthorizeOAuth2Access
signin:CreateOAuth2Token
```

AWS provides the managed policy:

```text
AWSMCPSignInOAuthAccessPolicy
```

Official references:

- [AWS MCP Server OAuth authentication](https://docs.aws.amazon.com/agent-toolkit/latest/userguide/oauth-authentication.html)
- [Create an IAM role for an IAM user](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html)
- [Switch to an IAM role in the AWS console](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-console.html)

## Step 5 — Choose the simpler identity path

Use one of these paths.

### Path A — Use your existing IAM identity

This is the easiest option.

Use it when the IAM user, IAM Identity Center identity, or federated role you already use for AWS has the permissions you want Claude to have.

Chapter 6 will show how to add `AWSMCPSignInOAuthAccessPolicy` if that identity needs the OAuth permission.

Continue to Step 7.

### Path B — Create a dedicated Claude role

Use this when you want Claude's AWS permissions separated from your normal AWS permissions.

The guide uses this role name:

```text
ClaudeHighDirectorRole
```

The role will initially receive:

```text
AWSMCPSignInOAuthAccessPolicy
AmazonS3ReadOnlyAccess
```

The first policy enables AWS MCP OAuth. The second gives enough S3 read access for the first resource test. You can add the operational service permissions Claude needs later.

## Step 6 — Create `ClaudeHighDirectorRole`

This path assumes you are signed in as an IAM user, IAM Identity Center identity, or federated identity that is allowed to create IAM roles.

AWS root sessions cannot use the console **Switch role** feature. If the top-right AWS account menu identifies your session as the root user, use an IAM or IAM Identity Center identity for the dedicated-role path.

### 6.1 — Find your AWS account ID

1. In the AWS console, select your account menu in the upper-right corner.
2. Find **Account ID**.
3. Record the 12-digit number in your private setup note.

Example:

```text
123456789012
```

### 6.2 — Open IAM

1. In the AWS console search box, enter `IAM`.
2. Open **IAM**.
3. In the left navigation, select **Roles**.
4. Select **Create role**.

### 6.3 — Choose who can assume the role

1. Under **Trusted entity type**, choose **AWS account**.
2. Choose **This account**.
3. Leave **Require external ID** off for this same-account browser role.
4. Leave **Require MFA** off unless you specifically want AWS to require an additional MFA step each time this role is assumed.
5. Select **Next**.

AWS will create a trust relationship that allows identities from your AWS account to assume the role when those identities also have `sts:AssumeRole` permission.

### 6.4 — Add the initial role permissions

On **Add permissions**:

1. Search for:

```text
AWSMCPSignInOAuthAccessPolicy
```

2. Select its checkbox.
3. Search for:

```text
AmazonS3ReadOnlyAccess
```

4. Select its checkbox.
5. Select **Next**.

### 6.5 — Name and create the role

1. For **Role name**, enter:

```text
ClaudeHighDirectorRole
```

2. For **Description**, enter:

```text
AWS permissions used by the High Director Claude AWS MCP connection.
```

3. Review the trusted entity and attached policies.
4. Select **Create role**.

### What you should see

The IAM **Roles** page should contain:

```text
ClaudeHighDirectorRole
```

Open the role and check **Permissions**. You should see:

```text
AWSMCPSignInOAuthAccessPolicy
AmazonS3ReadOnlyAccess
```

## Step 6A — Give your normal IAM user permission to assume the role

Creating the role is only half of the setup. Your signed-in IAM user also needs permission to switch into it.

If you use IAM Identity Center or another federated identity, the equivalent `sts:AssumeRole` permission may be managed through that identity system. For a normal IAM user, use the steps below.

### 6A.1 — Open your IAM user

1. In IAM, select **Users**.
2. Select the IAM username you normally use to sign in.
3. Open the **Permissions** tab.
4. Select **Add permissions**.
5. Choose **Create inline policy**.
6. Select the **JSON** editor.

### 6A.2 — Add the assume-role policy

Paste this policy, replacing `YOUR_ACCOUNT_ID` with your 12-digit AWS account ID:

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

Example with a fictional account ID:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      "Resource": "arn:aws:iam::123456789012:role/ClaudeHighDirectorRole"
    }
  ]
}
```

1. Select **Next**.
2. For policy name, enter:

```text
AllowAssumeClaudeHighDirectorRole
```

3. Select **Create policy**.

### What you should see

The IAM user's permissions should now include an inline policy named:

```text
AllowAssumeClaudeHighDirectorRole
```

## Step 6B — Test switching into the role

1. Select your AWS identity/account menu in the upper-right corner.
2. Select **Switch role**. If AWS multi-session is enabled, select **Add session → Switch role**.
3. For **Account**, enter your 12-digit AWS account ID.
4. For **Role**, enter:

```text
ClaudeHighDirectorRole
```

5. Optionally set the display name to:

```text
Claude High Director
```

6. Select **Switch Role**.

The upper-right AWS menu should now show the role name/display name.

When a role is active, its permissions replace your normal user's permissions for that role session; they are not added together.

## Step 6C — Add AWS service permissions later

The dedicated role starts with S3 read access so you can test the connection first.

When Claude needs to operate additional AWS services:

1. Open **IAM → Roles → ClaudeHighDirectorRole**.
2. Open **Permissions**.
3. Select **Add permissions → Attach policies**.
4. Search for the managed policy that matches the service Claude needs.
5. Select the policy.
6. Select **Add permissions**.

Common examples are:

```text
AmazonS3FullAccess
AWSLambda_FullAccess
CloudWatchFullAccessV2
AWSStepFunctionsFullAccess
```

Use the policies that match the services the project actually operates. More specific customer-managed policies can replace these later if you want tighter resource-level access.

Some AWS services also require `iam:PassRole` when Claude creates a resource that itself needs an execution role. Treat that as a separate permission and add it when the specific service requires it.

## Step 7 — Use browser OAuth

Browser OAuth is the step that connects Claude to the AWS identity you prepared above. You complete it entirely in the browser.

### 7.1 — Make sure the correct AWS identity is active

Keep the AWS Management Console open in one browser tab.

If you chose **Path A — existing IAM identity**:

1. Select the account/identity menu in the upper-right corner of AWS.
2. Confirm the displayed IAM user, IAM Identity Center session, or federated role is the identity you want Claude to use.

If you chose **Path B — `ClaudeHighDirectorRole`**:

1. Select the account/identity menu in the upper-right corner.
2. Confirm the active role/session shows:

```text
ClaudeHighDirectorRole
```

If it does not, use the **Switch role** steps in Step 6B first.

### 7.2 — Open normal Claude

1. Open a second browser tab.
2. Go to `https://claude.ai/`.
3. Sign in to your Claude Pro account.
4. Confirm you are in the normal Claude interface rather than Claude Code.

### 7.3 — Open Claude connectors

1. In Claude, open **Customize** or the current customization/settings area.
2. Select **Connectors**.
3. Select **+** or **Add connector**.
4. Choose **Add custom connector**.

### 7.4 — Enter the AWS MCP connector details

Use these values:

```text
Name: AWS MCP
Remote MCP server URL: https://aws-mcp.us-east-1.api.aws/mcp
Authentication type: OAuth
```

Then complete the current Claude connector screens in this order:

1. In **Name**, enter:

```text
AWS MCP
```

2. In **Remote MCP server URL** or the equivalent URL field, enter:

```text
https://aws-mcp.us-east-1.api.aws/mcp
```

3. Continue until Claude shows the **Authentication type** selector.
4. Select:

```text
OAuth
```

AWS MCP uses OAuth 2.1 through AWS Sign-in, so **OAuth** is the authentication type for this connector. Other authentication types in the selector apply to different MCP servers.

5. Continue to the OAuth configuration screen.
6. If Claude displays optional **OAuth Client ID** and **OAuth Client Secret** fields, leave those fields empty for AWS MCP. AWS MCP supports OAuth discovery and does not require you to create a separate OAuth client for this setup.
7. Review the connector summary.
8. Select **Add**, **Save**, or the current final button.

### What you should see

Claude's connector list should now contain:

```text
AWS MCP
```

The connector may show that authentication still needs to be completed. That is expected; the AWS sign-in flow is triggered when Claude first invokes an AWS MCP tool.

### 7.5 — Enable AWS MCP in the High Director Project

1. Return to the normal Claude sidebar.
2. Open **Projects**.
3. Open **High Director**.
4. Start a new chat.
5. Select the **+** button near the message field.
6. Open **Connectors**.
7. Enable **AWS MCP**.

### 7.6 — Trigger AWS OAuth

In the High Director chat, enter:

```text
Using the AWS connector, identify the AWS account and IAM identity or role available to you, and tell me the current identity name.
```

Send the message.

Claude should attempt to use the AWS MCP connector. Because the connector has not yet been authorized, AWS Sign-in should open automatically in a new tab, window, or redirect.

### 7.7 — Complete AWS Sign-in and consent

When AWS opens:

1. Confirm the AWS account is the account you prepared in this chapter.
2. Confirm the identity/session is the one you selected in Step 7.1.
3. Complete AWS sign-in if AWS asks you to authenticate again.
4. AWS should display an authorization/consent screen for the AWS MCP connection.
5. Review the account and identity shown on the page.
6. Select the AWS button that authorizes/allows the connection.
7. AWS should redirect you back to Claude, or show that authorization completed successfully.

### 7.8 — Verify Claude is connected

Return to the High Director chat if the browser does not return there automatically.

Claude should now complete the request and identify the AWS account/identity context available through the connector.

For the dedicated-role path, you should expect the AWS identity to be based on:

```text
ClaudeHighDirectorRole
```

### 7.9 — Run the first AWS query

Ask:

```text
Using AWS MCP, list the S3 buckets visible to this AWS identity and tell me which AWS identity or role you are using.
```

If the account has no S3 buckets, an empty result is still a successful connection test.

### 7.10 — If the AWS authorization page does not appear

First retry the connection using AWS's documented OAuth-initialization endpoint as the custom connector URL:

```text
https://aws-mcp.us-east-1.api.aws/mcp?oauth=initialize
```

When re-adding the connector, select **OAuth** again as the **Authentication type**.

Then repeat Steps 7.5 through 7.9.

If AWS instead shows a permission error mentioning:

```text
signin:AuthorizeOAuth2Access
signin:CreateOAuth2Token
```

check that the active IAM identity or `ClaudeHighDirectorRole` has:

```text
AWSMCPSignInOAuthAccessPolicy
```

## Step 8 — Record values

Add to your private setup note:

```text
AWS preferred region: us-east-2
AWS budget created: yes
AWS MCP authentication plan: OAuth through AWS Sign-in
AWS identity path: existing identity / ClaudeHighDirectorRole
AWS account ID:
AWS role name: ClaudeHighDirectorRole   [if used]
AWS MCP connector authentication type: OAuth
AWS MCP connector added in Claude: yes/no
AWS MCP OAuth completed: yes/no
```

## What you should see

You should now have:

- a working AWS console session;
- a budget/alert;
- either an existing IAM identity ready for MCP OAuth, or `ClaudeHighDirectorRole` ready to assume;
- `AWSMCPSignInOAuthAccessPolicy` available on the identity that authorizes the MCP connection;
- an **AWS MCP** connector in Claude configured with **Authentication type: OAuth**;
- completed AWS browser OAuth;
- a successful first AWS resource query from the High Director Project.

## If you do not see this

If **Create role**, **Add permissions**, or **Create inline policy** is unavailable, the current AWS identity lacks one or more IAM administration permissions. Use an AWS administrative identity you already control to complete the IAM setup.

If **Switch role** returns `AccessDenied`, check both halves of the role relationship:

```text
ClaudeHighDirectorRole trust policy
+ signed-in user has sts:AssumeRole on that role ARN
```

If OAuth fails, use the Step 7.10 checks before changing IAM service permissions.

## Ask ordinary Claude or ChatGPT this

```text
I am preparing AWS for Claude High Director using the managed AWS MCP Server and browser OAuth.

Identity path: [existing IAM identity / dedicated ClaudeHighDirectorRole]
AWS account ID: [12-digit ID]
Current IAM username or identity type: [name/type]
Claude connector authentication type selected: OAuth
I am stuck at: [create role / attach policy / add sts:AssumeRole / switch role / add AWS MCP connector / authentication type / AWS OAuth / first AWS query]
Exact non-secret error: [paste it]

Give me exact browser click-by-click steps and identify whether the issue is IAM role assumption, Claude connector configuration, AWS MCP OAuth, or AWS service permissions.
```

## Next chapter

Continue to [Chapter 6 — Connect Claude to the AWS MCP Server]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).
