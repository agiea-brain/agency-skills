---
name: revenue-goal-funnel-math
title: Revenue goal funnel math
description: |
  Use this skill when a founder sets a revenue or income goal and needs to know
  what it takes each week, or when a weekly review shows the goal slipping.
  Produces a backwards funnel from the goal down to weekly outreach volume,
  the actual-versus-required gap at every stage, and the one bottleneck to fix
  this week. Also use for "how many calls do I need", "reverse funnel", "goal
  math", "what's the bottleneck", "are we on pace", "weekly pipeline review".
category: Strategy
tags: [funnel-math, pipeline, founder-led-sales, weekly-review, bottleneck, b2b-services]
---

Applies when there is a number to hit and nobody has worked out what it means for this week. Produces one page: the chain from goal to touches, required versus actual at each step, and one named bottleneck.

## The play

1. Anchor the goal. If it is the owner's income, convert it first: income ÷ owner's share of profit ÷ margin = revenue needed. A revenue goal that pays the owner too little is a failed plan, so check this before going further.
2. Work backwards, one link at a time, using the chain in references/funnel-chain.md:
   - Revenue → clients needed (÷ average monthly value per client).
   - Clients → closes per month (net adds + expected churn).
   - Closes → proposals (÷ proposal-to-close rate).
   - Proposals → discovery calls held (÷ discovery-to-proposal rate).
   - Discovery calls → replies (÷ reply-to-call rate).
   - Replies → touches (÷ reply rate).
   - Divide by 4 for the weekly number.
3. Use measured rates, not hoped-for ones. Where you have fewer than 10 settled outcomes for a stage, use the planning defaults in references/thresholds.md and mark them as assumed.
4. Split the sales call stage in two: discovery and proposal. One "close rate" hides which call is broken. A 13% overall rate could be 60% × 22% (a proposal problem) or 30% × 43% (a discovery problem). The fixes are opposite.
5. Pull the trailing 7 days and the trailing 28 days of actuals for every stage. Put required and actual side by side.
6. Name the bottleneck. Compare each stage with the alarm lines in references/thresholds.md. If several are broken, pick the one furthest upstream. Fixing close rate with no calls on the calendar is theatre.
7. Write 3 to 5 actions, each dated, each tied to the bottleneck stage. "By Friday, rewrite the first touch for the two lowest-reply segments" is an action. "Improve reply rate" is not.
8. Re-run monthly. If a measured rate differs from the planning default for two months in a row, replace the default. A model that flatters you is worse than none.

Worked examples are in references/worked-examples.md.

## What good looks like

- First thing I check that most people skip: whether the close rate in the model is measured or assumed. It is usually assumed, usually 25%, and usually generous. Halve it and the required call volume doubles.
- The mediocre version: a top-down plan ("we need 10 clients") with no weekly touch number, one blended close rate, and three things to fix at once. It feels like a plan and changes nothing on Monday.
- I know the math is right when the owner can say one line from memory: "X touches a week → Y replies → Z calls → 1 close." If they cannot say that line, the review did not land.
- I know the review worked when next week's actuals moved on the one stage named, and nobody touched the others.

## Rules

- MUST split discovery and proposal into separate stages.
- MUST label every rate as measured (with sample size) or assumed.
- MUST name exactly one bottleneck per review.
- MUST pick the most upstream broken stage when several are below the line.
- NEVER count a proposal that was not actually delivered. A fake proposal in the funnel corrupts every rate below it.
- NEVER set a revenue goal without checking what it pays the owner.
