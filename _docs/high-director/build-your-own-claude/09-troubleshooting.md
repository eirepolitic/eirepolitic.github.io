---
title: Build Your Own High Director — Claude Edition 09 — Troubleshooting
summary: Troubleshoot Claude Project, autonomous Claude Code/GitHub operation, AWS MCP OAuth, and downstream IAM failures one layer at a time.
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
5. repository branch/check/merge automation
6. Claude custom connector configuration
7. AWS MCP OAuth authorization
8. downstream AWS IAM/service permissions
9. the specific GitHub or AWS resource
```

## First rule — preserve the exact error

Copy the exact non-secret error before retrying or changing configuration.

Useful evidence includes:

- which Claude surface you were using;
- repository name;
- GitHub task/branch/PR/check state;
- AWS service and region;
- AWS API action if shown;
- HTTP/error code;
- approximate failure time.

## Problem: Claude Project behavior is wrong

Check the Project instructions from Chapter 3 and start a fresh Project chat.

## Problem: Claude Code cannot see the repository

Check:

1. the repository exists in GitHub;
2. you are signed in to the intended GitHub account;
3. the Claude GitHub App is installed/authorized;
4. the App has access to that repository;
5. refresh/reopen the Claude Code repository selector.

## Problem: Claude Code can read but cannot push/create repository changes

This points to GitHub App authorization, repository permissions, or repository rules rather than AWS.

1. Preserve Claude Code's exact error.
2. Check the GitHub App's repository access.
3. Check repository rules/branch protections.
4. Confirm the connected GitHub identity/App has the required write capability.

## Problem: Claude completes work but the PR waits for the user

That is not the intended operating model for this guide.

The target repository flow is:

```text
Claude change → checks/validation → automated completion/merge → final verification
```

Check:

1. whether the repository uses pull requests for Claude Code web tasks;
2. whether required checks are passing;
3. whether GitHub auto-merge or an equivalent narrow repository automation is configured;
4. whether branch/ruleset requirements make autonomous completion impossible;
5. whether the automation is limited to the intended Claude-created changes rather than every PR.

## Problem: Claude made an incorrect repository change

Because Claude is the repository operator, use repository history for recovery rather than relying on manual pre-approval.

1. Identify the bad commit/branch/merge.
2. Preserve the exact repository state.
3. Ask Claude to diagnose the error.
4. Revert or correct the change through the normal repository workflow.
5. Run relevant tests/checks again.
6. Verify the final state.

If the same category of error repeats, improve tests, validation, repository instructions, or automation instead of introducing routine manual approval for every change.

## Problem: custom connector cannot be added

Check Claude account access, **Customize → Connectors**, the AWS MCP URL, and accidental URL formatting errors.

## Problem: AWS OAuth does not start

Compare the connector endpoint with AWS's current AWS MCP Server documentation and retry a harmless request.

## Problem: AWS OAuth returns an authorization error

AWS currently documents these OAuth-sign-in permissions:

```text
signin:AuthorizeOAuth2Access
signin:CreateOAuth2Token
```

Only add the AWS-documented OAuth access permission when the exact error shows it is missing and you are authorized to change that IAM identity.

## Problem: OAuth succeeds but an AWS operation returns AccessDenied

The connector is working. The downstream AWS service is denying the requested API action.

Identify the exact service, API action, resource, IAM principal, and region. Add only the intended permission where appropriate.

## Problem: AWS query returns no resources

An empty result may be correct. Check account, region, resource type, and whether the resource actually exists.

## Problem: Claude says usage limit reached

Claude Pro and Claude Code share plan usage. This is not a GitHub or AWS authentication failure.

## Problem: GitHub works but AWS fails

Treat them independently. Claude Code/GitHub authorization does not authenticate AWS MCP.

## Problem: AWS works but repository work fails

Treat the problem as Claude Code/GitHub/repository automation unless the repository task itself calls AWS.

## Standard troubleshooting prompt

```text
I am troubleshooting a browser-only High Director-style Claude setup.

Architecture:
- Claude Pro
- High Director Claude Project for planning
- Claude Code on the web as the primary repository modifier/operator
- Claude GitHub App for repository access
- routine repository work should complete without user PR/merge approval
- remote custom connector to the AWS managed MCP Server
- AWS browser OAuth

Surface that failed: [Claude Project / Claude Code / GitHub authorization / repository automation / connector / AWS OAuth / AWS API]
Last checkpoint that passed: [describe it]
Exact sanitized error: [paste it]
Expected result: [describe it]
Observed result: [describe it]

Identify the failing layer first, then give the smallest browser-only verification step. Preserve autonomous repository operation rather than adding routine human approval.
```

## What you should see

A useful diagnosis should identify the exact failing layer, for example:

```text
Claude successfully pushes the change and CI passes, but the PR remains open. Therefore Claude/GitHub write access works; the remaining issue is repository merge automation rather than user approval.
```

## Next chapter

Continue to [Chapter 10 — Maintenance and access review]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }}).
