---
title: Overlord Phase 3 — GitHub App and AWS Secrets Manager
summary: Third Phase 3 slice adding a control-plane GitHub App adapter backed by AWS Secrets Manager while preserving broker policy, exact-head checks, and durable audit evidence.
section: notes
doc_type: note
status: active
created: 2026-08-18
updated: 2026-08-18
last_verified: 2026-08-18
owner: High Director
order: 147
permalink: /projects/notes/overlord-phase-3-github-app-secrets-manager/
tags:
  - overlord
  - phase-3
  - github
  - github-app
  - aws
  - secrets-manager
---

# Overlord Phase 3 — GitHub App and AWS Secrets Manager

## Outcome

The third Phase 3 source slice is accepted. Overlord now has a real control-plane GitHub App adapter behind the existing `GitHubPort` plus an AWS Secrets Manager implementation behind the existing `SecretStorePort`.

The existing `GitHubBroker` remains the privileged mutation authority. This slice does not expose a product-facing GitHub write endpoint and does not give OpenCode direct repository credentials.

## Source Acceptance

Source PR `#27` — `feat: add hosted GitHub App and Secrets Manager adapters`:

```text
exact final PR head:       a26e26d3e082414b425844070e64e2ef44338cca
PR permanent CI:           #335
PR CI run ID:              32191862127
PR CI conclusion:          success
merged source main:        e1d16721e28b9a8a50b0dbf1a1cab7393079399a
post-merge CI:             #336
post-merge CI run ID:      32192005317
post-merge CI conclusion:  success
```

Both accepted CI gates included Compose validation, PostgreSQL startup/readiness, locked dependency synchronization, Ruff lint, Ruff format check, strict mypy, Alembic upgrade, and full pytest.

## AWS Secrets Manager Boundary

`AwsSecretsManagerSecretStore` implements the existing `SecretStorePort` and retrieves secrets by exact secret name using the runtime's ambient AWS IAM identity.

The hosted production secret is:

```text
region:       us-east-2
secret name:  overlord/production/github-app
value:        GitHub App PEM private key only
```

No AWS access key or secret access key is embedded in application code or committed configuration. The adapter relies on the hosted runtime's AWS identity.

The GitHub App private key is not stored in PostgreSQL, GitHub repository files, CI secrets for normal tests, application environment variables, or durable audit payloads.

## GitHub App Runtime Configuration

Non-secret runtime configuration now includes:

```text
OVERLORD_AWS_REGION
OVERLORD_GITHUB_APP_ID
OVERLORD_GITHUB_APP_INSTALLATION_ID
OVERLORD_GITHUB_APP_PRIVATE_KEY_SECRET_NAME
```

The App ID and Installation ID are identifiers rather than secret material. The private-key secret name defaults to `overlord/production/github-app` and the AWS region defaults to `us-east-2`.

Configuration validation requires App ID and Installation ID to be supplied together.

## GitHub App Authentication

`GitHubAppAdapter` retrieves the PEM private key through `SecretStorePort` only when it needs to authenticate as the GitHub App.

It signs a short-lived RS256 GitHub App JWT and exchanges that JWT for a GitHub installation access token. Installation tokens are kept only in process memory and reused until shortly before expiry. They are never persisted to PostgreSQL or audit events.

Repository API calls use the installation token rather than the GitHub App private key.

## Repository Lifecycle Coverage

The credentialed adapter implements the existing `GitHubPort` lifecycle boundary, including:

- repository context reads;
- file reads;
- code search;
- branch creation from an exact source SHA;
- multi-file commits with an exact expected branch head;
- pull-request create/update/read operations;
- check-run reads;
- exact-head pull-request merges.

Stale branch heads fail before a repository write. Merge requests continue to carry the expected head SHA supplied by `GitHubBroker`.

## Broker and Audit Boundaries

This slice does not replace or bypass the previously accepted broker and audit layers.

The intended hosted write path remains:

```text
application service
  -> GitHubBroker
  -> durable audit evidence / policy checks
  -> GitHubPort
  -> GitHubAppAdapter
  -> short-lived GitHub installation token
  -> GitHub API
```

OpenCode remains behind `DeveloperAgentPort` and receives no GitHub App private key, installation token, or AWS Secrets Manager read permission.

## Test Boundary

Normal CI remains credential-free and does not call live AWS Secrets Manager or live GitHub APIs.

Focused tests prove:

- exact Secrets Manager lookup by configured name;
- string and UTF-8 binary secret retrieval;
- empty secrets fail closed;
- GitHub App JWT signing uses the secret-store value;
- installation-token responses are cached only while valid;
- branch creation uses the exact resolved source SHA;
- stale-head commit attempts fail before a repository write;
- merge requests carry the exact expected head SHA and selected merge method.

## Owner Provisioning Completed

The owner has completed the external prerequisites for this slice:

- created the dedicated Overlord GitHub App;
- installed the App only on the `Overlord` repository;
- generated the GitHub App private key;
- recorded the App ID and Installation ID locally;
- stored the PEM private key in AWS Secrets Manager at `overlord/production/github-app` in `us-east-2`.

No private key or hosted credential was provided in chat or committed to either repository.

## Remaining Hosted Enablement

The adapter exists and the secret is provisioned, but hosted execution is not enabled until the runtime IAM/configuration boundary is completed.

Remaining work is deliberately limited to:

1. create a least-privilege IAM permission allowing only `secretsmanager:GetSecretValue` on `overlord/production/github-app`;
2. attach that permission only to the eventual Overlord hosted control-plane runtime identity;
3. configure App ID and Installation ID as non-secret hosted runtime settings;
4. perform a controlled live adapter smoke test through the broker/audit path before exposing any product-facing GitHub write operation.

Remote worker provisioning and Phase 4 infrastructure remain out of scope.

## Verification Record

- Last verified: `2026-08-18`.
- Verified against: source PR #27 exact final head `a26e26d3e082414b425844070e64e2ef44338cca`; PR CI #335 run `32191862127`; merged source main `e1d16721e28b9a8a50b0dbf1a1cab7393079399a`; post-merge CI #336 run `32192005317`; `AwsSecretsManagerSecretStore`; `GitHubAppAdapter`; hosted adapter factory; typed runtime settings; focused adapter tests.
- Verified by: High Director.
