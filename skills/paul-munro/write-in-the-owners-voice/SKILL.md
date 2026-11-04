---
name: write-in-the-owners-voice
title: Write in the owner's voice
description: |
  Use this skill when an agent drafts outward messages that go out under a
  firm owner's name (email, direct messages, posts, comments, texts) and the
  owner keeps catching wording they would never write. Drafts come from the
  owner's real sent writing: the agent changes the nouns of the nearest sent
  message, checks the draft against hard rules, never-written phrases, usual
  length and past corrections, and sends only on a pass from the last hour.
  Every night, drafts matched to sent mail become swaps, and a held-out test
  scores whether a judge can tell a draft from the real thing.
  Also use for "write it like me", "draft this in my voice", "reply for me",
  "that doesn't sound like me", "why does this read like a robot".
category: Operations
tags: [voice, drafting, email, owner-led, writing-check, send-gate]
---

Applies whenever you draft a message that will go out under the owner's name, to a client, a peer, a vendor, a prospect or the public. Produces one checked draft built from the owner's own sent writing, and a pass that lets it be sent within the hour.

## The play

1. Keep a local corpus of what the owner wrote: one record per sent message, the owner's words only. Quoted replies, forwarded blocks, the signature and tracking footers are cut. It is built from mail and chat exports, or from messages you read through a connector. The corpus holds client mail and personal messages, so it stays on the owner's machine. Record shapes are in `references/json-shapes.md`.
2. Before you write a word, pull the nearest examples and the register:
   ```
   examples --to ADDRESS_OR_NAME --channel email --n 8
   examples --to ADDRESS_OR_NAME --channel email --stats
   ```
   Examples rank by the same recipient first, then the same email domain, then the same channel and kind of recipient, then a similar length, then word overlap with the facts you give. A message that breaks a hard rule is never offered, so you cannot copy a habit the owner has since dropped. `--stats` gives the median length, the median sentence length, and the owner's usual openers and closers.
3. Write the draft by changing the nouns of the nearest example. Keep its opener, its length and its close. The rules are the check, never the source.
4. Put the exact text to be sent in a file, with no subject line, and check it:
   ```
   check FILE --to ADDRESS_OR_NAME --channel email --save-draft
   ```
   The check returns BLOCK, FLAG or PASS. What each catches is in `references/the-check.md`.
5. Act on the result:
   - BLOCK: rewrite each listed line as a new sentence. Changing its punctuation is not a rewrite. Run the check again.
   - FLAG: read each flagged word, phrase or length note. Change whatever the owner would not write. Keep what they would, such as a name or a term from the thread.
   - PASS or FLAG writes a pass for that exact text and saves the draft for the nightly loop.
6. Send that same text within 60 minutes. One changed word after the check needs a new check. A hook in front of every send tool refuses a send whose text has no pass from the last hour. A refusal is never worked around. The draft goes back to step 2.
7. When the owner corrects your wording, record the correction the same turn as a swap: your phrase, their phrase. From then on the check catches it.
8. Let the nightly loop run without the owner: yesterday's sent mail goes into the corpus, saved drafts are matched to what was sent, the changes become swaps, and a held-out test scores the drafting. The order is in `references/the-loop.md`.

## What good looks like

- First thing I check: whether the draft started from a sent example or from a description of my style. A draft written from rules reads like a draft written from rules. One note carried a technical phrase I had to catch myself, and that is why the system exists.
- The mediocre version is a long style guide and a reminder to follow it. It drifts within a week. The check and the gate hold because they are mechanical.
- I know it is working when I send drafts unchanged. Each one is recorded as a pass, and the swap list stops growing.
- I know the drafting is good when the held-out judge sits near 0.5. That means it cannot tell the draft from what I really sent.
- Red flag: a swap list full of the agent's own rewrites. Several drafts of one note once got written up as my corrections. Only the newest draft of a note is matched to what I sent now. The earlier ones are marked superseded and never become swaps.

## Rules

- MUST pull examples and the register before drafting, for every outward message in the owner's name.
- MUST check the exact text to be sent, and check again after any change.
- MUST rewrite every BLOCK line as a new sentence.
- MUST send within 60 minutes of the pass, or check again.
- MUST record each wording correction from the owner as a swap in the same turn.
- MUST keep the corpus local, on the owner's machine.
- NEVER upload, quote, post or link the corpus or any message in it to a connector, a shared page, a task tool or any remote host.
- NEVER draft from the style rules alone.
- NEVER work around a gate refusal. Go back to the examples.
- NEVER let the drafting side of the nightly test see the real message it is drafting.
- NEVER expect a script to do a model's job. The scripts call no model. The agent does that part.
