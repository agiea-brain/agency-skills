# The five numbers

Five, every week, same definitions. The restraint is the point: a client can hold five numbers in their head and will act on them. Twenty metrics get skimmed.

| Metric | Source | Definition | Why this one |
|---|---|---|---|
| Sessions | Google Analytics | All sessions, all channels, excluding internal traffic | The denominator for everything else |
| Conversions | Google Analytics | One named primary event per client, chosen at kickoff | The only number the client's board asks about |
| Conversion rate | Derived | Conversions / sessions | Separates a traffic problem from a site problem |
| Spend | Google Ads + Meta Ads | Total paid media, all platforms, same currency | The input |
| Cost per conversion | Derived | Spend / conversions attributed to paid | The output that decides next week's budget |

## Setting the primary conversion

One event per client, agreed at kickoff, never changed mid-engagement. A demo request, a qualified form fill, a trial start, a booked call. Not "all form submissions", which quietly includes the contact page, the newsletter and the careers enquiry.

Secondary events can be tracked and reported under the fold. They are never promoted into the headline number partway through an engagement, because it breaks every comparison that came before it.

## Segmenting

Report the five totals, then split sessions and conversions by channel group: organic, paid search, paid social, direct, referral. Five channel rows, not twelve sources.

Split paid by platform in the paid section only, never in the headline. The client cares what paid cost in total first, and which platform second.

## Filters that must be in place before any of this means anything

- Internal traffic excluded by IP or by a flag, including the agency's own
- Bot filtering on
- Cross-domain tracking configured if the form or the booking tool lives on another domain
- UTM conventions agreed and used, or every paid click lands in direct and the report is fiction

The cross-domain one accounts for most inherited analytics accounts that report a conversion rate that looks impossibly bad.

## Attribution

Pick a model at kickoff, name it in the report footer, and leave it alone. Platform-reported conversions and analytics-reported conversions will never match, and the gap is normal. Report one as the number of record and mention the other only when the gap itself changes sharply, which usually means a tracking change rather than a performance one.
