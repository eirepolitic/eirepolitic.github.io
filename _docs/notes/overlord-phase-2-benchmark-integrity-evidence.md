---
title: Overlord Phase 2 — Developer Benchmark Integrity and Git Evidence
summary: Implementation record for the offline Phase 2 benchmark hardening slice that protects deterministic validators and captures reproducible workspace Git evidence without invoking or selecting a real coding runtime.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 135
permalink: /projects/notes/overlord-phase-2-benchmark-integrity-evidence/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - benchmark
  - integrity
  - git
---

# Overlord Phase 2 — Developer Benchmark Integrity and Git Evidence

## Outcome

The next credential-free Phase 2 benchmark-evidence slice is complete.

The reproducible Developer benchmark corpus now protects deterministic validator files from unnoticed modification, validates workspace identity against the canonical manifest before tests execute, and captures independent Git baseline/head/status/diff evidence for prepared Git workspaces.

The real benchmark remains explicitly disabled by default. **No OpenHands/OpenCode task was executed and no default Developer runtime was selected.**

## Source Delivery

- Repository: `Overlord`
- Pull request: `#14` — `feat: harden Developer benchmark workspace integrity`
- Exact final PR head: `9e392777348911ba45a1db4d494ef3962d263cf8`
- Exact PR-head permanent CI: run `#176` — `success`
- Final merged `main` commit: `fcfe9f9b6a21bc07b0a05b3fcf5a60f4ddc0d3d5`
- Exact post-merge permanent CI: run `#177` — `success`

No dependency or canonical database-schema change was required, and `uv.lock` was not changed.

## Protected Benchmark Validators

`benchmarks/developer/manifest.json` is now schema version `2` and declares explicit `protected_paths` for each benchmark case:

```text
python-off-by-one      check_calculator.py
python-config-feature  check_config.py
python-slug-refactor   check_slug.py
```

Preparation verifies that every protected path is a real file in the canonical fixture before copying a case into a workspace.

Validation performs integrity checks **before executing any benchmark command**:

1. `.overlord-benchmark.json` must exactly match the canonical manifest schema/case data;
2. each declared protected validator must still exist in the workspace;
3. each protected validator must remain byte-identical to the canonical source fixture.

A missing or modified validator therefore fails validation instead of allowing a runtime to weaken the benchmark. Implementation files remain intentionally mutable.

## Reproducible Git Evidence

For a Git-backed prepared workspace, validation now records independent local evidence:

```text
baseline_commit
a current head_commit
git status --porcelain equivalent output
tracked diff from the root baseline commit
```

`baseline_commit` is derived from the repository's single root commit, so later runtime-created commits do not move the original comparison point.

Porcelain status exposes tracked and untracked workspace state. The baseline diff captures tracked changes whether they remain in the working tree or have been committed after preparation.

The evidence is produced by Overlord's local benchmark validator rather than trusting runtime-native Git reporting.

## Deterministic Validator Execution

Python validator subprocesses run with bytecode writes disabled.

This prevents validator-created `__pycache__` files from polluting workspace Git evidence and keeps a freshly prepared baseline clean after validation.

This behavior is limited to benchmark validation subprocesses and does not alter normal Python/application runtime behavior.

## Benchmark JSON Surface

`BenchmarkEvidence` now includes optional fields for:

```text
workspace_integrity_verified
baseline_commit
head_commit
git_status_porcelain
git_diff_from_baseline
```

The real comparison script maps corpus validation/Git evidence into those fields when a real trial is deliberately enabled later.

Unknown or unavailable evidence remains `None`. The harness still does not invent scores or select a winner.

## Acceptance Behavior

Unit coverage proves:

- all three corpus baselines remain intentionally unsolved;
- a known correct bugfix moves its case from failing to passing;
- freshly prepared Git workspaces remain clean after validation;
- modified protected validators are rejected before test execution;
- missing protected validators are rejected;
- tampered workspace identity metadata is rejected;
- committed changes advance current HEAD without changing the root baseline;
- uncommitted/untracked state appears in porcelain status;
- tracked changes appear in the baseline diff.

Existing Developer adapter/harness/delegation/recovery tests remain part of the full permanent suite.

## CI Gate

The final accepted PR head was:

`9e392777348911ba45a1db4d494ef3962d263cf8`

Permanent CI run `#176` succeeded on exactly that SHA with:

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

The squash merge produced source `main`:

`fcfe9f9b6a21bc07b0a05b3fcf5a60f4ddc0d3d5`

Permanent post-merge CI run `#177` succeeded on that exact commit with the same gate.

Earlier non-final PR heads were not accepted: run `#174` exposed a Ruff line-length defect, and run `#175` exposed nondeterministic validator-generated bytecode in Git evidence. Both defects were corrected before the final accepted head/run.

## Cost and Security Boundaries

This slice remains local, deterministic, and non-billable in normal CI.

It does not:

- start OpenHands;
- start OpenCode;
- call a hosted coding model;
- require provider/runtime credentials;
- create recurring cloud infrastructure;
- persist benchmark results as canonical application state;
- add a default Developer runtime;
- weaken or bypass existing port/adapter boundaries.

Protected-file comparison reads only the repository's canonical fixture and the prepared local workspace. Git evidence uses local Git commands only.

## Deferred Work

This slice does not perform a real controlled benchmark, select OpenHands/OpenCode, provision remote workers, broker production credentials, or enable GitHub write/merge automation.

Additional offline Phase 2 evidence work may still add explicit trial identity/repeated-result structures and deterministic comparison/report generation before any real paid/runtime trial is authorized.

## Related Documents

- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Reproducible Developer Benchmark Corpus](/projects/notes/overlord-phase-2-developer-benchmark-corpus/)
- [Overlord Phase 2 — Developer Run Recovery and Lifecycle Audit](/projects/notes/overlord-phase-2-developer-recovery-audit/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: Overlord PR #14; exact final PR head `9e392777348911ba45a1db4d494ef3962d263cf8`; permanent PR-head CI #176; merged source `main` `fcfe9f9b6a21bc07b0a05b3fcf5a60f4ddc0d3d5`; post-merge CI #177; corpus schema v2; protected-path validation; Git evidence capture; benchmark JSON mapping; deterministic validator subprocess behavior; unit tests; and updated source architecture/development documentation.
- Verified by: High Director.
- Verification scope: validator tamper detection, workspace identity integrity, Git root/head/status/diff evidence, deterministic validator side effects, exact CI acceptance, and no-real-runtime/no-cost boundary.
