---
title: Build Your Own High Director — Claude Edition 04 — Claude Code on the Web
summary: Install and authorize the Claude GitHub App, connect Claude Code on the web to GitHub, and verify autonomous browser-only repository operation.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Connect and Use Claude Code on the Web

## Goal

Install and authorize the Claude GitHub App, then prove that Claude Code on the web can work in `claude-director-test` without installing anything locally.

Claude Code on the web runs repository tasks remotely, can make changes and run tests, and normally pushes completed work to a branch and creates a pull request. In this guide, that pull request is treated as a repository record and automation boundary, not as a required user-approval step.

Official reference: [Claude Code on the web](https://support.claude.com/en/articles/12618689-claude-code-on-the-web).

## Important — Claude needs GitHub App access

For Claude Code on the web to work with a GitHub repository, Claude must be authorized through its GitHub integration/App and that App must have access to the repository you want Claude Code to use.

Use the Claude GitHub App for repository access in this guide.

## Important — The agent is the repository operator

This guide assumes Claude is the primary modifier and operator of the repositories connected to it.

The normal workflow proceeds without manual user review of each pull request.

Claude may use branches and pull requests when they improve traceability, automated testing, rollback, or change history. Where repository tooling permits, Claude should complete the repository workflow itself. If the web product produces a pull request but does not itself provide an autonomous merge control, configure repository automation rather than making the user the routine merge gate.

## Step 1 — Open Claude Code on the web

1. Sign in to Claude with the Pro account from Chapter 1.
2. Open Claude Code from the Claude interface or Anthropic's Claude Code web entry point.
3. Confirm the page offers a way to choose or connect a GitHub repository.

## Step 2 — Check whether the Claude GitHub App is already installed

### If Claude Code already shows `claude-director-test`

The GitHub App/integration is already installed and has access to the test repository.

Continue to Step 4.

### If Claude Code asks you to connect GitHub, or the repository is missing

Continue to Step 3.

## Step 3 — Install and authorize the Claude GitHub App

1. In Claude Code, select the button to **Connect GitHub**, **Install GitHub App**, or the current equivalent.
2. GitHub will open an authorization/installation page.
3. Confirm you are signed in to the GitHub account from Chapter 2.
4. Confirm the App/integration being installed is the Claude/Anthropic GitHub integration presented by Claude Code.
5. Select your personal GitHub account for this guide.
6. If GitHub offers **All repositories** or **Only select repositories**, choose **Only select repositories** for the first test.
7. Select `claude-director-test`.
8. Select GitHub's **Install**, **Authorize**, **Save**, or current equivalent button.
9. Complete any normal GitHub confirmation GitHub itself requires.
10. Return to Claude Code and refresh the repository selector if necessary.

## Step 4 — Select the test repository

1. Start a new Claude Code web task/session.
2. Select `claude-director-test`.
3. If Claude asks which branch to start from, use `main` unless your repository uses another default branch.

## Step 5 — Start with a read-only task

Enter:

```text
Inspect this repository. Read claude-test.txt and README.md. Tell me what is currently in the repository.
```

Claude should inspect the repository and report the existing files.

## Step 6 — Give Claude a complete test task

Enter:

```text
Create a new file named claude-code-test.md containing:

# Claude Code test
This file was created through Claude Code on the web.

Verify the change, run any relevant repository checks, and complete the repository-side workflow as far as the available GitHub/Claude tooling permits. Proceed without waiting for my approval.
```

Claude Code should work in its isolated environment and push the completed work to GitHub.

## Step 7 — Confirm the repository result

When the task finishes, inspect the result to verify that the automation worked as intended.

Check:

1. Claude's task summary.
2. The branch or pull request it created, if applicable.
3. Any tests or checks it ran.
4. Whether `claude-code-test.md` reached the intended final repository state.

If the web workflow stops with an open pull request because autonomous merge is not available in that surface, continue to Step 8.

## Step 8 — Configure automatic completion when pull requests are used

The objective is that ordinary Claude-created changes complete without waiting for a user to click **Merge**.

Use the simplest repository mechanism available to complete qualifying Claude-created pull requests automatically after required checks pass. Depending on the repository, this can be GitHub auto-merge or repository automation configured specifically for Claude-created branches/PRs.

The intended flow is:

```text
Claude change → automated validation → automated merge/completion
```

Keep any automated merge rule narrow enough that it applies only to the intended Claude-created changes.

If no autonomous merge mechanism is available for the repository, Claude may use a simpler supported write path instead where appropriate and permitted by the repository.

## Step 9 — Understand what Claude Code replaces

For normal GitHub development, Claude Code web replaces the following custom components from the ChatGPT edition:

```text
GitHub personal access token
custom GitHub Lambda wrapper
Lambda Function URL
APP_API_KEY
OpenAPI Action schema
manual branch/write API calls
```

Claude Code's GitHub App/integration handles repository authorization instead.

## Step 10 — Add additional repositories later

When you create another repository:

1. create it in GitHub;
2. open GitHub **Settings**;
3. find the installed GitHub Apps/integrations area;
4. open the Claude/Anthropic GitHub App installed for Claude Code;
5. add the new repository to its permitted repositories, or change to **All repositories** if that is intentionally what you want;
6. save the GitHub App configuration;
7. return to Claude Code;
8. refresh the repository selector;
9. select the newly authorized repository.

If a new repository is missing from Claude Code, first check the Claude GitHub App's repository access.

## What you should see

You should now have:

- the Claude GitHub App/integration installed and authorized in GitHub;
- `claude-director-test` included in the App's repository access;
- Claude Code web able to select that repository;
- a successful remote repository task;
- automated tests/checks where relevant;
- repository changes able to reach their intended final state without routine user approval.

## If you do not see this

- If Claude asks you to connect GitHub, install/authorize the Claude GitHub App.
- If the App is installed but `claude-director-test` is missing, add that repository in the App configuration.
- If Claude can create a branch/PR but it remains open indefinitely, inspect the repository's merge automation.
- If repository rules prevent the intended autonomous workflow, decide whether those rules should be adjusted for this agent-operated repository.
- If the task environment fails to set up, preserve the exact Claude Code error.
- If Claude makes an incorrect change, correct or revert it through the repository workflow.

## Ask ordinary Claude or ChatGPT this

```text
I am using Claude Code on the web as the primary autonomous operator of a GitHub repository.

Routine pull requests or merges should complete automatically where the available tooling permits. Branches and PRs may be used for traceability and checks.

Failing stage: [GitHub App / repository access / task / branch / PR / checks / automatic merge or completion]
What I expected: [describe it]
What I see: [describe it]
Exact non-secret error: [paste it]

Give me the simplest browser-based fix that preserves autonomous repository operation.
```

## Next chapter

Continue to [Chapter 5 — Create and prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).
