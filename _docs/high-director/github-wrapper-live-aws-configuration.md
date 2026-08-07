---
title: High Director GitHub Wrapper Live AWS Configuration
summary: User-supplied authoritative record of the deployed Lambda runtime, Function URL, environment-variable names, execution role, managed policy, and trust relationship for the High Director GitHub wrapper.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 22
permalink: /projects/high-director/github-wrapper-live-aws-configuration/
---

# High Director GitHub Wrapper Live AWS Configuration

## Purpose

This page records the live AWS configuration supplied from the AWS Console for the deployed GitHub wrapper Lambda behind the High Director GitHub Action.

## Evidence classification

**User-supplied authoritative live configuration**, supplied on 2026-08-06 through AWS Console screenshots and copied IAM trust-policy JSON.

## Sanitization

Before publication:

- the private Lambda Function URL hostname was omitted;
- the AWS account ID embedded in the console link/role ARN was omitted;
- environment-variable values were not supplied or published;
- no API key, GitHub token, AWS access key, password, private key, or other credential value is published;
- technically necessary non-secret names such as environment-variable keys, execution-role name, managed-policy name, runtime, handler, architecture, and IAM service principal are retained.

## Live Lambda runtime

| Setting | Live value |
|---|---|
| Runtime | `Python 3.13` |
| Handler | `src.app.handler` |
| Architecture | `x86_64` |
| Runtime update mode | `Auto` |
| Region | `us-east-2` |

The live runtime and handler match the supplied SAM template.

## Live Function URL configuration

| Setting | Live value |
|---|---|
| Function URL | Public Lambda Function URL; hostname redacted |
| AWS auth type | `NONE` |
| Invoke mode | `BUFFERED` |
| CORS | Not enabled |

The AWS Console explicitly states that the Function URL is public and can be reached by anyone who knows the URL. AWS IAM authentication is therefore not enforced at the Function URL layer.

Application-level access control remains the `X-API-Key` check implemented by `src/app.py` against the `APP_API_KEY` environment variable.

## Live environment-variable names

The supplied AWS Console view confirms these deployed environment-variable keys:

```text
APP_API_KEY
BRANCH_PREFIX
DEFAULT_BASE_BRANCH
GITHUB_OWNER
GITHUB_TOKEN
```

No values were supplied or published.

The application source also supports optional `GITHUB_API_VERSION` and `REQUEST_TIMEOUT`; these were not visible in the supplied live environment-variable list and therefore appear to be using application defaults unless configured elsewhere.

## Execution role

Live execution-role name:

```text
github-gpt-wrapper-GithubGptWrapperRole-6j2drFhUXMyo
```

The supplied role view shows one attached permissions policy:

```text
AWSLambdaBasicExecutionRole
```

No custom or inline policy document was supplied in this source set. Therefore this documentation does not claim that none exist beyond what was visible; only the single visible managed policy is verified.

## Trust relationship

The supplied trust policy is:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

This verifies that AWS Lambda is trusted to assume the execution role.

## Security boundary verified by live configuration

The currently verified request/authentication path is:

1. the Lambda Function URL is publicly reachable with AWS auth type `NONE`;
2. the FastAPI application requires `X-API-Key` and compares it with `APP_API_KEY`;
3. the application uses `GITHUB_TOKEN` as a Bearer token for calls to the GitHub REST API;
4. `GITHUB_OWNER` fixes the backend owner scope and repository inputs must be repository name only;
5. the Lambda execution role shown in AWS has the visible managed policy `AWSLambdaBasicExecutionRole` and trusts `lambda.amazonaws.com`.

The visible role policy is consistent with basic Lambda logging permissions; GitHub access is performed with the application-level GitHub token rather than AWS IAM permissions.

## Live-vs-template comparison

| Setting | SAM/source declaration | Live AWS value | Status |
|---|---|---|---|
| Runtime | `python3.13` | Python 3.13 | Match |
| Handler | `src.app.handler` | `src.app.handler` | Match |
| Function URL auth | `NONE` | `NONE` | Match |
| Invoke mode | `BUFFERED` | `BUFFERED` | Match |
| `APP_API_KEY` | declared | present | Match |
| `BRANCH_PREFIX` | declared | present | Match |
| `DEFAULT_BASE_BRANCH` | declared | present | Match |
| `GITHUB_OWNER` | declared | present | Match |
| `GITHUB_TOKEN` | declared | present | Match |
| Architecture | not explicitly set in supplied SAM template | `x86_64` | Live-only verified setting |
| CORS | not configured in supplied SAM template | not enabled | Consistent |

## What remains unverified

- Lambda memory and timeout in the live console, although the SAM template declares 512 MB and 30 seconds;
- exact deployed Lambda function name;
- actual environment-variable values;
- API-key and GitHub-token creation, storage, and rotation procedures;
- exact fine-grained GitHub PAT permissions currently granted;
- whether additional execution-role policies or inline policies exist beyond the visible supplied view;
- CloudWatch log-group retention, alarms, metrics, dashboards, and monitoring configuration;
- Lambda Function URL resource policy details;
- deployment history, versions, aliases, reserved concurrency, and retry/dead-letter settings.

## Verification record

- Verified: `2026-08-06`
- Source: user-supplied AWS Lambda and IAM Console screenshots plus trust-policy JSON
- Private identifiers redacted: Lambda URL hostname and AWS account ID
- Secret values published: none

## Related Documents

- [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }})
- [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
