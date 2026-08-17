---
title: Overlord Phase 3 — GitHub Policy Broker
summary: First Phase 3 slice establishing typed GitHub lifecycle operations, deterministic fake behavior, and fail-closed policy-driven merge authority.
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
  - opencode
  - merge
---

# Overlord Phase 3 — GitHub Policy Broker

## Outcome

The first Phase 3 GitHub lifecycle slice is complete.

Overlord now has a typed GitHub lifecycle port, a deterministic fake GitHub adapter, and an application-level `GitHubBroker` that centralizes repository write and merge authority behind explicit policy.

The owner delegated routine merge authority to policy rather than requiring a manual owner confirmation for every merge. This does **not** mean unconditional auto-merge: the broker fails closed whenever required evidence is missing, stale, ambiguous, or unsuccessful.

OpenCode remains behind `DeveloperAgentPort` and receives no GitHub API credential or direct merge authority.

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

Both accepted CI gates included Compose validation, PostgreSQL startup/readiness, locked dependency synchronization, Ruff lint, Ruff format check, strict mypy, Alembic upgrade, and full pytest.

## GitHub Lifecycle Contract

`GitHubPort` now models typed operations for:

```text
repository planning context
file read
code search
branch creation
exact-head file commits
pull-request create/update/read
check inspection
exact-head merge execution
```

Git/GitHub remain canonical for repository, commit, pull-request, and check state. Runtime-native Developer state is not promoted to canonical repository state.

## Policy-Driven Merge Authority

`GitHubPolicy` explicitly defines:

```text
allowed_repositories
allowed_base_branches
required_checks
require_required_checks
merge_method
```

`GitHubBroker` allows a merge only when all applicable policy evidence passes. Current fail-closed checks include:

```text
repository is allowlisted
pull request state is open
pull request is not draft
mergeability is explicitly true
base branch is allowlisted
pull request head SHA matches the expected head SHA
required-check policy is non-empty when required
required checks are present
required checks are completed
required checks concluded successfully
```

A missing check, pending check, failed check, unknown mergeability, draft PR, disallowed base, non-allowlisted repository, or stale expected SHA blocks the merge and does not call the adapter merge operation.

The adapter merge call repeats the expected PR head SHA, preserving the exact-head boundary between policy assessment and write execution.

## Deterministic Offline Adapter

`FakeGitHubAdapter` implements the lifecycle contract for normal CI without contacting GitHub.

It models:

- branch creation and branch-head identity;
- exact-head commit rejection;
- deterministic commit identities;
- file reads/search;
- PR creation/update/read;
- check state;
- PR-head advancement after a branch commit;
- exact-head merge execution;
- merge-call evidence for policy tests.

This lets Phase 3 policy behavior remain fully testable without repository credentials.

## Explicit Security Boundary

OpenCode does not receive GitHub installation tokens, personal access tokens, App private keys, or merge authority.

The intended product path is:

```text
OpenCode / DeveloperAgentPort
        |
        v
Overlord application/control plane
        |
        v
GitHubBroker policy decision
        |
        v
GitHubPort adapter
        |
        v
GitHub
```

Repository writes therefore remain centrally governable even though the owner does not need to approve every routine merge manually.

## Scope Exclusions

This slice intentionally did **not** add:

- a real GitHub App adapter;
- GitHub credentials;
- deployed product GitHub writes;
- a PostgreSQL schema migration;
- application dependency or lockfile changes;
- durable GitHub-operation persistence;
- new risk-classification records;
- direct OpenCode GitHub credentials;
- provider/model changes;
- paid model execution;
- Phase 4 remote worker infrastructure.

## Next Phase 3 Slice

The next slice may implement the real GitHub App adapter and durable GitHub operation/audit references behind the accepted `GitHubPort` / `GitHubBroker` boundary.

Implementation can remain credential-free in normal CI. Any future GitHub App private key or installation credential must be configured through an external secret/runtime mechanism and must never be committed to source or pasted into chat.

## Verification Record

- Last verified: `2026-08-17`.
- Verified against: owner delegated merge-policy authority; source PR #25 final head `3665ce71d4de64df9fb16779999ef9ceaceedfde`; PR CI #325 run `32056774141`; source main `c8c606ca292fe0f336b1643166f4c5442ee1519e`; post-merge CI #326 run `32056948790`.
- Verified by: High Director.
- Verification scope: typed lifecycle port, fake adapter behavior, allowlist/base/head/check/mergeability merge policy, exact-head merge execution, no direct OpenCode GitHub credentials, no schema/dependency/paid-runtime expansion.
