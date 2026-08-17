---
title: Overlord Phase 3 — GitHub Policy Broker
summary: First Phase 3 source slice establishing typed GitHub lifecycle operations, deterministic fake behavior, and fail-closed policy-driven merge authority.
section: notes
doc_type: note
status: active
created: 2026-08-17
updated: 2026-08-17
last_verified: 2026-08-17
owner: High Director
order: 145
permalink: /projects/notes/overlord-phase-3-github-policy-broker/
tags:
  - overlord
  - phase-3
  - github
  - policy
  - broker
  - merge
---

# Overlord Phase 3 — GitHub Policy Broker

## Outcome

The first Phase 3 source slice is complete. Overlord now has a typed GitHub lifecycle boundary and an application-level policy broker that can make fail-closed merge decisions without giving the selected OpenCode Developer runtime direct GitHub API authority.

This slice remains offline/fake-only. It does **not** configure a real GitHub App credential and does not perform product repository writes.

## Source Acceptance

Source PR `#25` — `feat: add Phase 3 GitHub policy broker`:

```text
exact final PR head:       3665ce71d4de64df9fb16779999ef9ceaceedfde
PR permanent CI:           #325
PR CI run ID:              32056774141
PR CI conclusion:          success
merged source main:        c8c606ca292fe0f336b1643166f4c5442ee1519e
post-merge CI:             #326
post-merge CI run ID:      32056948790
post-merge CI conclusion:  success
```

Both acceptance runs passed the permanent gates:

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

## GitHub Lifecycle Port

`GitHubPort` now covers the repository lifecycle required by the control plane while retaining the earlier planning-context operation.

The typed async surface includes:

- repository planning context;
- file reads;
- code search;
- branch creation;
- exact-head file commits;
- pull-request creation and update;
- pull-request inspection;
- check inspection;
- exact-head pull-request merge.

Runtime credentials never cross this port.

## Deterministic Fake Adapter

`FakeGitHubAdapter` implements the lifecycle without network access.

It models:

- branch identity and idempotent creation;
- deterministic commit SHAs;
- exact expected-head protection before commits;
- file create/update/delete behavior;
- open PR identity and updates;
- check results keyed by ref;
- exact-head merge protection;
- merge-method recording;
- deterministic merge SHAs.

Normal CI therefore exercises the GitHub lifecycle and policy logic without GitHub credentials or product writes.

## Policy-Driven Merge Authority

`GitHubBroker` owns GitHub write/merge authority. OpenCode remains behind `DeveloperAgentPort` and receives no direct GitHub API credential.

`GitHubPolicy` can constrain:

```text
allowed_repositories
allowed_base_branches
required_checks
require_required_checks
merge_method
```

A merge decision fails closed unless all configured evidence is acceptable.

The broker blocks merge when any relevant condition fails, including:

- repository outside the allowlist;
- PR not open;
- draft PR;
- mergeability not confirmed true;
- disallowed base branch;
- exact expected head SHA mismatch;
- empty required-check policy when required;
- missing required check;
- incomplete required check;
- failed required check.

When policy passes, the broker repeats the exact expected head SHA into the merge call. The default merge method is `squash`.

## Owner Authority Decision

The owner delegated routine merge decisions to Overlord rather than requiring manual confirmation for every merge.

Therefore Phase 3 uses **policy-driven automatic merge authority**. This is not unrestricted authority: missing, stale, unknown, or failed evidence blocks the merge.

Repository scope remains explicit allowlist-only.

## Boundaries Preserved

This slice does **not** introduce:

- a real GitHub App adapter;
- GitHub App credentials;
- product repository writes;
- a PostgreSQL schema migration;
- application dependency/lock changes;
- a model/provider change;
- additional paid benchmark/model execution;
- Phase 4 remote worker infrastructure.

Git/GitHub remain canonical for repository, branch, PR, check, and merge state. PostgreSQL remains canonical for Overlord application state.

## Next Phase 3 Slice

The safest next source slice is durable GitHub operation/audit persistence before enabling a real GitHub adapter.

That slice should record durable references to branch/commit/PR/check/merge operations and policy decisions in PostgreSQL, using Alembic for any schema additions. After the persistence/audit contract is accepted, a real GitHub App adapter can be implemented behind `GitHubPort` and wired at a separate credential checkpoint.

## Verification Record

- Last verified: `2026-08-17`.
- Verified against: source PR #25 final head `3665ce71d4de64df9fb16779999ef9ceaceedfde`; CI #325 run `32056774141`; merged source main `c8c606ca292fe0f336b1643166f4c5442ee1519e`; post-merge CI #326 run `32056948790`.
- Verified by: High Director.
- Verification scope: typed lifecycle port, deterministic fake adapter, exact-head protections, repository allowlist, required-check merge policy, owner-delegated policy-driven merge authority, and absence of real credentials/product writes.
