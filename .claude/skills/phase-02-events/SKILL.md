---
name: phase-02-events
description: >-
  Phase 2 of a CSEE practical course — Events & Kickoffs. Use this when a team
  lead wants to INVITE participants to an event: a kickoff, workshop, demo day,
  or presentation. Triggers on requests like "invite everyone to the kickoff",
  "send a demo day invitation", "announce the workshop on ...", "event invitation
  for ...".
---

# Phase 2 — Events & Kickoffs

Once students are onboarded, the team lead invites them to the live events of the
course (kickoff, workshops, demo day, final presentations).

## Messages in this phase

### Event Invitation Email (channel: Email)
Invites all participants to an event with the practical details and agenda.
Collect these details before drafting (ask the user for any that are missing):
- `event_name` (e.g. JST & TPL Demo Day)
- `date` (full date, e.g. Friday, February 7th, 2026)
- `time` (start and, if known, end time + timezone)
- `location` and `location_link` (maps link)
- `agenda_items` (the schedule / what will happen)
- `participation_note` (optional — e.g. "on-site, mandatory")
- `closing_note` (optional — e.g. after-party info)

## How to act

1. Confirm this is an event invitation.
2. Ask the user for any required detail that is missing — never invent or use placeholders.
3. Call `draft_message` from the `csee-messaging` MCP server, passing `phase: "phase-02-events"` plus the full request with every detail you collected.
4. Show the draft, then follow the normal send workflow in CLAUDE.md (confirm, then `send_email` for email / the slack connector for Slack).
