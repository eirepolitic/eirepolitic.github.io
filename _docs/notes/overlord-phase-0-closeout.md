---
title: Overlord — Phase 0 Closeout
summary: Final verification record for Overlord Phase 0, closing the provider-neutral domain, persistence, model, durability, policy, security, architecture-test, and developer-documentation acceptance gates.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 129
permalink: /projects/notes/overlord-phase-0-closeout/
tags:
  - overlord
  - implementation
  - phase-0
  - closeout
  - architecture
  - policy
  - security
---

# Overlord — Phase 0 Closeout

## Outcome

Overlord Phase 0 is complete against the approved Phase 0 implementation contract.

The repository now has a durable, testable, provider-neutral control-plane spine that can be extended into the Phase 1 local Manager loop without revisiting canonical state ownership, persistence technology, model/runtime replaceability, durable workflow semantics, tool authorization, budget semantics, or the core security boundary.

Phase 0 does not make Overlord production-ready. It deliberately stops before the Phase 1 functional loop, remote Developer Agent execution, production GitHub automation, hosted infrastructure, or mobile/PWA work.

## Final Source Delivery

- Repository: `Overlord`
- Closeout pull request: `#8` — `feat: complete Phase 0 closeout`
- Exact final PR head: `104fde71e6fd697223bc68bc21796030c531d3c2`
- Exact PR-head permanent CI: run `#114` — `success`
- Final Phase 0 `main` commit: `721de238683686d7e0bd810bb8c8fa856d66d913`
- Exact post-merge permanent CI: run `#115` — `success`

The final PR head passed the complete permanent CI workflow before merge. The resulting squash commit on `main` passed the same workflow again after merge.

## Phase 0 Delivery Sequence

The implemented Phase 0 sequence is represented by the repository foundation and milestone records:

1. repository/local PostgreSQL/CI foundation;
2. canonical domain model and PostgreSQL persistence;
3. provider-neutral ports, fake adapters, and structured Manager planning contract;
4. Pydantic AI Manager adapter behind the model port;
5. DBOS durable Manager workflow with restart/resume proof;
6. Phase 0 closeout architecture, policy, security, and documentation gates.

The approved plan's PR 0G closeout was used as the final package rather than inventing an additional P0.6 milestone.

## Canonical State Boundary

Overlord-owned PostgreSQL records remain authoritative for application state.

Canonical records include:

- conversations and messages;
- Work Requests;
- versioned Plans;
- Tasks and dependencies;
- Decision Requests, options, and Owner Decisions;
- Agent Runs;
- normalized model usage/cost records;
- Audit Events.

Provider-native model messages/sessions, DBOS workflow records, GitHub objects, and future Developer Agent runtime sessions are external/runtime references only.

SQLAlchemy ORM classes remain inside the persistence adapter. Canonical domain/application code does not depend on SQLAlchemy, DBOS, Pydantic AI, provider SDKs, or future coding-agent SDK types.

## Provider and Runtime Boundaries

Phase 0 leaves explicit provider-neutral contracts for:

- model generation through `LLMPort`;
- Developer Agent runtimes through `DeveloperAgentPort`;
- secret resolution through `SecretStorePort`;
- privileged tool execution through `ToolExecutorPort`;
- artifact storage through `ArtifactStorePort`;
- notification delivery through `NotificationServicePort`;
- speech-to-text through `SpeechToTextPort`;
- text-to-speech through `TextToSpeechPort`;
- canonical planning persistence through repository ports.

Deterministic fake/offline adapters exist where Phase 0 acceptance requires executable contract proof. Deferred production integrations remain replaceable.

## Model Abstraction

Pydantic AI v2 remains an adapter behind Overlord's model port.

Manager/application code routes by capability tier rather than hard-coded provider names:

```text
EFFICIENT
BALANCED
FRONTIER
```

Normal CI remains offline and does not require a paid model credential. Real-provider smoke execution is explicitly opt-in and is not part of repository acceptance.

Model/provider identity and stable token/cache usage are normalized back into Overlord contracts rather than making Pydantic AI/provider objects canonical.

## Durable Workflow Proof

DBOS remains the Phase 0 durable workflow adapter.

The permanent test suite proves the Manager workflow can:

1. create canonical planning state;
2. persist an owner `DecisionRequest` before waiting;
3. pause durably for owner input;
4. destroy/relaunch the DBOS runtime;
5. send the owner answer to the original stable workflow ID;
6. resume the exact workflow;
7. resolve the canonical owner decision;
8. complete without duplicating canonical Plan, Task, Decision, or Audit state;
9. reject/reuse duplicate starts through the same workflow identity.

DBOS system/checkpoint state remains runtime coordination state rather than canonical domain state.

## Budget Policy

Phase 0 now explicitly represents the approved prototype spending policy.

The default global budget primitive is:

```text
soft limit: USD 40.00/month
hard limit: USD 50.00/month
```

The hard ceiling is a resource governor, not an interaction quota.

Tests prove that an expensive execution projected beyond the hard ceiling returns `REQUIRE_BUDGET_APPROVAL`, while low-cost owner/Manager interaction remains `ALLOW` even at the ceiling.

This preserves ordinary interaction while constraining expensive model/Developer Agent execution first.

## Tool and Approval Policy

Phase 0 distinguishes owner product decisions from permission to execute restricted actions.

`ApprovalRequest` is the explicit provider-neutral permission primitive. Deterministic policy results include:

```text
ALLOW
DENY
REQUIRE_OWNER_DECISION
REQUIRE_APPROVAL
REQUIRE_BUDGET_APPROVAL
```

`AuthorizedToolService` evaluates policy before calling `ToolExecutorPort`.

A contract/unit test proves that when policy returns `REQUIRE_APPROVAL`, the fake executor receives no request. An LLM or agent can therefore propose an action but cannot bypass Overlord's deterministic authorization boundary.

## Security Boundary

Phase 0 closeout adds a recursive structured-log redaction utility and tests.

Common secret-bearing fields—including authorization values, API keys, passwords, access/refresh tokens, generic secret fields, and private keys—are replaced with:

```text
[REDACTED]
```

The secret-store contract resolves individual references and exposes no generic mechanism to enumerate every secret value.

No production credential is required for normal CI.

Arbitrary Developer Agent code execution is still outside the control-plane process and remains deferred to later isolated workers.

## Architecture Enforcement

Phase 0 closeout adds static architecture tests that inspect Python imports.

The tests enforce that:

- `domain` does not import FastAPI, SQLAlchemy, DBOS, Pydantic AI, AWS/GitHub SDKs, or other forbidden external framework/provider roots;
- `application` does not import concrete modules under `overlord.adapters`.

These tests are part of the permanent pytest suite and help protect the ports-and-adapters direction when later automated coding agents modify the repository.

## Documentation Closeout

The repository now contains the required self-documenting Phase 0 set:

```text
docs/architecture.md
docs/development.md
docs/domain-model.md
docs/security-boundaries.md
```

It also contains the six required architecture decision records:

```text
0001-control-plane-owns-canonical-state.md
0002-postgres-as-primary-state-store.md
0003-provider-neutral-model-gateway.md
0004-developer-agent-adapter-boundary.md
0005-db-os-for-phase-0-durability.md
0006-cost-ceiling-is-resource-governor-not-usage-quota.md
```

The README was finalized to describe the actual Phase 0 state rather than an earlier intermediate milestone.

The historical `tasks/` and `templates/` Markdown fixtures remain available and are not treated as the new canonical domain schema.

## Clean-Build / CI Gate

Permanent CI run `#114` succeeded on exact final PR head:

`104fde71e6fd697223bc68bc21796030c531d3c2`

Permanent CI run `#115` succeeded on exact final `main` commit:

`721de238683686d7e0bd810bb8c8fa856d66d913`

The permanent gate includes:

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

The full test suite covers the architecture direction, policy/budget behavior, approval/tool authorization, secret redaction, fake deferred adapter boundaries, canonical persistence/planning, Pydantic AI offline contracts, and DBOS restart/resume/idempotency proof.

No dependency change was required for 0G, so the previously verified lockfile remained current. The final workflow tree contains only the permanent `.github/workflows/ci.yml` workflow; temporary branch diagnostic workflows were removed before acceptance.

## Phase 0 Acceptance Summary

### Repository

- clean locked dependency installation: **passed**;
- Docker Compose/PostgreSQL development path: **passed**;
- explicit Alembic clean migration: **passed**;
- permanent CI: **green**;
- legacy `tasks/` / `templates/` retained: **yes**.

### Architecture

- canonical domain remains provider/runtime neutral: **passed**;
- model/Developer Agent/secret/tool/artifact/notification/speech boundaries exist: **passed**;
- dependency-direction architecture tests: **passed**.

### Database

- PostgreSQL is canonical state store: **passed**;
- migrations are explicit rather than startup `create_all()`: **passed**;
- repository/integration coverage: **passed**.

### Workflow durability

- durable owner-decision pause: **passed**;
- DBOS restart and exact workflow resume: **passed**;
- duplicate canonical state prevention: **passed**.

### Manager abstraction

- structured planning through provider-neutral port: **passed**;
- Pydantic AI adapter remains replaceable: **passed**;
- normal CI deterministic/offline: **passed**;
- normalized usage/provider metadata: **passed**.

### Policy and cost

- USD $50/month hard ceiling represented: **passed**;
- expensive execution constrained before interaction: **passed**;
- LLM/tool proposal cannot bypass policy: **passed**.

### Security

- secret redaction test: **passed**;
- no generic secret-listing interface: **passed**;
- privileged tool actions require policy evaluation: **passed**;
- normal CI requires no production credential: **passed**.

### Recovery / developer usability

- documented local setup/checks: **passed**;
- clean migration/test gate: **passed**;
- durable restart/recovery proof: **passed**;
- Phase 0 verification record: **this document**.

## Boundaries Preserved

Phase 0 closeout did **not** introduce:

- Phase 1 conversation API/application loop behavior;
- real Developer Agent execution;
- OpenHands or OpenCode integration;
- autonomous repository modification;
- production GitHub App write automation;
- remote/ephemeral workers;
- AWS Secrets Manager runtime wiring;
- DBOS Cloud/Conductor requirements;
- production deployment;
- passkeys/WebAuthn;
- PWA/mobile UI;
- Web Push;
- real speech-provider calls;
- recurring cloud infrastructure;
- real-provider credentials in CI.

## Next Stage

The approved implementation plan identifies the next stage after Phase 0 as **Phase 1 — working local Manager conversation/planning loop**.

No Phase 1 implementation is started by this closeout record. Phase 0 is deliberately stopped at the durable/provider-neutral foundation boundary.

## Related Documents

- [Overlord — Phase 0 Implementation Plan](/projects/notes/overlord-phase-0-implementation-plan/)
- [Overlord P0.1 — Repository Foundation](/projects/notes/overlord-p0-1-repository-foundation/)
- [Overlord P0.2 — Domain Model and Persistence](/projects/notes/overlord-p0-2-domain-persistence/)
- [Overlord P0.3 — Ports, Fake Adapters, and Planning Contract](/projects/notes/overlord-p0-3-planning-contract/)
- [Overlord P0.4 — Pydantic AI Manager Adapter](/projects/notes/overlord-p0-4-pydantic-ai-adapter/)
- [Overlord P0.5 — DBOS Durable Manager Workflow](/projects/notes/overlord-p0-5-dbos-durable-manager/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: the approved Phase 0 implementation plan; Overlord PR #8; exact PR head `104fde71e6fd697223bc68bc21796030c531d3c2`; permanent PR-head CI run #114; final Phase 0 `main` commit `721de238683686d7e0bd810bb8c8fa856d66d913`; exact post-merge permanent CI run #115; final workflow tree; Phase 0 domain/policy/ports/security/architecture tests; repository documentation and ADR set; and the previously merged P0.1–P0.5 implementation evidence.
- Verified by: High Director.
- Verification scope: repository/installability, canonical state boundaries, persistence/migrations, model/runtime replaceability, durable restart/resume, policy/approval/tool enforcement, budget semantics, secret redaction, architecture direction, documentation completeness, offline acceptance, and exact post-merge source verification.
