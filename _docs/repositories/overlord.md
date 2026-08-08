---
title: Overlord Repository and Markdown Task-Record System
summary: Source-grounded documentation for the current Overlord repository as a lightweight Markdown task-record store with work/personal partitions, YAML front matter, observed status conventions, fixture records, and no verified executable or cloud automation layer.
section: repositories
doc_type: repository
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: Overlord
---

# Overlord Repository and Markdown Task-Record System

## Purpose

`Overlord` is currently a lightweight Markdown repository for task records and reusable task/project/meeting skeletons.

The inspected repository does **not** contain a verified executable application, agent, API, cloud deployment, GitHub Actions workflow, external integration, database, or automation runtime. Its name must not be used to infer any of those capabilities.

## Repository maturity

The repository is structurally simple and early-stage:

- `README.md` contains only `# Overlord`;
- `tasks/work/` contains eight `test-task-*` fixture/example records;
- `tasks/personal/` is currently empty apart from `.gitkeep`;
- `templates/tasks/` contains three versioned Markdown templates;
- no code or validation tooling is present.

The current repository therefore behaves as a manually maintained Markdown record store rather than an application.

## Repository structure

```text
Overlord/
├── README.md
├── tasks/
│   ├── personal/
│   │   └── .gitkeep
│   └── work/
│       ├── .gitkeep
│       └── test-task-1.md ... test-task-8.md
└── templates/
    └── tasks/
        ├── .gitkeep
        ├── task_v1.md
        ├── project_v1.md
        └── meeting_v1.md
```

The `test-task-*` files are fixture/example data. They are not separate application components or documentation targets.

## Work/personal partition

Task records are partitioned by directory:

- `tasks/work/` — work-context task records;
- `tasks/personal/` — personal-context task records.

Observed work fixtures also contain front matter `context: "work"`, so directory and metadata currently reinforce the same classification.

No code enforces consistency between directory and `context`; the convention is manual.

## Record format

Observed fixture records use YAML front matter followed by five Markdown sections.

### Front matter

Observed fields:

| Field | Observed role |
| --- | --- |
| `title` | Human-readable record title. |
| `slug` | Filename/identifier-style slug. |
| `context` | Observed partition/context value such as `work`. |
| `template_type` | Record/template class; fixtures use `task`. |
| `template_version` | Version identifier; fixtures use `v1`. |
| `status` | Lifecycle/status label. |
| `created_at` | Creation timestamp. |
| `updated_at` | Last-updated timestamp. |

The repository does not contain a formal schema definition or parser that proves these fields are mandatory, typed, unique, or validated.

### Body sections

Observed records contain:

1. `## Overview`
2. `## Notes`
3. `## Next Actions`
4. `## Open Questions`
5. `## Changelog`

Fixtures typically fill empty-content sections with text such as `No information currently` and add a creation entry under `Changelog`.

## Status/lifecycle conventions

Observed fixture statuses include:

- `active`;
- `done`.

For example, `test-task-1.md` is `active`, while `test-task-8.md` is `done`.

These are observed values only. No repository source defines:

- an allowed status vocabulary;
- status transitions;
- automatic completion rules;
- reopening behavior;
- archival rules;
- validation that status and content agree.

Do not describe `active -> done` as an enforced state machine. It is only an observed manual convention.

## Timestamp conventions

Fixtures use ISO-8601-like timestamps, but formatting is not fully normalized:

- some values are quoted strings;
- at least one observed `updated_at` is unquoted YAML;
- timezone offsets vary, including `+00:00` and `-07:00`.

No formatter or validator enforces one canonical timestamp representation.

## Slug/filename convention

Observed examples align filename and `slug`, such as:

- file: `tasks/work/test-task-1.md`;
- front matter: `slug: "test-task-1"`.

This appears to be a convention rather than an enforced invariant. No code checks filename/slug equivalence or uniqueness.

## Template metadata relationship

Fixture records include:

- `template_type: "task"`;
- `template_version: "v1"`.

The repository also contains `templates/tasks/task_v1.md`, which establishes a plausible provenance convention between records and template files.

However, the current template files contain only Markdown body headings; they do not include front matter, and no generator links a record automatically to a template. Template metadata is therefore manually maintained.

## Manual record lifecycle

Based strictly on repository evidence, the practical lifecycle is manual:

1. choose a work/personal directory;
2. create a Markdown record;
3. populate front matter fields;
4. use the standard body headings;
5. update content/status/timestamps manually;
6. append changelog entries manually as desired.

No repository process automates these steps.

## Fixtures and examples

`tasks/work/test-task-1.md` through `test-task-8.md` provide evidence of the current record shape and formatting variability.

They should be treated as examples/fixtures, not production subsystems. Their placeholder content also means they are poor evidence for rich business-process semantics beyond the record format itself.

## Dependencies

There are no verified runtime dependencies, package manifests, executable source files, or build tools in the current tree.

Markdown and YAML-front-matter interpretation is conceptual/manual unless another external tool consumes these files; no such consumer is verified in this repository.

## Security and data considerations

The repository structure allows personal-context records under `tasks/personal/`, but that directory is currently empty.

Because this is a Git repository, maintainers should treat committed record content as repository data. The current source does not implement:

- field-level access control;
- encryption;
- secret scanning specific to task fields;
- privacy labels;
- personal/work access separation beyond directory naming.

Do not infer privacy or access controls from the `personal` directory name.

## Failure modes

Because there is no application runtime, current failure modes are primarily data-quality/manual-maintenance issues:

- malformed YAML front matter;
- missing expected metadata fields;
- filename/slug mismatch;
- inconsistent `context` and directory partition;
- unsupported/unexpected status strings;
- stale `updated_at` timestamps;
- changelog not updated with record changes;
- body sections omitted or renamed;
- template metadata not matching the skeleton actually used;
- formatting drift between records;
- accidental storage of information unsuitable for the repository's access model.

No automated validator currently detects these issues.

## Current limitations

- README provides no operating guidance beyond the repository name;
- no executable application or agent;
- no API;
- no cloud deployment;
- no GitHub Actions automation;
- no external integrations;
- no schema/Markdown validator;
- no controlled status vocabulary;
- no automated lifecycle transitions;
- no record generator;
- no search/index implementation in the repository;
- personal/work separation is organizational, not technical access control;
- fixture formatting demonstrates that conventions can drift manually.

## Related documentation

- [Overlord Versioned Task, Project, and Meeting Templates](../notes/overlord-versioned-task-project-meeting-templates.md)
- [Overlord Documentation Workstream Plan](../high-director/overlord-documentation-workstream-plan.md)
- [Repository Scan: Overlord](../high-director/repository-scan-overlord.md)
- [Documentation Target Catalogue](/projects/high-director/documentation-target-catalogue/)

## Continuation

If Overlord gains executable code, automation, schema validation, an API, integrations, or deployment infrastructure, document those capabilities only after they exist in source. Until then, maintain this page as the source-grounded description of a manual Markdown task-record repository.
