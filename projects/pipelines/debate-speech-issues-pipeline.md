---
layout: page
title: Debate Speech Issues Pipeline Documentation
permalink: /projects/pipelines/debate-speech-issues-pipeline/
---

# Debate Speech Issues Pipeline

> This document describes the full end-to-end pipeline that produces the **debate_speech_issues** analytics table in AWS Athena, from raw data extraction at source through LLM processing and warehouse ingestion.

---

## Overview

### Purpose

The Debate Speech Issues pipeline automatically collects Irish parliamentary debate data from the official Oireachtas API, transforms it into structured speech records, applies Large Language Model (LLM) classification to identify the primary political issue discussed in each speech, and produces analytics-ready datasets accessible through AWS Athena for querying and visualization.

The pipeline solves several key problems:

• Manual extraction and cleaning of parliamentary debate data  
• Lack of structured categorization of political speech topics  
• Difficulty analyzing debates at scale  
• Need for automated, repeatable monthly processing  

The final output enables political analysis, dashboards, and research into trends in Irish parliamentary discourse.

---

### Scope

This pipeline covers:

• Extraction of Dáil Éireann debate XML files from the Oireachtas API  
• Transformation of XML into structured speech datasets  
• LLM-based classification of speeches into a single political issue category  
• Storage of processed datasets in AWS S3 (CSV + Parquet)  
• Creation of Athena queryable analytics tables  

This pipeline does NOT cover:

• Sentiment analysis  
• Multi-label issue classification  
• TD stance or voting behavior analysis  
• Data from non-Dáil parliamentary chambers  

---

## Architecture

### High-Level Flow

Oireachtas API → Raw XML Storage → Speech Extraction → LLM Classification → Processed Data Lake → Athena Analytics Table

Detailed Flow:

1. Oireachtas API provides debate XML files  
2. XML files are stored in S3 raw zone  
3. XML is parsed into structured speech records  
4. LLM assigns a single political issue label per speech  
5. Processed datasets stored as CSV and Parquet in S3  
6. AWS Glue crawler updates schema  
7. Athena table exposes queryable dataset  

---

### Components

1. Debate XML Extractor — Python module executed via GitHub Actions  
2. Speech Extraction Transformer — Parses XML into structured tabular format  
3. LLM Issue Classification Module — Uses GPT-5 models to classify speeches  
4. Data Storage Layers — AWS S3 raw and processed zones  
5. AWS Glue Crawler — Infers schema from Parquet output  
6. Athena Analytics Table — Final queryable dataset: debate_speech_issues  

---

## Data Flow

### Inputs

Primary Input:

• Oireachtas Debates API (Akoma Ntoso XML format)

Secondary Input:

• Existing processed classification files for resumable processing

---

### Processing Steps

#### 1. Debate Extraction

A scheduled GitHub Actions workflow:

• Calls the Oireachtas API  
• Downloads all available Dáil 34 debate XML files  
• Uploads them to the S3 raw zone  

Storage location:

s3://eirepolitic-data/raw/debates/xml/

Files are named:

YYYY-MM-DD__<debate_id>.xml

---

#### 2. Speech Parsing

XML files are parsed into structured records containing:

• Speaker name  
• Speech text  
• Debate date  
• Section heading  
• Debate metadata  

Output stored as:

s3://eirepolitic-data/raw/debates/debate_speeches_extracted.csv

This dataset serves as the primary input to the classification stage.

---

#### 3. LLM Issue Classification

Each speech text is processed using an OpenAI GPT-5 model to assign a single political issue label.

Key characteristics:

• Resumable row-level processing  
• Automatic retry logic  
• Idempotent processing  
• Configurable via YAML  

The classification process reads existing output files and only processes speeches missing an issue label.

---

#### 4. Processed Data Storage

Results are written to the processed data lake.

CSV output:

s3://eirepolitic-data/processed/debates/debate_speeches_classified.csv

Parquet output:

s3://eirepolitic-data/processed/debates/parquets/debate_speeches_classified.parquet

Parquet format is used for efficient analytics querying.

---

#### 5. Athena Table Creation

AWS Glue crawler scans the Parquet dataset to infer schema.

Crawler is run manually when schema changes occur.

The resulting Athena table:

debate_speech_issues

This table serves as the primary analytics interface for querying debate issue data.

---

### Outputs

Primary Output:

• Athena table: debate_speech_issues

Supporting Outputs:

• Classified speeches CSV in S3  
• Parquet dataset optimized for analytics  

---

## Implementation Details

### Technologies Used

• Python 3.11  
• GitHub Actions (serverless orchestration)  
• AWS S3 (data lake storage)  
• AWS Glue (schema inference)  
• AWS Athena (analytics querying)  
• OpenAI GPT-5 models (LLM classification)  
• Pandas + PyArrow (data processing)  

---

### Execution Method

Hybrid:

• Scheduled monthly execution via GitHub Actions cron  
• Manual execution supported through workflow dispatch  

---

### Configuration

Environment Variables:

• AWS_ACCESS_KEY_ID  
• AWS_SECRET_ACCESS_KEY  
• AWS_REGION  
• S3_BUCKET  
• OPENAI_API_KEY  

Pipeline Parameters:

• Input/output S3 paths  
• LLM model configuration  
• Test row limits  
• Retry settings  

---

## Dependencies

### Internal

• Debate XML extraction module  
• Speech parsing module  
• Generic LLM table runner framework  

---

### External

• Oireachtas Public API  
• AWS S3, Glue, Athena  
• OpenAI API  

---

## Operational Details

### Runtime Characteristics

Frequency:

• Monthly automated execution

Typical Runtime:

Extraction: ~5–10 minutes  
Speech parsing: ~10–20 minutes  
LLM classification: 1–3 hours depending on dataset size  

---

### Failure Handling

• Row-level resumable processing  
• Automatic retry of failed LLM calls  
• Existing outputs preserved and incrementally updated  

---

### Monitoring

Pipeline health is monitored via:

• GitHub Actions workflow logs  
• Email notifications on workflow completion  
• Manual verification of S3 outputs  
• Athena query validation  

---

## Maintenance

### Known Limitations

• Entire dataset reprocessed each run rather than incremental debate ingestion  
• Single-label issue classification limits granularity  
• Processing time increases linearly with dataset growth  

---

### Future Improvements

• Incremental debate ingestion  
• Parallelized LLM processing  
• Multi-label issue classification  
• Automated Glue crawler execution  
• Data partitioning for Athena performance  

---

## Related Resources

### Code Location

GitHub Repository:

eirepolitic-data-pipeline

Key Modules:

• Debate XML extractor  
• Speech extraction transformer  
• Speech issue classifier  
• Generic LLM table runner  

---

### Documentation Links

• Oireachtas API Documentation  
• AWS Athena Documentation  
• OpenAI API Documentation  
