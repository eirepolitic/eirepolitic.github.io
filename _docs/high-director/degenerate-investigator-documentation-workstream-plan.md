---
title: Degenerate Investigator Documentation Workstream Plan
summary: Persistent execution plan, evidence baseline, sequencing, safety boundary, and merge/deployment gates for the degenerate_investigator documentation workstream.
section: high-director
doc_type: agent
status: active
owner: High Director
created: 2026-08-07
updated: 2026-08-07
repository: degenerate_investigator
---

# Degenerate Investigator Documentation Workstream Plan

## Purpose

Persistent execution plan for the `degenerate_investigator` documentation workstream. The owner-wide catalogue remains the read-only scope contract; this file records sequencing, evidence, progress, and continuation state for this workstream only.

## Scope

Assigned catalogue targets:

- P0-10: repository and UFC analytics architecture.
- P0-11: S3, orchestration, and security/configuration boundary.
- P1-25: current UFC event/fighter ingestion.
- P1-26: historical fight/fighter-profile ingestion.
- P1-27: current MMA market-context ingestion.
- P1-28: fighter recent-news enrichment.
- P1-29: matchup feature engineering.
- P1-30: historical training-dataset builder.
- P1-31: UFC winner-model training.
- P1-32: target-event scoring.
- P1-33: fight-analysis report generator.
- P2-43: S3-to-repository report publication workflow.

## Documentation boundary

Document the repository as an analytical UFC data/ML/reporting system. Market-price data is an analytical input and model-vs-market comparison signal only. The repository does not implement staking logic, bankroll management, bookmaker selection, or bookmaker-targeted recommendations; documentation must not introduce those capabilities or external service-access guidance.

The model source of truth must always distinguish:

- trained estimator behavior and artifacts;
- the explicit scoring heuristic fallback;
- the single-class training fallback estimator;
- persisted model metrics;
- prediction and report artifacts;
- report-text fallback behavior.

Never describe any fallback as if it were the trained Random Forest model.

## Verified evidence baseline

Evidence inspected on 2026-08-07:

- repository tree;
- `README.md`;
- `requirements.txt`;
- `common/io_helpers.py`;
- all files under `extract/`;
- all files under `process/`;
- all GitHub Actions workflows under `.github/workflows/`;
- `reports/latest_fight_report.md`.

Verified storage defaults from `common/io_helpers.py`:

- bucket: `degenerative-investigator`;
- region: `us-east-2`.

Verified orchestration boundary: workflows are independently invoked with `workflow_dispatch`; no repository-level workflow automatically chains the complete pipeline. Operators coordinate stage order through workflow inputs and S3 object contracts.

## Planned sequence

1. Foundation PR: repository architecture plus S3/orchestration/security boundary.
2. Current-ingestion PR: event card and fighter profiles.
3. Historical-ingestion PR: historical fights and fighter profiles.
4. External-enrichment PR: recent news plus internal market-context contracts only.
5. Feature/training-data PR: feature engineering and historical dataset construction.
6. Model PR: training and model artifact/metrics behavior.
7. Inference/report PR: target-event scoring and report generation.
8. Publication PR: S3-to-repository report export workflow.
9. Cross-link/final consistency pass after syncing with current `main`.

## Merge and deployment gate

Before every merge:

1. run repository documentation validation;
2. confirm validation success;
3. merge the focused PR;
4. confirm the matching GitHub Pages deployment succeeds for the merged SHA;
5. only then begin the next major component.

## Security rules

Document secret and environment-variable names only where technically necessary and safe. Never persist credential values, tokens, passwords, private keys, personal email addresses, or personal account identifiers.

Known core names include:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`;
- `S3_BUCKET`;
- `OPENAI_API_KEY`.

No separate news-service API integration was verified in source. If live AWS/IAM/S3 state is required and cannot be established from repository source, request one coherent evidence source at a time and record only sanitized findings.

## Progress

- [x] Read documentation standard, catalogue, discovery plan, repository scan, templates, and current documentation examples.
- [x] Inspect complete `degenerate_investigator` repository tree and substantive files.
- [x] Re-verify S3 defaults and workflow orchestration model.
- [x] Create persistent workstream plan.
- [ ] Publish and merge P0-10 repository architecture documentation.
- [ ] Publish and merge P0-11 S3/orchestration/security boundary documentation.
- [ ] Complete P1-25 through P1-33 in focused PRs, keeping market-context documentation strictly internal/analytical.
- [ ] Complete P2-43 publication workflow documentation.
- [ ] Final cross-link and continuation review.

## Current continuation point

Foundation branch: `docs/degenerate-foundation-20260807`.

Current task: validate and merge the repository architecture and S3/orchestration/security boundary pages. Do not start subordinate pipeline pages until the foundation PR is merged and its matching Pages deployment succeeds.
