---
title: Build Your Own Sly Director — 05 — Build GitHub MCP
summary: Build and connect the Sly Director GitHub MCP service using GitHub, AWS Lambda, WorkOS AuthKit Production, and Claude custom connectors.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-14
last_verified: 2026-09-14
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
src.app.handler
```

8. Save.

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

5. Deploy it:

```bash
aws lambda update-function-code \
  --function-name sly-director-github-mcp \
  --zip-file fileb://function.zip \
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

1. Stay on the WorkOS Dashboard for your `Overlord` team.
2. Press:

```text
Ctrl+K
```

On macOS, press:

```text
Command+K
```

3. In the command palette, type:

```text
Billing
```

4. Open the **Billing** result.
5. Find the **Payment information** card.
6. Add your payment method and billing information.
7. Save it.
8. Return to the main WorkOS Dashboard.
9. Use the environment selector near the top of the dashboard to switch to:

```text
Production
```

10. Keep **Production** selected for every remaining WorkOS step in this chapter.

A payment method is required to activate WorkOS Production. AuthKit username/password authentication is free below WorkOS's current free MAU threshold, but Production still requires billing information.

<details>
<summary>If Billing does not appear in Dashboard Search</summary>

Confirm you are signed into the `Overlord` team with an **Admin**, **Developer**, or **Sandbox Developer** role. WorkOS hides Billing from Support roles.

If you created the team yourself, you should normally be its Admin.

</details>

## Step 9 — Record the Production AuthKit domain

1. With **Production** selected, open the WorkOS **Overview**.
2. Find the **AuthKit domain**.
3. Copy the complete HTTPS URL.

It looks similar to:

```text
https://your-workspace.authkit.app
```

Use the WorkOS-provided domain. A custom domain is not required for Sly Director.

Record this value as:

```text
AUTHKIT_ISSUER
```

## Step 10 — Configure WorkOS for MCP clients

1. In the WorkOS Production environment, open:

```text
Connect → Configuration
```

2. Enable:

```text
Client ID Metadata Document (CIMD)
```

3. Also enable:

```text
Dynamic Client Registration (DCR)
```

CIMD is the current MCP client-registration mechanism. DCR remains enabled for compatibility with clients that still use the older registration path.

## Step 11 — Add the MCP Resource Indicator

Stay on **Connect → Configuration**.

1. Find **Resource Indicators**.
2. Add the exact `PUBLIC_MCP_URL` from Step 7.

Example:

```text
https://abc123.lambda-url.us-east-2.on.aws/mcp
```

3. Save it.
4. Open the `...` menu for that Resource Indicator.
5. Select:

```text
Set as default
```

The Resource Indicator must exactly match the MCP server's `resource` URL. WorkOS uses it as the access token's `aud` claim.

## Step 12 — Point Lambda at AuthKit Production

1. Return to AWS Lambda.
2. Open `sly-director-github-mcp`.
3. Open **Configuration → Environment variables → Edit**.
4. Set:

```text
AUTHKIT_ISSUER = the Production AuthKit domain from Step 9
```

Example:

```text
AUTHKIT_ISSUER = https://your-workspace.authkit.app
```

5. Confirm `PUBLIC_MCP_URL` still exactly matches the Resource Indicator from Step 11.
6. Save.

If old Cognito variables are still present, you may remove them now:

```text
COGNITO_REGION
COGNITO_USER_POOL_ID
COGNITO_APP_CLIENT_ID
```

## Step 13 — Verify the production endpoints before Claude

In CloudShell, run:

```bash
FUNCTION_URL=$(aws lambda get-function-url-config \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query FunctionUrl \
  --output text)

PUBLIC_MCP_URL=$(aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query 'Environment.Variables.PUBLIC_MCP_URL' \
  --output text)

AUTHKIT_ISSUER=$(aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query 'Environment.Variables.AUTHKIT_ISSUER' \
  --output text)

curl -i "${FUNCTION_URL}health"
echo
curl -i "${FUNCTION_URL}.well-known/oauth-protected-resource/mcp"
echo
curl -s "${AUTHKIT_ISSUER}/.well-known/oauth-authorization-server"
```

Check for all of these:

```text
health → HTTP 200
protected-resource metadata → HTTP 200 JSON
resource → exact PUBLIC_MCP_URL
authorization_servers → Production AUTHKIT_ISSUER
code_challenge_methods_supported → S256
grant_types_supported → authorization_code and refresh_token
```

Do not continue to Claude until these checks are correct.

## Step 14 — Add Sly Director GitHub to Claude

1. Open Claude.
2. Open **Customize → Connectors**.
3. Select **+ → Add custom connector**.
4. For the name, enter:

```text
Sly Director GitHub
```

5. Enter the exact remote MCP URL ending in `/mcp`.
6. Leave the optional **OAuth Client ID** and **OAuth Client Secret** advanced fields blank.
7. Select **Add**.
8. Select **Connect**.

Claude should discover the WorkOS AuthKit authorization server through the MCP metadata and register itself through CIMD/DCR.

## Step 15 — Complete the Production AuthKit login

1. Claude opens the WorkOS AuthKit hosted authentication page.
2. If this is the first user in the Production environment, use the available sign-up flow.
3. Create/sign in with your email and password.
4. Complete the WorkOS authorization/consent screen if it appears.
5. Return to Claude.

Email + Password authentication is enabled by default in AuthKit.

## Step 16 — Enable the connector in Sly Director

1. Open **Projects → Sly Director**.
2. Start a new chat.
3. Select **+ → Connectors**.
4. Enable:

```text
Sly Director GitHub
```

## Step 17 — Test repository reading

Send:

```text
Using the Sly Director GitHub connector, inspect the repository claude-director-test. List its files and read README.md and claude-test.txt. Tell me which GitHub tools you used.
```

Claude should return the repository contents through the custom connector.

## Step 18 — Test branch, file, pull request, Actions, and merge

Send this as one task:

```text
Using the Sly Director GitHub connector, perform this connection test on the repository claude-director-test.

1. Create a working branch named connection-test.
2. Create a file named sly-director-test.md containing:

# Sly Director GitHub MCP test
The Sly Director GitHub MCP connection is working.

3. Create .github/workflows/sly-director-connection-test.yml with this workflow:

name: Sly Director connection test

on:
  pull_request:
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Sly Director GitHub MCP is working"

4. Create a non-draft pull request into main.
5. Inspect the resulting GitHub Actions workflow run and jobs.
6. If validation succeeds, merge the pull request using squash merge.
7. Verify sly-director-test.md exists on main.
8. Report the final repository state.
```

## Step 19 — Verify the connector in Cowork

After the normal Claude test succeeds:

1. Open the **Sly Director** Project in Cowork.
2. Confirm **Sly Director GitHub** is enabled.
3. Ask Cowork to read `claude-director-test` and report the default branch and README contents.
4. Confirm the connector works without asking you to reconnect.

Continue to [Chapter 6 — Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).

<details>
<summary>Why Function URL authentication is NONE</summary>

The Lambda Function URL must be publicly reachable so Claude can discover OAuth metadata and reach the MCP transport.

The GitHub tools themselves remain protected by WorkOS AuthKit bearer-token validation inside the MCP application.

</details>

<details>
<summary>Why PUBLIC_MCP_URL must match the WorkOS Resource Indicator</summary>

WorkOS stamps the requested Resource Indicator into the access token's `aud` claim. The Lambda verifier requires that audience to equal `PUBLIC_MCP_URL` exactly.

A mismatch causes the MCP bearer token to be rejected.

</details>

<details>
<summary>Why CIMD and DCR are both enabled</summary>

Client ID Metadata Document is the current MCP mechanism for clients that have no pre-existing registration with the authorization server.

Dynamic Client Registration is retained for compatibility with MCP clients that still use the older registration flow.

</details>

<details>
<summary>Why Claude gets no manually entered OAuth client secret</summary>

AuthKit's MCP flow supports client discovery/registration. Claude's custom-connector OAuth Client ID and Client Secret fields are optional, so this guide leaves them blank and lets the MCP OAuth flow establish the client relationship.

</details>

<details>
<summary>Migrating from the earlier Cognito build</summary>

Keep the existing Lambda Function URL, GitHub token, Lambda role, and GitHub MCP tools.

After WorkOS AuthKit has passed both the normal Claude and Cowork tests, the old Cognito user pool is no longer part of Sly Director and can be removed separately.

</details>

<details>
<summary>GitHub token permissions</summary>

Start with access only to `claude-director-test`. After the full test succeeds, edit or replace the fine-grained token to add the real repositories Sly Director should operate.

</details>
