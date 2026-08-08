---
title: AutoDoc Appsmith live source — 2026-08-07
summary: Sanitized authoritative technical record derived from the user-supplied AutoDoc Appsmith application export, with secret values and private/internal identifiers removed.
section: high-director
doc_type: note
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 105
permalink: /projects/high-director/autodoc-appsmith-live-source-2026-08-07/
repository: eirepolitic.github.io
system: AutoDoc
source_repository: autodoc
tags:
  - high-director
  - autodoc
  - appsmith
  - source-evidence
  - sanitized
---

# AutoDoc Appsmith live source — 2026-08-07

## Purpose

This page persists sanitized authoritative evidence extracted from the AutoDoc Appsmith application export supplied on `2026-08-07`. The raw export is not stored because it contained GitHub PAT values. This record retains implementation structure, query/action paths, bindings, and drift evidence without secret values or private Appsmith identifiers.

## Source Record

- Supplied file: `AutoDoc.json`.
- Artifact type: `APPLICATION`.
- Appsmith client schema version: `2.0`.
- Appsmith server schema version: `12.0`.
- Application name/slug: `AutoDoc` / `autodoc`.
- Application/evaluation version fields: `2.0` / `2.0`.
- `isPublic`: `false`.
- Pages: `2`.
- Actions: `18`.
- JS Objects/action collections: `3`.
- Original-file SHA-256: `dd8d685d28fa4147c6f826acda2fb994b5c6c27d9ed868aa0afbd7012ebd5d6e`.

Published and unpublished action definitions were semantically equivalent for the documented behavior after ignoring Appsmith internal IDs and layout-only data.

## Sanitization Record

The source scan found:

- `2` distinct GitHub PAT values;
- `29` PAT occurrences in datasource/action definitions;
- no email-address pattern;
- no OpenAI API-key pattern.

No PAT value is reproduced, hashed for publication, committed, or used. Authorization is documented only as `Bearer <REDACTED_GITHUB_PAT>`.

Removed/not persisted material includes PAT/token values, Appsmith/Git internal object identifiers not needed for system understanding, permission-map internals, theme/layout geometry, image payloads, and private/account-identifying metadata.

Because two credential values were present in a portable export, both should be treated as exposed and rotated/revoked outside this documentation PR. Rotation is an access/security operation and is not performed here.

## Application Pages

### `Submit`

Current operational widgets include:

| Widget | Role |
| --- | --- |
| `Project` | Project/folder below `doc_configs/` |
| `Mode` | `Create new` -> `create`; `Re-run existing` -> `rerun` |
| `Doc_Key` | Generated from title or loaded from existing config; disabled |
| `Type` | `pipeline`, `dataset`, `dashboard`, `investigation`, `generic` |
| `Existing_Doc` | Rerun selector populated from `_index.json` |
| `Title` | Document title |
| `Context` | Rich-text context persisted in base config |
| `Asset_Type_1..5` | `python`, `yaml`, `sql`, `notebook`, `config`, `other` |
| `Source_Type_1..5` | `github_url`, `github_path`, `pasted` |
| `Asset_Locator_1..5` | URL/repository path |
| `Pasted_Content_1..5` | Inline content shown for `pasted` |

`Mode.onOptionChange` calls `GitHub_GetIndex.run()`. `Existing_Doc.onOptionChange` calls `DocLoader.loadSelected()`. The submit button calls `DocSubmitter.submit()` and is disabled when `Project`, `Title`, or `Type` is missing. A reset control calls `Reset.resetAll()`. Navigation opens `DocsViewer`.

The page displays application UI version text `V1.5`.

### `DocsViewer`

Current operational widgets include:

| Widget | Role |
| --- | --- |
| `Project_Select` | Project selector from `GitHub_ListProjects` |
| `Doc_Select` | `title`/`doc_key` selector from project `_index.json` |
| `Version_Select` | `raw` or `reviewed` |
| `Website_Type_Select` | Website destination directory selector |
| `Doc_MD` | Decoded Markdown display/edit field |
| `Update` | Calls `GitHub_UpsertDocMD.run()` |
| `Btn_ReviewDoc` | Calls `GitHub_TriggerReview.run()` |
| `Reviewed_Status` | Interprets reviewed-file state |
| publication button | Calls `GitHub_TriggerPublish.run()`; requires reviewed version plus destination type |

The page also displays `V1.5`.

## JS Objects

Exported JS Objects/action collections are `DocLoader`, `DocSubmitter`, and `Reset`.

### `DocLoader.loadSelected`

1. Run `GitHub_LoadConfig`.
2. Remove newlines from the base64 response.
3. Decode and parse JSON.
4. Store it in `appsmith.store.loadedConfig`.
5. Reset top-level widgets and asset block 1 so bindings refresh.
6. Show success/error notification.

Asset blocks 2–5 bind to `loadedConfig` but are not explicitly reset by this function. Runtime effect was not tested.

### `DocSubmitter.submit`

1. Call `GitHub_EnsureProject`; errors are caught/ignored.
2. Call `GitHub_GetConfig`.
3. Treat `200` as existing and store SHA; `404` as create-new; stop on other status.
4. Call `GitHub_UpsertConfig`; require `200` or `201`.
5. Call `GitHub_GetIndex`.
6. Treat `200` as existing and store SHA; `404` as create-new; stop on other status.
7. Call `GitHub_UpsertIndex`; require `200` or `201`.
8. Show `Config + index saved to GitHub`.

### `Reset.resetAll`

Clears `loadedConfig`, `cfgSha`, and `idxSha`, then resets mode/project/type/title/doc key/context/existing-document widgets and all five asset blocks.

## GitHub API Boundary

API host:

```text
https://api.github.com
```

Current exported actions operate against `eirepolitic/autodoc` and use `eirepolitic/eirepolitic.github.io` for website destination discovery.

### `Submit` actions

| Action | Method/type | Path/role |
| --- | --- | --- |
| `GitHub_Test` | GET | `/repos/eirepolitic/autodoc` |
| `GitHub_UpsertConfig` | PUT | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/<Doc_Key>.json` |
| `GitHub_GetConfig` | GET | Same config path |
| `GitHub_GetIndex` | GET | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/_index.json` |
| `GitHub_UpsertIndex` | PUT | Same index path |
| `GitHub_LoadConfig` | GET | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/<Existing_Doc>.json` |
| `GitHub_EnsureProject` | PUT | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/.gitkeep` |
| `loadSelected`, `submit`, `resetAll` | JS | UI orchestration |

### `DocsViewer` actions

| Action | Method | Path/role |
| --- | --- | --- |
| `GitHub_ListProjects` | GET | `/repos/eirepolitic/autodoc/contents/doc_configs` |
| `GitHub_GetIndex_Viewer` | GET | selected project `_index.json` |
| `GitHub_GetDocMD` | GET | raw or reviewed Markdown path |
| `GitHub_UpsertDocMD` | PUT | raw Markdown path |
| `GitHub_TriggerReview` | POST | `/repos/eirepolitic/autodoc/actions/workflows/review_doc.yml/dispatches` |
| `GitHub_CheckReviewed` | GET | reviewed Markdown path |
| `GitHub_ListWebsiteTypes` | GET | `/repos/eirepolitic/eirepolitic.github.io/contents/projects` |
| `GitHub_TriggerPublish` | POST | `/repos/eirepolitic/autodoc/actions/workflows/publish_to_website.yml/dispatches` |

Review dispatch uses `ref: main` plus `project`, index-derived `type`, `doc_key`, and `overwrite: "true"`. Publication dispatch uses `ref: main` plus `project`, index-derived `type`, `doc_key`, selected `dest_type`, and `overwrite: "true"`.

## Base-Config Producer Contract

`GitHub_UpsertConfig` builds:

```text
project
type
title
doc_key
context
updated_at
assets[]
```

Each asset contains `asset_kind`, `source`, `locator`, and `content`; `content` is stored only for `pasted`, otherwise `null`.

## Appsmith `_index.json` Producer Contract

`GitHub_UpsertIndex` decodes existing index state, removes any matching `doc_key`, appends `{doc_key, title, type, updated_at}`, sorts by title, base64 encodes the array, and sends the existing index SHA when present.

This differs from current backend `process/update_index.py`, which rebuilds the registry from base configs and uses Git commit time for `updated_at`. Backend regeneration is therefore the deterministic reconciliation path.

## Current Live vs Historical Handoff Drift

| Earlier handoff | 2026-08-07 export |
| --- | --- |
| Create value `new` | `create` |
| Intake/config page only | `Submit` plus `DocsViewer` |
| App does not call GitHub Actions API | Review and publication workflows are directly dispatched |
| Project folder manually pre-created | `GitHub_EnsureProject` writes `.gitkeep` |
| Submit begins with config lookup | Submit begins with EnsureProject |
| `generate_docs.yml` / `process/generate_docs.py` backend | Current staged backend workflows/processors |
| Enrichment optional/manual after generation | Current automatic backend includes enrichment before extraction/render/review |

Historical differences remain drift evidence rather than being silently overwritten.

## Verified Source-Analysis Risks

### Exported credentials

Two distinct GitHub PAT values were embedded in the portable export. Values are not retained. Both should be rotated/revoked.

### Direct `btoa` for config JSON

`GitHub_UpsertConfig` uses direct `btoa(JSON.stringify(...))`. The historical handoff described UTF-8-safe base64 encoding. Direct browser `btoa` can fail for some non-ASCII characters. This is a source-verified risk, not a reproduced runtime failure.

### Raw/reviewed update SHA mismatch possibility

`GitHub_GetDocMD` can read raw or reviewed Markdown according to `Version_Select`, but `GitHub_UpsertDocMD` always writes the raw path while using `GitHub_GetDocMD.data.sha`. When `reviewed` is selected, that SHA belongs to the reviewed path. This is a source-analysis risk and was not runtime-tested.

## Trust and Access Notes

- Exported application has `isPublic: false`.
- This does not prove exact workspace membership or PAT scopes.
- Actions perform GitHub Contents API reads/writes and workflow dispatches.
- No credential scope is inferred from token text.

## Next Safe Action

Use this sanitized record and current `autodoc` source to complete the Appsmith/config/index component. Do not change authentication, PAT scope, workflow dispatch, or publication architecture as part of documentation work.

Separately, rotate/revoke both exposed GitHub PATs through the appropriate GitHub/Appsmith credential-management path.

## Related Documents

- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: user-supplied `AutoDoc.json`, SHA-256 `dd8d685d28fa4147c6f826acda2fb994b5c6c27d9ed868aa0afbd7012ebd5d6e`; current `autodoc` source for backend conflict checks; historical handoff in `doc_configs/autodoc/autodoc_app.json`.
- Verified by: High Director
- Verification scope: application metadata, page/widget/action structure, GitHub paths/methods, JS orchestration, base/index producer logic, secret scan/redaction, and historical drift.
- Not verified: live runtime execution, workspace memberships, PAT scopes, or changes after the supplied export.
