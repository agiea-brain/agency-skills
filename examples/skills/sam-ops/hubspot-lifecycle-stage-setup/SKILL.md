---
name: hubspot-lifecycle-stage-setup
title: HubSpot lifecycle stage setup
description: |
  Use this skill when configuring lifecycle stages in HubSpot for a new or
  migrated portal. Produces a stage map, automation rules, and the reporting
  properties that make funnel reports trustworthy.
category: Implementation
tags: [crm, lifecycle, funnel]
tools: [hubspot]
---

Applies when a HubSpot portal needs lifecycle stages defined or repaired. Produces a stage map and automation plan.

## The play

1. List every stage currently in use and who moves contacts between them.
2. Collapse to the default HubSpot stages unless the team has a documented reason not to.
3. Define the one property that triggers each forward move; forbid backward moves by automation.

## What good looks like

- The best implementer asks who owns each stage before touching settings.
- The mediocre version adds custom stages nobody reports on.
- Good output lets the funnel report reconcile with the pipeline total.

## Rules

- MUST document the trigger property for every stage.
- NEVER automate a backward stage move.
