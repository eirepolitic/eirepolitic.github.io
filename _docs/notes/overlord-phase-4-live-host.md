---
title: Overlord Phase 4 — Live MVP Host
summary: Live deployment record for the first single-host Overlord MVP on DigitalOcean.
section: notes
doc_type: note
status: active
created: 2026-08-19
updated: 2026-08-29
last_verified: 2026-08-29
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

## Current state

The first always-on Overlord MVP host is provisioned and running on DigitalOcean.

```text
project:                  Overlord
environment:              production
host name:                overlord-prod-01
region:                   NYC3
OS:                       Ubuntu 24.04 LTS x64
Droplet class:            Basic / Regular SSD
size:                     2 vCPU / 4 GiB RAM / 80 GiB SSD
base price:               $24/month
initial source release:   562ee774a56b89eda8c1f913abf6adf0981f9b13
current verified release: f07ffa1ac1743a7f75b4415eab2a70852e528e2e
```

DigitalOcean improved metrics/monitoring is enabled. Managed Database and startup-script add-ons were not enabled.

The accepted architecture remains unchanged:

```text
PostgreSQL
  -> canonical Conversation / WorkRequest / Plan / Task / AgentRun / audit state

DBOS
  -> durable coordination, workflow output and checkpoints
  -> not canonical task/run state

Developer execution
  -> local disposable Docker
  -> OpenCode
  -> OpenAI

GitHub mutation authority
  -> GitHubPort
  -> GitHubBroker
  -> GitHub App adapter
  -> durable audit
```

Remote Developer workers remain deferred.

## Host and security boundary

Administrative SSH uses a passphrase-protected Ed25519 key. The host has a separate repository deploy key installed on `Overlord` with write access disabled. A repository-level GitHub Actions self-hosted runner named `overlord-prod-01` is installed as a systemd service and is used only by manually dispatched production operations workflows. Normal pull-request and `main` CI continue to run on GitHub-hosted runners.

PostgreSQL 17 runs in Docker and binds only to host loopback. The Overlord control plane runs as an enabled systemd service and binds only to `127.0.0.1:8000`. Production health and readiness checks are part of the accepted deployment workflow.

The production control plane obtains GitHub App authority through:

```text
DigitalOcean Overlord
-> narrowly scoped AWS IAM identity
-> AWS Secrets Manager us-east-2
-> overlord/production/github-app
```

Developer containers receive only the model credential needed for the bounded run. They do not receive the Docker socket, GitHub App private key, installation token, AWS credentials, PostgreSQL credentials, SSH private keys, broad host filesystem access, or broad Linux privileges.

The production source checkout remains root-managed and read-only to the `overlord` service account. Bounded local clone requires service-visible `GIT_CONFIG_GLOBAL=/etc/overlord/gitconfig` with trusted entries for `/opt/overlord-source` and `/opt/overlord-source/.git`.

## Accepted live milestones

### Local disposable Developer execution — 2026-08-20

Production proved the local execution chain:

```text
Overlord composition
-> DeveloperEnvironmentExecutionService
-> LocalDockerDeveloperEnvironmentAdapter
-> disposable OpenCode container
-> OpenCodeDeveloperAgentAdapter
-> OpenAI API
-> result / usage collection
-> automatic cleanup
```

The smoke test confirmed workspace access, bounded model execution, usage persistence, and automatic container cleanup while injecting only `OPENAI_API_KEY` into the Developer container.

Two runtime defects were corrected through normal PR and CI gates before acceptance: OpenCode readiness now uses `/global/health` instead of a raw TCP-connect probe, and an absent aggregate session-status entry is normalized to `idle` according to the accepted runtime semantics.

### GitHub App broker/audit read path — 2026-08-20

Production proved the credential and authority path:

```text
production control plane
-> AWS Secrets Manager
-> GitHub App JWT
-> short-lived installation token
-> GitHub API
-> GitHubBroker
-> exact-head policy evaluation
-> durable audit
```

The smoke test deliberately used a fail-closed merge policy sentinel and performed no repository mutation. Developer containers received no GitHub/AWS credentials.

### Bounded Developer API — 2026-08-24

Production accepted the bounded API path:

```text
POST /tasks/{task_id}/bounded-developer-runs
-> server-owned model credential loading
-> BoundedDeveloperExecutionService
-> canonical Task + AgentRun persistence
-> disposable task workspace
-> disposable OpenCode Developer container
-> OpenAI API
-> evidence / usage persistence
-> cleanup
-> durable audit
```

The API caller supplies only the exact source revision. Post-run acceptance verified completed task/run state, final evidence, usage, no residual task workspace, no residual task-scoped Developer container, and the ordered Developer dispatch/start/completion audit events.

### DBOS-backed bounded Developer execution — 2026-08-28

Production release `00d6472a3c006d2502ea1bd50a695028add9e3c4` accepted the DBOS-backed bounded execution path. Acceptance workflow run `33218577873` verified:

- stable task + revision DBOS workflow identity;
- one canonical AgentRun reused by the same task/revision retry;
- DBOS workflow `SUCCESS` with persisted output and at least one checkpoint;
- canonical Task/AgentRun state remains in PostgreSQL;
- final evidence and usage persisted;
- workspace/container cleanup completed;
- no GitHub mutation occurred.

### Bounded Developer GitHub publication — 2026-08-28

Production release `c5915d4321efc45e5be86a84a745395c0a31d259` accepted durable bounded Developer GitHub publication. Acceptance workflow run `33226001121` verified:

```text
POST /tasks/{task_id}/bounded-developer-publications
-> stable task + revision DBOS publication workflow
-> canonical completed bounded AgentRun
-> host-observed workspace-change validation
-> GitHubBroker policy
-> GitHub App adapter
-> deterministic task branch from exact source SHA
-> broker-controlled commit_files
-> canonical publication metadata
-> durable audit
-> DBOS output/checkpoint
```

Accepted evidence:

```text
SOURCE_REVISION=c5915d4321efc45e5be86a84a745395c0a31d259
TASK_ID=79af58db-2ae4-43e1-b9e0-b0adc6b000ac
TASK_BRANCH=overlord/task-79af58db-2ae4-43e1-b9e0-b0adc6b000ac
PUBLICATION_COMMIT=aece6684ae189c16cb98d613be3dc9cba5819769
MARKER_PATH=overlord-acceptance/publication-79af58db-2ae4-43e1-b9e0-b0adc6b000ac.txt
DBOS_WORKFLOW_ID=developer-github-publication:79af58db-2ae4-43e1-b9e0-b0adc6b000ac:a726c7b72c4a8524
RETRY_REUSED_RESULT=true
```

The ordered publication audit sequence was:

```text
DEVELOPER_GITHUB_PUBLICATION_PREPARED
github.branch.create.requested
github.branch.create.completed
github.commit_files.requested
github.commit_files.completed
DEVELOPER_GITHUB_PUBLICATION_COMPLETED
```

Production also proved that canonical short repository refs such as `Overlord` can remain provider-neutral: the credentialed GitHub App adapter resolves them against the App installation's accessible repository list and fails closed if no unique match exists.

### Broker-controlled Developer pull-request creation — 2026-08-29

Production release `506d4ad814411044bce771239a9daec9d8d7648a` accepted explicit bounded pull-request creation. Deployment run `33265412832` and acceptance run `33265432312` proved:

```text
POST /tasks/{task_id}/bounded-developer-pull-requests
-> completed publication metadata validation
-> live task branch head == persisted publication commit
-> GitHubBroker.create_pull_request
-> GitHub App PR creation / duplicate recovery
-> canonical AgentRun github_pull_request metadata
-> durable PR audit
-> stable DBOS PR workflow result/checkpoint
```

Accepted evidence:

```text
SOURCE_REVISION=506d4ad814411044bce771239a9daec9d8d7648a
TASK_ID=3e829b11-7bf6-490d-91f6-4f4c026bdc21
AGENT_RUN_ID=93bd3aae-a51d-4f9f-8417-ab75a1dba160
TASK_BRANCH=overlord/task-3e829b11-7bf6-490d-91f6-4f4c026bdc21
PUBLICATION_COMMIT=92f9655d650ac64c99c6327eaf886ed3fc664052
PULL_REQUEST_NUMBER=61
PULL_REQUEST_STATE=open
PULL_REQUEST_DRAFT=false
PULL_REQUEST_BASE=main
PUBLICATION_WORKFLOW_ID=developer-github-publication:3e829b11-7bf6-490d-91f6-4f4c026bdc21:20d188e66705c607
PULL_REQUEST_WORKFLOW_ID=developer-github-pull-request:3e829b11-7bf6-490d-91f6-4f4c026bdc21:20d188e66705c607
PULL_REQUEST_RETRY_REUSED_RESULT=true
```

The PR audit sequence appended:

```text
DEVELOPER_GITHUB_PULL_REQUEST_PREPARED
github.pull_request.create.requested
github.pull_request.create.completed
DEVELOPER_GITHUB_PULL_REQUEST_COMPLETED
```

PR #61 is intentionally preserved open and unmerged as production evidence. No merge operation was invoked.

### Exact-head pull-request check observation — 2026-08-29

Production release `1153368660e2f8e839c279bc9ae789e028985caf` is accepted for refreshable exact-head pull-request check observation.

Implementation PR #63 merged as `a7be6ab05da4f3f424b0e1a0dc68b2fe4005e7cf`. Its exact-head CI #537, run `33273309548`, and post-merge `main` CI #538, run `33273370609`, were fully green.

Production acceptance support PR #64 merged as the deployed release `1153368660e2f8e839c279bc9ae789e028985caf`. Its exact-head CI #539, run `33273463606`, and post-merge `main` CI #540, run `33273529881`, were fully green. Deploy production #11, run `33273579895`, completed successfully on that exact release.

The checked-in `Accept production Developer pull request observation` workflow run `33273633409` then completed successfully on the exact deployed SHA. It reused existing production evidence PR #61 and performed no GitHub mutation.

The accepted operation is:

```text
POST /tasks/{task_id}/bounded-developer-pull-request-observations
-> completed publication + PR canonical metadata
-> live PR must still be open
-> live PR head/base must match canonical publication/PR state
-> GitHubPort.list_checks(exact persisted publication commit SHA)
-> latest observation snapshot persisted on canonical AgentRun
-> durable observation audit event
```

The production acceptance called the observation endpoint twice. Both calls performed fresh GitHub reads and each added a durable `DEVELOPER_GITHUB_PULL_REQUEST_CHECKS_OBSERVED` audit event. This proves observation is intentionally refreshable rather than frozen behind one stable DBOS result.

The acceptance independently verified all of the following:

```text
TASK_ID=3e829b11-7bf6-490d-91f6-4f4c026bdc21
AGENT_RUN_ID=93bd3aae-a51d-4f9f-8417-ab75a1dba160
PULL_REQUEST_NUMBER=61
PULL_REQUEST_STATE=open
PULL_REQUEST_BASE=main
EXACT_HEAD_SHA=92f9655d650ac64c99c6327eaf886ed3fc664052
CHECK_COUNT>0
ALL_CHECKS_TERMINAL=true
ALL_CHECKS_SUCCESSFUL=true
REFRESH_AUDIT_EVENTS_ADDED=2
GITHUB_MUTATION=none
```

The API snapshot's check identities were also compared with a direct production GitHub App read of check-runs for the exact persisted publication commit. Zero check-runs are explicitly not treated as terminal or successful.

### Fail-closed merge evaluation — 2026-08-29

Production release `f07ffa1ac1743a7f75b4415eab2a70852e528e2e` is accepted for refreshable, non-mutating bounded Developer merge evaluation.

Implementation PR #65 merged as `d8fb7b9a7dfd70c97013cb2cc8b35e1468be4ac2`. Its exact-head CI #550, run `33277221034`, and post-merge `main` CI #551, run `33277289772`, were fully green.

Production acceptance support PR #66 merged as the deployed release `f07ffa1ac1743a7f75b4415eab2a70852e528e2e`. Its exact-head CI #552, run `33277395683`, and post-merge `main` CI #553, run `33277454134`, were fully green. Deploy production #12, run `33277524943`, completed successfully on that exact release.

The checked-in `Accept production Developer merge evaluation` workflow run `33277550160` completed successfully on the exact deployed SHA. It reused existing production evidence PR #61 and performed no GitHub mutation.

The accepted operation is:

```text
POST /tasks/{task_id}/bounded-developer-merge-evaluations
-> completed canonical publication + PR state
-> latest canonical exact-head observation
-> live PR read and exact head/base/state comparison
-> fresh GitHub check-runs for persisted publication commit
-> explicit server-owned required-check policy
-> canonical merge-evaluation snapshot
-> durable DEVELOPER_GITHUB_MERGE_EVALUATED audit event
```

The accepted production required-check policy is exactly:

```text
required checks: quality
required cardinality: exactly one observed + exactly one live
required status: completed
required conclusion: success
```

The evaluator fails closed if any configured required check is missing, duplicated, pending, neutral, skipped, cancelled, failed, or otherwise not exactly `completed/success` in both canonical observation evidence and a fresh live GitHub read. It also denies evaluation when the live PR state, head branch, base branch, or head SHA no longer matches canonical publication/PR state.

Production acceptance called the merge-evaluation endpoint twice and verified both evaluations were eligible. Each call performed fresh live reads and added a durable `DEVELOPER_GITHUB_MERGE_EVALUATED` audit event. The latest eligible result was persisted on the canonical AgentRun.

Accepted evidence:

```text
TASK_ID=3e829b11-7bf6-490d-91f6-4f4c026bdc21
AGENT_RUN_ID=93bd3aae-a51d-4f9f-8417-ab75a1dba160
PULL_REQUEST_NUMBER=61
PULL_REQUEST_STATE=open
PULL_REQUEST_BASE=main
EXACT_HEAD_SHA=92f9655d650ac64c99c6327eaf886ed3fc664052
REQUIRED_CHECK=quality
OBSERVED_COUNT=1
LIVE_COUNT=1
OBSERVED_STATUS=completed
OBSERVED_CONCLUSION=success
LIVE_STATUS=completed
LIVE_CONCLUSION=success
MERGE_ELIGIBLE=true
DENIAL_REASONS=[]
REFRESH_AUDIT_EVENTS_ADDED=2
MAIN_HEAD_UNCHANGED=true
PULL_REQUEST_UNCHANGED=true
GITHUB_MUTATION=none
```

PR #61 remained open, non-draft, clean and unmerged after acceptance. The production `main` head was unchanged by both evaluation calls. Merge evaluation is therefore accepted as evidence/policy only; there is still no production merge-mutation operation.

## Automated production operations

The production host uses the dedicated `overlord-prod-01` repository runner for manually dispatched deployment and acceptance workflows. Ordinary CI does not execute on the production host.

Deployment requires the exact fetched `origin/main` SHA, promotes `/opt/overlord-source` to `/opt/overlord/current`, syncs the locked environment, restarts the service, and verifies health/readiness. Failure diagnostics are sanitized and do not include application secrets, environment values, GitHub tokens, or model credentials.

Production deployment defects discovered earlier were corrected through normal PR/CI gates: persistent `.venv` ownership, runner traversal of protected production paths, and bounded startup polling for `/health` and `/ready`.

## Current authority boundary

The production-proven path is now:

```text
bounded Developer run
-> canonical host-observed changes
-> broker-controlled task branch + commit
-> broker-controlled PR creation
-> exact-head PR/check observation
-> explicit required-check merge evaluation
```

Mutation authority remains only:

```text
GitHubPort -> GitHubBroker -> GitHub App adapter -> durable audit
```

Check observation and merge evaluation are both read-only with respect to GitHub. PostgreSQL stores their latest canonical snapshots; durable audit preserves refresh/evaluation history. DBOS remains appropriate for stable mutation coordination/results, but is deliberately not used to freeze changing external CI or merge-evaluation state.

No Developer container receives GitHub App credentials or GitHub mutation authority. No automatic or API-driven merge operation is currently accepted in production.

## Next stage

The next implementation slice may add a separate broker-controlled **merge mutation** only if it preserves the production-proven evaluation boundary. It should not let a previously eligible snapshot become an unconditional authorization token.

A merge-mutation design should fail closed unless, immediately before mutation:

1. PR is still open and targets the expected base branch;
2. live PR head exactly equals the canonical publication commit;
3. canonical publication and PR state still match the live PR;
4. a fresh merge evaluation for that exact head is eligible;
5. required check identities remain explicitly configured;
6. every required check is still present exactly once and `completed/success` in canonical observation and fresh live GitHub state;
7. the mutation goes only through `GitHubPort -> GitHubBroker -> GitHub App adapter -> durable audit`;
8. retry/recovery cannot create duplicate merge effects or treat an ambiguous GitHub response as success without verification;
9. expected head SHA is supplied to the GitHub merge operation;
10. the merge result and canonical completion/audit evidence are persisted and independently production-accepted.

Remote Developer workers remain deferred until workload evidence justifies them.

## Verification record

- Last verified: `2026-08-29`.
- Current accepted production release: `f07ffa1ac1743a7f75b4415eab2a70852e528e2e`.
- Latest deploy: #12 / run `33277524943`, success.
- Latest production acceptance: merge evaluation #1 / run `33277550160`, success.
- Merge-evaluation implementation: PR #65; exact-head CI #550 / `33277221034`; merge `d8fb7b9a7dfd70c97013cb2cc8b35e1468be4ac2`; post-merge CI #551 / `33277289772`.
- Merge-evaluation acceptance support: PR #66; exact-head CI #552 / `33277395683`; merge `f07ffa1ac1743a7f75b4415eab2a70852e528e2e`; post-merge CI #553 / `33277454134`.
- Accepted production required-check policy: exactly one `quality` check, `completed/success`, matched in both canonical observation and fresh live GitHub evidence.
- Production evidence PR #61 remains open, non-draft and unmerged on base `main`, head `92f9655d650ac64c99c6327eaf886ed3fc664052`.
- Production evidence task: `3e829b11-7bf6-490d-91f6-4f4c026bdc21`.
- Production evidence AgentRun: `93bd3aae-a51d-4f9f-8417-ab75a1dba160`.
- Security verification: no Docker socket, AWS credential, GitHub App private key, installation token, or GitHub mutation authority entered a Developer container; merge-evaluation acceptance performed no GitHub mutation and did not change `main`.
- Verified by: High Director.
