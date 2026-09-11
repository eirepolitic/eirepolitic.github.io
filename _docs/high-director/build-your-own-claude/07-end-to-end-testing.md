---
title: Build Your Own High Director — Claude Edition 07 — End-to-End Testing
summary: Verify the High Director Claude Project, Claude Code GitHub workflow, and AWS MCP connection before using important repositories or AWS resources.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 87
permalink: /docs/high-director/build-your-own-claude/07-end-to-end-testing/
---

# Chapter 7 — End-to-End Testing

## Goal

Prove each part independently before using the setup for important work.

## Test 1 — High Director project behavior

Inside the **High Director** project, ask:

```text
I want to build a data-import tool in GitHub and eventually deploy it on AWS. I have not decided how it should run or what it may cost. Plan the decisions we need before implementation.
```

Expected behavior:

- Claude identifies decisions affecting architecture/cost;
- explanations are beginner-friendly;
- Claude does not pretend a repository or AWS resource already exists.

## Test 2 — Claude Code repository read

Open Claude Code web and select `claude-director-test`.

Ask:

```text
Inspect the repository and summarize its files. Do not make changes.
```

Expected result: Claude sees the files already committed to GitHub.

## Test 3 — Claude Code branch and PR

Ask Claude Code:

```text
Create a file named end-to-end-test.md containing a short explanation that this is the Claude edition end-to-end test. Verify the change, then prepare it on a branch for pull-request review.
```

Review the resulting change and PR in GitHub. Merge it only after confirming the change is correct.

## Test 4 — AWS MCP read-only connection

In the High Director project with **AWS MCP** enabled, ask:

```text
Using the AWS connector, list the S3 buckets visible to the authorized AWS identity. Do not create, modify, or delete anything.
```

A valid empty list is a successful result if the account has no buckets.

## Test 5 — First controlled AWS write

Only perform this test after you understand that AWS resources can incur charges.

Choose a low-impact resource you actually need rather than creating infrastructure solely for a test. If you have no current AWS write task, skip this test until you do.

When you are ready, ask Claude first for a plan containing:

```text
resource to be created or changed
AWS region
expected cost category
IAM permission required
how to verify success
how to undo the change
```

Review that plan before telling Claude to execute the AWS operation.

## Test 6 — Cross-surface workflow

Use the intended operating model:

1. In the High Director Project, plan a tiny repository change.
2. Open Claude Code web for `claude-director-test`.
3. Have Claude Code implement it.
4. Review/merge the PR in GitHub.
5. Return to the High Director Project for AWS/deployment planning if needed.

This is the Claude equivalent of the original High Director's combined planning + GitHub + AWS workflow, but it uses two Claude surfaces optimized for different jobs.

## Minimum readiness checklist

Before using an important repository or AWS workload, confirm:

```text
High Director project instructions behave correctly: yes
Claude Code can read test repository: yes
Claude Code can create reviewed PR: yes
AWS MCP connector authenticates: yes
Read-only AWS query works: yes
AWS account is correct: yes
AWS budget alert exists: yes
```

## What you should see

The system should now have two independently proven paths:

```text
Claude Project → AWS MCP → AWS
Claude Code web → GitHub
```

## If you do not see this

Do not rebuild both integrations when only one failed.

- Project behavior problem → fix project instructions.
- Repository problem → focus on Claude Code/GitHub authorization.
- AWS connector problem → focus on MCP/OAuth.
- AWS `AccessDenied` after OAuth works → focus on the exact downstream IAM permission.

## Ask ordinary Claude or ChatGPT this

```text
I am testing a Claude Pro High Director-style setup.

Paths:
1. Claude Project → AWS managed MCP Server → AWS
2. Claude Code on the web → GitHub

Test that passed most recently: [describe]
Test that failed: [describe]
Exact sanitized error: [paste]

Do not ask for credentials or tokens. Identify which path/layer is failing before suggesting changes.
```

## Next chapter

Continue to [Chapter 8 — Daily operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}).
