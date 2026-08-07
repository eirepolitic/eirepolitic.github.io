---
title: High Director Overview
summary: Entry point for verified and planned technical documentation of the High Director agent.
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

High Director is a GPT configured as a concise coding assistant for designing and building data pipelines and related infrastructure. Its user-authored instructions emphasize Python, GitHub, YAML, Appsmith, Power BI, Power Automate, and AWS, and direct it to help design, troubleshoot, document, and implement pipeline workflows and supporting infrastructure.

This purpose and the core behavioral rules are now verified from user-supplied authoritative GPT configuration. The lower-level runtime implementation, Action schemas, authentication, and AWS supporting infrastructure remain only partially documented.

## Authoritative GPT configuration

The sanitized source of truth for the GPT name, description, complete Instructions field, conversation starters, recommended model, visible Knowledge state, and visible Action entries is [High Director GPT Configuration]({{ '/projects/high-director/gpt-configuration/' | relative_url }}).

Verified behavioral rules include:

- keep responses short, direct, practical, and precise;
- ask a focused question instead of assuming required missing information;
- provide explicit ordered click-by-click instructions for how-to tasks;
- prefer immediately usable steps, commands, file structures, and examples;
- present the safest or simplest option first when multiple paths exist;
- obtain decisions affecting function, cost, design, architecture, or implementation before proceeding when required;
- plan build work before detailed implementation;
- pass repository name only to the configured GitHub action because owner is configured in the backend;
- do not diagnose repository formatting as the cause of a GitHub action failure unless the returned API error supports that conclusion.

## Current verified technical scope

Current evidence verifies:

- the authoritative GPT configuration and instructions supplied on 2026-08-06;
- a configured GitHub integration with an observed repository/workflow operation surface;
- two configured Actions in the GPT UI, one using a private AWS Lambda URL hostname and one visibly targeting `www.googleapis.com`;
- a dedicated High Director documentation section and persistent documentation initiative;
- repository-based documentation change management through branches, pull requests, validation, and GitHub Pages deployment.

See [High Director Capability and Component Inventory]({{ '/docs/high-director/capability-component-inventory/' | relative_url }}) for evidence classification and component boundaries.

## Runtime scope pending verification

The following still require authoritative source material:

- capability toggle settings;
- ChatGPT Action/OpenAPI schemas and operation IDs;
- action authentication settings;
- AWS Lambda source and configuration;
- API Gateway configuration, if any;
- IAM roles, policies, and trust relationships;
- runtime data flows;
- external configuration and dependencies;
- supporting external repositories/code;
- runtime failure modes and troubleshooting;
- deployment, rebuild, handoff, and continuation procedures for external components.

## Documentation principles

High Director documentation must distinguish verified implementation, user-supplied authoritative source, observable runtime evidence, inference, historical behavior, planned work, and unknown state. It must use one canonical source for each fact, keep secrets/private infrastructure details out of publication, validate every documentation PR before merge, and confirm the resulting Pages deployment before the next major documentation step.

## Initiative status

The current source of truth for implementation phases, missing sources, verification gates, and the next safe action is the [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }}).
