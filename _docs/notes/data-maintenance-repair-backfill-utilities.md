---
title: Data maintenance, repair, and backfill utilities
summary: Operational reference for current and retained eirepolitic-data-pipeline maintenance helpers, including read-only Oireachtas inventory, destructive S3 column deletion, CSV-to-Parquet conversion, repair CI, and the branch-scoped July 2026 Oireachtas validation-fixes backfill/acceptance campaign.
section: notes
doc_type: reference
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - GitHub Actions
  - AWS S3
  - pandas
  - PyArrow
order: 44
permalink: /projects/notes/data-maintenance-repair-backfill-utilities/
related:
  - /projects/repositories/eirepolitic-data-pipeline/
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/runbooks/oireachtas-refresh-validation-orchestration/
---

# Data maintenance, repair, and backfill utilities

## Purpose

This page groups supporting maintenance, repair, conversion, audit, and one-off backfill tooling in `eirepolitic-data-pipeline` that should not be mistaken for the normal scheduled Oireachtas production path.

The normal production refresh, candidate validation, promotion, rollback, write-policy, and contract controls are documented separately. This reference focuses on tools whose purpose is to inspect, repair, convert, delete, or validate exceptional data states.

## Scope and status summary

| Utility | Current source | Mutation scope | Current status |
| --- | --- | --- | --- |
| Oireachtas baseline inventory | `process/oireachtas_audit_inventory.py`, `.github/workflows/oireachtas_baseline_audit.yml` | read-only S3 listing; local/GitHub artifact output | current manual diagnostic |
| S3 CSV+Parquet column deleter | `process/delete_s3_column.py`, `.github/workflows/column_deleter.yml` | destructive in-place overwrite of two S3 objects | current active manual workflow; high risk |
| Debate classified CSV → Parquet converter | `process/debate_speeches_csv_to_parquet.py` | overwrites configured Parquet object; source CSV unchanged | current standalone compatibility/conversion helper; no dedicated workflow identified |
| Oireachtas repair CI | `.github/workflows/oireachtas_repair_ci.yml` | no production/S3 mutation | current code-quality/regression workflow; retains repair-branch trigger |
| Validation-fixes CI | `.github/workflows/oireachtas_validation_fixes_ci.yml` | no S3 mutation | retained branch-scoped repair-campaign CI |
| Validation-fixes candidate backfill | `.github/workflows/oireachtas_validation_fixes_candidate.yml` | builds an immutable candidate batch; no direct promotion step | retained July 2026 repair campaign, hard-coded branch/batch/date |
| Validation-fixes acceptance | `process/oireachtas_verify_validation_fixes.py`, `.github/workflows/oireachtas_validation_fixes_acceptance.yml` | read candidate/production/API; writes evidence to repair branch and workflow artifact | retained July 2026 repair campaign |

These classifications are based on current `main` plus branch/workflow configuration. A workflow file being present does not by itself mean it belongs in normal production operations.

## What is intentionally excluded

The following are not duplicated here because they are part of the normal Unified Oireachtas control plane:

- `process/oireachtas_seed_candidate.py`;
- `process/oireachtas_reassemble_candidate.py`;
- `process/oireachtas_batch_control.py`;
- reusable refresh/validation workflows;
- production promotion/rollback;
- scheduled cadence wrappers;
- downstream-contract staging/validation.

Those are documented under the Unified Oireachtas platform and refresh/validation runbook.

Legacy enrichment/classification/media tools are reserved for the P3 successor/status reconciliation and are not promoted to current maintenance utilities merely because they remain executable.

## 1. Oireachtas baseline inventory

### Purpose

`process/oireachtas_audit_inventory.py` creates a read-only object inventory for selected Oireachtas S3 prefixes.

Current scanned prefixes are:

```text
processed/oireachtas_unified/latest/
processed/oireachtas_unified/compat/
processed/oireachtas_unified/silver/
processed/oireachtas_unified/gold/
processed/oireachtas_unified/control/
processed/oireachtas_unified/review/
```

For each S3 object it records:

- prefix;
- key;
- size;
- ETag;
- last-modified UTC timestamp;
- storage class.

It also writes a JSON summary with object count, total bytes, per-prefix counts, bucket/region, generation time, and GitHub run/ref/SHA metadata when available.

### Workflow

Workflow: **Oireachtas baseline audit**.

It is `workflow_dispatch` only, uses Python 3.12, and explicitly sets:

```text
OIREACHTAS_PUBLISH_ENABLED=false
OIREACHTAS_PUBLISH_LATEST=false
```

The workflow uploads `artifacts/oireachtas-baseline-audit/` for 30 days.

### Risk classification

**Read-only / low mutation risk.**

The script calls S3 list APIs and writes only local workflow artifacts. It does not write S3 data products or production pointers.

### Limitation

This is an object inventory, not a row-level data-quality check. It can establish object presence/size/timestamps but not semantic correctness.

## 2. Delete Column From S3 CSV+Parquet

### Purpose

`process/delete_s3_column.py` deletes one named column from a caller-specified CSV object and a caller-specified Parquet object in the same bucket.

Current environment inputs:

- `CSV_KEY` — required;
- `PARQUET_KEY` — required;
- `COLUMN` — required;
- `STRICT` — optional, default `0`;
- `S3_BUCKET` — default `eirepolitic-data`;
- `AWS_REGION` — default `ca-central-1`.

### Workflow

Workflow: **Delete Column From S3 CSV+Parquet (Manual)**.

Manual inputs are passed directly to the script. It runs on Python 3.11 and uses AWS credentials from GitHub Actions secrets.

The workflow is still listed active in the GitHub workflow registry.

Observed runs:

- `21647221436`, 2026-02-03: success;
- `21878566586`, 2026-02-10: success.

These prove historical use of the destructive workflow, not that every future invocation is safe.

### Exact mutation behavior

The script:

1. downloads the complete CSV;
2. drops the requested column if present;
3. downloads the complete Parquet;
4. drops the requested column if present;
5. if `STRICT=1`, aborts before either write when the column was absent from either representation;
6. otherwise overwrites the original CSV key;
7. then overwrites the original Parquet key.

Even when a column is absent and `STRICT=0`, the original bytes are written back for that representation.

### `STRICT` is not a safety/dry-run mode

`STRICT=1` means only:

> fail if the column is absent from either file.

It does **not** mean:

- dry-run;
- create backup;
- require confirmation;
- compare schemas after mutation;
- require matching row counts;
- create a rollback object;
- restrict keys to an approved prefix.

### High-risk controls currently absent

Current implementation has no:

- dry-run option;
- confirmation token or typed acknowledgement;
- automatic backup/version copy;
- rollback command;
- allow-list of permitted S3 prefixes;
- schema/version manifest update;
- candidate-batch isolation;
- validation that the CSV and Parquet represent the same dataset before mutation.

CSV and Parquet writes are sequential. If the CSV overwrite succeeds and the Parquet overwrite fails, the pair can remain inconsistent.

### Safe operating rule

Do not use this workflow as routine schema management.

Before any invocation, an operator should independently establish:

1. the exact two S3 keys;
2. that both objects represent the intended dataset;
3. that the column is genuinely obsolete in downstream consumers;
4. that a recoverable previous version/backup exists outside this tool;
5. that the dataset is not a canonical Oireachtas object managed by table registry/write-policy/promotion controls.

The tool itself does not provide those safeguards.

## 3. Debate classified CSV → Parquet converter

### Purpose

`process/debate_speeches_csv_to_parquet.py` reads a classified debate CSV and writes a Parquet representation.

Defaults:

```text
S3_BUCKET=eirepolitic-data
CSV_KEY=processed/debates/debate_speeches_classified.csv
PARQUET_KEY=processed/debates/parquets/debate_speeches_classified.parquet
FORCE_STRING=1
```

### Transformation behavior

The source CSV is not modified.

Before writing Parquet, every column name is normalized by:

- trimming;
- lowercasing;
- converting whitespace/hyphens to underscores;
- removing characters outside ASCII letters/numbers/underscore;
- collapsing duplicate underscores;
- adding `_2`, `_3`, ... suffixes when normalized names collide.

With default `FORCE_STRING=1`, CSV fields are read as strings to reduce type inference surprises.

### Mutation and risk

The configured Parquet object is overwritten in place.

There is no:

- dry-run;
- previous-version backup;
- schema manifest;
- CSV-vs-Parquet post-write comparison;
- candidate-batch/pointer awareness.

Unlike the column deleter, the original CSV remains intact and can serve as a source for regeneration, so the destructive risk is lower. However, normalized Parquet column names do **not** necessarily match the source CSV column names exactly.

### Current status

The script exists on current `main`, but no dedicated current workflow was identified in the workflow tree. Treat it as a standalone compatibility/conversion helper, not a scheduled pipeline stage.

## 4. Oireachtas repair CI

### Workflow

`.github/workflows/oireachtas_repair_ci.yml` is a non-mutating validation workflow.

Triggers:

- manual dispatch;
- pull requests touching Oireachtas code/config/workflows/tests;
- pushes to `repair/oireachtas-production-hardening`.

Current branch inventory confirms `repair/oireachtas-production-hardening` still exists.

The workflow:

1. compiles Python under `extract/oireachtas`, `process`, and `tests`;
2. parses Oireachtas YAML;
3. validates the table registry by calling `python -m extract.oireachtas.build_table --list-tables --json`;
4. runs all `test_oireachtas_*.py` unit tests.

### Risk classification

**Read-only code-quality gate.**

It has `contents: read` and no AWS credentials or S3 mutation step in the inspected workflow.

Despite the name “repair CI,” it now functions as a broad Oireachtas regression gate as well as retaining its historical repair-branch trigger.

## 5. July 2026 Oireachtas validation-fixes campaign

Three current files form a retained repair campaign around branch `fix/oireachtas-validation-findings`:

- `o...validation_fixes_ci.yml`;
- `o...validation_fixes_candidate.yml`;
- `o...validation_fixes_acceptance.yml` plus `process/oireachtas_verify_validation_fixes.py`.

Current branch inventory confirms both:

```text
fix/oireachtas-validation-findings
release/oireachtas-validation-fixes-20260719-3
```

still exist.

These files are highly specific to a dated repair effort and should not be treated as a generic reusable backfill interface.

### Repair regression CI

`o...validation_fixes_ci.yml` checks the repair branch's historical-dedupe, business-key merge, refresh ordering, control-manifest counts, and repair regressions.

It explicitly checks configured business keys for:

```text
silver_member_parties:
member_code, party_uri, party_start, party_end

silver_member_constituencies:
member_code, constituency_uri, represent_start, represent_end
```

The workflow checks out `fix/oireachtas-validation-findings` even on manual dispatch.

### Candidate backfill

`o...validation_fixes_candidate.yml` calls the normal reusable refresh workflow with:

```text
refresh_type: yearly
mode: backfill
chamber: dail
house_no: 34
date_start: 2024-11-29
date_end: 2026-07-19
page_size: 200
batch_id: validation-fixes-20260719-3
publish_candidate: true
```

It lists all 31 canonical products and then runs the reusable validation workflow with consumers enabled for that exact batch.

Important boundary:

- `publish_candidate: true` means build/write the immutable candidate batch;
- the workflow contains **no production promotion step**.

This is safer than writing current production directly, but it is not parameterized enough to serve as the normal operator backfill interface because branch, dates, tables, and batch ID are hard-coded.

### Acceptance verifier

`process/oireachtas_verify_validation_fixes.py` performs issue-specific acceptance checks against candidate batch `validation-fixes-20260719-3` when called by the workflow.

Current checks include:

- candidate manifest validated with at least 31 products and no manifest validation errors;
- no duplicate member-party business keys;
- no duplicate member-constituency business keys;
- current party values unchanged relative to production;
- current constituency values unchanged relative to production;
- recent official debate sections present;
- recent official questions present;
- official bill versions present for candidate bills;
- official bill-debate business rows present;
- control manifest row counts/schema hashes/column counts match actual candidate CSV and Parquet objects.

For recent/legislation completeness checks it calls the public Oireachtas API directly and compares normalized official rows with the candidate.

The verifier returns exit code 1 when any acceptance check fails.

### Acceptance workflow side effects

`o...validation_fixes_acceptance.yml` sets production publication flags false and runs the verifier against the fixed candidate.

However, it has `contents: write` and intentionally commits generated acceptance evidence back to the `fix/oireachtas-validation-findings` branch under:

```text
docs/oireachtas_validation/fixes_acceptance/
```

It also uploads the same evidence as a GitHub artifact retained for 365 days.

Thus the workflow is **S3 read-only but GitHub-mutating**.

### Current status classification

These validation-fixes files are retained, branch-specific repair-campaign tooling.

Reasons they should not be presented as the normal current backfill interface:

- hard-coded repair branch;
- hard-coded batch ID;
- hard-coded historical date window;
- branch-specific regression test set;
- acceptance evidence committed back to that branch;
- normal production refresh/validation orchestration has since been documented and observed succeeding separately.

Do not delete or repurpose them merely because they are campaign-specific; they preserve repair provenance and can be useful forensic/reference evidence.

## Backfill decision rule

For a new Oireachtas backfill, prefer the current canonical refresh/candidate/validation controls documented in the production runbook rather than editing and reusing the July validation-fixes workflow blindly.

A new backfill should use:

- a new immutable batch ID;
- an explicitly reviewed date/window and table set;
- current reusable refresh and validation workflows;
- candidate-only publication first;
- current downstream contracts/consumer validation;
- deliberate promotion only after validation.

Whether to add a reusable generic backfill controller is an architecture/operations decision, not a documentation-only change.

## Utility safety matrix

| Utility | Reads production | Writes S3 | Writes GitHub | Dry-run | Automatic backup | Candidate isolation |
| --- | --- | --- | --- | --- | --- | --- |
| baseline inventory | object listing only | no | no | effectively read-only | n/a | n/a |
| column deleter | yes, arbitrary caller keys | **yes, destructive overwrite** | no | **no** | **no** | **no** |
| debate CSV→Parquet | yes, configured CSV | yes, Parquet overwrite | no | no | source CSV remains | no |
| repair CI | source only | no | no | n/a | n/a | n/a |
| validation-fixes CI | source only | no | no | n/a | n/a | n/a |
| validation-fixes candidate | reads current/candidate via normal platform | yes, immutable candidate | no | candidate-first | immutable batch | **yes** |
| validation-fixes acceptance | candidate + production + public API | no repair write | **yes, evidence branch** | verification only | n/a | explicit fixed candidate |

## Credential and access boundary

The S3-reading/writing workflows use GitHub Actions AWS secrets. Exact secret values are not documented.

The column deleter uses whatever S3 permissions are granted to its workflow credentials and contains no application-level prefix allow-list. Its practical blast radius is therefore governed primarily by IAM/bucket policy plus operator-supplied keys.

The baseline audit and acceptance workflows explicitly disable Oireachtas publication flags where relevant, but those flags are application-level controls and do not replace IAM restrictions.

Live IAM/bucket-policy state has not been inspected for this P2 reference.

## Failure and recovery guidance

### Column deleter failure

If the workflow fails after either write begins, do not simply rerun until confirming the current state of both objects.

Check:

1. whether CSV contains the target column;
2. whether Parquet contains the target column;
3. row counts and expected schema in both;
4. whether a recoverable prior S3 version/backup is available.

The script has no internal rollback.

### CSV→Parquet conversion failure

The CSV source is left untouched. Fix the conversion/configuration issue and regenerate the Parquet output from the source CSV after confirming the expected normalized schema.

### Candidate backfill failure

Do not promote an incomplete/failed candidate. Inspect refresh and reusable-validation failures using the normal Oireachtas runbook. A failed immutable candidate can be left unpromoted and superseded by a new batch.

### Acceptance failure

Treat a failed acceptance check as evidence that the repair candidate does not satisfy that campaign's specific gate. Do not weaken the check solely to obtain a green workflow.

## Known limitations

- There is no single generic current maintenance CLI that wraps all utilities with consistent backup/dry-run/confirmation semantics.
- The destructive column deleter is substantially less guarded than the current Oireachtas immutable-candidate publication model.
- The debate converter changes column names in the Parquet representation and has no dedicated current workflow.
- Repair/validation-fixes workflows retain branch/date/batch assumptions from specific 2026 campaigns.
- Branch existence proves retained source, not current production intent.
- Workflow registry “active” state proves GitHub can dispatch a workflow; it does not prove the workflow is recommended for routine operations.
- Exact live S3 versioning/IAM controls have not been verified here.

## Next safe development action

P2 target 38 is complete once this page passes documentation validation, merges, and its exact merge SHA succeeds in Pages.

The next assigned priority is P3 targets 47–54. Those should reconcile each retained legacy enrichment/classification/media/destructive/editorial component against current source and successor systems rather than creating duplicate current pages.

## Related documents

- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)
- [Operate Oireachtas refresh, validation, promotion, and rollback](/projects/runbooks/oireachtas-refresh-validation-orchestration/)
- [Oireachtas write policies and downstream contracts](/projects/notes/oireachtas-write-policies-downstream-contracts/)

## Verification record

- Last verified: `2026-08-07`
- Verified implementation/configuration: complete current `process/` and workflow trees; `process/oireachtas_audit_inventory.py`; `.github/workflows/oireachtas_baseline_audit.yml`; `process/delete_s3_column.py`; `.github/workflows/column_deleter.yml`; `process/debate_speeches_csv_to_parquet.py`; `.github/workflows/oireachtas_repair_ci.yml`; `.github/workflows/oireachtas_validation_fixes_ci.yml`; `.github/workflows/oireachtas_validation_fixes_candidate.yml`; `.github/workflows/oireachtas_validation_fixes_acceptance.yml`; `process/oireachtas_verify_validation_fixes.py`; current branch inventory.
- Observed runtime evidence: column-deleter workflow ID `230193524`, successful runs `21647221436` and `21878566586`.
- Verification scope: utility classification, mutation scope, destructive risk, dry-run/backup/rollback controls, candidate isolation, branch-specific repair/backfill behavior, acceptance checks, credential boundary, failure/recovery guidance, and current-vs-campaign status.
