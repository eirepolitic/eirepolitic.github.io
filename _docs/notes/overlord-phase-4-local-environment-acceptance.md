---
title: Overlord Phase 4 — Local Developer Environment Acceptance
summary: Acceptance record for the provider-neutral Developer Environment lifecycle and local Docker implementation.
section: notes
doc_type: note
status: active
created: 2026-08-18
updated: 2026-08-18
last_verified: 2026-08-18
owner: High Director
order: 150
permalink: /projects/notes/overlord-phase-4-local-environment-acceptance/
tags:
  - overlord
  - phase-4
  - docker
  - opencode
  - developer-environment
---

# Overlord Phase 4 — Local Developer Environment Acceptance

## Outcome

The first implementation slice of the revised Phase 4 architecture is accepted.

Source PR `#29` added a provider-neutral Developer Environment lifecycle boundary and the MVP local Docker implementation without changing `DeveloperAgentPort` or the accepted OpenCode runtime selection.

```text
final PR head:       dcb92f91349102e90359ee53dbde385ddd4d87a2
PR CI:               #352 / run 32216726291 / success
merged source main:  9baaa154585ace87ba9fc436f70f48eff38d175a
post-merge CI:       #353 / run 32217088422 / success
```

## Accepted Boundary

`DeveloperEnvironmentPort` owns disposable execution-context lifecycle. It is separate from `DeveloperAgentPort`, which continues to own the coding-agent conversation/runtime contract.

Execution placement is represented as:

```text
LOCAL_CONTAINER  default MVP mode
REMOTE           reserved future scaling mode
```

No production remote-worker adapter was added.

## Local Docker Adapter

`LocalDockerDeveloperEnvironmentAdapter` creates one task-scoped OpenCode container and returns its loopback runtime endpoint.

The accepted defaults include:

- task workspace as the only explicit host mount;
- no Docker socket mount into OpenCode;
- random loopback-only publication of the OpenCode server port;
- dropped Linux capabilities;
- `no-new-privileges`;
- bounded CPU, memory, and PID count;
- cleanup if runtime readiness fails;
- explicit destroy lifecycle;
- `LOCAL_CONTAINER` as the application configuration default.

OpenCode still uses external LLM provider APIs. The host does not run the LLM itself.

## Authority Boundary

This slice does not give Developer containers the GitHub App private key, GitHub installation tokens, AWS credentials, or GitHub mutation authority.

The accepted privileged repository path remains `GitHubBroker -> GitHubPort -> GitHubAppAdapter`, including exact-head controls and durable audit evidence.

## Deployment Direction

The next source slice prepares the single-host MVP runtime:

```text
one DigitalOcean Ubuntu VM
  -> Overlord / DBOS control plane
  -> PostgreSQL
  -> Docker daemon
  -> disposable local Developer containers
```

The control plane may own Docker lifecycle authority. OpenCode containers must not inherit that authority.

The earlier paid remote-worker provider benchmark remains deferred scaling research and is not required before the MVP host is provisioned.

## Verification Record

- Last verified: `2026-08-18`.
- Verified against: source PR #29, exact PR head `dcb92f91349102e90359ee53dbde385ddd4d87a2`, PR CI #352 run `32216726291`, merged source main `9baaa154585ace87ba9fc436f70f48eff38d175a`, post-merge CI #353 run `32217088422`.
- Verified by: High Director.
