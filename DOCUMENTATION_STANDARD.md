# Documentation Standard

This standard defines how technical documentation is created, organized, maintained, and archived for the Eire Politic knowledge base.

## Purpose

Documentation must support two primary uses:

1. Help the site owner review, operate, troubleshoot, and continue development.
2. Give High Director enough structured context to safely resume previous work.

Public readability and portfolio value are secondary benefits.

## Required front matter

Every published technical document must include:

```yaml
---
title: Clear human-readable title
summary: One-sentence description of the document
section: repositories
doc_type: repository
status: active
updated: 2026-08-05
---
```

Required fields:

- `title`: Unique, descriptive page title.
- `summary`: One sentence describing purpose or scope.
- `section`: Top-level navigation section.
- `doc_type`: Type of document.
- `status`: Lifecycle state.
- `updated`: Last meaningful content update in `YYYY-MM-DD` format.

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
created: 2026-08-05
last_verified: 2026-08-05
owner: eirepolitic
source_path: src/example.py
workflow: .github/workflows/example.yml
aws_region: eu-west-1
order: 10
permalink: /docs/example/
related:
  - /docs/related-page/
archived_date: 2026-08-05
superseded_by: /docs/new-page/
archive_reason: Replaced by a new implementation.
visibility: public
```

## Allowed sections

- `repositories`
- `systems`
- `data`
- `runbooks`
- `decisions`
- `high-director`
- `notes`
- `archive`

## Allowed document types

- `repository`: Overview of one GitHub repository.
- `system`: A service or capability spanning repositories or platforms.
- `pipeline`: A data-processing workflow.
- `schema`: A data model, table, file format, or contract.
- `runbook`: Operational instructions.
- `decision`: An architecture decision record.
- `agent`: High Director behavior, tools, access, or operating guidance.
- `reference`: General technical reference.
- `note`: Working knowledge that is useful but not yet formalized.

## Allowed statuses

- `planned`: Approved but not implemented.
- `active`: Current and in use.
- `paused`: Intentionally inactive but expected to resume.
- `deprecated`: Still present but should not be used for new work.
- `archived`: Historical or superseded.
- `unknown`: Current state has not been verified.

Do not use terms such as `done`, `live`, or `old` as lifecycle statuses.

## Classification rules

Classify a page by its **primary subject**, not by the tool, agent, person, or process that authored, coordinated, or executed the work.

Examples:

- A page about High Director configuration, capabilities, integrations, runtime architecture, security boundaries, implementation, or verification belongs in `high-director`.
- A repository-specific implementation page belongs in `repositories`, `systems`, `data`, `runbooks`, or another subject-appropriate section even when High Director created the page.
- An active documentation programme, repository scan, continuation plan, or coordination record that has not become formal system documentation belongs in `notes`.
- A completed or superseded workstream/discovery/build plan belongs in `archive` when it is retained for historical context.
- Documentation-site architecture belongs in `systems`, not `high-director`, because the documentation site is the subject.

High Director must not become a general bucket for projects merely because High Director performed the work.

## Naming conventions

- Use lowercase kebab-case filenames: `member-images-pipeline.md`.
- Use descriptive names instead of internal abbreviations.
- Keep one primary subject per page.
- Use ISO dates: `YYYY-MM-DD`.
- Keep repository names exact, including capitalization where relevant.

## URL conventions

- Prefer stable, readable URLs under `/docs/`.
- Do not include implementation folders such as `_docs` in public URLs.
- Preserve existing public URLs during migrations where practical.
- Add redirect pages when a public URL must change.
- Do not reuse a retired URL for unrelated content.

## Standard page structure

Use relevant sections from this order:

1. Overview
2. Current state
3. Source of truth
4. Architecture or workflow
5. Repositories and paths
6. Inputs and outputs
7. Dependencies
8. Configuration
9. How to run or operate
10. Validation
11. Failure modes
12. Security considerations
13. Known limitations
14. How to continue development
15. Related documentation

Omit sections that add no value. Do not add empty headings.

## Template usage

Use the category template under `_templates/` as the starting point for a new main documentation page.

- Templates are standards and guidance, not rigid forms.
- Remove guidance text, placeholders, and headings that add no value.
- Do not publish empty sections.
- Keep the main page complete for ordinary items.
- Create subordinate pages only when a topic has a separate owner or verification cycle, requires substantial procedure or reference detail, or makes the main page difficult to scan.
- Keep the main page authoritative for purpose, current implementation state, source-of-truth locations, dependencies, limitations, outstanding work, next safe action, and verification.
- Use stable internal links from the main page to subordinate pages and explain the relationship when it is not obvious.

## Writing rules

- State completed work as fact and proposed work as a proposal.
- Prefer exact repository names, paths, resource names, and workflow filenames.
- Explain acronyms on first use.
- Use commands and code blocks only when they are directly usable.
- Keep procedural steps in execution order.
- Record assumptions explicitly.
- Avoid marketing language.
- Never include passwords, tokens, private keys, session data, or secret values.
- Secret names and their purpose may be documented.

## Source-of-truth rules

Every operational page should identify where authoritative information lives. Examples:

- GitHub repository and file path
- GitHub Actions workflow
- AWS service and region
- S3 bucket and prefix
- Appsmith application
- Power BI workspace or report

Do not describe copied examples as authoritative configuration.

## Verification rules

Use `last_verified` when a page describes a deployed system, operational process, external service, or current configuration.

Verification means the documented behavior, location, or process was checked against the source of truth. Editing wording alone does not update `last_verified`.

## Archive rules

Archived documents must use:

```yaml
section: archive
status: archived
archived_date: 2026-08-05
archive_reason: Reason the document was archived.
```

Use `superseded_by` when a replacement exists.

Archived pages should remain readable and searchable unless they contain sensitive or misleading information. Add a visible archive notice in the page layout.

## Architecture decision records

Decision documents should include:

- Context
- Decision
- Alternatives considered
- Consequences
- Status
- Date

Do not rewrite old decisions to match later outcomes. Add a superseding decision instead.

## High Director continuation requirements

Pages intended to support future agent work should include:

- Exact repository name
- Exact relevant paths
- Current implementation state
- Known dependencies
- Completed work
- Outstanding work
- Next safe action
- Last verification date

These continuation requirements do not determine the page's navigation section. A continuation page about another repository or programme must still be classified by that page's primary subject and lifecycle.

## Review checklist

Before publishing:

- Required metadata is present.
- Status and document type use allowed values.
- The page is classified by its primary subject rather than by its author/coordinator.
- No secrets are included.
- Commands and paths are accurate.
- Completed and proposed work are clearly distinguished.
- Internal links use stable site URLs.
- The page states how to continue development when relevant.
