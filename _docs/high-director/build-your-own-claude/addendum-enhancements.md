---
title: "Build Your Own Sly Director — Optional Enhancements"
summary: Extend Sly Director with Skills, Plugins, scheduled autonomous tasks, and specialist tools.
section: high-director
doc_type: runbook
status: active
created: 2026-09-11
updated: 2026-09-11
last_verified: 2026-09-11
order: 91
permalink: /docs/high-director/build-your-own-claude/addendum-enhancements/
---

# Optional Enhancements

The core system is already:

```text
Sly Director Project
├─ normal chat
├─ Cowork
├─ GitHub MCP
└─ AWS MCP
```

Everything below is optional.

## 1 — Sly Director Operator Skill

This is the next useful upgrade after the core setup works.

The Skill would store Sly Director's detailed operating procedure:

```text
inspect
→ plan
→ split work into tasks
→ execute
→ validate
→ diagnose failures
→ retry/recover
→ verify final state
→ return only when complete or genuinely blocked
```

It also teaches Claude that progress updates are informational rather than requests for permission to continue.

## 2 — Scheduled Cowork work

Useful recurring jobs include:

```text
daily failed GitHub Actions review
weekly repository health review
weekly AWS cost/resource review
stale branch / pull-request review
documentation verification
```

Create these from **Cowork → Scheduled → New task**.

## 3 — Sly Director Plugin

Later, a Plugin can package the Operator Skill, connectors, and any specialist Cowork sub-agents so Sly Director is easier to recreate or move.

## 4 — Specialist Cowork sub-agents

Only add named specialist agents if repeated real work shows a benefit. Cowork can already coordinate parallel workstreams itself.

## 5 — Claude Code

Use Claude Code only when a task genuinely needs its specialist repository development environment. It is not the solution to the repeated `continue` problem; Cowork is.

## Recommended order

```text
1. Sly Director Project + GitHub MCP + AWS MCP
2. Cowork + Automatically approve
3. Sly Director Operator Skill
4. Scheduled Cowork routines
5. Plugin packaging / specialist sub-agents
6. Claude Code when technically required
```
