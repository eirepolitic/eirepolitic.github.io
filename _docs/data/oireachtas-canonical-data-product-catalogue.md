---
title: Oireachtas Canonical Data-Product Catalogue
summary: Registry-level catalogue of the 31 confirmed canonical silver, gold, and control products produced by the Unified Oireachtas Data Platform.
section: data
doc_type: reference
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: eirepolitic-data-pipeline
system: Unified Oireachtas Data Platform
order: 30
permalink: /projects/data/oireachtas-canonical-data-product-catalogue/
tags:
  - oireachtas
  - csv
  - parquet
  - canonical-data
related:
  - /projects/systems/unified-oireachtas-data-platform/
  - /projects/repositories/eirepolitic-data-pipeline/
  - /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
---

# Oireachtas Canonical Data-Product Catalogue

## Summary

This is the canonical documentation catalogue for the Unified Oireachtas Data Platform's checked-in table registry. The authoritative registry is `eirepolitic-data-pipeline/configs/oireachtas/tables.yml`.

As verified on 2026-08-07, it defines **31 products**, all with registry status `confirmed`:

- 23 silver products;
- 5 gold products;
- 3 control products.

The registry comment defines `confirmed` as a table builder having completed at least one manual validation run with DQ pass. That status is a checked-in implementation assertion; it is not a guarantee that the latest production object is currently healthy.

This page records exact registry names, grain-defining primary keys, cadences, configured source endpoints, columns, builder paths and configured write strategies. It does not invent data types because `tables.yml` declares column names but not a typed schema.

## Current Implementation State

**Verified configuration:** every product below exists in `configs/oireachtas/tables.yml` with status `confirmed`.

**Verified implementation:** `extract/oireachtas/build_table.py` dispatches registered products to table-specific `extract/oireachtas/table_*.py` builders. Current logical products are published as CSV and, for non-empty tables where supported by the builder, Parquet under `processed/oireachtas_unified/latest/`, with immutable candidate mapping handled by the batch-aware S3 layer.

**Important schema limitation:** registry columns are authoritative names/order, but no data types, nullable flags, or field descriptions are encoded per column. Those characteristics must be established from builder code and observed output before being documented as formal typed contracts.

## Source of Truth

| Concern | Authoritative source |
| --- | --- |
| Product names, layers, registry status, cadence, source endpoint, PK, description, columns | `configs/oireachtas/tables.yml` |
| Write strategy and selected relationship metadata | `configs/oireachtas/write_policies.yml` |
| Registry loader | `extract/oireachtas/schemas.py` |
| Product dispatch | `extract/oireachtas/build_table.py` |
| Product transformations and DQ | corresponding `extract/oireachtas/table_*.py` builder |
| Candidate/latest S3 semantics | `extract/oireachtas/io_s3.py`, `extract/oireachtas/batch.py` |
| Refresh selection | `process/oireachtas_refresh_inputs.py` |

If this page conflicts with current checked-in configuration or builder implementation, the current code/configuration wins and this page must be updated.

## Ownership and Lifecycle

The products are produced and governed by the Unified Oireachtas Data Platform in `eirepolitic-data-pipeline`.

Registry cadences are descriptive product cadences. Production refresh selection is additionally controlled by `process/oireachtas_refresh_inputs.py`; therefore a product can appear in more than one refresh set or have a registry cadence such as `weekly_current_year`, `follows_parent`, or `every_run` that is not itself a cron expression.

Canonical products are versioned operationally through immutable run outputs and immutable candidate batches. Production state is selected by the Oireachtas production pointer. Schema changes require coordinated registry, builder, validation and downstream compatibility review.

## Storage Forms

Typical canonical logical outputs are:

```text
processed/oireachtas_unified/latest/csv/<table>.csv
processed/oireachtas_unified/latest/parquet/<table>.parquet
```

Run-specific outputs use table/layer-specific paths under `processed/oireachtas_unified/`; representative patterns are documented on the Unified Oireachtas Data Platform page. Candidate publication maps the logical key into `processed/oireachtas_unified/batches/<batch_id>/...`.

## Silver Products

### Core dimensions and member identity

| Product | Cadence | Endpoint | Primary key | Write strategy | Builder | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `silver_houses` | yearly | `/houses` | `house_uri` | `snapshot_replace` | `extract/oireachtas/table_houses.py` | House/chamber dimension. |
| `silver_constituencies` | monthly | `/constituencies` | `constituency_uri` | `snapshot_replace` | `extract/oireachtas/table_constituencies.py` | Constituency dimension. |
| `silver_parties` | monthly | `/parties` | `party_uri` | `snapshot_replace` | `extract/oireachtas/table_parties.py` | Political party dimension. |
| `silver_members` | weekly | `/members` | `member_code` | `snapshot_replace` | `extract/oireachtas/table_members.py` | Stable member/person identity table. |

#### `silver_houses`

Columns, in registry order:

`house_uri`, `house_no`, `house_code`, `chamber`, `show_as`, `date_start`, `date_end`, `is_current`, `source_endpoint`, `snapshot_date`, `source_hash`.

#### `silver_constituencies`

`constituency_uri`, `constituency_code`, `constituency_name`, `show_as`, `house_uri`, `house_no`, `chamber`, `date_start`, `date_end`, `is_current`, `source_endpoint`, `snapshot_date`, `source_hash`.

#### `silver_parties`

`party_uri`, `party_code`, `party_name`, `show_as`, `date_start`, `date_end`, `is_current`, `source_endpoint`, `snapshot_date`, `source_hash`.

#### `silver_members`

`member_code`, `member_uri`, `full_name`, `first_name`, `last_name`, `display_name`, `gender`, `member_key`, `is_current_member`, `latest_party_name`, `latest_constituency_name`, `latest_house_no`, `source_endpoint`, `snapshot_date`, `source_hash`.

Verified builder behavior for `silver_members`: `/members` data is normalized from several observed wrapper shapes, missing member codes can fall back to a deterministic hash, current/latest membership context supplies the convenience party/constituency/house columns, and DQ requires a non-empty table, required columns, populated/unique PK and at least one populated `full_name`.

### Time-aware member relationships

| Product | Cadence | Endpoint | Primary key | Write strategy | Builder | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `silver_member_memberships` | weekly | `/members` | `membership_id` | `upsert` | `extract/oireachtas/table_member_memberships.py` | Time-aware member-to-house bridge. |
| `silver_member_parties` | weekly | `/members` | `member_party_id` | `upsert` | `extract/oireachtas/table_member_parties.py` | Time-aware member-to-party bridge. |
| `silver_member_constituencies` | weekly | `/members` | `member_constituency_id` | `upsert` | `extract/oireachtas/table_member_constituencies.py` | Time-aware member-to-constituency bridge. |
| `silver_member_offices` | weekly | `/members` | `member_office_id` | `upsert` | `extract/oireachtas/table_member_offices.py` | Member office/ministerial/chair role bridge where exposed. |

#### `silver_member_memberships`

`membership_id`, `member_code`, `member_uri`, `house_uri`, `house_no`, `house_code`, `chamber`, `membership_start`, `membership_end`, `is_current`, `source_hash`, `snapshot_date`.

Configured relationship metadata:

- validity: `membership_start` → `membership_end`, current flag `is_current`;
- FK `member_code` → `silver_members.member_code`;
- FK `house_uri` → `silver_houses.house_uri`.

#### `silver_member_parties`

`member_party_id`, `membership_id`, `member_code`, `party_uri`, `party_name`, `party_start`, `party_end`, `is_current`, `snapshot_date`.

Configured relationship metadata:

- validity: `party_start` → `party_end`, current flag `is_current`;
- business key: `member_code`, `party_uri`, `party_start`, `party_end`;
- FK `member_code` → `silver_members.member_code`;
- FK `membership_id` → `silver_member_memberships.membership_id`.

#### `silver_member_constituencies`

`member_constituency_id`, `membership_id`, `member_code`, `constituency_uri`, `constituency_name`, `represent_start`, `represent_end`, `is_current`, `snapshot_date`.

Configured relationship metadata:

- validity: `represent_start` → `represent_end`, current flag `is_current`;
- business key: `member_code`, `constituency_uri`, `represent_start`, `represent_end`;
- FK `member_code` → `silver_members.member_code`;
- FK `membership_id` → `silver_member_memberships.membership_id`.

#### `silver_member_offices`

`member_office_id`, `membership_id`, `member_code`, `office_uri`, `office_name`, `office_start`, `office_end`, `is_current`, `snapshot_date`.

Configured relationship metadata:

- validity: `office_start` → `office_end`, current flag `is_current`;
- FK `member_code` → `silver_members.member_code`;
- FK `membership_id` → `silver_member_memberships.membership_id`.

### Source files and debates

| Product | Cadence | Endpoint | Primary key | Write strategy | Builder | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `silver_source_files` | follows_parent | none in registry | `source_file_id` | `upsert` | `extract/oireachtas/table_source_files.py` | Inventory of XML/PDF/source files discovered from format fields. |
| `silver_debate_records` | weekly | `/debates` | `debate_id` | `upsert` | `extract/oireachtas/table_debate_records.py` | Debate metadata records. |
| `silver_debate_sections` | weekly | none in registry | `debate_section_id` | `upsert` | `extract/oireachtas/table_debate_sections.py` | Debate section records parsed from API/XML. |
| `silver_speeches` | weekly | none in registry | `speech_id` | `upsert` | `extract/oireachtas/table_speeches.py` | Atomic speech records parsed from debate XML. |

#### `silver_source_files`

`source_file_id`, `source_entity_type`, `source_entity_id`, `format_type`, `format_uri`, `format_url`, `s3_key`, `content_type`, `download_status`, `downloaded_at_utc`, `byte_size`, `etag_or_hash`, `snapshot_date`.

#### `silver_debate_records`

`debate_id`, `debate_uri`, `context_date`, `debate_date`, `chamber`, `house_uri`, `house_no`, `house_code`, `show_as`, `source_xml_uri`, `source_xml_url`, `source_pdf_uri`, `source_pdf_url`, `source_file_id_xml`, `source_file_id_pdf`, `api_result_hash`, `snapshot_date`.

#### `silver_debate_sections`

`debate_section_id`, `debate_id`, `section_eid`, `section_uri`, `section_order`, `heading`, `show_as`, `parent_section_id`, `snapshot_date`.

Configured FK: `debate_id` → `silver_debate_records.debate_id`.

#### `silver_speeches`

`speech_id`, `debate_id`, `debate_section_id`, `debate_date`, `speech_order`, `speaker_ref`, `speaker_name`, `speaker_member_code`, `speaker_match_method`, `speaker_match_confidence`, `speech_text`, `speech_text_hash`, `word_count`, `char_count`, `language`, `source_file_id`, `xml_source_key`, `snapshot_date`.

Configured relationships:

- `debate_id` → `silver_debate_records.debate_id`;
- nullable `debate_section_id` → `silver_debate_sections.debate_section_id`;
- nullable `speaker_member_code` → `silver_members.member_code`.

### Divisions and member votes

| Product | Cadence | Endpoint | Primary key | Write strategy | Builder | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `silver_divisions` | weekly | `/divisions` | `division_id` | `upsert` | `extract/oireachtas/table_divisions.py` | Division/vote event table. |
| `silver_division_tallies` | weekly | `/divisions` | `division_tally_id` | `upsert` | `extract/oireachtas/table_division_tallies.py` | Division-level tally counts by vote type. |
| `silver_member_votes` | weekly | `/divisions` | `member_vote_id` | `upsert` | `extract/oireachtas/table_member_votes.py` | Member-level vote records. |

#### `silver_divisions`

`division_id`, `vote_id`, `division_date`, `chamber`, `house_uri`, `house_no`, `committee_code`, `subject`, `outcome`, `debate_id`, `debate_section_id`, `debate_show_as`, `api_result_hash`, `snapshot_date`.

Configured nullable FK: `debate_id` → `silver_debate_records.debate_id`.

#### `silver_division_tallies`

`division_tally_id`, `division_id`, `vote_code`, `vote_label`, `show_as`, `member_count`, `snapshot_date`.

Configured FK: `division_id` → `silver_divisions.division_id`.

#### `silver_member_votes`

`member_vote_id`, `division_id`, `vote_id`, `division_date`, `member_code`, `member_name`, `vote_code`, `vote_label`, `party_name_at_vote`, `constituency_name_at_vote`, `snapshot_date`.

Configured relationships:

- `division_id` → `silver_divisions.division_id`;
- `member_code` → `silver_members.member_code`.

### Parliamentary questions

| Product | Cadence | Endpoint | Primary key | Write strategy | Builder | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `silver_questions` | weekly | `/questions` | `question_id` | `upsert` | `extract/oireachtas/table_questions.py` | Parliamentary questions. |

Columns:

`question_id`, `question_uri`, `question_date`, `question_no`, `question_type`, `question_text`, `answer_text`, `asked_by_member_code`, `asked_by_name`, `to_minister_or_department`, `debate_section_id`, `source_xml_uri`, `source_xml_url`, `source_pdf_uri`, `source_pdf_url`, `source_file_id_xml`, `source_file_id_pdf`, `snapshot_date`, `source_hash`.

Configured nullable FK: `asked_by_member_code` → `silver_members.member_code`.

### Legislation

| Product | Cadence | Endpoint | Primary key | Write strategy | Builder | Description |
| --- | --- | --- | --- | --- | --- | --- |
| `silver_bills` | monthly | `/legislation` | `bill_id` | `upsert` | `extract/oireachtas/table_bills.py` | Bill/legislation item table. |
| `silver_bill_versions` | monthly | `/legislation` | `bill_version_id` | `upsert` | `extract/oireachtas/table_bill_versions.py` | Bill version/document table. |
| `silver_bill_stages` | monthly | `/legislation` | `bill_stage_id` | `upsert` | `extract/oireachtas/table_bill_stages.py` | Bill stage/progress history. |
| `silver_bill_related_docs` | monthly | `/legislation` | `related_doc_id` | `upsert` | `extract/oireachtas/table_bill_related_docs.py` | Bill related/source documents such as explanatory memoranda. |
| `silver_bill_sponsors` | monthly | `/legislation` | `bill_sponsor_id` | `upsert` | `extract/oireachtas/table_bill_sponsors.py` | Bill sponsor bridge from legislation sponsor payloads. |
| `silver_bill_debates` | monthly | `/legislation` | `bill_debate_id` | `upsert` | `extract/oireachtas/table_bill_debates.py` | Bill-to-debate bridge from legislation debate references. |
| `silver_bill_events` | monthly | `/legislation` | `bill_event_id` | `upsert` | `extract/oireachtas/table_bill_events.py` | Bill event bridge from legislation event payloads. |

#### `silver_bills`

`bill_id`, `bill_uri`, `bill_no`, `bill_year`, `title`, `short_title`, `origin_house_uri`, `origin_house_name`, `bill_type`, `status`, `introduced_date`, `last_event_date`, `source_endpoint`, `snapshot_date`, `source_hash`.

#### `silver_bill_versions`

`bill_version_id`, `bill_id`, `version_label`, `version_date`, `format_pdf_uri`, `format_pdf_url`, `format_xml_uri`, `format_xml_url`, `source_file_id_pdf`, `source_file_id_xml`, `s3_pdf_key`, `s3_xml_key`, `snapshot_date`.

Configured FK: `bill_id` → `silver_bills.bill_id`.

#### `silver_bill_stages`

`bill_stage_id`, `bill_id`, `stage_name`, `stage_date`, `house_uri`, `house_name`, `stage_outcome`, `order_in_bill`, `snapshot_date`.

Configured FK: `bill_id` → `silver_bills.bill_id`.

#### `silver_bill_related_docs`

`related_doc_id`, `bill_id`, `related_doc_label`, `related_doc_date`, `doc_type`, `language`, `format_pdf_uri`, `format_pdf_url`, `format_xml_uri`, `format_xml_url`, `source_file_id_pdf`, `source_file_id_xml`, `s3_pdf_key`, `s3_xml_key`, `snapshot_date`.

Configured FK: `bill_id` → `silver_bills.bill_id`.

#### `silver_bill_sponsors`

`bill_sponsor_id`, `bill_id`, `sponsor_uri`, `sponsor_name`, `sponsor_role_uri`, `sponsor_role_name`, `is_primary`, `sponsor_order`, `snapshot_date`.

Configured FK: `bill_id` → `silver_bills.bill_id`.

#### `silver_bill_debates`

`bill_debate_id`, `bill_id`, `debate_id`, `debate_uri`, `debate_date`, `debate_show_as`, `debate_section_id`, `chamber_uri`, `chamber_name`, `debate_order`, `snapshot_date`.

Configured FK: `bill_id` → `silver_bills.bill_id`.

#### `silver_bill_events`

`bill_event_id`, `bill_id`, `event_uri`, `event_type_uri`, `event_name`, `event_date`, `chamber_uri`, `chamber_name`, `event_order`, `snapshot_date`.

Configured FK: `bill_id` → `silver_bills.bill_id`.

## Gold Products

All current gold products use configured write strategy `rebuild`.

| Product | Cadence | Primary key | Builder | Description |
| --- | --- | --- | --- | --- |
| `gold_current_members` | weekly | `member_code` | `extract/oireachtas/table_gold_current_members.py` | Current member roster mart. |
| `gold_member_activity_yearly` | weekly_current_year | `member_code`, `year` | `extract/oireachtas/table_gold_member_activity_yearly.py` | Member annual activity metrics. |
| `gold_member_activity_monthly` | weekly_current_year | `member_code`, `year_month` | `extract/oireachtas/table_gold_member_activity_monthly.py` | Member monthly activity metrics. |
| `gold_constituency_activity_yearly` | monthly | `constituency_name`, `year` | `extract/oireachtas/table_gold_constituency_activity_yearly.py` | Constituency annual activity metrics. |
| `gold_content_fact_pool` | weekly | `fact_id` | `extract/oireachtas/table_gold_content_fact_pool.py` | Deterministic candidate fact pool for Instagram content. |

### `gold_current_members`

Columns:

`member_code`, `full_name`, `party_name`, `constituency_name`, `house_no`, `office_name`, `snapshot_date`.

Verified lineage: reads logical latest `silver_members`, `silver_member_memberships`, `silver_member_parties`, `silver_member_constituencies`, and `silver_member_offices`; selects current-or-latest relationship records; filters to current members where current information is available; coalesces relationship values with convenience fields from `silver_members`.

Verified DQ requires non-empty output, registry columns, populated/unique member PK, populated `full_name`, `party_name`, `constituency_name`, and `house_no`; `office_name` is explicitly optional.

### `gold_member_activity_yearly`

`member_code`, `year`, `speech_count`, `debate_day_count`, `division_count`, `votes_cast_count`, `vote_participation_pct`, `ta_count`, `nil_count`, `staon_count`, `speech_rank`, `vote_participation_rank`, `snapshot_date`.

### `gold_member_activity_monthly`

`member_code`, `year_month`, `speech_count`, `debate_day_count`, `votes_cast_count`, `snapshot_date`.

### `gold_constituency_activity_yearly`

`constituency_name`, `year`, `member_count`, `speech_count`, `votes_cast_count`, `snapshot_date`.

### `gold_content_fact_pool`

`fact_id`, `fact_type`, `entity_type`, `entity_id`, `period_start`, `period_end`, `headline`, `metric_name`, `metric_value`, `source_table`, `source_key`, `snapshot_date`.

The registry describes this as a deterministic candidate fact pool for Instagram content. Detailed content-selection semantics must be taken from `table_gold_content_fact_pool.py`; they are not inferred from the field names here.

## Control Products

| Product | Cadence | Primary key | Write strategy | Builder | Description |
| --- | --- | --- | --- | --- | --- |
| `control_pipeline_runs` | every_run | `run_id` | `append` | `extract/oireachtas/table_control_pipeline_runs.py` | Pipeline run audit log. |
| `control_table_manifests` | every_run | `table_name` | `snapshot_replace` | `extract/oireachtas/table_control_table_manifests.py` | Latest manifest pointer per table. |
| `control_data_quality_results` | every_run | `dq_result_id` | `append` | `extract/oireachtas/table_control_data_quality_results.py` | Data-quality result records. |

### `control_pipeline_runs`

`run_id`, `workflow_run_id`, `table_name`, `mode`, `cadence`, `started_at_utc`, `finished_at_utc`, `status`, `input_params_json`, `raw_rows`, `output_rows`, `error_message`, `manifest_s3_key`.

### `control_table_manifests`

`table_name`, `latest_run_id`, `latest_snapshot_date`, `latest_parquet_key`, `latest_csv_key`, `row_count`, `column_count`, `schema_hash`, `primary_key_unique`, `dq_status`, `updated_at_utc`.

### `control_data_quality_results`

`dq_result_id`, `run_id`, `table_name`, `check_name`, `status`, `metric_value`, `threshold`, `message`, `created_at_utc`.

## Key and Relationship Model

Primary keys above are exact registry contracts. Composite PKs currently exist for:

- `gold_member_activity_yearly`: `member_code`, `year`;
- `gold_member_activity_monthly`: `member_code`, `year_month`;
- `gold_constituency_activity_yearly`: `constituency_name`, `year`.

`configs/oireachtas/write_policies.yml` declares selected foreign keys, not an exhaustive relational database constraint set. Current declared relationship families include member → membership/party/constituency/office, debate → section/speech/division, division → tallies/votes, member → votes/questions, and bill → bill child records.

The S3/CSV/Parquet implementation does not itself create database-enforced foreign keys. `extract/oireachtas/merge.py` provides `foreign_key_integrity()` for configured checks where a caller invokes it.

## Write Strategy Summary

### `snapshot_replace`

`silver_houses`, `silver_constituencies`, `silver_parties`, `silver_members`, `control_table_manifests`.

### `upsert`

All member relationship products, source/debate/speech/division/vote/question products, and all legislation silver products.

### `append`

`control_pipeline_runs`, `control_data_quality_results`.

### `rebuild`

All five gold products.

The exact enforcement implementation is documented separately in the write-policy/downstream-contract P0 reference. At implementation level, `merge_for_policy()` returns incoming rows for snapshot/rebuild and uses current+incoming deterministic PK deduplication for upsert/append, with a second business-key dedupe for policies that declare business keys.

## Refresh Membership

Registry cadence is not the only execution selector. Current default orchestration sets in `process/oireachtas_refresh_inputs.py` are:

- **weekly:** member identity/relationships, debates/speeches, divisions/votes, questions, five relevant gold products, and all control products;
- **monthly:** constituencies, parties, source files, all bill/legislation products, constituency/content gold products, and all control products;
- **yearly:** houses, constituencies, parties, members/relationships/offices, selected bill products, selected gold products, and all control products.

For exact current table order and window defaults, use the orchestration runbook and `process/oireachtas_refresh_inputs.py` rather than reconstructing the list from registry cadence labels.

## Data Quality and Validation

Every builder returns a DQ payload and the shared CLI fails the table run when DQ status is `fail`.

Verified common/representative checks include:

- output row count greater than zero;
- registry-required columns present;
- primary key present/nonblank;
- primary key unique;
- table-specific required content populated;
- S3 write errors converted into DQ failure.

Builder-specific DQ is authoritative. Do not assume every product uses every check above.

At batch level, the platform additionally requires valid table entries and candidate objects before a batch manifest can become `validated`. Downstream compatibility contracts and consumer checks are separate from canonical table DQ.

Automated regression tests in `tests/` cover write semantics, business-key merge, history dedupe, control manifest counts, candidate seeding, orchestration, contracts and related platform behavior.

## Configuration

Primary checked-in configuration:

```text
configs/oireachtas/tables.yml
configs/oireachtas/write_policies.yml
configs/oireachtas/api_params.yml
configs/oireachtas/downstream_contracts.yml
```

Relevant runtime environment-variable names include `AWS_REGION`, `S3_BUCKET`, `OIREACHTAS_BATCH_ID`, `OIREACHTAS_PUBLISH_LATEST`, and `OIREACHTAS_PUBLISH_ENABLED`.

## Security and Access

These canonical products represent public parliamentary-source data and derived metadata, but the platform's S3 access remains credential-controlled. No credentials or secret values belong in this catalogue.

The repository proves the configured bucket/region and workflow secret names; exact live IAM/bucket policy is not verified here.

## Failure Modes

Catalogue-level failure risks include:

- registry/builder schema mismatch;
- missing or changed upstream endpoint fields;
- incorrect PK generation/deduplication;
- stale/partial incremental windows;
- candidate S3 write failure;
- table-specific DQ failure;
- incompatible schema evolution affecting downstream compatibility adapters.

Contain changes in a test or immutable candidate batch, update affected validation/tests, and do not promote a failed candidate.

## Known Limitations

- The registry has column names but no formal types/nullability descriptions.
- Not every configured relationship is necessarily validated on every run; configuration declarations and invoked runtime checks are distinct facts.
- Per-column business definitions are not encoded in `tables.yml`; builder code is currently required to understand transformation semantics.
- Registry `confirmed` records a historical validation state, not live freshness/health.
- Cadence labels and orchestration table sets overlap but are not identical concepts.

## Outstanding Work

The detailed per-builder field derivation/DQ catalogue can be expanded into subordinate product/domain pages if operational need justifies it. The current P0 priority is to finish orchestration and write-policy/downstream-contract documentation without duplicating this registry contract.

## Next Safe Development Action

Document the refresh/validation orchestration as an operator runbook using current workflow YAML, `process/oireachtas_refresh_inputs.py`, batch-control helpers and observed scheduled runs. No schema or data-product implementation change is required.

## Related Documents

- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [IPA / Oireachtas documentation workstream plan](/projects/high-director/ipa-oireachtas-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `configs/oireachtas/tables.yml` SHA `1a98c25...`; `configs/oireachtas/write_policies.yml` SHA `7219ef6...`; `extract/oireachtas/schemas.py`; `extract/oireachtas/build_table.py`; complete table-builder tree; `extract/oireachtas/table_members.py`; `extract/oireachtas/table_gold_current_members.py`; `extract/oireachtas/merge.py`; `process/oireachtas_refresh_inputs.py`; Oireachtas test inventory.
- Verified by: High Director
- Verification scope: all 31 registry entries, layer/status/cadence/endpoint/PK/description/column definitions, builder locations, configured write strategy, selected relationship metadata, representative implementation/DQ behavior and orchestration relationship.
