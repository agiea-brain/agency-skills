#!/usr/bin/env python3
"""
test_gate.py: regression test for the citation gate.

Run after any change to validate_verdict.py, seats.json, or verdict-schema.json.
Builds a live evidence pack, constructs a valid verdict, then mutates it into each
known failure mode and asserts the gate catches it. Two cases assert the gate does
NOT fire: a validator that rejects everything is as useless as one that rejects
nothing.

  ./test_gate.py        -> "ALL 11 TESTS PASS" and exit 0
"""
import copy, json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PANEL = os.path.join(HERE, "panel.py")
VALIDATE = os.path.join(HERE, "validate_verdict.py")


def main():
    # Optional: ./test_gate.py --config <other panel seats.json> --seat <a seat in it>
    cfg = os.path.abspath(sys.argv[sys.argv.index("--config") + 1]) if "--config" in sys.argv \
        else os.path.join(HERE, "seats.json")
    seat = sys.argv[sys.argv.index("--seat") + 1] if "--seat" in sys.argv else "objector"
    CORPUS = os.path.normpath(os.path.join(os.path.dirname(cfg), "..", json.load(open(cfg))["corpus"]))
    cflag = ["--config", cfg]
    tmp = tempfile.mkdtemp(prefix="panel-gate-")
    pack_path = os.path.join(tmp, "pack.json")
    with open(pack_path, "w") as fh:
        fh.write(subprocess.run([sys.executable, PANEL] + cflag + ["evidence", "--seat", seat, "--n", "6"],
                                capture_output=True, text=True, check=True).stdout)
    pack = json.load(open(pack_path))
    k = [e["quote_key"] for e in pack["evidence"]]
    outside = next(q["quote_key"] for q in json.load(open(CORPUS))["quotes"] if q["quote_key"] not in k)

    good = {
        "seat": seat,
        "question": "Does the pricing page answer the cost objection?",
        "corpus_version": pack["corpus_version"],
        "retrieval": pack["retrieval"],
        "verdict": {"answer": "Names the price, never addresses the switching-cost fear.",
                    "confidence": "supported", "citations": [k[0], k[1]]},
        "strongest_objection": {"text": "Any new tool reads as extra work for a stretched team.", "citations": [k[2]]},
        "stopped_reading_at": "The pricing tier table.",
    }

    cases = [("valid verdict", good, 0)]

    def mut(name, fn, expected):
        v = copy.deepcopy(good)
        fn(v)
        cases.append((name, v, expected))

    def reband(v, **kw):
        v["retrieval"] = dict(v["retrieval"], **kw)

    mut("fabricated citation", lambda v: v["verdict"]["citations"].append("calls:does-not-exist#42"), 1)
    mut("real key outside the pack", lambda v: v["verdict"]["citations"].append(outside), 1)
    mut("missing forced dissent", lambda v: v.pop("strongest_objection"), 1)
    mut("dissent with no citations", lambda v: v["strongest_objection"].update({"citations": []}), 1)
    mut("insufficient density, answered anyway", lambda v: reband(v, density_band="insufficient", n=3), 1)
    mut("thin density claiming 'supported'", lambda v: reband(v, density_band="thin", n=7), 1)
    mut("thin density, correctly hedged",
        lambda v: (reband(v, density_band="thin", n=7), v["verdict"].__setitem__("confidence", "weak signal")), 0)
    mut("insufficient density, correctly refuses",
        lambda v: (reband(v, density_band="insufficient", n=3), v.__setitem__("verdict", None)), 0)
    mut("stale corpus version", lambda v: v.__setitem__("corpus_version", {"generated": "2026-01-01", "total": 900}), 1)
    mut("unknown seat", lambda v: v.__setitem__("seat", "the_persona"), 1)

    fails = 0
    for name, v, expected in cases:
        p = os.path.join(tmp, "t.json")
        json.dump(v, open(p, "w"))
        r = subprocess.run([sys.executable, VALIDATE, p, "--evidence", pack_path] + cflag, capture_output=True, text=True)
        ok = r.returncode == expected
        fails += 0 if ok else 1
        print(("  OK  " if ok else " FAIL ") + "%-40s exit=%s (want %s)" % (name, r.returncode, expected))

    if fails:
        print("\n%d TEST(S) FAILED" % fails)
        sys.exit(1)
    print("\nALL %d TESTS PASS" % len(cases))


if __name__ == "__main__":
    main()
