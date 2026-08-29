---
title: Overlord — Developer Model Cost and Routing Investigation
summary: Research into lowering autonomous Developer model cost through deterministic preprocessing, cheaper capable models, bounded escalation, and measured cost per successful task.
section: notes
doc_type: note
status: active
created: 2026-08-28
updated: 2026-08-28
last_verified: 2026-08-28
owner: High Director
order: 149
permalink: /projects/notes/overlord-developer-model-cost-routing-investigation/
tags:
  - overlord
  - developer
  - models
  - cost
  - routing
  - opencode
  - research
---

# Overlord — Developer Model Cost and Routing Investigation

## Outcome

A focused research investigation was completed into how Overlord can reduce autonomous Developer model cost without sacrificing the ability to perform real software-engineering work.

The evidence does not support immediately replacing the accepted production runtime or implementing a complex multi-provider swarm. It does support an empirical trial of a simpler staged route:

```text
Task
  -> deterministic repository/preflight evidence
  -> rule-based difficulty + risk classification
  -> cheaper capable Developer for ordinary work
  -> deterministic validation
  -> bounded repair while evidence improves
  -> stronger-model escalation for difficult/protected work or failed attempts
```

For the first trial, the recommended baseline remains inside the already accepted OpenAI/OpenCode path:

```text
GPT-5.6 Luna -> GPT-5.6 Terra -> GPT-5.6 Sol
```

This is an evaluation recommendation, not a production model-selection change.

## Architecture preserved

The investigation does not reopen the accepted control-plane design:

- PostgreSQL remains canonical state;
- DBOS remains the durable workflow coordinator;
- `DeveloperAgentPort` remains the provider-neutral Developer abstraction;
- local Developer work remains inside disposable Docker containers through OpenCode;
- GitHub authority remains behind `GitHubPort` / `GitHubBroker` and durable audit;
- Developer containers must not receive Docker socket, GitHub App private keys/tokens, AWS credentials, PostgreSQL credentials, broad host filesystem access, or broad Linux privileges;
- remote Developer workers remain deferred.

The current production bounded composition is OpenAI-specific at the credential/configuration layer, but the architectural abstraction remains provider-neutral.

## Why cost per successful task matters

Raw token price is not the right decision metric for autonomous engineering.

The investigation models expected cost as approximately:

```text
implementation attempts
+ review
+ repair
+ escalation
= expected cost per successfully completed task
```

A cheap model can be more expensive if it repeatedly fails. Conversely, a model that is much cheaper per token can remain cheaper even with a lower first-pass success rate if retries are bounded and a strong model remains available for recovery.

## Current capability evidence

Current coding-agent evidence shows that lower-cost models have become materially stronger. Common-harness long-horizon evaluations place several inexpensive models closer to frontier systems than simple token-price comparisons would suggest.

The working capability groups from the investigation are:

- **Tier A / frontier:** GPT-5.6 Sol, Claude Opus 5;
- **upper-B / escalation bridge:** GPT-5.6 Terra;
- **Tier B / capable autonomous implementers:** GPT-5.6 Luna, Gemini 3.7 Flash, DeepSeek V4 Pro, GLM-5.3-Flash, Kimi K3 and selected alternatives;
- **Tier C / cheap routine or specialist agents:** DeepSeek V4 Flash, Gemini Flash-Lite and specialist/smaller coder models;
- **Tier D:** deterministic tools rather than an LLM.

Public benchmarks are not treated as production truth. Current SWE/terminal evaluations have contamination, broken-task, harness and infrastructure sensitivity. Overlord therefore needs its own replay corpus before any production switch.

## Current price shape

Provider prices were reverified on 2026-08-28. The current OpenAI Standard short-context API price spread is especially relevant to the first trial:

| Model | Input / 1M | Cached input / 1M | Output / 1M |
|---|---:|---:|---:|
| GPT-5.6 Luna | $0.20 | $0.02 | $1.20 |
| GPT-5.6 Terra | $2.00 | $0.20 | $12.00 |
| GPT-5.6 Sol | $4.00 | $0.40 | $20.00 |

Sol's current reduced rate is promotional and should be reverified after 2026-11-21. Other providers also have temporary, cache-dependent, time-of-day, long-context, batch or host-specific pricing, so model name alone is insufficient for reliable accounting.

The detailed research document in the Overlord source repository contains the full normalized provider/model table and source list.

## Workload model

The source investigation defines four workload classes using actual Overlord history where possible:

- **Tiny:** focused maintenance, narrow adapter fixes, documentation/configuration;
- **Normal:** small features, ordinary multi-file bugs, adapter/application changes with tests;
- **Difficult:** DBOS lifecycle/recovery, persistence/concurrency, production failure investigation, architecture/security-sensitive changes;
- **Large:** broad migrations, major multi-module changes, and large unfamiliar repositories.

Expected one-attempt logical-input envelopes used for sensitivity analysis are approximately:

| Workload | Logical cumulative input | Output + reasoning |
|---|---:|---:|
| Tiny | 60K | 5K |
| Normal | 420K | 20K |
| Difficult | 2.25M | 60K |
| Large | 7.0M | 120K |

These are explicit modeling assumptions, not production measurements. The accepted production read-only smoke used only single-digit input tokens and is not representative of engineering work.

## Economic result

Under the central synthetic workload/success assumptions and a 70% cache-hit sensitivity, the Balanced task mix produced illustrative model spend of approximately:

| Architecture | Modeled cost / successful task |
|---|---:|
| Sol for everything | $1.99 |
| Luna -> Sol, full rediscovery | $0.91 |
| Luna -> deterministic tests -> seeded Sol | $0.73 |
| selective Terra planner + Luna + cheap review -> Sol | $0.68 |
| two DeepSeek V4 Flash attempts -> Sol | $0.77 |

These figures are **not production forecasts**. The success and handoff assumptions are synthetic. Their purpose is to show that cheap-primary routing has enough economic headroom to justify measured testing.

The same analysis found that a mandatory strong planner on every task can cost more than the cheap implementation it is intended to optimize. Strong planning should therefore be selective.

## Deterministic work first

Many actions should not consume an LLM call at all:

- repository tree and path classification;
- `git diff` inspection;
- ripgrep/search;
- AST/symbol and dependency extraction where available;
- formatting/lint/type checks;
- unit/integration tests;
- schema/static-security validation;
- CI status checks;
- coverage;
- deterministic patch application;
- structured extraction of compiler/test failures.

This reduces cost and produces more reliable evidence for routing and escalation.

## Context and caching

Autonomous agents repeatedly process prior context, so cumulative input can far exceed the amount of unique source code inspected.

The investigation therefore recommends:

- targeted retrieval rather than whole-repository serialization;
- revision-keyed repository maps;
- stable prompt prefixes;
- diff/evidence-scoped reviewers;
- compact structured failure output instead of large repeated logs;
- measured rather than assumed prompt-cache behavior;
- durable failure handoff packets for strong-model escalation.

At the modeled 70% cache sensitivity, cutting logical input by 50% reduces the illustrative Sol attempt cost by roughly 37% on Difficult tasks and 41% on Large tasks.

## Routing evidence

Difficulty and risk should be treated separately.

High-risk paths include DBOS durability/recovery, persistence/schema/migrations, GitHub authority/broker code, Developer isolation/security code, and production deployment/acceptance mechanisms. These can require stronger review even if implementation is small.

Good escalation signals are observable:

- repeated identical failures;
- no meaningful diff/test progress;
- exhausted token/dollar/step budgets;
- deterministic validation still failing after bounded repair;
- unexpected expansion into protected paths.

Model self-reported confidence is not sufficient routing evidence.

Provider outages and capability failures should also be separated: a timeout/429/5xx should trigger bounded same-tier provider/runtime fallback, not automatically consume premium model capacity.

## Accounting gap

Overlord already has a `ModelCall` persistence model and `DeveloperUsage` telemetry. The current bounded Developer path, however, persists aggregated Developer usage in `AgentRun.metadata` rather than demonstrating one canonical `ModelCall` row for every financially material Developer/model call.

The research also found that `total_input_tokens` does not currently have identical semantics across the OpenCode and OpenHands adapters.

Before routed production budgets are enforced, canonical accounting should preserve raw token components separately:

- uncached input;
- cache reads;
- cache writes;
- reasoning;
- output;
- provider-reported billed cost.

Provider/model/service tier, role, attempt ordinal, route reason and Task/AgentRun attribution should also be durable.

## Budget controls proposed

A future control-plane budget policy should support:

- maximum dollars per Task;
- maximum calls and Developer attempts;
- maximum cheap retries;
- maximum premium escalations;
- token/reasoning/output ceilings;
- wall-clock ceilings;
- daily/monthly/provider/premium-tier budgets;
- soft alerts and hard stops;
- emergency provider/model disable controls;
- spend attribution by Task and AgentRun.

Budget enforcement should remain in Overlord rather than being delegated to OpenCode or a model provider.

## Replay experiment before production change

The research recommendation is to move next to empirical evaluation, not production routing.

A paired corpus of roughly 15–25 historical Overlord tasks should compare at least:

1. Sol-only control;
2. Luna-only control;
3. deterministic preflight + Luna + bounded repair + Terra/Sol escalation;
4. optionally one cross-provider challenger after its exact host/pricing path is pinned.

The replay should use the production-like OpenCode/container/tool boundary and identical deterministic validators.

Proposed gates include:

- zero security-boundary violations;
- complete per-call cost attribution;
- zero accepted broken protected/high-risk changes;
- routed task completion at least about 90% of the Sol-only paired control;
- cost per successful task no more than about 65% of Sol-only before routing complexity is justified;
- premium escalation below 50% on Tiny + Normal work;
- measured reduction in premium rediscovery before crediting failure-handoff savings.

These gates should be fixed before results are observed.

## Cross-provider follow-up

If the same-provider routing experiment passes, the current priority challengers are:

1. DeepSeek V4 Pro / Flash;
2. GLM-5.3-Flash after exact host/pricing normalization;
3. Gemini 3.7 Flash using its post-introductory economics as the durable comparison;
4. Kimi/Qwen open-weight families where serving and cache economics are pinned;
5. other frontier/coding models where measured Overlord reliability justifies the cost.

The objective is not to find the cheapest token. It is to improve **cost per successful autonomous engineering task**.

## Next Step

Do not change the production Developer model route yet.

If the evaluation phase is approved, implement the smallest measurement prerequisites first:

1. canonical per-call Developer `ModelCall` accounting;
2. deterministic preflight/evidence capture;
3. historical-task replay harness;
4. budget/route telemetry;
5. only then a routing/escalation policy for the experiment.

The detailed research, pricing sources, benchmark analysis, workload model, cost calculations and routing-signal analysis live in the Overlord repository on the research branch/PR created for this investigation.

## Verification Record

- Last verified: `2026-08-28`.
- Verified against: current `Overlord/main`, canonical Phase 4 live-host note, recent Developer/DBOS PR history, current OpenCode documentation, and current provider pricing/model documentation.
- Historical Phase 4 live acceptance records were not rewritten by this investigation.
- Verified by: High Director.
