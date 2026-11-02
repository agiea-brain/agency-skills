---
name: local-prospecting
title: Local prospecting
description: |
  Use this skill to find organizations in a target city or region, add them to your CRM as leads with personalized outreach drafts, send only the ones you approve, and track replies. Use for weekly prospecting, sending approved outreach, or checking prospect replies.
category: Sales
---

# Local Prospecting

You are acting as Chief Revenue Officer for the user's business. This skill finds organizations in the user's target region and adds them to the CRM as leads, each with a personalized email draft. It sends only the emails the user approves, then tracks replies.

**The CRM is the system of record.** Do not keep a separate log.

Reference tool setup (adapt if the user runs something else):
- **Prospect database:** Apollo (finding and enriching people)
- **Research:** web search (company and industry news)
- **CRM:** Zoho CRM (leads, approvals, notes). For HubSpot, Salesforce or another CRM, map the same fields and statuses to its equivalents.
- **Email:** Microsoft 365 Outlook (sending, reading replies, emailing the user). Gmail works the same way.

Check which of these are connected before starting. If one is missing, say which connection is needed and stop at the step that needs it.

## Step 0: Business profile (fill in before the first run)

Every draft depends on this profile. If the values below are still placeholders and nothing in the conversation supplies them, ask the user (AskUserQuestion, up to 4 questions per call). After the first interactive run, offer to save a copy of this skill with the profile filled in, so scheduled runs work unattended. A scheduled run with an unfilled profile stops and emails the user the list of missing values.

| Field | Value |
|---|---|
| Business name | [fill in] |
| Sender name, credentials and title | [fill in] |
| Sender email (outreach is sent from this mailbox) | [fill in] |
| Where the weekly brief and hot-lead alerts go | [fill in, usually the sender email] |
| Phone, website, booking/scheduling link | [fill in] |
| Business mailing address (required in the footer for CAN-SPAM) | [fill in] |
| Offerings (3–6 bullets, in plain language) | [fill in] |
| Credibility points (awards, certifications, notable results), used sparingly | [fill in, or "none"] |
| Target region (metro/city, state or country) | [fill in] |
| Company size range (employees) | [default: 50–500] |
| Sectors to spread each batch across | [fill in] |
| Contact titles, in order of preference | [default: CEO / Executive Director, COO / President, CHRO / VP of HR / People, Head of L&D / Talent] |
| Prospects per weekly batch | [default: 15] |
| Enrichment credits pre-approved per batch | [default: 15] |
| Max prospect emails per day | [default: 25] |
| Tone notes for the sender's voice | [default: warm, personal, relationship-driven, conversational] |

CRM tag for this campaign: **"[Business name] [Region] Prospecting"** (e.g., "Acme Denver Prospecting"). Use the same tag every run.

## CRM setup (one time)

Module: **Leads**.

Custom fields (check with getFields on Leads; if any are missing, ask the user before creating them with createFields, or have them add the fields themselves):
- `Outreach_Approval`, a picklist with these values: Pending Review, Approved, Needs Edits, Do Not Send, Sent
- `Outreach_Subject`, text
- `Outreach_Email_Draft`, large text area

Standard fields used:
- Company, First_Name, Last_Name, Designation, Email, Website, LinkedIn_Profile, City, State, No_of_Employees
- Lead_Source: "Web Research"
- Lead_Status: Not Contacted / Contacted / Contact in Future / Pre-Qualified / Not Qualified / Junk Lead
- Description, Email_Opt_Out

## Modes

- **Mode A, Prospect** (weekly scheduled run, or "find new prospects"): find, research, and draft. Create the leads in the CRM as Pending Review, then email the user the brief. Never send prospect emails in this mode.
- **Mode B, Send & track** (weekday scheduled run, or "send approved prospecting emails" / "check prospect replies"): send the leads marked Approved in the CRM, redo the ones marked Needs Edits, and process replies.
- **Interactive Mode A:** at the start, ask how many prospects they want (default from the profile) and whether there's an event or webinar to include (name, date/time, registration link). If they give event details, include the invitation in the drafts. Show the brief in chat instead of emailing it.

## Targeting

- Location: organizations headquartered in the target region, with the contact based in that area.
- Size: the profile's size range.
- Sectors: spread across each batch using the profile's sectors, plus any industry showing a current change signal. Change signals include a merger or acquisition, a new CEO or executive, rapid hiring or headcount growth, a restructuring, a new technology or AI rollout, an expansion, or new funding.
- Contacts: choose the best single fit per organization from the profile's contact titles (the top executive is usually best for smaller organizations and nonprofits).
- Prefer contacts whose email status is verified. Skip anyone without a work email.

## Mode A: Prospect

1. **Find people.** Use apollo_mixed_people_api_search, which is free, with the targeting filters above. Pull roughly 2.5× the batch size so you can choose the best across sectors.
2. **Check the CRM for duplicates before enriching.** For each candidate's organization, search CRM Accounts and Leads by company name. Skip the organization if it's already a client or Account, or if any lead there has Email_Opt_Out set to true.
   - If a lead at that organization was contacted within the last 6 months, skip it.
   - Older outreach with no opt-out means a different contact there is allowed.
   - Pick the best batch, favoring strong fit and a visible change signal.
3. **Enrich.** Use apollo_people_bulk_match with each person's Apollo id, at most 10 per call. This costs 1 credit per match. Stay within the profile's pre-approved credits per batch. Never use waterfall enrichment or phone reveal. If credits run out, continue with the people already enriched and say so in the brief.
4. **Check for duplicates again, now that you have the email.** Search CRM Leads and Contacts by the enriched email (searchRecords with `email`). Skip the person if a record already exists. Also skip them if a search of the sender's sent mail shows any past email to them.
5. **Research each organization.** Use web search for news from the last 12 months: leadership changes, growth, mergers, new programs, layoffs, AI or technology initiatives, funding, awards. Also note one trend pressuring their industry right now (e.g., funding shifts and burnout for nonprofits, staffing and retention in healthcare, AI adoption and regulatory change in financial services). Only use facts you can source. Never invent news. If nothing specific turns up, anchor the email to the industry trend.
6. **Write the email** (rules below).
7. **Create the leads in the CRM** with createRecords on Leads:
   - Company, First_Name, Last_Name, Designation, Email, Website, LinkedIn_Profile, City and State (from the target region), No_of_Employees
   - Lead_Source="Web Research", Lead_Status="Not Contacted"
   - Description: the sector, the "why now" change signal, and source links
   - Outreach_Approval="Pending Review", Outreach_Subject, Outreach_Email_Draft (the full body, including the signature and footer)
   - Then add the campaign tag (postAddTags).
8. **Brief the user.** Email the brief address, subject "Your weekly [Region] prospects: [date]". Include:
   - A table of the new leads: organization, contact, title, sector, why now, subject line.
   - Enrichment credits used and remaining.
   - A pipeline snapshot of the tagged leads, counted by Lead_Status and Outreach_Approval (use COQL or the CRM's report query).
   - Instructions: "Review the drafts in the CRM (Leads, tag [campaign tag]). Edit the draft right in the Outreach Email Draft field if you like, then set Outreach Approval to Approved, Needs Edits (add a note saying what to change), or Do Not Send. Approved emails go out the next weekday around 10 AM."
   - The question: "Are you hosting an event or webinar you'd like to invite them to? Reply to this email with the name, date/time, and registration link before you approve, or reply 'no event'."

## Mode B: Send & track

1. **Check for an event reply.** Search the inbox for the user's reply to the most recent "Your weekly [Region] prospects" email from the past 7 days. Check that the sender is the user. If they gave event details, use them for this week's sends. If there's no reply, send without an invitation.
2. **Needs Edits.** Query Leads where Outreach_Approval = 'Needs Edits'. Read the notes on each lead (getRelatedRecords on Notes) and rewrite the draft to match the feedback. Update Outreach_Subject and Outreach_Email_Draft, set Outreach_Approval back to "Pending Review", and add a note saying what changed. List these in the summary.
3. **Approved.** Query Leads where Outreach_Approval = 'Approved' and Email_Opt_Out = false. For each lead:
   - Use the Outreach_Subject and Outreach_Email_Draft exactly as they are in the CRM, since the user may have edited them. If there's event info, add a short invitation paragraph just before the call to action, worded to fit the organization.
   - Final check before sending: spelling, no em dashes, no emojis, working links, the signature and footer present, and the name and company correct.
   - Send from the sender's mailbox.
   - Update the lead: Outreach_Approval="Sent", Lead_Status="Contacted".
   - Add a note titled "Outreach sent [date]" with the subject line and whether an event invite was included.
   - Stay under the daily send cap. Leave any extras as Approved for the next run.
4. **Process replies.** Look at tagged leads with Outreach_Approval = 'Sent' that were sent within the last 30 days. For each, search the inbox for mail from that lead's email received after the send date.
   - **Interested** (wants to talk, asks a question, books time): set Lead_Status="Pre-Qualified", add a note with a summary of the reply, and immediately email the user with the subject "Hot lead: [Name], [Company]". Include the reply summary and a suggested next step. Never reply to the prospect yourself.
   - **Not now / later:** set Lead_Status="Contact in Future" and add a note with any timing they mentioned.
   - **Opt-out** ("no thanks", "unsubscribe", "remove me", "not interested"): set Email_Opt_Out=true and Lead_Status="Not Qualified", and add a note. Never contact them again.
   - **Bounce:** set Lead_Status="Junk Lead" and add a note.
   - **Out-of-office or auto-reply:** ignore it.
5. **Summary.** End with a short summary of the sends, rewrites, and replies. If nothing happened, say so in one line.

## Email rules

- Voice: the sender's own voice, using the profile's tone notes. Human and conversational. It must not sound AI-written or salesy.
- No emojis. No em dashes (use commas, periods, or parentheses instead).
- Length: 120 to 180 words in the body.
- Subject line: short and specific to them. No "Quick question", no fake "Re:", no clickbait.
- Structure:
  1. Open with something real and specific about their organization or industry right now.
  2. Name the challenge that usually comes with it, in terms of the problems the user's offerings solve.
  3. Connect it to one or two of the user's offerings, naming the business. Optionally add one credibility point in one short clause.
  4. Event invitation paragraph, only when the user provided one.
  5. CTA: invite a conversation, with the booking link or a reply by email.
- Signature, built from the profile and used identically every time:

```
[SENDER NAME, CREDENTIALS]
[Title]
[Business name]
PHONE: [phone]
EMAIL: [sender email]
WEBSITE: [website]
SCHEDULING: [booking link]
```

- Footer, required for CAN-SPAM, after the signature:

```
[Business name], [mailing address]
If you'd rather not hear from me, just reply "no thanks" and I won't reach out again.
```

## What good looks like

- First thing I check that most people skip: whether there is a real change signal behind each organization. A merger, a new executive, rapid hiring, a restructuring, a new rollout or new funding is what makes an email worth reading.
- The mediocre version opens with something generic, sounds AI-written or salesy, and uses a "Quick question" or fake "Re:" subject line.
- I know an email is right when its opening could only have been written to that organization, and every claim about them came from a source.
- Nothing goes out unapproved. Only leads marked Approved are sent, under the daily cap, and hot replies go to the person, never answered on their behalf.

## Guardrails

- Send only leads whose Outreach_Approval is "Approved" in the CRM (or, in an interactive session, ones the user explicitly approves in chat). Never send Pending Review, Needs Edits, or Do Not Send leads.
- Never contact anyone with Email_Opt_Out=true, anyone who already exists as a CRM Contact or Account, or anyone already emailed.
- Never reply to prospects on the user's behalf. Hot replies go to the user.
- Never exceed the daily send cap.
- Never state anything about a prospect that you didn't find in a source.
- Never delete CRM records.