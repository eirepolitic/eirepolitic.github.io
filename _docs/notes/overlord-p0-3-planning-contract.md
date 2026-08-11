---
title: Overlord P0.3 — Ports, Fake Adapters, and Planning Contract
summary: Implementation record for Overlord P0.3, establishing provider-neutral runtime/tool ports, deterministic fake adapters, and a validated Manager planning service that persists versioned plans and owner decisions without a real LLM provider.
section: notes
doc_type: note
status: active
created: 2026-08-10
updated: 2026-08-10
last_verified: 2026-08-10
owner: High Director
order: 126
permalink: /projects/notes/overlord-p0-3-planning-contract/
tags:
  - overlord
  - implementation
  - phase-0
  - p0-3
  - planning
  - ports-and-adapters
  - fake-adapters
---

# Overlord P0.3 — Ports, Fake Adapters, and Planning Contract

## Outcome

P0.3 of the approved Overlord Phase 0 implementation plan is complete.

Overlord can now take a canonical `WorkRequest`, obtain optional repository context through a provider-neutral GitHub boundary, request a structured plan through an LLM boundary, validate that plan, generate canonical application IDs, and persist a versioned `Plan` / `Task` / `DecisionRequest` graph without depending on a real LLM provider or provider-native conversation object.

## Source Delivery

- Repository: `Overlord`
- Pull request: `#4` — `feat: add P0.3 planning contract and fake adapters`
- Merge commit: `bdb77a07205989817ba752ac4a5cf45d165a00b3`
- Exact post-merge CI: run `#66`
- CI conclusion: `success`

## Provider-Neutral Ports

P0.3 adds explicit application boundaries for:

- `LLMPort` — structured model generation and normalized model/provider/usage metadata;
- `DeveloperAgentPort` — future coding-agent task/session lifecycle;
- `GitHubPort` — repository context required by the planning service;
- `SecretStorePort` — runtime secret resolution;
- `PlanningRepositoryPort` — persistence operations consumed by `PlanningService`.

The application service depends on these contracts rather than provider SDKs or runtime-specific session objects.

## Deterministic Fake Adapters

P0.3 adds offline fake implementations for:

- language-model structured output;
- Developer Agent lifecycle;
- GitHub repository context;
- environment-backed local secret lookup.

The fake LLM records requests, returns a configured Pydantic structured object, validates that the returned object matches the requested output type, and emits normalized fake usage metadata.

The fake Developer Agent supports the planned lifecycle surface:

```text
create task
send instruction
stream events
get status
request summary
cancel
resume
get usage
finalize
```

These adapters make the planning/control-plane contracts testable without a paid model credential or external network dependency.

## Structured Planning Contract

The Manager planning boundary uses validated, provider-neutral structures for:

- task definitions;
- task dependencies;
- owner-decision requests;
- decision options;
- objective and summary;
- assumptions and findings;
- recommended next action;
- confidence.

### Stable local task keys

The model returns stable local task keys such as:

```text
inspect
implement
validate
```

The model does **not** generate canonical database IDs.

After validation, `PlanningService` creates Overlord-owned UUIDs and maps all parent/dependency/decision references to those canonical IDs.

This prevents a provider-specific model response from becoming the authoritative identity system.

## Planning Validation

P0.3 rejects malformed planning output before persistence.

Validated conditions include:

- task keys must be unique;
- parent task keys must exist;
- a task cannot be its own parent;
- parent hierarchies cannot contain cycles;
- dependency endpoints must exist;
- a task cannot depend on itself;
- duplicate dependency edges are rejected;
- dependency graphs cannot contain cycles;
- owner decisions may reference only known tasks;
- a decision may contain at most one recommended option;
- required planning text cannot be blank;
- task priorities remain within the canonical `0–100` range;
- confidence remains within `0–1`.

Invalid structured model output therefore cannot directly create canonical application state.

## Planning Service

`PlanningService` now performs the first real Manager-level application workflow:

```text
WorkRequest
    |
    v
load canonical request
    |
    +--> optional RepositoryContext through GitHubPort
    |
    v
build provider-neutral ModelRequest
    |
    v
LLMPort
    |
    v
validated PlanningResult
    |
    v
generate canonical Plan / Task / Decision IDs
    |
    v
persist versioned planning graph
    |
    v
emit AuditEvents
```

The LLM never inserts SQL rows directly.

## Plan Versioning

The planning repository boundary now exposes `get_latest_plan(work_request_id)`.

`PlanningService` uses this to create revisions rather than overwriting prior planning history:

```text
Plan v1
   |
   v
Plan v2 -> supersedes_plan_id = v1.id
```

The integration test proves that a second planning pass becomes version 2 and that the latest plan can be reloaded from canonical PostgreSQL state.

## Owner Decision Handling

If the planning result identifies a material owner decision:

- the affected task is persisted as `WAITING_OWNER`;
- `requires_owner_input` is set;
- a canonical `DecisionRequest` is created;
- any supplied decision options are persisted;
- an `OWNER_DECISION_REQUIRED` audit event is emitted;
- the overall Plan remains `DRAFT` while owner input is required.

Plans with no owner decision requirement can be created as `ACTIVE`.

The durable pause/resume behavior itself belongs to DBOS work in P0.5.

## Repository Context Boundary

The initial `GitHubPort` is deliberately narrow.

P0.3 only requires a `RepositoryContext` containing fields such as:

- repository reference;
- summary;
- default branch;
- known files;
- optional metadata.

This is enough to prove that planning can incorporate repository context without prematurely implementing broad GitHub write permissions. The full GitHub development lifecycle remains a later phase.

## Audit Evidence

Planning now emits canonical audit events including:

- `PLAN_CREATED`;
- `OWNER_DECISION_REQUIRED`.

The plan event records useful planning evidence such as:

- plan ID/version;
- assumptions;
- findings;
- recommended next action;
- confidence;
- model provider/model identifier reported by the adapter.

Provider-specific response objects are not required to understand the planning history.

## Tests

P0.3 adds three test layers.

### Planning unit tests

Prove rejection of:

- duplicate task keys;
- unknown dependency targets;
- dependency cycles;
- parent cycles;
- decisions referencing unknown task keys.

### Adapter contract tests

Prove deterministic behavior for:

- fake LLM structured output;
- fake Developer Agent lifecycle;
- fake GitHub repository context;
- local environment secret lookup.

### PostgreSQL planning integration test

Proves that a fake Manager can:

1. receive a persisted `WorkRequest`;
2. receive fake repository context;
3. produce a structured plan;
4. persist two tasks plus a dependency;
5. persist an architecture decision and options;
6. mark the affected task as waiting for owner input;
7. persist planning audit events;
8. reload the complete result from PostgreSQL;
9. run planning again;
10. create Plan version 2 that supersedes version 1.

No provider-native state is required to reload or continue the result.

## CI Gate

The exact post-merge Overlord CI run `#66` succeeded on commit:

`bdb77a07205989817ba752ac4a5cf45d165a00b3`

The gate included:

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

## Boundaries Preserved

P0.3 did **not** introduce:

- Pydantic AI as a runtime dependency;
- OpenAI, Anthropic, Google, or another paid LLM API credential;
- OpenHands or OpenCode;
- DBOS execution;
- remote Developer Workers;
- a production GitHub App;
- AWS Secrets Manager configuration;
- mobile/PWA functionality;
- recurring cloud infrastructure.

The fake adapter path remains sufficient for the normal CI suite.

## Next Work Package

The next approved work package is **P0.4 — Pydantic AI Manager Adapter**.

Planned scope includes:

- add Pydantic AI behind `LLMPort`;
- configuration-driven model/capability mapping;
- convert `ModelRequest` into a real Pydantic AI structured-output request;
- normalize returned provider/model/usage information into `ModelResponse`;
- preserve deterministic fake adapters for normal CI;
- provide an optional real-provider smoke-test path that is disabled unless explicitly configured.

P0.4 should not require a paid provider key for normal repository acceptance. A real smoke test should run only when deliberately configured.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord P0.1 — Repository Foundation](/projects/notes/overlord-p0-1-repository-foundation/)
- [Overlord P0.2 — Domain Model and Persistence](/projects/notes/overlord-p0-2-domain-persistence/)
- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)

## Verification Record

- Last verified: `2026-08-10`.
- Verified against: `Overlord` PR #4, merge commit `bdb77a07205989817ba752ac4a5cf45d165a00b3`, the final source tree on `main`, and exact successful post-merge CI run #66.
- Verified by: High Director.
- Verification scope: provider-neutral ports, fake adapters, planning schema/invariants, canonical ID generation, plan versioning, repository context, owner-decision persistence, audit events, contract tests, PostgreSQL planning integration, and final CI result.
