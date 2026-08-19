---
title: Overlord Phase 4 — Single-Host MVP Runtime
summary: Acceptance record and deployment plan for the single DigitalOcean-hosted Overlord MVP with local Docker Developer Environments.
section: notes
doc_type: note
status: active
created: 2026-08-18
updated: 2026-08-18
last_verified: 2026-08-18
owner: High Director
order: 151
permalink: /projects/notes/overlord-phase-4-single-host-runtime/
tags:
  - overlord
  - phase-4
  - digitalocean
  - docker
  - deployment
---

# Overlord Phase 4 — Single-Host MVP Runtime

## Source Acceptance

Source PR `#30` is accepted.

```text
final PR head:       0d2a70fe484b934ffba7a2560e72fe10a15dd136
PR CI:               #359 / run 32217340346 / success
merged source main:  562ee774a56b89eda8c1f913abf6adf0981f9b13
post-merge CI:       #360 / run 32217441927 / success
```

## Runtime Layout

The accepted deployment target is one always-on Ubuntu host, with DigitalOcean remaining the MVP front-runner.

- Overlord/DBOS runs as a host `systemd` service on loopback.
- PostgreSQL 17 runs in Docker and is exposed only on host loopback.
- The Overlord service account owns Docker lifecycle authority so it can create disposable Developer Environments.
- OpenCode runs inside task-scoped containers and does not receive the Docker socket.
- LLM inference remains external through configured provider APIs.
- Public API ingress is deliberately deferred; initial live verification uses localhost/SSH tunnelling.

## Deployment Assets

Source now contains:

```text
deploy/bootstrap-ubuntu.sh
deploy/docker-compose.production.yml
deploy/overlord.service
deploy/README.md
```

CI validates both development and production Compose configuration. Tests lock loopback-only database/API exposure, file-backed PostgreSQL password handling, control-plane Docker authority, and absence of embedded AWS/GitHub/LLM credentials in bootstrap.

## Cost-Sizing Starting Point

The cost-first MVP should begin with a DigitalOcean Basic shared-CPU Droplet rather than dedicated CPU. Current official pricing lists 4 GiB / 2 vCPU / 80 GiB at $24/month and 8 GiB / 4 vCPU / 160 GiB at $48/month.

The 4 GiB plan is the initial cost-minimizing candidate because the MVP targets one active Developer container and DigitalOcean supports later upward resize. If live memory/build evidence shows pressure, move to 8 GiB before adding remote-worker infrastructure.

## AWS/GitHub Sequence

The existing AWS/GitHub architecture remains unchanged:

```text
Secrets Manager region: us-east-2
secret:                 overlord/production/github-app
IAM policy:             OverlordProductionGitHubAppSecretRead
```

The policy remains unattached until the DigitalOcean host exists. After the host runtime is proven, configure a narrowly scoped AWS identity for the Overlord control plane only, then perform a controlled GitHub App smoke test through `GitHubBroker` and verify durable audit evidence.

## Next Owner Action

Provision the single DigitalOcean Droplet. Do not create the old remote-worker benchmark API token. Host provisioning will be performed interactively one owner-only step at a time.

## Verification Record

- Last verified: `2026-08-18`.
- Verified against: source PR #30 exact final head `0d2a70fe484b934ffba7a2560e72fe10a15dd136`, PR CI #359 run `32217340346`, merged source main `562ee774a56b89eda8c1f913abf6adf0981f9b13`, post-merge CI #360 run `32217441927`.
- Verified by: High Director.
