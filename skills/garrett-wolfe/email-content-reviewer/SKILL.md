---
name: email-content-reviewer
title: Sent cold email content review
description: |
  Use this skill when an agency needs to QA every cold email a client campaign
  has actually sent: names and company names rendering correctly, variables
  filled, message coherence, pitch accuracy, ICP fit, signal-to-message
  alignment, sender and signature consistency, CTA calibration and
  cross-campaign duplication. Produces findings tagged by severity and fix
  location with a prioritized action list. Also use for "review our emails",
  "QA our outbound", "are our emails going out correctly".
category: Sales
tags: [cold-email, qa, outbound, deliverability, data-quality]
tools: [instantly, clay]
---

# Email Content Reviewer

A thorough, line-by-line quality review of every cold outbound email sent from an Instantly instance. This skill covers both programmatic checks (scripts that run across all emails) and qualitative LLM review (reading each email as a human would).

**What this skill produces:**
- Issues tagged by severity: CRITICAL (broken/wrong), NOTABLE (suboptimal), PATTERN (systemic)
- Every finding tagged with fix location: Instantly template, copy generation, or upstream data/enrichment
- A prioritized action list

**Script paths:** `references/`: use the base directory shown in the system message when this skill loads.

---

## Step 0: Identify the Right MCP Instance

If multiple Instantly MCPs are connected, identify the right one before pulling data:
- Call `list_campaigns` (limit 5) on each MCP
- Look at campaign names and sending addresses to match the client the user named
- Use that MCP exclusively for the rest of the review

---

## Step 1: Pull All Sent Email History

**This requires pagination.** Do not stop at one page.

```
1. Call list_emails(email_type=sent, limit=100, sort_order=asc)
2. Save the result file path from the token-limit error
3. Extract next_starting_after cursor from the file
4. Pull next page using that cursor
5. Repeat until next_starting_after is null
```

Each page will be saved as a separate file. Collect all file paths.

**Also pull by campaign** for any campaign where chronological pagination may have gaps:
- Call list_emails(email_type=sent, limit=100, campaign_id=<id>) for each active campaign
- This catches any emails that may have been skipped in chronological ordering

After pulling, merge all files into a single deduped corpus:

```python
import json, glob
from html.parser import HTMLParser

class Strip(HTMLParser):
    def __init__(self): super().__init__(); self.r = []
    def handle_data(self, d): self.r.append(d)
    def text(self): return ' '.join(self.r).strip()

def strip(html):
    s = Strip(); s.feed(html or ''); return s.text()

files = glob.glob('<tool_results_dir>/mcp-<instance_id>-list_emails-*.txt')
all_emails = []; seen = set()
for fname in files:
    raw = json.load(open(fname))
    inner = json.loads(raw['result'])
    for e in inner.get('items', []):
        if e.get('id') not in seen:
            seen.add(e['id'])
            body_obj = e.get('body') or {}
            html = body_obj.get('html','') if isinstance(body_obj, dict) else str(body_obj)
            e['_body_text'] = strip(html)
            all_emails.append(e)

print(f"Total unique emails: {len(all_emails)}")
json.dump(all_emails, open('/tmp/all_emails.json','w'))
```

**Coverage check:** Compare total emails loaded against `emails_sent_count` from `get_campaign_analytics`. If coverage is below 85%, pull additional pages from specific date ranges or campaigns where you have gaps.

---

## Step 2: Programmatic Analysis (Run Both Scripts)

```bash
# Script 1: Copy quality: variables, subjects, targeting
python3 references/audit_emails.py /tmp/all_emails_as_mcp_file.txt

# Script 2: Structural analysis: duplicates, steps, CTAs, verticals, competitive
python3 references/deep_analysis.py <tool_results_dir> <mcp_instance_id_prefix>
```

The scripts output findings directly. Note every flagged item: these become entries in the final report.

---

## Step 3: LLM Content Review in Chunks

The programmatic scripts catch structural issues. This step catches meaning-level problems that require reading comprehension.

Split the emails into chunks of ~300 and review each chunk. For each email read:

### 3a. Name Quality

Does the first name used in the greeting look like a real, properly capitalized human name?

**Flag:**
- All-lowercase or all-uppercase (e.g., "DAVID", "michael")
- Initials used as first name ("Ck", "Jc", "Tj", "Lj")
- Middle initial leaked into greeting ("Hey Austin X,", "Hi Raymond T,")
- Full name instead of first name ("Hi John Smith,")
- Last name used as first name: check if the email username format is `lastname.firstinitial@` or similar
- Numeric characters in name ("John2", "3Smith")
- Name clearly doesn't match the recipient's email address in an obvious way (e.g., "Hi Sarah" going to john.smith@company.com when no nickname is plausible)

### 3b. Company Name Quality

Is the company name referenced in the email accurate and formatted correctly?

**Flag:**
- Legal entity suffixes left in: "Acme Fluid Systems Pty Ltd", "Northwind Electric Mfg. LLC"
- Initialisms lowercased: "Ibm" for IBM, "Amd" for AMD
- Parent holding company used instead of operating brand: a holding group's name where the prospect knows only the trading brand
- Wrong company entirely: the company name doesn't match the email domain in any recognizable way
- LinkedIn artifacts: year founded, location code, or division appended ("Acme 1898 QC-CA", "Northwind Marketing Group NMG")
- Two brands concatenated: "Acme Northwind"

### 3c. ICP Fit

Does this person's company actually need what the product does?

State who the product is for, then list who it is not for. Example, for a product built for teams with field sales reps who visit customer sites, flag:
- Pure software/SaaS companies (no physical territory reps)
- Financial services (inside sales or institutional, not field)
- Educational institutions or nonprofits
- Staffing and consulting firms
- E-commerce / DTC companies

Write this list per client from their product description before reviewing.

### 3d. Signal-to-Message Alignment

If the campaign targets a specific signal (new hire, promotion, job posting, product launch, M&A), does the email opening correctly reference that signal for this specific recipient?

**Flag:**
- Opening claims a signal that doesn't plausibly apply to this company (e.g., "I saw your firm just went through an M&A" for a small specialty manufacturer with no recent M&A activity)
- The signal is real but the wrong person is being contacted (e.g., a promotion signal triggered outreach to the wrong person who didn't get promoted)
- The opening references an event that happened to a parent company and is being attributed to a subsidiary

### 3e. Message Coherence

Read the email as the recipient would. Does it make sense from start to finish?

**Flag:**
- The opening hook does not connect to the pitch ("Saw you're growing the team" → completely generic pitch that ignores the growth context)
- Non-sequitur sentences: a sentence with no logical connection to the one before it
- The same social proof example appears in step 1, step 2, and step 3 with no variation (the same customer story in every step with no new angle)
- Broken causality: "Because you're scaling, our platform helps with admin": the causal connection is asserted but not explained
- Bump follow-ups with zero added content ("Bumping this up." alone)
- The CTA doesn't match the premise (email about scaling headcount → CTA is "worth 15 minutes to see if we can help with CRM data?": the ask doesn't connect to the headcount theme)

### 3f. Product Description Accuracy

Is the product described correctly? Check against what you know about the actual product.

List the product's core facts and cleared proof points, then flag:
- Pre-launch language ("we're building X") when the product is live with customers
- Stats not in the cleared proof point set (verify or remove)
- A customer's name written incorrectly
- A vague description ("AI platform") with no specific mechanism
- ROI math applied to a company where its assumptions are clearly unrealistic (for example, 100 reps at a 10-person company)

Build this list per client from their product documentation before reviewing.

### 3g. Sender/Signature Consistency

Does the email's from address match the person signed at the bottom?

**Flag:** Any email where the sender's email domain/username clearly belongs to Person A but the closing signature says "Person B, Title, Company."

Note: When checking this, be careful not to confuse the recipient's first name (which may appear in the greeting) with a signature name. Only flag when the *closing* signature is clearly a different person from the *sending* account.

---

## Step 4: Cross-Reference and Synthesize

After all chunks are reviewed:

1. **Deduplicate findings**: the same broken template variant will appear on many emails. Report it once with a count ("affects N emails across campaign X").

2. **Assign fix locations:**
   - **Instantly**: template configuration errors, empty step variants, step settings
   - **Copy generation**: outdated language, wrong product descriptions, unverified stats, copy that was generated incorrectly
   - **Upstream data/enrichment (Clay etc.)**: wrong company names, ICP mismatches, name formatting errors, wrong company matched to contact

3. **Prioritize by impact:**
   - CRITICAL: Broken emails landing in inboxes (empty body, wrong company name for a competitor, completely wrong recipient)
   - NOTABLE: Suboptimal but not harmful (bumps with no content, slightly off company name)
   - PATTERN: Systemic issue affecting many emails (pre-launch language, ROI math not scaled)

---

## Step 5: Report Format

```
# [Client] Email Content Review
Date: [today]
Emails reviewed: [N] (covering [date range])
Coverage: [N]% of all-time sends

## Critical Issues
[Numbered. For each: what's wrong, recipient example, exact quote, count affected]

## Issues by Category

### Names
[List each issue type with count and examples]

### Company Names
[List each issue type with count and examples]

### ICP Fit
[Which verticals/titles are out of scope, with counts]

### Copy Coherence & Pitch Accuracy
[Specific examples of broken sentences, wrong stats, pre-launch language]

### Structural (Steps, CTAs, Sender Consistency)
[From script output: step distribution, CTA breakdown, duplicates]

## Fix Location Summary

### Fix in Instantly
[Specific campaigns, step numbers, what to change]

### Fix in Copy Generation
[Template text to update, stats to verify or remove]

### Fix in Upstream Data (Clay / enrichment)
[Filters to add, normalization rules, ICP criteria]

## Priority Action List
### Do immediately
### Do this week
### Monitor going forward
```

---

## What good looks like

- Coverage is at least 85% of all-time sends before drawing conclusions, and small samples (under 50 sends) are labeled as such.
- The same broken template is reported once, with a count of the emails it affects.
- Every finding carries a severity and a fix location: the sending tool, copy generation, or upstream data.
- Red flag: an email that passes every structural check but does not make sense read start to finish. Read each one as the recipient would.

## Notes on Scope

- This skill reviews **sent** emails: what actually went out to prospects. It will not catch issues in draft campaigns or sequences that haven't fired yet.
- For campaigns that just launched (<50 emails sent), note the sample size and flag that findings may not be representative.
- The LLM review step requires actual judgment: reading each email as a thoughtful human would. Do not rush it. An email that looks fine structurally can still have a logical disconnect that only reveals itself when read naturally.
- When in doubt about whether a company name issue is from the wrong source or just a legitimate alternate name, check the email domain against the company name. If they don't obviously match, flag it.
