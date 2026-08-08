---
title: AutoDoc template and Markdown rendering
summary: Current verified AutoDoc rendering stage that combines base/type template structure with extracted section facts, calls OpenAI only for sections with facts, enforces front matter, and writes generated Markdown.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 37
permalink: /projects/systems/autodoc-template-markdown-rendering/
tags:
  - autodoc
  - templates
  - markdown
  - openai
  - pipeline
---

# AutoDoc template and Markdown rendering

## Summary

`process/render_sections.py` converts AutoDoc's persisted section-fact CSV into generated Markdown. It merges the common template with an optional type template, replaces only four deterministic top-level placeholders, splits the result into H2 sections, and uses `gpt-4.1-mini` to render each section that has non-empty extracted facts.

A section with no facts does not call OpenAI. It receives the fixed marker:

```text
_TBD (no extracted facts provided for this section)._
```

The renderer then combines the template preamble and rendered sections, ensures YAML front matter with the authoritative title and `layout: default`, and overwrites:

```text
docs/<project>/<type>/<doc_key>.md
```

## Source of Truth

```text
process/render_sections.py
.github/workflows/render_docs.yml
.github/workflows/autodoc_pipeline.yml
templates/base.md
templates/types/generic.md
templates/types/pipeline.md
templates/types/dataset.md
templates/types/dashboard.md
templates/types/investigation.md
```

Current implementation SHA:

```text
process/render_sections.py
ba99bedecca8a1482e7e49cd3863333fff308f67
```

Current executable source outranks older generated Markdown when formatting/layout/model descriptions differ.

## Entry Point

```text
PROJECT=<project> DOC_KEY=<doc_key> python process/render_sections.py
```

The script accesses required environment variables through:

```python
os.environ["PROJECT"]
os.environ["DOC_KEY"]
```

so a missing variable raises immediately.

The OpenAI client uses `OPENAI_API_KEY` through the standard environment configuration.

## Stage Dependencies

Rendering requires:

```text
doc_configs/<project>/<doc_key>.json
doc_configs/<project>/<doc_key>.enriched.json
doc_configs/<project>/summaries/<doc_key>.csv
templates/base.md
```

The base config provides `type` through direct indexing:

```text
cfg["type"]
```

so a missing `type` is fatal.

The enriched config is explicitly loaded even though rendering uses it only as the preferred title source. This enforces the pipeline stage dependency.

The summary CSV is required and supplies the facts used by section rendering.

## Template System

### Base template

`templates/base.md` supplies:

- H1 title/preamble metadata;
- `Overview`;
- `Assets`;
- `Inputs and Outputs`;
- `How it works`;
- `How to run`;
- `Data quality and validation`;
- `Maintenance`.

### Type templates

Current type extensions are:

| Type file | Additional H2 sections |
| --- | --- |
| `generic.md` | none; comment only |
| `pipeline.md` | `Orchestration`, `Lineage` |
| `dataset.md` | `Schema`, `Refresh and SLAs` |
| `dashboard.md` | `Data sources`, `Refresh`, `Key pages and visuals`, `Business definitions` |
| `investigation.md` | `Question`, `Method`, `Findings`, `Repro steps` |

`merge_templates()` performs simple text concatenation. If `templates/types/<type>.md` does not exist, the renderer uses only `templates/base.md`.

## Placeholder Behavior

The current renderer is not a general Jinja template renderer.

`apply_top_placeholders()` performs literal string replacement for only:

```text
{{title}}
{{project}}
{{type}}
{{generated_at}}
```

Values come from the base config except `generated_at`, which is current UTC ISO time.

Other placeholder-looking text such as:

```text
{{purpose}}
{{assets_list}}
{{inputs}}
{{outputs}}
{{orchestration}}
```

is not directly replaced by deterministic code. It remains in each section's `template_section_text` and is supplied to the LLM as structural guidance.

This distinction is important: template section placeholders are prompt guidance, not independently evaluated variables.

## H2 Split and Preamble

`split_by_h2()` matches:

```regex
^## (.+)$
```

The text before the first H2 becomes `preamble`. Every H2 produces a `(title, body)` section in template order.

If no H2 is found, the function returns the entire template as preamble and an empty section list. Rendering itself does not explicitly reject that state, although normal upstream extraction would have failed on a no-H2 template.

## Summary CSV Consumption

`load_section_facts()` reads:

```text
doc_configs/<project>/summaries/<doc_key>.csv
```

through `csv.DictReader`.

For every row:

```text
section_title -> stripped title
extracted_facts -> stripped facts
```

Rows with blank section title are ignored.

Facts are stored in a dictionary keyed by exact section title. If duplicate titles occur in the CSV, a later row replaces the earlier value for that title.

The renderer does not validate that the CSV contains every template section or only valid template sections.

## Section Rendering

For each template section:

```text
facts = facts_by_title.get(title, "")
```

### No facts

When `facts_bullets.strip()` is empty, `render_section()` returns without an OpenAI request:

```markdown
## <section title>

_TBD (no extracted facts provided for this section)._
```

### Facts present

The current prompt includes:

- section title;
- the complete template body for that section;
- the extracted-facts text for that section;
- instructions to output only the completed Markdown section;
- instruction to start with the correct H2;
- instruction to use only provided facts and omit missing details rather than guess;
- instruction to keep the section clean and technical.

Unlike extraction, rendering does use the section-template body in the actual model input.

## OpenAI Configuration

Current Python constant:

```text
MODEL = "gpt-4.1-mini"
```

Current request:

```text
client.responses.create(
    model="gpt-4.1-mini",
    input=<section prompt>,
    temperature=0,
)
```

There is no renderer model environment override.

There is no explicit retry/backoff or inter-section throttle in `render_sections.py`. A non-recovered client/API exception propagates and fails the process.

The number of OpenAI calls is the number of template sections with non-empty facts, not necessarily the total number of sections.

## Heading Enforcement

The returned model text is stripped.

If it does not begin, after left whitespace removal, with:

```text
## <section title>
```

then the renderer prepends that heading.

The model output is otherwise not parsed into a stricter Markdown schema.

## Final Document Assembly

The final body is:

```text
[preamble if non-empty]

[rendered H2 section]

[rendered H2 section]
...
```

The preamble is deterministic template text after the four top-placeholder substitutions. It is not sent through an LLM by this stage.

## Front Matter Enforcement

`ensure_front_matter()` ensures the final document starts with YAML front matter containing:

```yaml
---
title: "<title>"
layout: default
---
```

Title preference is:

```text
enriched.title
-> base cfg.title
-> doc_key
```

Blank final title becomes `Untitled`.

The title is YAML double-quoted with escaping for backslashes, quotes, and newlines.

If front matter already exists at the top, the function updates/inserts `title` and `layout` while preserving other lines/keys. It also strips a leading UTF-8 BOM before front-matter processing.

### Historical artifact drift

Some persisted historical AutoDoc-generated Markdown can contain different front-matter values such as `layout: doc`. Current renderer source explicitly calls:

```text
ensure_front_matter(..., layout="default")
```

so older artifact metadata must not override current implementation documentation.

## Output Contract

`write_markdown()` writes:

```text
docs/<project>/<type>/<doc_key>.md
```

It creates parent directories when necessary and writes UTF-8 text with exactly one terminating newline after `rstrip()` normalization.

The output path is overwritten by a successful render.

This is the **generated/raw** artifact path. Reviewed Markdown is a separate lifecycle state under the review stage.

## Data Sent to OpenAI

Rendering does **not** serialize or send the enriched JSON directly to the model.

Per rendered section, model input consists of:

```text
section title
section template body
extracted_facts text
fixed rendering instructions
```

The enriched config is loaded locally and used as the preferred title source.

This gives rendering a narrower model-context boundary than extraction, although the facts text can itself contain information derived from enriched assets.

## Automatic Workflow Integration

The automatic pipeline calls:

```text
PROJECT=<project> DOC_KEY=<doc_key> python process/render_sections.py
```

after extraction.

A render failure stops the automatic processing shell because it runs with `set -euo pipefail`.

When processing later reaches its generated-output commit step, `docs/**` is included among staged outputs.

The automatic pipeline ends at rendering; it does not automatically run review.

## Manual Render Workflow

Workflow:

```text
.github/workflows/render_docs.yml
Render Docs from Section Summaries
```

Trigger:

```text
workflow_dispatch
```

Required inputs:

```text
project
doc_key
```

Permissions:

```text
contents: write
```

Concurrency:

```text
render-docs
cancel-in-progress: false
```

Runtime:

```text
ubuntu-latest
Python 3.11
pip install openai
```

The workflow exports:

```text
OPENAI_API_KEY
PROJECT
DOC_KEY
```

After rendering, the manual workflow runs:

```text
git add docs/
```

not a single exact output path. Therefore any other pre-existing uncommitted changes under `docs/` in that runner worktree would also be staged. Under normal clean Actions checkout the intended change is the generated document.

If no staged change exists, the workflow exits successfully without a commit. Otherwise it commits and pushes directly to `autodoc`.

## Failure Modes and Recovery

### Config missing or invalid

Fix the base config. Rendering depends on valid `type` and project/doc identity.

### Enriched config missing

Run/fix enrichment first. Rendering intentionally enforces this dependency even though enriched content is not directly sent to the model.

### Summary CSV missing

Run/fix extraction. Do not create arbitrary Markdown to bypass the persisted facts contract.

### Template file missing

A missing `templates/base.md` is fatal through file reading. Missing type template is not fatal; base-only behavior is current design.

### Section facts missing/blank

The section receives the fixed `_TBD` marker and no model call is made. This does not fail the render.

### OpenAI error

There is no renderer-local retry loop. The process fails immediately on an exception. Preserve upstream CSV/enriched artifacts, resolve the API/input problem, then rerun render only.

### Model output omits expected H2

The renderer prepends the expected heading. It does not otherwise rewrite/validate the returned section structure.

### Existing generated Markdown

A successful render overwrites the generated path. Reviewed output remains separate and is not automatically regenerated by rendering.

## Trust, Security, and Cost Boundaries

- `OPENAI_API_KEY` is a secret name only; never expose its value.
- Facts previously extracted from repository source are sent to OpenAI again during rendering for non-empty sections.
- Template body text is also sent.
- Empty-fact sections have no model cost at rendering time.
- Changing model, prompt, section count, or retry behavior can affect cost/quality and requires explicit approval where it changes operation.
- Generated Markdown is durable repository content and can later become reviewed/public content; do not treat LLM output as authoritative implementation source without source verification.

## Known Limitations

- Only four top-level placeholders are deterministically replaced; section placeholders are LLM prompt guidance.
- No retry/backoff exists in renderer code.
- Output Markdown beyond H2-prefix enforcement is not structurally validated.
- Missing facts produce `_TBD` rather than failing the stage.
- Duplicate CSV section titles use the last row.
- Standalone rendering does not itself fail when a merged template has no H2 sections.
- Historical generated artifacts can reflect older renderer behavior/front matter.

## Next Safe Development Action

Publish this rendering component through validation, merge, and matching Pages success. Then document the separate LLM review/concision stage on a fresh branch from current `main`.

Do not change models, prompt/template semantics, front-matter policy, TBD behavior, or workflow staging behavior without explicit architecture/cost approval.

## Related Documents

- [AutoDoc section-fact extraction](/projects/systems/autodoc-section-fact-extraction/)
- [AutoDoc asset enrichment](/projects/systems/autodoc-asset-enrichment/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc/main` `process/render_sections.py` SHA `ba99bedecca8a1482e7e49cd3863333fff308f67`; current `render_docs.yml`, `autodoc_pipeline.yml`, all current base/type templates, and a persisted historical generated artifact for drift comparison.
- Verified by: High Director
- Verification scope: dependencies, template merge/types, deterministic placeholders, H2 split/preamble, CSV consumption, actual render prompt/model, no-facts behavior, heading/front-matter enforcement, output path/write semantics, workflow behavior, trust/cost boundaries, and historical drift.
- Not verified: current OpenAI service/account limits or runtime output quality for a new render.
