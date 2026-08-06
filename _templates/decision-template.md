---
title: <Decision title>
summary: <One sentence stating the decision and the problem it resolves>
section: decisions
doc_type: decision
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <Person or team>
order: 100
permalink: /projects/decisions/<slug>/
# Optional:
# repository: <Primary affected repository>
# system: <Affected system>
# tags:
#   - architecture
#   - <domain>
# superseded_by: /projects/decisions/<replacement>/
---

# <Decision title>

> Record the decision as it was made. Do not rewrite historical reasoning to match later outcomes. Create a superseding decision when the choice changes materially.

## Decision Status

State the governance state of the decision in plain language.

- Decision state: `<proposed | accepted | deprecated | superseded>`
- Decision date: `YYYY-MM-DD`
- Effective date: `YYYY-MM-DD` or `<not yet effective>`
- Owners or approvers: `<person, team, or role>`
- Superseded by: `<stable internal link or None>`

The front matter `status` must still use the site lifecycle vocabulary. Explain the architecture-decision state here rather than inventing a new front matter status.

## Summary

State the selected approach, the affected scope, and the main reason in two or three sentences. A reader should understand the decision without reading the full analysis.

## Context

Describe the problem, current implementation state, triggering event, constraints, assumptions, and forces that made a decision necessary.

Use exact repository names, file paths, systems, datasets, workflows, services, and platform objects. Separate verified facts from assumptions or unresolved information.

## Decision Drivers

List the criteria used to compare options, such as reliability, maintainability, security, cost, delivery speed, operational burden, compatibility, data quality, vendor constraints, or team capability.

Order the drivers when priority materially affected the result.

## Decision

State exactly what will be implemented, retained, removed, or prohibited.

Include:

- System and repository boundaries.
- Interfaces, data flows, and ownership changes.
- Configuration object names without secret values.
- Deployment or migration expectations.
- Compatibility or versioning commitments.
- Security and access implications.

Do not mix planned implementation details with completed work. Label each clearly.

## Source of Truth

Identify the authoritative implementation and governance locations.

- Decision record: `<this stable page URL>`
- Primary repository: `<exact repository name>`
- Implementation paths: `<exact paths>`
- Infrastructure definitions: `<exact repository and paths>`
- Configuration locations: `<environment, settings page, file, variable, parameter, connection, or secret object names>`
- Related issue, plan, or pull request: `<reference>`

State which source governs when documents or implementations conflict.

## Alternatives Considered

For each credible option, explain the approach, benefits, drawbacks, risks, and why it was not selected.

### <Alternative name>

- Description: `<what the option would do>`
- Benefits: `<meaningful advantages>`
- Drawbacks: `<meaningful disadvantages>`
- Rejection reason: `<why it did not best satisfy the drivers>`

Do not add weak alternatives solely to make the selected choice appear stronger.

## Consequences

### Positive

Record expected improvements and who benefits.

### Negative

Record accepted trade-offs, new dependencies, operational costs, migration burden, constraints, and failure risks.

### Neutral or Follow-on

Record implementation work, documentation changes, training, monitoring, cleanup, or later decisions created by this choice.

## Security and Privacy

Document changes to trust boundaries, identities, roles, permissions, data classification, encryption, logging, retention, secret handling, and third-party exposure.

Name configuration and secret objects only. Never include credentials, tokens, private keys, secret values, connection strings, confidential identifiers, or private data.

## Implementation State

Describe what parts of the decision are implemented, partially implemented, planned, paused, deprecated, or unverified.

Use exact repositories, branches, pull requests, commits, workflows, resources, and paths. State any difference between the accepted decision and the current implementation.

## Validation and Review

State how the decision and its implementation will be evaluated.

Include:

- Technical or operational success criteria.
- Security, performance, cost, reliability, and data-quality checks where relevant.
- Review date or triggering condition.
- Evidence required to retain, revise, or supersede the decision.

## Failure Modes and Reversal

Describe likely decision-level failure modes, early warning signs, containment, rollback or migration options, irreversible effects, and the threshold for revisiting the choice.

Link detailed operational recovery procedures to runbooks.

## Known Limitations

Record constraints that remain after the decision, including untested assumptions, platform limits, accepted technical debt, and areas intentionally outside scope.

## Outstanding Work

List implementation, migration, validation, documentation, security, operational, or follow-up decision work. Include exact location, owner, dependency, and issue or plan where available.

## Next Safe Development Action

State the smallest useful action that follows from the decision without requiring new architectural assumptions. Include the exact repository or platform location, prerequisite checks, expected change, and validation path.

## Related Documents

Link affected repositories, systems, schemas, runbooks, prior decisions, superseding decisions, plans, and implementation documents using stable internal links. Explain predecessor, successor, dependency, or implementation relationships.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<implementation commit, deployment, workflow run, configuration, or authoritative source>`
- Verified by: `<person or process>`
- Verification scope: `<decision status and implementation aspects actually checked>`

## When to Create Subordinate Pages

Keep the decision itself in one page. Create subordinate pages for detailed evaluations, benchmarks, threat models, migration plans, cost models, or implementation guides when they are independently maintained or too detailed for the decision record. Keep this page authoritative for context, drivers, decision, alternatives, consequences, status, implementation state, limitations, and review conditions.
