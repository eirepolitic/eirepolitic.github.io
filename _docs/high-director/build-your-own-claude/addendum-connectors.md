---
title: "Build Your Own High Director — Claude Edition — Addendum A: Connectors"
summary: Add optional Claude connectors such as Google Workspace after the core GitHub and AWS setup is working.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 91
permalink: /docs/high-director/build-your-own-claude/addendum-connectors/
---

# Addendum A — Google Workspace and Other Claude Connectors

## When to use this addendum

Complete the core guide first.

Claude's connector system can add cloud services without building a custom Action or Lambda gateway. Use an existing connector when it provides the capabilities you need.

## Google Workspace

Claude currently offers Google Workspace-related integrations/features depending on plan, account, and current product availability.

For personal use:

1. Open Claude.
2. Open **Customize → Connectors** or the current connector directory.
3. Look for the Google service you want to connect.
4. Select **Connect**.
5. Sign in to the intended Google account.
6. Read the OAuth consent screen.
7. Authorize only if the requested permissions match what you want Claude to do.

Do not create a Google Cloud OAuth application yourself when an official Claude connector already satisfies the requirement.

## Start with read-only tasks

After connecting a service, first ask Claude to perform a harmless read operation.

For example:

```text
Use the connected Google service to identify what calendars are available. Do not create, modify, move, or delete anything.
```

or:

```text
Use the connected service only to confirm that mailbox access is working. Do not send or delete anything.
```

## Write operations

For email, calendars, documents, or other services, inspect the intended change before executing it.

Useful wording:

```text
Show me exactly what you intend to send/create/change, including recipients, title, time, and notification behavior. Do not execute it until I approve the final details.
```

## Other connectors

Use the same preference order:

```text
1. official/built-in connector
2. established remote MCP connector
3. custom MCP server only when required
```

This keeps setup and maintenance simpler.

## What you should see

The connected service should appear in Claude's connector list and be individually enableable for conversations.

## If you do not see this

Check current Claude connector availability for your plan and region/account before building a custom integration.

## Ask ordinary Claude or ChatGPT this

```text
I want to connect [service] to Claude Pro using the simplest supported browser-only method.

I prefer an official Claude connector or existing remote MCP integration rather than building my own server.
Current screen/error: [describe]

Do not ask for passwords, OAuth tokens, API keys, or private content. Check the current Claude connector documentation and give me click-by-click setup steps.
```
