# A/B Testing Cold Email Copy

How to run a test that teaches you something. `references/ab_test.py` does the math: sample size,
minimum detectable effect, and the Bayesian readout. Researched 2026-10-26. The sample sizes here
come from the standard two-proportion formula, not vendor blog figures, which are mostly too small.

---

## 1. The hard truth: you can only detect big effects

Positive reply rates are 0.5-3%, so a test needs thousands of sends per arm to see anything short
of a doubling.

**Sends per arm** (two-sided α = 0.05, 80% power; metric = positive reply rate per unique lead):

| Baseline PRR | +25% | +50% | 2x | 3x |
|---|---|---|---|---|
| 0.5% | 56,193 | 15,599 | 4,673 | 1,553 |
| 1.0% | 27,937 | 7,750 | 2,319 | 769 |
| 1.5% | 18,519 | 5,134 | 1,534 | 507 |
| 2.0% | 13,809 | 3,826 | 1,141 | 376 |
| 3.0% | 9,100 | 2,518 | 749 | 245 |
| 5.0% | 5,333 | 1,471 | 435 | 141 |

A directional bar (α = 0.10) needs ~20% fewer sends. Quick approximation:
`n ≈ 16·p̄(1−p̄)/(p2−p1)²`.

**What follows:**
- **Vendor floors of 100-500 per variant only detect a 3x+ effect.** Eric's repo table (500 per arm
  for 2x at 1%) is about 4-5x too small. Use the table above.
- **Count events, not sends.** Read nothing until each arm has ~10 positives; trust it at ~30.
- **Size the test from your volume.** Fix the sends you can actually afford in the window, then
  solve for the minimum detectable effect (`ab_test.py mde`). If the MDE is above 2x, only list,
  offer, angle or segment changes are worth testing. Subject, PS and length tests have to wait for
  10k+ sends a month or pooled tagging (§5).

## 2. What to test, in order

**list/segment > offer > angle (lever / problem) > first line > CTA > subject > length/format > PS
> send time / sender.** Leverage shrinks down the list, and so does the effect you can expect, so
the order is forced by the math as much as by the experts.

At Eric's volume (~1.5M a month) Growth Engine X tests **segment × offer × angle as separate
campaigns** and "front-loads" testing: 11 segmented campaigns cracked one offer in ~48 hours. He
builds messages from swappable parts (value prop, problem statement, case study) and tracks each
trigger by its positive-reply ratio.

## 3. Test design

- **Whole-sequence tests (offer, angle, segment) run as separate campaigns.** Split the leads at
  random *before* upload, stratified by list batch and segment.
- **Step-1 tests (subject, first line, CTA) run as in-step variants.** Instantly assigns a variant
  at random **at each step, with no matching across steps** (a lead can get 1A then 2B), so
  in-sequence variants can't compare whole sequences. A new subject on a step 2+ variant breaks
  the thread.
- **One variable per test.** Multivariate needs n × cells, which is impossible here. The exception
  is **factorial tagging**: vary factors deliberately across many campaigns, tag every factor, and
  read main effects by pooling (§5).
- **Champion / challenger.** Keep a standing champion and run one challenger at a time, **50/50**
  (a 70/30 split needs ~25-40% more total sends for the same power). Promote by the rubric (§7),
  then write the next challenger.
- **Holdout for signal plays.** To learn whether a trigger or the sequence adds anything at all, keep
  5-10% of eligible leads unsent and compare meetings from any source over 60-90 days.
- **Turn Instantly auto-optimize off for real tests.** It optimizes raw reply, click or open rate,
  never positive replies, and has no documented threshold. Replies arrive late, so it commits to
  early leaders, and a variant can "win" because it landed on healthier mailboxes. Use it only to
  prune obvious duds (0 positives vs 6+ after ~1,000 sends each). Switch it off on any campaign
  that is a declared test.
- **Commit to n before launch.** Peeking and stopping on a lead is the top cause of false wins. If
  you must look early, plan 2-3 looks in advance.
- **Close a test only after every lead finishes the sequence plus 7 days.** That's typically 3-5
  weeks. Instantly's "5-7 days" is too short for multi-step sequences.

## 4. Metrics and confounders

**Metrics, in order:** positive reply rate per unique lead contacted (define "positive" before
launch) → meetings per 1,000 leads → qualified pipeline per 1,000 → closed-won per 1,000 (lagging;
use for offer decisions). Diagnostics only: bounce, unsubscribe and negative-reply rate, raw reply
rate, opens. A variant with more opens but fewer replies is clickbait, so kill it.

**Confounders to balance:**
- **Inbox placement:** variants with links, images or spammier words land differently. Run a
  placement seed test per arm, and compare bounce and negative replies.
- **Mailbox and domain:** every arm rotates across the same mailbox pool. Never give a variant its
  own domain. Log the mailbox on every send.
- **Day and time:** randomize within day.
- **List batch and enrichment vintage:** split every batch across all arms.
- **Segment mix:** stratify, or analyse within segment.
- **LinkedIn touches** on the same leads: balance them across arms or exclude.
- **Mid-test edits void the test.**
- **Novelty decay:** a winning opener wears out at volume ("never send the identical opener at
  volume", Eric).

## 5. Tag everything (so small tests pool)

Every campaign spec declares its copy choices from a **fixed vocabulary**, never free text. A
campaign that changes nothing from the champion says so.

| Tag | Values |
|---|---|
| `lever` | make_money, save_time_money, reduce_risk |
| `segment` | the segment_id from the messaging map (`segments-and-offers.md`) |
| `trigger_type` | none, funding, new_exec, new_hire, promotion, job_post, launch, m_and_a, earnings, fye, permit, website_visit, competitor_engagement, content_download, event, champion_move, intent, tech_change, sports, weather, calendar, other |
| `offer` | the offer_id from the messaging map, or `none` |
| `hook_type` (first line) | signal, observation, question, peer_proof, pain, search, billboard |
| `cta_type` | soft_question, interest_check, value_exchange, confirmation, referral, calendar, none |
| `proof` | named_client, metric, none (or the client-specific proof id) |
| `ps_type` | none, fact_reaction, social_proof, soft_offer, signal, referral |
| `subject_type` | signal, name, offer, problem, question |
| `length_band` | ≤50, 51-75, 76-100, 101-125 |

Record `test_id` and `arm` (champion / challenger / holdout) on every lead in a test, plus
`trigger_age_days` for trigger plays.

## 6. Test log (one per test, saved with the campaign spec)

```
Test ID:            T-YYYY-MM-DD-<short-name>         Owner:        Opened / closed:
Hypothesis:         For <segment>, <challenger> beats <champion> on PRR because <reason>.
Variable changed:   (exactly one)
Held constant:      list source, segment, mailboxes, schedule, steps, delays, everything else
Champion:           copy link + tags                  Challenger:   copy link + tags
Primary metric:     PRR per unique lead; "positive" = interested + soft + referral
Secondary:          meetings / 1k, bounce, negative-reply rate
Baseline PRR:       x% (source)   MDE: x   α / power: .05 / .8 (or Bayes thresholds)   n per arm: x
Allocation:         50/50, lead-level, stratified by batch + segment + day   Planned looks: x
Preflight:          variables non-empty, step-1 delay > 0, auto-optimize OFF, placement seed per arm
Results:            n, positives, PRR, 95% CI per arm | meetings/1k | P(B>A) | expected loss
Validity:           bounce per arm, open parity, placement per arm, mailbox/day balance
Decision:           PROMOTE / KEEP CHAMPION / EXTEND / ABANDON / KILL (harm)
Learning:           one generalizable sentence          Next test:
```

## 7. Decision rubric

1. **Validity gate** (fail any one = void): planned n reached; every lead finished the sequence plus
   7 days; bounce under 2% and within 0.5 points between arms; open or placement parity within ~20%;
   no mid-test edits; mailboxes and days balanced.
2. **Promote the challenger** when P(challenger > champion) ≥ 0.90 on PRR (p < 0.05 for permanent
   house-rule changes), expected loss < 0.1 point, the winner has ≥10 positives, and meetings per
   1k don't move the other way.
3. **Keep the champion** when P ≤ 0.10, or when the challenger raises raw replies but lowers PRR or
   meetings.
4. **Inconclusive** (0.10 < P < 0.90): extend once to 1.5x n if the upside is worth it. Otherwise
   keep the simpler or cheaper variant and log "no detectable difference at MDE x".
5. **Stop for harm** at any time: bounce over 3%, a spike in complaints or unsubscribes, or a
   placement drop.
6. **A win in one segment is a hypothesis for the next**, not a rule.

## 8. Bayesian readout (what `ab_test.py analyze` does)

Each arm's PRR posterior is `Beta(a0 + positives, b0 + sends − positives)`, with a weak prior
centered on the historical rate (Beta(1, 99) for ~1%). Report:
- **P(B > A)**, by Monte Carlo draws from both posteriors;
- **Expected loss** of choosing B: `E[max(pA − pB, 0)]`. Stop when it's below tolerance (0.1 point);
- the result under a second prior. If the decision flips, it isn't a decision yet.

Bayes doesn't create information. It makes acting under uncertainty explicit, which is what a
low-volume operator needs.
