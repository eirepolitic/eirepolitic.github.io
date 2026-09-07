---
title: Build Your Own High Director
summary: A zero-assumed-knowledge, browser-only guide for creating a personal High Director-style GPT that can work with GitHub repositories through an AWS Lambda wrapper.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 60
permalink: /docs/high-director/build-your-own/
---

# Build Your Own High Director

## What this guide does

This guide walks a complete beginner through creating a High Director-style system from scratch.

You do **not** need to know Python, Git, GitHub, YAML, AWS, APIs, Lambda, or OpenAPI before starting. The main path is browser-only. You will not install Git, Python, the AWS CLI, an editor, or any other software on your computer.

When finished, your GPT will be able to use an AWS Lambda-backed Action to work with repositories belonging to your GitHub account. The core implementation follows the same architecture and behavior as the currently verified High Director GitHub integration. The guide does not introduce architectural security changes that could change behavior or create new compatibility problems.

The optional addenda cover capabilities that are useful but not required for the initial build, including Google Workspace integration and additional AWS-facing tools.

## What you will build

The core path creates this chain:

```text
You
  |
  v
Custom GPT in ChatGPT
  |
  | HTTPS Action request + X-API-Key
  v
AWS Lambda Function URL
  |
  | GitHub personal access token
  v
GitHub REST API
  |
  v
Your repositories, branches, pull requests, workflows, variables, and secrets
```

The Lambda wrapper keeps your GitHub account owner configured on the backend. Your GPT therefore sends a repository name such as `my-project`, not `your-name/my-project`.

## Before you start: choose the correct path

Answer these questions in order.

### Question 1: Do you already have a custom GPT that you are allowed to edit?

- **Yes:** keep it. You can follow this guide and add the GitHub Action to that GPT.
- **No:** continue to Question 2.

### Question 2: Does your ChatGPT account belong to a Business, Enterprise, or Edu workspace where you have permission to create GPTs?

- **Yes:** you can create the GPT during this guide.
- **No or I do not know:** read [Chapter 1 — Accounts and prerequisites]({{ '/docs/high-director/build-your-own/01-accounts-and-prerequisites/' | relative_url }}) before spending money or creating cloud resources.

As verified on 2026-09-07, OpenAI states that new GPT creation is not available on personal Free, Go, Plus, or Pro accounts. Existing GPTs may still be editable when the account and permissions allow it. This is a platform requirement, not a limitation of the Lambda or GitHub design.

Official reference: [OpenAI — Creating and editing GPTs](https://help.openai.com/en/articles/8554397-creating-a-gpt).

### Question 3: Do you have a GitHub account?

- **Yes:** Chapter 2 will verify it and create a test repository if needed.
- **No:** Chapter 2 includes account creation from the first click.

### Question 4: Do you have an AWS account that you control?

- **Yes:** Chapter 4 begins with a safety and billing check before creating anything.
- **No:** Chapter 4 walks through creating one.

## Core chapters

Follow these pages in order. Do not skip ahead on the first build.

1. [Accounts and prerequisites]({{ '/docs/high-director/build-your-own/01-accounts-and-prerequisites/' | relative_url }})
2. [Create and prepare GitHub]({{ '/docs/high-director/build-your-own/02-github-account-and-first-repository/' | relative_url }})
3. [Create the GitHub access token]({{ '/docs/high-director/build-your-own/03-github-token/' | relative_url }})
4. [Create and prepare AWS]({{ '/docs/high-director/build-your-own/04-aws-account-and-safety/' | relative_url }})
5. [Deploy the GitHub wrapper Lambda]({{ '/docs/high-director/build-your-own/05-deploy-lambda/' | relative_url }})
6. [Create and test the Lambda Function URL]({{ '/docs/high-director/build-your-own/06-function-url-and-api-key/' | relative_url }})
7. [Create or configure the GPT]({{ '/docs/high-director/build-your-own/07-create-and-configure-gpt/' | relative_url }})
8. [Add the GitHub Action]({{ '/docs/high-director/build-your-own/08-add-github-action/' | relative_url }})
9. [End-to-end testing]({{ '/docs/high-director/build-your-own/09-end-to-end-testing/' | relative_url }})
10. [Daily use and safe operating habits]({{ '/docs/high-director/build-your-own/10-daily-operation/' | relative_url }})
11. [Troubleshooting]({{ '/docs/high-director/build-your-own/11-troubleshooting/' | relative_url }})
12. [Maintenance and credential rotation]({{ '/docs/high-director/build-your-own/12-maintenance/' | relative_url }})

Optional addenda:

- [Addendum A — Google Workspace]({{ '/docs/high-director/build-your-own/addendum-google-workspace/' | relative_url }})
- [Addendum B — Additional AWS capabilities]({{ '/docs/high-director/build-your-own/addendum-additional-aws-capabilities/' | relative_url }})

## What the GitHub Action will be able to do

The current High Director Action surface supports repository file and tree access, code search, preview/apply file changes, branches, pull requests, GitHub Actions workflow control and inspection, repository variables, and repository Actions secrets.

The backend implementation contains several routes that are not exposed by the current GPT schema. This guide keeps the initial Action surface aligned with the currently verified schema instead of adding unverified client behavior during the first build.

## What this guide deliberately does not change

The first build preserves these characteristics of the verified implementation:

- AWS Lambda Function URL with `AuthType: NONE`;
- application-level authentication using `X-API-Key`;
- GitHub fine-grained personal access token stored as a Lambda environment variable;
- one GitHub owner configured in the Lambda backend;
- repository names passed to the Action without `owner/`;
- branch prefix `gpt`;
- default base branch `main` unless changed during setup;
- current wrapper request and response behavior.

The guide may improve wording, packaging, verification, and beginner instructions, but it does not silently add server-side rules that change the wrapper's behavior.

## Important cost rule

Do not create a paid account, enable a paid service, choose a paid plan, or increase a cloud limit simply because a screen suggests it. Stop at the relevant chapter and read the cost note first.

AWS Lambda can be inexpensive for light personal use, but AWS is a metered cloud service and charges depend on usage and configuration. ChatGPT workspace eligibility can also involve a paid subscription. GitHub plans and usage limits can change.

## Secret-handling rule

During this guide you will create values that act like passwords. These include:

- the GitHub personal access token;
- the Lambda application API key;
- AWS account credentials;
- optional Google OAuth credentials.

Never paste secret values into this documentation, a GitHub file, a screenshot, a public issue, or a troubleshooting chat.

When this guide tells you to ask ordinary ChatGPT for troubleshooting help, replace secrets with text such as:

```text
[REDACTED]
```

## Standard checkpoint format

Each major chapter ends with three sections:

### What you should see

A short description of the expected successful result.

### If you do not see this

The safest checks to perform before changing anything.

### Ask ordinary ChatGPT this

A copy/paste prompt that provides enough non-secret context for a normal ChatGPT session to help diagnose the problem.

## Source of truth

This guide is derived from the verified High Director implementation documented in:

- [High Director GPT Configuration]({{ '/projects/high-director/gpt-configuration/' | relative_url }})
- [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }})
- [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }})
- [High Director GitHub Wrapper Live AWS Configuration]({{ '/projects/high-director/github-wrapper-live-aws-configuration/' | relative_url }})
- [High Director Runtime Architecture]({{ '/projects/high-director/runtime-architecture/' | relative_url }})
- [High Director Security and Configuration Reference]({{ '/projects/high-director/security-configuration-reference/' | relative_url }})

External platform interfaces can change. Pages that depend on current ChatGPT, GitHub, or AWS screens should be re-verified when those platforms change their user interfaces.
