# Scheduled task prompt template

Fill in the braces and pass this as the scheduled task prompt. It runs in a fresh session with no memory of setup, so it carries everything.

```
Produce my LinkedIn watchlist brief for the 24 hours ending now. Output it as a chat message in this session. Do not email it or create a file.

Tools: Composio (load COMPOSIO_SEARCH_TOOLS and COMPOSIO_MULTI_EXECUTE_TOOL via ToolSearch). Bright Data actions: BRIGHTDATA_SCRAPE_LINKEDIN_POSTS, BRIGHTDATA_GET_SNAPSHOT_STATUS, BRIGHTDATA_GET_SNAPSHOT_RESULTS.

Watchlist: {EMBEDDED LIST or "read Google Sheet {SHEET_ID}, tab {TAB}, columns url/name/type"}

What I care about: {FOCUS}

Procedure:
1. Use the current UTC time from the Composio response. Window = now minus 24 hours to now, ISO 8601 with Z.
2. Trigger two asynchronous BRIGHTDATA_SCRAPE_LINKEDIN_POSTS runs in one multi-execute call, both with limit_per_input {CAP}, include_errors true, format json, execution_mode asynchronous, custom_output_fields "url|user_id|user_name|account_type|date_posted|post_type|post_text|headline|num_likes|num_comments|discovery_input":
   - mode discover_by_profile_url, one item per person: url, start_date, end_date, only_authored_posts true
   - mode discover_by_company_url, one item per company: url, start_date, end_date
3. Wait with a background `sleep 60`, then check BRIGHTDATA_GET_SNAPSHOT_STATUS for both. Repeat until ready or failed (max 20 minutes). Fetch with BRIGHTDATA_GET_SNAPSHOT_RESULTS.
4. Retry any URL that errored (for example dead_page) once in a second batch.
5. Keep only records dated inside the window whose user_id matches the input slug.

Brief format (Markdown, plain direct tone, no em dashes, no exclamation points):
- Title: "LinkedIn brief, {date}: {N} posts from {M} accounts"
- Worth engaging (top 3 max): who, one line on why it matters given what I care about, link. Skip if nothing qualifies.
- People: one block per person who posted. Per post: 1 to 2 sentence summary in your own words, link, likes and comments.
- Companies: same structure.
- Footer: count of quiet accounts, then any URLs that still failed after retry, with the reason.
- If nobody posted, one line saying so.

Summarize rather than quote. Never invent fields that weren't returned. Read-only on LinkedIn. Send the brief with SendUserMessage, then stop.
```
