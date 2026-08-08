---
title: AutoDoc configuration and project index
summary: Verified contracts for AutoDoc base configuration JSON, enriched configuration JSON, and owner-scoped _index.json registries, including the current Appsmith producer boundary.
section: data
doc_type: schema
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 31
permalink: /projects/data/autodoc-configuration-and-project-index/
tags:
  - autodoc
  - json
  - configuration
  - schema
  - github
---

# AutoDoc configuration and project index

## Purpose

This page documents the current repository contracts used to configure AutoDoc projects, persist source-enrichment results, and provide the owner/project document registry used by Appsmith and backend workflows.

No formal JSON Schema file was found in `autodoc`. These are **observed and consumer-enforced contracts** derived from current configs, Python consumers, workflows, and the verified Appsmith export supplied on `2026-08-07`.

## Source of Truth

Backend contract authority:

- `doc_configs/<project>/<doc_key>.json`;
- `doc_configs/<project>/<doc_key>.enriched.json`;
- `doc_configs/<project>/_index.json`;
- `process/enrich_configs.py`;
- `process/section_extract.py`;
- `process/render_sections.py`;
- `process/update_index.py`;
- `.github/workflows/autodoc_pipeline.yml`.

Current Appsmith producer authority:

- sanitized source record `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`;
- current Appsmith documentation `_docs/systems/autodoc-appsmith-intake.md`.

The older handoff embedded in `doc_configs/autodoc/autodoc_app.json` remains historical evidence where it differs from the live export or current backend.

## Storage Layout

```text
doc_configs/
└── <project>/
    ├── <doc_key>.json
    ├── <doc_key>.enriched.json
    ├── _index.json
    └── summaries/
        └── <doc_key>.csv
```

The summary CSV is documented with the extraction stage; this page owns the JSON contracts.

## Base Configuration Contract

Current verified examples and the Appsmith producer use this logical structure:

```json
{
  "project": "autodoc",
  "type": "pipeline",
  "title": "Example title",
  "doc_key": "example_doc_key",
  "context": "<p>Context</p>",
  "updated_at": "2026-08-07T00:00:00.000Z",
  "assets": []
}
```

| Field | Type | Current behavior |
| --- | --- | --- |
| `project` | string | Project identity; normally matches `doc_configs/<project>/` |
| `type` | string | Required by extraction/rendering and selects type-template behavior |
| `title` | string | Document title and index display title |
| `doc_key` | string | Document identity; normally matches the config file stem |
| `context` | string | Preserved through enrichment and supplied to extraction; Appsmith writes rich-text content |
| `updated_at` | string | Producer-supplied config timestamp; not the current index freshness source |
| `assets` | array | Must be a list for enrichment; may be empty |

The automatic workflow also derives project/document identity from the changed repository path, so path/name conventions are operationally significant.

## Base Asset Contract

```json
{
  "asset_kind": "python",
  "source": "github_url",
  "locator": "https://github.com/example/example/blob/main/path/file.py",
  "content": null
}
```

| Field | Type | Purpose |
| --- | --- | --- |
| `asset_kind` | string or null | Classification; Appsmith currently offers `python`, `yaml`, `sql`, `notebook`, `config`, `other` |
| `source` | string | Current backend source mode: `pasted`, `github_path`, or `github_url` |
| `locator` | string | URL/path used by resolver; may be empty for pasted content |
| `content` | string or null | Inline content for `pasted`; current Appsmith writes null for non-pasted sources |

The current Appsmith page exposes up to five asset blocks and filters out blocks with no `asset_kind` before writing the base config.

## Enriched Configuration Contract

`process/enrich_configs.py` copies the base config, replaces `assets` with enriched asset objects, and adds `_enrichment`.

Each enriched asset adds:

| Field | Meaning |
| --- | --- |
| `resolved_content` | Canonical resolved text or base64 for detected binary content; null on failure |
| `resolved_content_lines` | Text split with line endings preserved; null for binary/failure |
| `resolved_meta` | Retrieval/provenance metadata |
| `resolved_ok` | Resolution success boolean |
| `resolved_error` | Captured per-asset resolution error or null |
| `resolved_at` | UTC resolution-attempt timestamp |

If an asset item is not an object, enrichment converts it to a structured failed-resolution object rather than failing solely for that item.

### `_enrichment`

Current source writes:

| Field | Meaning |
| --- | --- |
| `enriched_at` | Enriched-config creation timestamp |
| `enrichment_version` | Current source value `1.1` |
| `source_config_path` | Base config repository path |
| `github_repo_default` | Default repo used for relative `github_path` |
| `github_ref_default` | Default ref used for relative `github_path` |
| `project` | Resolved project |
| `doc_key` | Resolved document key |

Persisted historical enriched files can retain older runtime/default values; current code is authority for current behavior.

## Resolution Metadata Variants

Current enrichment can record:

- `pasted`: method plus `binary_base64: false`;
- GitHub Contents API: API URL/status/SHA/encoding/path/binary flag/method/owner/repo/ref;
- generic HTTP GET: status/final URL/content type/binary flag/method;
- error: at least an error method plus the per-asset exception text.

Detailed resolver behavior belongs to the enrichment/source-resolution page.

## `_index.json` Registry Contract

Current backend `process/update_index.py` writes an array of:

```json
{
  "doc_key": "autodoc_app",
  "title": "AutoDoc App",
  "type": "generic",
  "updated_at": "2026-02-25T17:52:53-08:00"
}
```

It scans base configs under `doc_configs/<project>/*.json`, excluding `_index.json` and `*.enriched.json`, then sorts entries case-insensitively by title.

| Field | Backend derivation |
| --- | --- |
| `doc_key` | `cfg.doc_key`, fallback to file stem |
| `title` | `cfg.title`, fallback empty string |
| `type` | `cfg.type`, fallback empty string |
| `updated_at` | latest Git committer timestamp for the base config path; current UTC time only if Git metadata cannot be obtained |

**Important:** backend registry `updated_at` does not come from the base config's `updated_at` field.

## Current Appsmith Index Producer

The verified Appsmith export also writes `_index.json` during Submit. It:

1. decodes existing index content when present;
2. removes the current `doc_key` entry;
3. appends current `doc_key`, `title`, `type`, and `new Date().toISOString()`;
4. sorts by title;
5. base64 encodes the array;
6. sends the existing index SHA for updates.

This means Appsmith and backend can assign different `updated_at` values for the same logical document because they represent different producer logic.

### Authority and recovery

- **Current Appsmith behavior:** maintains index immediately after config submit.
- **Current backend reconciliation:** regenerates index from base configs and Git history through `process/update_index.py`.

If `_index.json` is stale/inconsistent, the safe recovery path is the backend index rebuild rather than manual entry reconstruction.

## Producer and Consumer Boundaries

### Producers

- current Appsmith `GitHub_UpsertConfig` -> base config;
- current Appsmith `GitHub_UpsertIndex` -> immediate registry update;
- direct repository/config clients that follow the contract;
- `process/enrich_configs.py` -> enriched config;
- `process/update_index.py` -> deterministic registry rebuild.

### Consumers

- `.github/workflows/autodoc_pipeline.yml` detects changed base config paths;
- `process/enrich_configs.py` consumes base config/assets;
- `process/section_extract.py` consumes base + enriched config and requires `type`;
- `process/render_sections.py` consumes base + enriched config plus upstream summary artifacts;
- Appsmith rerun/document selectors consume `_index.json` and base configs.

## Validation Actually Enforced

There is no central schema validator. Current checks are distributed:

- enrichment requires `assets` to be a list;
- extraction/rendering require expected config/intermediate files;
- `type` is required for document-template behavior;
- unsupported asset `source` values become per-asset resolution failures;
- automatic path handling expects base configs below `doc_configs/<project>/` and excludes index/enriched files from the changed-base-config set;
- index rebuild fails on invalid included JSON.

Producers should preserve canonical fields/path conventions even where a consumer has fallback behavior.

## Failure Modes and Recovery

### Invalid base JSON

Repair the base config; do not patch enriched/generated artifacts as the primary fix.

### `assets` is not an array

Enrichment raises an error. Correct the base config and rerun the applicable stage.

### Individual asset fails resolution

Enrichment can still write the enriched config with `resolved_ok: false` and `resolved_error`. Correct source/locator/access, then rerun enrichment.

### Index is stale or missing

Use the index-rebuild path so `process/update_index.py` regenerates it from base configs and Git timestamps.

### Appsmith config succeeds but index write fails

Do not recreate the successful base config blindly. Rebuild the index from repository source.

### Config `updated_at` differs from index `updated_at`

This is expected. Config metadata, Appsmith immediate registry time, and backend Git-derived registry time are distinct signals.

## Security and Privacy

Do not store PATs, API keys, passwords, OAuth/access tokens, private keys, personal emails/account IDs, or private user data in config fields, context, asset content, or locators.

Enrichment can copy source content into repository-persisted JSON. Technical resolvability does not imply publication/privacy suitability.

The supplied Appsmith export contained two distinct GitHub PAT values. Those values are not retained in documentation and should be rotated/revoked separately.

## Known Limitations

- No formal JSON Schema or centralized config validator was found.
- Consumer fallbacks mean syntactically valid JSON can still fail semantic requirements later.
- Live Appsmith behavior is verified from the supplied export, not from post-export runtime interaction.
- Historical enriched/config artifacts can preserve older implementation state.

## Next Safe Action

Complete this focused Appsmith/config/index documentation through validation, merge, and matching Pages deployment. Then move to automatic pipeline orchestration/trust boundaries without modifying configuration or credential architecture.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [Sanitized Appsmith live source](/projects/high-director/autodoc-appsmith-live-source-2026-08-07/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc` `main`; current base/enriched configs and `_index.json`; `process/enrich_configs.py`; `section_extract.py`; `render_sections.py`; `update_index.py`; `.github/workflows/autodoc_pipeline.yml`; supplied Appsmith export recorded by SHA-256 in the sanitized live-source page.
- Verified by: High Director
- Verification scope: base/enriched/index contracts, producer/consumer behavior, current Appsmith writes, backend reconciliation, distributed validation, failure/recovery, and security boundary.
- Not verified: post-export Appsmith changes or external credential/access policy.
