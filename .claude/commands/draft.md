---
name: draft
description: Draft and send a CSEE message. Usage: /draft <your request>
---

Use the `draft_message` tool from the csee-messaging MCP server with the user's request: $ARGUMENTS

After showing the draft, ask if they want to send it. If yes:
- Email → call `send_email` from the csee-messaging MCP server
- Slack → use the slack MCP server (the official Slack connector) to post. Ask which channel or person to target if not specified.
