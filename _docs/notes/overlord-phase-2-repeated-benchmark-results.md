---
title: Overlord Phase 2 — Repeated Developer Benchmark Results
summary: Nine accepted real OpenHands/OpenCode comparisons across the three canonical corpus cases, with neutral aggregate evidence and a runtime recommendation.
section: notes
doc_type: note
status: active
created: 2026-08-13
updated: 2026-08-13
last_verified: 2026-08-13
owner: High Director
order: 143
permalink: /projects/notes/overlord-phase-2-repeated-benchmark-results/
tags:
  - overlord
  - phase-2
  - developer-agent
  - benchmark
  - openhands
  - opencode
  - github-actions
  - evaluation
---

# Overlord Phase 2 — Repeated Developer Benchmark Results

## Outcome

The approved repeated real Developer benchmark phase is complete.

Exactly **nine accepted comparison trials** are included in the final evidence set:

- three `python-off-by-one` trials;
- three `python-config-feature` trials;
- three `python-slug-refactor` trials.

Every accepted trial ran both OpenHands and OpenCode against separate fingerprint-identical workspaces with the same OpenAI provider/model and fixed runtime versions.

Both runtimes completed and passed validation in **9/9 accepted trials**.

The repeated evidence supports **OpenCode as the recommended default Developer runtime** for the next Overlord phase. This is a recommendation only; the owner must still explicitly choose the default runtime before production orchestration is changed.

## Fixed Comparison Configuration

```text
provider:                  openai
model:                     gpt-5.6-luna
OpenHands Agent Server:    1.42.0
OpenHands SDK/tools/ws:    1.42.1
OpenHands Python:          3.12
OpenCode:                  1.18.16
GitHub permission:         contents: read
benchmark timeout:         12 minutes
job timeout:               20 minutes
```

The final repeated runs used source `main`:

```text
ccd3db3fc8c68c3029b8921fc6d9b700b0691bb2
```

The earlier accepted first trial and one subsequent accepted off-by-one trial were produced before the later health-probe-only workflow hardening; the canonical corpus fingerprints, provider/model, runtime versions, and task semantics remained unchanged.

## Accepted Evidence Set

```text
case                  run ID       artifact ID
--------------------  -----------  ----------
python-off-by-one     31625963336  9153151709
python-off-by-one     31736766877  9195487578
python-off-by-one     31738130630  9196006331
python-config-feature 31738406506  9196115820
python-config-feature 31754356424  9202195206
python-config-feature 31754518477  9202252530
python-slug-refactor  31754684439  9202319361
python-slug-refactor  31754858982  9202377327
python-slug-refactor  31755031321  9202444458
```

The accepted trial IDs are:

```text
github-31625963336-1
github-31736766877-1
github-31738130630-1
github-31738406506-1
github-31754356424-1
github-31754518477-1
github-31754684439-1
github-31754858982-1
github-31755031321-1
```

All three corpus revisions remained stable across accepted repetitions:

```text
python-off-by-one:
sha256:810c0e17985a55887e945f972f3fa83a7dcd4f947782d7f581d0a8fbebe96a54

python-config-feature:
sha256:01b482bb4b49c7b398826293f764c5b140cd23b1aee45719544a76b29b1f5902

python-slug-refactor:
sha256:4011c912e08394257e1193fa54b96cec7a9650c66b9f54424cc7b062e8a53cdb
```

## Excluded Runs

The following runs are explicitly excluded from accepted runtime-selection evidence:

```text
31625965069  unintended duplicate; not separately owner-authorized
31736990042  local OpenCode health infrastructure attempt; never reached model comparison
31737553418  deliberately disarmed cancellation replacement
31627541359  non-billable authorization-latch negative proof
```

Artifact completeness alone does not make an excluded run accepted evidence. Owner authorization, corpus identity, and accepted execution boundaries are part of the evidence contract.

## Neutral Aggregate

Overlord's canonical `report_developer_benchmark_trials.py` reporter successfully aggregated exactly the nine accepted trial JSON files.

### OpenCode

```text
trials observed:             9
completed:                   9
tests passed:                9
tests failed:                0
median duration:             21.352578936 s
events observed:             36
reported accepted cost:      $0.03935416
output tokens:               7,265
normalized total input:      520,268 across 8 enriched trials
cache-read tokens:           452,085 across 8 enriched trials
cache-write tokens:          67,973 across 8 enriched trials
reasoning tokens:            1,877 across 8 enriched trials
```

### OpenHands

```text
trials observed:             9
completed:                   9
tests passed:                9
tests failed:                0
median duration:             28.968674646 s
events observed:             0
reported accepted cost:      $0.04887296
output tokens:               14,109
normalized total input:      503,961 across 8 enriched trials
cache-read tokens:           423,250 across 8 enriched trials
cache-write tokens:          0 across 8 enriched trials
reasoning tokens:            3,990 across 8 enriched trials
```

Combined runtime-reported cost for the **accepted evidence set** was:

```text
$0.08822712
```

This accepted-evidence cost excludes the historical unintended duplicate's partial usage and is not a statement of the OpenAI billing dashboard balance. It remains far below the benchmark project's `$10` hard ceiling.

## Per-Case Results

### `python-off-by-one`

Both runtimes passed 3/3 and produced one identical tracked diff across all repetitions.

```text
OpenCode median duration: 17.768518135 s
OpenHands median duration: 28.968674646 s
OpenCode cost total:       $0.01101500
OpenHands cost total:      $0.01275505
```

OpenCode was approximately 38.7% faster by median duration and 13.6% lower in reported cost on this case.

### `python-config-feature`

Both runtimes passed 3/3 and produced one identical tracked diff across all repetitions.

```text
OpenCode median duration: 22.298109083 s
OpenHands median duration: 25.057031077 s
OpenCode cost total:       $0.01407513
OpenHands cost total:      $0.01483345
```

OpenCode was approximately 11.0% faster by median duration and 5.1% lower in reported cost on this case.

### `python-slug-refactor`

Both runtimes passed 3/3.

```text
OpenCode median duration: 23.557669986 s
OpenHands median duration: 35.245984777 s
OpenCode cost total:       $0.01426403
OpenHands cost total:      $0.02128446
```

OpenCode was approximately 33.2% faster by median duration and 33.0% lower in reported cost on this case.

OpenCode produced the same tracked refactor diff in all three accepted runs. OpenHands produced two distinct valid implementations: one regular-expression implementation matching OpenCode's tracked diff and one loop-based separator-collapse implementation. Both OpenHands variants passed the protected validator.

## Overall Comparison

With reliability tied at 9/9 accepted passes:

```text
OpenCode overall median duration: 21.352578936 s
OpenHands overall median duration: 28.968674646 s
```

OpenCode's overall median was approximately **26.3% lower**.

Accepted runtime-reported cost totals were:

```text
OpenCode:  $0.03935416
OpenHands: $0.04887296
```

OpenCode's accepted cost was approximately **19.5% lower**.

The direction of the difference was consistent across all three task types: OpenCode had both the lower median duration and lower cost total on bugfix, feature, and refactor cases.

## Operational Tradeoffs

### Evidence favoring OpenCode

- 9/9 completion and 9/9 validation passes, matching OpenHands;
- lower median duration overall and on every corpus case;
- lower reported cost overall and on every corpus case;
- same tracked implementation across all three repetitions of every case;
- 36 normalized runtime events observed across the nine trials;
- no need to change provider/model/runtime versions to achieve the results.

### Evidence favoring OpenHands

OpenHands exposes a clearer native terminal execution signal. Newer accepted trials normalize its `execution_status=finished` correctly.

OpenCode's `/session/status` behavior remained conservative in Overlord: completed synchronous sessions were absent from the returned status map, so normalized `status` remained `unknown` rather than inventing a terminal state. Completion was nevertheless established independently by synchronous task return, canonical workspace validation, protected tests, and final evidence.

OpenHands also exposes detailed conversation-level runtime telemetry. That richer native terminal-status model is the strongest observed operational advantage over OpenCode in this corpus.

One OpenHands refactor trial also left an untracked Python `__pycache__/` workspace artifact while still passing integrity/validation; this did not alter protected files or tracked task output.

## Recommendation

**Recommend OpenCode as Overlord's default Developer runtime for the next implementation phase.**

Rationale:

1. correctness/reliability is tied at 9/9 accepted passes;
2. OpenCode is faster overall and on every case;
3. OpenCode is cheaper overall and on every case;
4. its tracked task output was maximally consistent across repeated runs;
5. its adapter surfaced normalized event activity during all trials;
6. the remaining status limitation is observable and bounded rather than a correctness failure because Overlord already validates final workspace evidence independently of runtime-native terminal state.

The recommendation does **not** authorize source code to select OpenCode automatically. Owner approval remains required before Overlord changes its default Developer runtime or begins Phase 3 product GitHub write/merge brokering.

## Infrastructure Hardening During the Phase

Source PR `#22` added allow-listed corpus case selection.

```text
PR #22 final head:     fec985ee2b7a763968fda764f423b0c8767882f6
CI #233:               success
merged source main:    b9924b251a97a0f78ba5b0801907c43da559fb78
post-merge CI #234:    success
```

Source PR `#23` bounded local runtime health requests after the unaccepted infrastructure attempt.

```text
PR #23 final head:     d884bdd4326fa981a61ca528446bf88fceffb747
CI #235:               success
merged source main:    ccd3db3fc8c68c3029b8921fc6d9b700b0691bb2
post-merge CI #236:    success
```

No runtime version, model, provider, database schema, application dependency lock, canonical persistence model, runtime-selection policy, or budget policy changed during either hardening slice.

## Current Safe State

After accepted trial 9/9 completed:

```text
source main:                           ccd3db3fc8c68c3029b8921fc6d9b700b0691bb2
real benchmark workflow:               disabled
OVERLORD_BENCHMARK_AUTHORIZATION_ID:   UNARMED
OVERLORD_BENCHMARK_RUN_CONFIRMATION:   DISABLED
last selected benchmark case:          python-slug-refactor
further paid runs authorized:          no
```

No additional paid benchmark run should be dispatched without a new explicit owner authorization.

## Next Checkpoint

The repeated benchmark evidence phase is complete.

The next owner decision is whether to accept the recommendation and choose **OpenCode** as Overlord's default Developer runtime.

If accepted, implementation may resume with the selected runtime behind `DeveloperAgentPort`. Phase 3 GitHub write/merge brokering remains a later, separately controlled product capability; benchmark artifacts remain non-canonical evaluation evidence.

## Related Documents

- [Overlord Phase 2 — First Real Developer Benchmark Evidence](/projects/notes/overlord-phase-2-first-real-benchmark-evidence/)
- [Overlord Phase 2 — Repeated Benchmark Case Selection](/projects/notes/overlord-phase-2-repeated-benchmark-case-selection/)
- [Overlord Phase 2 — Bounded Benchmark Health Probes](/projects/notes/overlord-phase-2-benchmark-health-probe-timeouts/)
- [Overlord Phase 2 — Repeated Developer Benchmark Trial Reporting](/projects/notes/overlord-phase-2-benchmark-trial-reporting/)
- [Overlord Phase 2 — Developer Benchmark Corpus Fingerprints](/projects/notes/overlord-phase-2-benchmark-case-fingerprint/)

## Verification Record

- Last verified: `2026-08-13`.
- Verified against: all nine accepted trial JSON artifacts listed above; canonical comparison report schema version 2; per-case aggregate evidence; source PR #22/#23 exact acceptance gates; and final real benchmark run `31755031321` success.
- Verified by: High Director.
- Verification scope: accepted/excluded trial identity, corpus fingerprints, completion/validation, durations, runtime-reported usage/cost, tracked Git evidence consistency, runtime status/event behavior, safe post-run repository state, and runtime recommendation boundary.
