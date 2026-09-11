---
title: Build Your Own High Director — Claude Edition 02 — GitHub and First Repository
summary: Prepare GitHub for Claude Code on the web and create a disposable first repository for safe testing.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 82
permalink: /docs/high-director/build-your-own-claude/02-github-and-first-repository/
---

# Chapter 2 — Create and Prepare GitHub

## Goal

Create a safe repository Claude Code can use for its first test.

## Step 1 — Sign in

1. Open [GitHub](https://github.com/).
2. Sign in.
3. Confirm the account is the one recorded in Chapter 1.

## Step 2 — Create a test repository

1. Select the **+** menu near the upper-right corner.
2. Select **New repository**.
3. Choose your personal account under **Owner**.
4. Enter:

```text
claude-director-test
```

5. Choose **Private** unless you intentionally want it public.
6. Turn on **Add a README file**.
7. Leave other settings at their defaults for this test.
8. Select **Create repository**.

## Step 3 — Confirm the default branch

1. Open the new repository.
2. Find the branch selector above the file list.
3. Confirm it says `main`.
4. If it uses another name, record that exact name instead.

## Step 4 — Add one simple test file

1. Select **Add file → Create new file**.
2. Name the file:

```text
claude-test.txt
```

3. Enter:

```text
Claude High Director connection test.
```

4. Commit the file to the default branch.

## Step 5 — Record the repository name

Add to your private setup note:

```text
GitHub test repository: claude-director-test
Default branch: main
```

## What you should see

The repository should contain:

```text
README.md
claude-test.txt
```

## If you do not see this

Check that you are signed in to the correct GitHub account and that the file was committed rather than left in an editor.

## Ask ordinary Claude or ChatGPT this

```text
I am preparing GitHub for Claude Code on the web.
Repository: claude-director-test
I am stuck at: [creation / README / test file / branch]
What I clicked: [describe it]
Exact non-secret error: [paste it]

Give me current click-by-click GitHub instructions.
```

## Next chapter

Continue to [Chapter 3 — Create the High Director Claude Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }}).
