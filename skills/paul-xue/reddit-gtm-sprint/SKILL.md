---
name: reddit-gtm-sprint
title: Reddit GTM sprint
description: |
  Use this skill when a client says "we should do something on Reddit" and
  you need research before anyone posts. Mines subreddits for verbatim
  complaints, isolates one purple-cow wedge, gap-analyzes the client's current
  positioning, and produces an organic and paid roadmap with cost-per-result
  math. Also use for "Reddit marketing research", "Reddit positioning",
  "what are Redditors saying about", "Reddit ads plan", "social listening on
  Reddit".
category: Marketing
tags: [reddit, positioning, social-listening, paid-social, organic-growth, gtm]
---

# Reddit GTM Sprint

One pass that takes a client from "we should do something on Reddit" to a defensible wedge plus an executable organic and paid plan. The research spine is identical for every client; only the execution branch changes.

**Order is not optional.** Intake → collect → analyze → gap → execute → deliver. Do not write any part of the roadmap before the corpus exists. A roadmap written ahead of the verbatims is a roadmap built on priors.

---

## 1. Intake: lock the brief before opening a browser

Ask in one round for whatever the request didn't already supply:

- **Client + URL**, and the specific page(s) carrying the claim being pressure-tested (materials page, pricing page, comparison page)
- **The differentiator** the client currently leads with, verbatim
- **Audience / niche** in the client's words
- **Seed subreddits** (3–6) and any seed threads the user already flagged
- **Track**: organic + subreddit growth, paid, or both
- **Target cost per result**, and what "result" means: email, add-to-cart, purchase, booked call, DM
- **Budget ceiling and timeline**
- **Execution constraints**: is there a brand account, a postable founder, an existing Reddit footprint, anything legal can't say?

If the session is unattended, infer from the URL, state every assumption in a block at the top of the deliverable, and proceed.

Write the answers to `brief.md` in the working directory. Every downstream section cites it.

---

## 2. Collect: verbatims are the product

**A browser connection is the primary path.** Setup and fallbacks are in references/connectors.md. Then:

1. Read the client's claim page(s) first, so you know what you're testing against before Reddit colors your reading.
2. Read each seed thread the user supplied, in full, comments included.
3. Per seed subreddit, run 2–4 query terms (the product category, the complaint noun, competitor names, "recommendations") sorted by Top/Relevance across the last 12–24 months.
4. Follow the trail outward. Threads name adjacent subreddits where the real conversation lives: chase those. The best subreddit for a client is often one they never named.

**Capture per thread**: URL, date, score, subreddit, the OP's pain in their own words, and the 3–8 highest-voted substantive comments quoted exactly. Never paraphrase into the corpus: paraphrase is where the insight dies. Note comment scores; a 400-upvote complaint is a different signal from a 4-upvote one.

**Also capture per subreddit**: subscriber count, activity level, and the self-promotion rules from the sidebar. This is what makes the organic plan real rather than aspirational.

**Minimum viable corpus**: 3+ subreddits, 6–10 threads each, 40+ substantive comments total. Below that, say so in the deliverable rather than overclaiming.

**Fallbacks, in order, when the browser stalls or a thread won't render**: `old.reddit.com` for the same URL → append `.json` to a thread URL → Riveter `scrape` / `search_agent` for bulk → WebSearch `site:reddit.com`. If no browser is connected at all, say so in one line and switch, don't retry it.

Save everything to `corpus.md`, organized by subreddit.

---

## 3. Analyze: isolate one wedge

Cluster the verbatims into complaint themes. For each theme score:

- **Frequency**: how many independent threads raise it
- **Intensity**: is this an annoyance or a rant? Quote the angriest phrasing
- **Buyability**: does solving it actually move a purchase, or is it just venting?

Pick **one** complaint as the wedge. Two wedges is no wedge.

**The purple cow test.** The angle must pass all three:

1. **Verifiable**: the client can prove it today, not aspirationally
2. **Unclaimable**: the top three competitors cannot say the same sentence
3. **Repeatable**: a Redditor could restate it in one line to a friend

If the client's current lead claim fails this test, say so plainly and early. Certifications and spec sheets usually fail #3: they are trust *confirmation*, not trust *acquisition*.

Also extract, separately: **what makes this audience distrust a brand in this category.** Ad-hostility, astroturf detection, specific phrases that read as marketing. On Reddit this is routinely a bigger factor than the positive claim, and it governs everything in section 5.

---

## 4. Gap analysis

A table, one row per want:

| What Redditors want | How they phrase it (quote) | What the client currently says | Gap | Fix |

Then two explicit call-outs:

- **Wasted leads**: claims the client puts front-and-center that no Redditor in the corpus mentions once
- **Unspoken assets**: things the corpus is begging for that the client already has but buries

Cite a thread URL on every row. An uncited row is an opinion.

---

## 5. Organic + subreddit growth track

Build only from the rules captured in section 2.

- **Tier the subreddits**: (A) links allowed, (B) comment-only / no promo, (C) mod-approval or AMA-only. Different play per tier; never propose a link drop into a tier-B sub.
- **Account strategy**: which persona posts: founder, brand, or employee-with-flair. State the disclosure approach explicitly; undisclosed brand posting is how a client gets banned and screenshotted.
- **Ratio**: at least 9 genuinely useful comments for every 1 post that mentions the client. Build the comment-target list from the threads already in the corpus, those are live, indexed, and still getting traffic.
- **Formats that carry on Reddit**: teardown of a category-wide lie, a real test with photos, an honest "here's when you should NOT buy ours", a founder AMA, an answer so complete it gets awarded.
- **Owned subreddit**: recommend one only if there is a recurring question the existing subs handle badly. Otherwise say don't.
- **Cadence**, and a 30 / 60 / 90 with a named owner and a measurable target per phase.

---

## 6. Paid track: work backwards from the target CPR

The arithmetic, stated once and used honestly:

```
CPC = CPM / (1000 × CTR)
CPR = CPC / CVR   =   CPM / (1000 × CTR × CVR)
```

So hitting a target CPR requires: `CTR × CVR ≥ CPM / (1000 × target CPR)`.

Worked example: $100 target CPR at a $6 CPM needs CTR × CVR ≥ 0.006%: a 0.6% CTR paired with a 1% CVR clears it; a 0.3% CTR needs 2% CVR to hold the same line.

Produce a **sensitivity table**, CPM rows against CTR × CVR combinations, cells marked pass/fail against the target, then say which input is actually movable for this client and why. Usually it is CVR via landing page, not CTR via creative. Be honest when the target CPR is not reachable at the stated budget; give the CPR that is, and what it would take to close the gap.

Then specify:

- **Creative**: conversation-format ads led with a verbatim from the corpus. Headlines are quotes, not slogans. 3–5 concepts, each mapped to a specific complaint cluster.
- **Targeting**: subreddit targeting first (the subs in the corpus, plus adjacent ones found in section 2), interest targeting second, broad last.
- **Test structure**: how many cells, daily budget per cell, minimum spend before a read, and explicit kill criteria.
- **Measurement**: Reddit Pixel events, the post-click path, and the fact that Reddit's attribution runs optimistic. Name the cross-check.

---

## 7. Product roadmap

Some complaints in the corpus are not marketing problems. Separate them: the fixes that need a product, packaging, warranty, pricing, or policy change, ranked by how many threads they'd defuse and how hard they are to ship. This is where a purple cow gets manufactured when the client doesn't already own one.

---

## 8. Deliverable

Build `clientname-reddit-gtm.md` and deliver it, then produce a shareable client-facing version.

Structure:

1. Assumptions and brief (one block)
2. TL;DR: the wedge in one sentence, the three moves, the CPR verdict
3. Corpus summary: subreddits, threads, comments, dates covered
4. Complaint clusters, scored, each with quotes
5. The purple-cow angle and why it passes all three tests
6. Gap analysis table
7. Organic plan + 30/60/90
8. Paid plan + sensitivity table + kill criteria
9. Product roadmap
10. Appendix: every thread URL used

---

## House defaults vs. hard rules

Some numbers in this skill are house defaults, not laws. Adjust them when the engagement gives you a reason, and say in the deliverable that you did.

**House defaults (adjustable with a stated reason):**

- The 9:1 comment-to-promotional-post ratio. Tighten it in heavily moderated or ad-hostile subs; loosen it only where a brand already has standing.
- The minimum corpus (3+ subreddits, 6–10 threads each, 40+ comments). A narrow B2B niche may not have this much material; note the shortfall instead of padding it.
- One wedge only. The discipline matters more than the number, but a client with two genuinely separate audiences may warrant two passes rather than one blurred angle.
- The 12–24 month recency window, and the 3–8 comments captured per thread.
- Targeting order in the paid plan, and the assumption that CVR is the movable input.

**Hard rules (do not adjust):**

- Every claim in the deliverable traces to a cited thread URL.
- Quotes are verbatim. Never invent a quote, a subscriber count, or a metric.
- Benchmarks not pulled from the client's own account data are labeled estimates.
- Thin evidence is labeled thin, never smoothed over.
- The roadmap is written after the corpus, never before.
- Disclosure in the organic plan is explicit. Never propose undisclosed brand posting.

---

## What good looks like

- First thing I check that most people skip: whether the client's current lead claim passes the purple-cow test. Certifications and spec sheets usually fail the third test: they are trust confirmation, not trust acquisition.
- The mediocre version writes the roadmap first and goes looking for quotes to support it. A roadmap written ahead of the verbatims is a roadmap built on priors.
- I know it is right when every row in the gap table cites a thread URL, there is exactly one wedge, and the organic plan is tiered by each subreddit's actual self-promotion rules.
- Red flag: a plan that drops links into comment-only subreddits, or posts as the brand without disclosure. That is how a client gets banned and screenshotted.

- Every claim traces to a cited thread URL. Uncited claims get cut.
- Benchmarks (CPMs, CTRs) are labeled as estimates unless pulled from the client's own account data.
- Never invent a quote, a subscriber count, or a metric.
- If the corpus is thin on some theme, say "thin evidence" next to it rather than smoothing it over.
- Verify before delivering: re-read the deliverable against `corpus.md` and confirm each quote appears there verbatim.
