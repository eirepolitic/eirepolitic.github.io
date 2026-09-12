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
├─ Sly Director GitHub
└─ AWS MCP
```

Everything below is optional after the core guide works.

## 1 — Sly Director Operator Skill

This is the next useful upgrade after real Sly Director/Cowork use shows which operating rules need to be more consistent.

The Skill can store Sly Director's detailed operating procedure:

```text
inspect
→ define completion criteria
→ plan
→ split work into dependent tasks
→ execute / parallelize independent work
→ validate
→ diagnose failures
→ retry or recover
→ preserve progress
→ verify final state
→ return only when complete or genuinely blocked
```

It can also reinforce that progress updates are informational rather than requests for permission to continue.

## 2 — Scheduled Cowork work

Useful recurring jobs include:

```text
daily failed GitHub Actions review
weekly repository health review
weekly AWS cost/resource review
stale branch / pull-request review
documentation verification
```

Create these from **Cowork → Scheduled → New task** and give the task access only to the connectors it needs.

## 3 — Sly Director Plugin

Later, a Plugin can package the Operator Skill, connectors, and any specialist Cowork sub-agents so Sly Director is easier to recreate or move.

## 4 — Specialist Cowork sub-agents

Only add named specialist agents if repeated real work shows a benefit. Cowork can already coordinate parallel workstreams itself.

## 5 — Claude Code

Use Claude Code only when a task genuinely needs its specialist repository development environment. It is not the solution to the repeated `continue` problem; Cowork is.

## Recommended order

```text
1. Sly Director Project + Sly Director GitHub + AWS MCP
2. Cowork + Automatically approve
3. Use the system on real work
4. Sly Director Operator Skill based on observed behavior
5. Scheduled Cowork routines
6. Plugin packaging / specialist sub-agents
7. Claude Code when technically required
```
