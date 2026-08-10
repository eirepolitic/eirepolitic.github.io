---
title: High Director Successor Research 01 — Agent Runtime and Control Plane
summary: First-pass research comparing current agent runtimes, durable workflow engines, coding-agent servers, model gateways, and GitHub authentication patterns for the High Director successor.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
owner: High Director
order: 116
permalink: /projects/notes/high-director-successor-research-01/
tags:
  - high-director
  - successor
  - research
  - pydantic-ai
  - dbos
  - openhands
  - langgraph
  - temporal
  - litellm
  - github
---

# High Director Successor Research 01 — Agent Runtime and Control Plane

## Purpose

This is the first current-market research pass for the planned High Director successor. It focuses on the architecture-critical layer:

- Manager Agent runtime;
- multi-agent orchestration;
- durable/resumable execution;
- Developer Agent execution;
- provider-neutral model access;
- GitHub authentication/tool access;
- parallel work and human approval boundaries.

Mobile UI, voice, notifications, hosting, detailed persistence/search, and exact operating cost will be researched in later passes.

This document records a **working hypothesis**, not a final architecture decision.

## Current Working Hypothesis

The strongest MVP architecture found in this pass is:

```text
Mobile/PWA client
      |
      v
Owner-controlled API/backend
      |
      v
Manager Agent
Pydantic AI
      |
      +-----------------------+
      |                       |
      v                       v
DBOS durable workflows     Tool gateway
      |                       |
      |                       +--> GitHub App
      |                       +--> AWS / Google / web / future tools
      |
      +--> OpenHands Agent Server(s)
      |       |
      |       +--> isolated Developer Agent workspaces
      |
      +--> provider-neutral Pydantic AI model interface
              |
              +--> OpenAI
              +--> Anthropic
              +--> Google
              +--> Bedrock
              +--> OpenRouter / compatible services
              +--> future providers
```

**Working recommendation:** prototype the Manager Agent/control plane with **Pydantic AI + DBOS**, use **OpenHands Software Agent SDK / Agent Server** as the first Developer Agent runtime, and use a **GitHub App** rather than a long-lived personal token as the primary GitHub integration.

Do **not** introduce Temporal or LiteLLM in the first prototype unless a concrete requirement appears that Pydantic AI + DBOS cannot satisfy cleanly.

## Why Pydantic AI Is the Current Manager-Agent Front-Runner

Pydantic AI currently provides several capabilities that directly match the successor requirements.

### Provider portability

The official model/provider documentation exposes integrations for OpenAI, Anthropic, Google, xAI, AWS Bedrock, Cerebras, Cohere, Groq, Hugging Face, Mistral, Ollama, OpenRouter, and other provider interfaces. This means the application does not need to be built around a single model vendor's agent product.

Source: [Pydantic AI — Models overview](https://pydantic.dev/docs/ai/models/overview/).

### Multi-agent control

Pydantic AI documents multiple levels of multi-agent architecture:

- agent delegation;
- programmatic agent hand-off;
- graph-based multi-agent control;
- deeper autonomous-agent patterns.

Its documented programmatic hand-off pattern is particularly relevant to the desired Manager Agent design because application code can decide which agent runs next rather than allowing one vendor-specific chat product to own the control flow.

Pydantic AI also supports different models for different agents and records usage/cost information across delegated runs. Its `UsageLimits` can place request, token, tool-call, and monetary-cost limits around an agent run.

Source: [Pydantic AI — Multi-Agent Patterns](https://pydantic.dev/docs/ai/guides/multi-agent-applications/).

### Human approval / deferred execution

Pydantic AI supports deferred tool execution, including patterns where a tool call is surfaced for external approval before execution. This is relevant to the owner-approval boundary for destructive, security-sensitive, architecture/cost, or access-control operations.

Source: [Pydantic AI — Deferred Tools](https://pydantic.dev/docs/ai/tools-toolsets/deferred-tools/).

### Durable execution integrations

Pydantic AI explicitly supports durable-agent execution and currently lists official integrations with:

- Temporal;
- DBOS;
- Prefect;
- Restate.

The documentation states that durable agents can preserve progress across API failures, application errors/restarts, and long-running/human-in-the-loop workflows.

Source: [Pydantic AI — Durable Execution](https://pydantic.dev/docs/ai/capabilities/durable_execution/overview/).

### Why this matters

Pydantic AI is currently attractive because it can remain the **agent/model abstraction layer**, while durability, tools, storage, UI, and developer workspaces remain separate infrastructure choices. That is a closer match to the successor's anti-lock-in requirement than using a vendor-owned chat/agent product as the application itself.

## DBOS as the Current MVP Durability Front-Runner

The Manager Agent cannot depend on one HTTP request remaining alive while a developer works. It needs durable task state that can pause for owner input, survive application restarts, queue parallel work, and resume without repeating completed external actions.

DBOS is currently the strongest lightweight option found for an MVP.

### Relevant properties

Official DBOS/Pydantic documentation shows that:

- workflows checkpoint progress to a database;
- interrupted workflows resume from the last completed step;
- external I/O is placed in steps;
- workflow inputs and step outputs are durably stored;
- queues provide database-backed concurrency/rate/priority control;
- DBOS can run in-process as a library;
- SQLite can be used for simple cases and Postgres for the intended durable architecture;
- there is no separate orchestration server required for the open-source Postgres architecture.

Sources:

- [Pydantic AI — DBOS integration](https://pydantic.dev/docs/ai/capabilities/durable_execution/dbos/)
- [DBOS — Workflows](https://docs.dbos.dev/python/tutorials/workflow-tutorial)
- [DBOS — Queues and concurrency](https://docs.dbos.dev/python/tutorials/queue-tutorial)
- [DBOS — Architecture](https://docs.dbos.dev/architecture)

### Why DBOS currently beats Temporal for v1

Temporal is more mature as a general durable-workflow platform and can run workflows for very long periods, including human-in-the-loop workflows that wait without consuming worker compute. However, Temporal introduces a dedicated orchestration service/runtime and additional operational concepts.

For a single-owner system with modest concurrency, DBOS appears capable of providing the needed recovery/queue behavior with fewer moving parts.

Sources:

- [Temporal — Workflows](https://docs.temporal.io/workflows)
- [Temporal — Human-in-the-loop agent](https://docs.temporal.io/ai-cookbook/human-in-the-loop-python)

### Current decision status

- **DBOS:** front-runner for prototype/MVP.
- **Temporal:** retain as an upgrade path if scale, workflow complexity, cross-service orchestration, or operational reliability requirements outgrow DBOS.

## LangGraph as the Main Manager-Runtime Alternative

LangGraph is a strong alternative rather than a rejected option.

Official LangGraph documentation provides:

- durable execution;
- persistence/checkpointing;
- streaming;
- human-in-the-loop interrupts;
- thread-scoped state;
- long-term stores;
- subgraph/subagent patterns;
- parallel subagent calls;
- indefinite pause/resume for human input.

Sources:

- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph subgraphs](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)

### Why it is currently second rather than first

LangGraph provides a very capable orchestration model, but it would make the graph/checkpointer runtime itself a larger part of our application architecture. Pydantic AI currently gives us a simpler model/provider abstraction plus the option to attach DBOS, Temporal, Prefect, or Restate as separate durability layers.

That separation is currently more aligned with the requirement that the LLM/provider layer remain easy to replace and that we own the surrounding application structure.

This is an architectural judgment from the current requirements, not a claim that LangGraph is less capable.

## OpenHands as the Current Developer-Agent Front-Runner

The Developer Agent requirement is substantially different from an ordinary tool-calling assistant. It needs a real workspace, repository/code editing, shell commands, file operations, potentially browser/MCP tools, long-running conversations/tasks, and a programmatic control surface for the Manager Agent.

OpenHands currently matches this unusually well.

### Software Agent SDK

The OpenHands Software Agent SDK exposes a Python API for running agents locally or remotely and includes tools for shell execution, file editing, browser operations, and MCP integrations.

Source: [OpenHands — Software Agent SDK](https://docs.openhands.dev/sdk).

### Agent Server

The Agent Server is especially relevant to the proposed manager/developer architecture. Official documentation describes:

1. a client application that creates and controls conversations;
2. an Agent Server providing HTTP/WebSocket execution;
3. an isolated workspace, which can be local, Docker-based, or remote.

The Manager backend can therefore create Developer Agent conversations, stream their events, inspect progress, send follow-up instructions, and maintain a mapping between our internal task IDs and OpenHands conversation IDs.

Sources:

- [OpenHands — Agent Server overview](https://docs.openhands.dev/sdk/guides/agent-server/overview)
- [OpenHands — Agent Server architecture](https://docs.openhands.dev/sdk/arch/agent-server)

### Isolation

OpenHands documents Docker workspaces and other remote sandbox options. This maps well to parallel Developer Agents because each development task can receive an isolated workspace rather than allowing multiple agents to modify one shared checkout.

Source: [OpenHands — Docker Sandbox](https://docs.openhands.dev/sdk/guides/agent-server/docker-sandbox).

### Conversation continuity

The Agent Server can retain server-side conversation state and workspace/tool context across follow-up requests. The API also supports conversation operations such as forking and condensation.

Sources:

- [OpenHands — OpenAI-compatible Agent Server endpoint](https://docs.openhands.dev/sdk/guides/agent-server/openai-gateway)
- [OpenHands — Fork a conversation](https://docs.openhands.dev/sdk/guides/convo-fork)
- [OpenHands — Condense conversation](https://docs.openhands.dev/sdk/guides/agent-server/api-reference/conversations/condense-conversation)

### Current design implication

The first prototype should **not build a coding agent from zero**. Instead, it should test whether OpenHands can act as a replaceable Developer Agent service behind our own Manager/control-plane API.

The Manager must own task state and approval policy. OpenHands should own developer-workspace execution, not the overall product architecture.

## Developer Conversation Model — Initial Research Direction

The earlier design left open whether developer agents should be persistent chats or isolated task runs.

Current research suggests a hybrid model:

- our system owns a durable **Development Task** record;
- each task may have one current Developer Agent conversation ID;
- the OpenHands conversation can remain persistent while useful because it retains workspace/tool context;
- task plans, decisions, milestones, PR/workflow references, and important summaries are persisted separately in our database;
- if a conversation becomes too large, fails, or needs a different provider/runtime, the Manager can create a replacement conversation from the durable task state;
- the OpenHands conversation is therefore an execution context, **not** the source of truth for the project.

This achieves the convenience of persistent developer context without making a third-party conversation format the durable application state.

## GitHub Authentication — GitHub App Is the Current Front-Runner

The successor is intended to have broad GitHub capability, but the model itself should never hold a long-lived personal access token.

A GitHub App currently appears to be the correct primary automation identity.

GitHub's official documentation states that installation access tokens are appropriate when an app acts on its own behalf, are limited by the permissions granted to the app/installation, can access REST and GraphQL APIs, and are generated from the app's installation identity.

Sources:

- [GitHub — About creating GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps)
- [GitHub — Authenticate as an installation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation)
- [GitHub — Generate installation access token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)

### Proposed pattern

```text
Manager/Developer Agent
        |
        v
Internal GitHub tool service
        |
        v
GitHub App private credential
        |
        v
short-lived installation access token
        |
        v
GitHub REST / GraphQL APIs
```

The tool service should generate/use installation tokens and expose policy-filtered tool operations to agents. Raw app credentials should never be placed into an LLM prompt or Developer Agent workspace unless a future architecture decision explicitly requires it.

### Broad permission versus autonomous policy

The GitHub App may eventually be granted broad technical permissions to support the owner's desired capabilities, but our internal policy layer should still decide which operations may proceed autonomously. Integration capability and agent authorization are separate concerns.

## LiteLLM — Useful, but Probably Not Required in v1

LiteLLM can provide a centralized LLM proxy/router with capabilities such as:

- cross-provider routing/load balancing;
- retries/cooldowns/fallbacks;
- spend tracking;
- provider/model budgets;
- model failover.

Sources:

- [LiteLLM — Router](https://docs.litellm.ai/docs/routing)
- [LiteLLM — Provider failover](https://docs.litellm.ai/docs/proxy/reliability)
- [LiteLLM — Spend tracking](https://docs.litellm.ai/docs/proxy/cost_tracking)
- [LiteLLM — Budget routing](https://docs.litellm.ai/docs/proxy/provider_budget_routing)

However, Pydantic AI already provides model/provider abstractions and can directly use multiple providers. Running LiteLLM immediately would add another service, configuration layer, database/Redis requirements for some production features, and another failure surface.

### Current recommendation

Start without LiteLLM. Design the internal LLM service boundary so LiteLLM can be inserted later if centralized provider failover, shared quotas, routing, or spend enforcement becomes valuable.

## First-Pass Option Ranking

| Concern | Current first choice | Main alternative | Current reason |
|---|---|---|---|
| Manager Agent/model abstraction | Pydantic AI | LangGraph/LangChain | Strong provider abstraction, multi-agent patterns, structured tools, usage limits, durable-engine choices |
| Durable task orchestration | DBOS + Postgres | Temporal | Lower operational complexity for expected initial scale |
| Developer Agent runtime | OpenHands Agent Server | custom coding agent / other harness | Programmatic conversation control plus isolated developer workspaces already exists |
| GitHub automation identity | GitHub App | PAT/OAuth-user token | Short-lived installation tokens and explicit app permissions fit autonomous service identity |
| LLM gateway | Direct Pydantic AI providers initially | LiteLLM | Fewer components in v1; LiteLLM remains a clean later routing layer |
| Long-term workflow upgrade | Temporal | DBOS remains | Temporal if durability/scale/distributed orchestration requirements justify added infrastructure |

## Proposed MVP Control Flow

```text
1. Owner creates message in mobile/web client.
2. Backend stores the message in owner-controlled conversation storage.
3. DBOS starts/resumes the Manager workflow.
4. Pydantic AI Manager Agent reads relevant durable state and repository context.
5. Manager either:
   a. answers owner,
   b. creates a plan,
   c. requests an approval/decision,
   d. creates one or more Development Tasks.
6. Development Tasks enter a DBOS queue with concurrency limits.
7. Each task provisions/connects to an isolated OpenHands Agent Server workspace.
8. Manager starts the OpenHands conversation with a generated task/context package.
9. OpenHands streams developer events/results back to the backend.
10. Backend persists raw event references plus structured task milestones.
11. Manager evaluates developer updates.
12. If safe to continue, Manager sends the next developer instruction automatically.
13. If owner input is required, Manager workflow pauses durably and triggers a notification.
14. Owner replies by text or voice; the same workflow resumes.
15. GitHub operations go through the internal GitHub App tool service and policy layer.
16. Manager closes the task only after applicable tests/PR/workflow/deployment gates pass.
```

## What This Architecture Keeps Under Owner Control

If implemented as currently hypothesized, the owner controls:

- Manager prompts/instructions and application code;
- durable workflow/process logic;
- Manager/Developer task state;
- primary database;
- Developer workspace orchestration;
- GitHub App and other tool integrations;
- approval/policy rules;
- model/provider configuration;
- conversation history and summaries;
- notifications/UI/voice integration;
- hosting and observability.

The LLM inference provider remains replaceable rather than owning the entire agent application.

OpenHands, Pydantic AI, and DBOS are software dependencies and should therefore also be treated as replaceable components behind internal interfaces rather than allowed to become the only representation of application state.

## Risks Identified in This Pass

### Framework churn

Agent frameworks are evolving rapidly. Internal interfaces should prevent Pydantic AI, DBOS, or OpenHands object models from becoming the permanent storage schema.

### OpenHands resource usage

Parallel isolated developer workspaces can consume substantially more CPU/RAM/storage than the Manager API itself. Hosting/cost research must model idle and concurrent-workspace behavior before architecture selection.

### Agent permissions

A broadly permissioned GitHub App is powerful. Internal approval/policy controls, audit logs, branch protections, and isolation must be designed before enabling sensitive operations autonomously.

### Durable side effects

Durable workflow systems require external side effects to be designed carefully so retries do not duplicate commits, PRs, notifications, or infrastructure changes. Every tool operation needs an idempotency/retry policy.

### Model portability is not perfect interchangeability

Providers expose different tool-call formats, context windows, reasoning controls, structured-output behavior, caching, and model-specific capabilities. The adapter layer should define a lowest-common contract plus explicit capability flags rather than pretending every model is identical.

## Research Not Yet Completed

The following areas still need current-market research before architecture selection:

1. hosting topology and real monthly cost at expected usage;
2. OpenHands compute/resource requirements and practical concurrent-worker hosting;
3. mobile/PWA framework and push-notification support;
4. speech-to-text and text-to-speech options/cost/latency;
5. database/search/context-memory architecture;
6. authentication for the owner-facing application;
7. secrets management;
8. sandbox/network-security model for Developer Agents;
9. AWS/Google/Appsmith/Power BI/Power Automate tool adapters;
10. observability and audit stack;
11. current LLM provider/model capabilities and API pricing;
12. whether the Manager Agent should use the same or a different provider/model from Developer Agents;
13. cost controls and provider-routing rules;
14. backup/export/disaster recovery;
15. comparison with any current integrated products that could reduce build effort without creating unacceptable lock-in.

## Next Research Pass

Research **deployment and cost architecture**, especially the compute implications of OpenHands workspaces. Compare practical self-hosting designs such as:

- one small always-on control-plane host + on-demand developer workers;
- AWS event-driven/container/VM options;
- inexpensive VPS/control-plane hosting plus separate ephemeral worker compute;
- managed sandbox providers where they materially reduce complexity;
- Postgres hosting options;
- expected idle cost versus one/two/several concurrent Developer Agents.

Then research the mobile/PWA + notifications + voice layer against the resulting backend topology.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [High Director overview](/projects/high-director/)
- [High Director runtime architecture](/projects/high-director/runtime-architecture/)

## Verification Record

- Last verified: `2026-08-09`
- Verified against: current official Pydantic AI, DBOS, LangGraph/LangChain, OpenHands, Temporal, LiteLLM, and GitHub documentation.
- Verified by: High Director
- Verification scope: manager-agent abstractions, multi-agent patterns, durable execution, developer-agent server/workspace capabilities, model-routing alternatives, and GitHub application authentication.
- Unverified areas: real-world resource consumption, actual operating cost, mobile/voice design, exact production security topology, and implementation fit under a prototype; these require subsequent research/testing.
