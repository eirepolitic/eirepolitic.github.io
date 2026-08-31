---
title: Overlord Phase 4 — Live MVP Host
summary: Live deployment record for the single-host Overlord MVP on DigitalOcean.
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

The always-on Overlord MVP is running on one DigitalOcean host. The hardening/infrastructure foundation is integrated and production-accepted, and post-acceptance repository housekeeping plus offline replay verification are complete.

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
current repository main:    59ed0afd17e7c44addaa8143230f3c274ea09200
```

`main` is intentionally ahead of the deployed release only by repository operations/documentation and a GitHub-hosted offline replay-verification workflow. No production runtime/application behavior changed after `953580c06d064f44c98dd73c3c59affc35579218`, so no additional production restart/deployment was required merely for SHA symmetry.

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

## Earlier accepted milestones

The single-host lifecycle was established incrementally before the final hardening integration:

- DBOS-backed bounded Developer execution was accepted on release `00d6472a3c006d2502ea1bd50a695028add9e3c4`, run `33218577873`.
- Durable Developer publication was accepted on release `c5915d4321efc45e5be86a84a745395c0a31d259`, run `33226001121`.
- Broker-controlled PR creation was accepted on release `506d4ad814411044bce771239a9daec9d8d7648a`, deploy `33265412832`, acceptance `33265432312`.
- Exact-head observation and fail-closed merge evaluation established the exact one-`quality`-check policy.
- Broker-controlled exact-head squash merge was implemented through PRs #67/#68.
- Canonical relational `repository_deliveries` and final lifecycle reconciliation were implemented through PRs #70/#71 and accepted by run `33290241151`.
- Repository-backed bounded execution was corrected so successful execution ends in `Task = validation`; release `dff7b585f721b333e17662b042b29b33fbecccef`, deploy #15 / `33325022603`, acceptance #2 / `33325045425`.
- Manager delivery preparation/approval was added by PR #75.
- Initial Manager acceptance `33348043526` failed safely and retained PR #77 as evidence: one approval, no merge preparation, no merge mutation, and unchanged `main`.
- PR #78 fixed the stable-DBOS-workflow poisoning issue by moving approval preflight before stable merge workflow creation; release `c7219bd983432e787ee543ba6691e8db528e53a9`, deploy #17 / `33348732528`.
- Successful fixed Manager approval acceptance #4 / `33348756583` merged PR #79 and proved stable stage reuse, pre-approval 409 with no stable merge workflow row, exact owner approval, broker merge, canonical delivery, and green post-mutation CI.
- PR #80 added the PostgreSQL-first Manager delivery status view; PR #81 released `e941d40916cd36dff927d7ffcc2b80b3a714fd26`, deploy #18 / `33350169371`, read-only acceptance #1 / `33350198239`.

Historical evidence PR #61 remains open and unmerged. Failed-safe evidence PR #77 remains open and unmerged. Neither is a cleanup target.

## Hardening and infrastructure foundation — 2026-08-30

Four parallel engineering workstreams were integrated sequentially with exact-head CI before each merge and fully green `main` after each merge.

### Interrupted merge-delivery recovery

PR #83 hardened the merge/reconciliation recovery boundary.

```text
worker exact head: 80ce8135a7d10bf25d05cf4a35dfbe196663b648
worker CI:         #641 / run 33351770700 / success
merge:             2de0d46ae6876f1fc6073b1251ac8cc20a56ff98
post-main CI:      #671 / run 33353992544 / success
```

The stable Task+revision DBOS merge workflow now owns the durable merge result only. PostgreSQL repository-delivery reconciliation is retried separately and idempotently.

Accepted recovery properties:

```text
owner approval preflight before stable workflow creation
-> stable merge workflow
-> durable merge result
-> retryable PostgreSQL reconciliation
```

A reconciliation failure cannot replay the GitHub merge workflow. Repeated calls reuse the durable merge result and rerun only idempotent reconciliation. PostgreSQL `repository_deliveries` remains canonical, and GitHubBroker authority is unchanged.

The critical DBOS rule remains:

```text
pre-approval merge request
-> HTTP 409
-> NO stable developer-github-merge workflow row
```

No broad `DBOS.reset_system_database(truncate=True)` workaround was introduced.

### Conservative repository branch retention

PR #84 added conservative branch-retention authority without exposing arbitrary branch deletion.

```text
worker exact head: 6c53e8a540bead52963f355ea2946a89b2864aa3
worker CI:         #670 / run 33352746709 / success
merge:             b1b7909ee94630c1ca1970e57d2f865f170d4548
post-main CI:      #672 / run 33354266550 / success
```

Retention remains server-derived:

```text
canonical repository_delivery state
-> age/eligibility query
-> revalidate merged PR identity/head/base/repository
-> verify no open-PR dependency
-> GitHubPort
-> GitHubBroker
-> GitHub App exact-head deletion
-> durable audit
```

The broker independently rejects `main`, allowed base/protected branches, malformed or non-Overlord task branch names, non-allowlisted repositories, and historical evidence branches. PR #61 and PR #77 protections are enforced in code and tests, not only documentation.

No production historical branch cleanup was performed during integration or acceptance.

### Model-neutral Developer replay harness

PR #85 integrated an offline replay/cost-routing foundation without changing production model routing.

```text
worker exact head: 2e8f3563dab388e23795538806443f60817b6ad6
worker CI:         #666 / run 33352596705 / success
merge:             a8ba17cb4692ee1ec0dd8d7ba5ef8653982bb6ea
post-main CI:      #673 / run 33354726677 / success
```

The harness freezes six Easy/Medium/Hard historical Developer cases with exact base SHAs, manifest fingerprints, declared validators, and constrained runtime/provider/model inputs. Runs use disposable detached Git workspaces, evaluator-side subprocess validators, and canonical AgentRun/ModelCall attribution based on runtime-reported usage.

The prepare-only command performs no live model call. No model prices were invented. No paid multi-model benchmark was run, and the production Developer model/routing configuration was not changed.

### Operational hygiene and observability

PR #82 landed last so repository-facing operations documentation reflects the integrated hardening state.

An integration correction was applied through PR #86 because the worker README/inventory still described the already-merged hardening streams as future parallel work.

```text
integration PR #86 head: 82e4c61d221e84453cfef77d8501a8c74cea0a4b
integration CI:          #674 / run 33354940002 / success
updated PR #82 head:     c40df3994ce2280ad4359e67bf3690dc3812325b
fresh PR #82 CI:         #675 / run 33355008056 / success
merge:                   226c16d555503bcabdebdce987c8e07ae93f67d2
post-main CI:            #676 / run 33355079769 / success
```

The operator status path is read-only and sanitized. It reports high-level environment/release/PostgreSQL readiness/execution-control-plane mode without printing secret values. Deployment writes the already-verified exact target SHA to root-owned `.overlord-release`, while preserving existing source-SHA guards, `.venv` handling, restart behavior, and `/health`/`/ready` polling.

## Combined production deployment and acceptance

The first combined hardening release was deployed as:

```text
release: 226c16d555503bcabdebdce987c8e07ae93f67d2
deploy:  #19 / run 33355428598 / success
```

### Recovery-compatible Manager delivery acceptance

Manager delivery approval acceptance #5 / run `33355914565` ran on deployed `226c16d555503bcabdebdce987c8e07ae93f67d2`.

It created one disposable acceptance PR #87:

```text
PR:                 #87
exact PR head:      eed2883d80ebfcbce61d3955a04bb001484933d4
exact-head CI:      #677 / run 33355938369 / success
resulting main:     0cae6146697e3f8fe2b40d958b6a7b2f412817b2
post-main CI:       #678 / run 33356022649 / success
redeploy:           #20 / run 33356093702 / success
```

The production acceptance proved the normal path still preserves the recovery guarantee:

```text
pre-approval merge request
-> 409
-> no stable DBOS merge workflow row
-> one exact owner approval
-> exact-head eligible merge
-> one GitHub merge
-> durable merge-result reuse
-> canonical repository_delivery reconciliation
-> completed lifecycle
```

### Read-only operator/release and retention acceptance

PR #88 added a deliberately read-only self-hosted production acceptance for the new operational visibility and retention foundation.

```text
PR #88 exact head: a1f95772a7fdbb1a84e7ca43e12ba326494dcd88
PR CI:              #679 / run 33356199964 / success
merge:              283d250298a719e1ecd750774cf2c721c635d4ef
post-main CI:       #680 / run 33356275931 / success
deploy:             #21 / run 33356343624 / success
```

Initial acceptance run `33356371113` failed safely before the probe executed. The exact deployed-release guard attempted to read the protected root-owned `.overlord-release` marker as the `github-runner` account. No GitHub mutation, retention cleanup, model call, or DBOS workflow occurred.

PR #89 fixed only that read boundary by using privileged read access while preserving the exact-SHA comparison.

```text
PR #89 exact head: 1c3c11ab494ee64e7ced9de898f4210ecbb8b884
PR CI:              #681 / run 33356457873 / success
merge/final release:953580c06d064f44c98dd73c3c59affc35579218
post-main CI:       #682 / run 33356548175 / success
deploy:             #22 / run 33356627581 / success
acceptance:         #2 / run 33356648604 / success
```

The successful read-only acceptance required:

```text
/opt/overlord-source exact SHA == workflow SHA
/opt/overlord/current/.overlord-release == workflow SHA
operator status = ready
PostgreSQL = reachable
GitHub control plane = github_app
required merge checks = [quality]
retention window = 30 days
canonical retention source query succeeds
PR #61/#77 evidence protections enforced
GitHub mutation performed = false
```

No production branch deletion was performed. Historical evidence PRs #61/#77 remain open and untouched.

## Post-acceptance housekeeping and replay verification

### Conservative Actions-registry housekeeping

The checked-in workflow tree had already been reduced to current operational workflows, but GitHub Actions retained historical registrations for deleted bootstrap/diagnostic YAML files.

A first conservative registry-cleanup batch disabled 15 clearly orphaned records while preserving their historical run evidence. No current workflow file was deleted, no production workflow was disabled, and PR #61/#77 evidence remained untouched.

The disabled historical registrations are recorded in `docs/operations-inventory.md`. They include old bootstrap/P0.2/P0.3 formatting, mypy, pytest, and diagnostic records. All are now `disabled_manually`, which is reversible and preserves run history.

The housekeeping documentation was integrated as:

```text
PR:                 #90
exact PR head:      5fbf4feb2ce3d36e17f26e000f15e896d0e5962e
exact-head CI:      #683 / run 33360707598 / success
merge:              acca895e7bdb36d6c2418a97c87e8a591828d06b
post-main CI:       #684 / run 33360800608 / success
```

Additional historical registry records that were not exposed with enough evidence for safe review remain untouched. No IDs were guessed and no broad registry deletion was performed.

### Six-case offline replay verification

Review of the benchmark workflows found that the existing `developer-benchmark-real.yml` is a legacy, intentionally disabled OpenAI/Luna workflow for three tiny fixture cases. It is not the six-case provider-neutral replay runner and remains disabled.

PR #91 added a separate GitHub-hosted offline verification workflow for the integrated six-case historical replay corpus. It fetches full repository history, validates each frozen base revision, prepares a disposable detached Git workspace for each case, asserts `live_model_calls = 0`, and uploads only non-secret JSONL evidence.

```text
PR:                 #91
exact PR head:      6a24ed84d989dd022ec2ae6c4ec7909718cfbcbb
exact-head CI:      #685 / run 33361041848 / success
merge:              59ed0afd17e7c44addaa8143230f3c274ea09200
post-main CI:       #686 / run 33361127417 / success
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

This proves the frozen revisions and disposable preparation path work on GitHub-hosted infrastructure. It does not establish comparative model quality or cost; those require a separate paid benchmark decision.

## Current policy boundary

The production-proven Manager policy remains:

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

The hardening/infrastructure foundation and the first safe housekeeping/replay-verification steps are complete. The next meaningful decision is whether to authorize a deliberately bounded paid model benchmark; it is not an automatic engineering action.

Recommended order:

1. keep the current single-host production MVP stable and observe real workload/recovery evidence;
2. complete any remaining Actions-registry audit only when exact historical workflow IDs/evidence are available; disable only proven orphaned records and preserve history;
3. if cost is approved, build/run a provider-neutral paid Stage 0 benchmark against the six-case replay design rather than enabling the legacy OpenAI/Luna tiny benchmark;
4. use measured Stage 0/Stage 1 evidence before considering production model routing changes;
5. evaluate remote Developer workers only if measured workload, isolation, or concurrency requirements justify them; and
6. treat mobile/PWA UI, notifications, speech, and broader product surfaces as separate product decisions.

Do not automatically redesign the system into EC2/IAM/distributed infrastructure, enable production model auto-routing, run destructive retention cleanup, or start remote Developer execution merely because the underlying foundations now exist.

## Verification record

- Last verified: `2026-08-30`.
- Current deployed production release: `953580c06d064f44c98dd73c3c59affc35579218`.
- Current repository `main`: `59ed0afd17e7c44addaa8143230f3c274ea09200`.
- Repository `main` is ahead of production only by non-runtime operations/documentation and offline-verification workflow changes; no additional deployment was required.
- Recovery hardening: PR #83; head `80ce8135a7d10bf25d05cf4a35dfbe196663b648`; CI #641 / `33351770700`; merge `2de0d46ae6876f1fc6073b1251ac8cc20a56ff98`; post-main CI #671 / `33353992544`.
- Repository retention: PR #84; head `6c53e8a540bead52963f355ea2946a89b2864aa3`; CI #670 / `33352746709`; merge `b1b7909ee94630c1ca1970e57d2f865f170d4548`; post-main CI #672 / `33354266550`.
- Replay harness: PR #85; head `2e8f3563dab388e23795538806443f60817b6ad6`; CI #666 / `33352596705`; merge `a8ba17cb4692ee1ec0dd8d7ba5ef8653982bb6ea`; post-main CI #673 / `33354726677`.
- Operational hygiene: PR #82; integrated head `c40df3994ce2280ad4359e67bf3690dc3812325b`; fresh CI #675 / `33355008056`; merge `226c16d555503bcabdebdce987c8e07ae93f67d2`; final combined CI #676 / `33355079769`.
- Combined deploy: #19 / `33355428598` on `226c16d555503bcabdebdce987c8e07ae93f67d2`.
- Recovery-compatible Manager approval acceptance: #5 / `33355914565`; PR #87 head `eed2883d80ebfcbce61d3955a04bb001484933d4`; PR CI #677 / `33355938369`; resulting `main` `0cae6146697e3f8fe2b40d958b6a7b2f412817b2`; post-main CI #678 / `33356022649`; deploy #20 / `33356093702`.
- Read-only operations/retention acceptance support: PR #88 head `a1f95772a7fdbb1a84e7ca43e12ba326494dcd88`; CI #679 / `33356199964`; merge `283d250298a719e1ecd750774cf2c721c635d4ef`; post-main CI #680 / `33356275931`; deploy #21 / `33356343624`.
- Safe failed marker-read acceptance: run `33356371113`; failed before probe execution; no production mutation.
- Marker-read fix/final production release: PR #89 head `1c3c11ab494ee64e7ced9de898f4210ecbb8b884`; CI #681 / `33356457873`; merge `953580c06d064f44c98dd73c3c59affc35579218`; post-main CI #682 / `33356548175`; deploy #22 / `33356627581`; successful read-only acceptance #2 / `33356648604`.
- Workflow-registry housekeeping: PR #90 head `5fbf4feb2ce3d36e17f26e000f15e896d0e5962e`; CI #683 / `33360707598`; merge `acca895e7bdb36d6c2418a97c87e8a591828d06b`; post-main CI #684 / `33360800608`; 15 orphaned historical registrations disabled without deleting run history.
- Offline replay verification support: PR #91 head `6a24ed84d989dd022ec2ae6c4ec7909718cfbcbb`; CI #685 / `33361041848`; merge `59ed0afd17e7c44addaa8143230f3c274ea09200`; post-main CI #686 / `33361127417`; offline verification #1 / `33361246871` success with six cases prepared and zero live model calls.
- Historical evidence PR #61 remains open and unmerged.
- Failed-safe evidence PR #77 remains open and unmerged.
- Required-check policy remains exactly one `quality` check in `completed/success` state, matched to the exact head.
- Production Developer routing was not changed and no paid replay benchmark was run.
- The legacy real Developer benchmark remains intentionally disabled and must not be mistaken for the provider-neutral six-case replay experiment.
- Security boundary remains unchanged: no Docker socket, AWS credential, GitHub App private key, installation token, PostgreSQL credential, or GitHub mutation authority entered a Developer container.
- Verified by: High Director.
