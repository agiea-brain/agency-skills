#!/usr/bin/env python3
"""
Instantly Campaign Email Auditor
Analyzes a batch of sent emails for variable rendering issues, copy quality problems,
and targeting anomalies. Takes the path to the saved MCP tool result file as input.

Usage:
    python3 audit_emails.py <path_to_emails_file>
    python3 audit_emails.py <path_to_emails_file> --limit 200

Output: Structured findings printed to stdout, grouped by issue type.
"""

import json
import re
import sys
import argparse
from html.parser import HTMLParser
from collections import Counter, defaultdict


# ─── HTML stripping ──────────────────────────────────────────────────────────

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []

    def handle_data(self, d):
        self._text.append(d)

    def get_text(self):
        return ' '.join(self._text).strip()

def strip_html(html_str):
    if not html_str:
        return ''
    s = HTMLStripper()
    try:
        s.feed(html_str)
        return s.get_text()
    except Exception:
        return html_str

def check_html_in_plain_text(plain_text):
    """
    Detect HTML tags that leaked into the RENDERED plain text: meaning the recipient
    would literally see '<div>' or '<br>' in their inbox. This is different from an
    HTML email having HTML in its source (which is fine).
    """
    # Only flag if the stripped plain text still contains literal tag syntax
    leaking = re.findall(r'<(?:div|br|p|span|b|i|u|a|ul|li|h[1-6]|strong|em)\b', plain_text, re.IGNORECASE)
    return leaking


# ─── Variable detection patterns ─────────────────────────────────────────────

# Templates still present (never rendered)
UNFILLED_PATTERNS = [
    re.compile(r'\{\{(?!RANDOM|accountSignature)[^}]{1,60}\}\}'),  # {{variable}}
    re.compile(r'\[(?:FIRST[ _]?NAME|LAST[ _]?NAME|COMPANY(?:[ _]?NAME)?|TITLE|EMAIL|PHONE|LINKEDIN)\]', re.IGNORECASE),
    re.compile(r'%[A-Z_]{2,30}%'),  # %VARIABLE%
    re.compile(r'\[\[.{1,30}\]\]'),  # [[variable]] style
]

# Soft failure: variable rendered to an empty or near-empty value
EMPTY_GREETING_PATTERNS = [
    re.compile(r'(?:Hi|Hey|Hello|Dear)\s*,'),               # "Hi ,": name was blank
    re.compile(r'(?:Hi|Hey|Hello|Dear)\s+\.\s'),             # "Hi . "
    re.compile(r'(?:Hi|Hey|Hello|Dear)\s+undefined\b', re.IGNORECASE),
    re.compile(r'(?:Hi|Hey|Hello|Dear)\s+null\b', re.IGNORECASE),
    re.compile(r'(?:Hi|Hey|Hello|Dear)\s+N/A\b', re.IGNORECASE),
    re.compile(r'(?:Hi|Hey|Hello|Dear)\s+\{\{'),             # template not stripped
]

# Only flag double-spaces that indicate a blank variable was dropped in, not
# normal phrases like "the portco" or "the team"
EMPTY_COMPANY_PATTERNS = [
    re.compile(r'\bat\s{2,}(?:\w)'),       # "at  company" (two+ spaces then a word)
    re.compile(r'\bfor\s{2,}(?:\w)'),      # "for  company"
    re.compile(r"^'s\b"),                  # starts with 's (company name was blank)
    re.compile(r'(?:at|for|of|with)\s+\'s\b'),  # "at 's team": blank name before apostrophe-s
]

# Generic/catch-all email prefixes that are almost never real decision-maker inboxes
GENERIC_EMAIL_PREFIXES = {
    'info', 'admin', 'contact', 'hello', 'support', 'noreply', 'no-reply',
    'help', 'sales', 'marketing', 'hr', 'team', 'office', 'careers',
    'jobs', 'webmaster', 'postmaster', 'mail', 'enquiries', 'enquiry',
    'hello', 'hi', 'service', 'billing', 'accounts',
}


# ─── Copy quality checks ─────────────────────────────────────────────────────

def check_empty_or_short(body_text):
    """
    Flag emails with suspiciously little content.
    Note: very short 'bump' emails (e.g. 'Bumping this up.') are common follow-up
    patterns: they're flagged here because they add no value, but that's a
    copywriting decision to surface rather than an outright bug.
    """
    word_count = len(body_text.split())
    if word_count == 0:
        return 'EMPTY body: no content at all'
    if word_count < 8:
        return f'NEAR-EMPTY body ({word_count} words): likely a bump step with no real value: "{body_text[:120]}"'
    return None

def check_subject_issues(subject, step):
    """Flag missing subjects on step 1 emails."""
    clean = (subject or '').strip()
    step_str = str(step or '')
    # Step identifiers for the first touch vary: check for common patterns
    is_first_step = (
        step_str in ('0_0_0', '0_0_1', '0_0_2', '1', 'step_1', '1_1') or
        re.match(r'^0_0_\d$', step_str) is not None
    )
    if not clean and is_first_step:
        return 'EMPTY subject on first-touch email: prospects have no reason to open this'
    if len(clean) < 3 and clean:
        return f'EXTREMELY SHORT subject: "{clean}"'
    return None

def check_truncation(body_text):
    """Detect copy that appears to trail off mid-sentence."""
    stripped = body_text.strip()
    if len(stripped) > 80:
        last_60 = stripped[-60:]
        # No sentence-ending punctuation in last 60 chars, ends mid-word
        if not re.search(r'[.!?]\s*$', stripped) and re.search(r'[a-z]{3,}$', stripped):
            # Exclude known short-form endings like CTAs
            cta_endings = ['let me know', 'open to chat', 'worth a look', 'happy to share',
                           'door is open', "door's open", 'reach out', 'pick this up']
            if any(stripped.lower().endswith(e) for e in cta_endings):
                return None
            # Exclude email signatures: after HTML stripping, signatures appear as plain text
            # and typically end with a company name or title (capitalized, no punctuation needed)
            sig_patterns = [
                re.compile(r'\b(?:Co-Founder|Founder|CEO|CTO|VP|President|Director)\s+[A-Z][a-z]+\s*$'),
                re.compile(r'Reply\s+"pause"', re.IGNORECASE),
                # Generic: last word is an all-caps abbreviation or TitleCase company name after a title
                re.compile(r'(?:Founder|CEO|President|Director)\s+[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)?\s*$'),
            ]
            if any(p.search(stripped) for p in sig_patterns):
                return None
            return f'POSSIBLE TRUNCATION: ends without punctuation: "...{last_60}"'
    return None

def check_name_mismatch(body_text, to_address):
    """
    Check if the name used in the greeting matches the recipient's email address.
    E.g., greeting says 'Hey Sarah' but email is john.smith@domain.com
    """
    if not to_address or '@' not in to_address:
        return None

    # Extract name from greeting (first word after Hi/Hey/Hello)
    greeting_match = re.match(r'(?:Hi|Hey|Hello|Dear)\s+([A-Z][a-z]{1,20})', body_text)
    if not greeting_match:
        return None
    greeting_name = greeting_match.group(1).lower()

    # Extract name components from email address
    email_prefix = to_address.split('@')[0].lower()
    # Normalize separators
    email_parts = re.split(r'[._\-]', email_prefix)
    email_parts = [p for p in email_parts if len(p) > 1]

    # If greeting name doesn't appear in any email name component, flag it
    if email_parts and not any(greeting_name in part or part in greeting_name for part in email_parts):
        # Only flag if the email looks like a personal address (first.last format), not a generic
        if len(email_parts) >= 2:
            return f'NAME MISMATCH: greeting says "{greeting_name}" but email is "{to_address}"'
    return None

def check_targeting_coherence(body_text, to_address, subject):
    """
    Flag obvious targeting mismatches where the email's premise doesn't fit the recipient.
    These are heuristic patterns: the LLM review pass catches more nuanced cases.
    """
    flags = []

    # Email talks about "portfolio companies" / "portcos" going to a non-PE domain
    # Common non-PE domains that end up in PE campaigns
    NON_PE_SIGNALS = ['morganstanley', 'goldmansachs', 'jpmorgan', 'bofa', 'citigroup',
                      'blackrock', 'fidelity', 'vanguard', 'mastercard', 'visa', 'amex']
    portco_mentions = re.search(r'\b(?:portco|portfolio compan|portfolio-level)\b', body_text, re.IGNORECASE)
    if portco_mentions and to_address:
        domain = to_address.split('@')[-1].lower() if '@' in to_address else ''
        for signal in NON_PE_SIGNALS:
            if signal in domain:
                flags.append(
                    f'TARGETING MISMATCH: email refers to "portcos/portfolio companies" but recipient is at {domain} (likely not a PE firm with software portcos)'
                )
                break

    # Email mentions "your firm" in a PE/fund context going to a corporate
    firm_context = re.search(r'\byour firm\b.{0,60}(?:portco|fund|investment|portfolio)', body_text, re.IGNORECASE)
    if firm_context and to_address:
        domain = to_address.split('@')[-1].lower() if '@' in to_address else ''
        for signal in NON_PE_SIGNALS:
            if signal in domain:
                flags.append(f'POSSIBLE TARGETING MISMATCH: "your firm" + PE context sent to {domain}')
                break

    return flags

def check_nonsensical_connections(body_text):
    """
    Flag sentences where the causal or logical connection seems broken.
    These are heuristic catches: a human should verify each one.
    """
    flags = []

    # "That signals X" where the antecedent is about a hiring action sent to a non-PE company
    that_signals = re.findall(r'That signals[^.]{10,100}(?:portfolio|portco)', body_text, re.IGNORECASE)
    for m in that_signals[:2]:
        flags.append(f'CHECK LOGIC: "That signals...portfolio" may not apply to this recipient: "{m.strip()[:100]}"')

    return flags

def is_generic_email(to_address):
    if not to_address or '@' not in to_address:
        return False
    prefix = to_address.split('@')[0].lower().strip()
    return prefix in GENERIC_EMAIL_PREFIXES

def check_opening_hook_repetition(first_sentence, seen_hooks, ctx):
    """
    Flag when the opening personalization line (the hook) is identical across emails.
    Template body copy WILL be the same: that's fine. But the hook should vary.
    """
    if len(first_sentence) < 20:
        return None
    normalized = re.sub(r'\s+', ' ', first_sentence.lower().strip())
    # Remove names/company names before comparing (so "Saw X hiring" == "Saw Y hiring")
    generic = re.sub(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b', 'NAME', first_sentence)
    generic_n = re.sub(r'\s+', ' ', generic.lower().strip())
    if generic_n in seen_hooks and len(generic_n) > 40:
        return f'HOOK NOT UNIQUE: same opening premise as another email in this batch: "{first_sentence[:80]}"'
    seen_hooks.add(generic_n)
    return None


# ─── Main analysis ────────────────────────────────────────────────────────────

def analyze_emails(emails):
    findings = defaultdict(list)
    seen_hooks = set()
    domain_counter = Counter()
    sender_domain_counter = Counter()
    step_counter = Counter()

    for i, e in enumerate(emails):
        if not isinstance(e, dict):
            continue

        email_id = e.get('id', f'email_{i}')
        to = e.get('to_address_email_list') or e.get('to_address') or ''
        frm = e.get('from_address_email') or e.get('eaccount') or ''
        subj = (e.get('subject') or '').strip()
        step = str(e.get('step', ''))
        ts = (e.get('timestamp_email') or e.get('timestamp_created') or '')[:10]

        body_obj = e.get('body') or {}
        raw_html = body_obj.get('html', '') if isinstance(body_obj, dict) else str(body_obj)
        body_text = strip_html(raw_html)

        step_counter[step] += 1

        ctx = f'[{ts}] step={step} | {frm} -> {to} | subj="{subj[:60]}"'

        # Track domains
        if '@' in to:
            domain_counter[to.split('@')[1]] += 1
        if '@' in frm:
            sender_domain_counter[frm.split('@')[1]] += 1

        # ── Variable rendering ──
        for pat in UNFILLED_PATTERNS:
            hits = pat.findall(subj + ' ' + body_text)
            if hits:
                findings['unfilled_variables'].append({
                    'ctx': ctx,
                    'issue': f'Unfilled template variable(s) still in email: {hits[:5]}',
                    'body_snippet': body_text[:200]
                })
                break

        for pat in EMPTY_GREETING_PATTERNS:
            m = pat.search(body_text)
            if m:
                findings['empty_name_greeting'].append({
                    'ctx': ctx,
                    'issue': f'Greeting rendered with empty/broken name',
                    'match': m.group(0),
                    'body_snippet': body_text[:150]
                })
                break

        for pat in EMPTY_COMPANY_PATTERNS:
            m = pat.search(body_text)
            if m:
                findings['empty_company_variable'].append({
                    'ctx': ctx,
                    'issue': 'Company name variable rendered blank',
                    'match': repr(m.group(0)),
                })
                break

        # ── Body quality ──
        empty_flag = check_empty_or_short(body_text)
        if empty_flag:
            findings['empty_or_short_body'].append({'ctx': ctx, 'issue': empty_flag})

        subj_flag = check_subject_issues(subj, step)
        if subj_flag:
            findings['subject_issues'].append({'ctx': ctx, 'issue': subj_flag})

        trunc_flag = check_truncation(body_text)
        if trunc_flag:
            findings['truncation'].append({'ctx': ctx, 'issue': trunc_flag})

        # HTML leaking into PLAIN TEXT (not just "has HTML in the HTML body")
        leaking_tags = check_html_in_plain_text(body_text)
        if leaking_tags:
            findings['html_leaking'].append({
                'ctx': ctx,
                'issue': f'HTML tags visible as literal text in rendered email: {set(leaking_tags[:5])}',
                'body_snippet': body_text[:200]
            })

        # ── Name mismatch ──
        name_mismatch = check_name_mismatch(body_text, to)
        if name_mismatch:
            findings['name_mismatch'].append({
                'ctx': ctx,
                'issue': name_mismatch,
                'body_snippet': body_text[:100]
            })

        # ── Targeting ──
        targeting_flags = check_targeting_coherence(body_text, to, subj)
        for f in targeting_flags:
            findings['targeting_mismatch'].append({'ctx': ctx, 'issue': f, 'body_snippet': body_text[:200]})

        nonsense_flags = check_nonsensical_connections(body_text)
        for f in nonsense_flags:
            findings['copy_logic_issues'].append({'ctx': ctx, 'issue': f, 'body_snippet': body_text[:300]})

        # ── Hook uniqueness (only check first-touch emails) ──
        is_first_touch = re.match(r'^0_0_\d$', step) or step in ('1', 'step_1')
        if is_first_touch and body_text:
            sentences = [s.strip() for s in re.split(r'[.!?]', body_text) if len(s.strip()) > 20]
            if sentences:
                hook_flag = check_opening_hook_repetition(sentences[0], seen_hooks, ctx)
                if hook_flag:
                    findings['non_unique_hook'].append({'ctx': ctx, 'issue': hook_flag})

        # ── Generic email address ──
        if is_generic_email(to):
            findings['generic_recipient_email'].append({
                'ctx': ctx,
                'issue': f'Sending to generic/role-based address: these almost never reply'
            })

    return findings, domain_counter, sender_domain_counter, step_counter


def print_findings(findings, domain_counter, sender_domain_counter, step_counter, total_emails):
    print(f"\n{'='*70}")
    print(f"EMAIL AUDIT RESULTS: {total_emails} emails analyzed")
    print(f"{'='*70}\n")

    severity_order = [
        ('unfilled_variables',       '🔴 CRITICAL: Unfilled Template Variables'),
        ('empty_name_greeting',      '🔴 CRITICAL: Empty Name in Greeting'),
        ('empty_or_short_body',      '🔴 CRITICAL: Empty or Near-Empty Email Body'),
        ('subject_issues',           '🟠 HIGH: Subject Line Issues'),
        ('targeting_mismatch',       '🟠 HIGH: Targeting Mismatch (Wrong ICP)'),
        ('name_mismatch',            '🟠 HIGH: Name in Greeting Doesn\'t Match Recipient'),
        ('html_leaking',             '🟠 HIGH: HTML Tags Visible as Literal Text'),
        ('empty_company_variable',   '🟠 HIGH: Company Name Variable Rendered Blank'),
        ('truncation',               '🟡 MEDIUM: Possible Truncated Copy'),
        ('copy_logic_issues',        '🟡 MEDIUM: Copy Logic to Review'),
        ('non_unique_hook',          '🟡 MEDIUM: Opening Hook Not Unique Across Emails'),
        ('generic_recipient_email',  '🟡 MEDIUM: Generic Recipient Email Addresses'),
    ]

    total_issues = sum(len(v) for v in findings.values())
    if total_issues == 0:
        print("✅ No programmatic issues detected. Proceed to manual copy review.\n")
    else:
        issue_types = len([k for k, v in findings.items() if v])
        print(f"Found {total_issues} flagged instances across {issue_types} issue type(s).\n")

    for key, label in severity_order:
        items = findings.get(key, [])
        if not items:
            continue
        print(f"\n{label} ({len(items)} instance{'s' if len(items)>1 else ''})")
        print('-' * 60)
        for item in items[:8]:
            print(f"  {item['ctx']}")
            print(f"  Issue: {item['issue']}")
            if 'match' in item:
                print(f"  Match: {item['match']}")
            if 'body_snippet' in item:
                snippet = item['body_snippet'][:200].replace('\n', ' ')
                print(f"  Body: {snippet}")
            print()
        if len(items) > 8:
            print(f"  ... and {len(items)-8} more\n")

    # Step distribution
    print(f"\n{'='*70}")
    print("STEP DISTRIBUTION")
    print('-' * 60)
    for step, cnt in sorted(step_counter.items(), key=lambda x: -x[1]):
        print(f"  step {step}: {cnt} emails")

    # Recipient domain breakdown
    print(f"\n{'='*70}")
    print("RECIPIENT DOMAIN BREAKDOWN (top 20)")
    print('-' * 60)
    for domain, cnt in domain_counter.most_common(20):
        print(f"  {domain}: {cnt} emails")

    # Flag if one domain dominates (potential targeting concentration risk)
    if domain_counter:
        top_domain, top_count = domain_counter.most_common(1)[0]
        pct = top_count / total_emails * 100
        if pct > 25:
            print(f"\n  ⚠️  CONCENTRATION WARNING: {top_domain} accounts for {pct:.0f}% of sends in this sample")

    print(f"\n{'='*70}")
    print("SENDING DOMAIN BREAKDOWN (top 15)")
    print('-' * 60)
    for domain, cnt in sender_domain_counter.most_common(15):
        print(f"  {domain}: {cnt} emails")


def main():
    parser = argparse.ArgumentParser(description='Audit Instantly sent emails for issues.')
    parser.add_argument('file', help='Path to the saved MCP tool result JSON file')
    parser.add_argument('--limit', type=int, default=None, help='Max emails to analyze')
    args = parser.parse_args()

    with open(args.file) as f:
        raw = json.load(f)

    # Handle the nested structure from the MCP file format: {result: "<json string>"}
    if isinstance(raw, dict) and 'result' in raw:
        inner = json.loads(raw['result'])
    else:
        inner = raw

    if isinstance(inner, dict):
        emails = inner.get('items', [])
    elif isinstance(inner, list):
        emails = inner
    else:
        print(f"Unexpected data structure: {type(inner)}")
        sys.exit(1)

    if args.limit:
        emails = emails[:args.limit]

    findings, domain_counter, sender_domain_counter, step_counter = analyze_emails(emails)
    print_findings(findings, domain_counter, sender_domain_counter, step_counter, len(emails))


if __name__ == '__main__':
    main()
