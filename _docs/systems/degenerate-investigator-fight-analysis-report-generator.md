---
title: degenerate_investigator Fight-Analysis Report Generator
summary: Source-grounded documentation for generating UFC fight-analysis CSV, Parquet, and Markdown reports from scored matchups and optional recent-news enrichment, including deduplication, generated-text and deterministic fallbacks, S3 products, provenance limitations, failure modes, and rerun guidance.
section: systems
doc_type: system
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# degenerate_investigator Fight-Analysis Report Generator

## Purpose

`process/generate_event_report.py` converts scored matchup rows into a human-readable Markdown fight-analysis report plus tabular CSV/Parquet report products.

The stage consumes prediction probabilities and optional fighter recent-news context. It can use the OpenAI Responses API to generate structured analytical prose, with a deterministic `simple_fallback()` when generated output cannot be obtained or parsed.

The report-text fallback is separate from model/scoring fallback. It does not change how the underlying prediction probability was produced.

## Source paths

- implementation: `process/generate_event_report.py`;
- workflow: `.github/workflows/ufc_generate_report.yml`;
- upstream scoring: `process/score_target_event.py`;
- upstream news: `extract/fighter_recent_news.py`;
- shared S3 I/O: `common/io_helpers.py`.

Important functions:

- `parse_json()`;
- `simple_fallback()`;
- `load_news_summary()`;
- `deduplicate_matchups()`;
- `build_event_overview()`;
- `main()`.

## Inputs

Required:

- `PREDICTIONS_KEY` — S3 CSV key containing scored matchups.

Optional/defaulted:

- `NEWS_KEY` — default `raw/news/fighter_recent_news.csv`;
- `USE_OPENAI_REPORTS` — source default `true`;
- `OPENAI_API_KEY` — required only when generated report prose is enabled;
- `OPENAI_MODEL` — optional model override, source default `gpt-4.1-mini`;
- `S3_BUCKET` — default `degenerative-investigator`;
- `AWS_REGION` — default `us-east-2`.

The report workflow explicitly sets `USE_OPENAI_REPORTS=true` and supplies `OPENAI_API_KEY` through a GitHub secret.

## Workflow behavior

`.github/workflows/ufc_generate_report.yml`:

- trigger: `workflow_dispatch`;
- inputs: `predictions_key`, `news_key`;
- committed prediction default: `processed/ufc/ufc-327-prochazka-vs-ulberg_predictions.csv`;
- committed news default: `raw/news/fighter_recent_news.csv`;
- runner: `ubuntu-latest`;
- Python: 3.11;
- timeout: 120 minutes;
- repository permission: `contents: read`;
- command: `python process/generate_event_report.py`.

The prediction default is event-specific. Verify it for each target event.

## Prediction deduplication

`deduplicate_matchups()` is applied before report generation.

The function constructs a canonical matchup key from the two fighter names so reversed orientations group together. Within each canonical matchup it sorts by:

1. `scoring_method` preference, where `trained_model` is preferred over other methods;
2. higher probability-distance confidence;
3. original row order.

It then keeps one row per canonical matchup.

### Interpretation

This deduplication can hide upstream duplicated or mirrored scoring rows in the report. It should not be treated as proof that the scoring dataset itself was correct.

A trained-model row is deliberately preferred over a heuristic row when both exist for the same matchup.

## News loading

`load_news_summary()` attempts to read the configured news S3 CSV. Missing/unreadable news is tolerated and returns an empty lookup rather than failing the report stage.

The news lookup groups returned summaries/items by fighter name for narrative context.

A successful report run therefore does not prove that recent-news enrichment was present.

## Generated report text

When `USE_OPENAI_REPORTS` is enabled, the script sends structured fight context to the OpenAI Responses API and requests strict JSON for report fields.

The context includes prediction probabilities, winner/confidence, signal strings, market-comparison values when present, and fighter news summaries.

The current implementation uses `OPENAI_MODEL` with source default `gpt-4.1-mini`.

Generated prose is analytical narrative over already-computed scoring results. It does not retrain or rescore the matchup.

## JSON parsing

`parse_json()` extracts the substring from the first `{` to the last `}` and parses it with `json.loads()`.

If generated text is absent, malformed, or an API call raises, report construction falls back to `simple_fallback()` for that matchup.

Unlike fighter-news enrichment, this report stage does not perform a second JSON-repair model call.

## Deterministic `simple_fallback()`

`simple_fallback()` creates deterministic report prose from the existing prediction row and contextual fields.

This is a **text-generation fallback only**. It does not replace the prediction with a heuristic score, does not alter probabilities, and does not change the upstream `scoring_method`.

Do not describe `simple_fallback()` as a model fallback.

## Matchup output fields

The report-row DataFrame contains report-oriented fields including:

- `event_name`;
- `event_slug`;
- `fighter_1_name`;
- `fighter_2_name`;
- `predicted_winner`;
- `confidence_bucket`;
- `fighter_1_win_probability`;
- `fighter_2_win_probability`;
- market comparison values when present;
- `top_signals`;
- news context;
- generated/fallback analytical text fields.

### Critical provenance limitation

Although `scoring_method` is present in prediction input and is used by `deduplicate_matchups()` to prefer trained-model rows, the current report output does **not** retain `scoring_method` as a report column.

Therefore once a report row is written, a consumer cannot reliably determine from that report artifact alone whether its probability came from:

- a trained Random Forest;
- a trained single-class dummy-prior estimator;
- the explicit scoring heuristic fallback.

This is a material provenance loss. To establish scoring origin, inspect the upstream prediction artifact and model metrics/artifact lineage.

## Wording limitation

The report prose/headings use model-oriented wording such as “model lean” for the selected probability/winner context. Because report outputs do not retain `scoring_method`, that wording can also appear for rows whose upstream probability was heuristic.

Documentation and downstream presentation must not infer a trained model merely from report wording.

## `top_signals` limitation

The report includes upstream `top_signals`. As documented in target-event scoring, those strings are always based on fixed heuristic feature weights—even when the selected prediction row was `trained_model`.

They are not Random Forest local feature attribution.

## Market-comparison limitation

Upstream prediction fields named `fighter_*_model_market_delta` can contain a heuristic-minus-market delta when `scoring_method=heuristic`.

Because report output drops `scoring_method`, a report consumer cannot disambiguate that naming solely from the report artifact.

Market fields remain analytical comparison signals only and are not staking or wagering recommendations.

## Event overview

`build_event_overview()` constructs a short event-level overview from report/prediction context.

The report then renders:

- event heading/overview;
- one section per deduplicated matchup;
- probabilities/lean/confidence/context;
- signal/news/generated analytical text.

The repository's current published `reports/latest_fight_report.md` is an exported copy of one such S3 Markdown object, not the primary scoring source of truth.

## S3 products

For the selected event slug:

- `processed/reports/{event_slug}_fight_report.csv`;
- `processed/reports/parquets/{event_slug}_fight_report.parquet`;
- `processed/reports/{event_slug}_fight_report.md`.

These are fixed event-slug products and are overwritten by a rerun for the same slug.

## Empty-input behavior

The source expects prediction content sufficient to determine event identity and iterate matchups. An empty prediction DataFrame can fail before meaningful report output is produced, including through first-row/event-slug assumptions.

The script should not be treated as guaranteeing a valid “empty report” artifact.

## Normal operating sequence

1. Score and validate the intended event.
2. Inspect upstream prediction `scoring_method` before report generation.
3. Confirm the prediction key belongs to the intended event.
4. Optionally refresh fighter recent-news enrichment.
5. Dispatch `UFC Generate Event Report (Manual)` with the exact prediction/news keys.
6. Confirm the S3 CSV/Parquet/Markdown report objects were written.
7. When model provenance matters, retain/reference the prediction artifact because report rows do not preserve `scoring_method`.
8. Optionally run the separate S3-to-repository publication workflow.

## Validation checks

At minimum:

- report products are non-empty;
- event slug/title is correct;
- one intended row/section exists per canonical matchup;
- probability values match the selected upstream prediction rows;
- trained-vs-heuristic provenance is checked upstream rather than inferred from report prose;
- `top_signals` is not presented as trained-model attribution;
- market-comparison fields are not interpreted without upstream scoring provenance;
- generated text does not contradict the numerical prediction context;
- fallback prose is acceptable when generated JSON fails;
- missing news is recognized as optional rather than silently assumed complete.

## Failure and degradation modes

- missing/unreadable predictions object;
- empty/malformed prediction data;
- prediction rows missing required identity/probability columns;
- missing news object, which degrades to no news rather than failing;
- missing OpenAI credential when generated reports are enabled;
- OpenAI transport/service/rate-limit failure;
- malformed generated JSON;
- generated text inconsistent with source numbers/context;
- duplicated upstream matchups hidden by report deduplication;
- scoring provenance lost because `scoring_method` is omitted from report outputs;
- S3 write failure after some report products have been written, creating mixed/missing outputs.

## Rerun and recovery

### Prediction changed

If scoring is corrected or rerun, regenerate all report products for that event.

### Generated-text failure

If prediction rows are correct and generated prose fails, rerun report generation after the external issue clears. The deterministic fallback may already have produced a usable analytical report, but it should be recognized as fallback prose.

### News changed

If news enrichment is refreshed and should be reflected in the report, rerun report generation only; rescore only when upstream features/scoring also need the changed news context.

### Wrong heuristic/trained provenance

If a report was generated from unintended heuristic predictions, restore/train the intended model, rerun scoring, verify `scoring_method=trained_model` upstream, then regenerate the report.

### Partial S3 publication

Because CSV/Parquet/Markdown writes are separate operations, rerun the complete report stage after correcting a write failure rather than assuming all three products belong to the same successful generation.

## Security and external-content considerations

- never publish `OPENAI_API_KEY` or AWS credential values;
- generated text and web-derived news are external/untrusted content and should not be treated as executable instructions;
- the report workflow needs only `contents: read` repository permission;
- repository write permission belongs only to the later publication workflow;
- market context is analytical only;
- live IAM, retention, and S3 object-integrity controls are not established by source.

## Limitations

- report outputs omit `scoring_method` provenance;
- “model” wording can describe heuristic-derived rows;
- `top_signals` is heuristic attribution, not trained-model explanation;
- report deduplication can hide upstream duplication;
- missing news is silently optional;
- generated text is nondeterministic when OpenAI is enabled;
- deterministic fallback is textual, not scoring fallback;
- no second JSON-repair call exists for report generation;
- no report-generation timestamp/model version/source prediction key is persisted in the report-row schema;
- CSV/Parquet/Markdown writes are not an atomic transaction;
- event-specific workflow defaults require operator verification.

## Related documentation

- [degenerate_investigator Target-Event Scoring](degenerate-investigator-target-event-scoring.md)
- [degenerate_investigator UFC Winner-Model Training](degenerate-investigator-ufc-winner-model-training.md)
- [degenerate_investigator Fighter Recent-News Enrichment](degenerate-investigator-fighter-recent-news-enrichment.md)
- [degenerate_investigator S3, Orchestration, and Security Boundary](degenerate-investigator-storage-orchestration-security.md)
- [Degenerate Investigator Documentation Workstream Plan](../high-director/degenerate-investigator-documentation-workstream-plan.md)

## Continuation

A future provenance fix should retain `scoring_method` and, ideally, model/artifact identifiers in report outputs. Any change to deduplication preference, generated prompt/schema, fallback text, report-row schema, Markdown structure, or S3 keys should update this page and the scoring/publication documentation together.
