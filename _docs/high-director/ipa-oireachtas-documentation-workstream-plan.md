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
| 17 | Instagram / constituency campaign rendering system | complete and published after fourth exact-SHA retry |
| 18 | AI member-profile / Instagram content workflow | complete and published |
| 19 | Member Profile Metrics Builder | draft on `docs/ipa-member-profile-metrics` |
| 20 | Reusable LLM Task Runner Framework | discovery complete enough to draft |

## Verified P1 discoveries

- The deterministic Instagram campaign workflow is review-only and does not publish, schedule, or approve content.
- The checked-in Option 5 AI workflows are manual experiments: member-profile template editing and constituency-cover background generation. Neither publishes or approves content.
- Member-profile AI editing uses source-truth sidecars, two image edits, one structured vision-validation call, and still requires human review of the final image.
- Constituency AI generation keeps exact visible title text out of the generated background and overlays it through the deterministic renderer.
- The member-profile Option 5 workflow still invokes a legacy vote extractor that no longer feeds the generic metrics builder by default; this is documented as a redundant legacy side effect, not current lineage.
- `process/build_member_profile_metrics.py` is the authoritative year-aware metrics implementation; `build_member_profile_metrics_2025.py` is only a compatibility wrapper.
- Current metrics inputs are four Unified Oireachtas compatibility products: members, member votes, member photos, and classified debate issues.
- Metric outputs are year-specific and support immutable candidate-batch consumer output when `OIREACHTAS_BATCH_ID` is active.
- Latest observed dedicated metrics workflow run `29299647855` on 2026-07-14 succeeded end-to-end.

## Discovery state

- [x] full P0 implementation/configuration/runtime audit and all six P0 documentation components
- [x] target 17 deterministic Instagram/constituency rendering documentation
- [x] target 18 AI member-profile/Instagram content workflow documentation
- [x] target 19 metrics inputs, aliases, formulas, output schema, candidate semantics, workflow, consumers, wrapper lineage, and runtime evidence
- [ ] target 20 Reusable LLM Task Runner Framework at dedicated component depth
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
| P1 Instagram/constituency rendering | #90 | `31229511638` success | first exact-SHA deployment cancelled | superseded by retries |
| P1 rendering publication retry #4 | #100 | `31229949203` success | `31229966372` success; `925938a0db20c0d58f5fda33f1fb361bc53dcf1d` | complete |
| P1 AI member-profile / Instagram content | #104 | `31230259270` success | `31230282153` success; `507464f44a3321b70a473bd75095abb28da22f08` | complete |
| P1 Member Profile Metrics Builder | pending PR | pending | pending | draft in progress |

## Publication-gate note

Parallel `main` changes repeatedly pre-empted target 17's exact-SHA Pages deployment. The fourth focused retry succeeded. Target 18 then passed validation and exact-SHA Pages normally. The same gate remains mandatory for targets 19 and 20.

## Next action

Validate, merge, and exact-SHA Pages-verify the Member Profile Metrics Builder page. Only after that gate succeeds, begin the Reusable LLM Task Runner Framework from current `main`.
