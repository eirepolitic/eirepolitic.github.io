---
title: Build Your Own High Director 05 — Deploy the GitHub Wrapper Lambda
summary: Build the verified High Director GitHub wrapper entirely in AWS CloudShell and deploy it to a Python 3.13 Lambda function without installing software locally.
section: high-director
doc_type: runbook
status: active
created: 2026-09-07
updated: 2026-09-07
last_verified: 2026-09-07
order: 65
permalink: /docs/high-director/build-your-own/05-deploy-lambda/
---

# Chapter 5 — Deploy the GitHub Wrapper Lambda

## Goal

At the end of this chapter you will have an AWS Lambda function containing the verified High Director GitHub wrapper code and dependencies.

You will configure:

```text
Function name: github-gpt-wrapper
Runtime: Python 3.13
Architecture: x86_64
Handler: src.app.handler
Memory: 512 MB
Timeout: 30 seconds
Region: us-east-2
```

You will also add the required environment variables, including your GitHub token and a new application API key.

## Important secret warning

This chapter handles two secrets:

- your GitHub personal access token;
- the new application API key that will protect calls from the GPT to the Lambda application.

Do not paste either secret into ChatGPT, GitHub files, this documentation site, screenshots, or troubleshooting messages.

## Step 1 — Return to CloudShell

1. Sign in to the AWS Management Console.
2. Confirm the region is **US East (Ohio)**.
3. Open **CloudShell**.
4. Click inside the terminal.
5. Paste:

```bash
cd ~/high-director-build
```

6. Press **Enter**.

## Step 2 — Download the published wrapper source parts

The authoritative sanitized source is stored in the Eire Politic documentation repository as four parts. The commands below download those exact published parts from GitHub.

Paste these commands one at a time:

```bash
rm -rf source package github-gpt-wrapper.zip requirements.txt
```

```bash
mkdir -p source/src package/src
```

```bash
curl -fL https://raw.githubusercontent.com/eirepolitic/eirepolitic.github.io/main/assets/high-director/github-wrapper-source/src/app.py.part01 -o source/src/app.py.part01
```

```bash
curl -fL https://raw.githubusercontent.com/eirepolitic/eirepolitic.github.io/main/assets/high-director/github-wrapper-source/src/app.py.part02 -o source/src/app.py.part02
```

```bash
curl -fL https://raw.githubusercontent.com/eirepolitic/eirepolitic.github.io/main/assets/high-director/github-wrapper-source/src/app.py.part03 -o source/src/app.py.part03
```

```bash
curl -fL https://raw.githubusercontent.com/eirepolitic/eirepolitic.github.io/main/assets/high-director/github-wrapper-source/src/app.py.part04 -o source/src/app.py.part04
```

```bash
curl -fL https://raw.githubusercontent.com/eirepolitic/eirepolitic.github.io/main/assets/high-director/github-wrapper-source/requirements.txt -o requirements.txt
```

If any `curl` command ends with an error, stop. Do not continue with missing source files.

## Step 3 — Reconstruct `src/app.py`

Paste:

```bash
cat source/src/app.py.part01 source/src/app.py.part02 source/src/app.py.part03 source/src/app.py.part04 > package/src/app.py
```

Then verify the file exists:

```bash
ls -lh package/src/app.py
```

You should see one `app.py` file with a non-zero size.

## Step 4 — Verify the dependency list

Paste:

```bash
cat requirements.txt
```

The verified dependency set should include these pinned packages:

```text
fastapi==0.115.12
mangum==0.19.0
httpx==0.28.1
PyNaCl==1.5.0
pydantic==2.11.3
```

If the downloaded file is empty or materially different, stop and compare it with the current [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }}) documentation before deploying.

## Step 5 — Install dependencies into the Lambda package folder

Paste:

```bash
python3 -m pip install -r requirements.txt -t package
```

This may print many lines. Warnings about running `pip` in a cloud shell are not automatically failures. The important result is that the command completes without an installation error.

Then paste:

```bash
ls package
```

You should see `src` plus installed Python packages.

## Step 6 — Create the ZIP file

Paste:

```bash
cd package && zip -qr ../github-gpt-wrapper.zip . && cd ..
```

Then paste:

```bash
ls -lh github-gpt-wrapper.zip
```

You should see a ZIP file with a non-zero size.

Do not upload the ZIP to a public repository. It contains application code and bundled dependencies. It does not yet contain your environment-variable secrets, but there is no need to publish it.

## Step 7 — Create the Lambda function in the AWS console

Keep CloudShell open in one browser tab. Open the normal AWS console in another tab.

1. In the AWS console search box, search for **Lambda**.
2. Open **Lambda**.
3. Select **Functions** if the function list is not already shown.
4. Select **Create function**.
5. Select **Author from scratch**.
6. In **Function name**, enter:

```text
github-gpt-wrapper
```

7. For **Runtime**, select **Python 3.13**.
8. For **Architecture**, select **x86_64**.
9. Expand **Change default execution role** or the current equivalent permissions section.
10. Choose **Create a new role with basic Lambda permissions**.
11. Do not add a Function URL yet; Chapter 6 handles it separately.
12. Select **Create function**.

AWS will create the function and a basic execution role. The verified High Director execution role uses the standard `AWSLambdaBasicExecutionRole` managed policy for basic logging.

## Step 8 — Upload the ZIP from CloudShell

Return to the CloudShell tab.

Paste:

```bash
aws lambda update-function-code --function-name github-gpt-wrapper --zip-file fileb://github-gpt-wrapper.zip --region us-east-2
```

Press **Enter**.

A successful response is JSON describing the function. You do not need to understand every field.

If the command says the function cannot be found, first confirm the AWS region and exact function name. Do not create a second function until you know why the first one was not found.

## Step 9 — Configure the handler

Return to the Lambda console and open `github-gpt-wrapper`.

1. Find **Runtime settings**.
2. Select **Edit**.
3. Set **Handler** to:

```text
src.app.handler
```

4. Leave the architecture as `x86_64`.
5. Select **Save**.

## Step 10 — Configure memory and timeout

1. Open the function's **Configuration** tab.
2. Select **General configuration**.
3. Select **Edit**.
4. Set **Memory** to:

```text
512 MB
```

5. Set **Timeout** to:

```text
30 seconds
```

6. Select **Save**.

## Step 11 — Generate the application API key

Return to CloudShell.

Paste:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Press **Enter**.

CloudShell will print a random string. That string is your **application API key**.

Immediately copy it into the same secure secret-storage method you used for the GitHub token.

Do not paste it into ChatGPT or your ordinary setup note.

If you lose it before configuring Lambda, generate a new one. There is no reason to recover the old one.

## Step 12 — Add Lambda environment variables

Return to the Lambda console for `github-gpt-wrapper`.

1. Open **Configuration**.
2. Select **Environment variables**.
3. Select **Edit**.
4. Add these five variables exactly:

| Key | Value |
|---|---|
| `GITHUB_OWNER` | your exact personal GitHub username |
| `GITHUB_TOKEN` | the fine-grained token from Chapter 3 |
| `APP_API_KEY` | the random application API key you just generated |
| `BRANCH_PREFIX` | `gpt` |
| `DEFAULT_BASE_BRANCH` | `main` or your actual default branch if different |

5. Check spelling carefully. Environment-variable names are case-sensitive.
6. Select **Save**.

The current verified wrapper also supports optional `GITHUB_API_VERSION` and `REQUEST_TIMEOUT` variables, but the application has defaults. Do not add unnecessary differences during the initial build.

## Step 13 — Record non-secret deployment details

In your private setup note, add:

```text
Lambda function: github-gpt-wrapper
AWS region: us-east-2
Runtime: Python 3.13
Architecture: x86_64
Handler: src.app.handler
Memory: 512 MB
Timeout: 30 seconds
GITHUB_OWNER configured: yes
GITHUB_TOKEN configured: yes
APP_API_KEY configured: yes
BRANCH_PREFIX: gpt
DEFAULT_BASE_BRANCH: main
APP_API_KEY stored separately: yes
```

Do not write the token or API-key values in the note.

## What you should see

The Lambda console should show:

- function `github-gpt-wrapper`;
- Python 3.13;
- x86_64;
- handler `src.app.handler`;
- five environment variables by name;
- no need for local software on your computer.

The function may not yet be callable from ChatGPT because the Function URL is created in Chapter 6.

## If you do not see this

Check in this order:

1. Confirm the AWS console region is **US East (Ohio)**.
2. Confirm CloudShell commands use `--region us-east-2`.
3. Confirm the function name is exactly `github-gpt-wrapper`.
4. If ZIP upload fails, run `ls -lh ~/high-director-build/github-gpt-wrapper.zip` and confirm it exists.
5. If dependency installation failed, copy the non-secret error text; do not start changing Python versions or package versions at random.
6. If Lambda later reports an import error, preserve the exact error text and check the package build before changing application code.

## Ask ordinary ChatGPT this

```text
I am deploying a Python 3.13 x86_64 AWS Lambda named github-gpt-wrapper entirely from AWS CloudShell.

Handler: src.app.handler
Memory: 512 MB
Timeout: 30 seconds
Region: us-east-2
The ZIP contains src/app.py plus dependencies installed with pip into the ZIP root.
Dependencies: fastapi 0.115.12, mangum 0.19.0, httpx 0.28.1, PyNaCl 1.5.0, pydantic 2.11.3.

The failing step is: [describe it]
Command or screen: [describe it]
Exact non-secret error: [paste it]

Do not ask for my GitHub token, Lambda APP_API_KEY, AWS credentials, account number, or other secrets. Diagnose the smallest likely cause first and give browser/CloudShell steps in order. Do not suggest changing package versions unless the error specifically supports that diagnosis.
```

## Next chapter

Continue to [Chapter 6 — Create and test the Lambda Function URL]({{ '/docs/high-director/build-your-own/06-function-url-and-api-key/' | relative_url }}).
