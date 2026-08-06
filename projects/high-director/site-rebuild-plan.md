---
title: "Documentation Site Rebuild Plan"
layout: default
permalink: /projects/high-director/site-rebuild-plan/
status: active
updated: 2026-08-05
---

# Documentation Site Rebuild Plan

This file is the persistent implementation plan for converting the site into a structured technical knowledge base for Eire Politic projects and High Director-assisted development.

## Operating rules

- Complete one step per chat checkpoint where practical.
- Keep each step small enough to implement, review, and merge in one session.
- Use branches and pull requests for material changes.
- Preserve existing URLs where practical.
- Do not store secrets in the repository.
- Update this plan after each completed step.
- Mark completed work with a completion date and pull request number.

## Status key

- `Not started`
- `In progress`
- `Blocked`
- `Complete`

## Step 0 — Record the plan

**Status:** Complete — 2026-08-05, PR #2

Create this persistent plan and expose it under the High Director documentation section.

**Deliverables**

- Build plan page
- Clear implementation order
- Checkpoints and completion records

## Step 1 — Documentation standard

**Status:** Complete — 2026-08-05

Define the content model before moving files.

**Deliverables**

- `DOCUMENTATION_STANDARD.md`
- Required and optional front matter fields
- Allowed document types and lifecycle statuses
- Naming, URL, archive, and writing conventions
- Templates for repository, system, runbook, decision, and general reference pages

**No user input expected.**

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

- Existing pipeline documents moved into `_docs/archive/`
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

- Top-level sections: Repositories, Systems, Data and Schemas, Runbooks, Architecture Decisions, High Director, Notes, Archive
- Ordered navigation using front matter
- Section landing pages
- Active-page highlighting
- Mobile navigation behavior

**No user input expected unless section names need changing.**

## Step 5 — Documentation layout and design system

**Status:** Not started

Replace the current large Cayman-style presentation with a compact documentation interface.

**Deliverables**

- Compact site header
- Persistent desktop sidebar
- Responsive mobile navigation
- Breadcrumbs
- Document metadata panel
- Automatic on-page table of contents
- Consistent typography, tables, code blocks, and callouts
- Centralized CSS and JavaScript assets
- Removal of avoidable inline styles

**Checkpoint:** Visual approval before applying optional cosmetic refinements.

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

**User input may be requested only for wording or featured content.**

## Step 7 — Client-side search

**Status:** Not started

Add search without an external service.

**Deliverables**

- Jekyll-generated JSON search index
- Search interface
- Matching across title, summary, repository, tags, technologies, and page text
- Keyboard-accessible results
- No external account, database, or paid service

## Step 8 — Indexes and relationships

**Status:** Not started

Make content discoverable through generated indexes.

**Deliverables**

- Repository index
- Technology index
- Document-type index
- Status index
- Recently updated index
- Related-document links
- Source repository and source path links where available

## Step 9 — Documentation quality validation

**Status:** Not started

Add automated checks for documentation integrity.

**Deliverables**

- Python validation script
- Required metadata checks
- Status and document-type validation
- Duplicate permalink detection
- Broken internal link checks
- Missing asset checks
- Archive metadata checks
- GitHub Actions pull-request workflow

**Checkpoint:** Review validation rules before making failures mandatory.

## Step 10 — Operational documentation

**Status:** Not started

Document how the site itself is maintained.

**Deliverables**

- Local editing and publishing instructions
- New-document workflow
- Archive workflow
- Navigation behavior
- Search-index behavior
- Validation and troubleshooting guide
- High Director continuation instructions

## Step 11 — Final cleanup and release

**Status:** Not started

Complete a final repository and live-site review.

**Deliverables**

- Custom 404 page
- Accessibility and mobile review
- Broken-link review
- Orphaned-file cleanup
- Metadata normalization
- Final architecture summary
- Update this plan with all pull requests and completion dates

## Decisions already made

- Keep GitHub Pages and Jekyll.
- Use Markdown as the primary documentation format.
- Keep the site optimized for internal technical reference first.
- Treat portfolio value as a secondary result of clear, attractive documentation.
- Avoid external services where repository-hosted functionality is sufficient.
- Prefer metadata-driven organization over folder-name logic.

## Decisions that may require user input later

- Whether selected documentation should be explicitly marked private-sensitive and excluded from publication.
- Which repositories and systems should be featured on the homepage.
- Whether archived pages should remain searchable by default.
- Whether the final visual style should be light-only or include a dark mode.

## Continuation note for a new chat

Read this file, inspect the latest merged pull requests, and continue from the first step whose status is not `Complete`. Update this page in the same pull request as each completed step.
