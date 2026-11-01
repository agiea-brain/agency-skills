#!/usr/bin/env python3
"""
score.py: score the panel's pre-registered predictions against what really happened.

The citation gate proves a verdict's evidence exists. It cannot prove the reasoning
is right. This does: every time the panel picks between variants BEFORE the real
result exists (an A/B test, two subject lines, a title rewrite), log it in
predictions.jsonl. When the result comes in, fill truth_winner. This script runs an
exact one-sided binomial test against a coin flip.

The headline number is not accuracy: it is power. A good panel lands around
65-70%, which is undetectable until roughly 30-40 scored predictions. Below that
this prints UNDERPOWERED rather than letting a lucky 4/5 read as success.

predictions.jsonl, one JSON object per line:
  {"id": "2026-11-03-subject-lines", "date": "2026-11-03", "question": "...",
   "variants": ["A text", "B text"], "panel_pick": "A", "truth_winner": null,
   "metric": "open rate", "notes": ""}

  ./score.py
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "..", "predictions.jsonl")


def binom_p_ge(c, n, p=0.5):
    return sum(math.comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(c, n + 1)) if n else 1.0


def min_correct_for_sig(n, alpha=0.05):
    for c in range(n + 1):
        if binom_p_ge(c, n) <= alpha:
            return c
    return None


def main():
    rows = [json.loads(l) for l in open(LEDGER) if l.strip()] if os.path.exists(LEDGER) else []
    scored = [r for r in rows if r.get("truth_winner") not in (None, "")]
    pending = len(rows) - len(scored)
    n = len(scored)
    correct = sum(1 for r in scored if r.get("panel_pick") == r.get("truth_winner"))
    print("predictions logged: %d   scored: %d   waiting on a result: %d" % (len(rows), n, pending))
    if not n:
        print("Nothing to score yet. Log a prediction before every real A/B result.")
        return
    p = binom_p_ge(correct, n)
    need = min_correct_for_sig(n)
    print("panel correct: %d/%d (%.0f%%)   p vs coin flip = %.3f" % (correct, n, 100.0 * correct / n, p))
    if n < 30:
        bar = "%d/%d" % (need, n) if need is not None else "more predictions: no score"
        print("UNDERPOWERED: at n=%d you need %s to beat chance. Treat verdicts as "
              "well-sourced opinion, not calibrated prediction." % (n, bar))
    elif p <= 0.05:
        print("CALIBRATED: the panel beats a coin flip on real outcomes.")
    else:
        print("NOT BEATING CHANCE at n=%d. Read the misses before trusting another verdict." % n)


if __name__ == "__main__":
    main()
