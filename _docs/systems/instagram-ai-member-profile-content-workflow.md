---
title: AI member-profile and Instagram visual content workflow
summary: Experimental manual OpenAI-assisted Instagram visual workflows for member-profile template edits and constituency-cover background generation, including source-truth controls, validation, outputs, security boundaries, runtime evidence, and current lineage limitations.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
system: AI member-profile and Instagram visual content workflow
repository: eirepolitic-data-pipeline
order: 41
permalink: /projects/systems/instagram-ai-member-profile-content-workflow/
technologies:
  - Python
  - GitHub Actions
  - OpenAI API
  - AWS S3
  - pandas
  - Playwright
related:
  - /projects/systems/instagram-constituency-campaign-rendering/
  - /projects/systems/irish-politics-analytics/
  - /projects/repositories/eirepolitic-data-pipeline/
  - /projects/high-director/ipa-oireachtas-documentation-workstream-plan/
---

# AI member-profile and Instagram visual content workflow

## Summary

`eirepolitic-data-pipeline` contains two checked-in **Option 5** OpenAI-assisted Instagram visual experiments:

1. a **member-profile template edit** that uses an existing member-profile slide as the master visual template, replaces the portrait and exact visible values, runs a vision-model validation of the first pass, and always produces a second corrective image edit; and
2. a **constituency-cover background generation** test that asks the image model only for a decorative background, then overlays exact constituency text through the deterministic local renderer.

Both workflows are manual GitHub Actions tests. They generate review artifacts; neither workflow publishes, schedules, or approves Instagram posts. The Option 5 source also does not generate captions or social copy.

The deterministic Instagram campaign/rendering system remains the safer publication-oriented review path and is documented separately.

## Current implementation state

**Verified implementation:** both Option 5 workflows exist on current `eirepolitic-data-pipeline/main` and use `workflow_dispatch` only.

**Verified implementation:** both workflows use OpenAI image generation/editing through `OPENAI_API_KEY` and GitHub-hosted execution. They write generated visual evidence to GitHub Actions artifacts.

**Verified implementation:** the member-profile workflow requires a checked-in template at `instagram/reference/member_profile_template.png`. The file is currently present. Older documentation that says the template still needs to be added is historical/stale.

**Verified implementation:** the member-profile spec declares both `review_required: true` and `source_truth_sidecar_required: true`.

**Observed runtime evidence:** the constituency-cover workflow completed successfully in run `24966222811` on 2026-04-26. The member-profile workflow had one failed initial run (`24969650417`) followed by successful runs `24970078480` and `24970547529`, with the latest observed success on 2026-04-27. These runs prove those historical revisions executed successfully; they do not guarantee current `main` will still succeed unchanged.

## Source of truth

| Concern | Current source |
| --- | --- |
| member-profile workflow | `.github/workflows/instagram_option5_member_profile_ai.yml` |
| member-profile edit implementation | `process/render_member_profile_ai_edit.py` |
| member-profile AI spec | `instagram/specs/member_profile_ai_test.yml` |
| checked-in master template | `instagram/reference/member_profile_template.png` |
| constituency-cover workflow | `.github/workflows/instagram_option5_constituency_cover_ai.yml` |
| constituency experiment spec | `instagram/specs/constituency_cover_ai_test.yml` |
| constituency job preparation | `process/instagram_option5_prepare_constituency_cover_test.py` |
| constituency image generation | `process/instagram_option5_generate_images.py` |
| constituency review sheet | `process/instagram_option5_build_review_sheet.py` |
| deterministic overlay renderer | `process/instagram_render_post.py` |
| current metrics implementation | `process/build_member_profile_metrics.py` |
| 2025 compatibility wrapper | `process/build_member_profile_metrics_2025.py` |
| legacy vote-record extractor still invoked by member AI workflow | `process/build_dail_votes_member_records.py` |

`instagram/OPTION5_MEMBER_PROFILE_AI_EDIT.md` and `instagram/OPTION5_LLM_IMAGE_TEST.md` are useful design/history notes, but current implementation wins where they differ.

## System boundary

Included:

- manual OpenAI image-generation/image-edit calls;
- member-profile source-truth preparation;
- first-pass member-profile image editing;
- machine validation of the first-pass image;
- second corrective image editing;
- constituency background prompt preparation and generation;
- deterministic constituency-title overlay;
- source sidecars, prompt records, model-response metadata, manifests, review sheets, and GitHub artifacts;
- current upstream member metrics preparation invoked by the member-profile workflow.

Not included:

- automatic Instagram publishing or scheduling;
- automatic editorial approval;
- LLM caption/social-copy generation;
- the deterministic member-profile/campaign renderer itself;
- the reusable generic LLM table runner;
- current canonical Oireachtas production orchestration except as an upstream data source.

## Path A: member-profile template AI edit

### Workflow

Workflow name: **Generate Instagram Option 5 Member Profile AI Edit Test (Manual)**.

Current manual inputs:

| Input | Default |
| --- | --- |
| `date_start` | `2025-01-01` |
| `date_end` | `2025-12-31` |
| `model` | `gpt-image-1` |
| `spec_path` | `instagram/specs/member_profile_ai_test.yml` |

Runtime:

- `ubuntu-latest`;
- Python 3.11;
- timeout 120 minutes;
- concurrency group `instagram-option5-member-profile-ai-edit`;
- `cancel-in-progress: false`;
- repository contents permission read-only.

The workflow currently runs:

1. `process/build_dail_votes_member_records.py`;
2. `process/build_member_profile_metrics_2025.py`;
3. `process/render_member_profile_ai_edit.py`;
4. uploads `generated_visual_tests/option5_member_profile_ai/` as a GitHub artifact.

### Current data-lineage drift

The workflow order still suggests that the legacy vote-record extractor feeds the 2025 metrics build. Current source shows that is no longer the default lineage.

`process/build_member_profile_metrics_2025.py` is now only a backward-compatible wrapper that sets `TARGET_YEAR=2025` and calls `process/build_member_profile_metrics.py`.

The generic metrics builder currently defaults to Unified Oireachtas compatibility inputs:

```text
processed/oireachtas_unified/compat/members/oireachtas_members_34th_dail_compat.csv
processed/oireachtas_unified/compat/votes/dail_vote_member_records_compat.csv
processed/oireachtas_unified/compat/media/members_photo_urls_compat.csv
processed/oireachtas_unified/compat/debates/debate_speeches_classified_compat.csv
```

Without environment-variable overrides, the preceding legacy vote extractor writes legacy `processed/votes/...` files that the current metrics builder does **not** read.

Therefore the current workflow's `build_dail_votes_member_records.py` step is a verified redundant/legacy side effect in the default configuration, not the active vote lineage feeding member metrics. Do not remove it as part of documentation work; any cleanup is a separate implementation change.

### Metrics output consumed by the AI edit

With `TARGET_YEAR=2025` and no candidate batch ID, the generic metrics builder writes:

```text
processed/members/member_profile_metrics_2025.csv
processed/members/parquets/member_profile_metrics_2025.parquet
```

`render_member_profile_ai_edit.py` defaults to reading:

```text
processed/members/member_profile_metrics_2025.csv
```

The current metrics fields used by the AI edit include:

- `member_code`;
- `full_name`;
- `constituency`;
- `party`;
- `photo_url`;
- `top_issue_2025`;
- `top_issue_count_2025`;
- `vote_participation_pct_2025`;
- `distinct_votes_participated_2025`;
- `all_distinct_vote_ids_2025`;
- `speech_count_2025`;
- `speech_rank_2025`.

Detailed metric definitions belong in the Member Profile Metrics Builder documentation.

### Member selection

`instagram/specs/member_profile_ai_test.yml` currently declares:

```text
pipeline_option: 5
mode: template_based_member_profile_ai_edit
review_required: true
source_truth_sidecar_required: true
year: 2025
```

The implementation:

1. keeps only metrics rows with a nonblank `photo_url`;
2. applies configured member-name exclusions;
3. sorts by `speech_count_2025` descending, then `full_name` ascending;
4. selects the first remaining member.

This is a single-member experiment, not a batch campaign renderer.

### Master template and member photo

The current template source is:

```text
instagram/reference/member_profile_template.png
```

The file exists in current source.

The member portrait is downloaded from the selected row's `photo_url`. The helper accepts HTTP(S) image URLs or local files and persists a local input copy for the run.

### Run layout

Each run is written beneath:

```text
generated_visual_tests/option5_member_profile_ai/<member-slug>__<UTC timestamp>/
```

with:

```text
inputs/
  template_image.*
  member_photo.*
outputs/
  member_profile_ai_edit_v1.png
  member_profile_ai_edit_v2.png
  member_profile_ai_edit.png
metadata/
  source_values.json
  prompt_v1.txt
  prompt_v2.txt
  validation_report.json
  openai_response_v1.json
  openai_response_v2.json
  validation_response.json
```

`member_profile_ai_edit.png` is currently a convenience alias/copy of the second-pass output.

## Member-profile source-truth controls

Before calling OpenAI, the script writes `metadata/source_values.json` containing the selected member and exact metric values plus explicit risk notes.

The exact visible values supplied to the image-edit prompts are:

- full name;
- constituency;
- party;
- top issue;
- vote participation percentage;
- speech rank.

The first prompt instructs the model to:

- use the first image as the master template;
- use the second image only as the replacement portrait;
- preserve layout, border ornaments, color palette, spacing, typography style, framing, and composition;
- replace old visible values with the supplied exact values;
- avoid redesigning the slide;
- avoid extra badges, logos, labels, charts, or invented values.

The prompt itself is saved for audit/review.

## Member-profile OpenAI call sequence

A normal current run performs **three OpenAI calls**:

1. **Image edit v1** using the master template plus member photo.
2. **Vision/text validation** using the template and generated v1 image through the OpenAI Responses API.
3. **Image edit v2** using the template, member photo, v1 image, and correction guidance.

The current image-model default is `gpt-image-1` and the current default requested size is `1024x1536`.

The current validation-model default is `gpt-4.1-mini`.

Because the workflow always performs two image edits plus one validation call, every manual run has an external API cost boundary. Actual cost depends on the active OpenAI pricing/model settings and is not encoded as a fixed repository value.

## First-pass machine validation

`validate_v1()` sends:

- the original template image;
- the generated v1 image;
- the exact source truth rendered into the validation prompt.

It requests structured JSON with:

- `template_fidelity_score` from 0 to 10;
- `text_legibility_score` from 0 to 10;
- `formatting_issues`;
- `suspect_text`;
- `needs_second_pass`;
- `correction_instructions`.

This validation is advisory input to the next edit. It is not an approval gate.

The implementation then sets:

```text
second_pass_policy = always_run
```

and performs the second edit regardless of the returned `needs_second_pass` value.

## Second-pass behavior and review boundary

The second-pass prompt reuses exact source values and incorporates validation issues/correction instructions. It supplies the template, member photo, and first-pass draft to the image edit.

Current source does **not** perform another machine vision validation of v2 after that second edit. It simply writes v2 and copies it to the `member_profile_ai_edit.png` latest alias.

Therefore:

- first-pass machine validation does not prove v2 correctness;
- v2 is not automatically approved;
- the final output must still be reviewed against `source_values.json`, the selected portrait, and visible expected text.

## Path B: constituency-cover AI background test

### Workflow

Workflow name: **Generate Instagram Option 5 Constituency Cover AI Test (Manual)**.

Current inputs:

| Input | Default |
| --- | --- |
| `constituency` | `Wicklow-Wexford` |
| `variant_count` | `1` |
| `model` | `gpt-image-1` |
| `style_mode` | `both` |
| `spec_path` | `instagram/specs/constituency_cover_ai_test.yml` |

Supported style modes are:

- `both`;
- `map_poster`;
- `textured_editorial`.

Runtime is Python 3.11 on `ubuntu-latest`, timeout 90 minutes, concurrency group `instagram-option5-constituency-cover-ai`, with `cancel-in-progress: false`.

The workflow:

1. prepares the experimental run/jobs;
2. generates OpenAI images;
3. recreates a blank human-review sheet;
4. renders deterministic cover overlays using `process/instagram_render_post.py` and Playwright;
5. uploads the run folder as a GitHub artifact.

### Safety-by-design text policy

The constituency spec explicitly sets:

```text
safe_first_target: constituency_cover
review_required: true
safe_text_policy: deterministic_overlay_only
```

The image prompt asks for decorative background artwork and reserves a clean central headline area. Negative rules prohibit dense labels, small text, charts, random numbers, extra logos, seals, watermarks, and politician faces.

The generated background is **not** trusted to carry exact factual text. Instead, the run creates a deterministic render spec and uses the established HTML/Playwright renderer to overlay the exact constituency title during review.

This is a materially different risk model from the member-profile image edit, where exact text is part of the generated edited image.

### Constituency input and current legacy dependency

`instagram_option5_prepare_constituency_cover_test.py` currently reads the optional constituency reference-image index from:

```text
processed/constituencies/constituency_images.csv
```

That is a retained legacy-style path rather than the Unified Oireachtas compatibility namespace.

If a matching image is available, its URL is included as an inspiration/reference cue in the generated prompt. The prompt instructs the model to use it loosely rather than reproduce it exactly.

### Run layout

Current runs are written beneath:

```text
generated_visual_tests/option5_constituency_cover/<constituency-slug>__<UTC timestamp>/
```

with:

```text
inputs/
  source_snapshot.json
  base_render_spec.yml
jobs/
  generation_jobs.jsonl
  generation_jobs.pretty.json
images/
  <record>.png
metadata/
  <record>.json
  generated_manifest.jsonl
  generated_manifest.csv
render_specs/
  <record>.yml
rendered_posts/
  <record>/...
review/
  review_sheet.csv
```

### Job generation

The preparer records:

- constituency name/slug;
- optional reference-image URL;
- exact visible truth text;
- source dataset key used;
- risk notes;
- prompt text;
- 12-character SHA-256 prompt hash;
- style direction;
- variant index;
- output image filename.

With the current default `style_mode=both` and `variant_count=1`, the workflow prepares two image-generation jobs: one for each style direction.

Therefore OpenAI image-generation cost scales with `variant_count × number_of_selected_styles`.

### Image generation and deterministic overlay

`instagram_option5_generate_images.py` uses `OpenAI().images.generate()` for each job. Existing images can be reused unless `--overwrite` is supplied.

It writes image response metadata and builds a per-image render spec whose `generated_background_image_path` points at the local generated image.

The workflow then calls `instagram_render_post.py` for each generated spec, so the constituency title/footer are rendered through the deterministic renderer rather than entrusted to the generated background.

## Human review artifacts

The constituency review sheet contains blank fields for manual completion:

- `brand_consistency`;
- `factual_correctness_visible_text`;
- `text_legibility`;
- `repeatability_note`;
- `better_than_deterministic_template`;
- `approved`;
- `review_notes`.

`process/instagram_option5_build_review_sheet.py` does not score or approve these fields automatically.

The member-profile test has machine validation for v1 but still requires human review of the final v2/latest image.

Neither Option 5 path has a publishing step.

## External processing and security boundary

Verified secrets consumed by these workflows are:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`;
- `OPENAI_API_KEY`.

Do not document secret values.

For the member-profile path, external OpenAI processing receives image content derived from:

- the checked-in master template;
- the selected member's downloaded portrait;
- the generated first-pass image during validation and second-pass correction;
- exact visible member/metric values embedded in prompts.

For the constituency path, OpenAI receives generated prompt text and may receive a public/reference constituency-image URL only as prompt text; current generation code uses `images.generate()` rather than uploading the reference image bytes as an image input.

The source repository proves these application-level data flows. It does not establish OpenAI account-level retention/configuration settings or AWS IAM policy details.

## S3 side effects

The Option 5 generated visual outputs themselves are uploaded as GitHub Actions artifacts, not written to S3 by the Option 5 rendering scripts.

However the member-profile workflow has upstream S3 side effects:

- the generic metrics builder writes `processed/members/member_profile_metrics_2025.csv` and Parquet when no candidate batch is active;
- the still-invoked legacy vote extractor writes legacy vote/division CSV and Parquet objects under `processed/votes/`.

Those writes occur before the OpenAI edit step.

The constituency workflow reads S3 political/reference data through the existing loader but does not write its generated visual bundle to S3 in the inspected Option 5 workflow.

## Observed runtime evidence

### Constituency-cover path

Workflow ID `266733276` has one observed manual run:

- run `24966222811`, 2026-04-26: **success**.

Observed successful steps included preparation, image generation, review-sheet refresh, deterministic cover-overlay rendering, and artifact upload.

### Member-profile path

Workflow ID `266755734` has three observed manual runs:

- `24969650417`, 2026-04-26: **failure** at the member-profile AI-edit step after vote extraction and metrics build succeeded;
- `24970078480`, 2026-04-26: **success**;
- `24970547529`, 2026-04-27: **success**, including vote extraction, metrics build, AI edit, and artifact upload.

The exact root cause of the first failed AI-edit run was not established in this documentation audit and is not inferred here.

These runs executed historical commit SHAs from April 2026. They are observed runtime evidence for those revisions, not proof that current `main` has been re-executed since the later Oireachtas/metrics refactor.

## Workflow-registry caveat

GitHub's workflow registry currently lists several names containing **Instagram Content Factory**. A direct lookup of `.github/workflows/instagram_factory_validate.yml` on current `main` returned `404 File not found`.

Therefore those workflow-registry records are not treated here as current checked-in implementation. They may be deleted/orphaned historical workflow metadata. Target 18 is documented from files that currently exist on `main`.

## Failure modes

### Member-profile path

Verified or directly implied by current code:

- no candidate member with a usable photo URL;
- missing/unreadable metrics CSV;
- missing checked-in template file;
- member photo HTTP/download failure;
- unsupported or unreadable image format;
- OpenAI image-edit API failure;
- first-pass response missing an image payload;
- structured validation response cannot be parsed as expected JSON;
- validation API failure;
- second-pass image-edit failure or missing image payload;
- artifact upload fails because output is absent.

A successful v1 validation call does not guarantee v2 correctness.

### Constituency path

Verified/directly implied failure areas include:

- invalid workflow inputs/spec;
- inability to load required constituency-data/reference sources;
- OpenAI image-generation failure or missing image payload;
- malformed generated manifest/render spec;
- deterministic Playwright render failure;
- artifact upload failure.

Review fields remaining blank is not a workflow failure; it means human review has not yet been completed.

## Safe operating procedure

### Member-profile test

1. Confirm the metrics source and target year are the intended ones before running.
2. Use the manual **Generate Instagram Option 5 Member Profile AI Edit Test (Manual)** workflow.
3. Keep the default model/spec unless deliberately evaluating another supported configuration.
4. After the run, inspect `source_values.json` before judging the image.
5. Compare the checked-in template, selected portrait, v1, validation report, and v2.
6. Verify every visible name/party/constituency/issue/percentage/rank against source truth.
7. Treat v2/latest as unapproved until human review is complete.
8. Do not infer publication readiness from visual plausibility or machine validation scores.

### Constituency-cover test

1. Choose the constituency and keep variant count small when experimenting because each generated job is an external model call.
2. Run the manual **Generate Instagram Option 5 Constituency Cover AI Test (Manual)** workflow.
3. Inspect `source_snapshot.json` and generated prompt jobs.
4. Review generated backgrounds separately from rendered deterministic overlays.
5. Score the review sheet manually, including brand consistency, text correctness, legibility, repeatability, and whether the result actually improves on deterministic templating.
6. Do not treat an empty or positive-looking review sheet as automated approval.
7. There is no publish action in the workflow.

## Known limitations

- Both workflows are explicitly manual experiments, not a production Instagram publication pipeline.
- Member-profile selection is one member per run and is currently tied to 2025 metric field names.
- The member-profile workflow always pays for/runs a second image edit even if first-pass validation says another pass is unnecessary.
- There is no final automated machine validation of the v2 member-profile output.
- The member-profile workflow still invokes a legacy vote extractor that no longer feeds the default generic metrics builder.
- The constituency experiment still reads a legacy constituency-image index path.
- The constituency experiment isolates exact title text from image generation, but the generated decorative layer still requires visual/brand review.
- The member-profile experiment asks the image model to render exact visible text, which remains higher risk for textual fidelity than deterministic overlay rendering.
- Current successful runtime observations are from April 2026 revisions, before later source refactors.
- Current live OpenAI account configuration, model availability, rate limits, retention settings, and actual pricing are outside repository evidence.
- GitHub workflow-registry entries without corresponding current files are not reliable implementation evidence.

## Next safe development action

Document the Member Profile Metrics Builder as the authoritative current upstream metric component. That page should define the generic year-aware inputs, metric formulas, candidate-batch behavior, legacy 2025 wrapper, output schema, workflows, consumers, and the exact relationship to both deterministic and AI member-profile rendering.

Do not redesign or remove the redundant legacy vote-extraction step as part of documentation; that would be a separate implementation decision.

## Related documents

- [Instagram and constituency campaign rendering system](/projects/systems/instagram-constituency-campaign-rendering/)
- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)
- [eirepolitic-data-pipeline](/projects/repositories/eirepolitic-data-pipeline/)
- [Irish Politics Analytics](/projects/systems/irish-politics-analytics/)

## Verification record

- Last verified: `2026-08-07`
- Verified implementation/configuration: `.github/workflows/instagram_option5_member_profile_ai.yml`; `.github/workflows/instagram_option5_constituency_cover_ai.yml`; `process/render_member_profile_ai_edit.py`; `instagram/specs/member_profile_ai_test.yml`; current `instagram/reference/` tree; `instagram/specs/constituency_cover_ai_test.yml`; `process/instagram_option5_prepare_constituency_cover_test.py`; `process/instagram_option5_generate_images.py`; `process/instagram_option5_build_review_sheet.py`; `process/build_member_profile_metrics_2025.py`; `process/build_member_profile_metrics.py`; `process/build_dail_votes_member_records.py`; current workflow registry/file-presence checks.
- Observed runtime evidence: constituency run `24966222811`; member-profile runs `24969650417`, `24970078480`, and `24970547529` plus job-step conclusions.
- Historical/supporting notes consulted: `instagram/OPTION5_MEMBER_PROFILE_AI_EDIT.md`, `instagram/OPTION5_LLM_IMAGE_TEST.md`.
- Verification scope: current Option 5 workflow boundaries, data lineage, model calls, prompts/source-truth controls, machine/human review, artifacts, S3 side effects, security boundary, observed execution, implementation drift, failure modes, and limitations.
