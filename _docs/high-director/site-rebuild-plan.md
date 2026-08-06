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

## Completed steps

- **Step 0 — Record the plan:** Complete — 2026-08-05, PR #2
- **Step 1 — Documentation standard:** Complete — 2026-08-05, PR #3
- **Step 2 — Jekyll collection foundation:** Complete — 2026-08-05, PR #4
- **Step 3 — Migrate and normalize documentation:** Complete — 2026-08-05, PR #5
- **Step 4 — Data-driven navigation:** Complete — 2026-08-05, PR #6
- **Step 5 — Documentation layout and design system:** Complete — 2026-08-05, PR #7

Step 5 delivered a compact sticky header, responsive documentation sidebar, breadcrumbs, status and metadata panels, archive notices, automatic on-page contents, centralized CSS and JavaScript, accessible navigation, and consistent styles for prose, code, tables, callouts, and section cards.

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
