#!/usr/bin/env python3
"""Lint a cold email sequence against the cold-email-sequence skill's rules.

Usage:
    python3 lint_copy.py sequence.json      # Instantly campaign / {"steps": [...]} / [steps]
    python3 lint_copy.py draft.txt          # text blocks, see below
    python3 lint_copy.py draft.txt --renders 50

Text format: one block per variant, headed "=== E<step> [variant label]".
An optional first line "subject: ..." sets the subject; blank or missing = threaded reply.

    === E1 A
    subject: field visits
    {{RANDOM|Hey|Hi}} {{firstName}}, ...
    === E2
    {{firstName}}, ...

Every spintax combination is rendered (sampled above --renders) and checked,
including P.S. lines (one at most, ≤20 words, no grading or job tie-ins).
Exit code 1 if any ERROR.
"""
import argparse
import html
import itertools
import json
import random
import re
import sys
from pathlib import Path

WORDS = json.loads((Path(__file__).resolve().parent.parent / "references" / "spam_words.json").read_text())

SAMPLE_VARS = {"firstname": "Alex", "first_name": "Alex", "companyname": "Acme",
               "company_name": "Acme", "company": "Acme"}
SKIP_VARS = {"accountsignature", "sendingaccountfirstname", "signature"}
YOU = re.compile(r"\b(you|your|you're|yours|you've|you'll)\b", re.I)
ME = re.compile(r"\b(i|i'm|i've|i'll|we|we're|we've|our|us|my|me)\b", re.I)
PS_LINE = re.compile(r"(?im)^\s*p\.?\s?s\.?[\s:,-]")
GRADING = re.compile(r"\b(impressive|accomplished|talented|great background|bet that|shaped how|honed|instincts|so you know)\b", re.I)
LINK = re.compile(r"(https?://|www\.|\b[a-z0-9-]+\.(com|io|ai|co|net|org)/)", re.I)


# ---------- parsing ----------

def html_to_text(s):
    s = re.sub(r"(?i)<br\s*/?>", "\n", s or "")
    s = re.sub(r"(?i)</(div|p)>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"\n{3,}", "\n\n", s).strip()


def load(path):
    p = Path(path)
    raw = p.read_text()
    if p.suffix == ".json":
        d = json.loads(raw)
        if isinstance(d, dict) and "sequences" in d:
            d = d["sequences"][0]
        steps = d["steps"] if isinstance(d, dict) else d
        out = []
        for i, st in enumerate(steps):
            vs = st.get("variants") or [st]
            out.append({"n": i + 1, "delay": st.get("delay"),
                        "variants": [{"label": chr(65 + j), "subject": v.get("subject") or "",
                                      "body": html_to_text(v.get("body", ""))}
                                     for j, v in enumerate(vs)]})
        return out
    steps = {}
    for block in re.split(r"(?m)^===\s*", raw)[1:]:
        head, _, rest = block.partition("\n")
        m = re.match(r"E?(\d+)\s*(.*)", head.strip(), re.I)
        if not m:
            continue
        n, label = int(m.group(1)), (m.group(2).strip() or "A")
        subject = ""
        lines = rest.strip("\n").split("\n")
        if lines and lines[0].lower().startswith("subject:"):
            subject = lines[0].split(":", 1)[1].strip()
            lines = lines[1:]
        steps.setdefault(n, {"n": n, "delay": None, "variants": []})["variants"].append(
            {"label": label, "subject": subject, "body": "\n".join(lines).strip()})
    return [steps[k] for k in sorted(steps)]


def parse_spintax(s):
    """Split into a list of literal strings and option-lists for each {{RANDOM|...}} block."""
    parts, i, errs = [], 0, []
    while True:
        j = s.find("{{RANDOM", i)
        if j < 0:
            parts.append(s[i:])
            return parts, errs
        parts.append(s[i:j])
        k, depth = j + 2, 1
        while k < len(s) and depth:
            if s.startswith("{{", k):
                depth, k = depth + 1, k + 2
            elif s.startswith("}}", k):
                depth, k = depth - 1, k + 2
            else:
                k += 1
        if depth:
            errs.append("unclosed {{RANDOM block")
            parts.append(s[j:])
            return parts, errs
        inner = s[j + 2:k - 2]
        head, _, body = inner.partition("|")
        if head.strip() != "RANDOM":
            errs.append(f"malformed block: {{{{{inner[:40]}}}}}")
        if head != "RANDOM" or re.search(r"\s\||\|\s", inner):
            errs.append("spaces around | in {{RANDOM}} (house style: none)")
        opts, d, cur = [], 0, ""
        for ch_i, ch in enumerate(body):
            if body.startswith("{{", ch_i):
                d += 1
            if body.startswith("}}", ch_i):
                d -= 1
            if ch == "|" and d == 0:
                opts.append(cur)
                cur = ""
            else:
                cur += ch
        opts.append(cur)
        parts.append(opts)
        i = k


def renders(s, cap, rng):
    parts, _ = parse_spintax(s)
    blocks = [p for p in parts if isinstance(p, list)]
    total = 1
    for b in blocks:
        total *= len(b)
    combos = (itertools.product(*blocks) if total <= cap
              else (tuple(rng.choice(b) for b in blocks) for _ in range(cap)))
    out = []
    for combo in combos:
        it = iter(combo)
        out.append("".join(p if isinstance(p, str) else next(it) for p in parts))
    return out or [s], len(blocks), total


VAR = re.compile(r"\{\{\s*([^{}|]+?)\s*(?:\|\s*([^{}]*?)\s*)?\}\}")


def fill_vars(s):
    """Variables -> sample values; {{var | fallback}} renders its fallback (worst case: lead field empty)."""
    def rep(m):
        name, fb = m.group(1).strip(), m.group(2)
        if name.lower() in SKIP_VARS:
            return ""
        if fb is not None:
            return fb
        return SAMPLE_VARS.get(name.lower(), f"<{name}>")
    return VAR.sub(rep, s).strip()


# ---------- metrics ----------

def words(s):
    return re.findall(r"[A-Za-z0-9<>'$%.,/-]+", s)


def syllables(w):
    w = re.sub(r"[^a-z]", "", w.lower())
    if not w:
        return 0
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith("le") and n > 1:
        n -= 1
    return max(1, n)


def fk_grade(s):
    ws = [w for w in re.findall(r"[A-Za-z']+", s)]
    sents = max(1, len(re.findall(r"[.?!]+|\n\n", s)))
    if not ws:
        return 0.0
    syl = sum(syllables(w) for w in ws)
    return 0.39 * len(ws) / sents + 11.8 * syl / len(ws) - 15.59


def has_phrase(text, phrase):
    t = text.lower()
    if re.match(r"^[\w' -]+$", phrase):
        return re.search(r"(?<![\w'])" + re.escape(phrase) + r"(?![\w'])", t) is not None
    return phrase in t


# ---------- lint ----------

def lint(steps, cap):
    rng = random.Random(7)
    findings, variables = [], set()

    def add(level, where, msg):
        findings.append((level, where, msg))

    if steps and steps[0].get("delay") == 0:
        add("ERROR", "E1", "step 1 delay is 0: email 2 sends ~20 min after email 1 (delay is the wait AFTER the step)")

    for st in steps:
        n = st["n"]
        cold = n == 1 or any(v["subject"].strip() for v in st["variants"])
        for v in st["variants"]:
            w = f"E{n}.{v['label']}"
            subj, body = v["subject"].strip(), v["body"]
            for m in VAR.finditer(subj + body):
                if m.group(1).strip() != "RANDOM":
                    variables.add(m.group(1).strip() + (" (has fallback)" if m.group(2) is not None else ""))

            # raw-syntax checks
            for label, txt in (("subject", subj), ("body", body)):
                stripped = re.sub(r"\{\{.*?\}\}", "", txt, flags=re.S)
                if re.search(r"\{[^{}]*\|[^{}]*\}", stripped):
                    add("ERROR", w, f"{label}: single-brace {{a|b}} spintax is Smartlead syntax; Instantly sends it literally")
                if txt.count("{{") != txt.count("}}"):
                    add("ERROR", w, f"{label}: unbalanced {{{{ }}}}")
                for e in set(parse_spintax(txt)[1]):
                    add("WARN" if "spaces" in e else "ERROR", w, f"{label}: {e}")
                if re.search(r"\[[^\]]{2,}\]", txt):
                    add("ERROR", w, f"{label}: unfilled template bracket {re.search(r'\[[^\]]{2,}\]', txt).group(0)}")

            # subject
            if n == 1 and not subj:
                add("ERROR", w, "email 1 needs a subject")
            if subj:
                sub_rs, sub_blocks, _ = renders(subj, cap, rng)
                sub_msgs = set()
                for r in sub_rs:
                    s = fill_vars(r)
                    nw = len(s.split())
                    if len(s) > 50:
                        sub_msgs.add(("ERROR", f"subject {len(s)} chars (>50): {s!r}"))
                    elif nw > 4:
                        sub_msgs.add(("WARN", f"subject {nw} words (aim 2-4): {s!r}"))
                    if "!" in s:
                        sub_msgs.add(("ERROR", f"exclamation in subject: {s!r}"))
                    for b in WORDS["bad_subjects"]:
                        if has_phrase(s, b):
                            sub_msgs.add(("ERROR", f"subject uses banned {b!r}"))
                for lvl, msg in sorted(sub_msgs):
                    add(lvl, w, msg)
                if sub_blocks == 0:
                    add("WARN", w, "subject has no {{RANDOM}} block (minimum: 1)")

            # body renders
            rs, nblocks, total = renders(body, cap, rng)
            min_blocks = 3 if cold else 2
            if nblocks < min_blocks:
                add("WARN", w, f"{nblocks} spintax blocks (minimum {min_blocks} for {'a cold open' if cold else 'a follow-up'})")
            seen = set()

            def once(level, msg):
                if msg not in seen:
                    seen.add(msg)
                    add(level, w, msg)

            wcs, qcounts = [], set()
            for r in rs:
                t = fill_vars(r)
                low = t.lower()
                wc = len(words(t))
                wcs.append(wc)
                q = t.count("?")
                qcounts.add(q)
                if re.search(r"\b(\w+)\s+\1\b", t, re.I) and not re.search(r"\b(that that|had had)\b", low):
                    once("ERROR", f"doubled word in a render: {re.search(r'\b(\w+)\s+\1\b', t, re.I).group(0)!r}")
                if re.search(r"\s[,.?]", t):
                    once("ERROR", f"space before punctuation in a render (blank variable or bad spin): {t[max(0, re.search(r'\s[,.?]', t).start() - 25):re.search(r'\s[,.?]', t).end() + 5]!r}")
                if re.search(r"[^\n ]  +", t):
                    once("WARN", "double space in a render")
                if re.search(r"[{}|]", t):
                    once("ERROR", "stray { } or | after rendering")
                if q > 1:
                    once("ERROR" if cold else "WARN", f"{q} questions in a render; exactly one question, the CTA")
                for ph in WORDS["hard"]:
                    if has_phrase(low, ph):
                        once("ERROR", f"spam phrase: {ph!r}")
                for ph in WORDS["agency_vocab"]:
                    if has_phrase(low, ph):
                        once("ERROR", f"agency vocabulary: {ph!r}")
                for ph in WORDS["openers_and_filler"]:
                    if has_phrase(low, ph):
                        once("ERROR", f"filler / prefacing / follow-up reference: {ph!r}")
                for ph in WORDS["calendar_cta"]:
                    if has_phrase(low, ph):
                        once("ERROR" if n == 1 else "WARN", f"calendar/time ask {ph!r}" + (" in email 1" if n == 1 else ""))
                ps_lines = [ln for ln in t.split("\n") if PS_LINE.match(ln)]
                if len(ps_lines) > 1:
                    once("ERROR", "more than one P.S.")
                for ln in ps_lines:
                    if len(ln.split()) > 21:
                        once("WARN", f"P.S. {len(ln.split()) - 1} words (aim ≤20)")
                    if GRADING.search(ln):
                        once("WARN", f"P.S. grades the person or ties the fact to their job: {GRADING.search(ln).group(0)!r}")
                for ph in WORDS["soft"]:
                    if has_phrase(low, ph):
                        once("WARN", f"soft spam word: {ph!r}")
            if 0 in qcounts:
                once("WARN", "a render has no question; is there a CTA?")
            if len(qcounts) > 1:
                once("WARN", f"question count differs across spins {sorted(qcounts)}")

            first = fill_vars(rs[0])
            if re.search(r"[ - -]", subj + body):
                add("ERROR", w, "em/en dash")
            if re.search(r"\s-\s", first):
                add("WARN", w, "' - ' used as a dash; use a period or comma")
            if "!" in body:
                add("ERROR", w, "exclamation mark")
            links = LINK.findall(first)
            if links and n == 1:
                add("ERROR", w, "link in email 1")
            elif len(links) > 1:
                add("ERROR", w, f"{len(links)} links; max one, own domain, from email 2")

            lo, hi = min(wcs), max(wcs)
            span = f"{lo}" if lo == hi else f"{lo}-{hi}"
            if cold:
                if hi > 125:
                    add("ERROR", w, f"{span} words (>125)")
                elif hi > 90:
                    add("WARN", w, f"{span} words (aim 50-90)")
                elif lo < 25:
                    add("WARN", w, f"{span} words (thin for a cold open)")
            else:
                if hi > 80:
                    add("ERROR", w, f"{span} words (follow-up >80)")
                elif hi > 50:
                    add("WARN", w, f"{span} words (follow-ups aim under 50)")
            g = fk_grade(first)
            if g > 8:
                add("WARN", w, f"reading grade {g:.1f} (aim ≤7)")
            you, me = len(YOU.findall(first)), len(ME.findall(first))
            if me > you:
                add("WARN", w, f"more I/we ({me}) than you ({you}); write about them")
            add("INFO", w, f"{span} words, grade {g:.1f}, {nblocks} spin blocks ({total} combos), you:I {you}:{me}")
    return findings, variables


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path")
    ap.add_argument("--renders", type=int, default=200, help="max combinations rendered per field")
    ap.add_argument("--quiet", action="store_true", help="hide INFO lines")
    a = ap.parse_args()
    steps = load(a.path)
    if not steps:
        sys.exit("no steps found (text files need '=== E1' headers)")
    findings, variables = lint(steps, a.renders)
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    for lvl, where, msg in sorted(findings, key=lambda f: (f[1], order[f[0]])):
        if a.quiet and lvl == "INFO":
            continue
        print(f"{lvl:5} {where:7} {msg}")
    errs = sum(f[0] == "ERROR" for f in findings)
    warns = sum(f[0] == "WARN" for f in findings)
    print(f"\n{len(steps)} steps, {errs} errors, {warns} warnings")
    if variables:
        print("variables used (preflight every one non-empty on every lead):",
              ", ".join(sorted(v for v in variables if v.lower() not in SKIP_VARS)))
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
