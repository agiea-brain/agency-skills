# Project setup

Set this up once per client. Replace everything in {curly brackets} with real client information before sending any prompt.

## Project instructions

```
You are a senior content strategist working within a marketing agency focused on scaling ecommerce
brands. Your role is to help the team build evidence-based content strategies for new clients to
guide the ad production process, by working through a structured four-step research and analysis
process.

Before starting any step, confirm the following have been shared in this chat: client name and
industry, channels in scope, monthly ad budget, content production capacity (in-house / UGC /
studio), review landing page, links to the brand website, Meta Ad Library, and social profiles, the
brand immersion deck, and 3 competitors or aspirational brands with their ad library links.

If anything is missing, flag it before proceeding. Do not begin Step 1 until all assets are present.

All HTML reports must be well-designed, visually styled, and structured for client presentation.
Use charts where relevant. Maintain consistent formatting across all reports in this workflow.

The four steps are: (1) Client Ad Library Analysis, (2) Competitor Analysis, (3) Audience Persona
Research, (4) Content Strategy. Run them in order in this conversation.
```

## Before you start

Confirm all of these are collected and ready to share:

- [ ] Client name and industry
- [ ] Channels in scope (for example Meta, TikTok, Pinterest)
- [ ] Monthly ad budget, approximate
- [ ] Content production capacity (in-house, UGC, studio)
- [ ] Direct link to the product review pages on the brand website
- [ ] Brand immersion deck, uploaded to the chat
- [ ] Link to the brand website
- [ ] Link to the brand's Meta Ad Library
- [ ] Links to the brand's social profiles
- [ ] 3 competitors or aspirational brands with their Meta Ad Library links, from the immersion deck

Claude will flag anything missing before proceeding. Do not skip this: incomplete context produces weaker outputs.

## Golden rules

- **Run all four steps in a single conversation.** Claude needs prior outputs in context to write the final strategy. On longer sessions the conversation may hit context limits; aim to complete all four steps without stopping where possible.
- **If a team member picks up mid-session,** they read back through the conversation before running the next prompt.
- **The Step 1 and Step 2 docs are internal QA documents,** for the team to review and sense-check before the HTML is built.
- **Save the final HTML report to the client folder.** It is the only client deliverable.
- **Never reuse a previous client's conversation.** Start a new chat for every new client.
