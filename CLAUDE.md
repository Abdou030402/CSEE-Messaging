# AI-Powered Course Announcement & Messaging Tool

## IMPORTANT — Read before doing anything

When the user asks to draft, write, or send any message (email or Slack), you MUST call the `draft_message` tool from the `csee-messaging` MCP server. Do NOT write the message yourself from scratch.

## Workflow

1. If any required details are missing (Slack channel, location, agenda, etc.) — ask the user before calling the tool.
2. Call `draft_message` with the full request including all details provided.
3. Show the result to the user.
4. Ask: "Send this?" — if yes:
   - **Email** → call `send_email` from the `csee-messaging` MCP server (sends to recipients in `recipients_email.txt`)
   - **Slack** → use the `slack` MCP server tools (the official Slack connector) to post to the channel the request specifies. If no target is mentioned, ask the user which channel or person to send to.

## Tools available

**csee-messaging MCP server**
- `draft_message(request)` — drafts the message using CSEE templates and tone
- `send_email(subject, message)` — sends to recipients in `recipients_email.txt`

**slack MCP server** — the official Slack MCP connector (remote, OAuth; posts as the authenticated user)
- Post messages to channels
- List channels
- Read channel history
- Look up users
- ...and more — use whichever tool the connector exposes that fits the request (do not assume exact tool names; discover them at runtime)

## Rules

- Never draft a CSEE message yourself. Always use `draft_message`.
- Never use placeholders. Ask for missing info first.
- Never ask who to send to for email. Recipients are in `recipients_email.txt`.
- For Slack, ask for the target channel or user if not specified in the request.
