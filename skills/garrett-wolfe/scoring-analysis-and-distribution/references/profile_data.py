"""
Profile data coverage and existing score distribution for a TAM CSV.

Usage:
  python3 profile_data.py path/to/source.csv

Configure SIGNAL_COLUMNS and EXISTING_SCORE_COLUMN for the dataset under audit.
Outputs:
  - stdout: per-column coverage + stats + score histogram + bug audit
  - profile_output.txt: same content

The bug audit checks for the four most common derived-score failures
(see SKILL.md Phase 1.1):
  1. Default-when-null : derived nonzero rate >> source coverage rate
  2. Normalization cap : *_Golden / *_Pct max < 1.0
  3. Band gaps         : gaps in keyword-based rubric definitions (manual entry)
  4. Empty enrichment  : column referenced in rubric but 0% populated

Plus a canonical-entity coverage check against CANONICAL_ENTITIES.
"""
import csv
import os
import statistics
import sys
from collections import Counter, defaultdict


# === CONFIGURE PER DATASET ===
SIGNAL_COLUMNS = [
    # ('display name', 'csv column name', type='int'|'float'|'str'|'bool')
    # Example for a service-firm TAM:
    # ('FTE', 'FTEs vF', 'int'),
    # ('Country', 'Country vF', 'str'),
    # ('Specialists', 'Specialist Ct vF', 'int'),
]
EXISTING_SCORE_COLUMN = 'Final Score Percentage'  # set to None if no existing score
EXISTING_GRAND_TOTAL_COLUMN = 'Grand Total Score'  # optional
NAME_COLUMN = 'Name vF'  # for canonical-entity matching

# Pairs of (raw value column, score column) to reverse-engineer rubrics
RUBRIC_PAIRS = [
    # ('FTEs vF', 'FTE Score'),
    # ('Country vF', 'Country Score'),
]

# Audit pairs: (derived_score_column, [source_input_columns])
# Used to detect default-when-null bugs (Phase 1.1 check #1)
DERIVED_SCORE_AUDIT = [
    # Example:
    # ('Domain Experience Golden', ['Domain Expertise Classification', 'Service Count']),
    # ('Activity Golden', ['Activity Count']),
]

# Columns expected to be normalized 0..1. Flags if observed max < cap.
NORMALIZED_COLUMNS = [
    # 'Country Score Golden',
    # 'Global Presence Golden',
    # 'Domain Experience Golden',
]
NORMALIZATION_CAP_THRESHOLD = 0.95  # warn if observed_max < this

# Canonical "any reasonable scoring puts these in the top 50" entities for the
# domain under audit. Used for sourcing-gap detection. Adapt per client.
CANONICAL_ENTITIES = [
    # 'Market Leader A', 'Market Leader B', 'Market Leader C',
]
# ==============================


def to_int(v):
    try: return int(float(v))
    except: return None
def to_float(v):
    try: return float(v)
    except: return None


def profile(rows):
    lines = []
    def p(*a): lines.append(' '.join(str(x) for x in a))

    p(f"Total rows: {len(rows)}")
    p('')

    # Column coverage
    p('=== Column coverage ===')
    p(f"{'Column':40s} {'Non-empty':>10} {'Pct':>6}")
    for r in [{}] + rows[:1]:
        pass
    cols = list(rows[0].keys())
    for c in cols:
        n = sum(1 for r in rows if (r.get(c) or '').strip())
        if n == 0:
            continue
        p(f"{c:40s} {n:>10} {100*n/len(rows):>5.1f}%")
    p('')

    # Signal-column distributions
    if SIGNAL_COLUMNS:
        p('=== Signal-column distributions ===')
        for name, col, typ in SIGNAL_COLUMNS:
            vals = [r.get(col, '') for r in rows]
            present = [v for v in vals if (v or '').strip()]
            p(f"\n{name} (col: {col})")
            p(f"  coverage: {len(present)}/{len(rows)} ({100*len(present)/len(rows):.1f}%)")
            if typ == 'int' or typ == 'float':
                nums = [to_float(v) for v in present]
                nums = [x for x in nums if x is not None]
                nz = [x for x in nums if x > 0]
                if nz:
                    sn = sorted(nz)
                    p(f"  nonzero: {len(nz)} median={statistics.median(nz):.1f} max={max(nz):.0f}")
                    for q in [10, 25, 50, 75, 90, 95, 99]:
                        idx = int(len(sn) * q / 100)
                        p(f"    P{q}: {sn[idx]:.1f}")
            elif typ == 'str':
                top = Counter(v for v in present).most_common(10)
                for v, n in top:
                    p(f"    {v[:40]}: {n}")
            elif typ == 'bool':
                p(f"    {Counter(v.lower() for v in present).most_common()}")
        p('')

    # Existing score distribution
    if EXISTING_SCORE_COLUMN:
        scores = [to_float(r.get(EXISTING_SCORE_COLUMN, '')) for r in rows]
        scores = [x for x in scores if x is not None]
        p(f'=== Existing score distribution ({EXISTING_SCORE_COLUMN}) ===')
        if scores:
            p(f"n={len(scores)} mean={statistics.mean(scores):.3f} median={statistics.median(scores):.3f} stdev={statistics.stdev(scores):.3f}")
            ss = sorted(scores)
            for q in [10, 25, 50, 75, 90, 95, 99]:
                p(f"  P{q}: {ss[int(len(ss)*q/100)]:.3f}")
            p('')
            p('Histogram (0.05 bins):')
            bh = Counter()
            for x in scores:
                bh[round(x / 0.05) * 0.05] += 1
            scale = max(1, max(bh.values()) // 50)
            for k in sorted(bh):
                bar = '#' * (bh[k] // scale)
                p(f"  {k:.2f}: {bh[k]:>6} {bar}")
        p('')

    # Reverse-engineer rubrics from raw value -> score column pairs
    if RUBRIC_PAIRS:
        p('=== Reverse-engineered rubric bins ===')
        for raw_col, score_col in RUBRIC_PAIRS:
            buckets = defaultdict(list)
            for r in rows:
                rv = to_float(r.get(raw_col, ''))
                sv = (r.get(score_col, '') or '').strip()
                if rv is not None and sv:
                    buckets[sv].append(rv)
            p(f"\n{raw_col} -> {score_col}:")
            for s in sorted(buckets, key=lambda x: (x == '', x)):
                vals = buckets[s]
                if vals:
                    p(f"  score={s!r}: range [{min(vals)}, {max(vals)}] n={len(vals)}")
        p('')

    # === BUG AUDIT (Phase 1.1) ===
    p('=== BUG AUDIT: derived score columns ===')

    # Check 1: default-when-null detector
    if DERIVED_SCORE_AUDIT:
        p('\n-- Default-when-null check --')
        p('Flags when a derived score is nonzero on far more rows than its source has data.')
        for derived, sources in DERIVED_SCORE_AUDIT:
            derived_vals = [to_float(r.get(derived, '')) for r in rows]
            derived_nonzero = sum(1 for v in derived_vals if v is not None and v > 0)
            derived_rate = derived_nonzero / len(rows) if rows else 0
            source_max_cov = 0
            source_details = []
            for s in sources:
                c = sum(1 for r in rows if (r.get(s) or '').strip()
                        and (r.get(s) or '').strip().lower() not in ('none', 'n/a', 'na'))
                rate = c / len(rows) if rows else 0
                source_max_cov = max(source_max_cov, rate)
                source_details.append(f'{s}={100*rate:.1f}%')
            verdict = 'OK'
            if derived_rate > source_max_cov + 0.2 and derived_rate > 0.5:
                verdict = 'LIKELY BUG: default-when-null'
            p(f"  {derived}: nonzero={100*derived_rate:.1f}%  vs sources [{', '.join(source_details)}]  → {verdict}")
        p('')

    # Check 2: normalization-cap detector
    if NORMALIZED_COLUMNS:
        p('-- Normalization-cap check --')
        p(f'Flags 0..1 columns whose observed max is below {NORMALIZATION_CAP_THRESHOLD}.')
        for col in NORMALIZED_COLUMNS:
            vals = [to_float(r.get(col, '')) for r in rows]
            vals = [v for v in vals if v is not None]
            if not vals:
                p(f"  {col}: NO DATA")
                continue
            mx = max(vals)
            verdict = 'OK' if mx >= NORMALIZATION_CAP_THRESHOLD else f'LIKELY BUG: denominator too large (max={mx:.2f} < {NORMALIZATION_CAP_THRESHOLD})'
            p(f"  {col}: observed max={mx:.3f}  → {verdict}")
        p('')

    # Check 3: empty enrichment columns (any column referenced in scoring but 0% populated)
    p('-- Empty enrichment check (columns with <2% coverage) --')
    cols = list(rows[0].keys()) if rows else []
    for c in cols:
        n = sum(1 for r in rows if (r.get(c) or '').strip())
        if n == 0:
            p(f"  {c}: 0% populated: DEAD COLUMN")
        elif n / len(rows) < 0.02:
            p(f"  {c}: {100*n/len(rows):.2f}% populated: likely broken pipeline step")
    p('')

    # Check 4: canonical-entity sourcing-gap detector
    if CANONICAL_ENTITIES:
        p('-- Canonical-entity sourcing-gap check --')
        p('Flags canonical top-tier entities missing from the source list.')
        for ent in CANONICAL_ENTITIES:
            needle = ent.lower()
            hits = sum(1 for r in rows if needle in (r.get(NAME_COLUMN, '') or '').lower())
            tag = '✓ present' if hits else 'MISSING'
            p(f"  {ent}: {tag} ({hits} matches)")
        p('')

    return lines


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} path/to/source.csv")
        sys.exit(1)
    path = sys.argv[1]
    with open(path) as f:
        rows = list(csv.DictReader(f))
    lines = profile(rows)
    out = '\n'.join(lines)
    print(out)
    out_path = os.path.join(os.path.dirname(os.path.abspath(path)) or '.', 'profile_output.txt')
    with open(out_path, 'w') as f:
        f.write(out)
    print(f"\nWrote {out_path}")


if __name__ == '__main__':
    main()
