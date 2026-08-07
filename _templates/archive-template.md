---
title: <Archived item title>
summary: <One sentence describing the historical item and why it was archived>
section: archive
doc_type: reference
status: archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
archived_date: YYYY-MM-DD
last_verified: YYYY-MM-DD
owner: <Person or team>
order: 100
permalink: /projects/archive/<slug>/
# Optional:
# repository: <Former primary repository>
# system: <Former system>
# superseded_by: /projects/.../
# archive_reason: <Short reason>
---

# <Archived item title>

> This page preserves historical context. It must not be treated as the current implementation unless explicitly stated.

## Archive Summary

State what was archived, why it is no longer current, and the period or milestone it represents.

## Archive Status

- Archived on: `YYYY-MM-DD`
- Archive reason: `<reason>`
- Replacement: `<stable internal link or None>`
- Current recommendation: `<what should be used instead>`

## Historical Context

Describe the problem the archived item solved, the environment in which it operated, and why it existed.

## Last Known Implementation State

Record the final verified state before archival.

Include exact repositories, branches, file paths, workflows, deployments, datasets, services, and configuration object names where useful.

Clearly distinguish verified final state from reconstructed history.

## Source of Truth

Identify the remaining authoritative historical sources, such as the final repository commit, release, workflow, deployment record, schema snapshot, or successor document.

State which source should be trusted if historical copies conflict.

## Why It Was Archived

Explain the technical, operational, business, architectural, or lifecycle reasons for archival.

## Successor or Replacement

Describe the replacement implementation or explain why none exists.

Use exact repository names, systems, file paths, or stable internal links where known.

## Security Considerations

Do not preserve secrets or sensitive operational details. Remove obsolete credentials while retaining useful structural information.

Never include credentials, tokens, private keys, secret values, connection strings, confidential identifiers, private personal data, or sensitive screenshots.

## Known Limitations

Explain why this document should not be used as current operational guidance, including outdated dependencies, obsolete paths, retired infrastructure, unverified assumptions, or changed interfaces.

## Outstanding Historical Questions

Record any uncertainties in the historical record that are worth resolving. Omit this section when no useful questions remain.

## Next Safe Action

State the safest action for a future developer who encounters this archived material.

Usually this should direct the reader to the successor implementation, current repository, or authoritative system page rather than modifying the archived implementation.

Example: Review the successor system page and current repository documentation before changing any code derived from this archived implementation.

## Related Documents

Link successor repositories, systems, decisions, runbooks, notes, or migration records using stable internal links. Explain predecessor, successor, or historical relationships where useful.

## Verification Record

- Last verified: `YYYY-MM-DD`
- Verified against: `<final commit, deployment, release, or authoritative historical record>`
- Verified by: `<person or process>`
- Verification scope: `<historical facts actually checked>`
- Unverified areas: `<list or None>`

## When to Create Subordinate Pages

Create subordinate pages only when preserving extensive historical architecture, migrations, incident analysis, or research is genuinely valuable. Keep this overview authoritative for archive reason, last known state, successor guidance, limitations, and the safest continuation path.
