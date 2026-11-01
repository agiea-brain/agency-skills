---
name: klaviyo-account-audit
title: Klaviyo account audit
description: |
  Use this skill when an e-commerce prospect or client hands over Klaviyo
  access and the account needs auditing before anyone proposes work.
  Produces the findings ranked by revenue at stake, and a filled-in Replit
  prompt that builds the audit deck from them. Also use for "audit their
  Klaviyo", "email audit for [client]", "what's broken in their flows",
  "build the audit deck".
category: Marketing
tags: [email-marketing, audit, ecommerce, lifecycle-marketing, pitch]
tools: [klaviyo, replit, shopify]
---

Applies when Klaviyo access arrives, before any proposal is written. Produces ranked findings with revenue attached to each, and the Replit prompt that turns them into the deck.

## The play

1. Check the plumbing before judging any campaign. Tracking installed and firing, the store integration syncing, deliverability authenticated, list growth real rather than purchased. Broken plumbing invalidates every number underneath it, and the checks are in references/audit-checklist.md.
2. Audit the flows before the campaigns. Flows run without anyone touching them, so a broken flow has been losing money every day since it broke, while a weak campaign lost money once. The order to check them in, and what each should be earning, is in references/audit-checklist.md.
3. Attach a revenue number to every finding. Not "the welcome flow is weak", but what it currently earns per recipient against what comparable accounts earn, multiplied by volume, as an annual figure. The method and the benchmarks are in references/revenue-sizing.md. A finding with no number is an opinion and gets cut.
4. Rank by revenue at stake, then by effort. The top three are what the deck is about. Everything else is an appendix, and most of it should not be in the deck at all.
5. Branch by what the account shows:
   - Flows missing entirely: the finding is the gap, and these are usually the largest and cheapest wins in the account.
   - Flows present but untouched since setup: check the dates. A flow last edited two years ago is running on a product catalogue and a price list that no longer exist.
   - Heavy discounting in every flow: the problem is margin, not email. Size it that way or the audit recommends more of what is hurting them.
   - Strong account overall: say so plainly and find the two real things. A padded audit on a good account is how a firm loses a sophisticated prospect.
   - Deliverability failing: nothing else matters. That becomes the whole audit.
6. Fill the prompt in references/replit-deck-prompt.md with the ranked findings and generate the deck. The prompt is filled with findings, never with raw exports, because a deck assembled from screenshots of the account is a report rather than an argument.
7. Review the generated deck against the findings before it goes anywhere. The prompt produces a draft, not a deliverable, and every number on a slide is checked against the source.

## What good looks like

- First thing I check that most people skip: when each flow was last edited. Accounts look busy and are actually frozen, and the edit dates say so in ten seconds.
- The mediocre version: a long list of best practices the account is not following, no numbers, screenshots of every flow, and a recommendation to do all of it. It demonstrates knowledge and sells nothing.
- I know the audit is right when the first slide says a single number the prospect did not know, and they ask how it was calculated.
- Second test: three findings, not fifteen. A prospect who agrees with three things buys. A prospect handed fifteen feels audited.
- Red flag: the findings would be true of any account in the category. That is a template, and they have seen it.

## Rules

- MUST verify tracking and store integration before reading any performance number.
- MUST attach a revenue figure to every finding in the deck.
- MUST rank by revenue at stake, and cut to three.
- MUST state the benchmark source and the assumptions behind every projection.
- MUST review the generated deck against the findings before sending.
- NEVER put a finding in the deck that cannot be sized.
- NEVER present a projection as a guarantee, and never quote a range tighter than the data supports.
