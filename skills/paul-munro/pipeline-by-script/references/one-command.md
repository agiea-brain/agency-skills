# One command

The script has six subcommands. Four of them record movements, and each of those writes the row and one timestamped log line together, keeps an archive copy of the file as it stood, writes the file, and rebuilds the dashboard. A refusal writes nothing.

## From a sentence to a command

The person speaks in a sentence. The agent writes the command, with every field explicit and every date concrete.

> "Sent the proposal to them this morning. It's on them now. I'll follow up Friday if I hear nothing."

```
move D4 --last "Proposal sent" --next "Follow up on the proposal" \
  --date "<Mon D of that Friday>" --whose "Theirs" \
  --log "Proposal sent; their move" --event sent --event price
```

The agent resolves "Friday" to a date before it runs the command. If the sentence did not say which row, or left the next step open, the agent asks.

## move

`move ID --log TEXT` plus at least one cell: `--last`, `--next`, `--date`, `--whose`, `--stage`, `--offer` (Could lead to, on a channel), `--value`, `--status`. Optional: `--replace-last`, `--event TYPE` (repeatable).

- Finds the row by ID in the open deals or channels table.
- Replaces only the cells given.
- `--last` goes in front of the existing Last activity, joined by ". ". `--replace-last` overwrites the cell instead.
- A `--last` that starts without a date gets the time of recording put in front, in the form "Mon D, H:MM AM TZ: ", so the drift check can read it. To record a movement from an earlier day, start `--last` with that date.
- A `--log` text that opens with the row's ID has that copy trimmed, since the timestamp already carries the ID.

## add

`add --log TEXT` plus every column: `--account` (the Door, on a channel), `--contact`, `--source`, `--offer` (Could lead to, on a channel), `--stage`, `--last`, `--next`, `--date`, `--whose`, and `--size` and `--value` for a deal or `--status` for a channel. Optional: `--table deals|channels` (deals by default), `--id`, `--event TYPE`.

- Every column needs a value. A missing one refuses and names it.
- The ID is the next free D or C number unless `--id` is given. An ID that already exists refuses.
- The log line reads "ID NEW ROW, <text>".

## close

`close ID --outcome TEXT --log TEXT`, optional `--closed TEXT` (today's "Mon D" by default).

- Removes the row from open deals or channels and appends "<name> (<ID>)", the closed day and the outcome to the closed table.
- The log line reads "ID CLOSED, <text>".
- The ID is retired.

## client

`client ACCOUNT --log TEXT` plus at least one of `--contact`, `--live` (What is live), `--billing`, `--next`. Optional: `--event TYPE`.

- Finds the row whose Account cell equals ACCOUNT, or starts with it followed by a space or " (", ignoring case.
- No match refuses and lists the accounts. More than one match refuses and asks for a longer name.
- Each cell given is replaced in full.
- The log line names the account, without any "(past)".

## drift and check

`drift` prints one line per row whose Last activity is older than its newest log line, and nothing when the file is clean. `--quiet` is the form the hook runs. `--leading` reads only the date at the very start of the cell. Details in drift-check.md.

`check` prints, for each table, the rows, the columns and the rows it could not read, then the number of log lines, then OK or FAIL.

A workspace option points any subcommand at another folder. Tests run that way, on a scratch copy.

## Refusals

The script refuses, and writes nothing, when:

- the ID is not in the open deals or channels table, or a new ID already exists or is not a letter and a number;
- no cell was given;
- a flag names a column the table lacks;
- a value holds a line break (a row stays on one line);
- the new row would have a different number of cells than the header (a pipe in a value is escaped first);
- a needed heading or table is missing from the file.

## Event tags

`--event` works on `move`, `add` and `client`, and repeats. The fixed set is sent, received, held, booked, ask, price, yes, post, intro and other. The log line then ends " [events: sent, price]". Without `--event` the line carries no tag.

The weekly record computes its counts from dated log lines in the week:

| Tag | Counts toward |
|---|---|
| sent | notes sent |
| held | sessions held; on a deal row, buyer conversations held too |
| received, intro, booked | came in |
| ask | asks made |
| price | priced asks |
| yes | paid yeses |
| post | posts published |
| other | recorded, counted toward no total |

An untagged line counts only on an uppercase marker: SENT, HELD, BOOKED, or a reply marker such as REPLIED. "NOT sent" counts as nothing. Asks, priced asks, paid yeses and posts come from tags alone, so a week with no tagged lines leaves those counts empty. The record's own note says how many lines were counted by tag, how many by marker, and how many went uncounted.

Commitments due and kept, and new clients, come from comparing archive copies (see file-layout.md). A commitment is a row whose next date fell in the week. It counts as kept when the row's Last activity or a log line for it is dated on or after that next date, within the week. A new client is an account new to the clients won table that week. A row added already marked "(past)" records an old engagement and counts as no win.
