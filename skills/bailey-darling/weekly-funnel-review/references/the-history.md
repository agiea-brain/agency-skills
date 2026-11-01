# The history

One row per week, appended, never overwritten. The stored history is the whole point; a dashboard that only shows this week cannot answer whether anything is working.

## The row

| Column | Note |
|---|---|
| `week_ending` | Same weekday every week |
| `traffic` | Sessions, filtered |
| `outbound_sent` | Total, plus a column per channel |
| `inbound` | Enquiries not from outbound |
| `calls_booked` | From the calendar |
| `calls_held` | From the sales tracker |
| `no_shows` | Booked minus held, stored rather than derived |
| `fit` | Held calls with a deal record |
| `opportunities` | Fit calls with a dated next step |
| `signed_current` | Current motion |
| `signed_legacy` | Everything predating it |
| `revenue_current` | |
| `revenue_legacy` | |
| `note` | One line, what changed and why |

Store `no_shows` rather than computing it at read time. If a definition changes later, a derived column silently rewrites history and a stored one does not.

## Reading it

Three comparisons, in this order:

1. **This week against last week.** Catches the thing that broke.
2. **This week against the four-week average.** Tells you whether it matters.
3. **The trend since the start date.** The only one that answers whether the motion is working.

Most weekly reviews only do the first, which is why they produce alarm rather than information.

## Conversion rates, not just counts

Calculate three every week and store them:

- Held divided by booked, the show rate
- Fit divided by held, the targeting rate
- Signed divided by fit, the close rate

A funnel can be flat on volume and improving sharply on all three, which is what a repositioning looks like in its first two months. Volume-only tracking misses it and the repositioning gets reversed.

## The note column

One line. What changed and why, in plain words.

> "Held down 4, three reschedules into next week, not a demand issue."

Read back six months later, the note column explains the shape of the chart better than any dashboard does. It is also the first thing skipped when busy, and worth protecting.

## Same day, same time

Monday morning works because the week is closed and the next one has not started. Any fixed day works. A review that slips by two days twice stops being a series.

Thirty minutes, including the note. If it regularly takes longer, the sources are the problem, not the review.

## What not to add

The pressure is always to add columns. Resist it. A twelve-column history filled in every week beats a thirty-column one filled in for six weeks and then abandoned, and the abandonment is what actually happens.

Anything that needs its own investigation to fill in does not belong in a weekly row.
