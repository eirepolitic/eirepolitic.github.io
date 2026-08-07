---
title: High Director Runtime Architecture
summary: Verified runtime architecture for the High Director GPT, GitHub wrapper Action, AWS Lambda implementation, Google Workspace Action, trust boundaries, and documentation control plane.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 24
permalink: /projects/high-director/runtime-architecture/
---

# High Director Runtime Architecture

## Purpose

This page is the canonical architecture record for the verified High Director runtime. It describes only components and boundaries supported by repository evidence, user-supplied authoritative configuration/source, or directly observed operation.

## Architecture summary

High Director consists of a configured ChatGPT GPT plus two custom Actions:

1. a GitHub wrapper Action hosted by an AWS Lambda Function URL;
2. a Google Workspace Action that calls Google Calendar and Gmail APIs using OAuth.

The documentation site in `eirepolitic.github.io` is a separate control/documentation component. It records the implementation but is not part of the runtime request path for ordinary High Director tasks.

## Verified component diagram

```text
User
  |
  v
High Director GPT
  |\
  | \
  |  \---- OAuth ----> Google Workspace APIs
  |                   |-- Google Calendar API
  |                   `-- Gmail API
  |
  `---- X-API-Key ----> Public AWS Lambda Function URL
                         |
                         v
                    FastAPI + Mangum
                    github-gpt-wrapper
                    src/app.py v0.3.0
                         |
                         | Bearer GITHUB_TOKEN
                         v
                    GitHub REST API
                         |
                         v
                    GitHub repositories,
                    pull requests,
                    workflows,
                    variables/secrets
```

## High Director GPT

Authoritative GPT configuration verifies:

- name: `High Director`;
- description: `Concise assistant for data pipelines and cloud build work.`;
- recommended model setting: `Thinking 5.6`;
- no visible/configured Knowledge files in the supplied configuration;
- two configured Actions;
- user-authored Instructions defining concise technical assistance, planning/confirmation behavior, repository-addressing rules, and failure-handling rules.

The ChatGPT platform's internal model execution, tool-routing internals, token storage, and hidden platform services are outside the directly inspectable implementation and remain platform-managed/unverified.

## GitHub Action architecture

### GPT Action contract

The configured GitHub Action uses:

- OpenAPI `3.1.0`;
- title `GitHub GPT Wrapper`;
- schema/API version `0.2.1`;
- 28 exposed Action operations;
- API-key authentication via HTTP header `X-API-Key`;
- a private AWS Lambda Function URL server hostname, intentionally omitted from public documentation.

### AWS transport boundary

Live AWS configuration verifies:

- public Lambda Function URL;
- AWS Function URL auth type `NONE`;
- invoke mode `BUFFERED`;
- CORS not enabled;
- region `us-east-2`;
- runtime Python 3.13;
- architecture `x86_64`;
- handler `src.app.handler`.

Because AWS auth type is `NONE`, AWS IAM does not authenticate the incoming Action request at the Function URL layer. The effective application request gate is the `X-API-Key` comparison performed inside `src/app.py` against the `APP_API_KEY` environment variable.

### Lambda application

The supplied source package verifies:

- application name `github-gpt-wrapper`;
- application version `0.3.0`;
- FastAPI application adapted to Lambda by Mangum;
- 31 application routes including `/health`;
- GitHub REST API base `https://api.github.com`;
- structured success/error responses;
- GitHub timeout/transport/error handling;
- repository-name normalization and single-owner enforcement;
- file/branch/PR/workflow/variable/secret functionality.

### GitHub authentication boundary

The Lambda application sends GitHub requests using:

```text
Authorization: Bearer <GITHUB_TOKEN>
```

The live Lambda environment confirms a `GITHUB_TOKEN` variable exists. The source/deployment documentation identifies it as a fine-grained GitHub personal access token.

The exact token value, granted repository set, permissions, storage lifecycle, and rotation process are intentionally not documented because they are secret or remain unverified.

### GitHub owner boundary

The Lambda application uses a backend `GITHUB_OWNER` environment variable and constructs GitHub REST paths with that owner. It rejects a `repo` argument containing `/`.

Therefore the GPT must supply repository name only, for example:

```text
eirepolitic.github.io
```

and must not pass `owner/repo`.

### Lambda execution role

Live AWS/IAM evidence verifies execution role:

```text
github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo
```

The supplied role view shows attached managed policy:

```text
AWSLambdaBasicExecutionRole
```

The supplied trust policy allows:

```text
Principal: lambda.amazonaws.com
Action: sts:AssumeRole
```

GitHub authorization itself is application-level through `GITHUB_TOKEN`, not through AWS IAM.

## Google Workspace Action architecture

### Action contract

The configured Google Action uses:

- OpenAPI `3.1.0`;
- title `Google Workspace API`;
- API version `1.2.0`;
- 12 operations total;
- primary Calendar server `https://www.googleapis.com`;
- Gmail server overrides to `https://gmail.googleapis.com`;
- OAuth authentication selected in GPT Builder.

### OAuth boundary

Verified authorization endpoint:

```text
https://accounts.google.com/o/oauth2/v2/auth
```

Verified token endpoint:

```text
https://oauth2.googleapis.com/token
```

Token exchange method: default POST request.

Configured scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

The OAuth Client ID and Client Secret exist in GPT Builder but were hidden and are not published. Token storage/refresh inside the ChatGPT platform is platform-managed and not directly verified.

### Calendar boundary

The Action can:

- list calendars;
- list/search events;
- create events;
- retrieve events;
- update events;
- delete events;
- move events between calendars.

The schema embeds explicit confirmation requirements for create/update/delete/move operations.

### Gmail boundary

The Action can:

- retrieve Gmail profile/mailbox totals;
- search/list message IDs;
- retrieve message content and metadata;
- retrieve attachments;
- send email.

The schema requires the assistant to display To, Cc, Bcc, Subject, and body and obtain explicit confirmation immediately before sending.

## Documentation/control plane

The `eirepolitic.github.io` repository is the persistent technical source of truth for documented High Director implementation.

Its publication flow is:

```text
focused branch
  -> pull request
  -> Validate documentation workflow
  -> merge to main
  -> GitHub Pages build/deployment
  -> confirm deployment success
```

This control plane does not mediate normal GitHub Action or Google Workspace Action requests. It governs documentation change management only.

## Trust boundaries

### Boundary 1 — User to High Director GPT

The user supplies task intent and confirmations. GPT behavior is constrained by the configured Instructions plus platform-level policies/tool semantics.

### Boundary 2 — GPT to GitHub wrapper

Trust mechanism: `X-API-Key`.

The destination Function URL is public at the network layer (`AuthType: NONE`), so secrecy of the URL is not the primary authentication control. Application-level API-key validation is the verified access control.

### Boundary 3 — Lambda wrapper to GitHub

Trust mechanism: Bearer `GITHUB_TOKEN` sent to GitHub REST API.

Repository scope is constrained by the backend owner plus the token's actual repository permissions.

### Boundary 4 — Lambda execution to AWS

Trust mechanism: Lambda execution role assumed by `lambda.amazonaws.com`.

Visible role permission evidence is `AWSLambdaBasicExecutionRole`. Additional permissions are not claimed without source.

### Boundary 5 — GPT to Google Workspace

Trust mechanism: OAuth authorization against Google using the four configured scopes.

The Google account identity and platform token-management implementation remain private/unverified.

## Data classifications crossing boundaries

### GitHub path

Potential data includes:

- repository paths and file contents;
- branch names and commit messages;
- pull-request titles/bodies/status;
- workflow identifiers, jobs, logs, and artifact metadata;
- Actions variable values when explicitly written;
- secret plaintext transiently when `setSecret` is called.

The wrapper encrypts GitHub Actions secret plaintext using the repository's GitHub public key before transmitting the encrypted value to GitHub. The secret value is not returned by the wrapper.

### Google path

Potential data includes:

- authenticated Gmail address/profile metadata;
- message metadata, bodies, raw MIME content, and attachments;
- calendar IDs and event details;
- attendee/organizer email addresses;
- locations, recurrence, reminders, and meeting links;
- outbound email contents;
- calendar mutation details.

These data are user/account data and must not be copied into public documentation unless sanitized and technically necessary.

## Architecture drift and constraints

Verified drift exists between:

- Lambda application `0.3.0`;
- configured GitHub Action schema `0.2.1`;
- bundled source-package OpenAPI `0.2.0`.

The Lambda implements routes not exposed by the current GPT schema: health, branch deletion, and artifact metadata.

The current GPT schema is the canonical callable Action surface; the Lambda source is canonical for backend implementation.

## Known architectural limitations

- capability toggles in GPT Builder remain unverified;
- internal ChatGPT platform routing/token persistence is not inspectable here;
- GitHub PAT permissions/rotation are not yet verified;
- Lambda live memory/timeout are not confirmed from the console, although the SAM template declares 512 MB / 30 seconds;
- full Function URL resource-policy details are unverified;
- CloudWatch/log retention/alarms/monitoring are unverified;
- Google connected-account identity, token lifecycle, consent-screen configuration, and admin controls are unverified;
- no API Gateway component is established for the GitHub path; verified evidence points directly to a Lambda Function URL.

## Verification record

Verified on 2026-08-06 from:

- authoritative GPT configuration/instructions;
- current GitHub Action OpenAPI schema;
- GitHub wrapper Lambda source/deployment package;
- live Lambda/IAM configuration;
- Google Workspace Action OpenAPI schema;
- Google OAuth configuration;
- directly observed GitHub integration behavior;
- repository workflow/deployment evidence.

## Related Documents

- [High Director GPT Configuration]({{ '/projects/high-director/gpt-configuration/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }})
- [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }})
- [High Director GitHub Wrapper Live AWS Configuration]({{ '/projects/high-director/github-wrapper-live-aws-configuration/' | relative_url }})
- [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
