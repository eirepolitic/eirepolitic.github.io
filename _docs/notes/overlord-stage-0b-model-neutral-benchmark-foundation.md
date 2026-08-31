---
title: Overlord Stage 0B — Model-Neutral Benchmark Foundation
summary: Acceptance record for provider-neutral gateway profiles, sealed replay workspaces, hidden validators, normalized call evidence, and zero-cost cross-provider profile preflight.
section: notes
doc_type: note
status: active
created: 2026-08-31
updated: 2026-08-31
last_verified: 2026-08-31
owner: High Director
order: 153
permalink: /projects/notes/overlord-stage-0b-model-neutral-benchmark-foundation/
tags:
  - overlord
  - benchmark
  - developer
  - model-routing
  - stage-0b
---

# Overlord Stage 0B — Model-Neutral Benchmark Foundation

## Status

Stage 0B is complete as a no-spend benchmark-foundation milestone.

```text
Overlord repository main: e2355cba04b60924fa195809ea92c7cfa392e520
Production deployed release: 953580c06d064f44c98dd73c3c59affc35579218
Production Developer routing changed: no
Live provider calls in Stage 0B acceptance: 0
Provider secrets used in Stage 0B acceptance: none
```

Production remains intentionally on the previously accepted release because Stage 0B changes are benchmark/evaluator infrastructure and are not wired into the production Developer execution path.

## Integrated foundation

### Provider-neutral benchmark gateway profiles

PR #100 added provider profiles for OpenAI, Anthropic, and Google/Gemini while preserving the existing OpenAI Stage 0 behavior.

```text
PR #100 exact-head CI: #744 / 33425024005 / success
merge: e4e5f7b48ff81fab16ef0bec25fb684116db5e07
post-main CI: #745 / 33425163884 / success
```

The benchmark-only gateway now has provider-specific controls for:

```text
endpoint/model allowlisting
provider authentication construction
output-token bounding
provider request IDs
normalized token/cache/reasoning usage
prompt-free per-call evidence
```

The gateway remains outside production routing authority and GitHub mutation authority.

### Sealed replay workspaces

A benchmark anti-leakage defect was found during Stage 0B review: a full Git clone pinned to a historical SHA could still expose later solution commits through the workspace `.git` object store.

PR #101 changed disposable replay preparation to initialize a fresh repository, fetch only the exact base commit at depth 1, check out detached, and remove the source remote.

```text
PR #101 exact-head CI: #746 / 33425544877 / success
merge: f8153d7c25adfcd6c4d8ad59486c5d363db1d23f
post-main CI: #747 / 33425687511 / success
```

Regression coverage proves a later historical solution commit cannot be resolved from the Developer-visible workspace.

### Evaluator-owned hidden validators

PR #102 introduced a hidden-validator registry and host-side evaluator runner. Hidden checks live in current evaluator source and are never copied into the sealed historical Developer workspace.

```text
PR #102 exact-head CI: #750 / 33426436744 / success
merge: 4331af9481bc98e1b7b35d74a4274700f3d4e6ea
post-main CI: #751 / success
```

The initial Easy-case acceptance proved hidden checks reject the buggy frozen revisions and accept their known fixes.

PR #104 extended hidden validation to all six replay cases:

```text
2 Easy
2 Medium
2 Hard
```

The hidden behavioral seams are:

```text
Easy-1: absent OpenCode status normalizes to idle
Easy-2: readiness requires bounded HTTP health polling
Medium-1: workspace changes are captured before cleanup and preserved
Medium-2: workspace changes become validated non-mutating commit intent
Hard-1: task+revision DBOS identity is stable and replay is idempotent
Hard-2: provider-neutral canonical state persists transactionally in PostgreSQL
```

```text
PR #104 exact-head CI: #765 / 33430433861 / success
merge: 47a15d0b645b2f9a25aea4359a23d5770b92206c
post-main CI: #766 / 33430583915 / success
```

PR #105 corrected the evaluator-only historical fetch boundary without exposing credentials to Developer workspaces.

```text
PR #105 exact-head CI: #767 / 33430800794 / success
merge: 2d10a056c4ac4cc733a820600fa49f8e700a0a36
post-main CI: #768 / 33430949476 / success
```

All-six hidden-validator preflight #3 / `33431069330` succeeded:

```text
all six frozen bases rejected: yes
all six preserved accepted fixes passed: yes
hidden validator files visible in Developer workspace: no
live model calls: 0
provider secrets used: no
```

### Normalized benchmark call evidence and candidate registry

PR #103 added benchmark-only contracts for candidate/model registries, price snapshots, and normalized prompt-free per-call provider evidence. Canonical production `ModelCall` semantics were not changed.

```text
PR #103 exact-head CI: #755 / 33429254528 / success
merge: 269c6ad143252fcede490adf5a4ab32d6cc491f6
post-main CI: #756 / 33429396221 / success
```

Each accepted gateway call can now record:

```text
provider
model
request ordinal
request SHA-256
upstream status
provider request ID
input tokens
cached input tokens
cache-write tokens where available
reasoning/thinking tokens where available
output tokens
total tokens
cost provenance
```

Cost provenance is explicit:

```text
provider_reported
estimated_from_snapshot
unavailable
```

Estimated cost must identify the versioned price snapshot used. Missing cost is not silently converted to zero.

### Zero-cost provider-profile integration acceptance

PR #106 added a manual mock integration workflow exercising the actual benchmark gateway HTTP boundary for OpenAI, Anthropic, and Google/Gemini with local mocked upstream responses only.

```text
PR #106 exact-head CI: #778 / 33431914312 / success
merge: e2355cba04b60924fa195809ea92c7cfa392e520
post-main CI: #779 / 33432042733 / success
provider-profile preflight #1: 33432181738 / success
artifact: developer-benchmark-provider-profile-preflight-33432181738
```

The preflight proves for all three profiles:

```text
provider identity preserved
provider endpoint/model policy enforced
output-token request clamped to the hard ceiling
one forwarded request allowed
second request denied before forwarding
provider credential substituted only at the gateway boundary
caller authentication/account headers not forwarded
normalized usage evidence produced
provider request ID captured
cost provenance remains unavailable when not actually reported
prompt/gateway/provider secret material absent from evidence
live provider calls = 0
provider secrets used = false
routing_evidence_eligible = false
```

## Boundary after Stage 0B

Stage 0B establishes a model-neutral evaluator and gateway foundation, but it does not yet prove live Anthropic or Google transport through the pinned OpenCode Developer runtime.

The next step is a bounded real-provider integration smoke, not a production routing change and not yet the six-case comparative benchmark.

Recommended initial live-integration roster:

```text
OpenAI:    gpt-5.6-luna       current production baseline / low-cost transport reference
Anthropic: claude-sonnet-5    current balanced coding/agentic candidate
Google:    gemini-3.7-flash   current GA coding/agentic candidate
```

Before that smoke, the pinned OpenCode `1.18.16` runtime should be verified against each native provider package and gateway request shape. The benchmark should continue to use disposable internal-only Developer networking and benchmark-scoped provider credentials.

No Stage 0B result justifies a production model-routing change.

## Next decision

The next user-controlled boundary is credentials and spend:

1. verify pinned OpenCode native request shapes for Anthropic and Google without live provider calls;
2. configure benchmark-scoped Anthropic and Google API credentials only after that preflight is green;
3. authorize one tightly bounded live integration request per provider;
4. freeze the first comparative candidate registry and pricing snapshot only after live accounting is verified; and
5. begin equal six-case Stage 1 benchmarking only after the live provider integrations are proven.
