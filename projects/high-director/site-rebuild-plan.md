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

Created this persistent plan and exposed it under High Director documentation.

## Step 1 — Documentation standard

**Status:** Complete — 2026-08-05, PR #3

Defined the content model before migration.

**Completed deliverables**

- `DOCUMENTATION_STANDARD.md`
- Required and optional front matter fields
- Allowed sections, document types, and lifecycle statuses
- Naming, URL, archive, verification, and writing rules
- Templates for repository, system, runbook, decision, and reference pages

## Step 2 — Jekyll collection foundation

**Status:** Not started

Create a `_docs` Jekyll collection and configure stable output URLs.

**Deliverables**

- `_docs/` directory structure
- `_config.yml` collection configuration
- Default front matter rules
- Basic collection index generation
- Compatibility check with GitHub Pages

**Checkpoint:** Confirm the collection builds before migrating existing documentation.

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

**Deliverables**

- Knowledge-base purpose statement
- Main documentation entry points
- Recently updated documents
- Active repositories and systems
- High Director entry point
- Secondary links to articles and public outputs

## Step 7 — Client-side search

**Status:** Not started

Add search without an external service.

**Deliverables**

- Jekyll-generated JSON search index
- Search interface
- Matching across title, summary, repository, tags, technologies, and page text
- Keyboard-accessible results

## Step 8 — Indexes and relationships

**Status:** Not started

Add generated repository, technology, document-type, status, and recent-update indexes, plus related-document links.

## Step 9 — Documentation quality validation

**Status:** Not started

Add automated checks for metadata, statuses, document types, duplicate permalinks, internal links, assets, and archive fields.

**Deliverables**

- Python validation script
- GitHub Actions pull-request workflow

**Checkpoint:** Review rules before making failures mandatory.

## Step 10 — Operational documentation

**Status:** Not started

Document local editing, publishing, new-document creation, archiving, navigation, search, validation, and troubleshooting.

## Step 11 — Final cleanup and release

**Status:** Not started

Complete the custom 404 page, accessibility and mobile review, broken-link review, orphan cleanup, metadata normalization, and final architecture summary.

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
