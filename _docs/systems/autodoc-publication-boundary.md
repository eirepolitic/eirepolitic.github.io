---
title: AutoDoc reviewed-document website publication boundary
summary: Current verified boundary that publishes reviewed AutoDoc Markdown into eirepolitic.github.io, including workflow inputs, path validation, WEBSITE_PAT use, overwrite behavior, direct-push semantics, failure modes, and the mismatch with current documentation governance.
section: systems
doc_type: system
status: active
created: 2026-08-07
updated: 2026-08-07
last_verified: 2026-08-07
owner: Eire Politic
repository: autodoc
system: AutoDoc
order: 34
permalink: /projects/systems/autodoc-publication-boundary/
tags:
  - autodoc
  - publishing
  - github-actions
  - github-pages
  - security
---

# AutoDoc reviewed-document website publication boundary

## Summary

AutoDoc publishes a reviewed Markdown artifact into the documentation website through `.github/workflows/publish_to_website.yml` in the `autodoc` repository. The workflow is manually dispatchable and is also dispatched by the current Appsmith `DocsViewer` page.

The workflow validates its input strings and source reviewed-file path, clones `eirepolitic.github.io` using the secret named `WEBSITE_PAT`, copies the reviewed Markdown file into `projects/<dest_type>/<doc_key>.md`, commits if content changed, and pushes directly to the cloned website repository.

This is **CURRENT VERIFIED BEHAVIOR**. It is not the same as **CURRENT DOCUMENTATION GOVERNANCE**, which requires branch/PR, successful `Validate documentation`, merge, successful matching Pages deployment, and live verification for material documentation changes.

No workflow redesign is approved by this documentation page.

## Source of Truth

Current implementation:

```text
autodoc/.github/workflows/publish_to_website.yml
```

Current caller evidence:

```text
_docs/systems/autodoc-appsmith-intake.md
_docs/high-director/autodoc-appsmith-live-source-2026-08-07.md
```

Current documentation governance:

```text
_docs/runbooks/publish-documentation-change.md
_docs/runbooks/documentation-site-operations.md
.github/workflows/validate-documentation.yml
scripts/validate_docs.py
```

Backend workflow source is authoritative for current publication mechanics. Site runbooks are authoritative for current documentation-governance expectations.

## Workflow Definition

Workflow name:

```text
Publish reviewed doc to website
```

Trigger:

```text
workflow_dispatch
```

Inputs:

| Input | Required | Current meaning |
| --- | --- | --- |
| `project` | yes | AutoDoc project below `doc_configs/<project>/` |
| `type` | yes | AutoDoc document type below `docs/<project>/<type>/` |
| `doc_key` | yes | Markdown filename without `.md` |
| `dest_type` | yes | Website folder below `projects/<dest_type>/` |
| `overwrite` | no | String, default `"true"`; controls replacement when destination file exists |

Workflow permissions declared in `autodoc`:

```yaml
permissions:
  contents: read
```

This permission applies to the workflow's normal repository token boundary in `autodoc`. Website write capability is supplied separately through the `WEBSITE_PAT` credential used in the clone URL.

## Current Appsmith Dispatch

The verified `DocsViewer` page dispatches this workflow through the GitHub Actions API with:

```text
ref: main
project: selected project
type: selected _index.json entry type
doc_key: selected _index.json entry doc_key
dest_type: selected website destination type
overwrite: "true"
```

The Appsmith publication button is disabled unless the selected AutoDoc version is `reviewed` and a destination type is selected.

That UI condition is a caller-side control. The workflow independently verifies the reviewed source file exists before publication.

## Source Artifact Boundary

The workflow constructs the source path as:

```text
docs/<project>/<type>/reviewed/<doc_key>.md
```

The file must exist in the checked-out `autodoc` repository. If it does not exist, the workflow exits with status code `2` before cloning the website repository.

This establishes an explicit generated/reviewed lifecycle boundary: the publication workflow accepts the reviewed-path artifact, not the raw generated path.

File existence alone does not prove the review workflow was successful, that a human approved the document, or that current documentation governance has been followed.

## Input Validation

Before locating the reviewed file, the workflow validates `project`, `type`, `doc_key`, and `dest_type`.

For each value it rejects:

- empty string;
- any value containing `..`;
- any value beginning with `/`.

It additionally requires `dest_type` to be a single folder name by rejecting values containing `/`.

### Validation boundary precision

Current source does **not** contain an equivalent explicit slash prohibition for `project`, `type`, or `doc_key`. Document the controls exactly as implemented; do not describe them as a general-purpose path sanitizer beyond those checks.

The workflow uses `set -euo pipefail`, so an explicit validation error exits the step and prevents later steps from running.

## Website Repository Trust Boundary

The clone step sets:

```text
WEBSITE_PAT <- secrets.WEBSITE_PAT
```

If the secret is empty, the workflow exits with status code `2`.

It then clones:

```text
https://github.com/eirepolitic/eirepolitic.github.io.git
```

using token authentication embedded in the clone URL at runtime.

Only the secret name and role are documented. The PAT value must never be published, copied into documentation, or exposed through screenshots/log excerpts.

The workflow configures the website-repository commit identity as:

```text
autodoc-bot
autodoc-bot@users.noreply.github.com
```

The workflow source does not hard-code a website branch name after clone. `git push` operates from the branch checked out by the clone and its configured upstream. Current documentation-site source establishes `main` as the site's default/source branch, but the AutoDoc publication workflow itself does not explicitly say `git checkout main`.

## Destination Boundary

The destination directory is:

```text
website/projects/<dest_type>
```

The directory must already exist. The workflow does not create it.

If the directory is missing, the workflow exits with status code `2` and instructs the operator to create the folder in the website repository or restrict the dropdown to existing folders.

Destination file:

```text
website/projects/<dest_type>/<doc_key>.md
```

The workflow copies the reviewed source file directly with `cp`; there is no transformation or documentation-standard validation in this workflow before the copy.

## Overwrite Semantics

If the destination file already exists:

- `overwrite == "true"` allows replacement;
- any other value causes the workflow to exit with status code `2`.

The current Appsmith caller always dispatches `overwrite: "true"`.

This means Appsmith publication currently permits replacement of an existing same-path website Markdown file when the workflow reaches this step successfully.

## Commit and Push Behavior

After copying, the workflow runs in the cloned website repository:

```text
git add -A
```

If the staged tree has no changes, it prints `No changes to commit.` and exits successfully without a commit or push.

If there are changes, it commits with:

```text
Publish reviewed doc: <doc_key> -> projects/<dest_type>/
```

then runs:

```text
git push
```

There is no branch creation, pull request creation, documentation validator invocation, merge step, or explicit Pages deployment wait/check in `publish_to_website.yml`.

## CURRENT VERIFIED BEHAVIOR

The current production path represented by source is:

```text
reviewed AutoDoc Markdown
  -> workflow_dispatch publish_to_website.yml
  -> input/path checks
  -> WEBSITE_PAT-authenticated clone of eirepolitic.github.io
  -> copy into projects/<dest_type>/<doc_key>.md
  -> direct commit in cloned website repository
  -> direct git push
```

A no-change copy produces no commit.

A successful `git push` is the end of this workflow's explicit responsibility.

## CURRENT DOCUMENTATION GOVERNANCE

The current documentation publishing runbooks require a material documentation change to follow:

```text
branch from current main
  -> focused pull request
  -> Validate documentation succeeds
  -> merge
  -> matching GitHub Pages build succeeds
  -> matching GitHub Pages deploy succeeds
  -> published result checked
```

The validator checks required metadata, allowed sections/types/statuses, dates, archive rules, duplicate permalinks, internal links/assets, and related-document URLs.

The AutoDoc direct publication workflow does not run these governance checks and does not create a PR.

## Governance Mismatch

The two paths are therefore intentionally documented as different current realities:

| Area | AutoDoc publication workflow | Current documentation governance |
| --- | --- | --- |
| Change branch | none created | required |
| Pull request | none | required |
| `Validate documentation` | not run | required before merge |
| Merge gate | none | required |
| Website repository write | direct PAT-authenticated push | merge to `main` after validation |
| Matching Pages success | not checked | required |
| Live result verification | not performed by workflow | required by runbook |

This is a verified mismatch, not an approved security or architecture change request.

## Trust and Security Boundaries

### Reviewed artifact -> publication job

Inputs select which reviewed artifact will be copied. Incorrect project/type/doc-key input can target the wrong reviewed path if it passes validation and exists.

### `autodoc` -> `eirepolitic.github.io`

`WEBSITE_PAT` crosses the repository boundary and grants the git operation whatever effective website-repository access its live configuration allows. Repository source proves the credential is used for authenticated clone/push; it does not prove the exact live PAT scope.

### Destination selection

`dest_type` controls the website subfolder. It is restricted to a single folder component, but the workflow does not independently check a documentation taxonomy beyond requiring that directory to exist.

### Direct website push

The workflow can place Markdown into a public GitHub Pages source repository without the current documentation PR validator gate. That is the central governance/trust mismatch.

## Failure Modes and Recovery

### Invalid input

**Behavior:** validation exits `2` before publication.

**Recovery:** correct the caller input. Do not weaken path checks to force a publish.

### Reviewed Markdown missing

**Behavior:** exits `2` before website clone.

**Recovery:** verify the reviewed artifact lifecycle. Run/fix review as appropriate rather than publishing raw Markdown.

### `WEBSITE_PAT` missing

**Behavior:** exits `2` at the clone step.

**Recovery:** treat this as a credential/access issue. Do not place a token value in source, documentation, workflow inputs, or chat logs. Credential changes require explicit security/access handling.

### Website clone/authentication fails

**Behavior:** unsuppressed git failure stops the workflow because `set -euo pipefail` is enabled.

**Recovery:** inspect non-secret error output and verify repository/credential access through approved administration. Do not expose token values while troubleshooting.

### Destination directory missing

**Behavior:** exits `2`; workflow does not create the folder.

**Recovery:** verify the intended website taxonomy/destination. Creating a new public information-architecture destination may be a design decision; do not create one implicitly as a recovery shortcut.

### Destination exists and overwrite is not true

**Behavior:** exits `2` without copying.

**Recovery:** decide whether replacement is intended. The current Appsmith path requests overwrite=true, but a caller can dispatch another value.

### Copied content is identical

**Behavior:** exits successfully with `No changes to commit.`; no new website commit.

### `git push` fails

**Behavior:** workflow fails at the final step.

**Recovery:** inspect repository state/access and retry only after resolving the actual cause. The copied file exists only in the runner checkout until a push succeeds.

### Direct push succeeds but Pages later fails

`publish_to_website.yml` has no matching Pages gate. Use current website operations/runbooks to inspect the Pages run for the pushed commit. A successful AutoDoc publication workflow alone is not evidence of a healthy deployed site.

## Operational Verification After Direct Publication

Until the architecture is intentionally changed, an operator assessing a direct AutoDoc publication should separately verify:

1. identify the resulting `eirepolitic.github.io` commit;
2. inspect whether current documentation validation/governance was bypassed;
3. inspect the matching GitHub Pages build/deploy result;
4. verify the public page/content if publication is intended;
5. correct problems through the normal documentation PR discipline rather than rewriting public history.

These are governance/verification steps, not steps implemented by `publish_to_website.yml` itself.

## Known Limitations

- Exact live `WEBSITE_PAT` scope is not established by repository source.
- The workflow does not explicitly select the website branch after clone.
- It validates selected path patterns but is not a replacement for the documentation validator.
- It does not create missing destination folders.
- It does not wait for or inspect GitHub Pages deployment.
- It does not establish human approval of the reviewed artifact.

## Next Safe Development Action

Publish this documentation component through the workstream's branch/PR/validation/merge/Pages gate. Then proceed to the P1 asset enrichment/source-resolution stage on a fresh branch from current `main`.

Do not alter `WEBSITE_PAT`, workflow permissions, overwrite defaults, Appsmith dispatch behavior, or publication architecture without explicit approval.

## Related Documents

- [AutoDoc system](/projects/systems/autodoc/)
- [AutoDoc Appsmith intake](/projects/systems/autodoc-appsmith-intake/)
- [AutoDoc pipeline orchestration](/projects/systems/autodoc-pipeline-orchestration/)
- [Publish a documentation change](/projects/runbooks/publish-documentation-change/)
- [Documentation site operations](/docs/runbooks/documentation-site-operations/)
- [AutoDoc documentation workstream plan](/projects/high-director/autodoc-documentation-workstream-plan/)

## Verification Record

- Last verified: `2026-08-07`
- Verified against: current `autodoc/main` `.github/workflows/publish_to_website.yml`; current verified AutoDoc Appsmith export documentation; current `eirepolitic.github.io` publication and site-operations runbooks.
- Verified by: High Director
- Verification scope: workflow name/trigger/inputs/permissions, validation logic, reviewed source path, `WEBSITE_PAT` boundary, destination/overwrite semantics, no-change behavior, commit/push behavior, failure paths, and current governance mismatch.
- Not verified: exact live PAT scope or external repository-rule enforcement.
