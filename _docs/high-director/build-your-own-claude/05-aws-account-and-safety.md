---
title: Build Your Own Sly Director — 05 — Build GitHub MCP
summary: Build and connect the Sly Director GitHub MCP service using GitHub, AWS Lambda, WorkOS AuthKit Production, and Claude custom connectors.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 85
permalink: /docs/high-director/build-your-own-claude/05-aws-account-and-safety/
---

# Chapter 5 — Build the Sly Director GitHub MCP Service

## Goal

Give Sly Director and Cowork direct GitHub tools for repository reads, file changes, branches, pull requests, merges, and GitHub Actions.

This guide uses **WorkOS AuthKit Production only**. It does not use a WorkOS staging or development environment.

```text
Sly Director / Cowork
        ↓
Claude custom connector
        ↓
WorkOS AuthKit Production OAuth
        ↓
AWS Lambda Function URL
        ↓
sly-director-github-mcp
        ↓
GitHub API
```

The deployable source is published under:

```text
assets/sly-director/github-mcp-source/
```

## Step 1 — Create the GitHub token

1. Open GitHub.
2. Select your profile picture.
3. Select **Settings**.
4. Select **Developer settings**.
5. Select **Personal access tokens → Fine-grained tokens**.
6. Select **Generate new token**.
7. For **Token name**, enter:

```text
Sly Director GitHub MCP
```

8. For the first build, choose a 90-day expiration.
9. Under **Repository access**, choose **Only select repositories**.
10. Select:

```text
claude-director-test
```

11. Set these repository permissions:

```text
Actions: Read and write
Contents: Read and write
Pull requests: Read and write
Secrets: Read and write
Variables: Read and write
Workflows: Read and write
```

12. Generate the token.
13. Copy it into a private temporary note.

## Step 2 — Create the Lambda function

1. Open the AWS console.
2. Confirm the region is:

```text
US East (Ohio) — us-east-2
```

3. Search for **Lambda**.
4. Open **Lambda**.
5. Select **Create function**.
6. Select **Author from scratch**.
7. For **Function name**, enter:

```text
sly-director-github-mcp
```

8. For **Runtime**, choose **Python 3.13**.
9. For **Architecture**, choose **x86_64**.
10. Use the option that creates a new basic Lambda execution role.
11. Select **Create function**.

If the function already exists from the earlier Cognito build, keep it and continue to Step 3.

## Step 3 — Set the Lambda runtime configuration

1. Open `sly-director-github-mcp`.
2. Open **Configuration → General configuration → Edit**.
3. Set **Memory** to:

```text
512 MB
```

4. Set **Timeout** to:

```text
30 seconds
```

5. Save.
6. Open **Code → Runtime settings → Edit**.
7. Set **Handler** to:

```text
src.lambda_entry.handler
```

8. Save.

The separate Lambda entrypoint creates a fresh stateless MCP Streamable HTTP app/session manager for each Lambda invocation so the MCP lifecycle starts correctly without attempting to reuse a single-use manager across warm invocations.

## Step 4 — Add the initial Lambda environment variables

Open **Configuration → Environment variables → Edit** and configure:

```text
GITHUB_OWNER = your GitHub username
GITHUB_TOKEN = your fine-grained GitHub token
PUBLIC_MCP_URL = https://placeholder.invalid/mcp
AUTHKIT_ISSUER = https://placeholder.invalid
DEFAULT_BASE_BRANCH = main
BRANCH_PREFIX = sly/
```

Save the variables.

If you are converting the earlier Cognito build, the old `COGNITO_*` variables are no longer used by the new package.

## Step 5 — Build and deploy the Lambda package

1. Open AWS **CloudShell**.
2. Wait for the `~ $` prompt.
3. Run:

```bash
cd ~
rm -rf eirepolitic.github.io
git clone https://github.com/eirepolitic/eirepolitic.github.io.git
cd eirepolitic.github.io/assets/sly-director/github-mcp-source
chmod +x build-package.sh
./build-package.sh
```

4. Wait for:

```text
Created: function.zip
```

5. Confirm the lifecycle-safe handler:

```bash
AWS_PAGER="" aws lambda update-function-configuration \
  --function-name sly-director-github-mcp \
  --handler src.lambda_entry.handler \
  --region us-east-2 \
  --query '{FunctionName:FunctionName,Handler:Handler,LastUpdateStatus:LastUpdateStatus}' \
  --output table \
  --no-cli-pager
```

6. Wait for the configuration update:

```bash
aws lambda wait function-updated \
  --function-name sly-director-github-mcp \
  --region us-east-2
```

7. Deploy the package without printing Lambda environment-variable secrets:

```bash
AWS_PAGER="" aws lambda update-function-code \
  --function-name sly-director-github-mcp \
  --zip-file fileb://function.zip \
  --region us-east-2 \
  --query '{FunctionName:FunctionName,LastUpdateStatus:LastUpdateStatus,LastModified:LastModified}' \
  --output table \
  --no-cli-pager
```

8. Wait for the code update:

```bash
aws lambda wait function-updated \
  --function-name sly-director-github-mcp \
  --region us-east-2
```

## Step 6 — Create or confirm the Lambda Function URL

1. Return to **Lambda → sly-director-github-mcp**.
2. Open **Configuration → Function URL**.
3. If no Function URL exists, select **Create function URL**.
4. Set **Auth type** to:

```text
NONE
```

5. Leave CORS unconfigured.
6. Save.
7. Copy the Function URL.

It looks similar to:

```text
https://abc123.lambda-url.us-east-2.on.aws/
```

Your MCP URL is the Function URL plus `/mcp`:

```text
https://abc123.lambda-url.us-east-2.on.aws/mcp
```

Record both values.

## Step 7 — Set the real MCP URL in Lambda

1. Open **Configuration → Environment variables → Edit**.
2. Replace `PUBLIC_MCP_URL` with the exact Lambda URL ending in `/mcp`.
3. Save.

Do not change `AUTHKIT_ISSUER` yet. WorkOS supplies that in a later step.

## Step 8 — Activate WorkOS Production

If you are on the WorkOS **Get started** screen and there is no **Settings** item in the left sidebar, use Dashboard Search instead.

1. Stay on the WorkOS Dashboard for your team.
2. Press **Ctrl+K** (or **Command+K** on macOS).
3. Type `Billing`.
4. Open the **Billing** result.
5. Find **Payment information**.
6. Add your payment method and billing information.
7. Save it.
8. Return to the main WorkOS Dashboard.
9. Use the environment selector near the top of the dashboard to switch to **Production**.
10. Keep **Production** selected for every remaining WorkOS step in this chapter.

## Step 9 — Record the Production AuthKit domain

1. With **Production** selected, open the WorkOS **Overview**.
2. Find the **AuthKit domain**.
3. Copy the complete HTTPS URL.
4. Record it as `AUTHKIT_ISSUER` without a trailing slash.

## Step 10 — Configure WorkOS for MCP clients

1. In WorkOS Production, open **Connect → Configuration**.
2. In the **MCP Auth** card, click **Enable**.
3. Select both:

```text
Dynamic Client Registration
Client ID Metadata Document
```

4. Click **Save changes**.
5. Leave **External Sign-in URI** unconfigured.

## Step 11 — Add the MCP Resource Indicator

1. In **MCP resource indicators**, click **Edit MCP resources**.
2. Add the exact `PUBLIC_MCP_URL` ending in `/mcp`.
3. Save it.
4. Use its `...` menu and choose **Set as default**.

## Step 12 — Configure the first Production AuthKit user

1. Press **Ctrl+K** in WorkOS Production.
2. Search for **Authentication**.
3. Open the **Authentication** page.
4. Confirm **Email + Password** is enabled.
5. Confirm **Sign up** is enabled.
6. Save any changes.

The WorkOS dashboard account used to administer the project is separate from the AuthKit application user that signs into the MCP OAuth flow.

## Step 13 — Point Lambda at AuthKit Production

1. Return to AWS Lambda.
2. Open `sly-director-github-mcp`.
3. Open **Configuration → Environment variables → Edit**.
4. Set `AUTHKIT_ISSUER` to the Production AuthKit domain.
5. Confirm `PUBLIC_MCP_URL` exactly matches the WorkOS Resource Indicator.
6. Save.

## Step 14 — Verify the production endpoints before Claude

In CloudShell, retrieve only the non-secret values and test the endpoints. Avoid commands that print the full Lambda configuration/environment.

```bash
FUNCTION_URL=$(aws lambda get-function-url-config \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query FunctionUrl \
  --output text \
  --no-cli-pager)

PUBLIC_MCP_URL=$(aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query 'Environment.Variables.PUBLIC_MCP_URL' \
  --output text \
  --no-cli-pager)

AUTHKIT_ISSUER=$(aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query 'Environment.Variables.AUTHKIT_ISSUER' \
  --output text \
  --no-cli-pager)

curl -sS "${FUNCTION_URL}health" | jq
curl -sS "${FUNCTION_URL}.well-known/oauth-protected-resource/mcp" | jq
curl -sS "${AUTHKIT_ISSUER}/.well-known/oauth-authorization-server" | jq
curl -sS "${AUTHKIT_ISSUER}/oauth2/jwks" | jq '{key_count:(.keys | length)}'
```

Confirm health is OK, MCP metadata points to the exact resource/issuer, AuthKit supports `S256`, `authorization_code`, and `refresh_token`, and JWKS contains at least one key.

## Step 15 — Add Sly Director GitHub to Claude

1. Open **Claude → Customize → Connectors**.
2. Add a custom connector named **Sly Director GitHub**.
3. Enter the exact remote MCP URL ending in `/mcp`.
4. Under **Authentication**, use **Sign in now** when Claude detects OAuth.
5. Under **OAuth client**, use **Use Claude's published identity** when Claude detects CIMD.
6. Leave **Request headers** empty.
7. Leave **Advanced** unchanged.
8. Save/add the connector and complete the WorkOS AuthKit sign-in flow.

Use **Register automatically** only as the DCR fallback if the detected CIMD path fails.

## Step 16 — Enable the connector in Sly Director

1. Open **Projects → Sly Director**.
2. Start a new chat.
3. Select **+ → Connectors**.
4. Enable **Sly Director GitHub**.

## Step 17 — Test repository reading

Send:

```text
Using the Sly Director GitHub connector, inspect the repository claude-director-test. List its files and read README.md and claude-test.txt. Tell me which GitHub tools you used.
```

Claude may report that connector tools are deferred and that it first ran a tool search to load the GitHub tool definitions. That is normal. The read test passes when Claude can list the repository tree and read both files through the connector.

## Step 18 — Test branch, file, pull request, Actions, and merge

Send this as one task:

```text
Using the Sly Director GitHub connector, perform this end-to-end write test on the repository claude-director-test.

1. Create a working branch named connection-test.
2. Create sly-director-test.md containing:

# Sly Director GitHub MCP test
The Sly Director GitHub MCP connection is working.

3. Create .github/workflows/sly-director-connection-test.yml with a pull_request/workflow_dispatch workflow that echoes "Sly Director GitHub MCP is working".
4. Create a non-draft pull request into main.
5. Inspect the resulting GitHub Actions workflow run and jobs.
6. If validation succeeds, squash-merge the pull request.
7. Verify sly-director-test.md exists on main.
8. Report the branch, files, PR number, workflow result, merge result, final verification, and GitHub tools used.

Do not stop for approval between these steps unless a genuine permission or validation failure requires my decision.
```

## Step 19 — Verify the connector in Cowork

After the normal Claude write test succeeds:

1. Open the **Sly Director** Project in Cowork.
2. Confirm **Sly Director GitHub** is enabled.
3. Ask Cowork to read `claude-director-test` and report the default branch and README contents.
4. Confirm the connector works without asking you to reconnect.

Continue to [Chapter 6 — Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).

<details>
<summary>Why Function URL authentication is NONE</summary>

The Lambda Function URL must be publicly reachable so Claude can discover OAuth metadata and reach the MCP transport. The GitHub tools themselves remain protected by WorkOS AuthKit bearer-token validation inside the MCP application.

</details>

<details>
<summary>Why the Lambda handler is src.lambda_entry.handler</summary>

The MCP Streamable HTTP session manager must run inside ASGI lifespan and is single-use. AWS Lambda can reuse a Python execution environment across invocations. The separate entrypoint creates a fresh stateless MCP app/session manager for each invocation, which avoids both an uninitialized task group and attempts to restart a previously used manager.

</details>

<details>
<summary>Why PUBLIC_MCP_URL must match the WorkOS Resource Indicator</summary>

WorkOS stamps the requested Resource Indicator into the access token's `aud` claim. The Lambda verifier requires that audience to equal `PUBLIC_MCP_URL` exactly.

</details>

<details>
<summary>Why CIMD and DCR are both enabled</summary>

CIMD is the preferred current MCP registration mechanism. DCR remains enabled as a compatibility fallback.

</details>
