---
title: Build Your Own Sly Director — Confirm the Cognito User
summary: Set the Sly Director Cognito user's password permanently and verify its email so Claude can sign in normally.
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

An administrator-created Cognito user can start with a temporary password and an unverified email. For this personal Sly Director setup, set a permanent password and mark the configured email as verified before attempting the Claude OAuth login.

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

The final line should show a real Cognito username, for example:

```text
Found Cognito user: 411bc5c0-10a1-700f-b8c3-0e40cb28c6be
```

Set the permanent password:

```bash
read -s -p "New permanent Cognito password: " COGNITO_PASSWORD
echo

aws cognito-idp admin-set-user-password \
  --user-pool-id "$POOL_ID" \
  --username "$USERNAME" \
  --password "$COGNITO_PASSWORD" \
  --permanent \
  --region us-east-2

unset COGNITO_PASSWORD
```

The password prompt does not display the password while you type it.

Mark the user's existing email as verified:

```bash
aws cognito-idp admin-update-user-attributes \
  --user-pool-id "$POOL_ID" \
  --username "$USERNAME" \
  --user-attributes Name=email_verified,Value=true \
  --region us-east-2
```

Verify both the account and email state:

```bash
aws cognito-idp admin-get-user \
  --user-pool-id "$POOL_ID" \
  --username "$USERNAME" \
  --region us-east-2 \
  --query '{Status:UserStatus,Email:UserAttributes[?Name==`email`]|[0].Value,EmailVerified:UserAttributes[?Name==`email_verified`]|[0].Value}' \
  --output json
```

The result should show:

```json
{
  "Status": "CONFIRMED",
  "Email": "your-email@example.com",
  "EmailVerified": "true"
}
```

## Continue the Claude connection

1. Close any old Cognito login or **Change password** page.
2. Return to Claude.
3. Open the **Sly Director GitHub** connector.
4. Select **Connect** again.
5. Enter the Cognito email address shown in the verification output.
6. Enter the permanent Cognito password.
7. Cognito should proceed through the OAuth login without the first-login password-change challenge.

<details>
<summary>If you saw `Invalid challenge transition`</summary>

An administrator-created user with a temporary password can be left in the `FORCE_CHANGE_PASSWORD` / `NEW_PASSWORD_REQUIRED` flow. Setting the password with `--permanent` changes the user to `CONFIRMED` and bypasses that first-login challenge.

</details>

<details>
<summary>If Cognito says `Incorrect username or password`</summary>

First confirm the verification output shows both:

```text
Status: CONFIRMED
EmailVerified: true
```

If both are correct, set the permanent password again with the secure password prompt above, then restart the Claude connector login from a new Cognito login page.

</details>

<details>
<summary>If this Cognito pool contains more than one user</summary>

Do not use the first-user shortcut. Open **Amazon Cognito → User pools → your Sly Director pool → User management → Users**, select the intended user, and copy that user's Cognito username before running the administrator commands.

</details>
