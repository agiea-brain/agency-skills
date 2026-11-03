---
name: ad-creative-content-strategy
title: Ad creative content strategy
description: |
  Use this skill when onboarding a new ecommerce client and the ad production
  team needs an evidence-based content strategy before anything gets shot.
  Produces internal ad library and competitor analyses, review-based audience
  personas, tone of voice and key messages, and a client-ready HTML strategy
  report with content pillars, hooks, funnel mapping and a testing framework.
  Also use for "content strategy for a new client", "analyse their ad
  library", "competitor ad analysis", "build personas from reviews", "creative
  strategy for Meta".
category: Marketing
tags: [content-strategy, paid-social, ad-creative, ecommerce, personas, onboarding]
tools: [meta-ads]
---

Applies at the start of a new ecommerce engagement, before ad production begins. Produces two internal analyses for review and one client deliverable: an HTML content strategy report.

## The play

1. Set up a Claude Project with the instructions in references/project-setup.md. Start a new chat for every new client. Never reuse a previous client's conversation.
2. Collect the assets before anything runs: client name and industry, channels in scope, monthly ad budget, production capacity (in-house, UGC or studio), the product review pages, the brand immersion deck, the website, the brand's Meta Ad Library, social profiles, and three competitors or aspirational brands with their ad library links. The full checklist is in references/project-setup.md. Claude flags anything missing before Step 1.
3. **Step 1, client ad library analysis.** Formats, partnership versus brand ads, repeated messaging, apparent personas, the longest-running ads, creative velocity, and a gap analysis comparing what the brand says it stands for against what is actually in its ads. Internal doc. Prompt and the no-active-ads alternate are in references/research-prompts.md.
4. **Step 2, competitor analysis.** The same framework across three competitor or aspirational ad libraries, ending with what the client can use strategically. Internal doc. Prompt in references/research-prompts.md.
5. **Step 3, audience persona research.** Scrape the brand's own product reviews, extract and rank personas with verbatim hook quotes, compare the real audience against the one the brand thinks it has, then define tone of voice and key messages. Four parts, in references/persona-and-voice-prompts.md.
6. **Step 4, content strategy.** Synthesise everything into a styled HTML report: content pillars mapped to personas, three hooks per pillar across varied hook types, funnel mapping across four stages, and a testing framework sized to the budget and production capacity. Prompt in references/strategy-prompt.md.

Run all four steps in one conversation, since the strategy needs every prior output in context. If someone picks up mid-session, they read back through the conversation before running the next prompt.

## What good looks like

- First thing I check that most people skip: the gap between what the brand says it stands for and what is actually running in its ads. The immersion deck says one thing; the ad library usually says another.
- The second is who the reviews say the audience is, compared with who the brand thinks it is. The personas come from real customer reviews, not from the brief, and the verbatim quotes become the hooks.
- The mediocre version defaults to solution-based hooks only. Every pillar gets three hooks across varied types: problem-first, pattern interrupt, contrarian, before and after, comment format, fear-based, future-self.
- I know the strategy is right when every content pillar and key message maps back to a named persona, and the testing framework fits what the client can actually produce and spend.
- Personas describe an actual audience type, like a skin-conscious millennial or a clean beauty buyer, never a funnel stage or a content format.

## Rules

- MUST collect all assets before Step 1.
- MUST keep the Step 1 and Step 2 docs internal. They are QA documents, not client deliverables.
- MUST build personas from the brand's own reviews, and note how many reviews were used.
- MUST note clearly wherever findings are inferred from organic content rather than paid ads.
- MUST source language guidelines from the brand immersion deck.
- MUST make the HTML report match the brand's look and feel. It is the only client deliverable.
- NEVER reuse a previous client's conversation.
