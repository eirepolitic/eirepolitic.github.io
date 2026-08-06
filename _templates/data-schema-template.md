---
title: <Dataset or schema name>
summary: <One sentence stating what the data represents, its grain, and primary use>
section: data
doc_type: reference
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <Person or team>
order: 100
permalink: /projects/data/<slug>/
# Optional:
# repository: <Repository containing authoritative definitions>
# system: <Producing or governing system>
# tags:
#   - <format>
#   - <domain>
---

# <Dataset or schema name>

> Remove unused guidance and headings. Do not invent values for undocumented fields.

## Summary

State what the dataset or schema represents, its row or event grain, primary consumers, and whether this document describes a logical contract, physical dataset, API payload, table, file, or model.

## Current Implementation State

Describe what exists now, active versions, environments, publication status, known producer differences, deprecations, and unverified areas.

Clearly separate the intended contract from observed data when they differ.

## Source of Truth

Identify the authoritative definition and implementation locations.

- Canonical schema: `<repository and exact path, registry subject, database object, or platform model>`
- Producer code: `<repository and exact path>`
- Transformation code: `<repository and exact path>`
- Storage object: `<bucket/key prefix, database.schema.table, dataset, or workspace object>`
- Validation code: `<repository and exact path or platform rule>`
- Consumer contract: `<stable document link or exact location>`

State which source wins when definitions conflict.

## Ownership and Lifecycle

Document producer, steward, consumers, update frequency or trigger, retention, versioning, compatibility policy, deprecation process, and deletion or archival expectations.

## Data Flow

Describe where the data originates, transformations applied, intermediate locations, publication path, and downstream consumers. Name exact repositories, jobs, workflows, tables, buckets, APIs, apps, reports, and flows.

## Inputs

List upstream sources with format, interface, grain, key fields, freshness expectation, sensitivity, and validation requirements.

## Outputs

List published forms with format, partitioning, location, consumers, update behavior, service expectations, and compatibility guarantees.

## Schema

Document fields in a compact table. Split into subordinate pages when the schema is too large to scan or is independently versioned.

| Field | Type | Required | Description | Constraints | Example |
| --- | --- | --- | --- | --- | --- |
| `<field_name>` | `<type>` | Yes/No | `<meaning>` | `<allowed values, range, format, or relationship>` | `<safe synthetic value>` |

Use synthetic examples. Never include real secrets, credentials, private personal data, or confidential records.

## Keys and Relationships

Define primary keys, natural keys, foreign keys, uniqueness, cardinality, ordering, deduplication, null handling, and referential expectations.

## Business and Transformation Rules

Document derived fields, filters, joins, precedence rules, mappings, normalization, timestamps, timezone handling, default behavior, and exception handling. Link exact implementation paths.

## Data Quality and Validation

State automated and manual checks, thresholds, schema validation, reconciliation, freshness checks, accepted exceptions, failure behavior, and evidence locations.

Include exact validation commands, jobs, tests, or queries where available.

## Configuration

Record configuration names and locations for producers, transformations, storage, validation, schedules, and consumers. Include names of variables, secret objects, connections, parameters, and resource identifiers without secret values.

## Security and Access

State classification, sensitive fields, access roles, encryption expectations, masking or redaction, retention constraints, approved uses, prohibited uses, audit requirements, and secret-storage boundaries.

Do not include production records or values that could identify a person, credential, account, or private resource.

## Failure Modes

Document missing, late, duplicated, malformed, incompatible, partial, or misrouted data; symptoms; detection method; evidence location; safe containment; replay or recovery approach; and escalation runbooks.

## Known Limitations

List known quality, coverage, freshness, lineage, scale, semantics, compatibility, retention, or platform limitations.

## Outstanding Work

List actionable schema, producer, validation, lineage, quality, migration, or documentation work with exact location and dependencies.

## Next Safe Development Action

State the smallest change or verification that can proceed safely. Include the authoritative definition, impacted producers and consumers, compatibility requirement, test path, and rollback or migration consideration.

## Related Documents

Link producing systems, repositories, consuming systems, runbooks, architecture decisions, migrations, and predecessor or successor schemas. State the relationship when useful.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<schema version, database object, files, code commit, validation run, or sample period>`
- Verified by: `<person or process>`
- Verification scope: `<definitions, fields, rules, and data checks actually verified>`

## When to Create Subordinate Pages

Create subordinate pages for large field catalogs, separate schema versions, domain-specific entities, detailed lineage, mappings, migrations, quality rules, or consumer contracts. Keep this overview authoritative for purpose, grain, source of truth, lifecycle, high-level flow, compatibility, security, limitations, outstanding work, and next safe action.
