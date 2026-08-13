---
title: Overlord Phase 2 — Repeated Benchmark Case Selection
summary: Implementation record for allow-listed corpus case selection supporting the approved eight-new-trial Developer benchmark phase.
section: notes
doc_type: note
status: active
created: 2026-08-13
updated: 2026-08-13
last_verified: 2026-08-13
owner: High Director
order: 141
permalink: /projects/notes/overlord-phase-2-repeated-benchmark-case-selection/
tags:
  - overlord
  - phase-2
  - developer-agent
  - benchmark
  - openhands
  - opencode
  - github-actions
---

# Overlord Phase 2 — Repeated Benchmark Case Selection

## Outcome

The guarded real Developer benchmark can now select any of the three approved canonical corpus cases through repository Actions variable `OVERLORD_BENCHMARK_CASE` while preserving the existing one-shot authorization, duplicate-cancelling concurrency, fixed provider/model/runtime versions, and read-only GitHub permission boundary.

The workflow allow-list is exactly:

```text
python-off-by-one
python-config-feature
python-slug-refactor
```

Any other case value fails in the first authorization step, before checkout or provider-secret access.

## Source Acceptance

Source PR `#22` — `feat: allow approved repeated benchmark case selection`:

```text
exact final PR head:       fec985ee2b7a763968fda764f423b0c8767882f6
PR permanent CI:           #233
PR CI run ID:              31736460229
PR CI conclusion:          success
merged source main:        b9924b251a97a0f78ba5b0801907c43da559fb78
post-merge CI:             #234
post-merge CI run ID:      31736603356
post-merge CI conclusion:  success
```

Both CI gates included Compose validation, PostgreSQL startup/readiness, locked dependency synchronization, Ruff lint, Ruff format check, strict mypy, Alembic upgrade, and full pytest.

No database migration, application dependency/lock change, provider/model change, runtime selection, or budget-policy change occurred.

## Approved Repeated Phase

The owner approved eight new paid comparisons under the existing benchmark-only `$10` hard ceiling:

```text
python-off-by-one:      2 new accepted trials
python-config-feature:  3 new accepted trials
python-slug-refactor:   3 new accepted trials
```

The previously accepted `python-off-by-one` trial remains the first accepted observation for that case. The historical unintended duplicate remains excluded.

Each comparison keeps:

```text
provider:                  openai
model:                     gpt-5.6-luna
OpenHands Agent Server:    1.42.0
OpenHands SDK/tools/ws:    1.42.1
OpenHands Python:          3.12
OpenCode:                  1.18.16
GitHub permission:         contents: read
benchmark timeout:         12 minutes
job timeout:               20 minutes
```

## One-at-a-Time Execution Boundary

Each approved paid comparison is executed sequentially:

1. select the allow-listed case with `OVERLORD_BENCHMARK_CASE`;
2. assign a unique `OVERLORD_BENCHMARK_AUTHORIZATION_ID`;
3. set `OVERLORD_BENCHMARK_RUN_CONFIRMATION=RUN_ONE_TRIAL`;
4. enable and dispatch the real workflow once;
5. verify the first authorization-latch step succeeds;
6. immediately restore `UNARMED` / `DISABLED` and disable the workflow;
7. require the captured run to complete successfully before starting another accepted trial.

The 30-second no-secret debounce and `cancel-in-progress: true` concurrency remain mandatory.

Trial JSON and summaries remain evaluation artifacts rather than canonical PostgreSQL state. This change does not select a Developer runtime.

## Verification Record

- Last verified: `2026-08-13`.
- Verified against: source PR #22 exact final head `fec985ee2b7a763968fda764f423b0c8767882f6`; permanent CI #233; merged source main `b9924b251a97a0f78ba5b0801907c43da559fb78`; post-merge CI #234; and the allow-listed real workflow definition.
- Verified by: High Director.
