---
title: Overlord Phase 4 — Live MVP Host
summary: Live deployment record for the single-host Overlord MVP on DigitalOcean.
section: notes
doc_type: note
status: active
created: 2026-08-19
updated: 2026-08-31
last_verified: 2026-08-31
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

The always-on Overlord MVP is running on one DigitalOcean host. The hardening/infrastructure foundation is integrated and production-accepted, and post-acceptance repository housekeeping, offline replay verification, and the fail-closed Stage 0 replay preflight foundation are complete.

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
current deployed release:   953580c06d064f44c98dd73c3c59affc35579218
current repository main:    fecae0c61b2190405f1d133bd130a51ff40a460d
```

`main` is intentionally ahead of the deployed release only by repository operations/documentation and GitHub-hosted replay/benchmark-preflight tooling. No production runtime/application behavior changed after `953580c06d064f44c98dd73c3c59affc35579218`, so no additional production restart/deployment was required merely for SHA symmetry.

Canonical architecture remains intentionally single-host:

```text
PostgreSQL
  -> canonical Conversation / WorkRequest / Plan / Task / AgentRun / audit state
  -> canonical repository_deliveries

DBOS
  -> durable workflow coordination/checkpoint/output
  -> NOT canonical Task/AgentRun/delivery state

Developer execution
  -> disposable local Docker container
  -> OpenCode
  -> OpenAI

GitHub mutation authority
  -> GitHubPort
  -> GitHubBroker
  -> GitHub App adapter
  -> durable audit
```

Remote Developer workers remain deferred. No EC2/IAM/distributed redesign is part of this milestone.

## Host and security boundary

Administrative SSH uses a passphrase-protected Ed25519 key. The host has a separate read-only repository deploy key. A repository-level self-hosted GitHub Actions runner named `overlord-prod-01` is installed as a systemd service and is used only by manually dispatched production operational workflows. Normal pull-request and `main` CI run on GitHub-hosted runners.

PostgreSQL 17 runs in Docker and binds only to host loopback. The Overlord control plane runs as an enabled systemd service and binds only to `127.0.0.1:8000`. Production source is root-managed under `/opt/overlord-source`, deployed code is `/opt/overlord/current`, runtime environment is `/etc/overlord/overlord.env`, and Developer workspaces are rooted at `/var/lib/overlord/workspaces`.

The production control plane obtains GitHub App authority through:

```text
DigitalOcean Overlord
-> narrowly scoped AWS IAM identity
-> AWS Secrets Manager us-east-2
-> overlord/production/github-app
```

Developer containers receive only the model credential needed for bounded execution. They do not receive the Docker socket, GitHub App private key, installation token, AWS credentials, PostgreSQL credentials, SSH private keys, broad host filesystem access, or broad Linux privileges.

## Production-proven delivery lifecycle

The current accepted end-to-end lifecycle is:

```text
bounded Developer execution
-> AgentRun = completed
-> Task = validation
-> durable publication
-> durable PR creation
-> exact-head check observation
-> fail-closed merge evaluation
-> awaiting owner approval
-> exact owner approval
-> approval preflight BEFORE stable DBOS merge workflow creation
-> in-workflow approval recheck
-> fresh merge evaluation
-> GitHubBroker exact-head gate
-> squash merge
-> repository_delivery reconciliation
-> Task = completed
-> dependent-task promotion
-> Plan / WorkRequest completion when appropriate
-> PostgreSQL-first Manager delivery-status view
```

The required merge check remains exactly:

```text
quality = completed/success
```

Missing, duplicate, pending, failed, cancelled, skipped, neutral, stale, or mismatched check evidence denies merge.

Successful bounded Developer execution does not complete repository-backed work. It stops at:

```text
AgentRun = completed
Task = validation
Task.completed_at = null
```

Final completion happens only after verified repository delivery.

## Hardening and infrastructure foundation

The integrated hardening streams remain:

- interrupted merge-delivery recovery through PR #83;
- conservative repository branch retention through PR #84;
- model-neutral six-case replay harness through PR #85; and
- operational hygiene/observability through PR #82 plus integration PR #86.

The combined production release reached `953580c06d064f44c98dd73c3c59affc35579218`, with final production deploy #22 / `33356627581` and read-only operations/retention acceptance #2 / `33356648604` both successful.

Historical evidence PR #61 remains open and unmerged. Failed-safe evidence PR #77 remains open and unmerged. Neither is a cleanup target.

## Post-acceptance housekeeping and replay verification

### Conservative Actions-registry housekeeping

A first conservative registry-cleanup batch disabled 15 clearly orphaned Actions workflow registrations while preserving their historical runs. No current workflow file was deleted, no production workflow was disabled, and PR #61/#77 evidence remained untouched.

```text
PR:                 #90
exact PR head:      5fbf4feb2ce3d36e17f26e000f15e896d0e5962e
exact-head CI:      #683 / run 33360707598 / success
merge:              acca895e7bdb36d6c2418a97c87e8a591828d06b
post-main CI:       #684 / run 33360800608 / success
```

A later read-only audit positively recovered six additional historical registrations but marked them `AMBIGUOUS`, not safe to disable, because the available GitHub workflow-registry connector exposes only the first 30 of 47 registrations and does not support pagination. No additional workflow IDs were guessed or disabled.

The intentionally disabled current workflow `developer-benchmark-real.yml` remains `KEEP`; it exists on `main` and is legacy benchmark support, not the provider-neutral replay runner.

### Six-case offline replay verification

PR #91 added a GitHub-hosted offline verification workflow for the integrated six-case historical replay corpus. It fetches full repository history, validates each frozen base revision, prepares a disposable detached Git workspace for each case, asserts `live_model_calls = 0`, and uploads only non-secret JSONL evidence.

```text
PR:                  #91
exact PR head:       6a24ed84d989dd022ec2ae6c4ec7909718cfbcbb
exact-head CI:       #685 / run 33361041848 / success
merge:               59ed0afd17e7c44addaa8143230f3c274ea09200
post-main CI:        #686 / run 33361127417 / success
offline verification:#1 / run 33361246871 / success
```

Offline verification #1 prepared all six frozen cases successfully:

```text
2 Easy
2 Medium
2 Hard
live model calls = 0
provider secrets used = none
paid benchmark dispatched = no
production routing changed = no
```

### Fail-closed Stage 0 replay preflight

A read-only benchmark design audit identified a critical control limitation before any paid benchmark was attempted: the current OpenCode adapter can report aggregate runtime usage/cost after execution, but cannot enforce a true pre-spend ceiling on underlying model turns. Post-hoc accounting is therefore not treated as a hard budget.

PR #92 added a provider-neutral Stage 0 policy, CLI, unit coverage, and a manually dispatched GitHub-hosted preflight workflow. The policy is limited to one Easy replay case and one Developer task attempt. A paid request requires an explicit reported-cost ceiling and a genuinely enforceable pre-spend control; because the current runtime layer does not provide such a control, paid execution remains fail-closed.

```text
PR:                  #92
final exact PR head: 68f82e01e21d966035f82c6c05fb06ae8e9ab5b4
exact-head CI:       #710 / run 33412632018 / success
merge:               fecae0c61b2190405f1d133bd130a51ff40a460d
post-main CI:        #711 / run 33412790577 / success
Stage 0 preflight:   #1 / run 33412946519 / success
```

The successful Stage 0 preflight proved:

```text
non-billable Easy-1 request = allowed
paid authorization flag = accepted as input
reported-cost ceiling = required for paid request
enforceable pre-spend control = absent
paid execution = denied fail-closed
live model calls = 0
provider secrets used = none
production routing changed = no
GitHub mutation authority used = no
production deployment = no
```

This establishes a truthful boundary: Stage 0 paid benchmarking must not proceed until the runtime/provider layer can enforce spend before inference. Runtime-reported cost/token evidence remains necessary for benchmark evidence, but it is not sufficient by itself to authorize a paid run.

## Current policy boundary

The production-proven Manager policy remains unchanged:

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
  approval preflight before stable DBOS workflow creation
  in-workflow approval recheck
  fresh merge evaluation
  GitHubBroker exact-head gate
  squash merge

recovery/reconciliation:
  stable durable merge result reused
  PostgreSQL reconciliation retried separately
  no second GitHub merge on reconciliation retry

read-only status/operations:
  PostgreSQL-first lifecycle snapshot
  sanitized operator status
  exact deployed release marker
  retention candidate discovery/protection evidence
  no GitHub mutation required
```

PostgreSQL remains canonical application state. DBOS remains durable coordination state. GitHub mutations remain confined to `GitHubPort -> GitHubBroker -> GitHub App -> durable audit`.

## Next stage

The next meaningful engineering question is no longer whether the replay harness works offline; it does. The blocker before any paid Stage 0 benchmark is a genuine enforceable pre-spend control.

Recommended order:

1. keep production on `953580c06d064f44c98dd73c3c59affc35579218`; repository `main` is ahead only by non-runtime benchmark/operations tooling;
2. investigate provider-side or runtime-side mechanisms that can enforce spend before inference, without weakening Developer isolation or introducing GitHub/production mutation authority;
3. reject controls that are merely post-hoc accounting or advisory limits;
4. only after an enforceable pre-spend control exists, authorize the smallest paid Stage 0 run against one Easy replay case;
5. require complete runtime-reported token/cost evidence and validator result before expanding to more models/cases;
6. require repeated six-case evidence before considering any production routing change; and
7. keep remote Developer workers and broader product phases as separate architecture/product decisions.

Do not enable the legacy real benchmark workflow, run a paid benchmark, change production model routing, run destructive retention cleanup, or redesign the single-host architecture merely because the preflight foundation exists.

## Verification record

- Last verified: `2026-08-31`.
- Current deployed production release: `953580c06d064f44c98dd73c3c59affc35579218`.
- Current repository `main`: `fecae0c61b2190405f1d133bd130a51ff40a460d`.
- Repository `main` is ahead of production only by non-runtime operations/replay/benchmark-preflight tooling; no additional deployment is required.
- Final production deploy: #22 / `33356627581` / success.
- Final production read-only operations/retention acceptance: #2 / `33356648604` / success.
- Workflow-registry housekeeping: PR #90; CI #683 / `33360707598`; merge `acca895e7bdb36d6c2418a97c87e8a591828d06b`; post-main CI #684 / `33360800608`.
- Offline replay verification: PR #91; CI #685 / `33361041848`; merge `59ed0afd17e7c44addaa8143230f3c274ea09200`; post-main CI #686 / `33361127417`; offline verification #1 / `33361246871` success with six cases prepared and zero live model calls.
- Stage 0 preflight: PR #92; final head `68f82e01e21d966035f82c6c05fb06ae8e9ab5b4`; exact-head CI #710 / `33412632018`; merge `fecae0c61b2190405f1d133bd130a51ff40a460d`; post-main CI #711 / `33412790577`; preflight #1 / `33412946519` success with paid execution denied fail-closed and zero live model calls.
- Historical evidence PR #61 remains open and unmerged.
- Failed-safe evidence PR #77 remains open and unmerged.
- Required-check policy remains exactly one `quality` check in `completed/success` state, matched to the exact head.
- Production Developer routing was not changed and no paid replay benchmark was run.
- The legacy real Developer benchmark remains intentionally disabled and must not be mistaken for the provider-neutral six-case replay experiment.
- Security boundary remains unchanged: no Docker socket, AWS credential, GitHub App private key, installation token, PostgreSQL credential, or GitHub mutation authority entered a Developer container.
- Verified by: High Director.
