---
title: <High Director topic or initiative>
summary: <One sentence stating the agent-assisted work, current state, and continuation purpose>
section: high-director
doc_type: agent
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: High Director
order: 100
permalink: /projects/high-director/<slug>/
# Optional:
# repository: <Primary repository name>
# system: <Affected system name>
# tags:
#   - high-director
#   - <domain>
---

# <High Director topic or initiative>

> Use this template for agent-assisted development plans, operating guidance, capability records, or continuation documents. Remove headings that add no value and never publish unresolved placeholders as facts.

## Purpose

State why this document exists, what work or capability it governs, and how it should help future High Director sessions continue safely.

## Current State

Describe what is implemented, merged, deployed, validated, pending review, blocked, paused, deprecated, or unverified.

Use exact pull request numbers, branches, commits, workflow runs, repositories, file paths, platform objects, and deployment states. Separate confirmed facts from assumptions and planned work.

## Scope

### Included

List the repositories, systems, platforms, files, workflows, datasets, documentation, or decisions covered.

### Excluded

State what must not be changed or started under this document, including blocked phases, architectural boundaries, security constraints, or deferred work.

## Source of Truth

Identify the authoritative locations for code, configuration, plans, deployments, and decisions.

- Repository: `<exact repository name>`
- Primary files: `<exact paths>`
- Working branch or default branch: `<branch name>`
- Pull requests: `<numbers or stable references>`
- Workflows: `<exact .github/workflows path or workflow name>`
- Platform objects: `<exact non-secret AWS, Appsmith, Power BI, Power Automate, or other names>`
- Parent plan or decision: `<stable internal documentation link>`

State which source wins when documentation and implementation differ.

## Completed Work

Record only work that is actually committed, merged, deployed, validated, or otherwise confirmed. Include evidence such as pull requests, commits, workflow results, and exact paths.

Do not describe drafted, previewed, or local-only changes as complete.

## Current Implementation Details

Explain the parts of the implementation needed to continue safely:

- Repository and directory structure.
- Important entry points and configuration files.
- Inputs, outputs, interfaces, and dependencies.
- Deployment and operational behavior.
- Validation commands and expected evidence.
- Known differences between intended and actual behavior.

Keep this section focused on continuation, not a full duplicate of repository or system documentation.

## Decisions and Constraints

Record decisions already made, unresolved decisions, architectural boundaries, user approvals, cost constraints, security rules, tooling limitations, and actions that require confirmation.

Link architecture decisions where available. Do not silently reinterpret earlier constraints.

## Security and Access

Document allowed access, approval boundaries, secret-storage locations, required roles, protected resources, and prohibited actions.

Name repositories, environments, variables, secret objects, roles, connections, parameters, and platform resources without exposing values.

Never include credentials, tokens, private keys, secret values, session data, private personal data, or confidential identifiers.

## Validation and Evidence

State how current claims were verified.

Include:

- Commands, tests, validators, or queries used.
- GitHub Actions workflow and run result.
- Deployment or Pages result where applicable.
- Files, commits, pull requests, or platform objects inspected.
- Areas not verified.

Editing this document alone does not justify changing `last_verified`.

## Failure Modes and Recovery

Document likely continuation failures, such as working from an outdated branch, bypassing validation, assuming a deployment succeeded, changing the wrong repository, exposing secrets, or starting a blocked phase.

For each, state the visible symptom, safe first check, authoritative evidence, and recovery or escalation path.

## Known Limitations

List missing access, unavailable tools, unverified behavior, incomplete documentation, platform limitations, manual dependencies, and assumptions that may affect future work.

## Outstanding Work

List actionable unfinished work in dependency order. Include exact repository, branch, file, platform object, blocker, and required approval where relevant.

Distinguish required work from optional improvements.

## Next Safe Development Action

State the smallest useful action that can be performed without guessing or changing architecture.

Include:

- Exact repository and branch.
- Exact file or platform object.
- Preconditions and checks.
- Expected change.
- Validation command or workflow.
- Merge or deployment gate.

Example: On branch `high-director/example-step`, update `_templates/example-template.md`, run the documentation validation workflow, and open a pull request without beginning the example-document phase.

## Handoff Notes

Record details a future High Director session must know before acting, including sequence, branch strategy, pending reviews, temporary conditions, naming conventions, and decisions that must not be revisited without cause.

Avoid repeating information already clear in the sections above.

## Related Documents

Link parent plans, repository pages, system pages, schemas, runbooks, architecture decisions, previous High Director records, and successor documents using stable internal links. Explain the relationship when useful.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<branch, commit, pull request, workflow run, deployment, repository files, or platform state>`
- Verified by: `<High Director, person, or process>`
- Verification scope: `<claims and implementation areas actually checked>`
- Unverified areas: `<list or None>`

## When to Create Subordinate Pages

Keep the main page authoritative for purpose, scope, current state, completed work, decisions, outstanding work, and next safe action. Create subordinate pages for large implementation phases, tool-specific procedures, detailed repository analyses, migration plans, validation evidence, or recurring runbooks when they are independently maintained or would make the main page difficult to scan.

Link subordinate pages from the exact section where they become relevant and preserve a clear parent-child relationship.
