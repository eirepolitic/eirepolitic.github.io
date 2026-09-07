---
title: Build Your Own High Director 12 — Maintenance and Credential Rotation
summary: Maintain the completed High Director-style integration, rotate credentials in a controlled order, monitor costs, and retire the system safely when no longer needed.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 72
permalink: /docs/high-director/build-your-own/12-maintenance/
---

# Chapter 12 — Maintenance and Credential Rotation

## Goal

Keep the system working without treating a credential expiry or platform UI change as a reason to rebuild everything.

The main items that can change over time are:

- GitHub fine-grained personal access token;
- Lambda `APP_API_KEY`;
- Lambda code/dependencies;
- ChatGPT Action configuration;
- GitHub/OpenAI/AWS user-interface wording;
- your AWS costs and account access.

## Monthly maintenance checklist

Once a month, or after a period of heavy use, check:

1. AWS Billing and Cost Management for unexpected spend.
2. The AWS budget created in Chapter 4 still exists and sends notifications to an address you read.
3. GitHub fine-grained token expiration date.
4. Lambda health endpoint.
5. One protected read from `director-test` if the integration has not been used recently.
6. GPT Action still lists the expected operations.
7. No unexpected repositories, branches, pull requests, workflow state changes, variables, or secrets were created by testing.

Do not rotate credentials merely because you checked them. Rotate when required by expiration, suspected exposure, account policy, or your own security schedule.

## Rotate the GitHub personal access token

Rotate this credential when it is approaching expiration, has been revoked, or may have been exposed.

### Step 1 — Create the replacement first

In GitHub:

1. Open your profile picture.
2. Select **Settings**.
3. Select **Developer settings**.
4. Open **Personal access tokens → Fine-grained tokens**.
5. Select **Generate new token**.
6. Use a temporary descriptive name such as:

```text
high-director-lambda-replacement
```

7. Select your personal account as **Resource owner**.
8. Select **All repositories** to preserve the architecture used by this guide.
9. Recreate the permissions required by Chapter 3:
   - Actions: Read and write;
   - Contents: Read and write;
   - Pull requests: Read and write;
   - Secrets: Read and write;
   - Variables: Read and write;
   - Workflows: Read and write.
10. Generate the token.
11. Store the new token privately.
12. Do **not** revoke the old token yet.

### Step 2 — Replace `GITHUB_TOKEN` in Lambda

1. Open AWS Lambda in `us-east-2`.
2. Open `github-gpt-wrapper`.
3. Open **Configuration → Environment variables**.
4. Select **Edit**.
5. Replace only the value of `GITHUB_TOKEN` with the new token.
6. Do not change `APP_API_KEY`, `GITHUB_OWNER`, `BRANCH_PREFIX`, or `DEFAULT_BASE_BRANCH` during this rotation.
7. Save.

### Step 3 — Test before revoking the old token

Run the Chapter 6 protected read test against `director-test.txt`.

Then test one normal read through the custom GPT.

If both succeed, the replacement token is working.

### Step 4 — Revoke the old token

Return to GitHub fine-grained token settings.

1. Identify the old token by name and expiration date.
2. Confirm the replacement has already passed testing.
3. Revoke/delete the old token.
4. Rename the replacement token later if you want a stable naming convention.

Do not revoke the old token before the replacement is installed unless the old token is suspected to be compromised. In a suspected-exposure case, revoke first and accept the short outage while installing the replacement.

## Rotate the Lambda `APP_API_KEY`

The current wrapper accepts one `APP_API_KEY` value. There is no documented dual-key overlap mechanism, so rotating it requires updating both Lambda and the GPT Action close together.

### Step 1 — Generate a new key

Open AWS CloudShell and run:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Store the new value privately.

### Step 2 — Update Lambda

1. Open `github-gpt-wrapper`.
2. Open **Configuration → Environment variables**.
3. Select **Edit**.
4. Replace only `APP_API_KEY` with the new value.
5. Save.

At this point the old key should stop authenticating protected wrapper routes.

### Step 3 — Update the GPT Action immediately

1. Open the GPT editor.
2. Open the GitHub Action.
3. Open **Authentication**.
4. Keep **API Key → Custom header → X-API-Key**.
5. Replace the stored API-key value with the new `APP_API_KEY`.
6. Save/update the Action configuration.

### Step 4 — Test

Use the GPT to read `director-test.txt`.

If it succeeds, record the rotation date in your private setup note.

Do not store the new key in the note itself.

## What to do if a secret is exposed

### GitHub token exposed

1. Revoke the exposed token in GitHub.
2. Create a replacement with the intended permissions.
3. Update Lambda `GITHUB_TOKEN`.
4. Test the protected backend read.
5. Review GitHub activity for unexpected operations during the exposure window.

### APP_API_KEY exposed

1. Generate a new `APP_API_KEY`.
2. Replace it in Lambda.
3. Replace it in the GPT Action authentication configuration.
4. Test the Action.
5. Do not reuse the exposed value.

Do not post the exposed credential while asking for help. State only which credential type was exposed and that it has been or will be rotated.

## Update Lambda code deliberately

Do not update dependencies or wrapper code just because newer versions exist.

The initial guide uses pinned dependencies matching the verified High Director source:

```text
fastapi==0.115.12
mangum==0.19.0
httpx==0.28.1
PyNaCl==1.5.0
pydantic==2.11.3
```

When you intentionally change code or dependencies:

1. record what you intend to change and why;
2. rebuild the ZIP in CloudShell;
3. update the Lambda code;
4. run the health test;
5. run the protected `director-test.txt` read;
6. test the affected Action operation in `director-test`;
7. only then use the changed wrapper on important repositories.

Do not combine a dependency upgrade, credential rotation, runtime change, and schema change into one troubleshooting attempt.

## If the Lambda Function URL changes

The normal setup does not require the Function URL to change during routine operation.

If you intentionally delete/recreate the Function URL or Lambda function:

1. obtain the new Function URL;
2. test `/health` directly;
3. test the protected backend read;
4. update only `servers[0].url` in the GPT Action schema;
5. keep API-key authentication configured as `X-API-Key`;
6. test the GPT Action again.

Do not create additional public Function URLs simply because one Action request failed.

## If the GitHub username changes

The wrapper owner boundary is controlled by:

```text
GITHUB_OWNER
```

A GitHub username/owner change is not just a GPT prompt change.

If the owner actually changes:

1. verify the GitHub account/repository ownership state;
2. verify the fine-grained token resource owner and repository access;
3. update `GITHUB_OWNER` in Lambda only after those facts are known;
4. test `director-test` or another safe repository under the new owner.

Do not send `owner/repo` in the Action to work around an incorrect backend owner.

## Back up configuration without backing up secrets

Keep a private maintenance record containing:

```text
AWS region
Lambda function name
runtime
architecture
handler
memory
timeout
Function URL recorded: yes/no
GitHub owner
GitHub token name
GitHub token expiration date
APP_API_KEY last rotated date
branch prefix
default base branch
GPT name
OpenAPI schema version
last successful end-to-end test date
```

Do not put secret values in this record.

## Retire the integration safely

If you no longer want the system:

1. stop using the custom GPT Action;
2. remove or disable the Action in the GPT editor;
3. revoke the GitHub fine-grained token;
4. delete the Lambda Function URL or Lambda function if it is no longer needed;
5. review AWS for any remaining resources you created specifically for this project;
6. review AWS Billing and Cost Management afterward;
7. delete dummy test variables/secrets and the `director-test` repository if you no longer want them.

Do not delete an AWS account simply to remove one Lambda function.

## Ask ordinary ChatGPT this

```text
I maintain a custom GPT → AWS Lambda → GitHub integration.

I need to perform this maintenance task: [GitHub token rotation / APP_API_KEY rotation / Lambda code update / Function URL change / owner change / retirement].
Current known working checkpoint: [describe it]
What has changed: [describe it]

Do not ask for my existing or replacement credentials. Give me a change-one-thing-at-a-time procedure that preserves the current architecture. Include a test before I revoke or remove the previous working component whenever that is safely possible.
```

## Core guide complete

If Chapters 1–12 are complete and the end-to-end tests pass, the core High Director-style GitHub integration is ready for normal use.

Optional extensions:

- [Addendum A — Google Workspace]({{ '/docs/high-director/build-your-own/addendum-google-workspace/' | relative_url }})
- [Addendum B — Additional AWS capabilities]({{ '/docs/high-director/build-your-own/addendum-additional-aws-capabilities/' | relative_url }})
