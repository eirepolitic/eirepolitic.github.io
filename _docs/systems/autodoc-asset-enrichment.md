---
title: AutoDoc asset enrichment and source resolution
summary: Current verified AutoDoc enrichment stage that resolves pasted, repository-path, GitHub URL, and generic HTTP asset content into persisted enriched configuration JSON.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 35
permalink: /projects/systems/autodoc-asset-enrichment/
tags:
  - autodoc
  - enrichment
  - github
  - http
  - pipeline
---

# AutoDoc asset enrichment and source resolution

## Summary

Asset enrichment is the first executable content-resolution stage in the current AutoDoc backend. `process/enrich_configs.py` reads base project configurations below `doc_configs/`, resolves each configured asset, and writes a persisted `<doc_key>.enriched.json` file containing source content, provenance/status metadata, per-asset resolution success/error state, and top-level enrichment metadata.

The automatic AutoDoc pipeline runs enrichment with `--overwrite` before section extraction. A separate manual workflow supports project/document filtering, overwrite control, and an `only_missing` option.

Enrichment does not call OpenAI. Its external trust boundary is source retrieval: configured GitHub or HTTP locations can cause the Actions runner to fetch external content that is then persisted in the `autodoc` repository.

## Source of Truth

Current implementation:

```text
process/enrich_configs.py
.github/workflows/enrich_configs.yml
.github/workflows/autodoc_pipeline.yml
requirements.txt
```

Current input/output schema:

```text
_docs/data/autodoc-configuration-and-project-index.md
```

Current verified implementation SHA for `process/enrich_configs.py`:

```text
70442976f979592c1f35b2acc1977520ed7471ee
```

## Entry Point

```text
python process/enrich_configs.py [--project PROJECT] [--doc-key DOC_KEY] [--overwrite] [--only-missing]
```

`main()` returns:

- `0` when all selected configurations complete successfully, including the case where no configs are found or all selected enriched outputs are skipped;
- `1` when one or more selected configuration files fail at configuration-processing level;
- `2` for missing repository prerequisites such as `doc_configs/` or a requested project directory that does not exist.

Individual asset-resolution failures are normally captured inside the enriched JSON and do not by themselves make the whole configuration fail.

## Environment

| Name | Current behavior |
| --- | --- |
| `GITHUB_TOKEN` | Optional for public sources; recommended/required by implementation comments for private GitHub repositories |
| `GITHUB_REPO` | Default `eirepolitic/autodoc`; used by relative `github_path` locators |
| `GITHUB_REF` | Default `main`; used by relative `github_path` locators |

The automatic workflow sets `GITHUB_TOKEN` from `AUTODOC_GITHUB_TOKEN || GITHUB_TOKEN`, and explicitly sets the default repository/ref to `eirepolitic/autodoc` / `main`.

Only credential names are documented. Token values must never be stored in configs or documentation.

## Configuration Selection

The script expects to run from the repository root and requires:

```text
doc_configs/
```

Without `--project`, it scans:

```text
doc_configs/*/*.json
```

With `--project`, it scans:

```text
doc_configs/<project>/*.json
```

`should_skip_cfg()` excludes:

- filenames beginning with `_`;
- filenames ending `.enriched.json`;
- non-`.json` files.

`--doc-key` then filters selected paths by file stem.

This means `_index.json` and enriched outputs are not treated as base configs by the enrichment scanner.

## Per-Configuration Processing

`enrich_config()`:

1. reads the base JSON as UTF-8;
2. resolves `project` from `cfg.project` or parent-directory name;
3. resolves `doc_key` from `cfg.doc_key` or base filename stem;
4. chooses output `<doc_key>.enriched.json` beside the base config;
5. skips the entire config when that output exists and `--overwrite` is false;
6. requires `assets` to be a list;
7. resolves/copies each asset;
8. adds top-level `_enrichment` metadata;
9. replaces the copied config's `assets` with enriched asset objects;
10. writes formatted UTF-8 JSON with `ensure_ascii=False`.

Output path:

```text
doc_configs/<project>/<doc_key>.enriched.json
```

## Supported Source Modes

Current `resolve_asset()` recognizes exactly:

```text
pasted
github_path
github_url
```

Any other `source` value produces a captured per-asset error:

```text
Unsupported asset source '<value>'. Expected: pasted | github_path | github_url
```

## `pasted`

Required source field:

```text
asset.content
```

Empty string or null content is treated as an asset-resolution failure.

Successful metadata:

```json
{
  "method": "pasted",
  "binary_base64": false
}
```

The original content becomes `resolved_content`, and text lines are also persisted in `resolved_content_lines`.

## `github_path`

`locator` is required.

Two locator forms are supported.

### Explicit repository/ref/path

Pattern:

```text
<owner>/<repo>@<ref>:<path>
```

This form overrides `GITHUB_REPO` and `GITHUB_REF`.

### Relative repository path

Any locator not matching the explicit form is treated as a path inside:

```text
GITHUB_REPO@GITHUB_REF
```

The default repository string must contain `/`; otherwise parsing raises an error.

Resolution uses the GitHub Contents API rather than raw HTTP file retrieval.

Successful metadata includes GitHub response/path information plus:

```text
method = github_contents_api
owner
repo
ref
```

## `github_url`

`locator` is required.

### Recognized GitHub URL forms

Current parser recognizes:

```text
https://github.com/<owner>/<repo>/blob/<ref>/<path>
https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<path>
```

Recognized URLs are converted into owner/repository/ref/path components and fetched through the GitHub Contents API.

Successful metadata includes:

```text
method = github_contents_api_from_url
owner
repo
ref
```

### Other URLs

If a `github_url` locator does not match either recognized GitHub pattern, current code falls back to generic HTTP GET.

Therefore `source: github_url` is not currently a GitHub-host allowlist. It can resolve a non-GitHub HTTP/HTTPS URL if `requests.get()` can retrieve it successfully.

Successful generic HTTP metadata includes:

```text
status
final_url
content_type
binary_base64
method = http_get
```

This behavior is current executable source and should not be narrowed in documentation to “GitHub URLs only.”

## GitHub Contents API Retrieval

`fetch_github_contents()` constructs:

```text
https://api.github.com/repos/<owner>/<repo>/contents/<path>?ref=<ref>
```

Request behavior:

- timeout: `60` seconds;
- headers include `Accept: application/vnd.github+json`;
- `User-Agent: autodoc-enricher`;
- `Authorization: Bearer <GITHUB_TOKEN>` only when a token is available.

The response must be a file response with non-empty base64 `content` and `encoding == "base64"`.

If GitHub returns a list, the requested path is treated as a directory and resolution fails for that asset.

The implementation strips newlines from the API's base64 wrapper before decoding, but preserves decoded file-content newlines.

## Generic HTTP Retrieval

`fetch_http_bytes()` uses:

```text
requests.get(url, timeout=60)
```

with `User-Agent: autodoc-enricher`.

If the URL string contains `api.github.com` and `GITHUB_TOKEN` exists, GitHub API headers including the Bearer token are added. Other generic HTTP URLs do not receive that GitHub authorization header through this function.

HTTP status errors are raised through `raise_for_status()` and then captured by the per-asset error boundary in `resolve_asset()`.

Current code records the final response URL and content type in enriched metadata.

## Text and Binary Handling

`is_probably_binary_bytes()` classifies content as binary when either:

- a null byte is present; or
- fewer than 75% of the first 2,000 bytes are ASCII-printable or tab/newline/carriage-return bytes.

### Text

Text is decoded as UTF-8 with:

```text
errors="replace"
```

Successful text assets store both:

```text
resolved_content
resolved_content_lines
```

`resolved_content_lines` uses `splitlines(keepends=True)`, so joining the lines reproduces the stored text including line endings.

### Binary

Binary content is base64 encoded as ASCII and stored in:

```text
resolved_content
```

with:

```text
resolved_meta.binary_base64 = true
resolved_content_lines = null
```

This is a heuristic classification, not MIME-based validation.

## Enriched Asset Contract

Every dictionary asset begins with copied base fields and receives/updates:

```text
resolved_content
resolved_content_lines
resolved_meta
resolved_ok
resolved_error
resolved_at
```

`resolved_at` is assigned for every resolution attempt.

### Success

On success:

```text
resolved_ok = true
resolved_error = null
```

and resolution-specific metadata/content are populated.

### Resolution failure

Exceptions inside `resolve_asset()` are captured into the asset rather than propagated:

```text
resolved_ok = false
resolved_error = <exception text>
resolved_content = null
resolved_content_lines = null
```

If no earlier metadata exists:

```json
{
  "method": "error"
}
```

### Non-object asset

If an item in `assets` is not a JSON object, the script creates a structured failed asset with null base fields and:

```text
resolved_error = Asset is not an object
resolved_meta.method = error
```

The rest of the configuration continues processing.

## Top-Level `_enrichment`

Current output adds:

| Field | Current value/source |
| --- | --- |
| `enriched_at` | UTC ISO timestamp |
| `enrichment_version` | `1.1` |
| `source_config_path` | processed base-config path with `/` separators |
| `github_repo_default` | effective `GITHUB_REPO` |
| `github_ref_default` | effective `GITHUB_REF` |
| `project` | config project or directory fallback |
| `doc_key` | config doc key or filename fallback |

Historical enriched files can contain older runtime/default values and should not override current source.

## `--overwrite`

Without `--overwrite`, an existing `<doc_key>.enriched.json` causes the entire selected config to be skipped before assets are examined.

The automatic pipeline always calls enrichment with:

```text
--overwrite
```

so a changed base config gets a newly generated enriched output.

## `--only-missing`

For each base asset object, when `--only-missing` is enabled and that asset already has a non-null `resolved_content`, the asset is copied unchanged instead of re-resolved.

This check is applied to the asset object read from the selected input/base config. It does not load and merge a previously existing enriched output as the source of missing-state decisions.

The manual workflow exposes this flag; the automatic pipeline does not use it.

## Multi-Config Error Behavior

The main loop processes sorted selected configurations independently.

A configuration-level exception such as invalid JSON or `assets` not being a list:

- increments `failed`;
- writes `FAIL <path>: <error>` to stderr;
- continues to later selected configs.

At completion it prints counts:

```text
wrote=<n> skipped=<n> failed=<n>
```

and returns exit code `1` when `failed > 0`.

A successful configuration can therefore coexist with another failed configuration in one broad manual run.

## Automatic Workflow Integration

`autodoc_pipeline.yml` invokes:

```text
python process/enrich_configs.py --project <project> --doc-key <doc_key> --overwrite
```

for each changed base config before extraction/rendering.

Because the automatic shell uses `set -euo pipefail`, a configuration-level enrichment process exit code `1` stops that automatic processing step before extraction for that run.

Per-asset failures that are captured in enriched JSON do not by themselves cause enrichment process exit code `1`.

## Manual Workflow

Workflow:

```text
.github/workflows/enrich_configs.yml
Enrich AutoDoc Configs (Manual)
```

Inputs:

| Input | Required | Default |
| --- | --- | --- |
| `project` | no | blank = all projects |
| `doc_key` | no | blank = all docs in selected scope |
| `overwrite` | yes | `false` |
| `only_missing` | yes | `false` |

Concurrency:

```text
enrich-autodoc-configs
cancel-in-progress: false
```

Permissions:

```text
contents: write
```

The manual workflow installs `requirements.txt`, runs the enrichment script, stages `doc_configs/**.enriched.json`, commits changed outputs, and pushes.

## External Hosts and Trust Boundaries

Verified external host behavior includes:

- `api.github.com` for GitHub Contents API;
- `github.com` / `raw.githubusercontent.com` as recognized locator forms that are converted to Contents API calls;
- arbitrary reachable HTTP/HTTPS hosts when a non-recognized `github_url` locator falls through to generic `requests.get()`.

Configured source location is therefore a trust boundary. A repository configuration can influence what the Actions runner retrieves and persists.

## Security and Privacy

Do not put credentials, private tokens, signed secret URLs, passwords, private keys, personal data, or confidential content into asset locators or pasted content.

Important persistence behavior:

- resolved source content is written into repository JSON;
- generic HTTP metadata records `final_url`;
- GitHub metadata records API/source provenance;
- error messages are persisted in `resolved_error`.

A locator containing a sensitive query parameter could therefore cause sensitive material to be persisted through source fields or resolution metadata. Use non-secret source references only.

A source being technically retrievable does not make it appropriate to copy into a public or shared repository or later send to OpenAI.

## Failure Modes and Recovery

### Base config invalid JSON

Configuration fails; repair the base JSON and rerun enrichment.

### `assets` is not a list

Configuration fails with `cfg.assets must be a list`; fix the base contract.

### Pasted content empty

Only that asset is marked failed. Supply legitimate content in the base config and rerun with overwrite as appropriate.

### GitHub locator points to directory

Only that asset is marked failed. Change the locator to a file path.

### GitHub/HTTP status failure or timeout

Only that asset is marked failed through `resolved_error`. Verify source availability/access without exposing credentials, then rerun.

### Existing enriched file unexpectedly skipped

Use the manual workflow's `overwrite=true` only when regeneration is intended. The automatic path already uses overwrite.

### Some assets succeed and others fail

Inspect each asset's `resolved_ok` / `resolved_error`. Do not assume the enriched file is fully usable merely because it exists.

### Registry/index issue

Enrichment does not own `_index.json`. Use the index rebuild path rather than editing enrichment output to repair registry state.

## Known Limitations

- `github_url` falls back to generic HTTP GET rather than enforcing a GitHub-only host policy.
- Binary detection is heuristic.
- UTF-8 decoding replaces invalid sequences rather than failing.
- No content-size limit is explicitly enforced in `enrich_configs.py`; practical limits come from source services, memory, Actions, or GitHub repository constraints.
- Per-asset resolution failure is persisted and tolerated, so downstream stages must distinguish resolved from failed assets.
- `--only-missing` operates on selected input asset objects rather than merging a previous enriched file.

## Next Safe Development Action

Publish this enrichment component through the standard documentation validation/merge/Pages gate. Then document the section-fact extraction stage and its persisted CSV contract on a fresh branch from updated `main`.

Do not change resolver host policy, token handling, timeouts, binary heuristics, or persistence behavior without explicit architecture/security approval.

## Related Documents

- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc/main` `process/enrich_configs.py` SHA `70442976f979592c1f35b2acc1977520ed7471ee`; current `enrich_configs.yml`, `autodoc_pipeline.yml`, `requirements.txt`; current config/enriched schema documentation.
- Verified by: High Director
- Verification scope: CLI/config selection, resolver modes/parsers, HTTP/GitHub retrieval, token-header behavior, text/binary handling, enriched fields, overwrite/only-missing semantics, exit/error behavior, automatic/manual workflow integration, external hosts, and security boundary.
- Not verified: live external source availability, private-repository token scope, or practical maximum asset size.
