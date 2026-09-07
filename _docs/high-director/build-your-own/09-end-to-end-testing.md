---
title: Build Your Own High Director 09 — End-to-End Testing
summary: Test the custom GPT against a safe GitHub repository in stages, proving read, write, branch, pull-request, workflow, variable, and secret capabilities before normal use.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 69
permalink: /docs/high-director/build-your-own/09-end-to-end-testing/
---

# Chapter 9 — End-to-End Testing

## Goal

This chapter proves that the full chain works:

```text
You → custom GPT → GPT Action → Lambda Function URL → GitHub REST API → director-test repository
```

Use only the `director-test` repository for the initial tests.

Do not begin by asking the GPT to modify an important repository.

## Before you start

Confirm all of these are true:

```text
Backend health test passed: yes
Authenticated Lambda file read passed: yes
GPT Action schema validates: yes
Action authentication uses APP_API_KEY in X-API-Key: yes
Test repository: director-test
```

If any answer is no, return to the relevant chapter.

## Stage 1 — Prove read-only access

Open the GPT Preview pane or a private chat with your draft GPT.

Ask:

```text
Read director-test.txt from the director-test repository and tell me its contents. Use the GitHub action. The repository parameter is director-test only.
```

The expected file content is:

```text
High Director connection test.
```

Then ask:

```text
List the repository tree for director-test.
```

You should see at least `README.md` and `director-test.txt`.

Then ask:

```text
Search the director-test repository for the phrase High Director.
```

This checks the three primary read/browse operations:

```text
getFile
listRepoTree
searchRepoContents
```

## Stage 2 — Prove preview without writing

Ask:

```text
Preview creating a file named gpt-test.md in director-test with this content:

# GPT connection test
This file was proposed through the custom GPT Action.

Use commit message: Preview GPT connection test.
Do not apply the change yet.
```

The GPT should use the preview operation and return a proposed branch name and diff.

Now open GitHub in another tab and refresh the `director-test` repository.

The new file should **not** exist on `main` yet.

This proves the preview endpoint is non-writing.

## Stage 3 — Apply the file change on a branch

Ask:

```text
Apply the gpt-test.md change you just previewed to a gpt-prefixed branch. Do not merge anything yet.
```

The Action should return a branch name and commit information.

In GitHub:

1. Open `director-test`.
2. Open the branch selector.
3. Confirm a new branch beginning with `gpt` exists.
4. Open that branch.
5. Confirm `gpt-test.md` exists there.
6. Switch back to `main`.
7. Confirm `gpt-test.md` is not yet on `main`.

This proves file apply and branch creation behavior.

## Stage 4 — Create and inspect a pull request

Ask the GPT:

```text
Create a draft pull request in director-test from the branch containing gpt-test.md into main. Title it "Test GPT GitHub integration" and explain that this is a safe connection test.
```

Then ask:

```text
List open pull requests in director-test.
```

Then:

```text
Get the details of the test pull request you just created.
```

In GitHub, open **Pull requests** and confirm the same draft pull request exists.

## Stage 5 — Update the pull request

Ask:

```text
Update the test pull request title to "Verified GPT GitHub integration". Keep it open.
```

Refresh GitHub and confirm the title changed.

This proves the update route.

## Stage 6 — Merge the test pull request

Because this is the isolated `director-test` repository and the change is known, ask:

```text
Merge the test pull request using the normal merge method.
```

If ChatGPT asks you to approve the external action, read the requested action and approve it only if it matches the test you intend.

Then open the repository's `main` branch in GitHub and confirm `gpt-test.md` is now present.

This proves pull-request merge behavior.

## Stage 7 — Test repository variables with harmless data

Do not use a real credential for this test.

Ask:

```text
Set a repository Actions variable in director-test named DIRECTOR_TEST_VARIABLE with value connection-ok.
```

Verify it in GitHub:

1. Open `director-test`.
2. Select **Settings**.
3. Open **Secrets and variables**.
4. Select **Actions**.
5. Open the **Variables** area.
6. Confirm `DIRECTOR_TEST_VARIABLE` exists.

Then ask:

```text
Delete the DIRECTOR_TEST_VARIABLE repository Actions variable from director-test.
```

Refresh GitHub and confirm it is gone.

## Stage 8 — Test repository secrets with a dummy value

Use a value that is deliberately not a real secret.

Ask:

```text
Set a repository Actions secret in director-test named DIRECTOR_TEST_SECRET with the dummy plaintext value not-a-real-secret.
```

Verify only that the secret name exists in GitHub. GitHub will not show you the stored plaintext value again.

Then ask:

```text
Delete the DIRECTOR_TEST_SECRET repository Actions secret from director-test.
```

Confirm the name is gone.

This proves the wrapper can fetch GitHub's repository public key, encrypt a secret with PyNaCl, store it, and delete it without using any real credential in the test.

## Stage 9 — Test workflow capabilities when a workflow exists

If `director-test` already has a GitHub Actions workflow, ask:

```text
List workflows in director-test. Do not enable, disable, or dispatch anything yet.
```

If no workflow exists, that is not a failure. Workflow operations require a workflow to exist.

For a later safe workflow test, create a simple `workflow_dispatch` workflow in `director-test`, review it, merge it, and then test these operations one at a time:

```text
listWorkflows
listWorkflowRuns
dispatchWorkflow
getWorkflowRun
listWorkflowRunJobs
getWorkflowRunLogs
listWorkflowRunArtifacts
enableWorkflow
disableWorkflow
```

Do not test enable/disable or dispatch against an important production workflow simply to prove the Action works.

## Stage 10 — Test close without merge using a second draft pull request

The first pull request was merged, so use a second harmless branch/PR to test closing.

Ask the GPT to:

1. preview a harmless file such as `close-test.txt`;
2. apply it to a new `gpt` branch;
3. create a draft pull request;
4. list/get the pull request;
5. close it without merging.

Confirm in GitHub that the pull request is closed and the file was not added to `main`.

## Capability verification matrix

Use this matrix to record what you have actually verified.

| Capability | Initial status |
|---|---|
| Read file | Test in Stage 1 |
| List repository tree | Test in Stage 1 |
| Search repository contents | Test in Stage 1 |
| Preview file upsert | Test in Stage 2 |
| Apply file upsert | Test in Stage 3 |
| Preview file delete | Test later on a disposable test file |
| Apply file delete | Test later on a disposable test file |
| List branches | Implicitly or explicitly test after Stage 3 |
| Create branch | Test in Stage 3 |
| List pull requests | Test in Stage 4 |
| Create pull request | Test in Stage 4 |
| Get pull request | Test in Stage 4 |
| Update pull request | Test in Stage 5 |
| Close pull request | Test in Stage 10 |
| Merge pull request | Test in Stage 6 |
| List workflows | Test in Stage 9 when workflow exists |
| List workflow runs | Test in Stage 9 when workflow exists |
| Get workflow run | Test in Stage 9 when workflow exists |
| List workflow jobs | Test in Stage 9 when workflow exists |
| Get workflow logs | Test in Stage 9 when workflow exists |
| List workflow artifacts | Test when a workflow produces an artifact |
| Dispatch workflow | Test only with a safe `workflow_dispatch` workflow |
| Enable workflow | Test only with a safe test workflow |
| Disable workflow | Test only with a safe test workflow |
| Set variable | Test in Stage 7 |
| Delete variable | Test in Stage 7 |
| Set secret | Test in Stage 8 using a dummy value |
| Delete secret | Test in Stage 8 |

## What you should see

At minimum, before using an important repository, you should have confirmed:

- read access;
- tree/search access;
- preview behavior;
- branch-based file write;
- pull-request creation and inspection;
- pull-request merge in the test repository;
- variable set/delete;
- dummy secret set/delete.

Workflow controls can be verified after a safe test workflow exists.

## If you do not see this

When one operation fails but earlier operations worked, do not rebuild the entire system.

Examples:

- reads work but writes fail → check GitHub `Contents` permission;
- files work but PR operations fail → check `Pull requests` permission;
- repository operations work but workflow operations fail → check `Actions`/`Workflows` permissions and whether the workflow exists;
- variables fail → check `Variables` permission;
- secrets fail → check `Secrets` permission and the exact GitHub response;
- every Action call returns Lambda `401` → check the GPT Action's `APP_API_KEY` configuration;
- backend CloudShell test works but GPT Action fails → focus on GPT schema/auth/domain settings rather than Lambda code.

## Ask ordinary ChatGPT this

```text
I am testing a custom GPT → AWS Lambda → GitHub REST API integration in a disposable repository named director-test.

Earlier tests that passed: [list them]
Operation that now fails: [operation]
Exact sanitized GPT Action response: [paste it]
GitHub HTTP status if shown: [status]

The Lambda backend was already tested independently. Do not ask for my APP_API_KEY, GitHub PAT, AWS credentials, or any real secret value. Map the failing operation to the likely GitHub fine-grained token permission or GPT Action layer and give me the smallest verification step first.
```

## Next chapter

Continue to [Chapter 10 — Daily use and safe operating habits]({{ '/docs/high-director/build-your-own/10-daily-operation/' | relative_url }}).
