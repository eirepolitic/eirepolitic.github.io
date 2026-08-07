---
title: Documentation Search Index
summary: Generated JSON dataset with one record per public technical document, consumed by browser-side documentation search.
section: data
doc_type: reference
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: Eire Politic
repository: eirepolitic.github.io
system: Eire Politic Documentation Site
order: 10
permalink: /projects/data/documentation-search-index/
tags:
  - json
  - search
related:
  - /projects/systems/documentation-site/
  - /projects/repositories/eirepolitic-github-io/
---

# Documentation Search Index

## Summary

`/search-index.json` is a generated JSON array with one object per public document in the Jekyll `docs` collection. Browser code in `assets/js/search.js` loads it to rank and render documentation search results.

## Current Implementation State

The index is generated during each Jekyll build from `site.docs`. Documents with `visibility: private` are excluded. The current consumer expects an array and treats missing optional values as empty strings or arrays.

## Source of Truth

- Canonical generation template: `search-index.json`
- Producer: Jekyll rendering of `site.docs`
- Consumer: `assets/js/search.js`
- Published object: `/search-index.json`
- Documentation metadata contract: `DOCUMENTATION_STANDARD.md`

If generated output and documentation disagree, the committed `search-index.json` Liquid template and current consumer code are authoritative for implementation behavior.

## Ownership and Lifecycle

The index is owned with the documentation site. It is regenerated on each successful Pages build, is not independently versioned, and changes when source documents or the generation template change.

## Data Flow

1. Markdown documents under `_docs/` are loaded into the Jekyll `docs` collection.
2. `search-index.json` filters out documents where `visibility == 'private'`.
3. Jekyll serializes metadata and normalized page content into a JSON array.
4. GitHub Pages publishes the generated file at `/search-index.json`.
5. `assets/js/search.js` fetches the array and performs client-side ranking.

## Inputs

Each input record is a Jekyll document with front matter and rendered content. Required metadata is governed by `DOCUMENTATION_STANDARD.md` and `scripts/validate_docs.py`.

## Outputs

The output is a single JSON array published at `/search-index.json`. Each object represents one searchable document.

## Schema

| Field | Type | Required in output | Description | Constraints |
| --- | --- | --- | --- | --- |
| `title` | string | Yes | Document title | Serialized from `doc.title` |
| `summary` | string | Yes | Short description | Defaults to empty string |
| `url` | string | Yes | Published relative URL | Generated from `doc.url` |
| `section` | string | Yes | Top-level documentation section | Defaults to empty string |
| `doc_type` | string | Yes | Documentation type | Defaults to empty string |
| `status` | string | Yes | Lifecycle status | Defaults to empty string |
| `repository` | string | Yes | Related repository name | Defaults to empty string |
| `technologies` | array | Yes | Technology labels | Defaults to empty array |
| `tags` | array | Yes | Search tags | Defaults to empty array |
| `updated` | string | Yes | Document update date | Formatted as `YYYY-MM-DD` |
| `content` | string | Yes | Searchable document body | HTML stripped and whitespace normalized |

## Keys and Relationships

The dataset has no explicit primary key. `url` functions as the practical document locator. The producer emits one object for each included Jekyll document in build iteration order.

## Business and Transformation Rules

- Exclude documents with `visibility: private`.
- Serialize metadata with Jekyll `jsonify`.
- Default missing scalar search metadata to empty strings.
- Default missing `technologies` and `tags` to empty arrays.
- Format `updated` as `YYYY-MM-DD`.
- Strip HTML and normalize whitespace from document content.

The browser consumer searches `title`, `summary`, `repository`, section/type/status metadata, technologies, tags, and content. Results are scored by field weight and then by `updated` date.

## Data Quality and Validation

Documentation validation checks required source metadata, allowed values, dates, and references before merge. A successful Pages build confirms the generation template renders. Search behavior is then verified by loading the published index through the browser search page.

## Configuration

- Generation template: `search-index.json`
- Consumer code: `assets/js/search.js`
- Collection configuration: `_config.yml`
- Source metadata rules: `DOCUMENTATION_STANDARD.md`

No secret configuration is required.

## Security and Access

The index is public. It must contain only information safe for public publication. `visibility: private` removes a document from this generated index but does not remove committed content from repository history and must not be treated as a security control.

## Failure Modes

- Invalid generated JSON: browser search fails to parse the response.
- Missing index: browser search reports temporary unavailability.
- Incorrect metadata type: ranking or result metadata may degrade.
- Sensitive content committed to a public document: it may be included in the index and repository history.

## Known Limitations

- Search is entirely client-side.
- The full normalized content of every public technical document is included in the index.
- There is no explicit schema version field.
- `url` is relied on as the practical locator but is not declared as a formal unique key.

## Outstanding Work

No schema change is required for the Example Documents phase. Template changes should occur only if real use exposes a defect.

## Next Safe Development Action

Use the existing Documentation Site Operations runbook as the real Runbook example, review it against `_templates/runbook-template.md`, and change only concrete gaps found through that comparison.

## Related Documents

- [Eire Politic Documentation Site](/projects/systems/documentation-site/) produces and serves this dataset.
- [eirepolitic.github.io](/projects/repositories/eirepolitic-github-io/) contains the producer and consumer source files.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: `search-index.json`, `assets/js/search.js`, `_config.yml`, `scripts/validate_docs.py`, and successful Pages deployment `31137516088`
- Verified by: High Director
- Verification scope: generation filter, output fields, transformations, consumer usage, security boundary, and failure behavior
