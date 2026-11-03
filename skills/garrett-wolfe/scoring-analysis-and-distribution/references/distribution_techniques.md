# Distribution Techniques: Phase 2 default upgrades

Reference formulas, thresholds, and worked examples for the six structural upgrades
called out in `SKILL.md` Phase 2. Apply these *before* spending on net-new
enrichment: they're free distribution-shape wins on existing data.

Each section: what it does, when to apply, formula, worked example.

---

## 1. Log transforms on heavy-tailed numeric axes

**What it does.** Replaces fixed bands with a smooth log curve. Preserves rank order
between firms in the same band that banding throws away.

**When to apply.** Any right-tailed numeric axis where P75 / P25 ratio > 4 or where a
single band catches > 30% of rows. Examples: practitioner count, specialist count,
public filings, FTEs, office count, headcount-by-role columns.

**Formula.**
```
score = min(max_pts, k * log10(value + 1))
```
Pick `k` so that the realistic top of the distribution hits `max_pts`. Quick rule:
`k = max_pts / log10(p99_value + 1)`.

**Worked example: specialist headcount (Client B).**

Original bands: `1-5=2, 6-10=2.5, 11-25=3, 26-50=4, 51-100=5, 101-250=6, 251+=7`.
Data: P50=0, P75=3, P99=55, max=1000.

Log replacement: `score = min(7, 2 * log10(specialists + 1))`
- 1 specialist  → 0.6
- 5      → 1.6
- 10     → 2.1
- 25     → 2.8
- 50     → 3.4
- 100    → 4.0
- 250    → 4.8
- 1000   → 6.0
- 10000  → 7.0 (capped)

Compared to original bands, a firm with 7 specialists now scores 1.8 instead of
sharing the same 2.5 with firms that have 10. Rank order within a 5x value range
is recovered.

---

## 2. Multiplicative fit gates

**What it does.** Compounds advantages across signals so high-fit firms separate
from the middle. Pure additive scoring is too forgiving: a firm with one strong
axis ends up close to a firm with five medium axes.

**When to apply.** Whenever distribution has no clear elite tier (top 10 too close
to top 100). Also when client wants the top 1-5% to visibly stand apart.

**Formula.**
```
Final = (sum of universal axis points) × Domain_Fit_Multiplier × Activity_Multiplier
```

**Tunable multipliers.** Calibrate to client. Example defaults for a service-firm TAM:

```
Domain_Fit_Multiplier:
  has_domain_focus=true AND specialists ≥ 10:  1.5
  has_domain_focus=true OR specialists ≥ 5:    1.2
  neither:                                   0.8

Activity_Multiplier:
  public_filings_last_12mo > 0 OR recent_activity < 365d:  1.3
  otherwise:                                                  1.0
```

Cap product at e.g. 2.0 so a single firm doesn't completely dominate.

**Worked example.** Two firms, both raw additive score = 15:
- Firm A: 12 specialists, domain focus = true, recent public filings
  → 15 × 1.5 × 1.3 = **29.25**
- Firm B: 0 specialists, domain focus = false, no recent activity
  → 15 × 0.8 × 1.0 = **12.0**

The 15-point tie becomes a 2.4× separation. Distribution stretches as a direct result.

---

## 3. Type-aware scoring for mixed populations

**What it does.** Handles lists with structurally different entity types (service firms
+ in-house teams in the same TAM) without averaging signal away.

**When to apply.** When the same list has > 5% non-primary-type rows AND the client
wants both segments scored on a comparable scale. Don't average-default a single
rubric: it dilutes signal for both populations.

**Pattern.** Split axes into three groups; compute two parallel scores; each row
gets its segment's score.

### Axis taxonomy

| Group | Behavior in service-firm rubric | Behavior in corporate rubric |
|---|---|---|
| Universal (country, FTE, public filings, domain mentions, domain leadership, recent activity) | Score normally | Score normally |
| Service-firm-only (practitioner count, specialist count, classification, domain expertise, number of offices) | Score normally | Weight = 0 (don't penalize, don't credit) |
| Corporate-only (Filing-heavy industry tier, in-house team size, R&D-intensity proxy, filings-per-FTE) | Weight = 0 | Score normally |

### Formula

```
Score_ServiceFirm = sum(universal_pts + service_firm_pts) / denominator_ServiceFirm
Score_Corporate = sum(universal_pts + corporate_pts) / denominator_Corporate

# Each row picks its segment based on classification
if classification in {Service Type A, Service Type B, Both}:
    Final = Score_ServiceFirm
elif classification in {Corporate, Corporate / In-House}:
    Final = Score_Corporate
else:  # ambiguous
    Final = max(Score_ServiceFirm, Score_Corporate)
```

### Corporate-only axes: recommended starter bands

| Axis | Source | Bands |
|---|---|---|
| Filing-heavy industry | NAICS / industry classification | Core industries = 3 ; adjacent = 1 ; unrelated = 0 |
| Filings per FTE | (public_filings / fte) | top 10% = 3 ; top 25% = 2 ; top 50% = 1 ; else 0 |
| In-house team size | LinkedIn count of employees with the relevant role keywords in title | log10 transform, max 3 |
| Filing history size | Public Filings | log10 transform, max 3 |
| Public filings mention the domain | EDGAR full-text | boolean = +1 |

---

## 4. Data-completeness confidence multiplier

**What it does.** Prevents sparse-data rows from accidentally ranking high on
partial info. A firm with only 3 of 15 fields enriched and scoring 0.7 on those
3 fields shouldn't beat a firm with 12 of 15 fields enriched scoring 0.6 on all.

**Formula.**
```
completeness = (# enrichable fields non-null) / (total enrichable fields)
confidence = 0.7 + 0.3 * completeness   # ranges 0.7 to 1.0
Final_adjusted = Raw_Score * confidence
```

**Tuning.** The 0.7 floor and 0.3 weight are starting points. Tighten the floor
(e.g., 0.5) if data sparseness is a known structural problem; loosen it if most
rows are well-enriched and you just want a small bonus for completeness.

**Don't apply to.** Universal/structural axes that are *expected* to be 100%
populated (country, classification). Apply only to enrichment-dependent axes.

---

## 5. Percentile-rank normalization within segments

**What it does.** Computes per-segment percentile rank and uses it as the score.
Guarantees a uniform distribution per segment. Each segment's top 1% sits at 99%,
each segment's bottom 1% at 1%: directly comparable across segments.

**When to apply.** When client wants a cleaner-looking headline distribution OR
when the rubric's natural ceiling differs by segment (e.g. service firms can hit 90%,
corporates cap at 60% structurally).

**Formula.**
```
for each segment S:
    rank firms in S by Raw_Score
    Percentile_within_S = rank / count(S)

# Blend with raw to keep absolute meaning
Final = 0.5 * Raw_Score_pct + 0.5 * Percentile_within_S
```

**Trade-off.** Pure percentile loses absolute meaning ("a 70%" no longer means
"hit 70% of the rubric"). Blended preserves both. Always explain the choice to
the client and label the column unambiguously.

---

## 5a. Bell curve normalization (inverse-normal CDF on percentile rank)

**What it does.** Maps the non-DQ pool's percentile rank through an inverse-normal
CDF to produce a bell-curve-shaped 0-100 Display Score. Preserves the exact ranking
from the raw rubric but distributes scores symmetrically around 50 with a standard
deviation of ~20. Reps see intuitive "best = 95, worst = 5" scores without needing
to understand the raw rubric's compressed scale.

**When to apply.** When the raw rubric produces correct rankings but the natural
score ceiling is far below 100 (common when low-coverage axes account for a large
share of the rubric weight). The raw scores compress into a narrow band (e.g., 0-50
on a 100-pt scale) and non-technical stakeholders interpret them as "everyone is
bad" instead of "the scale is compressed." Bell curve normalization fixes the
presentation without altering the ranking.

**Architecture.** This is a display-layer technique that sits ON TOP of the raw
rubric. It does not replace the rubric: it transforms the raw Grand Total into
a Display Score via a lookup formula. The raw Grand Total and per-card scores
remain unchanged and are the source of truth for debugging and rubric iteration.

**Formula.**
```
# Step 1: Compute percentile rank within non-DQ pool
percentile = rank(Grand_Total) / count(non_DQ_rows)

# Step 2: Inverse normal CDF → z-score
z = norm.ppf(clamp(percentile, 0.0005, 0.9995))

# Step 3: Scale to mean=50, std=20, clamp to 1-99
Display_Score = clamp(round(50 + z * 20), 1, 99)
```

**Clay implementation.** The inverse-normal CDF cannot be computed natively in Clay.
Instead, pre-compute the Grand Total → Display Score mapping table from the current
data, then implement as a **formula column** (NOT a scoring card) using Clayscript
chained ternary operators. Scoring cards use the Clay band UI; this is one of the
few columns that requires Clayscript:

```javascript
// Display Score: Clayscript formula column (type: Number)
// Pre-computed from inverse-normal CDF on the non-DQ pool
({{Grand Total Score}} || 0) >= 71 ? 99
: ({{Grand Total Score}} || 0) >= 66 ? 95
: ({{Grand Total Score}} || 0) >= 62 ? 90
: ({{Grand Total Score}} || 0) >= 58 ? 87
: ({{Grand Total Score}} || 0) >= 55 ? 84
: ({{Grand Total Score}} || 0) >= 51 ? 80
: ({{Grand Total Score}} || 0) >= 48 ? 77
: ({{Grand Total Score}} || 0) >= 46 ? 75
: ({{Grand Total Score}} || 0) >= 43 ? 71
: ({{Grand Total Score}} || 0) >= 40 ? 68
: ({{Grand Total Score}} || 0) >= 37 ? 65
: ({{Grand Total Score}} || 0) >= 35 ? 63
: ({{Grand Total Score}} || 0) >= 33 ? 61
: ({{Grand Total Score}} || 0) >= 30 ? 57
: ({{Grand Total Score}} || 0) >= 28 ? 55
: ({{Grand Total Score}} || 0) >= 25 ? 51
: ({{Grand Total Score}} || 0) >= 22 ? 47
: ({{Grand Total Score}} || 0) >= 19 ? 42
: ({{Grand Total Score}} || 0) >= 16 ? 38
: ({{Grand Total Score}} || 0) >= 13 ? 33
: ({{Grand Total Score}} || 0) >= 10 ? 26
: ({{Grand Total Score}} || 0) >= 8 ? 17
: ({{Grand Total Score}} || 0) >= 6 ? 5
: ({{Grand Total Score}} || 0) >= 3 ? 1
: 0
```

Note: Clayscript is JavaScript. Column references use `{{Column Name}}` syntax.
Guard against null with `|| 0`. Check values in descending order so the first
match wins. Set the column data type to "Number" for sorting/filtering.

**Recalibration.** The GT → Display lookup must be recomputed whenever the DQ
criteria, card bands, or card weights change materially. The mapping is derived
from the current pool's distribution: a structural change to the rubric shifts
the distribution and invalidates the lookup. Recalibration process:
1. Export the non-DQ pool's Grand Total column
2. Run the inverse-normal CDF transform (script in `references/simulate_scoring.py`)
3. Average Display Score per GT value to produce the new lookup table
4. Update the Clay IF formula

**HubSpot sync.** The Display Score is the value that syncs to HubSpot for reps.
Label it unambiguously (e.g., "Acme Fit Score") so it's not confused with the
raw Grand Total. The raw Grand Total and per-card scores stay in Clay for debugging.

**Tier column (Clayscript, type: Text).** Simple 5% score bands on the bell
curve Display Score. The bell curve already spreads companies across 0-1, so
even score bands produce a natural bell-shaped tier distribution: more
companies in the middle tiers (T10/T11), fewer at the extremes (T01/T20).
No recalibration needed when the pool changes: the bands are fixed.

```javascript
// 20 tiers, 5% score bands. Input: bell curve Display Score (0-1).
({{Score Mapping}} || 0) >= 0.95 ? "T01 (95-100%)"
: ({{Score Mapping}} || 0) >= 0.90 ? "T02 (90-95%)"
: ({{Score Mapping}} || 0) >= 0.85 ? "T03 (85-90%)"
: ({{Score Mapping}} || 0) >= 0.80 ? "T04 (80-85%)"
: ({{Score Mapping}} || 0) >= 0.75 ? "T05 (75-80%)"
: ({{Score Mapping}} || 0) >= 0.70 ? "T06 (70-74%)"
: ({{Score Mapping}} || 0) >= 0.65 ? "T07 (65-69%)"
: ({{Score Mapping}} || 0) >= 0.60 ? "T08 (60-64%)"
: ({{Score Mapping}} || 0) >= 0.55 ? "T09 (55-59%)"
: ({{Score Mapping}} || 0) >= 0.50 ? "T10 (50-54%)"
: ({{Score Mapping}} || 0) >= 0.45 ? "T11 (45-49%)"
: ({{Score Mapping}} || 0) >= 0.40 ? "T12 (40-44%)"
: ({{Score Mapping}} || 0) >= 0.35 ? "T13 (35-39%)"
: ({{Score Mapping}} || 0) >= 0.30 ? "T14 (30-34%)"
: ({{Score Mapping}} || 0) >= 0.25 ? "T15 (25-29%)"
: ({{Score Mapping}} || 0) >= 0.20 ? "T16 (20-24%)"
: ({{Score Mapping}} || 0) >= 0.15 ? "T17 (15-19%)"
: ({{Score Mapping}} || 0) >= 0.10 ? "T18 (10-14%)"
: ({{Score Mapping}} || 0) >= 0.05 ? "T19 (5-9%)"
: "T20 (0-4%)"
```

Column name may vary by client (`Score Mapping`, `Display Score`, etc.) , 
replace `{{Score Mapping}}` with the client's actual bell curve column name.

**Expected output.** Mean ~50, Median ~50, Stdev ~20. Tier distribution:
A (2%), B (8%), C (18%), D (22%), Low (50%). The slight left skew in the Low
tier is structural: DQ catches the worst misfits, but the bottom of the
surviving pool still has more sparse-data rows than the top has data-rich ones.

**Worked example (Client B).** A raw rubric (11 cards, maxes sum to 100) produced stdev 14.6 with scores in a 3-93 range. After bell curve normalization: stdev 20.2, mean 49, median 50, P5=16, P95=82. The top account went from raw 93 to Display 99, the median from raw 24 to Display 50, and the bottom from raw 3 to Display 1.

**Trade-off.** The Display Score is a relative rank, not an absolute measure.
"Display 75" means "better than 75% of the qualified pool," not "hit 75% of
the rubric criteria." This is a feature when the audience is reps who need to
prioritize: they care about relative ordering, not rubric semantics. It's a
limitation when the audience is the scoring model builder who needs to debug
which card is underperforming: use the raw Grand Total and per-card scores
for that.

---

## 6. Negative signals / explicit DQ axes

**What it does.** Pulls the bottom further down, stretching visible range upward
and surfacing misfit firms separately from low-data firms.

**When to apply.** Whenever the list has identifiable wrong-fit categories that
currently score the same as low-data correct-fit firms.

### Starter negative axes for a service-firm TAM

| Signal | Penalty |
|---|---:|
| Practice or service description matches an out-of-scope category | −3 |
| No website / dead domain | −2 |
| Below minimum size AND no activity signal | −2 |
| Defunct or merged (cross-reference a public list) | −5 (or hard DQ) |
| Solo operator indicators (FTE = 1) AND no domain signal | −1 |

### Starter negative axes for an in-house buyer

| Signal | Penalty |
|---|---:|
| Industry in {retail, hospitality, food service, professional services non-tech} | −2 |
| < 50 FTE AND 0 public filings | −2 |
| No website / dead domain | −2 |

### Hard DQ vs soft penalty

- **Hard DQ** when the row should not appear in the output at all (sanctioned country, dissolved entity, an out-of-scope firm type). Removes from list.
- **Soft penalty** when the row could conceivably belong but the signal suggests it's a poor fit. Reduces score, doesn't remove.

Default to soft penalty unless client has explicit "do not contact" criteria.

---

## How these stack

Order of application matters. The recommended composition:

```
1. Hard DQ filter (drop rows)
2. For each remaining row:
   raw_universal = sum(universal_axis_pts)
   raw_segment   = sum(segment_specific_axis_pts)  # service-firm OR corporate
   raw_negative  = sum(negative_signal_penalties)  # typically ≤ 0

   raw_total = max(0, raw_universal + raw_segment + raw_negative)

3. Apply log transforms inside the per-axis scorers (step into step 2)

4. multiplied = raw_total × Domain_Fit_Multiplier × Activity_Multiplier
5. confidence_adjusted = multiplied × completeness_multiplier
6. pct = confidence_adjusted / segment_denominator
7. (optional) blended = 0.5 * pct + 0.5 * percentile_within_segment(pct)
8. (optional) bell_curve = inverse_normal_cdf(percentile_rank) * 20 + 50
   → use when raw stdev plateaus and reps need 0-100 display scores
   → implement in Clay as GT → Display Score lookup (nested IF formula)
   → see §5a for full formula, Clay template, and recalibration process
```

Apply only what the data supports. If the segments are clean (single entity type),
skip type-aware (step 2 segment-split). If data completeness is uniformly high,
skip multiplier (step 5). Don't apply every technique on every engagement: pick
the 2-3 that address the specific distribution problems found in Phase 1.

---

## Decision matrix: which technique fixes which symptom

| Symptom from Phase 1 profile | Apply |
|---|---|
| Median in 10-25%, top tail thin (< 1% above 60%) | Log transforms + multiplicative gate |
| Top 10 too close to top 100 | Multiplicative fit gate |
| Same score on rows with vastly different enrichment depth | Completeness multiplier |
| Two populations (service firms + corporates) compressed together | Type-aware scoring |
| Headline distribution looks bad to non-technical reviewer | Percentile blend |
| Raw stdev plateaued at 10-18 due to low coverage on heavy axes; reps need 0-100 | Bell curve normalization (§5a) |
| Misfit rows scoring same as low-data correct-fit rows | Negative signals / soft DQ |
| Default-when-null in a derived column | Phase 1.1: fix the bug first, don't paper over with technique |
| Normalization cap < 1.0 | Phase 1.1: fix the denominator first |

Bug fixes (Phase 1.1) always come before distribution techniques. A technique
applied on top of a bug just hides the bug.
