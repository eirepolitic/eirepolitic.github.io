---
title: Overlord Stage 1 — OpenAI Replay Baseline
summary: Canonical evidence record for three frozen OpenAI GPT-5.6 Luna trials across each of the six historical Overlord Developer replay cases.
section: notes
doc_type: note
status: active
created: 2026-09-01
updated: 2026-09-01
last_verified: 2026-09-01
owner: High Director
order: 155
permalink: /projects/notes/overlord-stage-1-openai-replay-baseline/
tags:
  - overlord
  - benchmark
  - developer
  - openai
  - stage-1
---

# Overlord Stage 1 — OpenAI Replay Baseline

## Status

OpenAI Stage 1 is complete for the frozen six-case Developer replay corpus. Each case received exactly three independent trials under the same model/runtime/security/request envelope.

```text
Benchmark repository main: ce2d7d0273a9d2e2aa8a712d63be4fec7c5a0bd7
Provider:                  openai
Model:                     gpt-5.6-luna
Runtime:                   opencode-1.18.16
Cases:                     6
Trials per case:           3
Total Stage 1 trials:      18
Overall passes:             4 / 18
Harness defects:            0
Model/task failures:       14
Stage 1 estimated spend:   USD 0.4664240
Stage 0B OpenAI estimate:  USD 0.0012354
Total project test spend:  USD 0.4676594 / USD 5.00 authorized
Production routing changed: no
Production deployed:        no
```

Stage 0B and Stage 1 answer different questions. Stage 0B is transport/integration evidence for the benchmark gateway/provider path. Stage 1 is capability evidence under a frozen task/evaluator envelope. Neither automatically changes production routing.

Production remains on deployed release `953580c06d064f44c98dd73c3c59affc35579218` with Developer provider `openai`, model `gpt-5.6-luna`, image `overlord-developer:1.18.16`, and disposable local Docker execution. Benchmark/main and documentation advancement do not authorize a production deployment.

## Frozen Stage 1 envelope

Every trial used the same common envelope:

```text
provider:                         openai
model:                            gpt-5.6-luna
runtime:                          opencode-1.18.16
maximum forwarded requests:      8 per case
maximum output tokens/request:   1024
Developer direct Internet egress: blocked
provider credential location:    benchmark gateway only
hidden validation:               evaluator-side only
workspace:                       fresh shallow exact-SHA repository
historical later commits:         unavailable to Developer
```

The canonical corpus and per-case timeout/fingerprint source is `Overlord/benchmarks/developer/replay_manifest.json` at benchmark main `ce2d7d0273a9d2e2aa8a712d63be4fec7c5a0bd7`.

Developer-visible replay workspaces were prepared as fresh repositories by fetching only the exact frozen base SHA at depth 1, checking it out detached, verifying it, and removing the evaluator source remote. Hidden validator source remained evaluator-owned and outside the Developer workspace.

The benchmark gateway alone held the real provider credential and Internet egress. The Developer had no direct provider/Internet route and no Docker socket, GitHub credentials, AWS credentials, PostgreSQL credentials, SSH keys, broad host filesystem, broad privileges, or production authority.

## Trial evidence

`requests` is actual forwarded provider requests over the frozen maximum of 8. Dollar values are exact benchmark estimates from the sanitized prompt-free evidence.

| Case | Difficulty | Trial | Result | Visible | Hidden | Scope | Requests | Input tokens | Output tokens | Total tokens | Est. cost USD | Classification |
|---|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---|
| easy-1-opencode-absent-status-idle | Easy | 1 | PASS | PASS | PASS | PASS | 8/8 | 95,605 | 1,020 | 96,625 | 0.0203450 | pass |
| easy-1-opencode-absent-status-idle | Easy | 2 | PASS | PASS | PASS | PASS | 8/8 | 104,112 | 1,176 | 105,288 | 0.0222336 | pass |
| easy-1-opencode-absent-status-idle | Easy | 3 | PASS | PASS | PASS | PASS | 8/8 | 90,389 | 1,074 | 91,463 | 0.0194486 | pass |
| easy-2-opencode-http-readiness | Easy | 1 | FAIL | PASS | FAIL | PASS | 7/8 | 81,286 | 2,900 | 84,186 | 0.0197372 | model/task behavioral failure; hidden bounded-readiness behavior failed |
| easy-2-opencode-http-readiness | Easy | 2 | FAIL | PASS | FAIL | PASS | 8/8 | 112,130 | 2,926 | 115,056 | 0.0259372 | model/task behavioral failure; hidden bounded-readiness behavior failed |
| easy-2-opencode-http-readiness | Easy | 3 | PASS | PASS | PASS | PASS | 6/8 | 70,653 | 2,681 | 73,334 | 0.0173478 | pass |
| medium-1-capture-workspace-changes | Medium | 1 | FAIL | FAIL | FAIL | FAIL | 8/8 | 151,405 | 2,674 | 154,079 | 0.0334898 | model/task failure; no workspace changes |
| medium-1-capture-workspace-changes | Medium | 2 | FAIL | FAIL | FAIL | FAIL | 8/8 | 154,641 | 2,661 | 157,302 | 0.0341214 | model/task failure; no workspace changes |
| medium-1-capture-workspace-changes | Medium | 3 | FAIL | FAIL | FAIL | FAIL | 6/8 | 85,123 | 1,844 | 86,967 | 0.0192374 | model/task failure; no workspace changes |
| medium-2-broker-safe-commit-intent | Medium | 1 | FAIL | FAIL | FAIL | FAIL | 8/8 | 183,121 | 2,408 | 185,529 | 0.0395138 | model/task failure; fixed-envelope exhaustion, no changes |
| medium-2-broker-safe-commit-intent | Medium | 2 | FAIL | FAIL | FAIL | FAIL | 7/8 | 125,823 | 2,223 | 128,046 | 0.0278322 | model/task failure; no workspace changes |
| medium-2-broker-safe-commit-intent | Medium | 3 | FAIL | FAIL | FAIL | FAIL | 8/8 | 185,594 | 2,101 | 187,695 | 0.0396400 | model/task failure; fixed-envelope exhaustion, no changes |
| hard-1-dbos-durable-bounded-execution | Hard | 1 | FAIL | FAIL | FAIL | FAIL | 8/8 | 190,579 | 2,091 | 192,670 | 0.0406250 | model/task failure; fixed-envelope exhaustion, no changes |
| hard-1-dbos-durable-bounded-execution | Hard | 2 | FAIL | FAIL | FAIL | FAIL | 8/8 | 196,777 | 2,088 | 198,865 | 0.0418372 | model/task failure; fixed-envelope exhaustion, no changes |
| hard-1-dbos-durable-bounded-execution | Hard | 3 | FAIL | FAIL | FAIL | FAIL | 8/8 | 136,736 | 1,415 | 138,151 | 0.0290452 | model/task failure; fixed-envelope exhaustion, no changes |
| hard-2-domain-postgres-foundation | Hard | 1 | FAIL | FAIL | FAIL | FAIL | 6/8 | 53,041 | 2,118 | 55,159 | 0.0131498 | model/task failure; no workspace changes |
| hard-2-domain-postgres-foundation | Hard | 2 | FAIL | FAIL | FAIL | FAIL | 6/8 | 51,194 | 2,108 | 53,302 | 0.0127336 | model/task failure; clean transport, no workspace changes |
| hard-2-domain-postgres-foundation | Hard | 3 | FAIL | FAIL | FAIL | FAIL | 5/8 | 40,606 | 1,690 | 42,296 | 0.0101492 | model/task failure; clean transport, no workspace changes |

## Case summary

| Case | Difficulty | Passes / 3 | Interpretation |
|---|---|---:|---|
| easy-1-opencode-absent-status-idle | Easy | 3/3 | Reliable under the frozen envelope. |
| easy-2-opencode-http-readiness | Easy | 1/3 | Stochastically achievable, but two trials failed the core hidden bounded-readiness behavior. |
| medium-1-capture-workspace-changes | Medium | 0/3 | No implementation changes were produced in any trial. |
| medium-2-broker-safe-commit-intent | Medium | 0/3 | No implementation changes; two trials exhausted the fixed request envelope. |
| hard-1-dbos-durable-bounded-execution | Hard | 0/3 | All three trials exhausted the fixed request envelope without workspace changes. |
| hard-2-domain-postgres-foundation | Hard | 0/3 | All three trials ended without workspace changes despite clean provider transport. |

Overall success was `4/18` trials. There were `0` accepted harness defects and `14` model/task failures.

## Easy-2 classification

Easy-2 Trials 1 and 2 remain genuine benchmark failures rather than harness defects. The hidden validator checks the core requested behavior: bounded polling of OpenCode `/global/health`, including transient connection failure before readiness. The validator was preflighted against the frozen buggy base and preserved known fix, and Trial 3 passed the same unchanged validator and envelope. Therefore no special rerun or validator change is justified.

## Fixed-envelope failures

A case is not repaired by granting additional benchmark resources after observing failure. The request limit remained 8 forwarded provider calls per case and the output ceiling remained 1,024 tokens per request.

Medium-2 Trials 1 and 3 and Hard-1 Trials 1–3 exhausted the fixed request envelope. Their upstream forwarded requests were successful HTTP 200 responses; later requests were denied before provider forwarding when the cap was reached. Those outcomes are model/task failures under the declared benchmark method, not provider transport failures and not grounds to enlarge the limits.

## Cost reconciliation

Completed OpenAI Stage 1 trial estimates sum exactly to:

```text
OpenAI Stage 1:             USD 0.4664240
OpenAI Stage 0B transport:  USD 0.0012354
Total project testing:      USD 0.4676594
User-authorized maximum:    USD 5.0000000
Remaining authorization:   USD 4.5323406
Anthropic spend:            USD 0
Google spend:               USD 0
```

The Stage 0B amount is a documented estimate for transport/integration evidence. Stage 1 costs are the exact estimates recorded by the prompt-free benchmark evidence path. Missing provider dollar cost is never converted silently to zero.

## Evidence and source of truth

Canonical benchmark/evaluator source lives in the `Overlord` repository. Relevant sources include:

```text
benchmarks/developer/replay_manifest.json
benchmarks/developer/hidden_validators/manifest.json
src/overlord/application/developer_replay.py
src/overlord/application/developer_replay_hidden_validation.py
src/overlord/application/developer_benchmark_gateway.py
src/overlord/application/developer_benchmark_evidence.py
.github/workflows/developer-stage1-openai-replay-baseline.yml
scripts/evaluate_stage1_developer_replay.py
```

The Stage 1 workflow is `Developer Stage 1 OpenAI replay baseline`, workflow ID `347020167`.

First-trial sanitized classification evidence remains on the intentionally unmerged diagnostic branches:

```text
diag/stage1-easy1-result
diag/stage1-easy2-result
diag/stage1-medium1-result
diag/stage1-medium2-result
diag/stage1-hard1-result
diag/stage1-hard2-result
```

Repeat-trial sanitized results are retained on `diag/stage1-openai-repeats` under `.stage1-results/<RUN_ID>.json`. The branch-only extractor has no provider or production authority.

All reported evidence is prompt-free. Prompts, raw provider payloads, secrets, and hidden validator source are not published as benchmark result evidence.

## Authorization state

After the final paid Stage 1 run, the Stage 1 controls were returned to fail-closed values:

```text
OVERLORD_STAGE1_REPLAY_CASE=UNARMED
OVERLORD_STAGE1_REPLAY_CONFIRMATION=UNARMED
OVERLORD_STAGE1_REPLAY_AUTHORIZATION_ID=UNARMED
```

Stage 0B controls remain fail-closed:

```text
OVERLORD_STAGE0B_LIVE_PROVIDER=UNARMED
OVERLORD_STAGE0B_LIVE_CONFIRMATION=UNARMED
OVERLORD_STAGE0B_LIVE_AUTHORIZATION_ID=UNARMED
```

No Anthropic or Google paid run has been authorized or dispatched.

## Production boundary

This Stage 1 result is benchmark/capability evidence only. It does not authorize a production model change, production deployment, or production routing change.

Canonical production architecture remains:

```text
PostgreSQL -> canonical Conversation / WorkRequest / Plan / Task / AgentRun / audit / deliveries
DBOS       -> durable coordination/checkpoint/output only
Developer  -> disposable local Docker -> OpenCode -> model provider
GitHub     -> GitHubPort -> GitHubBroker -> GitHub App adapter -> durable audit
```

Historical evidence PRs #61 and #77 remain untouched. The legacy `developer-benchmark-real.yml` workflow remains intentionally disabled.

## Next boundary

OpenAI Stage 1 has exhausted the useful testing available with the existing OpenAI benchmark credential for this planned baseline. The next provider is Anthropic, but no Anthropic call should run until `OVERLORD_BENCHMARK_ANTHROPIC_API_KEY` is configured and a bounded Stage 0B Anthropic transport smoke is separately armed.

After Anthropic transport/accounting is accepted, Anthropic Stage 1 can be considered under the same fairness/security principles. Google follows Anthropic and receives the same separate credential, transport-smoke, and budget gate.

No production routing recommendation should be made until provider-comparable evidence exists and the user makes a separate explicit routing decision.
