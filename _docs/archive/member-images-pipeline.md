---
title: Member Images Pipeline
summary: Historical pipeline that scraped Oireachtas member profile images and published reusable S3 photo-URL datasets before its documentation was archived.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic
technologies:
  - Python
  - Amazon S3
  - Beautiful Soup
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-06
last_verified: 2026-02-27
archived_date: 2026-08-05
archive_reason: Historical pipeline documentation migrated into the knowledge-base archive.
permalink: /projects/pipelines/member_images_pipeline/
---

# Member Images Pipeline

## Archive Summary

The Member Images Pipeline is preserved as historical documentation for a pipeline that read 34th Dáil member records from S3, visited public Oireachtas member profiles, extracted profile-image URLs, and published CSV and Parquet outputs.

The page was moved into the knowledge-base archive on `2026-08-05`. It must not be treated as current operational guidance.

## Archive Status

- Archived on: `2026-08-05`
- Archive reason: Historical pipeline documentation migrated into the knowledge-base archive.
- Replacement: None documented.
- Current recommendation: Verify the current member-image implementation and source repository before reusing any path, workflow, bucket, command, or configuration recorded here.

## Historical Context

The pipeline existed to create a reusable table of member photo URLs from Oireachtas profile pages. It used Python, Amazon S3, Beautiful Soup, and GitHub Actions and was documented against the repository named `eirepolitic`.

## Last Known Implementation State

The last verified record, dated `2026-02-27`, described this behavior:

- Input: `raw/members/oireachtas_members_34th_dail.csv`.
- Required input columns: `member_code`, `full_name`, `uri`.
- Processing script: `process/members_photo_urls.py`.
- Workflow: `.github/workflows/member_photo_urls.yml`.
- Operation: manually triggered workflow with a `test_rows` limit.
- Resume behavior: existing output was reused and only rows missing `photo_url` were attempted.
- CSV output: `processed/members/members_photo_urls.csv`.
- Parquet output: `processed/members/parquets/members_photo_urls.parquet`.
- Output columns: `member_code`, `full_name`, `photo_url`.
- Historical default bucket: `eirepolitic-data`.
- Historical default region: `ca-central-1`.
- Recorded settings: `REQUEST_TIMEOUT`, `DELAY_BETWEEN_REQUESTS`, `AUTOSAVE_INTERVAL`, and `TEST_ROWS`.

These are last-known historical facts, not a claim about the current implementation.

## Source of Truth

The archived record identifies the following historical sources:

- Former repository: `eirepolitic`.
- Script: `process/members_photo_urls.py`.
- Workflow: `.github/workflows/member_photo_urls.yml`.
- This preserved archive page: `_docs/archive/member-images-pipeline.md`.

The former repository and source paths could not be verified through the currently configured GitHub connection on `2026-08-06`. Therefore this page preserves the last-known record only. A current repository or deployed system, if located later, should take precedence over this archive.

## Why It Was Archived

The recorded archive reason is that historical pipeline documentation was migrated into the knowledge-base archive. No separate technical retirement reason is documented in the preserved record, so none is inferred here.

## Successor or Replacement

No successor or replacement is documented in the preserved archive record.

A future maintainer should locate and verify the current member-image implementation before deciding whether this historical pipeline has been superseded, retired without replacement, or moved.

## Historical Operation

The preserved command was:

```bash
python process/members_photo_urls.py
```

Historical validation guidance was to confirm required input columns, inspect workflow failure counts, and verify both S3 output files.

This command and those validation steps have not been reverified against a current source repository and must not be executed as current guidance without first locating the authoritative implementation.

## Historical Failure Modes

The archived record identified:

- Oireachtas page structure changes.
- Missing profile images.
- Request failures or throttling.
- Missing S3 permissions.

These remain useful historical context but have not been checked against any current implementation.

## Security Considerations

Do not restore or copy historical credentials, access keys, tokens, connection strings, or secret values from old environments. The bucket and region names above are preserved only because they were already part of the historical public documentation; any current access must be verified through the current authoritative system and approved credentials.

## Known Limitations

- The former source repository is not available through the currently configured GitHub connection.
- The script and workflow paths are therefore unverified as current paths.
- No successor is documented.
- The archived command, bucket location, workflow behavior, and failure modes describe the last-known state only.
- The page does not establish whether the pipeline is still deployed, moved, or fully retired.

## Outstanding Historical Questions

- Does a current member-image pipeline exist in another repository or platform?
- Was `eirepolitic` renamed, moved, made unavailable, or retired?
- Is there a successor dataset or workflow that should be linked from this archive?

## Next Safe Action

Before changing or recreating this pipeline, locate the current authoritative member-image repository, workflow, or dataset and verify its implementation. If no current implementation exists, treat any recreation as new work requiring its own repository/system documentation and architecture review rather than modifying this archived record as though it were live.

## Related Documents

No verified successor document is currently available in this documentation site.

## Verification Record

- Last verified: `2026-02-27`
- Verified against: preserved historical archive record and its recorded script, workflow, input, output, and configuration names
- Verified by: historical documentation record; archive review by High Director on `2026-08-06`
- Verification scope: historical facts already present in this archive page and archive metadata
- Unverified areas: current repository availability, current script/workflow locations, current deployment state, current S3 objects, and successor implementation
