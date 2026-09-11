---
title: Build Your Own High Director — Claude Edition 08 — Daily Operation
summary: Use the High Director Claude Project, autonomous Claude Code repository operation, GitHub, and AWS MCP together after initial testing.
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

Use the right Claude surface for each task while allowing Claude to operate repositories without routine user approval.

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

## Use Claude Code web for repository implementation and operation

Use Claude Code when work requires the repository itself:

- inspect files;
- modify Python/YAML/docs;
- run tests or linters;
- create branches;
- create pull requests when useful;
- complete merges or repository workflows where supported;
- fix issues in an existing codebase.

Example:

```text
Inspect this repository and implement the scheduled import described below. Use the repository workflow that provides useful traceability with the least unnecessary overhead. Run the relevant tests/checks and complete the repository-side work without waiting for me to approve a pull request or merge.
```

## Repository operating model

Claude is expected to be the primary repository modifier and operator.

Normal repository work should **not** stop for user review or approval.

Branches and pull requests are still useful when they provide:

- history;
- CI/check execution;
- isolation;
- rollback points;
- compatibility with repository rules.

They are not intended to make the user a mandatory reviewer.

If a branch/PR workflow is used, the desired cycle is:

```text
plan → implement → test → branch/PR if useful → automated checks → automated completion/merge → verify final state
```

If the repository safely supports a simpler direct-write workflow, Claude may use that instead.

## Recommended normal workflow

For an important repository change:

1. Plan it in the High Director Project when architecture/cost/design decisions are involved.
2. Open the relevant repository in Claude Code web.
3. Give Claude Code the requirements and acceptance criteria.
4. Let it inspect the repository before editing.
5. Let it implement and run the relevant verification.
6. Let the repository workflow complete automatically where the available tooling supports it.
7. Have Claude verify the final repository state.
8. Return to the High Director Project for AWS deployment/operations if necessary.
9. Verify the live result.

Do not insert a manual user-review step merely because a pull request exists.

## New repositories

Claude Code works with repositories that already exist in GitHub.

For a new tool:

1. Create the repository on GitHub.
2. Add a README so the repository has an initial branch.
3. Ensure the Claude Code GitHub App has access to the repository.
4. Open it in Claude Code web.
5. Ask Claude Code to scaffold and operate the project based on the agreed plan.

## AWS operations

The removal of repository approval gates does **not** remove planning decisions for AWS changes that materially affect cost, access, deletion, public exposure, or architecture.

Useful wording:

```text
Before making this AWS change, tell me exactly which resource will change, which region it is in, what permission is required, the likely cost category, and how to undo the change. Then proceed once the required design/cost decisions are settled.
```

## S3

For S3 work, specify the bucket and intended action clearly.

Prefer:

```text
Using AWS, list objects under the reports/ prefix in bucket example-bucket. Do not modify anything.
```

rather than an ambiguous request such as:

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

Normal repository work should look like:

```text
Plan if needed → Claude Code → implementation → tests/checks → automatic repository completion → verification
```

AWS work should look like:

```text
Plan/decision if needed → AWS MCP → AWS change/query → verification
```

## If you do not see this

If Claude Code stops at an open PR waiting for you, treat that as a repository automation/configuration issue rather than the desired daily workflow.

If Claude is trying to perform repository implementation in a normal Project chat without repository tooling, move that task to Claude Code web.

## Ask ordinary Claude or ChatGPT this

```text
I have a High Director-style Claude setup where Claude is the primary repository modifier/operator.

Routine repository changes should not require me to approve pull requests or merges. Branches/PRs may still be used for history and automated checks.

Task I want to perform: [describe it]
Current repository workflow: [describe it]

Tell me the simplest autonomous sequence using Claude Code web and GitHub. Do not ask for credentials or secrets.
```

## Next chapter

Continue to [Chapter 9 — Troubleshooting]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }}).
