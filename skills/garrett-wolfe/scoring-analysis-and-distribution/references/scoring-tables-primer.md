# Scoring Tables Primer: Everything We Know

The full conceptual model for how Clay-style scoring tables work, why distributions compress, and how to widen them. Read this first if you're new to a scoring engagement. Loaded findings from the Client A engagement (a 44,723-row TAM).

---

## 1. The basic mechanics

```
Per scoring card:
  Raw Score    →  points the firm earned on that card
  Max          →  the highest possible Raw Score for that card = the card's weight
  Golden       →  Raw Score / Max → 0-1 normalized (display-only helper, optional)

Grand Total Score:        SUM of all cards' Raw Scores
Final Score Percentage:   Grand Total / sum of all maxes (e.g. /100 if maxes sum to 100)
```

**Per-card max = the card's weight.** There's no separate `× weight` multiplication step: the scaling lives in the band values themselves. Industry max=22 means Industry contributes up to 22% of Final %.

**Golden columns are display-only.** They exist for readability ("70% on Revenue") but don't feed Grand Total. The Grand Total uses Raw Scores directly.

---

## 2. The two metrics you optimize for

| Metric | What it measures | Target (typical) |
|---|---|---|
| **stdev of Final %** (within DQ=False pool) | Overall spread across the list | ≥ 0.20 usable, ≥ 0.25 great, 0.30+ exceptional |
| **Twin-firm spread** | Δ between two identical firms differing only in axis X. Run for every weighted axis. | ≥ 10 pts on the top 3 axes |

Optimize **both**. stdev alone can be flattered by a long penalty tail without giving you adjacent-row resolution. Twin-firm spread alone can be flattered by one outsized axis weight that compresses the rest.

---

## 3. The 6 levers that actually widen distribution

| Lever | Mechanism | Stdev gain | Architecture availability |
|---|---|---:|---|
| **1. Add bands** | More bands per card = more resolution. A 3-band card emits 3 values; a 9-band card emits 9. Prerequisite for everything else. | +0.02 to +0.06 | All |
| **2. Balance weights** | Spread weight across more axes. Flatter weight distribution → bell-shaped histogram. **Doesn't widen stdev directly**, but widens twin-firm spread on the lifted axis. | +0.00 to +0.01 | All |
| **3. Wide tier gaps within positive bands** | Tier 1 = 22, Tier 2 = 16, Tier 3 = 8. 6+ pt gaps do discrimination work that negatives would do, while staying positive. | +0.02 to +0.05 | All |
| **4. Expanded Hard DQ for objective no-fit** | Move "Industry = software / banks / restaurants" to Hard DQ. Removes from pool (no enrichment spend). Surviving pool has cleaner spread. | +0.01 to +0.04 (on survivors) | All |
| **5. Deep negative bands within cards** | Industry "Other" = −25, Product "software" = −15. Creates F-tier pile separate from candidates. | +0.04 to +0.10 | Pure-card-with-negatives only |
| **6. Cross-axis multipliers** | Fit_Multiplier (0.4-1.8 swing) + Negative_Penalty formula column. Compounds top-tier fit across axes. | +0.06 to +0.12 | With-multipliers only |

---

## 4. What does NOT widen distribution (common traps)

| Tempting move | Why it fails |
|---|---|
| Push more weight into the top axes (Industry/Reps/PE/Product) | Those axes correlate. Firms hitting all of them already top out together. **Tested: pushed Industry 22→28, stdev moved +0.007 but largest 0.01-pct bucket grew from 3.15% to 5.93%.** |
| Raise a card's raw max from 1 to 10 without adding bands | Mathematically identical to original. Golden = score/max → same 0-1 output. Resolution is set by band COUNT, not max value. |
| Add weight to an axis with low coverage | If only 5% of rows have data, bumping its weight only differentiates that 5%. Doesn't widen the histogram. |
| Add weight to an axis derived from another already-weighted axis (Rev/Rep, Fragmentation as Industry lookup) | Double-counts the same signal. Keep redundant axes as tie-breakers (weight 2-5). |

---

## 5. The three architecture options

The choice is **operational, not mathematical**. Ask the client first.

| Architecture | What you can use | What you give up | Stdev ceiling |
|---|---|---|---:|
| **Pure-positive + smart Hard DQ** (recommended default) | All scores ≥ 0. Wide tier gaps. Expanded Hard DQ filters obvious misfits. Soft-fit firms get low positive scores. | Negative bands. Cross-axis multipliers. | **+15-35%** (Client A v10d: 0.178 → ~0.22) |
| **Pure-card with negatives** | Each card max = weight. Deep negative bands within cards. No multipliers. Grand Total can go negative. | Cross-axis compounding. Cross-axis name regex. Operator must accept negative scores in UI. | **+30-60%** (Client A v10c: 0.178 → 0.279) |
| **With-multipliers** | Per-card weights + Fit_Multiplier + Completeness_Multiplier + Negative_Penalty column. Most aggressive. | 3 new formula columns. More complex Grand Total. Cross-axis multiplier harder to explain. | **+50-110%** (Client A v9: 0.178 → 0.367) |

### The deciding question (ask before designing bands)

**Does the client's tool (Clay or similar) STOP enrichment when a row is DQ'd?**

- **YES (Clay default)** → Pure-positive + smart Hard DQ. Reason: negative scores keep enriching rows that will never be customers. Hard DQ stops the waste.
- **NO** → Pure-card with negatives, or with-multipliers if they tolerate the formula columns.

### Hard DQ vs score-low-positive: the rule

- **Hard DQ**: firm's industry/type is *fundamentally* wrong (software, bank, school, restaurant). Future enrichment can't refine it into a fit.
- **Score-low-positive**: firm *might* be misclassified, weak-fit, or have wrong data that better enrichment could refine. Keep in pool with score 0-2.

---

## 6. The five most common bugs in existing rubrics

Always run these 4 detectors in Phase 1.1 before touching weights.

| Bug | Detection | Client A example |
|---|---|---|
| **Default-when-null** | Derived score column has nonzero rate >> source column coverage rate | PE Score Golden = 0.25 on 95% of rows because PE Backers Count defaulted to 1 |
| **Normalization-cap** | A `*_Golden` column's observed max caps well below 1.0 | Territories Golden capped at 0.44 because divisor was too large |
| **Band-gap** | Keyword bands have gaps (`1-5, 11-25, ...`: missing 6-10) | Specialist bands missed 6-10 range in a prior engagement |
| **Empty enrichment** | Column referenced in rubric but <2% populated | Distinct Company Countries = 15.5% populated, contributed to Territories cap |
| **VC-counted-as-PE** | PE detection treats any investor name as PE | 123 of 129 VC-backed firms (Sequoia, a16z, Venrock) scored as PE in original Client A model |

Fixing a single default-when-null bug often does more for the distribution than any weight tuning.

---

## 7. Validation gates: what tells you the rubric works

| Gate | Target | If it fails |
|---|---|---|
| Stdev of Final % (within non-DQ pool) | ≥ 0.20 (target 0.20-0.25 for pure-positive) | Apply more aggressive Lever 3, 4, or 5 |
| Largest 0.01-pct bucket | ≤ 5% | Weights too top-heavy: flatten across mid-tier axes |
| Twin-firm spread on top 3 axes | ≥ 10 pts each | Bump axis weight (only if uncorrelated) |
| DQ threshold separation | DQ rows median ≤ threshold − 10 pts; real candidates median ≥ threshold + 10 pts | Deepen Lever 4 or Lever 5 |
| Top-K named good-fit firms appear in A or B | ≥ 80% of known-good firms | Sourcing gap OR specific bug: re-run Phase 1.1 |
| Histogram shape | Bell-shaped around median; clear separation between F/Low tier and the rest | Apply Lever 2 (balance weights) |

---

## 8. Client A empirical track (worked example, all 10+ versions)

44,723-row Clay export. Started with stdev 0.178, mostly-tied A-tier (~15% of list), DTC consumer brands at the top, default-when-null bugs everywhere.

| Version | What changed | Stdev | Twin-firm Revenue | Architecture |
|---|---|---:|---:|---|
| Original Clay | baseline | 0.178 | <1 pt | n/a |
| v4 | Bug fixes + re-banded all cards | 0.239 | 4 pts | bug-fix prep |
| v5 | + reweight (Revenue 0→7, Employee 7→10) | 0.239 | 4 pts | reweight (no stdev gain: correlation) |
| v6 | + drop bottom clamp + Fit_Multiplier 0.5-1.6 | 0.280 | 7 pts | with-multipliers |
| v7c | + wider Fit_Multiplier 0.4-1.8 + 2× penalty | 0.368 | 13 pts | with-multipliers max |
| v9 | + balance weights | 0.367 | 20.6 pts | with-multipliers final |
| v10 | Switch to pure-card, moderate bands | 0.188 | 11 pts | pure-card baseline |
| v10b | + aggressive negative bands | 0.228 | 12 pts | pure-card-with-negatives |
| v10c | + max-aggressive negatives (Other=−25, software=−15) | 0.279 | 15 pts | pure-card-with-negatives max |
| **v10d (shipped)** | + remove all negatives, expand Hard DQ for objective misfits | **~0.22** | ~10-12 pts | **pure-positive + smart Hard DQ** |

**Why v10d shipped despite lower stdev:** in Clay, DQ stops enrichment. Negative-scoring rows otherwise keep burning enrichment credits forever on firms that will never become customers. v10d's operational benefit (no wasted enrichment + cleaner UX) outweighs the +0.05 stdev gap to v10c.

---

## 9. The implementation pattern for pure-positive + smart Hard DQ

This is the recommended default. Roughly 80-90 min in Clay for a 9-card rubric.

**Step 1: Expand DQ logic** (10 min):
```
DQ2 = OR(
  -- existing
  {FTEs vF} < 50,
  {AI Industry Score} = 0,
  {Domain vF} = "",
  -- NEW: objectively wrong-fit industries
  REGEX_MATCH(LOWER({Normal Industry vF}),
    "software development|saas|computer software|information technology and services|" &
    "financial services|banking|insurance|investment management|" &
    "restaurants|real estate|higher education"),
  -- NEW: Fortune 100
  {FTEs vF} > 10000
)
```

**Step 2: Rewrite each card** (5-10 min each):
- Add bands (Lever 1): 8-12 bands for right-tailed numerics like Revenue/Reps/FTEs
- Use wide tier gaps in positive ranges (Lever 3): Tier 1 = 22, Tier 2 = 16, Tier 3 = 8
- Bottom out at 0 (no negatives)
- Make sure card maxes sum to 100

**Step 3: Rewrite Grand Total** (5 min):
```
Grand Total Score = (pure sum of all 9 Raw Scores)
Final Score Percentage = Grand Total Score / 100
```

**Step 4: Add Tier column** (5 min):
```
Tier = IF(GrandTotal >= 75, "A",
       IF(GrandTotal >= 55, "B",
       IF(GrandTotal >= 35, "C",
       IF(GrandTotal >= 15, "D", "Low"))))
```

**Step 5 ((Optional) Add 9 Golden display columns** (15 min)) one per card, `=Raw / Max`. Display only, doesn't affect math.

**Step 6: Validate against the 6 gates** (above).

---

## 10. Raw Grand Total ≈ 85-95 by design (not 100)

A well-designed rubric with mutually-exclusive bullseyes produces a structural raw max of ~85-95. **No real firm hits every card's bullseye simultaneously** because they imply different firm sizes (e.g. 60-89 reps + 400-799 FTE + $1B-$5B revenue together implies $7.5M revenue per employee: unrealistic for field-sales orgs).

**This is correct behavior.** The Display Score (Phase 3a bell curve) goes 0-100 by construction and is what reps should see. Raw Grand Total is the debugging metric.

Don't "fix" the raw < 100 by loosening bullseyes: that collapses discrimination. The right answer is Display Score + tier off Display Score.

## 11. Tier scheme: 20 tiers at 5% intervals on Display Score

Recommended tier UX (replaces the old 5-tier A/B/C/D/Low scheme).
**Convention: T1 = top (best fit), T20 = bottom (worst fit).**

```
Tier = "T" + (20 - Math.floor(Math.min(0.99, ({{Display Score}} || 0)) / 0.05))
```

(For 0-100 Display scale: `"T" + (20 - Math.floor(Math.min(99, ({{Display Score}} || 0)) / 5))`)

`T1` (Display 0.95-1.00, best) through `T20` (Display 0-0.05, worst). Sort ascending: T1 first. Each tier's expected population is predictable:

| Tier | Display 0-1 range | Expected pop | Notes |
|---|---|---:|---|
| **T1** | **0.95-1.00 (best)** | **~2.4%** | Top priority outreach |
| T2 | 0.90-0.95 | ~0.6% | |
| T3 | 0.85-0.90 | ~1.9% | |
| T5 | 0.75-0.80 | ~4.6% | |
| T10 | 0.50-0.55 (median) | ~10.7% | |
| T15 | 0.25-0.30 | ~4.6% | |
| **T20** | **0-0.05 (worst)** | **~2.5%** | Low-fit; signal monitoring only |

Keep the old 5-tier scheme as a `Tier_Coarse` column for boss-memo summaries ("we have 3% A-tier"). The 20-tier `Tier` is for filtering and stack-rank UX.

## 12. The single most important insight

The **architecture choice precedes the band design.** The same scoring intent (Industry tier 1 = bullseye, software = wrong fit) renders three different ways depending on whether the tool supports cross-axis multipliers, whether DQ stops enrichment, and whether the operator tolerates negative scores in the UI.

**Default to pure-positive + smart Hard DQ + Display Score (bell curve) + 20-tier tiering.** It maps cleanly to how GTM teams actually run enrichment workflows: stop wasting credits on objectively wrong-fit firms (Hard DQ), keep enriching everything else even if they currently score low (because signal monitoring can promote them later), present a clean 0-100% score to non-technical reviewers without negative numbers to explain, and surface 5%-granular tiers for stack-rank filtering.
