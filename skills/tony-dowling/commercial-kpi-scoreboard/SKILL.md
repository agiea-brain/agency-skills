---
name: commercial-kpi-scoreboard
title: Commercial KPI scoreboard
description: |
  Use this skill when a sales manager or rep asks how the numbers look for a
  rep or the whole team over today, this week, this month or the quarter.
  Produces a six-row scoreboard from live CRM deal data: presentations made,
  closing ratio, sales velocity, average order value, current billing, and
  position against target, with a 2 to 3 line commercial read. Also use for
  "how is Danny doing this month", "team scoreboard", "closing ratio",
  "sales velocity", "are we on target", "KPI check".
category: Sales Coaching
tags: [kpis, scoreboard, closing-ratio, sales-velocity, quota, deal-telemetry]
tools: [hubspot]
---

Applies when someone wants the commercial truth about a rep or a team for a period, on demand. Produces one scoreboard, six KPIs, built from HubSpot deal timestamps rather than from anyone's recollection.

## The play

1. Resolve scope and period. Named rep: scope to that deal owner. No rep: whole team. No period: current month. State both at the top of the output before any number.
2. Resolve the pipeline. One sales pipeline in HubSpot: use it. Several: use the main sales pipeline and say which one was used. The user can name a different pipeline in the request.
3. Pull every relevant deal, filtered by owner and pipeline, with deal stage, stage-change timestamps, create date, close date, amount and pipeline. Stage-entry timestamps are the source for presentations, not the current stage.
4. Load targets. Prefer a native target or quota property in HubSpot. Otherwise read the client's targets document (one row per rep per period) from the client brain. Neither: show every other KPI and mark Position Against Target as "target not set".
5. Compute the six KPIs exactly as defined in references/kpi-definitions.md. The one most people get wrong: a presentation is any time the business was asked for cash, whichever call it happened on. All presentations in the period are the closing-ratio denominator, not just a particular call.
6. Handle the edges before publishing. A KPI with no underlying deals shows "n/a" and not 0, and never a divide-by-zero. Deals missing an amount or a close date are listed by name so the numbers are not silently skewed. A missing or stale targets document is stated, not guessed around.
7. Deliver the scoreboard: a one-line header (scope, period, pipeline), the six-row table, then a 2 to 3 line commercial read: what stands out, the biggest move to make, and any data-quality caveat.

## What good looks like

- First thing I check that most people skip: whether the presentation count came from stage-entry timestamps inside the period or from deals currently sitting in that stage. The second number is wrong and usually flattering.
- Second tell: whether closed-won deals with no amount were silently excluded. They drag average order value and billing down without anyone noticing.
- The mediocre version: a HubSpot report screenshot with a current-stage count, a closing ratio that only counts proposals from one call type, and no target line because nobody could find the targets document.
- I know the output is right when a manager can read the six rows and say the one move that would change the month, and the caveats at the bottom explain every number they would otherwise question.
- I know it has landed when the next conversation is about the move, not about whether the data is right.

## Rules

- MUST state scope, period and pipeline before any number.
- MUST count presentations from stage-entry timestamps inside the period.
- MUST use all presentations in the period as the closing-ratio denominator.
- MUST list deals missing amount or close date rather than drop them silently.
- NEVER show 0 for a KPI with no underlying deals. Show "n/a".
- NEVER guess a target. "Target not set" is an answer.
