---
title: <Action-oriented procedure title>
summary: <One sentence stating when to use this runbook and the intended result>
section: runbooks
doc_type: runbook
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <Person or team>
order: 100
permalink: /projects/runbooks/<slug>/
# Optional:
# repository: <Primary repository name>
# system: <Affected system name>
# tags:
#   - <platform>
#   - <operation>
---

# <Action-oriented procedure title>

> A runbook must be executable by a capable operator without hidden assumptions. Remove sections that do not apply; never leave empty emergency steps.

## Purpose

State the condition or task this runbook addresses, the intended outcome, and what it does not cover.

Use an action-oriented title such as `Recover a failed member-data publication` rather than a broad title such as `Pipeline notes`.

## Status and Last Verification

State whether the procedure is verified, partially verified, draft, deprecated, or emergency-only.

- Status: `<verified | partially verified | draft | deprecated>`
- Last verified: `YYYY-MM-DD`
- Verified against: `<environment, version, workflow, resource, or incident>`
- Expected duration: `<only when known and operationally useful>`

Do not label a procedure verified unless its steps and success checks were deliberately tested or observed.

## Use This Runbook When

List precise symptoms, alerts, requests, or maintenance conditions that should trigger this procedure.

## Do Not Use This Runbook When

List conditions requiring a different procedure, escalation, security response, data-restoration decision, or architectural change.

## Impact and Risk

Describe affected systems, users, data, environments, dependencies, downtime, irreversible actions, and possible side effects.

Identify steps requiring additional approval or a maintenance window.

## Prerequisites and Access

List required role, environment, tools, repository, branch, working directory, platform access, backups, approvals, and information to collect before starting.

Name roles, secret objects, connections, parameters, and configuration keys without values.

## Source of Truth

Record authoritative implementation and operational locations.

- Repository: `<exact repository name>`
- Procedure-related code: `<exact path>`
- Workflow or automation: `<exact workflow, job, flow, or app name>`
- Infrastructure or resource: `<exact non-secret resource name>`
- Logs and monitoring: `<exact service, dashboard, log group, or view>`
- Related schema or contract: `<stable internal link>`

## Safety Checks

Before making changes, verify:

1. The target environment and resource names are correct.
2. The observed symptoms match this runbook.
3. Required backups, snapshots, exports, or rollback paths exist.
4. No concurrent deployment or recovery operation conflicts with the procedure.
5. Sensitive information will not be copied into logs, issues, screenshots, or documentation.

Add situation-specific checks. Do not use generic confirmation steps as a substitute for evidence.

## Procedure

Number every operational step. Include exact clicks, commands, paths, inputs, expected output, and decision points.

### 1. <First action>

1. Open or change to `<exact location>`.
2. Run or select `<exact command or control>`.
3. Confirm `<observable expected result>`.

### 2. <Next action>

Continue with the smallest safe actions. Place warnings immediately before destructive or irreversible steps.

Use placeholders only where the operator must deliberately supply an environment-specific, non-secret value.

## Validation and Success Criteria

Define how to prove the intended state was restored or the task completed.

Include:

- Exact commands, queries, checks, dashboards, or workflow results.
- Expected values or state transitions.
- End-to-end consumer checks where relevant.
- Data reconciliation or schema validation where relevant.
- Evidence to record in an issue, incident, or change log.

## Rollback or Recovery

Describe how to return to the prior safe state, including prerequisites, commands or controls, data implications, and validation. State clearly when rollback is not possible or requires specialist approval.

## Failure Modes and Escalation

For each likely failure during the procedure, state the symptom, safe immediate action, evidence to collect, actions to avoid, and escalation destination.

| Failure | Safe response | Evidence | Escalate to |
| --- | --- | --- | --- |
| `<symptom>` | `<containment or stop condition>` | `<logs, run ID, timestamps, resource state>` | `<owner or linked runbook>` |

## Security Guidance

- Use approved identities, roles, devices, and secret stores.
- Never paste secret values into commands that will be retained in shell history when a safer method exists.
- Never record credentials, tokens, private keys, connection strings, confidential identifiers, or private data in this document.
- Redact sensitive values from screenshots, logs, issues, and copied output.
- Stop and escalate when unexpected access, data exposure, or integrity concerns appear.

Add system-specific least-privilege, audit, data-handling, and incident-response requirements.

## Known Limitations

Record conditions the runbook does not resolve, untested environments, manual dependencies, timing risks, data-loss risks, and assumptions that may become invalid.

## Follow-up Work

List cleanup, monitoring, issue creation, documentation updates, root-cause analysis, permanent fixes, or stakeholder communication required after the immediate procedure.

## Next Safe Action

State what the operator or developer should do immediately after the documented procedure, especially when the runbook ends at a containment or diagnostic state.

## Related Documents

Link the affected system, repositories, schemas, architecture decisions, incident procedures, deployment guides, and alternative runbooks using stable internal links.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<environment, version, run, incident, or maintenance event>`
- Verified by: `<person or process>`
- Verification scope: `<steps and outcomes actually checked>`
- Known unverified steps: `<list or None>`

## When to Create Subordinate Pages

Keep one runbook focused on one operational objective. Create subordinate or separate runbooks when procedures have different triggers, permissions, risk levels, owners, environments, or rollback paths. Move large command references, troubleshooting matrices, or platform-specific click paths to subordinate pages only when the main procedure remains directly executable and links to them at the exact step where needed.
