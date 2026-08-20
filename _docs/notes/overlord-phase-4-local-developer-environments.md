---
title: Overlord Phase 4 — Local Developer Environments
summary: Current Phase 4 MVP architecture replacing mandatory remote Developer worker VMs with disposable local Docker Developer Environments on the single Overlord host.
section: notes
doc_type: note
status: active
created: 2026-08-18
updated: 2026-08-20
last_verified: 2026-08-20
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

`LOCAL_CONTAINER` means the Developer Environment is created and destroyed through the local Docker daemon on the Overlord host. The current configuration string is `local_container`.

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
DeveloperEnvironmentExecutionService
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

## Implemented local execution path

The local MVP path is now implemented and live-tested.

Accepted composition:

```text
DeveloperEnvironmentExecutionService
-> LocalDockerDeveloperEnvironmentAdapter
-> task-scoped Docker container
-> OpenCode serve
-> OpenCodeDeveloperAgentAdapter
-> external LLM API
-> status / usage / summary
-> container destroy in finally
```

The pinned Developer image is `overlord-developer:1.18.16`. A task workspace is mounted at `/workspace`, OpenCode port `4096` is published only to a random host loopback port, and the container is started with bounded memory/CPU/PID limits, `no-new-privileges`, and all Linux capabilities dropped.

OpenCode readiness is not inferred from a TCP accept alone. `LocalDockerDeveloperEnvironmentAdapter` polls `GET /global/health` until OpenCode returns HTTP 200 with `healthy: true`, preventing task dispatch during the runtime's HTTP startup window.

`OpenCodeDeveloperAgentAdapter.create_task()` creates the session and dispatches the initial task prompt. Composition must not call `send_instruction()` with the same initial description afterward, because that would duplicate LLM work and token cost.

For OpenCode's aggregate session status endpoint, idle sessions may be absent from the returned map. The adapter therefore normalizes an absent entry to `idle` rather than reporting `unknown` after a synchronous prompt has completed.

## Live acceptance evidence — 2026-08-20

The production path was accepted on `overlord-prod-01` using accepted `Overlord/main` release `caa854725c07814dc095d0350d947f86193ae5e2`.

The bounded smoke test used:

```text
execution mode:  local_container
image:           overlord-developer:1.18.16
provider:        openai
model:           gpt-5.6-luna
```

The task created a temporary workspace containing `SMOKE.txt`, instructed the Developer to inspect it without modifying files, and requested one short confirmation sentence.

Accepted result:

```text
DEVELOPER_SMOKE_STATUS=idle
DEVELOPER_SMOKE_INPUT_TOKENS=9
DEVELOPER_SMOKE_OUTPUT_TOKENS=73
DEVELOPER_SMOKE_SUMMARY=Workspace is accessible, and `SMOKE.txt` was inspected successfully.
```

Container cleanup was verified after the run: no `overlord-developer-live-smoke` container remained. The Overlord service remained healthy and ready.

Only `OPENAI_API_KEY` was injected into the Developer container for the live test. The container did not receive AWS credentials, GitHub App credentials, a GitHub installation token, the Docker socket, or unrestricted host filesystem access.

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

A narrowly scoped AWS identity is now configured on the DigitalOcean control plane, and the live `AwsSecretsManagerSecretStore` path successfully read the required GitHub App secret. This does not change the rule that AWS credentials must not enter Developer containers.

The control plane is not being moved to EC2 merely to obtain an instance role.

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

Completed Phase 4 work:

- minimal Developer Environment lifecycle port/model;
- local Docker-backed adapter;
- `DeveloperEnvironmentExecutionService` composition around the existing Developer runtime;
- cleanup on success/failure through `finally`;
- bounded local resource/isolation defaults;
- OpenCode HTTP health readiness;
- production OpenCode/OpenAI smoke acceptance.

Still required in the active plan:

- controlled live GitHub App smoke through `GitHubBroker` and durable audit;
- deeper DBOS/durable workflow integration;
- Manager/control-plane Developer task lifecycle integration;
- additional recovery coverage where justified by durable workflow behavior.

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

Completed:

1. record the architecture revision;
2. preserve `DeveloperAgentPort` neutrality;
3. implement the minimal Developer Environment lifecycle boundary;
4. implement `LOCAL_CONTAINER` through Docker on the Overlord host;
5. prove OpenCode task startup/readiness/cleanup in that disposable environment;
6. provision the always-on DigitalOcean Overlord VM;
7. configure the hosted runtime settings/credentials required by the control plane;
8. configure and prove narrowly scoped AWS Secrets Manager access from that runtime;
9. prove the bounded live local Developer/OpenCode/OpenAI path.

Next:

10. perform a controlled live GitHub App smoke test through the existing broker/audit path;
11. continue DBOS/durable workflow and Manager task-lifecycle integration;
12. add `REMOTE` only when workload evidence justifies it.

## Cost/Function Rationale

The revision removes MVP infrastructure that does not directly contribute LLM intelligence. Model inference is external, so a remote VM per coding task primarily buys additional compute/isolation rather than model capability.

A single adequately sized DigitalOcean host plus disposable local containers should therefore be tested first. This reduces provider APIs, worker credentials, network orchestration, VM startup latency, and idle/fragmented compute cost while preserving a replaceable future scaling path.

The live acceptance result supports this MVP choice: the production host successfully created an isolated local Developer container, ran OpenCode against an external OpenAI model, returned a bounded result, and removed the container afterward without introducing a remote worker VM.

## Verification Record

- Last verified: `2026-08-20`.
- Verified against: accepted `Overlord/main` release `caa854725c07814dc095d0350d947f86193ae5e2`; live `overlord-prod-01`; `DeveloperAgentPort`; `DeveloperEnvironmentExecutionService`; `LocalDockerDeveloperEnvironmentAdapter`; `OpenCodeDeveloperAgentAdapter`; Phase 3 GitHub/AWS acceptance; original hosting research and consolidated design.
- Live evidence: status `idle`; 9 input tokens; 73 output tokens; workspace confirmation returned; disposable container cleanup confirmed; Overlord health/readiness remained good.
- Verified by: High Director.
