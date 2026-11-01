# Sweep gotchas

Each of these broke a real sweep before it was fixed.

| Symptom | Cause | Fix |
|---|---|---|
| The inbox call asked for 13 months of history | the agent worked out `after` by hand | compute the cutoff with code: now minus 14 days, epoch milliseconds |
| The cutoff was an hour off around a clock change | local time without a timezone | compute it in aware UTC |
| A day's sweep was logged as done but nothing was read | "No browser tab connected" was taken as a result | count the sweep only when Kondo returns real inbox data |
| Three chats came back rate limited | `load_chat` calls fired at once | one at a time, 3 seconds apart, one retry after the stated wait |
| One chat turned into eight records | the chat was read in pages | merge pages into one thread, dedupe on time plus text |
| Your own message looked last | their last message was an attachment with no text, and it was dropped | keep blank messages when deciding who spoke last |
| The same person was raised every morning | you had answered by text or email, which Kondo can't see | check your other channels' last outbound after their message |
| A thread you dismissed kept coming back | Kondo's activity time differs slightly from the message time | allow about a minute of slack before treating it as new activity |
| A date-only "replied" note looked older than their message | Kondo times are UTC; your notes are local dates | convert to local time first, and count a date-only note from the next day |

## Things to leave out of the human's summary

- Chats skipped because they were group chats or already dismissed. Mention counts only if asked.
- Any Kondo identifier (thread keys, profile URNs). Use names and, if asked, the person's public profile link.
