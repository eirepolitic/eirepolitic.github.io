---
title: Overlord Phase 4 — Hosting Provider Benchmark Harness
summary: First Phase 4 slice implementing the saved DigitalOcean-versus-Fly disposable worker benchmark before selecting a production hosting provider.
section: notes
doc_type: note
status: active
created: 2026-08-18
updated: 2026-08-18
last_verified: 2026-08-18
owner: High Director
order: 148
permalink: /projects/notes/overlord-phase-4-hosting-provider-benchmark/
tags:
  - overlord
  - phase-4
  - hosting
  - digitalocean
  - fly
  - benchmark
  - opencode
---

# Overlord Phase 4 — Hosting Provider Benchmark Harness

## Outcome

The first Phase 4 source slice is accepted. Overlord now contains the provider-neutral probe and manually dispatched paid benchmark harness required by the original hosting research before a production worker provider is selected.

No production hosting provider has been selected by this slice. DigitalOcean remains the current MVP front-runner and Fly remains the required comparison candidate from the saved hosting plan.

No paid DigitalOcean or Fly benchmark has been run yet.

## Source Acceptance

Source PR `#28` — `feat: add Phase 4 hosting provider benchmark`:

```text
exact final PR head:       44bdced50d8d233cdf039239d365bc5edca54057
PR permanent CI:           #337
PR CI run ID:              32212156127
PR CI conclusion:          success
merged source main:        3139333aff81db6c2a9afa982afcb3ade65ec21c
post-merge CI:             #338
post-merge CI run ID:      32212264118
post-merge CI conclusion:  success
```

Both accepted CI gates included Compose validation, PostgreSQL startup/readiness, locked dependency synchronization, Ruff lint, Ruff format check, strict mypy, Alembic upgrade, and full pytest.

## Saved Hosting Decision Sequence

The original hosting research deliberately did not make a final provider selection. It required a small disposable-worker prototype comparing at least DigitalOcean and Fly before production provisioning is implemented.

That sequence remains unchanged:

1. implement a provider benchmark harness;
2. run controlled one-worker trials;
3. run the two-worker concurrency comparison where useful;
4. compare measured startup/runtime/cleanup behavior and current effective cost;
5. select the MVP provider;
6. only then implement the production worker-provider boundary.

The temporary AWS EC2 direction considered during Phase 3 is not adopted. AWS Secrets Manager remains a supporting service, not a reason to replace the saved hosting benchmark process.

## Runtime Criterion Update

The original August 9 hosting research named OpenHands bootstrap/start latency because the Developer runtime had not yet been selected.

Phase 2 subsequently selected OpenCode as the owner-approved default Developer runtime behind `DeveloperAgentPort`. Phase 4 therefore measures the equivalent OpenCode installation/start/health behavior without reopening the completed runtime-selection architecture.

The benchmark pins OpenCode `1.18.16` to match the accepted Developer benchmark environment.

## Disposable Worker Probe

`scripts/hosting_provider_probe.sh` exercises the same basic worker capabilities on each provider:

- Ubuntu package update;
- Git installation;
- isolated local Git workspace creation/commit/status;
- Docker installation;
- `docker run --rm hello-world` compatibility;
- Node/npm installation;
- pinned OpenCode installation;
- OpenCode server startup;
- `/global/health` readiness;
- CPU, memory, architecture, kernel, and per-check timing evidence.

Capability failures are recorded in the probe evidence rather than silently converted into provider success. This is especially relevant to nested/container execution differences.

No production repository credential, GitHub App private key, AWS secret, or LLM API key is delivered to the disposable benchmark workers.

## Manual Cost Latch

`.github/workflows/hosting-provider-benchmark.yml` is `workflow_dispatch` only. It is not called by normal CI or pushes.

Every paid run requires all of:

- explicit provider selection;
- explicit worker count (`1` or `2`);
- an owner-supplied authorization identifier;
- the exact confirmation value `RUN_PROVIDER_TRIAL`;
- the relevant benchmark-only provider credential.

Provider jobs also have hard 25-minute workflow timeouts and cleanup steps guarded with `if: always()`.

## DigitalOcean Trial

The DigitalOcean path currently uses:

```text
region:  sfo3
size:    s-2vcpu-4gb
image:   ubuntu-24-04-x64
workers: 1 or 2
```

For each trial it:

1. generates a temporary Ed25519 SSH key on the GitHub Actions runner;
2. registers only the temporary public key with DigitalOcean;
3. creates one or two disposable 2-vCPU/4-GB Droplets;
4. measures API request-to-active latency;
5. measures active-to-SSH-ready latency;
6. runs the common worker probe;
7. records whether private networking is present;
8. destroys the Droplets even when a later benchmark step fails;
9. deletes the temporary DigitalOcean SSH key;
10. uploads JSON evidence for 30 days.

The benchmark credential is deliberately separate from future production worker credentials.

## Fly Trial

The Fly comparison currently uses:

```text
region:   sea
CPU kind: shared
vCPU:     2
memory:   4096 MB
workers:  1 or 2
```

For each trial it:

1. creates a temporary Fly app;
2. creates one or two disposable Ubuntu Machines;
3. resolves each Machine by its exact benchmark name;
4. runs the same probe through Fly platform SSH;
5. records create/start timing, private-network evidence, and probe results;
6. destroys the Machines in `always()` cleanup;
7. destroys the temporary Fly app;
8. uploads JSON evidence for 30 days.

## Comparison Evidence

The benchmark is designed to provide evidence for the original provider-selection criteria:

- worker creation/start latency;
- OpenCode bootstrap/readiness;
- basic workspace/Git behavior;
- Docker compatibility;
- private-network availability;
- cleanup reliability;
- one-versus-two-worker behavior;
- provider API/operational ergonomics;
- effective billed cost using the current provider rate at the time of the trial.

Published provider prices are intentionally not hard-coded into the worker probe. Cost comparison will use the current official rate when the evidence is evaluated.

## Current Provider Status

The current architecture-wide status remains:

```text
DigitalOcean  current MVP front-runner; benchmark first
Fly           required comparison candidate
AWS           Secrets Manager / later backup-artifact services
ProviderPort  production implementation deferred until evidence exists
```

The previously created AWS IAM policy `OverlordProductionGitHubAppSecretRead` remains intentionally unattached while the control-plane hosting/authentication mechanism is not yet finalized.

## Next Step

Run the controlled DigitalOcean one-worker benchmark first, because DigitalOcean is the saved front-runner. Then run the equivalent Fly one-worker benchmark. Only after comparable evidence exists should the project decide whether the two-worker pass is necessary before selecting the production provider.

Provider credentials must be created as benchmark-only credentials and stored in GitHub Actions secrets; they must never be pasted into chat or committed to the repository.

## Verification Record

- Last verified: `2026-08-18`.
- Verified against: source PR #28 exact final head `44bdced50d8d233cdf039239d365bc5edca54057`; PR CI #337 run `32212156127`; merged source main `3139333aff81db6c2a9afa982afcb3ade65ec21c`; post-merge CI #338 run `32212264118`; `scripts/hosting_provider_probe.sh`; `.github/workflows/hosting-provider-benchmark.yml`; original hosting research; accepted OpenCode Phase 2 runtime selection.
- Verified by: High Director.
