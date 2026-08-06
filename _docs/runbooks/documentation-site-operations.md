---
title: Documentation Site Operations
summary: Procedures for creating, editing, publishing, validating, archiving, and troubleshooting the documentation site.
section: runbooks
doc_type: runbook
status: active
repository: eirepolitic.github.io
technologies:
  - GitHub Pages
  - Jekyll
  - Markdown
  - GitHub Actions
  - Python
created: 2026-08-05
updated: 2026-08-05
last_verified: 2026-08-05
order: 10
related:
  - /projects/high-director/site-rebuild-plan/
  - /projects/high-director/
---

# Documentation Site Operations

## Purpose

Use this runbook to maintain the Eire Politic technical knowledge base and safely continue site development in a future chat.

## Source of truth

- Repository: `eirepolitic.github.io`
- Default branch: `main`
- Documentation collection: `_docs/`
- Documentation standard: `DOCUMENTATION_STANDARD.md`
- Templates: `_templates/`
- Section definitions: `_data/docs_sections.yml`
- Site configuration: `_config.yml`
- Documentation validator: `scripts/validate_docs.py`
- Validation workflow: `.github/workflows/validate-documentation.yml`
- Publishing: GitHub Pages from `main`

## Create a document

1. Select the correct template from `_templates/`.
2. Create the Markdown file under the matching `_docs/` section.
3. Use lowercase kebab-case for the filename.
4. Complete every required front matter field.
5. Add exact repository names, paths, workflows, services, and regions where relevant.
6. Do not include secret values.
7. Add `last_verified` only when the documented implementation was checked against its source of truth.
8. Add `related` URLs when explicit relationships are useful.
9. Run validation before merging.

Example path:

```text
_docs/repositories/example-repository.md
```

## Edit an existing document

1. Locate the authoritative page in `_docs/`.
2. Check its `status`, `updated`, and `last_verified` values.
3. Change only verified implementation facts or clearly label proposed work.
4. Set `updated` to the date of the meaningful content change.
5. Change `last_verified` only when the source system was checked.
6. Preserve the permalink unless an intentional migration is required.
7. Validate and review the rendered site after publishing.

## Publish changes

Use a branch and pull request for material changes.

1. Create a branch from `main`.
2. Make the documentation and supporting code changes.
3. Update the persistent rebuild plan when completing a planned site step.
4. Open a pull request into `main`.
5. Confirm the documentation validation workflow passes.
6. Merge the pull request.
7. Confirm the GitHub Pages deployment completes successfully.
8. Check the affected live URLs.

## Run validation

GitHub Actions runs validation automatically on relevant pull requests.

To run it locally:

```bash
python -m pip install PyYAML==6.0.2
python scripts/validate_docs.py
```

The validator checks:

- required metadata
- allowed sections, document types, and statuses
- ISO date formatting
- archive metadata
- duplicate permalinks
- internal links and assets
- related-document URLs

Do not merge a failing validation run unless the validator itself is being corrected and the replacement behavior is understood.

## Navigation behavior

Navigation is generated from `_data/docs_sections.yml` and document front matter.

- `section` determines the primary navigation category.
- `order` controls document order within a section.
- Section document counts are generated automatically.
- A new top-level section requires an entry in `_data/docs_sections.yml` and a landing page under `docs/`.
- Do not build navigation by checking physical folder substrings.

## Search behavior

The site builds `/search-index.json` from public documents in `_docs/`.

Search includes:

- title
- summary
- repository
- section
- document type
- status
- technologies
- tags
- page content

Documents with `visibility: private` are excluded from the generated index and published lists. Do not rely on this field to protect committed secrets or sensitive material; excluded content still exists in repository history if committed.

## Archive a document

1. Move the source file into `_docs/archive/`.
2. Set `section: archive`.
3. Set `status: archived`.
4. Add `archived_date`.
5. Add `archive_reason`.
6. Add `superseded_by` when a replacement exists.
7. Preserve the public permalink where practical.
8. Validate related links and navigation.

Archived documentation remains readable and searchable by default.

## Change a public URL

Avoid changing established URLs.

When a change is necessary:

1. Add an explicit `permalink` to the new authoritative page.
2. Preserve the old URL with a compatibility or redirect page where practical.
3. Update related metadata and internal links.
4. Run the duplicate permalink and broken-link checks.
5. Verify both the new page and compatibility path after deployment.

## Troubleshooting

### GitHub Pages build fails

1. Open the latest Pages workflow run.
2. Inspect the failed job and build log.
3. Check `_config.yml`, Liquid syntax, front matter, and layout references first.
4. Correct the issue on a branch and merge through a pull request.

### Documentation validation fails

1. Read each validator error from the workflow log.
2. Correct the referenced file and field.
3. Rerun the workflow through a new commit or manual dispatch.
4. Change the validator only when the rule is incorrect, not to bypass valid errors.

### A page is missing from navigation

Check:

- the file is under `_docs/`
- `section` uses an allowed value
- `visibility` is not `private`
- the document contains valid front matter
- the section exists in `_data/docs_sections.yml`

### Search does not find a page

Check:

- the page is in `_docs/`
- `visibility` is not `private`
- `/search-index.json` contains the page
- the latest Pages deployment succeeded
- browser caching is not serving an older index

### Styling or JavaScript does not update

1. Confirm the asset change reached `main`.
2. Confirm the Pages deployment completed.
3. Reload without cache.
4. Check browser developer tools for missing assets or JavaScript errors.

## Continue development in a new chat

1. Read `/projects/high-director/site-rebuild-plan/`.
2. Inspect the latest merged pull requests.
3. Read `DOCUMENTATION_STANDARD.md`.
4. Read this runbook.
5. Continue from the first rebuild step not marked `Complete`.
6. Use the exact repository name `eirepolitic.github.io` for repository actions.
7. Update the rebuild plan in the same pull request as the completed step.
8. Verify validation and Pages deployment before reporting completion.

## Security considerations

- Never commit passwords, tokens, secret values, private keys, or temporary credentials.
- Document secret names and purposes only.
- Treat all GitHub Pages output as public.
- Review S3 paths, account identifiers, personal data, and infrastructure details before publication.
- Removing a file from the site does not remove it from Git history.
