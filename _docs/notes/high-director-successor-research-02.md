---
title: High Director Successor Research 02 — Hosting and Cost Architecture
summary: Current-market research and first-pass cost model for hosting the successor control plane and on-demand Developer Agent workers while keeping infrastructure inexpensive and owner-controlled.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
owner: High Director
order: 117
permalink: /projects/notes/high-director-successor-research-02/
tags:
  - high-director
  - successor
  - research
  - hosting
  - cost
  - digitalocean
  - fly
  - aws
  - openhands
---

# High Director Successor Research 02 — Hosting and Cost Architecture

## Purpose

This is the second current-market research pass for the High Director successor. It focuses on how to host the proposed control plane and Developer Agent runtime cheaply enough to remain broadly comparable to a normal paid ChatGPT subscription plus modest infrastructure usage.

This memo does **not** include LLM token/API charges. Those will be modeled separately because model choice and usage pattern are intentionally provider-neutral and may change over time.

## Current Working Recommendation

For the first prototype/MVP, the strongest hosting pattern found is:

```text
Internet / phone client
        |
        v
small always-on control-plane VM
        |
        +--> API / authentication
        +--> Pydantic AI Manager
        +--> DBOS
        +--> Postgres
        +--> task scheduler / worker lifecycle controller
        +--> GitHub App / other tool services
        |
        v
private VPC network
        |
        +--> ephemeral Developer Worker 1 (OpenHands Agent Server)
        +--> ephemeral Developer Worker 2
        +--> ephemeral Developer Worker N
```

The key cost-control decision is that **Developer Agent compute should not remain running when no development task is active**.

The control plane remains continuously available for phone chat, notifications, task state, approvals, and scheduling. Developer workers are provisioned on demand, execute one isolated task/workspace, persist important state/results back to owner-controlled systems, and are destroyed when no longer required.

## Why Developer Workers Should Be Ephemeral

OpenHands currently recommends at least 4 GB RAM for local use. Its VM installation guide states that Ubuntu 24.04 with **2 vCPU and 4 GB RAM** is sufficient for a single user.

Sources:

- https://docs.openhands.dev/openhands/usage/run-openhands/local-setup
- https://docs.openhands.dev/openhands/usage/agent-canvas/backend-setup/vm

This worker size is much larger than the expected Manager/API control-plane footprint. Leaving several workers active continuously would therefore dominate infrastructure cost.

The Developer Agent task state should not depend on the VM surviving indefinitely. The durable source of truth should remain the control-plane database plus Git/GitHub artifacts, while the worker is a replaceable execution environment.

## DigitalOcean — Current MVP Hosting Front-Runner

DigitalOcean is currently the easiest platform to model for the first implementation because it combines simple VM pricing, per-second billing, an API for creating/deleting Droplets, user-data/cloud-init bootstrapping, VPC networking, and private Droplets.

### Current basic VM pricing

Official current Basic Droplet pricing includes:

| Size | Hourly | Monthly cap |
| --- | ---: | ---: |
| 1 vCPU / 1 GiB | $0.00893 | $6 |
| 1 vCPU / 2 GiB | $0.01786 | $12 |
| 2 vCPU / 2 GiB | $0.02679 | $18 |
| 2 vCPU / 4 GiB | $0.03571 | $24 |
| 4 vCPU / 8 GiB | $0.07143 | $48 |

Source: https://www.digitalocean.com/pricing/droplets

CPU Droplets are billed per second with a minimum 60-second/$0.01 charge, so destroying a worker after a task prevents paying the full monthly cap.

Source: https://docs.digitalocean.com/products/droplets/details/pricing/

### Programmatic worker provisioning

The DigitalOcean API can create and delete Droplets. Droplet creation supports `user_data`, allowing a worker to bootstrap automatically on first boot.

Sources:

- https://docs.digitalocean.com/reference/api/reference/droplets/
- https://docs.digitalocean.com/products/droplets/how-to/provide-user-data/

A worker bootstrap could therefore:

1. install/pull the approved OpenHands Agent Server image;
2. obtain short-lived task credentials from the control plane;
3. clone the assigned repository/branch;
4. start the Agent Server;
5. register its private endpoint with the Manager;
6. perform the assigned work;
7. push required Git/GitHub artifacts;
8. report completion;
9. be destroyed by the control plane.

A prebuilt snapshot/custom image could later reduce bootstrap latency if cloud-init proves too slow.

### Private worker networking

DigitalOcean supports private Droplets with VPC-only networking and no public IP. A VPC is not directly reachable from the public internet.

Sources:

- https://docs.digitalocean.com/products/droplets/details/private-droplets/
- https://docs.digitalocean.com/products/networking/vpc/

This is well aligned with the desired security boundary:

```text
phone/internet
     |
     v
public HTTPS control plane
     |
     v
private VPC
     |
     +--> Developer Agent workers
```

The workers should not need public inbound access. They do require controlled outbound internet access for GitHub, LLM/model calls if the worker makes them directly, package installation, web research, and other approved tools. The exact NAT/outbound design remains future security architecture work.

## First-Pass DigitalOcean Cost Model

These figures are infrastructure-only and exclude LLM API usage, domains, unusual data transfer, and optional services.

### Developer worker cost

At **$0.03571/hour** for a 2-vCPU/4-GB Basic Droplet:

| Aggregate active Developer Agent time/month | Approx. worker compute |
| ---: | ---: |
| 50 hours | $1.79 |
| 100 hours | $3.57 |
| 200 hours | $7.14 |
| 400 hours | $14.28 |

Aggregate hours include parallelism. For example, two workers running for five hours consume ten worker-hours.

### Control-plane candidate A — minimum-cost prototype

- 1 vCPU / 2 GiB: **$12/month**.
- 100 Developer worker-hours: **$3.57/month**.
- Compute subtotal: **$15.57/month**.

This is attractive but must be load-tested before selection because FastAPI/application services, DBOS, self-hosted Postgres, reverse proxying, notification workers, and future background services may make 2 GiB too constrained.

### Control-plane candidate B — more CPU headroom

- 2 vCPU / 2 GiB: **$18/month**.
- 100 Developer worker-hours: **$3.57/month**.
- Compute subtotal: **$21.57/month**.

This is likely a safer prototype starting point if Postgres is colocated, though real memory/CPU measurement is still required.

### Control-plane candidate C — 4-GB baseline

- 2 vCPU / 4 GiB: **$24/month**.
- 100 Developer worker-hours: **$3.57/month**.
- Compute subtotal: **$27.57/month**.

This has substantially more margin but already exceeds the desired subscription-like infrastructure floor before LLM usage.

## Backup Cost

DigitalOcean's basic automated backup pricing currently adds:

- weekly backups: **20%** of the Droplet's monthly cost;
- daily backups: **30%**.

Source: https://docs.digitalocean.com/products/backups/details/pricing/

Examples with weekly backups:

- $12 control plane -> approximately $2.40/month backup charge;
- $18 control plane -> approximately $3.60/month;
- $24 control plane -> approximately $4.80/month.

Ephemeral Developer Workers should generally not require full VM backups if their durable results are committed/persisted externally. Worker images/bootstrap definitions should be version-controlled or retained as reusable images instead.

## Resulting DigitalOcean Budget Examples

Excluding LLM calls:

| Configuration | Fixed/backup | 100 worker-hours | Approx. infrastructure total |
| --- | ---: | ---: | ---: |
| $12 control plane + weekly backups | $14.40 | $3.57 | **$17.97/month** |
| $18 control plane + weekly backups | $21.60 | $3.57 | **$25.17/month** |
| $24 control plane + weekly backups | $28.80 | $3.57 | **$32.37/month** |

This indicates that the infrastructure target is plausible if the smaller control-plane sizes work and Developer Workers are truly destroyed when idle.

## Fly.io — Slightly Cheaper Worker Compute

Fly.io currently prices a `shared-cpu-2x` Machine with 4 GB RAM at approximately **$0.0309/hour** / **$22.22/month** while running.

Source: https://fly.io/docs/about/pricing/

That gives approximately:

- 100 worker-hours: **$3.09**.

This is slightly cheaper than DigitalOcean's $3.57 for the same nominal 2-shared-CPU/4-GB worker period.

Fly Machines can therefore remain a strong alternative, particularly if stop/start behavior, fast machine provisioning, and regional placement prove better in prototype testing.

### Why it is not currently first

The current design benefits from simple full-VM lifecycle semantics, private worker networking, predictable cloud-init/image bootstrapping, and the option to run the whole stack on one provider initially. DigitalOcean's Droplet/VPC model is currently easier to reason about for a first implementation.

This is not a performance conclusion. Startup latency and OpenHands compatibility should be benchmarked on both before final selection.

## AWS Fargate — Technically Attractive, More Expensive

Fargate charges by vCPU and memory while a task is running. Current Linux/x86 US East pricing is approximately:

- $0.04048 per vCPU-hour;
- $0.004445 per GB-hour.

Source: https://aws.amazon.com/fargate/pricing/

A 2-vCPU/4-GB worker is therefore approximately **$0.09874/hour**, or roughly **$9.87 per 100 worker-hours**, before other AWS costs.

Fargate has excellent integration with IAM, ECS, networking, secrets, logs, and event-driven provisioning, and the owner already uses AWS. However, its raw worker compute is roughly 2.8x DigitalOcean's current 2-vCPU/4-GB Basic Droplet rate.

It remains a valid option if reduced operational complexity/security integration proves more valuable than the compute-price difference.

## OpenHands on Modal — Easy Scale-to-Zero but Costlier

OpenHands now publishes an official Modal deployment pattern. Its documented Agent Server uses 2 vCPU / 4 GB RAM.

OpenHands estimates:

- approximately **$0.14/hour** while running;
- approximately **$102/month** always-on;
- scale-to-zero available after idle periods;
- roughly 10–30 seconds cold start after scale-to-zero.

Source: https://docs.openhands.dev/openhands/usage/agent-canvas/backend-setup/modal

At the documented rate, 100 active worker-hours are approximately **$14**.

Modal is therefore attractive for operational simplicity and native scale-to-zero, but materially more expensive for sustained Developer Agent use than DigitalOcean or Fly shared compute.

The OpenHands Modal guide also notes that nested Docker is unavailable in that deployment pattern, which may limit development tasks that require Docker.

## Hetzner — Strong Cost Alternative Requiring Regional Price Validation

Hetzner has very low shared-compute pricing and supports APIs, private networks, firewalls, snapshots/backups, and cloud regions including Hillsboro, Oregon and Ashburn, Virginia.

Sources:

- https://www.hetzner.com/cloud/
- https://docs.hetzner.com/cloud/general/locations/

Its European cost-optimized CX23 is currently listed at 2 vCPU / 4 GB / 40 GB for **€5.99/month**, with hourly billing below the monthly cap.

Source: https://www.hetzner.com/cloud/cost-optimized/

However, the cost-optimized Intel/AMD plans are not available in the US locations. US locations use the regular shared AMD plans and have different pricing from Europe.

For a Vancouver-based owner, Hillsboro is geographically attractive, but the exact applicable US plan/currency price should be verified in an account-specific pricing comparison before selecting it.

Hetzner therefore remains a serious cost competitor, but DigitalOcean currently provides the cleaner first-pass dollar-denominated cost model for the desired worker size.

## Postgres Strategy

The architectural preference remains **owner-controlled Postgres** because DBOS uses the database as durable workflow state and the overall system goal is to keep important state under owner control.

### MVP option — colocate Postgres

For the prototype, Postgres can be colocated on the always-on control-plane VM to avoid a second fixed hosting bill.

Advantages:

- cheapest infrastructure floor;
- simplest networking;
- one backup target;
- fully owner-administered database.

Risks:

- one VM is a single failure domain;
- application and DB compete for RAM/CPU;
- scaling/recovery is less clean;
- maintenance of the VM can affect both API and durable workflow state.

The database files must therefore be backed up independently enough that loss of the VM does not destroy the durable system history.

### Managed Postgres alternatives

Managed Postgres could reduce operational risk but weakens the goal that most major infrastructure be directly controlled and may add a meaningful fixed cost.

Current examples:

- Neon has a free tier and usage-based paid compute/storage with no fixed minimum for its Launch-style usage model.
- Supabase Pro is currently $25/month and includes daily backups/other platform services.
- DigitalOcean managed Postgres begins substantially above the proposed self-hosted control-plane cost.

Sources:

- https://neon.com/pricing
- https://supabase.com/pricing
- https://www.digitalocean.com/pricing/managed-databases

For the first prototype, self-hosted Postgres is therefore preferred unless reliability testing demonstrates that this is an unacceptable operational burden.

## Proposed Worker Lifecycle

The desired Developer Worker lifecycle should be explicit and deterministic.

```text
Development Task queued
      |
      v
control plane requests worker VM
      |
      v
private worker boots from approved image/cloud-init
      |
      v
worker authenticates to control plane using short-lived bootstrap credential
      |
      v
OpenHands Agent Server becomes ready
      |
      v
Manager starts/continues developer task
      |
      v
code/tests/GitHub operations performed
      |
      v
important state/results persisted outside worker
      |
      v
worker marked disposable
      |
      v
VM destroyed
```

A worker must not be destroyed while it contains unpersisted changes that are the only copy of work. The lifecycle controller should require an explicit finalization check.

## Parallel Worker Model

Each Developer Agent should receive its own isolated worker/workspace unless prototype evidence proves that multiple safe isolated conversations can share one host without introducing file/process/security conflicts.

The simple model is:

```text
Task A -> Worker A -> repository branch A
Task B -> Worker B -> repository branch B
Task C -> Worker C -> repository branch C
```

The Manager/DBOS queue can cap simultaneous workers based on:

- configured maximum concurrency;
- current budget;
- provider quota;
- repository collision rules;
- task dependencies;
- current owner preference.

This turns concurrency into a controlled policy rather than an accidental cost multiplier.

## Cost Guardrails Required in the Product

The hosting architecture should include hard controls rather than relying on the Manager Agent to remember cost constraints.

Required controls should include:

- maximum concurrent Developer Workers;
- maximum worker lifetime;
- automatic idle timeout;
- automatic destruction after terminal task state;
- account-level daily/monthly worker-hour budget;
- alert when a worker remains alive unexpectedly;
- task-level estimated/actual compute time;
- LLM cost tracked separately from infrastructure cost;
- explicit approval before selecting a materially more expensive worker size;
- no orphan workers after workflow failures.

The control plane—not the LLM—must enforce these rules.

## Security Implications

The worker model creates a high-value execution environment because Developer Agents run code and access repositories/tools.

The first architecture should therefore aim for:

- private worker networking;
- no public inbound worker ports;
- short-lived bootstrap credentials;
- short-lived GitHub App installation tokens where possible;
- no permanent cloud/root credentials inside worker images;
- task-scoped secrets delivered only when required;
- worker destruction after task completion;
- outbound-network policy as a later hardening step;
- immutable/versioned base images/bootstrap definitions;
- audit events for provision/start/credential-delivery/destroy lifecycle actions.

A worker should be treated as potentially contaminated after running arbitrary repository code. Reuse should be avoided initially.

## Infrastructure Cost Versus LLM Cost

This pass strongly suggests that **LLM usage is likely to be the dominant variable cost**, not Developer Agent VM compute, if workers are ephemeral.

At current DigitalOcean pricing, even 200 aggregate worker-hours/month are only about $7.14. A coding agent can easily consume more than that in model API calls depending on model, context length, reasoning effort, and number of iterations.

Therefore infrastructure optimization beyond the proposed ephemeral-worker design is lower priority than:

- model selection/routing;
- prompt/context efficiency;
- caching/reuse;
- summarization/compaction;
- limiting unnecessary developer iterations;
- token/cost budgets;
- selecting expensive models only where their quality benefit justifies them.

The next cost model must therefore focus on current LLM API pricing and realistic Manager/Developer token usage.

## Current Ranking

| Hosting pattern | Current status | Reason |
| --- | --- | --- |
| DigitalOcean small control plane + ephemeral private Droplets | **Front-runner** | Simple API/VPC/cloud-init model, predictable pricing, cheap workers, easy first implementation |
| Fly Machines | Strong alternative | Slightly lower current shared-worker hourly rate; needs OpenHands/startup/networking prototype comparison |
| Hetzner Cloud | Strong cost challenger | Excellent headline pricing and US regions, but exact US plan pricing/availability differs from Europe and needs targeted validation |
| AWS ECS/Fargate | Strong operational/security alternative | Excellent AWS integration, but substantially higher raw worker compute cost |
| Modal OpenHands | Convenience alternative | Official OpenHands deployment and scale-to-zero, but higher active-hour cost and no nested Docker |
| Always-on OpenHands workers | Reject for MVP | Wastes most of the worker budget while idle and scales poorly with parallel agents |

## Prototype Decision Still Required

No hosting platform is selected yet.

Before choosing, run a small benchmark/prototype comparing at least DigitalOcean and Fly, and optionally Hetzner US, on:

- VM/Machine creation latency;
- OpenHands bootstrap/start latency;
- agent responsiveness;
- Docker/workspace compatibility;
- destroy/cleanup reliability;
- private networking/security configuration;
- API ergonomics;
- effective billed cost;
- behavior with two concurrent Developer Agents.

The prototype should use disposable test repositories and no production credentials beyond deliberately scoped test access.

## Next Research Pass

Research the **phone application, notifications, and voice layer** while keeping the backend architecture independent of the client.

Compare:

- PWA versus native/cross-platform mobile app;
- push notification options for iOS/Android;
- secure phone authentication;
- background notification behavior;
- microphone capture and speech-to-text;
- text-to-speech for short Manager summaries;
- streaming text/audio latency;
- whether voice processing should be device-side, self-hosted, or API-based;
- operating cost;
- ability to replace speech vendors without changing Manager/conversation state.

After that, perform the LLM provider/model/pricing research and build the first complete monthly cost scenarios.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [High Director Successor Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)

## Verification Record

- Last verified: `2026-08-09`
- Verified against: current official OpenHands, DigitalOcean, Fly.io, AWS Fargate, Modal/OpenHands, Hetzner, Neon, Supabase, and DigitalOcean managed-database documentation/pricing.
- Verified by: High Director
- Verification scope: OpenHands worker sizing, VM billing, worker lifecycle feasibility, private networking, backup pricing, Postgres hosting options, and first-pass infrastructure cost scenarios.
- Unverified areas: actual OpenHands worker CPU/RAM utilization, VM startup/bootstrapping latency, exact Hetzner US effective pricing, real concurrent-worker performance, control-plane memory requirements, and LLM API cost; these require prototype measurement or later research.
