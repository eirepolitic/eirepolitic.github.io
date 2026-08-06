---
title: <Specific note title>
summary: <One sentence stating the subject, scope, and why the note is useful>
section: notes
doc_type: note
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <Person or team>
order: 100
permalink: /projects/notes/<slug>/
# Optional:
# repository: <Related repository>
# system: <Related system>
# tags:
#   - <topic>
#   - working-note
---

# <Specific note title>

> Use notes for useful working knowledge that is not yet authoritative documentation. Remove headings that add no value and never present assumptions as verified facts.

## Purpose

State why this note exists, what question or task it supports, and who or what is expected to use it.

## Scope

Define what the note covers and what it intentionally does not cover.

Use exact repositories, file paths, systems, datasets, workflows, services, platform objects, or dates where relevant.

## Confidence and Status

State how reliable the content is and why.

- Confidence: `<high | medium | low>`
- Current state: `<verified observation | working hypothesis | partial reference | draft guidance>`
- Last verified: `YYYY-MM-DD`
- Verification source: `<repository, file, workflow, platform object, person, or external source>`

Do not use `last_verified` merely because the note was edited.

## Source of Truth

Identify authoritative sources related to the note, even when the note itself is not authoritative.

- Repository: `<exact repository name>`
- File or path: `<exact path>`
- Workflow or platform object: `<exact name>`
- Dataset or schema: `<exact location>`
- Decision or runbook: `<stable internal link>`

State clearly when no authoritative source has been identified.

## Observations

Record confirmed facts and directly observed behavior.

For each important observation, include the evidence and date when useful. Separate current behavior from historical behavior.

## Assumptions and Open Questions

List assumptions, uncertainties, conflicting evidence, and questions that must be resolved before the note is treated as implementation guidance.

## Working Guidance

Provide concise, practical guidance only where useful. Label unverified steps or recommendations clearly.

Use exact commands, clicks, repository paths, configuration names, and expected evidence when known. Do not include secret values.

## Inputs and Outputs

When the note concerns a process, pipeline, query, script, report, or integration, document the relevant inputs, outputs, formats, producers, consumers, and expected behavior.

Omit this section when the note is not about a process or data flow.

## Dependencies and Configuration

Record relevant repositories, packages, services, datasets, roles, environment variables, secret object names, connections, parameters, schedules, or platform settings.

Name configuration objects without exposing values.

## Security Considerations

State any access, privacy, data-classification, secret-handling, logging, or sharing concerns.

Never include credentials, tokens, private keys, secret values, confidential identifiers, production personal data, or sensitive screenshots.

## Known Limitations

Record where the note may be incomplete, outdated, environment-specific, inferred, or dependent on unverified behavior.

## Promotion Criteria

State what must happen before this note becomes authoritative repository, system, schema, runbook, decision, or High Director documentation.

Examples:

- Verify behavior against the deployed system.
- Confirm exact file paths and configuration names.
- Add validation evidence.
- Resolve open questions.
- Obtain owner review.
- Move stable content into the appropriate section template.

## Outstanding Work

List only actionable research, verification, cleanup, or documentation tasks.

## Next Safe Action

State the smallest useful action that can reduce uncertainty without changing architecture or production behavior.

Include the exact repository, file, command, platform object, or evidence source where possible.

## Related Documents

Link authoritative repository, system, schema, runbook, decision, High Director, archive, or successor documents using stable internal links. Explain the relationship when useful.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<source, commit, run, deployment, dataset, or platform state>`
- Verified by: `<person or process>`
- Verification scope: `<claims actually checked>`
- Unverified areas: `<list or None>`

## When to Create Subordinate Pages

Notes should normally remain small and focused. Create subordinate pages only when the note becomes a maintained research area with distinct sources, owners, or verification cycles. Prefer promoting stable material into the correct authoritative documentation section rather than growing a large note hierarchy.
