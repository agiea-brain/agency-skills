---
name: facilitator-notes
title: Facilitator notes
description: |
  Use this skill to standardize, write or enhance facilitator notes in any training slide deck (.pptx): standard section names and format, Agenda/Conclusion slides aligned to key messages, Workbook or handout page references.
category: Operations
---

# Facilitator Notes

Use this skill for any training deck (PowerPoint) when the user wants its facilitator notes formatted, standardized, written or improved. If the user has a reference deck whose notes they consider the gold standard, ask for it and match its style; otherwise use the standard below.

The deliverable is the same .pptx with updated speaker notes, plus updated Agenda and Conclusion slides. Work on a copy, and keep the original file name without a "(1)"-style suffix. Leave every other slide's visible content, layout, images, animations and media alone.

## Steps

1. **Inventory the deck.** Use python-pptx to read every slide's visible text and its notes. Also render the slides to images (LibreOffice to PDF, then to PNG) so you can see what each slide shows, including images, diagrams and how it builds.
2. **Find the participant material.**
   - If a Workbook is attached, read it and map each slide to its Workbook page(s).
   - If there's no Workbook but there are handouts, map slides to the handouts by name (and page or section if it has them). Use a **HANDOUT** section in place of **WORKBOOK**.
   - If neither is attached, use any page references already in the notes or on the slides. Ask the user for the Workbook or handout only if there are no references at all. If they aren't there to ask, write the notes without page numbers and list the gaps at the end.
   - Never invent a page number.
3. **Identify the key messages.** Find the 3–4 core messages the deck teaches. Pull them from the content slides, not from the old agenda.
4. **Update the Agenda slide.**
   - Rewrite the agenda items so they reflect the deck's real sections and key messages, in the order they're taught.
   - Keep the slide's existing layout, number of text boxes, fonts and styling. Edit only the text runs.
   - If the number of items has to change, say so rather than redesigning the slide.
5. **Update the Conclusion slide.**
   - Rewrite the takeaways so they restate the same key messages as the agenda, as one-line, action-oriented statements.
   - Same rule: change text only and keep the formatting.
6. **Write or improve the notes for every slide.**
   - **No notes:** write complete notes in the standard format below.
   - **Existing notes:** keep the author's content and voice. Fix the format and section names, then improve the notes. Add missing sections (especially SUGGESTED TIME, PURPOSE, TRANSITION and the WORKBOOK/HANDOUT reference). Make vague points concrete, add an ASK where the room should talk, and check that every TRANSITION leads into the next slide.
   - Make sure the timings roughly add up to the session length. If a total is stated, note it on slide 1.
   - When the Agenda or Conclusion slide changes, update its notes to match.
7. **Check the work.**
   - Re-open the saved file and dump all the notes.
   - Check that every section title is from the standard list (or is a slide-specific content heading).
   - Check that each Workbook or handout page cited matches the material.
   - Check that no original content was lost unless you deliberately rewrote it.
   - Render the Agenda and Conclusion slides and look at them to confirm nothing overflows.
8. **Deliver.**
   - Send the .pptx.
   - Give a short summary covering what changed on the Agenda and Conclusion slides, which slides got new notes and which got improved notes, and any gaps such as missing page references.

## Standard section names

Use only these names, in roughly this order. Use just the sections a slide needs.

| Section | Use for |
|---|---|
| **SUGGESTED TIME** | Always first. Minutes, plus a note in parentheses if helpful. |
| **WORKBOOK** (or **HANDOUT**) | Page number and title, and what participants do on it. |
| **SLIDE BUILD** | Animations or clicks, and video cues or links. If there's no animation, say "No animations. Everything appears at once." |
| **PURPOSE** | One or two sentences on why the slide exists. |
| **KEY MESSAGE** | The one idea participants must leave with. |
| **SAY** | Scripted lines in quotes. |
| **TALKING POINTS** | Points to cover, in the facilitator's own words. |
| **ASK** | Questions for the room. |
| **ACTIVITY** | An exercise (pairs, tables or individual), with timing. |
| **HOW TO RUN IT** | Step-by-step setup and instructions for an activity. |
| **DEBRIEF** | Questions and points for after an activity. |
| **FACILITATOR TIP** | Advice for the facilitator: watch-outs and coaching tips. |
| **ACCOUNTABILITY** | Accountability partners and sharing commitments. |
| **RECAP** | Summary of the takeaways (Conclusion slide). |
| **CALL BACK** | A link back to the opener or something said earlier. |
| **CLOSE** | Final words, thanks, evaluations and next steps. |
| **TRANSITION** | Always last (except on the final slide). A quoted bridge line into the next slide. |

**Other headings that are allowed:**
- BEFORE THE SESSION, for prep and tech checks.
- ATTRIBUTION, for model or research credits.
- CONNECT TO … , for example CONNECT TO THE MODEL or CONNECT TO THE SERIES.
- Headings that are part of one slide's content, such as WALK THE CURVE, PART 1: …, or a model's stage names.

**Map old names to the standard ones:**
- Ask the Room, Key Question, Closing Question, and Facilitate (when it's a question) → ASK
- Instructions, Setup, Do (activity setup) → HOW TO RUN IT. Merge Setup and Instructions when they're back to back.
- Group Activity, Activity Option, Practice Option, and Facilitate (when it's an exercise) → ACTIVITY
- Facilitator Tips, Facilitator Note, Coaching Tip → FACILITATOR TIP (always singular)
- Key Points, Points to Highlight, Key Teaching Points → TALKING POINTS
- Key Point → KEY MESSAGE
- Key Takeaways → RECAP
- Share (with accountability partners) → ACCOUNTABILITY
- Logistics, and Do (at the end) → CLOSE
- Debrief Questions → DEBRIEF
- Slide Advance, Video Cues, Link → SLIDE BUILD

Details go in parentheses after the name, in lowercase, e.g. **ASK (quick opener)**, **ACTIVITY (optional, 2–3 minutes)**, **DEBRIEF (pairs or whole group)**.

## Notes format

Every deck must match this exactly:

- **Section title:** in caps, bold, on its own line, with no colon. The section's content starts on the next line.
- **Spacing:** exactly one blank line between sections, and none at the start or end.
- **Bullets:** main points are plain lines with no bullet. Sub-items go on indent level 1 and start with "• ", or with "1. " when they're numbered steps.
- **Bold:** only section titles are bold. Body text is never bold.
- **Font:** no font size or font name set on the runs. Let the notes master's defaults apply.
- **No title line:** don't add a "SLIDE N – Title" line at the top of the notes.
- **Writing style:**
  - Use a warm, practical, plain-language facilitator voice (or the deck author's voice, if their existing notes show one).
  - Put scripted lines in straight quotes.
  - Use en dashes for ranges ("5–7 minutes").
  - Don't use em dashes. Use colons or periods instead.

Example:

```
SUGGESTED TIME            (bold)
8–10 minutes

WORKBOOK                  (bold)
Page 2: Transition Model. Ask participants to note what each phase looks like on their team.

KEY MESSAGE               (bold)
A well-managed transition shortens the productivity dip.

TALKING POINTS            (bold)
Walk through the three phases:
    • Endings: ...        (level 1)
    • Neutral Zone: ...   (level 1)

ASK                       (bold)
"Where is most of your team right now?"

TRANSITION                (bold)
"Let's look at what gets in the way."
```

## What good looks like

- First thing I check that most people skip: where the key messages actually come from. They get pulled from the content slides, not the old agenda, and then the Agenda and Conclusion slides are rewritten to match them.
- The mediocre version adds notes slide by slide and never checks that the timings add up to the session length, or that every TRANSITION actually leads into the next slide.
- I know it is right when a facilitator who has never seen the deck can run the room from the notes alone, and every Workbook or handout page cited matches the material.
- Never invent a page number. If the reference is missing, write the notes without it and list the gap.

## How to write the notes (python-pptx)

Rebuild each notes text frame paragraph by paragraph. Don't append to the existing text.

```python
from lxml import etree
A='http://schemas.openxmlformats.org/drawingml/2006/main'; q=lambda t:'{%s}%s'%(A,t)
def p_el(text=None, bold=False, lvl=0):
    p=etree.Element(q('p')); ppr=etree.SubElement(p,q('pPr'))
    if lvl: ppr.set('lvl',str(lvl))
    if text is not None:
        r=etree.SubElement(p,q('r'))
        if bold: etree.SubElement(r,q('rPr')).set('b','1')
        etree.SubElement(r,q('t')).text=text
    return p
# body = slide.notes_slide.notes_text_frame._txBody
# remove all <a:p>, then append: heading p_el(h,bold=True), content p_el(t,lvl=...), blank p_el() between sections
```

Before rewriting a notes frame, check whether it has hyperlinks or several runs in one paragraph, and keep those runs if so.

To edit the Agenda and Conclusion slides, replace the text in the existing runs (`run.text = ...`) so the formatting stays the same. Don't delete and re-add shapes.