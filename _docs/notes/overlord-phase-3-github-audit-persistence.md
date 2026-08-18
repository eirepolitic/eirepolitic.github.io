---
title: Overlord Phase 3 — GitHub Audit Persistence
summary: Second Phase 3 slice persisting correlated GitHub lifecycle and merge-policy evidence through canonical PostgreSQL audit events before any credentialed GitHub adapter is enabled.
section: notes
doc_type: note
status: active
created: 2026-08-17
updated: 2026-08-17
last_verified: 2026-08-17
owner: High Director
order: 146
permalink: /projects/notes/overlord-phase-3-github-audit-persistence/
tags:
  - overlord
  - phase-3
  - github
  - audit
  - postgresql
  - policy
---

# Overlord Phase 3 — GitHub Audit Persistence

## Outcome

The second Phase 3 source slice is accepted. GitHub lifecycle mutations controlled by `GitHubBroker` now emit correlated durable evidence through the existing canonical PostgreSQL `audit_events` store.

This closes the persistence prerequisite identified by the first Phase 3 slice. A real credentialed GitHub adapter is still not enabled, and OpenCode still receives no GitHub write credentials.

## Source Acceptance

Source PR `#26` — `feat: persist GitHub broker audit evidence`:

```text
exact final PR head:       22813c2b4c1a39d7d5105d92ec12bc4fa7374ad0
PR permanent CI:           #330
PR CI run ID:              32085972802
PR CI conclusion:          success
merged source main:        6f3289545291c2540f67e8174f72cf4861779570
post-merge CI:             #331
post-merge CI run ID:      32086083670
post-merge CI conclusion:  success
```

Both accepted CI gates included Compose validation, PostgreSQL startup/readiness, locked dependency synchronization, Ruff lint, Ruff format check, strict mypy, Alembic upgrade, and full pytest.

No new PostgreSQL table or migration was required because `audit_events` was already the canonical audit persistence boundary.

## Audit Repository Boundary

A minimal `AuditRepositoryPort` now exposes append-only audit persistence to application services. `PlanningRepositoryPort` retains that capability through the shared audit port rather than duplicating a GitHub-specific persistence contract.

`GitHubBroker` requires an audit repository dependency. GitHub write authority therefore remains in the control plane while persistence remains replaceable behind the repository port.

## Correlation Context

`GitHubAuditContext` carries explicit canonical correlation references for broker mutations:

```text
correlation_id
work_request_id
task_id
```

Every persisted broker event uses the same supplied correlation context, allowing GitHub lifecycle evidence to be joined back to canonical Overlord work and task state without making GitHub the application state store.

## Persisted Lifecycle Evidence

The broker records requested/completed lifecycle events around successful writes and records policy evidence for denied or evaluated operations.

Current event families include:

```text
github.policy.denied
github.branch.create.requested
github.branch.create.completed
github.commit_files.requested
github.commit_files.completed
github.pull_request.create.requested
github.pull_request.create.completed
github.pull_request.update.requested
github.pull_request.update.completed
github.merge.evaluated
github.merge.requested
github.merge.completed
```

Persisted payloads retain the repository, branch, exact expected/actual SHAs, pull-request number and state, required-check evidence, merge-policy decision/reasons, merge method, and resulting merge SHA where applicable.

File contents are not copied into audit payloads. Commit requests record file paths and whether each change is an upsert or deletion.

## Fail-Closed Write Ordering

For privileged mutations, the broker persists the requested audit event before invoking the GitHub adapter.

If canonical audit persistence is unavailable, the remote GitHub write is not attempted. This preserves the requirement that privileged repository mutations cannot proceed without durable control-plane evidence.

Completed events are appended only after the adapter returns successfully, preserving the distinction between attempted and completed operations.

## Merge Audit Evidence

`merge_if_allowed` now persists the complete merge evaluation before any merge call, including:

- repository and pull-request references;
- base/head branches;
- actual PR head SHA;
- expected head SHA;
- required check names, states, conclusions, and required flags;
- final allow/deny result;
- explicit denial reasons.

A permitted merge then records both the requested exact-head merge and the completed merge result.

The existing fail-closed policy behavior from the first Phase 3 slice is unchanged.

## Test Boundary

Focused tests prove:

- a normal branch → commit → PR → green-check → merge lifecycle emits the expected correlated audit sequence;
- denied merges persist the evaluated policy result and reasons;
- non-allowlisted writes persist a policy-denial event;
- stale-head commit attempts retain their requested exact-head evidence;
- failure of audit persistence prevents the GitHub adapter write from being called;
- correlated GitHub branch/commit references survive a PostgreSQL transaction boundary and can be read back through `SqlAlchemyRepository`.

Normal CI remains GitHub-write offline through `FakeGitHubAdapter`.

## Credential Boundary

This slice still requires no GitHub App private key, installation token, personal access token, or other GitHub write credential.

OpenCode remains behind `DeveloperAgentPort` and receives no direct repository mutation or merge authority. GitHub write authority remains owned by the Overlord control plane through `GitHubPort` and `GitHubBroker`.

## Remaining Phase 3 Work

This slice deliberately does **not** add:

- a real GitHub App adapter;
- GitHub App credential setup/token exchange;
- product-facing GitHub write endpoints;
- remote worker provisioning;
- Phase 4 paid/remote worker infrastructure.

The persistence prerequisite for a credentialed GitHub adapter is now satisfied. The next Phase 3 implementation slice can address the real control-plane-owned GitHub App adapter and credential boundary while preserving the existing broker, exact-head policy checks, and durable audit path.

## Verification Record

- Last verified: `2026-08-17`.
- Verified against: source PR #26 exact final head `22813c2b4c1a39d7d5105d92ec12bc4fa7374ad0`; permanent CI #330 run `32085972802`; merged source main `6f3289545291c2540f67e8174f72cf4861779570`; post-merge CI #331 run `32086083670`; `AuditRepositoryPort`; `GitHubAuditContext`; `GitHubBroker`; `SqlAlchemyRepository`; focused unit tests; PostgreSQL integration test.
- Verified by: High Director.
