---
title: Build Your Own Sly Director — Cognito Domain Setup
summary: Confirm the AWS-hosted Cognito domain for Sly Director and avoid the custom-domain ACM certificate path.
section: high-director
doc_type: runbook
status: active
created: 2026-09-11
updated: 2026-09-11
last_verified: 2026-09-11
order: 85
permalink: /docs/high-director/build-your-own-claude/cognito-domain-setup/
---

# Cognito Domain Setup

## Goal

Confirm that the AWS-hosted Cognito login domain exists. You do not need your own domain name or an ACM certificate.

## Complete this step

1. Open the AWS console.
2. Open **Amazon Cognito**.
3. Open **User pools**.
4. Select the Sly Director user pool.
5. Open:

```text
Branding → Domain
```

6. Look at the top card labeled:

```text
Cognito domain
```

### If a domain is already shown

If the top **Cognito domain** card already contains a URL such as:

```text
https://us-east-2xxxxxxxx.auth.us-east-2.amazoncognito.com
```

then this step is already complete.

1. Copy or record that existing URL.
2. Confirm **Branding version** says:

```text
Managed login
```

3. Ignore the entire **Custom domain** section below it.
4. Return to Chapter 5 and continue with **Step 6 — Create your first Cognito user**.

### If the Cognito domain card is empty

Only if no AWS-hosted Cognito domain exists:

1. In the **Cognito domain** section, select the available create/edit action.
2. Choose the AWS-hosted **Cognito domain** option.
3. Enter a unique prefix if AWS asks for one, for example:

```text
sly-director-yourname
```

4. For **Branding version**, choose:

```text
Managed login
```

5. Save/create the domain.
6. Wait until the domain appears in the top **Cognito domain** card.
7. Record the URL.

## Ignore the Custom domain section

The lower card labeled:

```text
Custom domain
```

is not used by this guide.

Do not select its **Create domain** button.

That path is only for a domain you own, such as:

```text
auth.example.com
```

and AWS requires an ACM certificate for it.

## If AWS asks for an ACM certificate

You are in the **Custom domain** workflow.

Cancel or go back to the main **Branding → Domain** page. Then use the existing top **Cognito domain** card instead.

## What you should see

```text
Top card: Cognito domain
Domain: an amazoncognito.com URL
Branding version: Managed login
Custom domain: unused
ACM certificate: not required
```

After this is confirmed, return to Chapter 5 and continue with the first Cognito user.
