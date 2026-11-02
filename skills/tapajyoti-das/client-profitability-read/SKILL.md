---
name: client-profitability-read
title: Client profitability read
description: |
  Use this skill when the firm is busy and the money does not reflect it,
  or before any decision about which clients to keep. Produces what each
  client actually earns per hour once revisions, account management and
  unbilled calls are counted, ranked, with the ones losing money named.
  Also use for "which clients actually make money", "effective hourly
  rate", "why are we busy and broke", "is this client worth it".
category: Finance
tags: [profitability, effective-rate, margin, client-mix, utilization]
---

Applies to a book of clients where fees are known and real delivery time is not. Produces the ranked read and the decisions it forces.

## The play

1. Get the fee per client for the period first, which is the easy half and the only half most firms have.

2. Then get the hours, and get them honestly. Not the hours in the scope, the hours that happened. Three places they hide:
   - Revisions beyond what was quoted.
   - Account management: the calls, the Slack replies, the status updates, the chasing. Rarely tracked and often the largest line.
   - Senior time spent unblocking juniors on that account.

3. Load the hours with a real cost, not a salary divided by 2,080. Include the non-billable share of each person's week, because a delivery person who is 60% billable costs the firm the whole week either way.

4. Calculate effective rate per client: fee divided by loaded hours. This is the number the whole exercise exists for, and it is usually nothing like the rate card.

5. Rank the book by it and look at the top and bottom together. The pattern matters more than any single client: it is usually a service line, a client size, or a particular kind of stakeholder rather than a bad client.

6. Name the clients below cost explicitly. A firm cannot decide about a client it has not been told is losing money, and the reason this read gets avoided is that the answer is frequently the biggest logo.

7. For each one below the line, say which lever applies: raise the price, cut the scope, change who delivers it, fix the process that is burning the hours, or let them go. Most of the time it is the process, not the price.

8. Note what you could not measure and how much it would move the answer. A read with a known gap in it is usable. One that implies precision it does not have gets a decision made on it and then gets blamed.

## What good looks like

- First thing I check that most people skip: account management time. Everybody counts delivery hours and almost nobody counts the calls, the Slack threads and the status updates. On the clients that look fine until you measure, that is where the margin went.
- The mediocre version: revenue per client sorted descending, which answers a different question and flatters the biggest account, which is frequently the worst one.
- I know it is right when the ranking surprises somebody. If it confirms what everyone already assumed, the hours are probably still coming out of the scope document rather than out of reality.
- Second test: at least one client is named as below cost. A read where everything is profitable has not loaded the hours properly.
- Red flag: the answer for every underwater client is "raise the price". Usually the hours are being burned by a process nobody has looked at, and raising the price just means being underwater more slowly.

## Rules

- MUST use hours that happened, not hours that were scoped.
- MUST include revisions, account management and senior unblocking time.
- MUST load hours with a cost that accounts for non-billable time.
- MUST rank the book and state the pattern, not just the individual results.
- MUST name any client below cost explicitly.
- MUST assign a lever to each client below the line.
- MUST state what could not be measured and how much it could move the result.
- NEVER present revenue per client as profitability.
- NEVER imply precision the time data does not support.
