---
title: Overlord Phase 2 — OpenCode Default Developer Runtime Selection
summary: Owner-approved selection of OpenCode as Overlord's default Developer runtime after repeated benchmark evidence and exact-SHA source acceptance.
section: notes
doc_type: note
status: active
created: 2026-08-17
updated: 2026-08-17
last_verified: 2026-08-17
owner: High Director
order: 144
permalink: /projects/notes/overlord-phase-2-opencode-runtime-selection/
tags:
  - overlord
  - phase-2
  - developer-agent
  - opencode
  - runtime-selection
  - architecture
---

# Overlord Phase 2 — OpenCode Default Developer Runtime Selection

## Outcome

Following the completed repeated benchmark evidence, the owner explicitly selected **OpenCode** as Overlord's default Developer runtime.

The selection is implemented behind the existing `DeveloperAgentPort` boundary. This does not make a hosted provider/model implicit and does not introduce Phase 3 GitHub write/merge brokering.

## Evidence Basis

The accepted repeated benchmark evidence contained nine real comparison trials across the canonical corpus:

```text
python-off-by-one:      3 accepted trials
python-config-feature:  3 accepted trials
python-slug-refactor:   3 accepted trials
```

Both OpenHands and OpenCode completed and passed validation in 9/9 accepted trials.

OpenCode was selected because it had the lower overall median duration and lower accepted reported cost, with the same direction of advantage on all three corpus cases.

Published benchmark evidence:

- [Repeated Developer Benchmark Results](/projects/notes/overlord-phase-2-repeated-benchmark-results/)
- [Repeated Benchmark Case Selection](/projects/notes/overlord-phase-2-repeated-benchmark-case-selection/)
- [Bounded Benchmark Health Probes](/projects/notes/overlord-phase-2-benchmark-health-probe-timeouts/)

## Source Implementation

Source PR `#24` — `feat: select OpenCode as default Developer runtime` — implemented the owner decision.

Accepted source evidence:

```text
exact final PR head:       103c1823d5d82b4b5c671ead8c927f8af006c842
PR permanent CI:           #284
PR CI run ID:              31924686470
PR CI conclusion:          success
merged source main:        ebc9af5135456e822d55aac06048b1dffe7326cb
post-merge CI:             #285
post-merge CI run ID:      31924773334
post-merge CI conclusion:  success
```

Both permanent CI gates included:

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

## Selected Runtime Boundary

`Settings` now identifies:

```text
OVERLORD_DEVELOPER_RUNTIME=opencode
```

The API composition root resolves OpenCode as the selected Developer runtime.

However, the real adapter is constructed only when provider and model are explicitly configured together. Supported compatibility names include:

```text
OVERLORD_DEVELOPER_PROVIDER
OVERLORD_DEVELOPER_MODEL
```

with compatibility aliases for the earlier `_ID` spellings.

If provider/model are not both configured, Developer execution remains unavailable and the API continues to return `503` rather than inheriting an implicit OpenCode server default.

This preserves a deliberate separation between:

1. **runtime selection** — OpenCode;
2. **provider/model selection** — environment-specific and explicit;
3. **provider credentials** — external secret/runtime configuration;
4. **GitHub product write/merge brokering** — deferred to Phase 3.

## Composition and Test Boundary

Explicitly injected Developer adapters continue to override the selected composition-root adapter. This keeps normal CI and offline tests deterministic without starting OpenCode or calling hosted coding models.

The selection did not move canonical application state into the runtime. PostgreSQL remains canonical for Overlord state, Git/GitHub remain canonical for repository state, and runtime-native session/status information remains external evidence/reference data.

## No Architecture Expansion

This selection slice did **not** introduce:

- a PostgreSQL schema migration;
- an application dependency or lockfile change;
- a production provider/model default;
- automatic runtime/model spending logic;
- GitHub product write/merge behavior;
- automatic PR merge authority;
- Manager dispatch into arbitrary remote workers;
- Phase 4 remote/paid worker infrastructure.

## Benchmark Workflow State

The real benchmark workflow remains outside normal product execution.

After completion of the repeated benchmark phase:

```text
real benchmark workflow:               inactive/disabled
OVERLORD_BENCHMARK_AUTHORIZATION_ID:   UNARMED
OVERLORD_BENCHMARK_RUN_CONFIRMATION:   DISABLED
further paid benchmark runs:           not authorized
```

The OpenCode selection does not authorize additional benchmark spend.

## Next Architecture Checkpoint

Phase 2 runtime evaluation and selection are complete.

The next implementation phase can build product execution around the selected OpenCode adapter while retaining `DeveloperAgentPort` as the boundary.

Phase 3 GitHub write/merge brokering remains a separately controlled capability and should be designed/implemented explicitly rather than inferred from runtime selection.

## Verification Record

- Last verified: `2026-08-17`.
- Verified against: owner runtime-selection decision; repeated benchmark results record; source PR #24 exact final head `103c1823d5d82b4b5c671ead8c927f8af006c842`; permanent CI #284 run `31924686470`; merged source main `ebc9af5135456e822d55aac06048b1dffe7326cb`; post-merge CI #285 run `31924773334`.
- Verified by: High Director.
- Verification scope: owner selection, exact-SHA source acceptance, composition-root runtime selection, explicit provider/model boundary, offline-test injection behavior, no-schema/no-dependency change, and deferred Phase 3 GitHub write boundary.
