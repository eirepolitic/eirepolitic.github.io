---
title: Overlord Phase 4 — Local Developer Environments
summary: Current Phase 4 MVP architecture replacing mandatory remote Developer worker VMs with disposable local Docker Developer Environments on the single Overlord host.
section: notes
doc_type: note
status: active
created: 2026-08-18
updated: 2026-08-18
last_verified: 2026-08-18
owner: High Director
order: 149
permalink: /projects/notes/overlord-phase-4-local-developer-environments/
tags:
  - overlord
  - phase-4
  - docker
  - opencode
  - digitalocean
  - developer-environment
---

# Overlord Phase 4 — Local Developer Environments

## Decision

The Phase 4 MVP execution architecture is revised.

Remote disposable Developer VMs are no longer an MVP requirement. The default Developer execution path is a disposable local Docker container/workspace on the same always-on host as the Overlord control plane.

LLM inference remains external. Overlord/OpenCode call configured external model APIs; the DigitalOcean host is not expected to run the language models themselves.

This decision supersedes the mandatory-remote-worker portions of the earlier consolidated design, hosting research implementation sequence, and Phase 4 provider-benchmark note. Those documents remain historical records rather than being rewritten as if the earlier decision never existed.

## MVP Host

DigitalOcean remains the preferred MVP hosting target from the original hosting research.

The initial deployment is one always-on server containing:

```text
DigitalOcean VM
├── Overlord Manager / control plane
├── DBOS / workflow services
├── PostgreSQL
├── Docker
└── disposable Developer Environments
    ├── task A -> local container/workspace -> OpenCode -> external LLM API
    └── task B -> local container/workspace -> OpenCode -> external LLM API
```

The initial concurrency target may be one active coding task at a time. One active coding task maps to one isolated Developer Environment.

## Execution Modes

The execution architecture should support a small provider-neutral mode boundary:

```text
LOCAL_CONTAINER  default MVP path
REMOTE           future optional scaling path
```

`LOCAL_CONTAINER` means the Developer Environment is created and destroyed through the local Docker daemon on the Overlord host.

`REMOTE` is deliberately deferred. It may later provision a remote VM/container host while preserving the same higher-level Developer execution contract.

Remote execution becomes justified only by evidence such as:

- large builds or test suites;
- resource-heavy Docker workloads;
- multiple parallel Developer Agents;
- stronger isolation requirements;
- local server CPU, memory, disk, or I/O limits.

## DeveloperAgentPort

The existing `DeveloperAgentPort` remains valid and provider/runtime neutral.

It describes the coding-agent conversation boundary:

- create session;
- send message;
- read session status;
- cancel session.

It does not provision infrastructure and does not require a remote VM. No redesign of this port is required for the MVP hosting change.

OpenCode remains the owner-selected default Developer runtime behind `DeveloperAgentPort`.

## Developer Environment Boundary

Phase 4 should add only the environment lifecycle abstraction needed around the existing Developer runtime.

Conceptually:

```text
DeveloperExecutionService
  -> DeveloperEnvironmentPort
       -> LocalDockerDeveloperEnvironmentAdapter   [MVP]
       -> RemoteDeveloperEnvironmentAdapter        [future]
  -> DeveloperAgentPort
       -> OpenCodeDeveloperAgentAdapter
```

The environment boundary owns disposable execution context lifecycle, not LLM reasoning and not GitHub mutation authority.

Expected environment responsibilities include:

- create an isolated task workspace/container;
- expose the OpenCode endpoint required by the existing adapter;
- enforce bounded CPU/memory/process/container privileges;
- mount only task-specific workspace/state required for execution;
- report readiness/health;
- terminate and remove the environment after task completion/cancellation/failure;
- avoid giving the Developer container unrestricted host access.

The exact port shape should remain minimal and be driven by the first local Docker implementation rather than by speculative remote-provider requirements.

## Security and Authority Boundaries

The Developer Environment is disposable compute, not the privileged repository mutation authority.

OpenCode and its container must not receive:

- the GitHub App private key;
- GitHub installation tokens;
- broad AWS permissions;
- unrestricted Docker-host control;
- unrestricted host filesystem access.

The previously accepted GitHub path remains:

```text
application service
  -> GitHubBroker
  -> policy / durable audit evidence
  -> GitHubPort
  -> GitHubAppAdapter
  -> short-lived installation token
  -> GitHub API
```

Developer output that requires a repository write must continue through that broker/audit boundary rather than by giving OpenCode direct GitHub credentials.

## AWS Boundary

The completed Phase 3 AWS/GitHub work remains valid:

```text
region:       us-east-2
secret:       overlord/production/github-app
IAM policy:   OverlordProductionGitHubAppSecretRead
```

The IAM policy remains intentionally unattached. The control plane is not being moved to EC2 merely to obtain an instance role.

After the DigitalOcean runtime exists, configure a narrowly scoped AWS identity/credential mechanism for that control plane to read only the required Secrets Manager value. Do not expose that AWS identity to Developer containers.

## Existing Source Impact Review

Current source inspection found no mandatory remote-worker dependency in the core Developer execution boundary.

Keep unchanged:

- `DeveloperAgentPort`;
- `DeveloperExecutionService` orchestration semantics;
- OpenCode as the default Developer runtime;
- `GitHubBroker`;
- `GitHubPort` and `GitHubAppAdapter`;
- AWS Secrets Manager adapter;
- durable audit and exact-head GitHub controls.

Needs Phase 4 work:

- add the minimal Developer Environment lifecycle port/model;
- add a local Docker-backed adapter;
- integrate environment lifecycle with Developer execution without coupling `DeveloperAgentPort` to Docker;
- add cleanup/recovery tests for completed, failed, cancelled, and abandoned environments;
- add resource/isolation defaults appropriate to the selected DigitalOcean VM.

Deferred rather than deleted:

- production remote-worker provider abstraction;
- DigitalOcean/Fly disposable worker lifecycle integration;
- two-worker remote concurrency testing;
- provider API credentials for remote workers.

## Existing Hosting Benchmark Harness

Source PR #28 added a paid DigitalOcean-versus-Fly remote-worker benchmark harness. It remains valid as optional future scaling research, but it is no longer on the MVP critical path.

Do not create the DigitalOcean benchmark API token requested by the old Step 6. Do not run the paid remote-worker benchmark as the next implementation step.

If remote execution becomes necessary later, the harness can be updated/reused to gather evidence before selecting the remote provider adapter.

## Revised Phase 4 Sequence

The active implementation sequence is now:

1. record this architecture revision;
2. preserve `DeveloperAgentPort` neutrality;
3. implement the minimal Developer Environment lifecycle boundary;
4. implement `LOCAL_CONTAINER` through Docker on the Overlord host;
5. prove OpenCode task startup/readiness/cleanup in that disposable environment;
6. plan and provision one always-on DigitalOcean Overlord VM;
7. configure only the hosted runtime settings/credentials required by the control plane;
8. configure narrowly scoped AWS Secrets Manager access from that runtime;
9. perform a controlled live GitHub App smoke test through the existing broker/audit path;
10. add `REMOTE` only when workload evidence justifies it.

## Cost/Function Rationale

The revision removes MVP infrastructure that does not directly contribute LLM intelligence. Model inference is external, so a remote VM per coding task primarily buys additional compute/isolation rather than model capability.

A single adequately sized DigitalOcean host plus disposable local containers should therefore be tested first. This reduces provider APIs, worker credentials, network orchestration, VM startup latency, and idle/fragmented compute cost while preserving a replaceable future scaling path.

## Verification Record

- Last verified: `2026-08-18`.
- Verified against: current `Overlord/main`; `DeveloperAgentPort`; `DeveloperExecutionService`; OpenCode adapter; Phase 3 GitHub/AWS acceptance; Phase 4 hosting-provider benchmark harness; original hosting research and consolidated design.
- Verified by: High Director.
