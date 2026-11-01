# File layout

One Markdown file holds the whole pipeline. Each part sits under a level-two heading, with one table below it, and the script finds each part by the start of its heading text. Columns are found the same way, by the start of the header name, so a header can carry a short note in brackets, as in `Stage (since)`. A generated dashboard and a folder of archive copies sit beside the file.

## Open deals

Heading starts with `Deals, open`.

| ID | Account | Contact (function) | Size | Source | Offer | Value | Stage (since) | Last activity | Next step | Next date | Whose move |
|---|---|---|---|---|---|---|---|---|---|---|---|

- **Last activity** holds dated sentences. Each `move` puts the new one in front of the old, joined by ". ", so the cell reads as a short history. The drift check reads its dates.
- **Next step** and **Next date** say what happens next and when.
- **Whose move** says who acts next. A change here is a movement, recorded like any other.

## Channels

Heading starts with `Channels`. A channel is a door that could lead to deals. Doors live in their own table so the deals table holds deals only.

| ID | Door | Contact (type) | Source | Could lead to | Status | Last activity | Next step | Next date | Whose move |
|---|---|---|---|---|---|---|---|---|---|

Status takes the place of Size and Value. The dashboard reads four statuses: Active, Waiting, Dormant and Closed.

## Clients (won)

| Account | Contact | What is live | Billing | Next |
|---|---|---|---|---|

This table has no ID column. The `client` subcommand finds a row by its Account cell. An account name ending in "(past)" marks an engagement that has ended. The cells are descriptions, so each update replaces a cell in full.

## Closed

| Record | Closed | Outcome |
|---|---|---|

`close` writes the Record cell as the row's name with its ID in brackets, the Closed cell as the day it closed, and the Outcome in the person's words.

## Activity log

Heading starts with `Activity log`. Newest line first, one line per movement:

```
- YYYY-MM-DD, H:MM AM TZ: D7 <what happened> [events: sent, price]
- YYYY-MM-DD, H:MM AM TZ: C3 NEW ROW, <why the door was added> [events: intro]
- YYYY-MM-DD, H:MM AM TZ: D5 CLOSED, <outcome and why>
- YYYY-MM-DD, H:MM AM TZ: <Account> <what changed> [events: yes]
```

The ID right after the timestamp is what ties a line to its row. Client lines carry the account name in its place. The events tag closes the line when the command names events.

## IDs

An ID is one capital letter and a number. Open deals take D numbers and channels take C numbers. `add` assigns the next free number in that series unless an ID is given. A closed ID stays retired, so every log line keeps pointing at one record.

## The dashboard

A builder script reads the pipeline file and the archive copies and writes a dashboard page into its own folder, and nothing outside it. Its parsing is deterministic: anything it cannot read shows as "not logged" or as the raw text. Every command rebuilds it, and a scheduled daily run rebuilds it as well. If the firm publishes the dashboard somewhere, the command's output carries a reminder to republish it.

Each render also writes a weekly record for the most recent Friday, covering Saturday to Friday. A record for that week that came from another source is left alone. What the record counts is in one-command.md.

## Archive copies

Before every write, the script copies the file as it stood into an archive folder, named with the date and minute (a number is added when two writes share a minute). It then writes to a temporary file and swaps it in, so the pipeline file is always whole.

The copies give the weekly record its starting point. It compares the copy from just before the week began (taken within the seven days before the week) with the file at the week's end. That comparison yields the week's commitments due and kept, and its new clients. With no copy in that window, those counts stay empty.
