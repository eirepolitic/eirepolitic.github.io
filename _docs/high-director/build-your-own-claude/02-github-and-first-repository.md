---
title: Build Your Own High Director — Claude Edition 02 — GitHub and First Repository
summary: Create the GitHub test repository used to verify Claude Code.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 82
permalink: /docs/high-director/build-your-own-claude/02-github-and-first-repository/
---

# Chapter 2 — Create the GitHub Test Repository

## Goal

Create one private repository Claude Code can use for testing.

## Complete this step

1. Open [GitHub](https://github.com/).
2. Select the **+** menu in the upper-right corner.
3. Select **New repository**.
4. Under **Owner**, select your personal GitHub account.
5. Set **Repository name** to:

```text
claude-director-test
```

6. Select **Private**.
7. Turn on **Add a README file**.
8. Select **Create repository**.
9. In the repository, select **Add file → Create new file**.
10. Set the filename to:

```text
claude-test.txt
```

11. Enter:

```text
Claude High Director connection test.
```

12. Commit the file to `main`.

## What you should see

The repository should contain:

```text
README.md
claude-test.txt
```

Continue to [Chapter 3 — Create the High Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }}).

<details>
<summary>Additional information</summary>

The repository is intentionally small and disposable. It gives Claude Code a safe place to prove repository access before you connect important repositories.

If your default branch has a name other than `main`, use that branch name throughout the guide.

</details>

<details>
<summary>Troubleshooting</summary>

If the files are missing, confirm you are in `claude-director-test` and that the new file was committed.

Useful prompt:

```text
I am creating the GitHub test repository claude-director-test.
I am stuck at: [repository creation / README / file creation / commit]
What I see: [describe it]
Give me current click-by-click GitHub instructions.
```

</details>
