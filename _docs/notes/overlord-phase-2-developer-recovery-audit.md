---
title: Overlord Phase 2 — Developer Run Recovery and Lifecycle Audit
summary: Implementation record for the non-billable Phase 2 slice that adds canonical Developer cancellation, failed-run retry, and deterministic AgentRun-correlated lifecycle audit events without selecting or invoking a real coding runtime.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 134
permalink: /projects/notes/overlord-phase-2-developer-recovery-audit/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - recovery
  - audit
---

# Overlord Phase 2 — Developer Run Recovery and Lifecycle Audit

## Outcome

The next non-billable Phase 2 Developer-execution slice is complete.

Overlord now supports explicit cancellation of active Developer runs, explicit retry of failed runs as new canonical `AgentRun` records, revalidation of owner/dependency gates before retry, and deterministic lifecycle `AuditEvent` records correlated to the canonical run ID.

The implementation remains provider-neutral behind `DeveloperAgentPort` and `DeveloperExecutionRepositoryPort`. The acceptance tests use PostgreSQL, FastAPI, DBOS application startup, and deterministic fake Developer adapters only.

**No real OpenHands/OpenCode execution occurred. No default Developer runtime has been selected.**

## Source Delivery

- Repository: `Overlord`
- Pull request: `#13` — `feat: add Developer run recovery and lifecycle audit`
- Exact final PR head: `8456b0c2359ce5a6fc7bd97fa6d55b151faf99ba`
- Exact PR-head permanent CI: run `#172` — `success`
- Final merged `main` commit: `c07e8bd9450f8a79c31688e59361177c1132af1c`
- Exact post-merge permanent CI: run `#173` — `success`

No dependency or schema change was required, and `uv.lock` was not changed.

## Cancellation Semantics

`POST /developer-runs/{agent-run-id}/cancel` accepts only active canonical runs (`created`, `running`, or `waiting`).

When the run already has an external session ID, Overlord first calls `DeveloperAgentPort.cancel()` on that external session. A successful cancellation then transitions:

```text
AgentRun -> cancelled
Task     -> ready
```

Cancellation deliberately does **not** cancel the enclosing Plan or WorkRequest. The cancelled run remains immutable history, while a later dispatch creates a new canonical `AgentRun`.

If the external runtime cancel call fails, Overlord records the failed cancel attempt in canonical audit history and leaves the canonical run active rather than falsely claiming cancellation.

## Failed-Run Retry

`POST /developer-runs/{agent-run-id}/retry` accepts only a failed Developer run.

Before retry, the canonical repository rechecks the same execution gates used for normal dispatch:

1. no unresolved owner decision for the Task;
2. all declared dependencies complete;
3. no active Developer run already exists for the Task.

The failed Task is returned to `ready`, then a **new** canonical `AgentRun` is created. The replacement run contains:

```text
retry_of_agent_run_id=<failed-run-id>
```

The failed run is never mutated back to an active status. Once the replacement runtime session starts, the Task and WorkRequest return to `running` through the normal canonical transition path.

## Canonical Lifecycle Audit

Developer execution now emits deterministic canonical `AuditEvent` rows through `DeveloperExecutionRepositoryPort`.

Each event uses:

```text
correlation_id = AgentRun.id
payload.agent_run_id = AgentRun.id
```

Stable lifecycle event types include:

```text
DEVELOPER_DISPATCH_CREATED
DEVELOPER_RUN_STARTED
DEVELOPER_RUN_WAITING
DEVELOPER_RUN_RESUMED
DEVELOPER_RUN_COMPLETED
DEVELOPER_RUN_FAILED
DEVELOPER_RUN_CANCELLED
DEVELOPER_CANCEL_FAILED
DEVELOPER_RESUME_FAILED
```

Dispatch-failure and finalization-failure audit payloads identify the lifecycle stage. Retry lineage is preserved on the replacement run metadata and dispatch audit payload.

The canonical `AgentRun(status=created)` and its dispatch audit record are committed before `DeveloperAgentPort.create_task()` contacts an external runtime.

## HTTP Surface

The Developer execution API now includes:

```text
POST /tasks/{task-id}/developer-runs
GET  /tasks/{task-id}/developer-runs
GET  /developer-runs/{agent-run-id}
POST /developer-runs/{agent-run-id}/waiting
POST /developer-runs/{agent-run-id}/resume
POST /developer-runs/{agent-run-id}/cancel
POST /developer-runs/{agent-run-id}/retry
POST /developer-runs/{agent-run-id}/finalize
```

Invalid canonical transitions return `409`, unknown records return `404`, and injected runtime failures return `502` where applicable.

The application still has no default Developer runtime. Without deliberate `DeveloperAgentPort` configuration, Developer execution endpoints return `503`.

## Acceptance Behavior

`tests/integration/test_developer_recovery_audit.py` proves two recovery paths using real local PostgreSQL plus fake runtime behavior.

Cancellation/redispatch proof:

1. dispatch a pending eligible Task;
2. cancel its active run;
3. verify the run is `cancelled` and the Task is `ready`;
4. redispatch the Task into a distinct canonical run;
5. finalize the replacement;
6. verify the WorkRequest completes;
7. verify exact run-correlated audit event sequences.

Failure/retry proof:

1. dispatch a Task;
2. inject one deterministic finalization failure;
3. verify the original AgentRun and Task are canonically `failed`;
4. retry the failed run;
5. verify a distinct replacement AgentRun with retry lineage;
6. finalize the replacement successfully;
7. verify the WorkRequest completes;
8. verify exact lifecycle audit sequences for both runs.

Existing delegation/dependency/wait/resume tests remain part of the full suite.

## CI Gate

Permanent CI run `#172` succeeded on exact final PR head:

`8456b0c2359ce5a6fc7bd97fa6d55b151faf99ba`

Permanent CI run `#173` succeeded on exact merged `main` commit:

`c07e8bd9450f8a79c31688e59361177c1132af1c`

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

## Cost and Security Boundaries

This slice is offline and non-billable in normal CI.

It does not:

- start OpenHands;
- start OpenCode;
- call a hosted coding model;
- require provider/runtime credentials;
- provision remote or recurring cloud infrastructure;
- add a production fake-runtime default;
- expose or broker long-lived secrets.

Runtime session identifiers remain external references on canonical AgentRuns. PostgreSQL remains authoritative for Task, WorkRequest, AgentRun, and AuditEvent lifecycle state.

## Deferred Work

This slice does not select OpenHands or OpenCode and does not enable automatic production dispatch into either runtime.

Controlled real benchmark execution, default-runtime selection, remote worker provisioning, GitHub write/merge brokering, credential brokering, and hosted deployment remain deferred to their approved boundaries.

Further credential-free Phase 2 benchmark-evidence hardening can proceed independently of the runtime selection decision.

## Related Documents

- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Reproducible Developer Benchmark Corpus](/projects/notes/overlord-phase-2-developer-benchmark-corpus/)
- [Overlord Phase 2 — Fake-Backed Manager Developer Delegation](/projects/notes/overlord-phase-2-manager-developer-delegation/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: Overlord PR #13; exact final PR head `8456b0c2359ce5a6fc7bd97fa6d55b151faf99ba`; permanent PR-head CI #172; merged `main` commit `c07e8bd9450f8a79c31688e59361177c1132af1c`; post-merge permanent CI #173; Developer execution service/repository/API changes; recovery/audit integration tests; and updated source architecture/development documentation.
- Verified by: High Director.
- Verification scope: cancellation truthfulness, redispatch, failed-run retry lineage, owner/dependency rechecks, canonical lifecycle auditing, canonical-first persistence, error mapping, exact CI acceptance, and no-real-runtime/cost boundary.
