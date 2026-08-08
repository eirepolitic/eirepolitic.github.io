---
title: Historical AutoDoc-generated Irish Politics pipeline artifacts
summary: Archive index for the six raw/reviewed AutoDoc pipeline-document pairs under autodoc/docs/eirepolitic/pipeline, preserving provenance while directing current implementation questions to reconciled Irish Politics documentation.
section: archive
doc_type: reference
status: archived
created: 2026-08-07
updated: 2026-08-07
archived_date: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 136
permalink: /projects/archive/autodoc-eirepolitic-generated-artifacts/
repository: autodoc
system: AutoDoc
archive_reason: AutoDoc-generated pipeline documents are retained as historical generated/reviewed evidence and are not authoritative for current Irish Politics implementation.
superseded_by: /projects/repositories/eirepolitic-data-pipeline/
tags:
  - autodoc
  - archive
  - eirepolitic
  - generated-documentation
---

# Historical AutoDoc-generated Irish Politics pipeline artifacts

> This page preserves AutoDoc artifact provenance. The generated prose under `autodoc/docs/eirepolitic/pipeline/` must not be treated as current Irish Politics implementation authority without verification against current source.

## Archive Summary

The current `autodoc` repository retains six historical Irish Politics pipeline documentation families under:

```text
docs/eirepolitic/pipeline/
```

Every family currently has:

1. a generated/raw Markdown file; and
2. a corresponding LLM-reviewed/concision file under `reviewed/`.

These files are valuable evidence of what AutoDoc generated at the time. They are **derived documentation artifacts**, not canonical implementation source for the current `eirepolitic-data-pipeline` repository.

Current Irish Politics archive/lineage pages in `eirepolitic.github.io` have already reconciled the relevant implementation status against current repository source. Use those pages and current source for present-day claims rather than copying statements from these historical AutoDoc outputs.

## Archive Status

- Archived on: `2026-08-07` for AutoDoc documentation classification purposes.
- Archive reason: generated/reviewed snapshots can preserve older architecture, workflow, path, model, and operating assumptions.
- Current implementation source: [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/).
- Current recommendation: use AutoDoc artifacts only for historical provenance/lineage; verify current behavior from current implementation and reconciled archive pages.

## Artifact Inventory

Current `autodoc/main` contains these raw/reviewed pairs:

| Document | Base-config registry timestamp | Raw artifact | Raw bytes | Reviewed artifact | Reviewed bytes | Current reconciled archive record |
| --- | --- | --- | ---: | --- | ---: | --- |
| Constituency Images Indexer | `2026-02-27T12:38:56-08:00` | `docs/eirepolitic/pipeline/constituency_images_indexer.md` | 16,381 | `docs/eirepolitic/pipeline/reviewed/constituency_images_indexer.md` | 8,679 | `_docs/archive/constituency-images-indexer.md` |
| Debate Issue Classifier | `2026-02-27T13:10:54-08:00` | `docs/eirepolitic/pipeline/debate_issue_classifier.md` | 19,559 | `docs/eirepolitic/pipeline/reviewed/debate_issue_classifier.md` | 11,097 | `_docs/archive/debate-issue-classifier.md` |
| LLM Column Creator | `2026-02-27T13:17:45-08:00` | `docs/eirepolitic/pipeline/llm_column_creator.md` | 20,663 | `docs/eirepolitic/pipeline/reviewed/llm_column_creator.md` | 10,798 | `_docs/archive/llm-column-creator.md` |
| Member Images Pipeline | `2026-02-27T13:52:01-08:00` | `docs/eirepolitic/pipeline/member_images_pipeline.md` | 16,355 | `docs/eirepolitic/pipeline/reviewed/member_images_pipeline.md` | 8,797 | `_docs/archive/member-images-pipeline.md` |
| Member Summaries Table | `2026-02-27T14:22:08-08:00` | `docs/eirepolitic/pipeline/member_summaries_table.md` | 21,022 | `docs/eirepolitic/pipeline/reviewed/member_summaries_table.md` | 11,207 | `_docs/archive/member-summaries-table.md` |
| S3 Column Deleter | `2026-02-26T17:42:40-08:00` | `docs/eirepolitic/pipeline/s3_column_deleter.md` | 12,395 | `docs/eirepolitic/pipeline/reviewed/s3_column_deleter.md` | 5,964 | `_docs/archive/s3-column-deleter.md` |

The registry timestamp is current `doc_configs/eirepolitic/_index.json.updated_at`, which the current index builder derives from the base config's Git commit timestamp. It is **not** asserted here as the exact raw/reviewed artifact generation time.

## Historical Artifact Family

For each listed document the retained AutoDoc lifecycle is:

```text
doc_configs/eirepolitic/<doc_key>.json
    -> <doc_key>.enriched.json
    -> summaries/<doc_key>.csv
    -> docs/eirepolitic/pipeline/<doc_key>.md
    -> docs/eirepolitic/pipeline/reviewed/<doc_key>.md
```

The current repository also retains the base configs, enriched configs, summary CSVs, and project `_index.json` for all six document keys.

This establishes their provenance as complete AutoDoc documentation artifact families rather than hand-authored current system pages.

## Raw vs Reviewed Interpretation

The raw path represents renderer output.

The `reviewed/` path represents the separate AutoDoc LLM review/concision state. Current AutoDoc review semantics do not constitute factual verification or human approval.

For the inspected Constituency Images Indexer pair, raw and reviewed files retain the same title/front matter and `Last generated` value while the reviewed copy is substantially shorter, consistent with AutoDoc's concision lifecycle.

Do not infer that every historical reviewed file satisfies current review code, model settings, formatting, or publication governance merely because the path contains `reviewed`.

## Why These Artifacts Are Historical Evidence

The generated prose can describe paths/workflows/systems that have since been:

- superseded;
- generalized into a newer framework;
- retained only for compatibility or lineage;
- still executable but no longer canonical production architecture;
- consumed by newer compatibility/enrichment layers without being fully retired.

The six current dedicated archive pages in the documentation site make these distinctions from current source. That reconciliation is stronger evidence than the generated AutoDoc prose itself.

## Current Reconciliation Boundary

Examples already established by current archive/repository documentation include:

- Constituency Images Indexer: historical standalone indexer; legacy output remains an input to a newer Oireachtas enrichment/compatibility path, so full retirement is not established.
- Debate Issue Classifier: historical classifier documentation; newer Oireachtas enrichment consumes existing classified output rather than replacing the classification function.
- LLM Column Creator: superseded predecessor concept; current equivalent capability belongs to the Reusable LLM Task Runner Framework rather than a current component with the old name.

The other dedicated archive pages perform the corresponding current-source reconciliation for Member Images Pipeline, Member Summaries Table, and S3 Column Deleter. This AutoDoc page intentionally does not duplicate their implementation details.

## Source of Truth

### Historical AutoDoc artifact provenance

Use current `autodoc/main`:

```text
doc_configs/eirepolitic/
docs/eirepolitic/pipeline/
docs/eirepolitic/pipeline/reviewed/
```

### Current Irish Politics implementation

Use current `eirepolitic-data-pipeline` source plus:

- [eirepolitic-data-pipeline repository](/projects/repositories/eirepolitic-data-pipeline/);
- the dedicated `_docs/archive/*.md` lineage pages named in the inventory.

If historical AutoDoc prose conflicts with current executable source or a source-verified archive reconciliation, current source/reconciliation wins.

## Why It Was Archived

The files were generated by an earlier AutoDoc documentation lifecycle and persist in the AutoDoc repository. Their role is now provenance, historical comparison, and lineage—not current operational guidance for Irish Politics pipelines.

Moving or deleting the source artifacts is not required for this classification. Their repository history can remain useful, and some underlying legacy implementations/outputs may still be transitional dependencies even when the generated documentation page is historical.

## Successor or Replacement

The appropriate successor is not one single AutoDoc page.

For present implementation questions:

1. start with [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/);
2. use the corresponding dedicated archive/lineage page for legacy-to-current mapping;
3. verify any operational claim against the actual current workflow/Python/configuration.

Do not regenerate these historical pages merely to make them look current unless the intent is explicitly to create a new current AutoDoc documentation artifact from verified current source.

## Security Considerations

Historical generated artifacts can contain technical paths, service names, environment-variable names, and derived source content. Do not add secret values or personal/private data while preserving or comparing them.

AutoDoc enrichment/review trust boundaries documented elsewhere still apply to any future regeneration.

## Known Limitations

- This classification does not prove the exact generation/review run IDs for all six artifacts.
- Registry timestamps date base-config Git state, not necessarily artifact generation.
- Historical prose can contain correct facts alongside obsolete assumptions.
- `reviewed/` means historical AutoDoc review state, not present-day human/factual approval.
- Underlying legacy code/workflows can remain checked in or partially depended upon even though these documentation artifacts are archived.

## Next Safe Action

When a historical AutoDoc claim is needed, follow its `doc_key` to the current dedicated archive page and current `eirepolitic-data-pipeline` source before using that claim operationally.

For the AutoDoc documentation workstream, the next action is the final current-`main` cross-page consistency review and workstream closeout.

## Related Documents

- [AutoDoc repository](/projects/repositories/autodoc/)
- [AutoDoc artifact recovery](/projects/runbooks/recover-autodoc-artifacts/)
- [AutoDoc review/concision](/projects/systems/autodoc-review-concision/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc/main` `docs/eirepolitic/pipeline/` tree; current raw/reviewed file sizes; current `doc_configs/eirepolitic/` tree and `_index.json`; inspected raw/reviewed Constituency Images Indexer pair; current dedicated archive/lineage pages and `eirepolitic-data-pipeline` repository page.
- Verified by: High Director
- Verification scope: artifact inventory, raw/reviewed pairing, lifecycle provenance, registry timestamps, authority classification, current reconciliation boundary, and successor guidance.
- Unverified areas: exact historical workflow run IDs/model versions for every generated/reviewed pair.
