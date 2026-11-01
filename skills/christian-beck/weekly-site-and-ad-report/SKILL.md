---
name: weekly-site-and-ad-report
title: Weekly site and ad report
description: |
  Use this skill on the fixed day each week when a client's site traffic and
  paid campaigns need reporting, and the report has to say what to do rather
  than what happened. Produces a short report: the five numbers that matter
  against last week and the four-week average, what moved and why, and one
  recommendation per channel the client can act on. Also use for "weekly
  report for [client]", "how did the ads do last week", "pull the traffic
  numbers", "marketing report".
category: Marketing
tags: [reporting, analytics, paid-media, weekly-cadence, client-reporting]
tools: [google-analytics, google-ads, meta-ads]
---

Applies on the same day every week, per client. Produces a one-screen report that leads with what changed and ends with what to do about it.

## The play

1. Pull the same five numbers every week, per client, from the same sources. Sessions, conversions, conversion rate, spend, and cost per conversion. The definitions and where each comes from are in references/metrics.md, and the definitions do not change once set, because a redefined metric erases the history that makes the report worth reading.
2. Set every number against two baselines, not one: last week, and the four-week rolling average. Week on week catches the spike, the rolling average tells you whether the spike matters. A number reported on its own is decoration.
3. Flag only what moved beyond normal variance for that client. The thresholds, and how to work out a client's own normal variance from their first eight weeks, are in references/thresholds.md. A small site will swing 30% on nothing at all, and reporting that swing as a finding teaches the client to ignore the report.
4. Explain each flagged move before writing a word of recommendation. Work the list in references/thresholds.md in order: tracking broken, a change you shipped, a change they shipped, seasonality or a calendar event, then the market. Most weeks the answer is in the first three, and the discipline is to rule those out rather than reach for the interesting explanation.
5. Branch by what is running:
   - Paid live, spend steady, cost per conversion moving: it is creative fatigue or auction pressure. Look at frequency and impression share before touching the budget.
   - Paid live and newly launched: report learning-phase numbers as directional only, and say so. A recommendation off four days of data is a guess with a chart behind it.
   - No paid this week: the report is shorter, not padded. Organic and conversion rate only.
   - A campaign launched or ended mid-week: name the date on the chart. Unlabelled, it reads as a trend forever after.
6. Write one recommendation per channel. Each names the action, the expected effect and who does it. Three recommendations a client acts on beat twelve observations they skim. The report format is in references/report-format.md.
7. Carry last week's recommendations forward with their outcome. A report that never checks its own previous advice is a newsletter.

## What good looks like

- First thing I check that most people skip: whether tracking is still working before reading a single number. A conversion drop to zero is a broken tag far more often than a dead channel, and nothing is more expensive than a recommendation built on a broken pixel.
- The mediocre version: an exported dashboard with twenty metrics, every one of them up or down in green and red, no explanation, and a closing line that says we will continue to monitor. It takes two minutes to generate and gives the client nothing to decide.
- I know the report is right when the client replies about a recommendation rather than a number.
- Second test: someone could read only the first three lines and know whether the week was good, bad or flat.
- Red flag: the same recommendation appearing three weeks running. Either it was never actioned, which is a conversation, or it was wrong.

## Rules

- MUST verify tracking before reading the numbers.
- MUST show every number against both last week and the four-week average.
- MUST keep the metric definitions fixed once set.
- MUST explain a move before recommending anything, ruling out tracking and shipped changes first.
- MUST carry forward last week's recommendations with their outcome.
- MUST label a newly launched campaign's numbers as directional.
- NEVER report a move inside normal variance as a finding.
- NEVER send a report whose only recommendation is to keep monitoring.
