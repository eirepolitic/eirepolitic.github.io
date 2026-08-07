---
title: bb-comp-prices product matching and confidence scoring
summary: Verified generic evidence scoring plus Amazon-specific exact-variant and verification-state rules that produce matched, review, and rejected product assessments.
section: systems
doc_type: pipeline
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: bb-comp-prices
system: Competitor Pricing Platform
order: 35
permalink: /projects/systems/bb-comp-prices-product-matching/
tags:
  - matching
  - data-quality
  - scoring
  - amazon
---

# bb-comp-prices product matching and confidence scoring

## Summary

The product-matching subsystem converts normalized Best Buy/Amazon product pairs into durable `matched`, `review`, or `rejected` assessments. It combines a reusable generic evidence score with a stricter Amazon-specific variant gate and Amazon acquisition verification level.

For the current persisted Amazon pipeline, the generic score is **not authoritative by itself**. After generic evidence is calculated, current `_assess_amazon_product()` applies exact Amazon variant rules that can force rejection, force search-verified candidates to review, or promote detail-verified exact variants to matched.

This is deterministic repository logic, not a learned model and not evidence of universal product-match accuracy.

## Source of Truth

- generic descriptors/assessment/output models: `src/bb_comp_prices/matching/models.py`;
- generic scoring logic: `src/bb_comp_prices/matching/score.py`;
- Amazon exact variant rules: `src/bb_comp_prices/competitors/amazon_variant.py`;
- persisted matching pipeline: `src/bb_comp_prices/pipeline/product_matching.py`;
- workflow: `.github/workflows/product_matching.yml`;
- Amazon-specific behavior tests: `tests/unit/test_product_matching_amazon.py`;
- generic scoring tests: `tests/unit/test_matching_score.py`;
- persisted output schema: [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/).

`docs/LATEST_PRODUCT_MATCHING_REPORT.md` is retained validation evidence but is stale relative to the current Amazon-specific override logic: it reports generic `attribute_score` outcomes for rows that current executable/tests now treat through the authoritative Amazon exact-variant/verification gate. It must not be used as proof of current disposition behavior.

## Inputs and Pairing Boundary

`run_product_matching()` reads:

```text
latest/bestbuy_products.parquet
latest/amazon_products.parquet
```

Amazon acquisition already stores the originating `bestbuy_product_id` on each `AmazonProductRecord`. Matching therefore does **not** perform an all-to-all candidate search. Each current Amazon row is assessed only against the Best Buy row with the same stored `bestbuy_product_id`.

If an Amazon row references a Best Buy ID absent from the current Best Buy latest dataset, that row is skipped and its ID is returned under `missing_bestbuy_ids`.

Current persisted pipeline output uses:

```text
competitor_source = amazon
competitor_product_id = ASIN
```

`ProductMatchRecord` permits `competitor_source="walmart"` at the schema level, but current `run_product_matching()` does not load a Walmart product dataset or create Walmart match records.

## Generic Product Descriptor

`ProductDescriptor` contains:

- `product_id`;
- `title`;
- optional `brand`;
- optional `model_number`;
- UPC list;
- optional condition.

Current Best Buy descriptors populate all available fields. Current Amazon descriptors built by `run_product_matching()` contain ASIN, title, and synthetic `condition="New"`; they do not populate Amazon brand/model/UPC fields from the current Amazon product schema.

This means generic UPC/model/brand evidence is potentially richer for other/future descriptors than it is for the current Amazon candidate descriptor.

## Generic Evidence and Scoring

`assess_product_match()` first normalizes text case/hyphens/whitespace and extracts recognized capacities and colours.

### Immediate rejection

The function immediately returns score `0` when:

- candidate title is missing (`missing_candidate_title`); or
- candidate title contains an implemented accessory term (`candidate_is_accessory`).

### Contradictions

Non-immediate contradiction evidence includes:

- `candidate_not_new` — candidate condition/title contains used/renewed/refurbished/restored/open-box terminology;
- `capacity_mismatch` — both sides contain explicit capacities and the sets are disjoint;
- `color_mismatch` — both sides contain recognized colours and the sets are disjoint;
- `brand_mismatch` — both explicit brand fields exist and differ after normalization.

### Exact evidence

- UPCs are digit-normalized and count as an exact UPC match when the non-empty sets intersect.
- Model evidence matches when normalized source model equals candidate model or appears in the candidate title.
- Brand evidence matches when normalized source brand equals candidate brand or appears in candidate title.

### Fuzzy/attribute score

The pre-cap score is:

```text
0.45 * RapidFuzz token_set_ratio(title)
+ 55 if UPC exact match
+ 35 if model exact/title match
+ 12 if brand match
+ 15 if explicit capacity sets are equal
+ 8  if recognized colour sets overlap
```

The score is then constrained by contradiction rules:

- any strong contradiction (`candidate_not_new`, `capacity_mismatch`, `brand_mismatch`) caps score below the review threshold (`review_threshold - 0.01`);
- `capacity_mismatch` or `candidate_not_new` additionally caps score at `25`;
- `color_mismatch` subtracts `25`;
- final score is rounded/clamped to `0..100`.

Generic `method` is:

- `exact_upc` when UPC evidence matches;
- otherwise `exact_model` when model evidence matches;
- otherwise `attribute_score`.

## Generic Threshold States

Default generic thresholds are:

```text
matched_threshold = 75
review_threshold  = 60
```

Generic state logic is:

1. contradictions plus score below review -> `rejected`;
2. score >= matched threshold -> `matched`;
3. score >= review threshold -> `review`;
4. otherwise -> `rejected`.

These thresholds are exposed by `.github/workflows/product_matching.yml` and passed into `run_product_matching()`.

However, the current Amazon-specific layer below supersedes the generic final state when exact variant verification succeeds/fails.

## Amazon-Specific Exact Variant Gate

`_assess_amazon_product()` first runs the generic assessment, then applies `exact_variant_mismatch_reasons()` using Best Buy and Amazon titles plus the source Best Buy model number.

The stricter Amazon variant function checks implemented contradictions including:

- missing candidate title;
- accessory;
- bundle;
- non-new condition terminology;
- recognized Pixel/Galaxy S/iPhone family-generation-variant mismatch;
- source family identifiable but candidate family missing unless model evidence resolves it;
- capacity mismatch;
- colour mismatch.

It also stores these fields under `attribute_evidence`:

```text
amazon_exact_variant_gate
amazon_variant_reasons
amazon_verification_level
```

### Variant contradiction -> rejected

Any Amazon exact-variant reason forces:

```text
status = rejected
score = 0
method = amazon_exact_variant_gate
```

Generic score strength cannot override that contradiction.

### Search-verified exact variant -> review

When acquisition produced `verification_level="search"` and no exact-variant contradiction exists:

```text
status = review
score = max(generic_score, 75)
method = amazon_search_variant_gate
```

Reason: an exact search result was observed, but the product detail page was not verified.

This manual-review boundary is explicit and is not controlled by lowering the configured generic review threshold.

### Detail-verified exact variant -> matched

For any verification level other than literal `search`—current data uses `detail`—with no variant contradiction:

```text
status = matched
score = max(generic_score, 90)
method = amazon_exact_variant_gate
```

Current tests explicitly verify that a correct detail-verified Amazon variant is not downgraded merely because the generic score would otherwise be lower.

## Meaning of Match Score

The persisted `match_score` should be interpreted together with `match_method`, verification evidence, and contradictions.

In particular:

- score `0` with `amazon_exact_variant_gate` represents a forced exact-variant rejection;
- search-verified exact variants have a floor of `75` but remain `review`;
- detail-verified exact variants have a floor of `90` and are `matched`;
- therefore current Amazon `match_score` is not a pure calibrated probability or a single continuous confidence measure.

Do not present `75`, `90`, or any other score as a percent probability that two products are identical.

## Evidence Stored Per Assessment

`ProductMatchRecord` persists:

- source Best Buy ID;
- competitor source/ID/URL;
- status;
- method;
- score;
- identifier evidence;
- attribute evidence;
- contradiction list;
- human-readable `review_reason`;
- run/timestamp.

Generic identifier evidence contains normalized source/candidate UPCs, UPC-match flag, source/candidate models, and model-match flag.

Generic attribute evidence contains brand evidence/conflict, title similarity, source/candidate capacities, and source/candidate colours. Amazon-specific fields are then added as described above.

CSV stores the evidence objects/lists as JSON text; Parquet preserves nested values through the repository writer.

## Outputs

When at least one assessment record exists:

```text
curated/product_matches_history/date=YYYY-MM-DD/run_id=<run_id>/part-00000.{csv,parquet}
latest/product_matches.{csv,parquet}
```

If no records are produced, no current writer call occurs. An older stable `latest/product_matches.*` can therefore remain. Operators must compare run IDs/timestamps rather than treating object existence as proof that matching ran successfully against the newest upstream inputs.

## Workflow Operation

`.github/workflows/product_matching.yml` is manual dispatch only and exposes:

- `matched_threshold`, default `75`;
- `review_threshold`, default `60`.

It uses Python 3.12, base package dependencies, `contents: read`, and secret-backed AWS access. It invokes `scripts/run_product_matching.py`, captures JSON output, uploads it for 14 days, and writes it to the job summary.

The end-to-end controller separately validates that the review threshold is below the matched threshold before invoking matching. The standalone workflow delegates argument validation to its wrapper/current implementation; operators should preserve `review < matched` to maintain meaningful generic threshold ordering.

## Validation Evidence

Current unit tests are more authoritative for the current Amazon override behavior than the retained latest matching report.

`tests/unit/test_product_matching_amazon.py` verifies:

- exact detail-verified Pixel variant -> authoritative `matched`, method `amazon_exact_variant_gate`, score at least 90;
- exact search-verified Samsung variant -> `review`, method `amazon_search_variant_gate`, score at least 75;
- wrong Pixel Pro/base variant -> `rejected` with `phone_family_mismatch`;
- an exact Samsung detail variant is not downgraded by a lower generic score.

`tests/unit/test_matching_score.py` covers reusable generic score behavior.

The committed `docs/LATEST_PRODUCT_MATCHING_REPORT.md` records 2 historical assessment rows (1 review, 1 rejected) and all of its implemented structural checks passing, but its methods are generic `attribute_score`. Because current source/tests now make Amazon exact-variant verification authoritative, this report is stale for current disposition semantics and should be regenerated before it is used as current operational validation.

## Manual Review Boundary

Current automatic/manual boundary is deliberately narrow:

- Amazon exact variant contradiction -> automatic reject;
- Amazon detail-verified exact variant -> automatic match;
- Amazon search-verified exact variant -> manual `review` because detail evidence is missing.

A reviewer should use the persisted acquisition raw evidence, Amazon product verification level, titles/variant evidence, and source Best Buy product details. The repository does not currently include a workflow that records a human approval decision back into the match dataset; `review` is a state/output for downstream/manual handling, not an implemented approval UI.

## Safe Rerun Procedure

1. Verify `latest/bestbuy_products.parquet` and `latest/amazon_products.parquet` have the intended compatible run IDs/observation context.
2. Confirm Amazon product `verification_level` values, because they directly determine review versus matched behavior after the exact variant gate.
3. Use default thresholds unless deliberately testing the generic scoring boundary; changing generic thresholds does not override exact Amazon contradiction or verification-state rules.
4. Run the matching workflow and inspect `missing_bestbuy_ids` plus matched/review/rejected counts.
5. Inspect individual `ProductMatchRecord` evidence and contradictions for unexpected outcomes.
6. Confirm history/latest output run IDs after success.
7. Do not accept a search-verified `review` simply by lowering thresholds; the current authoritative Amazon layer intentionally keeps it review-only.
8. Do not manually alter scores to force acceptance. If rules are wrong, change/test documented rule logic explicitly in source.

## Security and Data-Quality Boundary

Matching itself makes no retailer network calls. It reads/writes S3 through AWS credentials supplied by the executing environment. It therefore inherits the S3 security boundary but does not require retailer authentication/browser access.

The primary risk is data-quality rather than credential exposure: stale/mismatched `latest/` upstream products can produce technically valid assessments against unintended observations. Run IDs, timestamps, verification levels, and history objects are required operational context.

## Known Limitations

- Current persisted matching only evaluates Amazon rows already linked to a Best Buy product ID; it is not an independent candidate-discovery engine.
- `ProductMatchRecord` permits Walmart but current pipeline does not read Walmart products.
- Amazon candidate descriptors currently omit Amazon brand/model/UPC fields, reducing the generic exact-evidence channels available at this stage.
- Recognized phone families, colours, accessory/bundle/condition terms are finite rule sets.
- Amazon-specific floor scores (`75` review, `90` matched) mean match score is not a calibrated probability.
- Search-verified matches require review but there is no implemented repository approval workflow that writes a final human decision.
- Empty assessment runs do not clear an older `latest/product_matches.*` object.
- The committed latest matching report is stale relative to current executable Amazon override logic and needs regeneration.

## Next Safe Development Action

Move to the P2 Walmart.ca acquisition/probe subsystem. Document current probe/research maturity and the explicit end-to-end blocked state separately from planned production acquisition. Do not imply a persisted Walmart product/matching pipeline exists until executable source demonstrates it.

## Related Documents

- [Amazon.ca competitor acquisition and recovery](/projects/systems/bb-comp-prices-amazon-acquisition/)
- [bb-comp-prices S3 storage and data products](/projects/data/bb-comp-prices-data-products/)
- [bb-comp-prices orchestration/security boundary](/projects/systems/bb-comp-prices-orchestration-security/)
- [bb-comp-prices repository](/projects/repositories/bb-comp-prices/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: `bb-comp-prices` `main` commit `d24c5bd98a6764bd75476fbf31c6441657305640`; `matching/models.py`; `matching/score.py`; `competitors/amazon_variant.py`; `pipeline/product_matching.py`; `.github/workflows/product_matching.yml`; `tests/unit/test_matching_score.py`; `tests/unit/test_product_matching_amazon.py`; `docs/LATEST_PRODUCT_MATCHING_REPORT.md` as stale historical validation evidence.
- Verified by: High Director
- Verification scope: generic evidence/scoring formula, contradictions, thresholds, Amazon-specific authoritative variant and verification rules, persisted states/evidence, manual-review boundary, workflow/rerun behavior, stale latest/report risks, and current limitations.
