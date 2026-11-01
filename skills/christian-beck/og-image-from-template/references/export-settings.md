# Export, naming and the pre-ship check

## Dimensions

1200x630, which is 1.91:1. One size covers every platform that matters, because they all crop from this ratio rather than demanding their own.

| Platform | What it does with 1200x630 |
|---|---|
| LinkedIn | Shows it close to full |
| Facebook | Shows it close to full |
| X | Full width on `summary_large_image` |
| Slack, iMessage, WhatsApp | Scales it down hard. This is the thumbnail case that decides legibility. |

Do not ship a square variant unless something in the stack demands one. A second size is a second thing to keep in sync.

## Safe area

Keep text inside the central 80%, so 120px of margin left and right, 63px top and bottom. Crops bite the edges, and a title that ends flush to the frame loses its last word somewhere.

## Format and weight

| Content | Format | Ceiling |
|---|---|---|
| Type, flat color, vector shapes | PNG | 300KB |
| Photo or screenshot background | JPG at quality 80 | 300KB |

Over 300KB, some crawlers skip the fetch and the card renders with no image at all, which is worse than a plain one. If a PNG lands over the ceiling, it is photographic and should have been a JPG.

## Naming

`og-<page-slug>.png`. After the slug, never the title.

Titles get rewritten; slugs do not. A file named after a title becomes a lie the first time someone edits the heading, and nobody renames the file.

## The pre-ship check

Four things, in order, before the page goes live:

1. **The tag is right.** `og:image` points at an absolute URL, not a relative path. This is the single most common failure and it produces a blank card.
2. **The crawler can reach it.** Not behind auth, not on a staging host, not blocked in robots.
3. **The card renders.** Paste the live URL into a share-preview tool and look at the actual card, not the file.
4. **It reads at thumbnail.** Zoom the preview to 25%, or just look at it on a phone. If the title is not readable, nothing else matters.

## When a card will not update

Platforms cache aggressively. After replacing an image, the old one keeps showing. Re-scrape through the platform's own debugger rather than shipping a second file with a different name, because the second file leaves the first one live and cached somewhere forever.
