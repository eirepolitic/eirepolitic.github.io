---
title: Overlord Phase 2 — Developer Benchmark Corpus Fingerprints
summary: Implementation record for deterministic benchmark case fingerprints that bind trial evidence to an exact corpus revision without invoking or selecting a real coding runtime.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 137
permalink: /projects/notes/overlord-phase-2-benchmark-case-fingerprint/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - benchmark
  - integrity
  - fingerprint
---

# Overlord Phase 2 — Developer Benchmark Corpus Fingerprints

## Outcome

The next credential-free Phase 2 benchmark-evidence hardening slice is complete.

Overlord now derives a deterministic SHA-256 fingerprint for each canonical Developer benchmark case and binds prepared workspaces, validation results, saved trial records, and repeated-trial reports to that exact corpus revision.

Aggregation fails when the same case ID appears with different fingerprints, preventing evidence from different benchmark revisions from being combined unnoticed.

**No real OpenHands/OpenCode execution occurred and no default Developer runtime was selected.**

## Source Delivery

- Repository: `Overlord`
- Pull request: `#16` — `feat: bind Developer benchmark trials to corpus fingerprints`
- Exact final PR head: `2793b729a8e0e8b5ec9d5b0c7bb88cca6833c2f7`
- Exact PR-head permanent CI: run `#192` — `success`
- Final merged `main` commit: `1ec1e502a8a954d231d79edefc656348a0e2cf51`
- Exact post-merge permanent CI: run `#193` — `success`

No dependency or canonical database-schema change was required, and `uv.lock` was not changed.

## Canonical Case Fingerprint

`benchmark_case_fingerprint()` returns:

```text
sha256:<64 lowercase hexadecimal characters>
```

The digest is computed deterministically from:

1. benchmark manifest schema version;
2. the complete canonical case definition;
3. every fixture file's relative path;
4. every fixture file's exact bytes.

This means the fingerprint changes when the task prompt/case definition, validation commands, protected-path declarations, implementation baseline, validator, or any other fixture content changes.

The fingerprint identifies the **prepared corpus revision**. It does not make implementation files immutable during the actual coding trial.

## Workspace and Validation Binding

Benchmark preparation stamps `case_fingerprint` into `.overlord-benchmark.json` alongside the schema version and canonical case definition.

Validation recomputes the fingerprint from the current canonical corpus and requires the workspace metadata to match it before executing validators. The validation result also returns the canonical fingerprint as evidence.

Existing protected-validator checks remain in force. A workspace therefore fails integrity verification if its identity metadata/fingerprint is tampered with or if a protected validator is missing or modified.

## Trial and Report Schema v2

`BenchmarkTrialRecord` is now schema version `2` and requires:

```text
trial_id
case_id
case_fingerprint
results
```

`case_fingerprint` must match the canonical `sha256:` format.

The guarded benchmark runner places the following in both runtime task metadata:

```text
benchmark_case_id
benchmark_case_fingerprint
benchmark_trial_id
```

and writes the same case fingerprint into the emitted trial JSON.

`BenchmarkComparisonReport` is also schema version `2`. It records the exact fingerprint associated with each observed case.

If input trials contain the same `case_id` with different fingerprints, report generation fails with a corpus-revision mismatch instead of combining incomparable evidence.

## Acceptance Behavior

Unit coverage proves:

1. each corpus case produces a deterministic SHA-256 fingerprint;
2. prepared workspace metadata contains the canonical fingerprint;
3. validation returns the same canonical fingerprint;
4. modifying fixture implementation content changes the fingerprint;
5. runtime mutation of a prepared implementation file does not change the canonical corpus fingerprint;
6. tampered workspace fingerprint metadata is rejected;
7. trial schema v2 rejects malformed fingerprints;
8. report schema v2 preserves exact case fingerprints;
9. repeated reports reject the same case ID from different corpus revisions;
10. existing validator integrity, Git evidence, neutral aggregation, and no-winner behavior remain covered.

## CI Gate

Permanent CI run `#192` succeeded on exact final PR head:

`2793b729a8e0e8b5ec9d5b0c7bb88cca6833c2f7`

Permanent CI run `#193` succeeded on exact merged `main`:

`1ec1e502a8a954d231d79edefc656348a0e2cf51`

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

Several non-final PR heads exposed Ruff-format-only findings. A branch-only historically registered Ruff formatter was temporarily reintroduced and dispatched to apply canonical formatting.

The temporary workflow was deleted before the final accepted head. The final branch workflow tree contained only permanent `.github/workflows/ci.yml`.

Non-final failed/action-required runs are not acceptance evidence. Final acceptance is permanent CI `#192` on exact final head `2793b729a8e0e8b5ec9d5b0c7bb88cca6833c2f7`.

## Persistence, Cost, and Security Boundaries

Case fingerprints, workspace metadata, saved trials, and aggregate reports remain benchmark evaluation artifacts rather than canonical PostgreSQL application state.

This slice does not:

- start OpenHands;
- start OpenCode;
- call a hosted model;
- require provider/runtime credentials;
- create recurring cloud infrastructure;
- add a benchmark-result database schema;
- select a default Developer runtime.

Fingerprinting reads only local manifest/fixture bytes and uses the Python standard-library SHA-256 implementation.

## Deferred Work

OpenHands vs OpenCode remains undecided pending controlled real benchmark evidence.

Production automatic Manager-to-real-Developer execution, remote/ephemeral workers, GitHub write/merge brokering, production credential brokering, and hosted deployment remain outside this slice and their approved phase boundaries.

## Related Documents

- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Reproducible Developer Benchmark Corpus](/projects/notes/overlord-phase-2-developer-benchmark-corpus/)
- [Overlord Phase 2 — Developer Benchmark Integrity and Git Evidence](/projects/notes/overlord-phase-2-benchmark-integrity-evidence/)
- [Overlord Phase 2 — Repeated Developer Benchmark Trial Reporting](/projects/notes/overlord-phase-2-benchmark-trial-reporting/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: Overlord PR #16; exact final PR head `2793b729a8e0e8b5ec9d5b0c7bb88cca6833c2f7`; permanent PR-head CI #192; merged source `main` `1ec1e502a8a954d231d79edefc656348a0e2cf51`; post-merge CI #193; fingerprint implementation; workspace/validation binding; trial/report schemas v2; corpus-revision rejection tests; source architecture/development documentation; and final permanent-workflow tree.
- Verified by: High Director.
- Verification scope: deterministic corpus identity, workspace/trial/report revision binding, cross-revision aggregation rejection, exact CI acceptance, temporary diagnostic cleanup, non-canonical evaluation boundary, and no-real-runtime/no-cost/default-selection boundary.
