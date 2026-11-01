# The checklist

In order. Each section can invalidate everything below it, which is why the plumbing comes before the creative.

## 1. Plumbing

| Check | Failing looks like | If it fails |
|---|---|---|
| Store integration syncing | Order and product data stale or partial | Stop. Every revenue number in the account is wrong. |
| Tracking installed and firing | Viewed Product, Added to Cart, Started Checkout missing or sparse | Browse and cart flows cannot work. This is finding one. |
| Sending domain authenticated | Shared sending domain, or DMARC absent | Deliverability finding, outranks everything creative |
| List growth source | Sudden jumps, imported lists, no signup source data | Suppress and investigate before recommending more sending |
| Suppression hygiene | Bounces and unsubscribes still receiving | Compliance problem, not an optimisation |

## 2. Deliverability

Open rates are unreliable since privacy protection inflated them. Judge on click rate, bounce rate, spam complaints and unsubscribe rate, and on whether those numbers are stable or sliding.

| Signal | Healthy | Investigate |
|---|---|---|
| Spam complaint rate | Under 0.1% | Over 0.3% is urgent |
| Hard bounce rate | Under 0.5% | Over 2% suggests list quality |
| Unsubscribe rate per send | Under 0.3% | Over 0.5% suggests frequency or relevance |
| Click rate trend over 6 months | Flat or rising | Sliding means inbox placement, not creative |

A failing account here gets a one-finding audit. Recommending creative work on an account landing in spam is malpractice.

## 3. Flows, in revenue order

Checked before campaigns, because they run unattended.

| Flow | Present? | Last edited | What to look at |
|---|---|---|---|
| Abandoned checkout | Usually | Often years ago | Timing of the first send, number of steps, whether a discount is given away in step one |
| Welcome | Usually | Often never | Whether it sells or just introduces, and whether it segments by signup source |
| Browse abandonment | Often missing | | Requires tracking from section 1 |
| Post-purchase | Often thin | | Second-order timing against actual repurchase interval |
| Winback | Often missing | | Defined against their real purchase cycle, not a default 90 days |
| Back in stock, price drop | Rarely present | | Only worth it with the catalogue to support it |

For each: does it exist, when was it last touched, how many steps, what does it earn per recipient, and is a discount being given to people who would have bought anyway.

That last question is the one most audits never ask, and on a heavily discounted account it is the biggest finding in the file.

## 4. Campaigns

Six months of sends. Frequency, segmentation depth, and whether performance differs between segmented and full-list sends. Most accounts send to everyone and the numbers show it.

## 5. Segmentation and list

Engagement segments defined and used, VIP or repeat-buyer segment present, sunset policy for the unengaged. An account sending everything to everyone has a deliverability problem arriving in about three months.
