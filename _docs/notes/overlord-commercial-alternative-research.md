---
title: Overlord Commercial Alternative Research — Build vs Buy
summary: Current-market research evaluating whether a commercially supported subscription product can replace the intended end-state Overlord application.
section: notes
doc_type: note
status: active
created: 2026-08-12
updated: 2026-08-12
last_verified: 2026-08-12
owner: High Director
order: 129
permalink: /projects/notes/overlord-commercial-alternative-research/
tags:
  - overlord
  - research
  - architecture
  - build-vs-buy
  - factory
  - ona
  - openhands
  - kiro
  - devin
  - ai-agents
---

# Overlord Commercial Alternative Research — Build vs Buy

## Executive conclusion

**Recommendation: HYBRID.**

No commercially available product verified in this research is a true turnkey replacement for the intended end-state Overlord.

Several products now cover a large fraction of the design. The closest practical commercial substitute for a small technical operation is **Factory**, particularly Factory Missions running on managed Droid Computers. Factory can plan large engineering work, orchestrate multiple worker agents, validate results, run remotely, resume missions, expose progress through web/mobile interfaces, apply autonomy policies, use multiple models, integrate through MCP, and automate much of the software-development lifecycle.

Factory is still not equivalent to Overlord. Its documented product model does not provide the complete owner-controlled control plane Overlord is designed around: canonical state independent of the AI vendor, deterministic owner policy and approval enforcement, a general Manager spanning coding and infrastructure operations, hard Overlord-owned spending gates, a central credential broker, and provider-independent durability semantics.

A reasonable estimate is that Factory provides roughly **75% ±5%** of the intended Overlord functional capability today. The missing capabilities are disproportionately important because they contain Overlord's core ownership, security, durability, and portability model.

**Ona** is the other major commercial candidate. It is particularly strong in isolated cloud environments, GitHub/GitLab agent tooling, MCP integrations, AWS access using OIDC rather than static credentials, governance, background automations, and customer-controlled cloud deployment. Its main gap is the opposite of Factory's: it provides strong execution infrastructure, but not the persistent adaptive AI Manager envisioned for Overlord.

The strongest economic and architectural path is therefore:

> Keep Overlord as the thin owner-controlled Manager and control plane, while evaluating commercial products as replaceable Developer execution backends.

This retains the distinctive state, policy, budget, approvals, audit, credential, and provider-portability model while avoiding unnecessary duplication of commercial coding-agent runtime, sandbox, and worker infrastructure.

## Research scope

This research was performed to answer a specific build-vs-buy question:

> Could the end-state Overlord application be replaced by a commercially supported monthly or usage-based service, with the owner primarily connecting repositories, AWS resources, databases, APIs, SaaS tools, credentials, policies, and model choices?

The desired turnkey experience would be:

1. create an account;
2. connect GitHub repositories;
3. connect AWS and other infrastructure;
4. connect databases and SaaS tools;
5. configure credentials and secrets;
6. define permissions, policies, and approval gates;
7. optionally select AI models;
8. begin interacting with an AI Manager that can plan, delegate, execute, monitor, recover, and report.

Products were separated into four categories:

- **Category A — True turnkey replacement:** nearly the entire Overlord end state is already provided as a hosted/commercial service.
- **Category B — Strong partial replacement:** most core functionality is present, but meaningful custom integration or orchestration remains.
- **Category C — Component only:** solves a major area such as coding, SRE, workflow execution, or observability but is not an Overlord replacement.
- **Category D — Framework/build-your-own:** useful infrastructure or SDKs that would still require building an Overlord-equivalent application.

## Overlord source of truth

The end-state design was reconstructed from both the `Overlord` repository and the project documentation in `eirepolitic.github.io`, rather than inferred from the current implementation alone.

Primary source documents:

- `Overlord/README.md`
- `Overlord/docs/architecture.md`
- `Overlord/docs/security-boundaries.md`
- `_docs/notes/high-director-successor-consolidated-design.md`
- `_docs/notes/overlord-phase-0-closeout.md`
- `_docs/notes/overlord-phase-1-local-manager-loop.md`
- `_docs/notes/overlord-phase-2-manager-developer-delegation.md`
- `_docs/notes/overlord-phase-2-developer-recovery-audit.md`
- `_docs/notes/high-director-successor-research-06.md`

Related site pages:

- [High Director Successor — Consolidated Architecture and MVP Implementation Plan](/projects/notes/high-director-successor-consolidated-design/)
- [Overlord Phase 0 Closeout](/projects/notes/overlord-phase-0-closeout/)
- [Overlord Phase 1 — Local Manager Loop](/projects/notes/overlord-phase-1-local-manager-loop/)
- [Overlord Phase 2 — Manager/Developer Delegation](/projects/notes/overlord-phase-2-manager-developer-delegation/)
- [Overlord Phase 2 — Developer Recovery and Audit](/projects/notes/overlord-phase-2-developer-recovery-audit/)
- [High Director Successor Research 06 — Build vs Adopt and Interoperability Boundaries](/projects/notes/high-director-successor-research-06/)

## What the completed Overlord is intended to be

Overlord is intended to become an **owner-controlled autonomous engineering and operations control plane**, not merely an AI coding assistant.

Its intended interaction model is:

```text
Owner
  |
  v
Persistent Manager
  |
  +--> understand request / history / infrastructure
  +--> create and revise plan
  +--> identify owner decisions
  +--> enforce policy and budget
  +--> delegate independent tasks
  |
  +--> Developer Agent A
  +--> Developer Agent B
  +--> external tool / AWS / API / DB
  |
  +--> monitor / retry / recover
  +--> validate / review
  +--> PR / CI / deploy subject to policy
  |
  v
Owner receives decisions, milestones and result
```

The central design principle is:

> **Overlord owns the state and authority. Models and coding agents are replaceable workers.**

PostgreSQL is intended to remain authoritative for conversations, work requests, versioned plans, tasks and dependencies, owner decisions, AgentRuns, usage/cost information, and audit events. GitHub remains authoritative for repositories, branches, commits, pull requests, and CI objects.

## Current implementation state

The current repository is materially beyond an architecture prototype.

Implemented capabilities include:

- PostgreSQL canonical state and migrations;
- provider-neutral domain/application architecture;
- Pydantic AI Manager adapter;
- DBOS durable Manager workflow;
- tested restart/resume through an owner decision;
- persistent local Manager conversation and planning API;
- WorkRequests, Plans, Tasks, and dependencies;
- owner Decision Requests and responses;
- deterministic policy results including approvals and budget approval;
- prototype soft `$40` / hard `$50` monthly spending semantics;
- provider-neutral `DeveloperAgentPort`;
- canonical Developer AgentRun lifecycle;
- dependency-aware delegation;
- duplicate-run protection;
- wait/resume;
- cancellation;
- failed-run retry with lineage;
- Developer lifecycle auditing;
- real OpenHands adapter;
- real OpenCode adapter;
- reproducible Developer benchmark cases and integrity fingerprints;
- controlled real-runtime benchmark workflow;
- offline CI and architecture dependency tests.

Major remaining work includes:

1. selecting a production Developer runtime from real benchmark evidence;
2. connecting Manager execution automatically to a real runtime;
3. full GitHub App write/PR/CI/merge brokering;
4. isolated remote workers or a commercial replacement for those workers;
5. short-lived credential brokering;
6. hosted production deployment;
7. authentication/passkeys;
8. owner PWA/mobile interface;
9. notifications;
10. optional speech;
11. backup/restore/recovery drills;
12. production model/runtime routing;
13. broad AWS integration;
14. general MCP/API/database/SaaS integration;
15. deferred Appsmith, Google Workspace, Power BI, and Power Automate extension points.

## End-state capability model

The following capability model is the basis for product evaluation.

| Capability | Classification | Rationale |
| --- | --- | --- |
| Persistent Manager conversation/history | **REQUIRED** | Primary owner interface |
| Natural-language high-level work requests | **REQUIRED** | Core product interaction |
| Plan generation/revision | **REQUIRED** | Manager responsibility |
| Task decomposition and dependencies | **REQUIRED** | Core autonomous execution model |
| Owner Decision Requests | **REQUIRED** | Explicit architecture |
| Approval gates for risky operations | **REQUIRED** | Security boundary |
| Long-running background execution | **REQUIRED** | Core autonomy |
| Pause/resume/retry | **REQUIRED** | Core workflow semantics |
| Crash/restart recovery | **REQUIRED** | Explicit acceptance requirement |
| Parallel Developer tasks | **REQUIRED** | Explicit acceptance requirement |
| Multiple specialist agents | **REQUIRED** | Target architecture |
| GitHub private/multiple repository access | **REQUIRED** | Primary engineering surface |
| Branch/edit/test/commit/PR lifecycle | **REQUIRED** | MVP acceptance |
| CI monitoring and failure remediation | **REQUIRED** | MVP acceptance |
| Policy-controlled merge/deployment | **REQUIRED** | Intended end state |
| Shell/test/debug execution | **REQUIRED** | Developer runtime requirement |
| AWS connectivity | **REQUIRED** | Intended final integration |
| Scoped AWS operational actions | **HIGHLY DESIRABLE** | Broader AWS modification follows MVP |
| REST/API/database/MCP integrations | **REQUIRED** | General-purpose control-plane objective |
| Owner-controlled canonical state | **REQUIRED** | Fundamental architecture principle |
| Provider-independent Manager state | **REQUIRED** | Explicit acceptance requirement |
| Replaceable Developer runtime | **REQUIRED** | Explicit architecture |
| Model-provider flexibility | **REQUIRED** | Explicit architecture |
| Agent/task/run audit trail | **REQUIRED** | Security and operational model |
| Token/model/worker cost attribution | **REQUIRED** | Cost-control requirement |
| Hard spending enforcement | **REQUIRED** | Explicit policy requirement |
| Deterministic tool authorization | **REQUIRED** | Model may propose, but must not authorize itself |
| Short-lived/scoped credentials | **REQUIRED** | Security model |
| Isolated Developer environments | **REQUIRED** | Security model |
| Secret isolation from repository code | **REQUIRED** | Explicit security requirement |
| Hosted owner UI | **HIGHLY DESIRABLE** | Intended operational experience |
| Mobile-friendly access | **HIGHLY DESIRABLE** | Primary design targets phone use |
| Push notifications | **HIGHLY DESIRABLE** | Decision-required workflow |
| Voice STT/TTS | **OPTIONAL** | Useful but not defining |
| Appsmith | **OPTIONAL** | Deferred extension |
| Power BI / Power Automate | **OPTIONAL** | Deferred extension |
| Google Workspace | **OPTIONAL** | Deferred extension |
| Searchable retained history | **HIGHLY DESIRABLE** | Intended product |
| Backups/recovery | **REQUIRED** | Explicit acceptance requirement |
| Multi-user enterprise tenancy | **OUT OF SCOPE** initially | Explicitly deferred |
| Kubernetes | **OUT OF SCOPE** | Explicitly unnecessary |
| A2A federation | **OPTIONAL / DEFERRED** | Future extension |

## Market landscape

### Category A — True turnkey replacement

**None found.**

No presently documented product simultaneously satisfies the engineering-agent requirements and Overlord's independent control-plane, credential, policy, budget, durability, and multi-tool ownership requirements with a simple connect-and-run setup.

### Category B — Strong partial replacements

| Product | Approximate Overlord coverage | Strongest characteristic |
| --- | ---: | --- |
| **Factory** | **~75%** | Closest adaptive multi-agent engineering Manager |
| **Ona** | **~70%** | Strongest managed environment/security/infrastructure layer |
| **OpenHands Enterprise** | **~68–72%** | Best provider/runtime openness and control-plane architecture |
| **Kiro Web** | **~67%** | Strong autonomous multi-repository engineering flow |
| **Devin** | **~65%** | Mature managed autonomous software engineer |
| **OpenAI Frontier** | **~60–70% documentable** | Closest general enterprise agent-platform concept |

These percentages are directional rather than benchmark scores. REQUIRED capabilities are weighted much more heavily than optional interface features, and undocumented behavior is treated as `UNCLEAR` rather than assumed present.

### Category C — Major components only

**GitHub Copilot Cloud Agent** is a substantial GitHub-native coding product. It is useful as an autonomous coding component but does not provide the persistent cross-infrastructure Manager/control plane required for an Overlord replacement.

**AWS DevOps Agent** is an important operational/SRE complement. It supports autonomous incident investigation and AWS operational work, but it is not a complete autonomous software-development Manager and control plane.

Microsoft, Salesforce, ServiceNow, and similar enterprise agent platforms can build and govern general business agents, but substantial custom application, workflow, and engineering lifecycle construction would still be required.

### Category D — Framework/build-your-own

Pydantic AI, DBOS, Temporal, MCP servers, AgentCore-style infrastructure, OpenCode, and similar SDKs/runtimes can all be useful Overlord components.

They do not answer the build-vs-buy question because adopting them still means building the application and operating model around them.

The open-source OpenHands runtime belongs here when considered alone; OpenHands Enterprise is evaluated separately as a commercial partial replacement.

## Candidate 1 — Factory

### Why it is closest

Factory Missions is the closest commercial analogue to the intended Manager-to-Developer loop.

Mission Mode can plan work, delegate to worker agents, use a separate validator, track milestones, execute remotely, and expose Mission Control so the user can pause, redirect, and resume. Separate subagents can carry different prompts, models, and tool policies.

Factory's web, desktop, and mobile surfaces plus managed Droid Computers also map well to the desired experience in which the owner can work from a phone while execution continues remotely.

### Software engineering lifecycle

Factory is designed around coding, testing, deployment, reviews, CI automation, and broader software-development lifecycle workflows. Droid Exec provides a headless automation surface with controlled autonomy.

### Security and control

Documented controls include:

- project-scoped editing;
- command approvals;
- shell allow/deny/block lists;
- secret scanning that can block commit/push;
- sandboxing;
- organizational/enterprise controls;
- specialist subagents with separate tool policies.

### Models

Factory provides meaningful model flexibility, including BYOK/custom model configurations and separate orchestrator/worker/validator model choices.

This remains weaker than Overlord's design because the Factory platform itself still owns the orchestration service and much of the operational state.

### Cost

Current public individual pricing verified during this research:

- Pro: `$20/month`
- Plus: `$100/month`
- Max: `$200/month`

Plus introduces Factory-managed Droid Computers. Missions can incur Extra Usage beyond included limits.

For an Overlord-like remote workflow, **Plus at approximately $100/month is the realistic starting tier**, rather than the $20 headline tier.

### Critical limitations

Factory's own Mission documentation says Missions are not fully fire-and-forget and recommends active monitoring/redirection for long-running work. Its broader persistent “Software Factory” concept is currently a Private Preview product.

**Classification: Category B.**

Official sources:

- https://factory.ai/pricing
- https://docs.factory.ai/web/missions
- https://docs.factory.ai/features/missions/troubleshooting
- https://docs.factory.ai/web/software-factory
- https://docs.factory.ai/cli/account/security
- https://docs.factory.ai/model-independence/byok

## Candidate 2 — Ona

Ona is the strongest commercial alternative if the primary concern is avoiding ownership of worker infrastructure while retaining strong execution security.

Ona provides isolated environments containing repository code, toolchains, tests, and integrations, with parallel/background execution. It can run in Ona Cloud or in customer-controlled AWS/GCP environments.

### GitHub and engineering execution

Its source-control tools can manage pull requests, review comments, issues, repository search, and GitHub Actions status. Automations can perform closed-loop engineering tasks such as issue/error intake through test and pull request creation.

### AWS and security

This is one of Ona's strongest matches with the Overlord design.

Enterprise environments can use AWS OIDC federation. Ona obtains temporary AWS STS credentials for configured IAM roles, avoiding static AWS access keys in the agent environment.

Ona also exposes non-SCM tools through MCP and supports cloud-provider/database integration patterns.

### Main limitation

Ona's orchestration model is primarily trigger/automation-oriented rather than the persistent adaptive Manager envisioned for Overlord.

Its current Cloud agent direction also reduces provider/runtime neutrality: new Ona Cloud environments and automations are directed toward Codex Agent rather than a broad interchangeable Manager-runtime abstraction.

Enterprise AI budgets are documented as visibility controls rather than hard execution-blocking limits, so they do not match Overlord's deterministic hard spending gate.

### Cost

Public Core pricing begins around `$20/month`, with usage measured through Ona Compute Units combining AI and environment consumption.

The most relevant Overlord-style security features, including AWS OIDC and customer-controlled cloud deployment, require Enterprise arrangements and therefore do not have transparent self-service pricing.

**Classification: Category B.**

Official sources:

- https://ona.com/pricing
- https://ona.com/docs/ona/getting-started
- https://ona.com/docs/ona/agents/scm-tools
- https://ona.com/docs/ona/integrations/overview
- https://ona.com/docs/ona/identity/aws-oidc
- https://ona.com/docs/ona/automations/automations-in-practice
- https://ona.com/docs/ona/agents/overview

## Candidate 3 — OpenHands Enterprise

OpenHands is architecturally the closest commercial option to Overlord's provider-neutral philosophy.

Its Agent Control Plane is intended to manage agents across repositories, workflows, and teams while enforcing policies and tracking cost, usage, and activity. OpenHands is also explicitly model-agnostic and supports isolated execution plus scheduled/event-driven work.

Per-conversation maximum budget controls exist in the application settings.

### Why it is not the turnkey winner

The highest-control Agent Control Plane configuration is self-hosted/on-premise. That preserves owner control but transfers a meaningful amount of infrastructure and reliability responsibility back to the customer.

OpenHands also remains fundamentally a software-engineering agent platform. It does not by itself provide the complete general Manager over AWS, owner projects, arbitrary SaaS operations, durable owner decisions, and Overlord-owned canonical state.

### Strategic advantage

Overlord already contains an OpenHands adapter.

This makes OpenHands the **lowest-friction hybrid execution candidate** because the current architecture was deliberately designed around this replacement boundary.

**Classification: Category B.**

Official sources:

- https://www.openhands.dev/
- https://www.openhands.dev/blog/openhands-enterprise-agent-control-plane
- https://docs.openhands.dev/openhands/usage/settings/application-settings

## Candidate 4 — Kiro Web

Kiro Web can connect GitHub/GitLab repositories, plan high-level tasks, coordinate specialized subagents, work across multiple repositories, run inside an isolated cloud sandbox, and produce pull requests.

Sessions can continue after the user's local machine is closed, and cloud automations support recurring work.

### Maturity limitation

As of this research date, **Kiro Web remains Preview**. This is significant when comparing it with Overlord's explicit reliability and durability objectives.

### Cost

Current verified public pricing:

- Pro: `$20/month`
- Pro+: `$40/month`
- Pro Max: `$100/month`
- Power: `$200/month`

Autonomous Web execution uses the same credit system.

### Gap

Kiro is a strong autonomous engineering product rather than a provider-independent general operations Manager and control plane.

**Classification: Category B.**

Official sources:

- https://kiro.dev/web/
- https://kiro.dev/
- https://kiro.dev/pricing/

## Candidate 5 — Devin

Devin remains one of the most mature direct “autonomous software engineer” products.

It supports private repositories, pull requests, PR-comment interaction, sessions, scheduling, playbooks, and MCP connectivity to external tools and data.

### Cost

Current verified public/self-service pricing includes:

- Free: `$0`
- Pro: `$20/month`
- Max: `$200/month`
- Teams: minimum approximately `$80/month`
- Enterprise: negotiated/usage-based

### Gap

Devin's unit of work remains primarily a software-engineering session. It can be orchestrated programmatically and scheduled, but it does not provide Overlord's independent canonical state, replaceable Developer runtime, general AWS policy broker, deterministic budget/approval model, or provider-independent Manager.

**Classification: Category B.**

Official sources:

- https://devin.ai/pricing
- https://docs.devin.ai/integrations/gh
- https://docs.devin.ai/work-with-devin/devin-mcp
- https://docs.devin.ai/work-with-devin/mcp
- https://docs.devin.ai/admin/billing/self-serve

## Candidate 6 — OpenAI Frontier

Frontier is the closest broad enterprise concept to a persistent AI workforce/control plane. It provides shared business context, tools and execution environments, governance, permissions, and auditability, and it uses open standards for connecting additional agents.

### Why it is not the practical winner

Frontier is a contact-sales enterprise product rather than a transparent self-service subscription suitable for direct cost comparison.

Public documentation also does not establish FULL support for Overlord's concrete engineering lifecycle acceptance target:

```text
inspect repository
-> branch
-> edit
-> test
-> PR
-> watch CI
-> diagnose failed CI
-> repair
-> policy-controlled merge/deploy
-> retain exact durable evidence
```

Those capabilities therefore remain `UNCLEAR` rather than assumed.

It also does not satisfy Overlord's objective of making the Manager model provider itself replaceable.

**Classification: Category B, enterprise-only/practically incomplete for this use case.**

Official sources:

- https://openai.com/business/frontier/
- https://openai.com/index/introducing-openai-frontier/

## Products and frameworks that are not true replacements

| Product/category | Classification | Reason |
| --- | --- | --- |
| GitHub Copilot Cloud Agent | C | Strong GitHub coding agent; no general Manager/control plane |
| AWS DevOps Agent | C | Strong SRE/operations component; not full software-development Manager |
| OpenCode | C/D | Coding runtime; no hosted owner control plane |
| Pydantic AI | D | Agent framework |
| DBOS | D | Durable workflow infrastructure |
| Temporal | D | Workflow infrastructure |
| Microsoft Foundry/agent SDKs | D | Managed building blocks; application construction remains |
| Copilot Studio | C/D | Agent builder; owner still defines application/orchestration |
| Salesforce Agentforce | C | Strong business workflow agents, not engineering control plane |
| ServiceNow agent products | C | IT/business workflow orchestration, not full Overlord engineering lifecycle |
| MCP | D | Integration protocol, not a product |

Additional official sources used in the broader market comparison:

- https://github.com/features/copilot/plans
- https://aws.amazon.com/devops-agent/
- https://aws.amazon.com/devops-agent/pricing/

## Detailed candidate summary

| Candidate | Hosting | Multi-agent | GitHub lifecycle | AWS/tools | Governance | Model flexibility | Persistent Overlord-like Manager |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Factory | Hosted + managed computers | **Strong** | Strong | MCP/shell; AWS possible | Strong | Strong | **Partial/closest** |
| Ona | Hosted or customer VPC | Parallel agents/automations | **Strong** | **Strong**, AWS OIDC | **Strong** | Partial | Weak/Partial |
| OpenHands | Cloud/local/self-hosted | Strong | Strong | MCP/shell | **Strong Enterprise** | **Strongest** | Partial |
| Kiro | Hosted Web sandbox | **Strong** | **Strong** | Extensible | Moderate | Moderate | Partial |
| Devin | Hosted cloud | Parallel sessions | Strong | MCP/integrations | Strong Enterprise | Moderate | Partial |
| Frontier | Hosted enterprise | **Strong conceptual** | Unclear | **Strong general tools** | **Strong** | Weak for Manager models | Strong conceptual |

## Direct capability comparison

Legend: **FULL / PARTIAL / NO / UNCLEAR**

| Overlord capability | Factory | Ona | OpenHands | Kiro | Devin | Frontier |
| --- | --- | --- | --- | --- | --- | --- |
| Persistent user sessions/history | FULL | FULL | FULL | FULL | FULL | FULL |
| High-level natural-language request | FULL | FULL | FULL | FULL | FULL | FULL |
| Adaptive plan/decomposition | **FULL** | PARTIAL | PARTIAL | **FULL** | PARTIAL | PARTIAL |
| Owner decision gates | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL |
| Multi-agent delegation | **FULL** | PARTIAL | FULL | **FULL** | PARTIAL | FULL |
| Long-running background execution | FULL | FULL | FULL | FULL | FULL | FULL |
| Parallel work | FULL | FULL | FULL | FULL | FULL | FULL |
| Pause/resume/retry | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | UNCLEAR |
| Explicit crash/restart durability semantics | **UNCLEAR** | UNCLEAR | UNCLEAR | UNCLEAR | UNCLEAR | UNCLEAR |
| Private/multiple repositories | FULL | FULL | FULL | FULL | FULL | UNCLEAR |
| Code/shell/tests | FULL | FULL | FULL | FULL | FULL | PARTIAL |
| Branch/commit/PR | FULL | FULL | FULL | FULL | FULL | UNCLEAR |
| CI awareness/remediation | PARTIAL | PARTIAL | PARTIAL | **FULL/PARTIAL** | PARTIAL | UNCLEAR |
| Policy-controlled merge | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | UNCLEAR |
| AWS/tool execution | PARTIAL | **FULL/PARTIAL** | PARTIAL | PARTIAL | PARTIAL | PARTIAL |
| REST/MCP/SaaS integration | FULL | FULL | FULL | FULL | FULL | FULL |
| Owner-controlled canonical DB | **NO** | **NO** | PARTIAL | NO | NO | NO |
| State independent of model/runtime vendor | NO | NO | **PARTIAL/FULL self-hosted** | NO | NO | NO |
| Replaceable coding runtime | PARTIAL | PARTIAL | **FULL** | NO | NO | FULL/PARTIAL |
| Replaceable model providers | PARTIAL/FULL | PARTIAL | **FULL** | PARTIAL | PARTIAL | NO/PARTIAL |
| Audit/activity records | FULL enterprise | FULL | FULL enterprise | PARTIAL | FULL enterprise | FULL |
| Usage/cost tracking | FULL | FULL | FULL | FULL | FULL | PARTIAL/UNCLEAR |
| Hard spend governor | PARTIAL | **NO** | PARTIAL/FULL | PARTIAL | PARTIAL | UNCLEAR |
| Deterministic tool policy | PARTIAL/FULL | PARTIAL | PARTIAL/FULL | PARTIAL | PARTIAL | PARTIAL/FULL |
| Short-lived credential model | PARTIAL | **FULL for AWS OIDC** | PARTIAL | PARTIAL | PARTIAL | FULL/PARTIAL |
| Isolated execution | FULL | FULL | FULL | FULL | FULL | FULL |
| Mobile/browser owner access | FULL | FULL browser | PARTIAL/FULL | FULL browser | FULL | FULL |
| Notifications | PARTIAL | PARTIAL | PARTIAL | PARTIAL | PARTIAL | UNCLEAR |
| Voice | NO/UNCLEAR | NO | NO | NO/UNCLEAR | NO/UNCLEAR | UNCLEAR |
| Owner backups/portable recovery | NO/UNCLEAR | NO/UNCLEAR | **PARTIAL/FULL self-hosted** | NO/UNCLEAR | NO/UNCLEAR | NO/UNCLEAR |

The repeated `UNCLEAR` ratings for crash/restart semantics are intentional. Public vendor documentation demonstrates long-running sessions and resumption, but this research did not find the same explicit contract Overlord already tests: canonical application state plus exact workflow continuation after the orchestration runtime is destroyed and restarted.

## Security and control comparison

### Where Overlord is stronger by design

Overlord is designed to separate agent reasoning from authorization:

```text
LLM proposes action
       |
       v
deterministic Overlord policy
       |
   approval?
       |
       v
central broker
       |
short-lived/scoped credential
       |
       v
external system
```

The intended design prevents a coding agent from automatically owning long-lived GitHub App keys, broad hosting credentials, database administrator credentials, or equivalent privileged secrets.

The database also remains owner-controlled, so replacing OpenAI, Anthropic, OpenHands, OpenCode, DBOS, or another execution provider does not remove the application's canonical project and decision history.

### Where commercial vendors are stronger

Commercial vendors already operate and maintain:

- identity systems;
- sandbox fleets;
- network isolation;
- patching;
- managed runtime images;
- organizational policy systems;
- service monitoring;
- capacity and scaling;
- support processes.

A custom Overlord deployment would need to operate all of these correctly.

Ona deserves particular credit for AWS OIDC federation and temporary role credentials. Factory has strong practical controls such as project scoping, risky-command approval, command policies, sandboxing, and secret detection. OpenHands Enterprise is attractive where customer-controlled deployment and model/provider portability are more important than fully managed hosting.

## Reliability comparison

### Commercial-vendor advantage

A mature commercial service has a meaningful operational advantage in:

- worker provisioning;
- sandbox lifecycle;
- runtime upgrades;
- image maintenance;
- networking;
- scaling parallel workers;
- service monitoring;
- operational troubleshooting;
- support.

These are precisely the expensive parts of Overlord that remain incomplete.

### Agent reliability is a separate issue

Commercial infrastructure reliability does not automatically produce reliable autonomous reasoning.

Even sophisticated current products document limitations around long-running autonomous work, error accumulation, human intervention, or preview maturity. Buying a service therefore reduces infrastructure failures but does not eliminate:

- incorrect plans;
- failed fixes;
- bad assumptions;
- malformed actions;
- runaway retries;
- overly broad changes;
- ambiguous owner decisions.

### Overlord durability advantage

Overlord already has a particularly concrete durability test:

- canonical state written before waiting;
- stable logical workflow identity;
- DBOS runtime destroyed;
- DBOS restarted;
- original owner decision delivered;
- same workflow continues;
- canonical Plan/Task/Decision state is not duplicated.

This is a stronger explicit recovery contract than could be verified publicly for the commercial candidates.

### Overlord operational disadvantage

Those semantics only help if the surrounding custom service remains healthy.

Production Overlord would still require reliable:

- PostgreSQL operation;
- monitoring;
- backup verification;
- networking and security patching;
- host replacement;
- worker cleanup;
- credential rotation;
- application upgrades;
- alerting.

Commercial vendors are structurally better positioned for those routine platform-operational concerns.

## Cost and build-vs-buy comparison

### Continue building Overlord

The approved architecture deliberately targets low fixed infrastructure expenditure, with a prototype hard monthly budget of `$50` and low-cost always-on control-plane infrastructure.

Infrastructure is not the primary economic problem. **Engineering and maintenance time are.**

Remaining custom responsibilities include:

- remote worker provisioning;
- secret/credential broker;
- GitHub App lifecycle;
- production PostgreSQL/DBOS operation;
- UI/authentication;
- notifications;
- model/provider adapters;
- backup/recovery testing;
- observability;
- production security;
- external API maintenance;
- incident response for Overlord itself.

The remaining effort is best described as months of iterative part-time engineering plus indefinite maintenance rather than a precise number of development hours.

Overlord's long-term cost advantage is that models and runtimes can be routed and replaced independently rather than forcing all execution through one vendor's pricing model.

### Buy Factory

A realistic remote-worker starting point is approximately **$100/month Plus**, plus Extra Usage where needed.

At roughly `$1,200/year` before overages, the subscription cost is small compared with building and maintaining an entire autonomous coding/runtime platform.

The limitation is that the final 20–30% of Overlord requirements would remain.

### Buy Ona

Public entry pricing starts around **$20/month plus OCU consumption**.

The security capabilities most relevant to Overlord, such as AWS OIDC and customer-controlled cloud deployment, require Enterprise pricing plus any customer-run AWS infrastructure.

### Buy Kiro

Current public pricing ranges from `$20–$200/month`, with optional usage overage. It is inexpensive enough for experimentation, but the relevant Kiro Web product remains Preview.

### Buy Devin

Current self-service pricing ranges from `$20` to `$200/month`, with Teams beginning around `$80/month` and Enterprise negotiated separately.

Again, this is inexpensive compared with the cost of reproducing and maintaining an autonomous coding runtime.

### Buy OpenHands

Open-source/local OpenHands can be inexpensive apart from infrastructure and models. Enterprise governance is commercial/contact-sales.

Its economic advantage is primarily control, openness, and compatibility with the existing Overlord adapter—not complete elimination of platform operations.

### Buy Frontier

Current practical pricing is `UNCLEAR` because Frontier is sold through enterprise contact-sales rather than transparent self-service pricing.

## Closest actual commercial substitute

For the direct question:

> If Overlord development stopped today, what is the closest commercial product that could simply be subscribed to?

The answer is:

> **Factory, probably Factory Plus or Max using Missions and managed Droid Computers.**

Estimated realistic capability coverage:

> **approximately 75%, with an uncertainty of about ±5 percentage points.**

Factory comes closest to reproducing the experience of giving a Manager a substantial engineering goal and having that system plan, divide work among agents, validate results, operate remotely, and allow high-level owner intervention.

It does **not** reproduce Overlord's ownership architecture.

To make Factory genuinely equivalent, custom work would still be required for:

- canonical work/project state outside Factory;
- non-code AWS/database/SaaS operations;
- durable owner Decision Requests;
- deterministic action approval;
- hard budget enforcement;
- centralized secret/credential brokering;
- long-term owner-controlled audit history;
- provider/runtime portability;
- backup/recovery of application history;
- product-specific external integrations.

Building all of that around Factory would begin recreating the core of Overlord.

## What the owner would give up by abandoning Overlord

### Ownership

Commercial product state becomes an important part of the operational record rather than owner-controlled PostgreSQL being the single canonical application state.

### Provider independence

A vendor may permit model selection, but replacing the orchestration platform itself becomes a migration project.

### Deterministic policy ownership

Vendor permission models replace Overlord-specific policy primitives and owner Decision Request semantics.

### Canonical audit model

History becomes distributed across vendor sessions, GitHub, cloud logs, and connected systems.

### Custom budget semantics

Overlord can eventually deny projected expensive actions before execution while allowing low-cost Manager interaction to continue.

### Credential architecture

The owner accepts the commercial platform's trust boundary rather than controlling every privileged credential exchange.

### Exact workflow behavior

Overlord can implement unusual owner-specific workflows around AWS, Appsmith, databases, Power BI, Power Automate, or other systems that a general coding-agent vendor may never prioritize.

## What the owner would gain

### Immediate functionality

Commercial coding-agent products work now.

### Operational reliability

Worker provisioning, runtime patching, and environment lifecycle become vendor responsibilities.

### Faster access to coding-agent improvements

The vendor continuously maintains and improves the runtime.

### Lower engineering burden

A substantial class of infrastructure and runtime implementation decisions disappears.

### Predictable experimentation cost

Current `$20–$200/month` individual-product pricing is very small compared with implementing and maintaining a complete autonomous coding-agent runtime internally.

## Reversibility

Switching to a commercial product would be **partially reversible**.

Highly portable artifacts include:

- repository source code;
- Git history;
- branches, commits, and pull requests;
- CI configuration;
- infrastructure-as-code;
- repository-resident instructions/skills;
- standard MCP integrations.

Less portable assets include:

- agent conversation history;
- vendor-specific Missions/sessions;
- task decomposition;
- internal memory;
- automation configuration;
- permission policies;
- cost history;
- agent evaluations;
- vendor-specific knowledge stores.

This is another reason to retain Overlord's canonical domain model even when Developer execution is outsourced.

## Recommended path

### Decision recommendation: HYBRID

Do **not** abandon the Overlord repository.

Do **not** continue building a general-purpose coding sandbox/cloud-worker platform until commercial alternatives have been benchmarked through the existing Developer runtime abstraction.

The current architecture has already created the key seam required for this approach: `DeveloperAgentPort` separates Overlord's canonical state and Manager responsibilities from the coding runtime.

Use that abstraction deliberately.

### Target architecture

```text
                 OWNER
                   |
                   v
            OVERLORD MANAGER
       canonical state / DBOS
       decisions / audit / budget
       policy / credential broker
                   |
          DeveloperAgentPort
                   |
          +--------+---------+
          |        |         |
          v        v         v
       Factory  OpenHands   Ona
        or one selected commercial runtime
```

Overlord should continue to own:

- conversation and Manager state;
- WorkRequests;
- Plans;
- Tasks/dependencies;
- owner decisions;
- policy;
- budgets;
- AgentRun records;
- audit history;
- final GitHub authority;
- privileged credentials;
- AWS/tool authorization.

The commercial Developer runtime can own:

- coding-agent harness;
- coding-runtime model interaction;
- isolated compute;
- sandbox startup;
- terminal execution;
- code generation;
- tests and debugging;
- worker scaling;
- temporary execution state.

### Security-preserving execution model

Where practical, a commercial Developer runtime should not receive broad merge or cloud authority directly.

```text
commercial Developer
      |
      +--> inspect repository
      +--> edit/test/debug
      +--> return diff/commit/evidence
                 |
                 v
            OVERLORD POLICY
                 |
                 +--> GitHub broker
                 +--> AWS broker
                 +--> approval gate
```

This preserves the most valuable part of Overlord while outsourcing the commodity runtime layer.

### Commercial backends to benchmark first

The existing Phase 2 benchmark framework should eventually test:

1. **Factory** — strongest candidate if multi-agent autonomy and minimal operations are most important.
2. **OpenHands** — strongest candidate if provider independence, reversibility, and existing adapter compatibility are most important.
3. **Ona** — strongest candidate if secure cloud environments and AWS credential federation are most important.

Kiro and Devin remain useful user-facing comparisons, but the above three are the highest-value candidates for integration behind Overlord's existing adapter boundary.

## Bottom line

If Overlord development stopped today, the closest thing available as a subscription is **Factory**, probably beginning with the **approximately $100/month Plus tier** so autonomous work can run on managed remote computers.

It would provide roughly **three quarters of the intended end state** and immediately replace a substantial amount of coding-agent, multi-agent orchestration, sandbox, remote execution, and software-engineering workflow work that remains on the roadmap.

It would **not** replace the capability that makes Overlord architecturally distinctive: one owner-controlled Manager with durable independent state, strict decision and approval semantics, hard cost governance, centrally brokered credentials, cross-vendor runtime portability, and controlled authority over GitHub, AWS, databases, and arbitrary external systems.

Buying Factory, Ona, Kiro, Devin, or a similar platform would likely be **cheaper and operationally more reliable than building a complete in-house Developer-agent hosting platform**.

It is **not clearly cheaper or functionally better than retaining the Overlord control plane and buying Developer execution capability underneath it**.

The best current recommendation is therefore:

> **Finish the unique control-plane portion of Overlord and avoid rebuilding the Developer runtime/infrastructure capabilities that commercial engineering-agent platforms increasingly provide.**

## Verification record

- Last verified: `2026-08-12`
- Verified against: current Overlord source/design documents and current official product, pricing, security, integration, and architecture documentation for Factory, Ona, OpenHands, Kiro, Devin, OpenAI Frontier, GitHub Copilot, and AWS DevOps Agent.
- Verified by: High Director
- Research date: `2026-08-12`
- Important limitation: commercial product capabilities and pricing are time-sensitive. Re-verify before making a subscription or architecture decision.
- Unknowns are intentionally recorded as `UNCLEAR` rather than inferred from marketing terms such as “autonomous,” “enterprise automation,” or “agent platform.”
