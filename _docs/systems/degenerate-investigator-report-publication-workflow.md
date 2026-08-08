---
title: degenerate_investigator S3-to-Repository Report Publication Workflow
summary: Source-grounded documentation for copying a generated Markdown fight-analysis report from S3 into the repository and conditionally committing/pushing it through a write-enabled GitHub Actions workflow.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator S3-to-Repository Report Publication Workflow

## Purpose

P2-43 publishes one already-generated Markdown fight-analysis report from S3 into the `degenerate_investigator` repository.

It is a publication/copy boundary, not an analytical computation stage. It does not ingest UFC data, train or load a model, rescore a matchup, regenerate prose, or validate analytical correctness.

## Source paths

- export helper: `process/export_s3_report_to_repo.py`;
- workflow: `.github/workflows/export_latest_report_to_repo.yml`;
- default repository artifact: `reports/latest_fight_report.md`.

## Python export helper

`process/export_s3_report_to_repo.py` contains only `main()`.

Runtime configuration:

- `S3_BUCKET` — default `degenerative-investigator`;
- `AWS_REGION` — default `us-east-2`;
- `REPORT_KEY` — default `processed/reports/ufc-327-prochazka-vs-ulberg_fight_report.md`;
- `OUTPUT_PATH` — default `reports/latest_fight_report.md`.

Processing sequence:

1. create a boto3 S3 client in the configured region;
2. call `get_object()` for `S3_BUCKET` / `REPORT_KEY`;
3. read the object body;
4. decode with `utf-8-sig`, replacing invalid byte sequences;
5. create the output parent directory when necessary;
6. write UTF-8 text to `OUTPUT_PATH`;
7. print the source S3 URI and destination path.

The helper itself does not run git commands and does not need repository credentials.

## GitHub Actions workflow

`.github/workflows/export_latest_report_to_repo.yml` is named `Export Latest Report To Repo (Manual)`.

Trigger:

- `workflow_dispatch` only.

Inputs:

- `report_key` — S3 Markdown key, default `processed/reports/ufc-327-prochazka-vs-ulberg_fight_report.md`;
- `output_path` — repository destination, default `reports/latest_fight_report.md`.

The committed report default is event-specific and must be checked before publishing another event.

Runner/runtime:

- `ubuntu-latest`;
- Python 3.11;
- timeout 30 minutes;
- installs `requirements.txt`;
- executes `python process/export_s3_report_to_repo.py`.

## Permission boundary

The workflow declares:

`permissions: contents: write`

This distinguishes it from the analytical pipeline workflows, which use `contents: read`.

Checkout uses:

`persist-credentials: true`

so the GitHub Actions token remains available for the later `git push`.

This workflow is therefore a repository-write control boundary. Changes to its permissions, authentication mechanism, target branch behavior, or push strategy are security/architecture decisions rather than routine documentation edits.

## AWS configuration

The workflow passes these GitHub secret names:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`.

It sets:

- `S3_BUCKET=degenerative-investigator`;
- `REPORT_KEY` from workflow input/default;
- `OUTPUT_PATH` from workflow input/default.

Never document secret values.

## Commit/push behavior

After copying the file, the workflow:

1. configures the Git identity as `github-actions[bot]`;
2. runs `git add "$OUTPUT_PATH"`;
3. runs `git diff --cached --quiet || git commit -m "Export latest report to repo"`;
4. runs `git push`.

Consequences:

- unchanged exported content creates no commit;
- changed content creates one commit;
- `git push` is attempted even when no new commit was created;
- the push targets the checked-out branch/ref behavior established by `actions/checkout` and the workflow event context;
- there is no pull request step in this workflow.

## Publication lifecycle

The intended lifecycle is:

1. target-event scoring produces prediction objects;
2. report generation produces `processed/reports/{event_slug}_fight_report.md` in S3;
3. an operator dispatches the export workflow with that exact report key;
4. the helper copies the S3 Markdown object into the checkout;
5. git stages the configured output path;
6. unchanged content yields no new commit;
7. changed content is committed and pushed.

The publication workflow does not automatically run after report generation.

## Source-of-truth boundary

A successful repository publication proves only that the selected S3 Markdown object was copied and, if changed, pushed.

It does **not** prove:

- the report was generated from the intended event;
- the prediction artifact used a trained model rather than heuristic fallback;
- the trained model was Random Forest rather than dummy-prior;
- the report retained full scoring provenance;
- recent-news or market context was complete;
- model metrics were acceptable;
- the report itself was analytically correct.

Use upstream prediction/model/report-generation artifacts for those questions.

## Output-path risk

`OUTPUT_PATH` is a workflow input and is passed directly to `Path(...)`, `git add`, and repository write logic.

The source does not constrain the path to `reports/` or validate it against an allowlist. A caller with permission to dispatch the workflow can select another repository-relative path, subject to filesystem/git behavior and token permissions.

Changing this design to enforce an allowlist is an implementation/security decision.

## Failure modes

- selected `REPORT_KEY` does not exist;
- S3 read/authentication/region failure;
- S3 object contains unexpected text/encoding content;
- invalid or unwritable `OUTPUT_PATH`;
- dependency installation failure;
- repository token lacks write permission;
- branch protection or repository rules reject direct push;
- concurrent changes cause non-fast-forward push rejection;
- wrong event-specific default/report key publishes the wrong report;
- caller chooses an unintended output path;
- checkout/push semantics change because the workflow or GitHub Actions behavior changes.

## Rerun and recovery

### S3/read failure

Correct the report key or AWS access issue, then rerun only this publication workflow. Do not regenerate analytical artifacts unless they are themselves wrong.

### Wrong report published

Dispatch the workflow again with the correct `REPORT_KEY` and intended `OUTPUT_PATH`. The next successful changed export creates another repository commit restoring the desired content.

### Push failure after local export

Fix the repository-write/branch condition and rerun the workflow. The checkout is ephemeral, so do not assume the prior runner's local commit survives.

### No-change run

No recovery is required when the selected report content is already identical to the repository file. The conditional commit intentionally leaves history unchanged.

## Security considerations

- never publish AWS credential values;
- `contents: write` is required only for this publication path and should remain isolated from read-only analytical jobs;
- `persist-credentials: true` intentionally retains push credentials in the checkout;
- `OUTPUT_PATH` is caller-controlled and not allowlisted;
- S3 Markdown is external persisted content copied into the repository without analytical/content validation by this workflow;
- live branch-protection, token policy, IAM policy, S3 bucket policy, and audit controls are not proven by source.

## Limitations

- manual dispatch only;
- event-specific default report key;
- no automatic check that the selected report is the newest report;
- no automatic model/scoring provenance validation;
- no checksum/run identifier linking the repository copy to upstream objects;
- no pull-request review path; changed content is committed/pushed directly;
- caller-controlled output path is not restricted to `reports/`;
- no concurrency/rebase/retry logic for push conflicts;
- repository report is a publication artifact, not the authoritative analytical source.

## Related documentation

- [degenerate_investigator Fight-Analysis Report Generator](degenerate-investigator-fight-analysis-report-generator.md)
- [degenerate_investigator Target-Event Scoring](degenerate-investigator-target-event-scoring.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [degenerate_investigator Repository and UFC Analytics Architecture](../repositories/degenerate-investigator.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

Any change to report keying, output path, repository permissions, checkout credentials, commit conditions, push behavior, or publication strategy should update this page in the same change set. Do not infer upstream analytical correctness from publication success.
