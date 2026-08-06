---
title: "Documentation Site Rebuild Plan"
layout: default
permalink: /projects/high-director/site-rebuild-plan/
status: active
updated: 2026-08-05
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

Added `DOCUMENTATION_STANDARD.md` and templates for repositories, systems, runbooks, decisions, and references.

## Step 2 — Jekyll collection foundation

**Status:** Complete — 2026-08-05, PR #4

**Completed deliverables**

- Configured the `_docs` Jekyll collection with output enabled
- Added stable `/docs/:path/` permalinks
- Added default layout and visibility values
- Added section folders for repositories, systems, data, runbooks, decisions, High Director, notes, and archive
- Added a generated `/docs/` collection index
- Preserved all existing documentation during the foundation change

## Step 3 — Migrate and normalize existing documentation

**Status:** Not started

Move current technical pages into the collection and add consistent metadata.

**Deliverables**

- Pipeline documents moved into `_docs/archive/`
- Schema documents moved into `_docs/data/`
- High Director documents moved into `_docs/high-director/`
- Existing public URLs preserved where practical
- Redirect pages added where URLs must change
- Duplicate templates and obsolete placeholders removed

**Checkpoint:** Review navigation and confirm no important page was omitted.

## Step 4 — Data-driven navigation

**Status:** Not started

Replace folder-substring navigation with metadata-based navigation.

**Deliverables**

- Sections: Repositories, Systems, Data and Schemas, Runbooks, Architecture Decisions, High Director, Notes, Archive
- Ordered navigation using front matter
- Section landing pages
- Active-page highlighting
- Mobile navigation behavior

## Step 5 — Documentation layout and design system

**Status:** Not started

Build a compact documentation interface.

**Deliverables**

- Compact site header
- Persistent desktop sidebar
- Responsive mobile navigation
- Breadcrumbs
- Document metadata panel
- Automatic on-page table of contents
- Consistent typography, tables, code blocks, and callouts
- Centralized CSS and JavaScript
- Removal of avoidable inline styles

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
