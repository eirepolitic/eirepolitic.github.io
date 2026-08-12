---
title: Overlord Phase 1 — Local Manager Conversation Loop
summary: Implementation record for the first Phase 1 slice, adding a persistent local HTTP conversation and planning loop backed by canonical PostgreSQL state, DBOS durability, and offline model defaults.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 130
permalink: /projects/notes/overlord-phase-1-local-manager-loop/
tags:
  - overlord
  - implementation
  - phase-1
  - manager
  - fastapi
  - dbos
  - conversation
---

# Overlord Phase 1 — Local Manager Conversation Loop

## Outcome

The first approved Phase 1 slice is complete.

Overlord now exposes a working local, text-first Manager conversation/planning loop over FastAPI. An owner can create a canonical conversation, submit a text request, persist that request before any workflow side effect, start the durable Manager, inspect the resulting canonical Plan/Task/Decision state, answer a pending owner decision, and observe the same durable workflow resume to a ready state.

The slice deliberately stops before Developer Agent execution. Normal CI remains local, credential-free, and non-billable.

## Source Delivery

- Repository: `Overlord`
- Pull request: `#9` — `feat: add Phase 1 local Manager conversation loop`
- Exact final PR head: `49e58236cf3470c9bda94fb143bfc7c059e5fc8a`
- Exact PR-head permanent CI: run `#129` — `success`
- Final merged `main` commit: `312fd4692c1fefaedf49e949c11974c7eb3dd3cb`
- Exact post-merge permanent CI: run `#130` — `success`

No runtime dependency change was required for this slice, so the previously verified `uv.lock` remained current. Both the final PR head and the exact merged `main` commit passed `uv sync --locked --all-groups` as part of permanent CI.

## Local HTTP Surface

Phase 1 adds the first functional local control-plane API beyond health/readiness.

### Create a conversation

```text
POST /conversations
```

Creates a canonical `Conversation` in PostgreSQL.

### Read conversation history

```text
GET /conversations/{conversation_id}
```

Returns the canonical conversation plus persisted canonical messages in creation order.

### Submit an owner request

```text
POST /conversations/{conversation_id}/messages
```

The application:

1. verifies the conversation exists;
2. normalizes and validates the owner text;
3. creates a canonical `WorkRequest` with status `planning`;
4. creates the canonical owner `Message` linked to that WorkRequest;
5. commits both records to PostgreSQL;
6. starts the durable Manager workflow using the stable logical workflow identity.

The canonical owner request therefore exists before the external workflow start is attempted.

### Read planning state

```text
GET /work-requests/{work_request_id}
```

Returns the canonical WorkRequest, latest Plan, Tasks, pending Decision Requests/options, and the stable Manager workflow ID.

### Answer an owner decision

```text
POST /work-requests/{work_request_id}/decisions/{decision_request_id}
```

Before sending anything to DBOS, the application verifies that:

- the WorkRequest exists;
- the Decision Request is still pending for that WorkRequest;
- any selected option belongs to that Decision Request;
- the response text is not blank.

The answer is then delivered to the original durable Manager workflow.

## Application Boundary

`src/overlord/application/conversation_loop.py` contains the provider/runtime-neutral Phase 1 application service.

`LocalManagerService` depends on two Overlord-owned ports:

```text
ConversationRepositoryPort
ManagerWorkflowPort
```

It does not import:

- FastAPI;
- SQLAlchemy;
- DBOS;
- Pydantic AI;
- provider SDKs.

This keeps the Phase 0 ports-and-adapters direction intact while adding a real application loop.

## Conversation Persistence Boundary

`ConversationRepositoryPort` provides only the canonical reads/writes needed by the local Manager loop:

- create/read conversations;
- append/read messages;
- create/read Work Requests;
- update Work Request status;
- read the latest Plan;
- read Tasks;
- read pending Decision Requests/options;
- explicitly commit the canonical transaction.

`ConversationRepository` implements that contract with SQLAlchemy/PostgreSQL without exposing ORM rows or sessions through the application layer.

The owner Message and WorkRequest commit before durable workflow start. If workflow startup fails, the owner request remains canonical in `planning` and can be retried with the same stable workflow identity rather than being lost in an uncommitted transaction.

## Durable Workflow Port

Phase 1 introduces `ManagerWorkflowPort` so application code does not depend on DBOS directly.

The DBOS implementation is `DBOSManagerRuntime`.

Logical workflow identity is deterministic:

```text
manager:<work-request-id>
```

This is the idempotency/recovery identity for the Manager execution.

The DBOS configured-instance registration used by the FastAPI process is separately named:

```text
manager-api
```

That configured-instance name exists only to register the runtime implementation safely inside DBOS. It is not canonical work identity and does not replace the stable logical workflow ID.

## Canonical Status Progression

Phase 1 makes workflow progress visible in canonical application state rather than requiring an API client to inspect DBOS internals.

A normal owner-decision path is:

```text
WorkRequest
planning
   |
   v
waiting_owner
   |
   v
ready
```

When planning produces no owner decisions, plan persistence moves the WorkRequest directly from `planning` to `ready`.

When planning requires owner input:

- the canonical WorkRequest becomes `waiting_owner`;
- the decision-bound Task is `waiting_owner`;
- the durable workflow waits for the owner response.

When the final pending decision is resolved:

- the canonical Decision Request becomes resolved;
- the bound Task moves from `waiting_owner` to `ready`;
- the WorkRequest moves to `ready`.

These transitions occur inside the existing DBOS SQLAlchemy datasource transaction boundary for durable canonical side effects.

## Offline Model Defaults

Phase 1 restores and locks the intended P0.4 capability defaults:

```text
OVERLORD_MODEL_EFFICIENT=test
OVERLORD_MODEL_BALANCED=test
OVERLORD_MODEL_FRONTIER=test
```

The default local application can therefore use the real `PydanticAIAdapter` with Pydantic AI's offline `test` model and no provider credential.

Configuration may still explicitly set a capability mapping to `None`; `require_model_id()` then fails before a provider call. Provider/model switching remains configuration-only.

## End-to-End Acceptance Test

`tests/integration/test_local_manager_api.py` proves the Phase 1 loop through the real HTTP surface.

The test uses:

- FastAPI `TestClient`;
- the real local PostgreSQL database;
- the real DBOS durable workflow runtime;
- `FakeLLMAdapter` with deterministic structured Manager output;
- no provider credential or network model call.

The test performs this sequence:

1. create a conversation through `POST /conversations`;
2. submit an owner request through the message endpoint;
3. verify the returned WorkRequest begins in `planning`;
4. verify the stable workflow ID is `manager:<work-request-id>`;
5. read the canonical conversation history and confirm the owner message persisted;
6. poll canonical planning state until the WorkRequest reaches `waiting_owner`;
7. verify the Plan, waiting Task, Decision Request, and Decision Option are visible through the API;
8. submit the valid owner decision through the decision endpoint;
9. allow the same durable workflow to resume;
10. poll until the WorkRequest reaches `ready`;
11. verify the pending decision list is empty and the decision-bound Task is `ready`;
12. verify the fake Manager model executed exactly once.

The pre-existing P0.5 restart/resume/idempotency test remains in the permanent suite as a separate durability proof.

## CI Gate

Permanent CI run `#129` succeeded on exact final PR head:

`49e58236cf3470c9bda94fb143bfc7c059e5fc8a`

Permanent CI run `#130` succeeded on exact merged `main` commit:

`312fd4692c1fefaedf49e949c11974c7eb3dd3cb`

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

The final test suite includes the new HTTP Manager-loop proof, existing DBOS restart/recovery proof, Pydantic AI offline contract tests, canonical persistence tests, policy/security tests, and architecture dependency tests.

## Cost and Security Boundaries

This Phase 1 slice does not change the approved cost/security model.

Normal acceptance requires:

- no OpenAI credential;
- no Anthropic credential;
- no Google model credential;
- no billable model request;
- no DBOS Cloud/Conductor;
- no recurring cloud infrastructure.

The global prototype hard ceiling remains USD $50/month as a resource governor, not an interaction quota.

The local API does not expose raw database sessions, DBOS checkpoint records, or provider-native model/session objects as canonical state.

## Boundaries Preserved

This slice does **not** introduce:

- Developer Agent execution;
- OpenHands or OpenCode integration;
- autonomous repository modification;
- GitHub write/merge automation;
- remote or ephemeral Developer Workers;
- hosted deployment;
- production authentication/passkeys;
- PWA/mobile UI;
- notifications or speech-provider calls;
- real-provider credentials in CI;
- recurring cloud infrastructure.

## Next Stage

The approved architecture sequence identifies the next major capability after the local Manager loop as adding one Developer Agent behind the existing `DeveloperAgentPort`.

That work is **not** started by this implementation record. Phase 1 stops at the verified local Manager conversation/planning/owner-decision loop.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord — Phase 0 Closeout](/projects/notes/overlord-phase-0-closeout/)
- [Overlord P0.4 — Pydantic AI Manager Adapter](/projects/notes/overlord-p0-4-pydantic-ai-adapter/)
- [Overlord P0.5 — DBOS Durable Manager Workflow](/projects/notes/overlord-p0-5-dbos-durable-manager/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: `Overlord` PR #9; exact final PR head `49e58236cf3470c9bda94fb143bfc7c059e5fc8a`; permanent PR-head CI run #129; final merged `main` commit `312fd4692c1fefaedf49e949c11974c7eb3dd3cb`; exact post-merge permanent CI run #130; Phase 1 API/application/repository/workflow adapter source; source architecture/development documentation; offline model-default tests; HTTP integration test; and the existing P0.5 durability test.
- Verified by: High Director.
- Verification scope: persistent local conversation flow, canonical transaction ordering, provider-neutral application boundaries, stable DBOS workflow identity, canonical status progression, owner-decision validation/resume, offline model defaults, exact CI results, and preserved Phase 1 scope boundaries.
