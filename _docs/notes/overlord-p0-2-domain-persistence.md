---
title: Overlord P0.2 — Domain Model and Persistence
summary: Implementation record for Overlord P0.2, establishing canonical provider-neutral domain state, PostgreSQL persistence, explicit Alembic migrations, and real database integration tests.
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
  - persistence
---

# Overlord P0.2 — Domain Model and Persistence

## Outcome

P0.2 of the approved Overlord Phase 0 implementation plan is complete.

Overlord now has an owner-controlled canonical state model that can be loaded independently of any LLM provider conversation, Developer Agent session, or external agent runtime.

## Source Delivery

Primary feature delivery:

- Repository: `Overlord`
- Pull request: `#2` — `feat: add P0.2 domain model and persistence`
- Feature merge commit: `03f685ecff5370ca801eaa37b2cd1cd02033c120`

Final corrective delivery:

- Pull request: `#3` — `fix: clean up P0.2 merged diagnostics and formatting`
- Final verified `main` commit: `492a0cac1ba19b662c350128800e6f227c443907`
- Exact post-merge CI: run `#37`
- CI conclusion: `success`

## Implemented Domain State

The canonical domain layer now covers:

- conversations;
- provider-neutral messages;
- work requests;
- versioned plans;
- tasks;
- task dependencies;
- decision requests;
- decision options;
- immutable owner decisions;
- agent runs;
- normalized model usage/cost calls;
- append-oriented audit events.

Domain state uses Overlord-owned IDs and enums. Provider/runtime session identifiers remain optional external references rather than canonical task or conversation identifiers.

## Persistence Layer

P0.2 adds:

- SQLAlchemy 2.x typed PostgreSQL mappings;
- Psycopg 3 database connectivity;
- transactional session management with rollback on failure;
- repository adapters that return domain objects rather than ORM rows;
- explicit parent-before-child flush ordering while preserving a single transaction;
- deterministic task-parent insertion ordering;
- task dependency validation and cycle checks;
- decision bundle persistence;
- agent/model-cost persistence;
- audit-event persistence;
- provider-neutral message persistence.

The application/domain layer does not use provider-native or ORM objects as its authoritative representation of work state.

## Schema and Migrations

Alembic is now the authoritative schema migration mechanism.

Current revisions:

1. `0001_domain_state` — creates the initial canonical control-plane tables and constraints.
2. `0002_messages_alignment` — adds canonical messages and aligns task/dependency/index constraints with the domain model.

The CI gate proves that an empty PostgreSQL database can migrate to `head` before integration tests run.

## Database Constraints and Invariants

The implementation enforces or tests important rules including:

- plan versions must be positive;
- each work request cannot persist duplicate plan version numbers;
- task priority stays within the supported range;
- a task cannot depend on itself;
- supplied task dependency graphs cannot contain cycles;
- parent tasks must belong to the same supplied plan graph;
- task-parent hierarchy cannot contain a cycle;
- decision options and owner decisions must belong to the matching decision request;
- model token counts and reported cost cannot be negative;
- dependent persistence records are inserted only after required parents exist.

## Integration and Transaction Tests

P0.2 tests now exercise a real migrated PostgreSQL instance in CI.

Coverage includes:

- canonical message round-trip without relying on provider conversation state;
- conversation/work-request persistence;
- plan/task/dependency graph round-trip;
- decision request/options/owner-decision round-trip;
- agent-run persistence;
- model usage/cost round-trip;
- audit-event round-trip;
- duplicate plan-version rejection;
- transaction rollback without partial graph persistence;
- domain validation for invalid dependencies and cycles.

## CI Gate

The permanent CI workflow now verifies:

```text
docker compose config --quiet
docker compose up -d postgres
uv sync --locked --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run alembic upgrade head
uv run pytest
```

Exact post-merge CI run `#37` passed on final `main` commit `492a0cac1ba19b662c350128800e6f227c443907`.

## Corrective Merge Note

PR #2 initially had a successful pre-merge CI run, but branch-only diagnostic automation advanced the branch again before GitHub performed the squash merge. That caused temporary diagnostic files and one unformatted source line to enter the first `main` merge snapshot.

Post-merge CI correctly rejected that snapshot at the lint gate.

PR #3 then:

- removed all temporary diagnostic/status artifacts;
- applied the single Ruff formatting correction;
- ran the full CI suite successfully before merge;
- merged as the final P0.2 cleanup;
- passed the full CI suite again on the exact resulting `main` commit.

This is recorded explicitly so the failed intermediate post-merge run is not mistaken for the final P0.2 verification state.

## Cost and Infrastructure Boundary

P0.2 introduced no paid model calls, no remote Developer Workers, no production cloud deployment, and no recurring infrastructure beyond the already-approved local development environment.

The approved USD $50 monthly prototype ceiling remains configuration/policy rather than a fixed interaction quota.

## Next Work Package

The next approved work package is **P0.3 — Ports, fake adapters, and planning contract**.

Planned scope includes:

- provider-neutral `LLMPort`;
- `DeveloperAgentPort`;
- `SecretStorePort`;
- narrow future-facing GitHub port where needed;
- deterministic fake adapters;
- structured Manager planning input/output contract;
- PlanningService that validates model output before creating domain state;
- contract tests proving adapter replacement does not alter canonical state.

P0.3 should begin as a separate focused source PR.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord P0.1 — Repository Foundation](/projects/notes/overlord-p0-1-repository-foundation/)
- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)

## Verification Record

- Last verified: `2026-08-10`.
- Verified against: `Overlord` PR #2, feature merge `03f685ecff5370ca801eaa37b2cd1cd02033c120`, corrective PR #3, final `main` commit `492a0cac1ba19b662c350128800e6f227c443907`, repository tree on `main`, and successful exact post-merge CI run #37.
- Verified by: High Director.
- Verification scope: canonical domain records, provider-neutral message state, PostgreSQL mappings/repositories, Alembic migrations, transaction ordering/rollback, integration tests, dependency lock, repository documentation, and final CI state.
