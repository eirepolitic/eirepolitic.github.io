---
title: High Director Successor Research 05 — Persistent State, Memory, Backups, and Security
summary: Research and working design for owner-controlled durable state, retrieval, artifacts, audit history, backups, secrets, short-lived worker credentials, and network boundaries for the High Director successor.
section: notes
doc_type: note
status: active
created: 2026-08-09
updated: 2026-08-09
last_verified: 2026-08-09
owner: High Director
order: 120
permalink: /projects/notes/high-director-successor-research-05/
tags:
  - high-director
  - successor
  - research
  - postgres
  - memory
  - backup
  - audit
  - security
  - secrets
---

# High Director Successor Research 05 — Persistent State, Memory, Backups, and Security

## Purpose

This fifth research pass defines what must remain durable and owner-controlled outside any Manager or Developer Agent conversation.

The primary goal is that changing the LLM provider, replacing OpenHands, restarting the application, destroying a Developer Worker, or losing an individual agent conversation must **not** destroy the authoritative state of ongoing or completed work.

This note also defines the first-pass backup, secrets, audit, credential, and worker-network boundaries.

## Current Working Recommendation

Use three primary durable stores with distinct responsibilities:

```text
PostgreSQL
  -> authoritative structured application state
  -> conversations/messages
  -> tasks/dependencies
  -> plans/decisions/approvals
  -> agent/tool events
  -> worker/model/cost metadata
  -> notification state
  -> searchable summaries

Git / GitHub
  -> authoritative source code
  -> branches/commits/PRs
  -> CI/workflow evidence
  -> repository-native artifacts

S3-compatible object storage
  -> larger immutable/append-oriented artifacts
  -> database backups
  -> raw provider/tool payloads where retained
  -> diagnostic logs
  -> optional temporary audio
  -> exported audit records
```

For the first version:

- **Postgres should provide both transactional state and ordinary search.**
- Do **not** deploy a separate vector database.
- Add the `pgvector` extension only if prototype retrieval tests demonstrate a real semantic-search benefit.
- Use S3 for off-host backups and larger retained artifacts.
- Treat agent/provider conversations as replaceable execution contexts rather than application state.

## Core State Principle

The canonical state should answer these questions without opening an LLM-provider conversation:

- What did the owner ask for?
- What repository/system is involved?
- What plan was approved or inferred within policy?
- What tasks exist and which depend on others?
- Which Developer Agent is working on each task?
- What owner decisions were made?
- What tools were invoked?
- What branch/PR/workflow/deployment corresponds to the work?
- What is blocked and why?
- What did each model/provider cost?
- What is the next safe action?
- Is owner input required?
- Is the requested work complete?

If the database can answer those questions, replacing an agent conversation is operationally manageable.

## Why PostgreSQL Is the Current State-Store Front-Runner

PostgreSQL already supports the data types and search features needed for the initial product.

Relevant current capabilities include:

- normal relational tables and constraints;
- `jsonb` for structured provider/tool metadata that does not deserve a rigid column for every field;
- indexed JSON queries;
- built-in full-text search using `tsvector` / `tsquery`;
- GIN indexes for scalable text/search workloads;
- optional extensions such as `pgvector` if semantic retrieval is later justified.

Sources:

- https://www.postgresql.org/docs/current/datatype-json.html
- https://www.postgresql.org/docs/current/textsearch-controls.html
- https://www.postgresql.org/docs/current/gin.html
- https://github.com/pgvector/pgvector

For one owner's engineering history, adding Elasticsearch/OpenSearch plus a separate vector service at the beginning would create more operations, backups, credentials, and failure modes without evidence that native Postgres search is insufficient.

## Proposed Core Data Model

The exact schema is implementation work, but the architecture should separate stable domain records from append-oriented events.

### Identity and device state

```text
users
passkeys
sessions
devices
push_subscriptions
```

The initial deployment may have one owner account, but the schema should not hard-code authentication into one browser/device.

### Conversation state

```text
conversations
messages
message_attachments
conversation_summaries
```

A message should store canonical provider-neutral content plus metadata such as:

- author/role;
- conversation ID;
- task ID when applicable;
- timestamp;
- source mode (`text`, `voice_transcript`, `agent`, `tool`);
- model/provider for generated content;
- links to raw payload artifacts where retained.

### Project and repository state

```text
projects
repositories
repository_snapshots_or_refs
project_context_documents
```

Do not duplicate entire repositories into Postgres. Store Git references, selected extracted context, summaries, and indexes; Git/GitHub remains authoritative for code.

### Work management

```text
work_requests
plans
tasks
task_dependencies
task_status_history
agent_runs
worker_instances
```

A task is durable even if the current Developer Agent conversation/worker disappears.

### Human-in-the-loop state

```text
decisions
approval_requests
approvals
```

The system should persist:

- why an owner decision was required;
- alternatives presented;
- Manager recommendation;
- exact owner response;
- the policy/risk category that caused escalation;
- which blocked workflow resumed from that decision.

### Tool and execution evidence

```text
tool_calls
tool_results
external_resources
workflow_runs
validation_events
deployments
```

Large tool output should live in object storage where appropriate, with Postgres storing a digest, metadata, URI/key, retention category, and summarized result.

### Cost and model state

```text
model_profiles
model_price_profiles
model_calls
usage_daily
usage_monthly
budget_events
```

Price profiles must be versioned by effective date so historical cost remains reproducible even when providers change prices later.

### Audit state

```text
audit_events
security_events
credential_issuance_events
```

Important control-plane actions should be append-oriented and separately exported so deleting one database row is not sufficient to erase the only audit evidence.

## Event Model

The application should record high-value transitions as explicit events instead of reconstructing them later from logs.

Example:

```text
WORK_REQUEST_CREATED
PLAN_CREATED
PLAN_REVISED
TASK_CREATED
TASK_STARTED
WORKER_PROVISIONED
DEVELOPER_CONVERSATION_STARTED
TOOL_CALL_REQUESTED
TOOL_CALL_COMPLETED
OWNER_APPROVAL_REQUIRED
OWNER_DECISION_RECORDED
TASK_VALIDATION_FAILED
TASK_VALIDATION_PASSED
PR_OPENED
PR_MERGED
DEPLOYMENT_SUCCEEDED
TASK_COMPLETED
WORKER_DESTROYED
```

Each event should have a stable ID, timestamp, actor, task/conversation relationship, event type, structured payload, and correlation/idempotency key where applicable.

This event history is useful for the Manager, mobile timeline, troubleshooting, cost analysis, and security audits.

## Search and Memory Strategy

The first implementation should use a layered retrieval strategy rather than a single vague "memory" database.

### Layer 1 — structured retrieval

Use normal SQL for facts such as:

- active tasks;
- decisions for a repository;
- latest PR;
- unresolved blockers;
- previous failed attempts;
- model/cost history;
- latest verified architecture references.

### Layer 2 — PostgreSQL full-text search

Use built-in full-text search for:

- conversation messages;
- Manager summaries;
- task descriptions;
- decision rationales;
- retained tool-result summaries;
- documentation/context extracts.

PostgreSQL natively supports full-text vectors, queries, ranking, and GIN indexing.

Source: https://www.postgresql.org/docs/current/textsearch-controls.html

### Layer 3 — semantic retrieval only if justified

If real prototype tasks show that keyword/structured search misses useful historical context, add embeddings through `pgvector` inside the same database first.

`pgvector` supports exact and approximate nearest-neighbor search including HNSW and IVFFlat indexes.

Source: https://github.com/pgvector/pgvector

Do not add a dedicated external vector database merely because agent architectures commonly mention one.

## Context Construction

The Manager or Developer model should never receive the entire durable history automatically.

A context builder should select:

1. current work request;
2. current approved plan;
3. relevant task and dependencies;
4. unresolved decisions/constraints;
5. repository-specific rules and current Git refs;
6. recent conversation window;
7. selected prior summaries/events;
8. source files or retrieved excerpts required for the immediate step.

Then provider-specific caching can be applied to stable prefixes.

This keeps context cost controlled and makes provider switching easier.

## Conversation Summarization / Compaction

Long conversations should retain two things independently:

- the complete canonical event/message history in durable storage;
- one or more structured summaries optimized for future context assembly.

A summary should never replace the original historical record.

Suggested summary fields:

```text
objective
current_state
completed_work
open_tasks
owner_decisions
constraints
known_failures
repository_refs
next_safe_action
important_artifacts
```

The Manager can regenerate a summary if models improve or the existing summary proves inadequate.

## Artifact Storage

Use object storage for payloads too large or too immutable to justify database rows.

Potential artifact families:

```text
artifacts/
  tool-results/
  provider-raw/
  worker-logs/
  test-logs/
  transcripts/
  exports/
  backups/
  audit-exports/
```

Postgres stores metadata and references; object storage stores bytes.

Amazon S3 is a practical initial candidate because the owner already operates AWS resources and S3 supports versioning/lifecycle controls.

S3 Versioning preserves multiple variants of objects and can recover from accidental overwrite/delete.

Source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html

S3 Lifecycle can transition or expire retained objects automatically.

Source: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html

The architecture should use an internal object-store interface so S3 can later be replaced by another S3-compatible or self-hosted store if desired.

## Backup Strategy — Prototype

The first database backup design should be deliberately simple and regularly restore-tested.

### Initial layer

- nightly `pg_dump` in custom archive format;
- encrypt backup transport/storage;
- upload backup to a versioned object-store prefix;
- retain multiple daily/weekly generations with lifecycle rules;
- store checksum, database/schema version, creation timestamp, and backup job result;
- test `pg_restore` on a separate disposable database regularly.

PostgreSQL documents `pg_dump` plus `pg_restore` as a portable archive/restore mechanism.

Sources:

- https://www.postgresql.org/docs/current/app-pgdump.html
- https://www.postgresql.org/docs/current/app-pgrestore.html

### Later production layer

If recovery-point requirements become tighter, add base backups plus Write Ahead Log (WAL) archiving for point-in-time recovery.

PostgreSQL documents continuous WAL archiving as the mechanism for continuous backup/PITR.

Source: https://www.postgresql.org/docs/current/continuous-archiving.html

Do not implement PITR merely because it exists. Add it when measured value/risk justifies its additional operational burden.

## Backup Protection

S3 Object Lock can provide write-once/read-many retention for protected object versions and requires S3 Versioning.

Sources:

- https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-configure.html

For the prototype, Versioning + separate backup credentials may be sufficient. Object Lock is a later hardening option for backup/audit prefixes because retention configuration can intentionally prevent deletion and should not be enabled casually without a recovery/retention decision.

## Audit Export Strategy

The primary audit table lives in Postgres for queryability, but important audit records should periodically be exported to object storage in immutable batches.

Example:

```text
audit-exports/date=2026-08-09/hour=20/events.jsonl.gz
```

Each export can include:

- event IDs;
- time range;
- row count;
- content hash;
- previous-batch hash/reference.

This makes the audit trail harder to alter silently while keeping the implementation much simpler than introducing a dedicated SIEM for an initial single-owner system.

## Secret Classification

The platform will contain several classes of long-lived secrets:

- hosting/provider control API credentials;
- GitHub App private key/client secrets;
- LLM API credentials;
- speech API credentials;
- Web Push signing key;
- database credentials;
- optional AWS credentials;
- encryption/backup keys.

These must never be stored in messages, task prompts, normal Postgres application tables, Git repositories, or Developer Agent working directories.

## Secret-Management Options

Three reasonable approaches emerged.

### 1. Managed secret store

AWS Secrets Manager currently stores, audits, and can rotate secret material. Current pricing is approximately $0.40 per stored secret per month plus API requests.

Sources:

- https://aws.amazon.com/secrets-manager/
- https://aws.amazon.com/secrets-manager/pricing/

Advantages:

- low operational burden;
- access policies/auditing;
- rotation features;
- already within an AWS account the owner uses.

Disadvantages:

- another managed-cloud dependency;
- cross-cloud identity/bootstrap becomes relevant if the control plane is hosted elsewhere;
- even a small number of secrets adds fixed monthly cost.

### 2. Self-hosted secrets service

OpenBao is an open-source secrets manager managed under the Linux Foundation/OpenSSF ecosystem. It provides encrypted secret storage, policies, leases, revocation, and some dynamic-secret capabilities.

Sources:

- https://openbao.org/
- https://openbao.org/docs/concepts/policies/

Advantages:

- owner-controlled and vendor-neutral;
- strong policy/dynamic-secret model;
- API-based.

Disadvantages:

- another security-critical service to operate, back up, unseal, update, and recover;
- inappropriate to deploy casually on the same machine and then assume it protects against full host compromise.

### 3. Encrypted configuration with SOPS

SOPS supports encrypted YAML/JSON/ENV/INI/BINARY files and can use age or external KMS providers.

Sources:

- https://getsops.io/docs/
- https://getsops.io/docs/usage/identities/age/

Advantages:

- much less infrastructure;
- good fit for small static configuration sets;
- encrypted source/config can be version controlled safely when key handling is sound.

Disadvantages:

- does not automatically create a runtime dynamic-secret broker;
- decryption-key/bootstrap storage remains an important problem;
- less natural for issuing short-lived task credentials.

## Initial Secrets Recommendation

Do **not** install OpenBao in the first prototype unless a dynamic-secret requirement appears that simpler methods cannot satisfy.

The initial implementation should prototype either:

- managed secret storage, or
- a carefully controlled SOPS-based static bootstrap for the small number of long-lived control-plane credentials.

Then promote to a dedicated self-hosted secrets service if credential volume, dynamic leasing, audit requirements, or multi-host scale warrants it.

The most important security property is not the product name: **Developer Agent sandboxes must not receive long-lived platform credentials by default.**

## Credential Brokering

### GitHub

The control plane holds the GitHub App identity/private key.

When a worker requires direct Git access, the control plane can generate a GitHub App installation token limited to the relevant installation/repository/permissions where possible.

GitHub installation access tokens currently expire after **one hour** and can be revoked earlier.

Sources:

- https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation
- https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app

Prefer routing API operations such as PR management, workflow inspection, merging, secrets administration, and other high-value actions through the central GitHub tool service rather than giving every worker equivalent raw permission.

### Worker bootstrap

A new worker should receive a single short-lived/one-time bootstrap identity that allows it to:

- identify its assigned task;
- register itself;
- obtain only permitted task configuration;
- establish its Agent Server connection.

The bootstrap credential should expire quickly and become useless after registration.

### LLM provider credentials

This is an important prototype question.

OpenHands requires access to an LLM provider, but arbitrary repository code should not receive the provider's long-lived API key.

Prototype both of these patterns:

1. OpenHands Agent Server retains the LLM credential outside the code-execution sandbox while its workspace/container runs untrusted repository code.
2. A central LLM gateway/proxy receives OpenHands requests so the worker never stores the upstream provider key.

A dedicated LiteLLM proxy may become useful for the second pattern even though the Manager Agent does not otherwise require it.

Do not choose until the OpenHands sandbox/Agent Server isolation boundary is directly tested.

## Worker Network Boundary

Developer Workers should be treated as disposable, potentially contaminated execution environments.

Current DigitalOcean infrastructure supports VPC networking, cloud firewalls, and private Droplets with VPC-only inbound connectivity.

Sources:

- https://docs.digitalocean.com/products/networking/vpc/concepts/best-practices/
- https://docs.digitalocean.com/products/droplets/details/private-droplets/

Desired shape:

```text
Internet
   |
   v
HTTPS control plane
   |
   v
private VPC
   |
   +--> worker A
   +--> worker B
   +--> worker C
```

Workers should have:

- no public inbound service;
- control-plane-originated access only where feasible;
- explicit outbound access required for package repositories, GitHub, web research, or approved external services;
- no route to the control-plane database except through narrow application APIs;
- no access to another worker's task/workspace;
- automatic destruction at task completion/timeout.

Outbound network restrictions can be hardened after prototype measurement identifies what normal development actually requires.

## Control Plane Network Boundary

The public control plane should expose only the minimum owner-facing endpoints required for:

- HTTPS PWA/API access;
- Web Push registration/callback flows as required;
- authentication/WebAuthn;
- carefully authenticated worker control channels where necessary.

Postgres should not be internet-accessible.

Administrative access should use a deliberately restricted path rather than exposing SSH/database ports broadly.

## Sensitive Tool Policy

A model request and a tool authorization are separate decisions.

For every privileged tool call, the control plane should determine:

```text
requested action
actor/task
resource scope
credential required
policy classification
owner approval required?
idempotency key
maximum blast radius
```

The model may propose a tool call, but it does not decide whether the credential is released/executed.

This is especially important for:

- GitHub merges/deletions/secrets/variables;
- AWS changes;
- database writes outside the agent platform;
- credential/access-policy changes;
- destructive infrastructure operations;
- high-cost provisioning.

## Retention Policy Categories

Retention should be based on data type rather than one universal "save everything forever" setting.

Suggested initial categories:

### Durable indefinitely / until explicitly archived

- owner text messages;
- Manager messages;
- plans;
- owner decisions;
- task state;
- PR/workflow/deployment references;
- important summaries;
- cost records;
- high-value audit events.

### Medium-term diagnostic retention

- raw provider response JSON;
- detailed tool payloads;
- worker logs;
- test logs;
- transient screenshots/artifacts.

### Short-lived by default

- raw microphone recordings after successful transcription;
- temporary worker bootstrap artifacts;
- cached repository copies;
- expired short-lived credentials.

Retention windows should be configuration/policy and should be visible to the owner.

## Disaster-Recovery Goal

The minimum acceptable disaster-recovery test should prove that a fresh control-plane VM can be reconstructed from:

- infrastructure/bootstrap code;
- secret-recovery source;
- latest valid Postgres backup;
- object-storage artifacts;
- Git/GitHub repositories;
- documented configuration.

A recovery drill should verify that active tasks, owner decisions, conversation history, model-cost records, and repository references survive the loss of the original VM.

Do not call the system recoverable until this is tested.

## Current Security/State Architecture

The research stack now looks like:

```text
PWA + passkeys
       |
       v
HTTPS control plane
       |
       +--> Pydantic Manager
       +--> DBOS workflows
       +--> Postgres authoritative state/search
       +--> S3 artifacts/backups/audit exports
       +--> long-lived secret store
       +--> GitHub App tool broker
       +--> LLM capability router
       |
       v
private VPC
       |
       +--> disposable Developer Worker
               |
               +--> OpenHands Agent Server
               +--> isolated code workspace
               +--> short-lived task/Git credentials only
```

The exact product used for long-lived secrets and the exact OpenHands/LLM-key isolation design remain open prototype decisions.

## Prototype Tests Required

Before final architecture selection, test:

1. Rebuild a Manager context from Postgres without provider conversation history.
2. Replace a Developer Agent conversation and continue from durable task state.
3. Search past work using SQL/full-text only; measure whether semantic retrieval is actually missing.
4. Add `pgvector` in a test environment and compare retrieval quality before adopting it.
5. Restore a nightly `pg_dump` from object storage to a fresh Postgres instance.
6. Simulate loss of the control-plane VM and recover the application state.
7. Issue/revoke GitHub installation tokens and confirm repository/permission scope.
8. Run untrusted test repository code and verify it cannot read long-lived control-plane secrets.
9. Verify one worker cannot reach another worker or the database directly.
10. Compare SOPS/managed-secret/OpenBao operational burden before selecting the production secret store.
11. Verify raw voice audio deletion after transcription.
12. Verify audit export hashes/counts against Postgres events.

## Next Research Pass

The next pass should compare **existing integrated platforms/products that could replace portions of this architecture without reintroducing unacceptable lock-in**.

Research should ask:

- Does an existing self-hostable AI coding/control platform already provide the Manager hierarchy, queues, approvals, mobile-friendly UI, durable tasks, or tool gateway?
- Can OpenHands alone cover more of the control plane than currently assumed?
- Are products such as agent orchestration UIs or coding-agent platforms reusable as replaceable components rather than the system of record?
- Which components are clearly cheaper/safer to build ourselves versus adopt?
- Are there established open protocols such as MCP or ACP that should be internal extension boundaries?

After that comparison, the research programme should produce a consolidated architecture recommendation and an MVP implementation plan with explicit decisions for the owner.

## Related Documents

- [High Director Successor — Initial System Concept](/projects/notes/high-director-successor-concept/)
- [Research 01 — Agent Runtime and Control Plane](/projects/notes/high-director-successor-research-01/)
- [Research 02 — Hosting and Cost Architecture](/projects/notes/high-director-successor-research-02/)
- [Research 03 — Mobile, Notifications, Authentication, and Voice](/projects/notes/high-director-successor-research-03/)
- [Research 04 — LLM Provider Strategy and Cost](/projects/notes/high-director-successor-research-04/)

## Verification Record

- Last verified: `2026-08-09`
- Verified against: current PostgreSQL JSON/full-text/backup/WAL documentation; pgvector repository documentation; AWS S3 Versioning/Lifecycle/Object Lock documentation; AWS Secrets Manager documentation/pricing; OpenBao documentation; SOPS documentation; GitHub App installation-token documentation; DigitalOcean VPC/private-Droplet/firewall documentation.
- Verified by: High Director
- Verification scope: authoritative state boundaries, search approach, optional semantic retrieval, backup/recovery layers, artifact storage, secret-management options, short-lived GitHub credentials, worker isolation, retention, and audit architecture.
- Unverified areas: exact Postgres schema/index design, retrieval quality, backup timings, secret-store operational burden, OpenHands sandbox isolation from LLM credentials, outbound-network requirements, and actual recovery time; these require prototype testing.
