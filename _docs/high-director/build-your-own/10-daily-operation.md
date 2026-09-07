---
title: Build Your Own High Director 10 — Daily Operation
summary: Beginner operating guidance for using the High Director-style GPT safely and predictably after the integration has passed testing.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 70
permalink: /docs/high-director/build-your-own/10-daily-operation/
---

# Chapter 10 — Daily Use and Safe Operating Habits

## Goal

This chapter explains how to use the finished system without having to understand Git internals, AWS internals, or the GitHub REST API.

The wrapper is powerful enough to change files, create branches and pull requests, merge pull requests, dispatch or disable workflows, and manage repository Actions variables and secrets. Use that power deliberately.

## The most important repository rule

When the GPT asks for or sends the repository parameter, use the repository name only.

Correct:

```text
my-project
```

Incorrect:

```text
my-username/my-project
```

The owner is already configured in the Lambda environment variable `GITHUB_OWNER`.

## Recommended pattern for normal code changes

For ordinary repository changes, use this sequence:

1. tell the GPT which repository you want to work on;
2. ask it to inspect the relevant files first;
3. ask it to explain the proposed change briefly;
4. ask it to preview the file change;
5. review the diff the GPT returns;
6. tell it to apply the change to a `gpt` branch;
7. ask it to create a draft pull request;
8. review the pull request in GitHub;
9. merge only after you are satisfied with the change.

This is an operating habit, not a server-enforced requirement. The current wrapper can technically write to an existing default branch if a caller explicitly supplies that branch. Do not rely on the backend to prevent every bad instruction.

## Example request for a code change

Use wording such as:

```text
In repository my-project, inspect the existing files related to the data import. Explain what needs to change first. Then preview the smallest change. Do not apply it until I approve the preview.
```

After reviewing the preview:

```text
Apply that exact change to a new gpt-prefixed branch and create a draft pull request into main. Do not merge it.
```

## When creating a brand-new repository

The current wrapper operates **inside repositories** but does not expose a create-repository operation.

For a new project:

1. create the empty repository in the GitHub website;
2. add a README if you want an initial default branch immediately;
3. tell the GPT the new repository name;
4. ask it to inspect the tree;
5. then use preview/apply operations to create project files on a branch.

Do not assume the Action can create a GitHub repository simply because it can create files and branches inside one.

## When asking the GPT to write YAML workflows

A GitHub Actions workflow normally lives under:

```text
.github/workflows/
```

Before applying a workflow file:

1. ask the GPT what the workflow will trigger on;
2. ask what permissions it requests;
3. ask which secrets or variables it expects;
4. preview the YAML;
5. create it on a branch;
6. review the pull request;
7. merge only when you understand when the workflow will run.

A workflow can create costs or make external changes depending on what it does. The fact that a YAML file validates does not mean the automation is appropriate.

## Workflow control

The Action can:

```text
list workflows
inspect runs
inspect jobs
obtain log download URLs
list artifacts
dispatch workflow_dispatch workflows
enable workflows
disable workflows
```

For dispatch, enable, or disable operations, specify the exact repository and workflow you mean.

Do not use workflow state changes as a diagnostic shortcut. If a workflow failed, inspect the run/jobs/logs first.

## Pull-request merges

The wrapper supports:

```text
merge
squash
rebase
```

If you do not know which merge method a repository expects, ask the GPT to inspect the repository conventions or GitHub settings before choosing.

For an important repository, review the pull request in GitHub before asking the GPT to merge it.

## Repository variables

Use repository Actions variables for non-sensitive configuration such as:

```text
DEPLOY_REGION=us-east-2
DATA_ENV=dev
```

A variable is not a secret. Do not store passwords, API keys, tokens, or private credentials as variables.

## Repository secrets

Use repository Actions secrets for values that a GitHub Actions workflow needs to keep hidden.

The wrapper can set a secret because it:

1. obtains GitHub's repository Actions public key;
2. encrypts the supplied plaintext using PyNaCl;
3. sends the encrypted value to GitHub;
4. does not return the plaintext value.

GitHub will not let you read the stored plaintext back later. If you no longer know a secret value, replace it rather than trying to recover it through the Action.

Only provide a real secret in a conversation when you intentionally need the GPT Action to set that secret and you understand the privacy implications of submitting the value through ChatGPT and the configured Action. Do not include secrets in ordinary troubleshooting conversations or documentation.

## New repositories and token scope

This guide selected **All repositories** for the fine-grained token under your personal GitHub owner.

That means a newly created repository under that same owner should normally fall inside the token's repository-access selection without creating a new token solely for that repository.

The repository must still exist, and your GitHub user must still have the underlying access needed for the operation.

## Common safe request patterns

### Inspect before changing

```text
Inspect repository my-project and find the files responsible for [task]. Do not change anything yet.
```

### Preview a change

```text
Preview the smallest change needed in my-project. Show me the diff before applying it.
```

### Apply to a branch

```text
Apply the approved change to a new gpt-prefixed branch. Do not merge it.
```

### Create a pull request

```text
Create a draft pull request from that branch into main. Summarize what changed and any risks.
```

### Inspect a failed GitHub Action

```text
In my-project, list the recent runs for workflow [workflow name or ID]. Inspect the failed run and its jobs before suggesting a code change.
```

## Things not to do casually

Do not casually ask the GPT to:

- delete files without reviewing the target path;
- merge a pull request you have not reviewed;
- disable a workflow just because it failed;
- overwrite a real repository secret with a test value;
- write directly to `main` because it is faster;
- make multiple unrelated repository changes in one request when you are trying to diagnose a problem;
- change AWS IAM, Function URL authentication, or credential permissions to fix an ordinary application error.

## What you should see

Normal daily work should usually produce visible GitHub evidence:

```text
read result → branch → commit → pull request → review → merge
```

For workflow troubleshooting, the evidence chain is usually:

```text
workflow → run → jobs → logs/artifacts → diagnosis
```

## If you do not see this

If the GPT claims a write succeeded but you cannot see the branch, commit, pull request, variable, secret name, or workflow state in GitHub:

1. ask the GPT for the returned operation result;
2. check the relevant GitHub page directly;
3. do not repeat the write blindly;
4. move to Chapter 11 if the state is unclear.

## Ask ordinary ChatGPT this

```text
I use a custom GPT that calls a GitHub wrapper through AWS Lambda. The wrapper can read/write files, manage branches and PRs, inspect/control GitHub Actions, and manage repository variables/secrets.

I want help deciding the safest sequence for this task: [describe task].
Repository name: [repo name only]
Important constraints: [describe them]

Do not ask for tokens, API keys, secret values, or AWS credentials. Give me the safest operational sequence first, using preview/branch/PR review where appropriate. Do not assume a backend safeguard exists unless I explicitly say it does.
```

## Next chapter

Continue to [Chapter 11 — Troubleshooting]({{ '/docs/high-director/build-your-own/11-troubleshooting/' | relative_url }}).
