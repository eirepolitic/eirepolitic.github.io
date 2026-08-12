---
title: Overlord Phase 2 — Reproducible Developer Benchmark Corpus
summary: Implementation record for the non-billable Phase 2 evidence-preparation slice that adds isolated coding cases, clean Git workspace preparation, deterministic validators, and corpus-aware OpenHands/OpenCode comparison inputs.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 132
permalink: /projects/notes/overlord-phase-2-developer-benchmark-corpus/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - benchmark
  - openhands
  - opencode
---

# Overlord Phase 2 — Reproducible Developer Benchmark Corpus

## Outcome

The next non-billable Phase 2 evidence-preparation slice is complete.

Overlord now contains a small reproducible Developer Agent benchmark corpus designed to compare OpenHands and OpenCode on identical starting conditions before selecting a default coding runtime.

The corpus adds isolated bugfix, feature, and refactor cases; deterministic validators; clean Git-baseline preparation; separate runtime workspace requirements; CLI tooling; and corpus-aware validation in the real benchmark runner.

No real OpenHands/OpenCode execution occurred during this package. No paid model call, provider credential, worker provisioning, or recurring cloud infrastructure was required.

## Source Delivery

- Repository: `Overlord`
- Pull request: `#11` — `feat: add reproducible Developer benchmark corpus`
- Exact final PR head: `7e413410bf6dbe79c59d2e516e39cd0de51795a5`
- Exact PR-head permanent CI: run `#152` — `success`
- Final merged `main` commit: `a5d12b8ad8dbb1d571a89446cae46ce8961d6bb7`
- Exact post-merge permanent CI: run `#153` — `success`

The final documentation-inclusive PR head passed the complete permanent CI workflow before merge. The resulting squash commit on `main` passed the same workflow again after merge.

## Corpus Manifest

The versioned corpus manifest is:

```text
benchmarks/developer/manifest.json
```

It currently defines three cases:

```text
python-off-by-one      bugfix
python-config-feature  feature
python-slug-refactor   refactor
```

Each case contains:

- a stable case ID;
- an exact shared title/prompt;
- an isolated fixture directory;
- deterministic validator commands;
- a category used to ensure the corpus covers different coding behaviors.

## Case Coverage

### Bugfix

`python-off-by-one` starts with an inclusive-sum implementation that omits the upper endpoint.

The validator checks both the corrected inclusive behavior and preservation of the existing reverse-range `ValueError` behavior.

### Feature

`python-config-feature` starts with an unimplemented retry-policy parser.

The validator checks defaults, numeric-string coercion, lower-bound validation for attempts, and non-negative delay validation.

### Refactor

`python-slug-refactor` starts with working inline separator normalization but no reusable helper.

The task requires extracting `_collapse_separators()` while preserving external `normalize_slug()` behavior.

This prevents the benchmark from evaluating only one narrow class of coding task.

## Reproducible Workspace Preparation

`src/overlord/application/developer_benchmark_cases.py` adds the provider-neutral preparation/validation core.

`prepare_benchmark_case()`:

1. loads and validates the manifest;
2. locates the requested fixture;
3. refuses to overwrite a non-empty target directory;
4. copies the fixture into a fresh workspace;
5. writes `.overlord-benchmark.json` with the exact case definition;
6. optionally initializes a local Git repository;
7. configures a benchmark-only Git identity;
8. commits one clean baseline snapshot.

The resulting workspace is therefore resettable, auditable, and independent of the main Overlord repository state.

## Deterministic Validation

`validate_benchmark_case()`:

1. verifies the workspace contains benchmark metadata;
2. verifies that metadata matches the requested case;
3. executes the case's command arrays directly without shell interpolation;
4. captures return code, stdout, and stderr for each validator command;
5. stops on the first failing validator;
6. returns a structured overall pass/fail result.

The validator replaces the manifest's abstract `python` command with the currently running Python interpreter, making CI and local execution deterministic across environments.

## Baseline Safety Proof

Permanent tests verify that all three prepared baseline fixtures are intentionally unsolved.

That matters because a runtime cannot receive credit merely because the fixture already satisfied its validator.

The suite also proves that:

- a prepared Git baseline is clean immediately after preparation;
- the known correct repair for the bugfix case changes validation from failing to passing;
- preparation refuses to overwrite a non-empty target directory.

## Operator CLI

Two CLI wrappers make the corpus usable without application-layer imports.

Prepare a case:

```text
scripts/prepare_developer_benchmark_case.py
```

Validate a prepared workspace:

```text
scripts/validate_developer_benchmark_case.py
```

The validation CLI exits nonzero when a case fails, allowing the result to be consumed by scripts or later automation.

## Separate Runtime Workspaces

A fair OpenHands/OpenCode trial requires **two separately prepared workspaces** generated from the same case and repository commit.

The documented pattern is:

```text
/tmp/overlord-bench-openhands
/tmp/overlord-bench-opencode
```

One mutable workspace must not be reused for both runtimes. This prevents one coding agent from inheriting changes, artifacts, or Git state created by the other.

## Corpus-Aware Real Benchmark Runner

`scripts/benchmark_developer_agents.py` now requires:

```text
OVERLORD_DEVELOPER_BENCHMARK_CASE
OVERLORD_DEVELOPER_OPENHANDS_WORKSPACE
OVERLORD_DEVELOPER_OPENCODE_WORKSPACE
```

Rather than accepting a free-form prompt, the runner derives the exact shared title/description from the selected corpus case.

After each runtime completes, the runner validates that runtime's own prepared workspace and maps the deterministic validator result into benchmark evidence:

```text
completed
tests_passed
```

Runtime-native evidence remains separate, so a passing validator does not erase differences in event quality, cost, security posture, resource use, or operability.

## Fairness Rules

A comparison round should:

1. use the same case ID for both runtimes;
2. prepare both workspaces from the same source commit;
3. use equivalent model capability/cost constraints where practical;
4. avoid giving one runtime extra instructions unless intervention itself is being measured;
5. preserve raw runtime evidence and Git diffs;
6. run deterministic validators after completion;
7. leave unknown security/resource observations unknown rather than assuming success;
8. reset both workspaces before another trial.

One passing task is not enough evidence to select the default Developer runtime.

## CI Gate

Permanent CI run `#152` succeeded on exact final PR head:

`7e413410bf6dbe79c59d2e516e39cd0de51795a5`

Permanent CI run `#153` succeeded on exact merged `main` commit:

`a5d12b8ad8dbb1d571a89446cae46ce8961d6bb7`

Both gates included:

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

The full suite retained all existing Phase 0/1/2 coverage and added the benchmark corpus preparation/validation tests.

## Temporary Verification Cleanup

During branch development, temporary Ruff diagnostic/formatting workflows were used to capture one import-style finding and apply Ruff's canonical formatting.

Those temporary workflows and diagnostic files were removed before the final acceptance head.

The final source workflow tree remains limited to the permanent CI workflow.

## Cost and Security Boundary

This package is entirely non-billable in normal CI.

It does not:

- run OpenHands;
- run OpenCode;
- call a hosted coding model;
- require provider credentials;
- provision workers;
- create recurring cloud infrastructure.

The prototype's USD $50/month hard ceiling remains a resource governor, not an interaction quota.

Any future real benchmark remains explicitly opt-in because it may cause model/tool costs inside the separately configured coding runtimes.

## Runtime Selection Status

**OpenHands vs OpenCode remains undecided.**

The harness and reproducible corpus are now ready to collect evidence, but no real runtime comparison was executed as part of this slice.

The default Developer Agent should be selected only after repeated controlled trials provide enough evidence on completion quality, recovery, observability, permissions, Git behavior, cost, isolation, secret exposure, cleanup, resource use, and adapter maintenance burden.

## Boundaries Preserved

This package does **not** introduce:

- a selected default Developer runtime;
- Manager-to-Developer production delegation;
- autonomous repository modification by Overlord;
- remote or ephemeral Developer Workers;
- GitHub write/merge automation;
- production credential brokering;
- hosted deployment;
- recurring cloud resources;
- real coding-runtime execution in normal CI.

## Related Documents

- [Overlord — Phase 0 Closeout](/projects/notes/overlord-phase-0-closeout/)
- [Overlord Phase 1 — Local Manager Conversation Loop](/projects/notes/overlord-phase-1-local-manager-loop/)
- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [High Director Successor Research 06 — Build vs Adopt and Interoperability Boundaries](/projects/notes/high-director-successor-research-06/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: `Overlord` PR #11; exact final PR head `7e413410bf6dbe79c59d2e516e39cd0de51795a5`; permanent PR-head CI run #152; final merged `main` commit `a5d12b8ad8dbb1d571a89446cae46ce8961d6bb7`; exact post-merge permanent CI run #153; corpus manifest/fixtures; preparation and validation application code; CLI wrappers; corpus-aware benchmark runner; central architecture/development documentation; final workflow tree; and permanent corpus tests.
- Verified by: High Director.
- Verification scope: case diversity, clean baseline preparation, deterministic validation, separate runtime workspaces, baseline-unsolved proof, pass-after-fix proof, non-empty-target protection, corpus-aware benchmark inputs, offline acceptance, temporary-workflow cleanup, exact CI evidence, and no-runtime-selection constraint.
