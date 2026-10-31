---
name: ceo-exec-assistant
title: CEO exec assistant
description: |
  Use this skill when the person running a small agency needs to know what
  the week actually demands, pulled from the project tool and the calendar
  rather than from memory. Produces a short brief: what is committed today
  and this week, what is at risk, what the calendar makes impossible, and
  the three things to do first. Also use for "what's on this week", "am I
  missing anything", "catch me up before Monday", "what's slipping".
category: Operations
tags: [exec-assistant, weekly-planning, agency-ops, prioritization]
tools: [asana, google-calendar]
---

Applies at the start of the week, or any morning the day has got away from its owner. Produces a brief read in two minutes that names what to do first and what will not happen.

## The play

1. Pull two sources and nothing else. From Asana, every task assigned to them or where they are the approver, with due dates inside the next ten days. From Google Calendar, the week's committed hours. Email is not a source here; email is a to-do list written by other people.
2. Work out the real capacity before looking at the task list. Committed meeting hours subtracted from working hours, minus a fixed admin allowance. The arithmetic and the default allowance are in references/capacity-math.md. Doing this first is what keeps the brief honest, because a task list read without capacity in hand always looks achievable.
3. Sort what is left into four buckets: due today, due this week, at risk, and waiting on someone else. The sorting rules, including what makes a task at risk, are in references/triage-rules.md.
4. Name what will not happen. If committed work exceeds capacity, say which items are being dropped or moved rather than listing everything and letting the week decide. This is the part that makes the brief worth reading and the part most likely to be softened out of it.
5. Branch by what the calendar shows:
   - A day with more than four meeting hours: no deep work scheduled that day. Put only small items against it.
   - A client presentation or pitch this week: prep time is a task with a due date, not something that happens in the gaps. If it is not on the calendar, that is the first finding.
   - A day with no meetings: this is the only real capacity in the week. Protect it before anything else gets scheduled into it.
   - Overdue items more than a week old: they are not tasks any more. Flag them for deleting or rescheduling, not for doing.
6. End with three priorities, ordered, each one a thing that gets finished rather than worked on. Not five.
7. Read-only by default. The brief proposes task changes and calendar blocks; it never edits either without being asked. Any change to more than one item is confirmed first.

## What good looks like

- First thing I check that most people skip: the gap between what the calendar says is committed and what the task list assumes is available. Almost every overloaded week is visible in that one number before anyone opens a task.
- The mediocre version: the task list reprinted in a nicer font, with a cheerful summary line. It tells the owner what they already knew, in an order they already had, and does not say what to drop.
- I know the brief is right when something gets explicitly dropped. A brief where everything fits has not been read against the calendar.
- Second test: the three priorities are things that can be finished, not projects. "Finish the Harbour proposal" passes. "Work on Harbour" does not.
- Red flag: the same item appearing in the at-risk bucket three weeks running. It is not at risk, it is declined, and somebody should say so.

## Rules

- MUST calculate available hours before reading the task list.
- MUST name what will not happen when commitments exceed capacity.
- MUST limit the priorities to three, each one finishable.
- MUST keep the brief read-only unless asked to make a change, and confirm before changing more than one item.
- MUST treat prep for a client presentation as a task with a due date.
- NEVER pull from email. Two sources only.
- NEVER carry an item that has been overdue for more than a week without flagging it for a decision.
