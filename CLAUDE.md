# AI-Powered Course Announcement & Messaging Tool

## IMPORTANT — Read before doing anything

When the user asks to draft, write, or send any message (email or Slack), you MUST call the `draft_message` tool from the `csee-messaging` MCP server. Do NOT write the message yourself from scratch.

## Phases (Agent Skills)

The practical course runs in phases. Each phase is a real Agent Skill under
`.claude/skills/` (e.g. `phase-01-acceptance`, `phase-02-events`). They activate
automatically based on the user's plain-language request — that skill tells you
which message type it is and which details to collect. When the user describes a
messaging task, follow the matching phase skill. To add a new phase, drop a new
folder under `.claude/skills/` (see README → "Adding a new phase").

## Slack workspace (FIXED — never ask)

The team always uses ONE Slack workspace:

- **Workspace:** CSEE — team ID `T07HDKSAE3C` (https://app.slack.com/client/T07HDKSAE3C)

Channels are given by the user as a plain name (e.g. `jst-ws-2526` / `#jst-ws-2526`); resolve it within this workspace.

The user's Slack token is bound to this workspace at login, so every post already
goes to the right workspace. **Never ask the user which workspace** — only ask for
the **channel** (e.g. `#jst-ws-2526`) or the **person** when that isn't specified.
When a user first authenticates, they must authorize THIS workspace (see README → Connect Slack).

## Workflow

1. If any required details are missing (Slack channel, location, agenda, etc.) — ask the user before calling the tool. The active phase skill lists what each message type needs.
2. Call `draft_message` with the full request including all details provided. Pass the matching `phase` (the skill's folder name, e.g. `phase-01-acceptance`) so only that phase's templates are loaded.
3. Show the result to the user.
4. Ask: "Send this?" — if yes:
   - **Email** → call `send_email` from the `csee-messaging` MCP server (sends to recipients in `recipients_email.txt`)
   - **Slack** → use the `slack` MCP server tools (the official Slack connector) to post to the channel the request specifies. The workspace is fixed (see above) — never ask for it. If no channel/person is mentioned, ask only for the channel or person.
     - **If Slack is not connected yet** (the slack posting tools aren't available, or a call fails with an auth error), connect it depending on where you're running:
       - **Interactive terminal (`claude .`)** — tell the user to run `/mcp`, select **slack**, and complete the browser login. This is simpler than driving auth by hand: Claude Code captures the OAuth callback automatically, so there's no callback URL to copy-paste. After they confirm, continue and post the message automatically.
       - **Headless (non-interactive `claude -p`, where `/mcp` isn't available)** — fall back to driving auth yourself: call `mcp__slack__authenticate`, give the user the authorization URL it returns, ask them to open it and approve, then (if the redirect page errors) have them paste the `localhost` callback URL back and call `mcp__slack__complete_authentication` with it.
       - Either way, this browser approval is a one-time step — after it, never ask again.

## Tools available

**csee-messaging MCP server**
- `draft_message(request, phase?)` — drafts the message using CSEE templates and tone; pass the phase id to load only that phase's templates
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
- For Slack, the workspace is fixed — never ask which workspace. Only ask for the target channel or user if not specified in the request.
- If Slack needs authentication: in the interactive terminal, tell the user to run `/mcp` → select **slack** (Claude Code handles the OAuth callback automatically). Only in headless contexts where `/mcp` isn't available (e.g. a non-interactive `claude -p` run) fall back to driving `mcp__slack__authenticate` / `mcp__slack__complete_authentication` yourself. Either way it's a one-time browser approval — after it, continue automatically and never ask again.
