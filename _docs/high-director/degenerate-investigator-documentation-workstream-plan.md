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

Persistent execution and completion record for the `degenerate_investigator` documentation workstream. The owner-wide catalogue remains the read-only scope contract; this file records evidence, sequencing, completed target coverage, deployment gates, and future continuation rules for this workstream only.

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

- complete repository tree;
- `README.md`;
- `requirements.txt`;
- `common/io_helpers.py`;
- all files under `extract/`;
- all files under `process/`;
- all GitHub Actions workflows under `.github/workflows/`;
- `reports/latest_fight_report.md`.

Verified storage defaults from source:

- bucket: `degenerative-investigator`;
- region: `us-east-2`.

Verified orchestration boundary: workflows are independently invoked with `workflow_dispatch`; no repository-level workflow automatically chains the complete pipeline. Operators coordinate stage order through workflow inputs and S3 object contracts.

## Merge and deployment gate

Every component was handled through the required sequence:

1. repository documentation validation;
2. validation success confirmation;
3. focused merge;
4. matching GitHub Pages deployment success for the merged SHA;
5. only then continuation to the next major component.

The P1-32/P1-33 merge's first Pages run was cancelled by a newer parallel deployment, so those pages were explicitly re-gated through a fresh checkpoint merge rather than treating the cancelled run as success.

## Security rules

Document secret and environment-variable names only where technically necessary and safe. Never persist credential values, tokens, passwords, private keys, personal email addresses, or personal account identifiers.

Known core names include:

- `AWS_ACCESS_KEY_ID`;
- `AWS_SECRET_ACCESS_KEY`;
- `AWS_REGION`;
- `S3_BUCKET`;
- `OPENAI_API_KEY`.

If live AWS/IAM/S3 state is needed in future and cannot be established from repository source, collect one coherent sanitized deployed-state source at a time and do not guess.

## Completion record

- [x] P0-10 and P0-11 foundation merged; Pages succeeded for `050fabcd59fa154fdb9cac51fa19b422720e3504`.
- [x] P1-25 current UFC event/fighter ingestion merged; Pages succeeded for `2ee49dde1dac5ce26b4786731332acbf205612df`.
- [x] P1-26 historical fight/fighter-profile ingestion merged; Pages succeeded for `33f7bf19997ac91aa0b3b3803d14af989b0c9e80`.
- [x] P1-27 and P1-28 enrichment documentation merged; Pages succeeded for `cb7be00a986f5da4ae9a84e97afc4bfa1ae23e34`.
- [x] P1-29 and P1-30 feature/training-data documentation merged; Pages succeeded for `30dd2d6622386a56db5289c1c771a2af5d744c19`.
- [x] P1-31 winner-model training documentation merged; Pages succeeded for `ea39879138875a9ec09b8b9f7a0843a4f55ec3ef`.
- [x] P1-32 and P1-33 scoring/report documentation merged in PR #87 as `6210e0bc5da013747f0e8d0edfedb7bb11187dd6`; its original Pages run was cancelled by a newer parallel deployment.
- [x] P1-32/P1-33 were re-gated through PR #88; matching Pages deployment succeeded for `ed5c425e6edc5602a4406678d7f992e78cfe38b8`.
- [x] P2-43 report-publication workflow documentation merged; Pages succeeded for `6837cce5ba206f1936f5402ce2f8c25e87ec76ce`.
- [x] Final consistency pass corrected the current fighter-profile schema count from 18 to 19 fields.
- [x] Final consistency PR #94 merged; matching Pages deployment succeeded for `a3a3ac7fb9bb301f364b58724c7308ae9fb58507`.
- [x] All assigned `degenerate_investigator` catalogue targets are documented and deployment-gated.

## Current continuation point

The assigned `degenerate_investigator` documentation workstream is complete.

Future maintenance should be source-driven: when implementation changes alter workflow inputs, S3 keys, schemas, feature semantics, model/fallback behavior, report provenance, security/configuration names, or publication controls, update the corresponding authoritative page in the same change set and use the normal validation/Pages gate.
