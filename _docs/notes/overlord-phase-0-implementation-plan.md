---
title: Overlord Phase 0 — Implementation Plan
summary: Concrete Phase 0 implementation contract for the Overlord successor control plane, defining repository structure, domain models, interfaces, local stack, tests, security boundaries, and acceptance gates before agent/runtime integration begins.
section: notes
doc_type: note
status: active
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
owner: High Director
order: 123
permalink: /projects/notes/overlord-phase-0-implementation-plan/
tags:
  - overlord
  - high-director
  - successor
  - implementation
  - phase-0
  - architecture
  - python
  - postgres
---

# Overlord Phase 0 — Implementation Plan

## Purpose

This document turns the approved High Director successor architecture into a concrete **Phase 0 implementation contract** for the existing `Overlord` repository.

Phase 0 is intentionally narrow. Its purpose is to create the durable application spine and stable internal interfaces that later Manager Agents, Developer Agents, LLM providers, GitHub tooling, mobile clients, and cloud workers will use.

Phase 0 must **not** couple Overlord to one LLM provider, one coding-agent runtime, or one cloud host.

No recurring cloud infrastructure is required for Phase 0.

## Approved Product Decisions Carried Into Phase 0

The following decisions are already approved and should not be reopened during Phase 0 unless implementation evidence shows a material problem:

- project/repository: `Overlord`;
- prototype monthly spending ceiling: USD `$50`, treated as a spending ceiling rather than a user-message quota;
- MVP integration scope: GitHub development lifecycle first;
- Manager runtime direction: Pydantic AI behind an Overlord-owned interface;
- durable workflow direction: DBOS + PostgreSQL;
- Developer runtime direction: benchmark OpenHands and OpenCode behind the same Overlord-owned adapter;
- owner-facing client direction: installable PWA;
- authentication direction: passkeys/WebAuthn;
- voice direction: push-to-talk STT plus optional short TTS summaries;
- automation identity: GitHub App;
- runtime secrets direction: GitHub Actions Secrets for CI/CD and a runtime secret-store abstraction, with AWS Secrets Manager as the current production candidate;
- durable state must live outside provider/agent conversations;
- disposable Developer Workers rather than permanently running coding-agent machines;
- first-version tool interoperability should prefer MCP where it helps portability;
- ACP may be used for coding-agent adapters;
- A2A is deferred until independent remote-agent services are actually required.

## Phase 0 Goal

At the end of Phase 0, Overlord must be able to represent, validate, persist, retrieve, and test the lifecycle:

```text
Owner Work Request
       |
       v
Plan
       |
       v
Development Task(s)
       |
       +--> Agent Run reference
       |
       +--> Event history
       |
       +--> Decision / Approval if required
       |
       v
Completion / Failure / Cancellation
```

This must work **without** requiring a real LLM provider, OpenHands/OpenCode, GitHub App, remote worker, phone app, or cloud deployment.

That requirement is fundamental. If the lifecycle only exists inside a model or coding-agent session, Phase 0 has failed.

## Existing Repository State

The current `Overlord` repository is effectively a clean application slate.

Existing content consists of:

- a small README;
- several Markdown task fixtures under `tasks/`;
- task templates under `templates/tasks/`.

These files should be preserved during Phase 0. They may later be converted into test fixtures or migrated into the new task model, but there is no need to delete or restructure them before the application foundation exists.

## Technology Baseline

### Language

Use **Python 3.13** for the initial backend/control-plane implementation.

Rationale:

- fully compatible with the selected Python ecosystem direction;
- conservative enough to avoid making the project depend immediately on the newest interpreter release;
- easy later migration path;
- current Pydantic AI and DBOS requirements are below this baseline.

Python version should be declared centrally and enforced in CI.

### Packaging and dependency management

Use standard `pyproject.toml` packaging.

Recommended approach:

- `uv` for local environment/dependency management and lockfile generation;
- PEP 621 project metadata;
- no globally installed project dependencies required;
- committed lockfile for reproducible local/CI installs.

If a later CI/environment constraint makes `uv` problematic, the project metadata should remain usable with standard Python tooling.

### API framework

Use **FastAPI** for the HTTP control-plane API.

Phase 0 will expose only development/health/domain endpoints required to validate the architecture; owner-facing production authentication is not yet implemented.

### Validation/domain schemas

Use **Pydantic v2** for API/configuration/domain boundary validation.

Do not make Pydantic models themselves the persistence schema. Domain records and persistence mappings remain separately controlled.

### Database

Use **PostgreSQL**.

Local Phase 0 Postgres should run through Docker Compose.

The database is the authoritative store for application-domain state.

### Database access

Use **SQLAlchemy 2.x** with explicit repository/unit-of-work boundaries.

Use **Alembic** for schema migrations.

The domain layer must not import SQLAlchemy models directly.

### Durable workflow

Add **DBOS** only after the core domain/persistence lifecycle is working.

DBOS is Phase 0 scope because we need to prove durable pause/resume semantics, but it should be integrated after basic domain state so DBOS internals do not become the domain model.

### Tests

Use:

- `pytest`;
- `pytest-asyncio` where asynchronous tests are required;
- HTTP client integration tests against FastAPI;
- real Postgres integration tests for persistence/migrations;
- mocks/fakes only at external-adapter boundaries.

### Static quality tooling

Use:

- `ruff` for linting and formatting;
- `mypy` for static typing;
- `pytest` for behavior;
- coverage reporting with a meaningful threshold after initial scaffolding stabilizes.

Do not add overlapping formatters/linters unless there is a demonstrated need.

## Proposed Repository Structure

```text
Overlord/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── architecture/
│   ├── decisions/
│   └── development/
│
├── migrations/
│   ├── env.py
│   └── versions/
│
├── src/
│   └── overlord/
│       ├── __init__.py
│       │
│       ├── api/
│       │   ├── app.py
│       │   ├── dependencies.py
│       │   └── routes/
│       │
│       ├── domain/
│       │   ├── enums.py
│       │   ├── errors.py
│       │   ├── models/
│       │   └── services/
│       │
│       ├── persistence/
│       │   ├── database.py
│       │   ├── orm/
│       │   ├── repositories/
│       │   └── unit_of_work.py
│       │
│       ├── workflows/
│       │   ├── manager.py
│       │   └── task_lifecycle.py
│       │
│       ├── agents/
│       │   ├── manager.py
│       │   └── developer.py
│       │
│       ├── policies/
│       │   ├── approvals.py
│       │   ├── budgets.py
│       │   └── permissions.py
│       │
│       ├── tools/
│       │   ├── contracts.py
│       │   └── registry.py
│       │
│       ├── adapters/
│       │   ├── llm/
│       │   ├── developer/
│       │   ├── github/
│       │   ├── secrets/
│       │   ├── notifications/
│       │   ├── speech/
│       │   └── object_store/
│       │
│       ├── events/
│       │   ├── models.py
│       │   └── publisher.py
│       │
│       ├── config/
│       │   ├── settings.py
│       │   └── logging.py
│       │
│       └── observability/
│           ├── logging.py
│           └── metrics.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   └── fixtures/
│
├── tasks/
│   └── ... existing files preserved
├── templates/
│   └── ... existing files preserved
│
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

This structure is a starting contract, not a requirement to create empty modules for every future component immediately. Create a package only when Phase 0 code/tests require it.

## Architectural Dependency Rule

The intended dependency direction is:

```text
api / workflows / adapters
          |
          v
application/domain services
          |
          v
domain contracts/models
```

Persistence, Pydantic AI, DBOS, GitHub, OpenHands, OpenCode, AWS, or other vendor-specific objects must not leak into core domain models.

Examples:

- `Task` must not contain an `OpenHandsConversation` object;
- `ModelProfile` must not require an OpenAI-specific request class;
- `ApprovalRequest` must not depend on DBOS internals;
- domain services must not require FastAPI request objects;
- worker/task state must not be identified solely by an external runtime ID.

## Identifier Strategy

Use application-generated UUIDs for durable entities.

Recommended identifiers:

- `conversation_id`;
- `message_id`;
- `work_request_id`;
- `plan_id`;
- `task_id`;
- `agent_run_id`;
- `decision_id`;
- `approval_request_id`;
- `tool_call_id`;
- `event_id`;
- `external_resource_id`.

External IDs such as GitHub PR numbers, OpenHands conversation IDs, OpenCode session IDs, DBOS workflow IDs, or model-provider request IDs are stored as references, never as the application's primary identity.

## Domain Model v1

### Conversation

Represents one owner/Manager conversational thread.

Core fields:

```text
id
status
created_at
updated_at
```

Phase 0 needs only one conceptual owner, but the schema should not embed the owner's identity into conversation IDs or application globals.

### Message

Canonical text/event message stored independently of provider format.

Core fields:

```text
id
conversation_id
author_type
content_type
text
created_at
source_mode
related_task_id?
model_call_id?
metadata
```

Initial `author_type` values:

```text
OWNER
MANAGER
DEVELOPER
SYSTEM
TOOL
```

Initial `source_mode` values:

```text
TEXT
VOICE_TRANSCRIPT
AGENT
TOOL
SYSTEM
```

### WorkRequest

Represents the owner's requested outcome.

Core fields:

```text
id
conversation_id
title
description
status
created_at
updated_at
```

Suggested statuses:

```text
DRAFT
ACTIVE
WAITING_FOR_OWNER
COMPLETED
CANCELLED
FAILED
```

### Plan

A versioned plan for satisfying one WorkRequest.

Core fields:

```text
id
work_request_id
version
summary
status
created_at
created_by
```

Plans should be append/version oriented rather than overwritten invisibly.

### Task

Durable unit of executable development work.

Core fields:

```text
id
work_request_id
plan_id
title
description
status
priority
created_at
updated_at
repository_ref?
```

Suggested statuses:

```text
PENDING
READY
RUNNING
WAITING_FOR_OWNER
BLOCKED
VALIDATING
COMPLETED
FAILED
CANCELLED
```

### TaskDependency

Represents ordering/dependency relationships between tasks.

Core fields:

```text
predecessor_task_id
successor_task_id
dependency_type
```

Phase 0 only needs simple blocking dependencies.

### AgentRun

Represents one attempt to perform or supervise work using an agent runtime/model.

Core fields:

```text
id
task_id
agent_role
runtime_adapter
model_profile
status
started_at
ended_at
external_session_id?
```

`runtime_adapter` is a normalized identifier such as `fake`, `openhands`, or `opencode`, not a runtime-specific object.

### DecisionRequest

Represents a question that genuinely requires owner input.

Core fields:

```text
id
work_request_id?
task_id?
category
question
context_summary
recommended_option?
status
created_at
resolved_at?
```

Suggested categories:

```text
REQUIREMENTS
ARCHITECTURE
SECURITY
ACCESS
COST
DESTRUCTIVE_ACTION
PRIVACY
EXTERNAL_COMMITMENT
AMBIGUITY
```

### DecisionResponse

Stores the owner's exact response separately from the Manager's interpretation.

Core fields:

```text
id
decision_request_id
response_text
selected_option?
created_at
```

### ApprovalRequest

Represents permission to execute a potentially sensitive action.

This is distinct from a product/architecture decision.

Core fields:

```text
id
task_id?
action_type
resource
risk_class
status
expires_at?
created_at
```

### ExternalResource

Normalized pointer to a resource owned by another system.

Examples:

- repository;
- branch;
- commit;
- PR;
- GitHub workflow run;
- deployment;
- object-storage artifact;
- external agent session.

Core fields:

```text
id
resource_type
provider
external_id
uri?
metadata
created_at
```

### AuditEvent

Append-oriented record of important state transitions and privileged operations.

Core fields:

```text
id
event_type
actor_type
actor_id?
work_request_id?
task_id?
correlation_id?
payload
created_at
```

Phase 0 event types should include at least:

```text
WORK_REQUEST_CREATED
PLAN_CREATED
PLAN_ACTIVATED
TASK_CREATED
TASK_STATUS_CHANGED
AGENT_RUN_CREATED
AGENT_RUN_STATUS_CHANGED
DECISION_REQUIRED
DECISION_RECORDED
APPROVAL_REQUIRED
APPROVAL_RECORDED
WORK_REQUEST_COMPLETED
```

## Domain Invariants

The first implementation should enforce these rules in application/domain services rather than relying only on UI behavior.

1. A Task belongs to exactly one WorkRequest.
2. An active Task must reference a Plan belonging to the same WorkRequest.
3. A completed WorkRequest cannot contain non-terminal required Tasks.
4. A Task cannot become `RUNNING` while a blocking dependency is incomplete.
5. A Task cannot become `COMPLETED` directly from `PENDING` without an explicitly allowed transition.
6. A DecisionRequest in `PENDING` state can place the relevant WorkRequest/Task into `WAITING_FOR_OWNER`.
7. Recording a DecisionResponse does not automatically authorize destructive actions; approval policy remains separate.
8. External agent-session deletion must not delete the Task or WorkRequest.
9. Audit events for important transitions are append-only through normal application code.
10. Every mutable domain record carries timestamps and safe concurrency/version semantics where needed.

## State-Transition Services

Do not let API routes update status fields arbitrarily.

Create explicit application/domain services such as:

```text
create_work_request()
create_plan()
activate_plan()
create_task()
mark_task_ready()
start_task()
block_task()
request_owner_decision()
record_owner_decision()
start_agent_run()
complete_agent_run()
start_validation()
complete_task()
fail_task()
complete_work_request()
```

These services should validate allowed state transitions and emit audit events.

## Persistence Architecture

Use repository interfaces in the domain/application layer and SQLAlchemy implementations in the persistence layer.

Initial repository contracts:

```text
ConversationRepository
MessageRepository
WorkRequestRepository
PlanRepository
TaskRepository
AgentRunRepository
DecisionRepository
ApprovalRepository
ExternalResourceRepository
AuditEventRepository
```

Use a unit-of-work boundary so one domain transition and its audit event commit atomically.

Example:

```text
begin transaction
  change Task -> RUNNING
  create AgentRun
  append TASK_STATUS_CHANGED
  append AGENT_RUN_CREATED
commit
```

Do not publish external side effects from inside an uncommitted database transaction.

## Database Migration Rules

1. All schema changes use Alembic migrations.
2. CI must prove migrations apply to an empty database.
3. CI should prove migration head matches ORM metadata expectations.
4. No manual production schema edits.
5. Destructive migration patterns require explicit review in later phases.
6. Seed/example data must not be embedded into production migrations unless genuinely required.

## Configuration Model

Use a single typed Settings model loaded from environment variables/local `.env` during development.

Initial settings groups:

```text
APP_*
DATABASE_*
DBOS_*
LOG_*
MODEL_*
GITHUB_*        # placeholders only in Phase 0
SECRET_STORE_*  # placeholders only in Phase 0
```

`.env.example` contains names and safe example values only.

Never commit credentials.

Phase 0 should include a `LocalSecretStore`/environment-backed adapter behind the production `SecretStore` interface.

## Core Interfaces to Freeze in Phase 0

The word "freeze" here means establish tested semantics before external integrations; minor refinement remains possible.

### LLM service

Conceptual interface:

```text
complete(request: ModelRequest) -> ModelResponse
stream(request: ModelRequest) -> event stream
```

Normalized `ModelRequest` should carry:

- capability profile;
- messages/context;
- tool definitions;
- structured-output requirement;
- budget/token hints;
- correlation/task identifiers.

Normalized `ModelResponse` should carry:

- canonical assistant content;
- structured result if requested;
- tool requests;
- provider/model identifiers;
- token/cache/cost usage where known;
- finish/error classification.

Phase 0 implementation: **fake deterministic adapter only**.

Do not call paid LLM APIs during Phase 0 tests.

### Developer Agent

Conceptual interface:

```text
create_task(task_spec) -> runtime_handle
send_instruction(runtime_handle, instruction)
stream_events(runtime_handle, cursor?)
get_status(runtime_handle)
request_summary(runtime_handle)
cancel(runtime_handle)
resume(runtime_handle)
get_usage(runtime_handle)
finalize(runtime_handle)
```

Phase 0 implementation: fake in-memory/deterministic Developer Agent adapter used for contract tests.

### Tool service

Conceptual request:

```text
ToolInvocation
  tool_name
  operation
  arguments
  actor/task context
  idempotency_key
```

Conceptual result:

```text
ToolResult
  status
  normalized output
  external resource refs
  usage/cost metadata
  retry classification
```

Phase 0 uses fake tools only.

### Policy engine

Initial conceptual decisions:

```text
ALLOW
DENY
REQUIRE_OWNER_DECISION
REQUIRE_OWNER_APPROVAL
```

Inputs should include:

- actor/role;
- requested action;
- target resource;
- task/work-request context;
- risk category;
- estimated cost/blast radius where available.

Phase 0 policy may be simple rule-based Python.

Do not use an LLM as the security policy engine.

### Secret store

Conceptual interface:

```text
get_secret(name)
put_secret(name, value)      # may be unsupported by some runtime adapters
remove_secret(name)
```

Phase 0 uses an environment/local fake adapter only.

### Event publisher

Domain code should emit normalized application events through an interface independent of future Web Push, WebSocket, email, or queue products.

Phase 0 implementation writes persisted AuditEvents and may expose an in-process test subscriber.

## Manager Agent Boundary in Phase 0

Phase 0 does **not** implement the real Pydantic AI Manager.

Instead, define the Manager application contract and a deterministic fake implementation.

Conceptual input:

```text
ManagerTurnContext
  conversation
  work request
  active plan
  tasks
  pending decisions
  recent messages
  retrieved context
```

Conceptual output:

```text
ManagerTurnResult
  owner_message?
  proposed_plan?
  proposed_tasks[]
  developer_instructions[]
  decision_request?
  proposed_tool_calls[]
  workflow_directive
```

This lets Phase 1 connect Pydantic AI without changing the surrounding workflow/domain model.

## DBOS Integration Plan

DBOS should be introduced after basic domain/persistence tests are green.

Phase 0 durable workflow scenario:

```text
1. Create WorkRequest.
2. Start Manager workflow.
3. Fake Manager creates Plan + Task.
4. Task reaches a rule requiring owner input.
5. Persist DecisionRequest.
6. Workflow pauses durably.
7. Stop application process.
8. Restart application.
9. Record DecisionResponse.
10. Resume exact workflow.
11. Fake Developer Agent completes Task.
12. WorkRequest completes.
```

Acceptance requires database evidence that no duplicate Task/Decision/AgentRun is created during restart/retry.

## Idempotency Rules

Idempotency must be designed before real GitHub/cloud tools are added.

Phase 0 should define and test:

- client-generated request IDs for owner messages/work requests;
- tool-call idempotency keys;
- external-action correlation IDs;
- duplicate-event handling;
- workflow retry behavior;
- safe re-processing after process crash.

A repeated request with the same idempotency key must return/reuse the original logical operation rather than silently creating duplicates.

## API Scope for Phase 0

The API is developer-facing only and can be intentionally small.

Suggested endpoints:

```text
GET  /health
GET  /ready

POST /api/v1/conversations
POST /api/v1/conversations/{id}/messages
GET  /api/v1/conversations/{id}

POST /api/v1/work-requests
GET  /api/v1/work-requests/{id}

GET  /api/v1/work-requests/{id}/plans
GET  /api/v1/work-requests/{id}/tasks

GET  /api/v1/tasks/{id}
GET  /api/v1/tasks/{id}/events

GET  /api/v1/decisions/{id}
POST /api/v1/decisions/{id}/responses
```

No public deployment or production authentication is required yet.

API error responses should use one consistent structured schema.

## Observability

Phase 0 should establish structured logging before agent/tool integrations.

Every request/workflow/event log should include relevant IDs where available:

```text
request_id
conversation_id
work_request_id
task_id
agent_run_id
correlation_id
```

Do not log:

- secrets;
- environment-variable values;
- authorization headers;
- raw future provider credentials;
- raw audio.

Initial logs may be JSON to stdout.

Metrics infrastructure can remain lightweight, but code should expose/collect at least:

- workflow counts/status;
- task counts/status;
- decision wait duration;
- errors;
- later cost counters.

## Security Boundaries in Phase 0

Even before real credentials exist, implement the boundaries that later protect them.

### Required rules

- application code retrieves secrets only through the `SecretStore` interface;
- domain models never contain secret values;
- API responses never expose secret values;
- `.env` ignored by Git;
- `.env.example` contains no working credential;
- external adapters receive only the credential they require;
- fake Developer Agent has no direct persistence/database object access;
- future worker APIs will be separate from owner APIs;
- policy authorization is explicit before external tool execution.

### Not yet required

- AWS Secrets Manager configuration;
- GitHub App key;
- WebAuthn;
- TLS termination;
- private VPC;
- remote worker bootstrap credentials.

Those begin in later phases after the local boundaries exist.

## Budget Architecture in Phase 0

The `$50/month` ceiling must be represented as application configuration/policy, but Phase 0 should not impose arbitrary message quotas.

Create normalized usage concepts now:

```text
UsageRecord
  category
  provider
  model_or_resource
  input_units
  output_units
  cached_units
  quantity
  estimated_cost_usd
  actual_cost_usd?
  task_id?
  timestamp
```

Initial categories:

```text
LLM
DEVELOPER_COMPUTE
SPEECH_TO_TEXT
TEXT_TO_SPEECH
TOOL
STORAGE
OTHER
```

Phase 0 tests should prove that budget policy can:

- accumulate cost records;
- calculate month-to-date total;
- expose remaining budget;
- reject a simulated operation that would exceed a configured hard ceiling;
- allow unlimited zero-cost fake operations.

This establishes the desired behavior: **usage itself is not limited; spend is limited.**

## Existing Task Fixtures

Preserve existing `tasks/` and `templates/tasks/` content.

During Phase 0, add tests that parse at least one existing task Markdown file into a temporary import structure or fixture representation.

Do not make Markdown files the canonical production task store.

Later migration can map useful historical fields into Postgres while retaining the files as fixtures/history.

## Local Development Stack

Minimum local stack:

```text
Python 3.13 application
PostgreSQL container
```

`docker-compose.yml` should run Postgres only unless another dependency becomes necessary.

The application itself should normally run directly through the local Python environment for fast development/debugging.

Recommended developer commands:

```text
uv sync
uv run alembic upgrade head
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run uvicorn overlord.api.app:app --reload
```

Provide friendly Makefile/task-runner shortcuts only if they materially improve usability; do not hide the canonical underlying commands.

## CI Workflow

Create `.github/workflows/ci.yml`.

On PRs and pushes to `main`, CI should:

1. install the pinned Python version;
2. install dependencies from lockfile;
3. run Ruff lint;
4. run formatting check;
5. run mypy;
6. start Postgres service;
7. apply all Alembic migrations to a clean database;
8. run unit tests;
9. run integration tests;
10. run contract tests;
11. report test coverage.

No paid service credentials should be required for CI.

Do not add automatic production deployment in Phase 0.

## Test Strategy

### Unit tests

Cover:

- state-transition rules;
- policy decisions;
- budget calculations;
- model/developer/tool normalized schemas;
- task dependency behavior;
- decision/approval semantics;
- idempotency logic.

### Persistence integration tests

Use real Postgres for:

- repository CRUD/queries;
- transaction rollback;
- unique/idempotency constraints;
- migration correctness;
- event + state atomicity;
- status/history queries.

### API integration tests

Cover:

- conversation/message creation;
- work-request lifecycle;
- task listing;
- decision response;
- error schema;
- idempotent request behavior.

### Contract tests

Every adapter interface should have reusable contract tests.

Examples:

```text
DeveloperAgentContractTests
LLMServiceContractTests
SecretStoreContractTests
ToolServiceContractTests
```

The fake adapters must pass them first. Later OpenHands/OpenCode/provider adapters must pass the same tests.

### Workflow recovery test

Must include a real process/restart or equivalent durable-recovery test demonstrating the DBOS pause/resume scenario.

## Documentation Inside `Overlord`

Phase 0 should add concise repository-local documentation:

```text
README.md
  project purpose
  local quick start
  architecture summary
  test commands

docs/architecture/domain-model.md
docs/architecture/interfaces.md
docs/architecture/state-and-events.md
docs/development/local-setup.md
docs/development/testing.md
docs/decisions/
```

Architecture Decision Records should be used only for material decisions likely to matter later.

Initial ADR candidates:

```text
0001-python-313.md
0002-postgres-canonical-state.md
0003-provider-neutral-agent-contracts.md
0004-dbos-durable-workflows.md
```

Do not create ADRs for trivial formatting/package choices.

## Phase 0 Implementation Sequence

### P0.1 — Project scaffold

Create:

- `pyproject.toml`;
- lockfile;
- package skeleton;
- `.gitignore`;
- `.env.example`;
- basic settings/logging;
- FastAPI health endpoint;
- Postgres Docker Compose;
- initial CI.

Gate:

- clean install works;
- `/health` works;
- CI lint/type/test scaffold passes.

### P0.2 — Domain model and transition rules

Implement:

- enums/IDs/errors;
- WorkRequest;
- Plan;
- Task;
- TaskDependency;
- AgentRun;
- DecisionRequest/Response;
- ApprovalRequest;
- ExternalResource;
- AuditEvent;
- UsageRecord;
- domain transition services.

Gate:

- unit tests cover legal/illegal transitions;
- no persistence/framework imports in domain layer.

### P0.3 — Postgres persistence

Implement:

- SQLAlchemy mappings;
- repositories;
- unit of work;
- Alembic migrations;
- integration tests.

Gate:

- fresh database migration succeeds;
- domain lifecycle persists and reloads;
- transaction + event atomicity proven.

### P0.4 — API lifecycle

Implement development APIs for:

- conversations/messages;
- work requests;
- plans/tasks retrieval;
- decision responses;
- event timeline.

Gate:

- complete fake lifecycle can be driven through API calls;
- duplicate client request is idempotent.

### P0.5 — Adapter contracts and fake implementations

Implement normalized interfaces plus deterministic fake adapters for:

- LLM service;
- Manager;
- Developer Agent;
- tools;
- secret store;
- event publisher.

Gate:

- reusable adapter contract tests exist and pass;
- no paid/external service required.

### P0.6 — DBOS durable lifecycle

Implement Manager/task orchestration with the fake adapters.

Gate:

- pause on owner decision;
- stop/restart;
- resume exact workflow;
- no duplicate tasks/agent runs/decisions;
- final WorkRequest completes.

### P0.7 — Budget/policy enforcement

Implement:

- `$50` configurable hard monthly ceiling;
- usage aggregation;
- simulated action estimate;
- policy allow/deny/decision/approval outcomes.

Gate:

- zero-cost operations remain unrestricted;
- simulated over-budget spend is blocked/escalated;
- domain history records the reason.

### P0.8 — Documentation and Phase 0 closeout

Update:

- README;
- local setup;
- domain/interface docs;
- ADRs;
- exact acceptance evidence.

Gate:

- fresh-clone setup documented and tested;
- CI green;
- Phase 0 acceptance checklist completed.

## Phase 0 Acceptance Criteria

Phase 0 is complete only when all criteria below are true.

### Repository

- application package exists under `src/overlord`;
- dependency versions are reproducible;
- current legacy task/template files remain preserved;
- no working secrets committed.

### Domain independence

- complete request/plan/task/decision lifecycle exists in Overlord domain state;
- deleting/replacing a fake agent runtime reference does not delete domain state;
- vendor/framework classes do not appear in core domain model signatures.

### Persistence

- clean Postgres database can be created solely through migrations;
- state survives application restart;
- event/state transitions commit atomically;
- important history is queryable without an agent/provider API.

### Durable workflow

- workflow pauses waiting for owner input;
- application can restart;
- owner decision resumes correct workflow;
- no duplicate side-effect records occur during retry/recovery.

### Adapter portability

- fake LLM passes LLM contract tests;
- fake Developer Agent passes Developer contract tests;
- fake SecretStore passes SecretStore tests;
- fake tools pass Tool contract tests;
- adapter-specific IDs are stored as external references only.

### Policy/security

- sensitive operation paths require policy evaluation;
- secrets only enter application through SecretStore abstraction;
- secret values are absent from domain state and logs;
- budget policy is deterministic application logic, not model judgment.

### Cost model

- `$50` monthly spending ceiling is configurable;
- unlimited zero-cost local/fake actions are permitted;
- usage records aggregate correctly;
- simulated spend crossing the ceiling produces a deterministic block/escalation.

### Quality

- Ruff clean;
- formatting check clean;
- mypy clean for project code at the agreed strictness;
- pytest green;
- migrations tested;
- CI green;
- local setup documentation works from a clean clone.

## Explicitly Out of Scope for Phase 0

Do **not** add these during Phase 0 unless needed to resolve a blocker in the approved contract:

- real OpenAI/Anthropic/Google API calls;
- Pydantic AI Manager implementation;
- OpenHands;
- OpenCode;
- GitHub App creation/credentials;
- live GitHub mutation tools;
- DigitalOcean/Fly/Hetzner worker provisioning;
- AWS Secrets Manager configuration;
- S3 backup jobs;
- passkey authentication;
- PWA frontend;
- Web Push;
- speech services;
- MCP servers;
- ACP/A2A networking;
- pgvector;
- LiteLLM;
- Temporal;
- OpenBao;
- production hosting/deployment.

Keeping these out is deliberate: Phase 0 exists to make all of them replaceable integrations rather than foundational dependencies.

## Pull Request Strategy

Do not implement Phase 0 as one giant PR.

Recommended sequence:

1. `phase0/project-scaffold`
2. `phase0/domain-model`
3. `phase0/postgres-persistence`
4. `phase0/api-lifecycle`
5. `phase0/adapter-contracts`
6. `phase0/durable-workflow`
7. `phase0/policy-budget`
8. `phase0/closeout`

Each PR should:

- have focused scope;
- include tests for its behavior;
- update repository-local docs when the public/internal contract changes;
- keep `main` runnable;
- pass CI before merge.

The documentation website should be updated at meaningful architectural milestones rather than for every small code commit.

## Phase 1 Entry Gate

Do not begin the real Manager Agent or paid-provider integration until Phase 0 closeout proves:

```text
Overlord owns the state.
Overlord owns the workflow.
Overlord owns the policy boundary.
Overlord owns the adapter contracts.
External agents/models can disappear without destroying the task history.
```

Once that is proven, Phase 1 can safely introduce Pydantic AI and the first real model provider behind the existing contract.

## Decisions Deferred Until Later Evidence

Phase 0 must not force these choices:

- final LLM provider/model;
- OpenHands versus OpenCode default;
- DigitalOcean versus Fly/Hetzner host;
- STT/TTS provider;
- LiteLLM gateway requirement;
- pgvector requirement;
- native versus wrapped mobile client;
- OpenBao versus managed secrets long term;
- Temporal/Kubernetes requirement.

## Immediate Next Action After Approval

Begin **P0.1 — Project Scaffold** in the `Overlord` repository using a focused branch/PR.

The first code PR should contain infrastructure-free application scaffolding only:

- Python project metadata;
- lockfile;
- package skeleton;
- settings/logging;
- `/health` endpoint;
- local Postgres Compose definition;
- basic test/lint/type setup;
- CI workflow;
- local setup documentation.

No paid provider credentials or recurring cloud resources should be needed.

## Related Documents

- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)
- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)
- [Research 03 — Mobile, Notifications, Authentication, and Voice](/projects/notes/high-director-successor-research-03/)
- [Research 04 — LLM Provider Strategy and Cost](/projects/notes/high-director-successor-research-04/)
- [Research 05 — Persistent State, Memory, Backups, and Security](/projects/notes/high-director-successor-research-05/)
- [Research 06 — Build vs Adopt and Interoperability Boundaries](/projects/notes/high-director-successor-research-06/)

## Verification Record

- Last verified: `2026-08-10`
- Verified against: the approved consolidated successor architecture; current `Overlord` repository tree/README/task fixtures/templates; current official Python/Pydantic AI/DBOS compatibility information used to select the implementation baseline.
- Verified by: High Director
- Verification scope: Phase 0 scope, repository structure, language/runtime baseline, domain ownership, adapter boundaries, persistence/workflow approach, testing/CI, security/cost boundaries, implementation sequence, and acceptance criteria.
- Unverified areas: real adapter behavior, external-provider SDK integration, worker isolation, cloud hosting, mobile behavior, and actual model cost; intentionally deferred to later prototype phases.
