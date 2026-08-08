---
title: AutoDoc Appsmith intake and document control
summary: Current verified Appsmith implementation for AutoDoc configuration intake, existing-document loading, document editing, review dispatch, and publication dispatch.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 32
permalink: /projects/systems/autodoc-appsmith-intake/
tags:
  - autodoc
  - appsmith
  - github
  - configuration
  - documentation
---

# AutoDoc Appsmith intake and document control

## Summary

The current AutoDoc Appsmith application is a two-page private application. `Submit` creates/loads AutoDoc project configurations and maintains the project registry. `DocsViewer` reads and edits Markdown, checks reviewed artifacts, and dispatches review and website-publication workflows.

This page is based on the user-supplied Appsmith export dated `2026-08-07`. That export is authoritative for the captured current Appsmith implementation. Current `autodoc` workflows/Python remain stronger evidence for backend behavior where historical Appsmith handoff text conflicts with executable source.

The raw export is not stored because it contained GitHub PAT values. Sanitized evidence is persisted at `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`.

## Current Implementation State

Verified from the export:

- application: `AutoDoc`;
- `isPublic: false`;
- pages: `Submit`, `DocsViewer`;
- GitHub API host: `https://api.github.com`;
- primary repository: `eirepolitic/autodoc`;
- website destination discovery: `eirepolitic/eirepolitic.github.io`;
- Appsmith performs GitHub Contents API reads/writes;
- Appsmith dispatches `review_doc.yml` and `publish_to_website.yml`;
- Appsmith writes both base config and `_index.json` during submit;
- current backend can later rebuild `_index.json` deterministically.

The UI displays `V1.5` on both pages. Appsmith export metadata also contains application/evaluation version fields `2.0`; these are separate metadata values.

## Source of Truth

- Sanitized live source: `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`.
- Repository config/index contract: `_docs/data/autodoc-configuration-and-project-index.md`.
- Current backend: `autodoc` workflows plus `process/*.py`.
- Historical Appsmith handoff: `doc_configs/autodoc/autodoc_app.json`.

If a later verified live export differs, document it as current and retain this dated record as history/drift evidence.

## `Submit` Page

### Primary fields

| Widget | Current role |
| --- | --- |
| `Project` | Project/folder below `doc_configs/` |
| `Mode` | `Create new` = `create`; `Re-run existing` = `rerun` |
| `Doc_Key` | Generated/loaded slug; disabled for manual editing |
| `Type` | `pipeline`, `dataset`, `dashboard`, `investigation`, `generic` |
| `Existing_Doc` | Existing document selector from `_index.json` |
| `Title` | Document title |
| `Context` | Rich-text context persisted in base config |

Five asset blocks provide:

```text
Asset_Type_n
Source_Type_n
Asset_Locator_n
Pasted_Content_n
```

Asset types are `python`, `yaml`, `sql`, `notebook`, `config`, and `other`. Source modes are `github_url`, `github_path`, and `pasted`. Pasted content is shown only for the `pasted` source mode.

`Mode.onOptionChange` calls `GitHub_GetIndex.run()`. `Existing_Doc.onOptionChange` calls `DocLoader.loadSelected()`. The submit button calls `DocSubmitter.submit()` and is disabled when `Project`, `Title`, or `Type` is missing.

## Existing-Document Load

`DocLoader.loadSelected()` currently:

1. calls `GitHub_LoadConfig`;
2. strips newlines from returned base64 content;
3. decodes and parses the JSON;
4. stores it in `appsmith.store.loadedConfig`;
5. resets top-level widgets and asset block 1 so default bindings refresh;
6. shows a success/error notification.

Asset blocks 2–5 bind to `loadedConfig` but are not explicitly reset by this function. This is source-verified; runtime impact was not tested.

## Submit Orchestration

Current submit sequence:

```text
GitHub_EnsureProject
  -> GitHub_GetConfig
  -> GitHub_UpsertConfig
  -> GitHub_GetIndex
  -> GitHub_UpsertIndex
```

### Ensure project

`GitHub_EnsureProject` issues `PUT` to:

```text
/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/.gitkeep
```

Errors from this call are caught/ignored by the submit JS before later steps continue.

### Get/upsert base config

`GitHub_GetConfig` and `GitHub_UpsertConfig` use:

```text
/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/<Doc_Key>.json
```

The submit JS treats `200` as existing, `404` as create-new, and other statuses as stop/error state. Existing-file SHA is retained for the update request.

The logical base-config payload contains:

```text
project
type
title
doc_key
context
updated_at
assets[]
```

Each asset contains `asset_kind`, `source`, `locator`, and `content`. `content` is populated only for `pasted`; otherwise it is `null`.

The current expression uses direct `btoa(JSON.stringify(...))`. The historical handoff specified UTF-8-safe base64 handling. Direct browser `btoa` can fail for some non-ASCII characters, so this is a source-verified risk rather than a reproduced runtime defect.

### Get/upsert index

`GitHub_GetIndex` and `GitHub_UpsertIndex` use:

```text
/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/_index.json
```

The Appsmith index writer:

1. decodes existing index state;
2. removes any matching `doc_key` entry;
3. appends current `doc_key`, `title`, `type`, and `new Date().toISOString()`;
4. sorts by title;
5. base64 encodes the resulting array;
6. supplies current index SHA when updating.

A successful submit displays `Config + index saved to GitHub`.

## Appsmith Registry vs Backend Registry

Appsmith currently writes `_index.json` directly. Current backend `process/update_index.py` can rebuild the same registry from base config files and derives each registry `updated_at` from the base config's latest Git committer timestamp.

Therefore:

- Appsmith's registry write is current producer behavior;
- backend rebuild is the deterministic reconciliation/recovery path;
- a stale index should be rebuilt from base configs instead of manually reconstructed.

## `DocsViewer` Page

Current controls include:

| Widget | Current role |
| --- | --- |
| `Project_Select` | Project selector from `GitHub_ListProjects` |
| `Doc_Select` | Indexed document selector |
| `Version_Select` | `raw` or `reviewed` |
| `Website_Type_Select` | Website destination selector |
| `Doc_MD` | Decoded Markdown display/edit control |
| `Update` | Calls `GitHub_UpsertDocMD.run()` |
| `Btn_ReviewDoc` | Calls `GitHub_TriggerReview.run()` |
| `Reviewed_Status` | Interprets reviewed-file state |
| publication button | Calls `GitHub_TriggerPublish.run()` |

The publication button is disabled unless `reviewed` and a website destination type are selected.

## Document Discovery

`GitHub_ListProjects` reads:

```text
/repos/eirepolitic/autodoc/contents/doc_configs
```

`GitHub_GetIndex_Viewer` reads the selected project's `_index.json` and supplies `title`, `doc_key`, and `type` for downstream path/workflow inputs.

`GitHub_ListWebsiteTypes` reads:

```text
/repos/eirepolitic/eirepolitic.github.io/contents/projects
```

This is current exported discovery logic; it does not prove every returned directory is semantically valid for every document.

## Markdown Read/Write Boundary

`GitHub_GetDocMD` reads either:

```text
docs/<project>/<type>/<doc_key>.md
```

or:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

according to `Version_Select`.

`GitHub_UpsertDocMD` always writes the raw path:

```text
docs/<project>/<type>/<doc_key>.md
```

A source-analysis risk exists because the update SHA comes from `GitHub_GetDocMD.data.sha`. If `reviewed` is selected, that SHA belongs to the reviewed file while the write target remains raw. This can produce a SHA/path mismatch. Runtime failure was not reproduced in this workstream.

## Review Dispatch

`GitHub_TriggerReview` posts to:

```text
/repos/eirepolitic/autodoc/actions/workflows/review_doc.yml/dispatches
```

Current dispatch body includes:

```text
ref: main
project: selected project
type: selected index entry type
doc_key: selected index entry doc_key
overwrite: "true"
```

This is current live Appsmith behavior and supersedes the historical handoff statement that the app did not call the GitHub Actions API.

## Reviewed-File Check

`GitHub_CheckReviewed` reads:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

`Reviewed_Status` interprets existence/state for the user. File existence is not proof that the newer documentation publication governance was followed.

## Publication Dispatch

`GitHub_TriggerPublish` posts to:

```text
/repos/eirepolitic/autodoc/actions/workflows/publish_to_website.yml/dispatches
```

Current dispatch inputs include:

```text
ref: main
project: selected project
type: selected index entry type
doc_key: selected index entry doc_key
dest_type: selected website destination type
overwrite: "true"
```

The backend workflow currently uses `WEBSITE_PAT` to clone and directly push the reviewed Markdown file into `eirepolitic.github.io`.

This is **CURRENT VERIFIED BEHAVIOR**. **CURRENT DOCUMENTATION GOVERNANCE** separately requires branch/PR, successful `Validate documentation`, merge, and successful matching Pages deployment. The current Appsmith/publication path does not implement that newer governance sequence. This documentation records the mismatch but does not redesign it.

## Reset Behavior

`Reset.resetAll()` clears:

```text
loadedConfig
cfgSha
idxSha
```

It resets mode, project, type, title, doc key, context, existing document, and all five asset blocks.

## Authentication and Security Boundary

The supplied export used Bearer GitHub PAT authentication in datasource/action definitions. Two distinct PAT values were present in the portable export.

No PAT value is stored or reproduced in documentation. Exact PAT scopes and workspace membership are not inferred.

Because portable export content contained the credentials, both PATs should be treated as exposed and rotated/revoked outside this documentation PR. Changing credential storage/scope is a security/access-control operation and is not performed automatically here.

Appsmith exports should therefore be treated as sensitive until inspected and sanitized.

## Current vs Historical Drift

| Historical handoff | Current supplied export |
| --- | --- |
| Create value `new` | `create` |
| Intake/config page only | `Submit` plus `DocsViewer` |
| App does not call GitHub Actions API | Review and publication are directly dispatched |
| Project folder must be manually pre-created | `GitHub_EnsureProject` writes `.gitkeep` |
| Submit starts at config lookup | Submit starts with EnsureProject |
| `generate_docs.yml` / `process/generate_docs.py` backend | Current staged enrich/extract/render/review backend |
| Enrichment optional/manual after generation | Current automatic pipeline enriches before extract/render/review |

Historical differences are retained as drift evidence.

## Failure Modes and Recovery

### Config write fails

Inspect Appsmith/GitHub response status and target path. `404` from the existence check is expected for create-new; other unexpected statuses stop the current submit path.

### Index write fails after config succeeds

The base config may already be valid. Do not recreate it blindly. Run the backend index rebuild to regenerate `_index.json` from base configs.

### Existing document cannot load

Verify the `_index.json` entry and base-config path. Rebuild the index if the base config exists but registry state is stale.

### Review dispatch fails

Verify selected project/type/doc key and inspect the GitHub Actions workflow state. Do not treat raw Markdown as reviewed to bypass the failure.

### Publication dispatch succeeds but governance is incomplete

A successful direct publication is not equivalent to PR validation/merge/Pages governance. Keep implementation behavior and governance status separate.

### Non-ASCII config submission fails

The current config writer uses direct `btoa`. Preserve the input and inspect the action/browser error; do not strip or transliterate source text as a workaround.

## Known Limitations

- This verifies the supplied export state, not post-export changes.
- Exact Appsmith workspace membership and PAT scopes are unknown.
- Direct-`btoa`, raw/reviewed-SHA, and partial-reset risks were identified from source but not runtime reproduced.
- Publication remains coupled to the direct-push workflow and its documented governance mismatch.

## Next Safe Development Action

Publish this focused Appsmith/config/index component through `Validate documentation`, merge, and matching Pages deployment. Then document automatic pipeline orchestration and trust boundaries from current backend source on a separate `docs/autodoc-*` branch.

Do not modify PAT scope/storage, Appsmith query architecture, workflow-dispatch behavior, or publication architecture without explicit approval.

## Related Documents

- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [Sanitized Appsmith live source](/projects/high-director/autodoc-appsmith-live-source-2026-08-07/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: supplied AutoDoc Appsmith export recorded by SHA-256 in the sanitized live-source page; current `autodoc` workflows/Python for backend conflict checks; historical Appsmith handoff in `doc_configs/autodoc/autodoc_app.json`.
- Verified by: High Director
- Verification scope: pages/widgets, JS objects, GitHub actions/paths/methods, base config/index writes, Markdown editing, review/publication dispatches, credential boundary, recovery behavior, and historical drift.
- Not verified: post-export live changes, runtime reproduction of source-analysis risks, exact Appsmith workspace access, or PAT scopes.
