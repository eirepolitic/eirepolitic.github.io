---
title: Overlord — Phase 0 Implementation Plan
summary: Detailed implementation contract for establishing the Overlord successor repository, domain model, provider-neutral interfaces, local persistence, durable workflows, tests, and CI before cloud infrastructure or autonomous coding workers are introduced.
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
  - implementation-plan
  - phase-0
  - python
  - postgres
  - dbos
  - pydantic-ai
---

# Overlord — Phase 0 Implementation Plan

## Purpose

This document converts the approved High Director successor architecture into the first concrete implementation contract for the existing `Overlord` repository.

Phase 0 establishes the application spine and the interfaces that later phases will depend on. Its purpose is to make expensive future choices—LLM provider, Developer Agent runtime, worker host, speech provider, mobile wrapper, secret manager—replaceable rather than embedded in the application.

Phase 0 is intentionally **local-first**. It should not create recurring cloud infrastructure or give the new application broad production credentials.

## Approved Decisions

The owner has approved the following constraints:

- source repository: `Overlord`;
- prototype spending ceiling: **USD $50/month total**;
- the ceiling is a spending guardrail, not an artificial usage quota;
- the product should make normal use feel effectively unconstrained by routing work to efficient models/infrastructure wherever possible;
- MVP external integration scope begins with GitHub development workflows;
- broader AWS, Google Workspace, Appsmith, Power BI and Power Automate capabilities are deferred until the core system is proven;
- long-lived runtime secrets will eventually use a runtime secret-store interface, with AWS Secrets Manager currently preferred for the hosted prototype and GitHub Actions Secrets reserved for CI/deployment credentials;
- no production secret-store configuration is required in Phase 0.

## Existing `Overlord` Repository State

The repository is effectively a clean application slate.

Current content consists of:

- `README.md`;
- small Markdown task/test fixtures under `tasks/`;
- task templates under `templates/`.

These existing files should be preserved. Phase 0 should not delete or rewrite them unless a later cleanup task establishes that they are obsolete. They may become useful fixtures for Manager/task parsing tests.

## Phase 0 Outcome

At the end of Phase 0, a developer should be able to clone `Overlord` and run a local control-plane skeleton that can:

1. start a local PostgreSQL-backed application;
2. create a Manager conversation and owner work request;
3. create and persist a structured plan;
4. create Development Tasks and dependencies;
5. record agent runs, events, decisions, approvals and model-usage metadata;
6. execute a durable DBOS workflow;
7. pause that workflow for owner input;
8. stop the application;
9. restart it;
10. resume the same workflow from durable state;
11. invoke a provider-neutral Manager interface using a deterministic fake model in tests;
12. expose a minimal local API for inspecting the state;
13. pass automated unit, integration, migration and durability tests in GitHub Actions.

No real autonomous coding agent is required in Phase 0.

## Explicit Phase 0 Non-Goals

Do **not** implement these yet:

- OpenHands integration;
- OpenCode integration;
- Developer Worker VM provisioning;
- DigitalOcean/Fly/Hetzner deployment;
- production PWA;
- Web Push;
- passkeys;
- speech-to-text or text-to-speech;
- production AWS Secrets Manager wiring;
- broad GitHub App permissions;
- automatic PR creation/merging;
- Appsmith/Google/Power BI/Power Automate integrations;
- MCP servers beyond interface placeholders;
- ACP/A2A networking;
- `pgvector`;
- LiteLLM proxy;
- Temporal;
- Kubernetes;
- multi-user tenancy.

Phase 0 is successful only if the core application remains clean enough to add those later without redesigning its authoritative state model.

## Runtime Baseline

### Python

Use **Python 3.13** as the repository baseline.

Reasoning:

- Pydantic AI currently requires Python 3.10 or later;
- DBOS currently requires Python 3.9 or later;
- Python 3.13 is a mature supported maintenance line while Python 3.14 is the newest feature line;
- choosing 3.13 reduces early dependency-compatibility risk without creating a meaningful future migration problem.

Do not hard-code patch version behavior into the application. CI and local containers should use a current supported 3.13 patch release and the dependency lockfile should provide reproducibility.

### Packaging

Use:

- `pyproject.toml` as the authoritative package/project configuration;
- `uv` for local dependency resolution, locking and command execution;
- a committed lockfile;
- `src/` package layout.

The application package name should be `overlord`.

### Database

Use **PostgreSQL** for both application-state persistence and DBOS durability in Phase 0.

One local Postgres container may host separate logical databases:

```text
overlord        -> application/domain state
overlord_dbos   -> DBOS system/durable workflow state
```

Do not allow DBOS tables to become substitutes for application-domain records.

### Containers

Use Docker Compose for local infrastructure only:

```text
postgres
optional test-support services only when justified later
```

The Python application should normally run directly on the developer machine during Phase 0 so debugging remains simple. A containerized application target may be added once the local application works.

## Initial Technology Choices

Phase 0 should use the following libraries behind our own interfaces:

| Concern | Phase 0 choice | Boundary |
| --- | --- | --- |
| HTTP API | FastAPI | `overlord.api` |
| Validation/domain DTOs | Pydantic v2 | domain/application schemas |
| Manager LLM abstraction | Pydantic AI | behind `LLMPort` / Manager service |
| Durable workflow | DBOS | behind workflow/application boundary |
| SQL persistence | SQLAlchemy 2.x | repository adapters |
| PostgreSQL driver | psycopg 3 | persistence adapter only |
| Schema migration | Alembic | `migrations/` |
| Settings | pydantic-settings | `overlord.config` |
| HTTP client | httpx | outbound adapters only |
| Testing | pytest | `tests/` |
| Static lint/format | Ruff | repository-wide |
| Type checking | mypy | repository-wide, strictness increased gradually |

Framework-specific types should not leak into core domain records unless there is a strong reason.

## Proposed Repository Structure

```text
Overlord/
├── src/
│   └── overlord/
│       ├── __init__.py
│       ├── api/
│       │   ├── app.py
│       │   ├── dependencies.py
│       │   └── routes/
│       │       ├── health.py
│       │       ├── conversations.py
│       │       ├── work_requests.py
│       │       ├── tasks.py
│       │       └── decisions.py
│       ├── application/
│       │   ├── services/
│       │   │   ├── conversation_service.py
│       │   │   ├── planning_service.py
│       │   │   ├── task_service.py
│       │   │   └── decision_service.py
│       │   └── commands/
│       ├── domain/
│       │   ├── models/
│       │   ├── enums.py
│       │   ├── events.py
│       │   ├── errors.py
│       │   └── ids.py
│       ├── ports/
│       │   ├── llm.py
│       │   ├── developer_agent.py
│       │   ├── github.py
│       │   ├── secrets.py
│       │   ├── notifications.py
│       │   ├── speech.py
│       │   ├── repositories.py
│       │   └── clock.py
│       ├── adapters/
│       │   ├── llm/
│       │   │   ├── fake.py
│       │   │   └── pydantic_ai.py
│       │   ├── developer/
│       │   │   └── fake.py
│       │   ├── github/
│       │   │   └── fake.py
│       │   ├── secrets/
│       │   │   └── environment.py
│       │   └── persistence/
│       │       ├── database.py
│       │       ├── orm.py
│       │       └── repositories/
│       ├── workflows/
│       │   ├── manager_workflow.py
│       │   └── decision_wait.py
│       ├── config/
│       │   └── settings.py
│       └── observability/
│           └── logging.py
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── contract/
│   ├── durability/
│   └── fixtures/
├── migrations/
│   ├── env.py
│   └── versions/
├── docs/
│   ├── architecture.md
│   └── development.md
├── tasks/                     # existing fixtures retained
├── templates/                 # existing templates retained
├── .github/
│   └── workflows/
│       └── ci.yml
├── .env.example
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

The exact number of modules may be reduced during implementation if files become artificial wrappers. The boundaries are more important than preserving every proposed filename.

## Architecture Rule

Use a lightweight **ports-and-adapters / hexagonal** structure.

Direction of dependencies:

```text
API / workflows / adapters
          |
          v
application services
          |
          v
domain + ports
```

Core domain/application code must not import:

- OpenHands;
- OpenCode;
- vendor LLM SDKs directly;
- GitHub SDK clients directly;
- AWS SDK clients directly;
- FastAPI request objects;
- SQLAlchemy ORM sessions except inside persistence/application transaction boundaries;
- DBOS-specific state as the only representation of task state.

This rule is the main mechanism for preserving future provider/runtime portability.

## Domain Model v1

Phase 0 should define stable IDs using UUIDs generated by the application.

### Conversation

Represents a persistent owner/Manager conversation.

Minimum fields:

```text
id
created_at
updated_at
status
summary
```

### Message

Canonical conversation message independent of model provider.

Minimum fields:

```text
id
conversation_id
work_request_id? 
task_id?
author_type
content_type
content
source_mode
created_at
provider?
model?
external_message_id?
metadata
```

`source_mode` examples:

```text
text
voice_transcript
manager
system
tool
```

### WorkRequest

Represents an owner-requested outcome.

Minimum fields:

```text
id
conversation_id
title
request_text
status
repository_ref?
created_at
updated_at
```

### Plan

A versioned Manager plan for a WorkRequest.

Minimum fields:

```text
id
work_request_id
version
status
objective
summary
created_at
supersedes_plan_id?
```

Do not overwrite old plans when the Manager revises a plan.

### Task

Durable unit of delegated work.

Minimum fields:

```text
id
work_request_id
plan_id
parent_task_id?
title
description
status
priority
repository_ref?
branch_ref?
requires_owner_input
created_at
updated_at
started_at?
completed_at?
```

Initial task statuses:

```text
pending
ready
running
waiting_owner
blocked
validation
completed
failed
cancelled
```

### TaskDependency

```text
task_id
depends_on_task_id
dependency_type
```

Database constraints must reject self-dependencies and duplicate edges. Application logic should detect dependency cycles before work begins.

### DecisionRequest

Represents a point where owner input is required.

Minimum fields:

```text
id
work_request_id
task_id?
category
question
context
recommendation
status
created_at
resolved_at?
```

Initial categories:

```text
requirements
architecture
security
access
cost
destructive_action
privacy
external_commitment
ambiguous_tradeoff
```

### DecisionOption

```text
id
decision_request_id
label
description
is_recommended
```

### OwnerDecision

Immutable owner response.

```text
id
decision_request_id
selected_option_id?
response_text
created_at
```

### AgentRun

Represents one invocation/session/run of a Manager or Developer Agent runtime.

```text
id
agent_role
work_request_id
task_id?
runtime
provider
model
external_session_id?
status
started_at
ended_at?
metadata
```

The `external_session_id` is an adapter reference, never the canonical task ID.

### ModelCall

Normalized cost/usage event.

```text
id
agent_run_id?
work_request_id
task_id?
provider
model
capability_tier
input_tokens?
cached_input_tokens?
output_tokens?
reported_cost_usd?
started_at
completed_at
metadata
```

Phase 0 tests may populate fake usage. Real billing adapters arrive later.

### AuditEvent

Append-oriented event record.

```text
id
correlation_id
event_type
actor_type
actor_id?
work_request_id?
task_id?
created_at
payload
```

Important domain transitions should emit an AuditEvent explicitly rather than relying only on log lines.

## Provider-Neutral Ports

### `LLMPort`

The first model boundary should express capabilities needed by Overlord rather than mirror any provider's API.

Conceptual interface:

```python
class LLMPort(Protocol):
    async def generate(self, request: ModelRequest) -> ModelResponse: ...
```

`ModelRequest` should contain provider-neutral fields such as:

```text
capability_profile
system_instructions
messages
structured_output_schema?
tools?
budget_context?
request_metadata
```

`ModelResponse` should expose:

```text
canonical content
structured result?
tool proposals
usage
provider/model metadata
finish status
```

Do not expose provider-native conversation IDs as required application state.

### `DeveloperAgentPort`

Define now; implement only a fake adapter in Phase 0.

Required conceptual operations:

```text
create_task
send_instruction
stream_events / poll_events
get_status
request_summary
cancel
resume
get_usage
finalize
```

This is the future shared contract for OpenHands and OpenCode.

### `GitHubPort`

Define a narrow future-facing interface without granting real credentials in Phase 0.

Initial conceptual groups:

```text
repository read
branch operations
file operations
pull requests
workflow operations
merge operations
configuration/secrets administration
```

The implementation should later split read/write/high-risk authorization internally, even if the top-level adapter remains one GitHub integration.

### `SecretStorePort`

```text
get_secret(name)
```

Phase 0 adapter:

- local environment variables only;
- explicit test fake.

Future adapters:

- AWS Secrets Manager;
- SOPS/OpenBao if justified.

### Future placeholders

Define interfaces only when useful to preserve dependency direction; do not build real functionality yet:

- `NotificationPort`;
- `SpeechToTextPort`;
- `TextToSpeechPort`;
- worker-provisioning port.

Avoid creating dozens of empty interfaces with no concrete architectural purpose.

## Model Capability Profiles

Define the capability vocabulary now without choosing permanent providers.

```text
EFFICIENT
BALANCED
FRONTIER
```

A configuration record should be capable of mapping a profile to a provider/model later.

Phase 0 fake configuration example:

```yaml
models:
  efficient:
    adapter: fake
    model: fake-efficient
  balanced:
    adapter: fake
    model: fake-balanced
  frontier:
    adapter: fake
    model: fake-frontier
```

The domain should store the resolved provider/model on each ModelCall for auditability.

## Manager Planning Contract

Phase 0 should implement one deliberately narrow Manager behavior: convert a WorkRequest plus supplied repository/project context into a structured planning result.

Suggested output schema:

```text
objective
assumptions
findings
tasks[]
dependencies[]
owner_decisions_required[]
recommended_next_action
confidence
```

The planning service validates the model output before it becomes domain state.

The LLM must not directly insert arbitrary database rows.

Flow:

```text
owner WorkRequest
      |
      v
PlanningService
      |
      +--> build provider-neutral ModelRequest
      |
      v
LLMPort
      |
      v
structured PlanningResult
      |
      v
validate domain invariants
      |
      +--> create versioned Plan
      +--> create Tasks/dependencies
      +--> create DecisionRequests if needed
      +--> emit AuditEvents
```

## Durable Workflow v1

Implement one DBOS workflow proving the desired human-in-the-loop behavior.

Suggested lifecycle:

```text
WORK_REQUEST_CREATED
        |
        v
manager workflow starts
        |
        v
planning service creates plan/tasks
        |
        +--> no decision needed -> mark plan ready -> workflow completes
        |
        +--> decision needed
                |
                v
        persist DecisionRequest
                |
                v
        workflow waits durably
                |
        application may stop/restart
                |
        owner decision recorded
                |
                v
        exact workflow resumes
                |
                v
        plan/task state updated
                |
                v
        workflow completes
```

The implementation must prevent replay/retry from creating duplicate decisions/tasks/events. Use stable workflow IDs and explicit idempotency keys for domain side effects.

## Persistence Design

### SQLAlchemy

Use SQLAlchemy 2.x ORM or SQL expression mappings inside the persistence adapter.

Domain models should remain usable without an active ORM session. Persistence models may be separate from domain dataclasses/Pydantic models if that keeps boundaries cleaner.

### Transactions

Application services should perform related state changes atomically where appropriate.

Example:

```text
create Plan
create Tasks
create TaskDependencies
create AuditEvents
COMMIT
```

Do not allow partially persisted plans unless the domain explicitly models that state.

### Migrations

Use Alembic from the first schema.

CI must test:

```text
empty database -> upgrade head -> application tests
```

A downgrade path is desirable but not required for every irreversible production migration in the long term. Phase 0 migrations should remain reversible where practical.

## Minimal Local API

Phase 0 does not need the final mobile API. It needs enough HTTP endpoints to exercise and inspect the spine.

Suggested endpoints:

```text
GET  /health
GET  /ready
POST /conversations
GET  /conversations/{id}
POST /work-requests
GET  /work-requests/{id}
POST /work-requests/{id}/plan
GET  /work-requests/{id}/tasks
GET  /decisions/pending
POST /decisions/{id}/resolve
GET  /events?work_request_id=...
```

Do not expose adapter/provider-native internals through the public API.

Authentication may be a development-only local guard in Phase 0. Passkey authentication is a later mobile phase.

## Configuration

All settings should be loaded through one typed configuration layer.

Example environment names:

```text
OVERLORD_ENV
OVERLORD_LOG_LEVEL
OVERLORD_DATABASE_URL
OVERLORD_DBOS_DATABASE_URL
OVERLORD_MODEL_EFFICIENT
OVERLORD_MODEL_BALANCED
OVERLORD_MODEL_FRONTIER
```

Rules:

- commit `.env.example`, never `.env`;
- no real secrets in Git;
- fail startup clearly when required settings are absent;
- tests should build Settings explicitly rather than depend on the developer's shell environment;
- future AWS/GitHub credentials should enter only through adapters/secret stores.

## Logging and Observability

Phase 0 should implement structured application logging from the start.

Every important log/event should carry available correlation identifiers:

```text
conversation_id
work_request_id
plan_id
task_id
agent_run_id
workflow_id
correlation_id
```

Do not log:

- secret values;
- provider API keys;
- authorization headers;
- full future GitHub App private keys;
- raw owner audio.

AuditEvent records and application logs are different:

- AuditEvent = durable domain/security history;
- log = operational diagnostic information.

## Budget Model in Phase 0

The approved **$50/month ceiling** should be represented as policy/configuration now even though Phase 0 uses fake model cost.

Do not implement a fixed number of permitted chats/tasks/messages.

Instead define budget state such as:

```text
monthly_ceiling_usd = 50.00
month_spend_usd
projected_month_spend_usd
soft_warning_threshold
hard_ceiling_behavior
```

Desired future behavior:

1. route routine work efficiently without bothering the owner;
2. use caching/context compaction;
3. destroy idle workers;
4. prefer lower-cost models where quality is sufficient;
5. escalate model tier only when justified;
6. notify only when measured/projected spend risks the hard ceiling.

Phase 0 acceptance should prove that fake usage events roll up correctly and that a policy service can distinguish normal, warning and blocked-cost states without imposing arbitrary interaction quotas.

## Security Boundaries in Phase 0

Even locally, establish these rules now:

- domain/services never read raw secrets directly from arbitrary environment variables;
- only the secret-store/config adapter owns secret resolution;
- database credentials are not returned through API responses;
- provider credentials never enter canonical messages;
- fake Developer Agent adapters receive task-scoped data only;
- SQL queries use parameterization/ORM rather than string-built SQL;
- IDs supplied through the API are validated;
- event payloads should not silently become a secret dumping ground;
- debug logs should be safe to retain.

No claim of production security should be made after Phase 0; this phase only establishes the correct boundaries.

## Testing Strategy

### Unit tests

No database/network where possible.

Cover:

- domain status transitions;
- task dependency rules;
- plan versioning;
- owner-decision invariants;
- budget calculations;
- model capability routing decisions;
- policy/escalation classification;
- planning-result validation.

### Integration tests

Use real local/test PostgreSQL.

Cover:

- repository adapters;
- migrations;
- transaction rollback;
- full-text-friendly schema fields/indexes where introduced;
- API persistence behavior.

### Contract tests

Run every implementation against shared port expectations.

Phase 0 examples:

```text
FakeLLMAdapter satisfies LLMPort behavior
PydanticAIAdapter satisfies LLMPort behavior without becoming canonical state
FakeDeveloperAgent satisfies DeveloperAgentPort behavior
EnvironmentSecretStore satisfies SecretStorePort behavior
```

These tests become critical when OpenHands/OpenCode/AWS adapters are added later.

### Durability tests

Required Phase 0 proof:

1. start workflow;
2. persist DecisionRequest;
3. terminate/restart application process;
4. resolve decision;
5. resume same workflow;
6. verify no duplicate Plan/Task/Decision/AuditEvent rows;
7. verify terminal state is correct.

Also test retry of a completed workflow step does not duplicate side effects.

### API tests

Cover:

- validation errors;
- missing IDs;
- state transitions;
- idempotent submissions where required;
- pending decision flow;
- event timeline.

## Code Quality Gates

Every pull request should pass:

```text
uv sync --locked
ruff check .
ruff format --check .
mypy src
pytest
alembic upgrade head  # against clean CI Postgres
```

If mypy strict mode creates excessive scaffolding initially, begin with a documented baseline and increase strictness by package. Do not disable type checking globally merely to make CI green.

## GitHub Actions CI

Create one Phase 0 CI workflow triggered on pull requests and pushes to `main`.

Jobs may be combined initially but must prove:

1. dependency lock resolves;
2. lint/format;
3. type checks;
4. unit tests;
5. PostgreSQL service starts;
6. Alembic migration succeeds from empty DB;
7. integration tests;
8. DBOS durability test or deterministic integration equivalent.

No deployment job is required in Phase 0.

CI credentials should use GitHub Actions Secrets only if a future real external integration test requires them. Phase 0 should be able to pass with no paid-provider credential.

## Documentation Required in `Overlord`

Phase 0 must add/update:

### `README.md`

Should explain:

- what Overlord is;
- current development status;
- local prerequisites;
- exact commands to start Postgres/install dependencies/run the API/run tests;
- where architecture documentation lives;
- explicit warning that Phase 0 is not production-ready.

### `docs/architecture.md`

Should document:

- dependency direction;
- canonical state ownership;
- domain model overview;
- ports/adapters;
- DBOS boundary;
- future Manager/Developer architecture;
- security boundary.

### `docs/development.md`

Should document:

- environment setup;
- Docker Compose;
- migrations;
- test commands;
- lint/type commands;
- branch/PR expectations;
- how to add an adapter without bypassing ports.

## Implementation Work Packages

Phase 0 should be delivered in small reviewable PRs rather than one large bootstrap commit.

### P0.1 — Repository foundation

Deliver:

- Python 3.13 project metadata;
- `src/overlord` package;
- `uv` lockfile;
- Ruff/mypy/pytest configuration;
- Docker Compose Postgres;
- typed settings;
- minimal `/health` endpoint;
- README bootstrap instructions;
- initial CI.

Gate:

- fresh clone can start database/API;
- CI passes without paid credentials.

### P0.2 — Domain model and persistence

Deliver:

- domain IDs/enums/models;
- SQLAlchemy persistence mappings/repositories;
- Alembic initial migration;
- WorkRequest/Plan/Task/Decision/AuditEvent persistence;
- core unit/integration tests.

Gate:

- empty DB migrates successfully;
- domain invariants tested;
- plan/task/decision data round-trips through repositories.

### P0.3 — Ports, fake adapters and planning contract

Deliver:

- `LLMPort`;
- `DeveloperAgentPort`;
- `SecretStorePort`;
- skeletal `GitHubPort` if needed by the planning context contract;
- deterministic fake adapters;
- provider-neutral planning input/output schemas;
- PlanningService.

Gate:

- a WorkRequest produces a validated Plan/Task graph using only fake integrations;
- no provider-native object is required to reload the result.

### P0.4 — Pydantic AI Manager adapter

Deliver:

- Pydantic AI implementation of `LLMPort`;
- model capability configuration;
- optional real-provider smoke-test command disabled from normal CI;
- normalized usage/result mapping.

Gate:

- core tests still pass with fake adapter only;
- application services do not import Pydantic AI directly;
- switching fake/Pydantic AI adapters is configuration/injection only.

A paid API key is not required for normal acceptance. A real smoke test should run only when deliberately configured.

### P0.5 — DBOS durable Manager workflow

Deliver:

- DBOS initialization;
- durable Manager planning workflow;
- DecisionRequest pause/resume mechanism;
- stable workflow IDs/idempotency keys;
- restart/recovery integration tests.

Gate:

- workflow survives process restart;
- owner decision resumes exact work;
- retries do not duplicate domain side effects.

### P0.6 — Minimal inspection API and event timeline

Deliver:

- local endpoints for conversations/work requests/tasks/decisions/events;
- structured logging/correlation IDs;
- fake cost events and monthly-budget aggregation;
- final documentation updates.

Gate:

- complete local demonstration can be driven by HTTP/API tests;
- event history explains how the request progressed;
- fake spend reaches warning/hard-ceiling states without imposing message/task quotas.

## Pull Request Discipline

For each work package:

1. create a focused branch;
2. implement only that package plus required supporting fixes;
3. update relevant `Overlord` docs in the same PR;
4. run local checks;
5. open PR;
6. require GitHub Actions success;
7. merge only after the package acceptance gate passes;
8. update the documentation website with meaningful architectural findings/changes when the implementation differs from this plan.

Do not merge broken intermediate contracts merely because a later package is expected to fix them.

## Phase 0 Acceptance Criteria

Phase 0 is complete only when all of the following are true.

### Repository

- `Overlord` has reproducible Python 3.13 setup and committed dependency lock;
- local PostgreSQL starts through Docker Compose;
- README/development/architecture docs are current;
- existing task/template fixtures remain available.

### Domain independence

- WorkRequest, Plan, Task, Decision, AgentRun, ModelCall and AuditEvent state can be loaded without any LLM-provider session;
- changing adapter configuration does not require a database schema rewrite;
- Developer Agent session IDs are optional external references only.

### Planning

- deterministic fake Manager converts a WorkRequest into a structured Plan and Tasks;
- invalid/contradictory planning output is rejected by application/domain validation;
- plan revisions are versioned rather than overwritten.

### Durability

- DBOS Manager workflow persists through application restart;
- a pending owner decision survives restart;
- resolving it resumes the same workflow;
- replay/retry creates no duplicate decisions/tasks/events.

### Persistence

- clean database migrates to head;
- integration tests pass against real PostgreSQL;
- transaction failures do not leave partially-created plans/task graphs.

### Interfaces

- fake LLM and fake Developer Agent pass contract tests;
- Pydantic AI is accessed only through the LLM adapter/port boundary;
- SecretStore abstraction exists with local/test implementation;
- no real provider credential is required for CI.

### Cost policy

- USD $50 monthly ceiling exists as configuration/policy;
- fake cost events aggregate by task/model/provider;
- normal use is not blocked by arbitrary message/task quotas;
- warning/block decisions are based on measured/projected spend.

### Quality

- Ruff passes;
- formatting check passes;
- mypy baseline passes;
- pytest suite passes;
- migrations pass in CI;
- no known secret is committed;
- no deployment or recurring cloud resource has been created.

## Phase 0 Exit Review

Before Phase 1 begins, review:

1. whether the domain model proved sufficient without becoming framework-specific;
2. whether DBOS restart/pause/resume behavior works as expected;
3. whether Pydantic AI remains cleanly replaceable through `LLMPort`;
4. whether cost accounting/policy can support high apparent usage under the $50 ceiling;
5. whether any schema/interface decision should be corrected before Developer Agents are added;
6. actual local resource use;
7. outstanding security issues.

If the contracts are clean, proceed to Phase 1/Developer-runtime benchmark work without another broad research phase.

## Decisions Deferred During Phase 0

Do not stop implementation to ask for these unless evidence reveals a material cost/security/function difference:

- final OpenHands vs OpenCode selection;
- final LLM provider/model;
- final worker host;
- STT/TTS provider;
- native app vs PWA fallback;
- `pgvector`;
- LiteLLM;
- OpenBao;
- Temporal.

Those decisions remain evidence-driven.

## Next Action After Plan Approval

Begin **P0.1 — Repository foundation** in `Overlord`.

That is the first source-code change. It should create the Python project skeleton, local Postgres environment, typed configuration, health endpoint, tooling, CI, and developer documentation—without introducing paid services or real autonomous-agent credentials.

## Related Documents

- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)
- [Research 03 — Mobile, Notifications, Authentication, and Voice](/projects/notes/high-director-successor-research-03/)
- [Research 04 — LLM Provider Strategy and Cost](/projects/notes/high-director-successor-research-04/)
- [Research 05 — Persistent State, Memory, Backups, and Security](/projects/notes/high-director-successor-research-05/)
- [Research 06 — Build vs Adopt and Interoperability Boundaries](/projects/notes/high-director-successor-research-06/)

## Verification Record

- Last verified: `2026-08-10`.
- Verified against: current `Overlord` repository tree/content; approved consolidated successor design; current official Pydantic AI installation requirements; current official DBOS Python requirements; current Python 3.13 maintenance status.
- Verified by: High Director.
- Verification scope: Phase 0 repository state, runtime compatibility assumptions, package/domain/interface structure, local persistence/durability architecture, work-package sequence, test/CI gates, and owner-approved cost/scope constraints.
- Unverified areas: real Pydantic AI provider behavior, DBOS restart behavior in this exact codebase, model token use, Developer Agent runtime characteristics, remote worker hosting, and mobile behavior. These are deliberately left to implementation/prototype evidence.
