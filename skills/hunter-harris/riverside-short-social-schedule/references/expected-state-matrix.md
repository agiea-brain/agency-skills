# Expected-state matrix

Build this before the first write, and check every row against it after read-back.

## Columns

| Column | Example | Check |
|---|---|---|
| clip | short-3 | the edit ID and revision you approved, not a later edit |
| type | Short, 9:16 | dimensions match the platform |
| platform | YouTube, TikTok, Instagram | one row per platform |
| account | the connected account's ID | from `social_get_connected_platforms`, not typed |
| title | YouTube only | equals the approved title |
| caption | full text | equals the approved caption; carries the full-episode link |
| visibility | public | as approved |
| local time | Tue 14:00 America/New_York | the approved slot |
| UTC time | 19:00Z | converted for that date, not this week's offset |
| render settings | `composeSettings: {}` | present on create |
| approval | who approved, and when | present before any write |
| status | not attempted, unknown, failed, verified | updated as each write returns |

## The create call

`social_upload_create` takes the studio ID, platform, platform account ID, the clip (edit) ID, `scheduledAt` in UTC, `composeSettings`, and one platform block (`youtubeData`, `tiktokData` or `instagramData`) with the title, caption and visibility.

## Statuses after each call

| State | Meaning | Next |
|---|---|---|
| not attempted | nothing sent | create |
| unknown | sent, no clear answer | read the schedule once; if absent, stop and ask; never resend blind |
| failed | Riverside refused | confirm no upload exists, fix the cause, then create |
| verified | read back and matching | done |

## Known refusals and surprises

- **"Clip is not exported yet (status: draft)"** on a clip that was exported: `composeSettings` was missing from the create.
- **Create says "waiting for greenlight", read-back says "scheduled".** Normal. Trust the read-back.
- **Wrong attachment on a scheduled post.** Prepare the corrected export, then replace the attachment in place, keeping the post, copy and time.
- **The hour is off by one.** The UTC conversion used the wrong side of a daylight-saving change.
- **Rate limited.** Another session was calling the same account. One caller at a time.

## Removing a post

In Riverside's planner, "Remove schedule" only unschedules the post. A permanent delete is the separate "Remove post" action. Do it only with explicit approval, and read back afterwards.

## Scale, for orientation

Five Shorts on three platforms is fifteen creates a week. Run weekly for six weeks, ninety-three creates had one refusal, the missing render setting on the first run.
