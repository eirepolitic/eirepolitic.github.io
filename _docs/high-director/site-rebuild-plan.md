---
title: Documentation Site Rebuild Plan
summary: Persistent implementation plan for rebuilding the site as a structured technical knowledge base.
section: high-director
doc_type: agent
status: active
created: 2026-08-05
updated: 2026-08-05
last_verified: 2026-08-05
order: 20
permalink: /projects/high-director/site-rebuild-plan/
---

# Documentation Site Rebuild Plan

Persistent implementation plan for converting the site into a structured technical knowledge base for Eire Politic projects and High Director-assisted development.

## Operating rules

- Complete one step per chat checkpoint where practical.
- Keep each step small enough to implement, review, and merge in one session.
- Use branches and pull requests for material changes.
- Preserve existing URLs where practical.
- Do not store secrets in the repository.
- Update this plan after each completed step.

## Status key

`Not started` · `In progress` · `Blocked` · `Complete`

## Step 0 — Record the plan

**Status:** Complete — 2026-08-05, PR #2

## Step 1 — Documentation standard

**Status:** Complete — 2026-08-05, PR #3

Added `DOCUMENTATION_STANDARD.md` and reusable templates.

## Step 2 — Jekyll collection foundation

**Status:** Complete — 2026-08-05, PR #4

Configured the `_docs` collection, stable URLs, default metadata, section folders, and `/docs/` index.

## Step 3 — Migrate and normalize existing documentation

**Status:** Complete — 2026-08-05, PR #5

Migrated archive and High Director documentation, normalized metadata, preserved URLs, and removed duplicate sources.

## Step 4 — Data-driven navigation

**Status:** Complete — 2026-08-05, PR #6

**Completed deliverables**

- Added ordered section definitions in `_data/docs_sections.yml`
- Added metadata-driven documentation navigation
- Added landing pages for all eight sections
- Added document counts and ordered document lists
- Added active-section highlighting
- Added responsive mobile navigation using native disclosure controls
- Made the `/docs/` index metadata driven
- Configured collection pages to use the documentation layout

## Step 5 — Documentation layout and design system

**Status:** Not started

Build a compact documentation interface with a compact header, desktop sidebar, responsive mobile navigation, breadcrumbs, metadata, page contents, consistent components, and centralized assets.

**Checkpoint:** Visual approval before optional cosmetic refinements.

## Step 6 — Homepage redesign

**Status:** Not started

Make documentation the primary purpose of the homepage.

## Step 7 — Client-side search

**Status:** Not started

Add repository-hosted client-side search.

## Step 8 — Indexes and relationships

**Status:** Not started

Add generated repository, technology, document-type, status, and recent-update indexes, plus related-document links.

## Step 9 — Documentation quality validation

**Status:** Not started

Add automated metadata, permalink, link, asset, and archive checks with GitHub Actions.

## Step 10 — Operational documentation

**Status:** Not started

Document editing, publishing, navigation, search, validation, and troubleshooting.

## Step 11 — Final cleanup and release

**Status:** Not started

Complete accessibility, mobile, broken-link, orphaned-file, metadata, and architecture reviews.

## Decisions already made

- Keep GitHub Pages and Jekyll.
- Use Markdown as the primary format.
- Optimize for internal technical reference first.
- Treat portfolio value as a secondary result.
- Avoid external services where repository-hosted functionality is sufficient.
- Prefer metadata-driven organization over folder-name logic.

## Decisions that may require user input later

- Whether selected documentation should be excluded from publication.
- Which repositories and systems should be featured.
- Whether archived pages should be searched by default.
- Whether to add dark mode.

## Continuation note for a new chat

Read this file, inspect the latest merged pull requests, and continue from the first step whose status is not `Complete`. Update this page in the same pull request as each completed step.
