---
title: Overlord — Developer Model Options Report
summary: Plain-English decision report comparing the practical ways Overlord could lower autonomous Developer model cost while keeping reliable software-engineering capability.
section: notes
doc_type: note
status: active
created: 2026-08-29
updated: 2026-08-29
last_verified: 2026-08-29
owner: High Director
order: 150
permalink: /projects/notes/overlord-developer-model-options-report/
tags:
  - overlord
  - developer
  - models
  - cost
  - decision-report
  - research
---

# Overlord — Developer Model Options Report

## Short version

Overlord does **not** appear to need the most expensive AI model for every software-development task.

The most promising approach is:

```text
Use deterministic tools first
        ↓
Use a cheaper capable model for ordinary development work
        ↓
Run tests and other automatic checks
        ↓
If it succeeds, stop
        ↓
If it gets stuck or the task is risky, move to a stronger model
```

For the first real-world experiment, the simplest version is to stay with the provider already accepted in production:

```text
GPT-5.6 Luna
   ↓ if needed
GPT-5.6 Terra
   ↓ if needed
GPT-5.6 Sol
```

This lets us test whether routing actually saves money **without simultaneously introducing another provider, another credential path, and another operational dependency**.

The research suggests this approach could reduce model spending substantially, but the cost figures are still estimates. The next decision should be based on replaying real historical Overlord tasks and measuring success, retries, tokens, latency, and actual provider charges.

---

## What problem are we trying to solve?

Overlord's Developer agents need to be able to do real software-engineering work autonomously:

- inspect an unfamiliar repository;
- understand a task;
- find the relevant code;
- edit multiple files;
- write or update tests;
- run tests and other checks;
- diagnose failures;
- repair the change;
- know when to escalate.

The problem is that the most capable models can be much more expensive than cheaper models.

The question is therefore not:

> Which model has the lowest token price?

It is:

> Which setup gives us the lowest **cost per successfully completed development task** while remaining reliable?

A cheap model that fails five times can be more expensive than a stronger model that succeeds once. But a cheap model that handles most normal work and only occasionally needs help can be dramatically cheaper overall.

---

# The realistic options

## Option 1 — Use the strongest model for everything

### How it works

Every Developer task starts and finishes on a frontier model such as GPT-5.6 Sol or Claude Opus 5.

### Advantages

- simplest routing architecture;
- strongest capability available immediately;
- fewer decisions about escalation;
- good fit for difficult debugging and unfamiliar architecture.

### Disadvantages

- highest model cost;
- expensive capability is spent on trivial work;
- formatting fixes, simple tests, documentation, and ordinary bugs all pay frontier prices;
- little opportunity to learn which tasks genuinely require premium capability.

### Best fit

A good control case and emergency fallback, but probably not the cheapest sensible default.

### Research view

**Reliable but probably unnecessarily expensive.**

---

## Option 2 — Use one cheaper capable model for everything

### How it works

A lower-cost model such as GPT-5.6 Luna handles every development task, including retries.

### Advantages

- extremely simple;
- very low token cost;
- no routing logic;
- current coding benchmarks show surprisingly strong performance from some inexpensive models.

### Disadvantages

- difficult debugging and architecture work can expose larger capability gaps;
- repeatedly retrying the same weak approach can waste time;
- some failures will be highly correlated: asking the same model again may simply reproduce the same mistake;
- no stronger recovery path.

### Best fit

Useful as a benchmark/control, but risky as the only autonomous Developer capability.

### Research view

**Cheap, but not enough protection against hard failures.**

---

## Option 3 — Cheap primary model, stronger model when needed

### How it works

A cheaper capable model gets the first attempt. Automatic checks determine whether it is making progress. A stronger model is brought in only when necessary.

Example:

```text
Luna
  ↓ failure or high-risk task
Terra
  ↓ difficult failure / architecture / recovery
Sol
```

### Advantages

- captures most of the potential savings;
- strong model remains available for difficult work;
- can stay with one provider initially;
- easy to place hard limits on cheap attempts;
- fits Overlord's existing `efficient / balanced / frontier` capability concept.

### Disadvantages

- needs routing and escalation logic;
- needs reliable accounting so we know what each attempt costs;
- poor escalation rules could waste time before reaching the stronger model;
- we need evidence that failed cheap attempts leave useful information for the next model.

### Best fit

Ordinary development work with a reliable premium recovery path.

### Research view

**Best first option to test.**

---

## Option 4 — Cheap model plus automatic tests, premium model only after failures

### How it works

The inexpensive model writes the change. Deterministic tools judge it:

- tests;
- lint;
- type checking;
- formatting;
- schema validation;
- CI checks;
- static analysis.

A premium model is called only when those checks show the cheap attempt cannot finish the task cleanly.

### Advantages

- avoids paying another AI to review things a test suite can prove;
- very inexpensive for well-tested tasks;
- objective failure signals are better than asking the model whether it is confident;
- naturally produces information for escalation.

### Disadvantages

- tests do not prove every architectural or security property;
- weak test coverage can create false confidence;
- risky changes still require stronger semantic review.

### Best fit

Well-tested routine engineering tasks.

### Research view

**Likely part of the recommended architecture, rather than a separate competing architecture.**

---

## Option 5 — Strong planner, cheaper implementer

### How it works

A strong model first studies the task and creates a plan. A much cheaper model then performs the implementation.

### Advantages

- can reduce expensive rediscovery by weaker models;
- potentially useful on difficult or unfamiliar work;
- separates architecture reasoning from repetitive implementation.

### Disadvantages

- a strong planning call can cost more than an entire cheap implementation attempt;
- wasteful for small and normal tasks;
- the cheap implementer may still misunderstand the plan;
- adds another model call to every task if used indiscriminately.

### Best fit

Selective use on difficult or architecture-heavy tasks.

### Research view

**Useful escalation tool, but not a good default for every task.**

---

## Option 6 — Multiple cheap Developers compete before using a premium model

### How it works

Two or more inexpensive agents independently attempt the same task. A test suite or stronger judge picks the best result. Premium capability is used only if they all fail.

### Advantages

- cheap calls are inexpensive enough that several can still cost less than one frontier call;
- independent approaches can recover from one model taking the wrong path;
- useful when solutions can be judged deterministically.

### Disadvantages

- failures can be correlated;
- several agents may repeat the same mistake;
- extra latency;
- more orchestration and accounting;
- can become a wasteful swarm if attempts are not tightly bounded.

### Best fit

Tasks with strong deterministic validation and evidence that a second attempt genuinely recovers failures.

### Research view

**Economically possible, but should not be the first architecture implemented.**

---

## Option 7 — Frontier primary model with cheap reviewers

### How it works

The expensive model performs every implementation. Cheap models independently inspect the final diff and test results.

### Advantages

- strong implementation quality from the start;
- cheap review is inexpensive;
- may catch mistakes the primary model misses.

### Disadvantages

- does very little to reduce the largest cost: the frontier implementation itself;
- still pays premium prices on trivial work.

### Best fit

Reliability improvement where cost reduction is secondary.

### Research view

**Potentially useful for quality, but not a strong cost-saving strategy.**

---

## Option 8 — Use cheaper models from other providers

### How it works

Instead of—or alongside—OpenAI, Overlord routes work to lower-cost models from providers such as DeepSeek, Google, Z.ai/GLM, Moonshot/Kimi, or hosted open-weight model providers.

### Interesting candidates from the research

- DeepSeek V4 Pro / Flash;
- Gemini 3.7 Flash;
- GLM-5.3-Flash;
- Kimi K3;
- newer Qwen coding/agent families.

### Advantages

- some models are extremely inexpensive;
- several now perform surprisingly well on long-horizon coding benchmarks;
- reduces dependency on one model provider;
- open-weight models create additional hosting choices.

### Disadvantages

- provider integration and credentials become more complex;
- same model can behave differently across hosts;
- pricing can vary by time of day, caching, host, or context size;
- more operational and monitoring work;
- difficult to know whether savings come from routing or simply from changing providers unless tested separately.

### Best fit

A second evaluation phase after we have a measured same-provider routing baseline.

### Research view

**Very interesting, but probably the second experiment rather than the first.**

---

# Simple comparison

| Option | Cost potential | Reliability | Complexity | Recommended now? |
|---|---|---|---|---|
| Frontier model for everything | Low savings | Very high | Low | Control/fallback |
| Cheap model for everything | Very high savings | Uncertain on hard work | Low | Benchmark only |
| Cheap primary -> strong escalation | High savings | High if routing works | Medium | **Yes — first trial** |
| Cheap primary + automatic tests | High savings | High on well-tested work | Medium | **Yes — core part of trial** |
| Strong planner -> cheap implementer | Medium/high | Potentially high | Medium/high | Selective only |
| Multiple cheap attempts | Potentially high | Depends on failure diversity | High | Later experiment |
| Frontier primary + cheap review | Low savings | Potentially very high | Medium | Quality option, not cost option |
| Multi-provider cheap routing | Potentially very high | Model/provider dependent | High | Second phase |

---

# What do the rough numbers say?

The detailed technical cost model used a Balanced mix of Tiny, Normal, Difficult, and Large development tasks.

Under its central assumptions and a 70% cache-hit sensitivity, the illustrative model spend per successful task was approximately:

| Approach | Modeled cost / successful task |
|---|---:|
| Sol for everything | **$1.99** |
| Luna then Sol if needed | **$0.91** |
| Luna + automatic checks then Sol | **$0.73** |
| selective Terra planning + Luna + review + Sol | **$0.68** |
| two DeepSeek Flash attempts then Sol | **$0.77** |

These are **not production forecasts**.

They depend on assumptions about:

- how often each model succeeds;
- how much prompt caching occurs;
- how much information can be reused after a failed attempt;
- how large real Overlord tasks are;
- how many retries occur.

The important result is not that `$0.73` is the future cost of a task. The important result is that the price gap is large enough that a cheaper first attempt can fail fairly often and still leave room for a strong-model recovery without automatically becoming more expensive than starting with the frontier model.

---

# Why automatic tools matter so much

A large part of software development does not require AI reasoning.

Overlord can use ordinary tools to do things such as:

- search the repository;
- list changed files;
- inspect a Git diff;
- find symbols;
- run tests;
- run type checking;
- run linting and formatting;
- validate database migrations;
- check CI status;
- extract the important lines from an error log.

Every job handled deterministically is:

- cheaper;
- easier to audit;
- more repeatable;
- less likely to hallucinate.

This is why the recommended architecture starts with deterministic preprocessing rather than immediately asking another AI model to inspect everything.

---

# Why context size matters

An autonomous Developer does not just read the repository once.

It repeatedly sees some combination of:

- task instructions;
- source files;
- tests;
- previous conversation;
- tool output;
- error messages;
- its own earlier changes.

That means a task that only needs tens of thousands of unique tokens can process hundreds of thousands—or millions—of tokens over a long agent session.

The research therefore recommends:

- retrieving only relevant files;
- maintaining a compact repository map;
- summarizing large test failures;
- giving reviewers the final diff rather than the entire conversation;
- keeping repeated prompt prefixes stable so provider caching can work;
- handing a stronger model a compact failure packet rather than making it rediscover everything from scratch.

On larger tasks, this can reduce model cost by a large percentage even without changing models.

---

# What should go directly to a stronger model?

The cheapest model should not automatically receive every task.

Some changes are risky even when they are small.

Examples for Overlord include:

- DBOS durability, recovery, and concurrency;
- database schemas and migrations;
- GitHub authority and `GitHubBroker` boundaries;
- Developer-container isolation and security;
- production deployment and acceptance workflows;
- difficult production incidents;
- major architecture changes;
- recovery after cheaper models repeatedly fail.

These tasks should be allowed to start at Terra/Sol-class capability or require stronger review.

The key distinction is:

- **difficulty** — how hard is this to solve?;
- **risk** — how expensive would a convincing but incorrect solution be?

Those are not the same thing.

---

# What should cause escalation?

Good escalation signals are things Overlord can observe:

- the same test failure keeps returning;
- the same patch keeps failing;
- the model is no longer making progress;
- the task exceeds its call/token/dollar limit;
- a supposedly simple change unexpectedly spreads across many modules;
- a protected security/authority path becomes involved;
- deterministic validation still fails after a bounded repair attempt.

Things that should **not** independently decide escalation:

- the model saying it is confident;
- the task description containing the word "simple";
- repository size alone;
- one large test-failure count without understanding the root cause.

---

# What about provider outages?

A provider failure is not the same as a model being incapable.

For example:

- timeout;
- rate limit / HTTP 429;
- temporary HTTP 5xx;
- provider outage.

These should normally trigger a bounded retry or another provider/model in the **same capability class**.

They should not automatically cause Overlord to spend money on a frontier model.

---

# Why we are not recommending a big multi-agent swarm yet

OpenCode already supports subagents and different models, so it would technically be possible to build something like:

```text
planner
  -> researcher
  -> two implementers
  -> reviewer
  -> judge
  -> repair agent
```

The problem is not whether that can be built.

The problem is whether every extra role produces enough additional successful work to justify:

- more tokens;
- more latency;
- more failure modes;
- more accounting complexity;
- harder debugging;
- weaker cost attribution.

The current Overlord adapter also aggregates OpenCode session usage, so hiding several financially important models inside one OpenCode session would make budget accounting less clear.

For now, simpler explicit Overlord-controlled attempts are easier to measure and govern.

---

# Budget controls we will eventually need

If routing is implemented, Overlord should be able to set hard limits such as:

- maximum dollars per task;
- maximum model calls;
- maximum repair attempts;
- maximum cheap retries;
- maximum premium-model escalations;
- maximum tokens;
- maximum execution time;
- daily and monthly model budgets;
- provider-specific limits;
- emergency model/provider stop controls.

Every financially important call should be attributable back to:

```text
Task
  -> AgentRun
      -> provider
      -> model
      -> role
      -> attempt
      -> tokens
      -> actual cost
```

That accounting is not completely wired into the current bounded Developer path yet, so it is one of the prerequisites for a real routing experiment.

---

# Recommended next experiment

Before changing production routing, take roughly 15–25 real historical Overlord development tasks and replay them through several setups.

At minimum compare:

### Control A

**Sol only**

This tells us what the premium baseline can actually achieve and what it costs.

### Control B

**Luna only**

This tells us how capable the cheaper model really is under Overlord's actual OpenCode environment.

### Candidate route

**Deterministic preflight -> Luna -> automatic validation -> Terra/Sol escalation**

This is the proposed first production-style routing experiment.

### Optional challenger

One lower-cost external candidate such as DeepSeek V4 or GLM-5.3-Flash after its provider/host/pricing path is fixed.

---

# What would count as a successful experiment?

The detailed research proposes setting the rules **before** seeing results.

A sensible starting gate is:

- zero security-boundary violations;
- every paid model call accounted for;
- no broken high-risk change accepted as successful;
- routed system completes at least about 90% as many paired tasks as the Sol-only control;
- model cost per successful task is no more than about 65% of Sol-only;
- premium escalation stays below 50% for Tiny and Normal tasks;
- failed cheap attempts demonstrably reduce the amount of rediscovery needed by the stronger model before we claim handoff savings.

If routing only saves 20% while making the system much harder to operate, it may not be worth it.

If it saves 50–65% while maintaining nearly the same success rate, it becomes much more compelling.

---

# Current recommendation

## First choice to test

**Deterministic tools + Luna primary + Terra/Sol escalation.**

Why:

- potentially large savings;
- strong premium fallback remains available;
- minimal provider/integration change;
- easiest version to measure cleanly;
- preserves the existing accepted architecture.

## Second phase

If that works, test lower-cost cross-provider candidates such as:

1. DeepSeek V4 Pro / Flash;
2. GLM-5.3-Flash;
3. Gemini 3.7 Flash using durable rather than temporary pricing assumptions;
4. Kimi/Qwen open-weight options where the exact serving provider is pinned.

## Do not do yet

- do not replace production routing immediately;
- do not build a large multi-agent swarm;
- do not give every task a strong planner;
- do not allow unlimited cheap retries;
- do not rely on model self-confidence for escalation;
- do not place additional provider/AWS/GitHub/database credentials inside Developer containers;
- do not choose a provider from headline token price alone.

---

# Bottom line

The research suggests that **using the strongest model for every task is probably paying for capability we often do not need**.

A cheaper capable model can be given the ordinary work, automatic tools can judge much of the result, and expensive models can be reserved for the situations where they actually add value.

The economics look promising enough that this is worth testing. They are not yet strong enough to justify changing production without a small Overlord-specific replay experiment.

The next engineering investment should therefore be **measurement first, routing second**.

## Related research

For the technical evidence, detailed provider/model tables, benchmark discussion, workload assumptions, cost formulas, routing signals, and budget-design details, see the companion note:

- [Overlord — Developer Model Cost and Routing Investigation](/projects/notes/overlord-developer-model-cost-routing-investigation/)

## Verification record

- Last verified: `2026-08-29`.
- Based on: the completed Overlord Developer model cost/routing research merged into the source repository, current provider pricing verified during that investigation, and the existing production architecture/security constraints.
- This report is intentionally written for decision-making and browsing rather than implementation.
