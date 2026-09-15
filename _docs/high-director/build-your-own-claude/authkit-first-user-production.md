---
title: Sly Director — AuthKit Production First User
summary: Enable Email + Password and sign-up in WorkOS AuthKit Production before connecting Claude.
section: high-director
doc_type: runbook
status: active
created: 2026-09-14
updated: 2026-09-14
last_verified: 2026-09-14
order: 88
permalink: /docs/high-director/build-your-own-claude/authkit-first-user-production/
---

# AuthKit Production — First User

## Goal

Make the WorkOS AuthKit Production hosted login usable by the person connecting Sly Director GitHub from Claude.

The WorkOS Dashboard account used to administer WorkOS is separate from the AuthKit application user that signs in through the MCP OAuth flow.

## Configure AuthKit Production authentication

1. In WorkOS, confirm the selected environment is:

```text
Production
```

2. Press **Ctrl+K** (or **Command+K** on macOS).
3. Search for:

```text
Authentication
```

4. Open the environment's **Authentication** page.
5. Confirm **Email + Password** is enabled.
6. Confirm **Sign up** is enabled.
7. Save any changes.

Email + Password is the normal authentication method for this personal Sly Director setup. AuthKit's hosted UI changes the sign-in and sign-up options it displays based on the authentication methods enabled for the environment.

## Retry Claude

1. Close the failed AuthKit sign-in tab.
2. Return to Claude.
3. Open the **Sly Director GitHub** connector.
4. Select **Connect** again.
5. Use the AuthKit sign-up flow to create the first Production application user if one does not already exist.
6. Complete any email verification AuthKit requests.
7. Return to Claude after authorization completes.

## If the hosted login only shows `Continue with SSO`

Return to the WorkOS Production **Authentication** page and verify **Email + Password** is enabled.

A WorkOS dashboard login, including a Google login used to administer the WorkOS team, does not by itself create or authorize an AuthKit end user for the Sly Director MCP application.

<details>
<summary>If Sign up is disabled intentionally</summary>

AuthKit can operate as an invite-only application. In that case, create an invitation from the WorkOS **Users → Invites** area instead of enabling public sign-up.

For the one-person Sly Director setup, enabling normal sign-up during initial setup is simpler.

</details>
