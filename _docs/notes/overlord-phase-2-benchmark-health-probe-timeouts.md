---
title: Overlord Phase 2 — Bounded Benchmark Health Probes
summary: Runtime-orchestration fix for bounded OpenHands/OpenCode readiness requests after an unaccepted local startup hang during repeated benchmarking.
section: notes
doc_type: note
status: active
created: 2026-08-13
updated: 2026-08-13
last_verified: 2026-08-13
owner: High Director
order: 142
permalink: /projects/notes/overlord-phase-2-benchmark-health-probe-timeouts/
tags:
  - overlord
  - phase-2
  - benchmark
  - openhands
  - opencode
  - github-actions
---

# Overlord Phase 2 — Bounded Benchmark Health Probes

## Outcome

Repeated benchmark attempt `31736990042` reached local OpenCode startup but never reached the paid `Run one controlled real comparison` step. The OpenCode health request could remain blocked because the original `curl` probe had no per-request timeout.

The attempt was cancelled through the existing duplicate-cancelling concurrency boundary and is **not** an accepted comparison trial. A deliberately disarmed replacement run `31737553418` failed at the authorization latch and did not execute the paid path.

## Source Fix

Source PR `#23` — `fix: bound real benchmark health probes`:

```text
exact final PR head:       d884bdd4326fa981a61ca528446bf88fceffb747
PR permanent CI:           #235
PR CI run ID:              31737739090
PR CI conclusion:          success
merged source main:        ccd3db3fc8c68c3029b8921fc6d9b700b0691bb2
```

The real benchmark workflow now:

- bounds OpenHands `/health` and `/ready` requests with short connect/request timeouts;
- bounds OpenCode `/global/health` requests;
- detects early OpenCode process exit;
- bounds the OpenCode `/project/current` request;
- retains the existing retry loops rather than permitting one half-open request to hang indefinitely.

No provider/model/runtime-version, dependency-lock, database schema, runtime-selection, or budget-policy change occurred.

## Acceptance Boundary

An infrastructure attempt that fails before the model-comparison step does not consume one of the eight approved accepted-trial slots.

The approved recovery path is to fix the concrete local orchestration defect, pass permanent CI, and retry the same approved slot without silently changing OpenHands, OpenCode, or `gpt-5.6-luna`.

## Verification Record

- Last verified: `2026-08-13`.
- Verified against: unaccepted run `31736990042`; disarmed replacement `31737553418`; source PR #23 exact head `d884bdd4326fa981a61ca528446bf88fceffb747`; permanent CI #235; merged source main `ccd3db3fc8c68c3029b8921fc6d9b700b0691bb2`.
- Verified by: High Director.
