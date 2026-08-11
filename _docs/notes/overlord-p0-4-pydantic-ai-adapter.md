---
title: Overlord P0.4 — Pydantic AI Manager Adapter
summary: Implementation record for Overlord P0.4, connecting the provider-neutral LLM port to Pydantic AI v2 with explicit capability-tier model configuration, normalized usage metadata, offline contract testing, and an opt-in real-provider smoke path.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 127
permalink: /projects/notes/overlord-p0-4-pydantic-ai-adapter/
tags:
  - overlord
  - implementation
  - phase-0
  - p0-4
  - pydantic-ai
  - llm
  - provider-neutral
---

# Overlord P0.4 — Pydantic AI Manager Adapter

## Outcome

P0.4 of the approved Overlord Phase 0 implementation plan is complete.

Overlord now has a real LLM runtime implementation behind the existing provider-neutral `LLMPort`. Application services continue to depend on Overlord's own contracts; Pydantic AI and any upstream model provider remain replaceable adapter/runtime dependencies rather than canonical state owners.

## Source Delivery

- Repository: `Overlord`
- Feature pull request: `#5` — `feat: add P0.4 Pydantic AI Manager adapter`
- Feature merge commit: `37ca4b1ec739bf083ebb5bdb1df059e44ec68382`
- Corrective pull request: `#6` — `chore: complete P0.4 post-merge cleanup`
- Final `main` commit: `8bfd15b017d1a889eb51fd1b8fdce2163ae10724`
- Exact final post-merge CI: run `#90`
- CI conclusion: `success`

PR #5 merged while two temporary pytest diagnostic workflows were still present. PR #6 removed those workflows only; it did not change application code, dependencies, model configuration, or runtime behavior.

## Runtime Dependency

P0.4 adds Pydantic AI v2 through the repository dependency contract:

```text
pydantic-ai-slim[anthropic,google,openai]>=2.27,<3.0
```

The dependency is included in the committed `uv.lock`, so normal repository installation remains reproducible.

Pydantic AI is imported only inside the LLM adapter layer. `PlanningService`, domain models, persistence, and API contracts do not import provider-specific model SDKs.

## Capability-Tier Configuration

Overlord preserves the existing capability vocabulary:

```text
EFFICIENT
BALANCED
FRONTIER
```

Each tier can be mapped independently through typed settings:

```text
OVERLORD_MODEL_EFFICIENT
OVERLORD_MODEL_BALANCED
OVERLORD_MODEL_FRONTIER
```

Model mappings are unconfigured by default. `require_model_id()` rejects an unset tier before any model/provider request can occur.

This keeps model/provider selection explicit and allows future model changes without changing the planning service, database schema, or canonical work state.

## Pydantic AI Adapter

`PydanticAIAdapter` implements `LLMPort`.

Its flow is:

```text
ModelRequest
    |
    v
resolve capability tier
    |
    v
build Pydantic AI Agent
    |
    v
run structured request
    |
    v
validate requested output type
    |
    v
normalize provider/model/usage metadata
    |
    v
ModelResponse
```

### Adapter inputs

The adapter consumes Overlord-owned fields such as:

- capability tier;
- system instructions;
- canonical prompt messages;
- expected Pydantic structured-output type;
- request metadata.

### Adapter outputs

The adapter returns Overlord's `ModelResponse`, including normalized:

- structured output;
- provider;
- model;
- input tokens;
- cached-input tokens;
- output tokens;
- finish reason;
- external provider response ID where available.

Provider-native result objects do not leave the adapter boundary.

## Structured Output Safety

The adapter validates that the returned object matches the `output_type` requested by `ModelRequest`.

If an adapter/provider returns the wrong structured type, Overlord raises an error rather than passing malformed data into `PlanningService` or persistence.

The P0.3 planning validations therefore remain the next protection layer after model-runtime structured output.

## Offline Test Path

Normal CI does not require an OpenAI, Anthropic, Google, or other hosted-model API key.

P0.4 contract tests explicitly configure Pydantic AI's offline `test` model and exercise the real `PydanticAIAdapter` implementation. This proves that:

- Pydantic AI can instantiate through the Overlord adapter;
- structured output crosses the adapter correctly;
- normalized usage metadata is available;
- the `LLMPort` boundary remains intact;
- no billable provider call is required for repository acceptance.

The suite also verifies capability routing, provider-string switching, wrong structured-output rejection, and rejection of unconfigured tiers before any provider execution.

## Explicit Real-Provider Smoke Path

The repository includes:

```text
scripts/smoke_pydantic_ai.py
```

This path is deliberately disabled unless:

```text
OVERLORD_RUN_REAL_LLM_SMOKE=1
```

is explicitly set.

The script requires a configured real balanced-tier model before it will run. It is a deliberate manual operation rather than part of normal CI.

No real provider credential was added to the repository during P0.4, and no paid provider request was required for P0.4 acceptance.

## Provider Independence

The P0.4 implementation preserves the intended replacement boundary:

```text
PlanningService
      |
      v
LLMPort
      |
      +--> FakeLLMAdapter
      |
      +--> PydanticAIAdapter
                 |
                 +--> configured provider/model
```

Changing a provider or model does not require:

- rewriting `PlanningService`;
- changing canonical Plan/Task/Decision records;
- changing the PostgreSQL schema;
- migrating provider-owned conversation state;
- changing the Developer Agent contract.

Pydantic AI itself can also be replaced later by another `LLMPort` implementation if required.

## Tests

P0.4 adds/extends coverage for:

- configured capability-tier routing;
- model-provider string switching;
- unconfigured tier rejection before provider execution;
- normalized structured adapter response;
- provider/model metadata mapping;
- token/cache usage mapping;
- external response identifiers;
- wrong structured output rejection;
- real Pydantic AI adapter operation using the offline test model.

The final repository suite contained 31 tests during the P0.4 acceptance cycle and passed on the final cleaned `main` state.

## CI Gate

The exact final post-merge Overlord CI run `#90` succeeded on commit:

`8bfd15b017d1a889eb51fd1b8fdce2163ae10724`

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

The final `main` tree contains only the permanent `ci.yml` workflow; temporary P0.4 formatting, lock-bootstrap, and pytest diagnostic workflow files are not present.

## Boundaries Preserved

P0.4 did **not** introduce:

- a permanently selected hosted LLM provider/model;
- a provider API key in GitHub or source control;
- billable model calls in CI;
- DBOS workflow execution;
- OpenHands or OpenCode;
- remote Developer Workers;
- production GitHub App credentials;
- production AWS Secrets Manager configuration;
- mobile/PWA functionality;
- recurring cloud infrastructure.

## Next Work Package

The next approved work package is **P0.5 — DBOS Durable Manager Workflow**.

Planned scope includes:

- add DBOS behind the workflow/application boundary;
- create a durable Manager planning workflow;
- persist a canonical owner `DecisionRequest` before waiting;
- suspend durably while owner input is absent;
- survive application-process restart;
- resume the exact workflow after the owner decision is recorded;
- use stable workflow IDs and idempotency keys;
- prove replay/retry does not duplicate Plans, Tasks, Decisions, or AuditEvents.

P0.5 should continue to keep canonical work state in the Overlord domain/PostgreSQL schema rather than making DBOS internal state the only authority.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord P0.1 — Repository Foundation](/projects/notes/overlord-p0-1-repository-foundation/)
- [Overlord P0.2 — Domain Model and Persistence](/projects/notes/overlord-p0-2-domain-persistence/)
- [Overlord P0.3 — Ports, Fake Adapters, and Planning Contract](/projects/notes/overlord-p0-3-planning-contract/)
- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: `Overlord` feature PR #5, feature merge `37ca4b1ec739bf083ebb5bdb1df059e44ec68382`, corrective PR #6, final `main` commit `8bfd15b017d1a889eb51fd1b8fdce2163ae10724`, final source tree, and exact successful post-merge CI run #90.
- Verified by: High Director.
- Verification scope: Pydantic AI dependency/version boundary, explicit capability configuration, adapter normalization, structured-output validation, offline test execution, guarded real-provider smoke path, provider-neutral application boundary, post-merge cleanup, and final CI result.
