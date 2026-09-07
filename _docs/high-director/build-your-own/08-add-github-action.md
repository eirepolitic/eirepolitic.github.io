---
title: Build Your Own High Director 08 — Add the GitHub Action
summary: Connect the custom GPT to the Lambda wrapper using the verified 28-operation OpenAPI schema and an X-API-Key custom-header credential.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 68
permalink: /docs/high-director/build-your-own/08-add-github-action/
---

# Chapter 8 — Add the GitHub Action

## Goal

At the end of this chapter your custom GPT will have the same verified GitHub Action surface documented for High Director:

- file read;
- repository tree listing;
- repository code search;
- preview/apply file create or update;
- preview/apply file deletion;
- branch listing and creation;
- pull-request create/list/get/update/close/merge;
- GitHub Actions workflow listing and control;
- workflow-run, job, log, and artifact inspection;
- repository Actions variable create/update/delete;
- repository Actions secret create/update/delete.

The Action uses your Lambda Function URL and authenticates with your application API key in the `X-API-Key` HTTP header.

## Important distinction between the two secrets

You now have two different secrets:

```text
GitHub personal access token
    Lambda uses this when talking to GitHub.

APP_API_KEY
    ChatGPT uses this when talking to Lambda.
```

Do not put the GitHub personal access token into the GPT Action authentication screen.

The Action authentication value is the **APP_API_KEY** created in Chapter 5.

## Step 1 — Open the GPT editor

1. Open ChatGPT in a desktop web browser.
2. Open **Explore GPTs**.
3. Open **My GPTs** if you are editing an existing GPT.
4. Open the GPT from Chapter 7.
5. Select **Edit GPT** if needed.
6. Scroll to the **Actions** section.
7. Select **Create new action** or the current equivalent.

OpenAI's current Action documentation describes this path as **Actions → Create new action**.

Official reference: [OpenAI — Configuring actions in GPTs](https://help.openai.com/en/articles/9442513).

## Step 2 — Open the authoritative schema source

In another browser tab, open:

[High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }})

Scroll to **Sanitized authoritative OpenAPI source**.

The schema is OpenAPI `3.1.0`, API version `0.2.1`, and contains 28 operations.

## Step 3 — Copy the full YAML schema

1. Select the full YAML code block beginning with:

```yaml
openapi: 3.1.0
```

2. Copy the entire block through the final response definition.
3. Return to the GPT Action editor.
4. Paste it into the **Schema** editor.

Do not copy the explanatory text above or below the YAML code block.

## Step 4 — Replace the redacted server URL

The sanitized schema contains this placeholder:

```yaml
servers:
  - url: https://PRIVATE-LAMBDA-URL-REDACTED.invalid
```

Replace only the URL value with the real Lambda Function URL from Chapter 6.

For example, your edited lines should have this shape:

```yaml
servers:
  - url: https://YOUR-ACTUAL-ID.lambda-url.us-east-2.on.aws
```

Use your actual Function URL. Do not use the example text above.

The ending slash is not required in the schema server value. Avoid accidentally creating a double slash between the server and path.

Do not change the operation IDs, path names, request schemas, or security scheme during the initial build.

## Step 5 — Confirm schema validation

After pasting the schema, the GPT editor should validate it and display detected Action operations.

You should see operations including:

```text
getFile
listRepoTree
searchRepoContents
previewUpsertFile
applyUpsertFile
previewDeleteFile
applyDeleteFile
listBranches
createBranch
listPullRequests
createPullRequest
getPullRequest
updatePullRequest
closePullRequest
mergePullRequest
listWorkflows
listWorkflowRuns
getWorkflowRun
listWorkflowRunJobs
getWorkflowRunLogs
listWorkflowRunArtifacts
dispatchWorkflow
enableWorkflow
disableWorkflow
setVariable
deleteVariable
setSecret
deleteSecret
```

If the editor reports a schema error, stop and fix the schema before configuring authentication. Do not delete random sections until validation passes.

## Step 6 — Configure Action authentication

Find **Authentication**.

1. Select **API Key**.
2. Select the option for a **Custom header** if the editor asks how the key should be sent.
3. Set the header name to:

```text
X-API-Key
```

4. For the API-key value, paste the actual `APP_API_KEY` created in Chapter 5.
5. Save or confirm the authentication configuration.

Do not use **Bearer** unless the current GPT editor has changed and you have verified that its custom-header workflow is no longer available. The verified wrapper expects the literal header name `X-API-Key`.

Do not paste the GitHub personal access token here.

## Step 7 — Check the OpenAPI security declaration

The schema itself should contain:

```yaml
security:
  - ApiKeyAuth: []
```

and:

```yaml
securitySchemes:
  ApiKeyAuth:
    type: apiKey
    in: header
    name: X-API-Key
```

These declarations tell the GPT Action how the API is protected. The secret value itself belongs in the Action authentication UI, not inside the YAML.

## Step 8 — Check workspace domain restrictions

If the GPT editor displays a message similar to:

```text
No domains are allowed by your workspace's settings.
```

stop.

That is a ChatGPT workspace-policy issue, not an AWS or GitHub failure.

For Business, Enterprise, or Edu workspaces, an administrator may have to allow the Lambda Function URL domain for custom Actions.

Do not rebuild the Lambda to fix a workspace domain restriction.

## Step 9 — Keep the GPT private during testing

Do not publish the GPT to a broad audience during the initial setup.

The Action can modify repositories, merge pull requests, control workflows, and set repository secrets within the permissions granted to the GitHub token. Test it privately first.

If your workspace presents sharing options, use the narrowest sharing setting appropriate for your own testing.

## Step 10 — Save the draft Action configuration

If the editor requires a save step:

1. save the Action configuration;
2. remain in the GPT editor;
3. use Preview for Chapter 9 testing before broad sharing or publication.

## What you should see

The GPT editor should show one GitHub Action with:

```text
Server: your Lambda Function URL
Authentication: API Key
Header: X-API-Key
Schema: OpenAPI 3.1.0
API version: 0.2.1
Detected operations: 28
```

The schema editor should show no validation error.

## If you do not see this

Use the error category:

- **Schema validation error:** compare your pasted YAML with the authoritative v0.2.1 source and confirm only the server URL was changed.
- **No Action section:** check GPT/workspace eligibility and whether Apps are enabled instead of Actions.
- **No domains allowed:** contact the workspace administrator or change the workspace Action-domain policy if you are the authorized administrator.
- **Authentication configuration unclear:** confirm the editor supports API Key → Custom header and use `X-API-Key`.
- **Action test returns `401 unauthorized`:** re-enter the `APP_API_KEY`; do not rotate the GitHub token yet.
- **GitHub API error:** the Lambda connection worked far enough to reach GitHub; investigate the GitHub layer instead of rebuilding the GPT schema.

## Ask ordinary ChatGPT this

```text
I am configuring a custom GPT Action that calls my own AWS Lambda Function URL.

The API uses OpenAPI 3.1.0.
Authentication type: API Key
API-key style: custom header
Header name: X-API-Key
The schema has 28 GitHub-wrapper operations.
The server is my Lambda Function URL.

I am stuck at: [schema validation / authentication / domain policy / action test]
Exact sanitized error: [paste it]

I have removed the Function URL hostname if I do not want to share it, and I will not provide my APP_API_KEY, GitHub token, AWS credentials, or other secrets. Check current OpenAI custom GPT Action documentation and give me click-by-click troubleshooting steps. Do not tell me to change AWS or GitHub unless the error evidence points to that layer.
```

## Next chapter

Continue to [Chapter 9 — End-to-end testing]({{ '/docs/high-director/build-your-own/09-end-to-end-testing/' | relative_url }}).
