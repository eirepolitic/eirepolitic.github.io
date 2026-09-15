---
title: Sly Director — Direct Cognito OAuth Known Issue
summary: Historical record of the Claude.ai web authorization failure that led Sly Director to replace direct Cognito OAuth with WorkOS AuthKit Production.
section: high-director
doc_type: reference
status: active
created: 2026-09-12
updated: 2026-09-14
last_verified: 2026-09-14
order: 86
permalink: /docs/high-director/build-your-own-claude/cognito-claude-web-known-issue/
---

# Direct Cognito OAuth — Claude.ai Web Known Issue

## Current status

This page is historical. The active Sly Director build no longer uses Amazon Cognito as Claude's direct MCP authorization server.

The current architecture uses:

```text
Claude.ai / Cowork
      ↓
WorkOS AuthKit Production OAuth
      ↓
Sly Director GitHub MCP
```

Continue with [Chapter 5 — Build the Sly Director GitHub MCP Service]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).

## Why Cognito was replaced

The direct Cognito build reached this state during live verification:

```text
Cognito login succeeds
MCP protected-resource metadata returns HTTP 200 JSON
Lambda receives no bearer-token request after login
Claude shows: Authorization with the MCP server failed
```

That means authentication reached Cognito successfully but Claude.ai web failed during the post-login OAuth exchange before the MCP resource server received an access token.

Changing the Cognito password, callback URL, GitHub PAT, Lambda Function URL, or `PUBLIC_MCP_URL` did not address that failure boundary.

## Historical architecture

```text
Claude.ai / Cowork
      ↓
Amazon Cognito directly as MCP authorization server
      ↓
Sly Director GitHub MCP
```

This direct path is not used by the current build guide.

## Replacement

WorkOS AuthKit Production is now the selected MCP authorization server because it directly supports the MCP OAuth requirements used by remote clients, including authorization-server metadata, PKCE S256, Client ID Metadata Document, Dynamic Client Registration compatibility, Resource Indicators, refresh-token grants, and JWKS token verification.

The AWS Lambda Function URL, GitHub PAT, GitHub tools, and repository workflow remain otherwise unchanged.
