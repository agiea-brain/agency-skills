---
name: target-plan-coverage
title: Target plan and coverage
description: |
  Use this skill when a rep or a manager needs to know whether the next three
  months are covered: Monday planning, a monthly review, or any "are we going
  to hit it" question. Produces a per-month table for Month 0, +1 and +2 with
  target, booked revenue, the 80/55/35 booked benchmark, the gap, qualified
  pipeline and the 3x coverage verdict, plus where to focus. Also use for
  "pipeline coverage", "target plan", "booked versus target", "gap to target",
  "am I on track for next month", "Monday coverage run".
category: Sales Coaching
tags: [pipeline-coverage, target-plan, 80-55-35, forecasting, booked-revenue, monday-review]
tools: [hubspot]
---

Applies when the question is forward: not "how did last month go" but "is the next quarter covered". Produces one verdict (on track, at risk, off track), a three-month table, and 2 to 4 lines on where this rep should spend the week.

## The play

1. Scope. Which rep, which anchor month. Default to the requester's own book and the current month. Month 0 is the anchor, +1 and +2 follow.
2. Quotas. Read monthly rep quotas from the client's targets document in the client brain (one row per rep per month). Not there: HubSpot. Neither: ask. State the source of every figure in the output.
3. Booked revenue. Read actual contracted revenue per rep per month from the client's revenue-position document in the client brain. Do not infer booked revenue from HubSpot stages, however confident the stage names sound. No document: ask for it to be uploaded; do not substitute pipeline.
4. Open pipeline. Pull open HubSpot deals per rep by close date for each of the three months, with stage, amount and close date.
5. Qualified pipeline (Stage 2+). Count only stages HubSpot's forecast configuration treats as comfortably forecast. Not configured: use the stage definition in the client spreadsheet. Neither: ask. A deal is Stage 2+ when a presentation has happened and pricing is on the table; nothing earlier qualifies.
6. Per month compute Booked, Target, Booked % and the benchmark: Month 0 needs 80% booked, +1 needs 55%, +2 needs 35%. Maths and a worked case in references/coverage-math.md.
7. Gap = benchmark amount minus Booked, floored at zero. Booked at or above the benchmark: mark the month "on track" and move on.
8. Required coverage = 3 × Gap in Stage 2+ pipeline closing in that month. Compare with actual Stage 2+ pipeline. Report ratio and surplus or shortfall.
9. Coach. Which month is most at risk, and is it a booked shortfall or thin pipeline? Coverage exists but is not booked: accelerate late-stage deals. Coverage short: generate new Call 1s this week. Give 2 to 4 bullets, specific to the deals and the numbers.

Edge cases: no deals for a rep in a month is a critical gap, not an error. Duplicate quota or booked rows: use the most recent. Deals missing amount or close date: list under "needs cleanup", excluded from the maths. On the scheduled Monday run, produce one summary per rep, led by a roll-up of which reps are most at risk.

## What good looks like

- First thing I check that most people skip: whether "booked" came from the revenue-position document or from a HubSpot stage called something like "Verbal". Booked is contracted cash. Everything else is pipeline, however warm.
- Second tell: whether Month +2 was looked at at all. Most reviews stop at the current month, which is the one month nobody can still change much.
- The mediocre version: a current-month forecast with a weighted pipeline number, no booked line, one coverage figure for the whole quarter, and advice to "keep pushing".
- I know the output is right when each month has its own verdict and the coaching names which deals to accelerate or how many Call 1s to book, not "build pipeline".
- I know it has landed when the rep's Monday commitments match the month this review flagged.

## Rules

- MUST take booked revenue from the revenue-position document, never from CRM stages.
- MUST state the source of every quota and booked figure.
- MUST apply 80/55/35 to Month 0, +1, +2 in that order.
- MUST require 3x the gap in Stage 2+ pipeline, closing in that month.
- NEVER count a deal as Stage 2+ unless a presentation has happened and pricing is on the table.
- NEVER treat a rep with no deals in a month as an error. It is the finding.
