---
title: Operate Oireachtas refresh, validation, promotion, and rollback
summary: Run and troubleshoot the Unified Oireachtas scheduled or manual refresh pipeline, validate immutable candidates, promote only validated batches, and recover safely through pointer rollback.
section: runbooks
doc_type: runbook
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: eirepolitic-data-pipeline
system: Unified Oireachtas Data Platform
order: 30
permalink: /projects/runbooks/oireachtas-refresh-validation-orchestration/
tags:
  - oireachtas
  - github-actions
  - operations
  - s3
related:
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/data/oireachtas-canonical-data-product-catalogue/
  - /projects/repositories/eirepolitic-data-pipeline/
---

# Operate Oireachtas refresh, validation, promotion, and rollback

## Purpose

Use this runbook to observe scheduled Oireachtas production refreshes, create and validate a manual immutable candidate, inspect candidate/production state, promote an already validated candidate, or roll production back through the checked-in batch-control workflow.

The safest default for a manual run is **candidate publication enabled, consumer validation enabled, automatic promotion disabled**. That produces a complete candidate and validation evidence without changing the production pointer.

This runbook does not authorize schema changes, IAM changes, S3 policy changes, credential changes, or manual editing of production pointer objects.

## Status and Last Verification

- Status: **verified for the scheduled end-to-end flow; implementation-verified for manual controls**
- Last verified: `2026-08-07`
- Verified scheduled execution: `Oireachtas Refresh Validation Orchestrator` run `30740881592`, scheduled on `2026-08-02`
- Verified implementation: current orchestrator/reusable workflows, batch-control workflow, candidate seed/reassembly helpers, contract staging/validation code, and orchestration/write-semantics tests
- Known unverified step: this documentation workstream did not deliberately trigger a new production promotion or rollback.

## Use This Runbook When

Use it when:

- reviewing a weekly, monthly, or yearly scheduled refresh;
- running a safe manual candidate refresh and validation;
- investigating a failed refresh or validation job;
- checking the current and previous production pointers;
- promoting a specifically identified, already validated candidate after the appropriate operational decision;
- rolling back to `previous` or to another specifically identified validated batch.

## Do Not Use This Runbook When

Do not use it to:

- change the 31-product registry or table schemas;
- change write strategies or downstream-contract thresholds;
- bypass a failed DQ, contract, compatibility, mismatch, member-metric, or Instagram smoke check;
- manually copy candidate files over production logical keys;
- manually edit `production.json` or `previous.json`;
- change `OIREACHTAS_PUBLISH_ENABLED`, AWS credentials, IAM permissions, bucket policy, or other security controls as part of routine recovery.

If a production pointer cannot be updated because publishing is disabled, stop. Enabling production publication is an access/control decision outside this routine runbook.

## Impact and Risk

Refreshing into an immutable candidate is designed to avoid immediate production replacement. **Promotion and rollback are production-state changes** because they update which immutable batch the production pointer selects.

The platform serializes high-level orchestrators through concurrency group `oireachtas-production-orchestrator`, refresh work through `oireachtas-production-refresh`, and manual promotion/rollback controls through `oireachtas-production-promotion`; all use `cancel-in-progress: false` where configured. Do not intentionally start overlapping manual recovery work just because concurrency will queue it.

## Prerequisites and Access

You need:

- access to the `eirepolitic-data-pipeline` repository and its **Actions** tab;
- permission to dispatch the relevant workflows;
- repository AWS secrets already configured for the workflows (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`); do not expose their values;
- for production pointer changes, the repository variable `OIREACHTAS_PUBLISH_ENABLED` must already permit publication;
- the exact GitHub Actions run ID and, for candidate operations, the exact batch ID.

Current checked-in runtime defaults used by these workflows are S3 bucket `eirepolitic-data` and region `ca-central-1`.

## Source of Truth

- High-level production controller: `.github/workflows/oireachtas_refresh_validation_orchestrator.yml`
- Shared refresh implementation: `.github/workflows/oireachtas_refresh_reusable.yml`
- Shared validation implementation: `.github/workflows/oireachtas_validation_reusable.yml`
- Manual cadence wrappers: `.github/workflows/oireachtas_weekly_refresh.yml`, `oireachtas_monthly_refresh.yml`, `oireachtas_yearly_refresh.yml`
- Manual batch control: `.github/workflows/oireachtas_batch_control.yml`
- Cadence normalization: `process/oireachtas_refresh_inputs.py`
- Candidate seed: `process/oireachtas_seed_candidate.py`
- Candidate final reassembly: `process/oireachtas_reassemble_candidate.py`
- Batch CLI: `process/oireachtas_batch_control.py`
- Batch implementation: `extract/oireachtas/batch.py`
- S3 logical/batch resolution: `extract/oireachtas/io_s3.py`
- Contract staging: `process/oireachtas_stage_downstream_contracts.py`
- Contract validation: `process/oireachtas_validate_downstream_contracts.py`, `extract/oireachtas/contracts.py`
- Regression tests: `tests/test_oireachtas_refresh_orchestration.py`, `tests/test_oireachtas_batch_control.py`, `tests/test_oireachtas_seed_candidate.py`, `tests/test_oireachtas_write_semantics.py`

Current implementation/configuration overrides older handoff notes if they differ.

## Scheduled Production Behavior

Only `Oireachtas Refresh Validation Orchestrator` has the production refresh schedule. The weekly/monthly/yearly wrapper workflows are manual dispatch workflows.

Current orchestrator cron values are:

```text
45 6 * * 0     weekly
15 7 1 * *     monthly
30 7 2 1 *     yearly
```

For scheduled runs, the orchestrator forces:

```text
publish_candidate = true
run_consumers     = true
auto_promote      = true
```

The scheduled batch ID format is:

```text
scheduled-<weekly|monthly|yearly>-<github_run_id>-<github_run_attempt>
```

A scheduled run therefore changes production only after refresh and reusable validation both succeed and `promote_batch()` accepts the candidate as validated.

## Safety Checks

Before manually dispatching anything:

1. Open the repository's **Actions** tab and check whether `Oireachtas Refresh Validation Orchestrator`, an Oireachtas refresh, or `Oireachtas batch control` is currently running or queued.
2. Identify whether you are diagnosing an existing batch or creating a new one. Never reuse or guess a batch ID.
3. For a manual validation run, keep **Automatic promotion** off unless the explicit objective is a production change.
4. If inspecting or recovering production, run batch-control `status` before any `promote`, `rollback`, or `rollback-previous` operation and retain the output artifact.
5. Do not copy credentials, secret values, private account details, or unredacted sensitive logs into issues or documentation.
6. If the candidate fails refresh or validation, do not promote it and do not weaken validation to make it pass.

## Procedure A: Review a Scheduled Refresh

1. Open GitHub and navigate to the `eirepolitic-data-pipeline` repository.
2. Click **Actions**.
3. In the workflow list, click **Oireachtas Refresh Validation Orchestrator**.
4. Open the scheduled run you need to inspect.
5. Open the run summary and record the **run ID**, commit SHA, event (`schedule`), and batch ID shown in the orchestration plan/summary.
6. Confirm `prepare` succeeded.
7. Open the reusable `refresh` job. Confirm input normalization, candidate seeding, cadence table builds, and candidate manifest assembly succeeded.
8. Open the reusable `validation` job. Confirm enrichment staging, compatibility adapter build, six downstream-contract checks, compatibility/mismatch checks, enabled consumer validation, and final candidate reassembly succeeded.
9. If the scheduled run requested automatic promotion, confirm `promote` succeeded and the **Verify production pointer** step succeeded.
10. Confirm the automatic rollback step is skipped after successful pointer verification. If it ran, treat the run as a recovery event and inspect its output before declaring success.
11. Confirm the final `summary` job succeeded.
12. Retain or download the refresh, validation, and promotion evidence artifacts if the run is being used for audit, incident analysis, or a release decision.

A successful scheduled run is not proven by `refresh` alone. Scheduled success requires validation and, because scheduled runs set `auto_promote=true`, successful promotion and pointer verification.

## Procedure B: Create and Validate a Manual Candidate Without Promotion

This is the preferred manual verification path when you want production-sized evidence without changing the production pointer.

1. Open the repository in GitHub.
2. Click **Actions**.
3. Click **Oireachtas Refresh Validation Orchestrator**.
4. Click **Run workflow**.
5. Select the current intended branch, normally `main`.
6. Set **Refresh type** to `weekly`, `monthly`, or `yearly` as required.
7. Leave **Write an immutable candidate batch** enabled.
8. Leave **Run downstream consumer validation** enabled unless the specific test intentionally excludes consumers and that limitation will be recorded.
9. Leave **Promote only after all validation succeeds** disabled.
10. Click **Run workflow**.
11. Open the new run and record its run ID and generated batch ID from `prepare`.
12. Confirm `refresh` succeeds. Candidate seeding requires current production to use batch-pointer mode and the source production batch manifest to be validated.
13. Confirm `validation` succeeds. The reusable validation path stages auxiliary enrichments, builds core compatibility adapters, validates contracts/comparisons, runs enabled consumers, and reassembles the candidate.
14. Confirm the `promote` job is skipped because `auto_promote=false`.
15. Confirm `summary` succeeds.
16. Preserve the generated evidence artifacts and the exact batch ID if the candidate will be reviewed for a later promotion decision.

### Expected cadence defaults

When the orchestrator leaves date/page inputs blank, `process/oireachtas_refresh_inputs.py` applies:

| Refresh | Default mode | Date window | Page size |
| --- | --- | --- | ---: |
| weekly | `incremental` | 35 days before the as-of date through the as-of date | 100 |
| monthly | `incremental` | seven days before the previous month starts through the previous month end | 200 |
| yearly | `full` | previous calendar year, January 1 through December 31 | 200 |

The normalizer rejects unknown or duplicate tables, invalid modes, invalid chamber/house/date inputs, page sizes outside 1–200, sample counts outside 1–100, and reversed date windows. Control products are ordered at the end.

## Procedure C: Run a Manual Cadence Wrapper

Use a manual wrapper when you need cadence-specific table/date overrides and do not need the full orchestrator's validation/promotion sequence.

1. Open **Actions**.
2. Choose **Oireachtas Weekly Refresh**, **Oireachtas Monthly Refresh**, or **Oireachtas Yearly Refresh**.
3. Click **Run workflow**.
4. For a low-risk test, keep `mode=test` where offered and keep **publish_candidate** disabled.
5. If you intentionally need immutable candidate output, enable **publish_candidate** and record the generated `manual-<cadence>-<run_id>-<attempt>` batch ID.
6. Supply table/date/page overrides only when you can state why the default is unsuitable.
7. Run the workflow and inspect normalized inputs, table logs, DQ results, and candidate assembly output if publication was enabled.

These wrappers call the shared refresh workflow but **do not by themselves perform the full reusable downstream validation and automatic production promotion sequence**. Use Procedure B for an end-to-end candidate.

## Procedure D: Inspect Production and Previous Pointers

`status` is read-only at the pointer level and is the first batch-control operation to use during recovery.

1. Open **Actions**.
2. Click **Oireachtas batch control**.
3. Click **Run workflow**.
4. Set **Operation to perform** to `status`.
5. Leave **batch_id** and **required_tables** blank.
6. Click **Run workflow**.
7. Open the run and inspect **Run batch control**.
8. Download or retain the `oireachtas-batch-control-status-...` artifact.
9. Record the `production` mode/batch ID and the `previous` pointer before any production-changing operation.

Do not edit those pointer objects directly in S3.

## Procedure E: Promote an Already Validated Candidate

**This changes production state.** Use it only when the exact candidate has already passed the required validation and the publication decision has been made.

1. Complete Procedure D and record current `production` and `previous` state.
2. Confirm the exact candidate batch ID from its successful refresh/validation evidence. Do not type a reconstructed or guessed ID.
3. Open **Actions** → **Oireachtas batch control** → **Run workflow**.
4. Set **Operation to perform** to `promote`.
5. Enter the exact candidate in **batch_id**.
6. Leave **required_tables** blank.
7. Run the workflow.
8. The workflow validates batch-ID syntax, enables `OIREACHTAS_PUBLISH_LATEST` for the operation, and calls `process/oireachtas_batch_control.py promote`.
9. Promotion will still fail unless repository-level `OIREACHTAS_PUBLISH_ENABLED` already permits production publication and the candidate manifest status is `validated`.
10. After the workflow succeeds, immediately run Procedure D again.
11. Confirm `production.mode` is `batch` and `production.batch_id` equals the promoted batch.
12. Confirm `previous` records the prior production target expected for rollback.
13. Retain both the promotion artifact and the post-promotion status artifact.

If promotion succeeds but post-change status is unexpected, do not manually edit pointers; use the rollback procedure.

## Procedure F: Roll Back to the Previous Production Target

**This changes production state.** `rollback-previous` is the preferred recovery operation when the previous pointer is known-good and was captured by the normal promotion path.

1. Run Procedure D and capture current status evidence.
2. Verify that `previous` is populated and points to the intended recovery target.
3. Open **Actions** → **Oireachtas batch control** → **Run workflow**.
4. Choose `rollback-previous`.
5. Leave `batch_id` blank.
6. Run the workflow.
7. After success, run Procedure D again.
8. Verify that production now points to the expected previous target.
9. Record the failed/current batch, restored target, workflow run IDs, and reason for rollback.

The high-level orchestrator also invokes `rollback-previous` automatically if its promotion step succeeds but subsequent production-pointer verification fails.

## Procedure G: Roll Back to a Specific Validated Batch

Use this only when a specific validated historical batch—not simply the current `previous` pointer—is the intended recovery state.

1. Establish the exact target batch ID from retained batch evidence.
2. Confirm it is the intended validated batch; `rollback_batch()` refuses an unvalidated batch.
3. Run Procedure D and retain pre-change pointer state.
4. Open **Actions** → **Oireachtas batch control**.
5. Choose `rollback`.
6. Enter the exact validated batch ID in **batch_id**.
7. Run the workflow.
8. Run `status` again and verify production points to the intended batch.

The special batch ID `legacy_direct` exists for transition/recovery compatibility. Do not select it unless the explicit recovery decision is to restore direct logical-object reads rather than a validated immutable batch.

## Candidate Validation Stop Conditions

Treat these as hard stops for automatic promotion:

- refresh/table builder failure;
- table DQ failure;
- candidate object or batch-entry failure;
- candidate manifest not `validated`;
- stale auxiliary enrichment: staging refuses an object whose age exceeds its contract maximum;
- downstream contract failure for readability, minimum rows, columns, PK integrity, or freshness;
- compatibility/reference threshold failure;
- mismatch review failure;
- enabled member-profile metric build failure;
- enabled Instagram candidate smoke failure;
- final candidate reassembly failure.

Do not convert a stop condition into a pass by weakening thresholds during an incident unless that configuration change is separately reviewed as an intentional contract change.

## Validation and Success Criteria

### Manual candidate success

A safe manual candidate run is complete when:

- `prepare`, `refresh`, and `validation` all succeed;
- final candidate reassembly reports a validated candidate;
- consumer checks requested for the run succeed;
- `promote` is skipped when `auto_promote=false`;
- evidence identifies the exact batch ID and GitHub run.

### Scheduled production success

A scheduled run is complete when:

- `prepare`, `refresh`, `validation`, `promote`, and `summary` succeed;
- post-promotion status shows `production.mode=batch`;
- `production.batch_id` equals the generated candidate batch;
- automatic rollback is not required.

Observed runtime evidence: scheduled run `30740881592` on 2026-08-02 met these criteria.

## Failure Modes and Escalation

| Failure | Safe response | Evidence to retain | Escalation / next investigation |
| --- | --- | --- | --- |
| Input normalization fails | Stop; correct the invalid cadence/table/date/page input | prepare/normalize log | `process/oireachtas_refresh_inputs.py` and orchestration tests |
| Candidate seed fails | Do not bypass seeding; inspect production pointer/source batch validation | seed log, production status, source batch ID | `process/oireachtas_seed_candidate.py`, batch-control status |
| One or more table builds fail | Do not promote; fix/rerun into a candidate | table log, manifest, DQ payload | table builder and canonical catalogue |
| Auxiliary enrichment is stale | Do not copy stale data manually; refresh/reconcile that enrichment first | contract name, source age, logical/source key | relevant enrichment successor/contract owner |
| Contract validation fails | Do not promote; diagnose exact row/column/PK/freshness error | downstream-contract JSON | contracts config/code and policy reference |
| Compatibility/mismatch fails | Preserve report; reconcile canonical vs reference behavior | comparison/mismatch artifacts | compatibility adapter and thresholds |
| Consumer smoke fails | Do not promote when consumer validation is required | member metrics/Instagram smoke artifacts | relevant downstream P1 documentation/code |
| Promote says publication disabled | Stop; do not change the repository variable as routine recovery | batch-control log and current status | owner/security decision for publication control |
| Promote rejects batch as unvalidated | Stop; rerun/fix validation | batch manifest and validation output | batch implementation / validation workflow |
| Pointer verification fails after orchestrator promotion | Let automatic `rollback-previous` run; then verify status | pre/post status, promotion and rollback artifacts | batch/pointer implementation |
| Rollback fails or pointer state is ambiguous | Stop pointer mutation; retain all status artifacts | production/previous payloads and run IDs | system owner; inspect batch manifests before another change |

## Security Guidance

- Never expose AWS secret values from GitHub Actions.
- Do not add secret values to workflow inputs, documentation, issues, screenshots, or copied logs.
- Use the checked-in batch-control workflow rather than ad-hoc production pointer edits.
- Exact live IAM/bucket policy is not established by source. If permissions must be diagnosed at that level, obtain the relevant AWS configuration as a separate controlled source.
- Treat unexpected access-denied, cross-account, or object-integrity behavior as an access/infrastructure issue rather than weakening application validation.

## Known Limitations

- Scheduled end-to-end behavior has observed runtime evidence; this documentation workstream did not intentionally execute a new manual production promotion or rollback.
- GitHub workflow presence does not prove every repair/trial workflow is a current production procedure. This runbook intentionally uses the production orchestrator and batch-control paths only.
- Exact live IAM/S3 policy, versioning, lifecycle, Glue, and Athena configuration remain outside source verification.
- `legacy_direct` exists for transition/recovery compatibility and should not be selected casually.

## Follow-up Work

After any failed or recovered production run:

1. retain exact run IDs, batch IDs, commit SHA, and relevant artifacts;
2. record whether production was ever promoted and, if so, the pre/post pointer state;
3. correct implementation/configuration rather than editing candidate evidence;
4. rerun a new immutable candidate when data/code must change;
5. update this runbook if current workflow behavior has changed.

## Next Safe Action

With orchestration documented, finish the P0 write-policy and downstream-contract reference so operators can interpret policy/contract failures without reading YAML and Python directly.

## Related Documents

- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)
- [Oireachtas Canonical Data-Product Catalogue](/projects/data/oireachtas-canonical-data-product-catalogue/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `.github/workflows/oireachtas_refresh_validation_orchestrator.yml`, `oireachtas_refresh_reusable.yml`, `oireachtas_validation_reusable.yml`, `oireachtas_weekly_refresh.yml`, `oireachtas_batch_control.yml`; `process/oireachtas_refresh_inputs.py`, `oireachtas_seed_candidate.py`, `oireachtas_reassemble_candidate.py`, `oireachtas_batch_control.py`, `oireachtas_stage_downstream_contracts.py`, `oirechtas_validate_downstream_contracts.py` equivalent current validation helper path; `extract/oireachtas/batch.py`, `io_s3.py`, `contracts.py`; orchestration/write-semantics tests; GitHub Actions run `30740881592`.
- Verified by: High Director
- Verification scope: schedule/manual boundaries, candidate construction, validation gates, promotion/rollback controls, pointer verification, operational evidence, stop conditions, and safe GitHub Actions procedures.
- Known unverified steps: no production-changing manual dispatch was performed specifically for this documentation workstream.
