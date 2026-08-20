---
title: Overlord Phase 4 — Live MVP Host
summary: Live deployment record for the first single-host Overlord MVP on DigitalOcean.
section: notes
doc_type: note
status: active
created: 2026-08-19
updated: 2026-08-19
last_verified: 2026-08-19
owner: High Director
order: 152
permalink: /projects/notes/overlord-phase-4-live-host/
tags:
  - overlord
  - phase-4
  - digitalocean
  - deployment
  - production
---

# Overlord Phase 4 — Live MVP Host

## Live milestone

The first always-on Overlord MVP host is provisioned and running on DigitalOcean.

```text
project:              Overlord
environment:          production
host name:            overlord-prod-01
region:               NYC3
OS:                   Ubuntu 24.04 LTS x64
Droplet class:        Basic / Regular SSD
size:                 2 vCPU / 4 GiB RAM / 80 GiB SSD
base price:           $24/month
source release:       562ee774a56b89eda8c1f913abf6adf0981f9b13
```

DigitalOcean improved metrics/monitoring is enabled. Managed Database and startup-script add-ons were not enabled.

## Host access

Administrative SSH uses a passphrase-protected Ed25519 key. The host has a separate repository deploy key installed on `Overlord` with write access disabled. The source checkout therefore does not require a GitHub password or personal access token.

## Running services

The accepted Phase 4 single-host deployment assets were used without changing the architecture:

- PostgreSQL 17 is running in Docker and reports healthy;
- PostgreSQL is bound only to host loopback;
- the Overlord control plane is installed as an enabled `systemd` service;
- Overlord is bound only to `127.0.0.1:8000`;
- `/health` returned `{"status":"ok","service":"overlord"}`;
- `/ready` returned `{"status":"ready","service":"overlord"}`.

The PostgreSQL password was generated on the host and is not stored in Git. `/etc/overlord/postgres-password` and `/etc/overlord/overlord.env` are owned by `root:overlord` with `0640` permissions.

## Security and authority boundary

The control plane service account owns Docker lifecycle authority so it can create disposable local Developer Environments. OpenCode Developer containers do not receive the host Docker socket.

No GitHub App private key, installation token, AWS credential, PostgreSQL password, SSH private key, or LLM provider credential was committed to Git or copied into this documentation.

## Next stage

The next deployment stage is the already-planned cross-cloud AWS Secrets Manager identity:

```text
AWS region:  us-east-2
secret:      overlord/production/github-app
IAM policy:  OverlordProductionGitHubAppSecretRead
```

Create a dedicated IAM identity for the DigitalOcean-hosted Overlord control plane and attach only the existing secret-read policy. Do not attach the policy to EC2 and do not expose those credentials to Developer containers.

After Secrets Manager access is proven, configure the selected external LLM provider credential required by OpenCode, run a controlled local Developer Environment smoke test, and finally run the live GitHub App smoke test through `GitHubBroker` with durable audit verification.

## Verification record

- Last verified: `2026-08-19`.
- Verified against: live `overlord-prod-01` deployment of source main `562ee774a56b89eda8c1f913abf6adf0981f9b13`.
- Runtime checks: PostgreSQL healthy; Overlord `/health` OK; Overlord `/ready` ready.
- Verified by: High Director.
