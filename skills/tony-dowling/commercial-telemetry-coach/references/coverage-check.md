# /check-coverage and /audit

## The maths, per rep per month

```
Booked %        = Booked ÷ Target            pass if ≥ 80% (M0), 55% (M+1), 35% (M+2)
Gap             = Target − Booked             floored at 0
Coverage ratio  = Stage 2+ pipeline closing in month ÷ Gap     pass if ≥ 3x
```

Total the team beneath the reps. A team that passes while two reps fail is two reps failing.

## Portfolio check, per rep

- Account count against the 50 cap.
- Split against 8 A / 15 B / 27 C, with up to 15 developmental flags.
- Accounts with no meaningful touch in 30 days: listed by name as eviction due.

Off-ratio, over cap or holding eviction-due accounts is flagged with the specific correction.

## Output layout

```
Rep: [name]
| Month | Target | Booked | Booked % | Benchmark | Pass/Fail | Gap | Stage 2+ Pipeline | Coverage | 3x Pass/Fail |
Portfolio: [n]/50 · A [n]/8 · B [n]/15 · C [n]/27 · Flags [n]/15 · Eviction due: [names or none]

(one block per rep, then Team)

On the floor this week
1. [Rep]: [activity count and type], because [month, gap, ratio].
2. ...

Headline: [one sentence on overall forward health]
```

## Turning a shortfall into activity

The prescription is the point of the check. Convert the gap into Call 1s, presentations or cash asks using the rep's own ratios from the Weekly_Commitments history (or the firm's measured ratios where the rep's are thin).

Example: "Danny is at 40% booked for M+1 with 1.5x coverage and a £12k gap. At his 3 Call 1s to 1 presentation and 2 presentations to 1 close at £6k, he needs two closes, four presentations, and twelve Call 1s landing before month end. Five Call 1 discovery appointments this week."

Rules for prescriptions:

- Name the rep, the month, the gap and the ratio.
- Give an activity count, not an intention.
- Coverage exists but is not booked: prescribe cash asks on the named deals.
- Coverage short: prescribe Call 1s, because nothing can be accelerated into a month with no pipeline.
- Over cap or eviction due: prescribe the releases alongside the activity, so the rep has room to work.

## /audit checklist

| Item | Pass when | Fail action |
|---|---|---|
| Menu for Sale present | The workshop output is in the document store and readable | Locate or rebuild it; nothing downstream grounds without it |
| Comeback Book present | Same | Same |
| Workbook updated within 7 days | Every tab's Updated date is inside 7 days | Refresh the stale tab before any coverage check |
| Portfolios within cap | Every rep at or under 50 | Release accounts to the house pool, named |
| Portfolios on split | Roughly 8/15/27 plus up to 15 flags | Re-tier, named |
| No eviction overdue | No account untouched for 30+ days | Release, named |

Report each item pass or fail, and for every fail the single next action and who takes it.
