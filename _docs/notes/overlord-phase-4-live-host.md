---
title: Overlord Phase 4 — Live MVP Host
summary: Live deployment record for the first single-host Overlord MVP on DigitalOcean.
section: notes
doc_type: note
status: active
created: 2026-08-19
updated: 2026-08-30
last_verified: 2026-08-30
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

The first always-on Overlord MVP host is running on DigitalOcean.

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
current deployed release:   c7219bd983432e787ee543ba6691e8db528e53a9
current repository main:    cd06bf5c1df7353f984a343b9969f1da702bc5a3
```

The production architecture is:

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

## Production-proven lifecycle

The current end-to-end lifecycle is:

```text
bounded Developer execution
-> AgentRun = completed
-> Task = validation
-> durable publication
-> durable pull-request creation
-> refresh exact-head check observation
-> refresh fail-closed merge evaluation
-> await exact owner merge approval
-> preflight approval before stable DBOS merge workflow creation
-> durable broker-controlled exact-head squash merge
-> canonical repository delivery
-> Task = completed
-> dependent-task promotion
-> Plan / WorkRequest completion when all tasks are complete
```

GitHub mutation authority remains confined to:

```text
GitHubPort -> GitHubBroker -> GitHub App adapter -> durable audit
```

The caller cannot choose repository, PR number, branch, base, required checks, expected head SHA, merge method or GitHub credentials.

## Accepted live milestones

### Local disposable Developer execution

Production proved disposable Docker -> OpenCode -> OpenAI execution, evidence/usage collection and automatic cleanup. Only the model credential enters the Developer container.

### GitHub App broker/audit path

Production proved AWS Secrets Manager -> GitHub App JWT -> short-lived installation token -> GitHub API -> GitHubBroker -> durable audit. Initial acceptance was deliberately fail-closed and non-mutating.

### DBOS-backed bounded Developer execution

Release `00d6472a3c006d2502ea1bd50a695028add9e3c4`, acceptance `33218577873`, proved stable task+revision workflow identity, one canonical AgentRun, DBOS `SUCCESS` with checkpoint/output, PostgreSQL canonical state and cleanup.

### Bounded Developer GitHub publication

Release `c5915d4321efc45e5be86a84a745395c0a31d259`, acceptance `33226001121`, proved durable publication through `GitHubBroker`.

```text
TASK_ID=79af58db-2ae4-43e1-b9e0-b0adc6b000ac
TASK_BRANCH=overlord/task-79af58db-2ae4-43e1-b9e0-b0adc6b000ac
PUBLICATION_COMMIT=aece6684ae189c16cb98d613be3dc9cba5819769
DBOS_WORKFLOW_ID=developer-github-publication:79af58db-2ae4-43e1-b9e0-b0adc6b000ac:a726c7b72c4a8524
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

### Broker-controlled pull-request creation

Release `506d4ad814411044bce771239a9daec9d8d7648a`, deploy `33265412832`, acceptance `33265432312`, proved explicit PR creation through `GitHubBroker` with stable DBOS retry behavior.

Historical evidence PR #61 remains open and unmerged:

```text
TASK_ID=3e829b11-7bf6-490d-91f6-4f4c026bdc21
AGENT_RUN_ID=93bd3aae-a51d-4f9f-8417-ab75a1dba160
PULL_REQUEST_NUMBER=61
PUBLICATION_COMMIT=92f9655d650ac64c99c6327eaf886ed3fc664052
```

### Exact-head observation and fail-closed merge evaluation

Production accepted refreshable exact-head check observation and non-mutating merge evaluation. Required-check policy is server-owned and exactly:

```text
required check: quality
observed cardinality: exactly one
live cardinality: exactly one
required status: completed
required conclusion: success
```

Missing, duplicate, pending, neutral, skipped, cancelled, failed or mismatched evidence denies merge.

### Broker-controlled merge mutation

Implementation PR #67 and production support PR #68 established the durable exact-head squash merge path. Production acceptance proved fresh evaluation immediately before mutation, broker re-read of live PR/checks, exact expected head SHA, ambiguous-response recovery only when GitHub proves the exact prepared PR/head merged, stable DBOS result reuse and ordered durable audit.

### First-class repository delivery reconciliation

Implementation PR #70 added migration `0003_repository_deliveries`; production support PR #71 and acceptance `33290241151` proved exactly one relational delivery row per Task and final lifecycle reconciliation.

```text
verified merge
-> canonical repository_deliveries row
-> Task = completed
-> promote newly unblocked tasks
-> Plan = completed only when all plan tasks are completed
-> WorkRequest = completed only when all request tasks are completed
```

Live acceptance Task `38dd9023-0006-40a1-8b05-84bae8d39aed` transitioned `validation -> completed`; repository `main` advanced to `48fe44579c834554d6de091b79c1d400ad02627c`; post-mutation CI #590 / `33290312959` was green.

### Bounded execution validation lifecycle

Implementation PR #73 changed successful repository-backed bounded execution so execution completion no longer means repository delivery completion.

```text
bounded execution succeeds
-> AgentRun = completed
-> Task = validation
-> Task.completed_at = null
-> Plan remains active
-> WorkRequest remains running
-> dependencies remain blocked
-> repository_deliveries count = 0
```

Production support PR #74, release `dff7b585f721b333e17662b042b29b33fbecccef`, deploy #15 / `33325022603`, acceptance #2 / `33325045425`, proved the boundary with no repository diff and clean workspace/container teardown.

## Manager-controlled delivery and owner approval — 2026-08-30

### Manager preparation and approval policy

Feature PR #75 added the first explicit Manager-controlled delivery preparation surface.

```text
final exact head: 0c1f8e78f0bf41c54df742ba7dc1264e7ec6b1cb
exact-head CI:     #607 / run 33331859373 / success
merge:             f71d2447d70e5e02a21721eccd41f4cea81a917e
post-merge CI:     #608 / run 33331922088 / success
```

`POST /tasks/{task_id}/bounded-developer-deliveries` composes the existing durable bounded execution, publication and PR creation stages. Repeated calls reuse their stable task+revision DBOS results while exact-head observation and merge evaluation refresh. The endpoint returns either `awaiting_checks` or `awaiting_owner_approval` and never performs merge mutation.

`POST /tasks/{task_id}/bounded-developer-merge-approvals` records canonical owner approval only after a fresh eligible merge evaluation. Approval is exact to Task + AgentRun + source revision, idempotent, and represented by exactly one:

```text
OWNER_DEVELOPER_MERGE_APPROVED
```

Duplicate matching approvals fail closed.

The direct merge path also requires the exact approval, so the preparation/approval policy cannot be bypassed by calling the merge endpoint directly.

### Initial production acceptance and safe failure

Production support PR #76:

```text
final exact head: 88ffc4f238bcfcc68a7a6a2354f6b059f9c34fec
exact-head CI:     #615 / run 33347854431 / success
merge/release:     0719d46d0da5ada3114da1bfcec0b741f68e71c6
post-merge CI:     #616 / run 33347931319 / success
deploy:            #16 / run 33348005697 / success
```

Initial Manager acceptance #1 / run `33348043526` failed safely and exposed a DBOS ordering bug. It created PR #77 but did not merge it.

```text
TASK_ID=8857fe7f-a689-4f5b-a2ce-3df11901ae21
AGENT_RUN_ID=b85677d8-94c0-48f6-a9bd-710a895142f0
PULL_REQUEST_NUMBER=77
PUBLICATION_COMMIT=31a466690404a4e1a0525387c9d8054f8a5870c6
PR_EXACT_HEAD_CI=#617 / run 33348061572 / success
OWNER_APPROVAL_COUNT=1
TASK_STATUS=validation
GITHUB_MERGE_STATE=none
PR_STATE=open
PR_MERGED=false
MAIN_UNCHANGED=true
```

Read-only diagnostic run `33348239014` proved the ordered tail ended after owner approval and another evaluation, before `DEVELOPER_GITHUB_MERGE_PREPARED`.

Root cause:

```text
pre-approval merge request
-> stable developer-github-merge:{task}:{revision-digest} workflow started
-> approval check failed inside workflow
-> stable workflow ID persisted failed result
-> owner approval later recorded
-> same stable workflow ID replayed prior failure
-> merge preparation never started
```

This was fail-closed—no GitHub merge mutation occurred—but it poisoned that Task+revision merge workflow ID.

PR #77 remains open and unmerged as failed-safe evidence. It must not be manually merged.

### Stable-workflow preflight fix

Fix PR #78 moved approval preflight ahead of stable DBOS merge workflow creation while retaining the in-workflow approval check as defense in depth.

```text
final exact head: 2d4b0ae3b27cdbfd4299bbe00a6b2e79140030f9
exact-head CI:     #622 / run 33348551513 / success
merge/release:     c7219bd983432e787ee543ba6691e8db528e53a9
post-merge CI:     #623 / run 33348664176 / success
deploy:            #17 / run 33348732528 / success
```

The accepted ordering is now:

```text
merge API request
-> read-only exact owner-approval preflight
-> if absent: HTTP 409 and NO stable DBOS merge workflow row
-> if present: assign/start stable developer-github-merge workflow
-> in-workflow owner-approval recheck
-> fresh merge evaluation
-> github_merge = prepared
-> GitHubBroker final gate
-> exact-head squash merge
-> reconciliation
```

Regression coverage explicitly requires a denied preflight to leave `dbos.workflow_status` with zero rows for that stable merge workflow ID.

### Successful fixed production acceptance

Fresh Manager approval acceptance #4 / run `33348756583` completed successfully on deployed release `c7219bd983432e787ee543ba6691e8db528e53a9`.

```text
SOURCE_REVISION=c7219bd983432e787ee543ba6691e8db528e53a9
TASK_ID=4473d316-720a-44cf-9fd7-4904629983bd
AGENT_RUN_ID=ed9ba700-c573-48d2-8f6d-c0a5b47dc5d9
PULL_REQUEST_NUMBER=79
TASK_BRANCH=overlord/task-4473d316-720a-44cf-9fd7-4904629983bd
PUBLICATION_COMMIT=23f911dddfceab4242a06ea931a83fb609c56104
PR_EXACT_HEAD_CI=#624 / run 33348770013 / success
MERGE_SHA=cd06bf5c1df7353f984a343b9969f1da702bc5a3
POST_MUTATION_CI=#625 / run 33348842082 / success
```

The task+revision digest is `aa2b3ef888c38f26`, giving the durable workflow identities:

```text
bounded-developer:4473d316-720a-44cf-9fd7-4904629983bd:aa2b3ef888c38f26
developer-github-publication:4473d316-720a-44cf-9fd7-4904629983bd:aa2b3ef888c38f26
developer-github-pull-request:4473d316-720a-44cf-9fd7-4904629983bd:aa2b3ef888c38f26
developer-github-merge:4473d316-720a-44cf-9fd7-4904629983bd:aa2b3ef888c38f26
```

The successful production probe required and therefore proved:

- repeated Manager preparation reused the same bounded AgentRun, PR number and publication head while refreshing checks/evaluation;
- pre-approval merge returned HTTP 409 with PR and `main` unchanged;
- the pre-approval denial did not create the stable DBOS merge workflow;
- approval was exact to the Task, AgentRun and source revision;
- repeated approval reused exactly one canonical approval event;
- repeated merge reused one stable DBOS merge result;
- bounded, publication, PR and merge workflows each persisted `SUCCESS`, output and checkpoint evidence;
- merge remained squash-only and exact-head;
- exactly one canonical repository delivery was persisted;
- Task, Plan and WorkRequest reconciled to `completed`;
- GitHub `main` advanced exactly to `cd06bf5c1df7353f984a343b9969f1da702bc5a3`;
- normal post-mutation CI #625 / `33348842082` completed fully green on that exact SHA.

The production host remains deployed from `c7219bd983432e787ee543ba6691e8db528e53a9`. The later `cd06bf5c...` commit is the accepted harmless marker merge and has not been separately deployed.

## Current policy boundary

The production-proven Manager policy is now:

```text
automatic / durable:
  bounded execution
  publication
  PR creation
  exact-head observation
  merge evaluation

gated by owner:
  canonical exact merge approval

mutation after approval:
  approval preflight before DBOS workflow creation
  in-workflow approval recheck
  fresh merge evaluation
  GitHubBroker exact-head gate
  squash merge
  repository-delivery reconciliation
```

A missing approval cannot create or poison the stable merge workflow. Approval itself does not weaken any exact-head or required-check gate.

## Next stage

The core single-host Developer delivery lifecycle is production-proven through explicit owner approval and post-merge reconciliation. Priority next slices:

1. add a first-class Manager delivery status/read model so clients do not need to infer state from several stage endpoints;
2. define cleanup/retention policy for merged task branches, failed acceptance branches and harmless acceptance markers;
3. add controlled failure/recovery acceptance around interruption after approval but before/after merge preparation;
4. continue model-neutral Developer replay/cost-routing work separately from GitHub mutation authority;
5. keep remote Developer workers deferred until workload evidence justifies them.

## Verification record

- Last verified: `2026-08-30`.
- Current deployed production release: `c7219bd983432e787ee543ba6691e8db528e53a9`.
- Current accepted repository `main`: `cd06bf5c1df7353f984a343b9969f1da702bc5a3`.
- Manager orchestration feature: PR #75; CI #607 / `33331859373`; merge `f71d2447d70e5e02a21721eccd41f4cea81a917e`; post-main CI #608 / `33331922088`.
- Manager production support: PR #76; CI #615 / `33347854431`; release `0719d46d0da5ada3114da1bfcec0b741f68e71c6`; post-main CI #616 / `33347931319`; deploy #16 / `33348005697`.
- Failed-safe Manager acceptance: #1 / `33348043526`; PR #77 open/unmerged; exact-head CI #617 / `33348061572` green; one approval; no merge preparation; `main` unchanged.
- Stable-workflow fix: PR #78; final head `2d4b0ae3b27cdbfd4299bbe00a6b2e79140030f9`; CI #622 / `33348551513`; release `c7219bd983432e787ee543ba6691e8db528e53a9`; post-main CI #623 / `33348664176`; deploy #17 / `33348732528`.
- Successful Manager acceptance: #4 / `33348756583`; Task `4473d316-720a-44cf-9fd7-4904629983bd`; AgentRun `ed9ba700-c573-48d2-8f6d-c0a5b47dc5d9`; PR #79; publication head `23f911dddfceab4242a06ea931a83fb609c56104`; PR CI #624 / `33348770013`; merge `cd06bf5c1df7353f984a343b9969f1da702bc5a3`; post-mutation CI #625 / `33348842082` green.
- Historical evidence PR #61 remains open and unmerged.
- Failed-safe evidence PR #77 remains open and unmerged.
- Accepted required-check policy remains exactly one `quality` check, `completed/success`, matched in canonical observation and fresh live GitHub evidence.
- Security verification remains unchanged: no Docker socket, AWS credential, GitHub App private key, installation token or GitHub mutation authority entered a Developer container.
- Verified by: High Director.
