---
title: Instagram and constituency campaign rendering system
summary: Current rendering architecture for constituency carousels, member-profile campaign cards, external-template tests, review artifacts, copy packs, gated publish queues, and optional S3 previews.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
system: Instagram campaign rendering
repository: eirepolitic-data-pipeline
order: 40
permalink: /projects/systems/instagram-constituency-campaign-rendering/
technologies:
  - Python
  - GitHub Actions
  - AWS S3
  - pandas
  - Pillow
  - Jinja2
  - Playwright
  - Bannerbear
  - Placid
related:
  - /projects/systems/irish-politics-analytics/
  - /projects/repositories/eirepolitic-data-pipeline/
  - /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
---

# Instagram and constituency campaign rendering system

## Summary

`eirepolitic-data-pipeline` contains several related Instagram rendering paths that share data/context concepts but have different purposes:

1. a local constituency-carousel renderer that builds HTML with Jinja2 and screenshots it with Playwright;
2. a local deterministic JSON-template renderer implemented with Pillow;
3. a campaign renderer for `member_profile_batch_v1` that selects rows from member-profile metrics, renders profile cards, builds review artifacts, deterministic caption/alt-text drafts, and a review-gated queue;
4. external-template test adapters for Bannerbear and Placid with explicit YAML field mappings and local-HTML fallback;
5. experimental AI-image paths documented separately under the P1 AI content workflow.

The current manual campaign workflow produces review assets only. It does **not** publish, schedule, or approve Instagram posts.

## Current implementation state

**Verified implementation:** `.github/workflows/instagram_campaign_render.yml` is a manual `workflow_dispatch` controller for the current campaign renderer. Its default campaign is `member_profile_batch_v1`.

**Verified implementation:** `process/instagram_render_campaign.py` currently accepts only `campaign: member_profile_batch_v1`. It reads the campaign's configured metrics CSV, selects members, renders PNG cards through `instagram/renderer/template_renderer.py`, and initializes every generated review item as `review_status=needs_review` and `publish_ready=no`.

**Verified implementation:** the workflow subsequently builds deterministic captions/alt text and a publish-queue file. Queue inclusion requires explicit review approval, `publish_ready=yes`, and empty `safety_notes`. Creating a queue file does not publish content.

**Verified implementation:** the older/general constituency carousel path in `process/instagram_render_post.py` remains executable and has a local fixture regression test. It renders enabled constituency/member/issues/glossary slides from S3 or local fixture data using Jinja2 + Playwright.

**Implementation present, live external configuration unverified:** `process/instagram_template_pipeline.py` implements Bannerbear and Placid adapters. Missing provider credentials/template references can fall back to local HTML unless fallback is disabled. Checked-in code proves the adapters; this workstream has not verified live provider accounts, secrets, template IDs, or successful provider renders.

## Source of truth

| Concern | Current source |
| --- | --- |
| manual campaign controller | `.github/workflows/instagram_campaign_render.yml` |
| campaign rendering | `process/instagram_render_campaign.py` |
| current campaign spec | `instagram/campaigns/member_profile_batch_v1/render_spec.yml` |
| deterministic JSON-template rendering | `instagram/renderer/template_renderer.py` |
| template layouts/palettes | `instagram/templates/layouts/*.json`, `instagram/templates/palettes/*.json` |
| campaign copy pack | `process/instagram_build_copy_pack.py` |
| review-gated queue | `process/instagram_build_publish_queue.py` |
| optional S3 preview upload | `process/instagram_upload_preview_to_s3.py` |
| constituency HTML renderer | `process/instagram_render_post.py` |
| external provider adapter tests | `process/instagram_template_pipeline.py`, `instagram/mappings/*.yml`, `instagram/specs/*constituency*.yml` |
| local renderer regression test | `tests/test_instagram_renderer.py` |

`instagram/README.md` is useful context but current code/workflows are stronger evidence.

## Current system boundary

Included:

- constituency/member context building from political datasets;
- deterministic local rendering;
- member-profile batch campaign selection/rendering;
- HTML/PNG and JSON/YAML metadata artifacts;
- human-review index/table generation;
- deterministic draft captions and alt text;
- review-gated queue generation;
- optional S3 preview upload;
- Bannerbear/Placid request generation and fallback test paths.

Not included:

- automatic Instagram publishing;
- automatic approval;
- social-platform credential handling for posting;
- editorial sign-off;
- AI member-profile image editing, which is a separate P1 target;
- canonical political-data production, documented under the Unified Oireachtas platform.

## Path A: member-profile campaign renderer

### Campaign specification

Current production-like campaign configuration is:

`instagram/campaigns/member_profile_batch_v1/render_spec.yml`

It declares:

```text
campaign: member_profile_batch_v1
post_type: member_profile
selector: top_speech_count
selector limit: 10
source: s3://eirepolitic-data/processed/members/member_profile_metrics_2025.csv
template: instagram/templates/layouts/profile_card_v1.json
output: generated_posts/member_profile_batch_v1
palette: eirepolitic_dark
```

The footer identifies Oireachtas pipeline data for 2025.

### Selection behavior

`process/instagram_render_campaign.py` supports three selector modes:

- `top_speech_count`: descending speech count, then ascending member name;
- `all_with_photos`: rows with a nonblank `photo_url`;
- `explicit_members`: rows whose normalized full name is in the configured name list.

The current checked-in campaign uses `top_speech_count`.

The renderer currently prefers 2025 metric columns such as `speech_count_2025`, `speech_rank_2025`, `vote_participation_pct_2025`, and `top_issue_2025`, with limited fallbacks for some fields. This makes the current campaign implementation year-specific even though the separate Member Profile Metrics Builder supports a configurable target year.

### Binding contract

For each selected row the campaign renderer generates bindings including:

- `member_name`
- `party`
- `constituency`
- `member_photo`
- `top_issue`
- `vote_participation`
- `speech_rank`
- `speech_count_text`
- `footer_text`

Bindings are written under:

```text
generated_posts/member_profile_batch_v1/metadata/bindings/<member-slug>.yml
```

### Deterministic template renderer

`instagram/renderer/template_renderer.py` reads a JSON layout and YAML/JSON bindings, resolves a named palette, and renders PNG with Pillow.

Supported element types are:

- `rectangle`
- `text`
- `image`
- `line`

Text supports wrapping, maximum lines, optional shrink-to-fit, alignment, vertical alignment, and ellipsis at the minimum font size. Image elements support local paths or HTTP(S), contain/stretch/cover behavior, backgrounds, and rounded masks.

Missing bindings, missing images, image-load failures, and unsupported elements are recorded as warnings rather than silently discarded.

Each render writes:

- the PNG;
- a source-values JSON containing bindings, template ID, palette, timestamp, and warnings;
- a render manifest with dimensions, renderer version, template ID, path, and warnings.

### Review output

`write_review()` creates:

```text
<output_root>/review/review_table.csv
<output_root>/review/review_manifest.json
<output_root>/review/review_index.html
```

Every new item defaults to:

```text
review_status = needs_review
publish_ready = no
```

Review metadata also flags missing photos and render warnings. The generated checklist requires checking member identity, party/constituency, photo identity, metrics, text clipping/truncation, and renderer warnings.

This is an explicit human-review boundary.

## Draft copy and queue gating

### Copy pack

`process/instagram_build_copy_pack.py` turns the review table into deterministic drafts:

```text
<output_root>/copy/<member>.caption.txt
<output_root>/copy/<member>.alt_text.txt
<output_root>/copy/captions.csv
<output_root>/copy/copy_manifest.json
```

The current draft caption states the member, party, constituency, top 2025 debate issue, vote participation, speech count/rank, source note, and default hashtags. The code labels this copy as draft and instructs review before publishing.

This is deterministic string assembly, not an LLM step.

### Publish queue

`process/instagram_build_publish_queue.py` separates rows into:

```text
<output_root>/queue/publish_queue.csv
<output_root>/queue/blocked_items.csv
<output_root>/queue/publish_queue_manifest.json
```

An item is queued only when all three conditions are met:

1. `publish_ready` is yes/true/1;
2. `review_status` is one of `approved`, `ready`, `ready_to_publish`, or `publish_ready`;
3. `safety_notes` is empty.

Anything else is written to `blocked_items.csv` with reasons.

The queue builder explicitly states that it creates a queue file only and that publishing must remain a separate explicit step.

## Manual GitHub Actions workflow

Workflow name: **Instagram Campaign Render (Manual)**.

Inputs:

- `campaign_slug`, default `member_profile_batch_v1`;
- `spec_file`, default `render_spec.yml`;
- `limit`, default `3`;
- `upload_preview`, default `false`;
- `preview_public_read`, default `false`;
- `preview_root_prefix`, default `instagram/previews`.

Runtime:

- `ubuntu-latest`;
- Python 3.11;
- repository `requirements.txt`;
- AWS credentials from repository secrets;
- S3 bucket `eirepolitic-data`.

The workflow:

1. checks out source;
2. installs dependencies;
3. renders the selected campaign;
4. builds the copy pack;
5. builds the gated queue;
6. optionally uploads review assets to S3 and generates preview links;
7. uploads `generated_posts/**` and workflow debug files as a GitHub artifact.

Concurrency group: `instagram-campaign-render`, with `cancel-in-progress: false`.

The workflow summary explicitly says it is review-only and does not publish, schedule, or approve Instagram content.

## Optional S3 preview path

`process/instagram_upload_preview_to_s3.py` can upload the entire generated campaign output to both a versioned run prefix and a campaign `latest` prefix:

```text
instagram/previews/<campaign>/<run-label>/...
instagram/previews/<campaign>/latest/...
```

The workflow default is **not** to upload previews.

The upload helper can request `public-read` ACL only when explicitly enabled. Whether that results in public access also depends on bucket-level controls, which have not been verified here. Do not assume preview URLs are public from source code alone.

The `latest` preview prefix is overwritten by subsequent preview uploads for the same campaign; run-labelled prefixes preserve per-run review artifacts.

## Path B: constituency HTML carousel

`process/instagram_render_post.py` is the local constituency carousel path.

It loads a YAML post spec and builds context from these default dataset candidates:

- members: `raw/members/oireachtas_members_34th_dail.csv`;
- summaries: `processed/members/members_summaries.csv`;
- photos: `processed/members/member_photos/members_photo_urls.csv`, then `processed/members/members_photo_urls.csv` fallback;
- debate issues: `processed/debates/debate_speeches_classified.csv`;
- constituency images: `processed/constituencies/constituency_images.csv`.

Each dataset list can be overridden through an `INSTAGRAM_*_DATASET_KEYS` environment variable.

The renderer:

1. loads the first available CSV for each dataset;
2. joins member photos/backgrounds where possible;
3. normalizes names and constituency names;
4. matches classified debate issues to known members;
5. selects a requested member or defaults to the constituency member with the highest classified-speech count;
6. builds constituency/member issue counts and slide context;
7. renders enabled Jinja2 slide templates;
8. screenshots them with Playwright Chromium;
9. writes `post_context.json`, HTML, and PNG output.

Supported template types currently map to constituency overview, top issues, member profile, and glossary templates.

`tests/test_instagram_renderer.py` verifies a local fixture render creates five expected PNG slides and produces the expected Wicklow-Wexford/Aoife Byrne context.

## Path C: external template-provider tests

`process/instagram_template_pipeline.py` reuses the constituency context builder and adds explicit provider mappings.

Implemented provider values:

- `bannerbear`
- `placid`
- `local_html`

Bannerbear and Placid mappings are YAML files under `instagram/mappings/`. The code builds per-slide request payloads, records request/response JSON, polls asynchronous provider results when needed, downloads provider PNGs, and writes a run summary.

If the requested provider fails with a pipeline/provider configuration error, local HTML fallback occurs only when:

- fallback is not explicitly skipped;
- configured fallback provider is `local_html`;
- requested provider is not already `local_html`.

Live provider status is **unverified** in this documentation workstream. The source proves adapters and expected environment-variable names, not the existence of configured provider accounts/templates or successful current renders.

## Relationship to Unified Oireachtas data

There are two implementation generations in the rendering system:

- the constituency HTML/provider-test path defaults to older compatibility/legacy S3 dataset locations;
- the current member-profile campaign path reads `processed/members/member_profile_metrics_2025.csv`;
- the current Member Profile Metrics Builder can itself consume Unified Oireachtas compatibility products and can write candidate-batch consumer outputs when invoked in Oireachtas validation.

Therefore the Instagram layer is downstream of the Oireachtas platform but has not uniformly migrated every renderer input to canonical `processed/oireachtas_unified/...` keys. Do not rewrite these paths in documentation or code without confirming each component's cutover state.

## Authentication and security boundaries

Verified credential boundaries:

- campaign workflow uses `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_REGION` repository secrets;
- Bannerbear code expects an API-key environment variable, default `BANNERBEAR_API_KEY`;
- Placid code expects an API-token environment variable, default `PLACID_API_TOKEN`;
- provider template references can be read indirectly from environment variables via `env:<NAME>` mapping values.

No secret values are documented here.

The optional preview workflow can request public-read ACL. Because bucket public-access configuration is unverified, any change to preview visibility should be treated as an access-control decision, not routine documentation work.

## Failure modes

Verified failure paths include:

- missing/unreadable campaign source CSV;
- unsupported campaign or selector mode;
- missing JSON layout/palette/binding file;
- missing image or network image-load failure, usually surfaced as render warnings;
- provider credential/template-reference failure;
- provider render timeout/failure/missing image URL;
- constituency with no matching member;
- missing required members dataset for constituency rendering;
- S3 preview upload failure;
- queue blocking because review is incomplete, photo/render warnings remain, or `publish_ready` is not affirmative.

A render completing does not mean it is approved for publication. Review/queue state is a separate gate.

## Safe operating procedure

For the current member-profile campaign:

1. Use the manual **Instagram Campaign Render (Manual)** workflow.
2. Leave preview upload disabled unless S3 review links are required.
3. Render a small limit first when changing templates/bindings.
4. Inspect PNGs, `review_index.html`, `review_table.csv`, source-values metadata, and render warnings.
5. Verify names, party, constituency, photos, source metrics, and any truncation.
6. Only after review, update the review state used to build the copy/queue artifacts.
7. Confirm blocked/queued output reflects the intended approval state.
8. Treat the queue as a handoff artifact only; there is no publishing step in this workflow.

For provider tests, keep local fallback enabled unless the purpose is explicitly to prove the provider path and fail on missing provider configuration.

## Known limitations

- `member_profile_batch_v1` is hard-coded as the only campaign supported by `instagram_render_campaign.py`.
- The current campaign renderer is explicitly tied to 2025 metric column names.
- Constituency rendering still defaults to older S3 inputs rather than uniformly reading the unified compatibility namespace.
- Local Pillow text fitting can truncate/ellipsize text; human review remains required.
- Remote image rendering depends on network availability and source image correctness.
- External provider live configuration/status is not verified.
- The workflow creates no social-platform post and therefore does not prove a production Instagram publishing integration exists.
- Test coverage currently proves a local constituency fixture path; it is not comprehensive across every campaign/provider path.

## Next safe development action

Document the separate P1 AI member-profile / Instagram content workflow, including the Option 5 image-generation/edit paths, their prompts/specs, workflow controls, external API boundaries, generated review artifacts, and relationship to the deterministic renderer. Do not conflate experimental AI generation with the deterministic campaign renderer documented here.

## Related documents

- [Irish Politics Analytics](/projects/systems/irish-politics-analytics/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)

## Verification record

- Last verified: `2026-08-07`
- Verified implementation/configuration: full `instagram/` tree; `process/instagram*` tree; Instagram workflow tree; `process/instagram_render_campaign.py`; `instagram/renderer/template_renderer.py`; `instagram/campaigns/member_profile_batch_v1/render_spec.yml`; `process/instagram_build_copy_pack.py`; `process/instagram_build_publish_queue.py`; `process/instagram_render_post.py`; `process/instagram_template_pipeline.py`; `process/instagram_upload_preview_to_s3.py`; `.github/workflows/instagram_campaign_render.yml`; `tests/test_instagram_renderer.py`.
- Historical/supporting evidence: `instagram/README.md` consulted but not used to override current source.
- Verification scope: current renderer paths, data inputs, templates, campaign selection/bindings, review gate, deterministic copy/queue, optional S3 preview, external-provider adapter boundary, security boundary, failure modes, limitations, and local fixture test coverage.
