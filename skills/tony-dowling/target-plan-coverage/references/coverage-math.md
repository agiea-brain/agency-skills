# Coverage maths

## The three-month horizon

| Month | Booked benchmark | Why |
|---|---|---|
| Month 0 (current) | 80% of target booked | Only 20% of the month can still come from pipeline; anything less means the month is already lost or already lucky |
| Month +1 | 55% booked | Half the month should already be contracted cash with four to eight weeks to go |
| Month +2 | 35% booked | A third contracted; the rest is what this quarter's Call 1s are for |

## Per month

```
Booked %          = Booked ÷ Target
Benchmark amount  = Target × (0.80 | 0.55 | 0.35)
Gap               = max(0, Benchmark amount − Booked)
Required coverage = 3 × Gap
Coverage ratio    = Stage 2+ pipeline closing in month ÷ Gap
Status            = on track      if Gap = 0
                  = covered       if ratio ≥ 3
                  = at risk       if 1.5 ≤ ratio < 3
                  = off track     if ratio < 1.5
```

Stage 2+ pipeline means deals where a presentation has happened and pricing is on the table, with a close date inside the month. Pipeline closing in a different month does not count toward this month.

## Source order

| Figure | First | Then | Then |
|---|---|---|---|
| Quota | Targets document in the client brain | HubSpot target or goal property | Ask |
| Booked | Revenue-position document in the client brain | Ask for the upload | Never pipeline |
| Stage 2+ definition | HubSpot forecast configuration | Stage definition in the client spreadsheet | Ask |

Duplicate rows for the same rep and month: most recent wins.

## Worked example

Rep: one account manager. Targets document: £40,000 a month. Revenue-position document: Month 0 booked £34,000, +1 booked £18,000, +2 booked £6,000. Stage 2+ pipeline by close month: £10,000, £28,000, £30,000.

| Month | Target | Booked | Booked % | Benchmark | Gap | Stage 2+ | Required 3x | Ratio | Status |
|---|---|---|---|---|---|---|---|---|---|
| M0 | £40,000 | £34,000 | 85% | 80% | £0 | £10,000 | £0 | n/a | on track |
| M+1 | £40,000 | £18,000 | 45% | 55% | £4,000 | £28,000 | £12,000 | 7.0x | covered |
| M+2 | £40,000 | £6,000 | 15% | 35% | £8,000 | £30,000 | £24,000 | 3.75x | covered |

Verdict: on track. Where to focus: M+1 has the cover but is not booked; the week's job is to close two of the £28,000, not to prospect. M+2 is covered on paper; check the three largest deals really have pricing on the table.

Change one number: M+2 Stage 2+ at £9,000 instead of £30,000. Ratio 1.1x, off track. The coaching flips: this week is five new Call 1s, because nothing in the pipeline can be accelerated into a month that has no pipeline.

## Output layout

```
Verdict: [on track | at risk | off track]  Rep: [name]  Anchor: [month]

| Month | Target | Booked | Booked % | Heuristic % | Gap | Stage 2+ Pipeline | Required 3x | Coverage Status |

Where to focus
- [2 to 4 bullets naming the month, the cause, and the move]

Sources: quota from [source]; booked from [source]; Stage 2+ per [source].
Needs cleanup: [deals missing amount or close date, by name]
```
