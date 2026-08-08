---
title: Recover AutoDoc generated and reviewed artifacts
summary: Use this runbook to identify the last valid AutoDoc artifact and safely rerun only the required downstream stages through generated, reviewed, and published states.
section: runbooks
doc_type: runbook
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
order: 135
permalink: /projects/runbooks/recover-autodoc-artifacts/
repository: autodoc
system: AutoDoc
tags:
  - autodoc
  - recovery
  - artifacts
  - github-actions
---

# Recover AutoDoc generated and reviewed artifacts

## Purpose

Use this runbook when an AutoDoc document is missing, stale, partially regenerated, stuck between raw and reviewed state, or has a registry/publication inconsistency.

The objective is to identify the **last valid persisted artifact**, fix the actual upstream cause, and rerun only the smallest necessary downstream stage.

This runbook does not authorize credential rotation, model/prompt changes, publication-architecture changes, or destructive history rewriting.

## Status and Last Verification

- Status: verified from current repository/workflow source.
- Last verified: `2026-08-07`.
- Verified against: current `autodoc` workflows/Python, current generated/reviewed artifact tree, current AutoDoc Appsmith documentation, and current website-publication documentation.

## Use This Runbook When

Use it when:

- a base config exists but enrichment/extraction/rendering did not finish;
- an enriched config contains failed assets;
- a summary CSV is missing or stale;
- raw Markdown is missing or has `_TBD` sections;
- reviewed Markdown is missing or stale;
- Appsmith shows a document/index mismatch;
- publication cannot find a reviewed file;
- a manual recovery workflow is needed after an automatic-pipeline failure.

## Do Not Use This Runbook When

Do not use it to:

- rotate `GITHUB_TOKEN`, `AUTODOC_GITHUB_TOKEN`, `OPENAI_API_KEY`, `WEBSITE_PAT`, or Appsmith PATs;
- change OpenAI models/prompts/retry policy;
- change workflow permissions or publication architecture;
- repair a security incident involving exposed credentials;
- treat LLM `reviewed` state as human/factual approval.

Those require explicit security/architecture decisions.

## Artifact Lifecycle

For one document:

```text
doc_configs/<project>/<doc_key>.json
    base configuration
        |
        v
doc_configs/<project>/<doc_key>.enriched.json
    resolved source content + per-asset status
        |
        v
doc_configs/<project>/summaries/<doc_key>.csv
    section_title,extracted_facts
        |
        v
docs/<project>/<type>/<doc_key>.md
    generated/raw Markdown
        |
        v
docs/<project>/<type>/reviewed/<doc_key>.md
    LLM-reviewed/concision Markdown
        |
        v
optional website copy
projects/<dest_type>/<doc_key>.md in eirepolitic.github.io
```

Separate registry:

```text
doc_configs/<project>/_index.json
```

`_index.json` is not an upstream content artifact. It is a project registry that can be deterministically rebuilt from base configs.

## Artifact Authority

For recovery, use this order:

1. base config is authority for project/type/title/context/assets;
2. enriched JSON is disposable/rebuildable derived state;
3. summary CSV is disposable/rebuildable derived state;
4. generated/raw Markdown is disposable/rebuildable derived state;
5. reviewed Markdown is separately regenerable from raw Markdown;
6. website Markdown is a publication copy, not source authority;
7. `_index.json` is rebuildable registry state.

Do not repair an upstream contract by manually editing a downstream generated artifact unless the intended task is explicitly a document-content edit.

## Prerequisites and Access

You need:

- access to GitHub Actions for `autodoc`;
- read access to relevant repository files;
- write/dispatch rights where manual workflows require them;
- the non-secret values `project`, `doc_key`, and where needed `type`;
- current workflow/run IDs or failure messages.

Do not copy secret values into issues, logs, screenshots, or documentation.

## Source of Truth

Current recovery workflows:

```text
.github/workflows/enrich_configs.yml
.github/workflows/section_extract.yml
.github/workflows/render_docs.yml
.github/workflows/review_doc.yml
.github/workflows/index_rebuilder.yaml
```

Automatic orchestration:

```text
.github/workflows/autodoc_pipeline.yml
```

Stage implementations:

```text
process/enrich_configs.py
process/section_extract.py
process/render_sections.py
process/review_doc.py
process/update_index.py
```

## Safety Checks

Before rerunning anything:

1. Verify the exact `project`, `doc_key`, and current `type` from the base config.
2. Check the latest automatic/manual workflow result.
3. Identify which persisted artifacts currently exist.
4. Inspect the last existing artifact for obvious invalid/stale state.
5. Confirm no overlapping recovery workflow is already changing the same document.
6. Do not use publication as a test for an upstream generation failure.
7. Do not expose credentials while inspecting errors.

## Procedure

### 1. Inspect the base config

Open:

```text
doc_configs/<project>/<doc_key>.json
```

Confirm:

- valid JSON;
- correct `project`;
- non-empty `type`;
- correct `doc_key`;
- `assets` is an array;
- source locators/content are intentionally configured.

If the base config is wrong, fix it first. A normal base-config commit can trigger the automatic enrich -> extract -> render sequence.

### 2. Check enriched state

Inspect:

```text
doc_configs/<project>/<doc_key>.enriched.json
```

For every asset, check:

```text
resolved_ok
resolved_error
resolved_content
resolved_meta
```

If the enriched file is missing, stale, or contains source failures that must be corrected, use **Enrich AutoDoc Configs (Manual)**.

Recommended recovery inputs for one document:

```text
project = <project>
doc_key = <doc_key>
overwrite = true
only_missing = false
```

Use `only_missing=true` only when its exact current semantics are desired. It operates on selected input asset objects; it does not merge an older enriched output.

Success check:

- workflow succeeds;
- target enriched JSON exists;
- required assets show `resolved_ok: true`.

### 3. Check extraction state

Inspect:

```text
doc_configs/<project>/summaries/<doc_key>.csv
```

Expected header:

```text
section_title,extracted_facts
```

A previous CSV can remain after a later failed extraction attempt. Existence alone is not proof of latest-run success.

If extraction must be regenerated, dispatch **Extract Section Facts** with:

```text
project = <project>
doc_key = <doc_key>
```

Success check:

- workflow succeeds;
- CSV modification belongs to the successful run;
- expected template H2 section titles are represented.

### 4. Check generated/raw Markdown

Inspect:

```text
docs/<project>/<type>/<doc_key>.md
```

If it is missing/stale, or upstream extraction has been regenerated, dispatch **Render Docs from Section Summaries**:

```text
project = <project>
doc_key = <doc_key>
```

Success check:

- render workflow succeeds;
- raw Markdown exists at the expected type path;
- front matter/title are present;
- sections with no facts may legitimately contain:

```text
_TBD (no extracted facts provided for this section)._
```

A `_TBD` marker is not fixed by rerunning rendering alone unless the summary facts changed. Fix/rerun extraction or its upstream source when facts are genuinely missing.

### 5. Check reviewed Markdown

Inspect:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

If raw Markdown changed after the reviewed file was created, or reviewed output is missing/stale, dispatch **Review Documentation** with:

```text
project = <project>
type = <type>
doc_key = <doc_key>
overwrite = true
```

Success check:

- review workflow succeeds;
- reviewed file exists at the exact path;
- content has been inspected where accuracy/format preservation matters.

Important: `reviewed` means LLM concision output, not human approval or factual verification.

### 6. Repair `_index.json` separately when required

If Appsmith selectors/registry data are stale while base configs are correct, dispatch:

```text
Rebuild _index.json (Manual)
```

with:

```text
project = <project>
```

Success check:

- workflow succeeds;
- `doc_configs/<project>/_index.json` is regenerated from base configs;
- expected `doc_key`, `title`, and `type` are present.

Do not manually reconstruct index timestamps unless there is no executable recovery path. Current backend derives registry freshness from Git history.

### 7. Publish only after reviewed state is intentionally ready

Current publication requires:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

The Appsmith publication path can dispatch `publish_to_website.yml`, which directly copies/commits/pushes the reviewed file into the website repository.

Do not use publication to diagnose enrichment/extraction/render/review issues.

A successful AutoDoc publication workflow is not equivalent to current documentation governance. Website validation/Pages health must be assessed separately.

## Smallest-Safe-Rerun Matrix

| Last known-good state | Smallest normal next action |
| --- | --- |
| Base config only | Enrichment |
| Enriched config valid | Extraction |
| Summary CSV valid/current | Render |
| Raw Markdown valid/current | Review |
| Reviewed Markdown valid/current | Publication, only if intended |
| Base configs valid, index stale | Index rebuild only |

If an upstream artifact changes, all downstream artifacts should be treated as potentially stale until regenerated or deliberately verified.

## Validation and Success Criteria

Recovery is complete when:

- the required stage workflow succeeded;
- the expected target artifact exists at the exact path;
- the artifact corresponds to the current upstream state;
- no known upstream failure remains hidden by a downstream rerun;
- registry state is correct if Appsmith discovery depends on it;
- reviewed state is not mislabeled as human/factual approval;
- publication, if performed, has independent website/Pages verification as required.

Record non-secret evidence such as workflow name, run ID, commit SHA, affected path, and result.

## Rollback or Recovery

Most derived artifacts can be regenerated rather than rolled back manually.

If a new derived artifact is bad but the prior repository version was valid:

1. identify the bad stage and root cause;
2. correct the upstream input/source/configuration;
3. rerun the smallest affected stage and downstream stages;
4. prefer normal forward correction over rewriting repository history.

Do not revert credential/security changes through this runbook.

## Failure Modes and Escalation

| Failure | Safe response | Evidence |
| --- | --- | --- |
| Invalid base config | Fix base contract first | path, parser/error text |
| Asset resolution failed | Correct source/access then rerun enrichment | `resolved_error`, workflow run |
| Extraction API failure | Preserve prior CSV; resolve API/input issue then rerun extraction | run ID, non-secret error |
| Render API failure | Preserve CSV/raw history; rerun render after cause fixed | run ID |
| `_TBD` section | Determine whether facts are actually missing upstream | CSV row, source config |
| Review API failure | Keep raw Markdown; rerun review only | run ID |
| Reviewed file stale | Regenerate review with overwrite=true | raw/reviewed commits |
| Index stale | Run index rebuild | base config + rebuilt index |
| Publication missing source | Regenerate/verify reviewed artifact | reviewed path, publication run |
| Credential/auth failure | Stop; use approved security/access handling | redacted error only |

## Security Guidance

- Never paste `OPENAI_API_KEY`, `GITHUB_TOKEN`, `AUTODOC_GITHUB_TOKEN`, `WEBSITE_PAT`, or Appsmith PAT values into documentation or retained logs.
- Treat enrichment locators/content as potentially persistent repository data.
- Treat generated and reviewed Markdown as potentially publishable data.
- Stop routine recovery if unexpected credential exposure, private data, or unauthorized repository access is discovered.

## Known Limitations

- Manual workflows can commit directly to `autodoc`; they are operational recovery paths, not the website documentation-governance process.
- Extraction can leave an older CSV after a failed newer attempt.
- Review with overwrite=false can skip based only on target existence.
- Review output is not structurally/factually validated.
- The automatic pipeline stops at render; review/publication remain separate.
- Current publication path directly pushes to the website and does not itself enforce PR/validation/Pages governance.

## Follow-up Work

After recovery:

- document any new reproducible failure mode;
- fix systemic implementation issues in a separate approved development change;
- update the persistent AutoDoc documentation workstream if recovery evidence changes current understanding.

## Next Safe Action

After this runbook is published, classify the historical `docs/eirepolitic/pipeline/*` generated/reviewed artifacts without treating them as current Irish Politics implementation authority.

## Related Documents

- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)
- [AutoDoc section-fact extraction](/projects/systems/autodoc-section-fact-extraction/)
- [AutoDoc template/Markdown rendering](/projects/systems/autodoc-template-markdown-rendering/)
- [AutoDoc review/concision](/projects/systems/autodoc-review-concision/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)
- [AutoDoc configuration and project index](/projects/data/autodoc-configuration-and-project-index/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc` stage implementations/workflows; current `docs/` generated/reviewed tree; current AutoDoc Appsmith/config/publication documentation.
- Verified by: High Director
- Verification scope: lifecycle paths, authority/rebuildability, smallest-stage rerun logic, manual workflow inputs, success checks, registry recovery, reviewed/publication boundaries, and security stop conditions.
- Known unverified steps: no live recovery workflow was intentionally dispatched solely to test this documentation.
