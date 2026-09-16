---
title: Build Your Own Sly Director — 05 — Build the GitHub Connector
summary: Build the live-verified Sly Director GitHub connector with AWS Lambda and WorkOS AuthKit.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-15
last_verified: 2026-09-15
order: 85
permalink: /docs/high-director/build-your-own-claude/05-aws-account-and-safety/
---

# Chapter 5 — Build the Sly Director GitHub Connector

## Goal

Give Claude tools that can read and change GitHub repositories, create branches and pull requests, inspect GitHub Actions, and merge validated work.

The connector is a small program that runs in AWS Lambda. WorkOS AuthKit protects it with a sign-in page.

```text
Claude
→ WorkOS AuthKit sign-in
→ AWS Lambda connector
→ GitHub
```

## Step 1 — Create a GitHub token

The connector needs a GitHub token so it can act on your repositories.

1. Open GitHub.
2. Select your profile picture → **Settings**.
3. Select **Developer settings**.
4. Select **Personal access tokens → Fine-grained tokens**.
5. Select **Generate new token**.
6. For **Token name**, enter:

```text
Sly Director GitHub MCP
```

7. Choose a 90-day expiration for the first build.
8. Under **Repository access**, choose **All repositories**.
9. Give the token these repository permissions:

```text
Actions: Read and write
Contents: Read and write
Pull requests: Read and write
Secrets: Read and write
Variables: Read and write
Workflows: Read and write
```

10. Generate the token.
11. Copy it to a private temporary note. You will paste it into AWS once.

Using **All repositories** from the start lets Sly Director work on your existing repositories and repositories you create later without editing the token each time.

Do not paste this token into Claude, ChatGPT, GitHub issues, or documentation.

## Step 2 — Create the Lambda function

1. Open AWS while signed in as `sly-director-admin`.
2. Confirm the region is **US East (Ohio) — us-east-2**.
3. Search for **Lambda** and open it.
4. Select **Create function**.
5. Select **Author from scratch**.
6. For **Function name**, enter:

```text
sly-director-github-mcp
```

7. Runtime: **Python 3.13**.
8. Architecture: **x86_64**.
9. Keep the option to create a new basic Lambda execution role.
10. Select **Create function**.

## Step 3 — Set the Lambda runtime

1. Open **Configuration → General configuration → Edit**.
2. Set **Memory** to `512 MB`.
3. Set **Timeout** to `30 seconds`.
4. Save.
5. Open **Code → Runtime settings → Edit**.
6. Set **Handler** to:

```text
src.lambda_entry.handler
```

7. Save.

## Step 4 — Add the first environment variables

Environment variables are settings the connector reads when it starts.

1. Open **Configuration → Environment variables → Edit**.
2. Add:

```text
GITHUB_OWNER = your GitHub username
GITHUB_TOKEN = your fine-grained GitHub token
PUBLIC_MCP_URL = https://placeholder.invalid/mcp
AUTHKIT_ISSUER = https://placeholder.invalid
DEFAULT_BASE_BRANCH = main
BRANCH_PREFIX = sly/
```

3. Select **Save**.

`BRANCH_PREFIX=sly/` means a requested branch such as `connection-test` will be created as `sly/connection-test`.

## Step 5 — Deploy the connector code

AWS CloudShell is a command window inside AWS. You will only copy and paste the commands shown here.

1. Open **CloudShell** from the AWS top bar.
2. Wait for the `~ $` prompt.
3. Paste:

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

5. Paste:

```bash
AWS_PAGER="" aws lambda update-function-configuration \
  --function-name sly-director-github-mcp \
  --handler src.lambda_entry.handler \
  --region us-east-2 \
  --query '{FunctionName:FunctionName,Handler:Handler,LastUpdateStatus:LastUpdateStatus}' \
  --output table \
  --no-cli-pager
```

6. Wait for the update:

```bash
aws lambda wait function-updated \
  --function-name sly-director-github-mcp \
  --region us-east-2
```

7. Deploy the code:

```bash
AWS_PAGER="" aws lambda update-function-code \
  --function-name sly-director-github-mcp \
  --zip-file fileb://function.zip \
  --region us-east-2 \
  --query '{FunctionName:FunctionName,LastUpdateStatus:LastUpdateStatus,LastModified:LastModified}' \
  --output table \
  --no-cli-pager
```

8. Wait again:

```bash
aws lambda wait function-updated \
  --function-name sly-director-github-mcp \
  --region us-east-2
```

These commands deliberately hide Lambda environment-variable values so your GitHub token is not printed in CloudShell.

## Step 6 — Create the Lambda Function URL

1. Return to **Lambda → sly-director-github-mcp**.
2. Open **Configuration → Function URL**.
3. Select **Create function URL**.
4. Set **Auth type** to:

```text
NONE
```

5. Leave CORS unconfigured.
6. Save.
7. Copy the Function URL. It looks like:

```text
https://abc123.lambda-url.us-east-2.on.aws/
```

Your MCP URL is that URL plus `/mcp`:

```text
https://abc123.lambda-url.us-east-2.on.aws/mcp
```

The Function URL must be publicly reachable so Claude can discover the OAuth sign-in information. The `/mcp` endpoint itself will be protected by AuthKit.

## Step 7 — Save the real MCP URL

1. Open **Configuration → Environment variables → Edit**.
2. Replace `PUBLIC_MCP_URL` with your exact Function URL ending in `/mcp`.
3. Save.

## Step 8 — Prepare WorkOS Production

1. Open WorkOS.
2. Use the environment selector near the top of the Dashboard.
3. Switch to **Production**.
4. If Production asks for billing information before it can be activated, press **Ctrl+K** (or **Command+K** on macOS), search for **Billing**, add the required payment information, then return and select **Production** again.
5. Keep **Production** selected for the rest of this chapter.

## Step 9 — Find the AuthKit domain

1. In WorkOS Production, press **Ctrl+K** (or **Command+K** on macOS).
2. Type:

```text
Domains
```

3. Open the **Domains** result.
4. Find the AuthKit domain for the Production environment.
5. Copy the complete HTTPS domain.
6. Record it without a trailing slash, for example:

```text
https://example.authkit.app
```

This is the sign-in service Claude will use before it can call your connector.

## Step 10 — Configure WorkOS for MCP

1. In WorkOS Production, open **Connect → Configuration**.
2. In the **MCP Auth** card, select **Enable**.
3. Turn on both:

```text
Dynamic Client Registration
Client ID Metadata Document
```

4. Select **Save changes**.
5. Leave **External Sign-in URI** unconfigured.

CIMD is the current preferred way Claude identifies itself. DCR remains enabled as a compatibility fallback.

## Step 11 — Add the MCP Resource Indicator

1. In **MCP resource indicators**, select **Edit MCP resources**.
2. Add your exact `PUBLIC_MCP_URL` ending in `/mcp`.
3. Save it.
4. Open its `...` menu.
5. Select **Set as default**.

This tells WorkOS which connector the login token is meant for.

## Step 12 — Enable a normal AuthKit login

1. Press **Ctrl+K** in WorkOS Production.
2. Search for **Authentication**.
3. Open the **Authentication** page.
4. Make sure **Email + Password** is enabled.
5. Make sure **Sign up** is enabled.
6. Save any changes.

Your WorkOS Dashboard login and your AuthKit application login are separate. The first time Claude connects, you may need to create an AuthKit user through this sign-up flow.

## Step 13 — Point Lambda at WorkOS

1. Return to AWS Lambda.
2. Open `sly-director-github-mcp`.
3. Open **Configuration → Environment variables → Edit**.
4. Replace `AUTHKIT_ISSUER` with the Production AuthKit domain you copied.
5. Confirm `PUBLIC_MCP_URL` is still the exact Lambda URL ending in `/mcp`.
6. Save.

## Step 14 — Verify the connector before Claude

Open CloudShell and run:

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

You want:

- health shows `"ok": true`;
- the MCP resource is your exact `/mcp` URL;
- AuthKit supports `S256`, `authorization_code`, and `refresh_token`;
- JWKS shows at least one key.

## Step 15 — Add the connector to Claude

1. Open **Claude → Customize → Connectors**.
2. Select **Add custom connector**.
3. Name it:

```text
Sly Director GitHub
```

4. Enter your exact MCP URL ending in `/mcp`.
5. When Claude detects OAuth, choose:

```text
Authentication → Sign in now
OAuth client → Use Claude's published identity
```

6. Leave **Request headers** empty.
7. Leave **Advanced** unchanged.
8. Save/add the connector.
9. Select **Connect**.
10. Complete the WorkOS AuthKit sign-up/sign-in flow.

If Claude's published identity is not available, use **Register automatically** as the fallback.

## Step 16 — Test GitHub reading

1. Open **Projects → Sly Director**.
2. Start a normal chat.
3. Enable **Sly Director GitHub** from the `+` connector menu.
4. Send:

```text
Using the Sly Director GitHub connector, inspect the repository claude-director-test. List its files and read README.md and claude-test.txt. Tell me which GitHub tools you used.
```

A short delay while Claude loads deferred connector tools is normal.

## Step 17 — Test the full GitHub workflow

Send:

```text
Using the Sly Director GitHub connector, perform an end-to-end write test on claude-director-test.

Create a working branch, add a small test file and a simple GitHub Actions workflow, create a non-draft pull request into main, inspect the workflow run and jobs, correct recoverable failures if needed, squash-merge after validation succeeds, and verify the test file exists on main.

Do not stop for approval between these steps unless a genuine blocker requires my decision. Report the branch, files, PR number, workflow result, merge result, final verification, and GitHub tools used.
```

The connector will automatically prefix new branches with `sly/`.

When this succeeds, the GitHub connector is ready.

Continue to [Chapter 6 — Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).
