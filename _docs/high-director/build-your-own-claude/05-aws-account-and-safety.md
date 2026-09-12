---
title: Build Your Own Sly Director — 05 — Prepare AWS
summary: Prepare AWS for Sly Director's AWS MCP connection.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 85
permalink: /docs/high-director/build-your-own-claude/05-aws-account-and-safety/
---

# Chapter 5 — Prepare AWS

## Goal

Prepare the AWS account Sly Director will operate.

## Complete this step

1. Open the [AWS Management Console](https://console.aws.amazon.com/).
2. Sign in to the AWS account you want Sly Director to use.
3. For the simplest setup, use the **root user**.
4. Set the preferred workload region to:

```text
US East (Ohio) — us-east-2
```

5. Open **Billing and Cost Management → Budgets**.
6. Create a simple monthly-cost or zero-spend budget.
7. If you already created `claude-high-director-budget`, keep it. Otherwise use any clear name you prefer.
8. Leave this AWS session open for Chapter 6.

## What you should see

```text
AWS account: signed in
Preferred workload region: us-east-2
Budget alert: created
```

Continue to [Chapter 6 — Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).

<details>
<summary>Optional IAM-role setup</summary>

If you prefer a separate IAM role instead of root, keep using the existing optional `ClaudeHighDirectorRole` procedure/resource if you already created it. Its technical name does not need to change just because the product is now called Sly Director.

</details>
