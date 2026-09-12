---
title: Build Your Own Sly Director — 10 — Maintenance
summary: Maintain Sly Director, Cowork, the custom GitHub connector, AWS MCP, schedules, access, and costs.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 90
permalink: /docs/high-director/build-your-own-claude/10-maintenance/
---

# Chapter 10 — Maintenance

## Goal

Keep Sly Director, Cowork, its connectors, credentials, schedules, access, and AWS costs working as intended.

## Complete this step

Once a month:

1. Open **Projects → Sly Director** and confirm the current instructions are saved.
2. Open the **Sly Director** Cowork Project and confirm it still has the intended context/instructions.
3. Confirm **Sly Director GitHub** and **AWS MCP** are connected.
4. Run one harmless GitHub read and one harmless AWS query.
5. Open the Sly Director GitHub Lambda health URL and confirm it returns `"ok": true`.
6. Review recent Cowork tasks for recurring failures or unnecessary interruptions.
7. Review every scheduled Cowork task.
8. Pause or remove scheduled tasks you no longer want.
9. Review the GitHub fine-grained token's repository access and expiration date.
10. Review open branches, pull requests, and GitHub Actions failures from recent work.
11. Open **AWS → Billing and Cost Management** and review charges and the Sly Director budget.
12. Check for AWS resources from old tests that are still running.
13. Review any Sly Director Skills or Plugins and remove obsolete ones.

## When the GitHub token is nearing expiration

1. Open GitHub **Settings → Developer settings → Personal access tokens → Fine-grained tokens**.
2. Create a replacement token with the same intended repositories and permissions.
3. Open **AWS → Lambda → sly-director-github-mcp → Configuration → Environment variables**.
4. Replace `GITHUB_TOKEN` with the new token.
5. Save the Lambda configuration.
6. Test a harmless repository read through **Sly Director GitHub**.
7. Revoke the old token in GitHub after the new token works.

## What you should see

```text
Sly Director Project: working
Cowork autonomous execution: working
Sly Director GitHub: working
AWS MCP: working
GitHub token: valid and intentionally scoped
scheduled tasks: intentional
AWS cost: understood
```

The core guide is complete.

<details>
<summary>What to learn from Cowork interruptions</summary>

If Cowork repeatedly stops for the same unnecessary question, improve the Sly Director instructions, future Operator Skill, connector permissions, validation, or task instructions rather than accepting the interruption as normal.

</details>

<details>
<summary>Cognito maintenance</summary>

The Cognito app client exists so Claude can authenticate to the Sly Director GitHub MCP service. If you deliberately replace the Cognito app client, update both the Lambda `COGNITO_APP_CLIENT_ID` value and the Claude custom connector's Client ID/secret.

Changing Cognito unnecessarily creates more moving parts, so leave it alone while it is working.

</details>
