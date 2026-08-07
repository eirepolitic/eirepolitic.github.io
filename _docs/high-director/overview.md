---
title: High Director Overview
summary: Entry point for the verified technical documentation of the High Director agent, its integrations, runtime architecture, security boundaries, code, and operating procedures.
section: high-director
doc_type: agent
status: active
created: 2026-08-05
updated: 2026-08-06
last_verified: 2026-08-06
order: 10
permalink: /projects/high-director/
---

# High Director

## Overview

High Director is a GPT configured as a concise coding assistant for designing and building data pipelines and related infrastructure. Its authoritative user-authored instructions emphasize Python, GitHub, YAML, Appsmith, Power BI, Power Automate, and AWS, and direct it to help design, troubleshoot, document, and implement pipeline workflows and supporting infrastructure.

The documentation initiative has now established authoritative records for the GPT configuration, both configured Actions, the GitHub wrapper Lambda implementation, live AWS configuration, runtime architecture, data flows, security/configuration boundaries, code/dependencies, operations, troubleshooting, and handoff procedures.

## Authoritative GPT configuration

The sanitized source of truth for the GPT name, description, complete Instructions field, conversation starters, recommended model, visible Knowledge state, and configured Actions is [High Director GPT Configuration]({{ '/projects/high-director/gpt-configuration/' | relative_url }}).

Verified behavioral rules include:

- keep responses short, direct, practical, and precise;
- ask a focused question instead of assuming required missing information;
- provide explicit ordered click-by-click instructions for how-to tasks;
- prefer immediately usable steps, commands, file structures, and examples;
- present the safest or simplest option first when multiple paths exist;
- obtain decisions affecting function, cost, design, architecture, or implementation before proceeding when required;
- plan build work before detailed implementation;
- pass repository name only to the configured GitHub Action because owner is configured in the backend;
- do not diagnose repository formatting as the cause of a GitHub Action failure unless the returned API error supports that conclusion.

## Verified technical scope

Current authoritative documentation covers:

- GPT configuration and behavioral instructions;
- GitHub GPT Action OpenAPI contract and API-key authentication;
- GitHub wrapper FastAPI/Mangum Lambda source, dependencies, and deployment assets;
- live AWS Lambda runtime, Function URL, environment-key, execution-role, managed-policy, and trust configuration;
- Google Workspace GPT Action contract, Gmail/Calendar operations, OAuth endpoints, token exchange method, and configured scopes;
- runtime architecture and trust boundaries;
- GitHub, AWS, Google Workspace, secret, failure, and documentation-control data flows;
- security/configuration reference;
- operating/deployment procedures;
- troubleshooting, recovery boundaries, and handoff/continuation procedures;
- persistent sanitized source snapshots and code/dependency reference.

Canonical implementation pages:

- [Runtime Architecture]({{ '/projects/high-director/runtime-architecture/' | relative_url }})
- [Data Flows]({{ '/projects/high-director/data-flows/' | relative_url }})
- [Security and Configuration Reference]({{ '/projects/high-director/security-configuration-reference/' | relative_url }})
- [Code and Dependency Reference]({{ '/projects/high-director/code-and-dependency-reference/' | relative_url }})
- [GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})

## Operating and handoff documentation

- [Operate and Update High Director]({{ '/projects/runbooks/high-director-operations-and-deployment/' | relative_url }})
- [Troubleshoot and Hand Off High Director]({{ '/projects/runbooks/high-director-troubleshooting-and-handoff/' | relative_url }})

These runbooks preserve the rule that architecture, security, cost, access-control, credential, OAuth-scope, IAM-policy, or irreversible changes require an explicit decision before implementation.

## Known unresolved areas

The following remain explicitly unknown, unverified, private, or intentionally unpublished:

- GPT Builder capability-toggle state not shown in the supplied configuration source;
- API-key and GitHub-token values and their rotation procedures;
- exact fine-grained GitHub PAT permissions currently granted;
- complete Lambda execution-role policy inventory beyond the supplied visible evidence;
- live Lambda memory/timeout confirmation, although the SAM template declares 512 MB and 30 seconds;
- Lambda Function URL resource-policy details and monitoring/alerting configuration;
- Google OAuth client identity/secret, token storage/refresh behavior, connected-account identity, and reconnect/revocation procedure;
- CloudWatch alarm/log-retention, WAF/rate-limiting, dead-letter/retry, and other monitoring/perimeter controls unless later authoritative evidence verifies them.

These limitations are tracked in the canonical capability, security, runbook, and verification records rather than filled by inference.

## Documentation principles

High Director documentation must distinguish verified implementation, user-supplied authoritative source, observable runtime evidence, inference, historical behavior, planned work, and unknown state. It must use one canonical source for each fact, keep secrets/private infrastructure details out of publication, validate every documentation PR before merge, and confirm the resulting Pages deployment before the next major documentation step.

## Initiative status

Current phase status, verification gates, and the next safe action are maintained in the [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }}).
