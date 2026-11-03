# Levers: Empirical results from past engagements

Concrete deltas from the four levers, measured on real client datasets.
Use this to answer "which lever should I pull first?" by mapping the symptom
to the lever that empirically moved the right metric.

---

## The 6 levers, ranked by empirical impact

| Lever | Mechanism | Typical stdev delta | Twin-firm spread delta | Architecture |
|---|---|---:|---:|---|
| **1. Add bands (resolution)** | A 3-band card emits 3 values. A 9-band card emits 9. Resolution is the *prerequisite* for everything else. | +0.02 to +0.06 | huge per-axis (3-band → 9-band on Revenue moves spread from <1 pt to 12+ pts) | All |
| **2. Balance weights** | Spread weight across more axes: flattens histogram toward bell. Trim top axes, lift mid-tier axes. | +0.00 to +0.01 (rarely moves stdev) | +30-100% on the bumped axis | All |
| **3. Wide tier gaps within positive bands** | Tier 1 = 22, Tier 2 = 16, Tier 3 = 8. Gaps of 6+ pts do the discrimination work that negatives would do, while staying positive. | +0.02 to +0.05 | n/a | All |
| **4. Expanded Hard DQ for objective no-fit** | Move "Industry = software / banks / restaurants" to Hard DQ instead of trying to score them. Removes them from the pool entirely (no enrichment spend). Surviving pool has cleaner spread. | +0.01 to +0.04 (on the surviving pool) | n/a | All: especially aligned with Clay's "DQ stops enrichment" |
| **5. Deep negative bands within cards** | Push card band minimums to −15, −25 for misfit categories. Industry "Other" = −25, Product Type "software" = −15, etc. Creates a visible F-tier pile separate from candidates. | +0.04 to +0.10 | n/a (acts on penalized rows) | **Pure-card with negatives only** |
| **6. Cross-axis multipliers (Fit_Multiplier + Negative_Penalty column)** | Compounds top-fit firms across multiple axes. Name-regex / pattern penalties. Requires separate formula columns. | +0.06 to +0.12 | +5-10 pts on top tier | **With-multipliers architecture only** |

**Key insight by architecture:**
- **Pure-positive + smart Hard DQ**: Levers 1+2+3+4. Realistic ceiling +15% to +35% stdev. Cleanest UX, aligns with "DQ stops enrichment" workflow.
- **Pure-card with negatives**: Levers 1+2+3+5. Realistic ceiling +30% to +60% stdev. Lever 5 (deep negative bands) does ~half the work.
- **With-multipliers**: Levers 1+2+3+5+6. Realistic ceiling +60% to +110% stdev. Lever 6 adds another ~+50% over pure-card.

---

## What each lever does NOT do

| Lever | Common misconception |
|---|---|
| 1. Add bands | "More bands = wider distribution": partly true, but only if other levers are also applied. Bands alone bumped stdev by +0.061 in Client A; total possible was +0.190. |
| 2. Balance weights | "Pushing weight into the most discriminating axis widens distribution." False if the axis correlates with other top axes. **Tested: pushed Industry 22→28, Reps 20→25, PE 13→18, Product 12→15: stdev moved +0.007 but largest 0.01-pct bucket grew from 3.15% to 5.93%, violating the gate.** |
| 3. Widen Fit_Multiplier | "More aggressive multiplier always wins." False: if Multiplier × 2 pushes top firms past the cap, they all tie at the cap. Drop the cap together with the multiplier widening. |
| 4. Deepen penalty | "Negative scores look weird." Fine if you have an F-tier. The F-tier is a feature, not a bug: it's what creates the visible separation between DQ and real candidates. |

---

## Symptom → Lever decision matrix

| Symptom | Pull this lever | Expected result |
|---|---|---|
| Histogram has a spike of 30%+ of rows in one bin | 1 (bands): that card has too few bands | Spike spreads across multiple bins |
| Card has 3 bands but the data spans 5+ orders of magnitude | 1 (bands) | 8-10 log-shaped bands |
| Two firms identical except one axis differ by <5 pts | 2 (weights) | Bump that axis weight (if uncorrelated) |
| Top-K firms all tied at the cap | 3 (multiplier) + remove cap | Top stretches 20-40 pts above the rest |
| Largest 0.01-pct bucket > 5% (pile-up) | 2 (weights): likely overweighted top axes | Trim top, lift mid-tier |
| Distribution looks bimodal | 2 (weights): usually means one mega-axis dominates the others | Flatten across mid-tier |
| Bad-fit firms scoring in the C/D tier (above the DQ threshold) | 4 (penalty) | Penalty pushes them below the DQ threshold cleanly |
| DQ rows pile at exactly 0 (floor clamp) | 4 (drop clamp) | Bottom extends to -30/-60, F-tier separates from D-tier |
| stdev is low AND no obvious pile-up | 3+4 (multiplier and penalty together) | +0.06-0.09 stdev |
| stdev is fine but stack-rank "feels samey" | 2 (weights) | Twin-firm spread improves; histogram more bell-shaped |
| Top-25 named good-fit firms aren't appearing in A | NOT a lever: investigate sourcing gap or specific bug in Phase 1.1 | Fix root cause |

---

## Worked example: Client A scoring engagement

### With-multipliers track (full architecture)

| Stage | What changed | stdev | Twin-firm Revenue | Largest bucket | A-tier % | Lever(s) used |
|---|---|---:|---:|---:|---:|---|
| Original Clay (44,723 rows) | baseline | 0.178 | <1 pt | 3.79% | ~15% (3,400) | n/a |
| v4 | Bug fixes + re-banded all cards | 0.239 | 4 pts | n/a (clamp pile-up) | 0.9% (396) | 1 |
| v5 | + reweight (Revenue 0→7, Employee 7→10) | 0.239 | 4 pts | n/a (clamp pile-up) | 1.1% (476) | 2 (no stdev impact) |
| v6 | + drop clamp + widen Fit_Multiplier 0.5-1.6 | 0.280 | 7 pts | 3.15% | 1.7% (782) | 4 |
| v7c | + wider Fit_Multiplier 0.4-1.8 + ~2× penalty | 0.368 | 13 pts | 3.72% | 3.1% (1,386) | 4 stronger, 5 stronger |
| **v9 (with-multipliers final)** | + balance weights: Industry 22→18, Reps 20→18, Revenue 7→12, Employee 10→12 | **0.367** | **20.6 pts** | **2.96%** | **3.4%** | **2 (now visible in twin-firm)** |

### Pure-card with-negatives track

| Stage | What changed | stdev | Twin-firm Revenue | A-tier % | F-tier % | Lever(s) used |
|---|---|---:|---:|---:|---:|---|
| v10 | Pure card, moderate bands | 0.188 | 11 pts | 0.5% | 0.1% | 1 |
| v10b | + aggressive bands (Other=−15, software=−8) | 0.228 | 12 pts | 0.3% | 8.2% | 1+5 (moderate) |
| **v10c (pure-card final)** | + max-aggressive bands (Other=−25, software=−15) + intra-card PE tie-breaker | **0.279** | **15 pts** | **0.2%** | **14.5%** | **1+2+5 maxed** |

### Pure-positive + smart Hard DQ track (RECOMMENDED for Clay GTM workflows)

| Stage | What changed | stdev (est.) | Pool size | Architecture benefit |
|---|---|---:|---:|---|
| **v10d (final)** | All bands positive (Other=1, software=0); expanded Hard DQ on Normal Industry contains [software \| banks \| schools \| restaurants \| real estate]; Hard DQ mega-corps (FTE >10K) | **~0.22** | ~12K-15K candidates (down from 22K) | All scores 0-100. No negatives in UI. DQ'd rows don't waste enrichment credits. Soft-fit rows stay enriched and can promote on signals. |

**What this tells you:**
- Bug fixes + Lever 1 alone: +0.061 stdev (huge first move regardless of architecture)
- Lever 2 alone: +0 stdev BUT +400% twin-firm spread on the lifted axis
- Lever 5 (deep negative bands): +0.05 to +0.09: only available in pure-card-with-negatives
- Lever 6 (multipliers): +0.09: only available with-multipliers
- Lever 4 (expanded Hard DQ): substitutes for ~half of Lever 5's gain in pure-positive architecture
- **Pure-positive + smart DQ ceiling: ~+22% stdev (v10d)**
- **Pure-card with negatives ceiling: +57% stdev (v10c)**
- **With-multipliers ceiling: +107% stdev (v9)**
- **Gap between architectures is real but operational considerations matter more.** Client A chose v10d because Clay's "DQ stops enrichment" behavior makes negative-scoring rows operationally wasteful: they keep getting enriched but will never be customers.

**Failed variant (don't do this regardless of architecture):** pushed Industry/Reps/PE/Product weights aggressively. stdev moved +0.005 over v7c but largest bucket grew to 6.08%, violating the gate. Confirms: pushing weight into correlated top axes does NOT widen distribution.

## The architectural decision flowchart

```
Ask: Does the client's tool (Clay or similar) STOP enrichment when a row is DQ'd?

  YES (Clay default) ──► Recommend pure-positive + smart Hard DQ (v10d pattern)
                          Rationale: negative scores keep enriching rows that will never
                          be customers. Hard DQ stops the waste.

  NO  ──► Ask: Does the client tolerate cross-axis multipliers in formulas?

           NO  ──► Pure-card with negatives (v10c pattern)
                    Use Lever 5 (deep negatives) for spread

           YES ──► With-multipliers (v9 pattern)
                    Maximum spread, accepts 3 new formula columns
```

Default to pure-positive + smart Hard DQ unless the client explicitly asks for the extra stdev.

---

## Worked example: Client B (anonymized)

### Pure-positive + smart Hard DQ + bell curve normalization

A 41,652-row export with two entity types in one list. It started at stdev 8.2 on a 100-point scale, with scores compressed into the 0-20% range and a median of 9%.

**Root causes found in Phase 1:**
- 51% of rows were a structurally wrong-fit entity type
- Two axes were over 90% saturated, so they added a constant rather than differentiation
- 4 axes had under 5% coverage but carried 30% of the weight
- The denominator was 39 while the theoretical max was 50, and nobody could reach 39

| Stage | What changed | Raw stdev | Display stdev | Architecture |
|---|---|---:|---:|---|
| Original | baseline | 8.2 | n/a |: |
| v3 | Aggressive DQ, percentile-based bands on every card, weight moved from saturated axes to data-rich ones, maxes sum to 100 | 14.6 | n/a | Pure-positive + smart Hard DQ |
| v3 + bell curve | Display Score column: inverse-normal CDF on percentile rank, mean 50, std 20. Cards untouched | 14.6 | **20.2** | Pure-positive + bell curve display |

**Key insight:** the raw stdev plateaued at 14.6 because 30% of the weight sat on axes with under 5% coverage. More rubric rounds added less than 0.5 stdev each. Bell curve normalization added 5.6 display stdev by mapping the correct ranking onto a full 0-100 scale.

**Implementation details:**
- Scoring cards use Clay's band UI. Clayscript is only for formula columns: DQ, Grand Total, Display Score, Tier.
- The Display Score formula reads `{{Score Percentage}}` and must wrap its null guard in parens: `({{Score Percentage}} || 0)`. Clay strips `const` declarations, which breaks operator precedence.
- A Contains (Text) card must list every value explicitly. Missing values score 0 with no error; in this case coverage on one card fell from 98% to 48%.

**What this tells you:**
- Aggressive DQ is a prerequisite, not a lever. No weight tuning fixes a pool that's 51% non-ICP.
- Weight must follow coverage. Weight on a 5%-populated axis means 95% of rows score 0 on it.
- Saturated axes should carry minimal weight.
- Bell curve normalization is a legitimate final step once the raw stdev ceiling is hit. It extends a correct ranking; it doesn't replace rubric work.

---

## The "DQ threshold" calibration

Clients often want a natural cutoff (e.g. 40%) that cleanly separates DQ from real candidates. Validation:

| Check | Pass condition |
|---|---|
| DQ pile median | ≤ (threshold − 10 pts on the 100-pt raw scale) |
| Real candidates median | ≥ (threshold + 10 pts) |
| No firms between (threshold − 5) and (threshold + 5) | Ideally ≤ 5% of full list: the threshold should fall in a natural valley of the histogram |

If the histogram doesn't have a natural valley at the threshold, you can either (a) move the threshold to where the valley actually is, or (b) deepen the Negative_Penalty so the DQ pile shifts further down and a valley opens.

---

## Twin-firm test protocol

For each weighted axis (weight ≥ 5), run this:

1. Pick a real top-15 firm as the template
2. Clone it 8-10 times, varying ONLY axis X across its full realistic range
3. Score all clones
4. Report: spread between min and max clone, span of axis X values tested

Example output from a Revenue test on one top-15 account (Client A):

```
Revenue    v7c     v9 (lifted)
$1M       143.3   139.3
$10M      146.2   143.1
$100M     153.1   153.3
$1B       156.3   159.9
$25B      149.1   147.5

v7c spread $1M-$1B: 13 pts    v9 spread: 20.6 pts (+58%)
```

A passing test: **spread ≥ 10 pts on the top 3 axes by weight.**

If an axis fails the test, the diagnosis is usually one of:
- Card has too few bands → Lever 1
- Axis weight too low → Lever 2 (if uncorrelated)
- Axis is just not very discriminating in this dataset → leave it as a tie-breaker (low weight is correct)
