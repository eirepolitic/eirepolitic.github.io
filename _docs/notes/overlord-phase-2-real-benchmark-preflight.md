---
title: Overlord Phase 2 — Real Developer Benchmark Preflight
summary: Implementation record for the guarded GitHub Actions benchmark path and successful non-billable OpenHands/OpenCode runtime preflight before any paid model execution.
section: notes
doc_type: note
status: active
created: 2026-08-12
updated: 2026-08-12
last_verified: 2026-08-12
owner: High Director
order: 138
permalink: /projects/notes/overlord-phase-2-real-benchmark-preflight/
tags:
  - overlord
  - implementation
  - phase-2
  - developer-agent
  - benchmark
  - openhands
  - opencode
  - github-actions
---

# Overlord Phase 2 — Real Developer Benchmark Preflight

## Outcome

The credential/setup boundary for the first controlled real Developer benchmark is now implemented and the **non-billable runtime preflight succeeds**.

Overlord has separate manually dispatched GitHub Actions workflows for:

1. credential-free/non-billable runtime installation, workspace, health, and isolation proof;
2. a separately guarded real OpenHands/OpenCode comparison that may access the benchmark-only OpenAI API secret only after explicit owner authorization.

The real/billable workflow has **not been dispatched** as part of this implementation record.

## Source Delivery — Guarded Benchmark Infrastructure

Source PR `#17` — `feat: add guarded real Developer benchmark preflight`:

- exact final PR head: `7bdcc27774f36a25980509babd2242778e4b281b`;
- exact PR-head permanent CI: `#197` — success;
- merged source `main`: `613535d29f2f7795bd93f5c974597c1802dc4680`;
- exact post-merge permanent CI: `#198` — success.

This slice added:

- explicit OpenCode provider/model selection on every benchmark prompt;
- shared provider/model requirements in the guarded benchmark runner;
- `.github/workflows/developer-benchmark-preflight.yml`;
- `.github/workflows/developer-benchmark-real.yml`;
- read-only GitHub permissions for both manual workflows;
- separate fingerprint-identical benchmark workspaces;
- fixed first-comparison case/model/runtime settings;
- benchmark artifact capture;
- source architecture/development documentation.

No real model execution occurred in PR #17.

## Source Delivery — Dispatch and Runtime Hardening

Source PR `#18` — `fix: make Developer benchmark workflows dispatch-safe`:

- exact final PR head: `ce853e0612c3df9663ab488a0da676d3289d4dab`;
- exact final-head secret-free preflight: run `#11`, workflow run ID `31621482750` — success;
- exact final-head permanent CI: `#218`, workflow run ID `31621456183` — success;
- merged source `main`: `fcf401ab53e1410ab280cd647fe50b4d25cedfe6`;
- exact post-merge permanent CI: `#219`, workflow run ID `31621609118` — success.

No dependency lock or canonical database schema changed.

## Successful Non-Billable Preflight

The accepted preflight ran on exact PR #18 head:

`ce853e0612c3df9663ab488a0da676d3289d4dab`

It proved all of the following without a provider credential:

1. Overlord's locked development dependencies install normally;
2. separate OpenHands/OpenCode benchmark workspaces are prepared;
3. both workspaces have the same canonical case fingerprint;
4. both Git baselines are clean and intentionally unsolved;
5. the complete pinned OpenHands runtime bundle installs in an isolated Python 3.12 environment;
6. OpenCode `1.18.16` installs;
7. OpenHands reaches both `/health` and `/ready` on loopback;
8. OpenCode reaches its local health endpoint;
9. OpenCode reports the expected isolated benchmark project root;
10. non-secret preflight evidence is produced and uploaded as an Actions artifact.

Accepted evidence artifact:

```text
name: developer-benchmark-preflight-31621482750
artifact id: 9151419102
retention expiry: 2026-08-26
```

The preflight workflow references no OpenAI/provider secret and therefore cannot make a hosted-model request.

## OpenHands Runtime Compatibility

The verified isolated OpenHands runtime stack is:

```text
Python:                   3.12
openhands-agent-server:   1.42.0
openhands-sdk:            1.42.1
openhands-tools:          1.42.1
openhands-workspace:      1.42.1
startup:                  python -m openhands.agent_server
readiness window:         300 seconds
```

Overlord itself remains on Python 3.13.

The OpenHands packages are installed only inside the manually dispatched benchmark Actions environment. They are not Overlord application dependencies and were not added to `uv.lock`.

## Diagnostics and Corrections

The preflight was intentionally used to discover runtime/workflow defects before any paid execution.

### GitHub Actions context

The first post-PR17 dispatch was rejected by GitHub before a job started because job-level environment values used `runner.temp`, which is not available in that expression context.

The workflows were changed to use isolated fixed `/tmp` workspace roots. The parser failure did not access the benchmark secret, start either coding runtime, or make a provider request.

### OpenHands package boundary

Installing only `openhands-agent-server==1.42.0` was insufficient. A credential-free startup diagnostic captured:

```text
ModuleNotFoundError: No module named 'libtmux'
```

The workflow was corrected to install the complete pinned Agent Server package bundle shown above. The final accepted preflight then reached OpenHands health/readiness successfully.

Temporary diagnostic workflows and diagnostic files were deleted before final PR acceptance. The accepted branch workflow tree contained only:

```text
.github/workflows/ci.yml
.github/workflows/developer-benchmark-preflight.yml
.github/workflows/developer-benchmark-real.yml
```

## Real Benchmark Guardrail

The real workflow remains `workflow_dispatch`-only and uses `contents: read` GitHub permissions.

The first controlled real configuration is fixed to:

```text
corpus case:             python-off-by-one
OpenHands Agent Server:  1.42.0
OpenHands SDK/tools/ws:  1.42.1
OpenHands Python:        3.12
OpenCode:                1.18.16
provider:                openai
model:                   gpt-5.6-luna
trials per dispatch:     1
benchmark timeout:       12 minutes
job timeout:             20 minutes
GitHub permission:       contents: read
secret:                  OVERLORD_BENCHMARK_OPENAI_API_KEY
```

Both candidates receive the same provider/model identity and separate workspaces prepared from the same fingerprinted corpus case.

The real benchmark workflow does not have repository write permission and is separate from normal CI.

## Owner Cost Boundary

The owner created a dedicated OpenAI API project for this benchmark and configured a benchmark-only `$10 USD` hard spend ceiling.

That benchmark-specific external limit is separate from and does not replace Overlord's existing `$50/month` architectural project ceiling.

The presence of the repository secret or the `$10` ceiling does not itself authorize a paid workflow dispatch. A separate explicit owner run authorization remains required.

## Persistence and Evidence Boundary

Preflight evidence, real trial JSON, and comparison artifacts remain evaluation artifacts rather than canonical PostgreSQL application state.

The benchmark workflows do not add benchmark-result tables or make OpenHands/OpenCode native runtime state canonical.

## CI Acceptance

PR #18 permanent CI `#218` succeeded on exact final head:

`ce853e0612c3df9663ab488a0da676d3289d4dab`

Post-merge permanent CI `#219` succeeded on exact source `main`:

`fcf401ab53e1410ab280cd647fe50b4d25cedfe6`

Both permanent CI gates included:

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

## Next Checkpoint

All credential-free benchmark setup and runtime preflight work for this checkpoint is complete.

The next meaningful action is deliberately billable: dispatching one controlled real OpenHands-vs-OpenCode benchmark trial using the fixed configuration above.

That workflow must remain undispatched until the owner gives explicit final authorization for paid benchmark execution under the benchmark-only `$10` ceiling.

No default Developer runtime should be selected from preflight results alone.

## Related Documents

- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Reproducible Developer Benchmark Corpus](/projects/notes/overlord-phase-2-developer-benchmark-corpus/)
- [Overlord Phase 2 — Developer Benchmark Integrity and Git Evidence](/projects/notes/overlord-phase-2-benchmark-integrity-evidence/)
- [Overlord Phase 2 — Repeated Developer Benchmark Trial Reporting](/projects/notes/overlord-phase-2-benchmark-trial-reporting/)
- [Overlord Phase 2 — Developer Benchmark Corpus Fingerprints](/projects/notes/overlord-phase-2-benchmark-case-fingerprint/)

## Verification Record

- Last verified: `2026-08-12`.
- Verified against: source PR #17 and PR #18; exact PR heads and permanent CI gates; source main `fcf401ab53e1410ab280cd647fe50b4d25cedfe6`; secret-free preflight run `31621482750`; evidence artifact `9151419102`; final manual workflow tree; source architecture/development documentation; and post-merge CI #219.
- Verified by: High Director.
- Verification scope: manual workflow isolation, provider-secret boundary, corpus/workspace identity, OpenHands/OpenCode installation and health, OpenCode project-root isolation, OpenHands package compatibility, diagnostic cleanup, exact-SHA CI acceptance, non-canonical evaluation evidence, and no-paid-run/no-runtime-selection boundary.
