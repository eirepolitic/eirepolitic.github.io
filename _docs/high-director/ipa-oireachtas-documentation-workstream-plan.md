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

All six P0 components are complete and published.

### P1

| Order | Component | State |
| --- | --- | --- |
| 17 | Instagram / constituency campaign rendering system | merged; third exact-SHA Pages retry on `docs/ipa-instagram-rendering-pages-retry-3` |
| 18 | AI member-profile / Instagram content workflow | blocked on target 17 Pages gate |
| 19 | Member Profile Metrics Builder | discovery complete enough to draft |
| 20 | Reusable LLM Task Runner Framework | discovery complete enough to draft |

## Verified P1 rendering discoveries

- `Instagram Campaign Render (Manual)` is the current review-oriented campaign workflow and does not publish, schedule, or approve Instagram content.
- `process/instagram_render_campaign.py` currently supports only `member_profile_batch_v1` and initializes generated review rows as `needs_review` / `publish_ready=no`.
- `instagram/renderer/template_renderer.py` is a deterministic Pillow renderer for JSON layouts/palettes plus YAML/JSON bindings; it emits PNGs, source-value metadata, render manifests, and warnings.
- Deterministic caption/alt-text generation is separate from rendering and does not use an LLM.
- Publish-queue generation is gated by explicit approval state, `publish_ready`, and empty `safety_notes`; it creates files only and performs no social-platform publishing.
- `process/instagram_render_post.py` remains the executable constituency Jinja2/Playwright renderer and has a local fixture regression test.
- Bannerbear and Placid provider adapters are implemented with explicit mappings and local-HTML fallback, but live provider credentials/templates/successful current renders are unverified in this workstream.
- Constituency/provider-test paths still default to older compatibility/legacy S3 inputs, while the current member-profile campaign reads `processed/members/member_profile_metrics_2025.csv`.

## Discovery state

- [x] full P0 implementation/configuration/runtime audit and all six P0 documentation components
- [x] complete `instagram/`, `process/instagram*`, and Instagram workflow trees
- [x] campaign renderer/spec, deterministic renderer, copy pack, queue, S3 preview path
- [x] constituency HTML renderer, local renderer test, and provider-adapter architecture
- [ ] AI member-profile / Option 5 implementation and workflows at documentation depth
- [ ] Member Profile Metrics Builder at dedicated component depth
- [ ] Reusable LLM Task Runner Framework at dedicated component depth
- [ ] P2 maintenance/repair/backfill utility status and safety procedures
- [ ] P3 retained legacy/editorial successor/status reconciliation

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
| P1 Instagram/constituency rendering | #90 | `31229511638` success | `31229551593` cancelled after successful Jekyll build for SHA `b471aeacaba092610ce85f278bc74824ae0eee4a` | superseded by retry |
| P1 rendering publication retry #1 | #93 | `31229645985` success | `31229661485` cancelled after successful Jekyll build for SHA `2b02a5ca8f3e531f6fe4df7945719aa9314bd7bf` | superseded by retry #2 |
| P1 rendering publication retry #2 | #95 | `31229754311` success | `31229768879` cancelled before build/deploy for SHA `9d82f01e4bbff0608d3ae4859a21d4c837d46334` when newer `main` run `31229772219` entered the lane | superseded by retry #3 |
| P1 rendering publication retry #3 | pending PR | pending | pending | in progress |

## Publication-gate note

Parallel `main` changes have repeatedly pre-empted exact-SHA Pages deployment. Target 17 has passed documentation validation and successful Jekyll builds; the remaining issue is deployment concurrency. The workstream still requires successful exact-SHA Pages deployment before target 18 starts.

## Next action

Complete target-17 retry #3: validate, merge, and exact-SHA Pages-verify. Only then begin the AI member-profile / Instagram content workflow from current `main`.
