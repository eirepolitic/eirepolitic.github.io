---
title: Build Your Own High Director — Claude Edition 04 — Claude Code on the Web
summary: Connect Claude Code on the web to GitHub and verify repository access.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Connect Claude Code to GitHub

## Goal

Give Claude Code access to `claude-director-test` and verify it can modify the repository.

## Complete this step

1. Open Claude Code on the web from your Claude account.
2. Select **Connect GitHub**, **Install GitHub App**, or the current equivalent.
3. GitHub will open.
4. Select your personal GitHub account.
5. Choose **Only select repositories**.
6. Select:

```text
claude-director-test
```

7. Select **Install**, **Authorize**, or **Save**.
8. Return to Claude Code.
9. Select `claude-director-test`.
10. Start a task and enter:

```text
Inspect this repository. Read README.md and claude-test.txt and tell me what is in the repository.
```

11. After that succeeds, enter:

```text
Create a file named claude-code-test.md containing:

# Claude Code test
This file was created through Claude Code on the web.

Verify the change, run relevant checks, and complete the repository-side workflow as far as the available tooling permits. Proceed without waiting for my approval.
```

12. Open GitHub and confirm `claude-code-test.md` was created through Claude's repository workflow.

## What you should see

Claude Code should be able to read the repository and create a repository change.

Continue to [Chapter 5 — Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).

<details>
<summary>Additional information</summary>

Claude Code uses the Claude/Anthropic GitHub App. The primary path does not require a GitHub personal access token.

Claude is the intended repository operator. Branches and pull requests may be used when useful for checks and history. Routine user approval is not part of the intended workflow.

If Claude Code creates a pull request but the repository requires a merge step, repository automation or auto-merge can be configured later so qualifying changes complete without routine manual approval.

To add another repository later, open the Claude/Anthropic GitHub App configuration in GitHub and add that repository to its allowed repositories.

</details>

<details>
<summary>Troubleshooting</summary>

If the repository is missing, check the Claude GitHub App's repository access in GitHub settings.

If Claude can read but cannot write, inspect the exact Claude Code error and the repository rules/permissions.

Useful prompt:

```text
I am connecting Claude Code on the web to GitHub.
Repository: claude-director-test
I am stuck at: [GitHub App / repository selection / read / write / branch / PR]
Exact non-secret error: [paste it]
Give me the simplest browser-based fix.
```

</details>
