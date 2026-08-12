---
title: Overlord P0.5 — DBOS Durable Manager Workflow
summary: Implementation record for Overlord P0.5, adding a local DBOS-backed durable Manager workflow that survives restart, waits for owner decisions, and prevents duplicate canonical planning state.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 128
permalink: /projects/notes/overlord-p0-5-dbos-durable-manager/
tags:
  - overlord
  - implementation
  - phase-0
  - p0-5
  - dbos
  - durability
  - workflow
---

# Overlord P0.5 — DBOS Durable Manager Workflow

## Outcome

P0.5 of the approved Overlord Phase 0 implementation sequence is complete.

Overlord now has a local DBOS-backed durable Manager workflow that can create canonical planning state, persist an owner decision request, stop while waiting for owner input, survive a DBOS runtime restart, receive the owner answer, and resume the exact workflow without duplicating canonical plans, tasks, decisions, or audit events.

DBOS remains workflow/runtime infrastructure rather than canonical state. Normal CI remains local, credential-free, and non-billable.

## Source Delivery

- Repository: `Overlord`
- Pull request: `#7` — `feat: add P0.5 DBOS durable Manager workflow`
- Exact final PR head: `7ca51e6266c5322363ad3d73dc67561f0658bda5`
- Exact PR-head permanent CI: run `#106` — `success`
- Final P0.5 `main` commit: `7b8fc8c0e02538c91b3dc724bf3bed8d910a9a04`
- Exact post-merge permanent CI: run `#107` — `success`

The exact final PR head passed the permanent Overlord CI workflow before merge. The resulting squash commit on `main` then passed the same workflow again after merge.

## Runtime Dependency

P0.5 adds DBOS as a declared runtime dependency:

```text
dbos>=2.29,<3.0
```

The branch lockfile was refreshed before final acceptance. The temporary lock-generation workflow was removed before the final PR-head gate.

Permanent CI passed:

```text
uv sync --locked --all-groups
```

on both the final PR head and the exact merged `main` commit.

## Planning Boundary Refactor

P0.5 separates model generation from canonical persistence without changing the existing public planning behavior.

`PlanningService.generate_work_request_plan()` now performs structured Manager generation without inserting canonical planning rows.

`persist_planning_generation()` converts one validated generation into canonical:

- `Plan`;
- `Task`;
- `TaskDependency`;
- `DecisionRequest`;
- `DecisionOption`;
- audit events.

The existing `PlanningService.plan_work_request()` still composes generation and persistence for ordinary non-durable callers.

This separation lets DBOS checkpoint model generation independently and then coordinate canonical writes through an exactly-once workflow transaction boundary.

## Durable Manager Workflow

`src/overlord/adapters/workflow/dbos_manager.py` contains the P0.5 DBOS adapter.

The durable flow is:

```text
canonical WorkRequest
        |
        v
DBOS Manager workflow
        |
        +--> checkpoint structured planning generation
        |
        +--> exactly-once canonical plan persistence
        |
        +--> persist DecisionRequest before waiting
        |
        +--> publish pending decision ID
        |
        +--> durable owner-message wait
        |
    process/runtime restart is allowed here
        |
        +--> receive owner decision
        |
        +--> exactly-once canonical decision resolution
        |
        +--> record resolution audit event
        |
        v
workflow completes
```

Application/domain planning code does not import DBOS. DBOS wraps application behavior from the workflow adapter layer.

## Stable Workflow Identity

The caller supplies a stable workflow ID using DBOS `SetWorkflowID`.

That ID is the idempotency boundary for one Manager execution. Attempting to start the same logical workflow again with the same ID returns/reuses the existing durable execution rather than producing another canonical plan.

Owner responses are sent on a decision-specific topic with a decision-specific idempotency key.

## Canonical Decision Resolution

P0.5 adds `DurableSqlAlchemyRepository` for the durable owner-decision write path.

Decision resolution is idempotent:

- replaying the same resolution is harmless;
- a conflicting second resolution is rejected;
- a selected option must belong to the decision request;
- the canonical request becomes resolved only after the owner decision is stored.

The resolution path also emits one `OWNER_DECISION_RESOLVED` audit event through the durable transaction boundary.

## State Ownership

P0.5 keeps three distinct storage concerns explicit.

### Canonical Overlord state

The `overlord` database remains authoritative for domain/application records such as:

- Work Requests;
- Plans;
- Tasks;
- Decision Requests;
- Owner Decisions;
- Audit Events.

### DBOS system state

The existing `overlord_dbos` database stores DBOS workflow, step, event, and message checkpoint state.

### DBOS datasource coordination

The DBOS SQLAlchemy datasource uses a `dbos_workflow` schema in the canonical database for transaction-coordination metadata required by exactly-once datasource steps.

That DBOS metadata is runtime coordination state. It is not the canonical representation of a Plan, Task, Decision, or Audit Event.

## Restart / Resume Acceptance Proof

`tests/integration/test_dbos_manager_workflow.py` exercises the P0.5 durability boundary entirely offline.

The test:

1. creates a canonical Work Request in local PostgreSQL;
2. starts a Manager workflow with a stable workflow ID and `FakeLLMAdapter`;
3. waits until the canonical Decision Request has been persisted;
4. verifies one plan, one task, one decision request, and the expected pre-wait audit records exist;
5. destroys the DBOS runtime while the workflow is waiting for owner input;
6. relaunches DBOS against the same durability database;
7. sends the owner answer to the original workflow ID;
8. retrieves the recovered workflow result;
9. starts the same workflow ID again;
10. verifies the fake model executed only once and canonical state was not duplicated.

After resume, the test verifies exactly one canonical:

```text
Plan
Task
DecisionRequest
OwnerDecision
PLAN_CREATED audit event
OWNER_DECISION_REQUIRED audit event
OWNER_DECISION_RESOLVED audit event
```

This proves the required restart/pause/resume and duplicate-retry behavior without a hosted model or provider credential.

## Offline / Cost Boundary

Normal P0.5 acceptance uses:

- local PostgreSQL;
- local DBOS runtime state;
- `FakeLLMAdapter` for the durable workflow test;
- the existing offline/default model configuration for the rest of CI.

P0.5 does not require:

- an OpenAI API key;
- an Anthropic API key;
- a Google model API key;
- a paid LLM request;
- DBOS Cloud/Conductor;
- recurring cloud infrastructure.

The existing `$50/month` prototype ceiling remains a spending policy rather than an interaction quota.

## CI Gate

Permanent CI run `#106` succeeded on the exact final PR head:

`7ca51e6266c5322363ad3d73dc67561f0658bda5`

Permanent CI run `#107` then succeeded on the exact merged `main` commit:

`7b8fc8c0e02538c91b3dc724bf3bed8d910a9a04`

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

The full pytest suite includes the DBOS restart/resume/idempotency integration test.

## Temporary Verification Cleanup

Temporary branch-only workflows used to refresh `uv.lock` and expose exact Ruff/mypy diagnostics were removed before the final acceptance run.

The final P0.5 workflow tree contains only:

```text
.github/workflows/ci.yml
```

No diagnostic output files remain in the source tree.

## Boundaries Preserved

P0.5 did **not** introduce:

- DBOS as canonical domain state;
- DBOS imports into the domain layer;
- Pydantic AI imports into planning/domain code;
- provider-native conversation state as authoritative state;
- a real provider credential requirement for CI;
- a billable model acceptance test;
- OpenHands or OpenCode execution;
- remote Developer Workers;
- production GitHub App automation;
- production cloud deployment;
- recurring DBOS/cloud infrastructure;
- PWA/mobile functionality.

## Next Work Package

P0.5 stops at the durable Manager workflow proof.

The published Phase 0 implementation plan does not currently define a separately named `P0.6` package. No P0.6 implementation is started or implied by this record. Any next package should first be matched to the approved remaining Phase 0 acceptance work rather than inventing new scope.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord P0.1 — Repository Foundation](/projects/notes/overlord-p0-1-repository-foundation/)
- [Overlord P0.2 — Domain Model and Persistence](/projects/notes/overlord-p0-2-domain-persistence/)
- [Overlord P0.3 — Ports, Fake Adapters, and Planning Contract](/projects/notes/overlord-p0-3-planning-contract/)
- [Overlord P0.4 — Pydantic AI Manager Adapter](/projects/notes/overlord-p0-4-pydantic-ai-adapter/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: `Overlord` PR #7, exact final PR head `7ca51e6266c5322363ad3d73dc67561f0658bda5`, permanent CI run #106, final `main` commit `7b8fc8c0e02538c91b3dc724bf3bed8d910a9a04`, permanent CI run #107, final dependency/workflow tree, durable workflow adapter, persistence adapter, source documentation, and DBOS restart/resume integration test.
- Verified by: High Director.
- Verification scope: DBOS dependency/lock state, planning generation/persistence separation, stable workflow identity, durable owner-decision wait, restart/recovery, exactly-once canonical side effects, duplicate protection, state-ownership boundaries, offline CI, temporary-workflow cleanup, and exact post-merge verification.
