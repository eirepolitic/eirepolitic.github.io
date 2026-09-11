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

## Important — Projects are not inside Claude Code

Claude has two different browser surfaces in this guide:

```text
Normal Claude web app
→ Projects, project instructions, planning, connectors, AWS work

Claude Code on the web
→ GitHub repositories, code changes, tests, branches, pull requests
```

If you are currently looking at **Claude Code** and do not see **Projects**, that is expected.

For this chapter, leave Claude Code and return to the normal Claude web app at `claude.ai`.

## Step 1 — Confirm you are in the normal Claude app

1. Open a new browser tab.
2. Go to `https://claude.ai/`.
3. Confirm you are in the normal Claude chat interface, not the Claude Code repository workspace.
4. Look at the left sidebar.
5. Find **Projects**.

If you only see repository/task controls, you are still in Claude Code. Return to the normal Claude interface before continuing.

## Step 2 — Create the project

1. In the normal Claude sidebar, select **Projects**.
2. Select **Create project** or the current equivalent.
3. Name it:

```text
High Director
```

4. Add a description if Claude offers the field:

```text
Personal workspace for building, maintaining, and troubleshooting data pipelines, GitHub projects, automation, and AWS infrastructure.
```

## Step 3 — Open project instructions

1. Open the new **High Director** project.
2. Find **Set project instructions** or the current project-instructions control.
3. Paste the following instructions.

```text
Act as a concise coding and infrastructure assistant for designing and building data pipelines and related tools.

Assume I may have no understanding of the software, websites, or programming languages involved.

When I ask how to do something, provide explicit click-by-click instructions in order, with minimal fluff.

Prefer actionable steps, commands, file structures, and examples that I can immediately use.

Do not make important assumptions. When information is genuinely required to choose between designs that differ in function, cost, permissions, or architecture, identify the decision before implementation.

When I ask you to build something:

1. First establish the plan and identify any decisions that materially affect function, cost, security, or design.
2. After those decisions are settled, write the plan to the relevant repository.
3. If the build is small, proceed with the implementation steps.
4. If the build is larger, determine whether the work can be completed more efficiently across multiple new chat instances.
5. Where efficient, divide the plan into work for up to four separate chat instances. Write a complete prompt for each new chat instance, including all relevant context, its specific responsibilities, constraints, repository information, and the part of the plan it should complete.
6. After those separate chat instances complete their work, the user can return to the original chat instance and inform it that the work is complete. The original chat instance should then validate the completed work, reconcile or stitch together the different contributions, resolve any inconsistencies, and finish the overall plan.
7. The user may ask to move to a new chat instance at any point. When this happens, write a complete continuation prompt for the new chat instance. Include all context needed to continue from the current point in the plan, including decisions already made, work already completed, remaining work, relevant repository details, constraints, and the next intended steps.

For repository work, inspect the relevant repository and existing files before proposing changes. Prefer small, reviewable changes. Use branches and pull requests for normal changes rather than treating the default branch as a scratch area.

For AWS work, prefer the simplest and least expensive option that satisfies the requirement. Do not broaden IAM permissions simply to make an error disappear. Use only the permissions actually required for the intended operation.

When troubleshooting, preserve the exact error and identify the failing layer before changing architecture, credentials, permissions, dependencies, or unrelated settings.

Never ask me to paste passwords, access keys, OAuth tokens, GitHub credentials, or other secrets into ordinary troubleshooting text.
```

4. Select **Save instructions**.

## Step 4 — Keep project knowledge simple initially

Do not upload credentials, configuration exports containing secrets, or large collections of files just because Project knowledge is available.

For the first build, leave Project knowledge empty unless you have a specific non-secret reference document you want Claude to use.

Later, useful knowledge can include:

- architecture notes;
- coding conventions;
- non-secret data dictionaries;
- deployment standards;
- project requirements.

## Step 5 — Test the instructions

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

## Step 6 — Understand the division of work

Use the **High Director Project in normal Claude** for:

- planning;
- architecture;
- explanations;
- deciding what to build;
- AWS work through connectors;
- troubleshooting and documentation.

Use **Claude Code on the web** for work that needs to inspect, edit, test, branch, and commit a GitHub repository.

They use the same Claude account, but they are different browser surfaces.

## What you should see

In the normal Claude web app, you should have a project named **High Director** with saved project instructions and at least one successful test conversation.

You should **not** expect this Project to appear inside the Claude Code repository interface.

## If you do not see this

First confirm which interface you are in:

- normal Claude chat interface → Projects should be available according to current account/product availability;
- Claude Code repository interface → Projects are not expected there.

If Projects are still missing in the normal Claude app, verify the current Claude interface and account availability before changing anything else.

Do not create an API integration simply to recreate project instructions.

## Ask ordinary Claude or ChatGPT this

```text
I am creating a Claude Project to act as a persistent coding/infrastructure assistant.

I understand that Projects are in the normal Claude web app, not Claude Code on the web.
I am currently in: [normal Claude / Claude Code / unsure]
I am stuck at: [finding Projects / creating the project / project instructions / project knowledge / starting a project chat]
What I see: [describe it]
Exact non-secret error: [paste it]

Check current Claude Projects documentation and give me browser-only click-by-click steps. Do not ask for account credentials.
```

## Next chapter

Continue to [Chapter 4 — Connect and use Claude Code on the web]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }}).
