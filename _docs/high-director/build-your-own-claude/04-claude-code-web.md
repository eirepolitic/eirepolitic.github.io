---
title: Build Your Own High Director — Claude Edition 04 — Claude Code on the Web
summary: Connect Claude Code on the web to GitHub and verify browser-only repository editing, testing, branches, and pull requests.
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

Connect Claude Code on the web to GitHub and prove that it can work in `claude-director-test` without installing anything locally.

Anthropic documents Claude Code on the web as a browser-based service that clones a GitHub repository into an isolated remote environment, makes changes, runs commands/tests, pushes a branch, and creates a pull request for review.

Official reference: [Claude Code on the web](https://support.claude.com/en/articles/12618689-claude-code-on-the-web).

## Step 1 — Open Claude Code on the web

1. Sign in to Claude with the Pro account from Chapter 1.
2. Open Claude Code from the Claude interface or Anthropic's Claude Code web entry point.
3. Confirm the page offers a way to choose or connect a GitHub repository.

Do not install the terminal CLI for this guide.

## Step 2 — Connect GitHub

If Claude Code asks you to connect GitHub:

1. Select the GitHub connection button.
2. GitHub will open an authorization/install screen.
3. Confirm you are signed in to the intended GitHub account.
4. Read which repositories the GitHub integration will be allowed to access.
5. For the first test, grant access to `claude-director-test` at minimum.
6. Complete GitHub's authorization flow.
7. Return to Claude Code.

If GitHub offers a choice between all repositories and selected repositories, the simplest cautious first test is **selected repositories** with `claude-director-test`. You can add repositories later.

## Step 3 — Select the test repository

1. Start a new Claude Code web task/session.
2. Select:

```text
claude-director-test
```

3. If Claude asks which branch to start from, use `main` unless your repository uses another default branch.

## Step 4 — Start with a read-only task

Enter:

```text
Inspect this repository. Read claude-test.txt and README.md. Do not change any files yet. Tell me what is currently in the repository.
```

Claude should inspect the repository in its remote environment and report the existing files.

## Step 5 — Give Claude a small test task

Enter:

```text
Create a new file named claude-code-test.md containing:

# Claude Code test
This file was created through Claude Code on the web.

Before finishing, verify the file exists and show me what you changed.
```

Claude Code should work in its isolated environment.

## Step 6 — Review the task result

When the task finishes:

1. Review Claude's summary.
2. Review the file diff if the interface provides it.
3. Confirm the only intended repository change is `claude-code-test.md`.
4. Look for the branch/PR controls presented by Claude Code.

Anthropic's current documentation states that completed web tasks can push changes to a new GitHub branch and present them for pull-request review.

## Step 7 — Create or open the pull request

Use the Claude Code web interface to create/open the pull request for the completed task.

Then in GitHub:

1. Open `claude-director-test`.
2. Select **Pull requests**.
3. Open the pull request Claude created.
4. Review the **Files changed** tab.
5. Confirm `claude-code-test.md` is the intended change.

## Step 8 — Merge the safe test pull request

Because this is the disposable repository and the change is known:

1. Review the PR one final time.
2. Merge it using the repository's normal merge option.
3. Return to the repository's `main` branch.
4. Confirm `claude-code-test.md` now exists.

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

Claude Code's managed GitHub connection handles repository access instead.

## Step 10 — Add additional repositories later

When you create another repository:

1. create it in GitHub;
2. open the GitHub App/integration settings if Claude Code cannot see it;
3. add that repository to the integration's permitted repositories;
4. start a new Claude Code web task and select it.

Do not make the integration broader than necessary simply because a repository is missing from the selector.

## What you should see

You should now have:

- Claude Code web connected to GitHub;
- `claude-director-test` selectable;
- a successful remote repository task;
- a branch/pull request containing `claude-code-test.md`;
- the merged file visible on `main`.

## If you do not see this

- If the repository is missing, check the GitHub integration's repository access.
- If Claude cannot push/create a PR, check GitHub authorization rather than creating a PAT.
- If the task environment fails to set up, preserve the exact Claude Code error.
- If Claude made unwanted changes, do not merge the PR. Refine the task and run a new isolated task.

## Ask ordinary Claude or ChatGPT this

```text
I am using Claude Code on the web with a Claude Pro account and GitHub.
Repository: claude-director-test
I am not using the Claude Code CLI or local Git.

Failing stage: [connect GitHub / select repository / start task / edit / push branch / create PR]
What I expected: [describe it]
What I see: [describe it]
Exact non-secret error: [paste it]

Do not ask for GitHub passwords, OAuth tokens, or credentials. Check current Claude Code web documentation and give me browser-only troubleshooting steps.
```

## Next chapter

Continue to [Chapter 5 — Create and prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).
