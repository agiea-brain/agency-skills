#!/usr/bin/env python3
"""
build_corpus.py: merge extracted quote files into data/corpus.json.

Reads every data/quotes/*.jsonl (one quote per line, written during setup or a
refresh), checks each row against the codebook in SETUP.md, de-duplicates by
quote_key, and writes data/corpus.json with a fresh `generated` stamp.

Reports by set math, not row count: rows read, distinct keys, duplicate keys,
conflicting duplicates (same key, different text), and rejected rows with reasons.
Exits 1 if anything was rejected or conflicted, so a bad batch never slips in.

  ./build_corpus.py            # build
  ./build_corpus.py --check    # validate only, write nothing
"""
import argparse, collections, datetime, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
QUOTES = os.path.join(ROOT, "data", "quotes")
OUT = os.path.join(ROOT, "data", "corpus.json")
PROFILE = os.path.join(HERE, "profile.json")

STANCES = {"problem", "desire", "failed-solution", "objection", "proof", "decision-trigger"}
STAGES = {"Problem Aware", "Solution/Category Aware", "Product/Brand Aware", "Most Aware"}
SOURCES = {"discovery-call", "sales-call", "client-call", "interview"}
CONFIDENCE = {"high", "med", "low"}
KEY = re.compile(r"^[a-z-]+:[^#]+(#\d+)?$")
REQUIRED = ("quote_key", "quote", "stance", "stage", "source_type", "confidence")


def check_row(q, personas):
    errs = []
    for f in REQUIRED:
        if not q.get(f):
            errs.append("missing %s" % f)
    if q.get("quote_key") and not KEY.match(q["quote_key"]):
        errs.append("quote_key %r must look like source:id#n" % q["quote_key"])
    if q.get("stance") and q["stance"] not in STANCES:
        errs.append("stance %r not in %s" % (q["stance"], sorted(STANCES)))
    if q.get("stage") and q["stage"] not in STAGES:
        errs.append("stage %r not in %s" % (q["stage"], sorted(STAGES)))
    if q.get("source_type") and q["source_type"] not in SOURCES:
        errs.append("source_type %r not in %s" % (q["source_type"], sorted(SOURCES)))
    if q.get("confidence") and q["confidence"] not in CONFIDENCE:
        errs.append("confidence %r not in %s" % (q["confidence"], sorted(CONFIDENCE)))
    if q.get("persona") and personas and q["persona"] not in personas:
        errs.append("persona %r is not one of the personas in references/profile.json" % q["persona"])
    if q.get("date"):
        try:
            datetime.date.fromisoformat(q["date"])
        except ValueError:
            errs.append("date %r must be YYYY-MM-DD" % q["date"])
    return errs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate only; do not write data/corpus.json")
    a = ap.parse_args()

    personas = set(json.load(open(PROFILE)).get("personas") or []) if os.path.exists(PROFILE) else set()
    files = sorted(glob.glob(os.path.join(QUOTES, "*.jsonl")))
    if not files:
        sys.exit("no quote files in %s: extract quotes first (SETUP.md step 3)" % QUOTES)

    rows, rejected = 0, []
    by_key, dup_same, dup_conflict = {}, 0, []
    for path in files:
        for i, line in enumerate(open(path), 1):
            if not line.strip():
                continue
            rows += 1
            where = "%s:%d" % (os.path.basename(path), i)
            try:
                q = json.loads(line)
            except json.JSONDecodeError as e:
                rejected.append((where, ["not valid JSON: %s" % e]))
                continue
            errs = check_row(q, personas)
            if errs:
                rejected.append((where, errs))
                continue
            k = q["quote_key"]
            if k in by_key:
                if by_key[k]["quote"] == q["quote"]:
                    dup_same += 1
                else:
                    dup_conflict.append((where, k))
                continue
            by_key[k] = q

    print("files read:          %d" % len(files))
    print("rows read:           %d" % rows)
    print("distinct quote_keys: %d" % len(by_key))
    print("exact duplicates:    %d (dropped, harmless)" % dup_same)
    print("conflicting dupes:   %d" % len(dup_conflict))
    print("rejected rows:       %d" % len(rejected))
    for where, k in dup_conflict[:20]:
        print("  ! %s reuses quote_key %s with different text" % (where, k))
    for where, errs in rejected[:20]:
        print("  x %s: %s" % (where, "; ".join(errs)))
    if len(rejected) + len(dup_conflict) > 20:
        print("  ... and more")

    quotes = sorted(by_key.values(), key=lambda q: q["quote_key"])
    counts = collections.Counter(q["source_type"] for q in quotes)
    print("by source_type:      %s" % dict(counts))

    if rejected or dup_conflict:
        print("\nNOT WRITTEN: fix the rows above and rerun.")
        sys.exit(1)
    if a.check:
        print("\nCHECK PASSED (nothing written)")
        return

    corpus = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
              "total": len(quotes), "quotes": quotes}
    json.dump(corpus, open(OUT, "w"), indent=1, ensure_ascii=False)
    if os.path.exists(PROFILE):
        prof = json.load(open(PROFILE))
        prof["last_corpus_build"] = corpus["generated"]
        json.dump(prof, open(PROFILE, "w"), indent=2, ensure_ascii=False)
    print("\nWROTE %s: %d quotes, generated %s" % (os.path.relpath(OUT, ROOT), len(quotes), corpus["generated"]))


if __name__ == "__main__":
    main()
