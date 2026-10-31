# Security

Skills are instructions that AI agents execute with access to the reader's own systems: CRM, inbox, calendar, documents. Every submission is read by a maintainer for exfiltration, embedded secrets, instruction-override text, and unconfirmed destructive actions before it is merged. The full list of hard rejections is in [CONTRIBUTING.md](CONTRIBUTING.md#safety-what-is-rejected-outright).

## Reporting a problem

If a published skill does something it shouldn't, or you've found a way to get one past review:

- Open a [private security advisory](https://github.com/agiea-brain/agency-skills/security/advisories/new) on this repository.

Please don't file a public issue for security problems. A skill confirmed to be harmful is removed from the library and from everything that syncs from it, then the advisory is closed with a note.
