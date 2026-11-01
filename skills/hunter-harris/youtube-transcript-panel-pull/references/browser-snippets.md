# Browser snippets

Run these in the page with the agent's JavaScript tool. YouTube changes its markup from time to time. If a selector returns nothing, inspect the page and update it rather than falling back to the caption endpoint.

## Collect video IDs from a channel's Videos tab

Scroll to the bottom first if the channel has more videos than the first screen loads.

```js
[...new Set([...document.querySelectorAll('a[href*="/watch?v="]')]
  .map(a => a.href.match(/v=([\w-]{11})/)?.[1]).filter(Boolean))]
```

## Open the transcript panel

```js
document.querySelector('video')?.pause();
document.querySelector('tp-yt-paper-button#expand')?.click();
document.querySelector('ytd-video-description-transcript-section-renderer button')?.click();
```

## Read the rows and copy them

Wait a few seconds after opening the panel.

```js
const rows = [...document.querySelectorAll('transcript-segment-view-model')].map(e => {
  const ts = e.querySelector('[class*=Timestamp]')?.textContent.trim();
  const tx = e.querySelector('span[role=text]')?.textContent.replace(/\s+/g, ' ').trim();
  return `[${ts}] ${tx}`;
});
const ta = document.createElement('textarea');
ta.value = rows.join('\n');
document.body.appendChild(ta);
ta.select();
document.execCommand('copy');
ta.remove();
rows.length;
```

`navigator.clipboard.writeText` is often refused in an agent-driven browser because the page doesn't have focus. The textarea route works there.

On a Mac, write the file with `pbpaste > <video-id>.txt`. Elsewhere, use the platform's paste command, or have the agent return the text in chunks and write it.

## File header

```
YouTube transcript
Video ID: <id>
Title: <title>
Language: <from the panel's language menu>
Captions: auto-generated | creator-provided

[0:00] ...
```

## Failure signs

| You see | It means | Do |
|---|---|---|
| `rows.length` is 0 | the panel hasn't rendered | wait 3 to 5 seconds and rerun |
| no transcript button | description not expanded, or the video has no captions | expand and retry once, then record "no captions" |
| a few rows with chapter titles | you read the chapters list | check the selector is `transcript-segment-view-model` |
| caption URL returns an empty body | the endpoint needs a token | use the panel |
