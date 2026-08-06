---
title: <System name>
summary: <One sentence describing the system outcome, users, and boundary>
section: systems
doc_type: system
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <Person or team>
system: <Canonical system name>
order: 100
permalink: /projects/systems/<slug>/
# Optional:
# repository: <Primary repository name>
# tags:
#   - <platform>
#   - <domain>
---

# <System name>

> Keep this page authoritative for the complete system boundary. Remove headings that add no value rather than leaving them empty.

## Summary

State the business or technical outcome, principal users or consumers, and what is inside and outside the system boundary.

## Current Implementation State

Describe what is operating now across all repositories and platforms. Separate deployed, partially implemented, planned, retired, and unverified components.

Include current environments, active integrations, significant manual steps, and known differences between intended and actual operation.

## System Boundary

Define included components, excluded responsibilities, external actors, and ownership boundaries. Name exact repositories, AWS services, Appsmith apps, Power BI workspaces, Power Automate flows, GitHub workflows, datasets, and other platforms where applicable.

## Source of Truth

List authoritative sources for the system and explain which concern each governs.

| Concern | Authoritative source | Exact location |
| --- | --- | --- |
| Application code | `<repository>` | `<path>` |
| Infrastructure | `<repository or platform>` | `<path or resource name>` |
| Schema | `<document or registry>` | `<stable link or path>` |
| Operational procedure | `<runbook>` | `<stable internal link>` |
| Configuration | `<platform or repository>` | `<file, environment, or setting name>` |

## Architecture

Describe the major components, trust boundaries, data flow, control flow, and integration methods. Link to an architecture decision or detailed diagram when necessary.

Use exact interface names, queues, buckets, tables, APIs, workflows, apps, reports, and connection names.

## Components and Repositories

For each component, state its purpose, owner, repository or platform location, deployment state, and relationship to other components.

## Inputs and Outputs

### Inputs

Document producers, interfaces, formats, frequencies, expected volumes, validation rules, and sensitivity.

### Outputs

Document consumers, interfaces, formats, destinations, service expectations, retention, and compatibility obligations.

## Dependencies

List internal systems, external services, repositories, datasets, identities, infrastructure, schedules, and human processes required for operation. Identify critical and optional dependencies.

## Configuration

Record configuration object names and locations without values. Include environment variables, GitHub variables and secret names, AWS parameters, Appsmith datasources, Power BI connections, Power Automate connections, schedules, and feature flags when relevant.

## Deployment and Environments

Describe each environment, deployment trigger, workflow or manual path, target resources, approvals, migration requirements, rollback method, and post-deployment verification.

## Operation and Monitoring

Explain schedules, triggers, health signals, dashboards, logs, alerts, ownership, routine maintenance, capacity checks, and operational dependencies.

Link detailed procedures to runbooks rather than duplicating them.

## Validation

State how component behavior, interfaces, schemas, end-to-end flow, deployment, and documentation are verified. Record expected evidence and the last verified environment or release.

## Failure Modes and Recovery

Summarize likely cross-component failures, symptoms, evidence locations, safe first checks, containment boundaries, and authoritative recovery runbooks.

## Security and Access

Describe identities, roles, trust boundaries, network boundaries, data classifications, secret stores, least-privilege expectations, audit evidence, and prohibited data handling.

Name configuration and secret objects only. Never include secret values, credentials, tokens, private keys, or confidential identifiers.

## Known Limitations

Record current architectural, operational, data, platform, scaling, resilience, observability, and support limitations.

## Outstanding Work

List actionable work across components, with repository or platform location, dependency, blocker, and relevant issue or plan.

## Next Safe Development Action

State the smallest coordinated action that can proceed without guessing. Name the exact component, repository or platform object, prerequisite checks, expected impact, and validation path.

## Related Documents

Link repositories, schemas, runbooks, architecture decisions, component documentation, and dependent systems using stable internal links. State parent, child, upstream, downstream, or supersession relationships where useful.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<environments, deployments, repositories, workflow runs, or authoritative sources>`
- Verified by: `<person or process>`
- Verification scope: `<components and flows actually checked>`

## When to Create Subordinate Pages

Create subordinate pages for independently owned components, detailed architecture, interfaces, deployment procedures, environment-specific operation, migrations, or complex failure recovery. Keep this overview authoritative for system purpose, boundary, current state, component map, end-to-end inputs and outputs, dependencies, limitations, outstanding work, and next safe action.
