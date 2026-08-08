---
title: AutoDoc LLM review and concision
summary: Current verified AutoDoc review stage that sends the complete generated Markdown document to OpenAI for a concision pass and writes a separate reviewed artifact.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 38
permalink: /projects/systems/autodoc-review-concision/
tags:
  - autodoc
  - review
  - openai
  - markdown
  - pipeline
---

# AutoDoc LLM review and concision

## Summary

`process/review_doc.py` creates AutoDoc's separate reviewed-artifact state. It reads the full generated Markdown document, sends that entire document to OpenAI with instructions to make it more concise without changing formatting/headings/section order, and writes the model's returned text directly to:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

The current standard workflow explicitly sets `AUTODOC_MODEL=gpt-4.1`. Review is not part of the automatic enrich/extract/render pipeline; it is a separate `workflow_dispatch` stage and is also dispatched by the current Appsmith `DocsViewer` page.

“Reviewed” in this system means **LLM review/concision output**. The stage does not implement human approval, factual source verification, Markdown validation, documentation-site validation, or publication approval.

## Source of Truth

```text
process/review_doc.py
.github/workflows/review_doc.yml
_docs/systems/autodoc-appsmith-intake.md
.github/workflows/publish_to_website.yml
```

Current Python implementation SHA:

```text
1a422baef5c889a1a755e003642128359e7142f1
```

Current workflow SHA:

```text
ee53dbb87254f9bc3f446614792a5233f1bc4e78
```

## Entry Point and Environment

The script executes at module top level:

```text
python process/review_doc.py
```

Environment variables:

| Name | Behavior |
| --- | --- |
| `PROJECT` | Used directly in generated/reviewed paths |
| `TYPE` | Used directly in generated/reviewed paths |
| `DOC_KEY` | Used directly in generated/reviewed paths |
| `OVERWRITE` | Defaults to `true`; case-insensitive string comparison with `true` |
| `AUTODOC_MODEL` | Defaults to `gpt-4.1` |
| `OPENAI_API_KEY` | Consumed by the OpenAI client |

The Python script does not separately validate that `PROJECT`, `TYPE`, or `DOC_KEY` are non-empty before constructing paths.

The standard review workflow supplies all three required identity inputs and sets `AUTODOC_MODEL` explicitly to `gpt-4.1`.

## Generated Source Path

Source:

```text
docs/<project>/<type>/<doc_key>.md
```

The script reads the entire source document as UTF-8.

If the source path is missing and review is not skipped through the existing-target/overwrite rule, `read_text()` raises and the review step fails.

## Reviewed Target Path

Target directory:

```text
docs/<project>/<type>/reviewed/
```

Target file:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

The target directory is created before the overwrite check/source read. An empty directory itself is not durable in Git unless a file such as `.gitkeep` is present.

## Overwrite Behavior

Current Python logic:

```text
if target exists and overwrite is false:
    print("Skipping — reviewed file exists")
    exit(0)
```

This check occurs before the generated source is read.

Therefore an existing reviewed artifact plus `OVERWRITE=false` causes a successful skip even if the raw/generated source is currently missing or different.

The current workflow input defaults to:

```text
overwrite = "true"
```

and the verified Appsmith `DocsViewer` review dispatch also sends:

```text
overwrite: "true"
```

so the normal current UI path requests regeneration/replacement of the reviewed file.

## Review Prompt Contract

The entire generated document is interpolated into one prompt.

The prompt identifies the task as reviewing a technical documentation Markdown file and attempting to make it more concise.

Current rules instruct the model to:

1. not change formatting;
2. not change headings;
3. not reorder sections;
4. edit only text inside sections;
5. keep information only in its proper section and avoid restating it elsewhere;
6. return only valid Markdown.

The complete generated Markdown follows those rules in the same request.

## OpenAI Configuration

Python model selection:

```text
MODEL = os.getenv("AUTODOC_MODEL", "gpt-4.1")
```

Standard workflow environment:

```text
AUTODOC_MODEL = gpt-4.1
```

Current request:

```text
client.responses.create(
    model=MODEL,
    input=PROMPT,
    max_output_tokens=12000,
)
```

No `temperature` value is explicitly supplied by this stage.

There is no review-stage retry/backoff loop in `review_doc.py`.

The model response is read from:

```text
resp.output_text
```

and passed directly to `Path.write_text()`.

## Output Validation Boundary

Current code does not programmatically verify that the model actually preserved:

- YAML front matter;
- headings;
- section order;
- Markdown formatting;
- all facts;
- absence of new facts;
- documentation-site metadata;
- links;
- factual correctness.

The requirements exist only in the prompt.

No post-review documentation validator is run by `review_doc.py` or `review_doc.yml`.

If `resp.output_text` is not a usable string, the direct write can fail; there is no fallback to the original generated content.

## Trust and Semantic Boundary

The review prompt asks for concision and deduplication, not source re-verification.

Therefore:

```text
generated Markdown
  -> LLM concision/reorganization within stated constraints
  -> reviewed Markdown
```

must not be interpreted as:

```text
unverified document
  -> factual/human/security approval
```

The reviewed artifact remains derived LLM output.

## Data Sent to OpenAI

Unlike rendering's per-section requests, review sends the **entire generated Markdown document in one request**.

Anything present in generated Markdown can therefore cross the OpenAI boundary again at review time.

The review stage does not read the enriched JSON or summary CSV directly.

## Standard Review Workflow

Workflow:

```text
.github/workflows/review_doc.yml
Review Documentation
```

Trigger:

```text
workflow_dispatch
```

Inputs:

```text
project   required
type      required
doc_key   required
overwrite required, default "true"
```

Permissions:

```text
contents: write
```

Runtime:

```text
ubuntu-latest
Python 3.11
pip install openai requests
```

`requests` is installed by the workflow although current `review_doc.py` does not import it.

Secret name:

```text
OPENAI_API_KEY
```

The workflow has no explicit concurrency group.

## Workflow Commit Behavior

After the Python stage, the workflow runs:

```text
git add docs/
git commit ... || echo "No changes"
git push
```

This stages the entire `docs/` tree rather than the exact reviewed path. Under a normal clean Actions checkout the intended change is the reviewed artifact, but any other worktree changes under `docs/` would also be staged.

### Commit-message variable scope

The commit command is written as:

```text
git commit -m "Add reviewed doc: $DOC_KEY"
```

but `DOC_KEY` is defined only in the previous `Run review pipeline` step's `env:` block. GitHub Actions step-scoped environment variables do not automatically persist into later steps.

Therefore current workflow source does not establish a populated `$DOC_KEY` in the commit step; under normal step scoping the commit message suffix is empty unless another environment source provides it.

This is a source-verified workflow defect/risk. Documentation does not change it.

If the commit produces no changes, the `git commit` failure is suppressed by `|| echo "No changes"`; `git push` is still attempted afterward.

## Appsmith Review Dispatch

The current `DocsViewer` page dispatches:

```text
/repos/eirepolitic/autodoc/actions/workflows/review_doc.yml/dispatches
```

with:

```text
ref: main
project: selected project
type: selected index-entry type
doc_key: selected doc key
overwrite: "true"
```

This is the normal current UI boundary from raw document viewing/editing into review generation.

## Reviewed Artifact and Publication

Current website publication requires:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

and copies that file into `eirepolitic.github.io` when publication is dispatched.

Publication does not independently prove that the review output preserves source facts or passes the newer documentation validator/governance path.

The existence of a reviewed file is therefore a lifecycle/path condition, not an approval certificate.

## Persisted Examples

Current `autodoc` repository contains reviewed examples including:

```text
docs/autodoc/generic/reviewed/autodoc_app.md
docs/autodoc/pipeline/reviewed/autodoc_creation_pipeline.md
```

These artifacts demonstrate the lifecycle/path convention but can reflect the code/model state at the time they were created. Current workflow/Python source remains implementation authority.

## Failure Modes and Recovery

### Generated source missing

With overwrite enabled or no existing reviewed target, the script fails reading the source. Restore/regenerate the raw document before review.

### Reviewed target exists and overwrite=false

The script exits successfully without reading source or calling OpenAI. Confirm this skip is intentional before treating the target as current.

### OpenAI/API failure

There is no local retry loop. The step fails; preserve the existing generated/reviewed artifacts, resolve the API/account/input issue, then rerun review only.

### Model violates prompt constraints

Current code does not detect the violation. Inspect the reviewed artifact before publication where correctness matters. Do not assume “reviewed” means structurally or factually validated.

### No content change

The workflow's commit command can produce no commit and prints `No changes`; it still runs `git push`.

### Commit/push failure

Inspect repository state and non-secret error output. Do not expose `OPENAI_API_KEY` or repository credentials while troubleshooting.

## Security, Privacy, and Cost Boundaries

- The complete generated document is sent to OpenAI in one request.
- Maximum requested model output is `12000` tokens.
- The reviewed result is durable repository content and may later be published publicly.
- Do not include secrets/private data in generated documentation merely because the review stage is expected to edit it.
- Changing the model, prompt, maximum output, or retry strategy can affect cost/quality and requires explicit approval where operational behavior changes.

## Known Limitations

- No factual or structural post-review validator.
- No retry/backoff.
- No concurrency group in the review workflow.
- Full document is sent in one request.
- `reviewed` is an artifact-state name, not human approval.
- `git add docs/` is broader than the exact target path.
- The workflow commit step references `$DOC_KEY` outside the step where it is currently defined.
- Existing reviewed target plus overwrite=false can skip review without checking source freshness.

## Next Safe Development Action

Publish this P1 component through validation, merge, and matching Pages success. Then document the generated/reviewed artifact lifecycle and manual recovery workflows as P2 on a fresh branch from current `main`.

Do not change model, prompt, overwrite defaults, workflow scoping/concurrency, token limits, or approval semantics without explicit architecture/cost/security approval.

## Related Documents

- [AutoDoc template/Markdown rendering](/projects/systems/autodoc-template-markdown-rendering/)
- [AutoDoc publication boundary](/projects/systems/autodoc-publication-boundary/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc/main` `process/review_doc.py` SHA `1a422baef5c889a1a755e003642128359e7142f1`; current `review_doc.yml` SHA `ee53dbb87254f9bc3f446614792a5233f1bc4e78`; current Appsmith dispatch documentation; current publication workflow; current reviewed artifact tree.
- Verified by: High Director
- Verification scope: source/target paths, overwrite semantics, actual prompt/model/request, lack of validation/retry, whole-document OpenAI boundary, workflow inputs/permissions/commit behavior, Appsmith dispatch, publication relationship, failures, and limitations.
- Not verified: current OpenAI account limits, model-output quality, or human approval state of existing reviewed artifacts.
