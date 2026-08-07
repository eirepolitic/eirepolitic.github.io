---
title: Publish a Documentation Change
summary: Use this runbook to safely publish a documentation change through validation, merge, GitHub Pages deployment, and live verification.
section: runbooks
doc_type: runbook
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: Eire Politic
repository: eirepolitic.github.io
system: Eire Politic Documentation Site
order: 20
permalink: /projects/runbooks/publish-documentation-change/
tags:
  - github
  - publishing
related:
  - /docs/runbooks/documentation-site-operations/
  - /projects/repositories/eirepolitic-github-io/
  - /projects/systems/documentation-site/
---

# Publish a Documentation Change

## Purpose

Use this procedure for a material documentation change that must be reviewed, validated, merged into `main`, deployed through GitHub Pages, and checked after publication.

## Status and Last Verification

- Status: verified
- Last verified: `2026-08-06`
- Verified against: PRs #20 through #22 and Pages runs `31137413142`, `31137516088`, and `31137621658`

## Use This Runbook When

- Creating or materially updating a file under `_docs/`.
- Updating documentation templates or metadata rules.
- Publishing a documentation change that must reach the public GitHub Pages site.

## Do Not Use This Runbook When

- The change alters information architecture, security boundaries, or cost-bearing infrastructure and requires a separate decision.
- A suspected credential or confidential-data exposure is involved; stop and use the appropriate security response instead.

## Impact and Risk

A merged change can become public through GitHub Pages. Broken metadata or links can affect navigation, search, or rendering. Secret or confidential content must never be committed because removal from the live site does not remove repository history.

## Prerequisites and Access

- Repository: `eirepolitic.github.io`.
- Base branch: `main`.
- Permission to create branches, open pull requests, merge, and inspect GitHub Actions and Pages workflows.
- Relevant template under `_templates/` and `DOCUMENTATION_STANDARD.md` when creating a technical document.

## Source of Truth

- Repository: `eirepolitic.github.io`
- Documentation: `_docs/`
- Templates: `_templates/`
- Standard: `DOCUMENTATION_STANDARD.md`
- Validator: `scripts/validate_docs.py`
- Validation workflow: `.github/workflows/validate-documentation.yml`
- Publishing target: GitHub Pages from `main`

## Safety Checks

Before changing or merging documentation:

1. Confirm the branch was created from current `main`.
2. Confirm the intended category and template.
3. Verify facts against authoritative repository files or systems.
4. Ensure no credentials, tokens, private keys, personal data, or confidential identifiers are present.
5. Preserve established permalinks unless a deliberate migration is required.
6. Do not merge while documentation validation is failing.

## Procedure

### 1. Create the focused change

1. Create a branch from `main`.
2. Edit or create only the files required for the documentation step.
3. Update the persistent build or initiative plan when a tracked step changes state.
4. Set `updated` to the change date and change `last_verified` only when the implementation was deliberately checked.

### 2. Open the pull request

1. Open a pull request into `main`.
2. Keep the title and description limited to the focused documentation change.
3. Confirm `.github/workflows/validate-documentation.yml` creates a validation run for the pull request.

### 3. Validate before merge

1. Open the latest `Validate documentation` workflow run for the branch.
2. Confirm the run completes with `conclusion: success`.
3. If it fails, inspect the validator error, correct the referenced file or rule, and rerun through a new commit or manual dispatch.
4. Do not weaken the validator to bypass a valid error.

Optional local check:

```bash
python -m pip install PyYAML==6.0.2
python scripts/validate_docs.py
```

### 4. Merge

1. Merge only after validation passes.
2. Record the merge commit or pull request number in the persistent plan when the step is tracked.

### 5. Verify GitHub Pages

1. Open the Pages build and deployment run created for the merged commit on `main`.
2. Confirm the `build` job succeeds.
3. Confirm the `deploy` job succeeds.
4. Confirm the workflow reaches `status: completed` and `conclusion: success`.

### 6. Verify the published result

1. Open the affected live documentation URL.
2. Confirm the page renders and the intended content is present.
3. For new technical documents, confirm the expected section, navigation, related links, and search behavior.
4. Record the successful Pages run in the persistent plan when applicable.

## Validation and Success Criteria

The change is complete only when:

- Pull-request documentation validation passed.
- The pull request merged into `main`.
- GitHub Pages build succeeded for the merged commit.
- GitHub Pages deployment succeeded for the merged commit.
- The affected page is available at its expected published URL.

## Rollback or Recovery

If a published documentation change is wrong but not security-sensitive, create a small corrective or revert pull request, validate it, merge it, and verify the replacement Pages deployment. Do not rewrite published branch history as the normal recovery path.

If the issue involves sensitive data, stop normal publishing work and use the appropriate security response because a normal revert does not remove repository history.

## Failure Modes and Escalation

| Failure | Safe response | Evidence | Escalate to |
| --- | --- | --- | --- |
| Documentation validation fails | Fix the referenced document or valid rule violation | Workflow run and validator output | Documentation owner |
| Jekyll build fails | Inspect configuration, Liquid, front matter, and layout references | Pages build job | Documentation owner |
| Deploy job fails | Inspect the deploy job and avoid unrelated changes | Pages deployment run | Repository owner |
| Live page differs from merged source | Confirm the deployment commit and browser cache | Merge SHA, Pages run, live URL | Repository owner |

## Security Guidance

Use approved GitHub access only. Never place secret values in documentation, branch names, pull-request bodies, logs, screenshots, or copied workflow output. Treat all GitHub Pages content as public.

## Known Limitations

- This runbook covers documentation publishing only, not application or infrastructure deployment.
- GitHub Pages and GitHub Actions availability are external dependencies.
- A successful workflow does not replace human verification of factual documentation accuracy.

## Follow-up Work

Update related documentation or the persistent plan if the published change completes a tracked initiative step or exposes a real template defect.

## Next Safe Action

After successful publication, continue with the next incomplete item in `/projects/high-director/example-documents-plan/` using a new branch from updated `main`.

## Related Documents

- [Documentation Site Operations](/docs/runbooks/documentation-site-operations/) covers broader maintenance and troubleshooting.
- [eirepolitic.github.io](/projects/repositories/eirepolitic-github-io/) documents the repository.
- [Eire Politic Documentation Site](/projects/systems/documentation-site/) documents the system boundary.

## Verification Record

- Last verified: `2026-08-06`
- Verified against: PRs #20-#22, validation runs `31137389854`, `31137496390`, `31137604054`, and Pages runs `31137413142`, `31137516088`, `31137621658`
- Verified by: High Director
- Verification scope: branch/PR workflow, automated documentation validation, merge, Pages build, Pages deployment, and post-deployment confirmation
- Known unverified steps: live-page visual inspection is procedural and was not independently automated
