---
title: Overlord P0.2 — Domain Model and Persistence
summary: Implementation record for Overlord P0.2, establishing provider-neutral canonical domain state, PostgreSQL persistence, Alembic migrations, repository adapters, and database-backed validation tests.
section: notes
doc_type: note
status: active
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
owner: High Director
order: 125
permalink: /projects/notes/overlord-p0-2-domain-persistence/
tags:
  - overlord
  - implementation
  - phase-0
  - p0-2
  - postgres
  - sqlalchemy
  - alembic
---

# Overlord P0.2 — Domain Model and Persistence

## Outcome

P0.2 of the approved Overlord Phase 0 implementation plan is complete.

Overlord now has a provider-neutral canonical domain model and a PostgreSQL persistence layer that can reload important application state without depending on an LLM-provider conversation, Developer Agent runtime, or framework-native session object.

## Source Delivery

- Repository: `Overlord`
- Feature pull request: `#2` — `feat: add P0.2 domain model and persistence`
- Corrective pull request: `#3` — `fix: clean up P0.2 merged diagnostics and formatting`
- Final `main` commit: `492a0cac1ba19b662c350128800e6f227c443907`
- Exact post-merge CI: run `#37`
- CI conclusion: `success`

PR #2 merged while the final branch formatting/diagnostic cleanup was still landing. PR #3 was therefore used as a focused corrective change to apply the final formatted persistence implementation and remove temporary diagnostic artifacts. It did not expand P0.2 scope.

## Implemented Domain Layer

The repository now defines framework-independent canonical records for:

- conversations;
- messages;
- work requests;
- versioned plans;
- tasks;
- task dependencies;
- decision requests and options;
- owner decisions;
- agent runs;
- model calls and normalized usage/cost metadata;
- audit events.

The domain layer also defines stable enum vocabularies for conversation/work/task state, decision categories, agent roles, capability tiers, actors, dependency types, and message source modes.

### Domain invariants

P0.2 enforces important invariants before execution/persistence, including:

- non-blank canonical work/message/task/decision text;
- plan versions greater than or equal to one;
- task priority constrained to `0–100`;
- non-negative token/cost counters;
- no task self-dependencies;
- no dependency references outside the supplied plan;
- no cyclic task dependency graph;
- task parent references must remain inside the supplied plan;
- task parent hierarchies cannot contain cycles.

## Persistence Architecture

The persistence layer uses SQLAlchemy 2.x typed mappings behind separate domain/repository adapters.

The canonical domain records remain usable without a SQLAlchemy session. ORM rows are an implementation detail of the persistence adapter rather than the application business model.

The database schema now includes:

```text
conversations
messages
work_requests
plans
tasks
task_dependencies
decision_requests
decision_options
owner_decisions
agent_runs
model_calls
audit_events
```

Database constraints reinforce domain invariants such as unique plan versions per work request, valid priority ranges, non-self task dependencies, and non-negative model usage/cost values.

## Canonical Message Persistence

P0.2 includes explicit persistence for the canonical `Message` record.

This is important to the successor architecture because the owner/Manager conversation must survive replacement of the LLM provider. A provider-native message/session identifier can be stored as optional metadata, but it is not required to reload the canonical message history.

An integration test proves that a persisted owner message round-trips through PostgreSQL independently of any provider conversation object.

## Repository Adapters and Transaction Ordering

`SqlAlchemyRepository` provides explicit add/read operations for the P0.2 aggregates and evidence records.

The persistence mapping deliberately does not rely on SQLAlchemy ORM relationships to become the application graph. Because of that design, the repository explicitly flushes parent records before dependent records while keeping the entire operation inside the same transaction.

Examples include:

```text
Conversation -> WorkRequest
WorkRequest -> Plan
Plan -> Tasks
Tasks -> TaskDependencies
DecisionRequest -> DecisionOptions -> OwnerDecision
WorkRequest -> AgentRun -> ModelCall
```

This preserves foreign-key ordering without coupling domain navigation to SQLAlchemy relationship objects. Transaction rollback still applies to the full unit of work.

## Alembic Migrations

P0.2 establishes the repository's Alembic migration framework and current migration chain:

- `0001_domain_state.py`
- `0002_messages_and_constraint_alignment.py`

The second revision aligns the initial schema with the final P0.2 contract by adding canonical messages, enforcing the final task-priority constraint, aligning the dependency-type default, and adding the required decision-option index.

CI proves the complete migration chain can upgrade an empty PostgreSQL database to `head`.

## Tests

P0.2 adds database-backed integration coverage in addition to domain unit tests.

Coverage includes:

- domain text/range validation;
- self-dependency rejection;
- task dependency cycle detection;
- valid acyclic dependency graphs;
- aggregate persistence round-trip;
- canonical Message round-trip;
- decision option and owner-decision round-trip;
- agent/model/audit state round-trip;
- duplicate plan-version database constraint;
- transaction rollback after an integrity violation;
- settings behavior under CI environment overrides.

## CI Gate

The permanent Overlord CI now runs:

```text
docker compose config --quiet
PostgreSQL start/readiness
uv sync --locked --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run alembic upgrade head
uv run pytest
```

The exact post-merge run `#37` succeeded on commit `492a0cac1ba19b662c350128800e6f227c443907`.

## Boundaries Preserved

P0.2 did **not** introduce:

- paid LLM/provider credentials;
- a real Manager LLM adapter;
- DBOS workflow execution;
- OpenHands or OpenCode;
- remote Developer Workers;
- GitHub App credentials;
- production secret storage;
- mobile/PWA functionality;
- recurring cloud infrastructure.

The persistence design is intended to support those later components without making any of them the canonical state owner.

## Next Work Package

The next approved work package is **P0.3 — Ports, Fake Adapters, and Planning Contract**.

Planned scope includes:

- `LLMPort`;
- `DeveloperAgentPort`;
- `SecretStorePort`;
- a skeletal `GitHubPort` only where the planning context contract needs it;
- deterministic fake adapters;
- provider-neutral planning request/result schemas;
- `PlanningService`;
- contract tests for the fake adapters and planning boundary.

The P0.3 acceptance gate is that a `WorkRequest` can produce a validated, persisted `Plan` and `Task` graph using only deterministic fake integrations, with no provider-native object required to reload or continue the result.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord P0.1 — Repository Foundation](/projects/notes/overlord-p0-1-repository-foundation/)
- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)

## Verification Record

- Last verified: `2026-08-10`.
- Verified against: `Overlord` feature PR #2, corrective PR #3, final `main` commit `492a0cac1ba19b662c350128800e6f227c443907`, and successful exact post-merge CI run #37.
- Verified by: High Director.
- Verification scope: domain records/invariants, SQLAlchemy persistence mappings, canonical message persistence, transaction ordering/rollback, Alembic migrations, PostgreSQL integration tests, repository cleanup, and final CI result.
