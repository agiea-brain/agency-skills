"""
Scoring simulation harness: drop-in starter for any client engagement.

DEFAULT ARCHITECTURE: pure-positive + smart Hard DQ.
This is the recommended default per SKILL.md. All cards bottom out at 0,
soft-fit categories score low-positive (0-2), Hard DQ filters objectively
wrong-fit firms before scoring runs. No Fit_Multiplier, no Completeness_Multiplier,
no Negative_Penalty column.

If you need to switch architectures (e.g. client uses a non-Clay tool where DQ
doesn't stop enrichment, OR they want maximum stdev with multiplier columns),
toggle ARCHITECTURE below and uncomment the relevant scorer overrides.

What it does:
  1. Loads a CSV of accounts + existing per-criterion scores
  2. Computes a baseline (the client's current model) and a revised model
  3. Reports side-by-side: stdev, histogram, percentiles, largest pile-up bucket,
     A/B/C/D/F tier counts, and TWIN-FIRM SPREAD per axis
  4. Validates against the 6 gates from SKILL.md (architecture-appropriate stdev,
     bucket concentration ≤5%, twin-firm spread on top 3 axes, DQ-threshold valley,
     top-K named-firms recognition, histogram shape)

What you adapt per client (the CONFIGURE block):
  - ARCHITECTURE: 'pure-positive' (default) | 'pure-card-with-negatives' | 'with-multipliers'
  - SRC: path to the source CSV
  - NAME_COLUMN / CURRENT_FINAL_PCT_COLUMN: column names in the source
  - WEIGHTS: per-axis weight in Final % (sum should be 100)
  - DQ_THRESHOLD_PCT: where the client wants the DQ cutoff (e.g. 0.40)
  - hard_dq(row): returns (bool, reason): expanded list for pure-positive
  - score_*(row) functions: per-axis raw score → returns (score, max)
  - TWIN_FIRM_TEMPLATE_NAME: a real top-15 firm to clone for twin-firm tests
  - TWIN_FIRM_AXES: list of (axis_name, column, [test values]) tuples

Usage:
  python3 simulate_scoring.py path/to/source.csv

Outputs:
  scored_v[N].csv   per-row scores + breakdown columns
  summary_v[N].txt  the headline report (paste into RECOMMENDATIONS.md)
"""
import csv
import math
import os
import statistics
import sys
from collections import Counter

csv.field_size_limit(sys.maxsize)


# ============================================================
# CONFIGURE PER CLIENT: everything below this line is the contract
# ============================================================

# Architecture decision (Phase 0: set BEFORE anything else)
# Options:
#   'pure-positive'          : RECOMMENDED default. All scores ≥ 0. Expanded Hard DQ.
#                                Stdev target: ≥ 0.20. Used when DQ stops enrichment.
#   'pure-card-with-negatives' -  Negative bands within cards. No multipliers.
#                                Stdev target: ≥ 0.27. Used when DQ doesn't stop enrichment.
#   'with-multipliers'       : Fit_Multiplier + Negative_Penalty column + Completeness_Multiplier.
#                                Stdev target: ≥ 0.35. Used when client wants max spread.
ARCHITECTURE = 'pure-positive'

VERSION = 10
SRC = sys.argv[1] if len(sys.argv) > 1 else '/path/to/source.csv'
OUT_DIR = os.path.dirname(os.path.abspath(SRC)) or '.'
OUT_CSV = os.path.join(OUT_DIR, f'scored_v{VERSION}.csv')
OUT_TXT = os.path.join(OUT_DIR, f'summary_v{VERSION}.txt')

NAME_COLUMN = 'Name vF'
CURRENT_FINAL_PCT_COLUMN = 'Final Score Percentage'  # set None if absent
DQ_THRESHOLD_PCT = 0.40

# Per-axis weights in the Final % (must sum to 100)
# These weights are appropriate starting points for a PE-backed
# mid-market ICP. Adjust per client but preserve the principle:
# top 3 axes get ~50% of weight, mid-tier ~35%, tie-breakers ~15%.
WEIGHTS = {
    'industry':   22,    # primary fit signal
    'reps':       18,    # field-sales sweet spot
    'pe':         14,    # ownership signal (intra-card tie-breaker)
    'product':    12,    # motion proxy
    'employees':  12,    # 100% coverage = stable anchor
    'revenue':    12,    # scale signal (independent of /rep)
    'tech':        6,    # CRM maturity
    'maturity':    2,    # founded-year tie-breaker
    'country':     2,    # geo already filtered
}

# Tier cutoffs on raw Final pts.
# Pure-positive: 'Low' replaces 'F' since scores can't go negative.
# Pure-card-with-negatives: 'F' is rows that scored below 0 (visible misfit pile).
if ARCHITECTURE == 'pure-positive':
    TIER_CUTOFFS = {'A': 75, 'B': 55, 'C': 35, 'D': 15}  # below 15 = 'Low'
else:
    TIER_CUTOFFS = {'A': 75, 'B': 55, 'C': 35, 'D': 0}   # below 0 = 'F'


# ============================================================
# PER-AXIS SCORERS: each returns (raw_score, max_score)
# ============================================================

def tf(v):
    try: return float(v)
    except: return None
def ti(v):
    try: return int(float(v))
    except: return None
def s(v):
    return (v or '').strip()


def score_industry(row):
    """Industry → tier lookup. Pure-positive default (all values ≥ 0).

    Wide tier gaps (Tier 1 = 22, Tier 2 = 16, Tier 3 = 8) do the discrimination
    work that negative bands would do, while staying positive.

    For pure-card-with-negatives architecture: replace 0s with -5 to -25 for misfits.
    """
    bands = {
        # Example values. Replace with the client's industries.
        # Tier 1: true bullseye (max 22)
        'Bullseye Industry A': 22, 'Bullseye Industry B': 22,
        # Tier 2: strong fit (~16)
        'Strong Industry A': 16, 'Strong Industry B': 14,
        # Tier 3: good fit (~8-9)
        'Good Industry A': 9, 'Good Industry B': 8,
        # Tier 4: weaker fit (~3)
        'Weak Industry': 3,
        # Tier 5: soft fit, kept in pool with low score (~1-2)
        'Soft Industry': 2, 'Other': 1,
    }
    ind = s(row.get('AI Industry vF')) or s(row.get('AI Industry v3'))
    return bands.get(ind, 1), 22


def score_employees(row):
    """Employee count → score. Pure-positive (peak 400-799 FTE)."""
    fte = ti(row.get('FTEs vF'))
    if fte is None or fte < 50: return 0, 12
    if fte < 100:   return 2, 12
    if fte < 200:   return 5, 12
    if fte < 400:   return 8, 12
    if fte < 800:   return 12, 12   # peak
    if fte < 1500:  return 9, 12
    if fte < 3000:  return 4, 12
    if fte < 7500:  return 1, 12
    return 0, 12


def score_reps(row):
    """Field rep count → score. Pure-positive (peak 60-89 reps)."""
    raw = ti(row.get('Sales Reps')) or ti(row.get('Field Rep Count'))
    if raw is None or raw < 10: return 0, 18
    if raw < 20:    return 1, 18
    if raw < 30:    return 4, 18
    if raw < 50:    return 11, 18
    if raw < 60:    return 16, 18
    if raw < 90:    return 18, 18   # peak
    if raw < 120:   return 16, 18
    if raw < 150:   return 12, 18
    if raw < 200:   return 6, 18
    if raw < 300:   return 2, 18
    if raw < 500:   return 1, 18
    return 0, 18


def score_revenue(row):
    """Revenue → score. Log-shaped, pure-positive."""
    rev = tf(row.get('Revenue vF'))
    if rev is None or rev <= 0: return 0, 12
    if rev < 5e6:      return 0, 12
    if rev < 25e6:     return 2, 12
    if rev < 100e6:    return 5, 12
    if rev < 250e6:    return 8, 12
    if rev < 500e6:    return 10, 12
    if rev < 1e9:      return 11, 12
    if rev < 5e9:      return 12, 12   # peak
    if rev < 25e9:     return 6, 12
    return 0, 12


# Add the rest of the axes per your rubric (score_pe, score_product, score_tech, etc.).
# Each must return (raw, max). Keep them pure-positive.


# ============================================================
# HARD DQ: pure-positive architecture expects expanded DQ list
# Move objectively wrong-fit categories here so enrichment credits aren't spent
# on rows that can never become customers.
# ============================================================

HARD_DQ_INDUSTRY_PATTERNS = (
    'software development', 'saas', 'computer software',
    'information technology and services',
    'financial services', 'banking', 'insurance', 'investment management',
    'restaurants', 'real estate', 'higher education',
)

def hard_dq(row):
    """Return (is_dq, reason). Expanded for pure-positive architecture."""
    if s(row.get('DQ2')).lower() == 'true': return True, 'dq2'
    if s(row.get('Quick DQ')).lower() == 'true': return True, 'quick_dq'
    fte = ti(row.get('FTEs vF')) or 0
    if fte < 50: return True, 'ftes<50'
    if fte > 10000: return True, 'mega_corp(>10K FTE)'  # Fortune 100
    # Expanded: objective wrong-fit industries (pure-positive only)
    if ARCHITECTURE == 'pure-positive':
        ni = s(row.get('Normal Industry vF')).lower()
        if any(p in ni for p in HARD_DQ_INDUSTRY_PATTERNS):
            return True, f'industry({ni[:30]})'
    return False, ''


# ============================================================
# CROSS-AXIS HELPERS (only used in with-multipliers architecture)
# In pure-positive and pure-card-with-negatives: these are NOT called.
# ============================================================

def negative_penalty(row):
    """Cross-axis penalty column. Only used in 'with-multipliers' architecture."""
    pen = 0
    if s(row.get('AI Industry v3')) == 'Other': pen -= 20
    pt = s(row.get('Product Type vF')).lower()
    if pt == 'software':           pen -= 40
    elif pt in ('service', 'services'): pen -= 12
    return pen


def fit_multiplier(industry_g, pe_g, product_g):
    """Range 0.4-1.8. Compounds top-tier fit. with-multipliers only."""
    adv = industry_g * 0.5 + pe_g * 0.25 + product_g * 0.25
    return 0.4 + 1.4 * adv


COMPLETENESS_FIELDS = ['FTEs vF', 'Sales Reps', 'Revenue vF', 'PE Backers',
                       'Technologies Text', 'Product Count vF', 'Founded Year vF']
def completeness_multiplier(row):
    """0.70-1.00. with-multipliers only."""
    populated = sum(1 for c in COMPLETENESS_FIELDS if s(row.get(c)))
    return 0.7 + 0.3 * (populated / len(COMPLETENESS_FIELDS))


# ============================================================
# TWIN-FIRM TEST CONFIG
# ============================================================

TWIN_FIRM_TEMPLATE_NAME = 'Example Co'  # a real top-15 account in your dataset
TWIN_FIRM_AXES = [
    ('Revenue', 'Revenue vF', [1e6, 1e7, 5e7, 1e8, 2.5e8, 5e8, 1e9, 5e9, 2.5e10]),
    ('FTEs',    'FTEs vF',    [50, 100, 200, 400, 800, 1500, 3000, 7500]),
    ('Sales Reps', 'Sales Reps', [10, 20, 30, 50, 100, 150, 250, 500]),
]


# ============================================================
# CORE SCORING
# ============================================================

def score_row(row):
    """Score one row. Dispatches on ARCHITECTURE.

    pure-positive:           Grand Total = sum of card raw scores. Always ≥ 0.
    pure-card-with-negatives: Grand Total = sum of card raw scores. Can be < 0.
    with-multipliers:        Grand Total = (weighted sum × Fit_Mult × Compl_Mult) + Penalty.
    """
    dq, reason = hard_dq(row)
    if dq:
        return {'dq': True, 'dq_reason': reason, 'final_pts': 0, 'final_pct': 0, 'tier': 'DQ'}

    raw = {}
    for axis, fn in [
        ('industry', score_industry),
        ('employees', score_employees),
        ('reps', score_reps),
        ('revenue', score_revenue),
        # add the rest per your rubric
    ]:
        r, m = fn(row)
        raw[axis] = r

    # In pure-positive / pure-card-with-negatives, card max = weight (the
    # scaling lives in the band values themselves). Grand Total is a pure sum.
    if ARCHITECTURE in ('pure-positive', 'pure-card-with-negatives'):
        final_pts = sum(raw.values())
        if ARCHITECTURE == 'pure-positive':
            final_pts = max(0, final_pts)  # safety floor; shouldn't trigger
        final_pct = max(-0.5, min(1.0, final_pts / 100))
        fmult = cmult = 1.0
        pen = 0

    # In with-multipliers, the card emits 0-1 Golden (or raw/max), then we
    # apply weights + Fit_Multiplier + Completeness_Multiplier + Negative_Penalty.
    else:  # 'with-multipliers'
        golden = {axis: r / WEIGHTS.get(axis, 1) for axis, r in raw.items()}
        weighted = sum(golden.get(a, 0) * WEIGHTS.get(a, 0) for a in WEIGHTS)
        fmult = fit_multiplier(golden.get('industry', 0),
                               golden.get('pe', 0),
                               golden.get('product', 0))
        cmult = completeness_multiplier(row)
        pen = negative_penalty(row)
        final_pts = weighted * fmult * cmult + pen
        final_pct = max(-0.5, min(1.0, final_pts / 100))

    # Tier assignment
    tier = 'Low' if ARCHITECTURE == 'pure-positive' else 'F'
    for t, cut in TIER_CUTOFFS.items():
        if final_pts >= cut:
            tier = t
            break

    return {'dq': False, 'dq_reason': '',
            'final_pts': round(final_pts, 2), 'final_pct': round(final_pct, 4),
            'tier': tier, 'fit_mult': round(fmult, 3), 'compl_mult': round(cmult, 3),
            'arch': ARCHITECTURE,
            **{f'raw_{k}': round(v, 2) for k, v in raw.items()}}


# ============================================================
# REPORT GENERATION
# ============================================================

def report(scored, original_pcts):
    lines = []
    def p(*a): lines.append(' '.join(str(x) for x in a))

    real = [(r, sc) for r, sc in scored if not sc['dq']]
    pcts = [sc['final_pct'] for r, sc in real]
    pts = [sc['final_pts'] for r, sc in real]
    n = len(scored)

    p(f"Total rows: {n}  |  After DQ: {len(real)}  |  Version: v{VERSION}")
    p('')

    # Side-by-side stats
    p('=== Headline distribution: original vs v{} ==='.format(VERSION))
    p(f"{'Metric':28s} {'Original':>12s} {'v' + str(VERSION):>12s} {'Δ':>10s}")
    if original_pcts:
        for label, fn in [('stdev', statistics.stdev), ('mean', statistics.mean),
                          ('median', statistics.median), ('P25', lambda v: sorted(v)[int(len(v)*0.25)]),
                          ('P75', lambda v: sorted(v)[int(len(v)*0.75)]),
                          ('P95', lambda v: sorted(v)[int(len(v)*0.95)])]:
            o = fn(original_pcts); n_v = fn(pcts)
            p(f"{label:28s} {o:>12.4f} {n_v:>12.4f} {n_v - o:>+10.4f}")

    # Concentration check
    ctr_new = Counter(round(x, 2) for x in pcts)
    top_new = ctr_new.most_common(1)[0]
    if original_pcts:
        ctr_old = Counter(round(x, 2) for x in original_pcts)
        top_old = ctr_old.most_common(1)[0]
        p(f"{'Largest 0.01-bucket':28s} {100*top_old[1]/len(original_pcts):>11.2f}% {100*top_new[1]/len(pcts):>11.2f}%")
    p('')

    # Tier counts
    tier_ctr = Counter(sc['tier'] for r, sc in scored)
    p('Tier distribution:')
    for t in ['A', 'B', 'C', 'D', 'F', 'DQ']:
        c = tier_ctr.get(t, 0)
        p(f"  {t}: {c} ({100*c/n:.1f}%)")
    p('')

    # Histogram
    p('Histogram v{} (5-pt bins, after DQ):'.format(VERSION))
    bh = Counter()
    for x in pts:
        bh[round(x / 5) * 5] += 1
    scale = max(1, max(bh.values()) // 50) if bh else 1
    for k in sorted(bh):
        bar = '#' * (bh[k] // scale)
        p(f"  {k:>6.0f}: {bh[k]:>6} {bar}")
    p('')

    # DQ-threshold validation
    threshold_pts = DQ_THRESHOLD_PCT * 100
    below = sum(1 for x in pts if x < threshold_pts)
    above = sum(1 for x in pts if x >= threshold_pts)
    valley_window = sum(1 for x in pts if threshold_pts - 5 <= x <= threshold_pts + 5)
    p(f'=== DQ-threshold check ({DQ_THRESHOLD_PCT:.0%} = {threshold_pts:.0f} pts) ===')
    p(f"  Below threshold: {below} ({100*below/len(pts):.1f}%)")
    p(f"  Above threshold: {above} ({100*above/len(pts):.1f}%)")
    p(f"  In ±5 pt valley: {valley_window} ({100*valley_window/len(pts):.1f}%) : lower is better, ≤5% is good")
    p('')

    return lines


def twin_firm_test(rows):
    """Find the template firm, clone with varied axis values, score, report spread."""
    lines = []
    def p(*a): lines.append(' '.join(str(x) for x in a))
    template = None
    for r in rows:
        if s(r.get(NAME_COLUMN)) == TWIN_FIRM_TEMPLATE_NAME:
            template = dict(r)
            break
    if not template:
        p(f'(twin-firm template "{TWIN_FIRM_TEMPLATE_NAME}" not in dataset: skipping test)')
        return lines

    p(f'=== Twin-firm test (template: {TWIN_FIRM_TEMPLATE_NAME}) ===')
    p('Same firm scored with one axis varied. Spread shows visible stack-rank differentiation.')
    p('')
    for axis_name, col, values in TWIN_FIRM_AXES:
        results = []
        for v in values:
            tcopy = dict(template)
            tcopy[col] = str(v)
            sc = score_row(tcopy)
            results.append((v, sc['final_pts']))
        spread = max(r[1] for r in results) - min(r[1] for r in results)
        p(f'  {axis_name} ({col}):  spread = {spread:>5.1f} pts   ' +
          '  '.join(f'{v:>10.0f}→{pts:>6.1f}' for v, pts in results[:5]) + '  ...')
        gate = 'PASS' if spread >= 10 else 'FAIL: bump weight on this axis (if uncorrelated with top axes)'
        p(f'    gate (spread ≥ 10 pts): {gate}')
    p('')
    return lines


# ============================================================
# MAIN
# ============================================================

def main():
    assert sum(WEIGHTS.values()) >= 95 and sum(WEIGHTS.values()) <= 105, \
        f"WEIGHTS sum = {sum(WEIGHTS.values())}: should be ~100"

    print(f"Loading {SRC}...", file=sys.stderr)
    with open(SRC) as f:
        rows = list(csv.DictReader(f))
    print(f"Scoring {len(rows)} rows v{VERSION}...", file=sys.stderr)

    scored = [(r, score_row(r)) for r in rows]
    original_pcts = []
    if CURRENT_FINAL_PCT_COLUMN:
        original_pcts = [tf(r.get(CURRENT_FINAL_PCT_COLUMN))
                         for r, sc in scored if not sc['dq']]
        original_pcts = [x for x in original_pcts if x is not None]

    # Write per-row CSV
    breakdown_cols = ['dq', 'dq_reason', 'final_pts', 'final_pct', 'tier',
                      'fit_mult', 'compl_mult'] + [f'g_{k}' for k in WEIGHTS]
    keep_in = [NAME_COLUMN, 'Domain vF', 'AI Industry vF', 'FTEs vF',
               'Sales Reps', 'Revenue vF', 'PE Backers',
               CURRENT_FINAL_PCT_COLUMN] if CURRENT_FINAL_PCT_COLUMN else \
              [NAME_COLUMN, 'Domain vF', 'AI Industry vF', 'FTEs vF',
               'Sales Reps', 'Revenue vF', 'PE Backers']
    keep_in = [c for c in keep_in if c]
    with open(OUT_CSV, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(keep_in + [f'v{VERSION}_{c}' for c in breakdown_cols])
        for r, sc in scored:
            w.writerow([r.get(c, '') for c in keep_in] +
                       [sc.get(c, '') for c in breakdown_cols])
    print(f"Wrote {OUT_CSV}", file=sys.stderr)

    # Reports
    lines = []
    lines.extend(report(scored, original_pcts))
    lines.extend(twin_firm_test(rows))

    # Top 15
    real = [(r, sc) for r, sc in scored if not sc['dq']]
    rk = sorted(real, key=lambda x: -x[1]['final_pts'])
    lines.append(f'=== Top 15 v{VERSION} ===')
    for r, sc in rk[:15]:
        nm = s(r.get(NAME_COLUMN))[:32]
        ind = s(r.get('AI Industry vF'))[:18]
        lines.append(f"  {sc['final_pts']:>6.1f} {sc['tier']} | {nm:<32} | {ind:<18}")
    lines.append('')
    lines.append('=== Bottom 5 v{} ==='.format(VERSION))
    for r, sc in rk[-5:]:
        nm = s(r.get(NAME_COLUMN))[:32]
        lines.append(f"  {sc['final_pts']:>6.1f} {sc['tier']} | {nm}")

    out = '\n'.join(lines)
    with open(OUT_TXT, 'w') as f:
        f.write(out)
    print(out)
    print(f"\nWrote {OUT_TXT}")


if __name__ == '__main__':
    main()
