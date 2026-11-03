# Connectors and fallbacks

The skill ships no server configuration. Connect these yourself; the skill degrades in a defined order rather than failing.

| Tool | Role | Without it |
|---|---|---|
| **A browser connection** (for example a Chrome extension your agent can drive) | Primary collection path: browsing subreddits and reading threads with comments | Falls back to `old.reddit.com`, then `.json` thread endpoints, then web search. Slower, and comment trees come back less complete. |
| **A bulk scraping tool** (for example a local scraping MCP server) | Bulk collection when a client needs volume beyond hand-browsing | Collection stays manual. Fine for most engagements; noticeable on wide multi-subreddit sweeps. |
| **Web search** | Last-resort fallback and competitor checks | The purple-cow test's "unclaimable by competitors" step needs manual verification. |

Browser extensions and local servers are per-machine setups, not something the skill can carry. If neither is connected, the skill says so in one line and continues on the fallbacks instead of stalling.

## Fallback order

When the browser stalls or a thread won't render:

1. `old.reddit.com` for the same URL
2. Append `.json` to the thread URL
3. Bulk scrape or search through a scraping tool
4. Web search with `site:reddit.com`

If no browser is connected at all, say so in one line and switch. Don't retry it.

## Giving it enough up front

Give it as much as you have and it asks less:

> Research Reddit marketing for acme.com. The claim to test is on their materials page, start in r/example and r/example2, we're targeting $100 per email signup, both organic and ads.

## Changing the house defaults

The skill separates house defaults (the 9:1 comment ratio, the minimum corpus size, the one-wedge rule, the recency window) from hard rules (cite everything, quote verbatim, never invent a metric, roadmap after corpus, disclosure always explicit).

Defaults are adjustable per engagement, as long as the deliverable says they were adjusted. To change them for a whole team, edit the "House defaults vs. hard rules" section of the skill. The hard rules are not adjustable.
