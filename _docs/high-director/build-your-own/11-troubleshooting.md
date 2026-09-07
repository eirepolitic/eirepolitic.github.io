---
title: Build Your Own High Director 11 — Troubleshooting
summary: Beginner troubleshooting for separating ChatGPT, Action, Lambda, GitHub, and permission failures without exposing credentials or changing architecture at random.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 71
permalink: /docs/high-director/build-your-own/11-troubleshooting/
---

# Chapter 11 — Troubleshooting

## Goal

When something fails, identify **which layer failed** before changing anything.

The system has several independent layers:

```text
1. ChatGPT / GPT editor
2. GPT Action schema and Action authentication
3. AWS Lambda Function URL
4. Lambda application configuration
5. GitHub authentication and permissions
6. The specific repository/file/branch/PR/workflow being requested
```

Changing all of them at once usually makes troubleshooting harder.

## First rule — preserve the exact error

Before clicking around, copy the exact non-secret error message into a private note.

Useful evidence includes:

- HTTP status such as `400`, `401`, `403`, `404`, `422`, `502`, or `504`;
- operation name such as `getFile` or `mergePullRequest`;
- repository name;
- file path;
- branch name;
- pull-request number;
- workflow/run/job identifier;
- approximate time of failure.

Never include:

- `APP_API_KEY`;
- `GITHUB_TOKEN`;
- AWS passwords or access keys;
- real GitHub Actions secret plaintext;
- OAuth client secrets or tokens;
- payment details.

## Fast layer test

Ask yourself these questions in order.

### Can the Lambda health endpoint be reached?

Use the Chapter 6 health test.

- **No:** focus on AWS Lambda/Function URL/runtime/handler.
- **Yes:** continue.

### Can CloudShell read `director-test.txt` through the protected Lambda endpoint with the real APP_API_KEY?

- **No:** the problem is below ChatGPT. Focus on Lambda environment variables, APP_API_KEY, GitHub token, owner, repository, or GitHub permissions.
- **Yes:** continue.

### Does the same operation fail only when called from the GPT?

- **Yes:** focus on GPT Action authentication, schema, server URL, workspace domain policy, or Action-compatible model support.
- **No:** continue using the exact backend/GitHub error.

## Error reference

### `401 unauthorized` from the Lambda wrapper

Meaning: the wrapper rejected the `X-API-Key` value.

Check:

1. GPT Action authentication type is **API Key**.
2. Authentication style is **Custom header**.
3. Header name is exactly `X-API-Key`.
4. Lambda has an environment variable named `APP_API_KEY`.
5. The Action points to the intended Lambda Function URL.

Do **not** change the GitHub token to fix this error. The request has not successfully passed the wrapper's own authentication layer.

### GitHub `401`

Meaning: GitHub rejected the GitHub credential.

Check:

1. the `GITHUB_TOKEN` Lambda environment variable exists;
2. the fine-grained token has not expired or been revoked;
3. the token belongs to the intended resource owner;
4. you did not accidentally paste the `APP_API_KEY` into `GITHUB_TOKEN`.

### GitHub `403`

Meaning: GitHub understood the credential but refused the requested operation, or another GitHub policy/rate-limit condition applies.

Use the returned GitHub message. For permission-specific failures, map the operation to the permission:

| Operation type | Permission to check |
|---|---|
| File/branch create/update/delete | Contents; Workflows too when changing workflow files |
| Pull requests | Pull requests |
| Workflow/run controls | Actions / Workflows as required by the endpoint |
| Repository Actions variables | Variables |
| Repository Actions secrets | Secrets |

Do not simply turn every GitHub permission on.

### `404 not_found`

Check in this order:

1. repository name exists;
2. caller used repository name only, not `owner/repo`;
3. path/branch/PR/workflow/run exists;
4. `GITHUB_OWNER` is correct;
5. token repository access includes the repository;
6. the upstream GitHub response is not deliberately returning 404 because the credential cannot see the resource.

Do not assume every 404 is a bad token.

### `400` repository-name error

The wrapper deliberately rejects repository values containing `/`.

Use:

```text
director-test
```

not:

```text
username/director-test
```

### `422 validation_error`

The request structure did not match what the FastAPI/Pydantic model expected.

Check the OpenAPI schema for:

- required fields;
- exact field names;
- integer vs string values;
- allowed enum values;
- whether the value belongs in the path, query string, or request body.

Do not modify Lambda code first for a schema/request-shape failure.

### `502 github_transport_error`

The wrapper could not complete transport to GitHub.

1. retry a harmless read once;
2. if it persists, inspect Lambda logs if available;
3. check GitHub service status separately;
4. do not repeat a write operation while the result is uncertain.

### `504 github_timeout`

The wrapper timed out waiting for GitHub. The application default request timeout is 30 seconds unless overridden.

Retry a harmless read once. Do not increase timeouts or change infrastructure merely because one request timed out.

### Lambda import/module error

Check:

```text
Runtime = Python 3.13
Architecture = x86_64
Handler = src.app.handler
ZIP contains src/app.py
Dependencies are in ZIP root
```

If these are correct, preserve the exact module/import error before rebuilding the package.

### Lambda initialization failure

The wrapper refuses to initialize when any of these required values is missing:

```text
GITHUB_OWNER
GITHUB_TOKEN
APP_API_KEY
```

In Lambda:

1. open **Configuration**;
2. open **Environment variables**;
3. confirm those key names exist;
4. do not reveal their values in screenshots.

### GPT schema validation error

The initial build should use the authoritative OpenAPI v0.2.1 schema and change only the server URL.

Compare with [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }}).

Do not delete operations until the validator stops complaining. Identify the exact schema line/validation message instead.

### "No domains are allowed by your workspace's settings"

This is a ChatGPT workspace policy issue.

Do not rebuild Lambda or regenerate GitHub credentials.

If you are an authorized workspace administrator, review the current GPT Action domain settings. Otherwise contact the administrator who controls that workspace.

### Reads work, writes fail

This usually means the overall network/authentication path works.

Check the permission required by the write operation rather than changing Function URL settings.

### A write may have happened but ChatGPT says it failed

Do not immediately repeat the write.

Check GitHub directly:

- branch list;
- commit history;
- pull requests;
- Actions variable/secret name;
- workflow state.

Determine the actual current state before trying again.

## Finding Lambda logs

The basic Lambda execution role includes CloudWatch Logs permissions. If Lambda has produced logs and your AWS identity can read them:

1. open the Lambda function;
2. open **Monitor**;
3. choose the option to view logs in CloudWatch;
4. find entries near the failure time;
5. copy only the relevant error text;
6. remove account identifiers, tokens, API keys, and private request data before sharing it elsewhere.

Do not assume a CloudWatch alarm or custom dashboard exists. The baseline implementation does not establish those monitoring controls.

## The standard troubleshooting prompt

Use this with a normal ChatGPT session when you do not have access to this High Director instance:

```text
I am troubleshooting a browser-only custom GPT integration with this architecture:

Custom GPT → GPT Action → AWS Lambda Function URL → FastAPI/Mangum wrapper → GitHub REST API.

Known baseline:
- AWS region: us-east-2
- Lambda runtime: Python 3.13
- architecture: x86_64
- handler: src.app.handler
- Function URL auth: NONE
- application auth header: X-API-Key
- GitHub owner is stored in Lambda
- GPT sends repository name only
- GitHub credential is a fine-grained PAT

Operation that failed: [operation]
Earlier checkpoint that definitely passed: [checkpoint]
HTTP status: [status]
Exact sanitized error: [error]
Expected result: [expected]
Observed result: [observed]

Do not ask for API keys, personal access tokens, AWS credentials, secret values, account payment information, or OAuth secrets. First identify which layer the evidence points to. Then give me the smallest verification step. Do not suggest architecture, IAM, authentication, or broad permission changes unless the evidence specifically requires them.
```

## Screenshot rule

Before uploading a screenshot to ordinary ChatGPT or another support channel, inspect it for:

- Function URL;
- token values;
- API-key values;
- environment-variable values;
- AWS account identifiers;
- private repository content;
- personal email addresses;
- secret names that reveal sensitive infrastructure.

Crop or redact anything unnecessary.

## When to stop troubleshooting

Stop and seek a deliberate design/security decision if the proposed fix requires:

- changing Function URL authentication architecture;
- making AWS IAM permissions broader;
- making the GitHub token broader than the intended capabilities;
- disabling security controls;
- publishing a private credential;
- deleting/recreating infrastructure when the failure has not been diagnosed;
- changing multiple independent layers at once.

## Related detailed runbook

For deeper technical triage, see [Troubleshoot and Hand Off High Director]({{ '/projects/runbooks/high-director-troubleshooting-and-handoff/' | relative_url }}).

## What you should see

A useful troubleshooting session should end with a statement such as:

```text
The Lambda health check passes.
The protected CloudShell file-read check passes.
The GPT Action receives 401.
Therefore the problem is in GPT Action authentication rather than GitHub.
```

That is better than a long list of unrelated changes.

## Next chapter

Continue to [Chapter 12 — Maintenance and credential rotation]({{ '/docs/high-director/build-your-own/12-maintenance/' | relative_url }}).
