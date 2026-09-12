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

Open AWS CloudShell and run:

```bash
POOL_ID=$(aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query 'Environment.Variables.COGNITO_USER_POOL_ID' \
  --output text)

read -p "Cognito login email: " EMAIL

USERNAME=$(aws cognito-idp list-users \
  --user-pool-id "$POOL_ID" \
  --filter "email = \"$EMAIL\"" \
  --region us-east-2 \
  --query 'Users[0].Username' \
  --output text)

echo "Found Cognito user: $USERNAME"

read -s -p "New permanent Cognito password: " COGNITO_PASSWORD
echo

aws cognito-idp admin-set-user-password \
  --user-pool-id "$POOL_ID" \
  --username "$USERNAME" \
  --password "$COGNITO_PASSWORD" \
  --permanent \
  --region us-east-2

unset COGNITO_PASSWORD

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

The password prompt does not display the password while you type it.

## Continue the Claude connection

1. Return to Claude.
2. Open the **Sly Director GitHub** connector.
3. Select **Connect** again.
4. Enter the Cognito email address.
5. Enter the new permanent Cognito password.
6. Cognito should proceed directly through the OAuth login instead of opening the first-login **Change password** challenge.

## If you saw `Invalid challenge transition`

That error can occur while the user is still going through Cognito's temporary-password `NEW_PASSWORD_REQUIRED` challenge.

After the user status is `CONFIRMED`, restart the connector login from Claude rather than continuing the old password-change browser page.

<details>
<summary>Why this works</summary>

Amazon Cognito's `AdminSetUserPassword` operation can set either a temporary or permanent password. A temporary password leaves an administrator-created user in `FORCE_CHANGE_PASSWORD`. A permanent password changes the user to `CONFIRMED` and permits immediate normal sign-in.

</details>
