---
title: Build Your Own Sly Director — 02 — Create a GitHub Test Repository
summary: Create a small private repository used to prove the Sly Director GitHub connector works.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 82
permalink: /docs/high-director/build-your-own-claude/02-github-and-first-repository/
---

# Chapter 2 — Create the GitHub Test Repository

## Goal

Create a harmless repository where you can test Sly Director before using it on real work.

A repository is simply a GitHub folder that keeps files and their change history.

## Step 1 — Create the repository

1. Open GitHub.
2. In the top-right corner, select **+ → New repository**.
3. For **Repository name**, enter:

```text
claude-director-test
```

4. Select **Private**.
5. Turn on **Add a README file**.
6. Select **Create repository**.

## Step 2 — Add one test file

1. Inside the new repository, select **Add file → Create new file**.
2. For the filename, enter:

```text
claude-test.txt
```

3. Enter:

```text
Sly Director connection test.
```

4. Select **Commit changes**.
5. Keep the default option to commit directly to `main`.
6. Select **Commit changes** again.

## Step 3 — Check the result

You should now see at least:

```text
README.md
claude-test.txt
```

The default branch should be:

```text
main
```

You will use this repository later to test reading files, creating branches, opening pull requests, running GitHub Actions, and merging changes.

Continue to [Chapter 3 — Create the Sly Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }}).
