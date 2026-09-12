---
title: Build Your Own Sly Director — 05 — Build GitHub MCP
summary: Build and connect the complete Sly Director GitHub MCP service using GitHub, Amazon Cognito, AWS Lambda, and Claude custom connectors.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 85
permalink: /docs/high-director/build-your-own-claude/05-aws-account-and-safety/
---

# Chapter 5 — Build the Sly Director GitHub MCP Service

## Goal

Give Sly Director and Cowork direct GitHub tools for reading repositories, changing files, branches, pull requests, merges, and GitHub Actions.

You will build:

```text
Sly Director / Cowork
        ↓
Claude custom connector
        ↓
Cognito OAuth login
        ↓
AWS Lambda Function URL
        ↓
sly-director-github-mcp
        ↓
GitHub API
```

The source code used by this chapter is published in:

```text
assets/sly-director/github-mcp-source/
```

## Step 1 — Create the GitHub token

1. Open [GitHub](https://github.com/).
2. Select your profile picture in the upper-right corner.
3. Select **Settings**.
4. In the left navigation, select **Developer settings**.
5. Select **Personal access tokens**.
6. Select **Fine-grained tokens**.
7. Select **Generate new token**.
8. For **Token name**, enter:

```text
Sly Director GitHub MCP
```

9. Choose an expiration period. For the first build, choose **90 days**.
10. Under **Resource owner**, select your GitHub account.
11. Under **Repository access**, choose **Only select repositories**.
12. Select:

```text
claude-director-test
```

13. Under **Repository permissions**, set:

```text
Actions: Read and write
Contents: Read and write
Pull requests: Read and write
Secrets: Read and write
Variables: Read and write
Workflows: Read and write
```

14. Select **Generate token**.
15. Copy the token immediately.
16. Put it temporarily in a private note. You will paste it into AWS once and then remove it from that note.

## Step 2 — Create the Cognito login

1. Return to the AWS console.
2. Confirm the region is:

```text
US East (Ohio) — us-east-2
```

3. Search for **Cognito**.
4. Open **Amazon Cognito**.
5. Open **User pools**.
6. Select **Create user pool** or **Create application**, depending on the current console wording.
7. For **Application type**, select:

```text
Traditional web application
```

8. For the application name, enter:

```text
SlyDirectorClaude
```

9. Use **Email** as the sign-in identifier.
10. For the return/callback URL, enter exactly:

```text
https://claude.ai/api/mcp/auth_callback
```

11. Create the application/user pool.
12. Open the new user pool.
13. Record the **User pool ID** in your private setup note.
14. Open **Applications → App clients**.
15. Open **SlyDirectorClaude**.
16. Record the **Client ID**.
17. Find **Client secret** and select **Show client secret**.
18. Record the **Client secret** in your private setup note.
19. In the app client's managed-login/OAuth settings, confirm:

```text
OAuth flow: Authorization code grant
Allowed scope: openid
Callback URL: https://claude.ai/api/mcp/auth_callback
```

20. Save any changes.

## Step 3 — Create the Cognito web domain

1. Inside the same Cognito user pool, open **Branding → Domain**.
2. Select **Actions → Create Cognito domain**.
3. Enter a unique domain prefix. For example:

```text
sly-director-yourname
```

4. Use the available AWS-hosted login branding option.
5. Create the domain.
6. Record the resulting Cognito domain in your private setup note.

## Step 4 — Create your Cognito user

1. In the Cognito user pool, open **Users**.
2. Select **Create user**.
3. Enter the email address you want to use when Claude asks you to sign in.
4. Create the user with a temporary password.
5. Record the temporary password privately.

You will be asked to replace it with your own password during the first browser sign-in.

## Step 5 — Create the Lambda function

1. In the AWS search box, enter **Lambda**.
2. Open **Lambda**.
3. Select **Create function**.
4. Select **Author from scratch**.
5. For **Function name**, enter:

```text
sly-director-github-mcp
```

6. For **Runtime**, select:

```text
Python 3.13
```

7. For **Architecture**, select:

```text
x86_64
```

8. Under permissions, use the option that creates a new basic Lambda execution role.
9. Select **Create function**.

## Step 6 — Set the Lambda runtime configuration

1. Open the new `sly-director-github-mcp` function.
2. Open **Configuration → General configuration**.
3. Select **Edit**.
4. Set **Memory** to:

```text
512 MB
```

5. Set **Timeout** to:

```text
30 seconds
```

6. Save.
7. Open **Code → Runtime settings**.
8. Select **Edit**.
9. Set **Handler** to:

```text
src.app.handler
```

10. Save.

## Step 7 — Add the Lambda environment variables

1. Open **Configuration → Environment variables**.
2. Select **Edit**.
3. Add these values:

```text
GITHUB_OWNER = your GitHub username
GITHUB_TOKEN = the fine-grained token from Step 1
COGNITO_REGION = us-east-2
COGNITO_USER_POOL_ID = your Cognito User pool ID
COGNITO_APP_CLIENT_ID = your Cognito Client ID
PUBLIC_MCP_URL = https://placeholder.invalid/mcp
DEFAULT_BASE_BRANCH = main
BRANCH_PREFIX = sly/
```

4. Select **Save**.

The placeholder URL is temporary. You replace it after AWS creates the real Function URL.

## Step 8 — Build the deployment zip in CloudShell

1. Select the **CloudShell** icon in the AWS top navigation.
2. Wait until the terminal prompt appears.
3. Copy and paste this entire block:

```bash
rm -rf eirepolitic.github.io
git clone https://github.com/eirepolitic/eirepolitic.github.io.git
cd eirepolitic.github.io/assets/sly-director/github-mcp-source
chmod +x build-package.sh
./build-package.sh
```

4. Press **Enter**.
5. Wait until the last lines show:

```text
Created: function.zip
```

6. Then paste:

```bash
aws lambda update-function-code \
  --function-name sly-director-github-mcp \
  --zip-file fileb://function.zip \
  --region us-east-2
```

7. Press **Enter**.
8. The command should return JSON describing the updated Lambda function.

## Step 9 — Create the Function URL

1. Return to the Lambda browser tab.
2. Open `sly-director-github-mcp`.
3. Open **Configuration → Function URL**.
4. Select **Create function URL**.
5. For **Auth type**, select:

```text
NONE
```

6. Leave CORS disabled/unconfigured.
7. Select **Save**.
8. Copy the generated **Function URL**.

It looks similar to:

```text
https://abc123example.lambda-url.us-east-2.on.aws/
```

9. Add `mcp` to the end and record the complete MCP URL:

```text
https://abc123example.lambda-url.us-east-2.on.aws/mcp
```

The Function URL itself is public so Claude can reach the OAuth discovery and MCP endpoints. The MCP tools remain protected by Cognito OAuth inside the application.

## Step 10 — Replace the placeholder MCP URL

1. In the Lambda function, open **Configuration → Environment variables**.
2. Select **Edit**.
3. Replace `PUBLIC_MCP_URL` with the complete URL from Step 9, including `/mcp`.
4. Select **Save**.
5. Wait until Lambda shows the configuration update as complete.

## Step 11 — Check the Lambda health page

1. Copy the Function URL without `/mcp`.
2. Add:

```text
health
```

Example:

```text
https://abc123example.lambda-url.us-east-2.on.aws/health
```

3. Open it in a browser tab.

You should see JSON similar to:

```json
{
  "ok": true,
  "service": "sly-director-github-mcp",
  "owner": "your-github-username"
}
```

## Step 12 — Add the custom connector to Claude

1. Open [Claude](https://claude.ai/).
2. Open **Customize → Connectors**.
3. Select **+ → Add custom connector**.
4. For the connector name, enter:

```text
Sly Director GitHub
```

5. For the remote MCP URL, enter the complete URL ending in `/mcp`.
6. On the authentication screen, select:

```text
Authentication type: OAuth
OAuth client: Use your own OAuth client
```

7. Enter the **Cognito Client ID** from Step 2.
8. Enter the **Cognito Client secret** from Step 2.
9. Select **Add** or **Save**.
10. Select **Connect** when Claude offers the connection.
11. Cognito should open in the browser.
12. Sign in with the Cognito user from Step 4.
13. If Cognito asks you to replace the temporary password, create your permanent password.
14. Complete the authorization flow and return to Claude.

## Step 13 — Enable the connector in Sly Director

1. Open **Projects → Sly Director**.
2. Start a new chat.
3. Select **+ → Connectors**.
4. Enable:

```text
Sly Director GitHub
```

## Step 14 — Test repository reading

Send:

```text
Using the Sly Director GitHub connector, inspect the repository claude-director-test. List its files and read README.md and claude-test.txt. Tell me which GitHub tools you used.
```

Claude should return the repository contents without asking you to open Claude Code.

## Step 15 — Test branch, file, pull request, Actions, and merge

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

Sly Director should perform the repository workflow itself through the connector.

## What you should see

At the end of this chapter:

```text
Cognito user pool: working
Lambda: sly-director-github-mcp
Function URL: working
Claude connector: Sly Director GitHub
Repository read: working
Repository write: working
Branch: working
Pull request: working
GitHub Actions inspection: working
Merge: working
```

Continue to [Chapter 6 — Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }}).

<details>
<summary>What the Lambda source contains</summary>

The published source is under:

```text
assets/sly-director/github-mcp-source/
```

Important files:

```text
requirements.txt
build-package.sh
src/settings.py
src/auth.py
src/github_client.py
src/app.py
```

The MCP server uses the current Streamable HTTP transport. It validates Cognito access tokens, including the Cognito issuer, app-client ID, `openid` scope, and OAuth resource audience matching the exact MCP URL.

</details>

<details>
<summary>Why Function URL authentication is NONE</summary>

AWS Function URL authentication and Sly Director authentication are two different layers.

Claude must be able to reach the public MCP endpoint and its OAuth discovery information. The MCP application then requires and validates the Cognito bearer token before any GitHub tool executes.

</details>

<details>
<summary>Why the Function URL hostname is stored in PUBLIC_MCP_URL</summary>

The MCP SDK protects remote HTTP servers against DNS-rebinding attacks. It must know the exact public hostname it is serving.

`PUBLIC_MCP_URL` is used both as the OAuth resource audience and to allow the generated Lambda Function URL hostname.

If it is wrong, the connection can fail with an HTTP `421 Misdirected Request` or token-audience error.

</details>

<details>
<summary>GitHub token permissions</summary>

The permissions in Step 1 support the tool families used by Sly Director: repository contents/branches, pull requests, workflow operations, Actions runs/logs/artifacts, repository Actions variables, and repository Actions secrets.

Start with access only to `claude-director-test`. After the full test succeeds, edit or replace the fine-grained token to add the real repositories Sly Director should operate.

</details>

<details>
<summary>Troubleshooting</summary>

**Health page fails:** open **Lambda → Monitor → View CloudWatch logs** and inspect the newest error.

**Claude cannot authenticate:** confirm the Cognito app client uses `https://claude.ai/api/mcp/auth_callback`, authorization-code grant, `openid`, and the same Client ID/secret entered in Claude.

**Claude gets HTTP 421:** confirm `PUBLIC_MCP_URL` exactly matches the Function URL plus `/mcp`.

**GitHub returns 403:** check the fine-grained token's selected repositories and repository permissions.

**GitHub returns 404 for a private repository:** first confirm that repository is included in the fine-grained token's repository access.

**Workflow-file changes fail:** confirm **Workflows: Read and write** is enabled on the GitHub token.

</details>
