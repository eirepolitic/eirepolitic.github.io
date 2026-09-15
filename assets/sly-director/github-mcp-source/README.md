# Sly Director GitHub MCP source

This directory contains the reference source used by the Sly Director build guide.

## Runtime

- AWS Lambda
- Python 3.13
- x86_64
- handler: `src.app.handler`
- MCP Python SDK 2.0
- Streamable HTTP endpoint: `/mcp`
- WorkOS AuthKit OAuth bearer-token validation
- GitHub REST API backend

## Build the Lambda zip in AWS CloudShell

```bash
cd ~
rm -rf eirepolitic.github.io
git clone https://github.com/eirepolitic/eirepolitic.github.io.git
cd eirepolitic.github.io/assets/sly-director/github-mcp-source
chmod +x build-package.sh
./build-package.sh
```

The script creates:

```text
function.zip
```

Deploy it without printing the Lambda environment variables:

```bash
AWS_PAGER="" aws lambda update-function-code \
  --function-name sly-director-github-mcp \
  --zip-file fileb://function.zip \
  --region us-east-2 \
  --query '{FunctionName:FunctionName,LastUpdateStatus:LastUpdateStatus,LastModified:LastModified}' \
  --output table \
  --no-cli-pager
```

Then confirm the update completed:

```bash
AWS_PAGER="" aws lambda get-function-configuration \
  --function-name sly-director-github-mcp \
  --region us-east-2 \
  --query '{State:State,LastUpdateStatus:LastUpdateStatus,Reason:LastUpdateStatusReason}' \
  --output table \
  --no-cli-pager
```

Avoid running `update-function-code` without a `--query` filter because its full response can include Lambda environment variables such as `GITHUB_TOKEN`.

## Lambda handler

```text
src.app.handler
```

## Required environment variables

```text
GITHUB_OWNER
GITHUB_TOKEN
PUBLIC_MCP_URL
AUTHKIT_ISSUER
DEFAULT_BASE_BRANCH
BRANCH_PREFIX
```

Recommended defaults:

```text
DEFAULT_BASE_BRANCH=main
BRANCH_PREFIX=sly/
```

`PUBLIC_MCP_URL` must be the complete Lambda Function URL plus `/mcp`, for example:

```text
https://abc123.lambda-url.us-east-2.on.aws/mcp
```

`AUTHKIT_ISSUER` must be the WorkOS **Production** AuthKit domain, including `https://` and without a trailing slash, for example:

```text
https://example.authkit.app
```

## Authentication

The MCP endpoint accepts WorkOS AuthKit access tokens. The verifier checks:

- AuthKit issuer;
- RS256 signature using `AUTHKIT_ISSUER/oauth2/jwks`;
- token expiry;
- token subject;
- `aud` equal to `PUBLIC_MCP_URL`.

In WorkOS Production, register the exact `PUBLIC_MCP_URL` as a **Resource Indicator** and set it as the default Resource Indicator. Enable both **Client ID Metadata Document (CIMD)** and **Dynamic Client Registration (DCR)** under Connect configuration for broad MCP-client compatibility.

No WorkOS API key is required by the Lambda for access-token verification.

## GitHub tools

The server exposes tools for:

- repository metadata/tree/search/file reads;
- branch creation/deletion;
- file create/update/delete and multi-file updates;
- pull-request list/read/create/update/merge;
- GitHub Actions workflows/runs/jobs/log URLs/artifacts/dispatch/enable/disable;
- repository Actions variables and secrets.

The GitHub owner is server-side configuration. Tool calls pass the repository name only.
