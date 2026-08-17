---
title: Overlord Phase 3 — GitHub Policy Broker
summary: First Phase 3 slice establishing a typed GitHub lifecycle contract, deterministic fake adapter, and fail-closed policy-driven merge broker without real GitHub credentials.
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
  - opencode
  - policy
  - merge
---

# Overlord Phase 3 — GitHub Policy Broker

## Outcome

The first Phase 3 source slice is accepted. Overlord now has a typed asynchronous GitHub lifecycle port, a deterministic fake implementation for normal/offline CI, and an application-level `GitHubBroker` that centralizes repository write and merge authority.

The selected OpenCode Developer runtime does **not** receive GitHub credentials and does not create branches, commits, pull requests, or merges directly.

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

Both permanent CI gates included Compose validation, PostgreSQL startup/readiness, locked dependency synchronization, Ruff lint, Ruff format check, strict mypy, Alembic upgrade, and full pytest.

No PostgreSQL migration or application dependency/lock change was introduced by this slice.

## GitHub Lifecycle Contract

`GitHubPort` preserves the earlier read-only repository-planning context and now also models typed async lifecycle operations for:

```text
repository file reads
repository code search
branch creation
exact-head file commits
pull-request create/update/read
check inspection
exact-head pull-request merge
```

Git/GitHub remain canonical for repository, branch, commit, PR, and workflow/check state.

Branch commits and merges carry an `expected_head_sha`. Stale repository state is rejected instead of being silently overwritten or merged.

## Policy-Driven Merge Authority

The owner explicitly removed the requirement for manual owner approval on each merge. Merge authority is therefore policy-driven rather than click-gated.

`GitHubBroker` fails closed unless the evidence satisfies policy. Current policy dimensions include:

```text
allowed_repositories
allowed_base_branches
required_checks
require_required_checks
merge_method
```

Merge evaluation blocks when any relevant condition is missing or unsafe, including:

- repository not allowlisted;
- PR not open;
- draft PR;
- mergeability not explicitly confirmed;
- disallowed base branch;
- PR head different from the expected SHA;
- required-check policy empty when checks are required;
- required check absent;
- required check incomplete;
- required check failed.

The final adapter merge call repeats the exact expected head SHA, preserving protection against a repository race after policy evaluation.

## Deterministic Fake Adapter

`FakeGitHubAdapter` implements the lifecycle contract entirely in memory for normal CI.

It supports deterministic branch/commit/PR/check/merge transitions and retains the existing repository-context planning behavior.

Important properties include:

- idempotent branch creation when the requested branch already exists at the same source SHA;
- stale-head rejection for file commits;
- deterministic commit/merge SHA generation;
- open-PR reuse for the same head/base pair;
- PR head refresh when the corresponding branch receives a new commit;
- exact-head rejection during merge;
- recorded merge calls for policy assertions.

## Test Boundary

Focused Phase 3 unit tests prove:

- the broker can perform an allowlisted branch → commit → PR → green-check → merge lifecycle;
- a failed required check prevents merge;
- an unallowlisted repository cannot enter the write lifecycle;
- a stale branch head prevents a commit;
- a missing required check prevents merge.

Normal CI remains provider/runtime/GitHub-write offline.

## Credential Boundary

This slice requires no GitHub App private key, installation token, personal access token, or other GitHub write credential.

OpenCode remains behind `DeveloperAgentPort`. Privileged repository operations are owned by the Overlord control plane through `GitHubPort` and `GitHubBroker`.

No credential should be supplied to OpenCode itself.

## Deferred Phase 3 Work

This first slice deliberately does **not** add:

- a real GitHub App adapter;
- GitHub App credential setup;
- product-facing GitHub write endpoints;
- canonical durable GitHub operation references/audit persistence;
- remote worker provisioning;
- Phase 4 paid/remote worker infrastructure.

The next Phase 3 slice should add durable GitHub operation/audit references in PostgreSQL before a real credentialed adapter is activated.

## Verification Record

- Last verified: `2026-08-17`.
- Verified against: source PR #25 exact final head `3665ce71d4de64df9fb16779999ef9ceaceedfde`; permanent CI #325 run `32056774141`; merged source main `c8c606ca292fe0f336b1643166f4c5442ee1519e`; post-merge CI #326 run `32056948790`; source architecture/development notes; `GitHubPort`; `FakeGitHubAdapter`; `GitHubBroker`; focused Phase 3 tests.
- Verified by: High Director.
