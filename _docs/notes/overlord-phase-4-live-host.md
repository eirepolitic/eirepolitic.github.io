---
title: Overlord Phase 4 — Live MVP Host
summary: Live deployment record for the first single-host Overlord MVP on DigitalOcean.
section: notes
doc_type: note
status: active
created: 2026-08-19
updated: 2026-08-28
last_verified: 2026-08-28
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
current verified release: 00d6472a3c006d2502ea1bd50a695028add9e3c4
```

DigitalOcean improved metrics/monitoring is enabled. Managed Database and startup-script add-ons were not enabled.

## Host access

Administrative SSH uses a passphrase-protected Ed25519 key. The host has a separate repository deploy key installed on `Overlord` with write access disabled. The source checkout therefore does not require a GitHub password or personal access token.

A dedicated repository-level GitHub Actions self-hosted runner named `overlord-prod-01` is also installed as a systemd service. It is used only by manually dispatched production operations workflows. Normal pull-request and `main` CI continue to run on GitHub-hosted runners.

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

## Live bounded Developer API acceptance — 2026-08-24

Production release `2afdd597c3264a2b5005342ef890ebbc51497251` is accepted for the bounded disposable Developer API path.

The tested route was:

```text
POST /tasks/{task_id}/bounded-developer-runs
-> server-owned OpenAI credential loading
-> BoundedDeveloperExecutionService
-> canonical AgentRun + Task persistence
-> LocalGitCloneDeveloperWorkspaceAdapter
-> disposable task workspace
-> LocalDockerDeveloperEnvironmentAdapter
-> OpenCodeDeveloperAgentAdapter
-> OpenAI API
-> final evidence + usage persistence
-> workspace/container cleanup
-> durable audit events
```

The API caller supplied only the exact source revision. The server read the OpenAI API key from its configured root-managed key file and injected only `OPENAI_API_KEY` into the disposable Developer container. The container received no GitHub App credential, AWS credential, Docker socket, or broad host filesystem access.

Accepted live result:

```text
BOUNDED_SMOKE_HTTP=200
BOUNDED_SMOKE_TASK_STATUS=completed
BOUNDED_SMOKE_RUN_STATUS=completed
BOUNDED_SMOKE_REVISION_MATCH=true
BOUNDED_SMOKE_RUNTIME_STATE=idle
BOUNDED_SMOKE_INPUT_TOKENS=9
BOUNDED_SMOKE_OUTPUT_TOKENS=99
BOUNDED_SMOKE_FINAL_EVIDENCE_PRESENT=true
```

Post-run cleanup was also accepted:

- `/var/lib/overlord/workspaces` contained no residual task workspace;
- no task-scoped Developer container remained.

Canonical persistence and audit evidence were verified independently after the API response:

```text
BOUNDED_AUDIT_TASK_STATUS=completed
BOUNDED_AUDIT_RUN_STATUS=completed
BOUNDED_AUDIT_EXTERNAL_SESSION_NULL=true
BOUNDED_AUDIT_REVISION_MATCH=true
BOUNDED_AUDIT_FINAL_EVIDENCE_PRESENT=true
BOUNDED_AUDIT_EVENTS=DEVELOPER_DISPATCH_CREATED,DEVELOPER_RUN_STARTED,DEVELOPER_RUN_COMPLETED
```

### Trusted source checkout Git configuration

The first live bounded attempts failed before Docker/OpenCode startup at `git clone --shared --no-checkout /opt/overlord-source ...` with Git's dubious-ownership protection. The trusted production source checkout is root-managed and intentionally remains non-writable by the `overlord` service account.

Because the systemd service uses `ProtectHome=true`, a user-home Git config is not a reliable service configuration path. Production therefore uses a dedicated service-visible Git config:

```text
GIT_CONFIG_GLOBAL=/etc/overlord/gitconfig
```

The file is readable by the `overlord` service account and trusts only the two required local paths:

```text
safe.directory=/opt/overlord-source
safe.directory=/opt/overlord-source/.git
```

Both entries are required because `git clone --shared` evaluates the source Git directory as well as the working-tree path. This preserves the intended boundary: `/opt/overlord-source` stays root-managed and read-only to the service, while writable task state remains under `/var/lib/overlord/workspaces`.

## Live DBOS-backed bounded Developer acceptance — 2026-08-28

Production release `00d6472a3c006d2502ea1bd50a695028add9e3c4` is accepted for DBOS-backed bounded disposable Developer execution.

The release was deployed by the dedicated `Deploy production` workflow on the `overlord-prod-01` self-hosted runner. The successful deployment required the exact fetched `origin/main` SHA, promoted `/opt/overlord-source` to `/opt/overlord/current`, ran `uv sync --locked`, restarted `overlord`, and passed both `/health` and `/ready`.

The live acceptance then ran through the checked-in `Accept production bounded Developer` workflow. GitHub Actions run `33218577873` completed successfully. The probe created one fresh read-only canonical task and exercised:

```text
POST /tasks/{task_id}/bounded-developer-runs
-> stable task + revision DBOS workflow identity
-> DBOS bounded workflow
-> canonical AgentRun recovery/reuse
-> disposable task workspace
-> disposable OpenCode Developer container
-> OpenAI API
-> result + usage + final evidence persistence
-> DBOS workflow output/checkpoint persistence
-> deterministic workspace/container cleanup
```

The same task and deployed revision were submitted twice. The second call reused the first canonical AgentRun rather than creating a duplicate.

The acceptance workflow asserted all of the following before succeeding:

```text
TASK_STATUS=completed
RUN_STATUS=completed
REVISION_MATCH=true
RUNTIME_STATE=idle
EXTERNAL_SESSION_ID_NULL=true
USAGE_PERSISTED=true
FINAL_EVIDENCE_PERSISTED=true
READ_ONLY_DIFF_COUNT=0
CANONICAL_AGENT_RUN_COUNT=1
RETRY_REUSED_AGENT_RUN=true
DBOS_WORKFLOW_STATUS=SUCCESS
DBOS_WORKFLOW_OUTPUT_PRESENT=true
DBOS_STEP_CHECKPOINT_COUNT>=1
WORKSPACE_CLEAN=true
CONTAINER_CLEAN=true
AUDIT_EVENTS=DEVELOPER_DISPATCH_CREATED,DEVELOPER_RUN_STARTED,DEVELOPER_RUN_COMPLETED
```

This proves that the production API is now using the DBOS-backed bounded path, that the durable workflow identity and checkpoint exist, and that retrying the same task + revision does not duplicate canonical control-plane state. It also confirms that the external disposable execution remains read-only for this acceptance and leaves no task-scoped local resources behind.

The durability boundary remains unchanged: DBOS coordinates workflow durability/checkpointing, while canonical Task and AgentRun state remains owned by Overlord/PostgreSQL. GitHub mutation authority remains `GitHubPort -> GitHubBroker -> durable audit`; no GitHub App or AWS credentials entered the Developer container.

## Automated production operations

The production host now has a dedicated repository-level GitHub Actions runner named `overlord-prod-01`. The deployment workflow is manual-dispatch only and targets the custom `overlord-prod-01` runner label; ordinary CI does not execute on the production host.

The deployment path now also publishes a sanitized diagnostic record on failure containing only deployment stage, exit code, target/source SHA, service state, and bounded tool/permission diagnostics. No application secrets, environment values, GitHub tokens, or model credentials are included.

During automation setup, three operational defects were found and corrected through normal PR, exact-head CI, merge, and post-merge `main` gates:

1. release promotion changed the persistent `.venv` ownership before `uv sync`; deployment now restores `.venv` ownership to `overlord:overlord` and owner write permissions;
2. the GitHub runner could not traverse the protected production checkout directly; production-path `cd` and verification now run under the intended `overlord`/`sudo` account boundary;
3. the initial health probe assumed zero startup latency after `systemctl start`; deployment now polls `/health` and `/ready` for bounded startup windows.

These changes automate the already-established deployment path; they do not change the single-host architecture or Developer security boundaries.

## Next stage

The major live Phase 4 plumbing milestones are now proven:

1. local disposable Developer execution through OpenCode and OpenAI;
2. GitHub mutation authority through `GitHubBroker`, exact-head policy, the GitHub App adapter, and durable audit;
3. bounded task-scoped Developer execution through the production API with canonical run/task persistence, final evidence, usage, cleanup, and audit events;
4. DBOS-backed bounded execution with stable workflow identity, persisted checkpoint/result, canonical AgentRun reuse on retry, and deterministic local resource cleanup;
5. repository-controlled production deployment and acceptance through the dedicated self-hosted runner.

The next implementation work should build on this accepted single-host durable execution path rather than add new infrastructure. Remote Developer workers remain deferred until workload evidence justifies them. Provider/runtime-neutral ports and the `GitHubBroker` authority boundary remain the design constraints for the next slice.

## Verification record

- Last verified: `2026-08-28`.
- Verified against: live `overlord-prod-01`; accepted deployed release `00d6472a3c006d2502ea1bd50a695028add9e3c4`; DBOS-backed bounded Developer production acceptance run `33218577873`; AWS Secrets Manager GitHub App path; live local Developer/OpenCode/OpenAI path; bounded Developer API; `GitHubBroker`; canonical task/run persistence; durable audit persistence.
- Runtime checks: PostgreSQL healthy; Overlord `/health` OK; Overlord `/ready` ready; exact-revision bounded Developer execution completed; DBOS workflow status/output and step checkpoint persisted; retry reused one canonical AgentRun; final evidence and usage persisted; read-only diff was empty; disposable workspace and container cleanup confirmed; live fail-closed GitHub broker smoke accepted.
- Security checks: bounded API accepted only server-defined runtime configuration plus an exact revision; only `OPENAI_API_KEY` entered the Developer container; no Docker socket, AWS credential, GitHub App private key, or installation token entered a Developer container; the GitHub broker smoke performed no mutation.
- Operational requirements: production bounded local clone requires service-visible `GIT_CONFIG_GLOBAL=/etc/overlord/gitconfig` with `safe.directory` entries for `/opt/overlord-source` and `/opt/overlord-source/.git`; the persistent deployment `.venv` remains owned by `overlord`; production deploy/acceptance workflows target only the dedicated `overlord-prod-01` self-hosted runner.
- Verified by: High Director.
