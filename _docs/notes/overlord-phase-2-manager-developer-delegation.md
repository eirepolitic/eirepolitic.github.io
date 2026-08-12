---
title: Overlord Phase 2 — Fake-Backed Manager Developer Delegation
summary: Implementation record for the non-billable Phase 2 slice that adds canonical Developer execution state, Manager-to-DeveloperAgentPort delegation, dependency-aware dispatch, waiting/resume/finalization, and local API visibility using the fake Developer runtime in CI.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 133
permalink: /projects/notes/overlord-phase-2-manager-developer-delegation/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - delegation
  - manager
  - dbos
---

# Overlord Phase 2 — Fake-Backed Manager Developer Delegation

## Outcome

The next non-billable Phase 2 product slice is complete.

Overlord can now dispatch canonical Tasks through the existing provider-neutral `DeveloperAgentPort`, track canonical `AgentRun` state, reject duplicate active execution, respect owner-decision/dependency gates, wait/resume the same external session, finalize usage/evidence, promote newly unblocked tasks, and complete the Plan/WorkRequest when all tasks finish.

The full flow is proven through FastAPI + PostgreSQL + DBOS application startup with `FakeDeveloperAgentAdapter`.

**No real OpenHands/OpenCode execution occurred. No default Developer runtime has been selected.**

## Source Delivery

- Repository: `Overlord`
- Pull request: `#12` — `feat: add fake-backed Manager Developer delegation`
- Exact final PR head: `38d401f30aa5bed0f8fcd090598bea6fcfef363a`
- Exact PR-head permanent CI: run `#170` — `success`
- Final merged `main` commit: `7f83525f6e13c8f08a9bc248a0986ed1ffc6adf4`
- Exact post-merge permanent CI: run `#171` — `success`

The final PR workflow tree contained only the permanent `ci.yml` workflow.

## Canonical Execution Boundary

`DeveloperExecutionRepositoryPort` is the new application-facing persistence contract for execution state.

The SQLAlchemy implementation owns:

- task eligibility and promotion;
- row-locked task/run transitions;
- canonical AgentRun creation;
- active-run duplicate prevention;
- external-session reference storage;
- waiting/resume transitions;
- completion/failure transitions;
- dependent-task promotion;
- Plan/WorkRequest completion.

No new database schema was required; the slice reuses existing Task, TaskDependency, Plan, WorkRequest, DecisionRequest, and AgentRun records.

## Dispatch Eligibility

A task already in `ready` is dispatchable.

A `pending` task may move to `ready` only when:

1. it has no unresolved owner decision;
2. every declared dependency is complete.

Other task states cannot be dispatched.

The repository rejects a second active Developer AgentRun while an existing run for the task is `created`, `running`, or `waiting`.

## Canonical-First Runtime Start

`DeveloperExecutionService.dispatch()` creates and commits the canonical AgentRun **before** calling the external `DeveloperAgentPort`.

The sequence is:

```text
Task eligible
  -> AgentRun(created) persisted + committed
  -> DeveloperAgentPort.create_task(...)
  -> external session ID stored
  -> AgentRun(running)
  -> Task(running)
  -> WorkRequest(running)
```

If runtime startup raises, the canonical AgentRun, Task, and WorkRequest are marked failed instead of losing the dispatch attempt.

The external session ID remains an adapter/runtime reference; it never replaces the canonical AgentRun ID.

## Waiting and Resume

A running Developer run can transition to canonical `waiting`.

Resume calls `DeveloperAgentPort.resume()` using the stored external session ID, then transitions the canonical AgentRun back to `running`.

This proves that Manager-side orchestration can pause/resume the same coding-runtime session without adopting runtime-native state as canonical state.

## Finalization

Finalization obtains:

- runtime final evidence;
- runtime summary;
- normalized usage/cost metadata.

These values are persisted in canonical AgentRun metadata.

Successful finalization transitions:

```text
AgentRun -> completed
Task     -> completed
```

Completing a task reevaluates pending tasks in the same Plan. A task whose dependencies are now complete and which has no unresolved owner decision is promoted to `ready`.

When every task in the Plan is complete, the Plan and WorkRequest become `completed`.

A runtime finalization error instead marks the AgentRun, Task, and WorkRequest failed and stores the error in run metadata.

## Local API Surface

The FastAPI application now exposes:

```text
POST /tasks/{task-id}/developer-runs
GET  /tasks/{task-id}/developer-runs
GET  /developer-runs/{agent-run-id}
POST /developer-runs/{agent-run-id}/waiting
POST /developer-runs/{agent-run-id}/resume
POST /developer-runs/{agent-run-id}/finalize
```

The application has **no default Developer runtime**.

If `create_app()` is started without a deliberately injected/configured `DeveloperAgentPort`, Developer execution endpoints return HTTP `503`.

This prevents the fake adapter, OpenHands, or OpenCode from becoming an accidental production default.

## Acceptance Test

`tests/integration/test_developer_delegation_api.py` uses:

- real local PostgreSQL;
- FastAPI `TestClient`;
- normal DBOS application startup;
- `FakeDeveloperAgentAdapter`;
- no real model/coding-runtime credential.

The test creates a Plan with two dependent Tasks and proves:

1. the dependency-free pending task is promoted and dispatched;
2. duplicate active dispatch is rejected;
3. the first run finalizes and stores zero-cost fake usage;
4. completing task one automatically unblocks task two;
5. task two dispatches;
6. task two enters `waiting`;
7. the same run resumes;
8. task two finalizes;
9. Developer run query endpoints return canonical state;
10. the final Plan and WorkRequest become `completed`.

## DBOS Test-Isolation Regression

The new delegation API test initially exposed an existing DBOS configured-instance registry limitation when multiple FastAPI app lifespans were created in one pytest process.

`DBOS.destroy()` shuts down the runtime but does not remove the configured-instance registration, so two apps using `manager-api` caused a duplicate registration failure.

The fix preserves the production default `manager-api` while allowing `create_app()` to accept an alternate `manager_instance_name` for isolated embedded/test app instances.

The delegation test uses `manager-api-delegation-test`. Logical workflow IDs remain `manager:<work-request-id>` and canonical workflow semantics are unchanged.

The exact regression suite then passed both the existing Phase 1 Manager HTTP test and the new delegation HTTP test together.

## CI Gate

Permanent CI run `#170` succeeded on exact final PR head:

`38d401f30aa5bed0f8fcd090598bea6fcfef363a`

Permanent CI run `#171` succeeded on exact merged `main` commit:

`7f83525f6e13c8f08a9bc248a0986ed1ffc6adf4`

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

## Temporary Diagnostic Cleanup

During development, temporary branch-only Ruff and pytest diagnostic workflows were used to capture exact failures.

The discovered issues were limited to:

- two Ruff findings in the new application service;
- Ruff canonical formatting;
- the DBOS configured-instance collision between multiple app tests.

All temporary workflows and diagnostic files were deleted before the final PR head. The final source workflow tree contained only `.github/workflows/ci.yml`.

## Cost and Security Boundaries

This slice is non-billable in normal CI.

It does not:

- start OpenHands;
- start OpenCode;
- call a hosted coding model;
- require coding-runtime/provider credentials;
- provision a remote worker;
- create recurring cloud infrastructure.

The fake execution metadata identifies the runtime/provider/model as `fake` / `offline` / `deterministic` and reports zero cost.

Long-lived platform/provider credentials remain outside repository-controlled coding execution.

## Runtime Selection Status

**OpenHands vs OpenCode remains undecided.**

This slice proves the control-plane delegation mechanics independently of the coding runtime. The same `DeveloperExecutionService` can later operate against whichever `DeveloperAgentPort` implementation is selected by controlled benchmark evidence.

No production automatic Manager-to-real-Developer delegation is enabled yet.

## Related Documents

- [Overlord Phase 1 — Local Manager Conversation Loop](/projects/notes/overlord-phase-1-local-manager-loop/)
- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Reproducible Developer Benchmark Corpus](/projects/notes/overlord-phase-2-developer-benchmark-corpus/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: Overlord PR #12; exact final PR head `38d401f30aa5bed0f8fcd090598bea6fcfef363a`; permanent PR-head CI #170; merged `main` commit `7f83525f6e13c8f08a9bc248a0986ed1ffc6adf4`; post-merge permanent CI #171; canonical execution repository/service/API source; fake-backed delegation integration test; updated source architecture/development documentation; and final workflow tree.
- Verified by: High Director.
- Verification scope: eligibility/dependency gating, canonical-first AgentRun persistence, duplicate prevention, waiting/resume, completion/failure propagation, dependent promotion, WorkRequest completion, unconfigured-runtime protection, DBOS test isolation, exact CI results, no-real-runtime constraint, and temporary diagnostic cleanup.
