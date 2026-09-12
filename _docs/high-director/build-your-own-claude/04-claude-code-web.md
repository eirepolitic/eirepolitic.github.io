---
title: Build Your Own Sly Director — 04 — GitHub MCP Design
summary: Design the from-scratch GitHub MCP service that gives Sly Director and Cowork full GitHub operation tools without depending on an existing High Director installation.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 84
permalink: /docs/high-director/build-your-own-claude/04-claude-code-web/
---

# Chapter 4 — Design Sly Director's GitHub MCP Service

## Goal

Build one small AWS service that gives **Sly Director** and **Cowork** the GitHub tools they need.

This chapter is written for someone starting from zero. You do not need an existing OpenAI High Director, Lambda function, GitHub API service, or MCP server.

## The complete design

You will build this:

```text
Sly Director / Cowork
        ↓
Claude custom connector
        ↓
Amazon Cognito login
        ↓
AWS Lambda Function URL
        ↓
Lambda: sly-director-github-mcp
        ↓
GitHub API
        ↓
Your GitHub repositories
```

The new Lambda is both:

```text
MCP server
+
GitHub API client
```

There is no second GitHub backend in the normal installation.

## What you will create

Only four new pieces are required:

```text
1. GitHub fine-grained personal access token
2. AWS Lambda function: sly-director-github-mcp
3. Lambda Function URL
4. Amazon Cognito user pool + app client
```

You will then add the Lambda's MCP URL to Claude as a custom connector.

## Why this is the default design

It is intentionally small:

```text
no API Gateway
no EC2 server
no ECS/Fargate service
no database
no permanent virtual machine
no separate GitHub backend
no duplicate orchestration service
```

Lambda runs only when Sly Director calls it. Cognito handles the browser login and OAuth tokens. The Lambda uses one GitHub token to perform the GitHub operations you authorize.

## How a request works

When you tell Sly Director:

```text
Investigate this repository, fix the problem, validate it, and finish the repository workflow.
```

this happens:

```text
1. Claude decides it needs a GitHub tool.
2. Claude sends an MCP request to your Lambda Function URL.
3. The request contains the OAuth access token issued through Cognito.
4. The Lambda verifies that token.
5. The Lambda runs the requested GitHub operation using the server-side GitHub token.
6. GitHub returns the result.
7. The Lambda converts the result into an MCP tool result.
8. Claude continues the task.
```

The GitHub token stays in AWS. You never paste it into ordinary Sly Director conversations.

## GitHub tools the service should expose

The first complete version should support the operations required for autonomous repository work.

### Repository inspection

```text
list repository tree
search repository code
read a file
inspect repository metadata
```

### File and branch work

```text
create branch
create file
update file
delete file
create or update several files in one change
```

### Pull requests

```text
list pull requests
read pull request
create pull request
update pull request
close pull request
merge pull request
```

### GitHub Actions

```text
list workflows
run a workflow
list workflow runs
read workflow run
list workflow jobs
retrieve workflow logs
list workflow artifacts
enable workflow
disable workflow
```

### Repository Actions configuration

```text
create/update Actions variable
delete Actions variable
create/update Actions secret
delete Actions secret
```

This gives Sly Director the same general repository-operation class required by the OpenAI High Director while allowing Claude/Cowork to use it through MCP.

## Authentication design

There are two different credentials. They have different jobs.

```text
Cognito OAuth
→ proves the person connecting Claude is allowed to use the MCP server

GitHub token
→ determines what the MCP server itself may do in GitHub
```

### Claude-facing authentication

Use **Amazon Cognito**.

Create:

```text
User pool: SlyDirectorUsers
App client: SlyDirectorClaude
```

The app client uses an OAuth authorization-code flow with PKCE.

Claude will use the Cognito login page during connector authentication. After successful login, Claude receives an OAuth token. The MCP Lambda validates that token on subsequent requests.

For a personal installation, create one Cognito user for the owner of the Sly Director installation.

### GitHub-facing authentication

Use one **fine-grained GitHub personal access token** owned by the person who controls the repositories.

The token should be limited to the repositories Sly Director is meant to operate and granted the repository permissions required by the MCP tools.

Store the token in the Lambda configuration as:

```text
GITHUB_TOKEN
```

For this low-cost personal design, the Lambda environment is the default secret-storage location. Lambda encrypts environment variables at rest. A later higher-assurance installation can move the token to AWS Secrets Manager without changing the MCP architecture.

## AWS region

Use:

```text
us-east-2
```

for the Sly Director GitHub Lambda and Cognito resources unless you already have a reason to use a different supported region.

Keeping the new Sly Director infrastructure in one region makes it easier for a beginner to find and maintain.

## Lambda design

Create one function:

```text
Name: sly-director-github-mcp
Runtime: Python 3.13
Architecture: x86_64
Memory: 512 MB
Timeout: 30 seconds
Region: us-east-2
```

The source code should be small and divided into clear layers:

```text
src/
├─ app.py              # HTTP/MCP entry point
├─ auth.py             # Cognito token validation
├─ github_client.py    # calls GitHub REST API
├─ tools/
│  ├─ repositories.py
│  ├─ files.py
│  ├─ pull_requests.py
│  ├─ actions.py
│  └─ configuration.py
└─ settings.py         # environment/config loading
```

The Lambda should use the current MCP **Streamable HTTP** transport so Claude can call it as a remote MCP server through one HTTPS endpoint.

The implementation should be stateless. Each MCP request contains what the Lambda needs to process that request, so the first version does not need DynamoDB or another database.

## Lambda environment variables

The fresh installation should require only values such as:

```text
GITHUB_OWNER=<your GitHub username or organization>
GITHUB_TOKEN=<fine-grained GitHub token>
COGNITO_REGION=us-east-2
COGNITO_USER_POOL_ID=<created later>
COGNITO_APP_CLIENT_ID=<created later>
ALLOWED_BRANCH_PREFIX=sly/
DEFAULT_BASE_BRANCH=main
```

Do not put the GitHub token into the source code or repository.

## Function URL design

Create one Lambda Function URL for `sly-director-github-mcp`.

The Function URL is the public HTTPS address Claude contacts.

Conceptually:

```text
https://<generated-id>.lambda-url.us-east-2.on.aws/
```

The MCP application itself validates the Cognito bearer token before allowing GitHub tools to run.

CORS configuration should be kept minimal because Claude's remote connector communicates server-to-server with the MCP endpoint rather than using your browser as the GitHub API client.

## Cognito design

Cognito exists only to authenticate the Claude connector.

The setup should provide:

```text
hosted login page
OAuth authorization endpoint
OAuth token endpoint
user account
app client
redirect/callback to Claude
```

When the connector is added to Claude, use:

```text
Authentication type: OAuth
OAuth client: Use your own OAuth client
```

The guide's implementation section will provide the exact Cognito values to enter for the Client ID, authorization server, scopes, and Claude callback configuration.

## Cost design

This architecture is deliberately serverless.

For a personal installation with modest use, the main cost-producing components are:

```text
Lambda invocations and compute
Cognito monthly active-user usage if usage exceeds its applicable free allowance
GitHub plan/API limits associated with the user's GitHub account
```

There is no always-running AWS server.

AWS billing can change, so the build guide should have the user create an AWS Budget before deployment rather than promising a fixed monthly price.

## Repository safety model

The GitHub token determines the maximum GitHub access Sly Director has.

For a beginner installation:

1. Start by granting the token access only to the `claude-director-test` repository.
2. Verify read, write, branch, pull-request, merge, and Actions behavior.
3. Add production repositories only after the test succeeds.

This makes the first deployment easier to troubleshoot without reducing the eventual capability of Sly Director.

## Completion behavior

The GitHub MCP tools should support the Sly Director/Cowork operating loop:

```text
inspect
→ plan
→ edit
→ branch / PR when useful
→ run or inspect validation
→ diagnose failure
→ edit again
→ revalidate
→ merge / complete
→ inspect final state
```

A progress report from Cowork should not require a new GitHub connection or a new MCP session. The same remote service remains available throughout the task.

## Build sequence

The implementation should be completed in this order:

```text
1. Create the GitHub test repository
2. Create the fine-grained GitHub token
3. Create the Lambda source repository/files
4. Deploy sly-director-github-mcp
5. Create its Function URL
6. Create Cognito user pool and app client
7. Connect Cognito authentication to the MCP service
8. Add Sly Director GitHub as a Claude custom connector
9. Test repository read
10. Test file write
11. Test branch + pull request
12. Test GitHub Actions inspection
13. Test merge/completion
14. Test the same tools from Cowork
15. Add additional repositories
```

The next revision of this chapter can turn each numbered item into exact browser clicks and copy/paste files once the MCP implementation is added to the repository.

## What you should understand before implementation

You do **not** need to understand MCP, OAuth, Cognito, Lambda, or the GitHub API internally to follow the finished guide.

The final guide will tell a new builder:

```text
where to click
what name to enter
what checkbox to select
what code/file to copy
what value to record
what result should appear
```

Background explanations remain in expandable sections so the main procedure stays short.

<details>
<summary>If you already have the OpenAI High Director backend</summary>

An existing High Director installation can reduce duplicate code by using a thin MCP adapter that calls the existing High Director GitHub REST Lambda instead of calling GitHub directly.

That is an optimization for an existing installation, not the default Sly Director architecture.

A fresh third-party installation should build the single `sly-director-github-mcp` Lambda described above.

</details>

<details>
<summary>Why not use the normal Claude GitHub integration?</summary>

Claude's normal GitHub integration is useful for bringing repository content into Claude as context.

Sly Director requires a broader operation layer so Cowork can modify files, work with branches and pull requests, inspect validation, and complete repository workflows. The custom MCP service supplies those operations.

</details>

<details>
<summary>Why not run the MCP server on the user's computer?</summary>

The core Sly Director goal is autonomous Cowork execution that can continue while the user is away.

A cloud-hosted MCP service remains available when the user's computer is closed. A local-only server would weaken that goal.

</details>

## Next chapter

Once the GitHub MCP service is implemented and tested, continue to [Chapter 5 — Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }}).
