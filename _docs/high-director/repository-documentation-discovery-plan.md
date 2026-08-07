---
title: Repository Documentation Discovery Initiative
summary: Persistent completion and continuation record for the owner-wide repository documentation-target discovery initiative.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 29
permalink: /projects/high-director/repository-documentation-discovery/
---

# Repository Documentation Discovery Initiative

## Purpose

Identify and isolate every real repository, system, pipeline, service, integration, workflow, data product, security boundary, operational subsystem, and historical implementation across the repositories supplied by the system owner that merits full technical documentation.

## Authoritative repository scope

```text
eirepolitic.github.io
eirepolitic-data-pipeline
bb-comp-prices
degenerate_investigator
Overlord
autodoc
```

All six repositories have been scanned.

## Current status — 2026-08-07

- `eirepolitic.github.io` scan: complete — PR #54 / Pages #160.
- `eirepolitic-data-pipeline` scan: complete — PR #55 / Pages #161.
- `bb-comp-prices` scan: complete — PR #56 / Pages #162.
- `degenerate_investigator` scan: complete — PR #57 / Pages #163.
- `Overlord` scan: complete — PR #58 / Pages #164.
- `autodoc` scan: complete — PR #59 / Pages #165.
- Owner-wide consolidation/prioritization: content complete on working branch; validation/merge/Pages gate pending.

## Canonical discovery outputs

- `_docs/high-director/documentation-target-catalogue.md` — owner-wide deduplicated catalogue, priorities, documentation waves, external-source gaps and next recommended initiative.
- `_docs/high-director/repository-scan-bb-comp-prices.md` — detailed `bb-comp-prices` evidence/target inventory.
- `_docs/high-director/repository-scan-degenerate-investigator.md` — detailed `degenerate_investigator` evidence/target inventory.
- `_docs/high-director/repository-scan-overlord.md` — detailed `Overlord` evidence/target inventory.
- `_docs/high-director/repository-scan-autodoc.md` — detailed `autodoc` evidence/target inventory.
- this page — scan history, completion state and continuation rule.

Repository 1 and repository 2 findings are summarized in the target catalogue and earlier revisions of this plan; their source implementation remains directly inspectable in their repositories.

## Consolidation result

The owner-wide catalogue currently identifies:

- **16 P0 foundational initiatives**;
- **21 P1 active operational initiatives**;
- **9 P2 supporting initiatives**;
- **10 P3 historical/status-verification initiatives**;
- existing full documentation for the documentation site and High Director, which now move to maintenance-only status.

These counts represent documentation targets/initiatives, not file counts. Related files/components are intentionally grouped where a single canonical documentation source will prevent duplication.

## Key relationships resolved

- Historical pipeline pages in `eirepolitic.github.io` and historical AutoDoc output are not independent current implementations; `eirepolitic-data-pipeline` contains their source lineage.
- `bb-comp-prices` is a distinct competitor-pricing platform despite sharing an AWS/S3 pattern with `eirepolitic-data-pipeline`.
- `degenerate_investigator` is a distinct UFC analytics/ML system.
- `Overlord` is currently only a Markdown task-record/template repository and has no verified integration with High Director or the other repositories.
- `autodoc` links Appsmith, GitHub, OpenAI and website publication; current backend source is in the repository while the live Appsmith UI remains an external verification source.
- AutoDoc's current direct website-push workflow differs from the newer PR/validation/Pages documentation discipline and is explicitly retained as a future architecture/operations decision candidate.

## Documentation waves

### Wave 0 — complete/maintenance

- `eirepolitic.github.io` documentation site/repository.
- High Director and configured integrations.

### Wave 1 — foundations and control boundaries

Start with Irish Politics Analytics umbrella architecture and the `eirepolitic-data-pipeline`/Oireachtas foundation, then AutoDoc architecture/control boundaries, then repository/platform foundations for `bb-comp-prices` and `degenerate_investigator`.

### Wave 2 — active operational components

Document active media/member/LLM, competitor-pricing, UFC analytics/model/reporting, and AutoDoc generation stages.

### Wave 3 — supporting components

Document diagnostics, validation, developer/configuration references, maintenance utilities, manual recovery workflows, publication helpers and Overlord.

### Wave 4 — archival reconciliation

Resolve predecessor/successor status for historical political-data pipelines, experiments, superseded probes and generated historical artifacts.

## External-source rule

Do not request external material speculatively. Repository-inspectable source must be inspected directly.

Likely future external gaps are limited to live configuration that repositories cannot prove, especially:

- current AutoDoc Appsmith application export/configuration;
- live AWS/IAM/S3/Glue/Athena configuration when exact deployed state is required for political-data, competitor-pricing or UFC systems;
- user status confirmation when source cannot establish whether an old pipeline/experiment is retired or active.

Request one coherent source at a time only when the relevant full-documentation initiative reaches that evidence gap.

## Publication gate

The consolidation phase is complete only when:

1. documentation validation passes;
2. the catalogue PR merges;
3. the matching GitHub Pages deployment succeeds;
4. this plan is updated once more to mark the discovery initiative closed.

## Next safe development action

Complete the catalogue validation/merge/Pages gate. Then make one small closure update marking owner-wide discovery complete.

After closure, the next full-documentation initiative should begin with the **Irish Politics Analytics umbrella architecture and `eirepolitic-data-pipeline`/Unified Oireachtas foundation**, unless the system owner chooses another target from the catalogue.
