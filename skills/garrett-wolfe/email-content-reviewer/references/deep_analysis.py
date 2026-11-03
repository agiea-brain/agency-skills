#!/usr/bin/env python3
"""
Deep structural analysis of all sent emails from an Instantly instance.
Covers: cross-campaign duplicates, subject line quality, step/sequence structure,
sender/signature consistency, CTA calibration, competitive mentions, vertical distribution.

Usage:
    python3 deep_analysis.py <emails_dir>
    # emails_dir should contain all the saved list_emails MCP result files

Output: Structured findings to stdout.
"""

import json, glob, re, sys, os
from html.parser import HTMLParser
from collections import Counter, defaultdict

class Strip(HTMLParser):
    def __init__(self): super().__init__(); self.r = []
    def handle_data(self, d): self.r.append(d)
    def text(self): return ' '.join(self.r).strip()

def strip(html):
    s = Strip()
    try: s.feed(html or ''); return s.text()
    except: return html or ''

def load_emails(emails_dir, mcp_prefix):
    """Load and deduplicate all emails from saved MCP result files."""
    pattern = os.path.join(emails_dir, f'{mcp_prefix}-list_emails-*.txt')
    files = sorted(glob.glob(pattern))
    all_emails = []; seen = set()
    for fname in files:
        with open(fname) as f: raw = json.load(f)
        inner = json.loads(raw['result'])
        for e in inner.get('items', []):
            eid = e.get('id','')
            if eid not in seen:
                seen.add(eid)
                body_obj = e.get('body') or {}
                html = body_obj.get('html','') if isinstance(body_obj, dict) else str(body_obj)
                e['_body_text'] = strip(html)
                all_emails.append(e)
    return all_emails

def get_persona(from_addr):
    # Groups results by sending mailbox. Map usernames to sender names here if you want them merged.
    return (from_addr.split('@')[0] if '@' in from_addr else from_addr).lower()

# Set these per client. Each keyword is matched against the recipient's email address.
VERTICAL_KEYWORDS = {
    'tech/software': ['.ai', '.io', 'saas', 'software'],
    'education/nonprofit': ['.edu', '.k12', 'university', 'college', 'school'],
    'pharma/biotech/medtech': ['pharma', 'biotech', 'medtech'],
    'food/beverage/CPG': ['food', 'beverage'],
}

def classify_vertical(email):
    d = email.lower() if email else ''
    for vertical, keywords in VERTICAL_KEYWORDS.items():
        if any(k in d for k in keywords):
            return vertical
    return 'other'

def analyze(all_emails):
    total = len(all_emails)
    print(f"\n{'='*70}")
    print(f"DEEP ANALYSIS: {total} emails")
    print(f"{'='*70}")

    # Date range
    dates = sorted(set(e.get('timestamp_email','')[:10] for e in all_emails if e.get('timestamp_email')))
    if dates: print(f"Date range: {dates[0]} to {dates[-1]}")

    # 1. Cross-campaign duplicates
    print(f"\n{'─'*60}")
    print("1. CROSS-CAMPAIGN RECIPIENT OVERLAP")
    print(f"{'─'*60}")
    rc = defaultdict(set)
    for e in all_emails:
        to = (e.get('to_address_email_list') or '').lower().strip()
        c = e.get('campaign_id','')[:8]
        if to: rc[to].add(c)
    multi = {r: camps for r, camps in rc.items() if len(camps) > 1}
    print(f"  Recipients in 2+ campaigns: {len(multi)}")
    if multi:
        print("  Examples:")
        for r, camps in sorted(multi.items())[:15]:
            print(f"    {r}: {sorted(camps)}")
    else:
        print("  ✅ No recipients are being double-contacted across campaigns.")

    # 2. Subject line analysis
    print(f"\n{'─'*60}")
    print("2. SUBJECT LINE QUALITY")
    print(f"{'─'*60}")
    no_subj = [e for e in all_emails if not (e.get('subject') or '').strip()]
    empty_by_step = Counter(e.get('step','') for e in no_subj)
    print(f"  Empty subjects: {len(no_subj)} ({len(no_subj)/total*100:.0f}%)")
    print(f"    By step: {dict(empty_by_step.most_common(8))}")

    fake_re = [e for e in all_emails
               if (e.get('subject') or '').startswith('Re:')
               and str(e.get('step','')).startswith('0_0_')]
    if fake_re:
        print(f"  ⚠️  'Re:' on first-touch steps: {len(fake_re)}")
        for e in fake_re[:5]:
            print(f"    {e.get('to_address_email_list','')} | '{e.get('subject','')}'")
    else:
        print(f"  ✅ No 'Re:' subjects on first-touch emails.")

    top_subj = Counter((e.get('subject') or '').strip() for e in all_emails if (e.get('subject') or '').strip())
    print(f"\n  Top 12 subjects by frequency:")
    for subj, cnt in top_subj.most_common(12):
        print(f"    {cnt}x: '{subj[:72]}'")

    # 3. Step quality + length
    print(f"\n{'─'*60}")
    print("3. SEQUENCE STEP QUALITY")
    print(f"{'─'*60}")
    step_dist = Counter(e.get('step','') for e in all_emails)
    print("  Step distribution:")
    for step, cnt in sorted(step_dist.items()):
        print(f"    {step}: {cnt}")

    bump_pat = re.compile(r'^(hi |hey |dear )?[a-z ]+?, ?(bumping|resurfacing|following up|circling back)', re.I)
    bumps = [e for e in all_emails if bump_pat.match((e.get('_body_text') or '')[:100])]
    print(f"\n  Empty bump emails (bumping/resurfacing with no value add): {len(bumps)}")
    for e in bumps[:5]:
        print(f"    {e.get('to_address_email_list','')} | step={e.get('step','')} | '{e.get('_body_text','')[:80]}'")

    length_by_step = defaultdict(list)
    for e in all_emails:
        lvl = str(e.get('step',''))[:3]
        wc = len((e.get('_body_text') or '').split())
        length_by_step[lvl].append(wc)

    print("\n  Avg word count by step level:")
    for lvl in sorted(length_by_step):
        ws = length_by_step[lvl]
        if ws: print(f"    {lvl}_x: avg={sum(ws)/len(ws):.0f}w, min={min(ws)}, max={max(ws)}, n={len(ws)}")

    over200 = [e for e in all_emails if len((e.get('_body_text') or '').split()) > 200]
    if over200:
        print(f"\n  ⚠️  Emails >200 words (too long for cold outreach): {len(over200)}")
        for e in over200[:5]:
            wc = len((e.get('_body_text') or '').split())
            print(f"    {e.get('to_address_email_list','')} | {wc}w | step={e.get('step','')}")
    else:
        print(f"\n  ✅ All emails under 200 words: appropriate length.")

    # 4. Sender persona analysis
    print(f"\n{'─'*60}")
    print("4. SENDER PERSONA DISTRIBUTION")
    print(f"{'─'*60}")
    persona_counts = Counter(get_persona(e.get('from_address_email','')) for e in all_emails)
    for p, cnt in persona_counts.most_common():
        print(f"  {p}: {cnt} emails ({cnt/total*100:.0f}%)")

    # 5. CTA calibration
    print(f"\n{'─'*60}")
    print("5. CALL-TO-ACTION DISTRIBUTION")
    print(f"{'─'*60}")
    cta_pats = {
        '15 minutes': re.compile(r'worth 15 min|15 minutes|15 mins', re.I),
        '20 minutes': re.compile(r'worth 20 min|20 minutes|20 mins', re.I),
        'quick call/chat': re.compile(r'quick call|quick chat', re.I),
        'worth a look': re.compile(r'worth a look', re.I),
        'open to': re.compile(r'\bopen to\b', re.I),
        'happy to show/share': re.compile(r'happy to show|happy to share', re.I),
    }
    cta_counts = Counter()
    for e in all_emails:
        body = e.get('_body_text','')
        matched = next((label for label, pat in cta_pats.items() if pat.search(body)), 'no clear CTA')
        cta_counts[matched] += 1
    for cta, cnt in cta_counts.most_common():
        flag = ' ⚠️' if cta == 'no clear CTA' and cnt/total > 0.3 else ''
        print(f"  '{cta}': {cnt} ({cnt/total*100:.0f}%){flag}")

    # 6. Competitive mentions
    print(f"\n{'─'*60}")
    print("6. COMPETITIVE / THIRD-PARTY MENTIONS")
    print(f"{'─'*60}")
    # Set these per client: the CRMs you integrate with (mark 'intentional') and named competitors.
    watch_terms = {
        'salesforce': 'CRM mentioned: intentional',
        'hubspot': 'CRM mentioned: intentional',
        'copilot': 'Ambiguous: could be confused with Microsoft Copilot',
        '<competitor name>': 'Direct competitor',
    }
    for term, note in watch_terms.items():
        hits = [e for e in all_emails if term in (e.get('_body_text','') or '').lower()]
        if hits:
            flag = ' ✅' if 'intentional' in note else ' ⚠️' if 'competitor' in note or 'Ambiguous' in note else ' ℹ️'
            print(f"  '{term}': {len(hits)} mentions{flag}: {note}")
            for e in hits[:2]:
                idx = e.get('_body_text','').lower().find(term)
                snip = e.get('_body_text','')[max(0,idx-30):idx+60].replace('\n',' ')
                print(f"    -> {e.get('to_address_email_list','')} | '...{snip}...'")

    # 7. Vertical distribution
    print(f"\n{'─'*60}")
    print("7. RECIPIENT COMPANY VERTICAL DISTRIBUTION")
    print(f"{'─'*60}")
    vert_dist = Counter()
    for e in all_emails:
        vert_dist[classify_vertical(e.get('to_address_email_list',''))] += 1
    for vert, cnt in vert_dist.most_common():
        flag = ''  # set per client, e.g. ' NOT CORE ICP' for verticals outside the ICP
        print(f"  {vert}: {cnt} ({cnt/total*100:.0f}%){flag}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: deep_analysis.py <emails_dir> <mcp_prefix>")
        print("  emails_dir: directory containing saved MCP result files")
        print("  mcp_prefix: e.g. 'mcp-<instance-id>'")
        sys.exit(1)
    emails_dir = sys.argv[1]
    mcp_prefix = sys.argv[2]
    emails = load_emails(emails_dir, mcp_prefix)
    print(f"Loaded {len(emails)} unique emails from {emails_dir}")
    analyze(emails)
