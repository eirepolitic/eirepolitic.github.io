---
title: Overlord Stage 0B — OpenAI Live Transport Smoke
summary: Acceptance record for the first bounded live-provider Stage 0B smoke through pinned OpenCode and the benchmark gateway.
section: notes
doc_type: note
status: active
created: 2026-08-31
updated: 2026-08-31
last_verified: 2026-08-31
owner: High Director
order: 154
permalink: /projects/notes/overlord-stage-0b-openai-live-smoke/
tags:
  - overlord
  - benchmark
  - developer
  - openai
  - stage-0b
---

# Overlord Stage 0B — OpenAI Live Transport Smoke

## Status

The first real-provider Stage 0B transport smoke completed successfully against OpenAI through the benchmark-only hard gateway.

```text
Overlord main: 98f0c5ac064b01408240736a88c157c1e0db4d73
Workflow: Developer benchmark Stage 0B live provider smoke
Workflow ID: 346986133
Run: #1 / 33444495539
Result: completed/success
Authorization ID: stage0b-openai-20260831-1450
Provider: openai
Model: gpt-5.6-luna
Runtime: opencode-1.18.16
```

This was transport/accounting acceptance only. It is not model-quality or production-routing evidence.

## Safety and execution boundaries

The run was authorized for a maximum administrative spend of USD 0.05 and used the fail-closed Stage 0B live workflow.

```text
Maximum forwarded provider requests: 1
Maximum output tokens: 256
Actual forwarded provider requests: 1
Developer direct Internet egress: blocked
Workspace mutation: none
GitHub mutation authority: none
Production routing authority: none
Production deployment: none
```

The benchmark-scoped OpenAI secret existed and was selected successfully. Anthropic and Google credential-selection steps were skipped.

The Developer ran on an internal-only Docker network and could reach OpenAI only through the benchmark gateway.

## Live evidence

The gateway accepted exactly one OpenAI Responses request and returned HTTP 200.

```text
message HTTP status: 200
message curl status: 0
upstream provider status: 200
provider request ID captured: yes
normalized evidence valid: yes
evidence errors: none
changed paths: none
routing_evidence_eligible: false
```

Normalized usage reported by the OpenAI response:

```text
input tokens: 6,147
cached input tokens: 0
output tokens: 5
reasoning tokens: 0
total tokens: 6,152
```

The prompt-free evidence artifact is:

```text
developer-benchmark-stage0b-live-openai-33444495539
artifact ID: 9777541069
retention: 30 days
```

The gateway artifact intentionally records dollar-cost provenance as `unavailable`; it does not fabricate or overwrite provider-reported cost.

Using the current public GPT-5.6 Luna token prices only for an external estimate — USD 0.20 per million input tokens and USD 1.20 per million output tokens — the observed usage corresponds to approximately:

```text
input estimate:  6,147 × 0.20 / 1,000,000 = USD 0.0012294
output estimate:     5 × 1.20 / 1,000,000 = USD 0.0000060
total estimate:                              USD 0.0012354
```

This is approximately 0.12 US cents and is comfortably below the authorized USD 0.05 ceiling. The estimate is documentation only and does not change the artifact's `unavailable` cost provenance.

## Authorization reset

Immediately after the workflow completed, all Stage 0B live-smoke controls were returned to the fail-closed state:

```text
OVERLORD_STAGE0B_LIVE_PROVIDER=UNARMED
OVERLORD_STAGE0B_LIVE_CONFIRMATION=UNARMED
OVERLORD_STAGE0B_LIVE_AUTHORIZATION_ID=UNARMED
```

No second provider was armed or dispatched.

## Result

OpenAI live transport through pinned OpenCode `1.18.16` and the benchmark gateway is accepted for Stage 0B:

```text
native OpenCode request path works
hard one-request ceiling works
hard output-token clamp works
provider authentication substitution works
streaming response accounting works
request ID capture works
normalized usage capture works
Developer network isolation works
transport-only workspace remains unchanged
prompt-free evidence capture works
```

This result does not justify a production routing change.

## Next boundary

The next provider should be armed only after its benchmark-scoped credential is configured and explicit spend authorization is given.

Recommended sequence remains:

```text
1. Anthropic claude-sonnet-5 live transport smoke
2. Google gemini-3.7-flash live transport smoke
3. freeze comparative candidate/pricing registry after all three transports pass
4. begin equal six-case Stage 1 benchmarking only after separate authorization
```
