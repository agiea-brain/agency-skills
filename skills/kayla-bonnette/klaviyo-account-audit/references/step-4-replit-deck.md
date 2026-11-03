# Step 4: Replit deck prompt

Turns the final client-facing audit and proposal into a paste-ready Replit prompt that builds the full audit and proposal deck.

## Before running the prompt

- Confirm the client-facing audit and the proposal are both final and in this chat.
- Have the brand assets ready: logo URL, colours, fonts.
- Pick the proof to show: screenshots and data points from the internal audit's proof list.

## Prompt

```
Write a complete, paste-ready prompt for Replit to build a 15-20 slide presentation web app from
the final client-facing audit and proposal in this conversation. Please include:
- Slide-by-slide content in this order: Title, What we heard (their goals), The opportunity (number
  and how we got there), Key findings (one per slide, with proof), Scorecard, Quick wins,
  Recommendations, 30/60/90 plan, Investment, Additional services, Case studies, Next steps
- The exact headline and body copy for each slide, and which data, chart or screenshot goes where.
  Pull the Investment, Additional services and Case studies content from the final proposal
- Design direction: {brand assets: logo URL, colours, fonts}, clean modern layout, one idea per
  slide, large readable numbers, arrow-key navigation, export to PDF
- Clearly marked placeholders for screenshots and anything I need to add
```

## Output

A Replit prompt. Paste it into Replit, build the deck and add the screenshots. This is the deck you present to the client.
