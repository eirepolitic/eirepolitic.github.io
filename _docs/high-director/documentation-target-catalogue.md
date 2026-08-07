---
title: Owner-Wide Documentation Target Catalogue
summary: Consolidated, deduplicated catalogue of repositories, systems, pipelines, data products, integrations, workflows, security boundaries, and historical implementations identified across all six repositories.
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
order: 35
permalink: /projects/high-director/documentation-target-catalogue/
---

# Owner-Wide Documentation Target Catalogue

## Purpose

This page is the canonical discovery output for the owner-wide repository scan. It answers: **what should receive full technical documentation, what is already documented, what should be grouped together, what is historical only, and in what order should the work proceed?**

The catalogue is based on complete repository-tree scans of the six repository names supplied by the system owner plus representative implementation/configuration/workflow evidence from each repository.

## Discovery scope

```text
eirepolitic.github.io
eirepolitic-data-pipeline
bb-comp-prices
degenerate_investigator
Overlord
autodoc
```

All six repositories have been scanned.

## Priority definitions

- **P0 — foundational:** repositories/umbrella architecture, shared data platforms, trust/security boundaries, deployment/orchestration controls, and controls that can materially affect other systems.
- **P1 — active operational:** substantive active applications, pipelines, model workflows, and automations that operate on real data or external services.
- **P2 — supporting:** developer interfaces, diagnostics, validation frameworks, utilities, publication helpers, schemas/templates, or components whose role is subordinate to a larger system.
- **P3 — historical/status-verification:** retired/superseded implementations, experiments, predecessor records, and components whose current operational status is not established.

Priority is a documentation-order recommendation, not an implementation/change authorization.

## Already fully documented / maintenance only

These are real technical targets, but they already have current full documentation and should move into ordinary maintenance rather than another discovery-driven build:

| Target | Repository | Status |
|---|---|---|
| `eirepolitic.github.io` repository and documentation site | `eirepolitic.github.io` | Current full documentation exists |
| Documentation validation/search/publication subsystems | `eirepolitic.github.io` | Current full documentation exists |
| High Director agent | `eirepolitic.github.io` + external GPT/AWS/Google sources | Current full documentation exists |
| High Director GitHub/AWS/Google integrations | supporting external sources | Current full documentation exists |

## P0 — foundational documentation initiatives

### 1. Irish Politics Analytics umbrella architecture

**Repository:** cross-repository, anchored by `eirepolitic-data-pipeline` and `eirepolitic.github.io`.

**Document:** portfolio/system architecture, repository map, shared AWS/S3/data relationships, external services, ownership boundaries, successor/history map.

**Why P0:** several historical and current components belong to the same political-data ecosystem; documenting them independently first would duplicate architecture and lineage facts.

### 2. `eirepolitic-data-pipeline` repository

**Document:** repository purpose, structure, dependencies, workflow inventory, source-of-truth boundaries, runtime/configuration, deployment/update procedure, active-vs-legacy map.

**Evidence:** complete repository scan plus `configs/`, `extract/`, `process/`, `.github/workflows/`, `instagram/`, `docs/`.

### 3. Unified Oireachtas Data Platform

**Repository:** `eirepolitic-data-pipeline`.

**Document:** architecture; Oireachtas API ingestion; raw/canonical processing; table registry; dependency graph; backfill/refresh behavior; S3 paths; validation; failure/recovery; dependencies and code reference.

### 4. Oireachtas canonical data-product catalogue

**Repository:** `eirepolitic-data-pipeline`.

**Canonical evidence:** `configs/oireachtas/tables.yml`.

**Products currently represented:** houses, constituencies, parties, members, memberships, offices, sources, debates, speeches, votes, questions, legislation.

Use one catalogue as the canonical schema/lineage source. Create subordinate table pages only when complexity warrants it.

### 5. Oireachtas refresh/validation orchestration

**Repository:** `eirepolitic-data-pipeline`.

**Evidence:** `.github/workflows/oireachtas_*.yml`, `docs/oireachtas_packet_status.md`.

**Document:** triggers, dependency order, scheduled/manual behavior, validation gates, cutover/backfill procedures, failure handling, handoff.

### 6. Oireachtas write policies and downstream contracts

**Repository:** `eirepolitic-data-pipeline`.

**Evidence:** `configs/oireachtas/write_policies.yml`, `configs/oireachtas/downstream_contracts.yml`.

**Document:** append/replace/merge behavior, compatibility constraints, downstream consumers, protected assumptions, change procedure.

### 7. `bb-comp-prices` repository and platform overview

**Repository:** `bb-comp-prices`.

**Document:** repository page plus platform architecture entry point covering Best Buy discovery/extraction, competitor acquisition, matching, validation, storage, orchestration, configuration and current maturity.

The repository page and architecture may be separate pages but should be one documentation initiative.

### 8. `bb-comp-prices` S3 storage and data-product model

**Repository:** `bb-comp-prices`.

**Verified configuration:** `ca-central-1`, bucket `eirepolitic-data`, prefix `bb-comp-prices`.

**Document:** raw/history/latest/manifests/diagnostics layout, schemas, append/history rules, CSV/Parquet conventions, lineage and retention assumptions.

### 9. `bb-comp-prices` end-to-end orchestration and security/configuration boundary

**Repository:** `bb-comp-prices`.

**Evidence:** `.github/workflows/end_to_end.yml`, CLI/controller/config.

**Document:** stage controls, browser dependency, AWS secret names, concurrency/timeouts, failure artifacts, safe retry rules, operational runbook.

### 10. `degenerate_investigator` repository and UFC analytics architecture

**Repository:** `degenerate_investigator`.

**Document:** repository/system architecture, current/historical ingestion, enrichment, feature/training/scoring/reporting flow, external APIs, dependencies and limitations.

Preserve the repository's explicit boundary: it does not implement staking logic or bookmaker-targeted betting recommendations.

### 11. `degenerate_investigator` S3, orchestration and security/configuration boundary

**Repository:** `degenerate_investigator`.

**Verified defaults:** bucket `degenerative-investigator`, region `us-east-2`.

**Document:** S3 layout, GitHub Actions stage ordering, secret/configuration names, external APIs, rerun/recovery behavior, report publication path, model-artifact lifecycle.

### 12. `autodoc` repository and system architecture

**Repository:** `autodoc`.

**Document:** Appsmith intake → GitHub config/index → enrichment → section extraction → rendering → review → publication lifecycle; generated artifacts; workflow topology; dependencies; current-vs-historical implementation drift.

### 13. AutoDoc Appsmith intake/configuration application

**Repositories:** external Appsmith app + `autodoc` + `eirepolitic.github.io` embed.

**Document:** widgets, queries, JS orchestration, GitHub Contents API calls, config/index lifecycle, edit/rerun path, public embed, access/authentication, failure modes and deployment/update procedure.

**External verification needed:** current live Appsmith configuration/export when this initiative begins. The detailed pasted technical handoff in `doc_configs/autodoc/autodoc_app.json` is strong source evidence but does not prove present live UI state.

### 14. AutoDoc configuration schema and project-index registry

**Repository:** `autodoc`.

**Document:** base config, enriched config, asset model, `_index.json`, updated-at semantics, source modes, lifecycle and compatibility rules.

### 15. AutoDoc creation-pipeline orchestration and trust boundaries

**Repository:** `autodoc`.

**Evidence:** `.github/workflows/autodoc_pipeline.yml` plus stage workflows.

**Document:** push trigger, bot-loop protection, stage ordering, write permissions, OpenAI/GitHub credentials, rebase/commit behavior, manual recovery workflows and concurrency.

### 16. AutoDoc reviewed-document website publication boundary

**Repositories:** `autodoc` → `eirepolitic.github.io`.

**Evidence:** `.github/workflows/publish_to_website.yml`.

**Why P0:** the current workflow uses `WEBSITE_PAT`, clones the website repository, copies reviewed Markdown and pushes directly. This differs from the newer website discipline requiring focused PRs, documentation validation, merge, and matching Pages verification.

**Documentation requirement:** document current behavior and the control mismatch exactly. Any redesign is a separate architecture/security decision requiring explicit approval.

## P1 — active operational documentation initiatives

### Irish Politics Analytics / `eirepolitic-data-pipeline`

17. **Instagram / constituency campaign rendering system** — YAML campaign specs, political-data inputs, external template provider, local deterministic renderer, generated image artifacts, GitHub Actions.

18. **AI member-profile / Instagram content workflow** — AI content-generation stage, prompts/models/configuration, member inputs, outputs and workflow behavior where distinct from the rendering engine.

19. **Member Profile Metrics Builder** — `process/build_member_profile_metrics.py`, workflow, metric definitions, year/period assumptions, input/output schemas and consumers.

20. **Reusable LLM Task Runner Framework** — `process/llm_table_runner.py`, `tasks/`, controller workflow; OpenAI/YAML/S3 processing model, task schema, retries, outputs and reusable operating procedure.

### `bb-comp-prices`

21. **Best Buy Marketplace category discovery** — category/browser discovery, ownership/condition classification, pagination/lazy loading, validation and outputs.

22. **Best Buy product and Marketplace-offer extraction** — PDP/product parsing, recommended/alternate Marketplace offers, availability, normalization, S3 outputs and validation.

23. **Amazon.ca competitor acquisition/recovery system** — search/detail acquisition, ASIN candidate handling, variant gates, offer extraction, recovery/health diagnostics and source-specific failure modes.

24. **Product matching and confidence-scoring engine** — exact/fuzzy evidence, contradictions, scoring thresholds, matched/review/rejected states, labelled/validation evidence and manual-review boundary.

### `degenerate_investigator`

25. **Current UFC event/fighter ingestion** — UFC Stats event/card/profile extraction and raw data products.

26. **Historical fight/fighter-profile ingestion** — historical source collection feeding training datasets.

27. **Current MMA odds ingestion** — The Odds API integration, h2h normalization, implied-price/probability inputs, API configuration and raw products.

28. **Fighter recent-news enrichment** — OpenAI Responses API/web search, JSON extraction/repair, labels/summaries, error behavior and raw products.

29. **Matchup feature engineering** — event/profile/odds/news joins and derived difference features.

30. **Historical training-dataset builder** — historical joins, mirrored rows, target construction and training CSV/Parquet products.

31. **UFC winner-model training** — scikit-learn pipeline, Random Forest/Dummy fallback, train/test logic, metrics, pickle artifact and feature importance.

32. **Target-event scoring** — trained-model path, heuristic fallback, probabilities, confidence, signals and model-vs-market deltas.

33. **Fight-analysis report generator** — prediction/news joins, OpenAI/fallback text generation, Markdown/CSV/Parquet reports and analytical limitations.

### `autodoc`

34. **Asset enrichment/source-resolution stage** — pasted/GitHub-path/GitHub-URL/HTTP sources, private-repo access, text/binary behavior, provenance metadata and errors.

35. **LLM section-fact extraction stage** — base/type template split, enriched JSON input, facts-only extraction, rate-limit handling and summary CSV contract.

36. **Template and Markdown rendering system** — template types, metadata placeholders, section rendering, facts-only rule, YAML front matter and generated Markdown path.

37. **LLM review/concision stage** — reviewed-doc lifecycle, model selection, formatting/order preservation rules and overwrite behavior.

## P2 — supporting documentation initiatives

### `eirepolitic-data-pipeline`

38. **Data maintenance/repair/backfill utilities** — group destructive and repair helpers into an operational utilities reference unless an individual tool is independently scheduled/security-sensitive.

### `bb-comp-prices`

39. **Walmart.ca competitor acquisition/probe subsystem** — source-specific search/detail probes and maturity/status; promote to P1 if current implementation proves production-equivalent to Amazon.

40. **Probe/diagnostics/extraction-research framework** — group source probes, network/browser investigations and evidence reports rather than documenting every probe script separately.

41. **Validation/data-quality framework** — fixture/unit validation, schema/row/duplicate/price/variant checks, current reports and readiness gates.

42. **Python package/CLI/configuration/developer reference** — package layout, entry point, dependencies, settings, local/test execution.

### `degenerate_investigator`

43. **S3-to-repository report publication workflow** — generated-report transfer back to GitHub, permissions, rerun/idempotency and publication controls.

### `autodoc`

44. **Generated/reviewed documentation artifact lifecycle and manual recovery workflows** — base/enriched/summaries/generated/reviewed states, manual enrichment/extraction/render/review/index workflows, recovery and rerun procedure.

### `Overlord`

45. **`Overlord` repository/task-record system** — repository purpose/maturity, Markdown task schema, work/personal organization, lifecycle conventions.

46. **Overlord versioned task/project/meeting templates** — current v1 template equivalence, versioning/change rules, intended semantic distinctions only when implementation establishes them.

## P3 — historical/status-verification documentation initiatives

These should not be rebuilt as if they were current independent systems. Preserve authoritative archive/successor mapping and promote only if repository evidence proves they remain active.

47. **Constituency Images Indexer** — historical implementation/successor record.

48. **Debate Issue Classifier** — historical implementation/successor record.

49. **LLM Column Creator** — predecessor record linked to the current Reusable LLM Task Runner Framework.

50. **Member Images Pipeline** — historical implementation/successor record.

51. **Member Summaries Table** — historical implementation/successor record.

52. **S3 Column Deleter** — historical/destructive utility record; current maintenance tooling should be documented under operational utilities where applicable.

53. **Debate/speech classification and member-enrichment legacy scripts** retained inside `eirepolitic-data-pipeline` — lineage/status audit rather than duplicate current-system pages.

54. **Experimental/editorial content-generation workflows** such as `ridiculous_sentences_weekly.yml` — verify active intent before full current documentation; otherwise archive as experiment.

55. **Superseded `bb-comp-prices` probes/experiments** — retain provenance inside the diagnostics/history page, not as independent top-level docs.

56. **Historical AutoDoc-generated `docs/eirepolitic/pipeline/*` artifacts** — provenance/reference only; actual source repositories remain implementation sources of truth.

## Explicit non-targets

The repository scan intentionally excludes these from separate full-documentation initiatives:

- `.gitkeep` files;
- decorative/static assets with no subsystem behavior;
- individual generated `.enriched.json` files and summary CSVs;
- individual generated Markdown files when they are products of a documented generator;
- `Overlord` `test-task-*` fixtures;
- every individual Best Buy/Amazon/Walmart probe script when it belongs to the shared diagnostics framework;
- duplicate/historical AutoDoc generated versions of the same predecessor pipeline;
- secret values, tokens, keys, personal account identifiers and private credentials.

## Recommended documentation waves

### Wave 0 — already complete

- Documentation site/repository.
- High Director and integrations.

### Wave 1 — foundations and control boundaries

1. Irish Politics Analytics umbrella architecture.
2. `eirepolitic-data-pipeline` repository.
3. Unified Oireachtas Data Platform.
4. Oireachtas data catalogue.
5. Oireachtas orchestration.
6. Oireachtas write policies/downstream contracts.
7. `autodoc` repository/system architecture.
8. AutoDoc Appsmith application.
9. AutoDoc config/index model.
10. AutoDoc pipeline/security architecture.
11. AutoDoc website-publication control boundary.
12. `bb-comp-prices` repository/platform architecture + storage/orchestration boundary.
13. `degenerate_investigator` repository/system architecture + storage/orchestration boundary.

Wave 1 establishes the architecture each later component should link to instead of duplicating.

### Wave 2 — active operational pipelines

- active `eirepolitic-data-pipeline` media/member/LLM components;
- Best Buy/Amazon/matching pipelines;
- UFC ingestion/enrichment/features/training/scoring/reporting;
- AutoDoc enrichment/extraction/render/review stages.

### Wave 3 — supporting systems and developer/runbook detail

- Walmart subsystem;
- diagnostics and validation frameworks;
- developer/CLI references;
- maintenance utilities;
- report publication;
- AutoDoc manual recovery/artifact lifecycle;
- Overlord task-record system/templates.

### Wave 4 — archival reconciliation

- six existing historical pipeline records;
- retained legacy scripts;
- experiments and superseded probes;
- successor links and retirement/status evidence.

## External authoritative sources likely required later

Do not request these now. Request one coherent source only when the corresponding full-documentation initiative reaches the point where repository evidence is insufficient.

| Future initiative | Likely external source gap |
|---|---|
| AutoDoc Appsmith application | Live Appsmith application export/configuration, queries/actions/widgets/auth settings without secret values |
| AutoDoc security | Current Appsmith PAT permission/auth configuration and any non-repository deployment settings; never secret values |
| `eirepolitic-data-pipeline` security/cloud reference | Live AWS S3/IAM/Glue/Athena configuration where exact deployed state cannot be proven from source |
| `bb-comp-prices` security/cloud reference | Live S3/IAM configuration and any external browser/network infrastructure if used outside GitHub Actions |
| `degenerate_investigator` security/cloud reference | Live S3/IAM configuration and any external account-level API settings needed for exact deployed boundary |
| Historical pipeline status | User confirmation only where current source cannot establish retired/replaced/active intent |

Public API documentation and repository-inspectable source should be inspected directly rather than requested from the user.

## Cross-repository architecture facts to preserve

- `eirepolitic.github.io` is the persistent technical-documentation source of truth.
- `eirepolitic-data-pipeline` is the principal political-data implementation repository found in this scan.
- Historical pipeline pages in the documentation site and AutoDoc corpus must link to current/legacy source lineage rather than compete as duplicate sources of truth.
- `bb-comp-prices` is a separate competitor-pricing platform despite reusing the `eirepolitic-data-pipeline` AWS/S3 pattern.
- `degenerate_investigator` is a separate UFC analytics/ML system.
- `Overlord` currently has no verified integration with High Director or the other repositories.
- `autodoc` connects Appsmith, GitHub, OpenAI and website publication; its direct website-push path is a distinct control boundary that must remain visible until an approved architecture decision changes it.

## Next safe development action

After this catalogue passes validation and deploys successfully, close the discovery initiative. The next full-documentation initiative should begin with **Wave 1**, starting with the **Irish Politics Analytics umbrella architecture and `eirepolitic-data-pipeline` repository/Oireachtas foundation**, unless the system owner chooses a different priority.

No architecture/security/cost change is implied by this ordering.

## Related Documents

- [Repository Documentation Discovery Initiative]({{ '/projects/high-director/repository-documentation-discovery/' | relative_url }})
- [Repository Scan — bb-comp-prices]({{ '/projects/high-director/repository-scan-bb-comp-prices/' | relative_url }})
- [Repository Scan — degenerate_investigator]({{ '/projects/high-director/repository-scan-degenerate-investigator/' | relative_url }})
- [Repository Scan — Overlord]({{ '/projects/high-director/repository-scan-overlord/' | relative_url }})
- [Repository Scan — autodoc]({{ '/projects/high-director/repository-scan-autodoc/' | relative_url }})
