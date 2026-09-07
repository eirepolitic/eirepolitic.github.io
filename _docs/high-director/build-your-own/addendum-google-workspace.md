---
title: "Build Your Own High Director — Addendum A: Google Workspace"
summary: Optionally add Gmail and Google Calendar access to the completed High Director-style GPT using a separate Google OAuth Action.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 73
permalink: /docs/high-director/build-your-own/addendum-google-workspace/
---

# Addendum A — Google Workspace

## When to use this addendum

Complete the core GitHub/AWS build first. Add Google Workspace only after Chapters 1–12 are working.

This integration is optional. It is separate from the AWS Lambda GitHub wrapper and does not improve or repair GitHub access.

When configured, the Action can read Gmail, send email, list calendars, read calendar events, and create/update/delete/move calendar events for the Google account that completes the OAuth connection.

## Verified High Director Google Action

The currently documented High Director Google Workspace Action uses:

```text
OpenAPI: 3.1.0
API title: Google Workspace API
API version: 1.2.0
Authentication: OAuth
Calendar API server: https://www.googleapis.com
Gmail API server: https://gmail.googleapis.com
```

OAuth endpoints:

```text
Authorization URL: https://accounts.google.com/o/oauth2/v2/auth
Token URL: https://oauth2.googleapis.com/token
Token exchange: POST/default
```

Scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

Canonical reference: [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }}).

## What you need

You need:

- the custom GPT from the core guide;
- a Google account you control;
- access to Google Cloud Console;
- permission to create a Google Cloud project and OAuth client;
- the ability to connect that Google account to your GPT when ChatGPT presents the OAuth authorization screen.

You do not need to install Google SDKs or local software.

## Step 1 — Decide which Google account will be connected

Ask:

### Is this your own personal Google account?

- **Yes:** use that account for this addendum.
- **No:** stop unless the account owner or administrator has authorized you to connect it to a custom GPT.

The Action operates with the permissions granted by the connected Google account. Do not use another person's mailbox or calendar merely because you can sign in to it.

## Step 2 — Open Google Cloud Console

1. Open the Google Cloud Console in your browser.
2. Sign in with the Google account that will own the OAuth project.
3. Use the project selector near the top of the page.
4. Select **New Project**.
5. Enter a project name such as:

```text
High Director Google Action
```

6. If Google asks for an organization or location and you are using a personal account, use the options available for that account rather than inventing an organization.
7. Select **Create**.
8. Wait until the new project is selected in the console.

## Step 3 — Enable the Google Calendar API

1. Confirm the new project is selected.
2. Use the Google Cloud search box.
3. Search for **Google Calendar API**.
4. Open the API page.
5. Select **Enable**.
6. Wait until the API page shows that the API is enabled.

## Step 4 — Enable the Gmail API

1. Use the Google Cloud search box again.
2. Search for **Gmail API**.
3. Open the API page.
4. Select **Enable**.
5. Wait until the API page shows that the API is enabled.

Do not enable unrelated Google APIs for this addendum.

## Step 5 — Open Google Auth Platform

Google's current Cloud Console groups OAuth setup under **Google Auth Platform**.

1. Use the console search box.
2. Search for **Google Auth Platform**.
3. Open it.
4. If Google shows a **Get started** button, select it.

The exact navigation labels can change. Current Google documentation commonly separates OAuth configuration into areas such as **Branding**, **Audience**, **Data Access**, and **Clients**.

## Step 6 — Configure basic app information

If Google asks for branding/application details:

1. Enter an app name such as:

```text
High Director Google Action
```

2. Choose your own Google account as the user-support email when appropriate.
3. Enter the required developer contact email.
4. Complete only the required fields for your personal test configuration.
5. Do not invent a company, domain, privacy policy, or organization that you do not actually have.

## Step 7 — Choose the audience

For a normal personal Google account, the OAuth app will generally use an external audience because **Internal** is intended for eligible Google Workspace organizations.

1. Open **Audience**.
2. If your account offers **External**, choose it for a personal-account setup.
3. Keep the app in the narrowest testing configuration Google permits while you are setting it up for yourself.
4. If Google provides a **Test users** section, add the Google account you intend to connect.

Do not publish the OAuth app broadly just to make your own test account work.

Google can change verification requirements based on app audience, scopes, account type, and how broadly the app is distributed. Follow any current Google verification or consent requirements shown for your configuration rather than trying to bypass them.

## Step 8 — Configure OAuth scopes

Open **Data Access** or the current scope-management area.

Add these four scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

Do not add broader Gmail or Calendar scopes merely because they are available.

These scopes allow the same functional boundary documented for High Director:

- read the calendar list;
- manage calendar events;
- read Gmail;
- send Gmail.

## Step 9 — Start creating the OAuth client

Open **Clients** in Google Auth Platform.

1. Select **Create Client** or the current equivalent.
2. Choose **Web application** as the application type.
3. Enter a name such as:

```text
High Director GPT
```

Do not finish the redirect URI field yet. ChatGPT supplies the callback URL you must register.

## Step 10 — Get the callback URL from ChatGPT

Open the custom GPT editor in another browser tab.

1. Open your GPT.
2. Select **Edit GPT**.
3. Scroll to **Actions**.
4. Create a new Action for Google Workspace.
5. Open the Action's **Authentication** settings.
6. Select **OAuth**.
7. Locate the callback or redirect URL displayed by ChatGPT.
8. Copy that exact URL.

Do not substitute a callback URL from a tutorial or from another GPT. Use the callback URL shown for your own Action configuration.

## Step 11 — Add the callback URL to Google

Return to the Google OAuth client screen.

1. Find **Authorized redirect URIs**.
2. Select **Add URI**.
3. Paste the exact callback URL copied from ChatGPT.
4. Do not add unrelated localhost URLs or example URLs.
5. Select **Create** or **Save**.

Google should provide a **Client ID** and **Client secret**.

These are credentials. Store them privately. Do not publish them or paste them into ordinary troubleshooting chats.

## Step 12 — Configure OAuth in the GPT Action

Return to the GPT Action authentication screen.

Set:

```text
Authentication type: OAuth
Client ID: your Google OAuth Client ID
Client Secret: your Google OAuth Client Secret
Authorization URL: https://accounts.google.com/o/oauth2/v2/auth
Token URL: https://oauth2.googleapis.com/token
Token exchange method: default POST
```

Add the four scopes exactly:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

Save the authentication configuration.

## Step 13 — Add the Google Workspace OpenAPI schema

Use the canonical [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }}) as the authoritative description of the 12 operations and their request fields.

The Action should expose these operation IDs:

```text
listGoogleCalendars
listCalendarEvents
createCalendarEvent
getCalendarEvent
updateCalendarEvent
deleteCalendarEvent
moveCalendarEvent
getGmailProfile
searchGmailMessages
getGmailMessage
getGmailAttachment
sendGmailMessage
```

If you are reconstructing the schema from the canonical page, preserve the documented public Google API servers and request/response structures. Do not insert your OAuth client secret into the schema.

## Step 14 — Connect the Google account

Use the GPT Preview pane and request a harmless read such as:

```text
List the calendars available to my connected Google account. Do not create, edit, move, or delete anything.
```

ChatGPT should prompt you to sign in/authorize the Google connection if it has not been connected yet.

1. Read the Google consent screen.
2. Confirm the Google account is the intended one.
3. Review the requested permissions.
4. Continue only if they match the four intended scopes and you want this GPT to have those permissions.

## Step 15 — Test Gmail read access

Ask:

```text
Get my Gmail profile only. Do not read any message bodies and do not send email.
```

Then test search using a harmless query that does not require exposing private content in documentation.

Do not copy private email bodies into troubleshooting chats merely to prove that Gmail access works.

## Step 16 — Test Calendar read access

Ask:

```text
List my calendars. Do not create or change events.
```

Then, if desired:

```text
List events from my primary calendar for a small date range. Do not change anything.
```

## Step 17 — Test writes only with deliberate test data

Calendar write operations in the documented Action are designed to require explicit confirmation before create/update/delete/move actions.

For a test:

1. create a harmless calendar event clearly named as a test;
2. confirm the calendar, title, date/time, guests, and notification behavior before creation;
3. retrieve the event afterward;
4. delete it only after explicitly confirming the deletion.

For Gmail sending:

1. use an address you are authorized to send a test message to;
2. have the GPT show **To, Cc, Bcc, Subject, and body**;
3. confirm immediately before sending;
4. verify the message in Gmail afterward.

Do not use a real operational email or important calendar event for the first write test.

## What you should see

The GPT should have a second, separate Action with:

```text
Authentication: OAuth
Google Calendar operations: 7
Gmail operations: 5
Total operations: 12
Connected account: the Google account you intentionally authorized
```

GitHub access should continue to use the separate Lambda/API-key Action from the core guide.

## If you do not see this

Use these distinctions:

- **Google says redirect URI mismatch:** compare the exact ChatGPT callback URL with the Google OAuth client's authorized redirect URI.
- **Consent screen blocks you:** check app audience/test-user status and current Google verification requirements.
- **Calendar works but Gmail fails:** confirm the Gmail API is enabled and Gmail scopes are configured.
- **Gmail read works but send fails:** confirm `gmail.send` is present and inspect the returned Google API error.
- **OAuth login succeeds but the GPT Action fails schema validation:** troubleshoot the Action schema, not the Google client secret.
- **GitHub stops working:** do not assume the Google Action caused it; the two integrations use separate authentication paths.

Do not broaden OAuth scopes as a generic troubleshooting step.

## Ask ordinary ChatGPT this

```text
I am adding an optional Google Workspace OAuth Action to a custom GPT.

The Action should use:
Authorization URL: https://accounts.google.com/o/oauth2/v2/auth
Token URL: https://oauth2.googleapis.com/token
Scopes:
- calendar.events
- calendar.calendarlist.readonly
- gmail.readonly
- gmail.send

Google Cloud project APIs enabled: [Calendar yes/no, Gmail yes/no]
OAuth client type: Web application
Failing stage: [Google Auth Platform / redirect URI / consent / GPT OAuth setup / Calendar API / Gmail API]
Exact sanitized error: [paste it]

Do not ask for my OAuth Client Secret, access token, refresh token, Gmail content, or private calendar data. Check current Google and OpenAI documentation and give me browser-only, click-by-click troubleshooting steps. Do not broaden scopes unless the specific API operation requires it.
```

## Maintenance note

Google OAuth consent, app-verification requirements, test-user rules, and ChatGPT Action screens can change. Re-check current Google and OpenAI instructions if the screens differ materially from this addendum.
