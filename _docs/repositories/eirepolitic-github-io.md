---
title: eirepolitic.github.io
summary: GitHub Pages repository that publishes and validates the Eire Politic technical documentation site.
section: repositories
doc_type: repository
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: Eire Politic
repository: eirepolitic.github.io
order: 10
permalink: /projects/repositories/eirepolitic-github-io/
technologies:
  - GitHub Pages
  - Jekyll
  - Markdown
  - Liquid
  - JavaScript
  - Python
  - GitHub Actions
related:
  - /projects/high-director/site-architecture/
  - /docs/runbooks/documentation-site-operations/
---

# eirepolitic.github.io

## Summary

`eirepolitic.github.io` is the source repository for the Eire Politic technical knowledge base. It stores the Jekyll site, technical documentation, templates, validation tooling, and publishing configuration used by GitHub Pages.

## Current Implementation State

- Default branch: `main`.
- Published through GitHub Pages after changes reach `main`.
- Technical documentation is stored in `_docs/` and rendered as a Jekyll collection.
- Documentation validation runs through `.github/workflows/validate-documentation.yml`.
- The repository currently supports eight top-level documentation categories defined in `_data/docs_sections.yml`.

## Source of Truth

- Repository: `eirepolitic.github.io`
- Site configuration: `_config.yml`
- Technical documentation: `_docs/`
- Documentation templates: `_templates/`
- Section definitions: `_data/docs_sections.yml`
- Documentation standard: `DOCUMENTATION_STANDARD.md`
- Validator: `scripts/validate_docs.py`
- Validation workflow: `.github/workflows/validate-documentation.yml`
- Site layouts: `_layouts/`
- Shared navigation: `_includes/docs-nav.html`

## Repository Structure

```text
eirepolitic.github.io/
├── .github/workflows/          # Documentation validation workflow
├── _data/                      # Documentation section metadata
├── _docs/                      # Published technical documentation
├── _includes/                  # Shared Jekyll includes
├── _layouts/                   # Jekyll page layouts
├── _templates/                 # Documentation authoring templates
├── assets/                     # Site CSS, JavaScript, and images
├── docs/                       # Documentation landing and index pages
├── scripts/                    # Documentation validation tooling
├── _config.yml                 # Jekyll and collection configuration
└── DOCUMENTATION_STANDARD.md   # Documentation metadata and authoring standard
```

## Inputs and Outputs

### Inputs

The primary inputs are committed Markdown, YAML, HTML, CSS, JavaScript, and image assets. Documentation metadata must conform to `DOCUMENTATION_STANDARD.md` and the rules enforced by `scripts/validate_docs.py`.

### Outputs

GitHub Pages publishes the rendered static site from `main`. Jekyll also generates `/search-index.json` from public technical documentation for client-side search.

## Dependencies

- GitHub Pages for hosting and deployment.
- Jekyll for static-site generation.
- GitHub Actions for documentation validation.
- Python and `PyYAML==6.0.2` for `scripts/validate_docs.py`.
- Browser JavaScript for search and page navigation behavior.

## Configuration

| Name | Location | Purpose | Required |
| --- | --- | --- | --- |
| Jekyll site configuration | `_config.yml` | Defines the site, docs collection, defaults, and header pages | Yes |
| Documentation sections | `_data/docs_sections.yml` | Defines top-level documentation categories and navigation metadata | Yes |
| Documentation metadata rules | `DOCUMENTATION_STANDARD.md` | Defines allowed front matter and authoring requirements | Yes |
| Validation workflow | `.github/workflows/validate-documentation.yml` | Runs documentation validation on relevant changes and manual dispatch | Yes |

No secret values are required by the documented publishing or validation path.

## Local Development

The verified local validation path is:

```bash
python -m pip install PyYAML==6.0.2
python scripts/validate_docs.py
```

A local Jekyll preview command is not currently documented as a verified repository requirement.

## Deployment and Release

Material changes follow this path:

1. Create a branch from `main`.
2. Make a focused change.
3. Open a pull request.
4. Confirm documentation validation passes.
5. Merge into `main`.
6. Confirm the GitHub Pages build and deployment succeed.
7. Verify the affected live pages.

GitHub Pages deployment is the authoritative publishing mechanism; the repository does not contain a custom Pages deployment workflow.

## Validation

`scripts/validate_docs.py` checks required metadata, allowed sections, document types and statuses, date formats, archive metadata, duplicate permalinks, local references, and related URLs.

The validator is run by `.github/workflows/validate-documentation.yml` and can also be executed locally.

## Operations

Operational procedures are documented in [Documentation Site Operations](/docs/runbooks/documentation-site-operations/). Routine maintenance includes validating documentation changes, monitoring pull-request checks, confirming Pages deployments, and verifying live pages after merged changes.

## Failure Modes

- Documentation validation failure: inspect the validation run and correct the referenced document or validator rule.
- Pages build failure: inspect the Pages workflow, then check `_config.yml`, Liquid syntax, front matter, and layout references.
- Missing navigation or search results: verify document metadata, section definitions, visibility, generated indexes, and the latest Pages deployment.

## Security and Access

The published site is public. Do not commit credentials, tokens, private keys, session data, secret values, or confidential material. `visibility` affects generated listings and search but is not a security boundary because committed content remains in repository history.

## Known Limitations

- The repository relies on GitHub Pages and GitHub-hosted build infrastructure.
- Search is client-side and depends on the generated `search-index.json`.
- Local Jekyll preview steps are not currently verified in repository documentation.

## Outstanding Work

The Example Documents phase is now using this repository as the real repository-category example. Other documentation categories still require their own real examples.

## Next Safe Development Action

Create the system-category example for the documentation site using the verified architecture in `_docs/high-director/site-architecture.md`, then run `python scripts/validate_docs.py` before opening or updating the pull request.

## Related Documents

- [Documentation Site Architecture](/projects/high-director/site-architecture/) describes the system-level design and rendering model.
- [Documentation Site Operations](/docs/runbooks/documentation-site-operations/) contains operating and troubleshooting procedures.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: `main`, `_config.yml`, repository tree, documentation architecture, operations runbook, validator, validation workflow, and successful Pages deployment `31137199965`
- Verified by: High Director
- Verification scope: repository structure, publishing path, documentation collection, validation path, dependencies, and security model
