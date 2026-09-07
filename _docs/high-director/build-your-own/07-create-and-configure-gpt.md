---
title: Build Your Own High Director 07 — Create and Configure the GPT
summary: Create or edit the custom GPT and configure its identity, instructions, and basic behavior before adding the GitHub Action.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 67
permalink: /docs/high-director/build-your-own/07-create-and-configure-gpt/
---

# Chapter 7 — Create or Configure the GPT

## Goal

At the end of this chapter you will have a custom GPT with the High Director-style behavior configured, but no GitHub Action attached yet.

Separating behavior from the Action makes it easier to identify whether later problems come from GPT instructions or from the external API connection.

## Current ChatGPT account requirement

As verified on 2026-09-07, new GPT creation is not available on personal Free, Go, Plus, or Pro accounts. Existing GPTs may remain editable when plan and permission requirements allow it. New GPT creation is available in eligible Business, Enterprise, and Edu workspaces when workspace settings permit it.

Official references:

- [OpenAI — Creating and editing GPTs](https://help.openai.com/en/articles/8554397-creating-a-gpt)
- [OpenAI — Configuring actions in GPTs](https://help.openai.com/en/articles/9442513)

If Chapter 1 did not establish that you can create or edit a GPT, stop here.

## Step 1 — Open the GPT editor

### If you are creating a new GPT

1. Open ChatGPT in a desktop web browser.
2. Switch to the eligible Business, Enterprise, or Edu workspace if needed.
3. Open **Explore GPTs**.
4. Select **Create**.
5. Open the direct configuration/editor view if ChatGPT presents a choice between conversational creation and manual configuration.

### If you are editing an existing GPT

1. Open **Explore GPTs**.
2. Open **My GPTs**.
3. Select the GPT you want to use.
4. Select **Edit GPT**.

## Step 2 — Set the name

For a direct High Director-style build, enter:

```text
High Director
```

If you already have a GPT with that name or prefer a personal name, you may choose another name. The name does not affect the Lambda integration.

## Step 3 — Set the description

Enter:

```text
Concise assistant for data pipelines and cloud build work.
```

This matches the verified High Director description.

## Step 4 — Add conversation starters

Add these four starters:

```text
Design a Python ETL pipeline
```

```text
Show GitHub steps click by click
```

```text
Write a YAML workflow for this
```

```text
Help debug this AWS pipeline issue
```

These are examples only. They do not grant permissions or connect external systems.

## Step 5 — Set the Instructions field

Find the large **Instructions** field.

Replace placeholder instructions for a new GPT with the following verified High Director behavior text:

```text
A GPT that acts as a concise coding assistant for designing and building data pipelines and related infrastructure. It should be especially helpful with Python, GitHub, YAML, Appsmith, Power BI, Power Automate, and AWS. It should help users design, troubleshoot, document, and implement pipeline workflows and supporting infrastructure. Keep responses short, direct, and practical. Do not make assumptions; when required information is missing, ask a focused question before proceeding. When the user asks how to do something, provide explicit click-by-click instructions in order, with minimal fluff. Prefer actionable steps, commands, file structures, and examples that the user can immediately use. When relevant, suggest how custom actions could support recurring tasks such as creating or editing .py and .yaml files in GitHub repositories, but do not claim actions exist unless the user has added them. Be precise, technical, and efficient. Avoid unnecessary background explanation unless the user asks for it. When multiple valid paths exist, present the safest or simplest option first and confirm before choosing among options that would change architecture or implementation details. Keep responses short. Assume the user has no understanding of any software, websites or languages used. When requested to build something, first complete a plan, asking the user for any decisions relevant to function, cost or design, then go into the step by step directions after the user has confirmed the plan.

For this GitHub action, the owner is already configured in the backend.
Always pass the repository name only in the repo parameter, never owner/repo.

If a GitHub action call fails, do not guess that the repo format is wrong unless the API response explicitly says so.
Do not ask the user for the owner name for this action.
```

Do not add your GitHub username, GitHub token, Lambda API key, Function URL, AWS account number, or other credentials to the Instructions field.

## Step 6 — Leave Knowledge empty for the initial build

The verified High Director configuration had no visible Knowledge files in the supplied configuration record.

For the first setup:

1. Do not upload source code or credential files as Knowledge.
2. Leave Knowledge empty unless you already have a specific non-secret reference file you intentionally want the GPT to use.

This removes one variable from the initial test.

## Step 7 — Review built-in capabilities

OpenAI can change which capability toggles appear. The verified source material for High Director did not establish the exact capability-toggle state, so this guide does not invent a required configuration.

For the initial GitHub Action test:

1. Do not enable **Apps** if doing so prevents use of **Actions**.
2. Leave unrelated capability settings at their defaults unless you know you need them.
3. If the editor states that a GPT can use either Apps or Actions but not both, choose **Actions** for this build.

The GitHub integration does not require an uploaded Knowledge file.

## Step 8 — Choose an Action-compatible model

The original verified High Director configuration showed a recommended model of `Thinking 5.6` at the time of that configuration capture.

Do not treat that old label as a permanent requirement. OpenAI model names and Action support can change.

Use this rule:

1. Choose a current non-Pro model that the GPT editor allows with custom Actions.
2. If the editor removes or disables a model after you add an Action, use one of the Action-compatible models it offers.
3. Do not choose a model solely because its name matches an old screenshot.

OpenAI's current Action documentation notes that custom Actions are not available in Pro mode.

## Step 9 — Do not publish yet

If you are creating a new GPT, leave it as a draft while you add and test the Action in Chapter 8.

If you are editing an existing GPT, do not select **Update** until the Action configuration is complete unless the editor requires an intermediate save.

## Step 10 — Test behavior without the Action

Use the GPT editor's Preview pane.

Ask:

```text
I want to build a Python ETL pipeline but I have not decided where it will run. What should we decide first?
```

The GPT should respond by planning and asking about relevant design/cost/function decisions rather than pretending it already has the answer.

Then ask:

```text
How do I create a new GitHub repository?
```

It should give ordered beginner-friendly steps.

Do not ask it to access GitHub yet. The Action has not been configured.

## What you should see

You should have a draft or editable GPT with:

```text
Name: High Director (or your chosen name)
Description: Concise assistant for data pipelines and cloud build work.
Instructions: High Director-style instructions installed
Conversation starters: 4
Knowledge: empty for initial build
GitHub Action: not added yet
```

The Preview behavior should be concise, practical, and beginner-oriented.

## If you do not see this

- If **Create** is missing, return to Chapter 1 and verify workspace eligibility.
- If **Actions** is unavailable, check workspace policy and whether Apps are enabled instead.
- If the editor reports that no domains are allowed, a Business/Enterprise/Edu workspace administrator may need to permit Action domains.
- If the GPT ignores the desired behavior, re-check the Instructions field before adding more tools.

Do not modify AWS or GitHub credentials to fix a GPT-behavior problem.

## Ask ordinary ChatGPT this

```text
I am configuring a custom GPT in ChatGPT for a GitHub/AWS coding assistant.

I am stuck in the GPT editor before adding the Action.
My account/workspace type: [personal existing GPT / Business / Enterprise / Edu]
What I clicked: [describe it]
What I expected: [describe it]
What I see: [describe it]
Exact non-secret error or message: [paste it]

Do not ask for any API key, GitHub token, Function URL, AWS credential, or private workspace information. Check current OpenAI documentation and give me click-by-click instructions for the present GPT editor.
```

## Next chapter

Continue to [Chapter 8 — Add the GitHub Action]({{ '/docs/high-director/build-your-own/08-add-github-action/' | relative_url }}).
