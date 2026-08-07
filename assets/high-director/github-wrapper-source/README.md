# GitHub GPT Wrapper Starter

This starter gives your custom GPT an **Action API** that can:

- read repo files
- preview file diffs
- create or update files on a branch
- delete files on a branch
- open pull requests
- list, enable, disable, and dispatch workflows
- create or update Actions variables
- create or update Actions secrets
- delete variables and secrets

## What is in this folder

- `src/app.py` — FastAPI app for AWS Lambda
- `openapi.yaml` — import this into your custom GPT Action
- `template.yaml` — AWS SAM template for deployment
- `requirements.txt` — Python dependencies

## Recommended v1 behavior

Use the GPT like this:

1. Read the target file.
2. Preview the change.
3. Show the diff to you.
4. After you approve, apply the change to a branch.
5. Open a draft PR.

That keeps the approval gate at the PR.

## Step 1 — Create the GitHub token

Create a **fine-grained personal access token** for the single GitHub owner that contains your repos.

Recommended repository permissions:

- **Metadata:** Read
- **Contents:** Read and write
- **Pull requests:** Read and write
- **Actions:** Read and write
- **Variables:** Read and write
- **Secrets:** Read and write
- **Workflows:** Read and write

Use **All repositories** for that owner.

## Step 2 — Create an API key for the GPT Action

Create a long random string. Example command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Save this value. You will use it twice:

- as `APP_API_KEY` in Lambda
- as the API key inside the GPT Action setup

## Step 3 — Deploy to AWS Lambda

This starter uses **Lambda Function URL** because it is the cheapest simple HTTP option.

### Option A — Deploy with AWS SAM

1. Install:
   - AWS CLI
   - AWS SAM CLI
   - Python 3.12

2. In a terminal, go into this folder.

3. Install dependencies into the project:

```bash
pip install -r requirements.txt -t .
```

4. Build:

```bash
sam build
```

5. Deploy:

```bash
sam deploy --guided
```

6. When prompted:
   - Stack name: `github-gpt-wrapper`
   - AWS Region: your region
   - Parameter `GithubOwner`: your GitHub owner name
   - Parameter `GithubToken`: your fine-grained PAT
   - Parameter `AppApiKey`: your random API key
   - Parameter `DefaultBaseBranch`: `main`
   - Parameter `BranchPrefix`: `gpt`
   - Save arguments to config: `Y`

7. Copy the `FunctionUrl` output after deploy.

### Option B — Deploy in the Lambda console manually

Use this only if you do not want SAM.

1. Zip this folder **after** installing dependencies into the root.
2. In AWS, open **Lambda**.
3. Click **Create function**.
4. Choose **Author from scratch**.
5. Name: `github-gpt-wrapper`
6. Runtime: **Python 3.12**
7. Create the function.
8. Upload the zip file.
9. Set handler to:

```text
src.app.handler
```

10. Open **Configuration → Environment variables** and add:
    - `GITHUB_OWNER`
    - `GITHUB_TOKEN`
    - `APP_API_KEY`
    - `DEFAULT_BASE_BRANCH` = `main`
    - `BRANCH_PREFIX` = `gpt`

11. Open **Configuration → Function URL**.
12. Create a Function URL.
13. Auth type: **NONE**
14. Copy the Function URL.

## Step 4 — Test the API yourself

Replace the URL and key below.

### Health check

```bash
curl https://YOUR_FUNCTION_URL/health
```

### Read a file

```bash
curl -H "X-API-Key: YOUR_APP_API_KEY" \
  "https://YOUR_FUNCTION_URL/repos/YOUR_REPO/files?path=README.md"
```

### Preview a file update

```bash
curl -X POST "https://YOUR_FUNCTION_URL/repos/YOUR_REPO/files/preview-upsert" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_APP_API_KEY" \
  -d '{
    "path": "README.md",
    "content": "# New title\n\nUpdated by GPT.\n",
    "commit_message": "Update README with new title"
  }'
```

### Apply the file update to a branch

```bash
curl -X POST "https://YOUR_FUNCTION_URL/repos/YOUR_REPO/files/apply-upsert" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_APP_API_KEY" \
  -d '{
    "path": "README.md",
    "content": "# New title\n\nUpdated by GPT.\n",
    "commit_message": "Update README with new title",
    "branch_name": "gpt/readme-title-update"
  }'
```

### Open a draft PR

```bash
curl -X POST "https://YOUR_FUNCTION_URL/repos/YOUR_REPO/pull-requests" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_APP_API_KEY" \
  -d '{
    "title": "Update README title",
    "body": "Created by GPT wrapper.",
    "head_branch": "gpt/readme-title-update",
    "draft": true
  }'
```

## Step 5 — Add the Action to your GPT

1. Open your GPT in the GPT builder.
2. Open the **Actions** section.
3. Click **Create new action**.
4. Choose **Import from schema**.
5. Paste the contents of `openapi.yaml`.
6. Replace the server URL in `openapi.yaml` with your real Lambda Function URL.
7. Set authentication to **API Key**.
8. Header name: `X-API-Key`
9. Paste your `APP_API_KEY`.
10. Save the action.

## Step 6 — Add these operating rules to the GPT instructions

Paste this into the GPT instructions:

```text
When changing GitHub files:
1. Read the existing file first when it exists.
2. Call previewUpsertFile or previewDeleteFile before any write.
3. Show the diff to the user and ask for approval.
4. Only after approval, call applyUpsertFile or applyDeleteFile.
5. After a successful write, create a draft pull request unless the user explicitly says not to.
6. Never write directly to the default branch.
7. Never request or reveal existing secret values.
8. For workflow runs, only call dispatchWorkflow when the user explicitly asks to run the workflow.
```

## Example GPT flow

For a file update:

1. `getFile`
2. `previewUpsertFile`
3. you approve
4. `applyUpsertFile`
5. `createPullRequest`

For a file delete:

1. `previewDeleteFile`
2. you approve
3. `applyDeleteFile`
4. `createPullRequest`

## Notes

- This starter is scoped to **one GitHub owner**.
- It supports **all repositories** under that owner, depending on your PAT.
- It does **not** read secrets back from GitHub.
- It does **not** merge PRs.
- It does **not** write directly to `main` unless you later add a direct-write endpoint.
- If you edit files under `.github/workflows/`, your token needs workflow-related write permission.
