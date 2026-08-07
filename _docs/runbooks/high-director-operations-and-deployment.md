---
title: Operate and Update High Director
summary: Verified operating and deployment procedure for High Director documentation, GitHub Action configuration, Lambda wrapper deployment, and Google Workspace Action maintenance.
section: runbooks
doc_type: runbook
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 60
permalink: /projects/runbooks/high-director-operations-and-deployment/
tags:
  - high-director
  - deployment
  - operations
---

# Operate and Update High Director

## Purpose

Use this runbook for normal High Director maintenance and documentation-backed updates to the verified GPT configuration, GitHub Action/Lambda wrapper, or Google Workspace Action.

This runbook does not authorize architecture, security, cost, access-control, credential, OAuth-scope, IAM-policy, or irreversible changes. Those require an explicit decision first.

## Status and Last Verification

- Status: **partially verified**
- Last verified: `2026-08-06`
- Verified against: High Director GPT configuration, GitHub Action schema, Lambda source/SAM package, live Lambda/IAM configuration, Google Workspace Action schema/OAuth configuration, repository validation workflow, and successful Pages deployments.
- Known unverified deployment steps: a fresh Lambda redeployment and full Google OAuth reconnect have not been deliberately exercised during this documentation initiative.

## Use This Runbook When

Use it when:

- updating High Director documentation after a verified implementation/configuration change;
- changing the GPT Instructions, conversation starters, Action schema, or non-secret Action configuration;
- deploying an approved GitHub wrapper code/configuration update;
- validating that High Director documentation reflects the deployed implementation;
- performing ordinary maintenance that does not alter security/architecture boundaries.

## Do Not Use This Runbook When

Stop for a decision before proceeding if the proposed work changes:

- GitHub token permissions or repository scope;
- API-key authentication or key lifecycle;
- Lambda Function URL auth mode;
- IAM policies or trust relationships;
- Google OAuth scopes, client configuration, connected account, or authorization model;
- destructive repository/workflow/account behavior;
- infrastructure architecture or recurring cost.

## Source of Truth

- Documentation repository: `eirepolitic.github.io`
- Persistent plan: `_docs/high-director/high-director-documentation-initiative-plan.md`
- Runtime architecture: `_docs/high-director/runtime-architecture.md`
- Data flows: `_docs/high-director/data-flows.md`
- Security/configuration: `_docs/high-director/security-configuration-reference.md`
- GPT configuration: `_docs/high-director/gpt-configuration.md`
- Current GitHub Action schema: `_docs/high-director/github-action-openapi-schema.md`
- Lambda implementation analysis: `_docs/high-director/github-wrapper-lambda.md`
- Live AWS configuration: `_docs/high-director/github-wrapper-live-aws-configuration.md`
- Google Workspace Action: `_docs/high-director/google-workspace-action.md`
- Sanitized Lambda deployment assets: `assets/high-director/github-wrapper-source/`
- Documentation validator: `.github/workflows/validate-documentation.yml`

## Safety Checks

Before changing anything:

1. Identify the exact target component and authoritative current source.
2. Confirm the change does not alter architecture, security, cost, access control, or an irreversible boundary without a user decision.
3. Never copy API keys, GitHub tokens, OAuth secrets/tokens, AWS credentials, private Lambda hostname, personal account identifiers, or private user data into the repository.
4. Preserve exact non-secret implementation names, paths, operation IDs, environment-variable names, and versions.
5. Use a focused branch and PR for documentation changes.
6. Do not begin the next major documentation phase until the prior merged change has a successful Pages deployment.

## Procedure A — Update High Director Documentation

1. Read the current canonical page for the subject.
2. Inspect the authoritative implementation/configuration source.
3. Classify each new fact as verified implementation, user-supplied authoritative source, observable runtime evidence, inference, historical behavior, planned work, or unknown/unverified.
4. Sanitize private/sensitive values before publication.
5. Create a focused branch from `main`.
6. Update only the canonical page(s) required by the change.
7. Update `_docs/high-director/high-director-documentation-initiative-plan.md` after meaningful initiative progress.
8. Open a focused PR.
9. Run `Validate documentation`.
10. Confirm validation succeeds.
11. Merge the PR.
12. Find the `pages-build-deployment` run whose `head_sha` matches the merged commit.
13. Confirm the Pages run finishes with `conclusion: success`.
14. Only then continue to the next major documentation step.

## Procedure B — Update GPT Instructions or Non-secret Configuration

1. Open ChatGPT on the web.
2. Open **Explore GPTs** -> **My GPTs** -> **High Director** -> **Edit GPT**.
3. Compare the intended change with `_docs/high-director/gpt-configuration.md`.
4. If the change affects security, Actions, OAuth, architecture, cost, or access control, stop for an explicit decision.
5. Apply only the approved GPT configuration change.
6. Capture the changed non-secret fields exactly.
7. Do not copy Client Secrets, API keys, tokens, or private account identifiers.
8. Update the canonical GPT configuration documentation through Procedure A.
9. If Action behavior/configuration changed, update the relevant Action/architecture/security pages too.

## Procedure C — Update the GitHub Action Schema

1. Open **High Director** in GPT Builder.
2. Open the private Lambda-backed Action.
3. Copy the complete current OpenAPI schema.
4. Compare it against `_docs/high-director/github-action-openapi-schema.md` and the Lambda source version documented in `_docs/high-director/github-wrapper-lambda.md`.
5. Preserve operation IDs, paths, request/response schemas, and authentication declarations.
6. Redact the private Lambda hostname before publication.
7. If the proposed schema exposes a new write/destructive operation or changes authentication, stop for an explicit security/architecture decision.
8. Apply the approved schema update in GPT Builder.
9. Update canonical documentation through Procedure A.
10. Record any remaining schema/application version drift rather than silently reconciling it.

## Procedure D — Deploy an Approved GitHub Wrapper Lambda Change with SAM

Use only after the implementation change has been reviewed and any security/architecture decision has been made.

Verified deployment assets:

```text
assets/high-director/github-wrapper-source/template.yaml
assets/high-director/github-wrapper-source/requirements.txt
assets/high-director/github-wrapper-source/samconfig.toml
```

The sanitized published `samconfig.toml` contains a redacted owner and cannot be used as-is for a real deployment.

Expected declared deployment settings:

```text
Region: us-east-2
Runtime: python3.13
Handler: src.app.handler
Stack: github-gpt-wrapper
Function URL AuthType: NONE
Invoke mode: BUFFERED
```

Required deployment parameters/secret inputs include:

- GitHub owner;
- GitHub token;
- application API key;
- default base branch;
- branch prefix.

Do not place real secret values in repository files or documentation.

For a SAM-based deployment from the authoritative private source workspace:

1. Confirm AWS CLI/SAM credentials target the intended AWS account and `us-east-2`.
2. Confirm the source package contains the intended `src/app.py`, `template.yaml`, `requirements.txt`, and deployment configuration.
3. Confirm handler/runtime match the approved change.
4. Install/build dependencies using the deployment source's pinned `requirements.txt`.
5. Run `sam build`.
6. Review the generated change set/configuration before deployment.
7. Run the approved `sam deploy` flow using secret parameter inputs through an appropriate non-public mechanism.
8. Confirm the deployed Lambda Runtime and Handler in the AWS Console.
9. Confirm Function URL auth/invoke/CORS settings remain as intended.
10. Confirm environment-variable **names** are present; do not record values.
11. Confirm the execution role and trust relationship remain as approved.
12. Test a low-risk authenticated read operation through the Action before exercising writes.
13. Update the Action schema if required by the deployed API contract.
14. Update documentation through Procedure A.

Because a fresh SAM deployment was not deliberately performed in this documentation initiative, Steps 1-13 are **source-derived deployment procedure**, not a fully re-executed verification record.

## Procedure E — Maintain Google Workspace Action Configuration

1. Open High Director GPT Builder and the `www.googleapis.com` Action.
2. Compare the current Action schema with `_docs/high-director/google-workspace-action.md`.
3. Verify Authentication remains OAuth unless an approved security decision changes it.
4. Verify the documented authorization endpoint, token endpoint, token exchange method, and scopes.
5. If any OAuth scope changes, stop for explicit security/access-control approval.
6. If the schema changes Calendar/Gmail mutation behavior, review confirmation rules before applying it.
7. Never capture or publish Client ID, Client Secret, access token, refresh token, authorization code, or connected-account identifiers.
8. Apply only the approved configuration/schema change.
9. Update canonical documentation through Procedure A.

## Validation and Success Criteria

A maintenance/update is complete only when all applicable checks pass:

- GPT configuration matches the documented intended state;
- Action schema matches the approved callable contract;
- Lambda runtime/handler/configuration match the approved deployment where applicable;
- low-risk integration checks succeed;
- sensitive values are absent from public documentation;
- documentation validation succeeds;
- documentation PR merges;
- matching Pages deployment succeeds;
- persistent plan is synchronized.

## Rollback or Recovery

### Documentation-only change

Create a focused follow-up PR restoring the last verified documentation state. Validate, merge, and verify Pages normally.

### GPT configuration/schema change

Restore the last verified configuration/schema from the canonical documentation/source snapshot, provided doing so does not require restoring a secret value. Reconnect/re-enter credentials through the platform UI only when necessary and approved.

### Lambda deployment

Rollback method depends on the AWS deployment/version state. Deployment history, Lambda aliases/versions, and rollback automation are not yet verified, so do not claim a one-command rollback. If a code deployment causes failure, stop further writes, preserve evidence, and use the troubleshooting/handoff runbook once available.

## Failure Modes and Escalation

| Failure | Safe response | Evidence |
| --- | --- | --- |
| Documentation validation fails | Do not merge; inspect failing validator step and correct the documentation defect | Validation run/job/step |
| Pages deployment fails | Do not begin next major phase; inspect failed build/deploy job | Pages run/job/step |
| GitHub Action returns 401 | Do not expose/re-enter key in documentation; verify configured Action auth and Lambda env/key state through secure UI | Status/error only, no key value |
| GitHub Action returns repo-format error | Use repository name only; do not ask for owner | API error response |
| Lambda/GitHub transport/API failure | Stop risky mutations; preserve error/status details without secrets | Wrapper error object/status |
| Google mutation cannot be confirmed safely | Do not send/create/update/delete/move | Proposed operation details only |

## Security Guidance

- Never publish credential values.
- Treat Gmail/calendar content and private repository content as non-public unless explicitly sanitized and required.
- Do not weaken auth/IAM/OAuth controls as a troubleshooting shortcut.
- Do not expand GitHub PAT permissions or Google OAuth scopes without explicit approval.
- Do not change Function URL auth mode without an explicit architecture/security decision.

## Known Limitations

- Fresh Lambda deployment procedure is derived from authoritative source but not fully re-executed here.
- Lambda rollback/version/alias strategy is unverified.
- CloudWatch monitoring/retention/alarms are unverified.
- GitHub PAT exact permissions/rotation are unverified.
- Google OAuth reconnect/revocation procedure is not yet fully documented.

## Next Safe Action

After this runbook is validated, merged, and deployed, create a separate troubleshooting/handoff runbook covering failure diagnosis, recovery evidence, unresolved monitoring gaps, and continuation procedures.

## Related Documents

- [High Director Runtime Architecture]({{ '/projects/high-director/runtime-architecture/' | relative_url }})
- [High Director Data Flows]({{ '/projects/high-director/data-flows/' | relative_url }})
- [High Director Security and Configuration Reference]({{ '/projects/high-director/security-configuration-reference/' | relative_url }})
- [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }})
- [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})
- [Publish a Documentation Change]({{ '/projects/runbooks/publish-documentation-change/' | relative_url }})

## Verification Record

- Last verified: `2026-08-06`
- Verified against: authoritative configuration/source plus successfully exercised documentation publication flow
- Verified by: High Director documentation process
- Verification scope: documentation operations and source/configuration comparison; deployment steps source-derived where noted
- Known unverified steps: fresh SAM deploy, Lambda rollback, Google OAuth reconnect/revocation
