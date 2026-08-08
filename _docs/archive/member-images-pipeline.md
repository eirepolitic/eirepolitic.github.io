---
title: Member Images Pipeline
summary: Historical Oireachtas member-photo scraping pipeline retained as the source producer for the newer Unified Oireachtas member-photo enrichment and compatibility adapter.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - Amazon S3
  - Beautiful Soup
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-07
last_verified: 2026-08-07
archived_date: 2026-08-05
archive_reason: Historical standalone pipeline record retained for lineage; current Oireachtas member-photo enrichment consumes legacy photo-index outputs rather than replacing the scraping/discovery function.
permalink: /projects/pipelines/member_images_pipeline/
related:
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/systems/member-profile-metrics-builder/
  - /projects/systems/instagram-constituency-campaign-rendering/
---

# Member Images Pipeline

## Current status

This page is an **archive/lineage record**, but the historical implementation is now directly verifiable in the current repository.

Retained source:

```text
process/members_photo_urls.py
.github/workflows/member_photo_urls.yml
```

Current successor-layer source:

```text
extract/oireachtas/enrichment_member_photo_urls.py
.github/workflows/oireachtas_member_photo_enrichment_trial.yml
```

The successor layer does **not** scrape Oireachtas profile pages. It reads an existing legacy photo-URL CSV, adds enrichment/review metadata, and produces a Unified Oireachtas compatibility adapter.

Therefore full retirement of the legacy scraping/discovery function is **not established**.

## Retained legacy scraper

`process/members_photo_urls.py` reads a member roster containing:

- `member_code`;
- `full_name`;
- `uri`.

Its script-level default input is:

```text
raw/members/oireachtas_members_34th_dail.csv
```

For each row still missing `photo_url`, the script:

1. converts the Oireachtas data URI into a public member-profile URL where possible;
2. performs an HTTP GET;
3. parses the returned HTML with Beautiful Soup;
4. looks first for `img.c-member-about__img`;
5. tries several fallback image selectors if necessary;
6. converts the selected image `src` into an absolute URL;
7. stores the URL against `member_code`/`full_name`.

It is resumable by reusing nonblank `photo_url` values from the existing output CSV.

## Script defaults versus current workflow overrides

The retained script itself defaults to:

```text
OUTPUT_CSV_KEY=processed/members/members_photo_urls.csv
OUTPUT_PARQUET_KEY=processed/members/parquets/members_photo_urls.parquet
```

However, the current checked-in workflow `.github/workflows/member_photo_urls.yml` overrides those paths to:

```text
processed/members/member_photos/members_photo_urls.csv
processed/members/member_photos/parquets/members_photo_urls.parquet
```

That distinction matters because the newer enrichment code checks source candidates in this order:

1. `processed/members/member_photos/members_photo_urls.csv`;
2. `processed/members/members_photo_urls.csv`.

The previous archive record listed only the older root-level path and did not capture the current workflow override.

## Current manual workflow

Workflow: **Build Member Photo URLs (Manual)**.

Current behavior:

- manual `workflow_dispatch` only;
- Python 3.11;
- `test_rows` input, default `50`;
- 60-minute timeout;
- concurrency group `members-photo-urls`;
- AWS credentials from GitHub Actions secrets;
- input fixed to `raw/members/oireachtas_members_34th_dail.csv`;
- nested `processed/members/member_photos/...` output paths.

The workflow remains executable current source, but workflow presence does not by itself establish that it belongs to normal production operations.

## Resume, autosave, and mutation behavior

The scraper:

- loads the existing output CSV if present;
- reuses populated photo URLs by `member_code`;
- processes only missing URLs unless `TEST_ROWS` limits that work set;
- autosaves CSV and Parquet after the configured processed-row interval;
- writes final CSV and Parquet in place.

Current script defaults include:

```text
REQUEST_TIMEOUT=10
DELAY_BETWEEN_REQUESTS=0.2
AUTOSAVE_INTERVAL=50
TEST_ROWS=0
```

A page fetch/no-image failure leaves that member's `photo_url` blank and increments the failure counter; it does not abort the whole run by itself.

## Current Oireachtas enrichment relationship

`extract/oireachtas/enrichment_member_photo_urls.py` explicitly says:

- it does not scrape new pages;
- it does not overwrite existing legacy photo URL keys;
- it reshapes the current legacy photo URL CSV into a unified enrichment table plus a compatibility adapter.

### Enrichment trial outputs

```text
processed/oireachtas_unified/enrichment/media/member_photo_urls/member_photo_urls_trial.csv
processed/oireachtas_unified/enrichment/media/member_photo_urls/parquets/member_photo_urls_trial.parquet
```

The richer trial table adds fields including:

- `record_id`;
- `member_code`;
- `full_name`;
- `photo_url`;
- optional `source_url`;
- source key/system/hash;
- retrieval/review/run metadata.

### Compatibility outputs

```text
processed/oireachtas_unified/compat/media/members_photo_urls_compat.csv
processed/oireachtas_unified/compat/media/parquets/members_photo_urls_compat.parquet
```

The compatibility adapter contains:

```text
member_code
full_name
photo_url
```

`member_photo_urls` is one of the six current Unified Oireachtas downstream contracts. The Member Profile Metrics Builder reads this compatibility dataset by default, and current Instagram member-profile workflows consume the derived metrics/photo fields downstream.

## Current enrichment DQ

The enrichment trial checks:

- output row count greater than zero;
- unique generated `record_id`;
- populated `member_code` on every row;
- expected row count relative to the selected source/row limit.

Photo URL coverage is recorded but currently has informational severity: missing photo URLs do **not** by themselves cause the enrichment DQ status to fail.

The workflow writes manifests, schema/DQ files, review samples/reports, pushes review output to the `oireachtas-review-output` branch, and uploads workflow artifacts.

## Lineage interpretation

The checked-in relationship is currently:

```text
legacy member roster with profile URI
    ↓
legacy member-photo scraper
    ↓
processed/members/member_photos/members_photo_urls.csv
(or older root-level fallback)
    ↓
Unified Oireachtas member-photo enrichment trial
    ├─ richer enrichment/review output
    └─ members_photo_urls_compat.csv
         ↓
member-profile metrics
         ↓
Instagram deterministic/AI member-profile consumers
```

Therefore:

- the archive record represents the older scraping/discovery stage;
- the newer Oireachtas layer is an adapter/contract layer, not a replacement scraper;
- current downstream consumers have migrated toward the compatibility product;
- source-photo discovery still depends on a retained legacy producer or equivalent legacy output.

## Operational caution

Do not delete both legacy source candidates solely because `members_photo_urls_compat.csv` exists. Current enrichment code reads one of those legacy CSVs to build the compatibility product.

Do not assume the scraping selectors are stable. Oireachtas website HTML changes can cause individual photo discovery failures without a hard workflow failure.

The script performs direct public-page HTTP requests and should remain rate-conscious. The current delay is only a checked-in default, not a contractual rate limit.

## Security boundary

The workflow uses AWS credentials from GitHub Actions secrets. The scraper itself accesses public Oireachtas profile pages and does not require an OpenAI credential.

No secret values belong in documentation.

## Known limitations

- Photo discovery is tied to public webpage HTML structure rather than a declared media API contract.
- The current scraper input is the older raw members CSV, not the canonical Unified Oireachtas member table.
- Script defaults and workflow output paths differ.
- Missing `photo_url` rows are tolerated by the newer enrichment DQ as informational coverage gaps.
- Legacy output writes are direct/in-place and are not immutable candidate publication.
- The newer enrichment layer does not remove the need for an upstream photo-discovery source.
- File/workflow presence does not establish long-term production intent.

## Verification record

- Last verified: `2026-08-07`
- Legacy implementation verified against: `process/members_photo_urls.py`, `.github/workflows/member_photo_urls.yml`.
- Current successor-layer implementation verified against: `extract/oireachtas/enrichment_member_photo_urls.py`, `.github/workflows/oireachtas_member_photo_enrichment_trial.yml`.
- Current downstream relationship verified against the current member-photo compatibility contract and Member Profile Metrics Builder audit.
- Current classification: historical standalone scraping pipeline with retained executable source; newer Oireachtas enrichment/compatibility code depends on its legacy output. Full retirement is **not established**.
