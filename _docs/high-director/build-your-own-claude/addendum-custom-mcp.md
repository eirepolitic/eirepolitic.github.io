---
title: "Build Your Own High Director — Claude Edition — Addendum B: Custom MCP"
summary: Decide when to build a custom remote MCP server and how to keep it separate from the simpler Claude Code and managed AWS MCP paths.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 92
permalink: /docs/high-director/build-your-own-claude/addendum-custom-mcp/
---

# Addendum B — Advanced Custom MCP Servers

## When a custom MCP server is justified

Use a custom MCP server when Claude needs a capability that is not already provided by:

```text
Claude Code on the web
an official Claude connector
an existing remote MCP server
AWS managed MCP Server
```

Examples could include a private application API, a specialized internal database gateway, or a tightly controlled business workflow that has no existing connector.

## Why this is not the primary path

A custom remote MCP server adds:

- server hosting;
- authentication/OAuth design;
- public network reachability;
- tool schemas;
- authorization logic;
- monitoring;
- maintenance;
- new failure modes.

Anthropic documents remote custom connectors as cloud-to-cloud connections: Claude's infrastructure must be able to reach the remote MCP server over the internet.

Official reference: [Custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

## Design questions before implementation

Decide:

1. What exact operations does Claude need?
2. Which operations are read-only?
3. Which operations modify or delete data?
4. What identity should authorize each user?
5. What resources must be outside Claude's reach?
6. What information may safely pass through Claude?
7. What will host the MCP server?
8. What will it cost when idle and under normal use?
9. How will requests be logged/audited?
10. How will credentials be rotated or revoked?

Write code and IAM policies after these boundaries are known.

## Relationship to the original High Director Lambda wrapper

The original ChatGPT High Director uses a custom Lambda wrapper because custom GPT Actions need an HTTP/OpenAPI bridge for the GitHub capabilities used by that design.

Claude Code already provides the normal GitHub development path more simply, so the Claude edition uses that path instead of porting the old wrapper by default.

If a future requirement genuinely needs the old wrapper's API surface inside regular Claude chats, a separate project could adapt those backend operations into an MCP server. That would be a new implementation and should be tested independently rather than modifying the proven Claude Code path.

## Simplest hosting approach

When a custom server is necessary, prefer a managed/serverless hosting option that:

- supports HTTPS;
- is publicly reachable from Anthropic's cloud;
- can implement MCP correctly;
- supports the required authentication method;
- has clear logs and cost controls.

## Keep permissions narrow

Expose tools that correspond to the intended user actions.

## Test pattern

Use this order:

```text
health/connectivity
→ authentication
→ harmless read
→ intended read operations
→ one disposable write
→ verification
→ destructive actions only if genuinely required
```

Keep the core Claude Code/GitHub and managed AWS MCP integrations unchanged while testing the new connector.

## What you should see

A custom MCP server should appear as a separate Claude connector and remain independent from GitHub and the managed AWS MCP configuration.

## Ask ordinary Claude or ChatGPT this

```text
I have a working Claude Pro setup using Claude Code web for GitHub and the AWS managed MCP Server for AWS.

I am considering a custom remote MCP server for this missing capability: [describe capability].

Before giving implementation steps, tell me whether an existing Claude connector, Claude Code, or managed MCP service already covers it. If not, help me define the smallest tool surface, authentication model, hosting choice, permissions, cost, and test plan.
```
