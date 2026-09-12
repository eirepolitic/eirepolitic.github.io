---
title: Build Your Own Sly Director — Confirm the Cognito User
summary: Set the Sly Director Cognito user's password permanently so Claude does not enter the first-login password-change challenge.
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

An administrator-created Cognito user with a temporary password has status:

```text
FORCE_CHANGE_PASSWORD
```

That sends the first login through the `NEW_PASSWORD_REQUIRED` challenge. For this personal Sly Director setup, use a permanent password instead so the user is already:

```text
CONFIRMED
```

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

Then set the permanent password:

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

Verify the Cognito user status:

```bash
aws cognito-idp admin-get-user \
  --user-pool-id "$POOL_ID" \
  --username "$USERNAME" \
  --region us-east-2 \
  --query UserStatus \
  --output text
```

The final line should show:

```text
CONFIRMED
```

## Continue the Claude connection

1. Close any old Cognito **Change password** page.
2. Return to Claude.
3. Open the **Sly Director GitHub** connector.
4. Select **Connect** again.
5. Enter the Cognito email address.
6. Enter the new permanent Cognito password.
7. Cognito should proceed directly through the OAuth login instead of opening the first-login **Change password** challenge.

## If you saw `Invalid challenge transition`

That error can occur while the user is still going through Cognito's temporary-password `NEW_PASSWORD_REQUIRED` challenge.

After the user status is `CONFIRMED`, restart the connector login from Claude rather than continuing the old password-change browser page.

<details>
<summary>If this Cognito pool contains more than one user</summary>

Do not use the first-user shortcut. Open **Amazon Cognito → User pools → your Sly Director pool → User management → Users**, select the intended user, and copy that user's Cognito username before running `admin-set-user-password`.

</details>

<details>
<summary>Why this works</summary>

Amazon Cognito's `AdminSetUserPassword` operation can set either a temporary or permanent password. A temporary password leaves an administrator-created user in `FORCE_CHANGE_PASSWORD`. A permanent password changes the user to `CONFIRMED` and permits immediate normal sign-in.

</details>
