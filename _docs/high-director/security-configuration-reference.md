---
title: High Director Security and Configuration Reference
summary: Verified authentication, authorization, secret, IAM, OAuth, runtime configuration, trust-boundary, AWS operator, and security-limitation reference for High Director.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-09-26
last_verified: 2026-09-26
owner: High Director
order: 26
permalink: /projects/high-director/security-configuration-reference/
---

# High Director Security and Configuration Reference
## Purpose

This page is the canonical security/configuration reference for the verified High Director implementation. It records controls that are directly supported by authoritative configuration/source or observable runtime evidence and leaves unresolved areas explicitly unverified.

## Security model summary

High Director now has three distinct external trust paths:

1. **GitHub path** — GPT Action -> public AWS Lambda Function URL -> FastAPI wrapper -> GitHub REST API.
2. **Google Workspace path** — GPT Action -> Google OAuth -> Google Calendar/Gmail APIs.
3. **AWS operator path** — GPT GitHub Action -> GitHub Actions workflow -> dedicated AWS IAM user -> `sts:AssumeRole` -> `HighDirectorAwsAdmin` -> AWS APIs using temporary STS credentials.

The original GPT Builder configuration still contains only the GitHub and Google Workspace Actions. The AWS operator path is a later runtime extension implemented through GitHub Actions and must not be described as a third Builder Action.

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

## GitHub wrapper Lambda configuration reference

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

## GitHub wrapper Lambda execution role / IAM

Verified live role name:

```text
github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo
```

Visible attached managed policy:

```text
AWSLambdaBasicExecutionRole
```

Verified trust relationship permits `lambda.amazonaws.com` to call `sts:AssumeRole`.

The supplied evidence does not prove that no additional/inline policies exist. Do not state absence without a complete authoritative role-policy inventory.

## AWS operator authentication and authorization

The broad AWS operator extension is implemented independently of the GitHub wrapper Lambda execution role.

Verified runtime path:

```text
High Director
  -> GitHub Action
  -> GitHub Actions workflow
  -> github-eirepolitic-instagram-deployer
  -> sts:AssumeRole
  -> HighDirectorAwsAdmin
  -> temporary STS credentials
  -> AWS APIs
```

The one-time bootstrap is defined in:

```text
Eirepolitic-data-pipeline/infra/publishing/github_aws_bootstrap.yml
```

The broad AWS operations workflow is implemented in:

```text
Eirepolitic-data-pipeline/.github/workflows/deploy_instagram_publisher_lambda.yml
```

### Dedicated bootstrap IAM user

The existing IAM user:

```text
github-eirepolitic-instagram-deployer
```

retains the long-lived access keys stored in GitHub repository secrets. Those secret values are not documented or exposed.

The bootstrap attaches permission allowing that user to call `sts:AssumeRole` on `HighDirectorAwsAdmin`.

### `HighDirectorAwsAdmin`

Verified role name:

```text
HighDirectorAwsAdmin
```

Verified policy attachment:

```text
arn:aws:iam::aws:policy/AdministratorAccess
```

The role trust policy permits the dedicated GitHub deployer user to assume it.

The default configured maximum/session duration used by the workflow is one hour.

### Temporary credential handling

The GitHub Actions workflow:

1. loads the dedicated bootstrap IAM user's repository secrets;
2. calls `aws sts assume-role`;
3. receives an access key ID, secret access key, and session token;
4. masks all returned credential values in GitHub Actions output;
5. writes the temporary credentials into the current job environment;
6. verifies the caller identity;
7. performs the selected AWS operation under the assumed administrator role.

The temporary STS values must never be printed or published.

### Programmatic operation selection

The workflow supports the repository Actions variable:

```text
HIGH_DIRECTOR_AWS_OPERATION
```

This compensates for the current GitHub dispatch integration not accepting workflow input values directly.

When no explicit manual workflow input is present, the workflow uses the repository variable and otherwise falls back to:

```text
infrastructure-status
```

The resting value should remain a non-mutating operation when no change is intended.

### Verified AWS runtime behavior

On 2026-09-26, High Director successfully exercised the AWS operator path for:

- role assumption and caller-identity verification;
- CloudFormation creation of the Instagram publication ledger;
- CloudFormation creation of EventBridge Scheduler/SQS/IAM/CloudWatch support resources;
- read-only invocation of the Instagram publisher Lambda healthcheck;
- infrastructure status inspection.

These runs verify the AWS operator trust path end-to-end.

## AWS operator risk boundary

`AdministratorAccess` intentionally gives the assumed role broad AWS authority, including sensitive services such as IAM and Secrets Manager.

This materially increases the blast radius of a compromised GitHub workflow, repository credential, or repository governance path.

Primary controls are therefore:

- protection and periodic rotation of the dedicated long-lived deployer access keys;
- separation between bootstrap IAM user credentials and temporary administrator sessions;
- repository access and branch/review controls;
- GitHub workflow audit history;
- explicit project-level approval gates for sensitive production actions;
- account/organization-level AWS controls where configured.

Project approval gates remain binding even when IAM would technically allow the action. For example, the Instagram publishing project still requires explicit approval before the first visible `/media_publish` call and separate approval before general production scheduling.

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
- AWS account IDs or long-lived/temporary AWS credentials;
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
3. current application/workflow source for backend behavior;
4. deployment/bootstrap template for declared infrastructure intent;
5. README/starter guidance for historical/operator guidance only.

Known examples:

- GitHub wrapper Lambda application is `0.3.0`, current GPT Action schema is `0.2.1`, and bundled OpenAPI is `0.2.0`;
- the GPT Builder record still has two configured Actions, while the later AWS operator capability is implemented through GitHub Actions and therefore belongs to runtime architecture rather than Builder configuration.

## Known security limitations

- public GitHub-wrapper Function URL uses AWS auth `NONE`;
- API-key lifecycle/rotation is not documented;
- exact GitHub fine-grained PAT permissions and rotation are not verified;
- live GitHub-wrapper Lambda memory/timeout are not separately verified;
- full Function URL resource policy is unverified;
- complete GitHub-wrapper execution-role policy inventory is unverified;
- CloudWatch retention, alarms, monitoring, WAF/rate limiting, and other perimeter controls are unverified unless separately documented;
- ChatGPT platform storage/refresh handling for Google OAuth tokens is unverified;
- Google OAuth consent-screen/project/admin controls are unverified;
- capability toggles in GPT Builder remain unverified;
- the AWS bootstrap still relies on long-lived IAM-user access keys before role assumption;
- organization-level AWS controls such as SCPs are not documented unless separately verified;
- `AdministratorAccess` is intentionally broad and relies heavily on repository/workflow governance and project approval gates.

## Safe configuration-change rule

Changes to authentication type, OAuth scopes, GitHub token permissions, Lambda Function URL auth, IAM policies, AWS administrator-role trust/policy attachment, secret handling, account access, or other security boundaries require an explicit architecture/security decision before implementation.

Documentation-only corrections that do not change those controls may proceed through the normal focused PR/validation/Pages process.

## Verification record

Verified on 2026-09-26 from authoritative GPT configuration, GitHub/Google Action schemas, GitHub wrapper Lambda source/deployment package, live AWS/IAM source, Google OAuth configuration, merged High Director AWS bootstrap/workflow source, and directly observed successful `sts:AssumeRole` and AWS infrastructure operations.

## Related Documents

- [High Director Runtime Architecture]({{ '/projects/high-director/runtime-architecture/' | relative_url }})
- [High Director Data Flows]({{ '/projects/high-director/data-flows/' | relative_url }})
- [High Director AWS Operator Capability]({{ '/docs/high-director/aws-operator-capability/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director GitHub Wrapper Live AWS Configuration]({{ '/projects/high-director/github-wrapper-live-aws-configuration/' | relative_url }})
- [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
