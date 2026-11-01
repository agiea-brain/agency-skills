# Command recipes

One command, a plain sentence in, three files updated. These are the inputs that come up and what each should write.

## A call happened

> "Scoping call with Vance Partners. They want a proposal by the 12th, budget around 25k."

- **activity**: `call` line, verbatim substance
- **pipeline**: `stage` → scoping, `next_step` → send proposal, `next_step_date` → the 12th, `amount` → 24000 if not set, `last_activity` → today
- **dashboard**: regenerate

Note the amount is only filled when the row is empty. An existing amount is never overwritten from a casual mention; that needs its own explicit input, because of drift check 5.

## A date slipped

> "Vance close date moves to Dec 15, their legal review adds three weeks."

- **activity**: `note` line including the reason
- **pipeline**: `close_date` → 2026-12-15

The reason is not optional. A date change with no note trips the check, and the check exists because unexplained date moves are how a forecast drifts a quarter at a time.

## Nothing happened, and that is the update

> "Chased Orbit again, still nothing, nine days now."

- **activity**: `email` line
- **pipeline**: `last_activity` only

Nothing else moves. Silence is an event worth logging and never a reason to change a stage.

## It closed

> "Vance signed."

- **activity**: `signed` line
- **pipeline**: `stage` → closed, `next_step` cleared

The row stays in the live file until quarter end, then moves to the closed file. Keeping it visible for a few weeks is what makes the source field worth having.

## It died

> "Orbit went with someone in-house. Lost."

- **activity**: `lost` line, with the reason in the prose
- **pipeline**: `stage` → closed

Reason in the prose, not a field. A dropdown of loss reasons produces five values that all mean "price".

## A new one

> "Intro call booked with Harbour Studio, came through Cooper."

- **activity**: `note` line
- **pipeline**: new row, stage conversation, `source` → referral, Cooper, `next_step` → intro call with its date

`amount` and `close_date` stay empty. Guessing them at the intro stage puts a number in a forecast that nothing supports.

## Rules the command follows

- Append to the activity log, never rewrite it.
- One input, one account. A sentence naming two accounts is two commands.
- Any change touching more than one row stops and asks first.
- Unparseable input writes nothing and says what was unclear. A half-written update is worse than none.
- Never invent a date. "Next week" with no day asks, or writes the next Friday and says it did.
