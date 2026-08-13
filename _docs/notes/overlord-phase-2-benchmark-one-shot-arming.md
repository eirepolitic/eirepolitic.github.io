---
title: Overlord Phase 2 — Real Benchmark One-Shot Arming
summary: Follow-up record for the first real Developer benchmark, duplicate-dispatch containment, evidence normalization, and one-shot paid-run authorization controls.
section: notes
doc_type: note
status: active
created: 2026-08-12
updated: 2026-08-12
last_verified: 2026-08-12
owner: High Director
order: 140
permalink: /projects/notes/overlord-phase-2-benchmark-one-shot-arming/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - benchmark
  - openhands
  - opencode
  - github-actions
  - safety
---

# Overlord Phase 2 — Real Benchmark One-Shot Arming

## Outcome

Overlord completed one owner-authorized real OpenHands-vs-OpenCode Developer benchmark trial, contained an unintended duplicate workflow run, normalized the real-world runtime evidence, and hardened the billable workflow with one-shot authorization controls.

The accepted authorized trial remains valid evaluation evidence. The unintended duplicate run is explicitly excluded from runtime-selection evidence even though it progressed far enough to incur some provider usage.

No default Developer runtime is selected by this work.

## Accepted First Real Trial

Authorized workflow evidence:

```text
workflow:                  Real Developer benchmark
workflow run ID:           31625963336
workflow run number:       7
source SHA:                fcf401ab53e1410ab280cd647fe50b4d25cedfe6
trial ID:                  github-31625963336-1
case:                      python-off-by-one
case fingerprint:          sha256:810c0e17985a55887e945f972f3fa83a7dcd4f947782d7f581d0a8fbebe96a54
provider:                  openai
model:                     gpt-5.6-luna
artifact:                  developer-benchmark-31625963336-1
artifact ID:               9153151709
```

Both runtimes completed the approved task and passed protected validation.

Observed accepted-trial results:

```text
OpenHands: tests passed; integrity verified; 28.9687 s; $0.00466036
OpenCode:  tests passed; integrity verified; 11.1285 s; $0.00271361
accepted trial total reported cost: $0.00737397
```

Both produced the intended one-line off-by-one repair.

This single trial is evidence only. It is not sufficient to choose OpenHands or OpenCode as Overlord's default Developer runtime.

## Duplicate Dispatch Incident

A single intended paid dispatch produced two GitHub workflow runs within seconds:

```text
authorized accepted run: 31625963336
unintended duplicate:    31625965069
```

The duplicate was not owner-authorized as a separate comparison trial.

The duplicate was cancelled and is excluded from runtime-selection evidence. Cancellation propagated only after it had already entered model execution, so its partial artifact contains completed candidate results and approximately another `$0.0077` of reported provider usage.

Across the accepted trial and the unintended duplicate, observed runtime-reported provider usage was therefore approximately `$0.015`, still far below the benchmark project's external `$10` hard ceiling.

The duplicate artifact must not be aggregated into accepted repeated-trial evidence merely because it contains technically complete runtime results. Acceptance follows owner authorization as well as artifact validity.

## Credential Containment Correction

This record formally corrects the credential wording in the earlier [First Real Developer Benchmark Evidence](/projects/notes/overlord-phase-2-first-real-benchmark-evidence/) note.

The attempted GitHub secret deletion returned `404`; it was not verified as a successful deletion. The containment action that **did** succeed was overwriting the repository secret name `OVERLORD_BENCHMARK_OPENAI_API_KEY` with a harmless invalid value:

```text
BLOCKED_DUPLICATE_RUN_DO_NOT_USE
```

GitHub had already materialized the original usable credential into the duplicate job before that overwrite, so changing the repository secret could not retroactively remove the original value from the already-running job.

Current operational meaning:

- the repository secret name may exist;
- its configured value is deliberately invalid and is not a usable OpenAI API credential;
- a fresh valid benchmark key is required before any future approved paid benchmark run;
- credentials must never be committed to source, documentation, or chat.

Any prior wording that says the secret was successfully deleted or is definitely absent is superseded by this verified containment record.

## Source Hardening — Evidence Normalization

Source PR `#20` — `feat: normalize real Developer benchmark evidence` — incorporated the first real-trial observations.

Accepted source evidence:

```text
exact final PR head:       ca7dbc1dc2a5871e150a95e6a6913c85a94f8aa2
PR permanent CI:           #226
PR CI run ID:              31626895262
PR CI conclusion:          success
merged source main:        9745b4f8a49a6161eb3539aef7074d6d5f8de80b
post-merge CI:             #230
post-merge CI run ID:      31627036702
post-merge CI conclusion:  success
```

The slice preserved backward-compatible runtime-native usage fields while adding normalized total-input/cache/reasoning evidence, fixed OpenHands `execution_status` normalization, retained conservative OpenCode unknown-status behavior, suppressed Python bytecode noise in real runtime workspaces, added an early provider-secret presence check, and changed the real benchmark concurrency group to `cancel-in-progress: true`.

No database migration, application dependency change, provider/model change, budget-policy change, or runtime selection occurred.

## Source Hardening — One-Shot Arming

Source PR `#21` — `fix: add one-shot arming to real Developer benchmark` — added the remaining paid-dispatch safety boundary on top of PR #20.

Accepted source evidence:

```text
exact final PR head:       99f48898232b267dd85cd56411fae37f11396842
PR permanent CI:           #231
PR CI run ID:              31627779948
PR CI conclusion:          success
merged source main:        7f21d37278f8f30c3507d427b571cb64d4034691
post-merge CI:             #232
post-merge CI run ID:      31627930106
post-merge CI conclusion:  success
```

Both permanent CI gates included:

```text
docker compose config --quiet
PostgreSQL startup/readiness
uv sync --locked --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run alembic upgrade head
uv run pytest
```

No application dependency or lockfile change, PostgreSQL schema change, runtime selection, provider/model change, or budget-policy change was introduced.

## One-Shot Authorization Latch

The real benchmark workflow is normally disarmed through repository Actions variables:

```text
OVERLORD_BENCHMARK_AUTHORIZATION_ID=UNARMED
OVERLORD_BENCHMARK_RUN_CONFIRMATION=DISABLED
```

The workflow verifies these variables in its **first job step**.

For one explicitly owner-approved paid trial, the operator must:

1. assign a unique authorization ID;
2. set `OVERLORD_BENCHMARK_RUN_CONFIRMATION=RUN_ONE_TRIAL`;
3. enable the real benchmark workflow;
4. dispatch exactly once;
5. verify the surviving run passes the authorization-latch step;
6. restore the variables to `UNARMED` / `DISABLED`;
7. disable the real benchmark workflow again when no paid execution is expected.

The safe benchmark summary records the authorization ID for audit correlation.

The authorization ID is operational benchmark evidence only. It is not canonical PostgreSQL state and does not create a general budget ledger.

## No-Secret Duplicate Debounce

After a valid latch check, the real workflow waits 30 seconds before checkout or provider-secret access.

The paid workflow also retains:

```text
concurrency group:  real-developer-benchmark
cancel-in-progress: true
GitHub permission:  contents: read
```

A near-simultaneous duplicate dispatch can therefore cancel the older candidate during the no-secret debounce rather than intentionally serializing a second paid trial.

These controls reduce accidental duplicate paid execution. They do not replace the provider project's external `$10` hard ceiling or Overlord's existing `$50/month` architectural project ceiling.

## Negative Safety Proof

Non-billable workflow run `31627541359` exercised the real workflow while the repository was intentionally disarmed:

```text
OVERLORD_BENCHMARK_AUTHORIZATION_ID=UNARMED
OVERLORD_BENCHMARK_RUN_CONFIRMATION=DISABLED
```

The run failed at:

```text
Verify explicit paid-run authorization latch
```

All later paid-path steps were skipped, including:

- repository checkout;
- provider-secret presence check/access;
- OpenHands installation/startup;
- OpenCode installation/startup;
- provider profile/configuration;
- real model comparison.

The real benchmark workflow was disabled again immediately after this proof.

## Current Safe State

At this checkpoint:

```text
source main:                          7f21d37278f8f30c3507d427b571cb64d4034691
real benchmark workflow:              disabled
OVERLORD_BENCHMARK_AUTHORIZATION_ID:  UNARMED
OVERLORD_BENCHMARK_RUN_CONFIRMATION:  DISABLED
benchmark repository secret value:    deliberately invalid containment value
usable benchmark provider key:        not configured
```

No further paid benchmark trial is authorized by the source hardening or by this documentation record.

## Selection Boundary

Accepted evidence currently proves only that both candidates can solve the smallest approved bug-fix case under the controlled setup.

OpenCode was faster and cheaper on that individual accepted trial, but the approved selection process still requires repeated comparable evidence across the benchmark corpus, including feature and refactor behavior, before selecting a default Developer runtime.

The unintended duplicate must remain excluded from accepted repeated-trial aggregates.

## Next Owner Checkpoint

The next meaningful benchmark phase requires two owner actions before any further paid execution:

1. create/restore a **fresh valid** OpenAI benchmark API key in the `Overlord` repository secret `OVERLORD_BENCHMARK_OPENAI_API_KEY` because the current containment value is deliberately unusable;
2. explicitly authorize the repeated three-case benchmark phase under the benchmark-only `$10` ceiling.

Until then, the real workflow remains disabled and disarmed.

## Related Documents

- [Overlord Phase 2 — First Real Developer Benchmark Evidence](/projects/notes/overlord-phase-2-first-real-benchmark-evidence/)
- [Overlord Phase 2 — Real Developer Benchmark Preflight](/projects/notes/overlord-phase-2-real-benchmark-preflight/)
- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Repeated Developer Benchmark Trial Reporting](/projects/notes/overlord-phase-2-benchmark-trial-reporting/)
- [Overlord Phase 2 — Developer Benchmark Corpus Fingerprints](/projects/notes/overlord-phase-2-benchmark-case-fingerprint/)

## Verification Record

- Last verified: `2026-08-12`.
- Verified against: authorized real benchmark run `31625963336`; unintended duplicate run `31625965069`; accepted artifact `9153151709`; source PR #20 and CI #226/#230; source PR #21 exact head `99f48898232b267dd85cd56411fae37f11396842`; negative proof run `31627541359`; merged source main `7f21d37278f8f30c3507d427b571cb64d4034691`; and post-merge CI #232.
- Verified by: High Director.
- Verification scope: first accepted paid trial, duplicate-run exclusion/cost containment, corrected credential state, normalized usage/status evidence, duplicate-cancelling concurrency, one-shot authorization latch, no-secret debounce, exact-SHA CI acceptance, no-runtime-selection boundary, and no-additional-paid-run state.
