---
title: "Irish Politics Analytics / Oireachtas documentation workstream plan"
summary: "Persistent execution plan for the Irish Politics Analytics and eirepolitic-data-pipeline documentation workstream."
section: high-director
doc_type: agent
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: High Director
systems:
  - irish-politics-analytics
repositories:
  - eirepolitic.github.io
  - eirepolitic-data-pipeline
permalink: /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
---

# Irish Politics Analytics / Oireachtas documentation workstream plan

## Purpose

Mutable execution plan for the Irish Politics Analytics / `eirepolitic-data-pipeline` documentation workstream. The owner-wide target catalogue remains the read-only scope contract.

## Scope

- **P0:** umbrella architecture; repository; Unified Oireachtas platform; canonical product catalogue; refresh/validation orchestration; write policies/downstream contracts.
- **P1:** Instagram/constituency rendering; AI member-profile/Instagram workflow; Member Profile Metrics Builder; Reusable LLM Task Runner Framework.
- **P2:** maintenance, repair, and backfill utilities.
- **P3:** assigned legacy enrichment/classification/media/destructive/editorial targets and successor mapping.

Excluded except for necessary cross-references: AutoDoc, `bb-comp-prices`, `degenerate_investigator`, and Overlord.

## Evidence and publication rules

Current implementation/configuration outranks runtime evidence, user-supplied authoritative sources, current handoffs, archive material, and labelled inference. Never publish secrets or personal/private account details.

Each major documentation component uses a focused `docs/ipa-*` PR. Before moving to the next component: documentation validation must pass, the PR must merge, and the matching `pages-build-deployment` run must succeed for that exact merge SHA.

## Priority execution state

### P0

| Order | Component | State |
| --- | --- | --- |
| 1 | Irish Politics Analytics umbrella architecture | complete and published |
| 2 | `eirepolitic-data-pipeline` repository | complete and published |
| 3 | Unified Oireachtas Data Platform | complete and published |
| 4 | Oireachtas canonical data-product catalogue | complete and published |
| 5 | Oireachtas refresh/validation orchestration | complete and published |
| 6 | Oireachtas write policies and downstream contracts | complete and published |

**P0 status: complete.**

### P1

| Order | Component | State |
| --- | --- | --- |
| 17 | Instagram / constituency campaign rendering system | draft on `docs/ipa-instagram-rendering` |
| 18 | AI member-profile / Instagram content workflow | discovery in progress |
| 19 | Member Profile Metrics Builder | discovery complete enough to draft |
| 20 | Reusable LLM Task Runner Framework | discovery complete enough to draft |

## Verified P0 facts

- Canonical registry: 31 confirmed products — 23 silver, 5 gold, 3 control.
- Current source acquisition uses the public Oireachtas API with complete offset pagination, 429/5xx retry, repeated-page detection, and incomplete-pagination failure.
- Production publication uses immutable batches plus `production`/`previous` pointers; active candidate reads are isolated from production fallback.
- Weekly defaults: incremental, rolling 35-day window, page size 100. Monthly: incremental, previous month plus seven-day leading overlap, page size 200. Yearly: full previous calendar year, page size 200.
- Only the high-level refresh-validation orchestrator is scheduled; cadence wrappers are manual.
- Write strategies are `snapshot_replace`, `upsert`, `append`, and `rebuild`; all 31 products have policy coverage.
- Downstream validation currently contains six dataset contracts plus two legacy/reference comparison threshold sets.
- Auxiliary enrichment staging enforces source freshness before copying into a candidate.
- Production pointer mutation is guarded separately from candidate publication.
- **Observed runtime:** scheduled orchestrator run `30740881592` on 2026-08-02 completed refresh, validation, promotion, and pointer verification successfully.
- Historical July packet-status statements that scheduled observation was pending are stale relative to August runtime evidence.

## Verified P1 rendering discoveries

- `Instagram Campaign Render (Manual)` is the current review-oriented campaign workflow and does not publish, schedule, or approve Instagram content.
- `process/instagram_render_campaign.py` currently supports only `member_profile_batch_v1` and initializes generated review rows as `needs_review` / `publish_ready=no`.
- `instagram/renderer/template_renderer.py` is a deterministic Pillow renderer for JSON layouts/palettes plus YAML/JSON bindings; it emits PNGs, source-value metadata, render manifests, and warnings.
- deterministic caption/alt-text generation is separate from rendering and does not use an LLM.
- publish-queue generation is gated by explicit approval state, `publish_ready`, and empty `safety_notes`; it creates files only and performs no social-platform publishing.
- `process/instagram_render_post.py` remains the executable constituency Jinja2/Playwright renderer and has a local fixture regression test.
- Bannerbear and Placid provider adapters are implemented with explicit mappings and local-HTML fallback, but live provider credentials/templates/successful current renders are unverified in this workstream.
- constituency/provider-test paths still default to older compatibility/legacy S3 inputs, while the current member-profile campaign reads `processed/members/member_profile_metrics_2025.csv`.

## Discovery state

### Completed for P0

- [x] documentation standard/templates/catalogue/discovery plan and representative pages
- [x] complete `eirepolitic-data-pipeline` tree and dependency inventory
- [x] Oireachtas configs, package, process helpers, workflows, tests, handoffs and current runtime evidence
- [x] all canonical registry products, schemas-as-column-lists, PKs, cadences, endpoints and builder locations
- [x] write-policy coverage, merge semantics, relationship helpers and tests
- [x] downstream contract config, staging, compatibility adapters, comparison/mismatch behavior and contract tests
- [x] batch control, seeding, reassembly, promotion and rollback behavior

### P1 discovery

- [x] complete `instagram/` tree
- [x] complete `process/instagram*` tree
- [x] complete Instagram workflow tree
- [x] campaign renderer/spec, deterministic template renderer, copy pack, queue, S3 preview path
- [x] constituency HTML renderer and local renderer test
- [x] external provider adapter implementation at architecture level
- [ ] AI member-profile / Option 5 implementation and workflows at documentation depth
- [ ] Member Profile Metrics Builder at dedicated component depth
- [ ] Reusable LLM Task Runner Framework at dedicated component depth

### Later priorities

- [ ] P2 maintenance/repair/backfill utility status and safety procedures
- [ ] P3 retained legacy/editorial successor/status reconciliation
- [ ] exact live IAM/S3/Glue/Athena configuration only if a later documentation target requires deployed-account evidence

## PR ledger

| Component | PR | Validation | Pages | Result |
| --- | --- | --- | --- | --- |
| Workstream plan | #62 | `31219424981` success | `31219454738` success; `e25a90677d11c732bfe86a87616aa25191827cff` | complete |
| P0 umbrella architecture | #64 | `31219706244` success | `31219726250` success; `307441a2479cda507589bf77a796a54f6c0042ac` | complete |
| P0 repository | #66 | `31219954893` success | `31219991624` success; `49c130d88cf84418be3f15a17848f8d50f3112e1` | complete |
| P0 Unified Oireachtas platform | #68 | `31220172926` success | `31220199307` success; `74aa6405164440b62d28e6ac64d76f01388a7957` | complete |
| P0 data-product catalogue | #70 | `31220389309` success | first exact-SHA deployment cancelled by parallel `main` activity | superseded by retry |
| Catalogue publication retry | #73 | `31220665186` success | `31220683272` success; `6f5c9c1d9685addeed5ec75a05a6d701de04733d` | complete |
| P0 orchestration | #74 | validation passed | first exact-SHA deployment cancelled by parallel `main` activity | superseded by retry |
| Orchestration publication retry | #84 | `31229212100` success | `31229230209` success; `9b68becb6e2ca69c58c57cf1b2104948ec6a60d0` | complete |
| P0 policies/contracts | #85 | `31229340996` success | `31229357085` success; `021db2fe9fb9ea6b1d581b121508bdd8cd81bb83` | complete |
| P1 Instagram/constituency rendering | pending PR | pending | pending | draft in progress |

## Publication-gate note

Parallel `main` changes cancelled the first matching Pages deployment for both the catalogue and orchestration components while Jekyll was running. Neither cancellation reported a content-build failure. Both were resolved with focused retry PRs and successful Pages deployments for the retry merge SHA before subsequent work began.

## Next action

Validate, merge, and exact-SHA Pages-verify the Instagram/constituency campaign rendering system page. After that gate succeeds, begin the AI member-profile / Instagram content workflow from current `main`.
