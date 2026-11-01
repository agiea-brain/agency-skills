# The drift check

One check. A row has drifted when its Last activity is older than its newest log line. That happens when a log line or a row is written around the command: the command writes both together, so movements recorded through it stay in step.

## When it runs

- **At the start of every agent turn.** A hook runs the check in its quiet form before the agent reads the prompt. When the file is clean it prints nothing. When rows are stale it prints one line naming them and saying to fix them with a `move`. It has a short timeout, it never blocks the turn, and any failure inside it is swallowed, so it can never break a prompt.
- **On demand.** Run `drift` at any time.

It reads the open deals and channels tables. It changes nothing.

## What it prints

```
D4 <row name>: log <Day Mon D> vs row <Day Mon D>
```

One line per stale row, with the newest log date first and the row's date second.

## How the log date is read

The newest dated activity log line whose text, right after the timestamp, opens with the row's ID. A row with no log line is skipped.

## How the row date is read

The newest date that starts a sentence in the Last activity cell: at the start of the cell, or right after ". " or "; " (a closing quote or bracket before the space is allowed). A cell is a history, and its sentences are in no fixed order, so the leading date alone gives false alarms. `--leading` reads only the date at the very start of the cell, for when that literal reading is wanted.

A date is a month name and a day, with an optional weekday in front, or a full year-month-day. The year is the most recent one that puts the date on or before today. A stated weekday must match the date; if it matches in one nearby year, that year is used, and if it matches none, the date goes unread. A row with no readable date is skipped.

## Fixing a drift line

Run a `move` on the named row with a `--last` that records the movement in the log line. If the movement happened on an earlier day, start `--last` with that date, since a `--last` with no date gets the time of recording.
