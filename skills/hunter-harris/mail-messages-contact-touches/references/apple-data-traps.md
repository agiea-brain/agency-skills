# Apple data traps

Each trap below put wrong touches in a CRM, or dropped real ones, before it was fixed.

## Mail (`Envelope Index`)

- **The `automated_conversation` flag marks your own sends.** Treating flag 2 as bulk silently dropped a real one-to-one email. Rule that held: flag 1 is bulk unless you sent it; flag 2 is bulk unless you sent it or wrote in that thread. List or unsubscribe headers always mean bulk.
- **Recipient type 0 is To, 1 is Cc.** Reading 1 as To invented group conversations. A multi-address To or any Cc is context, not a reply.
- **Mailboxes.** Skip any mailbox whose name contains draft, spam, trash or junk.
- **Direction.** Outbound only when From is one of your verified addresses. List them explicitly; aliases and old domains count.
- **Second addresses.** A contact's other address can be added when a name matches exactly one contact and mail went both ways. Record it as a confirmed identifier; count and skip anything ambiguous.
- **No index.** Some machines have no `Envelope Index`; the fallback is the `.emlx` files, which is slower.

## Messages (`chat.db`)

- **Your RCS sends have `handle_id` 0.** They carry no number. Take the handle from the one-to-one chat they belong to, never from a group chat.
- **Group chats are `chat.style` 43.** Record them as "group text message" context at most. Drop your own group sends.
- **Reactions** have an `associated_message_type`; skip them.
- **Dates** are nanoseconds since 2001-01-01 UTC. Convert to local time before comparing with date-only CRM fields.
- **Phones.** Saved contacts often lack `+1`. Match the full digits first, then the last 10 for North American numbers only.

## Full Disk Access

Without it, the open fails or returns nothing, and a naive script reports "no new touches". Treat a failed or read-only-refused open as an error that names the fix: grant Full Disk Access to the terminal or interpreter in System Settings, under Privacy & Security.

## What to store

| Field | Example |
|---|---|
| date | local date and time |
| contact | your contact's ID |
| channel | email, text |
| direction | in, out |
| summary | `email: <subject>`, capped at 160 characters, or `text message` |
| source | message GUID or Mail's global message ID, for de-duplication |

Never store bodies. A text's body is read only to tell whether it had text or just an attachment.

## Scale, for orientation

A full-history backfill against about 100 active contacts produced roughly 735 touches: three quarters direct email, a fifth group or Cc email, and a handful of texts. Expect most of a backfill to be email.
