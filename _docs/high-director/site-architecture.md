---
title: Documentation Site Architecture
summary: Final architecture and maintenance model for the Eire Politic technical knowledge base.
section: high-director
doc_type: agent
status: active
repository: eirepolitic.github.io
technologies:
  - GitHub Pages
  - Jekyll
  - Markdown
  - Liquid
  - JavaScript
  - Python
  - GitHub Actions
created: 2026-08-05
updated: 2026-08-05
last_verified: 2026-08-05
order: 30
related:
  - /projects/high-director/site-rebuild-plan/
  - /docs/runbooks/documentation-site-operations/
---

# Documentation Site Architecture

## Purpose

The site is a version-controlled technical knowledge base for Eire Politic repositories, systems, data, operations, architecture decisions, and High Director-assisted development.

Its primary purpose is development continuity and technical reference. Public presentation and portfolio value are secondary outcomes.

## Hosting and build

- Repository: `eirepolitic.github.io`
- Default branch: `main`
- Hosting: GitHub Pages
- Static-site generator: Jekyll
- Primary content format: Markdown
- Deployment: GitHub Pages workflow after changes reach `main`

No database, application server, Lambda function, or external search service is required.

## Content model

Published technical documentation lives in `_docs/` as a Jekyll collection.

Top-level sections are defined in `_data/docs_sections.yml`:

- Repositories
- Systems
- Data and Schemas
- Runbooks
- Architecture Decisions
- High Director
- Notes
- Archive

Each document uses standardized front matter defined in `DOCUMENTATION_STANDARD.md`.

## Rendering model

- `_layouts/default.html` provides the global site shell.
- `_layouts/docs.html` renders technical documents.
- `_layouts/docs-section.html` renders section landing pages.
- `_includes/docs-nav.html` generates documentation navigation.
- `assets/css/site.css` contains the primary design system.
- `assets/css/search.css` and `assets/css/indexes.css` contain feature-specific styles.
- `assets/js/site.js` builds the on-page table of contents.
- `assets/js/search.js` runs browser-based documentation search.

## Navigation and discovery

Navigation and indexes are generated from document metadata rather than physical folder-name checks.

Discovery features include:

- section navigation and counts
- section landing pages
- full-text client-side search
- repository, technology, type, status, and recent-update indexes
- explicit related-document metadata
- automatic same-repository relationships
- recently updated content on the homepage

## Search architecture

Jekyll generates `/search-index.json` from public documents in `_docs/`.

The browser loads that file and ranks matches across titles, summaries, repositories, sections, types, statuses, technologies, tags, and page text.

The search requires no API, database, account, or paid service.

## Quality controls

`scripts/validate_docs.py` validates:

- required front matter
- allowed sections, document types, and statuses
- date formats
- archive requirements
- duplicate permalinks
- local links and assets
- explicit related URLs

`.github/workflows/validate-documentation.yml` runs the validator on relevant pull requests and by manual dispatch.

## Security model

The site is public. Secrets, credentials, private keys, tokens, session data, and confidential material must never be committed.

The `visibility` field controls generated listings and search inclusion, but it is not a security boundary because committed content remains in repository history.

## Change-management model

Material changes should follow this path:

1. Create a branch from `main`.
2. Make focused changes.
3. Open a pull request.
4. Confirm validation passes.
5. Merge into `main`.
6. Confirm the Pages deployment succeeds.
7. Verify affected live pages.

## Continuation model

Future development should begin by reading:

1. `DOCUMENTATION_STANDARD.md`
2. Documentation Site Operations
3. Documentation Site Rebuild Plan
4. The latest merged pull requests

The next safe action should be recorded in relevant system or repository documentation before a development session ends.
