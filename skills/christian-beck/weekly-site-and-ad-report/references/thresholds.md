# What counts as a move

A number is not a finding until it leaves that client's normal range. Small sites swing hard on nothing, and a report that treats every swing as news trains the client to stop reading.

## Establishing normal variance

Take the client's first eight weeks. For each metric, the week-on-week percentage change, highest and lowest. That spread is their normal. Anything inside it is noise for that client.

No eight weeks of history yet? Start with the defaults below and say in the report that the bands are provisional.

| Weekly sessions | Default flag threshold |
|---|---|
| Under 500 | 40% |
| 500 to 2,000 | 25% |
| 2,000 to 10,000 | 15% |
| Over 10,000 | 10% |

Conversions get one band wider than sessions, because the counts are smaller and noisier. Under 10 conversions a week, do not flag percentage moves at all; report the raw count and talk about the trend over four weeks.

## Always flag, whatever the size

- Conversions at zero for a full day with traffic arriving. Tracking, until proven otherwise.
- Spend over or under pacing by more than 20% against plan.
- Cost per conversion moving more than 30% with spend flat.
- Any channel going to zero.
- A single day accounting for more than half the week's sessions.

## Explaining a move, in order

Work the list top down and stop at the first that fits. The order matters because the boring explanations are the common ones, and the interesting explanation is the one that produces a wrong recommendation.

1. **Tracking.** Tag fired? Container published? Did anyone touch the site, the consent banner or the form?
2. **Something we shipped.** A page went live, a redirect, a nav change, a new form. Check the deploy log before theorising.
3. **Something they shipped.** A price change, a product announcement, an email send, a webinar, a conference. Ask rather than assume; clients routinely forget to mention a 40,000-recipient send.
4. **Calendar and seasonality.** Holiday, quarter end, industry event, the week everyone is at a conference.
5. **Platform or market.** Auction pressure, a competitor launch, an algorithm change. Last, and only with evidence from inside the platform, such as impression share or frequency.

## Paid specifics

| Signal | Threshold | Reading |
|---|---|---|
| Frequency | Over 2.5 in a week on a cold audience | Creative fatigue. Refresh before touching budget. |
| Impression share lost to rank | Rising 10 points | A quality or relevance problem, not a budget one |
| Impression share lost to budget | Over 20% | Genuinely budget constrained. This is the one worth more money. |
| Learning phase | Under 7 days or under 50 conversions | Directional only. Say so, recommend nothing. |
| CTR | Down 25% with impressions flat | The creative has been seen too often |

## When nothing moved

Say so in one line and keep the recommendation section. A flat week with a clear recommendation is a useful report. A flat week padded with commentary is how a weekly report loses its slot.
