---
title: Legacy debate and member enrichment lineage
summary: Cross-cutting status matrix for retained debate/speech classification and member-enrichment producers that still feed newer Unified Oireachtas enrichment and compatibility layers.
section: notes
doc_type: reference
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: eirepolitic-data-pipeline
technologies:
  - Python
  - GitHub Actions
  - Amazon S3
  - OpenAI API
order: 45
permalink: /projects/notes/legacy-debate-member-enrichment-lineage/
related:
  - /projects/pipelines/constituency_images_indexer/
  - /projects/pipelines/debate_issue_classifier/
  - /projects/pipelines/member_images_pipeline/
  - /projects/pipelines/member_summaries_table/
  - /projects/systems/unified-oireachtas-data-platform/
---

# Legacy debate and member enrichment lineage

## Purpose

This page answers a narrow P3 question: **which retained debate/speech classification and member-enrichment scripts in `eirepolitic-data-pipeline` are historical-only, which still produce data needed by newer code, and which newer files are adapters rather than true replacements?**

It is a lineage/status matrix, not another operating runbook. Detailed behavior belongs on the component pages linked below.

## Executive classification

Current source shows a transitional architecture rather than a clean legacy cutover.

Four newer Unified Oireachtas enrichment modules exist:

```text
extract/oireachtas/enrichment_constituency_images.py
extract/oireachtas/enrichment_member_photo_urls.py
extract/oireachtas/enrichment_member_summaries.py
extract/oireachtas/enrichment_speech_issue_labels.py
```

All four are **adapter/review/compatibility layers** over retained legacy outputs. None replaces its upstream discovery/generation/classification function.

The resulting pattern is:

```text
retained legacy producer
        ↓
legacy S3 output
        ↓
Unified Oireachtas enrichment trial
        ↓
Unified compatibility product
        ↓
current contracts / metrics / Instagram consumers
```

Therefore file presence should not be interpreted as duplicate implementations where one can simply be deleted. Several legacy outputs remain explicit checked-in dependencies.

## Lineage matrix

| Domain | Retained producer | Legacy source/output | Newer Oireachtas layer | Current status |
| --- | --- | --- | --- | --- |
| Constituency images | `process/constituency_images_indexer.py` | image objects under `processed/constituencies/images/` → `processed/constituencies/constituency_images.csv` | `enrichment_constituency_images.py` | legacy producer still required for current checked-in source lineage; newer layer does not discover/create images |
| Member photos | `process/members_photo_urls.py` | raw member roster/profile pages → nested `processed/members/member_photos/members_photo_urls.csv`, with older root-level fallback | `enrichment_member_photo_urls.py` | legacy scraper remains source producer; newer layer does not scrape pages |
| Member summaries | `process/members_background_summarizer.py` | raw member roster → `processed/members/members_summaries.csv` | `enrichment_member_summaries.py` | retained OpenAI generator remains summary producer; newer layer does not call OpenAI |
| Speech issue labels | `process/speech_issue_classifier.py` | `raw/debates/debate_speeches_extracted.csv` → `processed/debates/debate_speeches_classified.csv` | `enrichment_speech_issue_labels.py` | retained OpenAI classifier remains label producer; newer layer imports/validates existing labels |

None of these four lineages has source evidence establishing full producer retirement.

## Constituency-image lineage

Detailed record: [Constituency Images Indexer](/projects/pipelines/constituency_images_indexer/).

Current relationship:

```text
S3 image objects
  ↓
process/constituency_images_indexer.py
  ↓
processed/constituencies/constituency_images.csv
  ↓
extract/oireachtas/enrichment_constituency_images.py
  ├─ richer trial/review table
  └─ processed/oireachtas_unified/compat/media/constituency_images_compat.csv
```

The newer module explicitly does not create/download/overwrite image objects. Removing the legacy index without another discovery source would break the checked-in enrichment source path.

## Member-photo lineage

Detailed record: [Member Images Pipeline](/projects/pipelines/member_images_pipeline/).

Current relationship:

```text
raw/members/oireachtas_members_34th_dail.csv
  ↓
public Oireachtas member profile HTML
  ↓
process/members_photo_urls.py
  ↓
processed/members/member_photos/members_photo_urls.csv
  ↓ fallback supported: processed/members/members_photo_urls.csv
  ↓
extract/oireachtas/enrichment_member_photo_urls.py
  ↓
processed/oireachtas_unified/compat/media/members_photo_urls_compat.csv
```

The retained scraper still owns webpage discovery. The newer Oireachtas layer records provenance/review metadata and builds the compatibility product but does not fetch new profile pages.

## Member-summary lineage

Detailed record: [Member Summaries Table](/projects/pipelines/member_summaries_table/).

Current relationship:

```text
raw/members/oireachtas_members_34th_dail.csv
  ↓
process/members_background_summarizer.py
  ↓ OpenAI Responses API + web search
processed/members/members_summaries.csv
  ├─ also shared by generic LLM enrichment tasks
  ↓
extract/oireachtas/enrichment_member_summaries.py
  ↓
processed/oireachtas_unified/compat/text/members_summaries_compat.csv
```

The newer Oireachtas module explicitly does not call OpenAI. It cannot reproduce exact original model provenance from the legacy table and therefore records legacy/unknown provenance fields.

The underlying legacy table now has a second role: current generic LLM tasks also read/write it. That shared mutable-table behavior is documented under the Reusable LLM Task Runner Framework.

## Speech-classification lineage

Detailed record: [Debate Issue Classifier](/projects/pipelines/debate_issue_classifier/).

Current relationship:

```text
legacy monthly debate XML extraction/parser
  ↓
raw/debates/debate_speeches_extracted.csv
  ↓
process/speech_issue_classifier.py
  ↓ OpenAI Responses API
processed/debates/debate_speeches_classified.csv
  ↓
extract/oireachtas/enrichment_speech_issue_labels.py
  ↓
processed/oireachtas_unified/compat/debates/debate_speeches_classified_compat.csv
```

The newer enrichment module explicitly does not classify speech text. It checks/normalizes the existing fixed issue labels and creates review/compatibility outputs.

## Older scheduled extraction coexistence

`.github/workflows/monthly_extract.yml` remains scheduled in current source at:

```text
15 9 1 * *
```

and still invokes the older debate XML/member extraction chain.

That schedule is current checked-in configuration, but it must not be interpreted as making the old extractor the canonical Oireachtas architecture. Canonical Oireachtas products now come from the separately documented Unified Oireachtas platform.

The important P3 finding is narrower: some retained enrichment/classification producers still depend on legacy-shaped raw/processed inputs even after canonical ingestion moved elsewhere.

## Current consumers of the compatibility layer

The newer adapter outputs are not merely review experiments with no downstream relevance.

Current checked-in contracts include:

- `member_photo_urls`;
- `member_summaries`;
- `constituency_images`;
- `debate_issue_labels`.

Candidate validation stages those compatibility datasets into the Unified Oireachtas candidate and validates shape, primary-key integrity, minimum rows, and freshness.

Current Member Profile Metrics Builder defaults to the photo and debate-issue compatibility datasets. Instagram member-profile workflows then consume those derived member metrics/photo fields.

This establishes a live dependency path from retained enrichment producers through compatibility adapters into newer consumers, even though the producers themselves are not canonical Oireachtas tables.

## Status rules for maintainers

Use these classifications when reading current source:

### Retained dependency producer

Use this label when newer checked-in code still reads the older component's output directly.

Current examples:

- constituency image index;
- member photo URL table;
- member summary table;
- classified debate speech table.

### Adapter/compatibility successor

Use this label for the four `extract/oireachtas/enrichment_*` modules. They improve review/provenance/contract integration but do not perform the original producer's external discovery/generation/classification job.

### Canonical replacement

Do **not** use this label unless current source proves the upstream function has moved to canonical Oireachtas tables/workflows and the legacy producer/output is no longer required.

That condition is not currently established for these four lineages.

## What can safely be considered superseded

Some surrounding roles have moved:

- canonical Oireachtas member/debate ingestion belongs to the Unified Oireachtas platform, not the older raw extraction architecture;
- downstream consumers should prefer the Unified compatibility products where they are already configured to do so;
- archive pages should no longer be used as current runbooks where current system/reference pages exist.

Those changes do **not** mean the legacy enrichment producers are removable today.

## Migration implications

A future full cutover would require replacing each upstream function explicitly, for example:

- source constituency-image discovery/indexing from a canonical/current media source;
- member-photo discovery from a stable API/media contract or new canonical process;
- member-summary generation with an explicitly versioned current generation product;
- speech issue classification directly from canonical `silver_speeches` or another current speech product.

Only after downstream code no longer reads the legacy outputs could those producer scripts be classified as fully retired.

That would be an implementation/architecture change, not a documentation cleanup.

## Security and cost boundaries

The legacy producers have different external boundaries:

- constituency image indexer: S3 only;
- member photo scraper: S3 plus public Oireachtas HTTP pages;
- member background summarizer: S3 plus OpenAI Responses/web search;
- speech issue classifier: S3 plus OpenAI Responses API.

The newer enrichment modules do not add equivalent external discovery/model calls; they primarily read S3 legacy outputs and create new S3/review artifacts.

No credential values are documented here.

## Known limitations

- The architecture remains transitional: canonical Oireachtas ingestion and legacy enrichment producers coexist.
- Legacy producer outputs are direct mutable S3 paths rather than immutable canonical table products.
- Newer adapter provenance can only be as precise as the legacy source allows; member summaries and speech labels cannot reconstruct all original model metadata.
- Workflow presence/scheduling demonstrates executable configuration, not a long-term product-ownership decision.
- This page does not authorize deleting, migrating, or redesigning any legacy producer.

## Related documents

- [Constituency Images Indexer](/projects/pipelines/constituency_images_indexer/)
- [Debate Issue Classifier](/projects/pipelines/debate_issue_classifier/)
- [Member Images Pipeline](/projects/pipelines/member_images_pipeline/)
- [Member Summaries Table](/projects/pipelines/member_summaries_table/)
- [Unified Oireachtas Data Platform](/projects/systems/unified-oireachtas-data-platform/)
- [Oireachtas write policies and downstream contracts](/projects/notes/oireachtas-write-policies-downstream-contracts/)
- [Member Profile Metrics Builder](/projects/systems/member-profile-metrics-builder/)
- [Reusable LLM Task Runner Framework](/projects/systems/reusable-llm-task-runner-framework/)

## Verification record

- Last verified: `2026-08-07`
- Current canonical/enrichment package verified against the complete `extract/oireachtas/` tree.
- Retained producer inventory verified against the complete current `process/` tree.
- Detailed implementation/source relationships verified during P3 targets 47, 48, 50 and 51.
- Current classification: transitional legacy-producer → Unified enrichment/compatibility architecture; no full retirement established for the four producer lineages.
