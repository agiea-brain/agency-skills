---
name: weekly-funnel-review
title: Weekly funnel review
description: |
  Use this skill on the same day every week to see where new business
  actually comes from, when the numbers live in five different places and
  nobody agrees what a qualified call is. Produces one row per week,
  appended to a running history: traffic and outbound by channel, calls
  booked against calls held, fit, signed work, and revenue split by
  segment, with the one thing that changed. Also use for "weekly numbers",
  "where are leads coming from", "how many calls did we hold", "refresh the
  funnel".
category: RevOps
tags: [funnel, weekly-cadence, pipeline-metrics, attribution, reporting]
---

Applies on a fixed weekday, every week, to the firm's own new-business funnel. Produces one appended row and a short read of what moved.

## The play

1. Name one source of truth per metric before measuring anything, and write the list down. Two systems will always disagree about how many calls happened, and a week spent arguing about which is right is a week with no numbers. The rules for choosing, and the ones worth copying, are in references/definitions.md.
2. Fix the start date of the history and never move it. A rolling twelve-week window hides the trend that matters after a repositioning or a new service launch. Pick the date the current motion began and count from there.
3. Pull the stages in order: traffic, outbound activity by channel and by sender, calls booked, calls held, fit, opportunities, signed, revenue. The full chain and what each stage must exclude are in references/definitions.md.
4. Record booked and held as separate numbers, every week, from different sources. The gap between them is the no-show rate, it is usually the largest unmanaged leak in a small firm's funnel, and it is invisible to anyone tracking only one of the two.
5. Split revenue by segment, not as a single total. A legacy base and a new motion inside one number means the new motion is unreadable for a year. The split to use is in references/definitions.md.
6. Append the week to the history rather than overwriting a dashboard. A dashboard showing only this week cannot answer whether anything is working, and the history is the entire value of doing this weekly.
7. Branch by what the week shows:
   - A stage down with everything above it flat: a conversion problem at that stage. Look there, not at the top.
   - Everything down together: an input problem. Check whether the outbound actually went out.
   - Calls booked up, held flat: a no-show problem, which is a booking and reminder problem, not a demand problem.
   - A channel at zero that was not zero: check it ran before concluding anything about demand.
   - One channel producing everything: note the concentration. It is a risk even in a good week.
8. Write one line on what changed and why, and nothing else. The numbers are the artifact; the commentary is for the one thing a reader would otherwise have to work out themselves.

## What good looks like

- First thing I check that most people skip: booked minus held. Everyone tracks calls booked because it feels like progress, and the no-shows quietly delete a third of the week.
- The mediocre version: a dashboard rebuilt from scratch each week, with whatever metrics were handy, no stored history, and no fixed definitions. It produces a number nobody can compare to anything.
- I know the review is working when a disagreement about a number ends by naming the source rather than by debating the number.
- Second test: the history can answer "has this channel ever worked" without anyone opening another system.
- Red flag: a definition changing mid-quarter. Whatever the reason, the history before and after is no longer one series, and the change needs noting in the record.

## Rules

- MUST name one source of truth per metric and keep it fixed.
- MUST record booked and held separately, from different sources.
- MUST append each week to a stored history, never overwrite.
- MUST split revenue by segment.
- MUST keep the start date of the history fixed.
- MUST note any definition change in the record, with the date.
- NEVER compare a stage to a stage measured a different way.
- NEVER let a channel with no activity read as a channel with no demand.
