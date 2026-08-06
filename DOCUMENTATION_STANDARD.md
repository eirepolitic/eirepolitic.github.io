# Documentation Standard

This standard defines how technical documentation is created and maintained for the Eire Politic knowledge base.

## Purpose

Documentation must support:

1. continuing development after time away;
2. reconstructing prior decisions and system state;
3. operating and troubleshooting repositories and services;
4. presenting clear evidence of completed technical work.

## Required front matter

Every published technical document must include:

```yaml
---
title: Human-readable title
summary: One-sentence description
section: repositories
page_type: repository
status: active
created: 2026-08-05
updated: 2026-08-05
---
```

Allowed `section` values:

- `repositories`
- `systems`
- `data`
- `runbooks`
- `decisions`
- `high-director`
- `notes`
- `archive`

Allowed `page_type` values:

- `repository`
- `system`
- `pipeline`
- `schema`
- `runbook`
- `decision`
- `agent`
- `reference`
- `note`

Allowed `status` values:

- `planned`
- `active`
- `paused`
- `deprecated`
- `archived`

Dates use ISO format: `YYYY-MM-DD`.

## Optional front matter

Use these fields when applicable:

```yaml
repository: repository-name
technologies:
  - Python
  - AWS Lambda
tags:
  - ingestion
  - automation
source_path: path/in/repository.py
source_url: https://github.com/example/example
aws_region: eu-west-1
owners:
  - eirepolitic
order: 10
last_verified: 2026-08-05
superseded_by: /docs/example/
archive_reason: Replaced by a newer implementation.
related:
  - /docs/related-page/
```

Never store credentials, tokens, private keys, secret values, or sensitive personal data.

## Naming and URLs

- File names use lowercase kebab case: `member-images-pipeline.md`.
- Prefer stable, descriptive permalinks.
- Avoid dates in URLs unless the document is inherently chronological.
- Renames must preserve the old URL through a redirect or compatibility page where practical.
- Repository names, paths, workflow names, AWS resources, and configuration keys must be written exactly.

## Standard document structure

Use the sections that apply:

1. Overview
2. Current state
3. Source of truth
4. Architecture
5. Inputs and outputs
6. Dependencies
7. Configuration
8. How to run
9. Validation
10. Failure modes
11. Security considerations
12. Known limitations
13. How to continue development
14. Related documentation

Do not add empty sections.

## Writing rules

- Describe completed work separately from proposed work.
- Prefer exact paths, commands, resource names, and configuration keys.
- State assumptions explicitly.
- Keep operational instructions ordered and testable.
- Explain why important design choices were made.
- Record the last date a process was verified.
- Use concise language and short paragraphs.

## Archive rules

Archived documents must include:

```yaml
status: archived
section: archive
archived_date: 2026-08-05
archive_reason: Reason for retirement.
```

Add `superseded_by` when a replacement exists. Archived pages may remain searchable and must clearly display their archived status.

## Architecture decision records

Decision pages should contain:

- context;
- decision;
- alternatives considered;
- consequences;
- status;
- date.

Do not rewrite old decisions to match later outcomes. Add a superseding decision instead.

## Maintenance

- Update `updated` whenever material content changes.
- Update `last_verified` only after checking the documented process or resource.
- Review active operational pages when related implementation changes.
- Move obsolete material to Archive rather than deleting useful history.
