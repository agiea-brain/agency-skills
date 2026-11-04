# Bright Data setup and tested behavior

## Connection and actions

Bright Data through the Composio connector (`brightdata` toolkit). Load `COMPOSIO_SEARCH_TOOLS` and `COMPOSIO_MULTI_EXECUTE_TOOL` with ToolSearch, then run a search for "scrape LinkedIn posts using brightdata" to confirm the connection is active. Actions used:

- `BRIGHTDATA_SCRAPE_LINKEDIN_POSTS` (fixed dataset `gd_lyy3tktm25m4avu764`)
  - People: `mode: discover_by_profile_url`, item fields `url`, `start_date`, `end_date`, `only_authored_posts`
  - Companies: `mode: discover_by_company_url`, item fields `url`, `start_date`, `end_date`
- `BRIGHTDATA_GET_SNAPSHOT_STATUS`, `BRIGHTDATA_GET_SNAPSHOT_RESULTS`

If Composio isn't connected or has no active Bright Data account, tell the user what to connect and stop. Never ask for an API token in chat or put one in a prompt, because scheduled task prompts are stored in plain text.

## Tested behavior

These came out of live test runs. They explain the shape of the procedure below.

- Runs take 1 to 2 minutes per batch. Use asynchronous mode and wait with a background `sleep 60` between status checks; synchronous calls tend to time out.
- Profile discovery without `only_authored_posts` also returns other people's posts the person engaged with (2 of 3 results in one test). Set it to true, and also drop any record whose `user_id` doesn't match the profile slug.
- A profile can fail with `dead_page` on one run and succeed on the next. Retry failed URLs once before reporting them.
- Full records include about 10 comments each. Pass `custom_output_fields` so the payload stays small.
- An empty result for a company usually just means it didn't post in the window. That's a normal outcome, not a failure.
