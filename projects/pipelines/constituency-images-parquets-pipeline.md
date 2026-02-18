---
layout: page
title: Constituency Images Parquets Pipeline Documentation
permalink: /projects/pipelines/constituency-images-parquets-pipeline/
---

# constituency_images_parquets Pipeline

## Overview
### Purpose
Create and maintain the Athena external table `constituency_images_parquets` from a generated index of constituency image objects stored in S3.

---

## Architecture
### High-Level Flow
1. Constituency image files are produced manually (Inkscape: recolour SVG elements per constituency) and uploaded to S3.
2. `constituency_images_indexer.py` lists image objects under the configured S3 prefix and builds an index dataset with public URLs.
3. The index dataset is written to S3 as CSV and Parquet.
4. An AWS Glue crawler (`constituency_images`) maintains the Athena external table `constituency_images_parquets` over the Parquet LOCATION.

### Components
1. Manual image production (Inkscape) + S3 upload
2. Indexer job: `process/constituency_images_indexer.py`
3. Orchestration: GitHub Actions workflow `Build Constituency Image Index (Manual)`
4. Storage (S3):
   - CSV: `processed/constituencies/constituency_images.csv`
   - Parquet: `processed/constituencies/parquets/constituency_images.parquet`
5. Glue Crawler: `constituency_images`
6. Athena Table: `constituency_images_parquets`

---

## Data Flow
### Inputs
- S3 image object prefix (default):
  - `s3://eirepolitic-data/processed/constituencies/images/`
- Images are filtered to common extensions:
  - `.jpg`, `.jpeg`, `.png`, `.webp`, `.gif`, `.bmp`, `.tif`, `.tiff`, `.svg`

### Processing Steps
- List objects in S3 using `list_objects_v2` with pagination (`ContinuationToken`) under `SOURCE_PREFIX`.
- Filter keys by extension using `is_image_key()`.
- For each image key `k`:
  - `filename = last path segment of k`
  - `s3_key = k`
  - `url = https://{bucket}.s3.{region}.amazonaws.com/{url_encoded_key}`
    - Uses URL encoding via `urllib.parse.quote` to safely encode spaces and special characters.
- Build a dataframe of rows and sort by `filename` using a stable sort.
- Write outputs:
  - CSV to S3 with UTF-8 BOM (`utf-8-sig`) and content-type `text/csv`
  - Parquet to S3 using PyArrow with Snappy compression and content-type `application/x-parquet`

### Outputs
- CSV:
  - `s3://eirepolitic-data/processed/constituencies/constituency_images.csv`
- Parquet:
  - `s3://eirepolitic-data/processed/constituencies/parquets/constituency_images.parquet`
- Athena Table:
  - `constituency_images_parquets`

---

## Implementation Details
### Technologies Used
- Python 3.11
- GitHub Actions (manual workflow dispatch)
- AWS S3 (image storage + index storage)
- boto3 (S3 listing + writes)
- pandas (tabular build + sorting)
- pyarrow (Parquet writing; snappy compression)
- AWS Glue crawler (`constituency_images`)
- AWS Athena (external table over Parquet)

### Execution Method
- Manual trigger via GitHub Actions `workflow_dispatch`
- Job timeout: `timeout-minutes: 60`
- Concurrency:
  - `group: constituency-images-index`
  - `cancel-in-progress: false`

### Configuration
#### Script environment variables (defaults)
- `AWS_REGION` (default: `ca-central-1`)
- `S3_BUCKET` (default: `eirepolitic-data`)
- `SOURCE_PREFIX` (default: `processed/constituencies/images/`)
- `OUTPUT_CSV_KEY` (default: `processed/constituencies/constituency_images.csv`)
- `OUTPUT_PARQUET_KEY` (default: `processed/constituencies/parquets/constituency_images.parquet`)

#### GitHub Actions environment variables
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` (from secrets)
- `S3_BUCKET` = `eirepolitic-data`
- `SOURCE_PREFIX` = `processed/constituencies/images/`
- `OUTPUT_CSV_KEY` = `processed/constituencies/constituency_images.csv`
- `OUTPUT_PARQUET_KEY` = `processed/constituencies/parquets/constituency_images.parquet`

---

## Dependencies
### Internal
- Script:
  - `process/constituency_images_indexer.py`
- Workflow:
  - `Build Constituency Image Index (Manual)`

### External
- AWS S3 (ListObjectsV2 + PutObject permissions for relevant prefixes)
- Public access policy/config for `processed/constituencies/images/` (required for generated URLs to be usable)
- AWS Glue + Athena

---

## Operational Details
### Runtime Characteristics
- Trigger: manual via GitHub Actions
- Runtime driver: number of objects under `SOURCE_PREFIX`
- Expected runtime: seconds to a few minutes (single S3 list + single CSV + single Parquet write)

### Failure Handling
- If S3 listing fails (permissions/region/credentials): job fails with exception.
- If output writes fail: job fails; re-run after fixing credentials/permissions.
- Idempotency:
  - Outputs are overwritten on each run (same object keys), producing a current index.

### Monitoring
- GitHub Actions run logs (object count + output paths printed).
- Verify S3 objects exist:
  - `processed/constituencies/constituency_images.csv`
  - `processed/constituencies/parquets/constituency_images.parquet`
- Athena validation query after crawler/table update:
  - `SELECT COUNT(*) FROM constituency_images_parquets;`

---

## Maintenance
### Known Limitations
- URLs are constructed as virtual-hosted S3 URLs:
  - `https://{bucket}.s3.{region}.amazonaws.com/{key}`
  - If you switch to CloudFront/custom domains, URL construction must be updated.
- Table LOCATION points to the folder:
  - `s3://eirepolitic-data/processed/constituencies/parquets/`
  - Parquet writes currently produce a single file (`constituency_images.parquet`) but the crawler/table treat the folder as the dataset root.
- The crawler is the source of schema truth for Athena; if schema changes are introduced, the crawler must be re-run.

### Future Improvements
- Add derived fields if needed (e.g., `constituency`, `side`) based on filename parsing.
- Add a guard to skip keys that represent folders (already implicitly handled by extension filter).
- Add scheduled runs if new images are frequently added.

---

## Related Resources
### Code Location
- Script:
  - `process/constituency_images_indexer.py`
- Workflow:
  - GitHub Actions: `Build Constituency Image Index (Manual)`

### Athena Table DDL (current)
- Table: `constituency_images_parquets`
- Columns:
  - `filename` string
  - `s3_key` string
  - `url` string
- LOCATION:
  - `s3://eirepolitic-data/processed/constituencies/parquets/`
- Crawler:
  - `UPDATED_BY_CRAWLER = constituency_images`
