---
title: Build Your Own Sly Director — Cognito Domain Setup
summary: Choose the AWS-hosted Cognito domain for Sly Director and avoid the custom-domain ACM certificate path.
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

Create the AWS-hosted Cognito login domain without needing your own domain name or an ACM certificate.

## Complete this step

1. Open the AWS console.
2. Open **Amazon Cognito**.
3. Open **User pools**.
4. Select the Sly Director user pool.
5. Open:

```text
Branding → Domain
```

6. Next to **Domain**, select **Actions**.
7. Select:

```text
Create Cognito domain
```

Do **not** select:

```text
Create custom domain
```

8. Enter a unique prefix only, for example:

```text
sly-director-yourname
```

9. For **Branding version**, choose **Managed login** if AWS asks.
10. Select **Create**.
11. Wait until the domain becomes available.

The resulting domain should use Amazon Cognito's hosted domain and look similar to:

```text
https://sly-director-yourname.auth.us-east-2.amazoncognito.com
```

## If AWS asks for an ACM certificate

You are on the **Custom domain** path.

Back out of that screen and return to:

```text
Branding → Domain → Actions → Create Cognito domain
```

A custom domain is only needed when you want to use a domain name that you own, such as `auth.example.com`. AWS requires an ACM certificate for that path. Sly Director does not need a custom domain.

## What you should see

```text
Domain type: Amazon Cognito domain / Cognito domain
ACM certificate: not required
Custom DNS: not required
Managed login: available
```

After this succeeds, return to Chapter 5 and continue with the first Cognito user.
