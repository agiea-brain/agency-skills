---
name: linkedin-export-contact-import
title: LinkedIn export contact import
description: |
  Use this skill when you've downloaded your LinkedIn data export and want your
  connections, sent invites and DM history in your CRM or contact sheet.
  Produces upserted contacts plus dated touches, safe to re-run every week.
  "Import my LinkedIn export", "load my connections into the CRM",
  "who have I messaged on LinkedIn".
category: RevOps
tags: [data-export, crm-hygiene, contacts, import]
tools: [linkedin]
---

Applies when LinkedIn holds relationship history your CRM doesn't. Produces contacts from Connections and sent invitations, and one dated touch per one-to-one message, deduplicated so weekly re-imports add only what's new.

No scraping and no API: this works on the export LinkedIn gives every member.

## The play

1. Request the export from LinkedIn's data privacy settings. The basic export has Connections, Invitations and messages. The complete one adds comments, shares and reactions. A weekly rhythm that works: basic midweek, complete at the weekend.
2. Unzip each export into its own dated folder. Never overwrite the previous one.
3. Read `Connections.csv` from the line that starts `First Name,Last Name,`. LinkedIn puts notes above the header.
4. Key every person on the `/in/` part of their profile URL. A name-only match is a candidate: list it for the human to confirm.
5. Contacts come from Connections, plus OUTGOING rows from `Invitations.csv`. Count and skip members whose fields are all blank (hidden or deactivated).
6. From `messages.csv`, keep only one-to-one threads. Skip drafts, spam and group threads. Each message becomes a touch: date, person, channel, direction.
7. Dry run first. Show the proposed creates, merges and updates; apply only after the human approves.
8. Change a contact's status only from recent messages: within 60 days of the newest message in the export. Import exports in date order and never one older than the last. A two-year-old thread is history, not a live conversation.

The file-by-file quirks are in `references/export-file-notes.md`. Open it before writing the parser.

## What good looks like

- First check: a second run of the same export adds zero touches. If it adds any, the dedupe key is wrong.
- The mediocre version imports everything as current. Old threads flip contacts to "in conversation", group chats become replies, and drafts you never sent count as messages.
- The output is right when the counts reconcile: Connections rows equal new plus matched plus skipped-blank, and five spot-checked people show the right last message date.

## Rules

- MUST dry run before writing, and keep each export folder intact.
- MUST key on the profile URL slug; NEVER merge two people on name alone when more than one contact has that name.
- NEVER treat a draft, spam or group message as a touch.
- NEVER use an old export to downgrade data a newer one wrote.
- NEVER upload the export to a third-party service to parse it; it contains other people's messages.
