---
name: klaviyo-account-audit
title: Klaviyo account audit
description: |
  Use this skill when an ecommerce prospect or client has given read access to
  their Klaviyo account and you need to put a dollar figure on what it is
  leaving on the table, then turn that into a client deck and proposal.
  Produces an internal audit for review, a founder-ready client audit, a
  proposal, and a paste-ready Replit prompt that builds the deck. Also use for
  "audit their Klaviyo", "email and SMS audit", "Klaviyo revenue opportunity",
  "build the audit deck and proposal".
category: Marketing
tags: [email-marketing, sms, ecommerce, lifecycle-marketing, audit, proposal]
tools: [klaviyo, replit]
---

Applies once Klaviyo access and the discovery context are in hand. Produces four things in order: an internal audit, a client-facing audit, a proposal, and the deck prompt.

Most Klaviyo accounts leave significant revenue on the table, not through one big failure but through a dozen small ones: missing or outdated flows, campaigns sent to unengaged lists, sign-up forms that barely convert, broken tracking. Founders rarely see the full picture because the data is spread across dozens of reports. This audit puts a dollar figure on that gap, shows the math, and lays out exactly what to fix first.

## The play

1. Set up a Claude Project for the audit with the instructions in references/project-setup.md, and switch on the Klaviyo connector. Start a new chat for every brand. Never reuse a previous brand's conversation.
2. Collect the context before anything runs: brand and URL, what they sell and the price range, AOV, approximate gross margin, 90-day goals, discovery call notes, known issues and what has been tried, upcoming launches, who manages email and SMS today, and brand assets. The full checklist is in references/project-setup.md. Incomplete context produces weaker, more generic outputs, so Claude flags anything missing before Step 1.
3. **Step 1, data pull and internal audit.** Pull 90 days of data against the prior 90, check data integrity before drawing conclusions, size the 2 to 4 biggest levers with the formula shown, and write a detailed internal audit as a doc you can comment on. Then stop. The full prompt, and the alternate for accounts with limited or broken data, are in references/step-1-audit-prompt.md.
4. **Step 2, review and comments.** Read the whole audit, sense-check the revenue math and the assumptions list, and comment directly in the doc. Claude applies every comment and flags any it disagrees with. Repeat until the audit is final. Do not let Claude build the client version until your comments are in.
5. **Step 3, client audit and proposal.** Build a client-facing audit a founder can take in within five minutes, review it against the internal audit for anything missing or too detailed, then build the proposal with every line item tied to a finding. Prompts for all four parts are in references/step-3-client-and-proposal.md.
6. **Step 4, the deck.** Generate a paste-ready Replit prompt for a 15 to 20 slide presentation from the final client audit and proposal, build it in Replit, and add the screenshots. The prompt is in references/step-4-replit-deck.md.

Run all four steps in one conversation, since the proposal needs the audit, your comments and the client version in context.

## What good looks like

- First thing I check that most people skip: whether the data can be trusted. Placed Order, Started Checkout, Added to Cart and Viewed Product get checked for missing, duplicated or implausible values before any conclusion is built on them. Klaviyo attribution is often messy.
- The mediocre version is generic best-practice filler: stock A/B test lists, "creative tips", findings that would be true of any account. Every finding here cites a number from this account's data.
- I know the audit is right when every number traces back to the data, the revenue math uses the account's own rates as the baseline, and the ranges are conservative with no double-counted levers.
- Headlines state the takeaway, not the topic: "Your checkout flow converts at half the benchmark", not "Checkout Flow".
- Red flag: a proposal line item that can't be traced to a finding. Flag it rather than including it.

## Rules

- MUST treat the audit as read-only. Never create, edit, send or delete anything in Klaviyo. If Claude suggests a change in the account, decline it.
- MUST collect all context before Step 1.
- MUST show the formula with real inputs for every revenue figure, using ranges, not single numbers.
- MUST use the account's own rates first, and label any industry benchmark as a benchmark.
- MUST keep the Step 1 audit internal. It is a QA document, not a client deliverable.
- MUST stop after Step 1 and after each review, and wait for comments.
- NEVER show internal rates in the proposal. Package prices only.
- NEVER reuse a previous brand's conversation.
