# Sly Director GitHub MCP source

This directory contains the reference source used by the Sly Director build guide.

## Runtime

- AWS Lambda
- Python 3.13
- x86_64
- handler: `src.app.handler`
- MCP Python SDK 2.0
- Streamable HTTP endpoint: `/mcp`
- Cognito OAuth bearer-token validation
- GitHub REST API backend

## Build the Lambda zip in AWS CloudShell

```bash
git clone https://github.com/eirepolitic/eirepolitic.github.io.git
cd eirepolitic.github.io/assets/sly-director/github-mcp-source
chmod +x build-package.sh
./build-package.sh
```

The script creates:

```text
function.zip
```

Upload that zip to the Lambda function named `sly-director-github-mcp`.

## Lambda handler

```text
src.app.handler
```

## Required environment variables

```text
GITHUB_OWNER
GITHUB_TOKEN
COGNITO_REGION
COGNITO_USER_POOL_ID
COGNITO_APP_CLIENT_ID
PUBLIC_MCP_URL
DEFAULT_BASE_BRANCH
BRANCH_PREFIX
```

Recommended defaults:

```text
COGNITO_REGION=us-east-2
DEFAULT_BASE_BRANCH=main
BRANCH_PREFIX=sly/
```

`PUBLIC_MCP_URL` must be the complete Lambda Function URL plus `/mcp`, for example:

```text
https://abc123.lambda-url.us-east-2.on.aws/mcp
```

## Authentication

The MCP endpoint accepts Cognito **access tokens** issued to the configured app client. The verifier checks:

- Cognito issuer/signature;
- token expiry;
- `token_use=access`;
- configured Cognito app-client ID;
- `openid` scope;
- `aud` equal to `PUBLIC_MCP_URL`.

The audience is supplied through Cognito OAuth resource binding (RFC 8707).

## GitHub tools

The server exposes tools for:

- repository metadata/tree/search/file reads;
- branch creation/deletion;
- file create/update/delete and multi-file updates;
- pull-request list/read/create/update/merge;
- GitHub Actions workflows/runs/jobs/log URLs/artifacts/dispatch/enable/disable;
- repository Actions variables and secrets.

The GitHub owner is server-side configuration. Tool calls pass the repository name only.
