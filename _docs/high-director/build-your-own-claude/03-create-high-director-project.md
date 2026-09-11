---
title: Build Your Own High Director — Claude Edition 03 — Create the High Director Project
summary: Create the persistent Claude Project that carries High Director-style instructions across conversations.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-10
last_verified: 2026-09-10
order: 83
permalink: /docs/high-director/build-your-own-claude/03-create-high-director-project/
---

# Chapter 3 — Create the High Director Claude Project

## Goal

Create a Claude Project that acts as the persistent High Director workspace.

Claude Projects let you keep project instructions and project knowledge available across chats inside that project.

Official reference: [Create and manage projects](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects).

## Step 1 — Create the project

1. Open Claude in your browser.
2. Select **Projects** in the sidebar.
3. Select **Create project** or the current equivalent.
4. Name it:

```text
High Director
```

5. Add a description if Claude offers the field:

```text
Personal workspace for building, maintaining, and troubleshooting data pipelines, GitHub projects, automation, and AWS infrastructure.
```

## Step 2 — Open project instructions

1. Open the new **High Director** project.
2. Find **Set project instructions** or the current project-instructions control.
3. Paste the following instructions.

```text
Act as a concise coding and infrastructure assistant for designing and building data pipelines and related tools.

Be especially helpful with Python, GitHub, YAML, Appsmith, Power BI, Power Automate, AWS, and similar cloud/data tooling.

Assume I may have no understanding of the software, websites, or programming languages involved.

When I ask how to do something, provide explicit click-by-click instructions in order with minimal fluff.

Prefer actionable steps, commands, file structures, and examples I can immediately use.

Do not make important assumptions. When information is genuinely required to choose between designs that differ in function, cost, permissions, or architecture, identify the decision before implementation.

When I ask you to build something, first establish the plan and the decisions that materially affect function, cost, security, or design. After those decisions are settled, proceed with the implementation steps.

For repository work, inspect the relevant repository and existing files before proposing changes. Prefer small, reviewable changes. Use branches and pull requests for normal changes rather than treating the default branch as a scratch area.

For AWS work, prefer the simplest and least expensive option that satisfies the requirement. Do not broaden IAM permissions simply to make an error disappear. Use the permissions actually required for the intended operation.

When troubleshooting, preserve the exact error and identify the failing layer before changing architecture, credentials, permissions, dependencies, or unrelated settings.

Never ask me to paste passwords, access keys, OAuth tokens, GitHub credentials, or other secrets into ordinary troubleshooting text.
```

4. Select **Save instructions**.

## Step 3 — Keep project knowledge simple initially

Do not upload credentials, configuration exports containing secrets, or large collections of files just because Project knowledge is available.

For the first build, leave Project knowledge empty unless you have a specific non-secret reference document you want Claude to use.

Later, useful knowledge can include:

- architecture notes;
- coding conventions;
- non-secret data dictionaries;
- deployment standards;
- project requirements.

## Step 4 — Test the instructions

Start a new chat inside the High Director project.

Ask:

```text
I want to build a small data pipeline but I have not decided where it should run. What should we decide before implementation?
```

Claude should identify relevant design/cost decisions rather than jumping directly into an arbitrary architecture.

Then ask:

```text
I have never used GitHub before. Explain how I would create a repository.
```

The answer should be beginner-oriented and ordered.

## Step 5 — Understand the division of work

Use the **High Director Project** for:

- planning;
- architecture;
- explanations;
- deciding what to build;
- AWS work through connectors;
- troubleshooting and documentation.

Use **Claude Code on the web** for work that needs to inspect, edit, test, branch, and commit a GitHub repository.

They use the same Claude account, but they are different working surfaces.

## What you should see

You should have a project named **High Director** with saved project instructions and at least one successful test conversation.

## If you do not see this

If Projects or project instructions are missing, verify your Claude interface and plan before changing anything else.

Do not create an API integration simply to recreate project instructions.

## Ask ordinary Claude or ChatGPT this

```text
I am creating a Claude Project to act as a persistent coding/infrastructure assistant.
I am stuck at: [creating the project / project instructions / project knowledge / starting a project chat]
What I see: [describe it]
Exact non-secret error: [paste it]

Check current Claude Projects documentation and give me browser-only click-by-click steps. Do not ask for account credentials.
```

## Next chapter

Continue to [Chapter 4 — Connect and use Claude Code on the web]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }}).
