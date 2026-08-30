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
project:                    Overlord
environment:                production
host name:                  overlord-prod-01
region:                     NYC3
OS:                         Ubuntu 24.04 LTS x64
Droplet class:              Basic / Regular SSD
size:                       2 vCPU / 4 GiB RAM / 80 GiB SSD
base price:                 $24/month
initial source release:     562ee774a56b89eda8c1f913abf6adf0981f9b13
current deployed release:   fd19f6ce74d8907280fcb019d6cefe16d82adb96
current repository main:    48fe44579c834554d6de091b79c1d400ad02627c
```

The accepted architecture is:

```text
PostgreSQL
  -> canonical Conversation / WorkRequest / Plan / Task / AgentRun / audit state
  -> canonical repository_deliveries state after verified merge

DBOS
  -> durable coordination, workflow outputs and checkpoints
  -> not canonical task/run/delivery state

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

Administrative SSH uses a passphrase-protected Ed25519 key. The host has a separate read-only repository deploy key. A repository-level GitHub Actions self-hosted runner named `overlord-prod-01` is installed as a systemd service and is used only by manually dispatched production operations workflows. Normal pull-request and `main` CI run on GitHub-hosted runners.

PostgreSQL 17 runs in Docker and binds only to host loopback. The Overlord control plane runs as an enabled systemd service and binds only to `127.0.0.1:8000`. Production deployment verifies the exact requested SHA plus service health/readiness.

The production control plane obtains GitHub App authority through:

```text
DigitalOcean Overlord
-> narrowly scoped AWS IAM identity
-> AWS Secrets Manager us-east-2
-> overlord/production/github-app
```

Developer containers receive only the model credential needed for their bounded run. They do not receive the Docker socket, GitHub App private key, installation token, AWS credentials, PostgreSQL credentials, SSH private keys, broad host filesystem access, or broad Linux privileges.

Production source is root-managed under `/opt/overlord-source`, deployed code is `/opt/overlord/current`, runtime environment is `/etc/overlord/overlord.env`, and Developer workspaces are rooted at `/var/lib/overlord/workspaces`.

## Accepted live milestones

### Local disposable Developer execution — 2026-08-20

Production proved:

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

Only the model credential entered the Developer container.

### GitHub App broker/audit path — 2026-08-20

Production proved the credential and authority chain:

```text
production control plane
-> AWS Secrets Manager
-> GitHub App JWT
-> short-lived installation token
-> GitHub API
-> GitHubBroker
-> durable audit
```

The initial smoke test deliberately used a fail-closed policy and performed no mutation.

### Bounded Developer API — 2026-08-24

`POST /tasks/{task_id}/bounded-developer-runs` was accepted with server-owned model credential loading, canonical Task/AgentRun persistence, disposable workspace/container execution, evidence/usage persistence, cleanup and durable audit.

### DBOS-backed bounded Developer execution — 2026-08-28

Production release `00d6472a3c006d2502ea1bd50a695028add9e3c4` and acceptance run `33218577873` proved stable task+revision workflow identity, one canonical AgentRun, DBOS `SUCCESS` with output/checkpoint, PostgreSQL canonical state, cleanup and no GitHub mutation.

### Bounded Developer GitHub publication — 2026-08-28

Production release `c5915d4321efc45e5be86a84a745395c0a31d259` and acceptance run `33226001121` proved durable publication through `GitHubBroker`.

Accepted evidence included:

```text
TASK_ID=79af58db-2ae4-43e1-b9e0-b0adc6b000ac
TASK_BRANCH=overlord/task-79af58db-2ae4-43e1-b9e0-b0adc6b000ac
PUBLICATION_COMMIT=aece6684ae189c16cb98d613be3dc9cba5819769
DBOS_WORKFLOW_ID=developer-github-publication:79af58db-2ae4-43e1-b9e0-b0adc6b000ac:a726c7b72c4a8524
RETRY_REUSED_RESULT=true
```

Ordered mutation audit:

```text
DEVELOPER_GITHUB_PUBLICATION_PREPARED
github.branch.create.requested
github.branch.create.completed
github.commit_files.requested
github.commit_files.completed
DEVELOPER_GITHUB_PUBLICATION_COMPLETED
```

### Broker-controlled Developer pull-request creation — 2026-08-29

Production release `506d4ad814411044bce771239a9daec9d8d7648a`, deploy run `33265412832`, and acceptance run `33265432312` proved explicit PR creation through `GitHubBroker` with stable DBOS retry behavior.

Long-lived evidence remains:

```text
TASK_ID=3e829b11-7bf6-490d-91f6-4f4c026bdc21
AGENT_RUN_ID=93bd3aae-a51d-4f9f-8417-ab75a1dba160
PULL_REQUEST_NUMBER=61
TASK_BRANCH=overlord/task-3e829b11-7bf6-490d-91f6-4f4c026bdc21
PUBLICATION_COMMIT=92f9655d650ac64c99c6327eaf886ed3fc664052
PULL_REQUEST_STATE=open
PULL_REQUEST_BASE=main
```

PR #61 is still open and unmerged. It was not used for either live merge acceptance.

### Exact-head pull-request check observation — 2026-08-29

Production release `1153368660e2f8e839c279bc9ae789e028985caf` accepted refreshable exact-head check observation. Feature PR #63 and ops PR #64 passed exact-head and post-merge CI; deploy run `33273579895` and acceptance run `33273633409` were successful.

The accepted read path is:

```text
POST /tasks/{task_id}/bounded-developer-pull-request-observations
-> completed canonical publication + PR metadata
-> live PR exact head/base/state verification
-> GitHub check-runs for exact persisted publication SHA
-> latest canonical observation snapshot
-> durable observation audit
```

Observation is intentionally refreshable rather than frozen behind one DBOS result.

### Fail-closed merge evaluation — 2026-08-29

Production release `f07ffa1ac1743a7f75b4415eab2a70852e528e2e` accepted refreshable, non-mutating merge evaluation. Feature PR #65 and ops PR #66 passed exact-head and post-merge CI; deploy run `33277524943` and acceptance run `33277550160` were successful.

Accepted server-owned required-check policy:

```text
required check: quality
observed cardinality: exactly one
live cardinality: exactly one
required status: completed
required conclusion: success
```

Evaluation fails closed on missing, duplicate, pending, neutral, skipped, cancelled, failed or mismatched evidence, and on live PR state/head/base drift.

### Broker-controlled Developer merge mutation — 2026-08-29

Production accepts one explicit bounded Developer merge mutation path.

Implementation PR #67:

```text
final exact head: 95e2c923a2a7c1d4358fecba57ede51238a322fe
exact-head CI:     #564 / run 33280263450 / success
merge:             4db60d9b041eca4a83e0d86bb1d0c7759f7d8b27
post-merge CI:     #565 / run 33280323531 / success
```

Production acceptance support PR #68:

```text
final exact head: 42489aacde33dd4717dfba944126752f9e8d6232
exact-head CI:     #576 / run 33280674185 / success
merge/release:     547275ad50ce34aad6a4a9b1c23428a2113ef8be
post-merge CI:     #578 / run 33282090550 / success
deploy:            #13 / run 33282143267 / success
acceptance:        #1 / run 33282161767 / success
```

The accepted mutation endpoint is:

```text
POST /tasks/{task_id}/bounded-developer-merges
body: {"revision": "<exact source revision>"}
```

The caller cannot choose repository, PR number, branch, base, required checks, expected head SHA, merge method or GitHub credentials.

The merge service performs:

```text
canonical Task / AgentRun / publication / PR validation
-> fresh merge evaluation
-> canonical github_merge state=prepared
-> GitHubBroker.merge_if_allowed
-> broker re-reads live PR + exact-head checks
-> expected head SHA passed to GitHub merge API
-> squash merge
-> live merged-state verification
-> canonical github_merge state=completed
-> durable audit
-> stable DBOS merge result
```

The broker itself independently fails closed on repository/base/head drift, draft/non-mergeable PRs, empty required-check policy, duplicate required-check identities, missing checks, incomplete checks and any required conclusion other than `success`.

Ambiguous mutation recovery is accepted only when a follow-up GitHub read proves that the exact prepared PR/head is already merged and exposes a merge commit SHA. A merely closed PR is not treated as merged.

#### Live merge acceptance evidence

The production probe created a fresh synthetic bounded run and a harmless marker publication; historical PR #61 was left untouched.

```text
SOURCE_REVISION=547275ad50ce34aad6a4a9b1c23428a2113ef8be
TASK_ID=bc9b92d5-5aba-4b41-a3cf-93d4aa38b76a
AGENT_RUN_ID=23ebf425-ca59-46e9-a0de-51d6f5a3fa94
TASK_BRANCH=overlord/task-bc9b92d5-5aba-4b41-a3cf-93d4aa38b76a
PUBLICATION_COMMIT=3e01a2b1ac06e81cf9bb49a1c3e85e4301d8efed
PULL_REQUEST_NUMBER=69
PULL_REQUEST_BASE=main
REQUIRED_CHECK=quality
MERGE_METHOD=squash
MERGE_SHA=f4cc17aeeb22657a1b58aefb0ea99994b5c9b882
MERGE_WORKFLOW_ID=developer-github-merge:bc9b92d5-5aba-4b41-a3cf-93d4aa38b76a:6e2e79f06fd2bb60
MERGE_RETRY_REUSED_RESULT=true
```

PR #69's exact publication head passed canonical CI #579, run `33282170650`, before mutation. The production acceptance then completed successfully and PR #69 was verified closed and merged.

The accepted canonical merge audit suffix is:

```text
DEVELOPER_GITHUB_MERGE_EVALUATED
DEVELOPER_GITHUB_MERGE_EVALUATED
DEVELOPER_GITHUB_MERGE_PREPARED
github.merge.evaluated
github.merge.requested
github.merge.completed
DEVELOPER_GITHUB_MERGE_COMPLETED
```

The first evaluation was the explicit acceptance pre-check; the second was the fresh evaluation performed immediately inside the merge service before preparing mutation.

The repeated merge API call reused the stable DBOS result and did not create a second merge effect. The DBOS merge workflow persisted `SUCCESS`, output and checkpoint evidence.

After mutation, repository `main` advanced exactly to `f4cc17aeeb22657a1b58aefb0ea99994b5c9b882`, and canonical post-mutation CI #580, run `33282215741`, completed fully green on that exact SHA.

### First-class repository delivery reconciliation — 2026-08-29

Post-merge delivery is now canonical relational PostgreSQL state rather than living only in AgentRun metadata.

Implementation PR #70:

```text
final exact head: 589043c186959d5fbe83a86869e141e4bfb4deb9
exact-head CI:     #585 / run 33289935716 / success
merge:             e57a29a30dc5b80e2836072785689bc492dcc6e6
post-merge CI:     #586 / run 33289988975 / success
migration:         0003_repository_deliveries
```

Production acceptance support PR #71:

```text
final exact head: 3a9a628f23523d998ef7dc68f3894f772be5edc5
exact-head CI:     #587 / run 33290111837 / success
merge/release:     fd19f6ce74d8907280fcb019d6cefe16d82adb96
post-merge CI:     #588 / run 33290165959 / success
deploy:            #14 / run 33290221186 / success
acceptance:        #1 / run 33290241151 / success
```

Migration `0003_repository_deliveries` adds one immutable canonical delivery row per Task with relational links to WorkRequest, Plan and AgentRun plus:

```text
source revision
repository
pull request number
head branch / base branch
publication head SHA
merge SHA / merge method
merged status / merged timestamp
```

The durable Developer merge step now returns only after post-merge reconciliation runs. If DBOS retries after GitHub merge completion, the existing merge result is reused and reconciliation is idempotent by Task. Existing delivery identity must match exactly or reconciliation fails closed. `DEVELOPER_GITHUB_DELIVERY_RECONCILED` is emitted only on first creation, so a DBOS step replay cannot create duplicate delivery audit evidence.

Lifecycle reconciliation preserves the existing conservative completion rule:

```text
verified merge
-> canonical repository_deliveries row
-> Task = completed
-> promote newly unblocked tasks
-> Plan = completed only when all plan tasks are completed
-> WorkRequest = completed only when all request tasks are completed
```

#### Live reconciliation acceptance evidence

The acceptance deliberately seeded a fresh synthetic Task in `validation`, its Plan in `active`, and its WorkRequest in `running`, while keeping the bounded AgentRun completed. The normal accepted publication / PR / check / evaluation / merge path then ran unchanged.

```text
SOURCE_REVISION=fd19f6ce74d8907280fcb019d6cefe16d82adb96
TASK_ID=38dd9023-0006-40a1-8b05-84bae8d39aed
AGENT_RUN_ID=dde0a884-b5b1-4701-94cc-01977fb14b5e
TASK_BRANCH=overlord/task-38dd9023-0006-40a1-8b05-84bae8d39aed
PUBLICATION_COMMIT=c48e688936b2b2b505597a81bf28bb2d13e28aa0
PULL_REQUEST_NUMBER=72
PULL_REQUEST_BASE=main
REQUIRED_CHECK=quality
MERGE_METHOD=squash
MERGE_SHA=48fe44579c834554d6de091b79c1d400ad02627c
INITIAL_TASK_STATUS=validation
FINAL_TASK_STATUS=completed
INITIAL_PLAN_STATUS=active
FINAL_PLAN_STATUS=completed
INITIAL_WORK_REQUEST_STATUS=running
FINAL_WORK_REQUEST_STATUS=completed
REPOSITORY_DELIVERY_COUNT=1
RECONCILIATION_AUDIT_COUNT=1
```

PR #72's exact publication head passed canonical CI #589, run `33290256425`, before mutation. The production acceptance completed successfully and verified:

- exactly one relational `repository_deliveries` row for the Task;
- delivery identity matched the accepted AgentRun, source revision, repository, PR #72, branch/base, publication head, merge SHA and squash method;
- exactly one `DEVELOPER_GITHUB_DELIVERY_RECONCILED` audit event with canonical WorkRequest/Task correlation;
- the Task transitioned `validation -> completed`;
- the single-task Plan transitioned `active -> completed`;
- the single-task WorkRequest transitioned `running -> completed`;
- the repeated merge API call reused the stable DBOS result and did not create a second merge or reconciliation audit.

After acceptance, repository `main` advanced exactly to `48fe44579c834554d6de091b79c1d400ad02627c`. Canonical post-mutation CI #590, run `33290312959`, completed fully green on that exact SHA.

The production service remains deployed from `fd19f6ce74d8907280fcb019d6cefe16d82adb96`; `48fe4457...` is the accepted harmless marker merge and has not been separately deployed. Historical evidence PR #61 remains open and unmerged.

## Current authority boundary

The production-proven end-to-end GitHub lifecycle is now:

```text
bounded Developer run
-> canonical host-observed changes
-> broker-controlled task branch + commit
-> broker-controlled PR creation
-> exact-head PR/check observation
-> explicit required-check merge evaluation
-> broker-controlled exact-head squash merge
-> canonical merge completion + stable DBOS result
-> canonical relational repository delivery
-> Task / Plan / WorkRequest lifecycle reconciliation
```

GitHub mutations remain confined to:

```text
GitHubPort -> GitHubBroker -> GitHub App adapter -> durable audit
```

No Developer container receives GitHub App credentials or GitHub mutation authority.

Observation and merge evaluation remain refreshable read/evidence operations. Publication, PR creation and merge mutation use stable DBOS task+revision workflow identities for durable result reuse. PostgreSQL is canonical for lifecycle and delivery state.

## Next stage

The core single-host GitHub lifecycle and post-merge delivery reconciliation are production-proven. The next slices should focus on orchestration and operational hardening rather than another mutation primitive.

Priority candidates:

1. connect run -> publish -> PR -> observe -> evaluate -> merge -> reconcile into one explicit Manager-controlled lifecycle with clear human/automation policy boundaries;
2. change GitHub-backed bounded execution semantics so successful code execution moves the Task to `validation` rather than prematurely to `completed`, then let verified delivery reconciliation own final completion;
3. define cleanup/retention policy for merged task branches and acceptance markers;
4. add production evidence for controlled failure/recovery around an interrupted merge/reconciliation workflow without weakening exact-head checks;
5. continue model-neutral Developer replay/cost-routing work separately from GitHub mutation authority;
6. keep remote Developer workers deferred until workload evidence justifies them.

## Verification record

- Last verified: `2026-08-29`.
- Current deployed production release: `fd19f6ce74d8907280fcb019d6cefe16d82adb96`.
- Current accepted repository `main`: `48fe44579c834554d6de091b79c1d400ad02627c`.
- Latest deploy: #14 / run `33290221186`, success.
- Latest production acceptance: repository delivery reconciliation #1 / run `33290241151`, success.
- Accepted reconciliation implementation: PR #70; exact-head CI #585 / `33289935716`; merge `e57a29a30dc5b80e2836072785689bc492dcc6e6`; post-merge CI #586 / `33289988975`.
- Accepted reconciliation support/release: PR #71; exact-head CI #587 / `33290111837`; release `fd19f6ce74d8907280fcb019d6cefe16d82adb96`; post-merge CI #588 / `33290165959`.
- Live reconciliation PR #72: exact head `c48e688936b2b2b505597a81bf28bb2d13e28aa0`; CI #589 / `33290256425`; merged by Overlord to `48fe44579c834554d6de091b79c1d400ad02627c`; post-mutation CI #590 / `33290312959` green.
- Canonical delivery evidence: exactly one `repository_deliveries` row and exactly one `DEVELOPER_GITHUB_DELIVERY_RECONCILED` audit for the live Task.
- Historical evidence PR #61 remains open and unmerged.
- Accepted required-check policy: exactly one `quality` check, `completed/success`, matched in canonical observation and fresh live GitHub evidence.
- Security verification: no Docker socket, AWS credential, GitHub App private key, installation token or GitHub mutation authority entered a Developer container.
- Verified by: High Director.
