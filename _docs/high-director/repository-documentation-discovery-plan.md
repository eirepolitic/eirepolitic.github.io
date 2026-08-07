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

## Initiative status

**Complete.**

All six repositories supplied by the system owner were scanned, their real technical documentation targets were isolated, cross-repository duplicates were reconciled, and the owner-wide target catalogue was published successfully.

Final consolidation milestone:

```text
PR: #60
Validation: success
Pages deployment: #166
Pages conclusion: success
```

This closure update is administrative only. It changes no implementation, architecture, security, cost, or access control.

## Authoritative repository scope

```text
eirepolitic.github.io
eirepolitic-data-pipeline
bb-comp-prices
degenerate_investigator
Overlord
autodoc
```

## Completed scan record

| Repository | Result |
|---|---|
| `eirepolitic.github.io` | Complete — PR #54 / Pages #160 |
| `eirepolitic-data-pipeline` | Complete — PR #55 / Pages #161 |
| `bb-comp-prices` | Complete — PR #56 / Pages #162 |
| `degenerate_investigator` | Complete — PR #57 / Pages #163 |
| `Overlord` | Complete — PR #58 / Pages #164 |
| `autodoc` | Complete — PR #59 / Pages #165 |
| Owner-wide consolidation | Complete — PR #60 / Pages #166 |

## Canonical discovery outputs

- `_docs/high-director/documentation-target-catalogue.md` — canonical owner-wide deduplicated catalogue, priorities, documentation waves, external-source gaps, and next recommended initiative.
- `_docs/high-director/repository-scan-bb-comp-prices.md` — detailed `bb-comp-prices` target/evidence inventory.
- `_docs/high-director/repository-scan-degenerate-investigator.md` — detailed `degenerate_investigator` target/evidence inventory.
- `_docs/high-director/repository-scan-overlord.md` — detailed `Overlord` target/evidence inventory.
- `_docs/high-director/repository-scan-autodoc.md` — detailed `autodoc` target/evidence inventory.
- this page — discovery history, completion state, and continuation procedure.

## Consolidated result

The catalogue isolates **56 documentation targets/initiatives**:

```text
P0 foundational: 16
P1 active operational: 21
P2 supporting: 9
P3 historical/status-verification: 10
```

These are grouped documentation initiatives, not raw file counts. Related source files are intentionally grouped when one canonical page/set should own the facts.

Existing full documentation for the documentation site and High Director is treated as maintenance-only and is not counted as new build work.

## Documentation waves

### Wave 0 — complete / maintenance only

- `eirepolitic.github.io` documentation site/repository.
- High Director and configured integrations.

### Wave 1 — foundations and control boundaries

Begin with:

1. Irish Politics Analytics umbrella architecture.
2. `eirepolitic-data-pipeline` repository.
3. Unified Oireachtas Data Platform.
4. Oireachtas data-product catalogue.
5. Oireachtas refresh/validation orchestration.
6. Oireachtas write policies/downstream contracts.
7. AutoDoc architecture/Appsmith/config/pipeline/security/publication boundaries.
8. `bb-comp-prices` repository/platform/storage/orchestration foundation.
9. `degenerate_investigator` repository/system/storage/orchestration foundation.

### Wave 2 — active operational components

Document active political-data media/member/LLM, competitor-pricing, UFC analytics/model/reporting, and AutoDoc generation/review stages.

### Wave 3 — supporting components

Document diagnostics, validation, developer/configuration references, maintenance utilities, manual recovery/publication helpers, and Overlord.

### Wave 4 — archival reconciliation

Resolve predecessor/successor status for historical political-data pipelines, experiments, superseded probes, and generated historical artifacts.

## Important cross-repository conclusions

- `eirepolitic.github.io` is the persistent technical-documentation source of truth.
- `eirepolitic-data-pipeline` contains current/legacy implementation lineage for the political-data archive records.
- `bb-comp-prices` is a separate competitor-pricing platform despite sharing AWS/S3 patterns.
- `degenerate_investigator` is a separate UFC analytics/ML platform and explicitly excludes staking/bookmaker-targeted recommendation logic.
- `Overlord` is currently a lightweight Markdown task-record/template repository with no verified automation/integration relationship to High Director or the other repositories.
- `autodoc` links Appsmith, GitHub, OpenAI, generated documentation, and website publication.
- AutoDoc's current direct-push website publisher differs from the newer PR/validation/Pages discipline and remains a documented future architecture/operations decision candidate.

## External-source rule

Do not request external material speculatively. Inspect repository-accessible source directly first.

Request one coherent authoritative source only when a specific future documentation initiative is blocked by a gap such as:

- current live Appsmith configuration for AutoDoc;
- live AWS/IAM/S3/Glue/Athena configuration where deployed state cannot be established from source;
- user confirmation where code/history cannot establish whether an old implementation is active, retired, or superseded.

Do not request or publish secret values.

## Future maintenance procedure

When repository scope or implementation changes:

1. inspect the changed repository/source directly;
2. update the relevant repository scan and/or target catalogue only if the documentation inventory materially changes;
3. preserve current-vs-historical distinctions and deduplication;
4. use a focused PR;
5. run documentation validation before merge;
6. confirm the matching Pages deployment after merge.

## Outstanding discovery work

None.

Future work is full documentation of catalogue targets or maintenance driven by real implementation changes.

## Next safe development action

Start **Wave 1** with the **Irish Politics Analytics umbrella architecture and `eirepolitic-data-pipeline`/Unified Oireachtas foundation**, unless the system owner chooses a different target from `_docs/high-director/documentation-target-catalogue.md`.
