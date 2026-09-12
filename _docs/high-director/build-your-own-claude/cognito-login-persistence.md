---
title: Build Your Own Sly Director — Keep Cognito Signed In
summary: Configure a long Cognito refresh-token lifetime so Claude can renew access automatically without routine repeat logins.
section: high-director
doc_type: runbook
status: active
created: 2026-09-11
updated: 2026-09-11
last_verified: 2026-09-11
order: 85
permalink: /docs/high-director/build-your-own-claude/cognito-login-persistence/
---

# Keep Cognito Signed In

## Goal

Make the Cognito login used by **Sly Director GitHub** effectively a one-time setup step rather than something you expect to repeat every few weeks.

Claude automatically refreshes OAuth access tokens. Cognito access tokens are short-lived, but the Cognito refresh token lets Claude obtain new access tokens without opening the login page again.

Amazon Cognito's default refresh-token lifetime is 30 days. For this personal Sly Director setup, use the maximum practical lifetime:

```text
Refresh token expiration: 3650 days
```

That is approximately 10 years, which is the maximum Cognito supports.

## Complete this step

1. Open the AWS console.
2. Open **Amazon Cognito**.
3. Open **User pools**.
4. Select the user pool created for Sly Director.
5. Open:

```text
Applications → App clients
```

6. Select:

```text
SlyDirectorClaude
```

7. On the app-client page, find **App client information**.
8. Select **Edit**.
9. Find the token-expiration settings.
10. Set **Refresh token expiration** to:

```text
3650 days
```

11. Leave the normal access-token lifetime at its default unless you have a specific reason to change it.
12. Save the changes.

## What this means

The normal flow becomes:

```text
Initial setup
→ you sign in to Cognito once
→ Claude receives an access token + refresh token
→ access token expires
→ Claude refreshes it automatically
→ no login page appears
```

Claude refreshes stored OAuth tokens automatically, including proactive refresh shortly before expiry and reactive refresh when a server returns an authentication failure.

## When you may still have to sign in again

A new Cognito login can still be required if:

```text
the refresh token finally expires
you disconnect/reconnect the Claude connector
you revoke the Cognito session or authorization
the Cognito user is disabled or deleted
the app client is replaced or its credentials change
the connector's stored authentication is cleared
```

Routine one-hour access-token expiry should not require a manual login.

<details>
<summary>Why not make the access token itself last 10 years?</summary>

Short-lived access tokens are intentional. If an access token is exposed, its useful lifetime is limited.

The long-lived refresh token is the credential Claude stores for obtaining replacement access tokens. This gives the low-friction experience without making each bearer access token long-lived.

</details>
