---
title: Build Your Own High Director — Claude Edition 04 — Claude Code on the Web
summary: Install and authorize the Claude GitHub App, connect Claude Code on the web to GitHub, and verify browser-only repository editing, testing, branches, and pull requests.
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

Anthropic documents Claude Code on the web as a browser-based service that works with GitHub repositories in a remote environment, makes changes, runs commands/tests, pushes a branch, and prepares work for pull-request review.

Official reference: [Claude Code on the web](https://support.claude.com/en/articles/12618689-claude-code-on-the-web).

## Important — Claude needs GitHub App access

For Claude Code on the web to work with a GitHub repository, Claude must be authorized through its GitHub integration/App and that App must have access to the repository you want Claude Code to use.

For this guide, do **not** create a GitHub personal access token. Install/authorize the Claude GitHub App instead.

## Step 1 — Open Claude Code on the web

1. Sign in to Claude with the Pro account from Chapter 1.
2. Open Claude Code from the Claude interface or Anthropic's Claude Code web entry point.
3. Confirm the page offers a way to choose or connect a GitHub repository.

Do not install the terminal CLI for this guide.

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
5. GitHub may ask which account or organization should receive the App. Select your personal GitHub account for this guide.
6. GitHub may offer repository-access choices such as:
   - **All repositories**; or
   - **Only select repositories**.
7. For the first test, choose **Only select repositories** if that option is available.
8. Select:

```text
claude-director-test
```

9. Select GitHub's **Install**, **Authorize**, **Save**, or current equivalent button.
10. Complete any normal GitHub confirmation GitHub itself requires.
11. Return to Claude Code.
12. Refresh the repository selector if necessary.

You should now be able to see `claude-director-test` in Claude Code.

### Why selected repositories first?

Using only `claude-director-test` makes the initial setup easier to review. Later, you can add other repositories to the Claude GitHub App without creating a new personal access token.

If you deliberately want Claude Code to work across every repository in your personal GitHub account, you can change the App to **All repositories** later.

## Step 4 — Select the test repository

1. Start a new Claude Code web task/session.
2. Select:

```text
claude-director-test
```

3. If Claude asks which branch to start from, use `main` unless your repository uses another default branch.

## Step 5 — Start with a read-only task

Enter:

```text
Inspect this repository. Read claude-test.txt and README.md. Do not change any files yet. Tell me what is currently in the repository.
```

Claude should inspect the repository in its remote environment and report the existing files.

## Step 6 — Give Claude a small test task

Enter:

```text
Create a new file named claude-code-test.md containing:

# Claude Code test
This file was created through Claude Code on the web.

Before finishing, verify the file exists and show me what you changed.
```

Claude Code should work in its isolated environment.

## Step 7 — Review the task result

When the task finishes:

1. Review Claude's summary.
2. Review the file diff if the interface provides it.
3. Confirm the only intended repository change is `claude-code-test.md`.
4. Look for the branch/PR controls presented by Claude Code.

Anthropic's current documentation states that completed web tasks can push changes to a new GitHub branch and present them for pull-request review.

## Step 8 — Create or open the pull request

Use the Claude Code web interface to create/open the pull request for the completed task.

Then in GitHub:

1. Open `claude-director-test`.
2. Select **Pull requests**.
3. Open the pull request Claude created.
4. Review the **Files changed** tab.
5. Confirm `claude-code-test.md` is the intended change.

## Step 9 — Merge the safe test pull request

Because this is the disposable repository and the change is known:

1. Review the PR one final time.
2. Merge it using the repository's normal merge option.
3. Return to the repository's `main` branch.
4. Confirm `claude-code-test.md` now exists.

## Step 10 — Understand what Claude Code replaces

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

## Step 11 — Add additional repositories later

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

Do not create a PAT simply because a new repository is missing from Claude Code. First check the Claude GitHub App's repository access.

## What you should see

You should now have:

- the Claude GitHub App/integration installed and authorized in GitHub;
- `claude-director-test` included in the App's repository access;
- Claude Code web able to select that repository;
- a successful remote repository task;
- a branch/pull request containing `claude-code-test.md`;
- the merged file visible on `main`.

## If you do not see this

- If Claude asks you to connect GitHub, install/authorize the Claude GitHub App.
- If the App is installed but `claude-director-test` is missing, open the App's GitHub configuration and add that repository.
- If Claude cannot push/create a PR, check the GitHub App authorization and repository rules rather than creating a PAT.
- If the task environment fails to set up, preserve the exact Claude Code error.
- If Claude made unwanted changes, do not merge the PR. Refine the task and run a new isolated task.

## Ask ordinary Claude or ChatGPT this

```text
I am using Claude Code on the web with a Claude Pro account and GitHub.
Repository: claude-director-test
I am not using the Claude Code CLI, local Git, or a personal access token.
Claude Code should access GitHub through the Claude GitHub App/integration.

Failing stage: [install GitHub App / authorize GitHub / grant repository access / select repository / start task / edit / push branch / create PR]
What I expected: [describe it]
What I see: [describe it]
Exact non-secret error: [paste it]

Do not ask for GitHub passwords, OAuth tokens, or credentials. Check current Claude Code web documentation and give me browser-only troubleshooting steps.
```

## Next chapter

Continue to [Chapter 5 — Create and prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).
