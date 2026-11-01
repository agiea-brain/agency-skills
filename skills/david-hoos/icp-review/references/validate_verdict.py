#!/usr/bin/env python3
"""
validate_verdict.py: the hard gate.

A prompt asking the model to cite its sources is a suggestion. This is a check.
Every quote_key in a verdict must resolve to a real row in data/corpus.json,
and (when an evidence pack is supplied) must have actually been retrieved for the
question. Density and verdict strength must agree. Forced dissent must be present.

Exits 0 on pass, 1 on failure, printing every violation.

  ./validate_verdict.py verdict.json
  ./validate_verdict.py verdict.json --evidence pack.json

WHAT THIS DOES NOT DO: it proves the cited evidence exists and was retrieved. It
cannot prove the inference drawn from that evidence is sound: a verdict can cite
four real quotes and reason wrongly from them and still pass. Detecting that is the
backtest's job, not this gate's.
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEATS = CORPUS_PATH = VALID_SEATS = None


def configure(cfg_path=None):
    """Bind the gate to one panel's seats + corpus."""
    global SEATS, CORPUS_PATH, VALID_SEATS
    cfg_path = os.path.abspath(cfg_path or os.environ.get("PANEL_CONFIG")
                               or os.path.join(HERE, "seats.json"))
    SEATS = json.load(open(cfg_path))
    CORPUS_PATH = os.path.normpath(os.path.join(os.path.dirname(cfg_path), "..", SEATS["corpus"]))
    VALID_SEATS = set(SEATS["seats"])


configure()
BANDS = {"sufficient", "thin", "insufficient"}


def corpus_keys():
    c = json.load(open(CORPUS_PATH))
    return {q["quote_key"] for q in c["quotes"]}, c


def check(v, evidence=None):
    errs = []
    keys, corpus = corpus_keys()

    def need(obj, field, where, allow_empty=False):
        """allow_empty: the key must be PRESENT but may be empty: an unfiltered
        query legitimately has requested_filter == {}."""
        if field not in obj:
            errs.append("missing required field: %s.%s" % (where, field))
            return False
        if not allow_empty and obj.get(field) in (None, "", [], {}):
            errs.append("empty required field: %s.%s" % (where, field))
            return False
        return True

    # --- structure -----------------------------------------------------------
    for f in ("seat", "question", "corpus_version", "retrieval", "strongest_objection"):
        need(v, f, "verdict")
    if "verdict" not in v:
        errs.append("missing required field: verdict.verdict (use null for no-evidence)")

    if v.get("seat") not in VALID_SEATS:
        errs.append("unknown seat %r (expected one of %s)" % (v.get("seat"), ", ".join(sorted(VALID_SEATS))))

    cv = v.get("corpus_version") or {}
    if cv.get("total") != corpus.get("total") or cv.get("generated") != corpus.get("generated"):
        errs.append("corpus_version %s does not match the corpus on disk %s: the verdict was "
                    "produced against a different corpus state"
                    % (json.dumps(cv), json.dumps({"generated": corpus.get("generated"), "total": corpus.get("total")})))

    r = v.get("retrieval") or {}
    need(r, "requested_filter", "retrieval", allow_empty=True)
    need(r, "precision_level", "retrieval")
    need(r, "n", "retrieval", allow_empty=True)   # n == 0 is meaningful
    need(r, "density_band", "retrieval")
    band = r.get("density_band")
    if band not in BANDS:
        errs.append("retrieval.density_band %r must be one of %s" % (band, sorted(BANDS)))

    # --- density must agree with verdict strength ----------------------------
    verdict = v.get("verdict")
    if band == "insufficient" and verdict is not None:
        errs.append("density_band is 'insufficient' (n=%s) but a verdict was returned: "
                    "this seat has no standing to answer" % r.get("n"))
    if band == "thin" and isinstance(verdict, dict) and verdict.get("confidence") != "weak signal":
        errs.append("density_band is 'thin' (n=%s) so verdict.confidence must be 'weak signal', got %r"
                    % (r.get("n"), verdict.get("confidence")))
    if isinstance(verdict, dict):
        for f in ("answer", "confidence", "citations"):
            need(verdict, f, "verdict.verdict")

    # --- forced dissent ------------------------------------------------------
    so = v.get("strongest_objection") or {}
    if not so.get("text"):
        errs.append("strongest_objection.text is required on EVERY verdict, including favourable "
                    "ones: if the evidence contains no objection, say so and cite the nearest friction")
    if not so.get("citations"):
        errs.append("strongest_objection.citations must contain at least one quote_key")

    # --- scope ---------------------------------------------------------------
    seat_cfg = SEATS["seats"].get(v.get("seat"))
    if seat_cfg and verdict is not None and "unresolved_questions" not in v and seat_cfg.get("_scope_warning"):
        pass  # advisory only

    # --- citations resolve ---------------------------------------------------
    cited = []
    if isinstance(verdict, dict):
        cited += list(verdict.get("citations") or [])
    cited += list(so.get("citations") or [])
    for uq in v.get("unresolved_questions") or []:
        if not uq.get("citations"):
            errs.append("unresolved_questions entry %r carries no citations" % uq.get("question", "")[:50])
        cited += list(uq.get("citations") or [])

    unknown = [k for k in cited if k not in keys]
    for k in sorted(set(unknown)):
        errs.append("FABRICATED CITATION: quote_key %r does not exist in the corpus" % k)

    if evidence is not None:
        retrieved = {e["quote_key"] for e in evidence.get("evidence", [])}
        outside = [k for k in cited if k in keys and k not in retrieved]
        for k in sorted(set(outside)):
            errs.append("citation %r is a real quote but was NOT in the retrieved evidence pack "
                        "- it was sourced from outside the seat's slice" % k)

    return errs, len(set(cited))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verdict")
    ap.add_argument("--evidence", help="the evidence pack the verdict was built from")
    ap.add_argument("--config", help="seats.json of the panel (default: seats.json beside this script)")
    a = ap.parse_args()
    if a.config:
        configure(a.config)

    v = json.load(open(a.verdict))
    ev = json.load(open(a.evidence)) if a.evidence else None
    errs, n_cited = check(v, ev)

    if errs:
        print("REJECTED: %d violation(s):\n" % len(errs))
        for e in errs:
            print("  x %s" % e)
        sys.exit(1)
    print("PASS: %d citations, all resolve%s" % (n_cited, " and all within the evidence pack" if ev else ""))


if __name__ == "__main__":
    main()
