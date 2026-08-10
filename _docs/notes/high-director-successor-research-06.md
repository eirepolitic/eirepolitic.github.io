---
title: High Director Successor Research 06 — Build vs Adopt and Interoperability Boundaries
summary: Research comparing current self-hostable agent platforms and open protocols to decide which successor components should be owned directly and which should be adopted behind replaceable interfaces.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
owner: High Director
order: 121
permalink: /projects/notes/high-director-successor-research-06/
tags:
  - high-director
  - successor
  - research
  - openhands
  - opencode
  - letta
  - goose
  - dify
  - mcp
  - acp
  - a2a
---

# High Director Successor Research 06 — Build vs Adopt and Interoperability Boundaries

## Purpose

This sixth research pass asks which parts of the planned High Director successor should be built and owned directly, and which parts can safely be adopted from existing self-hostable/open agent projects without recreating the vendor-lock-in problem the successor is intended to solve.

It also evaluates three current interoperability protocols:

- Model Context Protocol (MCP) for tools/resources;
- Agent Client Protocol (ACP) for coding-agent/client sessions;
- Agent2Agent (A2A) for independent agent services and long-running tasks.

The goal is not to maximize the number of frameworks. It is to minimize custom code **without** allowing a replaceable framework to become the source of truth for conversations, task state, approvals, credentials, or project history.

## Current Working Recommendation

Build and own the **control plane**, but adopt coding-agent runtimes behind a replaceable Developer Agent interface.

```text
Owner PWA
   |
   v
OUR CONTROL PLANE
   |
   +--> Manager Agent / Pydantic AI
   +--> DBOS durable workflows
   +--> Postgres domain state
   +--> policy / approvals / budgets
   +--> GitHub + infrastructure tool broker
   +--> worker lifecycle
   +--> notifications / voice adapters
   |
   v
Developer Agent Adapter
   |
   +--> OpenHands
   +--> OpenCode
   +--> Goose
   +--> future ACP/A2A-compatible agent
```

The current recommendation is therefore:

### Build/own directly

- owner-facing PWA/API;
- authentication/session boundary;
- durable Manager conversation/domain state;
- work requests, plans, tasks, dependencies, decisions and approvals;
- DBOS orchestration and queues;
- policy and cost enforcement;
- worker provisioning/destruction;
- GitHub/tool credential brokering;
- normalized audit/usage/cost records;
- notification and voice abstractions;
- model capability registry/routing;
- adapter contracts for Developer Agents and tools.

### Adopt behind adapters

- coding-agent execution harnesses;
- shell/file/browser/code-editing loops;
- agent-specific context management;
- MCP-compatible tool implementations where appropriate;
- ACP adapters for coding agents where stable and useful;
- optional A2A adapters for future independent remote agent services.

## Why the Control Plane Should Remain Custom

No current product found cleanly matches the complete desired operating model while also satisfying the ownership/portability requirements.

The successor requires an owner-controlled source of truth for:

- the Manager conversation;
- owner decisions and approval policy;
- multiple parallel Developer tasks;
- repository/system context;
- agent-independent task continuity;
- GitHub/infrastructure permissions;
- cost budgets and escalation rules;
- mobile notifications and voice interaction;
- cross-provider model routing;
- audit and recovery.

Existing agent products provide useful pieces of this, but adopting one as the whole platform would cause our durable state and operating logic to inherit that product's concepts, APIs, session model, security assumptions, and release cycle.

That is acceptable for a replaceable worker. It is not acceptable for the successor's primary system of record.

## OpenHands — Current Developer Runtime Front-Runner

OpenHands remains the strongest initial Developer Agent candidate.

### Current strengths

The current open-source OpenHands Agent Canvas/SDK provides:

- a self-hosted control surface for conversations, files, terminals, model configuration, backends, and automations;
- local, Docker, VM, Modal, Kubernetes, and other remote backend patterns;
- a REST-based Agent Server;
- shell, file-editing, browsing, and MCP tool support;
- model-provider flexibility;
- ACP support for replacing the underlying coding agent;
- sub-agent delegation;
- parallel tool/sub-agent execution;
- resumable sub-agent tasks/conversations.

Sources:

- https://docs.openhands.dev/sdk
- https://docs.openhands.dev/openhands/usage/agent-canvas/overview
- https://docs.openhands.dev/sdk/guides/task-tool-set
- https://docs.openhands.dev/sdk/guides/parallel-tool-execution
- https://docs.openhands.dev/sdk/guides/agent-acp
- https://docs.openhands.dev/sdk/guides/mcp

The main OpenHands repository currently uses the MIT license.

Source: https://github.com/OpenHands/openhands

### Agent Canvas reduces some custom work

Agent Canvas is now more capable than the earlier research pass assumed. It describes itself as a self-hosted control surface that can use OpenHands, Claude Code, Codex, Gemini CLI, or another ACP-compatible agent and can work with remote backends.

This means we should test whether Agent Canvas can provide an **optional engineering-console UI** for debugging Developer Agents, rather than building every developer-facing diagnostic screen ourselves.

It should not replace the owner's Manager PWA because:

- its primary UX is developer/agent execution rather than owner-level task supervision;
- its state model should not become our durable project state;
- its backend API key grants powerful execution access and must remain inside our security boundary;
- our mobile notification/approval experience is more specialized.

Sources:

- https://docs.openhands.dev/openhands/usage/agent-canvas/overview
- https://docs.openhands.dev/openhands/usage/agent-canvas/first-time-setup
- https://docs.openhands.dev/openhands/usage/agent-canvas/mobile-access

### Important security test

OpenHands states that the Agent Canvas backend/Agent Server can execute commands and access its filesystem/environment/network. A remote backend API key must therefore be treated as a privileged execution credential.

Source: https://docs.openhands.dev/openhands/usage/agent-canvas/setup

Before selection, prototype exactly where LLM provider keys and task credentials live relative to repository command execution. If repository code can read a long-lived LLM key from the same execution environment, route model traffic through a central broker/proxy or otherwise separate credentials from the code workspace.

## OpenCode — Strong Developer Runtime Challenger

OpenCode is now a serious alternative to OpenHands rather than merely a terminal client.

### Relevant capabilities

Official current documentation shows:

- 75+ LLM providers through its provider/model layer;
- primary agents and specialized subagents;
- permission controls for tools;
- custom tools and MCP servers;
- parallel/multi-session operation;
- a headless `opencode serve` HTTP server;
- an OpenAPI 3.1 endpoint and generated SDK;
- APIs for projects, sessions, messages, files, tools, agents and events;
- ACP server support.

Sources:

- https://opencode.ai/
- https://opencode.ai/docs/providers/
- https://opencode.ai/docs/agents/
- https://opencode.ai/docs/tools/
- https://opencode.ai/docs/server/
- https://opencode.ai/docs/acp/

The current repository uses the MIT license.

Source: https://github.com/anomalyco/opencode/blob/dev/LICENSE

### Why it needs benchmarking against OpenHands

OpenCode may be attractive if it is lighter to provision and operate per disposable worker. Its headless server API makes programmatic Manager integration realistic.

However, desk research has not yet established whether its workspace isolation, long-running remote-server lifecycle, event/recovery model, and automation behavior are as suitable as OpenHands for unattended cloud Developer Workers.

The prototype should therefore implement the same internal Developer Agent contract against **both OpenHands and OpenCode** and run identical repository tasks.

## Goose — Valuable Secondary Candidate and Mobile Reference

Goose is a general-purpose open-source AI agent with desktop, CLI and API interfaces. Its current repository states support for multiple model providers and many MCP extensions and is part of the Agentic AI Foundation at the Linux Foundation.

Source: https://github.com/aaif-goose/goose

The repository currently uses the Apache-2.0 license.

Goose also has an official mobile repository containing an iOS client that connects remotely to a Goose agent through a remote protocol/tunnel.

Source: https://github.com/aaif-goose/goose-mobile

### Current role in our research

Goose is worth using for two purposes:

1. benchmark as a third Developer Agent implementation if OpenHands/OpenCode results are inconclusive;
2. study its remote mobile-agent UX/protocol for ideas relevant to our PWA.

It is not currently the first Developer Agent benchmark because OpenHands and OpenCode expose clearer server-oriented control surfaces in the material inspected so far.

## Letta — Strong Stateful-Agent Technology, but Not the Canonical State Store

Letta is explicitly designed around persistent/stateful agents and offers local/self-hosted App Server deployments.

Current capabilities include:

- model-agnostic agents;
- persistent memory/state;
- self-hosted App Server;
- Agent SDK;
- custom/built-in subagents;
- background parallel subagents;
- MCP tools;
- approval/runtime protocol features;
- custom channels;
- secrets injected into commands without exposing the value to the agent.

Sources:

- https://docs.letta.com/
- https://docs.letta.com/self-hosting/
- https://docs.letta.com/configuration/subagents/
- https://docs.letta.com/configuration/models
- https://docs.letta.com/configuration/secrets/

The main Letta repository currently uses Apache-2.0.

Source: https://github.com/letta-ai/letta

### Why Letta is not currently the Manager foundation

Letta's strongest differentiator—agent-owned persistent memory—is partly the state architecture we intentionally do **not** want to make authoritative.

Our design needs tasks, owner decisions, plans, repository references and approvals to remain understandable and recoverable without a specific agent runtime.

Letta should therefore be evaluated as:

- an alternate Manager-agent runtime;
- a specialized persistent subagent;
- a possible Developer Agent implementation;
- a source of useful memory/approval/channel patterns.

It should not replace Postgres domain state unless a prototype demonstrates a compelling benefit and we can still export/reconstruct the authoritative state independently.

## Dify — Useful Reference, Not Current Core Candidate

Dify provides a substantial self-hostable workflow/application platform.

Current documentation includes:

- Docker Compose self-hosting;
- workflow/chatflow builders;
- REST application APIs;
- tools and MCP;
- a new beta Agent with its own sandbox that can run commands and manipulate files;
- separately isolated code-execution services.

Sources:

- https://docs.dify.ai/en/self-host/deploy/quick-start/docker-compose
- https://docs.dify.ai/en/self-host/use-dify/build/new-agent/overview
- https://docs.dify.ai/en/api-reference/guides/get-started

### Why Dify is not preferred

The current self-hosting guide recommends at least 2 vCPU / 8 GiB for its Docker environment, making it a relatively heavy baseline for functionality we would largely duplicate in our custom state/policy/orchestration layer.

Its main repository also uses a modified Apache 2.0-based license with additional conditions rather than an unmodified permissive Apache/MIT license.

Sources:

- https://docs.dify.ai/en/self-host/deploy/quick-start/docker-compose
- https://github.com/langgenius/dify/blob/main/LICENSE

Dify may be useful for experimentation or UI/workflow ideas, but it is not currently recommended as the successor control plane.

## Developer Agent Abstraction

The control plane should define its own minimal contract rather than coding directly against OpenHands/OpenCode objects everywhere.

Conceptually:

```text
create_task(task_spec, workspace_spec, model_profile) -> agent_task_id
send_instruction(agent_task_id, message) -> accepted
stream_events(agent_task_id, cursor?) -> events
get_status(agent_task_id) -> status
request_summary(agent_task_id) -> summary
cancel(agent_task_id) -> result
resume(agent_task_id) -> result
get_usage(agent_task_id) -> normalized_usage
finalize(agent_task_id) -> artifact/result refs
```

The adapter is responsible for mapping these operations to OpenHands, OpenCode, Goose, ACP, or another implementation.

Our durable `task_id` remains distinct from the agent-runtime session/conversation ID.

## MCP — Recommended Tool/Resource Extension Boundary

MCP is currently the clearest standard boundary for tools/resources.

The current MCP specification defines a client/host/server architecture and standard ways for servers to expose tools and resources. Tools expose invocable actions with schemas; resources expose contextual data through URIs.

Sources:

- https://modelcontextprotocol.io/docs/2026-07-28/learn/architecture
- https://modelcontextprotocol.io/specification/2026-07-28/server/tools
- https://modelcontextprotocol.io/specification/2026-07-28/server/resources

OpenHands, OpenCode, Letta and Dify all currently expose MCP integration paths.

### Proposed use

Where practical, new integrations should expose an MCP-compatible interface so multiple agent runtimes can reuse them.

Examples:

```text
GitHub MCP adapter
AWS MCP adapter
Google Workspace MCP adapter
Appsmith MCP adapter
Power BI / Power Automate adapter
internal documentation/search resources
```

### Important limitation

MCP should **not** be the authorization policy engine.

Our tool broker still decides:

- whether a tool is available to this task;
- which credential/resource scope is used;
- whether owner approval is required;
- idempotency/retry rules;
- audit events;
- cost/blast-radius limits.

The MCP server is the standardized tool surface; the control plane remains the security authority.

The current MCP specification also publishes explicit security guidance, reinforcing that protocol connectivity does not remove the need for authorization and trust controls.

Source: https://modelcontextprotocol.io/specification/draft/basic/security_best_practices

## ACP — Recommended Coding-Agent Adapter, but Not Durable State Protocol

ACP standardizes communication between clients/editors and coding agents. Current stable ACP v1 features include session listing, resume, close, deletion, model/session configuration, usage/cost updates and other session lifecycle capabilities.

Sources:

- https://agentclientprotocol.com/updates
- https://agentclientprotocol.com/announcements/session-resume-stabilized
- https://agentclientprotocol.com/announcements/session-usage-stabilized

OpenCode currently exposes ACP, and OpenHands can run an ACP agent as its backend.

Sources:

- https://opencode.ai/docs/acp/
- https://docs.openhands.dev/sdk/guides/agent-acp

### Proposed use

ACP is a promising way to reduce custom adapters for coding-agent runtimes.

For example:

```text
our Developer Agent adapter
       |
       +--> native OpenHands adapter
       |
       +--> ACP adapter
                |
                +--> OpenCode
                +--> Goose/other ACP agents
                +--> future coding agents
```

### Why it should not become the database schema

ACP is designed around agent sessions, not our full business/domain state. Our task, plan, approval and audit tables should therefore remain independent of ACP session structures.

ACP v2 was published as a **draft** on July 20, 2026. Although many useful v1 session features are already stabilized, the v2 core is still under review/testing.

Source: https://agentclientprotocol.com/announcements/acp-v2-draft

The architecture should support ACP but avoid depending on v2-only semantics until they stabilize.

## A2A — Strong Future Agent-Service Boundary

A2A 1.0 is now a released open standard for communication between independent agent systems built with different frameworks/vendors.

The protocol includes:

- Agent Cards for capability/service discovery;
- messages and artifacts;
- task lifecycle/status;
- authentication descriptions;
- streaming;
- asynchronous/long-running operations;
- human-intervention patterns.

Sources:

- https://a2a-protocol.org/latest/specification/
- https://a2a-protocol.org/latest/topics/key-concepts/
- https://a2a-protocol.org/latest/topics/streaming-and-async/

A2A's official material explicitly distinguishes it from MCP: MCP connects models/agents to tools and context, while A2A connects independent agent systems to each other.

Source: https://a2a-protocol.org/latest/topics/a2a-and-mcp/

### Proposed use

A2A is probably unnecessary for an MVP where every Developer Agent is provisioned by one control plane.

However, our internal Developer Agent/task events should be designed so an A2A adapter can be added later. This would let the Manager delegate work to:

- a remote specialist agent;
- a different self-hosted agent cluster;
- an external service controlled by another system;
- future provider/vendor agent services without embedding their native protocol throughout the control plane.

Do not add A2A merely for architectural fashion. Add it when a second independently operated agent service creates a real interoperability need.

## Protocol Boundary Summary

```text
                OUR CONTROL PLANE
                       |
          +------------+-------------+
          |                          |
          v                          v
     Tool broker                Agent adapter
          |                          |
          v                          +--> native SDK/API
         MCP                         +--> ACP coding agent
                                     +--> A2A remote agent (later)
```

Recommended semantics:

- **MCP:** tools and contextual resources.
- **ACP:** coding-agent session interoperability.
- **A2A:** independent long-running agent-service interoperability.
- **Our Postgres/domain API:** authoritative state, policy, approvals, budgets, audit and lifecycle.

## Build-vs-Adopt Matrix

| Component | Build or adopt? | Current direction |
| --- | --- | --- |
| Mobile owner interface | Build | Specialized Manager UX, passkeys, voice, decisions, notifications |
| Backend/API | Build | Security/control boundary and stable client contract |
| Manager orchestration | Build using libraries | Pydantic AI + DBOS, domain state owned by us |
| Durable state | Build schema on Postgres | Must survive all framework/provider replacements |
| Policy/approval engine | Build | Core safety/cost/access requirement |
| GitHub/infrastructure broker | Build | Credential/policy isolation from agents |
| Worker provisioning | Build | Cost/security/cleanup policy |
| Coding loop | Adopt | OpenHands/OpenCode/Goose benchmark |
| Developer diagnostic UI | Adopt where useful | OpenHands Agent Canvas could supplement our Manager UI |
| Tool protocol | Adopt standard | MCP where practical |
| Coding-agent protocol | Adopt standard | ACP adapter where supported |
| Remote agent-to-agent protocol | Defer/adopt later | A2A when independently operated agents appear |
| Agent memory engine | Do not outsource authority | Letta may be optional runtime, but Postgres remains truth |
| Visual workflow platform | Do not adopt as core | Dify duplicates too much control-plane responsibility |

## Initial Developer Runtime Benchmark Shortlist

The prototype should benchmark, in this order:

1. **OpenHands** — current baseline/front-runner.
2. **OpenCode** — strongest direct challenger.
3. **Goose** — third candidate if results justify expanding the benchmark.
4. **Letta Code/Agent runtime** — separate experiment focused on whether persistent memory creates measurable benefit.

Dify does not need to enter the first coding-runtime benchmark.

## Benchmark Contract

Every runtime should be tested through the same control-plane-level task contract rather than by manually using its preferred UI.

Measure:

- provisioning/startup time;
- task completion rate;
- ability to resume after disconnect/restart;
- event-stream quality;
- code/test quality;
- tool/permission control;
- Git operations;
- model/provider switching;
- token/cost observability;
- sandbox isolation;
- secret exposure risk;
- workspace cleanup;
- implementation effort for our adapter;
- CPU/RAM usage;
- total task cost.

The best Developer Agent is the one that produces reliable work through our control plane at the best overall quality/cost/operability—not necessarily the one with the largest feature list.

## New Architecture Simplification

Because OpenHands itself can host ACP-compatible agents, one possible MVP is:

```text
our control plane
      |
      v
OpenHands Agent Server / Agent Canvas backend
      |
      +--> native OpenHands agent
      +--> OpenCode via ACP
      +--> other ACP agent
```

This could make OpenHands the **worker host/agent gateway** while keeping the specific coding agent replaceable.

This is worth prototyping, but it must not result in all Developer Agent state being stored only inside OpenHands. Our database still owns task lifecycle and essential summaries/events.

## Risks Identified in This Pass

### Too many protocols

Using MCP + ACP + A2A everywhere would increase complexity rather than reduce it. Only adopt a protocol where it replaces a real custom integration boundary.

### Framework state leakage

If our database stores OpenHands/Letta/OpenCode internal objects as the canonical representation of tasks, framework replacement becomes expensive. Store normalized domain state plus optional raw adapter metadata.

### Credential leakage from coding harnesses

Coding agents execute repository-controlled commands. Provider and platform credentials must be separated from code execution wherever possible and audited during the runtime benchmark.

### Product licensing changes

Even currently permissive projects can change future licensing for new versions/components. Record exact dependency/version/license metadata for production builds and keep adapters replaceable.

### Integrated UI temptation

Agent Canvas, Letta, Dify and similar products offer increasingly complete UIs. Reusing an engineering console is useful; allowing it to become the only owner/control UI would weaken the specialized Manager workflow and portability requirement.

## Current Overall Architecture After Six Research Passes

```text
INSTALLABLE OWNER PWA
  text / voice / Web Push / passkeys
             |
             v
OWNER-CONTROLLED CONTROL PLANE
  API + auth
  Pydantic AI Manager
  DBOS workflows/queues
  Postgres state/search
  S3 artifacts/backups
  policy/approval/budget engine
  GitHub/tool credential broker
  LLM capability router
  worker lifecycle controller
             |
             +--> MCP tool/resource services
             |
             v
PRIVATE EPHEMERAL WORKERS
  Developer Agent adapter
      |
      +--> OpenHands native
      +--> OpenCode/other via ACP
      +--> Goose or future runtime
      +--> A2A remote specialist later
```

This architecture keeps all essential user/project state and privileged control under owner-controlled infrastructure while allowing both model providers and coding-agent implementations to change independently.

## Next Step — Consolidated Recommendation Before Building

The exploratory research is now sufficient to produce a **consolidated proposed architecture and MVP implementation plan**.

That document should:

1. turn the six research passes into one coherent target architecture;
2. identify which choices are settled enough to proceed without owner input;
3. identify the small number of material decisions requiring owner approval;
4. define the first prototype scope;
5. define acceptance tests for mobile, Manager autonomy, Developer runtime interchangeability, security isolation, recovery and cost;
6. define likely repositories/services and implementation phases;
7. provide a first realistic monthly budget range with infrastructure separated from LLM consumption;
8. explicitly list what will **not** be built in v1.

No production infrastructure or successor application should be created until that consolidated plan is reviewed with the owner.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)
- [Research 03 — Mobile, Notifications, Authentication, and Voice](/projects/notes/high-director-successor-research-03/)
- [Research 04 — LLM Provider Strategy and Cost](/projects/notes/high-director-successor-research-04/)
- [Research 05 — Persistent State, Memory, Backups, and Security](/projects/notes/high-director-successor-research-05/)

## Verification Record

- Last verified: `2026-08-09`
- Verified against: current official OpenHands/Agent Canvas/SDK documentation and repository; OpenCode documentation/repository; Letta documentation/repository; Dify self-host/API/Agent documentation and license; Goose and Goose Mobile repositories; current MCP specification/security material; ACP current stable updates and v2 draft; A2A v1 specification and task/async documentation.
- Verified by: High Director
- Verification scope: self-hosting, programmatic control surfaces, subagents/parallelism, provider/tool portability, licensing, coding-agent replaceability, developer-console reuse, MCP/ACP/A2A protocol roles, and recommended build-vs-adopt boundary.
- Unverified areas: comparative task quality, worker resource use, restart/resume reliability, credential isolation inside coding harnesses, and adapter implementation effort; these require the proposed prototype benchmark.
