---
title: Sly Director — Verified GitHub Write-Test Behavior
summary: Live-verified branch-prefix and transient approval behavior for the Sly Director GitHub connector.
section: high-director
doc_type: reference
status: active
created: 2026-09-15
updated: 2026-09-15
last_verified: 2026-09-15
order: 90
permalink: /docs/high-director/build-your-own-claude/write-test-observed-behavior/
---

# Verified GitHub Write-Test Behavior

The end-to-end write test has been verified successfully against `claude-director-test`.

Verified operations:

```text
create branch
create/update files
create pull request
inspect workflow run
inspect workflow jobs
squash merge
verify final files on main
```

## Branch prefix

The connector automatically applies the configured branch prefix:

```text
BRANCH_PREFIX=sly/
```

For example, a requested branch name:

```text
connection-test
```

is created as:

```text
sly/connection-test
```

This is expected behavior and does not require any change to the tool call.

## Transient `No approval received.` response

During the live write test, one `get_workflow_run` call returned:

```text
No approval received.
```

An immediate identical retry succeeded.

Treat this as a transient connector approval-handshake timing issue when:

```text
the previous connector calls succeeded
the identical retry succeeds immediately
there is no GitHub permission or API error
```

Sly Director should retry the same read-only inspection call rather than treating this response as a repository-permission failure.

## Test branch cleanup

After the pull request is merged and final state is verified, the temporary branch can be deleted:

```text
sly/connection-test
```

Deleting the merged test branch keeps the repository clean and does not remove the merged commit from `main`.
