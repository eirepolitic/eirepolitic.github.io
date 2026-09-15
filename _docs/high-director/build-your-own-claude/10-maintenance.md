---
title: Build Your Own Sly Director — 10 — Maintenance
summary: Keep the working Sly Director setup healthy with a few simple checks.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 90
permalink: /docs/high-director/build-your-own-claude/10-maintenance/
---

# Chapter 10 — Maintain Sly Director

The finished setup needs very little routine maintenance.

## Replace the GitHub token before it expires

The fine-grained GitHub token created in Chapter 5 may have an expiration date.

Before it expires:

1. GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens**.
2. Create a replacement token with the same repository access and permissions.
3. AWS → **Lambda → sly-director-github-mcp → Configuration → Environment variables → Edit**.
4. Replace only:

```text
GITHUB_TOKEN
```

5. Save.
6. Re-test a simple repository read in Claude.
7. Revoke the old token after the new one works.

Never paste the token into chat or documentation.

## Reconnect a connector if authorization expires

If Claude shows either connector as disconnected:

1. Open **Claude → Customize → Connectors**.
2. Find the disconnected connector.
3. Select **Connect**.
4. Complete the sign-in flow again.

For AWS MCP, sign in as:

```text
sly-director-admin
```

not the root account.

## Keep the Lambda package current

Only redeploy the connector when this guide or the published connector source changes.

Use the Chapter 5 CloudShell deployment steps. Do not manually edit the Lambda code in the AWS browser editor.

After deploying, confirm:

```text
State: Active
Handler: src.lambda_entry.handler
LastUpdateStatus: Successful
```

## Periodically test the two connectors

A simple check is enough.

For GitHub:

```text
Using Sly Director GitHub, list the files in claude-director-test. Do not make changes.
```

For AWS:

```text
Using AWS MCP, report the current AWS identity and the state of sly-director-github-mcp in us-east-2. Do not make changes.
```

## Keep test repositories separate from real work

Keep `claude-director-test` as a safe place to test connector changes before giving new behavior access to important repositories.

When you are ready to use Sly Director on another GitHub repository, add that repository to the fine-grained GitHub token's repository access first.

## Finished

At this point the core Sly Director setup is complete:

```text
Claude Project: Sly Director
GitHub connector: working
AWS MCP: working
Cowork autonomy: verified
```

Use [Chapter 8 — Daily Operation]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }}) as the normal starting point after setup.
