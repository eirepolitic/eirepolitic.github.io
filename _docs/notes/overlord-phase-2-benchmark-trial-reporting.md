---
title: Overlord Phase 2 — Repeated Developer Benchmark Trial Reporting
summary: Implementation record for schema-versioned benchmark trial identity and neutral repeated-result reporting without selecting or invoking a real coding runtime.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 136
permalink: /projects/notes/overlord-phase-2-benchmark-trial-reporting/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - benchmark
  - reporting
---

# Overlord Phase 2 — Repeated Developer Benchmark Trial Reporting

## Outcome

The next credential-free Phase 2 benchmark-evidence slice is complete.

Overlord now has schema-versioned, explicitly identified benchmark trial JSON plus deterministic offline aggregation across repeated trials. Reports remain descriptive only: they contain no score, ranking, preferred runtime, or winner field.

Saved trial/report JSON remains an **evaluation artifact**, not canonical PostgreSQL application state.

**No real OpenHands/OpenCode execution occurred and no default Developer runtime was selected.**

## Source Delivery

- Repository: `Overlord`
- Pull request: `#15` — `feat: add repeated Developer benchmark trial reporting`
- Exact final PR head: `7b1e152f1caa99aedac5eb0e1878b8cc6a454838`
- Exact PR-head permanent CI: run `#185` — `success`
- Final merged `main` commit: `85c689b5ce1d85dad6cde0579bcfdd2820dafa1c`
- Exact post-merge permanent CI: run `#186` — `success`

No dependency or canonical database-schema change was required, and `uv.lock` was not changed.

## Trial Identity

`BenchmarkTrialRecord` is schema version `1` and records:

```text
trial_id
case_id
results[]
```

Each trial permits at most one result for a given runtime. Duplicate runtime results are rejected.

The guarded real benchmark runner accepts optional:

```text
OVERLORD_DEVELOPER_BENCHMARK_TRIAL_ID
```

A blank configured value is rejected. If omitted, the runner creates a local UUID for that invocation. The same trial ID is included in each runtime task's metadata and in the emitted trial JSON.

## Serializable Runtime Evidence

Each runtime result preserves:

- runtime and external task/session identifier;
- duration, normalized status, and summary;
- normalized input/output token counts and USD cost when available;
- runtime-specific final evidence;
- benchmark completion/test/recovery/security/isolation/cleanup evidence;
- protected-workspace integrity evidence;
- baseline/current Git commit, status, and diff evidence;
- observed event count.

Unknown measurements remain `None`; they are not silently converted to zero.

Usage evidence rejects negative token counts, negative costs, invalid numeric cost strings, and non-finite values.

## Neutral Repeated-Trial Report

`scripts/report_developer_benchmark_trials.py` accepts one or more saved trial JSON files and generates a schema-versioned comparison report.

Duplicate trial IDs are rejected. Results are grouped by runtime and summarized with:

```text
trials_observed
completed_trials
tests_passed_trials
tests_failed_trials
tests_unknown_trials
median_duration_seconds
events_observed_total
input_tokens_observed_trials
input_tokens_total
output_tokens_observed_trials
output_tokens_total
cost_usd_observed_trials
cost_usd_total
```

Observation counts explicitly distinguish unavailable measurements from measured zero values.

The report intentionally has no:

```text
winner
preferred_runtime
ranking
score
```

It therefore cannot silently decide OpenHands vs OpenCode.

## Persistence Boundary

Benchmark trial and aggregate report files are evaluation artifacts. They are not inserted into canonical WorkRequest/Task/AgentRun/model-usage tables and this slice introduces no benchmark-result database schema.

PostgreSQL remains authoritative for canonical Overlord application state; saved benchmark evidence can be independently retained/reviewed for the later owner runtime-selection decision.

## Acceptance Behavior

The new unit coverage proves:

1. trial identity and runtime results survive serialization;
2. duplicate runtime results in one trial are rejected;
3. duplicate trial IDs in an aggregate report are rejected;
4. completion/test/duration/event/token/cost evidence aggregates deterministically;
5. unknown test/usage evidence remains explicitly unknown;
6. malformed numeric usage evidence is rejected;
7. trial JSON round-trips exactly;
8. aggregate output exposes no winner/ranking/preferred-runtime/score field.

Existing benchmark corpus/integrity, runtime-adapter, delegation, recovery, PostgreSQL, DBOS, architecture, and security tests remain part of the permanent suite.

## CI Gate

Permanent CI run `#185` succeeded on exact final PR head:

`7b1e152f1caa99aedac5eb0e1878b8cc6a454838`

Permanent CI run `#186` succeeded on exact merged `main`:

`85c689b5ce1d85dad6cde0579bcfdd2820dafa1c`

Both acceptance gates included:

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

## Temporary Diagnostics

Non-final PR heads exposed Ruff lint/format findings. A branch-only registered Ruff-format diagnostic workflow was temporarily used to apply the repository's canonical formatter.

All temporary workflow files were deleted before the final accepted head. The exact final PR head contained only the intended permanent `.github/workflows/ci.yml` workflow.

Earlier non-final CI runs are not acceptance evidence; final acceptance is run `#185` on the exact final head above.

## Cost and Security Boundaries

This slice remains offline and non-billable in normal CI.

It does not:

- start OpenHands;
- start OpenCode;
- call a hosted model;
- require runtime/provider credentials;
- create recurring cloud infrastructure;
- select a default Developer runtime;
- make benchmark files canonical application state.

Real Developer benchmark execution remains guarded by `OVERLORD_RUN_REAL_DEVELOPER_BENCHMARK=1` and was not enabled.

## Deferred Work

OpenHands vs OpenCode remains undecided pending controlled real benchmark evidence.

Production automatic Manager-to-real-Developer execution, remote/ephemeral worker provisioning, GitHub write/merge brokering, production credential brokering, and hosted deployment remain outside this slice and their approved phase boundaries.

## Related Documents

- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Reproducible Developer Benchmark Corpus](/projects/notes/overlord-phase-2-developer-benchmark-corpus/)
- [Overlord Phase 2 — Developer Benchmark Integrity and Git Evidence](/projects/notes/overlord-phase-2-benchmark-integrity-evidence/)
- [Overlord Phase 2 — Fake-Backed Manager Developer Delegation](/projects/notes/overlord-phase-2-manager-developer-delegation/)
- [Overlord Phase 2 — Developer Run Recovery and Lifecycle Audit](/projects/notes/overlord-phase-2-developer-recovery-audit/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: Overlord PR #15; exact final PR head `7b1e152f1caa99aedac5eb0e1878b8cc6a454838`; permanent PR-head CI #185; merged source `main` `85c689b5ce1d85dad6cde0579bcfdd2820dafa1c`; post-merge CI #186; trial/reporting application models; guarded runner changes; offline report CLI; unit tests; source architecture/development documentation; and final permanent-workflow tree.
- Verified by: High Director.
- Verification scope: trial identity, duplicate protection, neutral aggregation, unknown-evidence semantics, numeric usage validation, non-canonical evaluation boundary, exact CI acceptance, temporary diagnostic cleanup, and no-real-runtime/no-cost/default-selection boundary.
