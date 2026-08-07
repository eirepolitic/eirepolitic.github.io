---
title: Documentation Validation Compatibility Findings
summary: Working note recording validator status-vocabulary and permalink findings observed while publishing the documentation examples.
section: notes
doc_type: note
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
repository: eirepolitic.github.io
system: Eire Politic Documentation Site
order: 10
permalink: /projects/notes/documentation-validation-findings/
tags:
  - validation
  - working-note
related:
  - /projects/high-director/example-documents-plan/
  - /projects/runbooks/publish-documentation-change/
---

# Documentation Validation Compatibility Findings

## Purpose

Record practical findings discovered while creating and validating the real documentation examples so future documentation work can avoid repeating the same compatibility mistakes. This note is supporting working knowledge; the validator, Jekyll configuration, and documentation standard remain authoritative.

## Scope

Covers two observed documentation-site behaviors in `eirepolitic.github.io`:

- front-matter lifecycle status compatibility with `scripts/validate_docs.py`;
- default versus explicit documentation permalinks under the Jekyll `docs` collection.

It does not define new metadata values or URL architecture.

## Confidence and Status

- Confidence: high
- Current state: verified observation
- Last verified: `2026-08-06`
- Verification source: `scripts/validate_docs.py`, `_config.yml`, PR validation runs, and affected documentation files

## Source of Truth

- Repository: `eirepolitic.github.io`
- Allowed status values: `scripts/validate_docs.py`
- Jekyll collection permalink rule: `_config.yml`
- Metadata guidance: `DOCUMENTATION_STANDARD.md`
- Publishing procedure: `/projects/runbooks/publish-documentation-change/`

If this note conflicts with those files, the current repository implementation and documentation standard govern.

## Observations

### `complete` is not a valid front-matter status

During the template-initiative completion update, the plan was initially changed to `status: complete`. Documentation validation failed because `scripts/validate_docs.py` allows only:

- `planned`
- `active`
- `paused`
- `deprecated`
- `archived`
- `unknown`

The plan was corrected to retain `status: active` while recording initiative completion explicitly in document content. The corrected validation run `31137183234` succeeded.

### Default documentation URLs follow the collection path

`_config.yml` defines the `docs` collection permalink as `/docs/:path/`. A document without its own explicit `permalink` therefore uses its collection path.

This mattered during PR #20: a related link to the existing site architecture page was initially written as `/projects/high-director/site-architecture/`, but `_docs/high-director/site-architecture.md` has no explicit permalink. The validator rejected that reference. Changing it to `/docs/high-director/site-architecture/` allowed validation run `31137389854` to pass.

### Explicit permalinks override the default pattern

New example documents can intentionally use stable `/projects/.../` URLs because they declare explicit `permalink` values in front matter. Link targets should be derived from the target document's actual front matter and collection rules, not inferred from its category name alone.

## Assumptions and Open Questions

No open question currently blocks documentation work. If the allowed status vocabulary or collection permalink configuration changes, this note must be reverified before its observations are reused.

## Working Guidance

Before adding a lifecycle status or internal documentation link:

1. Check `scripts/validate_docs.py` for the currently allowed status vocabulary.
2. Open the target document and check for an explicit `permalink`.
3. If no explicit permalink exists, apply the collection rule from `_config.yml`.
4. Run documentation validation before merge.

Do not add a new metadata value or alter URL architecture merely to make a document read more naturally.

## Security Considerations

These findings require no secrets. Do not include workflow credentials, tokens, private repository information, or sensitive values when recording validation evidence.

## Known Limitations

- The observations describe the current repository implementation, not a universal Jekyll rule set.
- Workflow run IDs are historical evidence and do not replace checking current code.
- The note is intentionally narrower than the documentation standard and operations runbook.

## Promotion Criteria

Promote a finding into authoritative documentation only if it represents a durable rule that is not already clear in `DOCUMENTATION_STANDARD.md`, `_config.yml`, or the validator. No promotion is currently required because the authoritative implementation already defines both behaviors.

## Outstanding Work

Reverify this note if the validator's allowed statuses, Jekyll collection configuration, or permalink conventions change.

## Next Safe Action

Inspect `_templates/archive-template.md` and one existing real document under `_docs/archive/`, then refine only factual gaps supported by the archived record itself.

## Related Documents

- [Example Documents Phase](/projects/high-director/example-documents-plan/) records the initiative where these findings were observed.
- [Publish a Documentation Change](/projects/runbooks/publish-documentation-change/) gives the authoritative publishing procedure.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: `scripts/validate_docs.py`, `_config.yml`, `_docs/high-director/site-architecture.md`, PR #19 validation run `31137183234`, and PR #20 validation run `31137389854`
- Verified by: High Director
- Verification scope: allowed status vocabulary, failed `complete` status, collection permalink pattern, explicit permalink behavior, and corrected architecture link
- Unverified areas: none within the stated scope
