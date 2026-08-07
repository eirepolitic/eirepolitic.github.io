---
title: High Director Security and Configuration Reference
summary: Verified authentication, authorization, secret, IAM, OAuth, runtime configuration, trust-boundary, and security-limitation reference for High Director.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 26
permalink: /projects/high-director/security-configuration-reference/
---

# High Director Security and Configuration Reference

## Purpose

This page is the canonical security/configuration reference for the verified High Director implementation. It records controls that are directly supported by authoritative configuration/source or observable runtime evidence and leaves unresolved areas explicitly unverified.

## Security model summary

High Director currently has two distinct external trust paths:

1. **GitHub path** — GPT Action -> public AWS Lambda Function URL -> FastAPI wrapper -> GitHub REST API.
2. **Google Workspace path** — GPT Action -> Google OAuth -> Google Calendar/Gmail APIs.

The two paths use separate authentication models and should not be conflated.

## GitHub path authentication

### GPT -> Lambda wrapper

Verified control:

```text
X-API-Key
```

The current GitHub Action OpenAPI schema declares `ApiKeyAuth` in the `X-API-Key` request header.

The Lambda application compares that header against the `APP_API_KEY` environment variable. Missing/invalid values return `401 unauthorized`.

### AWS Function URL layer

Live AWS configuration verifies:

```text
Auth type: NONE
Invoke mode: BUFFERED
CORS: not enabled
```

The Function URL is therefore publicly reachable at the network layer for anyone who knows the URL. AWS IAM authentication is not the request gate; application-level API-key validation is the verified access control.

The Function URL hostname is infrastructure-sensitive and intentionally not published.

### Lambda -> GitHub

The wrapper sends:

```text
Authorization: Bearer <GITHUB_TOKEN>
```

The live Lambda environment contains the `GITHUB_TOKEN` key. Source/deployment documentation identifies this as a fine-grained GitHub personal access token.

The token value, exact repository access, granted permissions, storage lifecycle, and rotation process are not published and remain partly unverified.

## GitHub owner/repository boundary

The backend stores the owner in `GITHUB_OWNER`.

The application rejects any `repo` argument containing `/` and inserts the backend owner into GitHub REST paths. High Director must therefore pass repository name only.

This prevents callers from selecting an arbitrary owner through the Action `repo` parameter, but actual accessible repositories also depend on the GitHub token's granted scope.

## GitHub write-capability boundary

The Action contract exposes write-capable operations including:

- file create/update/delete;
- branch creation;
- pull-request create/update/close/merge;
- workflow dispatch/enable/disable;
- Actions variable create/update/delete;
- Actions secret create/update/delete.

These are materially privileged operations. Agent operating rules, explicit user confirmation where required, focused PR discipline, repository protections, and GitHub token permissions are separate layers of control.

The Lambda application does **not** enforce preview-before-write or prevent an explicitly selected existing default branch from being used by file apply endpoints. Therefore those safeguards cannot be described as application-enforced controls.

## GitHub secret handling

`setSecret` accepts plaintext in the Action request body.

Verified implementation:

1. plaintext enters the Lambda request/process;
2. wrapper retrieves the repository Actions public key from GitHub;
3. plaintext is encrypted with PyNaCl `SealedBox`;
4. wrapper sends encrypted value plus key ID to GitHub;
5. plaintext is not returned by the API.

Security implication: secret plaintext exists transiently before encryption and must never be logged or copied into public documentation.

## Lambda configuration reference

### Live verified settings

| Setting | Value |
|---|---|
| Region | `us-east-2` |
| Runtime | Python 3.13 |
| Handler | `src.app.handler` |
| Architecture | `x86_64` |
| Runtime update mode | `Auto` |
| Function URL auth | `NONE` |
| Invoke mode | `BUFFERED` |
| CORS | Not enabled |

### SAM-declared settings

| Setting | Declared value |
|---|---|
| Memory | `512 MB` |
| Timeout | `30 seconds` |
| Function URL auth | `NONE` |
| Invoke mode | `BUFFERED` |

Live memory/timeout were not separately verified in the console.

### Environment-variable contract

Live keys:

```text
APP_API_KEY
BRANCH_PREFIX
DEFAULT_BASE_BRANCH
GITHUB_OWNER
GITHUB_TOKEN
```

Source-supported optional/defaulted keys:

```text
GITHUB_API_VERSION=2022-11-28
REQUEST_TIMEOUT=30
```

Values must not be published.

## Lambda execution role / IAM

Verified live role name:

```text
github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo
```

Visible attached managed policy:

```text
AWSLambdaBasicExecutionRole
```

Verified trust relationship:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

The supplied evidence does not prove that no additional/inline policies exist. Do not state absence without a complete authoritative role-policy inventory.

## Google Workspace authentication

The Google Workspace Action uses OAuth.

Verified endpoints:

```text
Authorization URL: https://accounts.google.com/o/oauth2/v2/auth
Token URL:         https://oauth2.googleapis.com/token
Token exchange:    default POST request
```

Configured scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

These scopes establish the configured permission boundary for Calendar event management, read-only calendar-list access, Gmail read access, and Gmail send capability.

OAuth Client ID/Secret, access tokens, refresh tokens, authorization codes, and connected-account identity are private and are not published.

## Google Workspace mutation controls

The Action schema embeds confirmation rules for sensitive writes:

- create calendar event only after confirming calendar, title, date, time, guests, and notification behavior;
- update event only after obtaining confirmation;
- delete event only after explicit confirmation;
- move event only after explicit confirmation;
- send email only after showing To, Cc, Bcc, Subject, and body and obtaining explicit confirmation immediately before send.

These are Action-description behavioral controls, not independently enforced server-side transaction guards.

## Sensitive data classes

Do not publish unsanitized:

- `APP_API_KEY` values;
- `GITHUB_TOKEN` values;
- OAuth Client ID/Secret where treated as confidential implementation identifiers;
- OAuth access/refresh tokens or authorization codes;
- AWS account IDs or credentials;
- private Lambda Function URL hostname;
- personal email/account identifiers unless technically necessary and explicitly safe;
- Gmail message bodies, raw MIME data, or attachments;
- private calendar/event/attendee details;
- GitHub Actions secret plaintext;
- private repository content.

## Configuration/source-of-truth hierarchy

Where documents disagree, use this order:

1. live authoritative configuration for deployed settings;
2. current authoritative Action schema for callable GPT operation surface;
3. current application source for backend behavior;
4. deployment template for declared infrastructure intent;
5. README/starter guidance for historical/operator guidance only.

Known example: Lambda application is `0.3.0`, current GPT Action schema is `0.2.1`, and bundled OpenAPI is `0.2.0`. The current GPT schema remains canonical for what the GPT can call; source remains canonical for backend behavior.

## Known security limitations

- public Function URL uses AWS auth `NONE`;
- API-key lifecycle/rotation is not documented;
- exact GitHub fine-grained PAT permissions and rotation are not verified;
- live Lambda memory/timeout are not separately verified;
- full Function URL resource policy is unverified;
- complete execution-role policy inventory is unverified;
- CloudWatch retention, alarms, monitoring, WAF/rate limiting, and other perimeter controls are unverified;
- ChatGPT platform storage/refresh handling for Google OAuth tokens is unverified;
- Google OAuth consent-screen/project/admin controls are unverified;
- capability toggles in GPT Builder remain unverified.

## Safe configuration-change rule

Changes to authentication type, OAuth scopes, GitHub token permissions, Lambda Function URL auth, IAM policies, secret handling, account access, or other security boundaries require an explicit architecture/security decision before implementation.

Documentation-only corrections that do not change those controls may proceed through the normal focused PR/validation/Pages process.

## Verification record

Verified on 2026-08-06 from authoritative GPT configuration, GitHub/Google Action schemas, GitHub wrapper Lambda source/deployment package, live AWS/IAM screenshots and trust policy, Google OAuth configuration, and observed GitHub operations.

## Related Documents

- [High Director Runtime Architecture]({{ '/projects/high-director/runtime-architecture/' | relative_url }})
- [High Director Data Flows]({{ '/projects/high-director/data-flows/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director GitHub Wrapper Live AWS Configuration]({{ '/projects/high-director/github-wrapper-live-aws-configuration/' | relative_url }})
- [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
