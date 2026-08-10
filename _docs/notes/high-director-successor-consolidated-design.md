---
title: High Director Successor — Consolidated Architecture and MVP Proposal
summary: Decision-ready architecture and prototype plan synthesizing the initial concept and six research passes for the provider-neutral High Director successor.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
owner: High Director
order: 122
permalink: /projects/notes/high-director-successor-consolidated-design/
tags:
  - high-director
  - successor
  - architecture
  - mvp
  - manager-agent
  - developer-agent
  - provider-neutral
---

# High Director Successor — Consolidated Architecture and MVP Proposal

## Purpose

This document consolidates the initial High Director successor concept and six current-market research passes into one decision-ready architecture and MVP proposal.

It is the handoff point between **research** and **prototype implementation**.

No production infrastructure or application should be created until the material owner decisions near the end of this document are approved.

## Product Goal

The successor should let the owner interact from a phone with one persistent **Manager Agent** by text or optional voice.

The Manager should:

1. receive a high-level request;
2. inspect relevant repositories, code, documentation and project history;
3. create and maintain an actionable plan;
4. identify only the decisions that genuinely require owner input;
5. create one or more Developer Agent tasks;
6. start and supervise those Developer Agents;
7. continue them automatically when no owner decision is required;
8. provide concise owner-facing progress updates rather than raw developer chatter;
9. pause durably and notify the owner when a material decision is required;
10. validate, review, merge/deploy, and close work according to repository/system rules;
11. retain a searchable owner-controlled history of requests, decisions, work, tool calls, costs and results.

The system must continue to function if the preferred LLM provider or Developer Agent implementation later changes.

## Recommended Target Architecture

```text
┌─────────────────────────────────────────────┐
│                OWNER PHONE                  │
│                                             │
│ Installable PWA                             │
│ - text Manager chat                         │
│ - push-to-talk                              │
│ - spoken summaries                          │
│ - Web Push                                  │
│ - passkey authentication                    │
│ - task / decision / result views            │
└──────────────────────┬──────────────────────┘
                       │ HTTPS
                       v
┌─────────────────────────────────────────────┐
│        OWNER-CONTROLLED CONTROL PLANE       │
│                                             │
│ API / authentication                        │
│ Manager Agent — Pydantic AI                 │
│ Durable workflow — DBOS                     │
│ Postgres — canonical state + search         │
│ Policy / approval engine                    │
│ Budget / usage enforcement                  │
│ LLM capability router                       │
│ GitHub / tool credential broker             │
│ Worker lifecycle controller                 │
│ Notification service                        │
│ STT / TTS adapters                          │
│ Audit / backup jobs                         │
└──────────────┬───────────────┬──────────────┘
               │               │
               │               +───────────────> S3-compatible storage
               │                                  artifacts / backups /
               │                                  audit exports
               │
               v
        PRIVATE WORKER NETWORK
               │
       ┌───────┴────────┐
       │                │
       v                v
 ephemeral worker   ephemeral worker
 task / branch A    task / branch B
       │                │
       v                v
 Developer Agent    Developer Agent
 adapter            adapter
       │                │
       +--> OpenHands    +--> OpenHands
       +--> OpenCode     +--> OpenCode
       +--> future ACP   +--> future ACP
```

## Architectural Principle: The Control Plane Is the Product

The most important conclusion from the research is that the product should **not** be an LLM conversation wrapped around tools.

The product is the owner-controlled control plane containing:

- durable project/task state;
- the Manager workflow;
- approval and escalation policy;
- credentials/tool boundaries;
- worker lifecycle;
- model routing;
- notifications;
- history and audit;
- recovery.

LLM models and coding agents are processing engines connected to that control plane.

This reverses the dependency of the current Custom GPT model: the LLM provider is a replaceable dependency rather than the platform that owns the conversation/application.

## Canonical State Ownership

### PostgreSQL

Canonical application state:

- owner identity/device records;
- Manager conversations and messages;
- work requests;
- plans;
- tasks and dependencies;
- task status history;
- Developer Agent run references;
- owner decisions and approvals;
- tool calls/results metadata;
- repository/PR/workflow/deployment references;
- model/provider usage and prices;
- notifications;
- audit/security events;
- searchable summaries.

### Git / GitHub

Canonical source-development state:

- repositories;
- branches;
- commits;
- pull requests;
- workflow runs;
- code/configuration/documentation artifacts.

### Object storage

Larger or append-oriented retained artifacts:

- database backups;
- raw diagnostic/tool payloads where useful;
- worker/test logs;
- optional provider payloads;
- audit exports;
- short-lived voice recordings until transcription;
- other large generated evidence.

### Explicit non-authorities

These must **not** be the only source of important state:

- OpenAI/Anthropic/Google conversation objects;
- OpenHands conversations;
- OpenCode sessions;
- Letta memory;
- Developer Worker filesystems;
- DBOS-specific internal objects without domain records;
- mobile local storage.

## Manager Agent

### Recommended runtime

**Pydantic AI** remains the preferred Manager model/runtime abstraction for the prototype.

Reasons established by Research 01/04:

- broad model-provider support;
- structured tools/outputs;
- multi-agent/delegation patterns;
- deferred/approval tool patterns;
- usage/cost controls;
- official durable-execution integrations;
- clean separation between model abstraction and workflow engine.

### Manager responsibilities

The Manager should own reasoning and communication, not unrestricted execution authority.

The Manager may:

- interpret requests;
- inspect allowed context/tools;
- build/revise plans;
- create Development Tasks;
- select a permitted model capability tier;
- evaluate Developer Agent events/results;
- decide whether the Developer should continue;
- propose tool actions;
- summarize progress;
- identify when owner input is necessary.

The control plane, not the model, enforces:

- permissions;
- spending limits;
- worker concurrency;
- destructive-action rules;
- secret release;
- credential scope;
- approval requirements;
- idempotency/retry behavior.

## Durable Workflow and Autonomy

### Recommended prototype engine

**DBOS + Postgres**.

DBOS should provide:

- resumable Manager/task workflows;
- durable pauses while awaiting owner decisions;
- queues;
- concurrency limits;
- retry boundaries;
- recovery after application restart.

Do not make DBOS Conductor/Console required for the product. Our own database/domain UI remains authoritative.

### Upgrade path

Retain Temporal as a future option if workflow scale/distribution/operational requirements outgrow DBOS.

The domain model should be sufficiently independent that replacing the workflow engine does not require rebuilding conversation/task history.

## Developer Agent Design

### Internal contract

Every coding runtime should implement one normalized Developer Agent adapter.

Minimum conceptual API:

```text
create_task()
send_instruction()
stream_events()
get_status()
request_summary()
cancel()
resume()
get_usage()
finalize()
```

The internal Development Task ID remains separate from the runtime's conversation/session ID.

### Prototype benchmark

Benchmark two implementations first:

1. **OpenHands** — baseline/front-runner.
2. **OpenCode** — strongest challenger.

Optional later candidates:

- Goose;
- Letta Code;
- another ACP-compatible coding agent.

### OpenHands role

OpenHands is currently the strongest initial candidate because of its Agent Server, isolated execution patterns, MCP support, subagents, parallel execution, provider flexibility and Agent Canvas.

Agent Canvas may be reused as an **engineering/debugging console** for Developer Agents. It should not replace the owner-facing Manager PWA or canonical state.

### OpenCode role

OpenCode should be benchmarked because it has:

- a headless HTTP/OpenAPI server;
- multi-session/subagent support;
- broad model support;
- MCP;
- tool permission configuration;
- ACP.

If it proves materially lighter/cheaper while matching OpenHands reliability, it may become the default Developer runtime.

## Worker Infrastructure

### Recommended pattern

One small always-on control-plane VM plus disposable Developer Worker VMs.

Each Development Task should initially receive its own worker and repository branch/worktree context.

```text
Task A -> Worker A -> branch A
Task B -> Worker B -> branch B
```

### Current hosting hypothesis

**DigitalOcean first prototype**, with Fly.io and Hetzner retained as benchmark/alternative hosts.

Reasons:

- simple API-controlled VM lifecycle;
- cloud-init/user-data;
- private VPC networking;
- predictable per-second pricing;
- current 2-vCPU/4-GB worker size aligns with documented OpenHands single-user VM guidance;
- relatively simple implementation compared with a more managed container platform.

AWS ECS/Fargate remains a security/operations alternative but currently costs materially more per active worker hour in the investigated configuration.

### Worker controls

Hard application controls:

- maximum concurrent workers;
- maximum worker lifetime;
- idle timeout;
- automatic terminal-state destruction;
- orphan detection/cleanup;
- per-task and monthly worker-hour budgets;
- no destruction while unpersisted work remains only on the worker.

## Model Architecture

### Capability profiles

Do not hard-code one provider or model.

Use configuration-defined profiles:

```text
EFFICIENT
BALANCED
FRONTIER
```

### Intended routing

**Manager**

- default: BALANCED;
- cheap secondary transformations: EFFICIENT;
- difficult architecture/security/failure escalation: FRONTIER.

**Developer**

- simple/low-risk: EFFICIENT or BALANCED;
- normal coding/debugging: BALANCED;
- difficult/failed/high-risk task: FRONTIER escalation;
- optionally independent reviewer on important changes.

### Initial benchmark providers

Current research supports testing candidates from:

- OpenAI;
- Anthropic;
- Google.

The benchmark—not provider reputation—should determine defaults for each capability tier.

### Cost controls

Hard controls should include:

- per-call token limits;
- per-task LLM budget;
- per-agent budget;
- daily/monthly budget;
- frontier escalation limit;
- retry limits;
- context-growth alerts;
- cached/uncached usage accounting;
- provider tool/search charges;
- projected monthly spend.

## Context and Memory

### Initial retrieval strategy

1. relational/structured SQL;
2. PostgreSQL full-text search;
3. add `pgvector` only if semantic-retrieval testing proves a material benefit.

Do not deploy a separate vector database in v1.

### Context builder

Each model request receives selected context rather than full history:

- current work request;
- plan;
- task/dependencies;
- decisions/constraints;
- repository rules/current refs;
- recent messages;
- selected summaries/events;
- exact source files/excerpts needed now.

Large model context windows are a safety valve, not the persistence architecture.

## Tools and Permissions

### GitHub

Use a **GitHub App** as the principal automation identity.

The application may ultimately have broad technical GitHub permissions as requested, but each task receives policy-filtered access.

The GitHub App private key stays on the control plane. Workers receive short-lived installation access only when direct Git access is required; high-value API actions should normally be brokered centrally.

### Other tools

Long-term integrations include:

- AWS;
- Google Workspace;
- Appsmith;
- Power BI;
- Power Automate;
- web research;
- S3/databases;
- future APIs.

Do not implement every integration in the first prototype.

### MCP

Use MCP where practical as the reusable tool/resource surface, with our policy broker remaining authoritative.

### ACP

Use ACP as an optional coding-agent interoperability adapter, especially for OpenCode and future coding harnesses.

Do not store canonical task state as ACP session state.

### A2A

Defer A2A until there is a genuinely independently operated remote agent service. Design task/event concepts so an adapter can be added later.

## Mobile Client

### Recommended MVP

Installable **PWA**.

Capabilities:

- Manager chat;
- push-to-talk;
- spoken Manager summaries;
- active work list;
- decision-required cards;
- completed work/results;
- notifications;
- settings/security/budget views.

### Authentication

Use WebAuthn/passkeys, with a deliberate recovery mechanism and re-authentication for high-value approvals where appropriate.

### Notifications

Deterministic application-level severity:

```text
INFO                 -> timeline only
MILESTONE            -> optional push
OWNER_INPUT_REQUIRED -> push + badge
SECURITY_COST_ALERT  -> high-priority acknowledgement
TASK_COMPLETE        -> push unless disabled
```

### Voice

Push-to-talk initially:

```text
record -> STT -> canonical text Manager message
Manager text response -> short speakable summary -> TTS
```

STT and TTS have separate provider adapters.

Do not build continuous realtime voice in v1.

## Security Boundary

### Long-lived credentials

Long-lived credentials live only in the control-plane secret boundary.

Developer Workers should not receive:

- GitHub App private key;
- hosting/cloud control credential;
- database admin credential;
- long-lived LLM keys where avoidable;
- master backup/encryption keys.

### Worker credentials

Prefer:

- one-time/short-lived worker bootstrap token;
- short-lived GitHub installation token scoped to task/repository;
- task-scoped service tokens;
- central privileged tool calls.

### LLM key isolation test

One unresolved prototype requirement is verifying whether OpenHands/OpenCode repository commands can access the runtime's provider credentials.

If separation is inadequate, introduce a central LLM gateway/proxy for Developer Workers so they receive a gateway credential rather than the upstream provider key.

This is the strongest current reason LiteLLM might become necessary despite not being required for the Manager layer.

## Secrets Strategy

Research does not justify deploying a full self-hosted secrets platform in the first prototype.

Prototype with one of:

- a small managed secret store such as AWS Secrets Manager; or
- tightly controlled SOPS-encrypted bootstrap configuration.

OpenBao remains a future option when dynamic leases/multi-host secret operations justify running another security-critical service.

**Recommended prototype default:** managed secret storage for long-lived control-plane credentials, because the small recurring cost is preferable to making a prototype self-hosted vault an additional high-risk service.

This is a security/cost choice requiring owner approval before implementation.

## Backup and Recovery

Prototype baseline:

- nightly custom-format `pg_dump`;
- versioned S3-compatible backup prefix;
- lifecycle retention;
- checksums/backup job records;
- regular `pg_restore` test to disposable database;
- Git/GitHub as code authority;
- infrastructure/bootstrap code version-controlled.

Later:

- WAL/PITR if recovery-point needs justify it;
- optional Object Lock for protected backup/audit prefixes.

Acceptance requires an actual recovery drill from a fresh VM.

## Proposed MVP Scope

The MVP should prove the unique product loop rather than implement every future integration.

### Included

1. Owner PWA with text Manager chat.
2. Passkey login.
3. Push-to-talk transcription and optional spoken summary.
4. Web Push notifications.
5. Durable Manager conversation/state.
6. One Manager Agent using provider-neutral model configuration.
7. Repository discovery/inspection through GitHub.
8. Plan creation and owner-decision escalation.
9. Durable Development Tasks.
10. Maximum two concurrent disposable Developer Workers.
11. OpenHands Developer adapter.
12. OpenCode Developer adapter for benchmark/comparison.
13. GitHub branch/file/PR/workflow/merge tool broker.
14. Test/validation/run monitoring.
15. Automatic Manager continuation when no owner input is required.
16. Owner-required decision pause/resume.
17. Model/worker/token/cost accounting.
18. Postgres full-text history search.
19. Backups and recovery test.
20. Audit/event timeline.

### Deferred from MVP

- Appsmith integration;
- Google Workspace integration;
- Power BI/Power Automate integration;
- broad AWS infrastructure modification beyond what is required to host/test the platform;
- A2A remote-agent federation;
- dedicated vector database;
- native mobile application;
- continuous realtime voice;
- OpenBao;
- Temporal;
- Kubernetes;
- complex multi-user/organization tenancy;
- production autoscaling beyond simple worker lifecycle;
- fully automated deployment to every existing repository/system.

These remain planned extension points, not rejected requirements.

## Prototype Phases

### Phase 0 — Repository and contracts

Create successor source repository and define:

- domain models;
- Developer Agent interface;
- model capability profile;
- tool/policy interface;
- event/audit model;
- configuration structure;
- local development environment.

No cloud execution required yet.

### Phase 1 — Local control-plane spine

Implement:

- FastAPI or equivalent Python API;
- Postgres;
- DBOS;
- basic Manager Agent;
- Manager text chat;
- work requests/plans/tasks;
- local GitHub read tools;
- durable pause/resume test.

### Phase 2 — Developer Agent benchmark harness

Implement identical adapters/tasks for:

- OpenHands;
- OpenCode.

Benchmark representative repository tasks and select initial default while preserving both adapters where practical.

### Phase 3 — GitHub development lifecycle

Implement GitHub App and broker:

- branch creation;
- reads/search;
- file changes;
- PR creation/update;
- workflow status/log inspection;
- merge subject to policy;
- durable references/audit.

### Phase 4 — Ephemeral remote workers

Provision private disposable workers through the chosen host and prove:

- startup/bootstrap;
- isolated repository task;
- short-lived credentials;
- event streaming;
- cleanup;
- restart/recovery;
- two-worker parallelism;
- no orphan workers.

### Phase 5 — Owner mobile experience

Implement:

- installable PWA;
- passkeys;
- Web Push;
- task/decision screens;
- push-to-talk STT;
- TTS summaries.

### Phase 6 — Security/recovery/cost gate

Prove:

- secret isolation;
- worker credential boundaries;
- database restore;
- control-plane rebuild;
- audit exports;
- hard budgets;
- model switching;
- Developer runtime switching.

### Phase 7 — Real repository pilot

Use one low-risk repository/change workflow with explicit owner approval before expanding to broader autonomous access.

## Acceptance Tests

The MVP should not be considered successful until it demonstrates all of these.

### Provider replacement

- continue the same Manager task using a different LLM provider from durable state;
- run comparable Developer tasks using at least two model providers;
- no migration of the core database/tool configuration required.

### Developer runtime replacement

- start equivalent test tasks through OpenHands and OpenCode adapters;
- replace a failed Developer session using durable task state;
- core task/history remains understandable after runtime replacement.

### Autonomy

- Manager delegates work and continues Developer without owner intervention for routine steps;
- Manager pauses only at a configured decision boundary;
- owner response resumes the exact durable workflow.

### Parallel work

- two independent Development Tasks run concurrently without workspace/branch collision;
- Manager accurately reports each status.

### GitHub lifecycle

- inspect repository;
- create branch;
- make/test change;
- open PR;
- monitor checks;
- fix validation failure;
- merge only under configured policy;
- persist exact evidence.

### Mobile

- install PWA on owner's phone;
- receive decision-required push while app closed;
- deep-link to task;
- answer by text and voice;
- play spoken summary.

### Recovery

- destroy/rebuild control-plane VM and restore state;
- continue an unfinished task after restore;
- destroy a Developer Worker without losing canonical work state.

### Security

- worker cannot read long-lived control-plane credentials;
- worker cannot connect directly to Postgres;
- another worker's workspace is unreachable;
- sensitive tool calls are rejected or approval-gated according to policy.

### Cost

- all LLM calls and worker hours attributed to task/model/provider;
- hard task/monthly budget prevents overrun;
- no idle/orphan Developer Worker remains billable after task completion.

## First-Pass Cost Envelope

The infrastructure research indicates that a lightweight implementation can keep fixed/worker compute modest if Developer Workers are ephemeral.

A representative researched DigitalOcean pattern was approximately:

- small control plane + weekly backup: roughly mid-teens to low-twenties USD/month depending on VM size;
- 100 active 2-vCPU/4-GB Developer Worker hours: roughly $3.57/month at the verified pricing snapshot.

Voice is expected to be a small variable cost relative to model reasoning.

**LLM usage remains the main uncertain expense.** Current model prices vary by more than an order of magnitude, so the MVP must measure real task usage before a credible ongoing monthly total can be promised.

The prototype should therefore have an owner-approved hard spending ceiling rather than assume usage will naturally stay near subscription cost.

## Decisions That Do Not Need Owner Input Yet

Based on the requirements and research, these are safe defaults for prototype design:

- PWA before native app;
- push-to-talk before realtime voice;
- Postgres before separate search/vector services;
- DBOS before Temporal;
- Pydantic AI for Manager abstraction;
- GitHub App rather than permanent PAT as automation identity;
- ephemeral per-task Developer Workers;
- MCP as preferred tool/resource extension interface;
- ACP adapter support for coding agents;
- no A2A requirement in v1;
- benchmark OpenHands against OpenCode;
- capability-tier model routing rather than one permanent LLM;
- preserve all core state outside agent/provider conversations.

## Material Owner Decisions Required Before Implementation

### Decision 1 — Prototype spending ceiling

A hard monthly/prototype budget is required before provisioning infrastructure or running model benchmarks.

**Recommended starting ceiling:** **USD $50/month total for the prototype**, divided internally between infrastructure and LLM/voice usage, with no automatic increase.

Reason: it is close enough to the desired subscription-style budget to force cost-efficient design while leaving enough room to collect real model/worker measurements.

If this ceiling proves too low to run a meaningful benchmark, the system should stop and present measured evidence before requesting an increase.

### Decision 2 — MVP integration scope

**Recommended:** first MVP can modify/test GitHub repositories and monitor GitHub Actions, but does not yet receive general-purpose AWS/Google/Appsmith/Power BI/Power Automate modification capability.

Those integrations remain in the architecture and are added after the core Manager/Developer/security model is proven.

Reason: GitHub alone is sufficient to prove the defining development loop while limiting credential/blast-radius complexity.

### Decision 3 — Prototype long-lived secret storage

**Recommended:** use AWS Secrets Manager for the small initial set of long-lived control-plane credentials, while keeping secrets behind an internal interface so SOPS/OpenBao/another store can replace it later.

Reason: safer initial operations than introducing a self-operated vault; the expected small number of secrets makes the recurring cost modest.

This creates a managed AWS dependency for secret storage, although the account/configuration remains owner-controlled.

### Decision 4 — Successor project name/repository name

A stable source repository should be created before Phase 0.

No name is selected in this research. The architecture should not depend on a branding/name decision.

## Decisions Deferred Until Prototype Evidence

Do not ask the owner to choose these by preference before testing:

- OpenHands versus OpenCode as default Developer Agent;
- DigitalOcean versus Fly/Hetzner long-term host;
- exact Manager/Developer LLM provider/model;
- STT/TTS provider;
- whether `pgvector` adds useful retrieval quality;
- whether a Developer LLM proxy such as LiteLLM is required for secret isolation;
- whether a native/Capacitor mobile wrapper is needed;
- whether OpenBao/Temporal/Kubernetes are ever justified.

Use measured prototype evidence first.

## Recommended Immediate Next Action

After the owner reviews/approves the material decisions above, create a **Phase 0 implementation plan** only.

That plan should define:

- repository name and initial file structure;
- local development stack;
- domain schema v1;
- interfaces/adapters;
- security boundaries;
- test strategy;
- branch/PR/documentation discipline;
- exact Phase 0 acceptance criteria.

Do not provision recurring cloud infrastructure until the local control-plane contracts and budget/security policy are reviewed.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)
- [Research 03 — Mobile, Notifications, Authentication, and Voice](/projects/notes/high-director-successor-research-03/)
- [Research 04 — LLM Provider Strategy and Cost](/projects/notes/high-director-successor-research-04/)
- [Research 05 — Persistent State, Memory, Backups, and Security](/projects/notes/high-director-successor-research-05/)
- [Research 06 — Build vs Adopt and Interoperability Boundaries](/projects/notes/high-director-successor-research-06/)

## Verification Record

- Last verified: `2026-08-09`
- Verified against: the published initial concept and Research 01–06, each based on current first-party project/provider documentation and current pricing evidence at its verification date.
- Verified by: High Director
- Verification scope: consolidated product flow, state ownership, Manager/Developer separation, runtime/hosting/mobile/model/security/tool boundaries, MVP scope, implementation phases, acceptance tests, cost uncertainty, and owner-decision boundary.
- Unverified areas: benchmark results, real task token use, worker utilization/startup latency, real-device PWA behavior, coding-runtime credential isolation, and recovery timings; these require the proposed prototype.
