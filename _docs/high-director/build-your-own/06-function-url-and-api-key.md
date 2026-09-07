---
title: Build Your Own High Director 06 — Function URL and API Key
summary: Create the public Lambda Function URL used by the GPT Action and verify both the wrapper health endpoint and API-key-protected GitHub access.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 66
permalink: /docs/high-director/build-your-own/06-function-url-and-api-key/
---

# Chapter 6 — Create and Test the Lambda Function URL

## Goal

At the end of this chapter you will have a working HTTPS endpoint for the Lambda wrapper and will have proved that:

1. the Lambda starts correctly;
2. its public Function URL is reachable;
3. the application API key rejects unauthorized protected requests;
4. the correct application API key can read your `director-test` GitHub repository through the wrapper.

This chapter tests the backend before ChatGPT is involved. That separation makes later troubleshooting much easier.

## Architecture choice preserved from High Director

The verified High Director deployment uses:

```text
Lambda Function URL AuthType: NONE
Invoke mode: BUFFERED
CORS: disabled
```

`AuthType: NONE` means AWS does not require IAM authentication at the Function URL layer. The application itself protects its GitHub routes by checking the `X-API-Key` header against the Lambda `APP_API_KEY` environment variable.

The `/health` route is intentionally not API-key protected in the current wrapper and returns basic service/version/owner information. Do not treat the Function URL itself as a password.

## Step 1 — Open the Lambda function

1. Sign in to the AWS Management Console.
2. Confirm the region is **US East (Ohio)**.
3. Open **Lambda**.
4. Open **Functions**.
5. Select `github-gpt-wrapper`.

## Step 2 — Create the Function URL

AWS may place Function URL controls on the **Configuration** tab or in the function overview.

1. Open the function's **Configuration** tab.
2. Find **Function URL**.
3. Select **Create function URL**.
4. For **Auth type**, select **NONE**.
5. If AWS displays a warning that the endpoint will be public, read it and acknowledge it only if you intend to follow this architecture.
6. Leave **CORS** disabled for the initial build.
7. Save or create the Function URL.

Official AWS reference: [Creating and managing Lambda function URLs](https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html).

## Step 3 — Copy the Function URL

AWS should display a URL similar in shape to:

```text
https://EXAMPLE.lambda-url.us-east-2.on.aws/
```

Copy your actual URL.

In your private setup note, add:

```text
Lambda Function URL recorded: yes
```

You may record the actual URL privately if useful. It is not an authentication secret, but it is still an infrastructure endpoint and does not need to be published.

## Step 4 — Test the health endpoint in CloudShell

Open AWS CloudShell.

Paste this line but replace `PASTE_YOUR_FUNCTION_URL_HERE` with your Function URL. Keep the ending `/`:

```bash
FUNCTION_URL="PASTE_YOUR_FUNCTION_URL_HERE"
```

Press **Enter**.

Then paste:

```bash
curl -sS "${FUNCTION_URL}health"
```

A successful response should contain JSON with values similar to:

```json
{
  "ok": true,
  "message": "ok",
  "result": {
    "service": "github-gpt-wrapper",
    "version": "0.3.0",
    "owner": "YOUR_GITHUB_USERNAME"
  }
}
```

The exact formatting may differ. The important values are:

```text
ok = true
service = github-gpt-wrapper
version = 0.3.0
owner = your intended GitHub username
```

If the owner is wrong, stop and correct `GITHUB_OWNER` in Lambda before continuing.

## Step 5 — Prove that a wrong API key is rejected

Paste this command:

```bash
curl -sS -G -H "X-API-Key: deliberately-wrong-test-key" --data-urlencode "path=director-test.txt" "${FUNCTION_URL}repos/director-test/files"
```

The wrapper should return an unauthorized response rather than the file contents.

A normal application-level failure is:

```text
401 unauthorized
```

If a deliberately wrong key can read the file, stop. Do not connect the endpoint to ChatGPT until the authentication behavior is understood.

## Step 6 — Load the real API key without displaying it

Use CloudShell's hidden-input mode so the key does not echo on screen.

Paste:

```bash
read -s -p "Paste APP_API_KEY, then press Enter: " APP_API_KEY; echo
```

Press **Enter**.

Paste the real `APP_API_KEY` stored securely in Chapter 5, then press **Enter** again.

The key should not be displayed while you type or paste it.

## Step 7 — Test protected GitHub file access

Paste:

```bash
curl -sS -G -H "X-API-Key: $APP_API_KEY" --data-urlencode "path=director-test.txt" "${FUNCTION_URL}repos/director-test/files"
```

A successful response should identify repository `director-test`, path `director-test.txt`, and contain the test text you created in Chapter 2.

You should see content equivalent to:

```text
High Director connection test.
```

This single request proves several pieces at once:

- Function URL routing works;
- the Lambda app started;
- `APP_API_KEY` matches;
- `GITHUB_OWNER` is correct;
- `GITHUB_TOKEN` is accepted by GitHub;
- the token can read the repository;
- the wrapper can decode and return the file.

## Step 8 — Remove the secret from the CloudShell variable

Paste:

```bash
unset APP_API_KEY
```

Then paste:

```bash
if [ -z "$APP_API_KEY" ]; then echo "APP_API_KEY cleared from this shell variable"; fi
```

You should see the confirmation message.

This does not delete the API key from Lambda. It only clears the temporary CloudShell shell variable used for testing.

## Step 9 — Record the backend checkpoint

Add this non-secret checklist to your setup note:

```text
Function URL created: yes
Health check: passed
Health owner correct: yes
Wrong API key rejected: yes
Correct API key read director-test.txt: yes
Backend ready for GPT Action: yes
```

Do not proceed to ChatGPT until all five checks pass.

## What you should see

The final protected test should return the contents of `director-test.txt` from GitHub through Lambda.

At this point the backend works independently of ChatGPT.

## If you do not see this

Use the response class to narrow the problem:

- **Function URL cannot be reached:** check Function URL creation, AWS region, and Lambda configuration.
- **`500` or import/module error:** check the ZIP package, handler, runtime, architecture, and dependency build.
- **`401 unauthorized`:** check `APP_API_KEY`; do not change the GitHub token for an application-key failure.
- **GitHub `401`:** the GitHub token is invalid, expired, or otherwise rejected.
- **GitHub `403`:** the token may be valid but lack permission for the requested operation, or GitHub may be refusing the request for another policy/rate-limit reason.
- **GitHub `404`:** confirm the owner, repository name, path, repository access granted to the token, and whether the resource exists.
- **`400` telling you to pass repository name only:** use `director-test`, not `username/director-test`.

Do not rotate both secrets at once when only one authentication layer is failing. Change one thing at a time and retest.

## Ask ordinary ChatGPT this

```text
I have an AWS Lambda Function URL for a FastAPI/Mangum GitHub wrapper.

Architecture:
- Lambda Python 3.13 x86_64
- handler src.app.handler
- Function URL AuthType NONE
- CORS disabled
- protected routes require X-API-Key
- Lambda then calls GitHub REST API with a fine-grained PAT
- GitHub owner is stored in GITHUB_OWNER
- caller passes repository name only

Backend test that failed: [health / wrong-key rejection / authenticated file read]
HTTP status if shown: [status]
Exact sanitized response or error: [paste it]

I have removed all tokens, API keys, AWS account identifiers, and other secrets. Diagnose which layer is failing before suggesting changes. Give the smallest click-by-click or CloudShell test first.
```

## Next chapter

Continue to [Chapter 7 — Create or configure the GPT]({{ '/docs/high-director/build-your-own/07-create-and-configure-gpt/' | relative_url }}).
