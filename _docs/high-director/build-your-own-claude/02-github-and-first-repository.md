---
title: Build Your Own Sly Director — 02 — GitHub Test Repository
summary: Create the GitHub test repository used to verify the Sly Director GitHub connector.
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

Create one private repository Sly Director can use to test its GitHub connector safely.

## Complete this step

If you already created `claude-director-test`, keep using it and continue to Chapter 3.

Otherwise:

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
9. Select **Add file → Create new file**.
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

```text
README.md
claude-test.txt
```

Continue to [Chapter 3 — Create the Sly Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }}).

<details>
<summary>Additional information</summary>

The test repository keeps its existing technical name so anyone already following the guide does not need to recreate it because the product was renamed.

Chapter 5 will create the **Sly Director GitHub** custom connector and initially give its GitHub token access only to this test repository.

</details>
