---
title: Overlord Phase 4 — Live MVP Host
summary: Live deployment record for the first single-host Overlord MVP on DigitalOcean.
section: notes
doc_type: note
status: active
created: 2026-08-19
updated: 2026-08-20
last_verified: 2026-08-20
owner: High Director
order: 152
permalink: /projects/notes/overlord-phase-4-live-host/
tags:
  - overlord
  - phase-4
  - digitalocean
  - deployment
  - production
---

# Overlord Phase 4 — Live MVP Host

## Live milestone

The first always-on Overlord MVP host is provisioned and running on DigitalOcean.

```text
project:              Overlord
environment:          production
host name:            overlord-prod-01
region:               NYC3
OS:                   Ubuntu 24.04 LTS x64
Droplet class:        Basic / Regular SSD
size:                 2 vCPU / 4 GiB RAM / 80 GiB SSD
base price:           $24/month
initial source release: 562ee774a56b89eda8c1f913abf6adf0981f9b13
current verified release: 4fed04c4c0c75c3b18a3bb956680d0511ae2be58
```

DigitalOcean improved metrics/monitoring is enabled. Managed Database and startup-script add-ons were not enabled.

## Host access

Administrative SSH uses a passphrase-protected Ed25519 key. The host has a separate repository deploy key installed on `Overlord` with write access disabled. The source checkout therefore does not require a GitHub password or personal access token.

## Running services

The accepted Phase 4 single-host deployment assets were used without changing the architecture:

- PostgreSQL 17 is running in Docker and reports healthy;
- PostgreSQL is bound only to host loopback;
- the Overlord control plane is installed as an enabled `systemd` service;
- Overlord is bound only to `127.0.0.1:8000`;
- `/health` returned `{"status":"ok","service":"overlord"}`;
- `/ready` returned `{"status":"ready","service":"overlord"}`.

The PostgreSQL password was generated on the host and is not stored in Git. `/etc/overlord/postgres-password` and `/etc/overlord/overlord.env` are owned by `root:overlord` with `0640` permissions.

## Security and authority boundary

The control plane service account owns Docker lifecycle authority so it can create disposable local Developer Environments. OpenCode Developer containers do not receive the host Docker socket.

No GitHub App private key, installation token, AWS credential, PostgreSQL password, SSH private key, or LLM provider credential was committed to Git or copied into this documentation.

The live control-plane secret path is also confirmed:

```text
DigitalOcean Overlord
-> narrowly scoped AWS IAM identity
-> AWS Secrets Manager us-east-2
-> overlord/production/github-app
```

The production adapter path using `AwsSecretsManagerSecretStore` returned `SECRET_READ_OK True`. The control plane was not moved to EC2 merely to obtain an instance role.

The production runtime also requires the two non-secret GitHub App identifiers in `/etc/overlord/overlord.env`:

- `OVERLORD_GITHUB_APP_ID`;
- `OVERLORD_GITHUB_APP_INSTALLATION_ID`.

The live broker smoke initially failed closed before GitHub authentication because these identifiers had not yet been configured. They were subsequently added without exposing the GitHub App private key or any installation token.

## Live local Developer smoke acceptance — 2026-08-20

The bounded local Developer smoke test is accepted on production release `caa854725c07814dc095d0350d947f86193ae5e2`.

The tested path was:

```text
Overlord application composition
-> DeveloperEnvironmentExecutionService
-> LocalDockerDeveloperEnvironmentAdapter
-> disposable overlord-developer:1.18.16 container
-> OpenCodeDeveloperAgentAdapter
-> OpenAI API
-> result / usage collection
-> automatic container cleanup
```

The smoke task created a temporary workspace containing `SMOKE.txt`, instructed the Developer to inspect it without modifying files, and requested one short confirmation sentence. Only `OPENAI_API_KEY` was injected into the disposable Developer container. No AWS credential, GitHub App private key, GitHub installation token, Docker socket, or unrestricted host filesystem access was provided.

Accepted live result:

```text
provider:                       openai
model:                          gpt-5.6-luna
Developer image:                overlord-developer:1.18.16
execution mode:                 local_container
DEVELOPER_SMOKE_STATUS:         idle
DEVELOPER_SMOKE_INPUT_TOKENS:   9
DEVELOPER_SMOKE_OUTPUT_TOKENS:  73
DEVELOPER_SMOKE_SUMMARY:        Workspace is accessible, and `SMOKE.txt` was inspected successfully.
```

Post-run verification found no `overlord-developer-live-smoke` container remaining. Overlord remained healthy and ready after deployment and the smoke test.

Two live-runtime defects were found and corrected through normal exact-head CI and post-merge `main` gates before final acceptance:

1. the smoke script originally passed an unsupported `timeout_seconds` constructor argument to `OpenCodeDeveloperAgentAdapter`; it now injects `UrllibJsonClient(..., timeout_seconds=180.0)` through the adapter's existing client boundary;
2. local Docker readiness originally used a TCP-connect probe, which could race OpenCode HTTP startup; readiness now polls `GET /global/health` until OpenCode reports healthy, and absent entries in OpenCode's aggregate session-status map are normalized to `idle` per OpenCode runtime semantics.

These fixes did not change `DeveloperAgentPort`, secret boundaries, Docker privileges, or the decision to keep remote Developer workers deferred.

## Live GitHub App broker/audit smoke acceptance — 2026-08-20

A controlled production GitHub App smoke test is accepted on source release `4fed04c4c0c75c3b18a3bb956680d0511ae2be58`.

The checked-in smoke command exercised the accepted authority path:

```text
production control plane
-> AWS Secrets Manager
-> GitHub App JWT
-> short-lived installation token
-> GitHub API
-> GitHubBroker
-> exact-head policy evaluation
-> durable audit repository
```

The test used already-merged `Overlord` PR #37 and its exact verified head SHA. `GitHubPolicy` also required an intentionally impossible sentinel check, making the smoke fail-closed even if other conditions unexpectedly passed. No repository mutation was possible or attempted.

Accepted result:

```text
GITHUB_BROKER_SMOKE_DECISION=denied
GITHUB_BROKER_SMOKE_HEAD_MATCH=true
GITHUB_BROKER_SMOKE_MUTATION=none
GITHUB_BROKER_SMOKE_AUDIT_EVENTS=github.merge.evaluated
GITHUB_BROKER_SMOKE_CORRELATION_ID=4c6abf5b-bda1-4ca7-83f3-4d4c4d8217ee
```

This confirms that the live DigitalOcean control plane can retrieve the GitHub App private key through the narrowly scoped AWS Secrets Manager adapter, obtain a short-lived installation token, read live GitHub PR/check state, enforce exact-head broker policy, and commit durable audit evidence without exposing GitHub App credentials to a Developer container.

The GitHub App remains installed only on the `Overlord` repository. Developer containers still receive no GitHub App private key, installation token, AWS credential, or Docker socket.

## Next stage

The two major live Phase 4 plumbing milestones are now proven:

1. local disposable Developer execution through OpenCode and OpenAI;
2. GitHub mutation authority through `GitHubBroker`, exact-head policy, the GitHub App adapter, and durable audit.

The next implementation slice should follow the existing Phase 4 plan rather than add new infrastructure:

```text
Manager / control-plane task lifecycle
-> DBOS / durable workflow orchestration
-> DeveloperEnvironmentExecutionService
-> DeveloperAgentPort
-> GitHubBroker for repository mutations
```

Priorities are deeper DBOS/durable workflow integration, making the Developer task lifecycle usable by the Manager/control plane, and recovery/idempotency coverage around those durable boundaries. `REMOTE` Developer execution remains deferred until workload evidence justifies it.

## Verification record

- Last verified: `2026-08-20`.
- Verified against: live `overlord-prod-01`; accepted `Overlord/main` release `4fed04c4c0c75c3b18a3bb956680d0511ae2be58`; AWS Secrets Manager GitHub App path; live local Developer/OpenCode/OpenAI path; `GitHubBroker`; durable audit persistence.
- Runtime checks: PostgreSQL healthy; Overlord `/health` OK; Overlord `/ready` ready; disposable Developer cleanup confirmed; live fail-closed GitHub broker smoke accepted.
- Security checks: no Docker socket, AWS credential, GitHub App private key, or installation token entered a Developer container; the GitHub broker smoke performed no mutation.
- Operational follow-up: restart the `overlord` systemd service after adding the two non-secret GitHub App identifiers so the long-running service inherits the updated environment.
- Verified by: High Director.
