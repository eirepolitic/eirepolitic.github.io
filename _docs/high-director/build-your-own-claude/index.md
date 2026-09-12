---
title: Build Your Own Sly Director
summary: Build a Claude-based director that uses normal chat for quick work and Cowork for long-running autonomous work, with GitHub MCP and AWS MCP as its tools.
section: high-director
doc_type: runbook
status: active
created: 2026-09-10
updated: 2026-09-11
last_verified: 2026-09-11
order: 80
permalink: /docs/high-director/build-your-own-claude/
---

# Build Your Own Sly Director

## The whole plan

Build **one Claude Project called Sly Director**.

Use it in two ways:

```text
Sly Director
├─ Normal chat → quick questions, planning, small changes
└─ Cowork → large jobs that should keep working without you

Both can use:
├─ GitHub MCP → repositories, files, branches, PRs, Actions
└─ AWS MCP → AWS resources and operations
```

That is the entire design.

For a small job, talk to **Sly Director** normally.

For a large job, open **Sly Director in Cowork**, give it the final objective, use **Automatically approve**, and let it continue through planning, implementation, testing, corrections, and verification until the work is finished or it genuinely needs you.

The later **Sly Director Operator Skill** is an improvement to this same system. It is not something you need to build before completing the guide.

## Build it in this order

1. [Check the required accounts and Claude features]({{ '/docs/high-director/build-your-own-claude/01-accounts-and-prerequisites/' | relative_url }})
2. [Create a small GitHub test repository]({{ '/docs/high-director/build-your-own-claude/02-github-and-first-repository/' | relative_url }})
3. [Create the Sly Director Project]({{ '/docs/high-director/build-your-own-claude/03-create-high-director-project/' | relative_url }})
4. [Connect GitHub MCP]({{ '/docs/high-director/build-your-own-claude/04-claude-code-web/' | relative_url }})
5. [Prepare AWS]({{ '/docs/high-director/build-your-own-claude/05-aws-account-and-safety/' | relative_url }})
6. [Connect AWS MCP]({{ '/docs/high-director/build-your-own-claude/06-aws-mcp-server/' | relative_url }})
7. [Set up Cowork for long-running autonomous work]({{ '/docs/high-director/build-your-own-claude/07-end-to-end-testing/' | relative_url }})
8. [Use Sly Director day to day]({{ '/docs/high-director/build-your-own-claude/08-daily-operation/' | relative_url }})
9. [Troubleshoot problems]({{ '/docs/high-director/build-your-own-claude/09-troubleshooting/' | relative_url }})
10. [Maintain the setup]({{ '/docs/high-director/build-your-own-claude/10-maintenance/' | relative_url }})

Optional later:

- [Skills, Plugins, scheduling, and specialist tools]({{ '/docs/high-director/build-your-own-claude/addendum-enhancements/' | relative_url }})
- [Google Workspace and other connectors]({{ '/docs/high-director/build-your-own-claude/addendum-connectors/' | relative_url }})
- [Custom MCP servers]({{ '/docs/high-director/build-your-own-claude/addendum-custom-mcp/' | relative_url }})

## What success looks like

You should eventually be able to say something like:

```text
Investigate this repository and the related AWS infrastructure. Find the cause of the problem, implement the best practical fix, validate it, correct recoverable failures, finish the repository workflow, verify the final state, and return to me when the job is complete or you genuinely need a decision from me.
```

For a substantial job, Sly Director should then continue working in Cowork instead of repeatedly stopping just to make you type `continue`.

<details>
<summary>How this relates to Overlord</summary>

Overlord was designed around the same underlying objective: keep a plan moving without losing state or requiring constant owner intervention.

Cowork now provides much of the runtime that Overlord was building manually:

```text
Overlord idea                        Sly Director equivalent
----------------------------------   ----------------------------------
durable long-running work            Cowork cloud sessions
task decomposition                    Cowork subtasks
parallel delegated workers            Cowork sub-agents
resume after interruption             persistent Cowork task state
validation and retry                  Sly Director instructions + Cowork
interrupt owner only when needed      Automatically approve + escalation rules
recurring autonomous work             Cowork scheduled tasks
```

The valuable Overlord operating rules remain useful. They are being carried into Sly Director's Project instructions and, later, the Sly Director Operator Skill.

</details>

<details>
<summary>Optional improvements after the core setup works</summary>

**Sly Director Operator Skill** — stores the detailed investigate → plan → implement → validate → retry → verify procedure so Claude follows it consistently.

**Scheduled Cowork tasks** — let Sly Director perform recurring work such as failed GitHub Actions reviews or AWS checks without you starting each run.

**Plugin packaging** — can later package Skills, connectors, and specialist Cowork helpers together.

**Claude Code** — remains a specialist fallback for repository work that genuinely requires a dedicated cloned-repository development environment.

</details>
