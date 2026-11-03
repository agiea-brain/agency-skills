#!/usr/bin/env python3
"""Sample size, minimum detectable effect and Bayesian readout for cold email A/B tests.

    python3 ab_test.py n 0.01 2            # sends per arm to detect 2x lift at a 1% baseline
    python3 ab_test.py n 0.01 1.5 --alpha 0.10
    python3 ab_test.py mde 0.01 3000       # smallest lift detectable with 3,000 sends per arm
    python3 ab_test.py analyze 2400 21 2400 38          # champion sends, positives, challenger sends, positives
    python3 ab_test.py analyze 2400 21 2400 38 --prior 1 99

Metric is positive reply rate per unique lead. Two-sided test, 80% power by default.
No dependencies (stdlib only).
"""
import argparse
import math
import random
from statistics import NormalDist

Z = NormalDist().inv_cdf


def n_per_arm(p1, lift, alpha=0.05, power=0.8):
    p2 = p1 * lift
    pbar = (p1 + p2) / 2
    num = Z(1 - alpha / 2) * math.sqrt(2 * pbar * (1 - pbar)) + Z(power) * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(num ** 2 / (p2 - p1) ** 2)


def mde(p1, n, alpha=0.05, power=0.8):
    lo, hi = 1.0001, 50.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if n_per_arm(p1, mid, alpha, power) > n:
            lo = mid
        else:
            hi = mid
    return hi


def analyze(na, xa, nb, xb, a0, b0, draws=200_000, seed=7):
    rng = random.Random(seed)
    wins, loss_b, loss_a = 0, 0.0, 0.0
    for _ in range(draws):
        pa = rng.betavariate(a0 + xa, b0 + na - xa)
        pb = rng.betavariate(a0 + xb, b0 + nb - xb)
        wins += pb > pa
        loss_b += max(pa - pb, 0)
        loss_a += max(pb - pa, 0)
    return wins / draws, loss_b / draws, loss_a / draws


def wilson(x, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = x / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0, c - h), c + h


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("n", help="sends per arm")
    s.add_argument("baseline", type=float)
    s.add_argument("lift", type=float, help="relative, e.g. 1.5 or 2")
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s = sub.add_parser("mde", help="minimum detectable lift for a given n per arm")
    s.add_argument("baseline", type=float)
    s.add_argument("n", type=int)
    s.add_argument("--alpha", type=float, default=0.05)
    s.add_argument("--power", type=float, default=0.8)
    s = sub.add_parser("analyze", help="Bayesian readout: champion (A) vs challenger (B)")
    for k in ("sends_a", "pos_a", "sends_b", "pos_b"):
        s.add_argument(k, type=int)
    s.add_argument("--prior", type=float, nargs=2, metavar=("A0", "B0"),
                   help="Beta prior; default Beta(1, 1/baseline - 1) from the pooled rate")
    s.add_argument("--tolerance", type=float, default=0.001, help="expected-loss stop threshold (0.001 = 0.1 point)")
    a = ap.parse_args()

    if a.cmd == "n":
        n = n_per_arm(a.baseline, a.lift, a.alpha, a.power)
        exp = n * a.baseline
        print(f"{n:,} sends per arm ({2 * n:,} total) to detect {a.lift}x on a {a.baseline:.2%} baseline "
              f"(alpha {a.alpha}, power {a.power}). Expect ~{exp:.0f} positives in the champion arm.")
    elif a.cmd == "mde":
        m = mde(a.baseline, a.n, a.alpha, a.power)
        print(f"With {a.n:,} sends per arm at {a.baseline:.2%}, the smallest detectable lift is {m:.2f}x "
              f"({a.baseline * m:.2%}).")
        if m > 2:
            print("MDE > 2x: only test list, offer, angle or segment changes at this volume.")
    else:
        pooled = (a.pos_a + a.pos_b) / max(1, a.sends_a + a.sends_b)
        priors = [tuple(a.prior)] if a.prior else [(1, max(1, round(1 / max(pooled, 1e-4)) - 1)), (1, 1)]
        for lbl, n, x in (("A champion", a.sends_a, a.pos_a), ("B challenger", a.sends_b, a.pos_b)):
            lo, hi = wilson(x, n)
            print(f"{lbl:13} {x:4} / {n:6,}  PRR {x / max(n, 1):.2%}  95% CI {lo:.2%}-{hi:.2%}")
        if min(a.pos_a, a.pos_b) < 10:
            print("note: an arm has under 10 positives; read this as a hypothesis, not a result.")
        for a0, b0 in priors:
            p, lb, la = analyze(a.sends_a, a.pos_a, a.sends_b, a.pos_b, a0, b0)
            if p >= 0.9 and lb < a.tolerance:
                verdict = "PROMOTE challenger (if the validity gate passed)"
            elif p <= 0.1:
                verdict = "KEEP champion"
            else:
                verdict = "INCONCLUSIVE: extend once to 1.5x n, or keep the simpler variant"
            print(f"prior Beta({a0:g},{b0:g}): P(B>A) = {p:.3f}, expected loss choosing B = {lb * 100:.3f} pts, "
                  f"choosing A = {la * 100:.3f} pts -> {verdict}")


if __name__ == "__main__":
    main()
