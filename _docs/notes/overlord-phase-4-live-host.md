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
current verified release: caa854725c07814dc095d0350d947f86193ae5e2
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

## Next stage

With AWS Secrets Manager access and the live local-container Developer path now proven, the next controlled production milestone is the live GitHub App smoke test through the existing `GitHubBroker` and durable audit path.

The GitHub test must preserve the accepted authority boundary:

```text
application service
-> GitHubBroker
-> policy / durable audit evidence
-> GitHubPort
-> GitHubAppAdapter
-> short-lived installation token
-> GitHub API
```

Developer containers must not receive GitHub App credentials merely to perform that test. After the broker/audit smoke is accepted, continue the existing Phase 4 plan for durable workflow integration and Manager/control-plane task lifecycle composition. `REMOTE` Developer execution remains deferred until workload evidence justifies it.

## Verification record

- Last verified: `2026-08-20`.
- Verified against: live `overlord-prod-01` deployment of accepted `Overlord/main` release `caa854725c07814dc095d0350d947f86193ae5e2`.
- Runtime checks: PostgreSQL healthy; Overlord `/health` OK; Overlord `/ready` ready; live local Developer/OpenCode/OpenAI smoke accepted; disposable Developer container cleanup confirmed.
- Security checks: only the required OpenAI key was injected into the smoke container; no Docker socket, AWS credential, or GitHub App credential entered the Developer environment.
- Verified by: High Director.
