"""
Phase 3a: Bell curve normalization template.

Drop-in starter for the bell curve transform documented in SKILL.md Phase 3a.
Loads `scored_v[N].csv` (from simulate_scoring.py), computes percentile rank
per non-DQ row, maps to a normal distribution (mean=50, stdev=20), and emits:

  - display_score_lookup.txt: paste-ready Clayscript IF formula for the
    Display Score column in Clay
  - scored_v[N]_with_display.csv: per-row CSV with Display Score appended

What you adapt per client (the CONFIGURE block):
  - SCORED_CSV: path to the simulate_scoring output
  - GT_COLUMN: name of the Grand Total column in that CSV (e.g. 'v11_gt')
  - DQ_COLUMN: name of the DQ flag column (e.g. 'v11_dq')

Usage:
  python3 bell_curve.py

Validation:
  - Display Score stdev should hit ≥ 20 (the 0.20 target on a 0-100 scale)
  - Display Score mean should be ~50
  - Histogram should look bell-shaped (modest piles at 0 and 100 are OK  - 
    those are the very top and bottom percentiles clamped)

Recalibration trigger:
  Recompute whenever DQ criteria, card bands, or card weights change.
  Quarterly sanity recalibration even if no structural changes: new
  enrichment data may have shifted the GT distribution.
"""
import csv, math, os, statistics, sys
from collections import Counter, defaultdict

csv.field_size_limit(sys.maxsize)


# ============================================================
# CONFIGURE PER CLIENT
# ============================================================
HERE = os.path.dirname(os.path.abspath(__file__))
SCORED_CSV = os.path.join(HERE, 'scored_v[N].csv')   # adapt per client
GT_COLUMN = 'v[N]_gt'                                  # adapt per client
DQ_COLUMN = 'v[N]_dq'                                  # adapt per client
VERSION = 'N'                                          # adapt per client

# DISPLAY_SCALE: 100 → Display Score on 0-100 scale (mean=50, stdev=20)
#                  1 → Display Score on 0-1 scale  (mean=0.50, stdev=0.20)
# Use 1 if Display Score is going into a Clay column with type=Percentage,
# or if you want it to match Final Score Percentage convention.
# Use 100 if Display Score is going into a Clay column with type=Number
# and you want literal 0-100 values shown.
DISPLAY_SCALE = 1


# ============================================================
# INVERSE NORMAL CDF (Beasley-Springer-Moro approximation)
# IMPORTANT: This is the CORRECT implementation. A previous version had an
# operator-precedence bug where `c[5] / denominator` was parsed as a separate
# term, causing the tail branches to return garbage for percentiles outside
# [0.025, 0.975]. That bug made the top/bottom ~2.5% of rows saturate at
# Display = 100 or 0. Numerators are now wrapped in outer parens.
# ============================================================
def inv_norm_cdf(p):
    """Inverse normal CDF. Returns z such that Phi(z) = p."""
    if p <= 0 or p >= 1:
        return -8 if p <= 0 else 8
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow = 0.02425
    phigh = 1 - plow
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        num = (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5])
        den = ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
        return num / den
    if p <= phigh:
        q = p - 0.5
        r = q * q
        num = ((((((a[0]*r + a[1])*r + a[2])*r + a[3])*r + a[4])*r + a[5]) * q)
        den = (((((b[0]*r + b[1])*r + b[2])*r + b[3])*r + b[4])*r + 1)
        return num / den
    q = math.sqrt(-2 * math.log(1 - p))
    num = (((((c[0]*q + c[1])*q + c[2])*q + c[3])*q + c[4])*q + c[5])
    den = ((((d[0]*q + d[1])*q + d[2])*q + d[3])*q + 1)
    return -num / den


def main():
    # 1. Load non-DQ Grand Total values
    gts = []
    with open(SCORED_CSV) as f:
        r = csv.DictReader(f)
        for row in r:
            if (row.get(DQ_COLUMN) or '').lower() in ('true', '1'):
                continue
            try:
                gts.append(float(row.get(GT_COLUMN)))
            except (TypeError, ValueError):
                continue
    n = len(gts)
    print(f"Loaded {n} non-DQ rows from {SCORED_CSV}", file=sys.stderr)
    print(f"Raw GT: mean={statistics.mean(gts):.2f} stdev={statistics.stdev(gts):.2f} "
          f"min={min(gts):.1f} max={max(gts):.1f}")

    # 2. Compute midrank per unique GT (handles ties)
    gt_counts = Counter(gts)
    gt_avg_rank = {}
    cum = 0
    for g in sorted(gt_counts):
        c = gt_counts[g]
        gt_avg_rank[g] = (cum + c / 2) / n
        cum += c

    # 3. Map each unique GT → Display via inv_norm_cdf
    #    On 0-100 scale: mean=50, stdev=20
    #    On 0-1   scale: mean=0.50, stdev=0.20
    mean = 0.50 * DISPLAY_SCALE
    stdev = 0.20 * DISPLAY_SCALE
    cap = 1.0 * DISPLAY_SCALE
    digits = 3 if DISPLAY_SCALE == 1 else 1
    gt_to_display = {}
    for g, r in gt_avg_rank.items():
        eps = 0.5 / n
        rc = min(1 - eps, max(eps, r))
        z = inv_norm_cdf(rc)
        display = max(0, min(cap, mean + stdev * z))
        gt_to_display[g] = round(display, digits)

    # 4. Validation: sanity check (thresholds adapt to DISPLAY_SCALE)
    display_per_row = [gt_to_display[g] for g in gts]
    d_mean = statistics.mean(display_per_row)
    d_stdev = statistics.stdev(display_per_row)
    near_max = 0.995 * DISPLAY_SCALE
    near_min = 0.005 * DISPLAY_SCALE
    d_max_count = sum(1 for x in display_per_row if x >= near_max)
    d_min_count = sum(1 for x in display_per_row if x <= near_min)
    print(f"\nDisplay Score (scale 0-{DISPLAY_SCALE}): mean={d_mean:.3f} stdev={d_stdev:.3f}")
    print(f"  rows at Display ≥ {near_max}: {d_max_count} ({100*d_max_count/n:.2f}%)")
    print(f"  rows at Display ≤ {near_min}: {d_min_count} ({100*d_min_count/n:.2f}%)")
    print()

    # SANITY GATES (per SKILL.md Phase 3a):
    expected_mean = 0.50 * DISPLAY_SCALE
    expected_stdev_floor = 0.18 * DISPLAY_SCALE
    if 100 * d_max_count / n > 3:
        print(f"WARNING: {100*d_max_count/n:.1f}% of rows at Display = max. "
              f"Suspect inv_norm_cdf precedence bug. Check the function.",
              file=sys.stderr)
    if abs(d_mean - expected_mean) > 0.02 * DISPLAY_SCALE:
        print(f"WARNING: Display mean = {d_mean:.3f}, expected ~{expected_mean}.",
              file=sys.stderr)
    if d_stdev < expected_stdev_floor:
        print(f"WARNING: Display stdev = {d_stdev:.3f}, target ≥ {0.20 * DISPLAY_SCALE}.",
              file=sys.stderr)

    # Histogram
    bh = Counter()
    for x in display_per_row:
        bh[round(x / 5) * 5] += 1
    scale = max(1, max(bh.values()) // 50) if bh else 1
    print('Display Score histogram (5-pt bins):')
    for k in sorted(bh):
        bar = '#' * (bh[k] // scale)
        print(f'  {k:>3}: {bh[k]:>6} {bar}')

    # 5. Write display_score_lookup.txt
    lookup_lines = [
        f'# Display Score Lookup: v{VERSION} (scale 0-{DISPLAY_SCALE})',
        '',
        f'Display Score output range: 0 to {DISPLAY_SCALE}.  '
        f'Mean ≈ {0.50 * DISPLAY_SCALE}, stdev ≈ {0.20 * DISPLAY_SCALE}.',
        '',
        '## Mapping table (Grand Total → Display Score)',
        '',
        '| Grand Total | Display Score | Row count |',
        '|---:|---:|---:|',
    ]
    d_fmt = '.3f' if DISPLAY_SCALE == 1 else '.1f'
    for g in sorted(gt_to_display):
        if gt_counts[g] >= 5:
            lookup_lines.append(f'| {g:.1f} | {gt_to_display[g]:{d_fmt}} | {gt_counts[g]} |')
    lookup_lines.append('')
    lookup_lines.append('## Paste-ready Clayscript formula for `Display Score` column')
    lookup_lines.append('Type: Number formula column.')
    lookup_lines.append('')
    lookup_lines.append('```')

    # Build nested IF chain: round GTs to nearest 0.5 to consolidate
    grouped = defaultdict(list)
    for g, d in gt_to_display.items():
        key = round(g * 2) / 2
        grouped[key].append(d)
    gt_to_display_rounded = {k: round(sum(vs)/len(vs), digits) for k, vs in grouped.items()}
    sorted_keys = sorted(gt_to_display_rounded.keys())
    expr = str(gt_to_display_rounded[sorted_keys[-1]])
    for k in reversed(sorted_keys[:-1]):
        d = gt_to_display_rounded[k]
        expr = f'(({{{{Grand Total Score}}}} || 0) <= {k} ? {d} : {expr})'
    lookup_lines.append(expr)
    lookup_lines.append('```')
    lookup_lines.append('')
    lookup_lines.append('## Paste-ready Tier Grade formula (T1 = top, T20 = bottom)')
    lookup_lines.append('Type: Text formula column.')
    lookup_lines.append('')
    lookup_lines.append('```')
    if DISPLAY_SCALE == 1:
        lookup_lines.append('"T" + (20 - Math.floor(Math.min(0.99, ({{Display Score}} || 0)) / 0.05))')
    else:
        lookup_lines.append('"T" + (20 - Math.floor(Math.min(99, ({{Display Score}} || 0)) / 5))')
    lookup_lines.append('```')
    lookup_lines.append('')
    lookup_lines.append(f'Produces T1 (Display {0.95 * DISPLAY_SCALE}-{DISPLAY_SCALE}, best) '
                        f'through T20 (Display 0-{0.05 * DISPLAY_SCALE}, worst).')
    lookup_lines.append('')
    lookup_lines.append('Convention: T1 = top tier (best fit), T20 = bottom tier (worst fit).')
    lookup_lines.append('If you prefer T20 = top, change `(20 - Math.floor(...))` to `(Math.floor(...) + 1)`.')
    lookup_lines.append('')
    lookup_lines.append('## Recalibration trigger')
    lookup_lines.append('')
    lookup_lines.append('Recompute the lookup whenever:')
    lookup_lines.append('- DQ criteria change (Hard DQ logic, wrong-fit industry list)')
    lookup_lines.append('- Card bands change (Keywords or Scores on any card)')
    lookup_lines.append('- Card weights change (per-card max values)')
    lookup_lines.append('- A scoring card is added or removed')
    lookup_lines.append('')
    lookup_lines.append('Quarterly sanity recalibration even without structural changes,')
    lookup_lines.append('in case new enrichment data has shifted the GT distribution.')
    lookup_lines.append('')
    lookup_lines.append('## Validation')
    lookup_lines.append('')
    lookup_lines.append(f'Raw GT stdev (non-DQ pool, n={n}): {statistics.stdev(gts):.3f}')
    lookup_lines.append(f'Display Score stdev: {d_stdev:.3f}  ← target ≥ 20')
    lookup_lines.append(f'Display Score mean: {d_mean:.2f}  ← target ≈ 50')
    lookup_lines.append(f'Rows at Display = 100 (true top tail): {d_max_count} ({100*d_max_count/n:.2f}%)')

    out_path = os.path.join(HERE, 'display_score_lookup.txt')
    with open(out_path, 'w') as f:
        f.write('\n'.join(lookup_lines))
    print(f'\nWrote {out_path}')

    # 6. Write per-row CSV with Display Score column appended
    out_csv = os.path.join(HERE, f'scored_v{VERSION}_with_display.csv')
    with open(SCORED_CSV) as f_in, open(out_csv, 'w', newline='') as f_out:
        r = csv.reader(f_in)
        w = csv.writer(f_out)
        header = next(r)
        w.writerow(header + [f'v{VERSION}_display_score'])
        gt_idx = header.index(GT_COLUMN)
        for row in r:
            try:
                d = gt_to_display.get(float(row[gt_idx]), '')
            except (ValueError, IndexError):
                d = ''
            w.writerow(row + [d])
    print(f'Wrote {out_csv}')


if __name__ == '__main__':
    main()
