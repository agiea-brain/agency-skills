#!/usr/bin/env python3
"""
panel.py: evidence retrieval for the ICP panel.

Slices data/corpus.json down to one seat's evidence pack, widening the filter
along a fixed ladder when the narrow slice is too thin, and reporting exactly which
precision level the answer is actually standing on.

Stdlib only: no pip install needed.

  ./panel.py seats
  ./panel.py evidence --seat cold_skeptic --persona "Mid-size firm"
  ./panel.py evidence --seat objector --pattern "Slow onboarding" --n 8

--config points at a different seats.json (default: seats.json beside this script).
"""
import argparse, datetime, hashlib, json, os, sys, collections

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = os.environ.get("PANEL_CONFIG") or os.path.join(HERE, "seats.json")
NARROW_DIMS = ("pattern", "persona", "stage", "topic")

CONF_RANK = {"high": 0, "med": 1, "low": 2}


def load():
    cfg = json.load(open(CFG))
    # cfg["corpus"] is relative to the panel root (the folder holding config/)
    corpus_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(CFG)), "..", cfg["corpus"]))
    if not os.path.exists(corpus_path):
        sys.exit("no corpus at %s: run setup first (see SETUP.md), then references/build_corpus.py" % corpus_path)
    corpus = json.load(open(corpus_path))
    return cfg, corpus


def apply_base(quotes, base):
    out = quotes
    if "source_type_in" in base:
        out = [q for q in out if q.get("source_type") in base["source_type_in"]]
    if "stance_in" in base:
        out = [q for q in out if q.get("stance") in base["stance_in"]]
    if "stage_in" in base:
        out = [q for q in out if q.get("stage") in base["stage_in"]]
    if "persona_in" in base:
        out = [q for q in out if q.get("persona") in base["persona_in"]]
    return out


def apply_narrow(quotes, **filters):
    out = quotes
    for dim, val in filters.items():
        if val:
            out = [q for q in out if (q.get(dim) or "") == val]
    return out


def rid(q):
    p = q.get("provenance") or {}
    return p.get("recording_id") or p.get("doc_id") or q.get("source_ref") or "?"


def sample(quotes, n):
    """Prefer high-confidence, then spread across distinct calls so n quotes from one
    call never masquerade as n independent data points."""
    by_call = collections.OrderedDict()
    for q in sorted(quotes, key=lambda x: CONF_RANK.get(x.get("confidence"), 3)):
        by_call.setdefault(rid(q), []).append(q)
    # Visit calls in a stable hash order, not corpus order: corpus order would draw only
    # from the alphabetically-first sources.
    by_call = collections.OrderedDict(
        sorted(by_call.items(), key=lambda kv: hashlib.sha1(str(kv[0]).encode()).hexdigest()))
    picked, exhausted = [], False
    while len(picked) < n and not exhausted:
        exhausted = True
        for call in list(by_call):
            if by_call[call]:
                picked.append(by_call[call].pop(0))
                exhausted = False
                if len(picked) >= n:
                    break
    return picked


def age_profile(quotes, stale_days=540):
    """Surface how old the evidence is. Never used to discard: pruning would gut a
    thin corpus, and 'is this pain still showing up' is a question you can only ask
    if you kept the old quotes."""
    ds = sorted(q["date"] for q in quotes if q.get("date"))
    out = {"dated": len(ds), "undated": len(quotes) - len(ds)}
    if not ds:
        return out
    today = datetime.date.today()
    ages = [(today - datetime.date.fromisoformat(d)).days for d in ds]
    ages.sort()
    out["oldest"] = ds[0]
    out["newest"] = ds[-1]
    out["median_age_days"] = ages[len(ages) // 2]
    recent = sum(1 for a in ages if a <= 365)
    out["within_12mo"] = recent
    out["share_within_12mo"] = round(recent / len(ages), 2)
    if ages[len(ages) // 2] > stale_days:
        out["flag"] = ("STALE: median evidence is %d days old. Say so in the verdict: this "
                       "describes what buyers said, not necessarily what they say now."
                       % ages[len(ages) // 2])
    return out


def band(n, bands):
    if n >= bands["sufficient"]:
        return "sufficient"
    if n >= bands["thin"]:
        return "thin"
    return "insufficient"


def retrieve(seat_key, n=12, **filters):
    cfg, corpus = load()
    if seat_key not in cfg["seats"]:
        sys.exit("unknown seat %r: choose from %s" % (seat_key, ", ".join(cfg["seats"])))
    seat = cfg["seats"][seat_key]
    bands = cfg["density_bands"]
    pool = apply_base(corpus["quotes"], seat["base_filter"])

    requested = {d: filters.get(d) for d in NARROW_DIMS}
    active = dict(requested)
    dropped = []

    # Widen one dimension at a time until the slice can carry a verdict.
    # Ladder from config, then any other requested dimension the config didn't rank.
    ladder = list(cfg["widening_ladder"]) + [d for d in NARROW_DIMS if d not in cfg["widening_ladder"]]
    for dim in [None] + ladder:
        if dim is not None:
            if not active.get(dim):
                continue
            active[dim] = None
            dropped.append(dim)
        hits = apply_narrow(pool, **active)
        if band(len(hits), bands) == "sufficient":
            break

    hits = apply_narrow(pool, **active)
    surviving = [k for k, v in active.items() if v] or ["seat base filter only"]
    picked = sample(hits, n)

    return {
        "seat": seat_key,
        "seat_role": seat["role"],
        "may_not_answer": seat["may_not_answer"],
        "corpus_version": {"generated": corpus.get("generated"), "total": corpus.get("total")},
        "retrieval": {
            "requested_filter": {k: v for k, v in requested.items() if v},
            "precision_level": "+".join(surviving),
            "dropped": dropped,
            "n": len(hits),
            "distinct_calls": len({rid(q) for q in hits}),
            "density_band": band(len(hits), bands),
            "source_mix": dict(collections.Counter(q.get("source_type") for q in hits)),
            "age_mix": age_profile(hits),
        },
        "evidence": [
            {
                "quote_key": q["quote_key"],
                "quote": q["quote"],
                "stance": q.get("stance"),
                "stage": q.get("stage"),
                "persona": q.get("persona") or None,
                "pattern": q.get("pattern"),
                "topic": q.get("topic"),
                "source_type": q.get("source_type"),
                "confidence": q.get("confidence"),
                "public_ok": q.get("public_ok"),
                "date": q.get("date"),
            }
            for q in picked
        ],
    }


def main():
    global CFG
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", help="seats.json of the panel to query (default: seats.json beside this script)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("seats", help="list seats and their sizes")
    e = sub.add_parser("evidence", help="build an evidence pack for one seat")
    e.add_argument("--seat", required=True)
    e.add_argument("--persona")
    e.add_argument("--stage")
    e.add_argument("--pattern")
    e.add_argument("--topic")
    e.add_argument("--n", type=int, default=12)
    a = ap.parse_args()
    if a.config:
        CFG = os.path.abspath(a.config)

    if a.cmd == "seats":
        cfg, corpus = load()
        bands = cfg["density_bands"]
        print("corpus: %s quotes (generated %s)\n" % (corpus.get("total"), corpus.get("generated")))
        for k, s in cfg["seats"].items():
            pool = apply_base(corpus["quotes"], s["base_filter"])
            calls = len({rid(q) for q in pool})
            flag = "" if band(len(pool), bands) == "sufficient" else \
                "   <-- too thin to judge anything; add more %s" % ", ".join(s["base_filter"].get("stance_in", ["quotes"]))
            print("%-14s n=%-5s calls=%-4s %s%s" % (k, len(pool), calls, s["role"], flag))
        return

    filters = {d: getattr(a, d) for d in NARROW_DIMS}
    print(json.dumps(retrieve(a.seat, a.n, **filters), indent=2))


if __name__ == "__main__":
    main()
