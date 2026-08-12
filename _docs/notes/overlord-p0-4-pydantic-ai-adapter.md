---
title: Overlord P0.4 — Pydantic AI Manager Adapter
summary: Implementation record for Overlord P0.4, connecting the provider-neutral LLM port to Pydantic AI v2 with capability-tier model routing, offline test-model coverage, normalized usage metadata, and an explicitly guarded real-provider smoke path.
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

Overlord now has a real Pydantic AI implementation of its existing provider-neutral `LLMPort`. Application services still depend only on Overlord contracts; Pydantic AI is an adapter that can be replaced without changing the canonical planning/domain model.

Normal repository acceptance remains offline and credential-free. Pydantic AI's built-in `test` model is used to exercise the real adapter without making a provider API call.

## Source Delivery

- Repository: `Overlord`
- Feature pull request: `#5` — `feat: add P0.4 Pydantic AI Manager adapter`
- Feature merge commit: `37ca4b1ec739bf083ebb5bdb1df059e44ec68382`
- Final cleanup pull request: `#6` — `chore: complete P0.4 post-merge cleanup`
- Exact cleanup PR head: `392e413dfe2a6d596d7d5f7ce0034ef4aad9fa9e`
- Cleanup PR CI: run `#89` — `success`
- Final P0.4 `main` commit: `8bfd15b017d1a889eb51fd1b8fdce2163ae10724`
- Exact final post-merge CI: run `#90` — `success`

PR #5 delivered the Pydantic AI adapter. PR #6 established the final P0.4 repository state after temporary verification workflows were cleaned up. The exact PR #6 head passed the permanent CI workflow before merge, and the exact resulting `main` SHA passed the same workflow again after merge.

## Runtime Dependency

The merged repository now includes:

```text
pydantic-ai>=2.0,<3.0
```

The P0.4 dependency-lock workflow eventually succeeded on its seventh run and committed the refreshed `uv.lock`. Final permanent CI then passed `uv sync --locked --all-groups` on the exact final `main` SHA, proving that the committed lockfile is current for the merged dependency set.

P0.4 deliberately keeps Pydantic AI behind `LLMPort`. The domain, persistence, planning, and future workflow layers do not import provider-specific model SDKs directly.

## Capability-Tier Routing

Overlord retains its three provider-neutral capability tiers:

```text
EFFICIENT
BALANCED
FRONTIER
```

Runtime settings expose independent model mappings:

```text
OVERLORD_MODEL_EFFICIENT
OVERLORD_MODEL_BALANCED
OVERLORD_MODEL_FRONTIER
```

Each mapping is a Pydantic AI-compatible model identifier. Switching one tier therefore changes configuration rather than application-service code or database schema.

### Safe defaults

All three tiers default to:

```text
test
```

This is Pydantic AI's offline test model. The default configuration therefore cannot accidentally create a paid provider request simply because `PydanticAIAdapter` is selected.

A tier may also be deliberately set to `None` / left unusable in explicit configuration, in which case `require_model_id()` raises `ModelConfigurationError` before a provider call is attempted.

## Pydantic AI Adapter

`src/overlord/adapters/llm/pydantic_ai.py` implements `LLMPort`.

The adapter currently:

1. receives Overlord's provider-neutral `ModelRequest`;
2. resolves the configured model for the requested capability tier;
3. constructs a Pydantic AI `Agent` with the requested structured `output_type`;
4. renders the current canonical planning messages into a deterministic prompt;
5. executes the selected Pydantic AI model;
6. validates that the returned structured object matches the requested output type;
7. normalizes model/provider identity and stable token usage into Overlord's `ModelResponse`;
8. preserves any provider response ID only as an optional external reference.

The adapter does not make provider-native conversation/session state authoritative.

## Structured Output Boundary

P0.3 already required the Manager to return a validated `PlanningResult`.

P0.4 proves that the same structured-output contract can now be supplied by a real model runtime without changing `PlanningService`:

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
              +--> test
              +--> future OpenAI mapping
              +--> future Anthropic mapping
              +--> future Google mapping
```

`PlanningService` does not know which branch is being used.

## Usage Normalization

The Pydantic AI adapter maps stable usage fields into Overlord's provider-neutral `ModelUsage`:

```text
input_tokens
cached_input_tokens
output_tokens
```

`ModelUsage.cost_usd` remains part of the wider Overlord contract, but P0.4 does not make a framework/provider price estimate authoritative. Cost calculation and hard-budget enforcement remain Overlord control-plane responsibilities.

This preserves the ability to change provider/pricing sources without redefining the LLM port.

## Compatibility Handling

The adapter includes a small compatibility layer around Pydantic AI result metadata so that Overlord can obtain usage and the final model response without exposing Pydantic AI message/result classes through application services.

If provider/model metadata is unavailable on the final response, the adapter falls back to the configured model identifier for audit metadata.

The special `test` model is normalized as provider/model `test`.

## Offline Adapter Tests

P0.4 adds contract coverage for the real adapter without requiring a network call.

The tests prove:

- capability-tier model resolution;
- deterministic Overlord message rendering;
- structured output validation;
- normalized input/cache/output token metadata;
- provider/model metadata mapping;
- optional external response ID mapping;
- rejection of a deliberately unconfigured capability tier;
- rejection of the wrong structured output type;
- execution through Pydantic AI's actual offline `test` model.

The final suite contained 31 passing tests during the P0.4 source gate.

## Real-Provider Smoke Boundary

`scripts/smoke_pydantic_ai.py` provides an explicitly opt-in real-provider proof path.

The command refuses to make a provider request unless:

```text
OVERLORD_RUN_REAL_LLM_SMOKE=1
```

is set and the balanced tier has been changed from `test` to a real provider/model identifier.

This smoke path is not part of normal CI.

Therefore:

- no paid provider credential is required to merge P0.4;
- no paid model is selected by default;
- no billable LLM request is required for repository acceptance;
- deliberately testing a hosted model remains an explicit operator action.

## Security Boundary

P0.4 does not add provider credentials to source control or canonical state.

Provider API keys remain runtime/adapter secrets. The planning/domain/persistence layers do not depend on provider API-key names.

Production runtime secret retrieval remains behind `SecretStorePort`; hosted secret-store wiring is still deferred.

## Temporary Workflow Cleanup

The temporary branch-only lock workflow `.github/workflows/p04-lock.yml` was removed after the lockfile was successfully refreshed. The final `main` workflow tree contains only the permanent `.github/workflows/ci.yml`; P0.4 lock, formatting, and pytest diagnostic workflows are not part of the final repository state.

## CI Gate

The final P0.4 `main` CI run `#90` succeeded on:

`8bfd15b017d1a889eb51fd1b8fdce2163ae10724`

The permanent gate included:

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

All substantive checks and the complete test suite passed on the exact final P0.4 `main` commit.

## Boundaries Preserved

P0.4 did **not** introduce:

- a permanent OpenAI model choice;
- a permanent Anthropic model choice;
- a permanent Google model choice;
- a paid-provider credential requirement for CI;
- provider-native canonical conversation state;
- DBOS workflow execution;
- OpenHands or OpenCode;
- remote Developer Workers;
- production GitHub App automation;
- AWS Secrets Manager runtime wiring;
- mobile/PWA functionality;
- recurring cloud infrastructure.

## Next Work Package

The next approved work package is **P0.5 — DBOS Durable Manager Workflow**.

Planned scope includes:

- add DBOS to the local control-plane runtime;
- execute Manager planning through a durable workflow;
- persist a canonical `DecisionRequest` before waiting for owner input;
- pause durably while owner input is outstanding;
- stop/restart the application process;
- resolve the owner decision;
- resume the exact workflow;
- use stable workflow/idempotency identifiers so replay/retry does not duplicate Plans, Tasks, Decisions, or AuditEvents;
- keep DBOS internal state separate from canonical Overlord domain state.

P0.5 acceptance should prove the restart/pause/resume behavior with no paid model credential required.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord P0.1 — Repository Foundation](/projects/notes/overlord-p0-1-repository-foundation/)
- [Overlord P0.2 — Domain Model and Persistence](/projects/notes/overlord-p0-2-domain-persistence/)
- [Overlord P0.3 — Ports, Fake Adapters, and Planning Contract](/projects/notes/overlord-p0-3-planning-contract/)
- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: `Overlord` PR #5, cleanup PR #6, lock workflow run #7, exact cleanup PR-head CI run #89, final `main` commit `8bfd15b017d1a889eb51fd1b8fdce2163ae10724`, exact post-merge CI run #90, merged `pyproject.toml`, adapter/configuration/tests, and the final `.github/workflows` tree.
- Verified by: High Director.
- Verification scope: Pydantic AI dependency, capability-tier routing, offline test defaults, structured adapter boundary, usage normalization, provider metadata, smoke-test guard, locked dependencies, temporary workflow removal, and exact final CI result.
