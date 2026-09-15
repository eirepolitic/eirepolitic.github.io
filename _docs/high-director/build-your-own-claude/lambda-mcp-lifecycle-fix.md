---
title: Sly Director — Lambda MCP Lifecycle Fix
summary: Use a fresh MCP Streamable HTTP session manager for every AWS Lambda invocation.
section: high-director
doc_type: runbook
status: active
created: 2026-09-15
updated: 2026-09-15
last_verified: 2026-09-15
order: 89
permalink: /docs/high-director/build-your-own-claude/lambda-mcp-lifecycle-fix/
---

# Lambda MCP Lifecycle Fix

## When this applies

Use this fix if Claude successfully completes WorkOS AuthKit authorization but then reports that **Sly Director GitHub returned an error when connecting**, and the Lambda logs contain:

```text
RuntimeError: Task group is not initialized. Make sure to use run().
```

## Cause

The MCP Python SDK's Streamable HTTP session manager must run inside the ASGI app lifespan. The manager is also single-use: after its lifespan exits, that same manager instance cannot be started again.

AWS Lambda can reuse a Python execution environment between invocations. Therefore neither of these patterns is correct:

```text
one global MCP app + lifespan off
→ session manager never starts
```

```text
one global MCP app + lifespan on
→ warm invocation tries to restart the same single-use manager
```

Sly Director instead uses a fresh Streamable HTTP app and manager for each Lambda invocation.

## Correct Lambda handler

The Lambda runtime handler must be:

```text
src.lambda_entry.handler
```

The entrypoint creates a fresh MCP app for the invocation and runs it through Mangum with lifespan enabled.

## Redeploy

Open AWS CloudShell and run:

```bash
cd ~
rm -rf eirepolitic.github.io
git clone https://github.com/eirepolitic/eirepolitic.github.io.git
cd eirepolitic.github.io/assets/sly-director/github-mcp-source
chmod +x build-package.sh
./build-package.sh
```

Then update the Lambda runtime handler:

```bash
AWS_PAGER="" aws lambda update-function-configuration \
  --function-name sly-director-github-mcp \
  --handler src.lambda_entry.handler \
  --region us-east-2 \
  --query '{FunctionName:FunctionName,Handler:Handler,LastUpdateStatus:LastUpdateStatus}' \
  --output table \
  --no-cli-pager
```

Wait for that configuration update to complete:

```bash
aws lambda wait function-updated \
  --function-name sly-director-github-mcp \
  --region us-east-2
```

Deploy the new package:

```bash
AWS_PAGER="" aws lambda update-function-code \
  --function-name sly-director-github-mcp \
  --zip-file fileb://function.zip \
  --region us-east-2 \
  --query '{FunctionName:FunctionName,LastUpdateStatus:LastUpdateStatus,LastModified:LastModified}' \
  --output table \
  --no-cli-pager
```

Wait again:

```bash
aws lambda wait function-updated \
  --function-name sly-director-github-mcp \
  --region us-east-2
```

Verify the handler and deployment state without printing environment variables:

```bash
AWS_PAGER="" aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query '{State:State,Handler:Handler,LastUpdateStatus:LastUpdateStatus,Reason:LastUpdateStatusReason}' \
  --output table \
  --no-cli-pager
```

Expected values:

```text
State             Active
Handler           src.lambda_entry.handler
LastUpdateStatus  Successful
```

## Retry Claude

After deployment succeeds:

1. Return to Claude.
2. Open **Sly Director GitHub**.
3. Select **Connect** again.
4. Complete AuthKit authorization if Claude asks for it again.

If the connector still fails, immediately inspect only the recent Lambda errors:

```bash
aws logs tail /aws/lambda/sly-director-github-mcp \
  --since 5m \
  --region us-east-2 \
  --format short \
  --no-cli-pager
```
