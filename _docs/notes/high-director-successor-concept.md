---
title: High Director Successor — Initial System Concept
summary: Working concept for a mobile-first, provider-neutral manager-agent system that supervises parallel developer agents while keeping infrastructure, tools, history, and control under the owner's control.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
owner: High Director
order: 115
permalink: /projects/notes/high-director-successor-concept/
tags:
  - high-director
  - successor
  - agent-platform
  - llm
  - mobile
  - voice
  - github
---

# High Director Successor — Initial System Concept

## Purpose

This note captures the initial product and architecture concept for a successor to the current High Director agent.

The successor should preserve the useful functions of High Director while removing dependence on OpenAI's Custom GPT/custom-agent product as the application platform. The intended result is an independently controlled agent system in which the replaceable component is the large-language-model provider rather than the surrounding application, tool access, data, process flow, or user experience.

This is a **design concept**, not an implementation decision. Hosting, framework, model providers, agent runtime, mobile implementation, speech services, and detailed persistence technology remain open until current options are researched and compared.

## Desired User Experience

The primary interface should behave like a persistent conversation with a high-level **Manager Agent**.

The owner should be able to use that conversation from a phone in either of two ways:

1. **Text mode** — a conventional chat interface similar to the current High Director conversation.
2. **Voice mode** — press a button, speak naturally, have speech transcribed into the same manager conversation, and receive short spoken versions of manager updates/questions.

Voice is therefore an interface layer over the same underlying conversation rather than a separate agent or workflow.

The manager should provide concise conversational updates suitable for reading in text. When voice mode is active, it should additionally create a shorter speakable version of each important update or question so the owner can interact without reading long technical output.

Phone support is mandatory. The first implementation may be either a responsive web application/PWA or a native mobile application, provided it is practical to operate from a phone and supports notifications, text chat, microphone input, and spoken responses.

## Core Operating Model

The system should use at least two agent roles.

### Manager Agent

The Manager Agent is the owner's primary interface and the high-level coordinator.

Its responsibilities should include:

- receive ideas, requests, corrections, and decisions through text or voice;
- understand the owner's intended outcome rather than requiring implementation-level instructions;
- identify the relevant repository, system, documentation, history, and current implementation;
- inspect the relevant code/configuration before proposing work;
- identify missing requirements and decisions that genuinely require owner input;
- create an actionable development plan;
- decide how work should be divided into developer-agent tasks;
- generate the task/prompt/context package for each developer agent;
- start and supervise developer-agent work;
- monitor developer-agent responses and tool results;
- evaluate whether a developer can safely continue without owner input;
- provide concise progress summaries to the owner;
- request owner decisions only when they materially affect requirements, architecture, security, cost, access, destructive actions, or other important boundaries;
- continue developer work autonomously when no owner decision is necessary;
- coordinate parallel developer agents where useful;
- maintain durable project/task/conversation state;
- verify that work is tested, reviewed, merged/deployed, or otherwise completed according to the applicable repository/system rules.

The manager is not intended to perform every development step itself. Its primary job is planning, delegation, supervision, decision routing, validation, and communication with the owner.

### Developer Agents

Developer Agents perform the detailed technical work delegated by the Manager Agent.

Typical responsibilities may include:

- repository/code inspection;
- implementation planning at the task level;
- editing code, YAML, infrastructure configuration, documentation, tests, and related assets;
- creating branches and commits;
- opening and updating pull requests;
- running or monitoring CI/workflows;
- diagnosing test/build failures;
- reporting progress, blockers, evidence, and proposed next actions to the Manager Agent.

The system should support multiple developer agents operating concurrently on independent tasks or repositories when that is safe and useful.

Whether developer work is represented internally as persistent conversations, isolated task runs with durable external state, or another execution model remains an open architecture decision. The correct choice should be based on reliability, context management, cost, observability, and provider portability rather than attempting to reproduce current chat behavior unnecessarily.

## Human-in-the-Loop Model

The intended system is **autonomous by default within approved boundaries** and owner-controlled where decisions matter.

The Manager Agent should not stop for routine implementation details that it can safely resolve from source, established standards, tests, or existing architecture.

Examples of work that should normally continue without owner intervention include:

- routine code changes consistent with an approved plan;
- fixing tests or validation failures;
- documentation updates;
- branch/commit/PR operations;
- inspecting logs and source;
- retrying safe/idempotent operations;
- choosing ordinary implementation details where architecture and cost are unchanged.

The manager should stop and request owner input for decisions that materially affect:

- product/function requirements;
- architecture;
- security or permissions;
- credentials/access boundaries;
- recurring or material cost;
- destructive/irreversible operations;
- privacy/data handling;
- external-service commitments;
- ambiguous trade-offs where the owner's preference matters.

The owner should therefore be able to give a high-level request and allow the manager/developer system to progress for extended periods without repeated approval of routine steps.

## Progress and Decision Flow

A desired interaction flow is:

1. The owner speaks or types an idea/request to the Manager Agent.
2. The Manager Agent identifies and inspects the relevant repositories, code, configuration, documentation, and prior project history.
3. The Manager Agent produces a plan and identifies any decisions that genuinely require owner input.
4. Once the plan is sufficiently determined, the Manager Agent prepares a developer-agent task package and starts the appropriate Developer Agent.
5. The Developer Agent performs the detailed work and reports progress/events back to the Manager Agent.
6. The Manager Agent evaluates each update rather than forwarding raw developer output directly.
7. If no owner decision is required, the Manager Agent instructs the Developer Agent to continue.
8. If owner input is required, the Manager Agent sends a concise summary explaining what changed, why a decision is required, available options, and its recommended/default option.
9. The owner responds by text or voice.
10. The Manager Agent incorporates the decision and resumes the developer work.
11. The Manager Agent coordinates validation, PR/merge/deployment or equivalent completion gates.
12. The Manager Agent records the outcome and informs the owner when the task is complete.

## Mobile and Notification Experience

The owner should be able to leave the application while work continues.

When a meaningful event occurs, the system should support a phone notification. Examples include:

- an owner decision is required;
- a developer is blocked;
- validation or deployment failed in a way requiring a decision;
- a major milestone completed;
- the overall task completed.

Routine internal developer messages should not create noisy user notifications.

When the owner opens the app from a notification, the relevant Manager Agent conversation should be immediately available. In voice mode, the manager should be able to speak a compact summary/question and accept a spoken answer.

## Voice Layer

Voice should be optional and layered on top of the text conversation.

Conceptual flow:

```text
Owner speech
  -> speech-to-text
  -> Manager Agent conversation
  -> normal manager reasoning/orchestration
  -> manager text response
  -> voice-summary transformation
  -> text-to-speech
  -> owner
```

The full technical manager message should remain available as text even when a shorter spoken summary is used.

The speech-to-text and text-to-speech technologies are not yet selected. They may be external services or locally/self-hosted components depending on quality, latency, cost, mobile support, privacy, and operational complexity.

## Provider-Neutral LLM Architecture

A core requirement is that the application must **not** be architecturally tied to one LLM vendor.

The system should define its own internal interfaces for at least:

- conversation messages;
- model requests/responses;
- tool calls and tool results;
- structured outputs;
- streaming;
- reasoning/task status metadata where available;
- usage/token/cost accounting;
- retry/error classification;
- model capability declarations.

Provider-specific adapters should translate between this internal contract and individual LLM services.

Conceptually:

```text
Manager / Developer Runtime
          |
          v
Provider-neutral LLM interface
          |
   +------+------+------+
   |             |      |
Provider A   Provider B Provider C
adapter       adapter    adapter
```

Changing model/provider should therefore primarily involve configuration plus the relevant provider adapter, rather than rewriting orchestration, repository access, persistence, notifications, mobile UI, or agent-management logic.

The architecture should also allow different roles to use different models. For example, a high-capability model might be selected for the Manager Agent while lower-cost models handle some developer/review/subtasks, provided quality remains acceptable.

No provider is selected at this stage.

## Tool and Integration Layer

The successor should own its tool/integration architecture rather than depend on a vendor-specific custom-agent tool mechanism.

The desired long-term integration scope includes:

- GitHub;
- AWS;
- Google Workspace;
- Appsmith;
- Power BI;
- Power Automate;
- web research/browsing;
- S3/object storage;
- databases and APIs required by managed repositories/systems;
- future tools added through a stable internal tool interface.

### GitHub

GitHub should be a first-class capability. Subject to the owner's configured security boundaries, the system is intended to support the full range of useful repository operations, including:

- repository/tree/file reads;
- code search;
- branch creation;
- file creation/update/deletion;
- commits;
- pull requests;
- PR review/management;
- workflow inspection;
- workflow dispatch;
- run/job/log/artifact inspection;
- merge operations;
- Actions variables/secrets administration where explicitly permitted;
- other GitHub API capabilities added when required.

The implementation should still apply least-privilege and approval controls at the task/policy layer even if the integration credential has broad technical capability.

## Persistent State and History

All important manager/developer state should be stored under infrastructure controlled by the owner rather than existing only inside an LLM provider's conversation product.

The retained history should include, where appropriate:

- manager conversations;
- owner text/voice transcripts;
- developer-agent tasks/conversations or task-run state;
- plans;
- owner decisions;
- prompts/context packages sent to developer agents;
- tool calls/results or durable references to them;
- repository/branch/PR/workflow identifiers;
- task state and dependencies;
- validation/deployment evidence;
- final outcomes and summaries;
- token/model/cost usage;
- audit/security events.

This history should be searchable and usable as context for future work without requiring the same LLM provider that originally produced it.

The exact database/object-storage/search design remains open.

## Conceptual System Components

From the current requirements, a likely architecture will need these logical components even though technologies are not yet selected:

1. **Mobile/web client** — text chat, microphone control, audio playback, task views, notifications.
2. **Application/API backend** — authenticated interface used by the client.
3. **Conversation service** — persistent owner/manager conversation state.
4. **Manager Agent runtime** — planning, supervision, decision routing, summaries, agent control.
5. **Developer Agent runtime** — task execution and technical work.
6. **Agent/task scheduler** — parallel execution, queues, resumability, cancellation, task dependencies.
7. **LLM gateway/provider-adapter layer** — provider-neutral model interface and usage accounting.
8. **Tool gateway** — GitHub, AWS, Google, Appsmith, web, databases, and future integrations.
9. **Policy/approval layer** — determines which actions can proceed autonomously and which require owner approval.
10. **Persistent state store** — conversations, tasks, decisions, metadata, audit history.
11. **Artifact/log storage** — larger tool results, generated files, transcripts, logs, evidence.
12. **Notification service** — push/update delivery to the phone.
13. **Speech layer** — optional STT/TTS adapters around the manager conversation.
14. **Observability/cost controls** — model usage, failures, tool activity, budgets, latency, and system health.

This logical separation is intentional: the LLM should be a processing dependency, not the platform on which the rest of the system exists.

## Control and Ownership Goal

The preferred end state is that the owner controls:

- application source code;
- orchestration/agent logic;
- system prompts/instructions;
- tool integrations;
- credentials and authorization policy;
- databases/history;
- task state;
- notification behavior;
- mobile/web interface;
- speech integration configuration;
- hosting/infrastructure;
- logs/audit data;
- provider/model routing configuration.

Ideally, the only essential major component outside direct ownership/control is the selected LLM inference service itself. Other external services may still be used where they provide a strong practical advantage, but the architecture should avoid making them irreplaceable where feasible.

## Cost Objective

The intended cost profile is broadly comparable to a normal paid ChatGPT subscription plus modest infrastructure usage rather than an autonomous system that routinely incurs large monthly model bills.

This is a target, not yet a verified estimate.

The design should therefore support:

- model selection by task/role;
- provider switching as prices change;
- token/context controls;
- reusable persistent context rather than repeatedly sending unnecessary history;
- summaries/context compaction;
- configurable concurrency;
- usage and cost accounting by task/model/provider;
- optional monthly/daily budgets or alerts;
- lower-cost models for appropriate subtasks;
- efficient event-driven infrastructure where practical.

Cost must be considered alongside reliability and development quality. The cheapest model is not automatically the appropriate default.

## Security and Access Principles

The system is expected to have powerful development and infrastructure capabilities, so its control plane must be treated as security-sensitive.

Initial design principles are:

- owner-authenticated access to the application;
- credentials stored outside prompts/conversation history;
- provider calls receive only the context required for the task;
- tool execution occurs through controlled integrations rather than giving models raw long-lived credentials;
- explicit audit history for important tool operations;
- policy checks before destructive, security-sensitive, access-control, or cost-significant actions;
- owner approval for material security/access changes;
- separation of tool permissions from model-provider identity;
- ability to revoke/change an LLM provider without replacing tool credentials or infrastructure;
- safe concurrency controls when multiple developer agents operate in parallel.

Detailed identity, authorization, secrets management, sandboxing, network isolation, and repository permission design remains future architecture work.

## Design Principles

The current concept implies these guiding principles:

1. **Provider independence** — no core workflow should depend directly on one vendor's proprietary agent product.
2. **Owner-controlled state** — conversations, decisions, tasks, and history remain in owner-controlled storage.
3. **Manager/developer separation** — high-level planning/supervision is distinct from detailed implementation work.
4. **Autonomy with escalation** — routine work continues automatically; owner decisions are requested only when materially necessary.
5. **Mobile first** — full useful operation must be possible from a phone.
6. **Voice is additive** — text remains canonical; voice is a convenient input/output layer.
7. **Tool portability** — GitHub/AWS/etc. integrations belong to the system, not to the chosen model vendor.
8. **Parallelism with control** — multiple developer agents may run concurrently, with task isolation and manager oversight.
9. **Durable auditability** — the system should explain what agents did, why, with which tools/models, and what the outcome was.
10. **Cost visibility** — model/infrastructure use should be measurable and controllable.
11. **Replaceable components** — model, speech, hosting, notification, and other external providers should be adapter/configuration choices where practical.

## Open Architecture Questions

These decisions should be made only after researching currently available platforms/services:

- self-built agent runtime versus an open/self-hostable orchestration framework;
- persistent developer conversations versus isolated/resumable task executions;
- backend/hosting platform;
- native app versus PWA/responsive web application;
- database and object-storage technologies;
- task queue/scheduler and long-running job model;
- LLM provider gateway design and which providers/models to support first;
- whether one provider-neutral API service already offers sufficient portability without creating excessive lock-in;
- speech-to-text and text-to-speech providers or self-hosted options;
- push-notification technology;
- authentication/identity design;
- secrets management;
- sandboxing/execution environment for code/developer agents;
- GitHub authentication model and permission boundaries;
- observability and cost-control stack;
- how much developer-agent state should be stored verbatim versus summarized/structured;
- context-retrieval/search design for long-term project history.

## Non-Decisions at This Stage

The following are deliberately **not** selected yet:

- LLM vendor/model;
- hosting provider;
- cloud platform;
- agent framework;
- programming language/framework for the application;
- database;
- mobile framework;
- speech provider;
- notification provider;
- GitHub authentication implementation;
- execution sandbox/container platform.

The next phase should research these against the requirements rather than selecting technology first and adapting requirements around it.

## Success Criteria

A successful successor should allow the owner to do something close to this from a phone:

> Describe a development idea by voice or text, let the Manager Agent inspect the real system and plan the work, allow it to start and supervise one or more Developer Agents, receive only meaningful progress/decision updates, answer required questions conversationally, and have the system continue autonomously until the requested work is validated and complete.

It should continue to work if the preferred LLM provider later changes, without rebuilding the surrounding application and integrations.

## Next Safe Action

Research current products, frameworks, model APIs/gateways, agent runtimes, mobile approaches, speech services, persistence options, and hosting approaches that could implement this concept.

The research should compare at least:

- provider portability;
- degree of owner control/self-hostability;
- agent orchestration and long-running/resumable task support;
- tool integration model;
- parallel developer-agent support;
- mobile/voice feasibility;
- security model;
- observability/auditability;
- implementation complexity;
- operating cost at the intended usage level;
- migration/exit risk.

No architecture should be selected until that comparison is complete.

## Related Documents

- [High Director overview](/projects/high-director/)
- [High Director runtime architecture](/projects/high-director/runtime-architecture/)
- [High Director capability/component inventory](/docs/high-director/capability-component-inventory/)
- [High Director security and configuration reference](/projects/high-director/security-configuration-reference/)
- [High Director documentation inventory](/docs/high-director/repository-documentation-inventory/)

## Confidence and Status

- Confidence: `high` for the desired behavior captured from owner requirements; `low` for technology choices because research has not begun.
- Current state: `draft guidance`
- Verification source: owner requirements provided on 2026-08-09 plus current High Director documentation for successor context.

## Verification Record

- Verified against: owner-stated successor requirements in the current design conversation and the current High Director documentation set.
- Verified by: High Director
- Verification scope: desired user experience, manager/developer operating model, autonomy boundary, parallelism, GitHub/tool scope, provider portability, mobile/voice requirements, persistent history, and cost objective.
- Unverified areas: technology availability, provider capabilities/pricing, implementation complexity, and actual operating cost; these require current-market research.
