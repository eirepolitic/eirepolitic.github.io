---
title: <Exact repository name>
summary: <One sentence stating what the repository delivers and where it fits>
section: repositories
doc_type: repository
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <Person or team>
repository: <Exact GitHub repository name>
order: 100
permalink: /projects/repositories/<slug>/
# Optional:
# system: <Related system name>
# tags:
#   - <technology>
#   - <domain>
---

# <Exact repository name>

> Remove guidance text and headings that add no value. Never leave placeholder sections empty.

## Summary

State what the repository does, who or what uses it, and its current role. Use verified present tense for implemented behavior and clearly label planned behavior.

Example: `member-data-pipeline` collects member records from the source API, normalizes them, and publishes validated Parquet datasets to the analytics bucket.

## Current Implementation State

Describe what is implemented now, the active branch or release model, important incomplete areas, and any known difference between source code and deployed behavior.

Include:

- Default branch and deployment branch, when different.
- Current production or operational state.
- Exact major entry points and file paths.
- Features that are planned, disabled, deprecated, or unverified.

## Source of Truth

Record authoritative locations. Prefer exact names and paths.

- Repository: `<exact repository name>`
- Primary entry point: `<path/to/file.py>`
- Workflow definitions: `<.github/workflows/file.yml>`
- Infrastructure definitions: `<path/to/template.yml>`
- Configuration files: `<path/to/config.yml>`
- Published documentation: `<stable internal documentation link>`

Do not list generated files as authoritative unless they are intentionally committed and maintained.

## Repository Structure

Explain only directories and files needed to understand or safely change the repository.

```text
<repository>/
├── <path>/        # <purpose>
├── <file>         # <purpose>
└── <file>         # <purpose>
```

## Inputs and Outputs

### Inputs

For each input, state the producer, interface, format, location, validation expectations, and whether it contains sensitive data.

### Outputs

For each output, state the consumer, format, destination, update behavior, and compatibility expectations.

## Dependencies

List runtime, build, infrastructure, external-service, repository, dataset, and workflow dependencies. Use exact package, service, repository, bucket, table, app, workflow, or connection names without secret values.

Explain which dependencies are required, optional, or only used during deployment.

## Configuration

Document configuration keys, file locations, environment variable names, GitHub Actions variable names, secret names, and environment names. Never record secret values.

| Name | Location | Purpose | Required | Safe example |
| --- | --- | --- | --- | --- |
| `<CONFIG_NAME>` | `<file, environment, or GitHub setting>` | `<purpose>` | Yes/No | `<non-secret example or omit>` |

## Local Development

Provide the minimum verified steps to prepare the environment, install dependencies, run the main path, and execute tests or validation.

Use exact commands and working directories. State prerequisites and supported versions when known.

## Deployment and Release

Describe the actual deployment path, including trigger, workflow file, target environment, artifacts, approval gates, rollback method, and post-deployment check.

Do not describe a deployment process as operational unless it has been verified.

## Validation

State how correctness is checked before and after changes.

Include:

- Automated tests and commands.
- Static checks, schema checks, or documentation validation.
- Expected success evidence.
- Last verified commit, release, workflow run, or date when useful.

## Operations

Describe scheduled execution, manual operation, monitoring, logs, alerts, ownership, and routine maintenance. Link to a runbook when procedures are detailed or incident-oriented.

## Failure Modes

Document likely failures, visible symptoms, where to inspect evidence, immediate safe checks, and escalation or recovery links.

Avoid duplicating a full runbook. Summarize the failure and link to the authoritative procedure.

## Security and Access

Record authentication method, access boundary, sensitive-data classification, secret storage locations, least-privilege expectations, and prohibited logging or storage behavior.

Never include credentials, tokens, private keys, secret values, private personal data, or confidential account identifiers.

## Known Limitations

List current technical, operational, data-quality, performance, platform, and support limitations. Distinguish accepted constraints from defects awaiting work.

## Outstanding Work

List only actionable unfinished work. Link to issues or plans where available and identify blockers or decisions required.

## Next Safe Development Action

State the smallest useful action that can be taken without guessing. Include the exact repository, branch or file path, prerequisite checks, and validation command.

Example: Update `scripts/transform_members.py` to handle the documented nullable field, then run `pytest tests/test_transform_members.py` before opening a pull request.

## Related Documents

Link to stable internal documents for parent systems, schemas, runbooks, decisions, deployment details, or dependent repositories. Explain the relationship when the title alone is unclear.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<commit, release, workflow run, deployment, or authoritative source>`
- Verified by: `<person or process>`
- Verification scope: `<what was actually checked>`

## When to Create Subordinate Pages

Keep this page complete for ordinary repositories. Create subordinate pages when one topic is independently maintained, has a different verification cycle or owner, requires detailed procedures, or would make this overview difficult to scan.

Suitable subordinate pages include architecture details, deployment guides, data contracts, API references, migration plans, or component-specific runbooks. Keep the overview authoritative for purpose, current state, source-of-truth locations, dependencies, limitations, outstanding work, and next safe action.
