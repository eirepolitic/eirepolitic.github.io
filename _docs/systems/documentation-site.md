---
title: Eire Politic Documentation Site
summary: Public GitHub Pages system that renders, validates, indexes, and publishes the Eire Politic technical knowledge base.
section: systems
doc_type: system
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: Eire Politic
system: Eire Politic Documentation Site
repository: eirepolitic.github.io
order: 10
permalink: /projects/systems/documentation-site/
technologies:
  - GitHub Pages
  - Jekyll
  - Markdown
  - Liquid
  - JavaScript
  - Python
  - GitHub Actions
related:
  - /projects/repositories/eirepolitic-github-io/
  - /docs/high-director/site-architecture/
  - /docs/runbooks/documentation-site-operations/
---

# Eire Politic Documentation Site

## Summary

The Eire Politic Documentation Site is the public technical knowledge-base system for repositories, systems, data, runbooks, architecture decisions, High Director work, notes, and archived material. It is implemented entirely in `eirepolitic.github.io` and published through GitHub Pages.

## Current Implementation State

The system is active on `main`. Jekyll renders committed Markdown and site assets, GitHub Actions validates documentation metadata and references, and GitHub Pages builds and deploys the published site after merges.

No application server, database, Lambda function, external search service, or paid search dependency is part of the current system.

## System Boundary

Included:

- `eirepolitic.github.io` repository content and configuration.
- Jekyll collection rendering for `_docs/`.
- Metadata-driven navigation and indexes.
- Client-side documentation search using generated `search-index.json`.
- Documentation validation through GitHub Actions.
- GitHub Pages build and deployment.

Excluded:

- Source systems documented by the site.
- Private credential stores or secret-management systems.
- External application backends.

## Source of Truth

| Concern | Authoritative source | Exact location |
| --- | --- | --- |
| Repository content | `eirepolitic.github.io` | `main` |
| Site configuration | `eirepolitic.github.io` | `_config.yml` |
| Documentation metadata | `eirepolitic.github.io` | `DOCUMENTATION_STANDARD.md` |
| Section model | `eirepolitic.github.io` | `_data/docs_sections.yml` |
| Validation | `eirepolitic.github.io` | `scripts/validate_docs.py` and `.github/workflows/validate-documentation.yml` |
| Operations | Documentation Site Operations | `/docs/runbooks/documentation-site-operations/` |

## Architecture

1. Authors commit Markdown, YAML, HTML, CSS, JavaScript, and assets to a feature branch.
2. Pull requests run documentation validation for relevant changes.
3. Approved changes merge into `main`.
4. GitHub Pages invokes the Jekyll build.
5. Jekyll renders the site and generated indexes, including `/search-index.json`.
6. GitHub Pages deploys the static output.
7. Browser JavaScript provides search and page-navigation behavior.

The system has a public trust boundary: anything committed may become publicly retrievable through repository history even when excluded from generated listings.

## Components and Repositories

- `eirepolitic.github.io`: sole repository and source of truth.
- `_docs/`: published technical documentation collection.
- `_layouts/` and `_includes/`: rendering and shared navigation.
- `_data/docs_sections.yml`: top-level category definitions.
- `assets/js/search.js`: client-side documentation search.
- `assets/js/site.js`: page navigation behavior.
- `scripts/validate_docs.py`: documentation metadata and reference validation.
- `.github/workflows/validate-documentation.yml`: pull-request and manual validation workflow.
- GitHub Pages: build and deployment platform.

## Inputs and Outputs

### Inputs

Committed repository files, primarily Markdown documentation and YAML metadata. Inputs must avoid secrets and conform to repository validation rules.

### Outputs

A public static website, generated documentation indexes, and `/search-index.json` for client-side search.

## Dependencies

Critical dependencies are GitHub repository hosting, GitHub Actions, GitHub Pages, Jekyll, Python, and `PyYAML==6.0.2` for documentation validation.

## Configuration

Primary configuration is stored in `_config.yml`, `_data/docs_sections.yml`, `DOCUMENTATION_STANDARD.md`, and `.github/workflows/validate-documentation.yml`. No secret values are required by the documented build, validation, or publishing path.

## Deployment and Environments

The verified environment is the public GitHub Pages site built from `main`. Material changes are merged through pull requests after documentation validation. GitHub Pages then builds and deploys the merged commit. A failed deployment is corrected on a new branch and revalidated before merge.

## Operation and Monitoring

Operational evidence comes from pull-request validation checks and GitHub Pages workflow runs. Routine operations, troubleshooting, and publishing procedures are documented in [Documentation Site Operations](/docs/runbooks/documentation-site-operations/).

## Validation

Validation includes:

- `python scripts/validate_docs.py` for metadata and reference checks.
- GitHub Actions validation on relevant pull requests.
- GitHub Pages build success after merge.
- GitHub Pages deployment success after build.
- Live-page verification for affected documentation.

## Failure Modes and Recovery

- Validator failure: correct the referenced metadata or broken link, then rerun validation.
- Jekyll build failure: inspect `_config.yml`, Liquid, front matter, layouts, and the Pages build log.
- Deployment failure after successful build: inspect the deploy job and retry only after the underlying issue is understood.
- Missing navigation or search content: verify section metadata, visibility, generated indexes, and the latest deployment.

## Security and Access

The site and repository are public. Credentials, tokens, private keys, session data, secret values, personal data, and confidential identifiers must not be committed. `visibility` controls generated listings, not repository-history access.

## Known Limitations

- Availability depends on GitHub Pages and GitHub-hosted infrastructure.
- Search is browser-side and depends on the generated index.
- No separately verified local Jekyll preview procedure is currently part of the operating standard.

## Outstanding Work

The Example Documents phase is documenting remaining categories using this live system and related real work.

## Next Safe Development Action

Create the Data & Schema example for the generated documentation search index or metadata model, using exact committed source files and generated fields as the evidence base, then run `python scripts/validate_docs.py`.

## Related Documents

- [eirepolitic.github.io](/projects/repositories/eirepolitic-github-io/) is the repository implementing this system.
- [Documentation Site Architecture](/docs/high-director/site-architecture/) records the established architecture and maintenance model.
- [Documentation Site Operations](/docs/runbooks/documentation-site-operations/) is the operating runbook.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: `main`, `_config.yml`, repository tree, architecture document, validation workflow, validator, and successful Pages deployment `31137413142`
- Verified by: High Director
- Verification scope: system boundary, components, build flow, validation path, deployment path, search architecture, and security model
