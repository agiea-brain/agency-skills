# DemandBird quirks

Each of these showed up while scheduling weekly LinkedIn posts through the MCP server.

## Time

- **Jitter.** Accounts can carry a default variance window around the scheduled time. `variance_minutes: 0` on `schedule_post` stores the exact time. Use a deliberate variance only when you want it.
- **Offsets.** Send `scheduled_at` with the offset that applies on that date (`-04:00` versus `-05:00` across a daylight-saving change). Keep the wall-clock time the human approved.

## Copy

- **Trailing newline.** The stored content drops a trailing newline. Treat that as the one allowed difference when comparing.
- **No voice pass.** Saving with `save_draft` stores your text verbatim. Drafting tools generate new copy; don't use them on approved text.
- **Mentions.** No person-mention (tagging) field turned up in the tools. Tag by hand after publishing if needed.

## Media

| Input | What happens | Do |
|---|---|---|
| PNG image | re-encoded to JPEG, dimensions kept | expect it; check it isn't cropped |
| PDF carousel | document title defaults to the filename | set `title` |
| large file | uploads around 100 MB worked | upload once, reuse the reference |

## First comments

- `save_draft` takes `first_comment: {text, delay_minutes}`.
- First comments are text only. A comment that needs an image has to be posted by hand.
- `get_post` doesn't return first comments, so the save acknowledgement is the only evidence before publishing. Check the live post afterwards.

## Rate limits

- A rejection carries no reset header, and the limit that applies to MCP calls isn't published.
- A batch that kept going after the first rejection wasted four calls and left drafts half-made.
- Pattern that works: one post at a time, stop at the first rejection, wait about a minute, run `list_scheduled_posts`, then continue only with posts that aren't there. Check drafts too: reuse a draft the failed call left behind rather than saving a second one.
- One read-back per post. Polling `get_post` spends the same budget.

## Token scope

A token scoped to create, edit, schedule and read was enough for this whole procedure. Leave out deletion, review decisions and channel management.
