---
name: pipeline-by-script
title: Pipeline by script
description: |
  Use this skill when a small firm runs its pipeline from its own folder with
  no CRM and an agent records what happens on each deal. Every movement (a
  send, a reply, a booking, a decision that changes the next step or whose
  move it is) goes in through one script command that writes the pipeline
  row, the activity log line, an archive copy and the rebuilt dashboard
  together, and a drift check at the start of every agent turn names any row
  left behind its log line. Produces one Markdown pipeline file (open deals,
  channels, clients won, closed, and a dated activity log), a generated
  dashboard whose weekly counts come from event tags, and the commands that
  keep them in step. Also use for "log that reply", "move the deal", "add
  this to the pipeline", "close it out", "update the client row", "track
  pipeline without a CRM", "why is this row out of date".
category: RevOps
tags: [pipeline, no-crm, activity-logging, dashboard, small-firm, drift-check]
---

Applies whenever something moves on a deal, a channel or a client at a small firm that keeps its pipeline in one Markdown file and runs no CRM. Produces one recorded movement: the row, the activity log line, an archive copy and the rebuilt dashboard, written together by one command.

## The play

1. Keep the whole pipeline in one Markdown file: open deals, channels (doors that could lead to deals, kept apart from deals), clients won, closed, and an activity log with the newest line first. A dashboard is generated from it. Tables, columns, IDs and archive copies are in references/file-layout.md.
2. Treat the agent as the interface. The person says what happened in a sentence. The agent turns it into one command with every field explicit: row ID, Last activity, next step, next date, whose move, log text and event tags. The script reads no prose and guesses no field; the only date it supplies is the time of recording, in front of a Last activity entry that starts without one. When the sentence leaves a needed field open, the agent asks.
3. Pick the subcommand by what happened:
   - Something moved on an open deal or a channel: `move`.
   - A new deal or a new door: `add`, with every column given. The script assigns the next free ID.
   - A deal or a door ended: `close`, with the outcome. The row moves to the closed table and its ID is retired.
   - Something changed on a won client: `client`, found by account name.
   Each writes the row and a timestamped log line together, keeps a copy of the file as it stood, and rebuilds the dashboard. A scheduled daily run rebuilds it too. Flags, refusals and a worked example are in references/one-command.md.
4. Tag every `move`, `add` and `client` with what happened, from a fixed set of ten: sent, received, held, booked, ask, price, yes, post, intro, other. The flag repeats. The dashboard computes the week's counts from these tags. An untagged line counts only on an uppercase marker such as SENT, HELD or BOOKED, and asks, prices, yeses and posts come from tags alone.
5. Record in the same turn the movement is seen. A send, a reply, a booking, and a decision that changes the next step or whose move it is all count as movements.
6. Let the drift check run at the start of every agent turn. A hook runs it and prints a line only when a row is stale: its Last activity is older than its newest log line. The check names the row and changes nothing. The fix is a `move` on that row. How each date is read is in references/drift-check.md.
7. When the script refuses, it writes nothing and says why. Correct the command and run it again.
8. When a movement turns up that no subcommand can record, extend the script. New deals, closes and client rows each became a subcommand once hand edits to them were the last movements the script could not record. Test the change on a scratch copy of the file; `check` prints the parse counts.

## What good looks like

- First thing I check: whether the turn opened with a drift line. The check is silent when the file is clean, so a drift line means someone wrote a row or a log line around the command. I fix it with a `move` on that row first.
- The mediocre version is rows and log lines edited by hand. They drift apart, which is why I built the script.
- I know it is working when the week's counts come straight off the dashboard, because every line carries its event tags and nobody counts by hand.
- Every row says whose move it is. A change to that is a movement, and I record it like a send or a reply.

## Rules

- MUST record every movement through the command, in the same turn it is seen.
- MUST name the events on every `move`, `add` and `client`, from the fixed set.
- MUST pass every field explicitly, and ask the person for any field the sentence left open.
- MUST fix a drift line with a `move` on the named row.
- MUST test any change to the script on a scratch copy of the pipeline file.
- NEVER edit a pipeline row or an activity log line by hand.
- NEVER edit the dashboard directly. Every write rebuilds it from the file.
- NEVER reuse a closed ID.
- NEVER let the drift check change the file or block a turn. It reports, and the agent acts.
