---
title: Use Metadata-Driven Static Documentation on GitHub Pages
summary: Retain a metadata-driven Jekyll documentation system on GitHub Pages instead of adding an application backend or external search service.
section: decisions
doc_type: decision
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: Eire Politic
repository: eirepolitic.github.io
system: Eire Politic Documentation Site
order: 10
permalink: /projects/decisions/use-metadata-driven-static-documentation/
tags:
  - architecture
  - github-pages
related:
  - /projects/systems/documentation-site/
  - /projects/repositories/eirepolitic-github-io/
  - /docs/high-director/site-architecture/
---

# Use Metadata-Driven Static Documentation on GitHub Pages

## Decision Status

- Decision state: accepted
- Decision date: `2026-08-05`
- Effective date: `2026-08-05`
- Owners or approvers: Eire Politic
- Superseded by: None

This record documents an architecture choice already implemented in the documentation site.

## Summary

The documentation system uses Jekyll, Markdown, Liquid, repository metadata, browser JavaScript, GitHub Actions, and GitHub Pages. Navigation, indexes, relationships, and search are derived from committed metadata and static content rather than an application server, database, or external search service.

## Context

The technical knowledge base needs version-controlled documentation, generated navigation, full-text discovery, validation, and reliable public publishing. The implemented site in `eirepolitic.github.io` already provides those capabilities through static files and GitHub-hosted tooling.

The architecture recorded in `_docs/high-director/site-architecture.md` explicitly states that no database, application server, Lambda function, or external search service is required.

## Decision Drivers

1. Keep documentation version-controlled with the implementation history.
2. Minimize operating cost and infrastructure burden.
3. Avoid unnecessary services, credentials, and deployment surfaces.
4. Generate navigation and discovery from standardized metadata rather than duplicated manual indexes.
5. Support automated validation before publication.
6. Keep the system easy to continue from repository source alone.

## Decision

Retain the following architecture:

- Store published technical documentation in `_docs/` as a Jekyll collection.
- Define top-level categories in `_data/docs_sections.yml`.
- Govern document metadata through `DOCUMENTATION_STANDARD.md`.
- Generate navigation and indexes from document metadata.
- Generate `/search-index.json` during the Jekyll build and perform search in `assets/js/search.js`.
- Validate documentation with `scripts/validate_docs.py` and `.github/workflows/validate-documentation.yml`.
- Publish from `main` through GitHub Pages.
- Do not introduce a database, application backend, Lambda function, or external search service unless a future requirement cannot be satisfied safely by the static model.

## Source of Truth

- Decision record: `/projects/decisions/use-metadata-driven-static-documentation/`
- Primary repository: `eirepolitic.github.io`
- Site configuration: `_config.yml`
- Section definitions: `_data/docs_sections.yml`
- Search generator: `search-index.json`
- Search consumer: `assets/js/search.js`
- Documentation validator: `scripts/validate_docs.py`
- Validation workflow: `.github/workflows/validate-documentation.yml`
- Architecture record: `_docs/high-director/site-architecture.md`

The committed implementation governs current behavior if this record and source code ever diverge.

## Alternatives Considered

### Application-backed documentation service

- Description: Run a web application and persistent datastore for documentation and discovery.
- Benefits: Could support server-side search, dynamic permissions, and richer application behavior.
- Drawbacks: Adds hosting, deployment, monitoring, security, credentials, and operating complexity.
- Rejection reason: Current documentation requirements are met by static generation without those dependencies.

### External hosted search service

- Description: Publish documentation content to a separate indexing/search platform.
- Benefits: Could provide advanced ranking and larger-scale search features.
- Drawbacks: Adds an external dependency, configuration, possible cost, synchronization, and another data exposure boundary.
- Rejection reason: The generated client-side index meets the present search requirement.

### Manually maintained navigation and indexes

- Description: Maintain section lists and cross-document indexes by hand.
- Benefits: Simple implementation for a very small site.
- Drawbacks: Duplicates metadata, increases drift risk, and requires repeated maintenance.
- Rejection reason: Metadata-driven generation is already implemented and reduces duplication.

## Consequences

### Positive

- Repository history remains the primary continuity mechanism.
- Publishing uses existing GitHub Pages infrastructure.
- Search requires no external account or paid service.
- Standard metadata can drive navigation, indexes, relationships, and validation.
- Fewer runtime services reduce operational and security surface area.

### Negative

- Search is browser-side and limited to the generated index and client logic.
- Dynamic authorization is not available; the published site is public.
- Availability depends on GitHub-hosted repository, Actions, and Pages services.

### Neutral or Follow-on

Documentation quality depends on maintaining accurate front matter, validation rules, templates, and source documents.

## Security and Privacy

The static architecture reduces credential-bearing runtime services but does not make committed content private. GitHub Pages output and repository history must be treated as public. `visibility: private` may exclude a document from generated listings and search but is not a security boundary.

## Implementation State

The decision is implemented on `main`:

- Jekyll collection configuration exists in `_config.yml`.
- Section metadata exists in `_data/docs_sections.yml`.
- Metadata-driven layouts and navigation are active.
- `/search-index.json` is generated from public documentation.
- Browser-side search is implemented in `assets/js/search.js`.
- Documentation validation runs through GitHub Actions.
- GitHub Pages builds and deploys merged changes.

## Validation and Review

Retain this decision while:

- Documentation validation continues to pass.
- GitHub Pages builds and deploys reliably.
- Client-side search remains adequate for the corpus.
- No requirement emerges for authenticated/private content, server-side processing, or search capability that materially exceeds the static model.

Revisit the decision if one of those conditions changes.

## Failure Modes and Reversal

- GitHub Pages outage: wait for service recovery; no alternate runtime is currently maintained.
- Search index becomes too large or inadequate: evaluate a replacement search architecture before adding an external dependency.
- Requirement for genuinely private documentation: do not rely on the current public repository; make a separate security and architecture decision.

Reversal would require a separately reviewed migration plan because it would add infrastructure, operational ownership, and potentially cost or security implications.

## Known Limitations

- No server-side search or dynamic application logic.
- No authenticated document access in the public site.
- Search quality is constrained by the current client-side scoring implementation.
- GitHub-hosted services are external dependencies.

## Outstanding Work

No architecture change is required by the Example Documents phase. Future changes should be driven by a concrete unmet requirement rather than template completion.

## Next Safe Development Action

Review the persistent Example Documents phase plan against `_templates/high-director-template.md` and use that real plan as the High Director category example, changing only concrete gaps exposed by the comparison.

## Related Documents

- [Eire Politic Documentation Site](/projects/systems/documentation-site/) describes the implemented system boundary.
- [eirepolitic.github.io](/projects/repositories/eirepolitic-github-io/) describes the implementing repository.
- [Documentation Site Architecture](/docs/high-director/site-architecture/) records the established architecture and maintenance model.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: `main`, `_config.yml`, `_data/docs_sections.yml`, `search-index.json`, `assets/js/search.js`, `scripts/validate_docs.py`, `.github/workflows/validate-documentation.yml`, `_docs/high-director/site-architecture.md`, and successful Pages deployment `31137754183`
- Verified by: High Director
- Verification scope: decision status, static system boundary, search implementation, validation implementation, publishing path, alternatives, and review triggers
