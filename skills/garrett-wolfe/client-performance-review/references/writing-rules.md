# Writing rules: concise, dense, clean

## Tone: honest and positive
The review has to make the client want to keep going, and every line still has to survive their own check of the numbers.
- **Lead with what worked**, then the momentum (month over month: "October was our best reply rate yet"). Trend beats a total.
- **Frame a gap as upside with its fix**: "24 said book a call, 9 have booked, so converting the rest is the cheapest win", not "only 9 converted".
- **Give a learning as an asset**: "we now know who buys" is a result of the quarter, even when meetings are modest.
- **Turn an objection into a play**: name it, then the answer we'll run.
- **Name what didn't work plainly, once** (section 4), with what we take from it. Candour is what makes the positives believable.
- **Say "together" and "we"**, credit the client's part (events, the founder's posts), and make the asks about getting there faster.
- **Show continuity**: the system keeps running and stays in their stack, so next quarter starts at full speed.
- **Never inflate**: no rounding up, no unconfirmed meetings counted, no "huge" or "incredible". Write "we're excited" once at most and back it with a number.

## Prose
- Each section starts with one sentence stating its takeaway. The reader should be able to read only those sentences and get the review.
- Use numbers, not adjectives: "0 of 900", not "very few". Give one comparison per claim ("6x cold email").
- Short paragraphs, 1 to 3 sentences. Use bullets for parallel items, prose for reasoning.
- Name companies when it makes a pattern concrete ("one prospect sent their rate sheet"), never as filler.
- Define a term once, in a footnote line under the first table that uses it (`_..._` renders small and grey).

## Tables (why the Google Docs version looked cramped, and the fix)
The cramped look came from five things: no column widths, so Docs splits the page evenly and the long column wraps; two values in a cell ("32 (1.64%)"); long headers ("Replied (#, %)"); a border on every side of every cell; and coloured fills on every group.

- **At most 5 columns in the body, 6 in the appendix.** If you need more, split the table or make a chart.
- **One value per cell.** Pick the number the reader compares (usually the rate) and drop or move the count. If both matter, give them two columns.
- **Headers of 1 to 3 words.** Put units in the header ("Reply rate"), not in every cell.
- **First column is the label and the widest.** Set widths with `<!-- table: widths=34,14,14,14,24 -->` whenever the auto split wraps a label.
- **Numbers right-aligned** (the script does this) with the same decimals down a column: percentages to 2 places under 10%, 1 place above that.
- **A group or total row has every filled cell bold** (`| **Group A** | **1,200** | ...`); the script adds the fill and the rule. Do not colour-code rows.
- **At most about 12 rows in the body.** Show the top rows by the metric and send the rest to the appendix.
- Use an em dash for "none", never a blank cell. Give a table title only when the section heading doesn't already say it.

## Charts
- Draw a chart only when the shape is the point: the funnel, a rate by segment against the average, or a trend over months. Otherwise use a table.
- The **title is the takeaway** ("Smaller companies reply 5x more"), never the axis name.
- Use one accent colour on the bars that carry the point (`"highlight"`) and grey on the rest. Draw a dashed reference line for the average (`"ref"`).
- Label values directly on the bars; no gridlines on bar charts and no legends for a single series.
- Use at most 2 charts in the body; the rest go in the appendix.

## Length
- Body (sections 1-7): about 4 pages. Appendix: as long as the data needs, but every table there still follows the rules above.
- If a section has nothing to say this period, write that in one line. Don't pad.
