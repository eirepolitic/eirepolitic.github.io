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

The current AutoDoc Appsmith application is a two-page private application that provides:

1. project/document configuration intake and rerun loading on `Submit`;
2. generated/reviewed Markdown viewing and raw-document editing on `DocsViewer`;
3. direct GitHub Actions dispatches for review and website publication from `DocsViewer`.

This page is based on the user-supplied Appsmith application export dated `2026-08-07`. The supplied export is stronger evidence for current Appsmith implementation than the older technical handoff embedded in `autodoc` configuration files. Current backend behavior is still established by current `autodoc` workflows/Python source when backend claims conflict with Appsmith historical text.

The original export contained secret GitHub PAT values and is therefore not stored in the documentation repository. A sanitized evidence record is persisted at `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`.

## Current Implementation State

Verified from the supplied export:

- application name: `AutoDoc`;
- application is not configured as public (`isPublic: false`);
- pages: `Submit` and `DocsViewer`;
- GitHub REST API host: `https://api.github.com`;
- primary source repository: `eirepolitic/autodoc`;
- website-repository discovery target: `eirepolitic/eirepolitic.github.io`;
- Appsmith performs GitHub Contents API reads/writes and GitHub Actions workflow-dispatch calls;
- base config and `_index.json` are both written by Appsmith during submit;
- current backend can separately rebuild `_index.json` deterministically from base configs;
- `DocsViewer` dispatches `review_doc.yml` and `publish_to_website.yml` on `main`.

The application displays version text `V1.5` on both pages. Appsmith export metadata includes application version/evaluation version `2.0`; these are different metadata concepts and should not be conflated.

## Source of Truth

Current Appsmith implementation evidence:

- sanitized live-source record: `_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md`;
- supplied export SHA-256 recorded there for source integrity;
- repository-side config/index contract: `_docs/data/autodoc-configuration-and-project-index.md`;
- current backend implementation: current `autodoc` workflows and `process/*.py`.

Historical Appsmith implementation evidence:

- detailed handoff embedded in `doc_configs/autodoc/autodoc_app.json`.

If a later live export differs, the later verified live configuration becomes current implementation and this source remains dated historical evidence.

## Page 1: `Submit`

`Submit` is the project configuration and rerun-intake page.

### Primary fields

| Widget | Role |
| --- | --- |
| `Project` | Project/folder under `doc_configs/` |
| `Mode` | `Create new` (`create`) or `Re-run existing` (`rerun`) |
| `Doc_Key` | Generated/loaded document slug; disabled for direct editing |
| `Type` | `pipeline`, `dataset`, `dashboard`, `investigation`, or `generic` |
| `Existing_Doc` | Existing indexed document selector in rerun mode |
| `Title` | Human-readable document title |
| `Context` | Rich-text context stored in base configuration |

### Asset fields

The page exposes five repeated asset blocks. Each block contains:

- `Asset_Type_n`;
- `Source_Type_n`;
- `Asset_Locator_n`;
- `Pasted_Content_n`.

Current asset-type options are:

```text
python
yaml
sql
notebook
config
other
```

Current source-type values are:

```text
github_url
github_path
pasted
```

`Pasted_Content_n` is shown only for a `pasted` source. The base-config producer filters the asset array to entries that have an `asset_kind`.

### Mode and existing-document behavior

`Mode.onOptionChange` calls `GitHub_GetIndex.run()`.

`Existing_Doc.onOptionChange` calls `DocLoader.loadSelected()`.

`DocLoader.loadSelected()`:

1. calls `GitHub_LoadConfig`;
2. decodes the GitHub Contents API base64 payload;
3. parses the JSON;
4. stores it in `appsmith.store.loadedConfig`;
5. resets top-level widgets so their bindings refresh;
6. explicitly resets asset block 1;
7. shows a success/error notification.

Asset blocks 2–5 also bind to `loadedConfig`, but the function does not explicitly reset them. The source difference is verified; the actual live runtime effect has not been reproduced and is therefore not documented as a confirmed user-visible defect.

## Submit Orchestration

The Submit button calls `DocSubmitter.submit()` and is disabled if `Project`, `Title`, or `Type` is missing.

Current orchestration is:

```text
GitHub_EnsureProject
  -> GitHub_GetConfig
  -> GitHub_UpsertConfig
  -> GitHub_GetIndex
  -> GitHub_UpsertIndex
```

### Step 1: ensure project folder

`GitHub_EnsureProject` sends a GitHub Contents API `PUT` for:

```text
/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/.gitkeep
```

The submit JS catches/ignores errors from this step before proceeding.

### Step 2: inspect base config

`GitHub_GetConfig` reads:

```text
/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/<Doc_Key>.json
```

The JS treats:

- `200` as an existing file and stores its SHA;
- `404` as create-new state;
- other statuses as stop/error state.

### Step 3: write base config

`GitHub_UpsertConfig` writes the same path. The current logical JSON body contains:

```text
project
type
title
doc_key
context
updated_at
assets[]
```

Each asset contains:

```text
asset_kind
source
locator
content
```

For non-`pasted` assets, `content` is `null`.

The current Appsmith expression uses direct browser `btoa(JSON.stringify(...))` for this config payload. This differs from the historical handoff's stated UTF-8-safe base64 requirement. Direct `btoa` can reject characters outside its byte-range expectations, so this is a source-verified implementation risk; no runtime failure was reproduced during documentation.

### Step 4: inspect index

`GitHub_GetIndex` reads:

```text
/repos/eirepolitic/autodoc/contents/doc_configs/<Project>/_index.json
```

It is also configured for automatic run behavior and is called through page/mode interactions.

### Step 5: write index

`GitHub_UpsertIndex`:

1. decodes the existing index when present;
2. removes the current `doc_key` entry;
3. appends current `doc_key`, `title`, `type`, and Appsmith-generated `updated_at`;
4. sorts the array by title;
5. base64 encodes the JSON;
6. writes with the current SHA when updating an existing index.

After a successful config/index sequence the JS displays `Config + index saved to GitHub`.

## Appsmith Registry vs Backend Registry Authority

There are two current ways `_index.json` can be produced:

### Current Appsmith producer

Appsmith directly updates `_index.json` during submit and uses `new Date().toISOString()` for each updated entry.

### Current backend reconciliation

`process/update_index.py` rebuilds `_index.json` from base config files, excludes enriched configs, sorts by title, and derives `updated_at` from the latest Git committer timestamp for the base config path.

Therefore the Appsmith-written registry is not the final deterministic authority for registry freshness. If the index becomes stale or inconsistent, the backend index rebuild path should be used rather than manually reconstructing entries.

## Page 2: `DocsViewer`

`DocsViewer` is the current document viewing/editing/review/publication page.

### Primary widgets

| Widget | Role |
| --- | --- |
| `Project_Select` | Project directory selector |
| `Doc_Select` | Indexed document selector |
| `Version_Select` | `raw` or `reviewed` |
| `Website_Type_Select` | Website destination directory selector |
| `Doc_MD` | Decoded Markdown display/edit field |
| `Update` | Writes Markdown through `GitHub_UpsertDocMD` |
| `Btn_ReviewDoc` | Dispatches review workflow |
| `Reviewed_Status` | Displays reviewed-file status |
| publication button | Dispatches website publication workflow |
| `UpdateCopy` | Returns to `Submit` |

The publication button is disabled unless the `reviewed` version and a website destination type are selected.

## Document Discovery

`GitHub_ListProjects` reads:

```text
/repos/eirepolitic/autodoc/contents/doc_configs
```

`GitHub_GetIndex_Viewer` reads the selected project's `_index.json`, which supplies `title`, `doc_key`, and `type` for document selection and downstream path/workflow inputs.

`GitHub_ListWebsiteTypes` reads:

```text
/repos/eirepolitic/eirepolitic.github.io/contents/projects
```

This establishes the current exported Appsmith logic for discovering website destination directories. It does not prove that every returned directory is an appropriate publication destination for every document.

## Markdown Read/Write Boundary

`GitHub_GetDocMD` reads either:

```text
docs/<project>/<type>/<doc_key>.md
```

or:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

depending on `Version_Select`.

The returned base64 content is decoded into `Doc_MD`.

`GitHub_UpsertDocMD` writes the raw path:

```text
docs/<project>/<type>/<doc_key>.md
```

A source-analysis risk exists: when `Version_Select` is `reviewed`, `GitHub_GetDocMD.data.sha` belongs to the reviewed file while `GitHub_UpsertDocMD` still writes the raw file path. If that SHA is supplied during a raw-file update, GitHub can reject it as a mismatched blob/version. This risk is verified from exported expressions but was not live-runtime tested.

## Review Dispatch

`GitHub_TriggerReview` sends a GitHub Actions workflow-dispatch request to:

```text
/repos/eirepolitic/autodoc/actions/workflows/review_doc.yml/dispatches
```

Current dispatch inputs include:

```text
ref: main
project: selected project
type: selected index entry type
doc_key: selected index entry doc_key
overwrite: "true"
```

This is current live Appsmith behavior and supersedes the older handoff statement that the Appsmith app did not call the GitHub Actions API.

## Reviewed-File Check

`GitHub_CheckReviewed` reads:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

`Reviewed_Status` interprets the result for the user. This is a file-existence/content-state check, not a proof that the review workflow itself succeeded cleanly or that the reviewed document is publication-approved under the newer documentation governance.

## Publication Dispatch

`GitHub_TriggerPublish` dispatches:

```text
/repos/eirepolitic/autodoc/actions/workflows/publish_to_website.yml/dispatches
```

Current inputs include:

```text
ref: main
project: selected project
type: selected index entry type
doc_key: selected index entry doc_key
dest_type: selected website destination type
overwrite: "true"
```

This triggers the current backend publication workflow, whose verified implementation uses `WEBSITE_PAT` to clone and directly push a reviewed Markdown file into `eirepolitic.github.io`.

This is **CURRENT VERIFIED BEHAVIOR**. It does not implement **CURRENT DOCUMENTATION GOVERNANCE**, which requires branch/PR, successful `Validate documentation`, merge, and matching Pages success. The mismatch is documented; no Appsmith or workflow redesign is approved by this documentation workstream.

## Reset Behavior

`Reset.resetAll()` clears Appsmith stored values for:

```text
loadedConfig
cfgSha
idxSha
```

It then resets mode, project, type, title, doc key, context, existing document, and all five asset blocks.

## GitHub Authentication Boundary

The supplied export used Bearer GitHub PAT authentication in datasource/action definitions. Two distinct PAT values were present in the portable export.

No PAT value is stored or reproduced in documentation.

Because portable export content contained the credentials, those two PATs must be treated as exposed credentials. Rotation/revocation is an access/security operation outside this documentation PR and should be performed explicitly in GitHub/Appsmith credential management.

The export does not establish exact PAT scopes or current workspace membership, so those are not inferred.

## Historical Drift from Repository Handoff

The older handoff remains useful historical evidence. Current verified differences include:

| Historical handoff | Current supplied Appsmith export |
| --- | --- |
| Create-mode value `new` | Create-mode value `create` |
| Intake/config page only | `Submit` plus `DocsViewer` |
| App does not call GitHub Actions API | `DocsViewer` dispatches review and publication workflows |
| Project folder must be manually pre-created | Submit attempts `GitHub_EnsureProject` `.gitkeep` write |
| Submit begins at config lookup | Submit begins with EnsureProject |
| Old generator workflow/script references | Current backend uses staged enrich/extract/render/review pipeline |
| Enrichment described as optional/manual after generation | Current automatic backend orchestration includes enrichment before extraction/render/review |

Historical differences are retained as drift evidence rather than erased.

## Failure Modes and Recovery

### Project/config write fails

Inspect the Appsmith action response and GitHub path/status. A `404` during config existence check is expected for create-new state; other unexpected statuses stop the current submit sequence.

### Index write fails after config succeeds

The base config may already be valid even if Appsmith index maintenance fails. Do not recreate the config blindly. Use the backend index rebuild path to reconcile `_index.json` from base configs.

### Existing document does not load

Verify the project `_index.json` entry and the corresponding base-config path. Rebuild the index if the config exists but the registry is stale.

### Review dispatch fails

Verify the selected project/type/doc key and inspect the GitHub Actions dispatch/workflow state. Do not bypass review by treating a raw file as reviewed.

### Publication dispatch succeeds but website governance is incomplete

A successful dispatch/direct push is not equivalent to the newer branch/PR/validation/merge/Pages discipline. The current workflow behavior and governance requirement remain separate until an architecture/security change is explicitly approved.

### Unicode/non-ASCII config submission fails

The current Appsmith config write uses direct `btoa`. If submission fails for non-ASCII content, preserve the input and inspect the browser/Appsmith action error. Do not silently strip or transliterate source text as a recovery mechanism.

## Security and Privacy

Never enter or persist PATs, API keys, passwords, OAuth/access tokens, private keys, personal emails/account IDs, or private user data in AutoDoc project context/assets.

Appsmith export files must be treated as sensitive until inspected because the current supplied export contained credentials. Do not commit raw exports automatically.

## Known Limitations

- This page verifies source/configuration state from the supplied export, not live interaction behavior after the export date.
- Exact Appsmith workspace memberships and GitHub PAT scopes are unknown.
- Source-analysis risks around direct `btoa`, raw/reviewed SHA handling, and partial reset behavior were not reproduced at runtime.
- Current Appsmith publication dispatch remains coupled to the direct-push publication workflow and therefore to the documented governance mismatch.

## Next Safe Development Action

Complete this focused Appsmith/config/index documentation change through `Validate documentation`, merge, and matching Pages deployment. Then document automatic pipeline orchestration/trust boundaries from current backend workflow source in a separate `docs/autodoc-*` branch.

Do not modify PAT scope/storage, Appsmith query architecture, workflow-dispatch behavior, or website-publication architecture without explicit approval.

## Related Documents

- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [Sanitized Appsmith live source](/projects/high-director/autodoc-appsmith-live-source-2026-08-07/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: supplied AutoDoc Appsmith export recorded by SHA-256 in the sanitized live-source page; current `autodoc` repository workflows/Python for backend conflict checks; historical Appsmith handoff in `doc_configs/autodoc/autodoc_app.json`.
- Verified by: High Director
- Verification scope: pages/widgets, JS objects, GitHub actions/paths/methods, base-config/index writes, document viewing/editing, review/publication dispatches, credential boundary, failure/recovery behavior, and historical drift.
- Not verified: post-export live changes, runtime reproduction of identified source-analysis risks, exact Appsmith workspace access, or PAT scopes.
