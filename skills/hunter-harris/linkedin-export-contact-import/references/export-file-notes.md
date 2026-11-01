# Export file notes

## Which file gives what

| File | In basic | Use | Watch for |
|---|---|---|---|
| `Connections.csv` | yes | name, profile URL, company, position, email (rarely), Connected On | notes above the header; hidden members are blank except Connected On |
| `Invitations.csv` | yes | invites you sent | keep rows whose `Direction` is `OUTGOING`; the message column is your note |
| `messages.csv` | yes | DMs | drafts (`IS MESSAGE DRAFT`), a SPAM folder, group threads |
| `Comments_<id>.csv` | complete only | your comments on others' posts | none of the basic export's people data |
| `Shares_<id>.csv`, `Reactions_<id>.csv` | complete only | your posts and reactions | not needed for contacts |

## Parsing

- **Header.** Find the line starting `First Name,Last Name,` and read from there. Hard-coding "skip 3 lines" works until LinkedIn edits the note.
- **Dates differ between files.** Seen across the export: `30 Jul 2026`, `2026-07-31 20:19:20 UTC`, `7/29/26, 1:59 PM`, `5/19/2026 2:06:34`. Try each format explicitly; don't let a parser guess day versus month.
- **Spaces.** The basic and complete exports encode the same visible space differently (non-breaking spaces in one). Normalize whitespace before comparing names or text, or the same row imports twice.
- **Group threads.** A thread is one-to-one when it has exactly one participant besides you.

## Dedupe

- One touch per person, channel, direction and day. Re-importing the same export must add nothing.
- A person's key: the profile URL slug. An exact name that matches one contact is only a candidate; list it for confirmation.

## First import versus weekly

- **First import** is a backfill. Nothing in it is "newly accepted": there's no previous export to compare against. Don't trigger follow-ups from it.
- **Weekly**, compare against the last export to find newly accepted invitations and new messages.
- Apply the 60-day rule for status changes: only messages within 60 days of the export's newest message can move someone to "in conversation".

## The common failure

The export gets downloaded and sits in a folder. Make the import a step of the weekly routine that checks for a newer export first, rather than waiting for someone to remember.
