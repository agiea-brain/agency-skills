---
name: kondo-owed-reply-sweep
title: Kondo owed-reply sweep
description: |
  Use this skill at the start or end of a day of LinkedIn prospecting, when you
  need to know which DMs are waiting on you. Produces a short list of people
  whose message is last, for you to decide which to answer. Uses Kondo's MCP
  server. "Who replied?", "check my DMs", "what LinkedIn replies do I owe".
category: Sales
tags: [dms, inbox, follow-up]
tools: [kondo, linkedin]
---

Applies when you prospect on LinkedIn and replies get lost in the inbox. Produces a list of the one-to-one threads where the other person spoke last, by name, for you to decide.

Needs Kondo connected to your agent through its MCP server. The sweep only reads, covers the last 14 days, and sees only LinkedIn.

## The play

1. Call `list_inbox` with the "needs my reply" view and an `after` cutoff 14 days back, computed in UTC epoch milliseconds. Use a fixed helper or a one-line script for the cutoff, never the agent's head. Save the raw response to a file.
2. An error or missing response means the sweep failed: say so and stop, never log it as done. A valid empty inbox means nothing is owed.
3. Drop group chats; they are never a reply owed. Drop threads you already marked "no reply needed", unless the person has written since.
4. For each remaining chat, call `read_chat`. If it comes back empty, call `load_chat` (also a read), spacing calls 3 seconds apart. If rate limited, wait as told and retry once.
5. If a chat comes back in pages, merge the pages into one thread before judging it.
6. Sort by time and look at the last real message. It is owed when the last message is theirs. An attachment with no text still counts as a message.
7. If you can check your email, texts or call log, suppress threads you already answered there after their last message. If you can't, keep them on the list.
8. List the owed people by name and ask once which to answer. For each one you say needs no reply, store the thread and the time of their last message, so it comes back only when they write again.
9. Close with one line: owed, answered, not owed.

The failure log behind steps 1 to 7 is in `references/sweep-gotchas.md`. Open it when a count looks wrong.

## What good looks like

- First check: the sweep really ran. An error string logged as "done" means a day of replies nobody saw.
- The mediocre version trusts Kondo's "needs reply" view as-is. It flags group chats, splits one paged chat into several, and asks every morning about people you answered by text.
- The output is right when every name on the list has their message last, nobody you answered elsewhere is on it, and the list is short enough to act on before the day's messaging starts.

## Rules

- MUST stay read-only: never send, draft into Kondo, label or archive a chat from this sweep.
- MUST name people, never show Kondo's internal identifiers.
- MUST let the human decide who needs a reply; record their words when they say "no reply needed".
- NEVER record anything when Kondo is down or returns an error.
- NEVER fire `load_chat` calls in parallel.
