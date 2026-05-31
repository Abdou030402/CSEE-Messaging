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

The repo ships with ready-to-edit example recipient lists (`recipients_email.txt`, `recipients_slack.txt`) — these are placeholder test data and will be replaced by a database lookup later. Just edit them in place:

- `recipients_email.txt` — the addresses emails go to (one per line).
- `recipients_slack.txt` — optional, for Slack DM lookups.

Set up your signature (gitignored, falls back to the committed example):
```bash
cp signature.example.txt signature.txt                 # your email signature
```
Edit `signature.txt` with your name/title/contact details (it's appended to every email). **Tip for testing:** put only your own address in `recipients_email.txt` first so you can verify end-to-end without emailing anyone else.

Optionally, drop your real past messages into `examples/historical_messages.md` (also gitignored) for better-matching drafts; otherwise the sanitized `examples/historical_messages.example.md` is used.

### 3. Connect Slack (official connector — OAuth, no tokens)

Slack is wired up in `.mcp.json` to the **official Slack MCP server** (`https://mcp.slack.com/mcp`). There are no apps to create, no bot tokens, and no environment variables to set — you just log in with your browser.

**The workspace is always the same one** — you never type or choose it when sending. Authorize this workspace, and only this one:

> **CSEE workspace** — team ID `T07HDKSAE3C` (open <https://app.slack.com/client/T07HDKSAE3C> to confirm you're authorizing this one).

Your login token is **bound to the workspace you pick at authorization**, and every later message automatically goes there — you only ever give a *channel* (e.g. `#jst-ws-2526`), never a workspace. **Tip:** sign into the CSEE workspace in your browser *before* authorizing, so the login completes straight to the right one.

**First time only, per workspace:** a Slack **workspace admin** must approve the Slack MCP integration for the workspace. (Slack Admin → Manage apps / Integrations → approve the Slack MCP server.) This is a one-time approval for the whole team.

**Each user:** authenticate your own account (next step covers this). Because it's your login, anything Claude posts goes out **as you**, and Claude can only see the channels you can.

### 4. Open the folder in Claude Code

```bash
claude .
```

Claude Code detects `.mcp.json` and prompts you to trust both the `csee-messaging` and `slack` servers — click **Allow** for both.

**You don't need to run `/mcp` or anything else to connect Slack.** The first time you ask Claude to send a Slack message, Claude detects that Slack isn't connected, starts the login for you, and hands you a one-time authorization link. Open it, approve in your browser, and Claude posts the message — and never asks again. (Approving in the browser is the one step that can't be automated: it's how you consent to Claude posting *as you*. After that the token is cached locally.)

> Prefer to connect up front instead of on first send? You still can — run `/mcp`, select **slack**, and complete the browser login. Either way it's a one-time step.

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

No slash command needed — plain language triggers everything (see "Phases & Skills" below).

Claude will:
1. Recognize which **course phase** your request belongs to (acceptance, events, …) and load that phase's knowledge
2. Draft the message using CSEE templates and tone
3. Show it to you
4. Ask which channel or person to send to (for Slack), or confirm the recipient list (for email)
5. Send on confirmation

---

## Prototype web UI (demo)

A minimal browser frontend for showcasing the flow without the terminal. It runs Claude
headless behind a tiny Flask server — same MCP tools, same `CLAUDE.md`, same phase skills.

```bash
pip install -r requirements.txt   # installs flask
python app.py                     # then open http://localhost:5000
```

Type a request, optionally tick **"Actually send it"** (otherwise it just drafts), and hit
**Run**. The page shows the draft or a ✅ Done confirmation.

- It's a **one-shot** UI: Claude won't ask follow-up questions — it drafts with whatever
  details you give and omits the rest (no placeholders). Put all the details in the box.
- **Email** works out of the box (sends to `recipients_email.txt`). **Slack** sending needs
  the one-time browser authorization first — do it once in `claude .` (just ask to send any
  Slack message and approve the link); after that the cached token lets the web UI post too.
- The server uses `--dangerously-skip-permissions` so it can act without interactive prompts.
  It's meant for a **local demo on your own machine**, not public hosting.

---

## How it works

```
csee-messaging-skill/
├── .mcp.json                         # Registers both MCP servers with Claude Code
├── CLAUDE.md                         # Workflow instructions loaded into every Claude session
├── style_guide.md                    # Shared CSEE tone, rules & channel formatting (drafting system prompt)
├── mcp_server.py                     # Custom MCP server — exposes draft_message and send_email
├── draft_message.py                  # Calls Claude with CSEE system prompt to draft messages
├── send_email.py                     # Gmail SMTP sender (App Password)
├── recipients_email.txt              # Email recipient list (example test data; one per line)
├── recipients_slack.txt              # Slack DM lookup list (example test data)
├── .env.example                      # Gmail credentials template
├── examples/
│   └── historical_messages.example.md
└── .claude/
    ├── settings.json                 # Pre-approves MCP tool permissions
    └── skills/                       # One Agent Skill per course phase (auto-selected by Claude)
        ├── phase-01-acceptance/
        │   ├── SKILL.md              #   trigger + what to collect for this phase
        │   └── templates/            #   acceptance_email.md, slack_welcome_contract.md
        └── phase-02-events/
            ├── SKILL.md
            └── templates/            #   event_invitation_email.md
```

**Two MCP servers run side by side:**
- `csee-messaging` — your custom server. Handles `draft_message` (CSEE tone + templates via Claude) and `send_email` (Gmail SMTP, sends from your account to `recipients_email.txt`).
- `slack` — the **official Slack MCP connector** (remote, OAuth). Gives Claude access to your Slack workspace as your own account: post to channels, read messages, look up users, and more. No tokens to manage.

### Phases & Skills

The practical course runs in **phases**, and each phase is a real **Claude Agent Skill** under `.claude/skills/`. A skill is a folder with a `SKILL.md` whose `description` tells Claude *when* to use it. Claude reads those descriptions automatically and, from your plain-language request, picks the matching phase — no slash command, no manual selection.

- **`.claude/skills/<phase>/SKILL.md`** — the phase "brain": what messages exist in this phase, what details to collect, and the instruction to call `draft_message` with that phase id.
- **`.claude/skills/<phase>/templates/`** — that phase's message templates.
- **`style_guide.md`** — shared CSEE voice + email/Slack formatting, loaded for *every* draft.
- **`draft_message(request, phase)`** — loads only the named phase's templates, so context stays small as phases grow.

> Note: `SKILL.md` under `.claude/skills/<phase>/` is a real Claude Code Agent Skill. The top-level `style_guide.md` is **not** a skill — it's a plain content file the MCP server injects into the drafting prompt. (It used to be named `SKILL.md`, which was misleading.)

### Why the official Slack connector but App Password for email?

We deliberately use the **official Slack connector** (OAuth, posts as you, one-command setup) but kept the **Gmail App Password** sender for email. The official Gmail connector is *draft-only* (it cannot actually send — you'd have to open Gmail and hit send yourself) and requires every user to create their own Google Cloud OAuth client. The App Password path actually sends, sends from each person's own account, and is the simplest possible per-user setup (generate one token, paste it in `.env`). See the meeting-notes / decision summary for the full rationale.

---

## Adding a new phase

Each phase is self-contained — adding one is just dropping in a folder, no code changes:

1. Create `.claude/skills/phase-NN-name/SKILL.md` with YAML frontmatter:
   ```yaml
   ---
   name: phase-NN-name
   description: >-
     When to use this phase — list the messages it covers and example phrases
     a team lead would type. Claude uses this to auto-select the phase.
   ---
   ```
   In the body, list the message types, the details to collect for each, and tell Claude to call `draft_message` with `phase: "phase-NN-name"`.
2. Add that phase's templates under `.claude/skills/phase-NN-name/templates/*.md`.
3. (Optional) Add the message type to `style_guide.md` if it needs special tone/formatting rules.

That's it — `draft_message` discovers the templates by phase folder automatically.

## Adding a new message type to an existing phase

1. Add a `.md` template under that phase's `templates/` folder.
2. Mention it in that phase's `SKILL.md` (what it is + what to collect).
