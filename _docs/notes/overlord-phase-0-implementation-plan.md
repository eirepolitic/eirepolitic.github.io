---
title: Overlord — Phase 0 Implementation Plan
summary: Detailed pre-development implementation contract for establishing the Overlord repository, domain model, interfaces, local control-plane spine, tests, security boundaries, and Phase 0 acceptance gates.
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
  - high-director-successor
  - implementation-plan
  - phase-0
  - architecture
  - python
  - postgres
  - dbos
---

# Overlord — Phase 0 Implementation Plan

## Purpose

This document converts the approved High Director successor architecture into the concrete implementation contract for **Phase 0** of the `Overlord` repository.

Phase 0 is intentionally narrow. It establishes the repository foundation, domain model, provider/runtime-neutral interfaces, local development environment, tests, and architectural guardrails that later phases will build on.

Phase 0 does **not** provision recurring cloud infrastructure, create remote Developer Agent workers, enable broad production credentials, or build the phone/PWA interface.

The goal is to make the expensive architectural decisions explicit before application code begins to accumulate around accidental framework choices.

## Approved Inputs

The Phase 0 plan is based on the following owner-approved decisions:

- successor repository: `Overlord`;
- monthly prototype spending ceiling: **USD $50 total**;
- the ceiling is a spending guardrail, **not an intended usage quota**;
- product design should make ordinary use feel effectively unrestricted by minimizing marginal cost through model routing, caching, compact context, mocked/local testing, and ephemeral compute;
- MVP integration scope begins with GitHub development workflows;
- broader AWS, Google Workspace, Appsmith, Power BI, and Power Automate capabilities remain future extension points;
- GitHub Actions Secrets are intended for CI/CD secrets;
- runtime long-lived secrets will use a replaceable `SecretStore` interface, with AWS Secrets Manager as the current recommended hosted implementation when remote runtime deployment begins;
- PWA/mobile, remote workers, voice, notifications, and production deployment are later phases.

## Existing `Overlord` Repository State

The repository is effectively a clean application slate.

Existing material consists of:

- a small README;
- test-task Markdown files;
- task-template Markdown files.

Those files should be retained during Phase 0. They are useful historical fixtures and may later become seed inputs for task-schema compatibility tests.

No current application architecture needs to be preserved.

## Phase 0 Objectives

Phase 0 should establish these foundations:

1. a production-shaped Python package structure;
2. a clear domain model independent of Pydantic AI, DBOS, OpenHands, OpenCode, or any single database ORM;
3. PostgreSQL-backed persistence with migrations;
4. durable workflow interfaces and one minimal DBOS-backed workflow proof;
5. provider-neutral model capability profiles;
6. runtime-neutral Developer Agent contracts;
7. tool/policy/approval contracts;
8. provider-neutral secret, notification, speech, and artifact interfaces even though most implementations are deferred;
9. a deterministic event/audit model;
10. local Docker-based development;
11. automated unit/integration tests;
12. lint/type/test CI;
13. architecture tests that prevent framework leakage into the domain layer;
14. local cost/budget policy primitives;
15. documentation sufficient for another developer/agent to work in the repository safely.

## Non-Goals

Do **not** implement these in Phase 0:

- production cloud deployment;
- DigitalOcean/Fly/Hetzner worker provisioning;
- AWS Secrets Manager integration beyond an interface/stub if useful;
- GitHub App installation or broad write permissions;
- OpenHands integration;
- OpenCode integration;
- real Developer Agent execution;
- PWA/mobile UI;
- passkeys;
- Web Push;
- STT/TTS;
- MCP servers;
- ACP/A2A integration;
- vector search;
- pgvector;
- Temporal;
- Kubernetes;
- realtime voice;
- autonomous repository modification.

Those are later phases and should not expand Phase 0 scope.

## Technology Baseline

### Language

**Python 3.13**.

Rationale:

- modern async/runtime support;
- broad compatibility with the selected Python ecosystem;
- conservative relative to adopting the newest interpreter immediately;
- easy later migration once dependency compatibility is proven.

The repository should declare the supported Python range explicitly rather than silently depending on one developer machine.

Initial target:

```text
>=3.13,<3.14
```

Re-evaluate Python 3.14 after the core dependency set is exercised in CI.

### API framework

**FastAPI**.

Use it only at the HTTP boundary. Domain and application services must not import FastAPI objects.

### Domain validation / schemas

**Pydantic v2** for external/application boundary schemas where useful.

Domain entities should remain plain Python dataclasses/enums/value objects where this keeps framework coupling lower. Pydantic models should not automatically become the canonical domain model.

### Manager-agent library

**Pydantic AI**, behind Overlord-owned interfaces.

Phase 0 should define the adapter boundary and one minimal structured-output proof, not build the full Manager Agent.

### Durable workflow engine

**DBOS**, behind Overlord-owned workflow/application services.

Phase 0 should prove durable execution/restart semantics locally.

### Database

**PostgreSQL**.

Use PostgreSQL from the beginning rather than SQLite for application integration tests because DBOS durability and later production behavior depend on Postgres semantics.

### ORM / SQL layer

**SQLAlchemy 2.x** with **Alembic** migrations.

Important rule: SQLAlchemy ORM models live in the persistence layer and map to/from domain objects. Domain code must not import SQLAlchemy.

### PostgreSQL driver

Use a modern supported PostgreSQL driver consistently across SQLAlchemy/DBOS needs. Prefer one driver family rather than mixing multiple clients unless a framework requires it.

The exact sync/async driver choice should be verified during the first implementation PR against DBOS and SQLAlchemy integration behavior.

### Testing

- `pytest`;
- `pytest-asyncio` where asynchronous integration tests require it;
- containerized PostgreSQL integration tests;
- mocks/fakes for LLMs, secrets, tools, Developer Agents, notifications, and external services.

### Quality tooling

Initial recommendation:

- **Ruff** for linting/formatting;
- **mypy** for static typing;
- **pytest** for tests.

Keep the initial toolchain small. Do not add overlapping linters/formatters without evidence they catch additional meaningful problems.

### Packaging/dependency management

Use standard `pyproject.toml` packaging.

Prefer a lockfile-capable workflow. The exact package installer (`uv` or another standards-compatible tool) may be selected during the first repository bootstrap PR, provided:

- CI is deterministic;
- dependencies are locked;
- local setup remains simple;
- no proprietary package manager becomes required.

Current recommendation: **`uv`** for fast local/CI environment management, while retaining standards-compatible `pyproject.toml` metadata.

## Proposed Repository Structure

```text
Overlord/
├── .github/
│   └── workflows/
│       └── ci.yml
├── docs/
│   ├── architecture.md
│   ├── development.md
│   ├── domain-model.md
│   ├── security-boundaries.md
│   └── decisions/
├── migrations/
│   ├── versions/
│   └── env.py
├── src/
│   └── overlord/
│       ├── __init__.py
│       ├── api/
│       │   ├── app.py
│       │   ├── dependencies.py
│       │   └── routes/
│       ├── application/
│       │   ├── services/
│       │   ├── commands/
│       │   └── queries/
│       ├── domain/
│       │   ├── entities/
│       │   ├── enums.py
│       │   ├── events.py
│       │   ├── policies.py
│       │   └── value_objects.py
│       ├── ports/
│       │   ├── agent.py
│       │   ├── developer.py
│       │   ├── llm.py
│       │   ├── repositories.py
│       │   ├── tools.py
│       │   ├── secrets.py
│       │   ├── artifacts.py
│       │   ├── notifications.py
│       │   ├── speech.py
│       │   └── clock.py
│       ├── adapters/
│       │   ├── llm/
│       │   │   └── pydantic_ai.py
│       │   ├── developer/
│       │   ├── github/
│       │   ├── secrets/
│       │   ├── artifacts/
│       │   ├── notifications/
│       │   └── speech/
│       ├── persistence/
│       │   ├── db.py
│       │   ├── models/
│       │   ├── mappings/
│       │   └── repositories/
│       ├── workflows/
│       │   ├── dbos_runtime.py
│       │   └── manager_workflow.py
│       ├── policy/
│       │   ├── approvals.py
│       │   ├── budgets.py
│       │   └── permissions.py
│       ├── config/
│       │   ├── settings.py
│       │   └── model_profiles.py
│       └── observability/
│           ├── logging.py
│           └── metrics.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── architecture/
│   ├── fixtures/
│   └── conftest.py
├── tasks/                 # existing fixtures retained
├── templates/             # existing templates retained
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── pyproject.toml
├── README.md
└── uv.lock                # if uv selected
```

## Layering Rules

The key dependency direction should be:

```text
API / adapters / persistence / workflows
                  |
                  v
             application
                  |
                  v
                domain
```

`domain` must not depend on:

- FastAPI;
- SQLAlchemy;
- DBOS;
- Pydantic AI;
- OpenHands;
- OpenCode;
- provider SDKs;
- GitHub SDK/API clients;
- AWS SDKs.

`ports` define interfaces required by application/domain services.

`adapters` implement those ports using external libraries/services.

This is the principal mechanism that keeps the successor replaceable over time.

## Domain Model v1

Phase 0 should implement the minimum durable concepts needed for the Manager/Developer workflow.

### `Conversation`

Represents the durable owner/Manager conversation.

Minimum fields:

```text
id
kind
status
created_at
updated_at
```

### `Message`

Provider-neutral canonical message/event content.

Minimum fields:

```text
id
conversation_id
author_type
content_type
content
created_at
source_mode
provider_metadata_ref? 
```

The canonical text/content must remain usable without provider-native message objects.

### `WorkRequest`

Represents what the owner is asking Overlord to accomplish.

Minimum fields:

```text
id
conversation_id
title
objective
status
created_at
updated_at
```

### `Plan`

A versioned implementation plan associated with a Work Request.

Minimum fields:

```text
id
work_request_id
version
status
summary
created_at
supersedes_plan_id?
```

Plans are immutable versions after publication; revisions create a new version.

### `Task`

The durable unit delegated to a Developer Agent or internal workflow.

Minimum fields:

```text
id
work_request_id
plan_id
parent_task_id?
title
objective
status
priority
repository_ref?
created_at
updated_at
```

### `TaskDependency`

Explicit dependency edges between tasks.

Minimum fields:

```text
upstream_task_id
downstream_task_id
dependency_type
```

### `AgentRun`

Represents one execution attempt using a Manager or Developer runtime.

Minimum fields:

```text
id
task_id?
conversation_id?
agent_role
runtime_type
runtime_session_id?
model_profile_id?
status
started_at
ended_at?
```

A runtime session ID is adapter metadata, not the canonical task identity.

### `DecisionRequest`

Represents a question that genuinely requires owner input.

Minimum fields:

```text
id
work_request_id
task_id?
category
question
context_summary
recommended_option?
status
created_at
resolved_at?
```

### `DecisionOption`

Structured choices when applicable.

Minimum fields:

```text
id
decision_request_id
key
label
description
cost_impact?
risk_level?
```

### `Decision`

Canonical record of the owner's answer.

Minimum fields:

```text
id
decision_request_id
selected_option_key?
freeform_response?
created_at
```

### `ApprovalRequest`

Separate from a product decision. Represents permission to execute a restricted action.

Examples:

- destructive operation;
- security/access change;
- spending increase;
- privileged merge/deployment action.

Minimum fields:

```text
id
task_id?
policy_rule
requested_action
resource_scope
status
created_at
expires_at?
```

### `ToolCall`

Canonical proposed/executed tool invocation.

Minimum fields:

```text
id
agent_run_id
idempotency_key
tool_name
action
resource_scope
request_payload
status
created_at
completed_at?
```

### `ToolResult`

Minimum fields:

```text
id
tool_call_id
success
summary
artifact_ref?
structured_result?
created_at
```

### `DomainEvent`

Append-oriented state transition/event record.

Minimum fields:

```text
id
event_type
aggregate_type
aggregate_id
actor_type
actor_id?
correlation_id
causation_id?
payload
created_at
```

### `UsageRecord`

Normalizes model/compute usage.

Minimum fields:

```text
id
work_request_id?
task_id?
agent_run_id?
provider
model_or_resource
usage_type
quantity
unit
cost_usd
price_profile_id?
created_at
```

### `BudgetPolicy`

Initial prototype budget configuration.

Minimum fields:

```text
id
scope_type
scope_id?
period
soft_limit_usd?
hard_limit_usd
status
```

The global prototype policy begins at **$50/month**.

The budget layer should optimize use rather than block ordinary interaction prematurely. Low-cost Manager chat/summarization should continue whenever possible even as the system approaches the ceiling; expensive execution should be the first thing constrained.

## Required State Machines

Statuses should be explicit enums with validated transitions rather than arbitrary strings.

### Work Request

```text
DRAFT
PLANNING
READY
IN_PROGRESS
AWAITING_OWNER
VALIDATING
COMPLETED
CANCELLED
FAILED
```

### Task

```text
PENDING
BLOCKED
READY
RUNNING
AWAITING_OWNER
VALIDATING
SUCCEEDED
FAILED
CANCELLED
```

### Agent Run

```text
CREATED
STARTING
RUNNING
PAUSED
SUCCEEDED
FAILED
CANCELLED
```

### Decision Request

```text
OPEN
ANSWERED
CANCELLED
SUPERSEDED
```

### Approval Request

```text
PENDING
APPROVED
DENIED
EXPIRED
CANCELLED
```

Transitions must be centrally validated and covered by unit tests.

## Core Port / Interface Contracts

Phase 0 should define these as Python `Protocol`/ABC-style interfaces with fake implementations used in tests.

## `ModelGateway`

Purpose: provider-neutral Manager/subtask model access.

Conceptual methods:

```python
async def generate(request: ModelRequest) -> ModelResponse
async def stream(request: ModelRequest) -> AsyncIterator[ModelEvent]
```

`ModelRequest` should include:

- capability profile, not only provider/model name;
- messages/context;
- structured-output schema descriptor;
- tool descriptors;
- token/cost limits;
- cache hints;
- correlation/task IDs.

`ModelResponse` should normalize:

- canonical output;
- structured result;
- tool requests;
- provider/model identity;
- token/cache usage;
- estimated/actual cost;
- finish/error classification.

## `DeveloperAgent`

Purpose: interchangeable OpenHands/OpenCode/future coding runtime.

Conceptual methods:

```python
async def create_task(spec: DeveloperTaskSpec) -> DeveloperSession
async def send_instruction(session_id: str, message: str) -> None
async def events(session_id: str, cursor: str | None = None) -> AsyncIterator[DeveloperEvent]
async def status(session_id: str) -> DeveloperStatus
async def summarize(session_id: str) -> DeveloperSummary
async def cancel(session_id: str) -> None
async def resume(session_id: str) -> None
async def usage(session_id: str) -> DeveloperUsage
async def finalize(session_id: str) -> DeveloperResult
```

No OpenHands/OpenCode types should appear in the interface.

## `ToolExecutor`

Purpose: privileged external action boundary.

Conceptual flow:

```text
agent proposes ToolRequest
        |
        v
policy evaluates request
        |
        +--> denied
        +--> owner approval required
        +--> permitted
                 |
                 v
             executor
                 |
                 v
           ToolResult + audit
```

The tool interface must carry:

- actor/task context;
- idempotency key;
- resource scope;
- risk/action category;
- timeout/retry policy.

## `PolicyEngine`

Conceptual result:

```text
ALLOW
DENY
REQUIRE_OWNER_DECISION
REQUIRE_APPROVAL
REQUIRE_BUDGET_APPROVAL
```

The policy engine should be deterministic application code/configuration. The LLM may supply context or recommendations but cannot override policy results.

## `SecretStore`

Conceptual methods:

```python
async def get_secret(ref: SecretRef) -> SecretValue
async def get_metadata(ref: SecretRef) -> SecretMetadata
```

Do not expose a generic “list every secret value” method.

Implementations later may include:

- environment/local development;
- AWS Secrets Manager;
- SOPS/bootstrap;
- OpenBao.

## `ArtifactStore`

Provider-neutral binary/large-object store.

Conceptual methods:

```python
async def put(...)
async def get(...)
async def delete(...)
async def metadata(...)
```

Local-filesystem fake/implementation is sufficient in Phase 0.

## `NotificationService`

Define the interface and severity model only.

```text
INFO
MILESTONE
OWNER_INPUT_REQUIRED
SECURITY_COST_ALERT
TASK_COMPLETE
```

No Web Push implementation is required yet.

## `SpeechToText` / `TextToSpeech`

Define interfaces only to prevent future phone code from depending on one speech vendor.

No Phase 0 speech calls are required.

## Repository Interfaces

Define persistence ports around domain concepts rather than passing SQLAlchemy sessions throughout the application.

Examples:

```text
ConversationRepository
WorkRequestRepository
PlanRepository
TaskRepository
DecisionRepository
ApprovalRepository
EventRepository
UsageRepository
BudgetRepository
```

Application services should operate through these interfaces.

## Event Taxonomy v1

At minimum define stable event names for:

```text
CONVERSATION_CREATED
MESSAGE_RECORDED
WORK_REQUEST_CREATED
WORK_REQUEST_STATUS_CHANGED
PLAN_CREATED
PLAN_SUPERSEDED
TASK_CREATED
TASK_DEPENDENCY_ADDED
TASK_STATUS_CHANGED
AGENT_RUN_CREATED
AGENT_RUN_STATUS_CHANGED
TOOL_CALL_REQUESTED
TOOL_CALL_AUTHORIZED
TOOL_CALL_DENIED
TOOL_CALL_COMPLETED
OWNER_DECISION_REQUIRED
OWNER_DECISION_RECORDED
APPROVAL_REQUESTED
APPROVAL_GRANTED
APPROVAL_DENIED
BUDGET_WARNING
BUDGET_BLOCKED
WORK_REQUEST_COMPLETED
```

Event payloads must be versionable. Include an event schema version from the start.

## Configuration Model

All configuration should be centralized through typed settings.

Categories:

```text
app
api
database
dbos
logging
model_profiles
budget
security
feature_flags
external_adapters
```

### `.env.example`

Must contain names and explanatory placeholders only—never usable credentials.

Example categories:

```text
OVERLORD_ENV
OVERLORD_DATABASE_URL
OVERLORD_LOG_LEVEL
OVERLORD_MONTHLY_BUDGET_USD=50
OVERLORD_MODEL_PROFILE_MANAGER=balanced
OVERLORD_MODEL_PROFILE_EFFICIENT=efficient
```

Provider-specific credentials should remain optional in Phase 0 because tests should use fake model adapters by default.

## Model Capability Configuration

Do not encode provider names directly into Manager logic.

Conceptual configuration:

```yaml
profiles:
  efficient:
    purpose: low-cost routine transformations
    provider_model: test/fake-efficient
    max_cost_per_call_usd: 0.05

  balanced:
    purpose: normal manager reasoning
    provider_model: test/fake-balanced
    max_cost_per_call_usd: 0.50

  frontier:
    purpose: difficult escalation
    provider_model: test/fake-frontier
    requires_budget_check: true
```

Production provider/model identifiers replace the fake values later without changing domain/application logic.

## Budget Semantics

The owner explicitly does not want cost limits to discourage use.

Therefore the budget architecture should distinguish **interaction availability** from **expensive execution**.

Recommended order when projected spend approaches the hard ceiling:

1. route routine transformations to cheaper capable models;
2. increase cache/context reuse;
3. compact context more aggressively;
4. avoid unnecessary duplicate review calls;
5. prefer existing running worker capacity where safe;
6. prevent new frontier-model escalation unless essential;
7. prevent new costly Developer Agent execution if it would exceed the ceiling;
8. keep low-cost owner/Manager interaction available where possible;
9. notify the owner with measured spend/projected impact before requesting a budget increase.

The **$50/month** ceiling should therefore function like a resource governor, not a message-count quota.

Phase 0 only implements the policy primitives and test cases; it does not yet know real provider economics.

## Persistence Design

### Migration-first development

Schema changes require Alembic migrations from the beginning.

Do not use application startup `create_all()` as the normal database migration mechanism.

### Database schema organization

A single application schema is acceptable initially.

Tables should use:

- UUID-style stable IDs generated by the application;
- timezone-aware timestamps;
- explicit enum/check constraints where appropriate;
- foreign keys;
- unique constraints for idempotency keys;
- JSONB only for legitimately flexible payloads, not to avoid modeling core fields.

### Transaction boundary

Application commands should define transactional units of work.

Tool/network calls should not be hidden inside database transactions that can remain open for long periods.

External side effects need explicit idempotency handling.

## DBOS Phase 0 Proof

Phase 0 should contain one deliberately small workflow proving the architecture.

### Scenario

```text
1. Create WorkRequest.
2. Start ManagerPlanningWorkflow.
3. Workflow creates a Plan and one Task using fake model output.
4. Policy determines an owner decision is required.
5. Workflow persists DecisionRequest and pauses.
6. Application process is stopped/restarted.
7. Owner answer is recorded.
8. Exact workflow resumes.
9. Task moves to READY.
10. Workflow completes.
```

No real Developer Agent or GitHub write operation is required.

### Required proof

The test must demonstrate that restart/retry does not:

- duplicate the plan;
- duplicate the task;
- duplicate the decision request;
- lose the correlation between owner answer and workflow;
- emit duplicate non-idempotent domain events.

## Minimal Manager-Agent Proof

Pydantic AI should be used only after the workflow/domain foundation exists.

The first Manager proof should accept a deterministic test input such as:

```text
"Update repository X so CI verifies documentation links."
```

It should produce a structured application-level result containing:

```text
objective
repository_candidates
plan_steps
decisions_required
task_drafts
risk_summary
```

For CI/unit tests this should use a deterministic fake/test model.

An optional manually triggered integration test may use a real provider, but it must:

- not run automatically on every CI build;
- have a strict low dollar cap;
- record provider/model/usage;
- be safe to skip when no API credential is configured.

## API Surface in Phase 0

Keep the API deliberately small.

Suggested endpoints:

```text
GET  /health
GET  /ready
POST /v1/conversations
POST /v1/conversations/{id}/messages
POST /v1/work-requests
GET  /v1/work-requests/{id}
GET  /v1/work-requests/{id}/tasks
GET  /v1/decisions/{id}
POST /v1/decisions/{id}/answer
GET  /v1/events
GET  /v1/usage/summary
```

This is an internal prototype API, not yet the final mobile contract.

Do not add broad generic CRUD endpoints for every table. Expose application actions/use cases.

## Authentication in Phase 0

Do not implement production passkeys yet.

Local API options:

- loopback/local-only development; or
- a simple development-only bearer token controlled through environment configuration.

The authentication boundary must be isolated so WebAuthn/passkeys can replace the dev mechanism later.

Never accidentally deploy the development bypass to a publicly reachable environment.

## Security Boundaries in Phase 0

Even before real credentials exist, enforce structural boundaries.

### Domain/application code must never receive raw global credentials.

It receives secret references or scoped adapter interfaces.

### Logs must redact secrets.

Implement a redaction utility/test for common secret-bearing configuration fields.

### External tool calls require policy evaluation.

Even fake GitHub tools in Phase 0 should go through `PolicyEngine` + `ToolExecutor` rather than being called directly from an agent adapter.

### No provider payload is authoritative.

Normalize required information into Overlord state before considering a workflow step complete.

### No arbitrary code execution in the control-plane process.

Developer code execution arrives later in isolated workers.

## Observability

Phase 0 should establish structured logs from the beginning.

Every significant log/event should carry relevant correlation identifiers:

```text
request_id
conversation_id
work_request_id
task_id
agent_run_id
tool_call_id
workflow_id
```

Do not log:

- secret values;
- full authorization headers;
- unnecessary raw provider payloads;
- unredacted environment dumps.

Metrics infrastructure can remain lightweight, but the application should expose enough internal counters/timers that a later metrics backend can be attached.

## Testing Strategy

### Unit tests

Must cover:

- state-machine transitions;
- domain invariants;
- budget policy;
- approval policy;
- event creation;
- model-profile routing decisions;
- idempotency keys;
- adapter normalization;
- configuration validation;
- log redaction.

### Integration tests

Against real local PostgreSQL:

- migrations up/down where practical;
- repository persistence;
- transactional behavior;
- JSON/event payload round trip;
- full-text-search groundwork if implemented in Phase 0;
- DBOS workflow pause/restart/resume;
- duplicate-retry protection.

### Architecture tests

Add tests or static checks proving:

- `domain` does not import FastAPI/SQLAlchemy/DBOS/Pydantic AI/provider SDKs;
- `application` does not import concrete external adapters;
- provider-specific modules do not leak into canonical domain types.

These tests are especially important because automated coding agents will later modify this repository.

### Contract tests

Create reusable contract suites for future adapter implementations:

```text
DeveloperAgentContract
ModelGatewayContract
SecretStoreContract
ArtifactStoreContract
ToolExecutorContract
```

Fake adapters must pass them first. OpenHands/OpenCode/provider implementations inherit the same contract later.

## Existing Task Fixtures

Do not delete `tasks/` or `templates/`.

During Phase 0:

- document them as legacy/prototype fixtures;
- add them to test fixture discovery if useful;
- do not treat their current Markdown schema as the canonical new domain model;
- later create explicit import/parsing compatibility only if there is value.

## CI Workflow

Create one initial GitHub Actions workflow triggered on pull requests and `main` pushes.

Minimum jobs:

```text
lint
format-check
type-check
unit-tests
integration-tests-postgres
architecture-tests
migration-check
```

Use GitHub Actions service containers or an equivalent ephemeral Postgres service for integration tests.

Real provider/LLM tests should **not** be required for normal CI.

### CI secret usage

GitHub Actions Secrets are appropriate for future optional integration/deployment jobs.

No production/runtime secret should be copied into normal unit-test jobs.

## Branch and Pull Request Discipline

Phase 0 should be delivered through focused PRs rather than one large bootstrap commit.

Recommended sequence:

### PR 0A — Repository foundation

- `pyproject.toml`;
- package skeleton;
- Docker/local Postgres;
- basic FastAPI health endpoint;
- lint/type/test configuration;
- CI workflow;
- development documentation.

### PR 0B — Domain model and events

- domain entities/value objects/enums;
- state transitions;
- events;
- budget/policy primitives;
- unit tests.

### PR 0C — Persistence

- SQLAlchemy models/mappings;
- repository interfaces/implementations;
- Alembic migrations;
- Postgres integration tests.

### PR 0D — Ports and fake adapters

- ModelGateway;
- DeveloperAgent;
- ToolExecutor;
- PolicyEngine;
- SecretStore;
- ArtifactStore;
- Notification/Speech interfaces;
- reusable contract tests;
- deterministic fake implementations.

### PR 0E — DBOS durable workflow proof

- DBOS configuration;
- planning workflow;
- durable pause/restart/resume scenario;
- idempotency tests.

### PR 0F — Minimal Manager structured-output proof

- Pydantic AI adapter;
- deterministic fake model in CI;
- structured planning output;
- optional manual real-provider smoke test;
- usage normalization.

### PR 0G — Phase 0 closeout

- architectural consistency review;
- README/developer docs finalization;
- local clean-build test;
- recovery/restart demonstration;
- Phase 0 verification record.

Each PR should pass CI before merging.

## Documentation Required Inside `Overlord`

Phase 0 should leave the repository self-documenting.

Minimum docs:

### `docs/architecture.md`

- dependency/layer diagram;
- authoritative state boundaries;
- runtime/provider replaceability rules.

### `docs/domain-model.md`

- entities;
- state machines;
- event taxonomy;
- identifiers/correlation semantics.

### `docs/security-boundaries.md`

- secret/reference rules;
- policy/tool boundary;
- log redaction;
- future worker isolation assumptions.

### `docs/development.md`

- prerequisites;
- environment setup;
- database start/migrate/reset;
- running API/tests/lint/type checks;
- how to add an adapter safely.

### `docs/decisions/`

Use lightweight architecture decision records for choices that materially constrain the design.

Initial ADRs should include:

```text
0001-control-plane-owns-canonical-state.md
0002-postgres-as-primary-state-store.md
0003-provider-neutral-model-gateway.md
0004-developer-agent-adapter-boundary.md
0005-db-os-for-phase-0-durability.md
0006-cost-ceiling-is-resource-governor-not-usage-quota.md
```

## Phase 0 Acceptance Criteria

Phase 0 is complete only when all of these are true.

### Repository

- application installs from a clean clone;
- local setup is documented;
- CI is green;
- all dependencies are declared/locked;
- existing `tasks/` and `templates/` remain available.

### Architecture

- canonical domain model contains no provider/runtime-specific types;
- adapter contracts exist for models, Developer Agents, secrets, tools, artifacts, notifications and speech;
- architecture tests enforce dependency direction.

### Database

- Postgres starts locally through the supported development workflow;
- migrations build a fresh database;
- migrations are not replaced by startup `create_all()`;
- domain entities round-trip through repository implementations;
- event/idempotency uniqueness works.

### Workflow durability

- test Work Request starts planning workflow;
- workflow pauses on an owner decision;
- application can restart;
- the exact workflow resumes after answer;
- no duplicate Plan/Task/Decision/Event is produced.

### Manager abstraction

- Manager structured planning call works through `ModelGateway`;
- default CI uses a deterministic fake model;
- switching the configured fake/provider profile requires configuration/adapter changes only, not domain changes;
- usage/cost result is normalized.

### Policy and cost

- `$50/month` global hard ceiling is represented in budget policy;
- policy distinguishes cheap interaction from expensive execution;
- tests prove a costly action can be blocked while low-cost interaction remains permitted;
- LLM cannot bypass policy by requesting a tool directly.

### Security

- test secret values are redacted from logs;
- domain/application services do not expose a secret-listing mechanism;
- tool actions require policy evaluation;
- no production credential is required to run normal CI.

### Recovery/developer usability

- a new developer/agent can clone the repository, start Postgres, migrate, run the API, and pass tests using only repository documentation;
- stopped/restarted services recover durable test state;
- Phase 0 closeout document records evidence.

## Definition of Done

Phase 0 does **not** mean Overlord is usable as the final successor.

It means the core application has a durable, testable, provider-neutral spine that is safe to extend.

At completion, it should be possible to begin Phase 1/2 work without revisiting fundamental questions such as:

- where canonical state lives;
- what a Work Request/Plan/Task/Decision is;
- how agents are represented;
- how provider models are swapped;
- how coding runtimes are swapped;
- how privileged tools are authorized;
- how cost is enforced;
- how external implementations are kept out of the domain model.

## What Happens Immediately After Phase 0

The next development stage should be the **local control-plane functional loop**, then the Developer Agent benchmark.

Expected sequence:

```text
Phase 0
repository + contracts + durability spine
      |
      v
Phase 1
working local Manager conversation/planning loop
      |
      v
Phase 2
OpenHands vs OpenCode benchmark through same DeveloperAgent interface
      |
      v
Phase 3
GitHub App and complete branch/PR/Actions lifecycle
      |
      v
Phase 4
remote ephemeral workers
      |
      v
Phase 5
phone/PWA + notifications + voice
```

No new broad architecture research is required before Phase 0 implementation unless a concrete dependency incompatibility appears.

## Implementation Approval Gate

This document is the final pre-code Phase 0 review artifact.

After owner approval, implementation should begin with **PR 0A — Repository foundation** in `Overlord`.

The implementation should not silently expand scope. Any proposed change that materially affects recurring cost, security boundaries, canonical state ownership, framework/provider lock-in, or the approved MVP scope should return to the owner as a decision rather than being hidden inside a coding PR.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)
- [Research 03 — Mobile, Notifications, Authentication, and Voice](/projects/notes/high-director-successor-research-03/)
- [Research 04 — LLM Provider Strategy and Cost](/projects/notes/high-director-successor-research-04/)
- [Research 05 — Persistent State, Memory, Backups, and Security](/projects/notes/high-director-successor-research-05/)
- [Research 06 — Build vs Adopt and Interoperability Boundaries](/projects/notes/high-director-successor-research-06/)

## Verification Record

- Last verified: `2026-08-10`
- Verified against: approved successor architecture and owner decisions; current `Overlord` repository tree/fixtures; current documented compatibility direction for Pydantic AI, DBOS, FastAPI, SQLAlchemy/Alembic and PostgreSQL.
- Verified by: High Director
- Verification scope: Phase 0 scope, repository structure, domain model, interfaces, persistence/workflow approach, local development boundaries, test/CI strategy, cost semantics, security rules, implementation sequence and acceptance criteria.
- Unverified areas: exact PostgreSQL driver combination with the final DBOS/SQLAlchemy versions, exact lockfile tool choice, and real-provider Pydantic AI behavior; these are intentionally resolved through PR 0A/0F compatibility tests rather than architecture assumptions.
