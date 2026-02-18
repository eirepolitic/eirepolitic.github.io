---
layout: page
title: Member Photos Table
permalink: /projects/member-photos-table/
---

## Overview

### Purpose (What problem this pipeline solves.)
This pipeline builds and maintains a dataset of Oireachtas members and their publicly accessible profile photo URLs. It generates a clean, structured Parquet dataset in S3 that serves as the data source for the Athena table `member_photos_parquets`, enabling downstream tools (such as Power BI) to reliably access member photo URLs via Athena.

### Scope (What it covers / doesn’t cover.)

**Covers**
- Reading the official members dataset from S3.
- Converting member URIs into public Oireachtas profile URLs.
- Scraping each member’s profile page for their photo URL.
- Writing a resumable CSV and Parquet dataset to S3.
- Producing a Parquet dataset suitable for Athena querying.
- Manual execution via GitHub Actions.

---

## Architecture

### High-Level Flow (Steps from input → output.)

1. Load members CSV from S3.
2. Load existing output CSV (if present) to support resumability.
3. Identify members missing a photo URL.
4. Convert member URI → public Oireachtas profile page.
5. Scrape the profile page to extract the photo URL.
6. Write updated CSV and Parquet outputs to S3.
7. Glue crawler is manually run to refresh the Athena schema if needed.

### Components

1. **Python Scraper Module**
   - `members_photo_urls.py`
   - Handles S3 IO, scraping, resumability, and Parquet writing.

2. **GitHub Actions Workflow**
   - Manual execution environment.
   - Handles AWS authentication and runtime orchestration.

3. **AWS Glue Crawler (Manual)**
   - Updates Athena schema when structural changes occur.

4. **Athena External Table**
   - Queries the Parquet dataset in S3.

---

## Data Flow

### Inputs

- **Primary Input**
  - `s3://eirepolitic-data/raw/members/oireachtas_members_34th_dail.csv`
  - Required columns:
    - `member_code`
    - `full_name`
    - `uri`

### Processing Steps

1. Load input CSV from S3.
2. Load existing output CSV if present.
3. Build a lookup map of existing photo URLs.
4. Identify rows with missing `photo_url`.
5. For each missing row:
   - Convert the member URI to a public profile URL.
   - Request the HTML page.
   - Extract the photo image source using CSS selectors.
   - Convert relative paths to absolute URLs.
6. Autosave periodically during processing.
7. Write final CSV and Parquet outputs.

### Outputs

- **CSV Output**
  - `s3://eirepolitic-data/processed/members/member_photos/members_photo_urls.csv`

- **Parquet Output (Athena Source)**
  - `s3://eirepolitic-data/processed/members/member_photos/parquets/members_photo_urls.parquet`

---

## Implementation Details

### Technologies Used

- Python
- AWS S3
- AWS Glue (manual crawler)
- AWS Athena
- pandas
- boto3
- requests
- BeautifulSoup
- pyarrow (Parquet)

### Execution Method

- Manual (GitHub Actions workflow dispatch)

### Configuration

#### Environment Variables

- AWS credentials
- `S3_BUCKET`
- `INPUT_KEY`
- `OUTPUT_CSV_KEY`
- `OUTPUT_PARQUET_KEY`
- `REQUEST_TIMEOUT`
- `DELAY_BETWEEN_REQUESTS`
- `AUTOSAVE_INTERVAL`
- `TEST_ROWS`

#### Runtime Parameters

- `test_rows` (workflow input)
  - Limits number of rows processed for testing.

---

## Dependencies

### Internal

- Python module: `process/members_photo_urls.py`
- GitHub Actions workflow configuration
- Repository `requirements.txt`

### External

- Oireachtas public member profile website
- AWS S3
- AWS Glue
- AWS Athena

---

## Operational Details

### Runtime Characteristics

- **Frequency:** Manual only
- **Typical Runtime:** Varies based on number of missing rows and network latency.

### Failure Handling

- Per-row scraping failures are logged and skipped.
- Failed rows remain with missing `photo_url` values.
- Autosave mechanism prevents loss of progress.
- Final outputs are always written regardless of errors.

### Monitoring

- GitHub Actions logs provide:
  - Progress indicators
  - Failure counts
  - Autosave checkpoints
- No automated alerts configured.

---

## Maintenance

### Known Limitations

- Dependent on the HTML structure of the Oireachtas website.
- Photo URLs are not refreshed once populated.
- Glue crawler must be run manually after schema changes.
- Scraping failures may occur due to temporary website issues.

### Future Improvements

- Add automated crawler trigger after pipeline completion.
- Implement retry logic for transient HTTP failures.
- Add monitoring alerts for scraping failures.
- Optionally allow periodic revalidation of photo URLs.

---

## Related Resources

### Code Location

- Python module:
  - `process/members_photo_urls.py`

- GitHub Actions workflow:
  - “Build Member Photo URLs (Manual)”

### Athena Table Definition

```sql
CREATE EXTERNAL TABLE `member_photos_parquets`(
  `member_code` string, 
  `full_name` string, 
  `photo_url` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://eirepolitic-data/processed/members/member_photos/parquets/';
