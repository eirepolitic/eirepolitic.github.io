---
title: High Director Successor Research 04 — LLM Provider Strategy and Cost
summary: Current-market research on provider-neutral Manager and Developer model routing, API pricing, context/caching, tool support, OpenHands integration, and LLM cost controls for the High Director successor.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
owner: High Director
order: 119
permalink: /projects/notes/high-director-successor-research-04/
tags:
  - high-director
  - successor
  - research
  - llm
  - openai
  - anthropic
  - gemini
  - openhands
  - cost
  - routing
---

# High Director Successor Research 04 — LLM Provider Strategy and Cost

## Purpose

This fourth research pass evaluates the replaceable LLM layer for the High Director successor.

The goal is **not** to select one permanent provider or model. The goal is to define a model-routing architecture that can use whichever services provide the best quality/cost combination at a given time without changing the Manager workflow, Developer Agent runtime, tool integrations, application state, mobile client, or approval policy.

Pricing and model availability change quickly. Every price in this note is a point-in-time observation verified on 2026-08-09 and must be re-read before procurement or production configuration.

## Current Working Recommendation

Use a **capability-tier model policy**, with provider/model names stored in configuration rather than embedded throughout application logic.

```text
Application role/task
       |
       v
Capability profile
       |
       +--> EFFICIENT
       +--> BALANCED
       +--> FRONTIER
       |
       v
Provider/model registry
       |
       +--> OpenAI adapter
       +--> Anthropic adapter
       +--> Google adapter
       +--> future providers
```

Initial intended use:

- **EFFICIENT** — routine summarization, classification, extraction, progress condensation, simple edits, cheap validation/review subtasks.
- **BALANCED** — normal Manager conversation/planning and ordinary Developer Agent work.
- **FRONTIER** — difficult architecture/debugging/review, ambiguous failures, security-sensitive reasoning, or explicit escalation after a cheaper model fails.

The selected model for each tier should be changeable through configuration and benchmark results.

## Why One Model Should Not Run Everything

Current API pricing varies by more than an order of magnitude between efficient and frontier tiers.

A simple normalized cost unit is useful for sensitivity analysis:

```text
1.0 million input tokens
0.2 million output tokens
```

This is **not a prediction of task usage**. It only makes current model prices easier to compare.

At current standard pricing:

| Model | Input / MTok | Output / MTok | Normalized unit |
| --- | ---: | ---: | ---: |
| OpenAI GPT-5.6 Luna | $0.20 | $1.20 | **$0.44** |
| Google Gemini 3.5 Flash-Lite | $0.30 | $2.50 | **$0.80** |
| Anthropic Claude Haiku 4.5 | $1.00 | $5.00 | **$2.00** |
| Google Gemini 3.6 Flash | $1.50 | $7.50 | **$3.00** |
| Anthropic Claude Sonnet 5 — introductory through 2026-08-31 | $2.00 | $10.00 | **$4.00** |
| OpenAI GPT-5.6 Terra | $2.00 | $12.00 | **$4.40** |
| Anthropic Claude Sonnet 5 — standard from 2026-09-01 | $3.00 | $15.00 | **$6.00** |
| Anthropic Claude Opus 5 | $5.00 | $25.00 | **$10.00** |
| OpenAI GPT-5.6 Sol | $5.00 | $30.00 | **$11.00** |

Sources:

- https://developers.openai.com/api/docs/pricing
- https://platform.claude.com/docs/en/about-claude/pricing
- https://ai.google.dev/gemini-api/docs/pricing

The practical conclusion is structural: using the frontier model for every manager summary, developer iteration, and low-risk edit can multiply LLM spend without necessarily improving the final outcome proportionally.

## OpenAI Current Position

OpenAI's current GPT-5.6 family is explicitly segmented into:

- `gpt-5.6-sol` — frontier model for complex professional work;
- `gpt-5.6-terra` — balance of intelligence and cost;
- `gpt-5.6-luna` — cost-sensitive/high-volume workloads.

All three currently expose function tools, web search, file search, computer use, reasoning controls, 1.05M-token context windows, and up to 128k output tokens.

Source: https://developers.openai.com/api/docs/models

### Current standard short-context pricing

| Model | Input | Cached input | Cache write | Output |
| --- | ---: | ---: | ---: | ---: |
| GPT-5.6 Sol | $5.00 | $0.50 | $6.25 | $30.00 |
| GPT-5.6 Terra | $2.00 | $0.20 | $2.50 | $12.00 |
| GPT-5.6 Luna | $0.20 | $0.02 | $0.25 | $1.20 |

Prices are USD per 1M tokens.

Requests exceeding OpenAI's current long-context threshold are charged at higher rates for the full request. This is another reason not to treat the advertised 1M-token window as a target context size.

Source: https://developers.openai.com/api/docs/pricing

### Prompt caching

GPT-5.6 supports prompt caching. OpenAI documents cache writes at 1.25x uncached input rate and cache reads at substantially reduced rates; explicit breakpoints can be used so stable prefixes are cached without repeatedly writing changing suffixes.

Sources:

- https://developers.openai.com/api/docs/guides/prompt-caching
- https://developers.openai.com/api/docs/guides/latest-model

This maps well to persistent agent instructions, tool schemas, repository policies, and stable project-context prefixes.

## Anthropic Current Position

Anthropic currently provides a similar useful tier spread.

Current first-party Claude Platform pricing includes:

| Model | Base input | 5m cache write | 1h cache write | Cache hit | Output |
| --- | ---: | ---: | ---: | ---: | ---: |
| Claude Opus 5 | $5.00 | $6.25 | $10.00 | $0.50 | $25.00 |
| Claude Sonnet 5 — through 2026-08-31 | $2.00 | $2.50 | $4.00 | $0.20 | $10.00 |
| Claude Sonnet 5 — from 2026-09-01 | $3.00 | $3.75 | $6.00 | $0.30 | $15.00 |
| Claude Haiku 4.5 | $1.00 | $1.25 | $2.00 | $0.10 | $5.00 |

Prices are USD per 1M tokens.

Source: https://platform.claude.com/docs/en/about-claude/pricing

Anthropic states that cache hits cost 10% of base input price; a five-minute cache write costs 1.25x base input and a one-hour write costs 2x.

Claude Sonnet 5 currently has a 1M-token context window, up to 128k output tokens, and the same general tool/platform feature set as Sonnet 4.6 except Priority Tier. Claude Opus 5 also provides a 1M context window and is documented for long-context reasoning/tool use.

Sources:

- https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5
- https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5

### Important pricing date

Sonnet 5's $2/$10 input/output rate is introductory pricing through **August 31, 2026**. Standard pricing becomes $3/$15 beginning **September 1, 2026**.

Any model-routing decision made during this design phase must use the post-introductory rate for long-term cost planning unless Anthropic changes it again.

## Google Gemini Current Position

Google's current Gemini Developer API provides several strong price/performance tiers.

Current models include Gemini 3.6 Flash, Gemini 3.5 Flash, Gemini 3.5 Flash-Lite, Gemini 3.1 Pro Preview, and Gemini 3.1 Flash-Lite, among others.

Sources:

- https://ai.google.dev/gemini-api/docs/models
- https://ai.google.dev/gemini-api/docs/pricing

### Representative current prices

| Model | Standard input | Standard output | Cached-context token rate |
| --- | ---: | ---: | ---: |
| Gemini 3.6 Flash | $1.50 | $7.50 | $0.15 |
| Gemini 3.5 Flash | $1.50 | $9.00 | $0.15 |
| Gemini 3.5 Flash-Lite | $0.30 | $2.50 | $0.03 |
| Gemini 3.1 Flash-Lite | $0.25 | $1.50 | $0.025 |
| Gemini 3.1 Pro Preview | $2/$4 input depending on context size | $12/$18 output depending on context size | model/context dependent |

Prices are USD per 1M tokens. Some Gemini tiers also have Batch/Flex/Priority pricing, so the exact request mode must be part of cost accounting rather than assuming every invocation has the same rate.

Google currently describes Gemini 3.6 Flash as its most intelligent speed-oriented model and Gemini 3.5 Flash-Lite as its most cost-efficient generally available model for high-volume agentic work.

The latest Gemini 3.x models support long context and agent-oriented capabilities such as function calling, structured outputs, and built-in tools. Gemini's Interactions API also supports caching/state patterns intended to reduce repeated-context cost.

Sources:

- https://ai.google.dev/gemini-api/docs/latest-model
- https://ai.google.dev/gemini-api/docs/gemini-3
- https://ai.google.dev/gemini-api/docs/caching

## Long Context Should Be a Safety Valve, Not the Memory Architecture

The current leading models advertise context windows around 1M tokens. That does **not** mean the successor should replay a million tokens of conversation/repository history on every turn.

Reasons:

- long requests may cost materially more;
- repeated context increases latency;
- irrelevant history can impair reasoning quality;
- provider tokenizer behavior differs;
- switching models/providers becomes harder if state is represented only by one giant provider conversation;
- tool call/result histories can grow quickly during coding work.

The durable system should instead retain full source history in owner-controlled storage while constructing a purpose-specific context package for each agent run.

Suggested layers:

```text
full durable history/database
       |
       +--> current task state
       +--> owner decisions
       +--> repository/source references
       +--> current plan
       +--> recent raw conversation
       +--> structured summaries
       |
       v
context builder
       |
       v
provider request
```

Large-context windows then provide resilience for unusually complex work rather than becoming the normal persistence strategy.

## Prompt Caching Should Be Designed In

All three current provider families offer mechanisms that can reduce cost for repeated context.

Likely reusable context includes:

- Manager system instructions;
- tool definitions;
- security/approval policy;
- repository-specific development rules;
- current architecture summaries;
- stable portions of a Developer Agent task package.

The provider-neutral request model should distinguish:

```text
stable cacheable prefix
changing task context
new user/developer event
```

Provider adapters can then map this into each vendor's specific caching mechanism.

The application must record actual cached-input/cache-write usage because cache economics differ by provider and TTL.

## OpenHands Developer-Model Integration

OpenHands already has a provider-neutral LLM layer based on LiteLLM conventions and accepts model identifiers such as `provider/model_name`.

OpenHands also exposes token/cost/latency metrics per LLM call and aggregated conversation cost.

Sources:

- https://docs.openhands.dev/sdk/arch/llm
- https://docs.openhands.dev/sdk/guides/metrics

This changes the earlier LiteLLM conclusion slightly:

- the **Manager control plane** does not currently need a separate LiteLLM proxy because Pydantic AI already provides provider abstraction;
- **OpenHands internally already uses LiteLLM-style provider abstraction**, so Developer Agents can switch among supported providers without us rebuilding their LLM client;
- we should still normalize OpenHands usage/cost events into our own durable accounting schema.

The application must not store only OpenHands/LiteLLM-specific model state because OpenHands itself remains a replaceable worker dependency.

## OpenHands Subscription Authentication Is Optional, Not Core Architecture

OpenHands documents an OAuth-based subscription-login path that can use supported Codex models through a ChatGPT Plus/Pro subscription without consuming normal API credits.

Source: https://docs.openhands.dev/sdk/guides/llm-subscriptions

This may be worth testing as an optional cost-saving development profile where permitted by the service and model support.

It should **not** be the core architecture because:

- it is provider/subscription-specific;
- supported model availability can change;
- the successor's central requirement is easy provider replacement;
- long-running autonomous server behavior should not depend exclusively on an interactive consumer subscription authentication path.

The canonical architecture remains API/provider adapters with explicit usage accounting.

## Proposed Capability Registry

The system should maintain model configuration in data rather than conditional code scattered through agents.

Example conceptual record:

```yaml
model_id: openai/gpt-5.6-terra
provider: openai
capability_tier: balanced
supports_tools: true
supports_structured_output: true
supports_reasoning_control: true
supports_prompt_cache: true
context_window: 1050000
max_output: 128000
cost_profile: openai-gpt-5.6-terra-2026-07-30
allowed_roles:
  - manager
  - developer
  - reviewer
status: active
```

Pricing should live in a separately versioned cost profile because prices can change without the model identifier changing.

## Proposed Role Policy

### Manager Agent

Default to **BALANCED**.

The Manager needs reliable planning, source synthesis, tool selection, developer supervision, and judgment about whether owner input is required. Using the cheapest model for this role could create false savings if poor planning causes repeated Developer work.

Use **EFFICIENT** for deterministic secondary tasks such as:

- shortening an already-created update for speech;
- metadata classification;
- simple extraction;
- low-risk summarization.

Escalate Manager reasoning to **FRONTIER** when:

- architecture/security decisions are complex;
- multiple Developer Agents disagree;
- a difficult failure remains unresolved;
- the balanced model explicitly reports insufficient confidence;
- the owner requests highest-capability review.

### Developer Agents

Developer model selection should be task-based rather than static.

Potential policy:

```text
simple documentation/config/small test fix
    -> efficient or balanced

normal feature/refactor/debug task
    -> balanced

failed attempt / complex debugging / architecture-sensitive implementation
    -> frontier escalation

final high-risk review
    -> independent balanced/frontier reviewer
```

No provider should be declared the best coding model from desk research alone. OpenHands must benchmark candidate models on the user's actual repositories and task types.

## Cost Guardrails

LLM cost limits must be enforced by the application, not merely suggested in prompts.

Required controls:

- monthly global LLM budget;
- daily soft/hard budget;
- per-task budget;
- per-Developer-Agent budget;
- maximum frontier-model spend without owner approval;
- maximum input/output tokens per call where supported;
- context-size threshold that triggers compaction/retrieval instead of uncontrolled replay;
- retry limits;
- automatic pause before materially exceeding a task estimate;
- cost tracking by provider/model/role/task/repository;
- cached versus uncached usage tracking;
- alert on abnormal token growth;
- explicit recording of provider-side tool/search charges.

The Manager can recommend escalation, but the control plane decides whether the configured budget permits it.

## Illustrative Monthly Cost Sensitivity

Real monthly LLM cost cannot yet be forecast responsibly because we do not have measured token usage from the successor prototype.

However, the normalized cost table demonstrates why routing matters.

For example, ten normalized workload units would cost approximately:

- GPT-5.6 Luna: $4.40;
- Gemini 3.5 Flash-Lite: $8.00;
- Gemini 3.6 Flash: $30.00;
- GPT-5.6 Terra: $44.00;
- Claude Sonnet 5 at post-introductory pricing: $60.00;
- Claude Opus 5: $100.00;
- GPT-5.6 Sol: $110.00.

Again, ten units are not a monthly usage forecast; this is a sensitivity example showing the cost multiplier created by model selection.

A subscription-like total budget therefore requires **measured token usage + aggressive role/task routing**, not merely cheap VM hosting.

## Initial Budget Design Hypothesis

Until a prototype provides real usage data, a sensible architecture target is to make model spend independently configurable from infrastructure spend.

For example:

```text
Infrastructure budget       configurable
Manager LLM budget          configurable
Developer LLM budget        configurable
Voice budget                configurable
Frontier escalation reserve configurable
```

The system should show the owner both current month spend and projected spend at the current usage rate.

No hard dollar values should be frozen into the design until prototype measurements exist.

## Provider Failover

Failover should be **capability aware**, not simply "if provider A errors, call provider B."

Before a model can be configured as a fallback for another, automated compatibility tests should confirm the required profile:

- structured output schema adherence;
- tool/function calling;
- streaming event semantics;
- reasoning controls where relied upon;
- context limits;
- multimodal requirements;
- prompt-cache behavior;
- OpenHands compatibility for developer use.

Example:

```text
manager-balanced
  primary: provider/model A
  fallback: provider/model B
  required_profile: manager_balanced_v1
```

This prevents a runtime outage from silently changing behavior to a model that cannot satisfy the task contract.

## Model Changes Must Not Rewrite Conversation History

Durable messages should use our own provider-neutral schema.

Store at minimum:

- role/author;
- canonical text/content;
- structured attachments/references;
- tool request/result records;
- model/provider used for each generated event;
- usage/cost;
- timestamp;
- parent/task/conversation identifiers.

Provider-specific request/response blobs can be retained for audit/debugging where useful, but they must not be the only representation of conversation state.

This enables a conversation to start on one provider and continue later through another.

## Current Candidate Mapping for Prototype Testing

This is a test matrix, not a production selection.

### Efficient profile candidates

- OpenAI GPT-5.6 Luna;
- Google Gemini 3.5 Flash-Lite or Gemini 3.1 Flash-Lite;
- Anthropic Claude Haiku 4.5.

### Balanced profile candidates

- OpenAI GPT-5.6 Terra;
- Anthropic Claude Sonnet 5;
- Google Gemini 3.6 Flash.

### Frontier profile candidates

- OpenAI GPT-5.6 Sol;
- Anthropic Claude Opus 5;
- additional current frontier models should be added only after verifying API availability/tool compatibility at benchmark time.

The benchmark should measure outcome quality, iterations required, latency, tokens, cache behavior, and total task cost—not token price alone.

## Required Prototype Benchmark

Before selecting default models, create a reproducible evaluation suite from representative, non-sensitive tasks across the user's repositories.

Suggested categories:

1. repository comprehension and planning;
2. small Python bug fix;
3. YAML/GitHub Actions change;
4. multi-file feature implementation;
5. failing-test diagnosis;
6. documentation update requiring source verification;
7. architecture review without code changes;
8. PR review/failure recovery;
9. context-heavy continuation task;
10. parallel-agent coordination summary for the Manager.

For each model/profile record:

- success/failure;
- human corrections required;
- number of agent iterations;
- wall-clock time;
- uncached input tokens;
- cached input/cache-write tokens;
- output/reasoning tokens where reported;
- provider tool/search costs;
- Developer Worker hours;
- total dollar cost;
- final code/test quality.

Only this benchmark can establish which models are economically best for the actual workload.

## Current Architecture Implication

The first four research passes now fit together as:

```text
PWA / passkey / push-to-talk
        |
        v
small always-on control plane
        |
        +--> Pydantic AI Manager
        |       |
        |       v
        |   capability-tier model router
        |       |
        |       +--> OpenAI
        |       +--> Anthropic
        |       +--> Google
        |
        +--> DBOS + Postgres durable task state
        |
        +--> GitHub App / tool services
        |
        +--> ephemeral private Developer Workers
                |
                v
             OpenHands
                |
                v
         configured Developer model
```

No provider owns the durable workflow, task state, permissions, tools, mobile client, or conversation history.

## Next Research Pass

The next pass should examine **persistent data, retrieval/memory, audit logging, backups, and secrets/security architecture**.

It should determine:

- Postgres schema boundaries for conversations/tasks/decisions/events/usage;
- whether vector search is actually needed or Postgres full-text/structured retrieval is sufficient initially;
- artifact/log storage design;
- repository-context indexing strategy;
- conversation compaction/summarization strategy;
- backup and disaster recovery;
- secrets manager options;
- worker credential issuance/revocation;
- audit-event model;
- owner/session security;
- network boundary between control plane and Developer Workers.

After that, prototype design can begin with a much firmer architecture and explicit open decisions.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)
- [Research 03 — Mobile, Notifications, Authentication, and Voice](/projects/notes/high-director-successor-research-03/)

## Verification Record

- Last verified: `2026-08-09`
- Verified against: current official OpenAI API model/pricing/caching documentation; Anthropic Claude model/pricing/context/caching documentation; Google Gemini model/pricing/caching/tool documentation; OpenHands LLM architecture, subscription-auth, and metrics documentation.
- Verified by: High Director
- Verification scope: current candidate model tiers, prices, context/tool capabilities, caching economics, OpenHands provider abstraction, cost/accounting implications, and provider-neutral routing design.
- Unverified areas: model quality on the owner's actual repositories, real token usage, effective cache-hit rates, task latency, OpenHands model-specific reliability, and monthly LLM spend; these require the proposed benchmark/prototype.
