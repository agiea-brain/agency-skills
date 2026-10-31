# List health rules

## Rent the list

Accounts belong to the business. A rep holds them on licence, and the licence is renewed by meaningful activity. A book has a cap (documented in the client brain; 50 is the default, up to 100 where documented) because a rep cannot stack-pitch 120 accounts, and a stale account in one rep's book is a live account denied to another.

## Tiers

| Tier | What it is | Clock |
|---|---|---|
| A | Largest, most expandable accounts | 60 / 90 days |
| B | Solid, regular buyers | 60 / 90 days |
| C | Small or occasional buyers | 60 / 90 days |
| Flag | Developmental: a prospect or small account being proved into the book | 30 days |

Use the client's documented split where one exists. The default telemetry split for a 50 cap is 8 A, 15 B, 27 C, plus up to 15 developmental flags.

## Meaningful touch

A touch counts only if it produced an outcome.

| Signal | Counts? | Weight |
|---|---|---|
| Meeting booked (future date in the diary) | Yes | Primary |
| Brief taken (a documented requirement, no meeting yet) | Yes | Secondary |
| Call with no outcome | No | Noted as weak signal |
| Email sent, no reply | No | Noted as weak signal |
| Email reply with no next step | No | Noted as weak signal |
| Closed deal | Yes | Counts as a touch on the close date |

Days Since Last Touch = today minus the most recent counting signal, taking the latest of HubSpot activity and call notes or meeting transcripts.

## Status

| Status | Applies to | Condition | Action |
|---|---|---|---|
| Healthy | A/B/C | Meaningful touch ≤ 60 days | Stack pitch |
| Inactive Alert | A/B/C | 61 to 90 days | 3-Month Proof Rule: book a meeting (preferred) or take a brief before day 90 |
| Eviction Candidate | A/B/C | > 90 days, or no activity data at all | Release to the house pool; manual check first if data is missing |
| On Track | Flag | Touch ≤ 30 days | Keep proving |
| Flag Expired | Flag | > 30 days | Promote-and-swap, or drop |

Promote-and-swap: the flag has earned a tier, so it enters the book and an equivalent C account leaves, keeping the count under the cap.

## Stack pitch

A stack pitch asks for a 100% expansion across adjacent services, with 25 to 30% net growth as the realistic landing. It is built, not generic:

1. List what the account buys today.
2. Open the Menu for Sale and mark the services adjacent to those (same buyer, same problem area, or the next step in the same workflow).
3. Name two or three of them and the commercial reason this account would want them now.

Not a stack pitch: more of the same service, a renewal, a price rise, "see if they need anything".

## Output

```
Capacity: 52/50 active, 2 over; 4 eviction candidates would free room; 3 flags expiring

| Account Name | Tier | Days Since Last Touch | Status | Recommended Stack Pitch Angle |
(sorted: Eviction Candidate and Flag Expired, then Inactive Alert, then Healthy by expansion potential)

Actions this week
1. [meeting to book / brief to take / account to drop or swap, one per line, 3 to 5 lines]
```
