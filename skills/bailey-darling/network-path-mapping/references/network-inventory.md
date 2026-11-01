# Building the inventory

Most people can name forty contacts and actually have four hundred. The gap between those numbers is the whole point of this exercise, and it is why the first step is an export rather than a brainstorm.

## Start with the connections export

Request a copy of your own data from your professional network's privacy settings and choose the connections archive. Most services email a download link within minutes, though a full archive can take up to a day. Request it before doing anything else in this skill; everything below is faster once the file is in hand.

What arrives is a CSV, one row per connection, with roughly these columns:

| Column | Use |
|---|---|
| First name, last name | The identifier |
| Company | The match against the target list |
| Position | Whether they can reach a buyer |
| Connected on | A proxy for how the relationship started |
| Email address | Present only for some connections |
| Profile URL | For checking where they are now |

Three things to do with it before matching anything:

1. **Sort by company** and look for any name that appears on the target list. These are the one-hop paths and they are found in about five minutes.
2. **Sort by connected-on date, oldest first.** The oldest connections are usually former colleagues and former clients, which are the two highest-value groups. The newest are usually event and inbound contacts, which are the weakest.
3. **Flag anyone whose current company differs from where you knew them.** That is the former-client-at-a-new-company case, and it is the best path in the file.

The export is a snapshot and it says nothing about relationship strength, which is scored by hand in references/path-strength.md. It also goes stale: people change jobs constantly, so re-export quarterly rather than maintaining the CSV by hand.

Treat the file as personal data. It holds other people's employment details and sometimes their email addresses. Keep it where client data is kept, do not upload it anywhere you would not upload a client list, and do not use the email column for bulk sending. It is for mapping paths, not for building a send list, and using it that way burns the network this skill exists to build.

## Where else to pull from

In order of value, not of convenience.

| Source | Why it is worth the time |
|---|---|
| Former clients, and where they work now | Already bought from you. Highest conversion of anything here. |
| Former colleagues from every job | They know your work directly. Scattered across the market by now. |
| People who referred you work before | A proven referrer, often never asked twice |
| Vendors and tool reps in your market | They meet your buyers weekly and are almost never asked |
| Peer firms doing adjacent work | Referral partners, not competitors, when the services do not overlap |
| Investors, advisors, accelerator contacts | Wide networks, and introductions are part of what they do |
| Event and conference contacts | Weak by default, but they map to specific firms |
The first two rows produce more usable paths than everything below them combined, and neither is fully visible in the export, which is why the export is the start and not the whole inventory.

## Fields

| Field | Example | Why |
|---|---|---|
| `name` | | |
| `where now` | VP Marketing, Harbour Logistics | The target-list match |
| `where before` | Was at Northwind when we worked together | The strength of the tie |
| `how we know each other` | Ran a six-month engagement, 2024 | Decides what can be asked |
| `strength` | 1 to 4, see path-strength.md | The ranking |
| `last contact` | date | Whether an ask is premature |
| `their network` | Freight and logistics, Toronto | Where they can reach |
| `has referred before` | yes / no | The strongest predictor there is |

`where before` matters more than it looks. The tie formed at the old company is the real relationship; the new company is just where it now points.

## Keeping it current

Job changes are the engine. Every time someone in the inventory moves, a new path appears, and it has a window: the first three months in a role, when they are building their own vendor list and have budget nobody has spent yet.

Check for moves monthly. It takes ten minutes and it is the highest-yield maintenance in the whole system.

## The first pass

Do not try to be complete. The export plus two hours on former clients and former colleagues will produce 100 to 200 scored names. Run the matching on that. The long tail can wait until the obvious paths are worked.

Completeness is the enemy here: an inventory built over three weeks is usually built instead of doing the asks.
