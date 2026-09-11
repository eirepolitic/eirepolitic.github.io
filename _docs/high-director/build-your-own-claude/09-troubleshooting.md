---
title: Build Your Own High Director — Claude Edition 09 — Troubleshooting
summary: Troubleshoot Claude Project, Claude Code, GitHub, AWS MCP OAuth, and downstream IAM failures one layer at a time.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 89
permalink: /docs/high-director/build-your-own-claude/09-troubleshooting/
---

# Chapter 9 — Troubleshooting

## Goal

Identify the failing layer before changing anything.

The Claude edition has these main layers:

```text
1. Claude account / plan
2. High Director Project instructions
3. Claude Code on the web
4. Claude Code ↔ GitHub authorization
5. Claude custom connector configuration
6. AWS MCP OAuth authorization
7. downstream AWS IAM/service permissions
8. the specific GitHub or AWS resource
```

## First rule — preserve the exact error

Copy the exact non-secret error before retrying or changing configuration.

Useful evidence includes:

- which Claude surface you were using;
- repository name;
- GitHub task/PR state;
- AWS service and region;
- AWS API action if shown;
- HTTP/error code;
- approximate failure time.

Never share passwords, access keys, OAuth tokens, payment details, private secret values, or recovery codes.

## Problem: Claude Project behavior is wrong

Symptoms:

- explanations are not beginner-friendly;
- Claude skips planning decisions;
- it assumes tools/accounts exist;
- it proposes broad permissions without evidence.

Check:

1. Open the **High Director** Project.
2. Open **Project instructions**.
3. Confirm the instructions from Chapter 3 are present and saved.
4. Start a fresh chat inside the Project and retest.

Do not change GitHub or AWS permissions to fix instruction behavior.

## Problem: Claude Code cannot see the repository

Check:

1. the repository exists in GitHub;
2. you are signed in to the intended GitHub account;
3. the Claude Code GitHub integration is installed/authorized;
4. the integration has access to that repository;
5. refresh/reopen the Claude Code repository selector.

Do not create a PAT as the first workaround.

## Problem: Claude Code can read but cannot push or create a PR

This points to the GitHub integration/authorization or repository permissions rather than AWS.

1. Preserve Claude Code's exact error.
2. Check the GitHub integration's repository access.
3. Check whether repository rules/branch protections restrict the attempted operation.
4. Verify your own GitHub account has permission to create branches/PRs.

Do not disable branch protection merely to make a test pass.

## Problem: Claude Code changed the wrong files

Do not merge the pull request.

1. Review the diff.
2. Close or abandon the unwanted PR/task if appropriate.
3. Start a new task with narrower requirements.
4. Explicitly name the allowed files or acceptance criteria when useful.

Because web tasks run in isolated environments, a bad proposed change does not need to be merged.

## Problem: custom connector cannot be added

Check:

1. your Claude account is signed in correctly;
2. **Customize → Connectors** is available;
3. the AWS MCP URL matches current AWS documentation;
4. there are no accidental spaces or extra text in the URL.

Do not deploy your own MCP server just because the managed connector was typed incorrectly.

## Problem: AWS OAuth does not start

This usually points to the connector URL or MCP OAuth discovery.

1. Compare the endpoint with AWS's current AWS MCP Server setup page.
2. Remove and re-add the connector only after confirming the URL.
3. Retry a harmless AWS knowledge/read request.

If AWS documentation currently requires `?oauth=initialize` for a legacy/non-discovering client, use it only when the client behavior actually requires that compatibility path.

## Problem: AWS OAuth returns an authorization error

AWS currently documents these OAuth-sign-in permissions:

```text
signin:AuthorizeOAuth2Access
signin:CreateOAuth2Token
```

Check whether the AWS identity used for sign-in has those permissions.

AWS currently provides the managed policy:

```text
AWSMCPSignInOAuthAccessPolicy
```

Only add it when the exact error/evidence shows the OAuth permissions are missing and you are authorized to change that IAM identity.

Do not use `AdministratorAccess` as an OAuth fix.

## Problem: OAuth succeeds but an AWS operation returns AccessDenied

The connector is working. The downstream AWS service is denying the requested API action.

Use the exact error to identify:

```text
AWS service
API action
resource ARN if shown
IAM principal
region
```

Then decide whether that operation is genuinely part of the intended capability.

Add only the required permission when appropriate.

Do not make the identity broadly administrative simply to eliminate one `AccessDenied`.

## Problem: AWS query returns no resources

An empty result is not necessarily an error.

Check:

1. correct AWS account;
2. correct resource region when the service is regional;
3. correct service/resource type;
4. whether the account genuinely contains that resource.

## Problem: Claude says usage limit reached

Claude Pro and Claude Code share plan usage.

This is not a GitHub/AWS authentication failure.

Options can include waiting for the usage window to reset, purchasing optional usage credits if offered, or considering a higher plan if the limit is consistently restrictive.

Do not buy additional capacity until you know the limitation is actually usage-related.

## Problem: GitHub works but AWS fails

Treat them independently.

Claude Code/GitHub authorization does not authenticate AWS MCP.

Do not modify GitHub access to troubleshoot AWS.

## Problem: AWS works but repository work fails

Treat the problem as Claude Code/GitHub unless the repository task itself calls AWS.

Do not change IAM to fix a GitHub-only task.

## Standard troubleshooting prompt

```text
I am troubleshooting a browser-only High Director-style Claude setup.

Architecture:
- Claude Pro
- High Director Claude Project for planning
- Claude Code on the web for GitHub
- remote custom connector to the AWS managed MCP Server
- AWS browser OAuth, no local proxy and no AWS access keys

Surface that failed: [Claude Project / Claude Code / GitHub / connector / AWS OAuth / AWS API]
Last checkpoint that passed: [describe it]
Exact sanitized error: [paste it]
Expected result: [describe it]
Observed result: [describe it]

Do not ask for credentials, tokens, payment information, private secret values, or recovery codes. Identify the failing layer first, then give the smallest browser-only verification step. Do not suggest broad IAM or repository-permission changes unless the evidence specifically requires them.
```

## What you should see

A useful diagnosis should be specific, for example:

```text
Claude can connect to AWS and list S3 buckets, but creating a Lambda function returns AccessDenied for lambda:CreateFunction. Therefore MCP/OAuth works; the missing capability is a downstream IAM permission for the requested AWS action.
```

## Next chapter

Continue to [Chapter 10 — Maintenance and access review]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }}).
