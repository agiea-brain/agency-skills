---
name: client-performance-review
title: Client performance review doc
description: |
  Use this skill when an agency owes a client its periodic outbound performance
  review (QBR, 30-60-90, "three months in") and wants a commentable doc the
  client reads before the call. Pulls the numbers by channel and campaign, writes
  the summary, levers, what has not worked, new plays and the client's asks, adds
  a data appendix (TAM, who replies, objections), renders clean tables and
  charts, and runs the comment-and-call loop. Also use for "performance review",
  "QBR", "results doc", "write up how outbound is going".
category: Customer Success
tags: [qbr, client-reporting, outbound, performance-review, retention]
tools: [instantly, heyreach, hubspot, slack]
---

# Client performance review

One document the client reads alone, comments on, and then we walk through together on a call.
Model: the fictional review in `references/example-review.md`, rendered by the script.

**Output:** a Google Doc in the client's shared Drive folder, built from a Markdown source that lives
in the client repo at `docs/reviews/YYYY-MM-DD-<period>.md` (so the next review diffs against it).

## Step 1: Pull the numbers (the client project notes say where each lives)

Fix the window first (e.g. launch to last Sunday) and state it in the byline. Pull, per channel and per campaign:

| Metric | Source (typical) | Definition to hold to |
|---|---|---|
| Accounts scored / qualified / top tier | warehouse fit table | current fit model only, never a retired one |
| Signals detected / qualified / reached | signal tables | count people for recurring signals (promotions fire weekly) |
| People emailed, emails sent, new people | Instantly analytics + sent log | people, not leads rows; dedupe across campaigns |
| LinkedIn reached / accepted / replied | HeyReach stats | |
| Replies | reply-bot / inbox log | **human** replies only: no auto-reply, OOO, bounce, own follow-ups |
| Positive replies | reply classifier | interest of any kind: book, info, referral, "later" |
| Said "book a call" | classifier / manual | the yes, before it becomes a meeting |
| Meetings booked | calendar / HubSpot / confirmed list | proof of a meeting, not a positive reply |
| Deals | CRM | open and closed, with stage |
| Objections | reply classifier, grouped | count accounts, not messages |

Then cut **interested per 1,000 reached** by company size, seniority, industry, product line, mail provider
and channel. This one rate makes every segment comparable. Do not quote a rate on fewer than 100 people;
show the count instead ("0 of 400").

Save the pulled numbers as `docs/reviews/<date>-data.json` (or CSV) beside the Markdown, so every figure in the doc traces back to a query.

## Step 2: Write the Markdown in this order

Read `references/writing-rules.md` first, especially the tone section: honest, but written so the client wants to keep going. Every section opens with its takeaway in one sentence.

1. **Summary**: one callout (`> **Headline.** ...`) plus at most 4 bullets: results, the biggest leak, the best channel, the top objection.
2. **The numbers**: funnel chart (scored → meetings), a month-by-channel table, then **By campaign**, grouped by product line with a bold total row per group. Outcomes (meetings by source, deals) go here as a short table.
3. **How we get more meetings**: levers ranked by expected impact: lever, what we'll do, expected impact. Say which ones are untested.
4. **Where we have not seen success**: segments, campaigns or signals that did not work, with the count and what we take from it. Be candid; this section builds trust.
5. **What we will improve**: our own fixes (speed, tracking, routing, copy, tests). Bullets.
6. **New plays**: "what we learned" → "what we will run". Each play tied to a number in section 2 or the appendix.
7. **Where we need <client> to push**: asks with the reason each matters. Concrete: a seat, a person, a calendar, a sign-off.

`---` page break, then **Data appendix**:

- **A. TAM**: by industry and by fit tier: accounts, top tier, reached, interested per 1k.
- **B. Who replies**: company size, seniority/persona, industry; hbar charts against the average. List the replying companies by name where it helps.
- **C. Objections**: what they said, accounts, how we answer it.
- Optional: events, signal lanes, full campaign list, "what runs underneath" (one paragraph), definitions.

Keep the body (sections 1 to 7) to about 4 pages. Anything wider or longer goes to the appendix.

## Step 3: Render and check

```bash
python3 -m venv /tmp/rv && /tmp/rv/bin/pip install -q python-docx matplotlib
/tmp/rv/bin/python references/build_review_doc.py \
  docs/reviews/2026-10-26-q3.md -o /tmp/review.docx --pdf
```

Open the PDF (or `pdftoppm -r 80 -png`) and look at every page: no wrapped number cells, no table
wider than the page, every chart titled with its takeaway. Syntax for tables, charts, callouts and
column widths is in the script's docstring.

## Step 4: Put it in Google Docs

Drag the `.docx` into the client's Drive folder (Drive converts it to a Google Doc; with "Convert uploads"
off, open it and use File → Save as Google Docs). Then: title it `<Client>: <period> review (draft)`,
share as **Commenter** with the client, and look at every table in the Google render. Inter sets wider in Google Docs than in the LibreOffice preview, so a header that just fits in the PDF can wrap in Docs; widen that column and re-import.

Re-importing creates a new doc, and comments do not carry over. Freeze the numbers before sharing. After that, edit in Google Docs
by hand and copy the change back to the Markdown.

## Step 5: The review loop

1. Send the doc 2-3 business days before the call, in the shared client Slack channel, using `references/slack-message.md`
   (link first, 3 findings with numbers, the asks, a comment deadline, a call ask). Draft it for the account owner; never post it yourself.
2. Before the call, answer every factual comment in-thread; collect the open questions as the agenda.
3. On the call: 5 min on the summary, then comments, then plays and asks. Leave with an owner and date for each ask.
4. After: resolve comments, write `decisions/<date>-review.md` in the client repo (what was agreed, who owns what), and update the plays.

## What good looks like

- Every figure traces back to the saved data file from a query, never memory, and anything estimated is marked as estimated.
- Replies are human replies only, and a meeting needs proof of a meeting, not a positive reply. Count people, not lead rows.
- No rate on fewer than 100 people: show the count instead ("0 of 400").
- "Where we have not seen success" is candid, with the count and what we take from it. That section builds trust.
- Red flag: sharing the doc before the numbers are frozen. Re-importing creates a new doc and the client's comments do not carry over.

## Hard rules

- **Numbers from queries, never memory.** Every figure traces to `<date>-data.json`. Mark anything estimated as estimated.
- **Unverified claims stay out**: no customer names, benchmarks or logos the client has not signed off on.
- Edit the prose for AI patterns before sharing.
- Draft first to the account owner; the client gets it only after our review.
