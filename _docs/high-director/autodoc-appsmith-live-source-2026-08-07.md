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

This page persists the sanitized authoritative evidence extracted from the AutoDoc Appsmith application export supplied on `2026-08-07`. It is the current live-source evidence for Appsmith implementation details in the AutoDoc documentation workstream.

The original export is **not** stored in the documentation repository because it contained secret credential values. This record preserves the technically relevant application structure, query/action paths, bindings, and drift evidence while deliberately omitting secret values and private/internal Appsmith identifiers.

## Source Record

- Supplied file name: `AutoDoc.json`.
- Source type: Appsmith application export.
- Appsmith artifact type: `APPLICATION`.
- Client schema version: `2.0`.
- Server schema version: `12.0`.
- Application name: `AutoDoc`.
- Application slug: `autodoc`.
- Application version field: `2.0`.
- Evaluation version field: `2.0`.
- `isPublic`: `false`.
- Pages: `2`.
- Actions: `18`.
- JS Objects/action collections: `3`.
- Original-file SHA-256: `dd8d685d28fa4147c6f826acda2fb994b5c6c27d9ed868aa0afbd7012ebd5d6e`.

The export contains both published and unpublished definitions. No semantic differences were found between published and unpublished action definitions. The two page definitions are semantically aligned for the documented bindings/actions after ignoring Appsmith internal IDs and layout-only geometry.

## Sanitization Record

The source scan detected:

- `2` distinct GitHub PAT values;
- `29` PAT occurrences across the exported datasource/action definitions;
- `0` email-address patterns;
- `0` OpenAI API-key patterns.

Neither GitHub PAT value is reproduced, hashed for publication, committed, or used by this workstream. Authorization values are represented only as `Bearer <REDACTED_GITHUB_PAT>` in documentation.

Removed/not persisted material includes:

- PAT/token values;
- Appsmith/Git internal object identifiers not required to understand the system;
- `userPermissions`/`policyMap` internals;
- theme payloads and visual-layout geometry;
- image payloads;
- private/account-identifying metadata not required by the technical documentation.

Because two credential values were present in a portable export, both should be treated as exposed and rotated/revoked outside this documentation change. Rotation is an access/security operation and is not performed by this documentation workstream.

## Application Pages

### `Submit`

The current exported intake/configuration page contains these operational widgets:

| Widget | Type | Current role |
| --- | --- | --- |
| `Project` | input | Project/folder name below `doc_configs/` |
| `Mode` | select | `Create new` -> `create`; `Re-run existing` -> `rerun` |
| `Doc_Key` | input, disabled | Slug generated from `Title`, or loaded config `doc_key` in rerun mode |
| `Type` | select | `pipeline`, `dataset`, `dashboard`, `investigation`, `generic` |
| `Existing_Doc` | select | Visible in rerun mode; populated from `_index.json` |
| `Title` | input | Human-readable document title |
| `Context` | rich-text editor | HTML/text context stored in base config |
| `Asset_Type_1..5` | select | `python`, `yaml`, `sql`, `notebook`, `config`, `other` |
| `Source_Type_1..5` | select | `github_url`, `github_path`, `pasted` |
| `Asset_Locator_1..5` | input | GitHub URL/repository path |
| `Pasted_Content_1..5` | rich-text editor | Visible only when corresponding source is `pasted` |
| `Button1` | button | Calls `DocSubmitter.submit()` |
| `reset_button` | icon button | Calls `Reset.resetAll()` |
| `Button2` | button | Navigates to `DocsViewer` |

`Mode.onOptionChange` calls `GitHub_GetIndex.run()`. `Existing_Doc.onOptionChange` calls `DocLoader.loadSelected()`. The Submit button is disabled when `Project`, `Title`, or `Type` is missing.

The page displays version text `V1.5`.

### `DocsViewer`

The current exported document-editor/publication page contains:

| Widget | Type | Current role |
| --- | --- | --- |
| `Project_Select` | select | Lists directories returned by `GitHub_ListProjects` |
| `Doc_Select` | select | Lists `title`/`doc_key` entries decoded from project `_index.json` |
| `Version_Select` | select | `raw` or `reviewed` |
| `Website_Type_Select` | select | Lists website destination directories returned by `GitHub_ListWebsiteTypes` |
| `Doc_MD` | multi-line input | Decodes and displays selected Markdown from GitHub |
| `Update` | button | Calls `GitHub_UpsertDocMD.run()` |
| `Btn_ReviewDoc` | button | Calls `GitHub_TriggerReview.run()` |
| `Reviewed_Status` | text | Interprets reviewed-file existence/status |
| `Button1` | button | Calls `GitHub_TriggerPublish.run()`; disabled unless `reviewed` and a destination type are selected |
| `UpdateCopy` | button | Navigates back to `Submit` |

The page displays version text `V1.5`.

## JS Objects

The export contains these JS Object/action-collection names on `Submit`:

- `DocLoader`
- `DocSubmitter`
- `Reset`

The executable functions are exported as JS-plugin actions named `loadSelected`, `submit`, and `resetAll`.

### `DocLoader.loadSelected`

Verified flow:

1. Run `GitHub_LoadConfig`.
2. Remove newline characters from returned base64 `content`.
3. Decode and `JSON.parse` the config.
4. Store it in `appsmith.store.loadedConfig`.
5. Reset top-level widgets and the first asset block so defaults refresh.
6. Show a success/error alert.

The exported function explicitly resets `Asset_Type_1`, `Source_Type_1`, `Asset_Locator_1`, and `Pasted_Content_1`, but does not explicitly reset asset blocks 2–5. Those later widgets do have `loadedConfig.assets[n]` default bindings; the runtime effect of not explicitly resetting them has not been tested in this workstream.

### `DocSubmitter.submit`

Verified flow:

1. Call `GitHub_EnsureProject`; errors are intentionally caught/ignored.
2. Call `GitHub_GetConfig`.
3. Treat `200` as existing and store its SHA; treat `404` as create-new; stop on other status.
4. Call `GitHub_UpsertConfig`; require `200` or `201`.
5. Call `GitHub_GetIndex`.
6. Treat `200` as existing and store its SHA; treat `404` as create-new; stop on other status.
7. Call `GitHub_UpsertIndex`; require `200` or `201`.
8. Show `Config + index saved to GitHub`.

### `Reset.resetAll`

The exported reset function clears `loadedConfig`, `cfgSha`, and `idxSha`; resets mode/project/type/title/doc key/context/existing-document widgets; then resets all five asset blocks.

## GitHub API Boundary

The exported Appsmith application uses the GitHub REST API at:

```text
https://api.github.com
```

The current action set operates against `eirepolitic/autodoc` and, for website destination discovery, `eirepolitic/eirepolitic.github.io`.

The authentication scheme in the export is a Bearer GitHub PAT. **No credential value is persisted here.**

## Current REST/JS Action Inventory

### `Submit` page

| Action | Type/method | Current path/role |
| --- | --- | --- |
| `GitHub_Test` | GET | `/repos/eirepolitic/autodoc` |
| `GitHub_UpsertConfig` | PUT | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/<Doc_Key>.json` |
| `GitHub_GetConfig` | GET | Same base-config path; obtains file/SHA state |
| `GitHub_GetIndex` | GET | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/_index.json` |
| `GitHub_UpsertIndex` | PUT | Same index path; removes/replaces current `doc_key`, sorts by title |
| `GitHub_LoadConfig` | GET | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/<Existing_Doc>.json` |
| `loadSelected` | JS | Decode/store/reset existing config |
| `submit` | JS | Orchestrate project/config/index writes |
| `GitHub_EnsureProject` | PUT | `/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/.gitkeep` |
| `resetAll` | JS | Clear stored state/widgets |

`GitHub_GetIndex` is exported with automatic run behaviour and is also called on mode change/page load.

### `DocsViewer` page

| Action | Method | Current path/role |
| --- | --- | --- |
| `GitHub_ListProjects` | GET | `/repos/eirepolitic/autodoc/contents/doc_configs` |
| `GitHub_GetIndex_Viewer` | GET | `doc_configs/<selected-project>/_index.json` |
| `GitHub_GetDocMD` | GET | `docs/<project>/<type>/<doc_key>.md` or `docs/<project>/<type>/reviewed/<doc_key>.md` |
| `GitHub_UpsertDocMD` | PUT | Writes `docs/<project>/<type>/<doc_key>.md` |
| `GitHub_TriggerReview` | POST | `/repos/eirepolitic/autodoc/actions/workflows/review_doc.yml/dispatches` |
| `GitHub_CheckReviewed` | GET | Checks `docs/<project>/<type>/reviewed/<doc_key>.md` |
| `GitHub_ListWebsiteTypes` | GET | `/repos/eirepolitic/eirepolitic.github.io/contents/projects` |
| `GitHub_TriggerPublish` | POST | `/repos/eirepolitic/autodoc/actions/workflows/publish_to_website.yml/dispatches` |

`GitHub_TriggerReview` dispatches `main` with `project`, index-derived `type`, `doc_key`, and `overwrite: "true"`.

`GitHub_TriggerPublish` dispatches `main` with `project`, index-derived `type`, `doc_key`, selected `dest_type`, and `overwrite: "true"`.

## Base-Config Producer Contract

`GitHub_UpsertConfig` currently constructs this logical object before base64 encoding:

```text
project
  <- Project.text
type
  <- Type.selectedOptionValue
title
  <- Title.text
doc_key
  <- Doc_Key.text
context
  <- Context.text
updated_at
  <- new Date().toISOString()
assets[]
  <- up to five asset blocks, filtered to entries with asset_kind
```

Each asset contains:

```text
asset_kind
source
locator
content
```

`content` is stored only when source is `pasted`; otherwise it is `null`.

## Appsmith `_index.json` Producer Contract

`GitHub_UpsertIndex` currently:

1. decodes the existing index when returned;
2. removes an existing entry whose `doc_key` matches `Doc_Key.text`;
3. appends `{ doc_key, title, type, updated_at: new Date().toISOString() }`;
4. sorts by title;
5. base64 encodes the resulting JSON;
6. sends the existing index SHA when available.

This current Appsmith producer behavior differs from the current backend `process/update_index.py` authority, which rebuilds `_index.json` from base configs and derives each index `updated_at` from the base config's Git commit timestamp. The Appsmith-written registry is therefore a producer-side convenience state; backend regeneration is the deterministic reconciliation path.

## Current Live vs Repository Handoff Drift

The earlier handoff embedded in `doc_configs/autodoc/autodoc_app.json` remains historical evidence. The supplied export establishes these current differences:

| Earlier handoff | 2026-08-07 supplied export |
| --- | --- |
| `Mode` create value documented as `new` | Current value is `create`; rerun remains `rerun` |
| Handoff documents the intake/config page | Current app also has `DocsViewer` document editor/publication page |
| App "does NOT call GitHub Actions API" | Current `DocsViewer` directly dispatches `review_doc.yml` and `publish_to_website.yml` |
| Parent project folder documented as requiring manual pre-creation | Current submit path calls `GitHub_EnsureProject` to write `.gitkeep` before the config write |
| Submit flow begins with GetConfig | Current submit flow begins with EnsureProject, then GetConfig/UpsertConfig/GetIndex/UpsertIndex |
| Historical generator described `generate_docs.yml` / `process/generate_docs.py` | Current backend uses the multi-stage workflows/processors documented from repository source |
| Enrichment described as optional/manual after generation | Current backend automatic orchestration includes enrichment before extraction/render/review |

Historical claims that contradict current backend executable source remain classified as drift/history rather than silently replaced.

## Verified Source-Analysis Risks

### Exported credentials

Two distinct GitHub PAT values were embedded in the portable Appsmith export. This proves the current exported configuration contains secret material in datasource/action definitions rather than a fully non-exported secret boundary. Values are not retained in documentation. Both credentials should be rotated/revoked.

### Direct `btoa` for config JSON

`GitHub_UpsertConfig` uses direct `btoa(JSON.stringify(...))`. The historical handoff explicitly states that base64 encoding should be UTF-8 safe. Direct browser `btoa` can fail for characters outside its accepted byte range. This is a source-verified implementation mismatch; runtime failure has not been reproduced in this workstream.

### Raw/reviewed update SHA mismatch possibility

`GitHub_GetDocMD` reads either the raw or reviewed path according to `Version_Select`, but `GitHub_UpsertDocMD` always writes the raw path while taking its update SHA from `GitHub_GetDocMD.data.sha`. If `reviewed` is selected, that SHA belongs to the reviewed path rather than the raw path. This is a source-analysis risk for failed/mismatched updates; it has not been runtime-tested here.

### Partial explicit reset on load

`DocLoader.loadSelected` explicitly resets only asset block 1 after loading a config even though blocks 2–5 also bind to `loadedConfig`. The runtime effect is unknown; do not claim a user-visible defect without live reproduction.

## Trust and Access Notes

- The exported application has `isPublic: false`.
- This proves the application itself is not configured as public in the supplied export; it does not establish the exact current workspace/user membership or GitHub PAT scopes.
- Current actions perform GitHub Contents API reads/writes and workflow dispatch calls, so the active credential path must be capable of the operations it successfully performs.
- No PAT value or scope claim is inferred from the token string itself.

## Next Safe Action

Use this sanitized source record plus current `autodoc` repository source to complete the authoritative AutoDoc Appsmith/config/index documentation. Do not change Appsmith authentication, PAT scope, workflow dispatch behavior, or publication architecture as part of documentation work.

Separately, treat both exported GitHub PAT values as exposed and rotate/revoke them through the relevant GitHub/Appsmith credential-management path.

## Related Documents

- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: user-supplied `AutoDoc.json`, original SHA-256 `dd8d685d28fa4147c6f826acda2fb994b5c6c27d9ed868aa0afbd7012ebd5d6e`; current `autodoc` repository source for backend conflict checks; historical handoff in `doc_configs/autodoc/autodoc_app.json`.
- Verified by: High Director
- Verification scope: application metadata, page/widget/action structure, GitHub paths/methods, JS orchestration, base/index producer logic, published/unpublished semantic comparison, secret scan/redaction, and historical drift.
- Not verified: live runtime execution, exact workspace memberships, actual GitHub PAT scopes, or post-export changes made after the supplied file was created.
