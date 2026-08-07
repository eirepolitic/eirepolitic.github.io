---
title: High Director Data Flows
summary: Verified request, authentication, mutation, secret, Google Workspace, and documentation-publication data flows for High Director.
section: high-director
doc_type: agent
status: active
created: 2026-08-06
updated: 2026-08-06
last_verified: 2026-08-06
owner: High Director
order: 25
permalink: /projects/high-director/data-flows/
---

# High Director Data Flows

## Purpose

This page is the canonical source for verified High Director data flows. It describes how requests and data cross the documented trust boundaries without inventing internal ChatGPT platform behavior that is not directly inspectable.

## Evidence model

Each flow is built from one or more of:

- authoritative GPT configuration;
- authoritative GitHub Action OpenAPI schema;
- authoritative GitHub wrapper Lambda source/deployment package;
- live Lambda/IAM configuration;
- authoritative Google Workspace Action schema/OAuth configuration;
- directly observed GitHub operations during this documentation initiative;
- repository workflow definitions.

## Flow 1 — GitHub read operation

Example operations:

- `getFile`
- `listRepoTree`
- `searchRepoContents`
- `listBranches`
- `listPullRequests`
- `listWorkflows`
- workflow-run/job inspection operations

Verified sequence:

```text
User request
  -> High Director GPT selects a GitHub Action operation
  -> Action request sent to the public Lambda Function URL
     with X-API-Key
  -> FastAPI application compares X-API-Key with APP_API_KEY
  -> application validates repo as repository-name-only
  -> application inserts backend GITHUB_OWNER
  -> application calls https://api.github.com
     with Authorization: Bearer <GITHUB_TOKEN>
  -> GitHub REST API returns repository/workflow data
  -> Lambda wrapper normalizes the response
  -> Action result returns to High Director
  -> High Director presents/uses the result
```

Data crossing the Lambda boundary may include repository name, path/ref/query terms, pull-request identifiers, workflow IDs, run IDs, file contents, workflow/job metadata, and artifact metadata.

## Flow 2 — GitHub file preview

Operations:

- `previewUpsertFile`
- `previewDeleteFile`

### Preview upsert

The request can contain:

- repository name;
- path;
- complete proposed file content;
- commit message;
- optional base branch;
- optional target branch name.

The Lambda application retrieves the current file when needed and calculates a unified diff without writing the change to GitHub.

### Preview delete

The application reads the target file and returns a deletion diff without deleting it.

Preview behavior is implemented as a separate API surface from apply behavior. The application itself does not enforce that every apply operation must have been preceded by a preview.

## Flow 3 — GitHub file create/update

Operation:

```text
applyUpsertFile
```

Verified sequence:

```text
Action request
  -> X-API-Key validation
  -> repo normalization / backend owner insertion
  -> determine base branch
  -> determine/sanitize target branch
  -> create target branch if absent
  -> inspect existing file when needed
  -> base64-encode full file content
  -> GitHub Contents API PUT
  -> GitHub commit/content response
  -> normalized Action response
```

The source application can write to an existing target branch. It does not contain an application-level prohibition against choosing the default branch as the target branch. Avoiding direct default-branch writes therefore depends on agent operating discipline and repository protections.

## Flow 4 — GitHub file deletion

Operation:

```text
applyDeleteFile
```

Verified sequence:

```text
Action request
  -> API-key validation
  -> owner/repo normalization
  -> determine base and target branch
  -> create target branch if needed
  -> retrieve target file SHA
  -> GitHub Contents API DELETE
  -> normalized deletion/commit response
```

The branch-deletion route in the Lambda source does explicitly protect the repository default branch, but that route is not exposed in the currently configured GPT Action schema v0.2.1.

## Flow 5 — Pull-request lifecycle

Configured Action operations include:

- `listPullRequests`
- `createPullRequest`
- `getPullRequest`
- `updatePullRequest`
- `closePullRequest`
- `mergePullRequest`

Typical documented change flow exercised during this initiative:

```text
create branch
  -> apply documentation file changes
  -> create pull request
  -> run/observe documentation validation
  -> merge pull request after validation succeeds
  -> verify matching GitHub Pages deployment
```

The wrapper supports merge methods `merge`, `squash`, and `rebase`; this documentation initiative uses focused PRs and has used squash merges.

## Flow 6 — GitHub workflow dispatch/inspection

Configured operations support:

- workflow listing;
- run listing;
- run details;
- jobs/steps;
- logs redirect URL;
- artifacts;
- dispatch;
- enable/disable.

For the documentation validator, the exercised sequence is:

```text
High Director
  -> dispatchWorkflow(workflow_id, branch/ref)
  -> GitHub Actions creates run
  -> listWorkflowRuns / getWorkflowRun
  -> listWorkflowRunJobs as needed
  -> confirm conclusion == success
```

The documentation policy requires successful validation before documentation merge.

## Flow 7 — GitHub Actions variable mutation

Operations:

- `setVariable`
- `deleteVariable`

`setVariable` accepts a plaintext variable value in the request body. The wrapper attempts creation and, when the GitHub API reports an existing-variable conflict, follows the code's update path.

Repository Actions variables are not secret storage. Values supplied through this operation should be treated according to their real sensitivity rather than assuming GitHub Variables provide secret confidentiality.

## Flow 8 — GitHub Actions secret mutation

Operation:

```text
setSecret
```

Verified sequence:

```text
plaintext_value enters Lambda request body
  -> wrapper requests repository Actions public key from GitHub
  -> wrapper encrypts plaintext using PyNaCl SealedBox
  -> wrapper base64-encodes encrypted ciphertext
  -> wrapper sends encrypted_value + key_id to GitHub
  -> GitHub stores the Actions secret
  -> wrapper returns status/metadata only
```

Security boundary:

- plaintext exists transiently in the Action request/Lambda process;
- the wrapper does not return the plaintext value;
- documentation must never persist a real secret value.

## Flow 9 — GitHub logs

The Lambda application requests workflow-run logs with redirect following disabled.

Verified behavior:

```text
Lambda -> GitHub logs endpoint
GitHub -> redirect response containing temporary download location
Lambda -> returns redirect location to caller
```

The lifecycle/security properties of the temporary GitHub download URL are controlled by GitHub and are not documented beyond this observed implementation behavior.

## Flow 10 — Google OAuth authorization boundary

Configured OAuth settings:

```text
Authorization URL: https://accounts.google.com/o/oauth2/v2/auth
Token URL:         https://oauth2.googleapis.com/token
Token exchange:    default POST request
```

Configured scopes:

```text
https://www.googleapis.com/auth/calendar.events
https://www.googleapis.com/auth/calendar.calendarlist.readonly
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```

Verified boundary:

```text
User/Google authorization
  -> Google authorization endpoint
  -> configured OAuth grant for four scopes
  -> token exchange at Google token endpoint
  -> ChatGPT Action platform uses resulting OAuth authorization
     for Google API requests
```

The exact token storage, refresh-token lifecycle, encryption, and platform-side credential implementation are not directly inspectable and remain unverified.

## Flow 11 — Google Calendar read

Operations:

- `listGoogleCalendars`
- `listCalendarEvents`
- `getCalendarEvent`

Examples of data crossing the Google Action boundary:

- calendar IDs/names;
- access roles/time zones;
- event titles/descriptions/locations;
- start/end times;
- attendees and response status;
- organizer details;
- recurrence;
- Google Meet/conference entry points.

The authenticated account is represented through Google API `me` semantics or supplied calendar IDs; the actual account identity is private and not published.

## Flow 12 — Google Calendar create

Operation:

```text
createCalendarEvent
```

The schema requires confirmation of:

- calendar;
- title;
- date;
- time;
- guests;
- notification behavior.

After confirmation, the Action sends the event body to the Calendar API. Optional request/query data can include `sendUpdates`, conference-data version, attendees, recurrence, reminders, visibility, transparency, guest permissions, and Meet creation information.

## Flow 13 — Google Calendar update/delete/move

Operations:

- `updateCalendarEvent`
- `deleteCalendarEvent`
- `moveCalendarEvent`

The schema requires confirmation before applying these mutations.

`updateCalendarEvent` uses PATCH and can replace complete attendee or recurrence arrays when those fields are supplied.

`deleteCalendarEvent` can control guest notification behavior through `sendUpdates`.

`moveCalendarEvent` sends a destination calendar ID and changes the event organizer as part of the Google Calendar move operation.

## Flow 14 — Gmail profile/search/read

Operations:

- `getGmailProfile`
- `searchGmailMessages`
- `getGmailMessage`
- `getGmailAttachment`

Typical sequence:

```text
searchGmailMessages
  -> message/thread IDs
  -> getGmailMessage(selected ID)
  -> headers/snippet/body structure/attachment references
  -> getGmailAttachment when attachment content is needed
```

Potential sensitive data includes authenticated email address, message subjects/headers/bodies, raw MIME content, sender/recipient addresses, filenames, and attachment contents.

Such data must not be copied into the public documentation site unless explicitly required, sanitized, and safe to publish.

## Flow 15 — Gmail send

Operation:

```text
sendGmailMessage
```

The request body contains:

- `raw`: complete RFC 2822 MIME message encoded as base64url;
- optional `threadId` for replies.

The schema requires High Director to display To, Cc, Bcc, Subject, and body and obtain explicit confirmation immediately before sending.

Verified sequence:

```text
compose proposed email
  -> show recipient/header/body fields to user
  -> obtain explicit confirmation
  -> MIME/base64url request to Gmail send API
  -> Gmail returns message/thread identifiers
```

## Flow 16 — Documentation publication control flow

For every documentation change in this initiative:

```text
inspect verified source
  -> sanitize sensitive/private material
  -> create focused branch
  -> add/update canonical documentation
  -> open focused PR
  -> run Validate documentation
  -> confirm success
  -> merge
  -> identify matching pages-build-deployment run
  -> confirm deployment success
  -> update persistent plan / continue
```

This is a control/documentation flow and is separate from normal High Director runtime task processing.

## Flow 17 — Supplied external source ingestion

When the system owner supplies Action schemas, source packages, AWS configuration, prompts, or other technical material:

```text
user-supplied authoritative source
  -> inspect source
  -> classify evidence
  -> identify secrets/private identifiers
  -> sanitize only what should not be public
  -> preserve technically necessary structure/names
  -> publish sanitized source/reference/documentation
  -> validate/merge/deploy
```

Examples already performed:

- private Lambda hostname redacted;
- AWS account ID omitted;
- literal GitHub owner redacted from deployment config;
- Client ID/Client Secret omitted;
- token/key values never published;
- third-party vendored package code excluded from publication.

## Failure-path flows

### Invalid GitHub Action API key

```text
request -> require_api_key -> 401 unauthorized
```

### Invalid `repo` shape

```text
repo contains '/'
  -> normalize_repo_name
  -> 400 bad_request
  -> message says repository name only, not owner/repo
```

### GitHub timeout

```text
Lambda -> GitHub API timeout
  -> 504 github_timeout
```

### GitHub transport failure

```text
HTTP transport failure
  -> 502 github_transport_error
```

### GitHub API error

```text
GitHub non-expected status
  -> wrapper surfaces github_error with upstream status/details
```

### Request validation failure

```text
FastAPI/Pydantic validation failure
  -> 422 validation_error
```

### Unhandled wrapper failure

```text
unexpected exception
  -> 500 internal_error
```

## Data that must not enter public documentation unsanitized

- API keys;
- GitHub tokens/PATs;
- OAuth Client ID/Secret where treated as confidential implementation identifiers;
- OAuth access/refresh tokens;
- AWS credentials;
- private Lambda hostname;
- personal account IDs;
- personal email addresses where not technically necessary;
- real Gmail message content/attachments;
- private calendar/event/attendee data;
- secret values passed to `setSecret`;
- private repository content not intended for publication.

## Known flow limitations

- ChatGPT platform tool-selection internals are not documented.
- OAuth token storage/refresh internals are not documented.
- GitHub PAT repository/permission scope is not verified.
- Lambda monitoring/log-retention flows are not yet verified.
- The currently configured GitHub Action schema exposes fewer operations than the Lambda application implements.

## Verification record

Verified on 2026-08-06 from the canonical architecture/source pages and directly observed documentation workflow behavior.

## Related Documents

- [High Director Runtime Architecture]({{ '/projects/high-director/runtime-architecture/' | relative_url }})
- [High Director GitHub Integration]({{ '/docs/high-director/github-integration/' | relative_url }})
- [High Director GitHub Action OpenAPI Schema]({{ '/projects/high-director/github-action-openapi-schema/' | relative_url }})
- [High Director GitHub Wrapper Lambda]({{ '/projects/high-director/github-wrapper-lambda/' | relative_url }})
- [High Director Google Workspace Action]({{ '/projects/high-director/google-workspace-action/' | relative_url }})
- [High Director Documentation Initiative Plan]({{ '/docs/high-director/high-director-documentation-initiative-plan/' | relative_url }})
