---
name: pipeline-by-script
title: Pipeline by script
description: |
  Use this skill when a firm is too small for a CRM but keeps losing track of
  its own pipeline, and every deal update should take one command instead of
  ten minutes of clicking. Produces three files kept in sync by a single
  command: a pipeline row per opportunity, an append-only activity log, and a
  generated dashboard, plus a drift check that flags rows the log does not
  support. Also use for "track pipeline without a CRM", "log that call",
  "update the deal", "my CRM is a spreadsheet nobody fills in".
category: RevOps
tags: [pipeline, no-crm, activity-logging, dashboard, small-firm]
---

Applies to a firm running its own pipeline without a CRM, every time something happens on a deal. Produces one command that writes the pipeline row, the activity log and the dashboard together, and a check that catches them drifting apart.

## The play

1. Set up three files and never mix their jobs. The pipeline file holds one row per live opportunity and current state only. The activity file is append-only and holds what actually happened, one line per event. The dashboard is generated from the other two and is never written by hand. Fields and formats are in references/schema.md.
2. Run everything through one command that takes a plain sentence. "Had the scoping call with the Vance account, they want a proposal by the 12th" writes the activity line, updates the row's stage, next step and date, and regenerates the dashboard. One input, three writes, no second place to remember.
3. Never hand-edit the pipeline file or the dashboard. Hand edits are how a CRM rots, and a three-file setup rots faster because nothing validates them. Hand-edit only the activity log, and only to correct a typo in something already logged.
4. Let the log be the truth and the row be a summary of it. Any row state that no activity line supports is a guess. That rule is what makes the drift check possible at all.
5. Run the drift check on every command and once on a fixed day each week. It flags the row, the rule it broke and the last supporting activity, and it changes nothing on its own. The checks and their thresholds are in references/drift-rules.md.
6. Branch on what the check returns:
   - Next step dated in the past: the deal moved and nobody logged it, or it stalled. Either way the next command is a log entry, not a date change.
   - Stage advanced with no activity behind it: optimism. Roll the stage back to what the log supports.
   - No activity for longer than the deal's own cycle allows: the deal is quiet, not slow. Surface it in the weekly review.
   - Amount or close date changed with no note: always wrong. Every change to either carries a reason in the log.
7. Work the whole list once a week, in one sitting, from the dashboard. The dashboard exists for that half hour and nothing else. Example commands and the writes they produce are in references/command-recipes.md.

## What good looks like

- First thing I check that most people skip: the gap between the newest activity line and the oldest pipeline row. If the log is current and a row has not moved in a month, the problem is the deal. If the log itself is stale, the problem is the habit, and no tooling fixes that.
- The mediocre version: a spreadsheet with twenty columns, half of them empty, updated the night before a forecast conversation. It produces a number nobody can trace back to anything that happened.
- I know this is working when logging something takes under thirty seconds and happens while still on the call or straight after.
- Second test: the weekly review is a half hour of decisions, not a half hour of data entry. If the review is spent updating rows, the command is not being used.
- Red flag: the dashboard gets edited by hand. The moment that happens the generated file has become a fourth source of truth and the setup is finished.

## Rules

- MUST write all three files from one command, every time.
- MUST keep the activity log append-only.
- MUST make every amount or close-date change carry a reason in the log.
- MUST let the drift check report only. It never edits a row, closes a deal or deletes a line.
- MUST confirm with the person before any change that touches more than one row at a time.
- NEVER hand-edit the pipeline file or the dashboard.
- NEVER add a field without removing one. The setup survives on being smaller than a CRM, not on catching up with it.
