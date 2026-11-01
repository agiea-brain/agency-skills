# Drift checks

Drift is a pipeline row claiming something the activity log does not support. The check reports it and stops there. It never edits a row, advances a stage, closes a deal or deletes a line.

## The checks

| # | Check | Threshold | What it usually means |
|---|---|---|---|
| 1 | `next_step_date` is in the past | 1 day | The thing happened and went unlogged, or it did not happen |
| 2 | `stage` advanced with no activity line on or after the change | any | Optimism. Roll the stage back. |
| 3 | No activity on a live row | 14 days, or 7 at `verbal` | Quiet, not slow |
| 4 | `close_date` changed with no `note` within a day | any | A date moved for a reason nobody wrote down |
| 5 | `amount` changed with no `note` within a day | any | Same, and worse |
| 6 | `close_date` is in the past, stage is not `closed` | 1 day | The forecast is now fiction |
| 7 | Row at `verbal` | 21 days | The signature gap. The most expensive flag here. |
| 8 | `next_step` reads as a thing that happens, not a thing you do | any | "Waiting to hear back" is not a next step |
| 9 | Row has no `source` | any | Fix it now, while you still remember |

## Reading the output

Each flag prints the account, the rule, and the last activity line that bears on it. Three fields, so the fix is obvious without opening anything:

```
Orbit Collective   [3] no activity 19 days
  last: 2026-10-11 | email | Chased the signature. No reply in 9 days.

Vance Partners     [1] next step 4 days overdue
  last: 2026-10-30 | note | Close date moved to Dec 15.
```

## Thresholds are per firm

The 14 days in check 3 assumes a sales cycle measured in weeks. Halve it for transactional work, double it for engagements that run a quarter to close. Set it once from your own closed-won history: the longest gap between touches on a deal that still closed, rounded up.

Check 7, the 21 days at `verbal`, is the one not to loosen. Deals do not sit at verbal because everyone is busy.

## What is not a drift check

- Anything that scores or ranks a deal. This file answers whether the record is honest, not whether the deal is good.
- Anything that acts. The moment a check can edit a row, the log stops being the truth.
- Reminders to follow up. A flag is evidence; what to do about it is the weekly review.

## When the list gets long

More than five flags means the habit slipped, not that five deals went wrong. Clear it by logging what actually happened, one line each, then rerun. Resolving flags by editing rows to match is the exact failure this is built to prevent.
