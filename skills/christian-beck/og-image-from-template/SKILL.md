---
name: og-image-from-template
title: OG image from template
description: |
  Use this skill when a post, page or case study is about to ship and it needs
  a social share image, and the firm already has a Figma template for them.
  Produces an exported OG image at the right dimensions, named and placed for
  the page's meta tags, with the title set to fit rather than truncated. Also
  use for "make the OG image", "social card for this post", "the preview looks
  broken when I share the link", "og:image".
category: Marketing
tags: [og-image, social-sharing, design-ops, publishing]
tools: [figma]
---

Applies when a page is ready to publish and needs its share image. Produces one exported image, correctly sized and named, from the firm's existing template rather than a new design each time.

## The play

1. Open the firm's OG template in Figma and duplicate the frame. Never start from a blank frame. The template exists so that every share image looks like it came from the same company, and the second a one-off is designed, that stops being true.
2. Fill the template's named layers only: title, optional eyebrow or category, optional author. The layer names and what each accepts are in references/template-contract.md. Any layer not in that list is structure, not content, and is not touched.
3. Fit the title rather than truncating it. Count characters before pasting, and if it overruns, rewrite it shorter. An OG title is not the page title and does not have to match it. Character budgets per size are in references/template-contract.md.
4. Branch by what the page is:
   - Blog post or article: title plus category eyebrow. No author unless the firm's template includes one by default.
   - Case study: client name as the eyebrow, result as the title. The result is the thing worth sharing, not the client's name.
   - Landing or service page: the page's promise, not its heading. Headings are written for people already on the page.
   - Any page with a strong existing image: use it as the template's background layer at the template's own treatment, never raw. A raw photo behind white text fails on half of all feeds.
5. Export at 1200x630 as PNG, or JPG when the image is photographic and the PNG lands over 300KB. Dimensions, naming and the file-size ceiling are in references/export-settings.md.
6. Name the file after the page slug, not the title, and place it where the site expects images for that page type.
7. Check the render before shipping, not after. Paste the live URL into a share-preview checker and look at the actual card. The checklist for what to look at is in references/export-settings.md.

## What good looks like

- First thing I check that most people skip: the image at thumbnail size, which is how most people will see it. If the title is unreadable at 25% zoom, the design is wrong no matter how it looks in the editor.
- The mediocre version: the page's H1 pasted into the template at whatever length it happens to be, auto-shrunk to fit, exported at the wrong ratio, and never looked at again. It technically has an OG image.
- I know it is right when the card is legible at thumbnail size, the title is a sentence someone would click, and it is visibly from the same family as the last ten.
- Red flag: someone has detached the template instance to make something fit. That is a template problem to fix once, not a one-off to work around.

## Rules

- MUST duplicate the template frame. Never design a one-off.
- MUST fill only the named content layers.
- MUST rewrite an overlong title rather than shrink the text or truncate it.
- MUST export at 1200x630 and keep the file under 300KB.
- MUST look at the rendered card before the page ships.
- NEVER detach a template instance to make content fit.
- NEVER put text the template did not plan for into a frame, including logos, badges and dates.
