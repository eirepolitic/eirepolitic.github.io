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

The always-on Overlord MVP is running on one DigitalOcean host. The hardening/infrastructure foundation is integrated and production-accepted. Post-acceptance repository housekeeping, six-case offline replay verification, the fail-closed Stage 0 replay preflight, and the benchmark-only one-request provider gateway are complete.

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
current repository main:    9706196c0e2627ddc9ecf36bb370204a38dd12f7
```

`main` is intentionally ahead of the deployed release by repository operations, replay/benchmark infrastructure, and GitHub-hosted benchmark workflows that are not wired into the production Developer execution path. Production runtime/application behavior remains on `953580c06d064f44c98dd73c3c59affc35579218`; no production restart or deployment was required merely for repository SHA symmetry.

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

Production Developer containers receive only the model credential needed for bounded execution. They do not receive the Docker socket, GitHub App private key, installation token, AWS credentials, PostgreSQL credentials, SSH private keys, broad host filesystem access, or broad Linux privileges.

The benchmark-only Stage 0 path is stricter: the disposable Developer container receives no real OpenAI credential. It receives only a one-run gateway token and is placed on an internal Docker network with no direct Internet route. The benchmark gateway alone is dual-homed to the egress network and holds the benchmark-scoped provider credential.

## Production-proven delivery lifecycle

The current accepted end-to-end lifecycle is:

```text
bounded Developer execution
-> AgentRun = completed
-> Task = validation
-> durable publication
-> PR creation
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

The intentionally disabled current workflow `developer-benchmark-real.yml` remains legacy support and is not the provider-neutral replay experiment.

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

A benchmark design audit identified a critical control limitation before paid benchmarking: the pinned OpenCode path could report usage/cost after execution, but could not enforce a true pre-spend ceiling on underlying model turns. Post-hoc accounting was therefore not treated as a hard budget.

PR #92 added a provider-neutral Stage 0 policy, CLI, tests, and a manually dispatched non-billable preflight workflow.

```text
PR:                  #92
final exact PR head: 68f82e01e21d966035f82c6c05fb06ae8e9ab5b4
exact-head CI:       #710 / run 33412632018 / success
merge:               fecae0c61b2190405f1d133bd130a51ff40a460d
post-main CI:        #711 / run 33412790577 / success
Stage 0 preflight:   #1 / run 33412946519 / success
```

The preflight proved paid execution remained fail-closed until a genuine pre-forward control existed.

## Benchmark-only provider request gateway

Option 1 was selected: add a benchmark-only local request-counting gateway instead of changing the production OpenCode execution path.

### Gateway foundation

PR #93 added the gateway authorization policy, HTTP adapter, separate gateway image, host runner CLI, adversarial tests, and a zero-cost Docker-network preflight.

```text
PR:                    #93
final exact PR head:   c2f508664d43107db422dc3f7d315f6d4c500f51
exact-head CI:         #727 / run 33416918325 / success
merge:                 750c8c142d96408489772eef8fdcf6389251c781
post-main CI:          #728 / run 33417042442 / success
gateway preflight:     #1 / run 33417156712 / success
```

The gateway preflight proved:

```text
Developer direct Internet route = blocked
gateway reachable from Developer internal network = yes
provider request forwarded = 0
provider credential used = no
```

The gateway enforces before forwarding:

```text
one-run bearer token
allowlisted inference endpoints
exact model allowlist
hard forwarded-request count
hard output-token ceiling
prompt-free request hashes/status evidence
```

The real provider credential exists only in the gateway process/container. The Developer container cannot bypass the gateway to reach OpenAI directly.

### Paid Stage 0 workflow consolidation and diagnostics

Concurrent PRs #94/#95 created two Stage 0 paid smoke variants. PR #96 consolidated them into one authoritative workflow, retaining the stronger isolation/accounting path and adding duplicate-dispatch protection and a 30-second pre-secret debounce.

```text
PR #94 merge:            896af19a13a321f72dff9e9072ee3a4ca32c127e
PR #95 merge:            85e7126a239482c1881c7a4271c0c8bca387fb80
PR #96 exact-head CI:    #733 / run 33418203818 / success
PR #96 merge:            51fa409400eac049152433d0d15460931923e46c
post-main CI:            #734 / run 33418341071 / success
```

One-shot repository variables authorize a single run. Each accepted run captures its authorization at job start, enters a 30-second debounce, and the repository authorization variables are deleted before provider-secret access. Any later duplicate dispatch therefore fails closed.

PR #97 made failed paid runs diagnosable by persisting prompt-free evidence before fail-closed validation. PR #98 fixed a GitHub Actions same-step environment handoff bug in evidence collection. PR #99 changed positive output-token requests to clamp down to the hard ceiling rather than rejecting otherwise valid requests and added fixed-category denial reasons.

```text
PR #97 exact-head CI:    #735 / run 33419688054 / success
PR #97 merge:            40a47300f745f8ef4d093de98eb38ce1b4242cde
post-main CI:            #736 / run 33419818836 / success

PR #98 exact-head CI:    #737 / run 33420663837 / success
PR #98 merge:            94662bd46e057fbabbfe6febef7e058981d5dc60
post-main CI:            #738 / run 33420814757 / success

PR #99 exact-head CI:    #739 / run 33421492780 / success
PR #99 merge:            9706196c0e2627ddc9ecf36bb370204a38dd12f7
post-main CI:            #740 / run 33421633404 / success
```

### Successful one-request Stage 0 acceptance

Paid smoke #5 / run `33421905015` ran on exact repository `main` `9706196c0e2627ddc9ecf36bb370204a38dd12f7` after all source gates were green.

The one-shot authorization was consumed and both authorization variables were deleted during the debounce before provider-secret access.

Final prompt-free evidence:

```text
authorization:             stage0-easy1-final-one-request-20260831-1051
case:                      easy-1-opencode-absent-status-idle
frozen base SHA:           994e827910df09c1af0db06808922df3d94d9271
provider:                  openai
model:                     gpt-5.6-luna
runtime:                   opencode
Developer direct egress:   false
hard forwarded limit:      1
hard output-token limit:   256
forwarded requests:        1
denied later requests:     7
denial reason:             provider request budget exhausted
upstream statuses:         [200]
upstream request IDs:      one sanitized request ID recorded
validator:                 passed
workspace changed paths:   none
evidence valid:            true
routing evidence eligible: false
```

The seven denied requests are important proof: after the first provider request, OpenCode attempted additional model turns. The gateway denied all seven before provider forwarding because the one-request budget was exhausted. This demonstrates the pre-spend control works independently of OpenCode's own step behavior.

Runtime-reported accounting from the accepted run:

```text
input tokens:              3
cache-read tokens:         0
cache-write tokens:        6187
total input tokens:        6190
output tokens:             107
reasoning tokens:          18
runtime-reported cost USD: 0
```

`runtime-reported cost USD: 0` is recorded exactly as reported by the runtime. It is not treated as proof that the provider billed zero dollars, and no price table or inferred provider cost was invented. Provider billing, if needed, must be checked from authoritative provider-side billing data.

The OpenCode message request itself reached its 180-second local curl limit (`message_curl_status = 28`, HTTP status string `000`), but this did not weaken the gateway evidence: the gateway independently recorded exactly one upstream provider request with HTTP 200, seven later denials, complete runtime usage/cost evidence, and the frozen Easy-1 validator passed. The run therefore completed successfully as a Stage 0 transport/budget-control acceptance, not as comparative model-quality evidence.

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
```

PostgreSQL remains canonical application state. DBOS remains durable coordination state. GitHub mutations remain confined to `GitHubPort -> GitHubBroker -> GitHub App -> durable audit`.

The benchmark-only gateway has no production routing authority and no GitHub mutation authority. Stage 0 evidence is explicitly marked `routing_evidence_eligible = false`.

## Next stage

Stage 0 is complete: the six-case corpus is frozen and offline-valid, the provider gateway has a real enforceable pre-forward request ceiling, the Developer cannot bypass it, and one paid Easy-1 request was accepted with prompt-free usage/control evidence.

The next meaningful decision is the comparative benchmark roster and spend envelope, not more infrastructure work.

Recommended order:

1. keep production on `953580c06d064f44c98dd73c3c59affc35579218`; repository `main` is ahead only by non-production benchmark/operations tooling;
2. define the Stage 1 comparison roster and a bounded spend envelope;
3. first compare models on Easy-1 using the same gateway and deterministic validator;
4. only expand to all six frozen cases after each candidate proves complete accounting and bounded execution;
5. require repeated six-case evidence before considering production model-routing changes; and
6. keep remote Developer workers, mobile/PWA UI, notifications, speech, and distributed infrastructure as separate architecture/product decisions.

Do not change production model routing from Stage 0 alone. Do not enable the legacy real benchmark as a substitute for the provider-neutral replay design.

## Verification record

- Last verified: `2026-08-31`.
- Current deployed production release: `953580c06d064f44c98dd73c3c59affc35579218`.
- Current repository `main`: `9706196c0e2627ddc9ecf36bb370204a38dd12f7`.
- Repository `main` is ahead of production by benchmark/operations tooling not wired into the production Developer execution path; no additional production deployment is required.
- Final production deploy: #22 / `33356627581` / success.
- Final production read-only operations/retention acceptance: #2 / `33356648604` / success.
- Workflow-registry housekeeping: PR #90; CI #683 / `33360707598`; merge `acca895e7bdb36d6c2418a97c87e8a591828d06b`; post-main CI #684 / `33360800608`.
- Offline replay verification: PR #91; CI #685 / `33361041848`; merge `59ed0afd17e7c44addaa8143230f3c274ea09200`; post-main CI #686 / `33361127417`; offline verification #1 / `33361246871` success.
- Stage 0 preflight: PR #92; exact-head CI #710 / `33412632018`; merge `fecae0c61b2190405f1d133bd130a51ff40a460d`; post-main CI #711 / `33412790577`; preflight #1 / `33412946519` success.
- Benchmark gateway: PR #93; exact-head CI #727 / `33416918325`; merge `750c8c142d96408489772eef8fdcf6389251c781`; post-main CI #728 / `33417042442`; zero-cost gateway preflight #1 / `33417156712` success.
- Paid-smoke consolidation: PR #96; CI #733 / `33418203818`; merge `51fa409400eac049152433d0d15460931923e46c`; post-main CI #734 / `33418341071`.
- Evidence persistence: PR #97; CI #735 / `33419688054`; merge `40a47300f745f8ef4d093de98eb38ce1b4242cde`; post-main CI #736 / `33419818836`.
- Evidence status handoff: PR #98; CI #737 / `33420663837`; merge `94662bd46e057fbabbfe6febef7e058981d5dc60`; post-main CI #738 / `33420814757`.
- Gateway output clamping/denial evidence: PR #99; CI #739 / `33421492780`; merge `9706196c0e2627ddc9ecf36bb370204a38dd12f7`; post-main CI #740 / `33421633404`.
- Successful Stage 0 paid transport/budget-control acceptance: run #5 / `33421905015` / success; exactly one upstream provider request, HTTP 200, seven later requests denied before forwarding, 256 output-token ceiling, runtime usage/cost evidence present, Easy-1 validator passed, no direct Developer egress, no changed workspace paths.
- Historical evidence PR #61 remains open and unmerged.
- Failed-safe evidence PR #77 remains open and unmerged.
- Required-check policy remains exactly one `quality` check in `completed/success` state, matched to the exact head.
- Production Developer routing was not changed.
- The legacy real Developer benchmark remains intentionally disabled and must not be mistaken for the provider-neutral six-case replay experiment.
- Security boundary remains unchanged: no Docker socket, AWS credential, GitHub App private key, installation token, PostgreSQL credential, or GitHub mutation authority entered a Developer container.
- Verified by: High Director.
