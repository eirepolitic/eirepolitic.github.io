---
title: Sly Director — Direct Cognito OAuth Known Issue
summary: Current Claude.ai web connector authorization can fail after successful Cognito login before the MCP server receives a bearer token.
section: high-director
doc_type: reference
status: active
created: 2026-09-12
updated: 2026-09-12
last_verified: 2026-09-12
order: 86
permalink: /docs/high-director/build-your-own-claude/cognito-claude-web-known-issue/
---

# Direct Cognito OAuth — Claude.ai Web Known Issue

## Current status

Do not continue troubleshooting passwords, callback URLs, GitHub permissions, or the MCP Lambda if all of the following are true:

```text
Cognito login succeeds
MCP protected-resource metadata returns HTTP 200 JSON
Lambda receives no bearer-token request after login
Claude shows: Authorization with the MCP server failed
```

This failure pattern has been reproduced with Claude.ai web against an OAuth 2.1 + Amazon Cognito MCP stack. In the reported case, the same MCP/Cognito stack worked through Claude Code while Claude.ai web failed during the post-login token exchange.

## What this means for Sly Director

The direct architecture:

```text
Claude.ai / Cowork
      ↓
Amazon Cognito directly as MCP authorization server
      ↓
Sly Director GitHub MCP
```

is not considered a reliable supported path for this guide as of 2026-09-12.

The MCP Lambda and Cognito user can both be healthy while Claude.ai web still fails before presenting a bearer token to the MCP resource server.

## Do not keep changing the working pieces

Once the pattern above is confirmed, stop changing:

```text
Cognito password
Cognito callback URL
GitHub PAT
Lambda Function URL
PUBLIC_MCP_URL
MCP protected-resource metadata
```

Those changes do not address a failure occurring in Claude's post-login OAuth broker.

## Replacement design decision

The replacement authorization layer must be explicitly compatible with remote MCP OAuth used by Claude.ai and Cowork.

The simplest current option under review is a dedicated MCP-compatible authorization provider such as WorkOS AuthKit. A second option is an AWS-hosted OAuth compatibility broker, but that adds substantially more code and maintenance.

Do not continue Chapter 5 past the connector authorization step until the replacement authorization design is selected and documented.
