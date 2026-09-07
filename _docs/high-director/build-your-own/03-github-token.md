---
title: Build Your Own High Director 03 — GitHub Access Token
summary: Create the fine-grained GitHub personal access token used by the Lambda wrapper, with the repository access and permissions needed by the verified High Director capabilities.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 63
permalink: /docs/high-director/build-your-own/03-github-token/
---

# Chapter 3 — Create the GitHub Access Token

## Goal

At the end of this chapter you will have one **fine-grained personal access token** that the AWS Lambda wrapper can use to call the GitHub REST API on your behalf.

The token is a secret. Anyone who obtains it may be able to perform the GitHub operations you authorize below.

## Why this token is needed

The custom GPT does not sign in to GitHub directly. Instead:

1. the GPT calls your AWS Lambda Action;
2. Lambda receives the request;
3. Lambda uses your GitHub token when it calls GitHub's REST API;
4. GitHub applies the permissions attached to the token.

GitHub recommends fine-grained personal access tokens when they can support the required API operations. The verified High Director wrapper is designed for a fine-grained token.

Official reference: [GitHub — Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).

## Important choice used by this guide

This guide follows the selected High Director-style personal-owner model:

```text
Resource owner: your personal GitHub account
Repository access: All repositories
```

This means repositories that you create later under the same personal GitHub owner can be used by the wrapper without creating a new token solely to add the repository.

This is convenient, but it is broader access than selecting only one repository. Treat the token as highly sensitive.

## Step 1 — Open fine-grained token settings

1. Sign in to [GitHub](https://github.com/).
2. Select your profile picture in the upper-right corner.
3. Select **Settings**.
4. Scroll to the bottom of the left sidebar.
5. Select **Developer settings**.
6. In the left sidebar, expand or find **Personal access tokens**.
7. Select **Fine-grained tokens**.
8. Select **Generate new token**.
9. GitHub may ask you to confirm your password or two-factor authentication. Complete that normal GitHub verification flow.

Do not select **Tokens (classic)** for the normal path in this guide.

## Step 2 — Name the token

In **Token name**, enter:

```text
high-director-lambda
```

In **Description**, enter something such as:

```text
Used by my AWS Lambda GitHub wrapper for my custom GPT.
```

## Step 3 — Choose an expiration

GitHub may allow multiple expiration choices.

Choose an expiration you are willing to maintain. A shorter lifetime reduces the time a leaked token remains useful, but it also means you must rotate it more often.

For the first setup, do not choose an unusually short expiration that might expire while you are still building the system.

Record the expiration date in your private setup note:

```text
GitHub token expires: YYYY-MM-DD
```

Do not record the token value in that note.

## Step 4 — Select the resource owner

Under **Resource owner**:

1. Select your personal GitHub account.
2. Confirm the displayed username exactly matches the GitHub owner recorded in Chapter 2.

If you select a different owner, the token will not behave like the personal-owner setup described by this guide.

## Step 5 — Select repository access

Under **Repository access**:

1. Select **All repositories**.
2. Read GitHub's explanation of what this grants before continuing.

If you intentionally want a more restricted implementation, you can instead select individual repositories, but that is not the architecture chosen for this guide and new repositories would need to be added to the token's access later.

## Step 6 — Set repository permissions

Find **Repository permissions**.

Set only the permissions needed by the wrapper's exposed capabilities. Permission names and grouping can change slightly in GitHub's interface, so use the current fine-grained token screen and GitHub REST documentation if a label differs.

Set these permissions to **Read and write** where that option is available:

| Permission | Setting | Why the wrapper needs it |
|---|---|---|
| Actions | Read and write | List workflows, inspect runs/jobs/artifacts, dispatch workflows, enable/disable workflows |
| Contents | Read and write | Read files and trees, create branches through Git references, create/update/delete repository files |
| Pull requests | Read and write | Create, list, inspect, update, close, and merge pull requests |
| Secrets | Read and write | Obtain the repository Actions public key and create/delete repository Actions secrets |
| Variables | Read and write | Create, update, and delete repository Actions variables |
| Workflows | Read and write | Supports writing workflow files under `.github/workflows/` through the contents API |

Leave unrelated repository permissions at **No access** unless GitHub automatically grants read-only **Metadata**, which is normal and required by many repository API operations.

Do not grant administration, issues, deployments, packages, webhooks, codespaces, or other unrelated permissions just because they are available.

GitHub's endpoint-permission reference is the authority if the platform changes the permissions required by an endpoint: [Permissions required for fine-grained personal access tokens](https://docs.github.com/en/rest/authentication/permissions-required-for-fine-grained-personal-access-tokens).

## Step 7 — Generate the token

Before selecting the final button, check:

```text
Resource owner = your personal GitHub username
Repository access = All repositories
Actions = Read and write
Contents = Read and write
Pull requests = Read and write
Secrets = Read and write
Variables = Read and write
Workflows = Read and write
```

Then:

1. Select **Generate token**.
2. GitHub will display the token value.
3. Copy it immediately.

## Step 8 — Store the token temporarily and safely

You will paste this token into the AWS Lambda environment-variable screen in Chapter 5.

For the short period between now and then:

1. Keep the token in a secure password manager or another private secret-storage method you already trust.
2. Do not send it by email or chat.
3. Do not paste it into ChatGPT.
4. Do not paste it into a GitHub repository.
5. Do not include it in screenshots.
6. Do not add it to the private setup note that contains ordinary configuration values.

If you accidentally expose the token, revoke it in GitHub and create a replacement before continuing.

## Step 9 — Record only the token metadata

In your private setup note, add:

```text
GitHub token name: high-director-lambda
GitHub token resource owner: YOUR_USERNAME
GitHub token repository access: All repositories
GitHub token expiration: YYYY-MM-DD
GitHub token value stored separately: yes
```

Do not write the actual token value there.

## What you should see

In GitHub's fine-grained token list, you should see a token named:

```text
high-director-lambda
```

Its resource owner should be your personal GitHub account. You should have the token value stored privately for Chapter 5.

## If you do not see this

Check these conditions before generating additional tokens:

1. Verify your GitHub email address is confirmed.
2. Confirm you are in **Settings → Developer settings → Personal access tokens → Fine-grained tokens**.
3. Confirm your personal account appears under **Resource owner**.
4. If GitHub rejects a permission combination, copy the exact non-secret message and check the current GitHub endpoint-permission documentation.
5. If the token value was displayed once and you lost it, do not guess it. Delete/revoke that token and create a new one.

## Ask ordinary ChatGPT this

```text
I am creating a GitHub fine-grained personal access token for an AWS Lambda wrapper that calls the GitHub REST API.

The wrapper needs repository file read/write, branch operations, pull request read/write and merge, GitHub Actions workflow/run operations, repository Actions variables, and repository Actions secrets.

I am using my personal GitHub account as the resource owner and All repositories as repository access.

I am stuck at: [screen or field]
What I expected: [describe it]
What I see: [describe it]
Exact non-secret error: [paste it]

Do not ask me to paste my token. Check the current GitHub documentation and give me click-by-click instructions. If a permission name has changed, tell me the current equivalent and why it is required.
```

## Next chapter

Continue to [Chapter 4 — Create and prepare AWS]({{ '/docs/high-director/build-your-own/04-aws-account-and-safety/' | relative_url }}).
