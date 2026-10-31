# The three files

Plain text, in one folder, under version control if you have it. Nothing here needs a database.

## 1. pipeline.csv, current state

One row per live opportunity. Closed rows move to a separate file at the end of each quarter so the live file stays short enough to read in one screen.

| Field | Example | Why it exists |
|---|---|---|
| `account` | Vance Partners | The only identifier. No IDs. |
| `stage` | proposal | One of five, listed below. |
| `amount` | 24000 | Annual or total engagement value, your choice, used consistently. |
| `close_date` | 2026-12-15 | The date you believe, not the date you hope. |
| `next_step` | send proposal | A thing you do, not a thing that happens. |
| `next_step_date` | 2026-11-04 | The date that drives the drift check. |
| `last_activity` | 2026-10-29 | Written by the command, never by you. |
| `source` | referral, Cooper | Where it came from. Pays for itself inside a year. |

Eight fields. Resist the ninth.

**Stages**, five, deliberately coarse:

`conversation` → `scoping` → `proposal` → `verbal` → `closed`

`verbal` means they said yes and nothing is signed. It exists because the gap between verbal and signed is where small firms lose the most time and where the drift check earns its keep.

## What is deliberately missing

- **Probability percentages.** A number nobody can defend, averaged into a forecast nobody believes.
- **Contact records.** Your email already holds them.
- **Custom fields per deal type.** The pressure to add these is the pressure to buy a CRM.
- **Owner.** Add it only when more than one person sells.

## 2. activity.md, append-only

One line per event, newest at the bottom. Nothing is ever deleted or reordered.

```
2026-10-29 | Vance Partners | call | Scoping call. Wants proposal by the 12th. Budget confirmed ~25k.
2026-10-29 | Orbit Collective | email | Chased the signature. No reply in 9 days.
2026-10-30 | Vance Partners | note | Close date moved to Dec 15. Their legal review adds 3 weeks.
```

Four parts: date, account, type, what happened. Types: `call`, `email`, `meeting`, `note`, `proposal`, `signed`, `lost`.

The last field is the one that matters, and it is prose. Write what you would tell a colleague, not a status.

## 3. dashboard, generated

Rebuilt from the other two on every command. Never hand-edited, never the input to anything.

What it shows, in this order: total by stage, deals with a drift flag, deals with no activity in 14 days, next steps due this week, and what closed or was lost in the last 30 days. That order matches the order of a weekly review.

If a question cannot be answered from the two source files, it does not belong on the dashboard.
