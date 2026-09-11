---
title: Build Your Own High Director — Claude Edition 08 — Daily Operation
summary: Use the High Director Claude Project, Claude Code web, GitHub, and AWS MCP together safely after initial testing.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 88
permalink: /docs/high-director/build-your-own-claude/08-daily-operation/
---

# Chapter 8 — Daily Operation

## Goal

Use the right Claude surface for each task without mixing planning, repository execution, and AWS changes unnecessarily.

## Use the High Director Project for planning

Use the Project when you need to:

- define requirements;
- compare architectures;
- decide cost/security tradeoffs;
- plan AWS resources;
- troubleshoot errors;
- write documentation or implementation plans;
- use the AWS MCP connector.

Example:

```text
I want to build a scheduled data import that stores results in S3. Ask me only the decisions that materially affect cost, permissions, or architecture. Then produce the implementation plan.
```

## Use Claude Code web for repository implementation

Use Claude Code when work requires the repository itself:

- inspect files;
- modify Python/YAML/docs;
- run tests or linters;
- create a branch;
- prepare a pull request;
- fix an issue in an existing codebase.

Example:

```text
Inspect this repository and identify the smallest change needed to add the scheduled import described below. Implement it, add or update tests where appropriate, run the relevant verification, and prepare the result for pull-request review.
```

## Recommended normal workflow

For an important change:

1. Plan it in the High Director Project.
2. Decide architecture, cost, permissions, and acceptance criteria.
3. Open the relevant repository in Claude Code web.
4. Give Claude Code the approved implementation requirements.
5. Let it inspect the repository before editing.
6. Review its changes and verification results.
7. Review the GitHub pull request.
8. Merge only when satisfied.
9. Return to the High Director Project for AWS deployment/operations if necessary.
10. Verify the live result.

## New repositories

Claude Code works with repositories that already exist in GitHub.

For a new tool:

1. Create the repository on GitHub.
2. Add a README so the repository has an initial branch.
3. Ensure the Claude Code GitHub integration has access to the repository.
4. Open it in Claude Code web.
5. Ask Claude Code to scaffold the project based on the plan.

## AWS operations

When using AWS MCP, ask Claude to explain before executing any operation with meaningful cost, access, deletion, public exposure, or architecture consequences.

Useful wording:

```text
Before making this AWS change, tell me exactly which resource will change, which region it is in, what permission is required, the likely cost category, and how to undo the change. Then wait for my decision.
```

For routine read-only queries, that extra checkpoint is usually unnecessary.

## S3

For S3 work, specify the bucket and intended action clearly.

Prefer a narrow request such as:

```text
Using AWS, list objects under the reports/ prefix in bucket example-bucket. Do not modify anything.
```

rather than:

```text
Check my S3 and fix it.
```

## Lambda, Step Functions, and CloudWatch

Use AWS MCP to inspect existing resources first.

A useful diagnostic sequence is:

```text
resource → configuration → recent execution → logs/metrics → diagnosis → proposed change
```

Do not respond to a failed Lambda or workflow by changing IAM, timeouts, memory, networking, and code simultaneously.

## Usage limits

Claude Pro and Claude Code share plan usage. If you reach the included usage limit, that is not a GitHub or AWS failure.

Anthropic may offer additional usage credits or higher-tier plans. Do not upgrade automatically; first determine whether the limitation is occasional or persistent enough to justify additional cost.

## Keep GitHub and AWS permissions separate

The Claude Code GitHub integration and AWS MCP authorization are independent.

A GitHub failure is not fixed by changing AWS IAM.

An AWS `AccessDenied` is not fixed by changing GitHub authorization.

## What you should see

Normal work should follow one of these paths:

```text
Plan → Claude Code → GitHub PR → review → merge
```

or:

```text
Plan → AWS MCP → AWS change/query → verification
```

## If you do not see this

If Claude is trying to perform repository work in a normal Project chat without repository tooling, move that implementation task to Claude Code web.

If Claude Code needs an AWS decision, make the decision in the High Director Project and then give the result back to Claude Code.

## Ask ordinary Claude or ChatGPT this

```text
I have a High Director-style Claude setup with:
- Claude Project for planning and AWS MCP
- Claude Code on the web for GitHub repository work

Task I want to perform: [describe it]

Tell me which surface I should use first and the safest sequence. Do not ask for credentials or secrets.
```

## Next chapter

Continue to [Chapter 9 — Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }}).
