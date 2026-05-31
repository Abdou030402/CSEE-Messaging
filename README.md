# AI-Powered Course Announcement & Messaging Tool

AI-powered tool for drafting and sending CSEE course announcements, emails, and Slack messages — integrated directly into Claude Code via MCP.

Claude drafts messages using CSEE templates and tone, then sends them via Gmail (SMTP) or directly to any Slack channel using the **official Slack MCP connector**. Each teammate authenticates their own Slack account, so messages post **as them**.

---

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Python 3.9+
- A Gmail account with 2-Step Verification enabled
- A Slack workspace where the **Slack MCP integration has been approved by a workspace admin** (one-time, see step 3)

---

## Setup (one-time, ~5 minutes)

### 1. Clone and install Python dependencies

```bash
git clone <repo-url>
cd csee-messaging-skill
pip install -r requirements.txt
```

### 2. Configure Gmail (email sending)

You need a Gmail App Password — a one-time token that lets the tool send email from **your** account without using your real password. No Google Cloud project, no OAuth setup.

1. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select **Mail** and your device, then click **Generate**
3. Copy the 16-character password shown

Then set up your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```
GMAIL_SENDER=you@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

Then create your recipient list from the committed example (the real files are gitignored):
```bash
cp recipients_email.example.txt recipients_email.txt
cp recipients_slack.example.txt recipients_slack.txt   # optional, for Slack DM lookups
cp signature.example.txt signature.txt                 # your email signature
```
Edit `recipients_email.txt` with the addresses you want to send to, and `signature.txt` with your name/title/contact details (it's appended to every email). **Tip for testing:** put only your own address in `recipients_email.txt` first so you can verify end-to-end without emailing the real list.

Optionally, drop your real past messages into `examples/historical_messages.md` (also gitignored) for better-matching drafts; otherwise the sanitized `examples/historical_messages.example.md` is used.

### 3. Connect Slack (official connector — OAuth, no tokens)

Slack is wired up in `.mcp.json` to the **official Slack MCP server** (`https://mcp.slack.com/mcp`). There are no apps to create, no bot tokens, and no environment variables to set — you just log in with your browser.

**First time only, per workspace:** a Slack **workspace admin** must approve the Slack MCP integration for the workspace. (Slack Admin → Manage apps / Integrations → approve the Slack MCP server.) This is a one-time approval for the whole team.

**Each user:** authenticate your own account (next step covers this). Because it's your login, anything Claude posts goes out **as you**, and Claude can only see the channels you can.

### 4. Open the folder in Claude Code and authenticate

```bash
claude .
```

Claude Code detects `.mcp.json` and prompts you to trust both the `csee-messaging` and `slack` servers — click **Allow** for both.

Then authenticate Slack:

```
/mcp
```

Select **slack** and complete the browser login. That's it — you're connected.

> The first time you run `/mcp` it opens Slack's OAuth page in your browser. Approve, and the token is stored locally by Claude Code. You won't need to repeat this.

---

## Usage

Just describe what you want in plain English:

```
draft an acceptance email for JST WS 2025/26, confirmation deadline Oct 5th 23:59, drop deadline Oct 13th 23:59, slack link https://...
```
```
send a slack message to #jst-ws-2526 reminding about the contract deadline this Sunday 23:59
```
```
post to #announcements that the JST kickoff is on June 3rd at 18:00 in room MI 01.09.014
```
```
/draft event invitation for the JST kickoff on June 3rd at 18:00 in room MI 01.09.014
```

Claude will:
1. Draft the message using CSEE templates and tone
2. Show it to you
3. Ask which channel or person to send to (for Slack), or confirm the recipient list (for email)
4. Send on confirmation

---

## How it works

```
csee-messaging-skill/
├── .mcp.json                         # Registers both MCP servers with Claude Code
├── CLAUDE.md                         # Workflow instructions loaded into every Claude session
├── SKILL.md                          # CSEE tone, rules, and message types (system prompt)
├── mcp_server.py                     # Custom MCP server — exposes draft_message and send_email
├── draft_message.py                  # Calls Claude with CSEE system prompt to draft messages
├── send_email.py                     # Gmail SMTP sender (App Password)
├── recipients_email.txt              # Email recipient list (one per line)
├── .env.example                      # Gmail credentials template
├── templates/
│   ├── acceptance_email.md
│   ├── event_invitation_email.md
│   └── slack_welcome_contract.md
├── examples/
│   └── historical_messages.md
└── .claude/
    ├── settings.json                 # Pre-approves MCP tool permissions
    └── commands/
        └── draft.md                  # /draft slash command
```

**Two MCP servers run side by side:**
- `csee-messaging` — your custom server. Handles `draft_message` (CSEE tone + templates via Claude) and `send_email` (Gmail SMTP, sends from your account to `recipients_email.txt`).
- `slack` — the **official Slack MCP connector** (remote, OAuth). Gives Claude access to your Slack workspace as your own account: post to channels, read messages, look up users, and more. No tokens to manage.

### Why the official Slack connector but App Password for email?

We deliberately use the **official Slack connector** (OAuth, posts as you, one-command setup) but kept the **Gmail App Password** sender for email. The official Gmail connector is *draft-only* (it cannot actually send — you'd have to open Gmail and hit send yourself) and requires every user to create their own Google Cloud OAuth client. The App Password path actually sends, sends from each person's own account, and is the simplest possible per-user setup (generate one token, paste it in `.env`). See the meeting-notes / decision summary for the full rationale.

---

## Adding new templates

1. Add a `.md` file in `templates/`
2. Add the message type to `SKILL.md`
3. Load it in `draft_message.py` inside `SYSTEM_PROMPT`
