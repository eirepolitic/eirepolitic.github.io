---
title: AutoDoc configuration and project index
summary: Verified repository contracts for AutoDoc base configuration JSON, enriched configuration JSON, and owner-scoped _index.json project registries.
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

This page documents the current repository-backed data contracts used to configure AutoDoc projects, persist source-enrichment results, and provide an owner/project document registry.

No formal JSON Schema file is present in the verified `autodoc` tree. The contracts below are therefore **observed and consumer-enforced contracts** derived from current configuration files plus current Python consumers. Where a field is required by a downstream stage, that requirement is identified explicitly rather than inferred from examples alone.

## Status and Last Verification

- Status: active and verified from current repository source.
- Last verified: `2026-08-07`.
- Current live Appsmith widget/query state is not required to establish these repository contracts, although Appsmith is one producer of base configurations.

## Source of Truth

Current authoritative sources are:

- `doc_configs/<project>/<doc_key>.json` — base configuration instances;
- `doc_configs/<project>/<doc_key>.enriched.json` — enrichment outputs;
- `doc_configs/<project>/_index.json` — owner/project registry;
- `process/enrich_configs.py` — enrichment input/output behavior;
- `process/section_extract.py` — config/enriched requirements for extraction;
- `process/render_sections.py` — config/enriched requirements for rendering;
- `process/update_index.py` — authoritative index rebuild behavior;
- `.github/workflows/autodoc_pipeline.yml` — automatic path and index regeneration boundary.

The embedded Appsmith handoff in `doc_configs/autodoc/autodoc_app.json` is captured-state evidence for one producer of these files. It is not stronger than current Python source for the backend contract.

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

This page owns the JSON contracts. The `summaries/<doc_key>.csv` intermediate contract belongs to the section-extraction documentation.

## Base Configuration Contract

Verified examples include `doc_configs/autodoc/autodoc_app.json` and `doc_configs/autodoc/autodoc_creation_pipeline.json`.

Observed top-level structure:

```json
{
  "project": "autodoc",
  "type": "pipeline",
  "title": "Example title",
  "doc_key": "example_doc_key",
  "context": "<p>HTML or other text context</p>",
  "updated_at": "2026-02-27T01:24:30.036Z",
  "assets": []
}
```

### Top-level fields

| Field | Observed type | Current consumer behavior | Notes |
| --- | --- | --- | --- |
| `project` | string | Used as project identity in configs/enrichment metadata; automatic workflow also derives project from the file path | Should correspond to `doc_configs/<project>/` |
| `type` | string | Required by `section_extract.py` and directly indexed by `render_sections.py` | Selects `templates/types/<type>.md` when present |
| `title` | string | Used for generated document title and `_index.json` display title | `update_index.py` permits empty string if absent |
| `doc_key` | string | Used by enrichment/index logic; some consumers also derive/fallback from file name | Normal convention is file name `<doc_key>.json` |
| `context` | string | Preserved into enriched JSON and supplied with the rest of the enriched configuration to extraction | Current examples store HTML from the Appsmith rich-text editor |
| `updated_at` | string | Preserved as base-config metadata | Not used by `update_index.py` for registry freshness |
| `assets` | array | Must be a list for `enrich_configs.py`; otherwise enrichment raises an error | May be empty |

The current automatic workflow determines changed project/document identity from `doc_configs/<project>/<filename>.json`. This means file location/name are operationally significant even though corresponding JSON fields are also present.

## Base Asset Contract

Observed asset object:

```json
{
  "asset_kind": "python",
  "source": "github_url",
  "locator": "https://github.com/example/example/blob/main/path/file.py",
  "content": null
}
```

### Base asset fields

| Field | Observed type | Purpose |
| --- | --- | --- |
| `asset_kind` | string or null | Classification such as `python`, `yaml`, `sql`, `notebook`, `config`, or `other`; backend enrichment preserves it rather than enforcing the captured Appsmith option set |
| `source` | string | Source-resolution mode. Current backend supports exactly `pasted`, `github_path`, or `github_url` |
| `locator` | string | Path or URL used by resolvers; may be empty for pasted content |
| `content` | string or null | Inline source content for `pasted`; commonly null for externally resolved sources |

For current backend source modes and detailed resolver behavior, see the dedicated enrichment/source-resolution page when published.

## Enriched Configuration Contract

`process/enrich_configs.py` copies the base configuration, replaces `assets` with enriched asset objects, and adds a top-level `_enrichment` object.

Observed/enforced shape:

```json
{
  "project": "autodoc",
  "type": "pipeline",
  "title": "Example title",
  "doc_key": "example_doc_key",
  "context": "...",
  "updated_at": "...",
  "assets": [
    {
      "asset_kind": "python",
      "source": "github_url",
      "locator": "...",
      "content": null,
      "resolved_content": "...",
      "resolved_content_lines": ["...\n"],
      "resolved_meta": {},
      "resolved_ok": true,
      "resolved_error": null,
      "resolved_at": "2026-02-27T01:24:48.344867Z"
    }
  ],
  "_enrichment": {
    "enriched_at": "...",
    "enrichment_version": "1.1",
    "source_config_path": "doc_configs/autodoc/example_doc_key.json",
    "github_repo_default": "eirepolitic/autodoc",
    "github_ref_default": "main",
    "project": "autodoc",
    "doc_key": "example_doc_key"
  }
}
```

The example above shows the current code's default `github_ref_default` value. Historical persisted enriched artifacts may retain values produced by an earlier run/environment and should not be mistaken for current code defaults.

## Enriched Asset Fields

Each dictionary asset is copied, then enrichment fields are initialized or populated:

| Field | Type | Meaning |
| --- | --- | --- |
| `resolved_content` | string or null | Canonical resolved value; text for text assets, base64 string for detected binary assets, null on failure |
| `resolved_content_lines` | array of strings or null | Text split with line endings preserved; omitted/null for binary or failed resolution |
| `resolved_meta` | object or null | Retrieval/provenance metadata, or `{ "method": "error" }` on a caught resolution failure |
| `resolved_ok` | boolean | Whether that asset resolved successfully |
| `resolved_error` | string or null | Captured exception/error message for the asset |
| `resolved_at` | string | UTC ISO timestamp assigned for the resolution attempt |

If an `assets` item is not an object, current enrichment does not crash solely for that item. It converts the item to a structured failed-resolution object with null base fields and `resolved_error: "Asset is not an object"`.

## Resolution Metadata Variants

Current source can emit metadata depending on resolution method.

### Pasted

```json
{
  "method": "pasted",
  "binary_base64": false
}
```

### GitHub Contents API

GitHub-based resolution metadata can include:

```text
api_url
status
sha
encoding
path
binary_base64
method
owner
repo
ref
```

`method` is currently `github_contents_api` for `github_path` or `github_contents_api_from_url` for a recognized GitHub blob/raw URL.

### Generic HTTP GET

Metadata can include:

```text
status
final_url
content_type
binary_base64
method = http_get
```

### Error

Caught asset-resolution failures produce `resolved_ok: false`, null resolved content/lines, the exception text in `resolved_error`, and at least `resolved_meta.method = error` when no earlier metadata exists.

## Top-Level `_enrichment` Contract

Current `process/enrich_configs.py` writes:

| Field | Meaning |
| --- | --- |
| `enriched_at` | UTC timestamp for creation of the enriched configuration |
| `enrichment_version` | Current source value `1.1` |
| `source_config_path` | Repository-relative path of the base config processed |
| `github_repo_default` | Default repository used for relative `github_path` locators |
| `github_ref_default` | Default ref used for relative `github_path` locators |
| `project` | Project resolved from config or directory name |
| `doc_key` | Document key resolved from config or file stem |

## `_index.json` Registry Contract

Current `process/update_index.py` is authoritative for registry generation. For each base configuration under `doc_configs/<project>/*.json`, excluding `_index.json` and `*.enriched.json`, it writes one item:

```json
{
  "doc_key": "autodoc_app",
  "title": "AutoDoc App",
  "type": "generic",
  "updated_at": "2026-02-25T17:52:53-08:00"
}
```

The full file is a JSON array sorted case-insensitively by `title`.

### Index field derivation

| Field | Derivation |
| --- | --- |
| `doc_key` | `cfg.doc_key`, falling back to the base config file stem |
| `title` | `cfg.title`, falling back to empty string |
| `type` | `cfg.type`, falling back to empty string |
| `updated_at` | latest Git committer timestamp for the base config path via `git log -1 --format=%cI`; current UTC time only if Git metadata cannot be obtained |

**Important:** `_index.json.updated_at` does **not** come from the base JSON's `updated_at` field.

## Registry Lifecycle

The captured Appsmith handoff says the UI historically updated `_index.json` directly after writing a base config. Current backend orchestration provides a stronger authoritative reconciliation mechanism: after processing changed base configs, `.github/workflows/autodoc_pipeline.yml` calls `process/update_index.py --project <project>` for every affected project and commits the regenerated registry.

This creates an important distinction:

- **Captured Appsmith behavior:** direct config upsert followed by direct index upsert.
- **Current backend authority:** index can be rebuilt deterministically from base configs and Git history.

A stale or manually edited `_index.json` therefore should be repaired by rebuilding from source configs rather than treated as the sole source of project truth.

## Producer and Consumer Boundaries

### Producers

Verified/captured producers include:

- Appsmith intake/configuration application — captured handoff describes GitHub Contents API writes to base config and index;
- direct repository edits or other GitHub clients capable of creating a valid base config;
- `process/enrich_configs.py` — enriched config producer;
- `process/update_index.py` — authoritative index rebuilder.

### Consumers

- `.github/workflows/autodoc_pipeline.yml` detects changed base config paths;
- `process/enrich_configs.py` consumes base config/assets;
- `process/section_extract.py` consumes base + enriched config and requires `type`;
- `process/render_sections.py` consumes base + enriched config and requires `type` plus expected upstream artifacts;
- captured Appsmith rerun/edit UI consumes `_index.json` and existing base configs.

## Validation Rules Actually Enforced

There is no central JSON validation layer verified in the repository. Validation is distributed across consumers:

- `assets` must be an array/list for enrichment;
- `type` must exist for extraction and rendering to select document-template behavior;
- referenced base/enriched files must exist for downstream stages;
- unsupported asset `source` values become per-asset enrichment failures;
- automatic pipeline path parsing expects base configs below `doc_configs/<project>/` and excludes `_index.json`/`.enriched.json` from its changed-base-config set;
- index rebuild parses every included base JSON and will fail if an included file is invalid JSON.

Because validation is distributed, producers should preserve the canonical field names and path conventions even where an individual function has a fallback.

## Failure Modes and Recovery

### Invalid JSON

**Symptom:** the relevant Python consumer raises during `json.loads`.

**Recovery:** repair the base JSON; do not patch generated/enriched outputs as the primary fix.

### `assets` is not an array

**Symptom:** enrichment raises `cfg.assets must be a list` for that config.

**Recovery:** fix the base configuration and rerun enrichment/automatic processing.

### Individual asset cannot resolve

**Symptom:** enriched config is still written, but the asset has `resolved_ok: false` and `resolved_error`.

**Recovery:** correct the asset source/locator/access problem, then rerun enrichment with the applicable overwrite/recovery path.

### `_index.json` is stale or incorrect

**Symptom:** captured UI selection may omit or mislabel documents even though base configs exist.

**Recovery:** run the dedicated index rebuild path so `process/update_index.py` regenerates the registry from base configs and Git timestamps.

### Base-config `updated_at` differs from registry `updated_at`

This is expected. They represent different signals: producer-supplied config metadata versus repository commit time used by the current index builder.

## Security and Privacy

Base and enriched configs are repository content. Do not store secrets, PATs, `OPENAI_API_KEY`, access tokens, passwords, private keys, personal emails/account IDs, or private user data in `context`, `assets.content`, locators, or other fields.

Enrichment can copy external source content into the repository. A source being technically resolvable does not make its content safe to publish or persist. Credential values must never be embedded in config JSON.

## Known Limitations

- No formal JSON Schema or centralized config validator was found.
- Current consumers tolerate some missing fields through fallbacks, so a syntactically valid config can still fail later-stage semantics.
- Exact current Appsmith producer behavior remains to be verified from live Appsmith source; this page does not infer live widget/query state from the historical handoff.
- Historical enriched files preserve the state of the code/environment that created them and can differ from current source defaults.

## Next Safe Action

Verify the current live AutoDoc Appsmith application as one coherent source, compare it with the captured handoff, persist a sanitized current-state record, and then complete the Appsmith intake/configuration page without altering this repository contract unless source evidence proves a real current difference.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)
- [Repository scan — AutoDoc](/projects/high-director/repository-scan-autodoc/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc` `main`; `doc_configs/autodoc/autodoc_app.json`; `doc_configs/autodoc/autodoc_creation_pipeline.json`; `doc_configs/autodoc/autodoc_creation_pipeline.enriched.json`; `doc_configs/autodoc/_index.json`; `process/enrich_configs.py`; `process/section_extract.py`; `process/render_sections.py`; `process/update_index.py`; `.github/workflows/autodoc_pipeline.yml`.
- Verified by: High Director
- Verification scope: base configuration fields, asset fields, enriched configuration additions, enrichment metadata, registry fields/derivation/order, producer/consumer boundaries, distributed validation, and recovery rules.
- Unverified area: exact current live Appsmith producer configuration.
