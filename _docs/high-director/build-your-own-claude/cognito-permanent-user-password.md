---
title: Build Your Own Sly Director — Confirm the Cognito User
summary: Set the Sly Director Cognito user's password permanently so Claude can sign in normally.
section: high-director
doc_type: runbook
status: active
created: 2026-09-12
updated: 2026-09-12
last_verified: 2026-09-12
order: 85
permalink: /docs/high-director/build-your-own-claude/cognito-permanent-user-password/
---

# Confirm the Cognito User

## Goal

Make the Sly Director Cognito user ready for normal sign-in before connecting Claude.

An administrator-created Cognito user can start with a temporary password. For this personal Sly Director setup, set a permanent password before attempting the Claude OAuth login.

## Complete this step

This guide creates one Cognito user for Sly Director. Open AWS CloudShell and run:

```bash
POOL_ID=$(aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query 'Environment.Variables.COGNITO_USER_POOL_ID' \
  --output text)

USERNAME=$(aws cognito-idp list-users \
  --user-pool-id "$POOL_ID" \
  --region us-east-2 \
  --query 'Users[0].Username' \
  --output text)

echo "Found Cognito user: $USERNAME"
```

The final line should show a real Cognito username.

Set and confirm the permanent password without displaying it:

```bash
read -s -p "New permanent Cognito password: " COGNITO_PASSWORD
echo
read -s -p "Type it again: " COGNITO_PASSWORD_CONFIRM
echo

if [ "$COGNITO_PASSWORD" != "$COGNITO_PASSWORD_CONFIRM" ]; then
  echo "Passwords do not match. Run this password block again."
  unset COGNITO_PASSWORD COGNITO_PASSWORD_CONFIRM
else
  aws cognito-idp admin-set-user-password \
    --user-pool-id "$POOL_ID" \
    --username "$USERNAME" \
    --password "$COGNITO_PASSWORD" \
    --permanent \
    --region us-east-2
  unset COGNITO_PASSWORD COGNITO_PASSWORD_CONFIRM
fi
```

Verify the account state:

```bash
aws cognito-idp admin-get-user \
  --user-pool-id "$POOL_ID" \
  --username "$USERNAME" \
  --region us-east-2 \
  --query '{Status:UserStatus,Email:UserAttributes[?Name==`email`]|[0].Value,EmailVerified:UserAttributes[?Name==`email_verified`]|[0].Value}' \
  --output json
```

The important result is:

```text
Status: CONFIRMED
```

If this user pool was created with `UsernameAttributes: ["email"]`, the email address is the sign-in identifier. Email verification is not required merely to use an email username, although marking the email verified is useful for account-recovery and verification workflows.

## Continue the Claude connection

1. Close any old Cognito login or **Change password** page.
2. Return to Claude.
3. Open the **Sly Director GitHub** connector.
4. Select **Connect** again.
5. Enter the Cognito email address.
6. Enter the permanent Cognito password you just confirmed twice.

<details>
<summary>If you saw `Invalid challenge transition`</summary>

An administrator-created user with a temporary password can be left in the `FORCE_CHANGE_PASSWORD` / `NEW_PASSWORD_REQUIRED` flow. Setting the password with `--permanent` changes the user to `CONFIRMED` and bypasses that first-login challenge.

</details>

<details>
<summary>If Cognito still says `Incorrect username or password`</summary>

Confirm the user pool uses email as its username attribute and that the displayed user email is the address you are entering. Then reset the permanent password again with the two-entry password block above and restart the Claude connector login from a new Cognito login page.

</details>

<details>
<summary>If this Cognito pool contains more than one user</summary>

Do not use the first-user shortcut. Open **Amazon Cognito → User pools → your Sly Director pool → User management → Users**, select the intended user, and copy that user's Cognito username before running the administrator commands.

</details>
