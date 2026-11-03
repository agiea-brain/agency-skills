# Conference Outreach

Conferences are the warmest cold lane we run. The message is "we'll both be there", which is true
and checkable, not a pitch. They matter most for vertical buyers who don't live on LinkedIn or
answer cold email (surgeons, field ops, clinic and job-site leaders), who all show up to their
industry's annual meeting.

---

## 1. The flywheel: pre, during, post

| Phase | Channels | Timing |
|---|---|---|
| **Pre** | email → LinkedIn request → call or text | email 2-3 weeks out; LinkedIn 1-2 weeks out; text or call the week of |
| **During** | booth, floor walk on a hit list, booked coffees, side events | 10am-3pm floor: one meeting every 15-20 min = 12-20 a day |
| **Post** | email + LinkedIn follow-up referencing what you talked about, then BDR calls on non-replies | the Monday after; done within the week |

**The metric is cost per qualified meeting.** $20K all-in for 40 real conversations = $500 per
meeting, which beats most channels when CAC runs $5-10K+. Conferences fail when teams skip the
pre-work, walk without a hit list, and don't follow up. A booth helps but isn't required: a general
admission pass plus a hit list plus booked coffees works.

## 2. Building the list

1. **Scrape the event's own site first:** exhibitors, speakers, sponsors. It's free, and it's the
   highest-precision source because it isn't an inference. Buy the attendee list if one is sold
   ($500-2K is almost always worth it).
2. **Search LinkedIn posts mentioning the event.** People announce they're going. Treat these as an
   *inference*, not a fact: on one Texas home-care event, 597 posts → 190 kept → 25 accounts
   matched, and most top matches rested on one common word in a generic agency name.
3. **Enrich and score accounts** exactly as you would any account. Sort the hit list by score, with
   the reason visible ("25+ field reps, 15 managers, PE-acquired last year").
4. **Find 2-3 buyers per top account.** For registrants, the roster *is* the person.
5. **Exhibitors cut both ways.** A vendor exhibitor is a competitor to position against and is
   **never** emailed as a prospect. A provider exhibitor is an account with budget.

### The three questions that decide a run
1. **Did attendees consent to sharing their details?** If the roster has a consent column, it is the
   *only* thing deciding who can be emailed, and a blank means no. The one consented roster (6 human
   replies from 67 people reached) far out-replied the others (0-2 replies each).
2. **Does the roster carry email addresses?** If not, run every free gate **before** paying to find
   an address, so you never buy an address for a vendor, a clinician or an existing customer.
3. **Who is a buyer at this kind of organization?** Personas invert by vertical: a nurse doesn't
   pick the billing system at an IDD provider, but the Administrator and Director of Nursing *are*
   the licensed leadership at a Texas home-health agency. Personas are event-scoped.

### Gates (all fail closed)
- **Customers come from the live CRM**, never a cached column. One gate read an all-false column and
  reported "no customers on this roster".
- **Suppression is alias-expanded** (`acmeclinic.org` and `acme-clinic.org` are the same
  customer).
- Reply gate: anyone who replied to any campaign is out. Do-not-contact list, cooldowns.
- **Check whether you're on your own roster** (one roster listed the client itself and three
  competitors).
- The usual per-account cap is normally **off** for a one-week event (everyone at the account knows
  they're going). Address-level dedup still applies.

## 3. Copy rules for this lane

- **Anchor steps to the event dates, not a cadence.** Three emails: about a week out, the first
  morning of the event, and the Monday after. A normal 3-day follow-up lands mid-conference, when
  nobody reads email.
- **Instantly delays count from each lead's start, not the calendar.** A late-enrolled lead gets
  "see you there" after the event. Enroll everyone on the same day, or schedule the steps, and
  verify the dates before launch.
- **Never claim a detail you can't verify per recipient.** No booth number you don't have (keep it a
  token: `{{boothLine}}` with a safe fallback), no "I saw your post", no "great meeting you" unless
  you met. A conference list is where an unverifiable detail gets read by the person standing next
  to the one it was true of.
- **Company voice vs person voice.** "We're exhibiting at booth 1412" is a fact about the company and
  stays true whoever travels. "I'll be there" is only safe if that person is going. A LinkedIn DM is
  always signed by a person.
- **Attending vs exhibiting changes every ask.** With no booth there's no "come by", and no booth token
  at all. The ask becomes a hallway conversation or a call.
- **Say where the address came from** when it's a shared roster: "your name is on the registrant
  list the association circulates, which is where this address came from." Transparency is the
  whole asset of this lane.
- **Every merge token carries a fallback** (`{{firstName | there}}`, `{{companyName | your agency}}`)
  so a blank is structurally impossible.
- **The ask must not grow between steps** (15 minutes in step 1 can't become 30 in step 3).
- **Single variant.** 60 people across three steps can't resolve a copy test.
- Post-event copy references something tangible from the conversation (from the Granola notes),
  never generic "great to connect".
- Both campaigns are created **switched off**. A person reads the event-specific copy last and
  launches it.

### Templates

Pre-event (about a week out). Subject: `{{RANDOM|[event] next week|see you at [event]}}`
```
{{RANDOM|Hey|Hi}} {{firstName}}, {{RANDOM|looks like|saw}} {{companyName}} is headed to [event] next week. We'll be there too {{boothLine}}.

[One line: the problem we help [persona]s with, in their words.]

{{RANDOM|Worth grabbing 15 minutes on the floor?|Open to a quick coffee while we're both there?}}
```

First morning (same thread, blank subject):
```
{{firstName}}, we're {{RANDOM|set up|here}} {{boothLine}} through [day]. If a coffee works better than the floor, {{RANDOM|just reply with a time|send me a time}}.
```

The Monday after (new subject: `after [event]`). Met them:
```
{{firstName}}, {{RANDOM|good|great}} talking about [specific thing from notes] at [event]. [The next step we agreed, in one line.]

{{RANDOM|Still good for [day]?|Does [day] still work?}}
```
Didn't meet:
```
{{firstName}}, sorry we missed each other at [event]. [One line of what people kept asking us about there.]

{{RANDOM|Worth 15 minutes this week instead?|Want the short version over email?}}
```

Week-of text (needs a mobile number and a reason to expect it to be welcome; this has booked well at trade shows when the list was tight):
```
hey [name], <your name> here, just got into [city] for [event]. would love to grab a coffee if you're around.
```

## 4. During the event

- Work the hit list in score order, and read the buyer's LinkedIn and firmographics before walking up.
- Record or take notes (Granola), get contact details, and land a concrete next step.
- Be memorable: post-event outreach only works if they remember you.
- Each night, have Claude ingest the notes: update the CRM and draft the follow-ups.

## 5. After the event: retire the campaign

**Retire the conference campaign once its last email sends, and release its leads.** The copy is
false after the event, and in Instantly a lead held by any campaign is blocked from every other one,
so a drained conference campaign silently becomes a tombstone for everyone in it. Clear its id from
the campaign map.

## 6. Tags
`trigger_type: event`, `segment: <event-slug>`, and the persona. Track meetings per event
separately from cold lanes, or the conference's cost per meeting can never be computed.
