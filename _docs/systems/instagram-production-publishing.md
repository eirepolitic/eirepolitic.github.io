---
title: Instagram production publishing and scheduling
summary: Production workflow for publishing reviewed Eirepolitic Instagram factory outputs immediately or through one-time EventBridge scheduling, with immutable assets, approval fingerprints, durable execution state, and Meta Graph API delivery.
section: systems
doc_type: system
status: active
created: 2026-09-27
updated: 2026-09-27
last_verified: 2026-09-27
owner: Eire Politic
system: Instagram production publishing
repository: eirepolitic-data-pipeline
order: 42
permalink: /projects/systems/instagram-production-publishing/
technologies:
  - GitHub Actions
  - AWS Lambda
  - Amazon DynamoDB
  - Amazon S3
  - EventBridge Scheduler
  - Amazon SQS
  - AWS Secrets Manager
  - Meta Instagram Graph API
related:
  - /projects/repositories/eirepolitic-data-pipeline/
  - /projects/systems/instagram-constituency-campaign-rendering/
  - /projects/systems/instagram-ai-member-profile-content-workflow/
---

# Instagram production publishing and scheduling

## Summary

Eirepolitic now has a production Instagram publication system in `Eirepolitic-data-pipeline` for reviewed outputs from the Instagram content factory.

The supported operator/agent path is:

1. run **Instagram factory render (generic)**;
2. review the generated preview;
3. copy the factory GitHub Actions run ID;
4. run **Instagram publish (standard)**;
5. choose `scheduled` or `immediate`;
6. for scheduled mode, provide local time plus an IANA timezone;
7. allow the workflow to promote the exact reviewed artifact into immutable production state and execute it.

Agents should not recreate the mechanism with direct Meta calls, manual S3 uploads, custom EventBridge schedules, or temporary Lambda actions.

## Canonical source of truth

The implementation and detailed runbook live in `Eirepolitic-data-pipeline`:

- `docs/operations/instagram_publishing_standard.md` — canonical operating contract;
- `instagram/PUBLISHING.md` — agent quick-start;
- `.github/workflows/instagram_factory_render.yml` — content render/review source;
- `.github/workflows/instagram_publish_standard.yml` — normal publication interface;
- `.github/workflows/deploy_instagram_publisher_lambda.yml` — maintenance only;
- `publishing/standard_pipeline.py` — factory artifact promotion and approval;
- `publishing/lambda_handler.py` — immediate/scheduled execution entrypoint.

If this page and repository implementation ever differ, the canonical runbook and current code in `Eirepolitic-data-pipeline` win.

## Factory-to-publisher boundary

The factory remains deliberately non-publishing. Successful generic renders emit a machine-readable `publication_handoff.json` into the uploaded `generated_render/` artifact. That handoff records relative slide paths, caption path when present, project/period identity, QA result, and the factory safety flags.

The factory continues to report `publication_enabled=false`. Production publishing authority is created separately when `Instagram publish (standard)` records an approval fingerprint for the exact immutable assets, caption, Instagram options, and publication version.

This separation prevents content-generation code from silently becoming a publication authority.

## Standard workflow inputs

Required:

- `factory_run_id` — GitHub Actions run ID from the reviewed generic factory render;
- `approved_by` — human/operator identity approving the exact output;
- `mode` — `scheduled` or `immediate`.

Scheduled mode also requires:

- `scheduled_local` — local timestamp in `YYYY-MM-DDTHH:MM:SS` form;
- `timezone` — IANA timezone, for example `America/Vancouver`.

Optional:

- `caption_override` — only when the factory artifact contains no caption file;
- `options_json` — advanced Instagram options such as alt text, media tags, collaborators, location ID, or first comment.

The normal default for `options_json` is `{}`.

## Publication lifecycle

The standard workflow:

1. downloads the exact factory artifact by run ID;
2. validates the portable handoff and QA state;
3. converts slides to deterministic delivery JPEGs;
4. uploads content-addressed immutable assets to the private approved-assets S3 bucket;
5. persists the `AssetPackage` in DynamoDB;
6. creates the exact `PublicationRequest`;
7. records an approval fingerprint tied to that request and asset hashes;
8. either invokes the Lambda immediately or creates a one-time EventBridge Scheduler job;
9. persists Meta container IDs and permanent media IDs through the durable execution store;
10. marks the control record `published` after successful `/media_publish`.

For scheduled posts, Scheduler contains only publication identity/version. The approved content stays in DynamoDB/S3 and credentials stay in Secrets Manager.

## Retry and idempotency behavior

The publisher does not rely on process memory for retry safety. Execution-attempt state is stored in DynamoDB, including Meta container/media identifiers and operation status.

If a Lambda invocation is retried, the runtime reloads that durable state and reuses the existing provider identifiers instead of blindly creating another post. One-time EventBridge schedules use a dedicated execution role, SQS DLQ, bounded retry policy, and `ActionAfterCompletion=DELETE`.

## Production verification

The system was proven against the real Eirepolitic Instagram Professional account on September 26, 2026.

**Gate 4 immediate canary:** a real test image/caption was published successfully through the production S3 → DynamoDB → Lambda → Meta `/media` → `/media_publish` path. The returned permanent Instagram media ID was persisted and the test post was then manually deleted.

**Gate 5 scheduled canary:** the same neutral test content was published successfully by a one-time EventBridge Scheduler invocation at the requested Pacific time. The schedule, target, role, DLQ, and payload were verified before execution. The post was manually deleted after verification.

These canaries established that both immediate and scheduled production paths work end to end.

## Agent operating rule

When an agent is asked to publish a factory-generated post, it should use `Instagram publish (standard)` rather than design or improvise a publication mechanism.

Default sequence:

1. verify the factory render completed;
2. confirm the exact preview was reviewed;
3. obtain the factory run ID;
4. use scheduled mode unless immediate publication was explicitly requested;
5. preserve the user's requested local time and timezone exactly;
6. report both the local time and resolved UTC time for scheduled posts;
7. report the resulting publication/schedule state after the workflow completes.

If the artifact has no caption, obtain the exact approved caption and pass it through `caption_override`. Do not invent missing copy unless the user explicitly asks the agent to write it.

## AWS production components

Region: `us-east-2`.

Core components:

- Lambda: `eirepolitic-instagram-publisher`;
- DynamoDB publication ledger: `eirepolitic-publications`;
- Scheduler group: `eirepolitic-instagram`;
- Scheduler execution role: `eirepolitic-instagram-scheduler-execution`;
- Scheduler DLQ: `eirepolitic-instagram-scheduler-dlq`;
- private versioned approved-assets S3 bucket from the runtime-support stack;
- Secrets Manager secret: `eirepolitic/instagram/publishing`.

The publishing workflow accesses AWS through the established GitHub → `HighDirectorAwsAdmin` STS path. Secret values are not stored in repository documentation.

## Maintenance boundary

`Instagram publishing infrastructure operations` is a maintenance workflow for Lambda deployment, CloudFormation stacks, healthcheck, and infrastructure status. It is not the normal posting interface.

Normal publication always uses `Instagram publish (standard)`.

## Verification record

- Last verified: `2026-09-27`
- Immediate production publish verified: `2026-09-26`
- Scheduled production publish verified: `2026-09-26`
- Canonical repository: `Eirepolitic-data-pipeline`
- Canonical runbook: `docs/operations/instagram_publishing_standard.md`
