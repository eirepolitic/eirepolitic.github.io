---
title: Build Your Own Sly Director — 02 — GitHub and First Repository
summary: Create the GitHub test repository used to verify GitHub MCP from the Sly Director Project.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 82
permalink: /docs/high-director/build-your-own-claude/02-github-and-first-repository/
---

# Chapter 2 — Create the GitHub Test Repository

## Goal

Create one private repository Sly Director can use to test GitHub MCP safely.

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
Sly Director connection test.
```

12. Commit the file to `main`.

## What you should see

The repository should contain:

```text
README.md
claude-test.txt
```

Continue to [Chapter 3 — Create the Sly Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }}).

<details>
<summary>Additional information</summary>

The repository name remains `claude-director-test` so anyone who already followed the earlier guide does not need to rename or recreate it. Chapter 4 will access it directly from the Sly Director Project through GitHub MCP.

If your default branch has a name other than `main`, use that branch name throughout the guide.

</details>

<details>
<summary>Troubleshooting</summary>

If the files are missing, confirm you are in `claude-director-test` and that the new file was committed.

</details>
