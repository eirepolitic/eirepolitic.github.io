---
title: Troubleshoot and Hand Off High Director
summary: Verified troubleshooting, recovery, evidence-capture, escalation, and continuation runbook for High Director and its GitHub/AWS/Google integrations.
section: runbooks
doc_type: runbook
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 61
permalink: /projects/runbooks/high-director-troubleshooting-and-handoff/
tags:
  - high-director
  - troubleshooting
  - handoff
  - recovery
---

# Troubleshoot and Hand Off High Director

## Purpose

Use this runbook to diagnose verified High Director failure modes, preserve useful evidence safely, avoid security shortcuts, and hand work to another capable agent/developer without relying on conversation history.

This runbook does not authorize architecture, security, cost, access-control, credential, OAuth-scope, IAM-policy, or irreversible changes. Stop for an explicit decision before making those changes.

## Source of Truth

Start from these canonical documents:

- `_docs/high-director/high-director-documentation-initiative-plan.md`
- `_docs/high-director/runtime-architecture.md`
- `_docs/high-director/data-flows.md`
- `_docs/high-director/security-configuration-reference.md`
- `_docs/high-director/github-integration.md`
- `_docs/high-director/github-action-openapi-schema.md`
- `_docs/high-director/github-wrapper-lambda.md`
- `_docs/high-director/github-wrapper-live-aws-configuration.md`
- `_docs/high-director/google-workspace-action.md`
- `_docs/runbooks/high-director-operations-and-deployment.md`

Where implementation sources disagree, use the hierarchy documented in the security/configuration reference: live configuration, then current Action schema, then application source, then deployment template, then README/starter guidance.

## Immediate Safety Rules

Before troubleshooting:

1. Do not paste or publish `APP_API_KEY`, `GITHUB_TOKEN`, OAuth Client Secret, access/refresh tokens, AWS credentials, private Function URL hostname, private email/calendar content, or GitHub Actions secret plaintext.
2. Do not weaken Function URL auth, IAM, OAuth scopes, GitHub token permissions, or repository protections as a diagnostic shortcut.
3. Stop write-capable operations if the failure could cause duplicate email/calendar changes, direct repository writes, unintended merges, workflow state changes, or secret mutation.
4. Preserve exact error status, operation ID, route, workflow/run ID, PR number, branch, commit SHA, and timestamp where safe.
5. Separate observed evidence from inference.

## Triage Order

Use this order to avoid chasing the wrong layer:

1. identify the failing user-visible operation;
2. identify which trust path is involved: GitHub/AWS or Google Workspace;
3. inspect the exact returned error/status first;
4. verify the current Action contract still contains the intended operation;
5. verify the relevant live configuration/source boundary;
6. retry only low-risk reads unless the user has confirmed a write;
7. capture evidence and stop if the next step requires credential, IAM, OAuth-scope, architecture, or access-control changes.

## GitHub Action Failures

### 401 unauthorized

Meaning: the Lambda application rejected the `X-API-Key` value.

Safe checks:

1. Confirm the GPT Action authentication type is API Key.
2. Confirm the header name remains `X-API-Key` in the current schema.
3. In AWS Lambda, confirm the environment-variable key `APP_API_KEY` exists without exposing its value.
4. Confirm the Function URL still targets the intended wrapper.
5. Do not paste or compare secret values in chat/documentation.

Escalation boundary: changing/rotating the API key is a security/credential operation and requires an explicit decision.

### 400 repo-name error

The backend deliberately rejects `owner/repo`.

Use repository name only, for example:

```text
eirepolitic.github.io
```

Do not ask for the owner name; owner is configured in `GITHUB_OWNER`.

### 404 not found

Check, in order:

1. repository name;
2. file/path/ref/branch/workflow/run/PR identifier;
3. whether the target exists in the configured single-owner GitHub scope;
4. whether the current Action operation/path matches the documented schema.

Do not assume authentication failure from a 404 without supporting evidence.

### 422 validation error

The wrapper/Pydantic/FastAPI rejected input structure.

Check the current Action schema for required fields, enums, types, and path/query/body placement. Preserve the returned validation details; do not reconstruct request fields from memory.

### 502 `github_transport_error`

The wrapper could not complete transport to GitHub.

Safe response:

1. stop risky writes;
2. preserve status/error details;
3. retry a low-risk read once if appropriate;
4. if persistent, inspect AWS/Lambda operational evidence when available.

Monitoring/logging configuration is not fully documented, so do not claim CloudWatch evidence exists until verified.

### 504 `github_timeout`

The wrapper timed out waiting for GitHub.

The application default request timeout is `30` seconds unless configured otherwise. Retry only a low-risk read. Do not increase timeout or change infrastructure without a design/cost decision.

### `github_error` with upstream GitHub status

Treat the upstream GitHub status/message as the immediate diagnostic. Do not guess that repository format, permissions, or token scope caused the failure unless the response supports it.

## GitHub Write-Safety Failures

### Preview/apply mismatch

Preview-before-write is an operating rule, not a server-enforced prerequisite.

If an apply call was made without the intended preview/approval:

1. stop further writes;
2. inspect branch/commit/PR state;
3. do not merge;
4. correct through a focused branch/PR if needed;
5. preserve the incident in documentation if it reveals a real runbook/control gap.

### Direct default-branch write risk

The Lambda application does not technically prevent an explicitly selected existing default branch from being used by apply endpoints.

If a direct write may have occurred:

1. stop further writes;
2. inspect the target branch and commit history;
3. do not rewrite history automatically;
4. use normal repository recovery/revert procedures through a reviewed PR where possible;
5. treat changes to server-side enforcement as an architecture/security decision.

### PR merge failure

Capture PR number, merge method, optional SHA, and returned GitHub error. Verify current PR state before retrying. Do not repeatedly retry merge when branch protection, conflicts, or required checks are unresolved.

### Workflow dispatch/enable/disable failure

Verify workflow ID/path and current workflow state. Dispatch only when explicitly requested. Enabling/disabling workflows is a write-capable control action; do not alter workflow state as a troubleshooting shortcut.

## AWS Lambda / Function URL Failures

Verified live baseline:

```text
Region: us-east-2
Runtime: Python 3.13
Handler: src.app.handler
Architecture: x86_64
Function URL auth: NONE
Invoke mode: BUFFERED
CORS: not enabled
```

Live environment-variable keys expected:

```text
APP_API_KEY
BRANCH_PREFIX
DEFAULT_BASE_BRANCH
GITHUB_OWNER
GITHUB_TOKEN
```

### Lambda fails to initialize

Source code raises at startup if `GITHUB_OWNER`, `GITHUB_TOKEN`, or `APP_API_KEY` is missing.

Safe check: verify those variable names exist in the Lambda configuration. Do not reveal values.

### Function URL unreachable or wrong endpoint

Verify the live Function URL entry in AWS and the GPT Action server target. Do not publish the hostname. Changing Function URL auth/resource policy is a security/architecture change.

### Runtime/handler drift

Compare live AWS settings with:

```text
Runtime: Python 3.13
Handler: src.app.handler
```

If they differ, record the drift first. Do not silently change live configuration or documentation until authoritative intended state is established.

### IAM/execution-role issue

Verified role:

```text
github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo
```

Verified visible managed policy:

```text
AWSLambdaBasicExecutionRole
```

Verified trust principal:

```text
lambda.amazonaws.com
```

The evidence does not prove no additional policies exist. Do not remove/add policies or change trust relationships without an explicit security decision.

## GitHub Secret-Write Failures

The wrapper uses GitHub's Actions public key plus PyNaCl `SealedBox` before sending encrypted secret material.

If `setSecret` fails:

1. never request/read back an existing secret value;
2. capture only status/error metadata;
3. verify the target repository/name and GitHub API response;
4. do not log or publish supplied plaintext;
5. stop if remediation requires token-permission expansion or credential changes.

## Google Workspace Failures

Verified OAuth scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

Verified OAuth endpoints:

```text
Authorization: https://accounts.google.com/o/oauth2/v2/auth
Token:         https://oauth2.googleapis.com/token
Token exchange: default POST request
```

### Authentication/authorization failure

Do not expose Client ID/Secret or tokens. Confirm only the non-secret OAuth endpoints/scopes and that the GPT Action authentication type is OAuth.

Reconnect/revocation behavior is not fully verified. Do not invent a reconnect procedure or change scopes without authoritative configuration and explicit approval.

### Gmail read/search failure

Confirm the requested operation is one of:

- `getGmailProfile`
- `searchGmailMessages`
- `getGmailMessage`
- `getGmailAttachment`

Preserve Google API error/status. Do not publish message bodies, attachments, authenticated email address, or account-specific identifiers while troubleshooting.

### Email send failure

`sendGmailMessage` requires explicit confirmation immediately before sending after showing To, Cc, Bcc, Subject, and body.

If send state is uncertain:

1. do not immediately resend;
2. inspect safe evidence first (for example, returned error and later mailbox state if the user asks/authorizes inspection);
3. avoid duplicate sends;
4. preserve message/thread IDs only when technically necessary and safe.

### Calendar create/update/delete/move failure

All write-sensitive calendar operations require confirmation according to the Action descriptions.

If outcome is uncertain:

1. do not repeat the mutation blindly;
2. retrieve/list the relevant event when appropriate;
3. compare current event state with the intended change;
4. retry only after confirming it will not duplicate or compound the mutation.

## Documentation Pipeline Failures

### Validation fails

Do not merge. Inspect `Validate documentation` run/job/step, correct the documentation defect, rerun validation, and merge only after success.

### Pages deployment fails

Do not start the next major documentation step. Confirm the Pages run matches the merged commit SHA, inspect build/deploy job failure, and correct through a focused PR if repository changes are required.

### Persistent plan is stale

Treat `_docs/high-director/high-director-documentation-initiative-plan.md` as the authoritative continuation record. Update it through a focused PR after meaningful initiative progress.

## Evidence Capture Checklist

For a handoff or unresolved incident, record only safe metadata:

- date/time;
- affected component;
- operation ID/action name;
- repository name only (not owner/repo for this integration);
- branch/PR/workflow/run IDs and commit SHA where relevant;
- HTTP/error status and sanitized message;
- expected vs observed behavior;
- last known successful verification/deployment;
- exact authoritative document/source consulted;
- actions already attempted;
- unresolved question;
- next safe action;
- whether a security/architecture/access-control decision is required.

Never include secret values or private user data.

## Handoff Procedure

A capable replacement agent/developer should proceed in this order:

1. Read `_docs/high-director/high-director-documentation-initiative-plan.md`.
2. Read the canonical page for the component being changed/troubleshot.
3. Check the latest merged PR and matching successful Pages deployment before assuming documented work is live.
4. Preserve evidence classification: verified implementation, user-supplied authoritative source, observable runtime evidence, inference, historical behavior, planned work, unknown/unverified.
5. Do not rely on conversation history when the documentation repository contains the source of truth.
6. Request external source only when a concrete evidence gap blocks safe continuation; request one coherent source at a time.
7. Sanitize supplied material before publication.
8. Use a small focused branch/PR.
9. Run documentation validation before merge.
10. Confirm the resulting Pages deployment before the next major step.

## Recovery Boundaries

The following recovery procedures remain unverified or incomplete and must not be invented:

- automated Lambda rollback/version/alias recovery;
- CloudWatch alarm/log-retention based incident response;
- GitHub PAT rotation/recovery procedure;
- `APP_API_KEY` rotation procedure;
- Google OAuth reconnect/revocation procedure;
- complete Lambda Function URL resource-policy recovery;
- complete IAM policy inventory/recovery.

If one of these blocks work, request the relevant authoritative configuration/process from the user rather than guessing.

## Known Monitoring Gaps

Current documentation does not verify:

- CloudWatch log retention;
- CloudWatch alarms/metrics dashboards;
- WAF or rate limiting;
- Lambda dead-letter/retry configuration;
- reserved concurrency;
- GitHub token lifecycle monitoring;
- Google OAuth audit/revocation monitoring.

Do not describe these controls as present unless later authoritative evidence verifies them.

## Completion Criteria

A troubleshooting/handoff cycle is complete when:

- the observed issue is resolved or explicitly bounded as unresolved;
- no secret/private data was published;
- any security/architecture decision is recorded before implementation;
- canonical documentation reflects verified findings if behavior/configuration changed;
- documentation validation passes;
- documentation PR merges;
- matching Pages deployment succeeds;
- the persistent initiative plan is synchronized.

## Related Documents

- [Operate and Update High Director]({{ '/projects/runbooks/high-director-operations-and-deployment/' | relative_url }})
- [High Director Security and Configuration Reference]({{ '/projects/high-director/security-configuration-reference/' | relative_url }})
- [High Director Runtime Architecture]({{ '/projects/high-director/runtime-architecture/' | relative_url }})
- [High Director Data Flows]({{ '/projects/high-director/data-flows/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }})
- [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})

## Verification Record

- Last verified: `2026-08-06`
- Verified against: authoritative High Director configuration/source documents and observed GitHub documentation workflows
- Verification scope: known failure modes, safe evidence collection, recovery boundaries, and continuation procedure
- Known unverified recovery areas: credential rotation, Lambda rollback/versioning, Google OAuth reconnect/revocation, monitoring/alerting controls
