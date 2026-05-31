---
name: phase-01-acceptance
description: >-
  Phase 1 of a CSEE practical course — Acceptance & Onboarding. Use this when a
  team lead wants to (a) tell students they have been ACCEPTED into the course
  (acceptance email), or (b) WELCOME a new team member on Slack and send them the
  Fellowship CONTRACT folder. Triggers on requests like "send the acceptance
  email", "tell the students they got in", "welcome the new students", "send the
  contract message", "onboard the new team member".
---

# Phase 1 — Acceptance & Onboarding

This is the first phase of the practical course: students have been selected, and
the team lead now confirms their spot and onboards them.

## Messages in this phase

### 1. Acceptance Email (channel: Email)
Congratulates accepted students and tells them how to confirm their spot.
Collect these details before drafting (ask the user for any that are missing):
- `course_name` (e.g. JST — JavaScript Technology)
- `semester` (e.g. winter semester 2025/26)
- `confirmation_deadline` (exact date + time, e.g. Saturday, Oct 5th, 23:59)
- `drop_deadline` (exact date + time)
- `slack_invite_link`
- `applicant_count` (optional — used for the "stood out among X applicants" line)

### 2. Slack Welcome + Contract (channel: Slack)
Welcomes a new fellow/team member and points them to their contract folder.
Collect these details:
- `first_name` of the recipient
- `batch_name` (e.g. Batch 1 – Summer 2026)
- `folder_link` (the contract folder)
- `translation_link` (English translation of the contract)
- `deadline` (when they should finish the steps)

## How to act

1. Figure out which of the two messages above the user wants.
2. Ask the user for any required detail that is missing — never invent or use placeholders.
3. Call `draft_message` from the `csee-messaging` MCP server, passing `phase: "phase-01-acceptance"` plus the full request with every detail you collected.
4. Show the draft, then follow the normal send workflow in CLAUDE.md (confirm, then `send_email` for email / the slack connector for Slack).
