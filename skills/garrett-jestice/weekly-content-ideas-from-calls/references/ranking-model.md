# Ranking model

The metric is **comments per 1,000 impressions** (CP1K) on published posts. Likes are passive and follower-weighted; impressions reward reach, not resonance. Comments cost the reader something, so they are the only cheap signal that a post gave someone a reason to speak.

## Build the baseline once

1. Export the last 90 days of posts with impressions and comment counts.
2. CP1K = comments / (impressions / 1,000).
3. Sort and take the median. That is the baseline. Recompute quarterly, not weekly.

Typical ranges for a founder or practitioner account. Use your own numbers once you have 90 days.

| CP1K | Read |
|---|---|
| Under 1.0 | Nobody had anything to say. Topic was agreeable. |
| 1.0 to 2.5 | Working. The normal band. |
| 2.5 to 5.0 | Struck a nerve. Look for what the post did that the others did not. |
| Over 5.0 | Either a genuine position or a fight. Check which before repeating it. |

## Score each candidate idea

Five factors, 1 to 5 each. Total out of 25.

| Factor | 1 | 5 |
|---|---|---|
| Specificity | A topic | A sentence a named role actually said, with a number or a concrete situation in it |
| Tension | Everyone agrees | A real practitioner would push back |
| Recurrence | Heard once | Heard from three or more different buyers |
| Proximity to the buyer's money | Interesting | Costs them revenue, headcount or a deadline right now |
| Past CP1K of the nearest matching post | Below baseline | Top quartile |

## Thresholds

| Score | Action |
|---|---|
| 19 to 25 | Top 3 candidate |
| 13 to 18 | Keep in the 8 to 12 |
| Under 13 | Cut, unless it is the only moment from a client segment with no coverage this quarter |

## Overrides that beat the score

- Repeated by two or more different buyers in the same week: promote to top 3.
- Contradicts something already published: promote to top 3.
- Single client, highly specific, no pattern elsewhere: cap at the 8 to 12, never top 3.
- Any moment that cannot be anonymised: cut, whatever it scores.
