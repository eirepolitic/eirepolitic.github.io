---
title: Overlord Phase 2 — Developer Agent Benchmark Harness
summary: Implementation record for the first Phase 2 slice, adding replaceable OpenHands and OpenCode Developer Agent adapters plus an offline-tested comparison harness and explicitly guarded real benchmark runner.
section: notes
doc_type: note
status: active
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
owner: High Director
order: 131
permalink: /projects/notes/overlord-phase-2-developer-benchmark-harness/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - openhands
  - opencode
  - benchmark
---

# Overlord Phase 2 — Developer Agent Benchmark Harness

## Outcome

The first Phase 2 Developer Agent slice is complete.

Overlord now has two real coding-runtime adapters behind the existing provider-neutral `DeveloperAgentPort`:

- OpenHands Agent Server;
- OpenCode headless server.

A normalized benchmark harness can run the same `DeveloperTaskSpec` through either runtime and collect comparable evidence without making either runtime's native session model canonical.

Normal CI remains offline with respect to both coding runtimes. It does not start OpenHands or OpenCode, does not make a hosted coding-model call, and does not require a provider credential.

**No default Developer Agent has been selected.** The implementation deliberately stops at benchmark readiness. A real identical-task benchmark must produce sufficient quality/cost/operability evidence before OpenHands or OpenCode becomes the preferred runtime.

## Source Delivery

- Repository: `Overlord`
- Pull request: `#10` — `feat: add Phase 2 Developer Agent benchmark harness`
- Exact final PR head: `cb3895c4dc6807ab4f12f0c3f9dd7e2ee2b2b6c1`
- Exact PR-head permanent CI: run `#140` — `success`
- Final merged `main` commit: `7c0867f8b31de5132707714decdf6540fb931307`
- Exact post-merge permanent CI: run `#141` — `success`

The final PR head passed the complete permanent CI workflow before merge. The resulting squash commit on `main` passed the same workflow again after merge.

No runtime dependency was added for OpenHands or OpenCode, so `uv.lock` did not require a refresh. The adapters use a small standard-library HTTP boundary and communicate with already-running local runtime servers.

## Developer Agent Contract

The existing Overlord-owned `DeveloperAgentPort` remains the application-facing coding-runtime boundary.

The normalized operations are:

```text
create_task
send_instruction
stream_events
get_status
request_summary
cancel
resume
get_usage
finalize
```

`DeveloperTaskSpec` remains provider-neutral and includes the requested work, repository/branch references, capability tier, and optional metadata.

Runtime session/conversation IDs remain external references. They do not replace canonical Overlord Task or AgentRun identifiers.

## Shared HTTP Boundary

`src/overlord/adapters/developer/http.py` adds a small async JSON HTTP abstraction:

```text
JsonHttpClientPort
UrllibJsonClient
HttpResponse
```

The concrete client uses Python's standard library and executes blocking HTTP calls through `asyncio.to_thread()`.

This keeps Overlord independent of OpenHands/OpenCode SDK packages and makes adapter behavior fully injectable for offline contract tests.

## OpenHands Adapter

`src/overlord/adapters/developer/openhands.py` implements `DeveloperAgentPort` against an already-running OpenHands Agent Server.

The adapter currently:

1. sends the normalized task prompt through the server's OpenAI-compatible chat surface;
2. captures the returned OpenHands conversation ID as an external runtime reference;
3. sends follow-up instructions to the same conversation;
4. reads native conversation state for status/evidence snapshots;
5. maps exposed runtime events into provider-neutral `DeveloperEvent` values;
6. keeps the final assistant response as a normalized summary;
7. normalizes prompt/output token counts when exposed;
8. normalizes accumulated cost when exposed;
9. returns raw final conversation evidence only as adapter metadata.

An optional OpenHands Agent Server session key is supplied at runtime only. It is not committed to source control or canonical state.

## OpenCode Adapter

`src/overlord/adapters/developer/opencode.py` implements the same port against an already-running `opencode serve` headless server.

The adapter currently:

1. creates an OpenCode session;
2. sends the identical normalized task prompt as a text message;
3. sends later instructions through the same session;
4. maps session message text into provider-neutral events;
5. reads normalized session status;
6. extracts the most recent assistant text as a summary;
7. normalizes token/cost metadata when exposed;
8. captures session details as optional runtime metadata;
9. captures the session file diff as final benchmark evidence.

OpenCode session objects remain adapter-local/external metadata rather than canonical Overlord work state.

## Runtime Configuration

Phase 2 adds local-only runtime settings:

```text
OVERLORD_DEVELOPER_OPENHANDS_BASE_URL=http://127.0.0.1:8001
OVERLORD_DEVELOPER_OPENHANDS_MODEL=openhands_overlord_benchmark
OVERLORD_DEVELOPER_OPENCODE_BASE_URL=http://127.0.0.1:4096
OVERLORD_RUN_REAL_DEVELOPER_BENCHMARK=0
```

These defaults do **not** install, launch, or provision either coding runtime.

A real benchmark requires the operator to deliberately run and configure each server separately.

## Benchmark Harness

`src/overlord/application/developer_benchmark.py` contains the provider-neutral comparison harness.

For each runtime, it records:

```text
runtime
agent_task_id
duration_seconds
status
summary
normalized usage
runtime final evidence
events_observed
benchmark evidence
```

`BenchmarkEvidence` has explicit fields for:

- task completion;
- test success;
- Git-operation success;
- resume/recovery success;
- permission-control verification;
- sandbox-isolation verification;
- secret-exposure verification;
- workspace-cleanup verification;
- peak CPU observation;
- peak memory observation;
- reviewer notes.

Unmeasured evidence remains `None`. The harness does not assign optimistic values or invent runtime capabilities.

## No Automatic Runtime Selection

The harness intentionally contains no ranking or winner-selection policy.

The approved research contract requires the default Developer Agent to be selected from repeated, identical repository-task evidence covering more than raw completion.

The broader decision must consider:

- provisioning/startup time;
- task completion rate;
- restart/resume reliability;
- event-stream usefulness;
- code/test quality;
- tool and permission control;
- Git operations;
- model/provider switching;
- token/cost observability;
- sandbox isolation;
- secret-exposure risk;
- workspace cleanup;
- adapter implementation/maintenance effort;
- CPU/RAM use;
- total task cost.

OpenHands and OpenCode therefore remain equal replaceable candidates after this implementation package.

## Offline Contract Tests

`tests/contract/test_developer_runtime_adapters.py` exercises both real adapters with an injected fake JSON HTTP client.

The OpenHands contract test proves:

- runtime conversation-ID normalization;
- status mapping;
- event mapping;
- final summary mapping;
- token/cost normalization;
- runtime final-evidence mapping;
- session/API authorization header behavior without contacting a server.

The OpenCode contract test proves:

- runtime session-ID normalization;
- normalized prompt submission;
- status mapping;
- event/summary mapping;
- token/cost normalization;
- session diff evidence;
- no real OpenCode process/network dependency.

`tests/unit/test_developer_benchmark.py` proves:

- the same task can be compared across multiple `DeveloperAgentPort` implementations;
- elapsed time is normalized;
- benchmark evidence remains explicit;
- unknown runtimes are rejected;
- the harness does not need a preferred runtime to operate.

## Explicit Real-Benchmark Boundary

`scripts/benchmark_developer_agents.py` provides the real comparison path.

The script exits unless:

```text
OVERLORD_RUN_REAL_DEVELOPER_BENCHMARK=1
```

is deliberately enabled.

It also requires an explicit benchmark task description:

```text
OVERLORD_DEVELOPER_BENCHMARK_DESCRIPTION
```

Optional inputs include task title, repository reference, branch/worktree reference, and an OpenHands server session key supplied only through the process environment.

The script runs the same `DeveloperTaskSpec` against OpenHands and OpenCode and prints JSON comparison evidence.

It does not:

- provision either runtime;
- install either runtime;
- create a remote worker;
- create recurring cloud infrastructure;
- store provider credentials;
- declare a runtime winner.

A real benchmark may cause model/tool costs inside the separately configured coding runtimes, so execution remains a deliberate operator action under the existing spending policy.

## CI Gate

Permanent CI run `#140` succeeded on exact final PR head:

`cb3895c4dc6807ab4f12f0c3f9dd7e2ee2b2b6c1`

Permanent CI run `#141` succeeded on exact merged `main` commit:

`7c0867f8b31de5132707714decdf6540fb931307`

Both gates included:

```text
docker compose config --quiet
PostgreSQL startup/readiness
uv sync --locked --all-groups
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run alembic upgrade head
uv run pytest
```

The full suite also retains the existing Phase 0/1 tests for canonical persistence, policy/security boundaries, Pydantic AI offline behavior, DBOS restart/resume/idempotency, and the local Manager HTTP loop.

## Temporary Diagnostic Cleanup

One temporary branch-only Ruff diagnostic workflow was used after the first Phase 2 CI run found three style findings.

The exact findings were limited to:

- one line-length violation;
- one unused `field` import;
- one unused `AsyncIterator` import.

They were fixed, and the temporary workflow/diagnostic output were deleted before the final green PR head.

The merged workflow tree continues to contain only the permanent `ci.yml` workflow.

## Cost and Security Boundaries

The prototype's global hard spending ceiling remains USD $50/month as a resource governor rather than an interaction quota.

Normal Phase 2 CI:

- makes no paid Manager model call;
- makes no coding-runtime model call;
- starts neither OpenHands nor OpenCode;
- requires no OpenHands/OpenCode/provider credential;
- creates no cloud worker or recurring cloud resource.

Coding runtimes are privileged execution environments. Future worker deployment must keep long-lived provider/platform credentials outside repository-controlled code wherever possible and route privileged external side effects through Overlord's policy/tool boundaries.

## Boundaries Preserved

This implementation package does **not** introduce:

- a selected default Developer Agent;
- Manager-to-Developer task delegation in the production workflow;
- autonomous repository modification by Overlord;
- remote/ephemeral Developer Workers;
- worker provisioning or cleanup infrastructure;
- production GitHub write/merge automation;
- production secret brokering;
- hosted deployment;
- PWA/mobile work;
- notification/speech provider implementations;
- recurring cloud infrastructure;
- real runtime execution in normal CI.

## Next Decision Gate

The next Developer-runtime step is **evidence collection**, not architectural preselection.

OpenHands and OpenCode should be run against repeated identical repository tasks under controlled workspace/model conditions. The resulting task-quality, recovery, security, resource-use, and cost evidence should be recorded before selecting the default runtime or integrating Developer execution into the Manager workflow.

No such real benchmark was run as part of this implementation record.

## Related Documents

- [Overlord — Phase 0 Closeout](/projects/notes/overlord-phase-0-closeout/)
- [Overlord Phase 1 — Local Manager Conversation Loop](/projects/notes/overlord-phase-1-local-manager-loop/)
- [High Director Successor Research 06 — Build vs Adopt and Interoperability Boundaries](/projects/notes/high-director-successor-research-06/)
- [High Director Successor — Consolidated Architecture and MVP Proposal](/projects/notes/high-director-successor-consolidated-design/)

## Verification Record

- Last verified: `2026-08-11`.
- Verified against: `Overlord` PR #10; exact final PR head `cb3895c4dc6807ab4f12f0c3f9dd7e2ee2b2b6c1`; permanent PR-head CI run #140; final merged `main` commit `7c0867f8b31de5132707714decdf6540fb931307`; exact post-merge permanent CI run #141; final Phase 2 adapter/harness/config/script/source documentation; offline runtime contract tests; benchmark harness tests; and final permanent workflow tree.
- Verified by: High Director.
- Verification scope: OpenHands/OpenCode adapter replaceability, normalized runtime identity/status/events/usage/evidence, no-SDK HTTP boundary, offline acceptance, benchmark evidence schema, guarded real runner, configuration/cost/security boundaries, no-runtime-selection constraint, temporary diagnostic cleanup, and exact post-merge source verification.
