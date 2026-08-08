---
title: Constituency Images Indexer
summary: Historical constituency-image indexing implementation retained as the source producer for the newer Oireachtas constituency-image enrichment/compatibility trial.
section: archive
doc_type: pipeline
status: archived
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - Amazon S3
  - AWS Glue
  - Amazon Athena
  - GitHub Actions
created: 2026-02-27
updated: 2026-08-07
last_verified: 2026-08-07
archived_date: 2026-08-05
archive_reason: Historical standalone pipeline record retained for lineage; current Oireachtas enrichment code consumes its legacy output rather than replacing the indexing function.
permalink: /projects/pipelines/constituency_images_indexer/
related:
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/notes/oireachtas-write-policies-downstream-contracts/
---

# Constituency Images Indexer

## Current status

This page is an **archive/lineage record**, not the source of truth for the current Unified Oireachtas enrichment layer.

The original implementation is still present on `eirepolitic-data-pipeline/main`:

- `process/constituency_images_indexer.py`
- `.github/workflows/constituency_images_index.yml`

GitHub also retains one observed successful manual run of the legacy workflow: run `21652253875` on 2026-02-03.

However, file/workflow presence and a historical successful run do not establish that this standalone indexer is still part of normal production operations.

The important current lineage fact is that the newer Oireachtas constituency-image enrichment trial **depends on the legacy index output**. It does not independently discover or create constituency image files.

## Historical implementation

The indexer lists image objects under:

```text
s3://eirepolitic-data/processed/constituencies/images/
```

and writes an index containing:

- `filename`
- `s3_key`
- `url`

Historical/default outputs:

```text
processed/constituencies/constituency_images.csv
processed/constituencies/parquets/constituency_images.parquet
```

Supported image extensions in current retained source are:

```text
.jpg .jpeg .png .webp .gif .bmp .tif .tiff .svg
```

The retained code paginates S3 `list_objects_v2`, filters by extension, derives a URL from bucket/region/key, sorts by filename, and overwrites the CSV and Parquet index objects.

Default configuration remains:

```text
AWS_REGION=ca-central-1
S3_BUCKET=eirepolitic-data
SOURCE_PREFIX=processed/constituencies/images/
OUTPUT_CSV_KEY=processed/constituencies/constituency_images.csv
OUTPUT_PARQUET_KEY=processed/constituencies/parquets/constituency_images.parquet
```

## Historical workflow

`.github/workflows/constituency_images_index.yml` remains a manually dispatchable workflow in current source.

Its existence should be read as **retained executable implementation**, not proof of current production intent. The current scheduled Oireachtas orchestrator does not establish this legacy workflow as part of its normal canonical refresh sequence.

## Current successor relationship

Current successor-layer code:

```text
extract/oireachtas/enrichment_constituency_images.py
.github/workflows/oireachtas_constituency_image_enrichment_trial.yml
```

The module explicitly describes itself as a side-by-side enrichment trial and states that it does **not** create, download, or overwrite image files.

Its source is hard-coded to the legacy index:

```text
processed/constituencies/constituency_images.csv
```

It reshapes that legacy source into a richer trial table plus a compatibility adapter.

### Trial outputs

```text
processed/oireachtas_unified/enrichment/media/constituency_images/constituency_images_trial.csv
processed/oireachtas_unified/enrichment/media/constituency_images/parquets/constituency_images_trial.parquet
```

The trial table adds fields including:

- deterministic `record_id`;
- inferred/declared `constituency`;
- `filename`;
- `image_key`;
- `image_url`;
- `media_type`;
- source/run metadata;
- `review_status`.

### Compatibility outputs

```text
processed/oireachtas_unified/compat/media/constituency_images_compat.csv
processed/oireachtas_unified/compat/media/parquets/constituency_images_compat.parquet
```

The compatibility adapter deliberately restores the three legacy-shaped fields:

```text
filename
s3_key
url
```

That compatibility CSV is one of the six current downstream contracts documented for the Unified Oireachtas platform.

## Current enrichment validation

The newer enrichment code performs checks including:

- nonzero row count;
- unique deterministic `record_id`;
- populated constituency;
- at least one image locator (`image_key` or `image_url`) on every row;
- expected row count relative to the legacy source/optional row limit.

It also writes run manifests, review samples, schema/DQ JSON, Markdown review reports, and local review bundles.

The trial workflow can publish those review artifacts to the `oireachtas-review-output` Git branch and explicitly states that it does not overwrite legacy image index keys or image files.

## Lineage interpretation

The relationship is currently:

```text
S3 image objects
    ↓
legacy Constituency Images Indexer
    ↓
processed/constituencies/constituency_images.csv
    ↓
Oireachtas constituency-image enrichment trial
    ├─ richer enrichment/review outputs
    └─ Unified Oireachtas compatibility adapter
```

Therefore:

- the **standalone documentation** for the indexer is historical/archive material;
- the **legacy CSV remains an active dependency of the checked-in enrichment trial**;
- the newer enrichment code is a consumer/adapter layer, not a complete replacement for image discovery/index creation;
- current source does not justify claiming the legacy indexer has been fully retired.

## Operational caution

Do not delete or relocate the legacy CSV solely because a Unified Oireachtas compatibility product now exists. Current enrichment code still reads that legacy key directly.

Likewise, do not assume public accessibility merely because the historical indexer constructs S3-style HTTPS URLs. Actual object/bucket public-access policy is an AWS account-level property and has not been verified by this documentation audit.

## Historical validation guidance

The old page recommended checking both output objects and using Athena/Glue metadata. That remains historical operating context for the standalone indexer, but current Oireachtas enrichment correctness should instead be assessed through its trial DQ/review outputs and downstream compatibility contract.

## Known limitations

- The retained legacy indexer overwrites its CSV and Parquet outputs directly rather than using Oireachtas immutable candidate publication.
- URL construction does not prove an object is publicly readable.
- The index contains no canonical constituency ID; the newer enrichment layer may infer constituency names from filenames when the source lacks them.
- The current enrichment trial is still dependent on the legacy index key, so successor migration is incomplete at the source-discovery layer.
- Neither retained workflow presence nor workflow-registry active state proves normal production intent.

## Verification record

- Last verified: `2026-08-07`
- Legacy implementation verified against: `process/constituency_images_indexer.py`, `.github/workflows/constituency_images_index.yml`.
- Current successor-layer implementation verified against: `extract/oireachtas/enrichment_constituency_images.py`, `.github/workflows/oireachtas_constituency_image_enrichment_trial.yml`.
- Observed legacy runtime evidence: workflow run `21652253875`, success, 2026-02-03.
- Current classification: historical standalone pipeline record with retained executable source; its output remains an explicit dependency of the newer Oireachtas enrichment/compatibility trial. Full retirement is **not established**.
