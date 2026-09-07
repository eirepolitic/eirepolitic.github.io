---
title: Build Your Own High Director 02 — GitHub Account and First Repository
summary: Prepare GitHub for a High Director-style agent, including creating a first repository when the user has never used GitHub before.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 62
permalink: /docs/high-director/build-your-own/02-github-account-and-first-repository/
---

# Chapter 2 — Create and Prepare GitHub

## Goal

At the end of this chapter you will have:

- a confirmed GitHub username;
- at least one repository that you own;
- a simple test file in that repository;
- the repository name recorded exactly as GitHub displays it.

If you already use GitHub and own repositories, you can still create the small test repository below. It gives you a safe place to test the future GPT without risking an existing project.

## What is a repository?

A **repository**, often shortened to **repo**, is a project folder stored on GitHub. It can contain code, documentation, configuration files, GitHub Actions workflows, and file history.

The High Director-style wrapper is designed so that the GPT receives only the repository name. For example:

```text
director-test
```

Do not give the Action this form:

```text
your-username/director-test
```

The GitHub owner is configured separately in AWS later.

## Step 1 — Sign in to GitHub

1. Open [GitHub](https://github.com/).
2. Select **Sign in** if you are not already signed in.
3. Sign in to the account you want the future GPT to control.
4. Select your profile picture.
5. Confirm the username shown is the one you recorded in Chapter 1.

If the username is wrong, sign out and use the correct account before continuing.

## Step 2 — Create a safe test repository

Even if you already have repositories, use a separate test repository for the first end-to-end test.

1. In GitHub, select the **+** button near the upper-right corner.
2. Select **New repository**.
3. Under **Owner**, choose your personal GitHub account.
4. In **Repository name**, enter:

```text
director-test
```

5. In **Description**, optionally enter:

```text
Safe test repository for my custom GPT GitHub integration.
```

6. Choose **Private** if GitHub offers the choice and you do not want the test repository public.
7. Turn on **Add a README file**.
8. Leave the other options at their defaults unless you already understand and intentionally want to change them.
9. Select **Create repository**.

## Step 3 — Confirm the default branch

After GitHub opens the new repository:

1. Look near the file list for the branch selector.
2. It should normally show `main`.
3. If it shows `main`, continue.
4. If it shows a different branch name, record that exact name in your private setup note.

The verified High Director wrapper can use a configured `DEFAULT_BASE_BRANCH`. This guide uses `main` because that matches the current deployment and the normal new-repository default.

Do not rename your default branch solely for this guide if you already have a different established default. Instead, use the actual branch name later when configuring the Lambda environment variable.

## Step 4 — Create a simple test file

The README is enough to prove read access, but a second file makes later testing clearer.

1. In the `director-test` repository, select **Add file**.
2. Select **Create new file**.
3. In the file-name box, enter:

```text
director-test.txt
```

4. In the editor, enter:

```text
High Director connection test.
```

5. Find the commit section.
6. Leave the default option to commit directly to the current default branch for this one manual setup file.
7. Enter a commit message such as:

```text
Add connection test file
```

8. Select **Commit changes**.

## Step 5 — Learn the four GitHub areas you will use later

You do not need to understand them yet. You only need to know where they are.

Open your `director-test` repository and identify these tabs or sections:

1. **Code** — files and folders in the repository.
2. **Pull requests** — proposed branch changes that can be reviewed and merged.
3. **Actions** — automated workflows stored under `.github/workflows/`.
4. **Settings** — repository configuration, including Actions secrets and variables.

Do not change anything in these areas yet.

## Step 6 — Decide how broad the token should be

Your selected architecture is the same broad-owner approach used by High Director: the Lambda stores one GitHub owner and the GitHub token determines which repositories under that owner it can access.

For a personal account, Chapter 3 will instruct you to select **All repositories** for the fine-grained personal access token so new repositories created later can be used without regenerating the token each time.

This is intentionally broader than a one-repository-only setup. The tradeoff is that anyone who obtains the token could exercise the token's granted permissions across those repositories. Treat the token like a password.

## Step 7 — Record the GitHub values you will need later

In your private setup note, add:

```text
GitHub owner: YOUR_USERNAME
Test repository: director-test
Default base branch: main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

The owner and repository name are not secrets. Do not add any token yet.

## What you should see

Open the repository's **Code** tab. You should see at least:

```text
README.md
director-test.txt
```

The repository should belong to the personal GitHub account you intend to connect to the Lambda.

## If you do not see this

Check these items in order:

1. Confirm you are signed in to the correct GitHub account.
2. Select your profile picture and verify the username.
3. Return to the repository list from your profile.
4. Open `director-test` again.
5. Confirm the file was committed rather than left in an unsaved editor.
6. Do not delete or recreate the GitHub account to fix a repository problem.

## Ask ordinary ChatGPT this

```text
I am setting up GitHub for a browser-only custom GPT integration.

My GitHub username is not secret, but I will not provide any password or token.
I am trying to create or inspect a test repository named director-test.
What I clicked: [describe the clicks]
What I expected: [describe it]
What I actually see: [describe it]
Exact non-secret error: [paste it]

Give me current GitHub click-by-click troubleshooting steps. Do not ask for my password, personal access token, recovery codes, or other secrets.
```

## Next chapter

Continue to [Chapter 3 — Create the GitHub access token]({{ '/docs/high-director/build-your-own/03-github-token/' | relative_url }}).
