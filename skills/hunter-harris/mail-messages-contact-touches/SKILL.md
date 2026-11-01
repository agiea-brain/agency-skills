---
name: mail-messages-contact-touches
title: Mail and Messages contact touches
description: |
  Use this skill on a Mac when your CRM or contact sheet doesn't know who you
  last emailed or texted. Produces dated touch records (date, contact, channel,
  direction, email subject) from Apple Mail and Messages, without storing message
  bodies. "Log my emails and texts to the CRM", "when did I last talk to them",
  "backfill contact history".
category: RevOps
tags: [crm-hygiene, macos, contact-history]
tools: [apple-mail, apple-messages]
---

Applies when relationship history lives in your inbox and phone, not your CRM. Produces one dated touch per real one-to-one email or text, matched to a contact, ready to append.

Runs locally on a Mac. Both databases are opened read-only; raw records stay on the machine, and only the derived fields reach the CRM.

## The play

1. Build an index from your contact list: lowercase emails, and phones reduced to digits.
2. Open `~/Library/Messages/chat.db` and the newest `~/Library/Mail/V*/MailData/Envelope Index` as read-only SQLite (`file:...?mode=ro`). The terminal or interpreter needs Full Disk Access. If the open fails, stop and say so; don't report "no touches".
3. Texts: skip reactions, convert Apple's nanosecond dates, and match the handle. Group chats are context, never a direct touch.
4. Email: read sender, To and Cc, date, subject and mailbox. Skip drafts, spam, trash, junk and bulk mail. It is outbound only when the From address is one of yours.
5. Match: exact email, or exact phone; fall back to the last 10 digits only for North American numbers. Anything matching more than one contact is skipped and counted, not guessed.
6. Emit date, contact, channel, direction, a summary (the email subject, or just "text message") and a source ID.
7. Dry run first and show the counts by channel. Write only after the human approves. De-duplicate on the source ID so a re-run adds nothing.
8. Start with an 8-day window. Backfill full history once, on purpose.

The field-level traps (Mail's automated flag, RCS sends, To versus Cc) are in `references/apple-data-traps.md`. Read it before writing the query, and check the flag meanings against a few messages you know before importing.

## What good looks like

- First check: your own sent mail shows up as outbound. If it doesn't, the automated-mail filter is eating it.
- The mediocre version treats every group text and Cc as a conversation, and the CRM fills with "touches" from threads where you were one of twelve.
- The output is right when a contact you emailed yesterday shows yesterday, a backfill is spot-checked against the inbox for five contacts, and a second run adds zero rows.

## Rules

- MUST open both databases read-only, and never copy them out of the machine.
- MUST store subjects at most, never message bodies or attachments.
- MUST dry-run and get approval before writing to the CRM.
- NEVER guess between two contacts that share an email or number.
- NEVER report an empty result when Full Disk Access was refused.
