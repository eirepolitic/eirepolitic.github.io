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

High Director is the subject of this documentation section. The repository currently verifies the documentation framework and development process around the agent, but it does not yet contain enough authoritative source material to describe the complete runtime implementation.

Detailed runtime claims must therefore be treated as **unknown / unverified** until implementation source, configuration, schemas, or other authoritative evidence is inspected.

## Current verified scope

This repository directly verifies:

- a dedicated High Director documentation section;
- a persistent High Director documentation initiative plan;
- repository-based documentation change management through branches, pull requests, validation, and GitHub Pages deployment;
- documentation templates, standards, architecture records, runbooks, and verification records used to maintain this section.

See [High Director Repository Documentation Inventory]({{ '/docs/high-director/repository-documentation-inventory/' | relative_url }}) for the canonical repository-only evidence map.

## Runtime scope pending verification

The following subjects are planned for authoritative documentation but are not yet verified by this repository:

- purpose and complete responsibility boundaries;
- capability catalogue and behavioral rules;
- tools and external integrations;
- GitHub integration implementation;
- AWS, Lambda, API Gateway, and IAM integration;
- ChatGPT Actions and OpenAPI schemas;
- authentication and authorization;
- runtime data flows;
- configuration and dependencies;
- supporting code;
- runtime failure modes and troubleshooting;
- deployment, rebuild, handoff, and continuation procedures.

## Documentation principles

High Director documentation must:

- distinguish verified implementation, user-supplied authoritative source, inference, historical behavior, planned work, and unknown state;
- prefer real implementation over artificial examples;
- keep secrets and unnecessary personal information out of published material;
- use one canonical source for each fact and link instead of duplicating it;
- validate every documentation PR before merge;
- verify the resulting GitHub Pages deployment before starting the next major documentation phase.

## Initiative status

The current source of truth for implementation phases, missing sources, verification gates, and the next safe action is the [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }}).
