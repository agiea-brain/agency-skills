# Step 1: Klaviyo data pull and internal audit

Pulls 90 days of Klaviyo data, estimates the revenue opportunity with the math shown, and builds a detailed internal audit as a doc you can comment on. Ends by stopping for your review.

## Prompt

```
Can you run a Klaviyo audit for {brand}? Use the Klaviyo connector to pull the data yourself. This is
read-only: do not change anything in Klaviyo.

Context:
- Brand: {brand}, {URL}
- What they sell + price range: {products and price range}
- Average order value: {AOV}
- Gross margin (approx): {margin}
- Goals for the next 90 days: {goals}
- What they said on the discovery call: {pain points, priorities, budget signals}
- Known issues / already tried: {known issues}
- Upcoming launches/promotions: {launches}
- Who manages email/SMS today: {in-house / agency / nobody}

1. Data pull (last 90 days, compared to the prior 90):
- Account overview: total revenue vs Klaviyo-attributed revenue, split flows vs campaigns, email vs SMS.
- Flows: every live, draft and manual flow. For each: trigger, filters, number of messages, timing,
  recipients, open/click/conversion rate, revenue, revenue per recipient. Review the content of each
  message (offer, product display, personalisation, design issues). Flag missing core flows (welcome,
  browse abandon, cart abandon, checkout abandon, post-purchase, win-back, back in stock, sunset).
- Campaigns: every send. Audience, volume, open/click/conversion, revenue per recipient,
  unsubscribe and spam rates, send frequency, best and worst performers and why.
- List growth: sign-up forms (type, display rules, offer, submit rate), new subscribers per week,
  trend, net growth after unsubscribes.
- Segmentation & deliverability: engaged vs unengaged audience size, whether campaigns go to
  engaged-only segments, bounce and spam complaint rates, sending domain setup.
- SMS (if used): subscribers gained vs lost, consent capture, flow vs campaign usage, revenue.
- Data integrity: check Placed Order, Started Checkout, Added to Cart and Viewed Product for
  missing, duplicated or implausible values. Flag anything that makes the numbers unreliable before
  drawing conclusions from them.

2. Revenue opportunity:
- Pick the 2-4 biggest levers from the data. For each, show the formula with real inputs, e.g.
  "~10.5k back-in-stock requests x 30% restocked x 2-4% purchase x $259 AOV = $16k-$33k / 90 days".
- Use the account's own rates as the baseline. Use industry benchmarks only where the account has
  no data, and say so.
- Be conservative: ranges, not single numbers. Do not double-count overlapping levers. List
  excluded levers as upside.
- Headline: total opportunity per 90 days and annualised.

3. The end report should be a doc I can comment on, for internal review. Full detail, not
client-polished. Please include:
- Executive summary: the opportunity and the math, the 3-5 biggest issues, what to fix first
- Scorecard: red / amber / green for Sign-up capture, Flows, Campaigns, Segmentation,
  Deliverability, SMS, Data & tracking, with one line of evidence each
- Findings by area: what we found (specific numbers and the report or metric they came from), why
  it matters (revenue impact), what to do. Include per-flow and per-email detail, revenue per
  recipient, and benchmark comparisons
- Quick wins: under 2 weeks, outsized impact, ranked
- Structural fixes: ranked by impact vs effort. For each flow rebuild, outline the proposed
  sequence (each message's timing, purpose and core content)
- 30/60/90-day plan with expected outcomes per phase
- Tie-back: how each major finding maps to what they said on the discovery call
- Assumptions and open questions: every assumption behind the revenue math, anything you
  couldn't verify, data that looks wrong
- Proof to capture: screenshots and data points worth showing the client

Then stop. Tell me the audit is ready for review and wait. Do not build the client version until I
say comments are in.
```

## If the account has limited data

Use this instead if the account is under 90 days old, was recently migrated, or has broken tracking.

```
{brand}'s Klaviyo account has limited or unreliable data: {reason, e.g. migrated from Mailchimp 6
weeks ago / Placed Order not tracking}. Run the same audit using whatever data is available, and
state the date range used for every figure. Where the account's own rates are missing, use industry
benchmarks for the revenue math and label each one clearly as a benchmark. Lead the audit with
the data gaps and what needs fixing before the numbers can be trusted.
```

## Output

One internal audit doc, for QA review only. Not a client deliverable.

# Step 2: Review and comments

Check the audit and correct it before anything is built for the client.

Before running the prompt:

- Read the full audit. Sense-check the revenue math, the assumptions list and anything flagged as unverified.
- Leave comments directly in the doc: corrections, numbers to change, findings to cut, points to emphasise, anything the client is sensitive about.
- Decide on scope: which flows, phases and fixes you want to recommend.

```
Comments are in. Read every comment in the audit doc and apply all changes to the agency audit
first. Then give me a short summary of what you changed. Flag any comment you disagree with or
that conflicts with the data, with your reasoning. Do not start the client version until I confirm.
```

Output: the updated internal audit and a change summary in chat. Repeat until the audit is final.
