---
title: Overlord Phase 2 — First Real Developer Benchmark Evidence
summary: First controlled paid OpenHands/OpenCode comparison, duplicate-dispatch containment, and follow-up evidence normalization.
section: notes
doc_type: note
status: active
created: 2026-08-12
updated: 2026-08-12
last_verified: 2026-08-12
owner: High Director
order: 139
permalink: /projects/notes/overlord-phase-2-first-real-benchmark-evidence/
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

# Overlord Phase 2 — First Real Developer Benchmark Evidence

## Outcome

Overlord completed its first controlled real OpenHands-vs-OpenCode Developer benchmark on the approved `python-off-by-one` corpus case using the same OpenAI provider/model for both candidates.

Both runtimes produced the same intended one-line repair, passed the protected validator, and preserved the canonical corpus fingerprint. The single completed trial is useful evidence but is **not sufficient to select a default Developer runtime**.

A duplicate workflow run was also observed and contained. Follow-up source hardening now normalizes runtime usage evidence, handles OpenHands terminal status correctly, reduces Git workspace noise, and changes benchmark concurrency so accidental duplicate dispatches cancel the older run instead of intentionally serializing multiple paid comparisons.

## First Controlled Real Trial

Authorized workflow run:

```text
workflow:                  Real Developer benchmark
workflow run ID:           31625963336
workflow run number:       7
source main SHA:           fcf401ab53e1410ab280cd647fe50b4d25cedfe6
trial ID:                  github-31625963336-1
case:                      python-off-by-one
case fingerprint:          sha256:810c0e17985a55887e945f972f3fa83a7dcd4f947782d7f581d0a8fbebe96a54
provider:                  openai
model:                     gpt-5.6-luna
artifact:                  developer-benchmark-31625963336-1
artifact ID:               9153151709
```

The workflow job and evidence upload completed successfully.

## Runtime Results

### OpenHands

```text
completed:                 true
tests passed:              true
workspace integrity:       true
duration:                  28.968674646 seconds
reported cost:             $0.00466036
reported prompt tokens:    58052
reported output tokens:    1127
cache-read tokens:         48713
cache-write tokens:        0
reasoning tokens:          191
```

OpenHands changed:

```diff
-return sum(range(start, end))
+return sum(range(start, end + 1))
```

Its canonical Git status showed only `calculator.py` modified. The full runtime evidence reported `execution_status: finished`; the older adapter recorded normalized status as `unknown` because it did not yet read that field.

### OpenCode

```text
completed:                 true
tests passed:              true
workspace integrity:       true
duration:                  11.128506547 seconds
reported cost:             $0.00271361
direct input tokens:       15
reported output tokens:    339
cache-read tokens:         26068
cache-write tokens:        6933
reasoning tokens:          41
```

OpenCode made the same intended one-line repair:

```diff
-return sum(range(start, end))
+return sum(range(start, end + 1))
```

Its canonical Git status also contained an untracked `__pycache__/` directory. That was interpreter noise rather than a task change. The protected validator still passed and the workspace fingerprint remained valid.

OpenCode's completed synchronous session was absent from the runtime's returned status map, so Overlord retained `unknown` rather than inventing a terminal runtime state.

## Cost Observation

The two completed runtime results reported a combined observed cost of:

```text
$0.00737397
```

This is the sum of the costs reported by the accepted completed trial only. It is **not** a statement of the provider project's current balance or total billing because the duplicate run may have incurred partial usage before cancellation.

The benchmark project's externally configured `$10` hard ceiling remains separate from Overlord's existing `$50/month` architectural project ceiling.

## Duplicate Dispatch Incident

One benchmark dispatch request resulted in two GitHub workflow runs approximately two seconds apart:

```text
authorized completed run: 31625963336
additional run:           31625965069
```

The second run was not intended as an additional completed comparison.

Containment actions were:

1. no further real benchmark dispatches were made;
2. the repository secret `OVERLORD_BENCHMARK_OPENAI_API_KEY` was deleted;
3. the duplicate run was observed until GitHub cancelled it during its model-execution step;
4. its comparison summary step was skipped;
5. it is excluded from completed-trial evidence.

Deleting the repository secret did not retroactively remove the credential from the already-started duplicate job because the job had already materialized its environment. The repository secret remains absent after containment.

The OpenAI project-level hard spending ceiling remained the external cost backstop throughout the incident.

## Follow-Up Source Hardening

Source PR `#20` — `feat: normalize real Developer benchmark evidence` — incorporated the concrete lessons from the first real trial.

Accepted source evidence:

```text
exact final PR head:       ca7dbc1dc2a5871e150a95e6a6913c85a94f8aa2
PR permanent CI:           #226
PR CI run ID:              31626895262
PR CI conclusion:          success
merged source main:        9745b4f8a49a6161eb3539aef7074d6d5f8de80b
post-merge CI:             #230
post-merge CI run ID:      31627036702
post-merge CI conclusion:  success
```

Both permanent CI gates included Compose validation, PostgreSQL readiness, locked dependency synchronization, Ruff lint, Ruff format check, strict mypy, Alembic upgrade, and full pytest.

No database schema migration, application dependency change, default Developer runtime selection, provider/model change, or budget-policy change was introduced.

## Usage Evidence Normalization

`DeveloperUsage` retains the existing runtime-native fields and adds optional comparison fields:

```text
input_tokens
output_tokens
cost_usd
total_input_tokens
cache_read_tokens
cache_write_tokens
reasoning_tokens
```

The existing `input_tokens` meaning is preserved for backward compatibility.

For OpenHands, `total_input_tokens` uses its accumulated prompt-token total while the runtime's cache-read/write details are retained separately.

For OpenCode, `input_tokens` remains the runtime's direct input count while normalized `total_input_tokens` is direct input plus cache-read plus cache-write tokens.

Repeated-trial reports now aggregate the raw and normalized fields independently. Older schema-version-2 trial artifacts that do not contain the enriched fields continue to parse with those new values unknown rather than zero.

## Runtime Status Normalization

OpenHands status normalization now reads `execution_status` before legacy/fallback state fields. This converts evidence such as the first real trial's `finished` state correctly instead of recording `unknown`.

For OpenCode, an absent session entry in the returned status map remains explicitly `unknown`. The implementation does not infer a terminal state that the runtime API did not provide.

## Workflow Hardening

The real benchmark workflow now uses:

```text
concurrency group:         real-developer-benchmark
cancel-in-progress:        true
provider-secret precheck:  required
GitHub permissions:        contents: read
```

If another dispatch enters the same concurrency group, GitHub is instructed to cancel the older in-progress run rather than queueing a second paid comparison behind it.

The workflow also starts both runtime environments with `PYTHONDONTWRITEBYTECODE=1` to reduce interpreter-generated `__pycache__` noise in future canonical Git evidence.

The provider-secret check occurs before runtime installation and causes the real workflow to fail immediately when `OVERLORD_BENCHMARK_OPENAI_API_KEY` is absent.

## Credential Boundary

`OVERLORD_BENCHMARK_OPENAI_API_KEY` was deliberately removed from the `Overlord` repository during duplicate-run containment and remains absent at this checkpoint.

No more real Developer benchmark execution is possible through the guarded workflow until the owner deliberately supplies a fresh/current benchmark credential again.

Credentials must never be committed to either repository or pasted into documentation/chat.

## Selection Boundary

The first completed trial shows:

- both candidates can solve the smallest approved bug-fix case;
- both produced the same canonical task repair;
- both passed the protected validator and integrity checks;
- OpenCode was faster and reported a lower cost on this individual trial;
- runtime-native token accounting differs enough that normalized evidence is required before comparing usage directly.

These observations do **not** establish a preferred Developer runtime.

The approved Phase 2 selection process still requires repeated comparable evidence across the benchmark corpus, including the feature and refactor cases, before OpenHands or OpenCode can become Overlord's default Developer runtime.

## Next Checkpoint

All source-side offline hardening and documentation for the first real trial are complete.

The next owner-only action is credential restoration: revoke the prior benchmark API key if it has not already been revoked, create a fresh benchmark key, and store it in the `Overlord` repository as `OVERLORD_BENCHMARK_OPENAI_API_KEY`.

No further paid benchmark run should be dispatched until that credential step is explicitly completed.

## Related Documents

- [Overlord Phase 2 — Real Developer Benchmark Preflight](/projects/notes/overlord-phase-2-real-benchmark-preflight/)
- [Overlord Phase 2 — Developer Agent Benchmark Harness](/projects/notes/overlord-phase-2-developer-benchmark-harness/)
- [Overlord Phase 2 — Reproducible Developer Benchmark Corpus](/projects/notes/overlord-phase-2-developer-benchmark-corpus/)
- [Overlord Phase 2 — Developer Benchmark Integrity and Git Evidence](/projects/notes/overlord-phase-2-benchmark-integrity-evidence/)
- [Overlord Phase 2 — Repeated Developer Benchmark Trial Reporting](/projects/notes/overlord-phase-2-benchmark-trial-reporting/)
- [Overlord Phase 2 — Developer Benchmark Corpus Fingerprints](/projects/notes/overlord-phase-2-benchmark-case-fingerprint/)

## Verification Record

- Last verified: `2026-08-12`.
- Verified against: real benchmark run `31625963336`; trial artifact `9153151709`; duplicate run `31625965069`; source PR #20 exact head `ca7dbc1dc2a5871e150a95e6a6913c85a94f8aa2`; PR CI #226; merged source main `9745b4f8a49a6161eb3539aef7074d6d5f8de80b`; and post-merge CI #230.
- Verified by: High Director.
- Verification scope: first paid trial correctness/integrity/cost evidence, duplicate-run containment, credential removal, normalized token accounting, runtime status semantics, workflow concurrency hardening, exact-SHA source acceptance, and no-runtime-selection boundary.
