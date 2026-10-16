---
title: October 2026 Project Cleanup, Migration & Development Plan
summary: Priority-ordered working plan for migrating GitHub ownership, standardizing repositories, rebuilding documentation flow, cleaning active projects, and running revenue investigations.
section: notes
doc_type: note
status: active
created: 2026-10-15
updated: 2026-10-15
last_verified: 2026-10-15
owner: Warren Gleeson
order: 200
permalink: /projects/notes/october-2026-project-work-plan/
tags:
  - planning
  - github
  - migration
  - documentation
  - portfolio
  - general-director
  - cleanup
---

# October 2026 Project Cleanup, Migration & Development Plan

## Purpose

This is the working checklist for the current three-day project sprint. It is intentionally priority-ordered rather than time-boxed. Work should continue from the highest-value unfinished item rather than following a rigid daily schedule.

Primary goals:

1. establish Warren Gleeson's personal GitHub account as the primary home for active projects;
2. preserve existing functionality while cleaning and standardizing repositories;
3. make `General_Director` the default operating layer for human and AI-agent work;
4. rebuild the documentation/portfolio architecture so repositories are the source of truth;
5. continue Overlord development without disrupting its current working architecture;
6. preserve and clean the Eirepolitic data pipeline and Instagram content factory; and
7. run low-touch online-business investigations in parallel.

## Operating principles

- Preserve working functionality first.
- Do not redesign working systems from scratch unless explicitly approved for that component.
- Prefer repository transfer over code copying so history and repository metadata are preserved.
- Archive obsolete repositories rather than delete them.
- Repositories are the canonical source of truth for documentation.
- The documentation website is a presentation and aggregation layer, not a second canonical documentation source.
- Use common standards where projects have similar operating needs, but allow justified deviations.
- Human-facing portfolio documentation and AI-agent operating documentation should be distinct.
- Do not polish individual projects in ways that will immediately need to be reorganized again after migration or standardization.

## Phase 0 — Light setup / preparation

- [ ] Create the new personal GitHub account using `warrengleeson` if available.
- [ ] Configure the account as Warren Gleeson's professional/personal development account.
- [ ] Reserve/create the `warrengleeson.github.io` repository when appropriate.
- [ ] Keep the current Eirepolitic account available during migration.
- [ ] Prepare the first revenue-investigation brief so agents can begin immediately when active work starts.
- [ ] Use this page as the fixed working checklist and update it as decisions change.

## Phase 1 — GitHub migration foundation

Target state: the personal account becomes the primary owner of active projects. The old Eirepolitic account remains dormant rather than being deleted.

- [ ] Confirm the final migration order for repositories.
- [ ] Transfer active repositories to the personal account where GitHub transfer is appropriate.
- [ ] Preserve Git history, issues, pull requests, releases, Actions configuration, webhooks, deploy keys, secrets/settings, and integrations wherever GitHub supports preservation.
- [ ] Verify redirects and external references after each transfer.
- [ ] Review GitHub Pages behavior separately because Pages URLs may require explicit migration work.
- [ ] Audit external integrations encountered during migration, including AWS, DigitalOcean, GitHub Actions, Meta/Instagram, credentials, webhooks, Pages, and secrets.
- [ ] Disconnect obsolete integrations from the old Eirepolitic account.
- [ ] Leave the old Eirepolitic account dormant once migration is complete and dependencies are disconnected.

## Phase 2 — General repository operating standard

`General_Director` should become the default operating layer for AI agents and future repo work unless a project has a justified reason to deviate.

Initial implementation should use templates and checklists. Automated enforcement can follow later.

### Default repository standard

- [ ] `README.md`
- [ ] `DIRECTOR.md`
- [ ] architecture overview
- [ ] deployment / infrastructure notes
- [ ] testing instructions
- [ ] AI-agent operating/development instructions
- [ ] current status / roadmap
- [ ] `project.yaml`

Suggested `project.yaml` fields:

```yaml
status: active
visibility: public
summary: ""
docs_publish: true
portfolio_publish: false
```

### Documentation standard

- [ ] Move/adapt the useful rules from the current documentation site's `DOCUMENTATION_STANDARD.md` into `General_Director`.
- [ ] Keep repository documentation canonical.
- [ ] Separate AI-agent operating documentation from concise human-facing project documentation.
- [ ] Preserve lifecycle status, verification dates, archive rules, source-of-truth rules, and agent-continuation requirements where useful.
- [ ] Define how exceptions to the standard are documented.

### Future enhancements — not core sprint scope

- [ ] Automated validation for missing standard files, stale metadata, inconsistent project status, and documentation drift.
- [ ] Periodic higher-cost LLM documentation sweep to identify gaps, contradictions, stale material, and cleanup opportunities.

## Phase 3 — Documentation and portfolio architecture

Target site: `warrengleeson.github.io`.

Initial approach: preserve the current documentation site's overall technical-documentation style and improve it incrementally rather than redesigning immediately.

- [ ] Build the new personal documentation/portfolio repository.
- [ ] Use each project repository as the canonical documentation source.
- [ ] Build a low-cost automated sync flow that copies/publishes repository documentation into the documentation site.
- [ ] Prefer update-on-change plus a scheduled reconciliation run if practical.
- [ ] Public repositories publish documentation by default.
- [ ] Private repositories publish nothing unless explicitly approved.
- [ ] Allow explicitly selected/sanitized documentation from private repos to be published.
- [ ] Add project lifecycle/status display sourced from repository metadata.
- [ ] Create concise portfolio surface pages only for projects mature enough to showcase.
- [ ] Keep deeper technical documentation available underneath the surface layer.
- [ ] Create a research/plans section that is public by default but not prominently surfaced as portfolio material.
- [ ] Keep existing Eirepolitic articles/posts available during the initial migration.
- [ ] Consider a smaller Eirepolitic-specific site later for Eirepolitic-only functions such as web versions of Instagram posts.

## Phase 4 — Repository cleanup and classification

### `General_Director`

**Status:** KEEP / FOUNDATION

- [ ] Treat as the primary operating layer for future agent work.
- [ ] Review for currentness before broad rollout.
- [ ] Integrate repository/documentation templates and checklists.
- [ ] Integrate the documentation standard.

### `eirepolitic-data-pipeline`

**Status:** KEEP / CLEAN / PORTFOLIO

Core functionality to preserve:

1. data ingestion / extraction from multiple sources;
2. transformation and storage in AWS; and
3. Instagram content creation/publishing factory.

- [ ] Keep as one repository unless a component has a strong independent reason to become its own project.
- [ ] Identify vestigial, unused, duplicated, and disconnected code.
- [ ] Preserve functioning pipeline and content-factory behavior while cleaning.
- [ ] Define reusable components and how agents should operate/update them.
- [ ] Standardize documentation and agent entry points.
- [ ] Review AWS and Meta/Instagram dependencies as part of cleanup/migration.

### `Overlord`

**Status:** KEEP / ACTIVE DEVELOPMENT

- [ ] Continue Claude-led development.
- [ ] Use owner review to make decisions, provide headers/context, and approve direction.
- [ ] Do not casually re-architect the current working control plane.
- [ ] Keep production architecture and benchmark work separated unless explicitly changed.

### `bb-comp-prices`

**Status:** KEEP / ACTIVE BUT PAUSED

Purpose: competitor price scraping/matching project intended to map Best Buy's assortment against equivalent listings at retailers such as Amazon and Walmart.

- [ ] Preserve repository for future development.
- [ ] Include technical documentation on the docs site.
- [ ] Do not create a prominent portfolio surface page until the project has made substantially more progress.

### `degenerate_investigator`

**Status:** KEEP / ACTIVE BUT PAUSED

Purpose: MMA analysis/investigation tool intended to provide fight information before watching events.

- [ ] Preserve repository for future development.
- [ ] Include technical documentation on the docs site.
- [ ] Do not create a prominent portfolio surface page until the project has made substantially more progress.

### `claude-director-test`

**Status:** ARCHIVE

- [ ] Confirm no unique useful material remains.
- [ ] Archive rather than delete.

### `autodoc`

**Status:** SALVAGE THEN ARCHIVE

- [ ] Review templates, documentation-generation patterns, examples, and useful process logic.
- [ ] Move useful concepts into `General_Director` and/or the new documentation sync architecture.
- [ ] Archive the original repository once useful material has been preserved.

### `eirepolitic.github.io`

**Status:** KEEP AS REFERENCE / FUNCTIONALLY REBUILD

- [ ] Preserve useful documentation standards, templates, navigation concepts, archive rules, and styling.
- [ ] Keep existing articles/posts available initially.
- [ ] Shift canonical project documentation into individual repositories.
- [ ] Rebuild the site role around aggregation/presentation rather than primary knowledge storage.
- [ ] Eventually migrate the main personal documentation/portfolio role to `warrengleeson.github.io`.

## Parallel workstream — Revenue investigations

Goal: identify feasible, low-touch, low-capital online businesses that can be substantially researched, built, or operated with agent assistance. Ideas do not need to use current AI/data-pipeline skills.

### Stage 1 — Broad idea generation

- [ ] Generate a wide pool of possible online-business models.
- [ ] Avoid over-filtering during the first pass.
- [ ] Capture ideas in the research section of the documentation site.

### Stage 2 — Initial viability scoring

Evaluate viable candidates against:

- startup cost;
- time to first revenue;
- ongoing human effort;
- automation potential;
- legal/platform risk; and
- expected upside.

- [ ] Score/filter the initial pool.
- [ ] Select the strongest candidates for deeper investigation.

### Stage 3 — Detailed investigation

- [ ] Research market feasibility, execution requirements, competition, constraints, and likely failure modes.
- [ ] Produce decision-ready reports for the strongest candidates.

### Stage 4 — Planning

- [ ] Create implementation plans for ideas that survive deeper investigation.

### Stage 5 — Development

- [ ] Begin building/testing ideas when investigation quality justifies moving forward.
- [ ] Continue development only while evidence remains favorable.

## Current decisions

- New personal GitHub username target: `warrengleeson`.
- New documentation/portfolio target: `warrengleeson.github.io`.
- All active/private projects should normally live under the same personal GitHub account; use repository visibility rather than a second anonymous account by default.
- Research is public by default.
- Private-repository documentation publication is opt-in.
- Eirepolitic Instagram brand/account remains in use.
- GitHub Pages remains the preferred hosting mechanism unless a strong reason to change appears.
- Existing working functionality takes priority over cleanup elegance.
- Repo migration should preserve as much repository history/configuration as practical.
- Obsolete repositories should be archived rather than deleted.
- The plan is priority-ordered rather than tied to fixed hourly schedules.

## Completion rule

At any point, continue with the highest-value unfinished item that does not depend on an unresolved decision or an incomplete prerequisite. If a new decision changes architecture, migration risk, cost, or public/private exposure, update this plan before executing the change.
